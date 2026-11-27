# Build-readiness review (script) — RWB-S4-E5003-APP Run the notice period timer

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S4-E5003-APP (RWB S4 E5003 APP Run the notice period timer v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-litigation |
| Legacy key | RWB-E5-003 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 9, Fail 5. Detcheck rows: 20 (0 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E5-003-05', not by a criterion; exception X11 is covered by 'BR4', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-LIT-07' has no BR ID; rule row 'R-LIT-08' has no BR ID; rule row 'R-LIT-15' has no BR ID; rule row 'R-LIT-09' has no BR ID; rule row 'R-LIT-12, R-LIT-13, R-LIT-14' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-31' has no BR ID; 7 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR4, BR5, BR6, BR7, BR8; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 14 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 12 data rows; detcheck: P2 Name `served_result` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `period_expires_at` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `prescription_days_remaining` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-9043, CG-ALL-9044, CG-ALL-9045, CG-ALL-9046, CG-ALL-9059 |
| 8 | Contract | Partial | detcheck: P2 Workflow ID form and start rule of LitigationWorkflow are not stated; P2 Activity openNoticeAction is not in Temporal Catalog v1; P2 Activity evaluateNoticePeriodRule is not in Temporal Catalog v1; P2 Activity recordDecision is not in Temporal Catalog v1 (+6 more) | CG-ALL-9048, CG-ALL-9049, CG-ALL-9050, CG-ALL-9051, CG-ALL-9052, CG-ALL-9053, CG-ALL-9054, CG-ALL-9055, CG-ALL-9056, CG-ALL-9057 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-19 has no empty, loading, error, no access state in the story | CG-ALL-9060, CG-ALL-9061 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E5-003-01, TC-E5-003-02, TC-E5-003-03, TC-E5-003-04, TC-E5-003-05, TC-E5-003-06 | CG-ALL-9058 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 dependencies named; detcheck: P2 HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a notice that is not `NOTICE_DISPATCHED`, an action that is not `OPEN`, or a period already started; 503 the decision-record library or a consumed contract unavailable. The request and answer shapes are declared by `RWB-S4-E5003-CON`, which this story consumes as its first build dependency | CG-ALL-9047 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S4-E5003-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_comms, rwb_decision, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 16 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9043 | Name `served_result` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9044 | Name `period_expires_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9045 | Name `prescription_days_remaining` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9046 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9047 | HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a notice that is not `NOTICE_DISPATCHED`, an action that is not `OPEN`, or a period already started; 503 the decision-record library or a consumed contract unavailable. The request and answer shapes are declared by `RWB-S4-E5003-CON`, which this story consumes as its first build dependency | X5 | Missing | Business analyst |
| CG-ALL-9048 | Workflow ID form and start rule of LitigationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9049 | Activity openNoticeAction is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9050 | Activity evaluateNoticePeriodRule is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9051 | Activity recordDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9052 | Activity attachProof is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9053 | Activity startNoticePeriod is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9054 | Activity announceCaseRoute is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9055 | Activity announceNoticeUnserved is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9056 | Activity expireNoticePeriod is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9057 | Activity prescriptionWarning is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9058 | Test cases not in Test Cases v8: TC-E5-003-01, TC-E5-003-02, TC-E5-003-03, TC-E5-003-04, TC-E5-003-05, TC-E5-003-06 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9059 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9060 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9061 | SCR-19 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9062 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X7: A role without the Litigation right calls an operation (covered by 'TC-E5-003-05' only) | Not specified in the source documents | |
| AC6 | §5 X11: A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table (covered by 'BR4' only) | Not specified in the source documents | |
| AC7 | §8 BR1, BR2, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
