# Integration evidence: API contract, migration and cross-layer checks

Run `INC-003-epic-1-RWB-E1-042`.

**Container suite of record: tip `25c8f94`** — `./gradlew recoveryIntegrationTest` exit 0, 59 tests,
0 failures, 0 skipped: `ParameterConfigIT` 33 + `$FlagOff` 4, `ParameterMigrationIT` 4,
`RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6 (`../code-gate-fix/round2/it-full.log`). Unit and
coverage figures are in `../unit-tests/report.md` (388 tests; LINE 91.0 %, INSTRUCTION 90.7 %,
BRANCH 80.9 %, METHOD 95.8 %). Earlier container runs are superseded: `../backend/it.log` 46 tests,
`../review-fix/round2/it-full.log` 54 tests at `74e4ccb`, `../code-gate-fix/it-full.log` 55 tests at
`9056ed2`.

## 1. API contract

| Item | Result |
|---|---|
| OpenAPI file | `api/recovery-api-v4.yaml` **not edited** — `getAdminParameters` and the `Parameter` schema already exist (plan-time check 9). `frontend/src/api/schema.d.ts` not regenerated. |
| Operation implemented | `GET /api/recovery/v1/admin/parameters`, query `key` (prefix), `kind`, `owner`, `environment` (default `rwb.environment`), 200 `Parameter[]`, 401 MSG-P4-001, 403 MSG-P4-002, 503 status-only |
| Renderer | `CatalogParameterView` (`@JsonInclude(NON_NULL)`, `default` mapped from `defaultValue`); a secret omits `default`, `valueInForce`, `versionNo` and `validFrom`; a PRODUCT row omits the three value fields |
| Verified by | `ParameterCatalogControllerTest` (5 cases incl. the filters, the secret, the 403 with the action text and the status-only 503) and `ParameterConfigIT` (`prodContextReadsSeedVersionOne`, `secretIsListedWithoutValue`, `filtersByPrefixKindOwnerEnvironment`, `readWithoutTheRightIsRefused`) |
| Load operations | Served through `casewf.config.api.ParameterLoadHandler` and exposed by RWB-E1-043 (D-RUN-10, D-RUN-20); **no controller** is built here. Asserted through the interface at HTTP depth (message ID, status, placeholders, field, database state) in `ParameterConfigIT`. |
| Contract artefacts | `plan/contracts/backend-apis.json` and `plan/contracts/frontend-integrations.json` (frontend `NOT_APPLICABLE`) remain accurate: no delta was found while implementing. |

## 2. Migration

| Item | Result |
|---|---|
| File | `V0001__rwb_e1_042_parameter_catalog_and_seed.sql` (next free number in this branch; the orchestrator assigns the merge number, D-RUN-07) |
| Line 1 / line 2 | `-- Story: RWB-E1-042` / the header citing Physical Schema v6, D-RCV-28 and SPEC-001/-002/-006 |
| Qualifier | `${recoverySchema}` only; no `SET search_path`, no `GRANT`, no `REVOKE` |
| Applied on an empty schema | `ParameterMigrationIT#emptySchemaGetsTablesConstraintsIndexesAndSeed` — 22 + 19 v6 columns asserted one by one, all 16 constraints, all 4 indexes, 19 catalog rows, 40 value rows, the seed identity and audit columns |
| Applied on a Physical-Schema-v6 schema | `ParameterMigrationIT#physicalSchemaSixGetsTheAdditions` — the v6 column list is byte-identical before and after; only the three added columns, the constraints and the indexes appear |
| Drift | `ParameterMigrationIT#catalogTableEqualsTheGeneratedKeys` — `parameter_catalog` equals `ParameterKeys.all()` on every mirrored column; a fixture catalog with one changed default fails naming key and column |
| Lint | `RecoveryMigrationLintTest` green with the file (15 rules, identifier-only, quote-aware); the `used_by` and `COMMENT ON` text holds `recovery.` inside string literals by design |

## 3. Cross-layer checks

| Check | Result |
|---|---|
| Catalog file ↔ generated keys | `ParameterKeysGenerationTest#generatedKeysMatchTheCatalogFile` (every column, row for row) |
| Catalog file ↔ database | `ParameterMigrationIT#catalogTableEqualsTheGeneratedKeys` |
| Generated keys ↔ 40 seeded values | `ParameterMigrationIT#emptySchemaGetsTablesConstraintsIndexesAndSeed` (counts, `version_no 1`, `APPROVED`, seed identity) and the migration's self-check `DO` block |
| Service ↔ database | `ParameterConfigIT#eachEnvironmentResolvesItsOwnValue`, `#futureVersionStartsOnItsDate`, `#rollbackRestoresTheEarlierVersion` |
| Handler ↔ event ↔ cache | `ParameterConfigIT#approvalPublishesOneEventWithNoUserId`, `#rollbackRestoresTheEarlierVersion` (the GET right after the rollback returns the earlier value), `ParameterCacheTest#aRebuildAfterTheEventReReadsTheRows` |
| Recorder ↔ transaction | `ParameterConfigIT#recorderFailureLeavesRowsValidated` (rows stay `VALIDATED`, no approver, 503 MSG-P7-003) |
| Load idempotency ↔ approved rows (code-gate CODE-001) | `ParameterConfigIT#anApprovedLoadRepeatsInsteadOfBeingRefused` (same `loadId`, `repeat=true`, `APPROVED`, one row); `#conflictingContentIsRefused` (a different load still 409 `MSG-P3-027`) |
| Module boundaries | `RecoveryBoundaryTest`, `ModulithTest` (no P1/P2/P4 → P3 edge; `config.api` published) |
| Guardrails | no UUID literal outside tests; `password` only as a key or property name; one migration; no new dependency; no file under `frontend/`, `api/`, `infra/`, `scripts/` changed |
