---
title: "Implementation Plan: RWB-E1-001 Recovery tables for the 14 data products"
run_id: "INC-009-epic-1-RWB-E1-001"
story: "RWB-E1-001"
epic: "EPIC-001"
status: "SUCCESS (planning complete; two Blocker = Yes document gaps carried, human ruling required before the merge of the migration)"
revision: "v1 (18 Nov 2026): first plan for spec revision 4 (spec gate round 4 PASS, 0 Critical / 0 High / 0 Medium / 0 Low). No human approval is claimed; GAP-E1001-17 and GAP-E1001-18 stay Blocker = Yes on ASM-E1001-13 / ASM-E1001-14"
prepared: "2026-11-18"
---

# Implementation Plan: RWB-E1-001 Recovery tables for the 14 data products

Design Source: **NOT_APPLICABLE** — UI In Scope NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE]
[SCREENS: 0]` in `../specify/spec.md`. No screen task, no `plan/frontend/components.md`.

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` revision 4. Spec gate round 4: `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-4.md`). `REQUIREMENT_COVERAGE_RESULT: FAILURE [TOTAL_RULES: 33] [COVERED_RULES: 32] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 2]`; the 2 contradictions are `GAP-E1001-17` and `GAP-E1001-18`, both Blocker = Yes and carried on labelled assumptions (§ "Blocker carry-forward") |
| Carried inputs | RWB-TE-001 plan v7 (module homes, package-private records, `ApplicationYamlEnvironment`, `RecoveryBoundaryTest`), RWB-E1-044 plan v2 (`RecoveryFlywayConfig`, `RecoveryMigrationRunner`, lint T-044-21, migration folder), RWB-E1-042 plan v2 (`casewf.config.api`, `access.api`, `FixedMessageCatalog`, `parameter_catalog`/`parameter_value`, `config/parameter-catalog.csv`), RWB-E1-043 plan v1 and spec revision 10 (P4 `access.api.ReferenceTableHandler` SPI, registry, endpoint, rights, audit, 38 catalog rows) |
| Code base | This repository read on 18 Nov 2026. It is the pre-RWB-TE-001 layout (`recovery/platform`, `rules`, `workflow`, `documents`; migration folder holds `README.md` only). The plan targets the post-TE-001 homes the spec names; TASK-00 checks PRE-1..PRE-4 before any file is written. No Gradle, Docker, git or network command was run at plan time |
| Builder | Implementation Builder, its own git worktree on `feature/RWB-E1-001-recovery-schema` from `develop-recovery`; commits `RWB-E1-001: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers |
| Smallest change | One migration; eight new P1 classes; one additive P4 message-catalog edit; two `parameter_catalog` rows in the CSV and the migration; one flag; the S1/S2/S3 local switches and the `RecoveryDatabaseIT` stage change; tests. No endpoint, request/response schema, dependency, Gradle task or frontend file |
| Migration | One file, `V<seq>__rwb_e1_001_recovery_schema.sql`; `<seq>` assigned at merge (D-RUN-07). Line 1 `-- Story: RWB-E1-001` |
| Module scope | One ACE module (recovery): P1 `dataengine.internal.catalog` (new), additive P4 `access.internal.FixedMessageCatalog`; P1 imports P4 `access.api` only; no `casewf` import (D-RUN-18, D-RUN-21) |

## Upstream readiness

| Check | Result |
|---|---|
| Spec status | Revision 4; the two Blocker = Yes gaps are carried on labelled assumptions; no human ruling is claimed |
| Spec gate | `PASS` round 4, 0 findings (`../review/spec-gate-review-4.md`); findings 025/026 resolved in revision 4; no earlier finding reopened |
| `REQUIREMENT_COVERAGE_RESULT` (spec) | `FAILURE` with `MISSING_RULES: 0`, `AMBIGUOUS_RULES: 0`, `CONTRADICTIONS: 2` — both are the blocker gaps; see § "Blocker carry-forward". No requirement row is `BLOCKED` in the spec's own Status vocabulary (BR3, BR7 and NFR-RWB-006 are `COVERED (ASM)`) |
| Clarification log | 13 rows: CLAR-001..-008, -010, -013 `RESOLVED`; CLAR-009 `OPEN (non-blocking)`; CLAR-011 and CLAR-012 `OPEN (Blocker = Yes gap 17 / 18)`. `CLARIFICATION_STATUS: RESOLVED_WITH_OPEN_ITEMS`. The two Blocker rows have resulting SPECs (004/006/018) and a labelled assumption each; no clarification decision is missing or contradictory |
| Design evidence | `NOT_REQUIRED`; UI In Scope NO; no effective screen, no `SCR-*` screen, no Figma link |
| Migration | One production file; `<seq>` not fixed (D-RUN-07) |
| Base dependency | RWB-TE-001 (order 2), RWB-E1-044 (order 1), RWB-E1-042 (order 3) and RWB-E1-043 (order 8) are **earlier stories**, not seams (D-RUN-08; Build Sequence v6 orders 1, 2, 3, 8, 9). Build Sequence v6 order 9 is this story |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 2] [UNBLOCK_ACTION: human ruling on GAP-E1001-17 and GAP-E1001-18 before the merge of this story's migration (OPEN-NEW-6, OPEN-NEW-7); CLAR-009 is non-blocking and does not stop planning]`.

Planning is complete: every in-scope `SPEC-*`, `AC*`, `BR*`, `TC-*`, `X*`, `CLAR-*` and NFR is mapped
to tasks and named tests. The two blocker items stop the **merge**, not the branch work (spec Status:
"it stops nothing earlier").

## Blocker carry-forward (read before build)

| Gap | What conflicts | Carried on | Effect on this plan | What clears it |
|---|---|---|---|---|
| `GAP-E1001-17` (Blocker = **Yes**) | Story v7 §13's DP07 system-of-record text is 139 characters; the story's own DDL, PS v6 line 820, DF-REF-074 and Logical Data Model and Data Dictionary v8 (`06-data/recovery-workbench-logical-data-model-and-data-dictionary-v8-xlsx.md`, line 561) say `varchar(120)` | `ASM-E1001-13`: text verbatim, column and DF-REF-074 `varchar(200)` | TASK-03 creates `varchar(200)`; TASK-01/02 test the seed fits and DP07 is 139; TASK-18 records that the widening is an assumption | A **human** ruling by the data architect, recorded as a decision (OPEN-NEW-6). A ruling that shortens DP07 instead reverts the column to `varchar(120)` and changes the seed text and DF-REF-074; the tests stay |
| `GAP-E1001-18` (Blocker = **Yes**) | PS v6 marks 18 fields personal; PDPA Inventory v4 marks 523 of 1,366 (17 Restricted), 9 of them `false` in PS v6; 26 PS-v6-only fields have no Inventory row | `ASM-E1001-14`: protective union, 526 `true`, literal in each `INSERT`, never an `UPDATE`; the 26 stay `false`; DF-REF-288/-289 named in the ask | TASK-03 seeds 526 literals; TASK-01/02 compare the set with the fixture and run the TE-011 lint (conditional); TASK-18 records the assumption | A **human** ruling by the data architect with the DPO (OPEN-NEW-7). A narrower set may only remove marks; the fixture and the seed change with the ruling, no code |

Neither gap is resolved, downgraded or converted into an approval by this plan, by a task, by
`shared-updates.md` or by the later plan gate. The two run decisions this story leans on (D-RUN-12,
D-RUN-21) are orchestrator (Claude Code, an AI agent) decisions, not human rulings; their ratification is
OPEN-050 and is not claimed. TASK-19 is the merge-readiness check: **it must fail the merge if the human
ruling record is absent**, whatever else is green.

## Base and dependency outputs (read, not rebuilt)

| Output | What this plan takes | Where applied |
|---|---|---|
| `aisdlc/output/INC-002-epic-1-RWB-TE-001/plan/plan.md` v7, `tasks.md`, `data-model.md` | Module map (P1 `dataengine` with `api` and `internal` package-info already exists), `RecoveryBoundaryTest`, `ModulithTest`, `ApplicationYamlEnvironment`, the combined JaCoCo bundle `recoveryClasses` + tooling packages, `T/testsupport` conventions | TASK-00, TASK-09, TASK-15 |
| `aisdlc/output/INC-001-epic-1-RWB-E1-044/plan/plan.md` v2, `tasks.md` | `casewf.migration.RecoveryFlywayConfig` and `RecoveryMigrationRunner`, the `${recoverySchema}` folder, the identifier-only quote-aware `RecoveryMigrationLintTest` (T-044-21), `migrationToolingClasses`, migration-folder `README.md` | TASK-00, TASK-03, TASK-13 |
| `aisdlc/output/INC-003-epic-1-RWB-E1-042/plan/plan.md` v2, `tasks.md`, `data-model.md` | `casewf.config.api` (`ParameterService`, `BusinessDateProvider`), `access.api` (`MessageResolver`, `ApiProblemException`, `ApiError`), `access.internal.FixedMessageCatalog` (nine IDs), `parameter_catalog` (22 columns) and `parameter_value` (19 + 3), `config/parameter-catalog.csv` (19 rows, 16-column header), `CatalogFileParser`, `CatalogCompletenessRules` | TASK-05, TASK-10, TASK-11, TASK-13, TASK-14 |
| `aisdlc/output/INC-008-epic-1-RWB-E1-043/plan/plan.md` v1, `tasks.md`; `../INC-008-epic-1-RWB-E1-043/specify/spec.md` revision 10 | P4 `access.api.ReferenceTableHandler` (+ `Dating`), `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport`, `RowCheckFailure`; the P3 registry, the two admin operations, rights, the interim `REFERENCE_LOAD_AUDIT` line, the 38 catalog rows, `reference_version`/`reference_row` | TASK-05, TASK-07, TASK-11, TASK-14 |
| `../specify/spec.md`, `contracts/*`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `evidence/*` | The 19 SPEC rows (011 retired), 33 requirement rows, 20 TC IDs, 13 CLAR rows, the 526-field list, the seed-length evidence | Whole plan |
| `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` and its repo copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`; `requirement/legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md`; `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md`, `d-rcv-36-temporal-and-drools.md` | Every table, column, constraint, index, trigger, comment and seed; D-RCV-28 (migration), D-RCV-29 (seed), D-RCV-35 U3/U4, D-RCV-36 row 18/T10 | TASK-03, TASK-05 |

## Plan-time checks (read only)

| # | Check | Result (18 Nov 2026) |
|---|---|---|
| 1 | Base layout | The checkout is **pre-TE-001**: `backend/src/main/java/th/co/scb/ace/demo/recovery/` holds `platform`, `rules`, `workflow`, `documents`. The plan uses the post-TE-001 homes from TE-001 plan v7; TASK-00 confirms PRE-1 before writing. |
| 2 | Migration folder | `backend/src/main/resources/db/modulemigration/recovery/` holds `README.md` only; no `.sql`, so no `<seq>` can be inferred. |
| 3 | `application.yaml` | `rwb.flyway.enabled: true` with no environment override; `rwb.schema: recovery`; `rwb.p3.temporal/drools` only. S3 adds `${RWB_FLYWAY_ENABLED:true}`. |
| 4 | `application-local.yaml` | No `rwb.p1` key; S3/flag add `rwb.p1.data-catalog: true`. |
| 5 | `.env.example` and `docker-compose.yml` | Both default `RWB_LOAD_REFERENCE_SCHEMA=true`; no `RWB_LOAD_REFERENCE_VIEWS`; the backend service lists `RWB_P3_TEMPORAL`/`RWB_P3_DROOLS` only. |
| 6 | `infra/postgres/init/10-load-ace-database.sh` | Loads PS v6 (tables **and** views) when S1=true, else creates schema + `pgcrypto`. No S2 branch. |
| 7 | `infra/postgres/init/20-grants.sql.inc` | `ALTER DEFAULT PRIVILEGES FOR ROLE rwb_migrator` already gives `recovery_svc` DML on Flyway-created tables and USAGE/SELECT on sequences. No change needed. |
| 8 | `backend/src/test/java/th/co/scb/ace/demo/recovery/RecoveryDatabaseIT.java` | Sets `RWB_LOAD_REFERENCE_SCHEMA=true` (line 42); asserts 30 `v_ace_*` views, 0 visible `public` tables, views read-only/`ace_view_owner`, the baseline row `version = '0'` (line 102), append-only `decision_log_entry`, identity split. Moves to S1=false, S2=true; every assertion kept. |
| 9 | Physical Schema v6 counts (read with a Python 3 parser) | 93 `CREATE TABLE`; 92 `ADD CONSTRAINT fk_`; 112 `CREATE [UNIQUE] INDEX`; 89 `COMMENT ON TABLE`; 1,026 `COMMENT ON COLUMN`; 123 `sys_objects`; 1,379 `sys_fields`; 598 `lov_value`; 54 `role`; 421 `permission`; 8 `rule_package`; 0 `delegation_limit`. On the 4 T8 tables: 4 table comments + 53 column comments = 57. All match the spec's counting table. |
| 10 | T8 FK/index | Only `fk_reference_row_version_id` and `ix_reference_row_version_id` touch the T8 tables; the four FKs from `retention_rule`, `document_type`, `document_checklist_item` and `document_hub_parameter` to `reference_version` are kept (target exists). |
| 11 | Story v7 §13 seed lengths | `../specify/evidence/pdpa_v4_vs_ps_v6-output.txt`: DP07 `system_of_record` = **139** (`varchar(120)` over), DP04 = 97, all other values fit. |
| 12 | `is_personal` union list | `../specify/evidence/is_personal_union_v4.tsv` = 2 comment lines + **526** field IDs (528 lines). |
| 13 | E1-043 live SPI (spec revision 10, "Reference load handler") | `ReferenceLoadFile(String tableCode, LocalDate validFrom, List<String> columns, List<Map<String,Object>> rows)`; `ValidationReport(List<RowCheckFailure>)`; `RowCheckFailure(int row, String column, String messageCode, Map<String,String> placeholders)`; `HandlerMessage(String messageCode, Map<String,String> placeholders)`; `Dating { DATED, CURRENT_STATE }`; defaults `keyColumns()`, `repeatMessage()`, `supportsRollback()` false, `onRolledBack`, `changeSummary()`, `dating()`. |
| 14 | E1-042 catalog | `config/parameter-catalog.csv` header has 16 columns (`key,kind,value_type,unit,min_value,max_value,default_value,scope,required,owner_role,environments,used_by,secret,value_source,env_property,description`); `used_by` is `;`-separated, each ≤ 100 characters; `value_source` and `env_property` are **CSV fields, not DB columns**. The completeness rule scans code → catalog (not catalog → code), so two rows with no Java reader pass. |
| 15 | TE-001 module map | P1 is `dataengine` with published `api`; `dataengine/api` and `dataengine/internal` `package-info.java` exist after TE-001. This story adds only the `internal/catalog` sub-package and publishes no type, so the map, `ModulithTest`, `RecoveryBoundaryTest` and `publishedSurfaceIsExactlyTheSpecifiedTypes` are unchanged. |
| 16 | Test commands | `scripts/dev.ps1 test` = Gradle `test` + `npm run check`; `it` = `recoveryIntegrationTest`; `e2e` = `e2eTest` + Playwright. Gradle needs `$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"`. |

No measured coverage or test result is claimed at plan time.

## Preconditions

Each is a stop-and-report checked by TASK-00 and recorded in `implement/backend/preflight.md`. A
precondition that is absent or different stops the build; the plan is not silently adapted.

| ID | Precondition | Proof in the merged base | If absent |
|---|---|---|---|
| PRE-1 | RWB-TE-001 is merged | P3 `casewf` homes; P4 `access.api`/`access.internal`; `T/testsupport/ApplicationYamlEnvironment.java`; `T/architecture/RecoveryBoundaryTest.java`; P1 `dataengine` with `api` and `internal`; old `platform`/`rules`/`workflow`/`documents` gone | stop, report PRE-1 |
| PRE-2 | RWB-E1-044 is merged | `R/casewf/migration/RecoveryFlywayConfig.java`, `RecoveryMigrationRunner.java`, `MigrationPropertiesConfig.java`; identifier-only quote-aware `RecoveryMigrationLintTest`; migration folder holds `README.md` only | stop, report PRE-2 |
| PRE-3 | RWB-E1-042 is merged | `casewf.config.api` types; `FixedMessageCatalog` with nine IDs; `config/parameter-catalog.csv` with 19 rows and the 16-column header; `parameter_catalog` and `parameter_value` migrations | stop, report PRE-3 |
| PRE-4 | RWB-E1-043 revision 10 is merged | P4 `access.api.ReferenceTableHandler` + five SPI records; the registry, `POST /admin/reference-loads` and `/{loadId}/approve`; `reference_version`/`reference_row` migrations; `REFERENCE_LOAD_AUDIT` line | stop, report PRE-4 |
| PRE-5 | Base gates green | `./gradlew test recoveryCoverageReport` exits 0 at the worktree base; the four bundle counters are recorded | stop, report PRE-5 |
| PRE-6 | **Human ruling on GAP-E1001-17 and GAP-E1001-18 is recorded** | A decision record naming the DP07 width and the `is_personal` set | **Not needed to write code**; TASK-19 forbids the merge without it. If the ruling differs from `ASM-E1001-13`/`-14`, the builder applies the ruling before merge and re-runs the affected tests |

D-RUN-07 (`<seq>` at merge), D-RUN-08 (seams), D-RUN-12 (one table owner), D-RUN-17 (earlier plans are
the base), D-RUN-18 (P4 SPI), D-RUN-21 (one-module reading) are orchestrator run decisions, not human
rulings; ratification is OPEN-050 and is not claimed.

## Scope

In scope; each bullet maps to tasks in `tasks.md`:

1. **S-1 Migration:** one `V<seq>__rwb_e1_001_recovery_schema.sql` with the 89 tables, 91 FKs, 111
   indexes, 3 CHECKs, 2 triggers, 85+973 comments, the dictionary seed, the 14 `data_product` rows and
   `v_data_dictionary` (SPEC-001..-008). → TASK-03
2. **S-2 Dictionary and `is_personal`:** 123 `sys_objects`; 1,379 + 3 `sys_fields`; the 526 literals;
   the 3 provisional rows; seed widths (SPEC-006, -018; ASM-E1001-13, -14, -17). → TASK-01, TASK-03
3. **S-3 Published view:** `v_data_dictionary` with the 20 columns of SPEC-005 and AC2's two rows
   (SPEC-005). → TASK-03, TASK-14
4. **S-4 Entity and repository:** `DataProduct`, `DataProductRepository`, `CatalogRole`,
   `CatalogRoleRepository` (SPEC-012). → TASK-07
5. **S-5 Handler checks K0–K5 and the F1–F3 grammar:** `validate`, `tableCode`, `keyColumns`,
   `repeatMessage`, `dating`, `supportsRollback`, `changeSummary`; the four message IDs EN/TH
   (SPEC-013, -015). → TASK-04, TASK-05, TASK-06, TASK-07
6. **S-6 Apply and idempotency:** one transaction, 14 rows by `product_code`, version +1,
   `valid_from`; repeat → 409 MSG-P1-011 (SPEC-014). → TASK-07, TASK-14
7. **S-7 Flag, registration and boundary:** `rwb.p1.data-catalog`; the bean is collected by the P4
   type; no `PARAMETER` bean; no module-map or published-surface change (SPEC-017, -019). → TASK-08,
   TASK-09
8. **S-8 Catalog rows:** two `parameter_catalog` rows in the CSV and the migration, one row shape; no
   `refdata.columns` and no LOV-REF-TABLE row (SPEC-019 item 5). → TASK-10, TASK-11
9. **S-9 Local switch:** S1 `false`, S2 new `true`, S3 `${RWB_FLYWAY_ENABLED:true}`; compose, env,
   init script, READMEs; `RecoveryDatabaseIT` moves to S1=false/S2=true; earlier-story ITs pinned or
   moved with no assertion removed (SPEC-010). → TASK-12, TASK-13, TASK-16
10. **S-10 Migration, conformance and seed evidence:** `RecoverySchemaMigrationIT`,
    `DataDictionaryConformanceTest`, `SeedIntegrityIT` (SPEC-007..-010, -018). → TASK-01, TASK-02,
    TASK-03, TASK-16
11. **S-11 API-level acceptance:** the 14-row load, approval, 422 refusals, 409 repeat, 403 and the
    audit line through the E1-043 endpoint (AC3, AC7–AC11, X8). → TASK-14
12. **S-12 Unit tests and the 80 % gate:** handler, grammar, apply, flag, messages, catalog rows,
    static seed derivation; `recoveryCoverageVerification` at 80 × 4 (SPEC-013..-019). → TASK-15
13. **S-13 Merge gate:** `./scripts/dev.ps1 test`, `it`, `e2e` (SPEC-008, -010). → TASK-16, TASK-17
14. **S-14 Scope, guardrails, evidence and merge readiness:** one module, no secrets/PII, no later
    story built, the unit results table, the `<seq>` and the human ruling record (SPEC-016, -017;
    BR6, BR8). → TASK-18, TASK-19

Out of scope (Story v7 §19; each a named seam or exclusion, D-RUN-08; not built):
`v_ace_*` views, helper functions, grants and the view conformance test (RWB-E1-069); freshness
(RWB-E1-015); access per data product, PDPA masking and the catalog entry screen (RWB-E1-016);
retention (RWB-E1-017); Stage 2 products; the dictionary endpoint and field versions (RWB-E1-064);
`rule_package` content (RWB-E1-072); `delegation_limit` content (RWB-E1-038); the persistent access log
(RWB-E1-039); the message table (no owner); the `sys_fields`/`sys_objects` handler (RWB-E1-064,
`GAP-E1001-23`); the `LOV-REF-TABLE` / `refdata.columns.data_product` rows (not needed, D-RUN-11);
rollback of a catalog version (`ASM-E1001-20`, `GAP-E1001-24`).

## One-module check (D-RUN-21)

AGENTS.md §7 and §9 ask that a plan "touches one module". Build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md`
decisions table, 18 Nov 2026 05:36, orchestrator Claude Code; **not ratified**, OPEN-050, owner the
recovery tech lead) reads this as **the ACE module, the recovery module**.

| Check | Result |
|---|---|
| ACE module touched | `recovery` only — every main and test class is under `th.co.scb.ace.demo.recovery` |
| Nested design modules | P1 `dataengine.internal.catalog` (new code); P4 `access.internal.FixedMessageCatalog` (four additive entries, E1-042's seam). P1 imports P4 `access.api` only; **no P1 → P3 edge** (D-RUN-18) |
| Published types | None added or changed. P4 `access.api` is consumed, not owned; `dataengine.api` stays empty; the module map and `RecoveryBoundaryTest` are unchanged |
| Other ACE modules | None. No `common`, `collection` or pre-TE-001 package is created, read or referenced |
| Non-Java files touched | one migration; `config/parameter-catalog.csv`; `application.yaml`; `application-local.yaml`; `infra/postgres/init/10-load-ace-database.sh`; `docker-compose.yml`; `.env.example`; `README.md`; the migration-folder `README.md` |
| Shared build file | `backend/build.gradle.kts` is **not** changed: no dependency, task or tooling package is added; the bundle already measures every recovery main class |
| Verdict | **PASS — one ACE module (recovery).** No return to the analyst under AGENTS §7; no `common` or `collection` change. D-RUN-21 is an orchestrator reading, not a human ruling |

Boundary evidence: `ModulithTest` and `RecoveryBoundaryTest` stay green (TASK-09, TASK-15);
`DataProductCatalogLoadIT` proves E1-043 collects the bean by the P4 type; no P4 type refers to P1.

## Frontend Plan

**NOT_APPLICABLE.** UI In Scope NO. Story v7 §15: "No screen in this story"; the dictionary endpoint,
the catalog entry screen (SCR-40) and masking are later stories (Story v7 §19). The change adds no
screen, route, component, i18n key, client call or OpenAPI change; `api/recovery-api-v4.yaml` and
`frontend/src/api/schema.d.ts` are not regenerated. No file under `frontend/` is added or changed, so
there is no frontend implementation task, no frontend unit/coverage task, no component inventory and
no functional-automation journey. `plan/frontend/components.md` is **not written**.
`contracts/frontend-integrations.json` records the N/A with this evidence. `npm run check` still runs
in the merge gate (TASK-17) to prove no regression.

## Backend Plan

Surface status: **CHANGED**. Unit tests **REQUIRED** (trace SPEC-001..-019; gate: one `BUNDLE` rule,
`LINE`, `INSTRUCTION`, `BRANCH`, `METHOD` each ≥ 0.80 over all recovery main classes, which includes
`dataengine.internal.catalog`; no new tooling package).

Paths are exact. `R` = `backend/src/main/java/th/co/scb/ace/demo/recovery`; `T` =
`backend/src/test/java/th/co/scb/ace/demo/recovery`; `M` = `backend/src/main/resources`; `TR` =
`backend/src/test/resources`.

### Files added or changed — main

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Add | `M/db/modulemigration/recovery/V<seq>__rwb_e1_001_recovery_schema.sql` | Line 1 `-- Story: RWB-E1-001`; line 2 header; the statement groups of `data-model.md` § 1 | TASK-03, TASK-11 | 001..008, 019 |
| Add | `R/dataengine/internal/catalog/DataProduct.java` | Package-private JPA entity for `${recoverySchema}.data_product`; explicit `@Table(name = "data_product")` and `@Column` names, no schema literal; `@Version` on `version` | TASK-07 | 012 |
| Add | `R/dataengine/internal/catalog/DataProductRepository.java` | Package-private `Repository<DataProduct, UUID>`: `findAllByProductCodeIn(Collection<String>)`, `findByProductCode(String)` | TASK-07 | 012 |
| Add | `R/dataengine/internal/catalog/CatalogRole.java` | Package-private read-only entity for `role` (`role_code`, `is_active`) used by K4 | TASK-07 | 013 |
| Add | `R/dataengine/internal/catalog/CatalogRoleRepository.java` | Package-private `Repository<CatalogRole, UUID>`: `@Query("select r.roleCode from CatalogRole r where r.active = true")` | TASK-07 | 013 |
| Add | `R/dataengine/internal/catalog/SystemOfRecordGrammar.java` | The F1–F3 grammar (`ASM-E1001-09`), compiled once; `matches(String)` only, no message text, no product value | TASK-07 | 013 |
| Add | `R/dataengine/internal/catalog/CatalogFileRules.java` | K0-H header, K0-R required/width and K1 product-set checks; returns `RowCheckFailure`s; no repository access | TASK-07 | 013 |
| Add | `R/dataengine/internal/catalog/DataProductCatalogHandler.java` | Package-private `@Component` implementing `access.api.ReferenceTableHandler`; `apply` is `@Transactional`; TASK-09 adds `DataProductCatalogSettings`, `@EnableConfigurationProperties` and `@ConditionalOnProperty` on this class | TASK-07, TASK-09 | 013, 014, 017 |
| Add | `R/dataengine/internal/catalog/DataProductCatalogSettings.java` | Package-private `@ConfigurationProperties(prefix = "rwb.p1")` record `(boolean dataCatalog)` | TASK-09 | 017 |
| Edit | `R/access/internal/FixedMessageCatalog.java` | Four additive IDs (MSG-P1-003, -004, -007, -011), EN and TH, per `data-model.md` § 14.3; no other text changed | TASK-05 | 015 |
| Edit | `M/config/parameter-catalog.csv` | Two rows, one shape (`data-model.md` § 11); 19 → 21 rows; header unchanged | TASK-11 | 019 |
| Edit | `M/application.yaml` | `rwb.flyway.enabled: ${RWB_FLYWAY_ENABLED:true}`; new `rwb.p1.data-catalog: ${RWB_P1_DATA_CATALOG:false}` | TASK-13 | 010, 017 |
| Edit | `M/application-local.yaml` | `rwb.p1.data-catalog: true` | TASK-13 | 017 |
| Edit | `infra/postgres/init/10-load-ace-database.sh` | S1 default `false`; new S2 branch (`RWB_LOAD_REFERENCE_VIEWS`, default `true`) that runs the PS v6 view section with `SET search_path TO recovery;` and the same `ON_ERROR_STOP`; header comment updated | TASK-13 | 010 |
| Edit | `docker-compose.yml` | postgres: `RWB_LOAD_REFERENCE_SCHEMA: ${RWB_LOAD_REFERENCE_SCHEMA:-false}`, `RWB_LOAD_REFERENCE_VIEWS: ${RWB_LOAD_REFERENCE_VIEWS:-true}`; backend: `RWB_FLYWAY_ENABLED: ${RWB_FLYWAY_ENABLED:-true}`, `RWB_P1_DATA_CATALOG: ${RWB_P1_DATA_CATALOG:-false}` | TASK-13 | 010 |
| Edit | `.env.example` | S1 `false`, S2 `true`, S3 `true` with one comment line each (no secret) | TASK-13 | 010 |
| Edit | `README.md` | "Local versus target" row "Recovery schema" → "Flyway (E1-042, E1-043, E1-001 migrations); PS v6 view section at init until RWB-E1-069 (`RWB_LOAD_REFERENCE_VIEWS`)"; the "When RWB-E1-001 delivers V0001-V0003" paragraph reworded, and the reset/`up` instruction kept | TASK-13 | 010 |
| Edit | `M/db/modulemigration/recovery/README.md` | Last paragraph: the folder is populated by E1-042/E1-043/E1-001; PS v6 is views-only locally until E1-069; `<seq>` wording; E1-044 SPEC-015 alignment (OPEN-NEW-9) | TASK-13 | 010 |

### Files added or changed — test scope and fixtures

| Kind | Path | Content | Task | SPEC |
|---|---|---|---|---|
| Add | `T/architecture/dictionary/MigrationDerivationTest.java` | Parses the migration and `../infra/postgres/schema/03-recovery-physical-schema-v6.sql`; proves the 89-table set, every column, 91 FKs, 111 indexes, 85+973 comments, no T8 object, no `IF NOT EXISTS`/`DROP`/`GRANT`/`SET search_path`, no literal schema outside strings/comments, the view definition | TASK-01 | 002, 003, 005, 006, 008 |
| Add | `T/architecture/dictionary/DictionarySeedShapeTest.java` | Every `sys_fields` row is an `INSERT` with a literal `is_personal`; no `UPDATE sys_fields`; 526 `true` = fixture; 3 provisional rows; 123/1,379+3/598/54/421/0/0 counts; every `data_product` seed value fits its declared width; DP07 = 139 exactly; each seed value matches exactly one F1–F3 form | TASK-01 | 004, 006, 018; ASM-E1001-13, -14, -17 |
| Add | `T/architecture/dictionary/ParameterCatalogRowsTest.java` | Parses the CSV and the migration; the two rows exist with the one shape; no `refdata.columns.data_product`; no LOV-REF-TABLE row; no `parameter_value` row | TASK-10 | 019 |
| Add | `T/architecture/dictionary/DataDictionaryConformanceTest.java` (`@Tag("recovery-it")`) | C1/C2/C3 over `information_schema.columns` vs `sys_fields`, `flyway_schema_history_recovery` excluded; the three AC5 proof fixtures on a throwaway schema; the `char(64)` pass case | TASK-02 | 009 |
| Add | `T/testsupport/RecoverySchemaContainer.java` | Abstract Testcontainers base: one PostgreSQL 16.16 container from `infra/postgres/init` with `RWB_LOAD_REFERENCE_SCHEMA=false`, `RWB_LOAD_REFERENCE_VIEWS=false`, `RWB_ACE_TIER2_PROBE=true`; `@DynamicPropertySource` for the datasource and the Flyway account; package `th.co.scb.ace.demo.recovery.testsupport` | TASK-02 | 010 |
| Add | `T/dataengine/internal/catalog/RecoverySchemaMigrationIT.java` (`@Tag("recovery-it")`) | 93 tables, 89 created here, the 4 T8 tables exist once, the 20 removed tables and `payment_match_rule` absent, 0 constraints into `public`, the 18 link columns `varchar(255)` in no FK, no `v_ace_*`/helper function from this file, re-run applies 0, the failing-`valuation_ext` copy leaves nothing and no success row, earlier-story objects intact, AC2's dictionary row | TASK-02 | 002, 003, 005, 007, 008, 010, 019 |
| Add | `T/dataengine/internal/catalog/SeedIntegrityIT.java` (`@Tag("recovery-it")`) | Seed fits its column widths from `information_schema.columns`; DP07 verbatim; `is_personal = true` exactly the 526 fixture IDs; the 3 provisional rows exist with their types | TASK-02 | 018; ASM-E1001-13, -14, -17 |
| Add | `T/dataengine/internal/catalog/SystemOfRecordGrammarTest.java` | F1/F2/F3 pass cases; the 10 SPEC-013 negatives; the 14 seed values match exactly one form; `the core bank` is a source | TASK-06 | 013 |
| Add | `T/dataengine/internal/catalog/DataProductCatalogHandlerTest.java` | K0-H, K0-R (required + width + the two rendered MSG-P3-027 texts), K1 (missing/unknown/duplicate), K2 (empty + forms), K3 (absent + non-UUID), K4 (active role code, AC9 text), K5 (four values, AC9 text), finding order, `validate` writes nothing, `tableCode`, `keyColumns`, `repeatMessage`, `dating`, `supportsRollback`, `changeSummary` | TASK-06 | 013, 014, 015 |
| Add | `T/dataengine/internal/catalog/DataProductCatalogApplyTest.java` | 14 updates by `product_code`, returns 14, `valid_from`/`updated_at` set, no insert/delete, a missing product throws and no `saveAll` occurs | TASK-06 | 014 |
| Add | `T/dataengine/internal/catalog/DataProductCatalogSettingsTest.java` | `ApplicationContextRunner` with mocked `DataProductRepository` and `CatalogRoleRepository` beans: flag on → one handler bean of the P4 type with `tableCode()` `data_product`; flag off → no bean; no `PARAMETER` bean; a second handler for the same code is E1-043's test, not duplicated | TASK-08 | 017, 019 |
| Add | `T/access/internal/DataProductMessagesTest.java` | The four IDs resolve EN exactly and TH non-empty; the four rendered texts of `data-model.md` § 14.3; MSG-P3-027 and MSG-GEN-001 already exist | TASK-04 | 015 |
| Edit | `T/casewf/migration/RecoveryFlywayConfigTest.java` | Add `bindsFlywayEnabledFromApplicationYaml`: `${RWB_FLYWAY_ENABLED:true}` binds `true` on the isolated environment; no assertion changed | TASK-12 | 010 |
| Edit | `T/RecoveryDatabaseIT.java` | `RWB_LOAD_REFERENCE_SCHEMA=false`, add `RWB_LOAD_REFERENCE_VIEWS=true`; every existing assertion kept (30 views, 0 public tables, read-only views/owner, baseline row 0, append-only, identity split) | TASK-12 | 010 |
| Add | `T/dataengine/internal/catalog/DataProductCatalogLoadIT.java` (`@Tag("recovery-it")`) | The E1-043 endpoint end to end: 201+validated then 200+approved → 14 rows, version +1, AC2 view rows with the synthetic owner; 422 MSG-P1-003/-004/-007 with all details (AC7/8/9/11); 409 MSG-P1-011 repeat, nothing written (AC10); RW-DATASTEW 403 MSG-P4-002 + one REFUSED audit line (X8); flag off 422 MSG-P3-027; apply rollback when a product row disappears (the 13 remaining rows unchanged and no version recorded; no message code asserted) | TASK-14 | 013..019 |
| Add | `TR/dictionary/is-personal-union-v4.tsv` | 526 field IDs, copied from `../specify/evidence/is_personal_union_v4.tsv` (field IDs and metadata only) | TASK-01 | 006, 018 |
| Add | `TR/reference-loads/data-product/*.csv` | The 12 fixtures of `data-model.md` § 15, synthetic values only | TASK-06, TASK-14 | 013..015 |

### Files explicitly not changed

`backend/build.gradle.kts`; `api/recovery-api-v4.yaml`; `frontend/**`; `backend/src/test/resources/architecture/recovery-modules.yaml`;
`T/architecture/RecoveryBoundaryTest.java`; `T/ModulithTest.java`; `T/architecture/RecoveryMigrationLintTest.java`;
`R/casewf/**` (the Flyway bean and the E1-043 registry are consumed, not edited); `R/access/api/**`;
`infra/postgres/init/20-grants.sql.inc`; `infra/postgres/schema/**`; `scripts/dev.ps1`;
`backend/src/test/.../e2e/PlatformE2ETest.java`. A change to any of these must appear here before it is
made; TASK-18 diffs the branch against this list.

### Handler design (SPEC-013, § 14 of `data-model.md`)

`DataProductCatalogHandler` implements `recovery.access.api.ReferenceTableHandler` as a package-private
Spring bean behind `rwb.p1.data-catalog`:

| Method | Behaviour |
|---|---|
| `tableCode()` | `"data_product"` |
| `keyColumns()` | `List.of("product_code")` |
| `repeatMessage(file)` | `new HandlerMessage("MSG-P1-011", Map.of("source", "data product catalog", "date", file.validFrom().toString()))` |
| `dating()` | `Dating.CURRENT_STATE` |
| `supportsRollback()` | not overridden (SPI default `false`; `ASM-E1001-20`) |
| `changeSummary(file)` | not overridden (SPI default `List.of()`) |
| `validate(file)` | K0-H, K1, then per row in file order K0-R, K2, K3, K4, K5; returns `ValidationReport`; **no repository write, no `save`** |
| `apply(loadId, file, validFrom)` | `@Transactional`; loads the 14 rows by `product_code` in one query; updates the seven file fields and `valid_from`, `updated_at`; returns 14; throws if a product is absent; never inserts or deletes |

Details that the plan fixes and the unit tests assert:

- **K0-H** compares `file.columns()` with the exact 8-name list, each once, in order. Failure:
  `RowCheckFailure(0, null, "MSG-P3-027", {table=data_product, check="the header must hold the 8 catalog columns"})`.
- **K1** compares the set of non-empty `product_code` values with DP01–DP14, each once. `{products}` is
  the ascending comma list of the missing codes; when nothing is missing, the duplicated or unexpected
  codes are named instead (so an unknown code is refused by the same check, SPEC-013). `column =
  product_code`, `row = 0`.
- **K0-R** requires `product_code`, `product_name`, `definition`, `owner_role`, `refresh_cycle`; an
  empty value is MSG-GEN-001 with `{field}` = the column name; a value longer than its column is
  MSG-P3-027 with `{table}=data_product`, `{check}="value too long for {column}"`. `system_of_record`
  and `owner_user_id` are **not** required here (their absence is K2/K3, Story v7 X4), but every
  present value is width-checked (`system_of_record` 200, `expected_by` 20, all others as § 3).
- **K2** is `SystemOfRecordGrammar.matches`; an empty value is K2. **K3** requires a present value that
  parses as a UUID. Both are MSG-P1-003 with `{product}` = code, `column` = the field.
- **K4** uses `CatalogRoleRepository.activeRoleCodes()` (one query per validate); `{values}` is
  literally `the role codes in LOV-ROLE` (the 54 codes are not listed to the caller).
- **K5** uses the four LOV-REFRESH values in `sort_order`, `{values}` = `DAILY, WEEKLY, MONTHLY, ON_CHANGE`.
- **K4/K5** return `{row}` = the 1-based data row (header excluded), the same number as
  `RowCheckFailure.row`, because E1-043 passes handler placeholders through unchanged (SPEC-025 L13).
- **Order:** file-level K0-H, K1; then rows in file order, each row K0-R, K2, K3, K4, K5. K0 never
  suppresses K2/K3 for the same row, so the two single-defect fixtures (TC-18, TC-19) yield exactly one
  finding and `messageCode` MSG-P1-003.
- No product value, role, refresh cycle or message text is a Java literal beyond the 14 codes BR2 fixes
  and the four LOV-REFRESH values the AC9 text quotes. The grammar is code; the values are data.

### Apply, idempotency and the one deviation (SPEC-014)

`apply` writes the 14 seeded rows in E1-043's approve transaction (REQUIRED), matched by `product_code`,
with `valid_from` = the load's date, the seven file values, `updated_at` = now and `version` +1 through
`@Version`. It returns 14. It never inserts or deletes (`ASM-E1001-08`); a missing product throws and
the whole transaction rolls back (proved by `DataProductCatalogLoadIT`, not only by a mock).

**Deviation, recorded not hidden:** the published SPI's `apply` carries no actor, so
`data_product.updated_by` cannot be set from it. E1-043 records the approver in
`reference_version.approver_user_id`; this handler leaves `updated_by` at its seeded NULL and sets
`updated_at` only. This is `PG-E1001-02` (Blocker = No) in `document-gaps.md`; the field matrix cell is
not silently claimed. Asking E1-043 for an actor-bearing `apply` is not done (the spec states this
story asks E1-043 for nothing).

A repeat is E1-043's L9: `repeatMessage` gives MSG-P1-011, the answer is 409 `Problem` with `{source}`
and `{date}`, nothing is written, for any business date (AC10, X7; `GAP-E1001-13`). A file equal to the
version in force under a **different** `validFrom` is not a repeat.

### Flag and registration (SPEC-017, SPEC-019)

`rwb.p1.data-catalog` defaults `false` and is `true` in `application-local.yaml` (and `RWB_P1_DATA_CATALOG`
in the environment/compose). On: the bean exists and E1-043's `ReferenceTableHandlers` collects it by
the P4 type at start-up, so `data_product` is a handler code. Off: no bean, so E1-043 sees an unknown
code and answers 422 MSG-P3-027 (its SPEC-025 item 1) — the previous code path. The migration and the
view are not behind the flag. No `PARAMETER` bean is created (D-RUN-20).

### Local switch (SPEC-010)

| Switch | Values | Default after this story | Owner of the later change |
|---|---|---|---|
| S1 `RWB_LOAD_REFERENCE_SCHEMA` | `true`: load all of PS v6 at init; `false`: schema + `pgcrypto` only | **`false`** in `.env.example`, `docker-compose.yml` and the script | RWB-E1-069 may retire `true` |
| S2 `RWB_LOAD_REFERENCE_VIEWS` (new) | Read only when S1=`false`. `true`: run the PS v6 section from the marker `-- ACE source views. Section A ships as V0002; Section B ships after RWB-ACE-001.` to EOF, prefixed `SET search_path TO recovery;`, same `ON_ERROR_STOP` strictness. `false`: no views | **`true`** (views-only stand-in for V0002/V0003) | **RWB-E1-069** flips it to `false` and deletes the branch, then applies its Flyway-mode grants and runs the `RecoveryDatabaseIT` view assertions against Flyway-created views |
| S3 `RWB_FLYWAY_ENABLED` | maps `rwb.flyway.enabled` | `true` | — |

Valid combinations: S1=`false` + S3=`true` (default: Flyway builds the tables, S2 supplies the views);
S1=`true` only with S3=`false` (reference browsing); S1=`true` + S3=`true` is refused by the init
script's message and fails fast on the first migration (X9). `20-grants.sql.inc` is unchanged; its
default privileges cover Flyway-created tables. An existing local volume keeps its old contents:
README tells developers to run `./scripts/dev.ps1 reset` then `up` after this merge.

Test stages: `./scripts/dev.ps1 test` needs no database; `RecoverySchemaMigrationIT`,
`DataDictionaryConformanceTest`, `SeedIntegrityIT` and `DataProductCatalogLoadIT` use S1=`false`,
S2=`false`; `RecoveryDatabaseIT` moves from S1=`true` to S1=`false`, S2=`true` and keeps every
assertion (the baseline `version='0'` row holds because the views make the schema non-empty,
`ASM-E1001-18`); earlier stories' ITs that build an S1=`true` container are pinned to the migrations
merged before this story or moved to S1=`false`, with no assertion removed (OPEN-NEW-9).

Hand-off to RWB-E1-069 (answer to its review 107): this story does not build V0002/V0003; it supplies
the S2 stand-in and the README text. Two E1-069 SPEC-015 points are stale against this design and are
named in OPEN-NEW-9: (a) says E1-069 flips S1 (this story flips it), and (c) says the baseline-`0`
assertion is replaced (this story keeps it in the S2 stage).

### Messages (SPEC-015)

Four IDs are added to E1-042's `access.internal.FixedMessageCatalog` (EN and TH), not held in
`dataengine`: MSG-P1-003 (Story v7 English; MSG v4 Thai, status Proposed), MSG-P1-004, MSG-P1-007,
MSG-P1-011. `ApiProblemException` and `ProblemFactory` are unchanged; E1-043 raises the Problem. No
message text is written in the handler; the handler returns IDs and placeholders only.

## Migration

One file: `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_001_recovery_schema.sql`.
**No number is fixed** (D-RUN-07); the orchestrator assigns `<seq>` at merge as the next four-digit
number in merge order (D-RCV-28); the lint requires a contiguous sequence from `V0001`. Line 1 is
exactly `-- Story: RWB-E1-001`; line 2 is a header comment citing Physical Schema v6, D-RCV-28 and the
spec. It is the only non-fix file for this story; forward only; never edited after merge.

The body is PS v6 lines 16–6130 in file order, transformed by T1–T11 of SPEC-002 and nothing else:

| # | Treatment |
|---|---|
| T1 | Removes `CREATE SCHEMA`, `SET search_path`, `CREATE EXTENSION` (environment preconditions) |
| T2 | Qualifies every object `${recoverySchema}.<name>`; no literal schema outside strings/comments |
| T3 | Replaces the PS v6 view with SPEC-005 (20 columns) |
| T4 | Replaces the PS v6 `data_product` seed with the 14 Story v7 §13 values |
| T5 | Does **not** carry the 8 `rule_package` rows |
| T6 | Does **not** carry the PS v6 view section (line 6131+: 3 helper functions, 30 `v_ace_*` views, commented grants) |
| T7 | Adds no `GRANT`/`REVOKE` |
| T8 | Does **not** create `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row`, `fk_reference_row_version_id`, `ix_reference_row_version_id`, or the 4+53 comments on them; **does** seed their 4 `sys_objects` and 53 `sys_fields` rows and **does** create the 4 FKs from this story's tables to `reference_version` |
| T9 | `data_product.system_of_record` and DF-REF-074 `physical_type` become `varchar(200)` (`ASM-E1001-13`) |
| T10 | `is_personal` is the literal `true`/`false` in each `sys_fields` INSERT row (`ASM-E1001-14`) |
| T11 | Adds DF-REF-300/-301/-302 for E1-042's three `parameter_value` columns (`ASM-E1001-17`) |

Exact table list — **89 created**, D-RUN-12:

```text
recovery_case case_account case_party deviation queue assignment task timer treatment
guarantee_claim legal_action notice hearing partner partner_instruction listing asset_sale
debt_sale_lot debt_sale_account interaction document document_field document_custody
decision_log_entry proceeds write_off rule_package rule_package_version rule_row delegation_limit
lov_value role permission template data_product data_product_access data_product_load data_contract
sys_objects sys_fields sys_field_version case_list_row reconciliation_result lake_copy_watermark
retention_rule dp_treatment dp_guarantee_claim interface_config outbound_item processed_event
idempotency_key outbox_event outbox_delivery feature_flag feature_flag_change job_catalog
efs_ledger_outcome case_entry_exclusion queue_member queue_measure rule_test_case masking_rule
role_conflict partner_user document_type document_checklist_item case_document_check
document_hub_parameter document_intake document_text retention_action merge_field signature_request
approval measure_definition measure_snapshot measure_publish agent_policy agent_prompt agent_run
agent_sample agent_evaluation_run agent_evaluation agent_feedback agent_alert party_ext
contact_point_ext account_ext valuation_ext
```

**D-RUN-12 skips (4 tables):** `parameter_catalog`, `parameter_value`, `reference_version`,
`reference_row`. Their dictionary rows stay (4 objects, 53 fields). Counts after the file: 93 tables in
the schema, 123 `sys_objects`, 1,382 `sys_fields`, 91 FKs, 111 indexes, 3 CHECKs, 2 triggers, 598
`lov_value`, 54 `role`, 421 `permission`, 14 `data_product`, 0 `delegation_limit`, 0 `rule_package`,
2 `parameter_catalog` rows added here.

No `IF NOT EXISTS`, `DROP`, `CONCURRENTLY`, `CREATE SCHEMA/ROLE/EXTENSION`, `GRANT`/`REVOKE` or
`SET search_path`. No data outside `${recoverySchema}`. No `v_ace_*` view or helper function. The file
does not guard against objects that already exist, so a duplicate fails the migration (AC4) instead of
being skipped. The two `parameter_catalog` inserts are the only `ON CONFLICT` statements and are
required by SPEC-019 item 5.

`MigrationDerivationTest` (unit) and `RecoverySchemaMigrationIT` (container) prove the derivation and
the counts; `DataDictionaryConformanceTest` proves C1/C2/C3; `SeedIntegrityIT` proves the seed and the
marks.

## Rule tables and reference sources read

| Source (name, version) | What it supplies | Applied in |
|---|---|---|
| Story file v7, RWB-E1-001 v1 (`04-user-stories/…/rwb-e1-001-…-v1.md`) §§ 4, 5, 7–19 | AC1–AC11, BR1–BR9, X1–X11, the 20 test cases, authority, contract, guardrails, out-of-scope | Whole plan |
| Physical Schema v6 (16 Nov 2026), `06-data/recovery-workbench-physical-schema-v6.sql` (repo copy `infra/postgres/schema/03-…`) | Every table, column, type, width, nullability, default, key, FK, index, CHECK, function, trigger, comment and seed row | TASK-03; `data-model.md` §§ 2–10 |
| Decision Log v10, D-RCV-28 / D-RCV-29; D-RCV-35 U3/U4; D-RCV-36 change register A.5/A.7, row 18, T5/T10 | Migration naming and `<seq>`, seed ownership, extension tables, no source copy, no `payment_match_rule`, no rule table | SPEC-001..-003, -006; TASK-03, TASK-18 |
| API Specification v4, `postAdminReferenceLoads` (line 3167), approve (3214), `ReferenceLoad` (8832), `Problem`, E403/E409/E422 | The two operations and their responses; `data_product` is a free `table` string, so no OpenAPI edit | TASK-14; `contracts/backend-apis.json` |
| Error and Message Standard v4 lines 77, 78, 81, 85, 151, and MSG-GEN-001 | The four message texts and placeholders; MSG-P3-027 for K0 | TASK-04, TASK-05, TASK-06, TASK-14 |
| RWB-E1-043 spec revision 10, SPEC-002, -006, -024..-032 and `shared-updates.md` § 3.1 | The P4 SPI, L1–L13 check order, repeat at L9, `CURRENT_STATE`, the two catalog keys, the audit line, `is_personal` protection | TASK-05, TASK-07, TASK-11, TASK-14 |
| RWB-E1-042 spec revision 13 §7.1/§7.2/§10.2/§12.3/§12.11/§12.14 and plan v2 `data-model.md` §§ 4.1–4.2 | `parameter_catalog` columns and CSV rules, `used_by` grammar, `FixedMessageCatalog`, `MessageResolver`, the three added `parameter_value` columns | TASK-05, TASK-10, TASK-11, TASK-13 |
| RWB-E1-044 spec v14-7 SPEC-007/SPEC-015 and plan v2 | The migration lint (identifier-only, quote-aware), the `${recoverySchema}` folder and its README | TASK-00, TASK-03, TASK-13 |
| RWB-TE-001 plan v7 and spec v4 SPEC-001/SPEC-022/SPEC-025/SPEC-026 | Module homes, `dataengine` in the map, `RecoveryBoundaryTest`, `ApplicationYamlEnvironment`, the coverage bundle | TASK-00, TASK-09, TASK-15 |
| PDPA Inventory v4 (Fields tab, Key); Personal Data Protection Design v2 line 31; `evidence/is_personal_union_v4.tsv` | The 526-field union and the 17 Restricted fields | TASK-01, TASK-03, TASK-18 |
| Logical Data Model and Data Dictionary v8, `06-data/recovery-workbench-logical-data-model-and-data-dictionary-v8-xlsx.md` line 561 (DF-REF-074) | The 120 width the ruling must also update if it widens | `GAP-E1001-17`; `document-gaps.md` |
| Users, Roles and Permissions v4 (Reference data column) | RW-REFADM loads (`CRUD`), RW-DATASTEW approves (`RU`; no `C`) | TASK-11, TASK-14 |
| Testing standards v2.0; `implementation-execution-gates.md` | Levels, `recovery-it`, synthetic data, the 80 % gates and evidence | TASK-02, TASK-14..TASK-18 |
| `AI-SDLC-BUILD-LOG.md` decisions table (D-RUN-07, -08, -12, -17, -18, -21) | Migration number, seams, one table owner, earlier plans as base, SPI home, one-module reading — orchestrator decisions, not ratified (OPEN-050) | Whole plan |

No product value, owner, role or refresh cycle is written as Java code: the 14 products and their values
are seed and load data; only the 14 codes BR2 fixes and the four LOV-REFRESH values the AC9 text quotes
are constants. No route, threshold or message text is a literal: routes are E1-043's, texts are in the
catalog.

## Unit test applicability

| Surface | Changes | Unit tests | Coverage gate | Trace | Evidence and rationale |
|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | Story v7 §15; spec §19 | No screen, route, component or i18n key; no file under `frontend/`; OpenAPI and `schema.d.ts` unchanged |
| Backend | YES — migration, P1 catalog classes, additive message entries, two catalog rows, flag, local switch | **REQUIRED** | `recoveryCoverageVerification`: one `BUNDLE` rule, `LINE`, `INSTRUCTION`, `BRANCH`, `METHOD` each ≥ 0.80 over the TE-001 combined bundle (all recovery main classes, which takes in `dataengine.internal.catalog`); no new exclusion, threshold or tooling package | SPEC-001..-019; AC1–AC11; BR1–BR9 | K0–K5, F1–F3, apply, the flag condition and the catalog rows are hand-written logic. JUnit 5 + AssertJ, Mockito, `ApplicationContextRunner`, `ApplicationYamlEnvironment`; JaCoCo |

Separately required integration tests (`recovery-it`, not replaced by unit tests):
`RecoverySchemaMigrationIT`, `DataDictionaryConformanceTest`, `SeedIntegrityIT`, the moved
`RecoveryDatabaseIT` and `DataProductCatalogLoadIT`. No measured coverage is claimed here; TASK-15
runs the gate and reports the four counters. A counter below 0.80 is a blocker, never an exclusion or a
lowered threshold.

## Execution order (tests before code, AGENTS.md rules 3 and 10)

1. **TASK-00** pre-flight on the merged base; baseline counters; the `<seq>`-free state; the ruling
   register (PRE-6 recorded, not required yet).
2. **Red, unit:** TASK-01 (`MigrationDerivationTest`, `DictionarySeedShapeTest`, the fixture copy).
3. **Red, container:** TASK-02 (`RecoverySchemaContainer`, `RecoverySchemaMigrationIT`,
   `DataDictionaryConformanceTest`, `SeedIntegrityIT`) — assertion-red on the empty schema.
4. **Green:** TASK-03 (the migration) makes TASK-01 and TASK-02 green.
5. **Red:** TASK-04 (message tests) → **TASK-05** (the four IDs).
6. **Red:** TASK-06 (grammar, handler, apply) → **TASK-07** (P1 classes).
7. **Red:** TASK-08 (flag/settings) → **TASK-09** (settings + condition).
8. **Red:** TASK-10 (catalog rows) → **TASK-11** (CSV + migration rows).
9. **Red:** TASK-12 (S3 binding + `RecoveryDatabaseIT` stage edit) → **TASK-13** (the switches, scripts,
   compose, env, READMEs).
10. **System/API:** TASK-14 (`DataProductCatalogLoadIT`); a red case is fixed in the owning green task,
    never by weakening the assertion.
11. **Verification:** TASK-15 (unit + coverage), TASK-16 (container suite and `it`), TASK-17 (`test` and
    `e2e`), TASK-18 (scope, guardrails, evidence, one module), TASK-19 (merge readiness and the human
    ruling).

Every red run and every green run is saved under `implement/` as command, exit code and the first
failing assertion or the final summary line. Compile-red tasks run directly before their green task, so
every other task's verification runs on a compiling test source set.

## Functional Test Scenarios

| ID | Scenario | Owner | Assignment | Evidence |
|---|---|---|---|---|
| FTS-E1001-01 | RW-REFADM loads a 14-row catalog (201, validated), RW-DATASTEW approves it (200, 14 rows), `v_data_dictionary` shows DP01's product system of record, refresh cycle and synthetic owner; the same file again answers 409 MSG-P1-011 and writes nothing; a two-system DP06 and an ownerless DP11 answer 422 MSG-P1-003 with both details; 13 rows answer MSG-P1-004 "Missing: DP09."; `DP_OWNER`/`HOURLY` answer the two AC9 texts; a bare "CCMS" answers MSG-P1-003; RW-DATASTEW loading gets 403 MSG-P4-002 and one REFUSED `event=REFERENCE_LOAD_AUDIT` line | API Tester | **ASSIGNED** — the only HTTP surface; run against the local stack with `api-tests/` evidence (TASK-14 also runs it as a `recovery-it` test) | `api-tests/` report with each status, `messageCode`, `detail`, the audit line and the view row; compare with TC-E1-001-03, -07..-12 |
| FTS-E1001-02 | A data steward opens a catalog screen and edits a product | Functional Automation Test | **NOT_APPLICABLE** — UI In Scope NO; the catalog entry screen is RWB-E1-016/Epic 8 | — |
| FTS-E1001-03 | Pipeline applies the migration in a clean schema, the conformance test passes, a re-run applies nothing, a branch with an extra column or a changed type fails with the AC5 texts | Implementation Builder (integration) | **NOT a functional-automation journey**; executed by `RecoverySchemaMigrationIT`, `DataDictionaryConformanceTest`, `SeedIntegrityIT` (TASK-02, TASK-16) | `implement/backend/it.log`; JUnit XML |
| HV-E1001-01 | The human ruling on DP07's width (`GAP-E1001-17`) and the `is_personal` set (`GAP-E1001-18`) is recorded before the merge | Human (data architect; data architect with the DPO) | **OPEN — blocking the merge, not the branch**; never reported as tested | `shared-updates.md` rows; OPEN-NEW-6, OPEN-NEW-7; TASK-19 |
| HV-E1001-02 | The DEV and SIT catalog load files carry a real owner user ID per product | Human (RW-DATASTEW, RW-REFADM) | **OPEN** — outside the repository; tests use synthetic UUIDs | `shared-updates.md`; Story v7 §3 |
| HV-E1001-03 | The recovery tech lead ratifies D-RUN-12, D-RUN-18 and D-RUN-21 | Human (recovery tech lead) | **OPEN** — OPEN-050; not tested | `shared-updates.md` |
| HV-E1001-04 | RWB-E1-039 adds the persistent access-log assertion for a refused `data_product` load | Human (RWB-E1-039 owner) | **OPEN, later story**; this story asserts the interim audit line | OPEN-NEW-10; `GAP-E1001-22` |
| HV-E1001-05 | RWB-TE-011's PDPA lint reports zero findings on this migration once both are merged | Human (RWB-TE-011 owner) | **Conditional** — TASK-18 runs the lint if merged, otherwise records it pending, never waived | OPEN-NEW-11; `GAP-E1001-21` |

No functional-automation journey exists because the story adds no screen; that is recorded as
`NOT_APPLICABLE` with evidence, not as an executed test.

## Requirement Logic To Task Coverage

`REQ_REF` values are the 33 rows of `../specify/spec.md` "Requirement-to-SPEC Logic Coverage"; none is
merged, dropped, generalized or weakened. `COVERED (ASM)` means the rule is implemented and tested on a
**Blocker = Yes** assumption; the ruling may change seed data only. `COVERED (as an exclusion)` is the
N/A row, kept visible with its reason.

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| BR1 | 006, 009 | TASK-01, -02, -03 | DIRECT_IMPLEMENTATION | `MigrationDerivationTest`; `DataDictionaryConformanceTest` C1/C2/C3 (1,050/1,050, 1,078/1,078); `DictionarySeedShapeTest` | COVERED |
| BR2 | 004, 006, 013 | TASK-03, -06, -07, -14 | DIRECT_IMPLEMENTATION | 14-row seed; K1; `DataProductCatalogLoadIT#validLoadIsValidatedThenAppliedOnApproval` | COVERED |
| BR3 | 004, 013, 018 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | `SystemOfRecordGrammarTest`; K2/K3; `DataProductCatalogLoadIT#twoDefectsAreBothReported`; `GAP-E1001-17` carried | COVERED (ASM) |
| BR4 | 013, 014 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | `validate` writes nothing; `apply` one transaction; 422 and the rollback IT case | COVERED |
| BR5 | 013 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | F1/F2 require `ACE (ingested from …)`; the AC11 bare-source case | COVERED |
| BR6 | 001, 002, 008 | TASK-03, -13, -16 | DIRECT_IMPLEMENTATION | `MigrationDerivationTest` (no literal schema, no `SET search_path`); `${recoverySchema}` in the file; re-run IT | COVERED |
| BR7 | 002 (T10), 006, 018 | TASK-01, -03, -15, -18 | DIRECT_IMPLEMENTATION | `DictionarySeedShapeTest` (526 literals, no `UPDATE`); `SeedIntegrityIT`; TE-011 lint (conditional); `GAP-E1001-18` carried | COVERED (ASM) |
| BR8 | 003 | TASK-02, -03 | DIRECT_IMPLEMENTATION | `RecoverySchemaMigrationIT#noConstraintReferencesPublic`, `#theEighteenLinkColumnsAreVarchar255WithNoForeignKey` | COVERED |
| BR9 | 006, 002 | TASK-03 | DIRECT_IMPLEMENTATION | 30 view objects, 304 `DF-ACE-*` rows; no view created; `MigrationDerivationTest` | COVERED |
| AC1 | 002, 003, 009, 010 | TASK-02, -03 | DIRECT_IMPLEMENTATION | `RecoverySchemaMigrationIT` (93 tables, 89 created, 4 T8, 20 removed, no `payment_match_rule`, conformance) | COVERED |
| AC2 | 005, 006 | TASK-03, -14 | DIRECT_IMPLEMENTATION | `RecoverySchemaMigrationIT#viewReturnsTheAc2Rows`; `DataProductCatalogLoadIT#viewReturnsAc2RowsAfterCatalogLoad` | COVERED |
| AC3 | 013, 014, 017, 019 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | Valid load + approve; DP01/DP03/DP06 values; 14 rows | COVERED |
| AC4 | 007 | TASK-02, -03 | DIRECT_IMPLEMENTATION | The failing-`valuation_ext` copy: no object, no success row, earlier objects intact | COVERED |
| AC5 | 009 | TASK-02, -03 | DIRECT_IMPLEMENTATION | Both AC5 texts; the `char(64)` pass | COVERED |
| AC6 | 008 | TASK-02, -03 | DIRECT_IMPLEMENTATION | Second migrate applies 0; 123/1,382 unchanged | COVERED |
| AC7 | 013, 015 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | DP06 two systems + DP11 no owner → two MSG-P1-003 findings, `messageCode` MSG-P1-003 | COVERED |
| AC8 | 013, 015 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | 13 rows → MSG-P1-004 "Missing: DP09." | COVERED |
| AC9 | 013, 015 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | The two verbatim texts, `{row}` 4 and 5, nothing written | COVERED |
| AC10 | 014, 015, 019 | TASK-07, -14 | DIRECT_IMPLEMENTATION | `repeatMessage` + E1-043 L9: 409 MSG-P1-011, nothing written (`GAP-E1001-13`) | COVERED |
| AC11 | 013, 015 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | Bare "CCMS" → MSG-P1-003, no row, version in force unchanged | COVERED |
| X1–X3 | 007, 008, 009 | TASK-02, -03 | DIRECT_IMPLEMENTATION | Failing statement, conformance failure, re-run in the same ITs | COVERED |
| X4–X7 | 013, 014, 015 | TASK-06, -07, -14 | DIRECT_IMPLEMENTATION | The four fixtures and the repeat case | COVERED |
| X8 / TC-E1-001-11 | 016, 019 | TASK-14, -18 | INHERITED_EXISTING_BEHAVIOR + SEAM | 403 MSG-P4-002, nothing written, one REFUSED `REFERENCE_LOAD_AUDIT` line; persistent access log is RWB-E1-039's (`GAP-E1001-22`) | COVERED |
| §10 Authority | 014, 016, 019 | TASK-11, -14, -18 | INHERITED_EXISTING_BEHAVIOR | RW-REFADM loads, RW-DATASTEW is refused C and may approve (E1-043's A-08); the two catalog keys; maker-checker inherited | COVERED |
| §12 Contract | 005, 012–015, 019 | TASK-03, -05, -06, -07, -14 | DIRECT_IMPLEMENTATION | The SPI methods, the 422/403/409 shapes, the view columns; `PG-E1001-02` records the one unwritable standard column (`updated_by`) | COVERED (PG-E1001-02) |
| §13 Solution plan | 001–010, 012–019 | TASK-03..TASK-14 | DIRECT_IMPLEMENTATION | Files, build steps 1–7, flag, tests | COVERED |
| §17 Guardrails | 003, 005, 017, 019 | TASK-18 | DIRECT_IMPLEMENTATION | Scope/guardrail check: no business value in code, no PII, no ACE table, no `public` constraint, dictionary reads only recovery tables | COVERED |
| §19 Out of scope | 002, 010 | TASK-18 | DIRECT_IMPLEMENTATION | Diff/scope check against the exclusion list | COVERED |
| NFR-RWB-005 Security | 016 | TASK-14, -18 | INHERITED_EXISTING_BEHAVIOR | E1-043's method checks and the 403 test; the migration runs as `rwb_migrator` (ADR-010) | COVERED |
| NFR-RWB-006 Privacy | 006, 017, 018 | TASK-01, -03, -15, -18 | DIRECT_IMPLEMENTATION | The 526 union; synthetic UUIDs only; no value leaves the DB (`GAP-E1001-18` carried) | COVERED (ASM) |
| NFR-RWB-008 Observability | 007 | TASK-02, -03 | DIRECT_IMPLEMENTATION | A failing statement is in the Flyway log; the E1-043 audit line for refusals | COVERED |
| NFR-RWB-009 Operability | 008, 017, 019 | TASK-09, -13, -19 | DIRECT_IMPLEMENTATION | Flag off → no bean → 422; forward-only migration; release/rollback note | COVERED |
| NFR-RWB-001..004, -007, -010 | — | TASK-18 | INHERITED_EXISTING_BEHAVIOR (exclusion) | No runtime read path with a target, no screen, no retained record class in this story (retention is RWB-E1-017) | COVERED (as an exclusion) |

No row is `BLOCKED`. 29 rows are unconditional; BR3, BR7 and NFR-RWB-006 are `COVERED (ASM)` on the
two Blocker = Yes gaps; 1 row is an evidence-backed exclusion. §12 carries one recorded partial:
`data_product.updated_by` is not writable through the published `apply` signature (`PG-E1001-02`,
Blocker = No); the rest of §12 is direct. The two spec contradictions stay where the spec put them —
this table does not clear them.

## SPEC to task map

| SPEC | Tasks | Named tests |
|---|---|---|
| SPEC-RWB-E1-001-001 | TASK-03 | `MigrationDerivationTest#fileIdentityAndName`; lint (inherited) |
| SPEC-RWB-E1-001-002 | TASK-01, -02, -03 | `MigrationDerivationTest` (T1/T2/T5/T6/T7/T8/T9/T10/T11); `DictionarySeedShapeTest` |
| SPEC-RWB-E1-001-003 | TASK-02, -03 | `RecoverySchemaMigrationIT#noConstraintReferencesPublic`, `#theEighteenLinkColumns…`; `MigrationDerivationTest#foreignKeysAndIndexesMatch` |
| SPEC-RWB-E1-001-004 | TASK-03, -06, -07 | `DataProductCatalogHandlerTest#headerMustHoldTheEightCatalogColumns`; `DictionarySeedShapeTest#dataProductSeedFitsItsColumns` |
| SPEC-RWB-E1-001-005 | TASK-03, -14 | `RecoverySchemaMigrationIT#viewReturnsTheAc2Rows`; `DataProductCatalogLoadIT#viewReturnsAc2RowsAfterCatalogLoad` |
| SPEC-RWB-E1-001-006 | TASK-03 | `DictionarySeedShapeTest` (all); `SeedIntegrityIT` |
| SPEC-RWB-E1-001-007 | TASK-02, -03 | `RecoverySchemaMigrationIT#failedStatementLeavesNoObjectAndNoSuccessRow` |
| SPEC-RWB-E1-001-008 | TASK-02, -03 | `RecoverySchemaMigrationIT#rerunAppliesNothing` |
| SPEC-RWB-E1-001-009 | TASK-02, -03 | `DataDictionaryConformanceTest` C1/C2/C3 + proofs |
| SPEC-RWB-E1-001-010 | TASK-12, -13, -16 | `RecoveryFlywayConfigTest#bindsFlywayEnabledFromApplicationYaml`; `RecoveryDatabaseIT` (all); compose/script check |
| SPEC-RWB-E1-001-011 (retired) | — | No task; the lint is E1-044's (D-RUN-13) |
| SPEC-RWB-E1-001-012 | TASK-07 | `DataProductCatalogApplyTest`; `DataProductCatalogLoadIT` |
| SPEC-RWB-E1-001-013 | TASK-06, -07 | `DataProductCatalogHandlerTest`; `SystemOfRecordGrammarTest` |
| SPEC-RWB-E1-001-014 | TASK-07, -14 | `DataProductCatalogApplyTest`; `DataProductCatalogLoadIT#repeat…`, `#applyRollsBack…` |
| SPEC-RWB-E1-001-015 | TASK-04, -05, -06, -14 | `DataProductMessagesTest`; `DataProductCatalogHandlerTest` (texts); `DataProductCatalogLoadIT` |
| SPEC-RWB-E1-001-016 | TASK-14, -18 | `DataProductCatalogLoadIT#dataStewardGets403…`; scope check |
| SPEC-RWB-E1-001-017 | TASK-08, -09, -18 | `DataProductCatalogSettingsTest`; scope check |
| SPEC-RWB-E1-001-018 | TASK-01, -02, -03, -18 | `DictionarySeedShapeTest`; `SeedIntegrityIT`; lint (conditional) |
| SPEC-RWB-E1-001-019 | TASK-10, -11, -18 | `ParameterCatalogRowsTest`; `DataProductCatalogLoadIT#validLoadIsValidatedThenAppliedOnApproval` (the authority reads both keys); scope check |

No orphan: every SPEC 001–019 (011 retired) has at least one task and a named test.

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]`,
no effective-screen node and no `SCR-*` screen in the spec. SCR-40 and the catalog entry screen are
Epic 8/RWB-E1-016 and out of scope. No screen consolidation task is required; the pre-submit check in
`tasks.md` records this, and TASK-18 checks that no UI file changed.

## Security, privacy and compliance

- **Authentication and authorisation.** No endpoint is added. The two operations carry E1-043's
  `@PreAuthorize` checks (Reference data C for load, A for approve) and its per-table lists, which this
  story seeds as two `parameter_catalog` rows (`RW-REFADM`, `RW-DATASTEW`). TC-E1-001-11's 403 comes
  from E1-043's method check plus `ApiExceptionHandler`, not from this story's code. No role, right or
  route is a literal here.
- **Audit.** A refusal writes one `event=REFERENCE_LOAD_AUDIT` line with `operation=LOAD`,
  `table=data_product`, `outcome=REFUSED`, `messageCode`, `traceId` and no user ID, row content or
  personal data (E1-043 SPEC-027/-028). The persistent access log is RWB-E1-039's seam
  (`GAP-E1001-22`, OPEN-NEW-10). The approval's AC-VERS decision entry and maker-checker are E1-043's.
- **Personal data.** No customer data. `owner_user_id` is a staff identifier: seeded NULL, loaded with a
  synthetic UUID, never logged, never returned by a log line; the view exposes it to a reader with
  schema access, as Story v7 §12 requires. `is_personal` is metadata; the 526 marks are the privacy
  deliverable and the migration contains no `UPDATE` that could change them. All test identities are
  random UUIDs.
- **Secrets.** None. No credential, token or connection string is added; `.env.example` gains switch
  values only (no secret); `pgcrypto` remains an environment precondition.
- **Database access.** The migration runs as `rwb_migrator` (ADR-010) and writes only
  `${recoverySchema}`; the handler runs as `recovery_svc` and reads/writes `data_product` and reads
  `role`; no `public` table is read or written; no constraint points into `public`; no `GRANT`/`REVOKE`
  in the file. The default privileges cover Flyway-created objects.
- **KYC/AML, suitability, delegation of authority.** Not applicable: schema and reference metadata, no
  credit decision, no approval limit.
- **Compliance-critical carry.** `GAP-E1001-18` is a personal-data classification decision; this plan
  keeps the protective union and requires the human ruling before merge. It does not present the
  protective reading as approved.

## Release and rollback

- **Release:** backend only. The migration runs whenever the recovery Flyway bean runs; it is forward
  only and never edited after merge. The handler is behind `rwb.p1.data-catalog` (default `false`,
  `true` in the local profile); with the flag off, E1-043 sees an unknown code and answers 422
  MSG-P3-027 — the previous code path. The view and the seeded tables are not behind the flag.
- **Rollback:** turn the flag off, or revert the merge request. The previous tag ignores the new tables;
  Flyway `clean` stays disabled. Removing seeded rows needs a new migration and a reviewed change; the
  two catalog rows are inert without the code.
- **Local:** after merge, `./scripts/dev.ps1 reset` then `up`; S1=`false`, S2=`true`, S3=`true`.
- **Release note item:** the migration creates 89 tables, the dictionary (123 objects, 1,382 fields with
  526 personal marks), `v_data_dictionary`, and updates the local database build to a Flyway-built
  schema with the PS v6 view section as the temporary view stand-in; the catalog load is available only
  with `rwb.p1.data-catalog=true`, and the **merge is gated on the human ruling for DP07's width and the
  `is_personal` set**.
- **Merge:** the orchestrator merges into `develop-recovery` only after `./scripts/dev.ps1 test` and
  `./scripts/dev.ps1 it` exit 0, TASK-18 is complete, the `<seq>` is assigned (D-RUN-07) and TASK-19
  finds the human ruling record. Nothing here is a human approval.

## Assumptions

Plan-stage assumptions are in `assumptions.md` (`PA-E1001-01` to `PA-E1001-17`). Spec assumptions
`ASM-E1001-01` .. `-20` are carried unchanged; `ASM-E1001-13` and `-14` keep their Blocker = Yes status
and are not re-litigated, accepted or ratified here. The same file restates the two carried blockers
first, so the builder meets them before any plan assumption.

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 20 tasks (TASK-00..TASK-19) for one forward-only migration with 89 tables and the 1,382-row dictionary (526 personal marks), the data_product catalog handler on E1-043's P4 SPI, the two catalog rows, the S1-S3 local switch and the unit/container/API suites; UI NOT_APPLICABLE.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec revision 4 passed its gate round 4 with 0 findings; every in-scope SPEC, AC, BR, TC, X and CLAR maps to a task and a named test; no coverage row is BLOCKED; the two Blocker = Yes gaps are carried visibly and do not stop the branch work] [UNBLOCK_ACTION: human ruling on GAP-E1001-17 and GAP-E1001-18 before the merge of the migration (OPEN-NEW-6, OPEN-NEW-7); D-RUN-12/-18/-21 ratification OPEN-050]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 2] [UNBLOCK_ACTION: the two Blocker = Yes clarification rows (CLAR-011, CLAR-012) need the human ruling before merge; CLAR-009 is non-blocking]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; no screen, route or component change]
PLAN_BLOCKER_CARRY: 2 [GAP-E1001-17 on ASM-E1001-13; GAP-E1001-18 on ASM-E1001-14; Blocker = Yes; not resolved, not ratified, merge gated by TASK-19]
PLAN_DEVIATIONS: 1 [PG-E1001-02: data_product.updated_by cannot be written through the published apply signature; updated_at is written, the approver is audited in reference_version]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: 33 of 33 requirement-logic rows map to tasks and named tests; 29 unconditional, 3 on the Blocker = Yes assumptions (BR3, BR7, NFR-RWB-006), 1 evidence-backed exclusion (NFR-RWB-001..004, -007, -010); the 2 spec contradictions stay recorded upstream.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 33] [TASK_COVERED_RULES: 33] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
CARRIED_SPEC_CONTRADICTIONS: 2 [GAP-E1001-17, GAP-E1001-18 — Blocker = Yes; human ruling required before build (the merge of this story's migration); no AI triage is that ruling]
```
