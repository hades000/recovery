# Build-readiness review (script) — RWB-S4-E5007-APP Verify the pack and approve filing

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S4-E5007-APP (RWB S4 E5007 APP Verify the pack and approve filing v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-litigation |
| Legacy key | RWB-E5-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 17 (1 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X12 is covered by 'BR8', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-LIT-04' has no BR ID; rule row 'R-LIT-11' has no BR ID; rule row 'R-LIT-16' has no BR ID; rule row 'R-LIT-21' has no BR ID; rule row 'R-LIT-23' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; 7 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR4, BR5, BR6, BR7, BR8; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 17 data rows; detcheck: P2 Name `pack_verified_at` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Field IDs DF-WRK-017 to DF-WRK-036 are not all fields of task in LDM v9; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-9136, CG-ALL-9137, CG-ALL-9138, CG-ALL-9149 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a status or a case state that refuses the step; 503 the decision-record library or a consumed contract unavailable. API-S4-001 `POST /notices/{noticeId}/approve` is named by the legacy endpoint block of RWB-E5-007, is first in E2 and belongs to the notice story of this service; P1 Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of LitigationWorkflow are not stated; P2 Activity verifyPack is not in Temporal Catalog v1 (+4 more) | CG-ALL-9139, CG-ALL-9140, CG-ALL-9141, CG-ALL-9142, CG-ALL-9143, CG-ALL-9144, CG-ALL-9145, CG-ALL-9146 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-19 has no empty, loading, error, no access state in the story | CG-ALL-9150, CG-ALL-9151 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-9148 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E5-007-01, TC-E5-007-02, TC-E5-007-03, TC-E5-007-04, TC-E5-007-05, TC-E5-007-06 | CG-ALL-9147 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S4-E5007-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_comms, rwb_decision, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9140 | Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9136 | Name `pack_verified_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9137 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9138 | Field IDs DF-WRK-017 to DF-WRK-036 are not all fields of task in LDM v9 | X3 | Conflict | Data |
| CG-ALL-9139 | HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a status or a case state that refuses the step; 503 the decision-record library or a consumed contract unavailable. API-S4-001 `POST /notices/{noticeId}/approve` is named by the legacy endpoint block of RWB-E5-007, is first in E2 and belongs to the notice story of this service | X5 | Missing | Business analyst |
| CG-ALL-9141 | Workflow ID form and start rule of LitigationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9142 | Activity verifyPack is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9143 | Activity recordDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9144 | Activity raiseOfficerTask is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9145 | Activity announceCaseRoute is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9146 | Activity authoriseFiling is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9147 | Test cases not in Test Cases v8: TC-E5-007-01, TC-E5-007-02, TC-E5-007-03, TC-E5-007-04, TC-E5-007-05, TC-E5-007-06 | X9 | Missing | QA |
| CG-ALL-9148 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9149 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9150 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9151 | SCR-19 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9152 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X12: A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table (covered by 'BR8' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC9 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
