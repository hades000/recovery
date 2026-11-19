# Plan gate review, round 1: RWB-E1-069, read-only ACE source views, grants and boundary rule

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-069-PG1` (first plan gate for this RUN_ID) |
| RUN_ID | `INC-010-epic-1-RWB-E1-069` |
| Stage | Plan gate, round 1 |
| Artefacts | `aisdlc/output/INC-010-epic-1-RWB-E1-069/plan/`: `plan.md` v1, `tasks.md`, `data-model.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `tests/scenarios.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `agent-run-log.md` |
| Gated spec | `../specify/spec.md` revision 4, spec gate round 4 `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-4.md`) |
| Story | Story RWB-E1-069 v1, Epic 1 Story Files v7, 15 Nov 2026 |
| Reviewer | Compliance Reviewer (plan gate), read-only |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 3 Medium, 6 Low: `PLAN-001`..`PLAN-009` |
| Handoff | **Blocked.** The Implementation Planner remediates every finding and the plan gate is re-run (D-RUN-09). |

## 1. What was checked

**Rules applied.** `.claude/agents/compliance-reviewer.md` (plan-gate mode), `aisdlc/RUN-BRIEF.md` (hard rules 1-8; D-RUN-07, D-RUN-08, D-RUN-09, D-RUN-12, D-RUN-14, D-RUN-17, D-RUN-21), `aisdlc/.github/rules/` (`planning-execution-gates.md`, `implementation-execution-gates.md`, `pdlc.md`, `security-quality-standards.md`, `traceability-standards.md`), the contexts `backend-context.md`, `backend-standards.md`, `testing-standards.md`, and `AGENTS.md` (Recovery Workbench standards v2) §3, §4, §7 and §9.

**Method.** The plan set was read in full, then each claim that bears on the gate was checked against the live file or the live dependency instead of the planner's summary:

- Spec revision 4 (`../specify/spec.md`): all 20 SPEC items, the 42 `Requirement-to-SPEC Logic Coverage` rows, the 31 AC clauses, BR1..BR9, the two additional rows (§4 step 2, §17 guardrails), the 30-view field ranges, the four extension tables, SPEC-012 BND-6, SPEC-018 X2, SPEC-019 data protection, the unit-test row and the Status block.
- Story RWB-E1-069 v1: AC1..AC8, BR1..BR9, §3, §4, §11, §12, §13, §14, §16, §17, §19.
- Live dependencies: RWB-E1-044 plan v2 (`architecture/migration/rule/` package), RWB-E1-001 spec Revision 4 (`SPEC-003`: 89 tables including the four extension tables; the T8 four belong to E1-042/E1-043), RWB-TE-001 plan v7 and spec v4 (`architecture.boundary`, opaque `sourceViews`), and the current `backend/build.gradle.kts` (one JaCoCo bundle; LINE/INSTRUCTION/BRANCH/METHOD at 0.80; execution data from `test`).
- Code and document baselines, read only: `RecoveryBoundaryTest.noRecoveryClassNamesAPublicTable` (line 196, line scanner), `RecoveryDatabaseIT` (S1 `true`; `version = '0'` assertion), `ModuleMap`/`ModuleMapLoader` (opaque `sourceViews`), `20-grants.sql.inc` (line 12 `ALL TABLES`, line 61 function default privilege naming `ace_view_owner`), `10-load-ace-database.sh` (probe and S1 branch; no S2 branch yet), `02-ace-tier2-probe.sql` (14 tables, 12 columns), `01-ace-schema-v1.sql` (all 21 Tier 1 tables present), and ACE Source Views v1 lines 94-711 (30 views; `v_ace_contact` is a `UNION ALL` of phone, email and address; `v_ace_plan` reads `ai_recommended_plan` in a `LEFT JOIN LATERAL`).
- No Gradle run, container or database was started; no git command was run. This is a plan-gate text and file inspection.

**Independent counts.** 42 spec rows and 42 plan rows (no `BLOCKED`); 20 SPEC items each mapped to a task; 20 tasks (TASK-00..TASK-19) each with Description, Files, Trace, `BLOCKED_BY` and Verification; 12 scope bullets S-1..S-12 each mapped; 31 AC clauses, 9 BRs and the two extra rows each mapped to a named test; 18 test IDs; 12 exceptional cases X1..X12; 2 migrations (`V<seq>__rwb_e1_069_ace_source_views.sql`, `V<seq>__rwb_e1_069_ace_tier2_views.sql`); 30 views (16 Section A, 14 Section B); 177 + 127 = 304 fields; four extension tables 12 / 14 / 9 / 14 = 49 columns; 80% on four counters; 30 document gaps `DG-L01`..`DG-L30` and 3 planner gaps `DG-P01`..`DG-P03`, all Blocker = No.

## 2. Findings

### PLAN-001 - Medium - The plan's "complete" test-scope inventory omits two required test classes

**Evidence.** `plan.md` "Files added or changed - test scope, fixtures and test data (complete list)" (lines 140-164) does not list `T/architecture/migration/MigrationSeamRulesTest.java` or `T/architecture/migration/LintExceptionsLoaderTest.java`. `tasks.md` TASK-03 (line 29) names both as files it writes, and its verification runs `--tests "*MigrationSeamRulesTest" --tests "*LintExceptionsLoaderTest"`. The same omission is in `plan.md` "Smallest change" (line 22), which counts one conformance test class, one conformance-target reader, one `sourceViews` reader and three BND-6 tooling classes, but no seam test class and no exception-loader test.

**Why it matters.** `AGENTS.md` v2 §9 "Plan approved" requires the plan to name every file, test and migration. `TASK-19` (1) then requires the diff to touch only the files in `plan.md` "Files added or changed". A Builder that writes the two tests TASK-03 requires would fail the plan's own scope check; a Builder that omits them would fail TASK-03's verification.

**Required fix.** Add both classes to the test-scope table with task TASK-03, and to "Smallest change"; state that they are test classes outside the 80% measured bundle.

### PLAN-002 - Medium - The lint rule paths and the exception-class package are inconsistent with RWB-E1-044 plan v2

**Evidence.** `plan.md` line 161 and `tasks.md` TASK-04 (line 30) name the edit targets `T/architecture/migration/LiteralSchemaRule.java`, `GrantRule.java` and `KeyDuplicateRule.java`. RWB-E1-044 plan v2 line 147 places all 15 rule classes, including these three, in `T/architecture/migration/rule/`. `tasks.md` TASK-00 (line 26) already uses the correct `T/architecture/migration/rule/LiteralSchemaRule.java`. `plan.md` line 161 also says `LintExceptions.java` and `LintExceptionsLoader.java` go "in the same package" as the rules, while `tasks.md` TASK-04 puts them in `T/architecture/migration` (the parent). `LintExceptionsLoaderTest` is planned in the parent.

**Why it matters.** A Builder following the file table would edit paths that do not exist, or create duplicate classes outside the shipped rule package; the seam would not be applied at the shipped extension point. `TASK-00` and `TASK-04` would point at different files. `TASK-19`'s diff check would flag the actual `rule/` edits as out of scope.

**Required fix.** Correct the three rule paths to `T/architecture/migration/rule/...` in `plan.md` and TASK-04; state one exact package for `LintExceptions`, `LintExceptionsLoader` and `LintExceptionsLoaderTest` (parent `architecture.migration` if that is the intent), and align TASK-00, TASK-03, TASK-04 and TASK-16 to it.

### PLAN-003 - Medium - The BND-6 table-to-view map cannot resolve the UNION and LATERAL sources it must name

**Evidence.** `plan.md` line 229 and `data-model.md` line 150 define the map as "the view whose top-level `FROM` names the table, otherwise the views that `JOIN` it". ACE Source Views v1 lines 198-234 define `v_ace_contact` as `SELECT ... FROM public.phone UNION ALL SELECT ... FROM public.email UNION ALL SELECT ... FROM public.address`; `email` and `address` are neither a top-level `FROM` nor joined to the other branches. ACE Source Views v1 lines 439-448 read `public.ai_recommended_plan` inside a `LEFT JOIN LATERAL`. `tasks.md` TASK-12 (line 38) and `data-model.md` line 150 require `phone`, `email` and `address` to give `v_ace_contact`; the plan's map can give that only for `phone`.

**Why it matters.** `Bnd6RuleTest` at TASK-12 asserts the three mappings, and TASK-13's verification is that the test is green. With the stated rule the `email` and `address` assertions fail, and the message for `ai_recommended_plan` falls back to the generic text. The Builder would have to change the map (not planned) or weaken the test (forbidden by `AGENTS.md` §4.5). The gated spec's SPEC-012 names `phone`, `email` and `address` -> `v_ace_contact` explicitly, so the map is the part that must change.

**Required fix.** Define the map over every SELECT branch of a `UNION`/`UNION ALL` and every nested `FROM` (including `LATERAL`), not only the first top-level `FROM` and top-level `JOIN`; add `email` and `address` fixture assertions (and, if useful, `ai_recommended_plan` -> `v_ace_plan`), or state the exact derivation that yields the required examples.

### PLAN-004 - Low - TASK-00's hard stop on E1-001 seed totals contradicts PA-E1-069-11 and the spec

**Evidence.** `tasks.md` TASK-00 (line 26) says "**Stop and report** if any of (1)-(3) is absent or if the E1-001 seed differs from 123 / 1,382 / 1,078 / 49 / 526". `assumptions.md` PA-E1-069-11 (line 17) says "If the merged RWB-E1-001 file seeds different totals, TASK-09 records the actual values, the test asserts those, and the difference is reported to the orchestrator as a spec-input change." `spec.md` SPEC-010 last bullet (line 198) says the test "asserts what that file seeds and the plan records the change".

**Why it matters.** The same condition has two dispositions: one stops the Builder, the other records a deviation and continues. The spec's disposition is the later, gated one.

**Required fix.** Make TASK-00 record the seed counts and proceed with a deviation note (per PA-E1-069-11 and SPEC-010), keeping the stop for absent files, classes or the S2 branch only; or, if a stop is intended, change PA-E1-069-11 and the spec reference accordingly. One disposition per condition.

### PLAN-005 - Low - TASK-08's full-state totals conflict with TASK-09's A-only green state

**Evidence.** `tasks.md` TASK-08 (line 34) requires `ViewConformanceTest` to assert "views 30 / 304 / 177 / 127" and "`is_personal` 304 non-null, 250 true, 54 false". TASK-09 (line 35) must be green "for the Section A state (16 views; the Section B assertions assert absence)". `assumptions.md` PA-E1-069-17 (line 23) says only the view count and the Section A/B split are derived from the migration folder plus `sourceViews`; it does not say how the dictionary totals or the `is_personal` counts switch between the A-only and A+B states.

**Why it matters.** If the class hard-codes 30 views, 304 fields, 250 true and 54 false, TASK-09's green gate fails because only 16 views and 177 fields exist. If it does not, TASK-08's written instruction is unmet. The planner has the right idea in PA-E1-069-17 but has not applied it to every count.

**Required fix.** State the A-only expected values (16 views, 177 Section A fields, 177 `is_personal` rows for the present views) and the A+B values (30, 304, 177 + 127, 250 true and 54 false), and make the Section B-dependent assertions conditional on the Section B file or add them in TASK-10/TASK-11.

### PLAN-006 - Low - TASK-14's stated red reason contradicts its own S2 setting

**Evidence.** `tasks.md` TASK-14 (line 40) rewrites the container environment to S2 `false`, then says the red is "with S2 still `true` the views come from the Physical Schema v6 stand-in". With `RWB_LOAD_REFERENCE_VIEWS=false` the S2 branch does not run; the schema is empty at init, so init creates no views, and after Flyway only the 16 Section A views exist. The test's first failure is the 30-view assertion or the per-file history assertion, not the S2 stand-in.

**Why it matters.** The recorded red evidence would not match the test's actual first failing assertion, and the Builder's test-first record would be misleading. It is not a blocker because the test is red either way.

**Required fix.** Correct the expected red reason to the S2 `false` state (no `v_ace_*` view from init; the 30-view assertion and the per-file history assertion fail; the baseline row is absent).

### PLAN-007 - Low - The scope paragraph misstates the E1-001 table set

**Evidence.** `plan.md` line 61 says "the four extension tables and the 92 PS v6 tables belong to the RWB-E1-001 migration". RWB-E1-001 spec Revision 4 SPEC-003 (lines 232-237) says E1-001 creates 89 tables **including** `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`; the T8 four (`parameter_catalog`, `parameter_value`, `reference_version`, `reference_row`) belong to E1-042/E1-043; with T8 the schema holds the 93 PS v6 tables.

**Why it matters.** The D-RUN-12 conclusion (E1-069 creates no table) is correct, but the ownership count is wrong. A reader checking D-RUN-12 against this sentence would look for 92 tables plus four extension tables, which does not match either spec.

**Required fix.** Say "the four extension tables are among the 89 tables the RWB-E1-001 migration creates; the four T8 tables belong to RWB-E1-042/E1-043; E1-069 creates no table".

### PLAN-008 - Low - `shared-updates.md`'s proposed SPEC-to-test rows disagree with `plan.md`

**Evidence.** `shared-updates.md` line 25 gives SPEC-002 as TASK-09 only; `plan.md` line 412 gives TASK-08, -09. `shared-updates.md` line 40 gives SPEC-017 as TASK-08, -09, -14; `plan.md` line 427 gives TASK-08, -09, -10, -11, -14.

**Why it matters.** The orchestrator applies these rows to `Traceability_Matrix.md`. The matrix would under-report the tasks that implement and verify SPEC-002 and SPEC-017, and the plan set would disagree with its own shared proposal.

**Required fix.** Align the SPEC-002 and SPEC-017 rows in `shared-updates.md` with `plan.md` "SPEC to task map" (TASK-08, -09 and TASK-08, -09, -10, -11, -14 respectively), or change `plan.md` and the test map consistently.

### PLAN-009 - Low - The data model's per-view source-table column omits joined sources

**Evidence.** `data-model.md` lines 20-35 list `v_ace_account` as `public.account` only, `v_ace_payment` as `public.payment` only, `v_ace_collateral` as `public.collateral` only, `v_ace_bucket_log` as `public.bucket_log_snapshot` only, and `v_ace_plan` without `public.account`. ACE Source Views v1 lines 139-141 join `public.product` and `public.branch` in `v_ace_account`; lines 162-163 join `public.account` in `v_ace_payment`; lines 276-277 join `public.asset` in `v_ace_collateral`; lines 369-370 join `public.account` in `v_ace_bucket_log`; lines 439-442 join `public.account` in `v_ace_plan`.

**Why it matters.** The `AceTableCatalog` derives the ACE table set from the SQL (the plan says so), so the build is not wrong; but the data model is the plan's stated source-table map and is incomplete for five views. The plan's own `data-model.md` section 8 relies on the full 35-name qualifier set, so a reader reconciling the two sections sees a contradiction.

**Required fix.** List every `public.<table>` qualifier per view in the "Source table(s)" column, or label the column "primary source" and add the complete join list; keep the 21 Tier 1 / 14 Tier 2 count.

## 3. Coverage table

| # | Check | Evidence | Result |
|---|---|---|---|
| 1 | Gated spec revision and upstream readiness | `../specify/spec.md` revision 4; spec gate review-4 `PASS` 0/0/0/0; `Status: SUCCESS`; `REQUIREMENT_COVERAGE_RESULT` 42/0/0; `CLARIFICATION_STATUS: NOT_REQUIRED`; no `CLAR-*`; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` | PASS |
| 2 | 42/42 requirement rows | Spec `Requirement-to-SPEC Logic Coverage` 42 rows; `plan.md` 42 rows; all `COVERED`; no `BLOCKED`; `PLAN_REQUIREMENT_COVERAGE_RESULT` 42/42, 0 missing, 0 ambiguous, 0 contradictions | PASS |
| 3 | 30 views and field split | 16 Section A + 14 Section B = 30; 177 + 127 = 304; `data-model.md` section 1 re-counted against ACE Source Views v1 lines 94-711 and story section 11 | PASS |
| 4 | Four extension tables | `party_ext` 12, `contact_point_ext` 14, `account_ext` 9, `valuation_ext` 14 = 49; created by the RWB-E1-001 migration; E1-069 creates none (D-RUN-12); `plan.md` line 61 wording is wrong (PLAN-007) | PASS with PLAN-007 |
| 5 | BND-6 | Detectors (a)-(d); allowed names from `sourceViews`; ASM-013 exemptions; eight fixtures; failure text; default `test` task; `RecoveryBoundaryTest` body only. The table-to-view map is defective for `UNION ALL` and `LATERAL` sources (PLAN-003) | PASS with PLAN-003 |
| 6 | Tier 2 probe stand-in (RWB-ACE-001) | ASM-005, DG-L16, DG-L20, OI-069-D; `RWB_ACE_TIER2_PROBE` default `true`; 14 probe tables and 12 columns; Section B merges only after RWB-ACE-001 is deployed; **Blocker = No** | PASS |
| 7 | Two migration placeholders | `V<seq>__rwb_e1_069_ace_source_views.sql` and `V<seq>__rwb_e1_069_ace_tier2_views.sql`; line 1 `-- Story: RWB-E1-069`; no fixed number in any plan file; A then B; contiguous at merge (D-RUN-07) | PASS |
| 8 | 80% x4 unit gate | LINE, INSTRUCTION, BRANCH and METHOD at 0.80, one bundle: recovery main classes plus `architecture/boundary/**` and `architecture/migration/**`; `test`-task execution data; per-class 80% for new/changed tooling; `RecoveryFlywayTestSupport` outside the claim | PASS |
| 9 | No human approval or ratification | `plan.md` line 445; `tasks.md` line 96; `assumptions.md` ASM-016 and PA-E1-069-15; `data-model.md` line 103; D-RUN-14 is the orchestrator's, OI-069-M / OPEN-051 open; D-RUN-21 and OPEN-050 unratified; no approval claimed | PASS |
| 10 | D-RUN-07 | Two migration names with `V<seq>`; 0 occurrences of a fixed `V` plus four digits in the plan files; lint fixtures carry test data numbers only; versions read from file names (SPEC-017) | PASS |
| 11 | D-RUN-12 | E1-069 creates no table; the four extension tables are E1-001's; E1-042/E1-043 tables are not recreated; the two files create views, helpers and grants only | PASS with PLAN-007 |
| 12 | D-RUN-14 | `rwb_migrator`: `USAGE ON SCHEMA public`, no table privilege, `ace_view_owner` with `WITH INHERIT FALSE, SET TRUE`, no ACE DBA role; SELECT grants to `ace_view_owner` stay with the ACE DBA; local init is the stand-in only | PASS |
| 13 | D-RUN-17 | TE-001 v4 package layout (`casewf.migration`, `architecture.boundary`); E1-069 order 10 after E1-001 (order 9) and E1-044 (order 1); TASK-00 stops if either merge is absent | PASS |
| 14 | D-RUN-21 | "one module" read as the ACE recovery module; all touched test-scope packages are under `th.co.scb.ace.demo.recovery`; no `common` or `collection` change; PA-E1-069-15 and OPEN-050 | PASS |
| 15 | Plan structure and task completeness | `## Requirement Logic To Task Coverage` with the required columns; 20 tasks; every task has Description, Files, Trace, `BLOCKED_BY`, Verification; `## Pre-submit checks` all `[x]`; status lines present | PASS |
| 16 | SPEC/AC/BR/TC/scope mapping | 20/20 SPEC items; 31 AC clauses and 9 BRs plus the two extra rows; 18 test IDs; 12 scope bullets; 12 X cases; 6 NFR rows; no orphan and no dangling `TASK-*` | PASS |
| 17 | AGENTS.md §7/§9 file, test and migration naming | Two migrations named; production list complete; test-scope "complete" list omits two test classes (PLAN-001); three rule paths wrong (PLAN-002); one module verified | FAIL with PLAN-001, PLAN-002 |
| 18 | Shared files and governance | No shared file edited by the planner; `shared-updates.md` carries the matrix, INDEX, card, open-items, DOCUMENT-GAPS and build-log proposals; SPEC-002/SPEC-017 rows drift from `plan.md` (PLAN-008); no question to the user | PASS with PLAN-008 |
| 19 | Personal data, secrets and data protection | Synthetic values only (`ACC0000017`, `P0000123`, `X000000005678`, container passwords); no real name, ID, account or address; external-mode credentials are pipeline variables only; no credential in code; SPEC-019's 12 Restricted fields are in scope and TASK-19 records them in the evidence; `is_personal` 250/54 among the 304 | PASS |
| 20 | Frontend/backend applicability | Backend `REQUIRED`; frontend `NOT_APPLICABLE` with UI In Scope NO, story section 15, unchanged `platform.ts` and `npm run check` in TASK-18; no frontend task; `frontend/components.md` not required | PASS |

## 4. Gate result

`GATE_RESULT: FAIL` - 0 Critical, 0 High, 3 Medium, 6 Low.

The plan is strong on the gated content: the spec revision 4 upstream is `PASS` 0/0/0/0; the 42 requirement rows are all present and `COVERED`; the 30 views and 304 fields are counted; the four extension tables are correctly inherited from RWB-E1-001; BND-6's detectors, allow-list and exemptions are planned; RWB-ACE-001 is the Tier 2 probe stand-in with Blocker = No; the two migration placeholders and their line 1 are correct; the 80% LINE/INSTRUCTION/BRANCH/METHOD gate is planned at bundle and class level; D-RUN-07/12/14/17/21 are applied as recorded; and no human approval or ratification is claimed (OI-069-M / OPEN-051 remain open, OPEN-050 unratified).

The three Medium findings are plan-integrity defects that would break the plan's own execution or the "Plan approved" gate: two required test classes are missing from the complete file list, three lint rule paths and the exception-class package disagree with the shipped RWB-E1-044 layout, and the BND-6 table-to-view map cannot derive two of the required `v_ace_contact` mappings. The six Low findings are internal-consistency and documentation defects. No finding re-opens the gated spec or changes a grant, a view body, a test target or a blocker value.

**NEXT_STEP:** Implementation Planner remediation run 2 (plan v2) addressing `PLAN-001`..`PLAN-009`, then plan gate round 2. Under D-RUN-09 the orchestrator does not accept a Low-only failure; all nine findings are to be fixed.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 3] [LOW: 6]
