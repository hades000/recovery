# Plan gate review, round 2: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-PLAN-002` |
| Gate | Plan gate, round 2 (Compliance Reviewer; bounded re-gate after remediation run 2) |
| Previous round | `review/plan-gate-review.md` (`REVIEW-RWB-E1-043-PLAN-001`), `FAIL` 0 Critical / 0 High / 1 Medium / 7 Low (PLAN-001..PLAN-008) |
| Artefacts reviewed | `plan/plan.md` v1 (remediation run 2, 18 Nov 2026), `plan/tasks.md` v1, `plan/data-model.md` v1, `plan/tests/scenarios.md`, `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/contracts/backend-apis.json` v1, `plan/contracts/frontend-integrations.json` v1, `plan/agent-run-log.md`. The `.run1.md` / `.run1.json` snapshots were diffed as the audit trail. |
| Gated spec | `specify/spec.md` revision 10; spec gate round 10 `REVIEW-RWB-E1-043-SPEC-010` `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-10.md`) |
| Story | User Stories Epic 1 Story Files v7, RWB-E1-043 v2 (`requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md`) |
| Sources checked | `AGENTS.md` sections 7 and 9; `planning-execution-gates.md`; `implementation-execution-gates.md` (80% gate); `pdlc.md`; `AI-SDLC-BUILD-LOG.md` decisions D-RUN-07..22; `infra/postgres/schema/03-recovery-physical-schema-v6.sql`; `api/recovery-api-v4.yaml`; Users, Roles and Permissions v4 lines 73-110; RWB-TE-001 plan v7; RWB-E1-044 plan v2; RWB-E1-042 plan v2; the code baseline's test tree and empty migration folder; `aisdlc/docs/open-items.md` OPEN-050. All read only. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03); no build, Gradle, Docker or git command run. Only this review file written. |

## Status

**`PLAN_GATE: PASS`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 0 | |

`REVIEW_STATUS: PASS`. All eight round-1 findings are resolved. The remediation diff is limited to
those findings: no requirement, SPEC, AC, BR, X, TC, SEC or CLAR row was added, removed, merged or
weakened, and the 20-task structure, its order and its dependencies are unchanged. No new finding is
opened in this round. The design, traceability and execution order are executable as written.

## Round-1 findings: resolution check

| ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| PLAN-001 | Medium | **Resolved** | `ReferenceMigrationIT` no longer reads the CSV: TASK-01 asserts the DDL, columns, constraints, indexes, triggers, negatives and the 38 catalog keys with their `value_type`, `default_value` and `owner_role` (`plan/tasks.md` TASK-01); TASK-02's verification says the IT compares the 38 rows with the plan's expected key set, "not with `M/config/parameter-catalog.csv` (the CSV equality is TASK-15, after TASK-04)". The database-to-CSV equality is `ReferenceLoadIT#catalogRowsMatchTheCatalogFile` in TASK-15, which runs after TASK-04 writes the 57-row file (`plan.md` test-scope rows, "Execution order" step 4, the S7 section 13 step 2 row 343 and SPEC-029 map row 400; `data-model.md` line 221; `tests/scenarios.md` T-E1-043-22 and T-E1-043-33). At TASK-02 the migration itself writes the 38 keys, so the green point is now reachable without the CSV. |
| PLAN-002 | Low | **Resolved** | The three non-recovery TE-001 test files are named in full: `backend/src/test/java/th/co/scb/ace/demo/testsupport/ApplicationYamlEnvironment.java`, `backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java` and `backend/src/test/java/th/co/scb/ace/demo/e2e/PlatformE2ETest.java` (`plan.md` lines 46, 79 and 230, with line 232 explaining why the TE-001 `T/...` shorthand is wrong). No current artefact uses `T/testsupport`, `T/.../e2e` or `T/.../ModulithTest` as a path; the only remaining occurrences are the run-log entry that records the old defect and that explanatory line. The full paths match E1-044 plan v2 line 49 and E1-042 plan v2's unchanged list. |
| PLAN-003 | Low | **Resolved** | `data-model.md` line 298 now reads "RWB-E1-001's own migration (`V<seq>` assigned at merge, D-RUN-07); the PS6 local load provides the rows until then". No `V0001` or `V0042` remains as a fixed number in the current plan artefacts; the only `V0001` mention is the migration lint's "contiguous sequence from V0001" rule (`plan.md` line 236), which is a rule, not an assignment. |
| PLAN-004 | Low | **Resolved** | `plan.md` lines 73-82 add a "Preconditions" table defining PRE-1 (TE-001 merged), PRE-2 (E1-044's identifier-only, quote-aware lint merged), PRE-3 (E1-042 merged) and PRE-4 (base gates green and the recovery migration folder empty), each with source/order, proof in the merged base and the stop action. TASK-00 and the pre-submit check point to it, and `shared-updates.md` R23 cites PRE-2. No undefined `PRE-*` label remains. |
| PLAN-005 | Low | **Resolved** | `plan.md` line 49 and `agent-run-log.md` lines 12, 81 and 120 now state "33 TC IDs plus SEC-01..17 (49 plan T-IDs)" instead of the stale "40 test IDs". The verified sets are 33 TC IDs (`TC-E1-043-01..11`, `TC-RB-01/-02`, `TC-HD-01..05`, `TC-PB-01/-02`, `TC-FL-01`, `TC-MG-01`, `TC-BR1`, `TC-TM-01..05`, `TC-RP-01`, `TC-FD-01`, `TC-DR-01`, `TC-BD-01`, `TC-CAT-01`), 17 SEC IDs and 49 `T-E1-043-*` rows in `tests/scenarios.md`; every one is mapped. |
| PLAN-006 | Low | **Resolved** | `ReferenceLoadIT#rowKeyAndHandlerDefect` asserts the 500 status, the existing `ApiExceptionHandler.unexpected` body (`title`, `status`) and that **no `traceId` member is present**, with nothing written (TASK-15; `plan.md` line 366; `tests/scenarios.md` line 88; `document-gaps.md` PG-E1-043-03; `contracts/backend-apis.json` `problemBody` and the 500 row). PG-E1-043-03 and `shared-updates.md` R18 stay open, and the row is explicitly not claimed as full coverage of SPEC-025's `traceId` word. |
| PLAN-007 | Low | **Resolved** | The extra `DROP CONSTRAINT IF EXISTS uk_reference_version_from_hash` is gone from `plan.md`: group 3 is now only the `uk_reference_row` drop plus the guarded `uk_reference_row_version` block (`plan.md` line 242), identical to `data-model.md` line 30, and group 4 adds `uk_reference_version_from_hash` with the two CHECKs and the FK in all three files (`plan.md` line 243; `data-model.md` line 31; TASK-02). The eight statement groups appear in the same order and with the same content in `plan.md`, `data-model.md` section 1 and TASK-02; `data-model.md` group 6's cross-reference to section 7 is corrected. |
| PLAN-008 | Low | **Resolved** | TASK-19 now reads: "The diff touches only the files listed in `plan.md` 'Files added or changed' and leaves every file of 'Files explicitly not changed' untouched" (`tasks.md` line 51). The per-task scope list that follows is unchanged. |

## Coverage (unchanged by the remediation)

| Set | Required | Mapped | Missing | Evidence |
|---|---:|---:|---:|---|
| Requirement rows | 49 | 49 | 0 | `plan.md` lines 314-362 against `spec.md` lines 117-165; 48 `DIRECT_IMPLEMENTATION`, 1 `INHERITED_EXISTING_BEHAVIOR`, all `COVERED`, none `BLOCKED` |
| SPEC | 32 | 32 | 0 | `plan.md` lines 370-403; `SPEC-RWB-E1-043-001..032`; every row has at least one task and a named test |
| AC | 10 | 10 | 0 | `tests/scenarios.md` section 2 (AC1..AC10) |
| BR | 9 | 9 | 0 | `tests/scenarios.md` section 3 (BR1..BR9) |
| X | 7 | 7 | 0 | `tests/scenarios.md` section 4 (X1..X7) |
| TC | 33 | 33 | 0 | `spec.md` "Test scenarios"; `tests/scenarios.md` sections 1 and 5; TC-BR1 maps to T-E1-043-23 and `ReferenceLoadIT#ruleCodeAndHolidayRefused` in TASK-15 |
| SEC | 17 | 17 | 0 | `tests/scenarios.md` section 1 (SEC-01..SEC-17) |
| CLAR | 20 | 20 | 0 | `tests/scenarios.md` section 6 (CLAR-001..020) |
| Plan T-IDs | 49 | 49 | 0 | `tests/scenarios.md` section 1 (T-E1-043-01..49) |

The 16 requirement lines owned by other stories remain seams and are not counted; the 40 source
contradictions remain settled in the spec and this plan introduces none. No orphan SPEC remains.

## Plan-gate checks

| Check | Result |
|---|---|
| One migration | `V<seq>__rwb_e1_043_reference_versions.sql`; line 1 `-- Story: RWB-E1-043`; `<seq>` assigned at merge (D-RUN-07, D-RCV-28); one file, forward only; no `R__` file; no other migration name or fixed number in any current artefact. Pass |
| `reference_version` | 29 columns, types, widths, nullability and defaults match Physical Schema v6 lines 1437-1468; `uk_reference_version`; the new uniqueness, CHECKs, partial index, `load_id` index and append-only trigger. Pass |
| `reference_row` | 11 columns match Physical Schema v6 lines 1471-1484; `uk_reference_row` dropped; `uk_reference_row_version (version_id, row_key)` added; `fk_reference_row_version_id` and `ix_reference_row_version_id` kept. Pass |
| 38 catalog rows | 12 `refdata.columns.*` (STRING, `none`, RW-REFADM) + 13 `rwb.refload.loader.*` + 13 `rwb.refload.approver.*` = 38, CODE_LIST, `required=false`, owner RW-RISK; no `parameter_value` row. Pass |
| 37 grant rows | One per RW- role for area `Reference data`; matrix letters plus the six A roles of A-08; no `Rules and parameters` row changed. Pass |
| 80% x 4 gate | `recoveryCoverageVerification`: one `BUNDLE` with LINE, INSTRUCTION, BRANCH and METHOD each 0.80; native `recoveryCoverageReport.xml` / HTML; no exclusion, no lowered threshold; frontend `NOT_APPLICABLE` with scope evidence. Pass |
| Security and authority | Three operations with `@PreAuthorize` naming `referenceLoadAuthority`, area `Reference data` and C/A/U; per-table lists through `ParameterService`; 401/403/404; `MSG-P4-002` action text; SEC-01..17. Pass |
| Personal data | Staff identifiers only; never logged, never in the response or audit; synthetic UUIDs only; no customer data. Pass |
| Audit | `REFERENCE_LOAD_AUDIT` for load, approve and rollback, DONE and REFUSED; `DECISION_RECORDED` AC-VERS; no user ID, row content or reason. Pass |
| Frontend | `NOT_APPLICABLE` with UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]`, no `plan/frontend/components.md`, no `frontend/` change. Pass |
| Preconditions | PRE-1..PRE-4 defined with proof and stop action; TASK-00 and the pre-submit check cite them. Pass |
| No human approval | No ratification, approval or acceptance of D-RUN-18..21; OPEN-050 and the 15 owner-acceptance items stay open. Pass |
| D-RUN decisions | D-RUN-07 (one file, no number), D-RUN-08 (seams only), D-RUN-10/11 (shared endpoint, handler registry), D-RUN-17 (TE-001 layout), D-RUN-18/19/20 (P4 SPI, parameter reads, `PARAMETER` branch), D-RUN-21 (one ACE module). Pass, all unratified as recorded |

## Regression check

The `.run1` snapshots were diffed against the current files. `assumptions.md` and
`contracts/frontend-integrations.json` are unchanged (0 lines added or removed); every other change is one of the eight
fixes: the revision lines, the `Preconditions` table, the full TE-001 paths, the 33/49 counts, the
`V<seq>` seed-ownership row, the catalog-comparison move, TASK-19's scope sentence and the
`traceId`-absent assertions in `document-gaps.md`, `shared-updates.md`, `contracts/backend-apis.json`
and `tests/scenarios.md`. The requirement row "S7 section 13 step 2" and the SPEC-029 map each gained
`TASK-15` and `ReferenceLoadIT#catalogRowsMatchTheCatalogFile` — additive trace, not a weakened
statement. `tasks.md` still has 20 task rows (TASK-00..TASK-19), each with six cells and a
`BLOCKED_BY` and verification; the task order and dependency graph are unchanged. No test was
deleted, skipped or weakened; the only test moved is the catalog comparison, to the point where its
input exists.

## Open items carried (not findings)

- PG-E1-043-03 / R18: SPEC-025's 500 `traceId` word stays open; the case asserts its absence and is
  not claimed as coverage. Request to the E1-042/API owner.
- OPEN-050 (recovery tech lead): D-RUN-18..21 applied but unratified; no approval is claimed.
- PG-E1-043-01..06, all Blocker = No; the 59 spec gaps; GAP-43's unowned tables; HV-E1043-01..05
  remain human-verification gaps, never reported as tested.
- `RATIFICATION_CLAIMS: none`.

## Gate decision

The round-1 Medium and all seven Lows are resolved with evidence in the current plan artefacts. The
remediation adds no coverage gap and removes no task, test, SPEC, AC, BR, X, TC, SEC or CLAR row.
The plan names every file, test and migration, stays inside the one ACE module (recovery) under the
recorded D-RUN-21 reading, and plans the 80% x 4 gate. No finding remains open, so D-RUN-09 is not
invoked and no finding is accepted or waived.

PLAN_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
