# Plan gate review, round 1: RWB-E1-001 Recovery tables for the 14 data products

| Item | Value |
|---|---|
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Gate | PLAN GATE (Compliance Reviewer, round 1) |
| Reviewed | `plan/plan.md`, `tasks.md`, `data-model.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `tests/scenarios.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `agent-run-log.md` |
| Against | Gated spec revision 4 (`specify/spec.md`; spec gate round 4 `PASS` 0 Critical / 0 High / 0 Medium / 0 Low, `review/spec-gate-review-4.md`), Story v7 (`.../rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md`), the document set, `planning-execution-gates.md`, `implementation-execution-gates.md`, `AGENTS.md` §7/§9, `RUN-BRIEF.md`, and decisions D-RUN-07/-09/-12/-17/-21 in `AI-SDLC-BUILD-LOG.md` |
| Instructions | `.claude/agents/compliance-reviewer.md`; `aisdlc/RUN-BRIEF.md` |
| Date | 18 November 2026 |
| Reviewer | Compliance Reviewer (agent run); no human approval is claimed or implied |

## Overall status

**STATUS: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 12 |

The plan is technically strong: 33/33 requirement rows, the 89-table set exactly matches Physical Schema v6 minus the four D-RUN-12 tables, the 526 personal marks and the DP07 blocker are carried visibly, and the one-migration rule is correctly left unfixed. It fails this round because two plan statements cannot hold on the merged base the plan itself requires (the migration folder is not empty) and one rollback statement is not viable after the migration is applied. The remaining findings are evidence, traceability and test-detail defects.

## Findings

### PLAN-001 — Medium — PRE-2, TASK-00 and TASK-03 assert an empty / single-file migration folder that the plan's own base contradicts

**Evidence.** `plan.md` "Preconditions" PRE-2 says the merged base proof is "migration folder holds `README.md` only" (`plan.md` line 99). `tasks.md` TASK-00 item (3) says "No `.sql` in `M/db/modulemigration/recovery/`; no `<seq>` inferred" (line 55), and TASK-03's verification says "the file is the only `.sql`" (line 58). The plan itself requires PRE-3 (E1-042 merged) and PRE-4 (E1-043 merged) (`plan.md` lines 100–101), and `data-model.md` § 1 says the sequence is "after the RWB-E1-042 and RWB-E1-043 files" (line 35). Both earlier stories add a migration in that same folder: RWB-E1-042 `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` (`INC-003` plan, line 213) and RWB-E1-043 `V<seq>__rwb_e1_043_reference_versions.sql` (`INC-008` spec, "New Nodes Required"). On the base the plan requires there are therefore at least two `.sql` files, not "README.md only" and not "the only `.sql`". `plan.md` "Preconditions" also says "a precondition that is absent or different stops the build; the plan is not silently adapted" (lines 93–94), so the false proof can stop or misdirect the first task.

**Required fix.** Change PRE-2's proof and TASK-00 item (3) to: "the folder holds `README.md` plus the RWB-E1-042 and RWB-E1-043 migration files; no RWB-E1-001 file exists before TASK-03; the next contiguous `<seq>` is free and is not fixed (D-RUN-07)". Change TASK-03's verification to "this story's file is the only new `.sql`; the earlier-story files are unchanged".

### PLAN-002 — Medium — the stated tag-revert rollback is not viable after the migration has run

**Evidence.** `plan.md` "Release and rollback" says "Rollback: turn the flag off, or revert the merge request. The previous tag ignores the new tables; Flyway `clean` stays disabled" (line 603). But the migration is forward-only and has already written `flyway_schema_history_recovery`; a previous tag does not carry the E1-001 file. RWB-E1-044 adds `validateOnMigrate(true)` (`INC-001` plan, line 125) and leaves `ignoreMigrationPatterns` at Flyway's `*:future` default (`INC-001` plan, line 190), so a previous tag would fail Flyway validation with an applied migration not resolved locally. TASK-19 writes the release note item from this section (`tasks.md`, line 74), so the unsafe route can reach operations.

**Required fix.** State that a tag revert after the migration has run does not remove the schema and would fail Flyway validation; the supported rollback is flag-off (the previous code path) or a forward corrective migration. If a tag revert is required, say the migration file must remain in the tag or the revert is not a rollback; do not add `ignoreMigrationPatterns` as a workaround (it weakens the gate).

### PLAN-003 — Low — the SPEC-012 repository method "find all active" is missing

**Evidence.** SPEC-012 requires `DataProduct` and `DataProductRepository` "(find all active, find by product_code)" (`spec.md` line 399). `plan.md` lists only `findAllByProductCodeIn(Collection<String>)` and `findByProductCode(String)` (`plan.md` line 202); no `findAllByIsActiveTrue()` or equivalent appears in `tasks.md` or the tests.

**Required fix.** Add the active-read method and a unit test, or record why it is not required and obtain the spec owner's agreement (a plan-stage `PG-*` row is not enough to drop a named spec surface).

### PLAN-004 — Low — TC-E1-001-16's "second bean fails start-up" case is not planned

**Evidence.** The gated spec's TC-E1-001-16 includes "a second bean for `data_product` fails start-up" and marks the case "This story" (`spec.md` line 739). `tasks.md` TASK-08 and `tests/scenarios.md` T-E1001-16 plan only `beanExistsWhenFlagOn`, `noBeanWhenFlagOff` and `noParameterHandlerBean` (`tasks.md` line 63; `tests/scenarios.md` line 41); the plan says "a second handler for the same code is E1-043's test, not duplicated" without naming that test.

**Required fix.** Name the E1-043 registration/duplicate-code test that proves the case, or add the `ApplicationContextRunner` case here. Do not leave a gated TC clause with no named owner.

### PLAN-005 — Low — the `DF-REF-076` Inventory v4 citation is factually wrong

**Evidence.** `data-model.md` § 13 says `data_product.owner_user_id` "is personal by the protective reading (DF-REF-076 has no Inventory v4 row; the same pattern is personal elsewhere)" (line 426). The PDPA Inventory v4 has `| DF-REF-076 | data_product | owner_user_id | Staff identifier | Internal | Yes | ...` and the union fixture records the row's source as `INVv4` (`specify/evidence/is_personal_union_v4.tsv`). The classification and the 526 set are correct; the parenthetical is not.

**Required fix.** Replace the parenthetical with the Inventory v4 row (Staff identifier, Internal, Personal data = Yes) as the source of the union mark.

### PLAN-006 — Low — the fixture shape and the owner-UUID statement disagree

**Evidence.** `data-model.md` § 15 says the personal-field fixture is "526 field IDs ... field IDs only" (line 484), while `plan.md`'s file table says "(field IDs and metadata only)" (line 238) and `PA-E1001-12` says "field IDs plus object/field metadata (the ... columns)" (line 34). Separately, `data-model.md` § 13 says "the owner UUIDs are generated per test (`UUID.randomUUID()`)" (line 432), while `valid-14-rows.csv` is a static fixture with "synthetic owner UUIDs" (line 485) and the repeat case requires the same bytes.

**Required fix.** State one fixture shape (field IDs plus object/field metadata for TE-011's `(object, field)` match, with the mark comparison by field ID), and say whether the owner UUIDs are fixed synthetic values in the CSV or generated into it at test time. The repeat case must use identical bytes.

### PLAN-007 — Low — TASK-16's earlier-story IT edits are not named by exact path

**Evidence.** `tasks.md` TASK-16 says "the earlier-story IT files only if TASK-00 found an S1=`true` container" and "the earlier-story IT files only if..." (line 71); `PG-E1001-06` names "E1-042's `TC-E1-042-14` and E1-043's PS v6 baseline IT" but no file path (`document-gaps.md` line 30). The spec says those ITs must move (`spec.md` SPEC-010), so TASK-00 will find them. The plan's "Files added or changed" table does not name them.

**Required fix.** Name the exact E1-042 and E1-043 IT file paths in the file table and TASK-16, or restrict TASK-16 to "none found" with the TASK-00 evidence that no S1=`true` container exists.

### PLAN-008 — Low — clarification count and OPEN-050 scope are overstated

**Evidence.** `plan.md` status says `PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 2]` (line 628), while the spec has three open rows: CLAR-009 (non-blocking), CLAR-011 and CLAR-012 (`spec.md` line 793). `plan.md` lines 105–107 and `shared-updates.md` line 54 attach D-RUN-07/-08/-12/-17 to OPEN-050, but OPEN-050 is defined for D-RUN-18..21 only (`aisdlc/docs/open-items.md`). D-RUN-12 is an orchestrator decision without that ratification row.

**Required fix.** Report `OPEN_ITEMS: 3` (2 blocking + CLAR-009 non-blocking) and attach D-RUN-12 (and D-RUN-07/-17 if ratification is wanted) to a separate open item or a note, not to OPEN-050. Keep "no ratification claimed" for D-RUN-18..21.

### PLAN-009 — Low — the System test's business date is not stated

**Evidence.** `tasks.md` TASK-14 loads `valid-14-rows.csv` (valid from 2026-11-30) and expects the approve to return 200 with 14 rows (`tasks.md` line 69). E1-043's `CURRENT_STATE` rule refuses approval while `validFrom` is after the business date (`spec.md` SPEC-019 item 9; E1-043 SPEC-032 rule 6). The plan says only "the business date comes from `BusinessDateProvider`"; it does not state the date the IT sets.

**Required fix.** State the business date used for the approve (2026-11-30 or later) and how the IT sets it; add it to TASK-14's verification.

### PLAN-010 — Low — "12 CSV fixtures" does not match the 11 files in the fixture table

**Evidence.** `tasks.md` TASK-06 says "Add the 12 CSV fixtures" (line 61) and `plan.md` line 239 says "The 12 fixtures of `data-model.md` § 15". § 15 lists 11 distinct CSV files (the repeat reuses `valid-14-rows.csv` and the failing copy is generated at runtime). The wildcard `TR/reference-loads/data-product/*.csv` in the file table is not an exact file list.

**Required fix.** Correct the count and name the 11 CSV files, or describe the repeat and the failing copy as cases rather than files. If 12 is intended, add the twelfth file and name it.

### PLAN-011 — Low — the merge precondition omits the e2e gate

**Evidence.** `plan.md` "Release and rollback" says the orchestrator merges "only after `./scripts/dev.ps1 test` and `./scripts/dev.ps1 it` exit 0" (line 612). TASK-17 separately requires `./scripts/dev.ps1 e2e` and the stack run (`tasks.md` line 72); TASK-18 depends on TASK-17, but the merge sentence's explicit list omits it.

**Required fix.** Add `./scripts/dev.ps1 e2e` (and the TASK-17 result) to the merge precondition in "Release and rollback".

### PLAN-012 — Low — the coverage gate is the project-wide bundle, not the spec's `dataengine` target

**Evidence.** The gated spec's Unit Test Applicability sets the backend gate at "80% lines, branches, statements and functions on `th.co.scb.ace.demo.recovery.dataengine`" (`spec.md` line 714). `plan.md` sets it at "one `BUNDLE` rule, `LINE`, `INSTRUCTION`, `BRANCH`, `METHOD` each ≥ 0.80 over the TE-001 combined bundle (all recovery main classes, which includes `dataengine.internal.catalog`)" (lines 188–190). A high-coverage legacy class can mask a below-80% changed package.

**Required fix.** Keep the inherited bundle gate (the repo's native `recoveryCoverageVerification`) but also report the `dataengine` package's own four counters from the same JaCoCo XML in TASK-15/TASK-18, or state why the package-scoped spec gate is satisfied by the bundle.

### PLAN-013 — Low — `DictionarySeedShapeTest` asserts the F1–F3 grammar before the grammar exists

**Evidence.** `tasks.md` TASK-01 makes `DictionarySeedShapeTest` assert "each seed value matches exactly one F1–F3 form" (line 56); `plan.md` repeats it (line 224). `SystemOfRecordGrammar` is created by TASK-07 (lines 205, 62). TASK-01 must therefore either duplicate the grammar in the test or import a class that does not exist; the second makes TASK-01 compile-red, contradicting the plan's statement that only TASK-06 is compile-red and every other task runs on a compiling test source set (`tasks.md` line 106).

**Required fix.** Move the seed-to-grammar assertion to `SystemOfRecordGrammarTest` (TASK-06), or keep a test-local grammar in TASK-01 and record it as a deliberate second source with a cross-check in TASK-06.

### PLAN-014 — Low — the `updated_by` deviation is disclosed but not shown as a partial in the coverage summary

**Evidence.** SPEC-014 requires `apply` to set "`updated_at` and `updated_by`" (`spec.md` line 478) and the field matrix repeats it (line 664). The live E1-043 `apply` carries no actor, so the plan writes `updated_at` only and leaves `updated_by` NULL (`plan.md` "Apply, idempotency and the one deviation"; `PG-E1001-02`). This is recorded as `PLAN_DEVIATIONS: 1` (line 631) and `PA-E1001-06` (tech lead), which is the right disclosure, but the coverage summary says "33 of 33 ... 29 unconditional, 3 on assumptions, 1 exclusion" and the §12 row is "COVERED (PG-E1001-02)" without changing that count (lines 520, 632).

**Required fix.** Show §12 Contract as a recorded partial in `PLAN_REQUIREMENT_COVERAGE_SUMMARY` (not only in the row) and make the tech lead's disposition of `PG-E1001-02` a named precondition of the plan approval, or implement the cell. Do not let a Blocker = No gap read as full coverage.

## Requirement coverage table (33/33)

The plan's `## Requirement Logic To Task Coverage` has exactly the 33 `REQ_REF` rows of the gated spec, in the same set; no row is merged, dropped or renamed. Statuses below are the plan's, cross-checked against `spec.md` "Requirement-to-SPEC Logic Coverage".

| REQ_REF | Plan status | Tasks | Named verification |
|---|---|---|---|
| BR1 | COVERED | 01, 02, 03 | `MigrationDerivationTest`; `DataDictionaryConformanceTest` C1/C2/C3; `DictionarySeedShapeTest` |
| BR2 | COVERED | 03, 06, 07, 14 | 14-row seed; K1; `DataProductCatalogLoadIT#validLoadIsValidatedThenAppliedOnApproval` |
| BR3 | COVERED (ASM) | 06, 07, 14 | `SystemOfRecordGrammarTest`; K2/K3; `DataProductCatalogLoadIT#twoDefectsAreBothReported`; GAP-17 carried |
| BR4 | COVERED | 06, 07, 14 | `validate` writes nothing; one transaction; 422 and rollback IT case |
| BR5 | COVERED | 06, 07, 14 | F1/F2; AC11 bare source |
| BR6 | COVERED | 03, 13, 16 | `MigrationDerivationTest`; `${recoverySchema}`; re-run IT |
| BR7 | COVERED (ASM) | 01, 03, 15, 18 | 526 literals; no `UPDATE`; `SeedIntegrityIT`; TE-011 lint (conditional); GAP-18 |
| BR8 | COVERED | 02, 03 | `#noConstraintReferencesPublic`; `#theEighteenLinkColumns...` |
| BR9 | COVERED | 03 | 30 view objects; 304 `DF-ACE-*`; `MigrationDerivationTest` |
| AC1 | COVERED | 02, 03 | `RecoverySchemaMigrationIT` (93/89/4/20/no `payment_match_rule`; conformance) |
| AC2 | COVERED | 03, 14 | `#viewReturnsTheAc2Rows`; `#viewReturnsAc2RowsAfterCatalogLoad` |
| AC3 | COVERED | 06, 07, 14 | valid load + approve; DP01/DP03/DP06 |
| AC4 | COVERED | 02, 03 | failing-`valuation_ext` copy |
| AC5 | COVERED | 02, 03 | both AC5 texts; `char(64)` pass |
| AC6 | COVERED | 02, 03 | second migrate applies 0 |
| AC7 | COVERED | 06, 07, 14 | DP06/DP11 → MSG-P1-003 |
| AC8 | COVERED | 06, 07, 14 | 13 rows → MSG-P1-004 "Missing: DP09." |
| AC9 | COVERED | 06, 07, 14 | two verbatim texts, rows 4/5 |
| AC10 | COVERED | 07, 14 | 409 MSG-P1-011, nothing written |
| AC11 | COVERED | 06, 07, 14 | bare "CCMS" → MSG-P1-003 |
| X1–X3 | COVERED | 02, 03 | failing statement; conformance; re-run |
| X4–X7 | COVERED | 06, 07, 14 | four fixtures + repeat |
| X8 / TC-11 | COVERED | 14, 18 | 403 MSG-P4-002; one REFUSED audit line; E1-039 seam |
| §10 Authority | COVERED | 11, 14, 18 | RW-REFADM/RW-DATASTEW; two catalog keys; maker-checker inherited |
| §12 Contract | COVERED (PG-E1001-02) | 03, 05, 06, 07, 14 | SPI, 422/403/409, view; `updated_by` partial (PLAN-014) |
| §13 Solution plan | COVERED | 03..14 | files, build steps, flag, tests |
| §17 Guardrails | COVERED | 18 | scope/guardrail check |
| §19 Out of scope | COVERED | 18 | diff/scope check |
| NFR-RWB-005 | COVERED | 14, 18 | E1-043 method checks; migration as `rwb_migrator` |
| NFR-RWB-006 | COVERED (ASM) | 01, 03, 15, 18 | 526 union; synthetic UUIDs; GAP-18 |
| NFR-RWB-008 | COVERED | 02, 03 | failing statement in Flyway log; refusal audit line |
| NFR-RWB-009 | COVERED | 09, 13, 19 | flag-off 422; forward-only; release/rollback (PLAN-002) |
| NFR-RWB-001..004, -007, -010 | COVERED (as an exclusion) | 18 | no runtime read path with a target, no screen, no retained class |

`PLAN_REQUIREMENT_COVERAGE_RESULT` is `SUCCESS [TOTAL_RULES: 33] [TASK_COVERED_RULES: 33] [MISSING_TASK_RULES: 0]`, and this review confirms 33 rows, 29 unconditional, 3 on the two Blocker = Yes assumptions, 1 exclusion, with §12 carrying the recorded `PG-E1001-02` partial. The two spec contradictions are carried on `CARRIED_SPEC_CONTRADICTIONS: 2`; the plan does not clear or downgrade them.

## Gate checklist

| Check | Result |
|---|---|
| 33/33 requirement rows mapped, no row merged/dropped/generalized | PASS |
| Every SPEC-001..019 (011 retired) mapped to a task and a named test | PASS |
| Every AC1–AC11, BR1–BR9, X1–X11, TC-01..20, CLAR-001..013 mapped | PASS |
| Every file by exact path | FAIL — PLAN-007 (earlier-story IT edits unnamed); PLAN-010 (fixture count/wildcard) |
| One migration, `V<seq>__rwb_e1_001_recovery_schema.sql`, line 1 `-- Story: RWB-E1-001`, no fixed number (D-RUN-07) | PASS |
| D-RUN-12: four tables and their 1 FK / 1 index / 57 comments not created; 4 + 53 dictionary rows and the 4 FKs kept | PASS (table set and counts verified against PS v6) |
| D-RUN-17: TE-001 v7 layout; E1-044, E1-042 and E1-043 are earlier; E1-001 order 9 | PASS (PRE-2 wording defect is PLAN-001) |
| D-RUN-21: one ACE (recovery) module, no common/collection, no P1 → P3 main edge | PASS |
| Two Blocker = Yes gaps visible, no human ruling claimed, TASK-19 stops the merge without one | PASS |
| No human approval, ratification or blocker clearance claimed | PASS |
| Coverage gate 80% ×4 planned for the backend; frontend `NOT_APPLICABLE` with evidence | PASS with PLAN-012 (scope) |
| Tests precede code; no test skipped or weakened; inherited IT assertions kept | PASS with PLAN-004/-013 (test detail) |
| No new dependency, no build.gradle change, no OpenAPI/frontend change | PASS |
| No secrets, no personal data in code/fixtures/logs; synthetic UUIDs | PASS (PLAN-005 is a citation error, not a data error) |
| Shared files and the build log untouched by this stage | PASS |
| Blockers/assumptions/document gaps complete and evidence-cited | FAIL — PLAN-001/-005/-008/-014 |

## Blocking statement

**STATUS: FAIL.** The plan is not approved in this round. PLAN-001 and PLAN-002 are Medium and block the handoff; PLAN-003..PLAN-014 are Low and are to be fixed in the same remediation round (D-RUN-09). The plan's core design — one forward-only migration, the 89-table set, the 526-mark dictionary, the P4 handler, the two catalog rows, the local switch and the merge gate on the two human rulings — is sound and is not reopened by this review.

`GAP-E1001-17` and `GAP-E1001-18` remain **Blocker = Yes** on `ASM-E1001-13` and `ASM-E1001-14`. No AI triage in this review, and no plan text, is the human ruling. TASK-19's merge block remains the governing control.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 12]
