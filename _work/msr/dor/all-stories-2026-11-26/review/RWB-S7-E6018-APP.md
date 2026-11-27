# Build-readiness review (script) — RWB-S7-E6018-APP Approve a write-off inside the limit

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S7-E6018-APP (RWB S7 E6018 APP Approve a write-off inside the limit v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-writeoff |
| Legacy key | RWB-E6-018 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 15 (7 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'write-off committee member' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'Section 17, BR6', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-WO-15' has no BR ID; rule row 'R-WO-12' has no BR ID; 11 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-10971, CG-ALL-10983 |
| 8 | Contract | Fail | detcheck: P1 POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) is not in rwb-writeoff.yaml; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 No API Specification v5 yaml has the base of /api/recovery/access/v1 (+4 more) | CG-ALL-10972, CG-ALL-10973, CG-ALL-10974, CG-ALL-10975, CG-ALL-10976, CG-ALL-10977, CG-ALL-10978, CG-ALL-10979, CG-ALL-10980 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-27 has no empty, loading, error, no access state in the story | CG-ALL-10984 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10982 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-018-01, TC-E6-018-02, TC-E6-018-03, TC-E6-018-04, TC-E6-018-05, TC-E6-018-06 | CG-ALL-10981 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S7-E6018-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_access, rwb_case, rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10972 | POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) is not in rwb-writeoff.yaml | X5 | Missing | Solution architect |
| CG-ALL-10973 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10974 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10975 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-10976 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-10977 | Workflow WriteOffWorkflow task queue rwb-writeoff` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |
| CG-ALL-10979 | Workflow The committee branch of `WriteOffWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10971 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10978 | Workflow ID form and start rule of WriteOffWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10980 | Activity approveWriteOffInLimit is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10981 | Test cases not in Test Cases v8: TC-E6-018-01, TC-E6-018-02, TC-E6-018-03, TC-E6-018-04, TC-E6-018-05, TC-E6-018-06 | X9 | Missing | QA |
| CG-ALL-10982 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10983 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10984 | SCR-27 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10985 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X9: A component, a statement or a test reaches another service's schema or a `v_ace_*` view (covered by 'Section 17, BR6' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC9 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
