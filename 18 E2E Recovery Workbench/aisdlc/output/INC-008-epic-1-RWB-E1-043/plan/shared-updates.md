# Shared updates requested: RWB-E1-043 plan

RUN_ID `INC-008-epic-1-RWB-E1-043`, stage `plan`, 2026-11-18, run 1; remediation run 2 of 18 Nov 2026 changes only the PG-E1-043-03 row (PLAN-006) and adds no request. This stage **did not edit any shared file** (RUN-BRIEF rule 3). The orchestrator applies these rows in order and assigns IDs where needed. The spec stage's `specify/shared-updates.md` revision 10 (rows 1-40, sections 3.1-3.6) stands and is not repeated here; this file adds only what the plan stage needs. No row is a human approval, and no row ratifies D-RUN-18..21.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

| Change | Row |
|---|---|
| Story row INC-008 / RWB-E1-043, status column | Replace the spec-stage text with: "Planned - plan v1 (plan run 1, 18 Nov 2026; `output/INC-008-epic-1-RWB-E1-043/plan/plan.md`, `tasks.md`); plan gate pending. Spec revision 10 passed its gate on 18 Nov 2026 (round 10, 0/0/0/0). Build not started" |
| Add a plan trace for `FR-RWB-011` | `FR-RWB-011` -> `SPEC-RWB-E1-043-001` .. `-032` -> `TASK-00` .. `TASK-19` (`output/INC-008-epic-1-RWB-E1-043/plan/tasks.md`) -> tests `TC-E1-043-01` .. `-11`, `TC-RB-01/-02`, `TC-HD-01..05`, `TC-PB-01/-02`, `TC-TM-01..05`, `TC-RP-01`, `TC-FD-01`, `TC-DR-01`, `TC-FL-01`, `TC-MG-01`, `TC-BD-01`, `TC-CAT-01`, `SEC-01..17` (`plan/tests/scenarios.md`) -> code pending, branch cut after RWB-TE-001, RWB-E1-044 and RWB-E1-042 merge -> modules `casewf.refdata`, `casewf.refdata.api`, additive `access.api` and `access.internal` |
| Add the migration trace | `FR-RWB-011` -> `V<seq>__rwb_e1_043_reference_versions.sql` (`backend/src/main/resources/db/modulemigration/recovery/`); `<seq>` assigned at merge (D-RUN-07); record the assigned number here once the orchestrator sets it |
| Add the catalog and grants trace | `FR-RWB-011` -> `backend/src/main/resources/config/parameter-catalog.csv` (38 rows) and `backend/src/main/resources/access/interim-capability-grants.csv` (37 Reference data rows); reviewed with the catalog owner and the access owner |
| Note the 16 lines owned elsewhere | The spec's "Requirement lines built by another story" rows stay open and are not counted as planned here; no trace is claimed for them |

## 2. `aisdlc/docs/increments/INC-008-epic-1-RWB-E1-043.md` and `INDEX.md`

| File | Change |
|---|---|
| `aisdlc/docs/increments/INC-008-epic-1-RWB-E1-043.md`, Status | "Planned - plan v1 (plan run 1, 18 Nov 2026; `plan/plan.md`, `plan/tasks.md`, `plan/data-model.md`, `plan/contracts/*`, `plan/tests/scenarios.md`); plan gate pending; spec revision 10 passed round 10 (0/0/0/0). The previous plan attempt failed before writing; no plan file was overwritten." |
| The same file, files table (if it carries one) | Add `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_043_reference_versions.sql`, `backend/src/main/resources/config/parameter-catalog.csv` (38 rows), `backend/src/main/resources/access/interim-capability-grants.csv` (37 rows), `backend/src/main/resources/application.yaml` and `application-local.yaml` (`rwb.p3.refdata-versions`), the P3 `casewf/refdata/**` files, the P4 `access/api` and `access/internal` additions, the `[TE-001]` module map and `RecoveryBoundaryTest` edits |
| `aisdlc/docs/increments/INDEX.md`, status column and summary | "Planned" instead of "Specified"; keep the 10 Nov "Implemented" note as the ACE monorepo pack, not this repository |

## 3. `aisdlc/DOCUMENT-GAPS.md` (candidates)

| Local ID | Document (name, version, section) | Gap or conflict | Second source | Blocker? | Why | How the plan proceeded |
|---|---|---|---|---|---|---|
| PG-E1-043-01 | RWB-E1-043 spec revision 10, story v7 section 12 `ReferenceVersion` (11 components) | SPEC-011 requires `rollback_reason` from `versions()`; the record has no such component | Spec SPEC-011; story v7 section 12; the "signatures verbatim" row | No | The record is new; adding a 12th component removes and reorders nothing | Additive `rollbackReason`; `PA-E1-043-02`; TASK-06, TASK-09, TASK-12 |
| PG-E1-043-02 | RWB-E1-043 spec revision 10, SPEC-025 L4 | SPEC-002/TC-BR1 need 422 for a rule code or HOLIDAY; L4 would 403 a missing list key; SEC-06 needs 403 for a known code | Spec SPEC-002, TC-BR1, SPEC-025 L4, SEC-06 | No | The authority only decides the table right; the registry decides the code | Unknown code passes the table right and the registry answers 422; known code enforces the list; `PA-E1-043-15`; T-E1-043-23, T-E1-043-45, SEC-06 |
| PG-E1-043-03 | RWB-E1-043 spec revision 10, Exceptional-case "500 with `traceId`" | The existing `ApiExceptionHandler.unexpected` has no `traceId`, and the spec puts `ApiExceptionHandler`/`ProblemFactory` out of scope | Spec "Impacted Existing Nodes"; `platform/internal/ApiExceptionHandler.java`; `ProblemFactory.java`; TC-HD-05 | No | A defect path; no data written; the field is out of scope | Test asserts 500, the existing body and the absence of `traceId`; request to the E1-042/API owner (R18); TASK-19 checks the files unchanged |
| PG-E1-043-04 | RWB-E1-043 spec revision 10, SPEC-029; RWB-E1-042 section 7.1; Physical Schema v6 `parameter_catalog.description NOT NULL` | No description text exists for the 38 rows | E1-042 data-model section 2.1; PS6 lines 1386-1410; the spec's 38-row table | No | Documentation field only; no rule reads it | Plan-written one-line descriptions; `PA-E1-043-06`; TASK-04; R17 |
| PG-E1-043-05 | RWB-E1-043 spec revision 10, SPEC-002/SPEC-003 | No source fixes `table_code` case or case sensitivity; LOV codes are upper, handler codes lower, catalog keys lower | PS6 LOV seed; S7-001 `data_product`; S7-064 `sys_fields`; S7-019 `QUEUE`/`QUEUE_MEMBER` | No | Either reading stores a different string; no rule changes | Store exactly as supplied; lower-case the catalog key; exact matching; `PA-E1-043-03`; R19 |
| PG-E1-043-06 | RWB-E1-042 plan v2 "Tooling design" / `CatalogCompletenessRules`: a non-literal key is a finding | This story uses `ParameterKeys.byName("prefix." + code, Class)` for dynamic codes (SPEC-027, A-26); if the merged rule scans `byName`, the build fails | E1-042 plan v2 (the scanned forms do not include `byName`); spec A-26, SPEC-027 | No | Test-scope gate; no runtime behaviour; the plan must not change another story's gate unplanned | TASK-00 reads the merged rule; if it scans `byName`, stop and report; otherwise no change |

## 4. `aisdlc/docs/open-items.md`

| Change | Row |
|---|---|
| Keep OPEN-050 open | "OPEN-050 (owner: recovery tech lead): ratify D-RUN-18, D-RUN-19, D-RUN-20 and D-RUN-21. The RWB-E1-043 plan v1 (18 Nov 2026) applies them as orchestrator rulings and claims no ratification; the SPI placement, the LOV read, the `PARAMETER` branch and the one-module reading follow `plan.md` sections 'One-module check', 'Backend Plan' and `contracts/backend-apis.json`." |
| Add a note against the A-08 / A-31 / A-39 rows | "The RWB-E1-043 plan adds 37 Reference data grant rows and 26 per-table list rows from the spec's assumptions; no owner has accepted them. RWB-E1-037 replaces the grants file and the matrix; until then the file and the catalog are the only path." |
| Add a note against the GAP-43 row | "The plan's HV-E1043-01 is blocked on the 12 table contents; PRODUCT, REGION and EXPOSURE_BAND still have no named owner. The plan does not load any table content." |
| Add a note against the GAP-48 / GAP-53 rows | "HV-E1043-05 asks the API owner to retag the three operations to P3 and to add the 404/500 rows (and the 500 `traceId`, PG-E1-043-03). No code change is planned for either." |
| Add a note against the `sys_fields` / `is_personal` row (RW-COMPLY) | "The plan builds the registry and generic checks only; RWB-E1-064 must meet the `is_personal` requirement of SPEC-031. HV-E1043-03 is blocked on it." |
| Do not close | The 46 spec assumptions, the 59 gaps, CLAR-001..020's `RESOLVED_BY_ASSUMPTION` decisions and the 15 owner-acceptance items stay as the spec records them; none is answered by this plan |

## 5. Requests to document and story owners (no repository file edited)

| ID | Target | Request | Evidence |
|---|---|---|---|
| R1 | Engagement lead | Record the human ratification of D-RUN-08, D-RUN-10, D-RUN-11, D-RUN-12, D-RUN-18, D-RUN-19, D-RUN-20 and D-RUN-21, or keep them as unratified run rulings; OPEN-050 is the tracker | `plan.md` status; `assumptions.md` PA-E1-043-18 |
| R2 | Recovery tech lead | Confirm A-33 (the `reference_version` trigger exempts only the eight columns; `is_active`, `state`, `created_at`, `created_by` frozen) | SPEC-001; `data-model.md` section 4 |
| R3 | RW-COMPLY | Confirm the `sys_fields` `is_personal` protection requirement and the governed path that may change a mark (GAP-38; SPEC-031) | `plan.md` "Security, privacy and compliance"; HV-E1043-03 |
| R4 | RWB-E1-064 owner | Register a `sys_fields` handler of type `access.api.ReferenceTableHandler` (`dating()` = `CURRENT_STATE`), seed `rwb.refload.loader/approver.sys_fields`, refuse an `is_personal` change and never write it (SPEC-031; GAP-38, GAP-55) | `plan.md` "Out of scope"; `contracts/backend-apis.json` `handlerContract` |
| R5 | RWB-E1-001 owner | Register a `data_product` handler (`CURRENT_STATE`, `keyColumns` `product_code`, repeat message MSG-P1-011, no `refdata.columns.data_product`, defaults RW-REFADM/RW-DATASTEW); add its two list keys and its message IDs | SPEC-025; A-40; GAP-44, GAP-54; TC-HD-03 |
| R6 | RWB-E1-042 owner | Keep the published names of `casewf.config.api` and `access.api` stable (A-25); this story consumes `ParameterService`, `ParameterKeys.byName`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider`, `MessageResolver`, `CapabilityCheck`, `ApiProblemException`, `ApiError` | `plan.md` "Plan-time checks" 3; `contracts/backend-apis.json` `consumedInterfaces` |
| R7 | Access owner and Risk | Accept or change A-31 (default loader/approver lists) and A-39 (no load may carry an `rwb.refload.*` key; the lists change by a reviewed catalog change until RWB-E1-037) | SPEC-027, SPEC-029; `data-model.md` section 8 |
| R8 | RWB-E1-022 owner | Replace `ActorIdResolver` with the session user; confirm the `oid`-then-`sub` rule (A-07) | SPEC-015; SEC-16; HV-E1043-02 |
| R9 | RWB-E1-039 owner | Replace `LoggingReferenceLoadAudit` with the access log and its AC-DENY entry; the refusal is not attributable to an actor until then (GAP-42) | SPEC-028; A-30; R20 |
| R10 | QA lead and the 12 table owners | Provide version 1 content and definitions for the 12 tables before the release SIT exit (GAP-43); PRODUCT, REGION and EXPOSURE_BAND have no named owner | SPEC-022; HV-E1043-01 |
| R11 | RWB-E1-019 owner | Implement the QUEUE and QUEUE_MEMBER handlers on the P4 SPI, declare `dating()`, and keep or replace `QueueVersionApplier` (A-42, A-46; GAP-58) | SPEC-025; `contracts/backend-apis.json` `p4HandlerSpi` |
| R12 | RWB-E1-027 owner | Replace `LoggingReferenceDecisionRecorder` with a call to P7 `DecisionLogWriter` (A-43) | SPEC-008; TC-DR-01 |
| R13 | RWB-E1-037 owner | Replace the interim `CapabilityCheck` and the grants file; decide the A matrix, including RW-DATASTEW (A-08; GAP-14, GAP-46) | SPEC-027 |
| R14 | RWB-E1-069 owner | Deliver the `v_ace_batch_status` reader; the real `BusinessDateProvider` returns the greatest `business_date` with `is_complete = true` (A-01) | SPEC-017; GAP-12 |
| R15 | RWB-E1-011 owner | Add the load result to the daily data quality report if that story's scope allows (GAP-33) | S7 section 15; `plan.md` "Out of scope" |
| R16 | Message owner | Confirm `MSG-P4-003` wording for an unknown load (GAP-27) and the MSG-P3-027 text used for the no-version alert (GAP-05) | SPEC-020; GAP-27 |
| R17 | Catalog owner | Review the 38 new catalog rows and their descriptions; every row is a reviewed change (E1-042 section 7.1; A-09) | SPEC-029; PG-E1-043-04 |
| R18 | API owner | Retag the three operations from P4 to P3 (GAP-53); add the 404 (flag off) and 500 (handler defect) rows (GAP-48); consider the 500 `traceId` (PG-E1-043-03) | `contracts/backend-apis.json`; `plan.md` "API change assessment" |
| R19 | Data owner | Confirm the `table_code` case/matching rule (PG-E1-043-05) and the current-state reading of `data_product` and `sys_fields` (GAP-54, GAP-55; A-42) | `data-model.md` sections 2 and 9 |
| R20 | DPO | Confirm that author/approver IDs are personal and must stay out of logs and audit events; backend context v2.0 line 138 conflicts (GAP-42; A-30) | SPEC-028; `data-model.md` section 10 |
| R21 | RWB-TE-001 owner | Confirm the `[TE-001]` module map and `RecoveryBoundaryTest` shape this plan extends; T-TE001-14's expected sets are extended, nothing removed | `plan.md` "Plan-time checks" 1 and 14 |
| R22 | Plan gate (orchestrator) | Check the one-module reading under D-RUN-21: P3 `casewf.refdata` plus additive P4 `access` is one ACE module (recovery); no analyst referral; no tech-lead approval claimed | `plan.md` "One-module check"; GAP-59 |
| R23 | RWB-E1-044 owner | Confirm the identifier-only, quote-aware `RecoveryMigrationLintTest` is the merged one (T-044-21); the seed's `recovery.casewf.refdata` strings depend on it | `plan.md` "Plan-time checks" 2; PRE-2 |
| R24 | Recovery tech lead | Ratify D-RUN-18 (SPI in `access.api`), D-RUN-19 (parameter reads through `access.api`), D-RUN-20 (`PARAMETER` branch) and D-RUN-21 (one ACE module); OPEN-050 | `plan.md`; `contracts/backend-apis.json`; GAP-36, GAP-51, GAP-53, GAP-57, GAP-59 |
| R25 | RWB-E1-028 and RWB-E1-072 owners | Consume `ReferenceDataReaders.forReader` and `NoVersionInForceException`; record the version used with each decision | SPEC-012, SPEC-014; A-02 |
| R26 | RWB-E1-064 owner | See R4; the `is_personal` rule is the owning story's, not this story's | SPEC-031; GAP-38 |
| R27 | RWB-E1-038, RWB-E1-045, RWB-E1-046 owners and Legal | Provide the DELEGATION_LIMIT, PRODUCT_PARAMETER/SERVICE_LEVEL, TEMPLATE and LEGAL_PERIOD content and definitions before the release SIT exit | SPEC-022; GAP-43 |
| R28 | `AGENTS.md` owner | Define "module" in sections 7 and 9; GAP-59 stays recorded even though D-RUN-21 settles this build | GAP-59; `plan.md` "One-module check" |
| R29 | RWB-E1-042 owner and the plan gate | The T-TE001-14 expected sets are RWB-E1-042's merged set plus this story's six `access.api` entries, `ReferenceTableHandler.Dating` and the six `casewf.refdata.api` types; if E1-042 merges a different set, add the same entries to that set | SPEC-019; `RecoveryBoundaryTest` plan; `plan.md` "Plan-time checks" 14 |
| R30 | RWB-E1-019 owner | The orchestrator's triage of 2026-11-18 05:52:36 answers R33: a P3 handler may implement the P4 SPI; `PARAMETER` remains a dispatcher branch (A-46; GAP-58) | SPEC-025; `contracts/backend-apis.json` |
| R31 | Data owner and RWB-E1-064 owner | Record the `CURRENT_STATE` decision for `data_product` and `sys_fields` and the one-approved-version-per-date rule (GAP-54, GAP-55; A-42) | SPEC-032; TC-TM-05 |
| R32 | Orchestrator | Record that D-RUN-20's answer is applied (the P4 SPI is for handlers outside the registry's module; `PARAMETER` is a dispatcher branch) | SPEC-025; GAP-57 |
| R33 | Orchestrator | Record that the 2026-11-18 05:52:36 triage answers R33 (P3 handlers may implement the P4 SPI) | SPEC-019, SPEC-025; GAP-58 |

## 6. Notes

- No shared file, code file or build log was edited by this stage. `aisdlc/docs/open-items.md`, `aisdlc/requirement/Traceability_Matrix.md`, `aisdlc/docs/increments/INDEX.md`, the increment card and `aisdlc/DOCUMENT-GAPS.md` are the orchestrator's to change.
- The spec stage's `specify/shared-updates.md` revision 10 already carries R1..R40 and sections 3.1-3.6; this file does not duplicate them and does not renumber them. Where an ID collides, the spec stage's row keeps its number and the orchestrator maps the plan row by its target and content.
- No row claims a human approval, a ratification of D-RUN-18..21, or the acceptance of A-01/A-07/A-08/A-09/A-16/A-17/A-27/A-31/A-33/A-34/A-37/A-38/A-39/A-40/A-41/A-42/A-43.
