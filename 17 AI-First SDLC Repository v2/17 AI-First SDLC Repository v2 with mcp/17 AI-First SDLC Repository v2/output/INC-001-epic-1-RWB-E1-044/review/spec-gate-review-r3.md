# Spec gate review, round 3: RWB-E1-044 (INC-001-epic-1-RWB-E1-044)

| Field | Value |
|---|---|
| Review type | SPEC GATE (specification stage), round 3 (re-review after remediation) |
| Story | RWB-E1-044 (Jira `TB0001-1205`, epic `TB0001-1162`) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-10 |
| Round 1 | `output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review.md`: FAIL, Medium -001, -002; Low -003..-010 (all closed in round 2) |
| Round 2 | `output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review-r2.md`: FAIL, Low only -011..-015 |
| Artifacts reviewed | `specify/spec.md`, `specify/compliance-validation.md`, `specify/agent-run-log.md`, `specify/contracts/backend-apis.json`, `specify/contracts/frontend-integrations.json` (both parse as JSON); `docs/increments/INC-001-epic-1-RWB-E1-044.md`; `docs/open-items.md`; `docs/decisions/INC-001-decisions.md` D-RCV-03, -17, -18, -28, -44..-47, OPEN-003/-006/-014 rulings; `requirement/Traceability_Matrix.md` rows 126, 140, 337 (gate-status text not assessed, per instruction) |
| Sources | Story file v5 (`RWB E1 044 ... v1.md`); `.github/contexts/backend-context.md` §13, `backend-standards.md` BS-2.3/BS-2.6; `.github/rules/specification-execution-gates.md` |
| ACE evidence (read-only) | `ace-monorepo` `develop` 9f450bbd. `git diff eedf5c75 9f450bbd` is empty for `application.yaml`, `AppConfig.java`, `SampleModuleConfig.java`, `backend/build.gradle.kts`, `ModulithTest.java`. `application.yaml`: core `spring.flyway` 71–77, `scb-aks` URL `currentSchema=ace` 224, `flyway.enabled: false` 244–245, `db-migrate` 276–303 with URL 295. `db/migration`: V001..V025, V025.1..V025.3, V026..V030, no duplicate version. `SampleModuleConfig`: no `schemas`/`defaultSchema`/`createSchemas`, **`baselineVersion("0")`, `baselineOnMigrate(true)`**. `db/migration-env/<env>/V001.001__grant_permission.sql`: `ALTER DEFAULT PRIVILEGES FOR ROLE "ACEDbFlywayRole_<ENV>" GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES` (and sequences) to `"ACEAppRole_<ENV>"`. |
| Tool evidence | Flyway 12.11.0 sources (`flyway-core`, Gradle cache) and `flyway-database-postgresql` 12.10.0 (the version ACE pins): `SchemaHistoryFactory.prepareSchemas` 61–93 (with no `schemas`/`defaultSchema` the current schema becomes the default schema and is added to the schema list); `Flyway.migrate` 195–235 (`createSchemas` → `DbSchemas.create`; "Found non-empty schema(s) ... but no schema history table" when the history table is missing, a listed schema is non-empty and `baselineOnMigrate` is false); `FlywayModel` 85 (`createSchemas` defaults to `true`); `PostgreSQLConnection.doGetCurrentSchema` 57–68 (falls back to `SHOW search_path` when `current_schema` is null). |
| Overall status | **FAIL** |
| Blocking | **YES**: High REVIEW-RWB-E1-044-016 and Medium REVIEW-RWB-E1-044-017. |

## Summary

The requested remediation is in place. D-RCV-47 is applied consistently across the spec, both contracts,
the card and the registers: schema `ace` from the connection, prefix `rwb_`, no `${recoverySchema}`, no
schema property, no DBA request. OPEN-020 is withdrawn, OPEN-014 is superseded and OPEN-025 is settled.
DEV is in scope with the same image digest. The runner fails fast when no recovery bean exists.
Round-2 findings -012..-015 are closed. -015 is tracked as OPEN-029.

Checking against Flyway's source found two defects that D-RCV-47 introduced. Both are in the Flyway
settings SPEC-003 keeps from the `recovery`-schema design:

- **High:** SPEC-003 sets `baselineOnMigrate(false)`. Schema `ace` already holds ACE core tables in DEV,
  SIT, UAT, PROD and on local PostgreSQL. The first recovery migrate therefore throws "Found non-empty
  schema(s) "ace" but no schema history table". This stops every recovery deployment and the local
  developer start. The sample module avoids this with `baselineVersion("0")` and `baselineOnMigrate(true)`.
  No specified test starts from a non-empty `ace`, so the test suite would not catch it.
- **Medium:** The spec says that leaving out `createSchemas` means Flyway "creates no schema". Flyway's
  default is `createSchemas=true`. If `currentSchema` names a missing schema, Flyway creates that schema
  and continues. That contradicts SPEC-002, T-044-03 and D-RCV-47's intent.

The fresh read also found four Low items:

- gaps in the `rwb_` lint rule set;
- the application account's DML on `rwb_` tables relies on ACE default privileges, and the spec does not say so;
- context files that contradict D-RCV-47 will be read by the next stage, this story's own plan;
- the run log and `compliance-validation.md` §4 do not record the 2026-11-10 remediation.

## Round 2 closure

| Finding | Severity | Closure | Evidence |
|---|---|---|---|
| REVIEW-RWB-E1-044-011 | Low | **CLOSED**, on condition that this round-3 result is written to the spec Status reporting block (`spec.md:255-258` still shows gate 2), `compliance-validation.md` §4 and the card's Compliance review row (`:159`). The pattern recurs in REVIEW-021. | Header status `spec.md:21` names gates 1–3 and the 2026-11-10 remediation. The card evidence row `:150` lists all three report paths. |
| REVIEW-RWB-E1-044-012 | Low | **CLOSED** | Card `:51` has a superseded note under the business outcome naming CLAR-001 A, D-RCV-44, OPEN-027, D-RCV-05 and D-RCV-47. Card `:90` has one under story authority naming CLAR-002 A, D-RCV-12, OPEN-019 and D-RCV-47. The main-flow note `:41` now covers D-RCV-47 and DEV. |
| REVIEW-RWB-E1-044-013 | Low | **CLOSED** | `spec.md:35`, `:87`, `:88`, `:158` SPEC-005 "Environments" (one image, same digest to DEV, SIT, UAT, PROD), `:220`; CLAR-007 `:234`; contract `migrationJob.environments` and `image`; `open-items.md:20` OPEN-019 lists DEV; `:38` OPEN-013 ruling extended to DEV. OPEN-020 no longer applies (withdrawn `:33`). |
| REVIEW-RWB-E1-044-014 | Low | **CLOSED** | SPEC-004 (a) `:157` limits the H2 skip to outside the migration job. SPEC-005 `:158` "Fail fast, no skip": the runner is not conditional on the bean and logs `MSG-P3-016` `object=recoveryFlyway` at ERROR, exit non-zero. X9 `:129`. Backend beans `:180`. T-044-12 `:207` adds the H2/no-bean case. Contract `missingBeanOrNonPostgres`. SPEC-018 `object` includes `recoveryFlyway`. |
| REVIEW-RWB-E1-044-015 | Low | **CLOSED** (deferred by the human, tracked) | `open-items.md:27` OPEN-029 (1) carries the D-RCV-44 run rule and OPEN-026 for TS-RCV-3 / backend-context §13 together with OPEN-022. Context files are unchanged, as instructed. See REVIEW-020 for the D-RCV-47 part's due date. |

Requested item 3 (OPEN-025): **done**. It is in the Settled table (`open-items.md:34`). The spec header
`:20`, T-044-14 `:210` and `compliance-validation.md:33` re-read ACE at 9f450bbd. Verified: the shared
files are unchanged and there is no duplicate core version.

Requested item 1 (D-RCV-47): **applied** in SPEC-001, -002, -004 (d), -005, -006, -007, -012, -018,
T-044-03, -05, -12, -15, CON-001/-002, the card, CLAR-005 and CLAR-007. The D-RCV-45 wording is
reinterpreted in `INC-001-decisions.md:83` and SPEC-004 (d). No `${recoverySchema}`, schema `recovery`,
schema property or DBA request remains as a requirement. The only remaining mentions are historical or
negative-fixture references: header `:19`, CLAR-005, T-044-05 `${recoverySchema}.rwb_x` (forbidden case),
and compliance-validation §4 history. The settings carried over unchanged are wrong for a shared,
non-empty schema: see REVIEW-016 and -017.

## New findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-E1-044-016 | **High** | `spec.md:156` SPEC-003 (`baselineOnMigrate(false)`); `:154` SPEC-001; contract CON-001 `settings.baselineOnMigrate: false`; T-044-01/-03/-12 (all start from an empty schema) | BR1, BR5, Flow 5–6; SPEC-001, -003, -005; D-RCV-47; FR-RWB-020 | Under D-RCV-47 the recovery bean sets no `schemas`, so Flyway's schema list is the connection's current schema `ace` (`SchemaHistoryFactory.prepareSchemas` 74–90). When `flyway_schema_history_recovery` does not yet exist and `ace` is non-empty, `Flyway.migrate` (Flyway 12.11.0, 205–232) throws `FlywayException` "Found non-empty schema(s) "ace" but no schema history table. Use baseline() or set baselineOnMigrate to true" unless `baselineOnMigrate` is true. `ace` holds ACE core tables in every real environment, and the core step runs first. The first recovery run (RWB-E1-042 `V0001`) therefore fails in DEV, SIT, UAT and PROD, and a local developer start on PostgreSQL fails at the recovery initializer. ACE's own pattern avoids this: `SampleModuleConfig` uses `baselineVersion("0")` + `baselineOnMigrate(true)` (backend-context CTX-TECH-BE-FW-03). The setting was safe with an empty, Flyway-only schema `recovery`; D-RCV-47 removed that premise. Every specified container test creates `ace` empty, so the suite would pass and the defect would first appear on deploy. | Recovery tech lead rules on the baseline setting, recorded as D-RCV-48: follow `SampleModuleConfig` with `baselineVersion("0")` and `baselineOnMigrate(true)`, so `V0001` and later are applied above baseline 0. State in SPEC-003 why this is safe: the history table missing on a non-empty `ace` only means "first recovery run". Update CON-001. Add a container test in which `ace` already holds a non-`rwb_` table (and a core-like `flyway_schema_history`) before the first recovery migrate. It asserts a baseline row at version 0, then `V0001` applied, and no non-`rwb_` object touched. Extend T-044-12 and T-044-15 to use such a pre-populated `ace`. |
| REVIEW-RWB-E1-044-017 | Medium | `spec.md:154` SPEC-001 ("no ... `createSchemas(...)` ... call ... so Flyway ... creates no schema"); `:155` SPEC-002 (missing schema "fails ... nothing is created"); `:198` T-044-03 (missing-schema case "creates nothing in any schema"); `:157` SPEC-004 (d), `:207` T-044-12, `:209` T-044-15 ("no schema created"); contract CON-001 `settings.schema`; `INC-001-decisions.md:85` D-RCV-47 "no `createSchemas`" | BR2; SPEC-001, -002; D-RCV-47 intent ("No DBA request for a schema", no schema of its own) | Flyway's `createSchemas` defaults to `true` (`FlywayModel` 85), and `Flyway.migrate` 195–196 calls `DbSchemas.create` for the schema list whenever it is true. Leaving the call out does **not** stop schema creation. When `currentSchema` names a schema that does not exist, PostgreSQL `current_schema` is null and Flyway takes the `search_path` value as the schema (`PostgreSQLConnection` 57–68). It then creates that schema, if the account has `CREATE` on the database, and migrates into it. That is the opposite of SPEC-002 and of T-044-03's expected result. A mistyped or missing `currentSchema` in an environment would create a stray schema. D-RCV-47's "no `createSchemas`" is ambiguous between "no call" and "no schema creation", and the spec read it as "no call". | Have the recovery tech lead clarify D-RCV-47 (or record it in D-RCV-48) as "`createSchemas(false)` set explicitly; Flyway never creates a schema". Change SPEC-001 and CON-001 to set `createSchemas(false)`, and correct the "creates no schema" rationale. Keep T-044-03's missing-schema case: with `createSchemas(false)`, Flyway warns and then fails creating the history table, so the migrate fails and creates nothing. Assert that no schema with the missing name exists afterwards. |
| REVIEW-RWB-E1-044-018 | Low | `spec.md:160` SPEC-007 (5); `:200` T-044-05; contract CON-002 `objectNames.appliesTo`, `acceptedGap` | Guardrail "no read of another module's tables"; D-RCV-47 (prefix on every table, sequence and index); BR2 | Since D-RCV-47, the prefix rule is the only automated guard against touching ACE core or other module objects in the shared schema. The listed positions miss table references that are neither checked nor listed as accepted gaps: `FROM` / `JOIN` / `USING` (for example `INSERT INTO rwb_x SELECT ... FROM efs_account`, which passes), `ALTER SEQUENCE` / `ALTER INDEX` targets other than `RENAME TO` (`ALTER SEQUENCE efs_seq RESTART` passes), `CREATE TRIGGER ... ON`, `CREATE POLICY / RULE ... ON`, `LOCK TABLE`, `GRANT/REVOKE ... ON [TABLE]`, `ALTER TABLE ... OWNER TO`. Unnamed indexes and implicit `serial`/identity sequences are not mentioned either; PostgreSQL derives their names from the `rwb_` table, so they pass correctly. The contract says `COMMENT ON` where the spec says `COMMENT ON TABLE/COLUMN`. | Either add these positions to rule (5) with T-044-05 fixtures (at least `FROM`/`JOIN`, `ALTER SEQUENCE/INDEX`, `CREATE TRIGGER ... ON`, `GRANT ... ON`), or list each one as an accepted gap left to code review in SPEC-007 and CON-002. State that unnamed indexes and implicit sequences are compliant by derivation. Align the `COMMENT ON` wording. |
| REVIEW-RWB-E1-044-019 | Low | `spec.md:65` §10 Authority, `:158` SPEC-005, `:182` Authorization ("no new grant"); `open-items.md:39` OPEN-014 (superseded, it had "the application account gets DML only") | §10 Authority; AGENTS.md least privilege; later recovery stories that read and write `rwb_` tables | With schema `recovery` gone, nothing in the spec says how the application account gets DML on new `rwb_` tables. In ACE this comes from `db/migration-env/<env>/V001.001__grant_permission.sql`: `ALTER DEFAULT PRIVILEGES FOR ROLE "ACEDbFlywayRole_<ENV>"` grants DML on tables and sequences created by that role. It holds only if the recovery Jenkins step creates objects as the same role as the core step. Nothing stops a recovery migration from adding its own `GRANT` with an environment-specific role name, which would break "same file in every environment". | State in SPEC-005 / Authorization that application-account DML on `rwb_` tables and sequences is inherited from ACE's existing default privileges for the migration-job role (cite the file), and that the recovery step must run as that same role (an input to OPEN-019). Forbid `GRANT`/`REVOKE` in recovery migrations: add them to the lint (with REVIEW-018) or to the guardrails. |
| REVIEW-RWB-E1-044-020 | Low | `open-items.md:27` OPEN-029 "Needed by: before the next recovery migration story is planned"; `.github/contexts/backend-standards.md:32` BS-2.3, `:35` BS-2.6; `backend-context.md` CTX-TECH-BE-FW-13 (`:260`) and 5 further `recoverySchema`/schema `recovery` mentions | D-RCV-47; CLAUDE.md "decision wins; report the conflict for Context Updater" | The next stage is `/planner` for this story. The Planner reads BS-2.3 ("Own schema `recovery` ... `${recoverySchema}`"), BS-2.6 and CTX-TECH-BE-FW-13 (`createSchemas(false)`, DBA creates `recovery`), which contradict D-RCV-47. OPEN-029's due date can be read as excluding RWB-E1-044 itself, so the plan may fall back to the old design. The conflict is reported (OPEN-029); only the timing is at fault. | Set OPEN-029 "Needed by" to "before `/planner INC-001-epic-1-RWB-E1-044`", or record in the card / spec header that the RWB-E1-044 plan follows D-RCV-47 over BS-2.3/BS-2.6/CTX-TECH-BE-FW-13 until OPEN-029 is done. Include in the context sync the baseline and `createSchemas` outcome of REVIEW-016/-017. |
| REVIEW-RWB-E1-044-021 | Low | `specify/agent-run-log.md` (last entry is spec gate 2, 2026-11-09); `compliance-validation.md:96` | traceability-standards; REVIEW-011 pattern | The run log has no entry for the 2026-11-10 work (D-RCV-47 applied, gate-2 -012..-014 fixed, -015 to OPEN-029, OPEN-025 settled, ACE re-read at 9f450bbd). `compliance-validation.md` §4 still ends "Open for human disposition: REVIEW-RWB-E1-044-012..015", although its own `:35` says -012..-014 are covered. | Add the 2026-11-10 remediation entry to the run log. Update §4 with a gate-2 remediation table (as for gate 1) and this round-3 result. |

## Checks with no finding

| Check | Result |
|---|---|
| Change Scope Declaration | NEW_STORY, UI NO, Logic YES, API NO / NO_API_CHANGE. Impacted nodes now name schema `ace` (shared, `rwb_`) and Jenkins in DEV..PROD. Contracts agree (`apiInScope: false`, `uiInScope: false`). |
| Requirement coverage | BR1–BR7, flows, §10, §12–§14, X-paths, guardrails, NFR-027 and the precondition each map to SPEC items. Only `DIRECT` / `INHERITED_EXISTING_BEHAVIOR` and `COVERED` are used; no BLOCKED rows. The BR2 and BR6 notes reflect D-RCV-47. |
| Unit Test Applicability | Frontend NO / NOT_APPLICABLE with evidence. Backend YES / REQUIRED / 80% lines, instructions, branches, methods; the scope includes test-scope tooling (D-RCV-43); `implementation-execution-gates.md` is referenced; the acceptance criteria include the D-RCV-44 evidence rule and T-044-15. Test additions from REVIEW-016/-017 fall inside the same scope. |
| SPEC to FR/NFR | SPEC-001..019 unique; each traces to FR-RWB-020 (plus FR-RWB-001 / NFR-RWB-006 where relevant). D-RCV-47 is added to the relevant rows. |
| Lint rules (1)–(4) vs D-RCV-47 | No schema qualifier of any kind (including `ace`, `public` and the old placeholder); only `information_schema`/`pg_catalog` reads; no schema statements; any `SET search_path` forbidden; dollar-quoted bodies scanned. This matches D-RCV-47 "no schema literal" and supersedes the OPEN-003 allowance correctly. Prefix rule gaps: REVIEW-018. |
| Flyway history-table location | With no `schemas`/`defaultSchema`, `flyway_schema_history_recovery` is created in the current schema `ace`, next to `flyway_schema_history` and `flyway_schema_history_samplemodule`, as SPEC-001 and BR6 state (verified in `prepareSchemas`). |
| X9 / runner fail-fast | Consistent across SPEC-004 (a), SPEC-005, X9, beans row, T-044-12 and the contract. |
| D-RCV-45 under D-RCV-47 | The reinterpretation is recorded in the register (`:83`) and SPEC-004 (d); T-044-15 asserts no history table and no `rwb_` object. (No schema creation holds only once REVIEW-017 is fixed.) |
| Schema comparator | SPEC-012 restricts to `rwb_` tables/sequences with their columns, constraints and indexes, and excludes the history table and non-`rwb_` objects. That is correct for a shared schema. |
| Clarification Log | CLAR-001..010 RESOLVED. CLAR-005 and CLAR-007 re-resolved by D-RCV-47 with date and decider. No OPEN items. |
| Registers | OPEN-020 withdrawn, OPEN-014/-006/-003 marked superseded, D-RCV-03/-17 and the schema parts of D-RCV-18/-28 marked superseded, OPEN-025 settled, OPEN-028 (ACE tech lead check of the sample-module pattern) and OPEN-029 added. IDs continue without reuse. |
| ACE footprint | `AppConfig`, `application.yaml`, `SampleModuleConfig`, security config untouched. `build.gradle.kts` test scope only (`excludeTags("e2e")` at 155–159 verified at 9f450bbd). New `application-db-migrate-recovery.yaml`. |
| Security, secrets, PII | No endpoint. `mainDataSource` is reused with managed identity. Synthetic fixtures only. No credentials, real data or production rows in any reviewed artefact. |
| Contracts | Valid JSON. CON-001 `activation` mirrors SPEC-004 (a)–(d) and SPEC-005 including DEV, image digest and fail-fast. CON-002 mirrors SPEC-006..-009 (except the wording in REVIEW-018). `frontend-integrations.json` matches UI NO. |
| Design evidence | `NOT_REQUIRED` with UI NO. |

## Gate result

```text
REVIEW_STATUS: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 1] [LOW: 4]
REVIEW_BLOCKING: YES (High REVIEW-RWB-E1-044-016; Medium REVIEW-RWB-E1-044-017)
ROUND_2_CLOSURE: -011 CLOSED (condition: round-3 result recorded in spec Status reporting, compliance-validation §4, card); -012, -013, -014 CLOSED; -015 CLOSED (deferred, tracked as OPEN-029)
NEW_FINDINGS: -016 High, -017 Medium, -018..-021 Low
NEXT_STEP: Recovery tech lead rules on the recovery Flyway baseline and schema-creation settings (D-RCV-48: baselineVersion("0") + baselineOnMigrate(true) as SampleModuleConfig; explicit createSchemas(false)); human re-runs /specify INC-001-epic-1-RWB-E1-044 to apply -016..-021 (or records explicit acceptance of the Low items), then the spec gate is re-run (round 4). Product Owner specification approval with OPEN-027 follows a non-blocking gate; /planner does not start until then.
```
