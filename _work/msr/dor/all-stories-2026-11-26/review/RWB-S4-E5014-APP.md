# Build-readiness review (script) — RWB-S4-E5014-APP Decide and manage an appeal

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S4-E5014-APP (RWB S4 E5014 APP Decide and manage an appeal v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-litigation |
| Legacy key | RWB-E5-014 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 19 (5 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X11 is covered by 'BR4', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-LIT-45' has no BR ID; rule row 'R-LIT-46' has no BR ID; rule row 'R-LIT-47' has no BR ID; rule row 'R-LIT-48' has no BR ID; rule row 'R-LIT-49' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; 6 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR4, BR5, BR6, BR7; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 12 transitions; detcheck: P1 The story adds JUDGMENT_DISMISSED to the closed list LOV-LEGAL-STATUS; P1 The story adds APPEAL_DECISION to the closed list LOV-LEGAL-STATUS; P1 The story adds APPEAL_FILED to the closed list LOV-LEGAL-STATUS; P1 The story adds IN_HEARING to the closed list LOV-LEGAL-STATUS (+1 more) | CG-ALL-9325, CG-ALL-9326, CG-ALL-9327, CG-ALL-9328, CG-ALL-9329 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 17 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-9330, CG-ALL-9340 |
| 8 | Contract | Partial | detcheck: P2 Workflow ID form and start rule of LitigationWorkflow are not stated; P2 Activity openAppeal is not in Temporal Catalog v1; P2 Activity recordDecision is not in Temporal Catalog v1; P2 Activity requestApproval is not in Temporal Catalog v1 (+3 more) | CG-ALL-9332, CG-ALL-9333, CG-ALL-9334, CG-ALL-9335, CG-ALL-9336, CG-ALL-9337, CG-ALL-9338 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-19 has no empty, loading, error, no access state in the story | CG-ALL-9341, CG-ALL-9342 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E5-014-01, TC-E5-014-02, TC-E5-014-03, TC-E5-014-04 | CG-ALL-9339 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 dependencies named; detcheck: P2 HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a status or an action type that refuses the step, or a case that is not in `JUDGMENT_DISMISSED`; 503 the decision-record library or a consumed contract unavailable. The hearing operation API-S4-005 and the notice approval API-S4-001 belong to other stories of this service and are not served here. The request and answer shapes are declared by `RWB-S4-E5014-CON`, which this story consumes as its first build dependency | CG-ALL-9331 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S4-E5014-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_comms, rwb_decision, rwb_document, rwb_partner | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9325 | The story adds JUDGMENT_DISMISSED to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-9326 | The story adds APPEAL_DECISION to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-9327 | The story adds APPEAL_FILED to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-9328 | The story adds IN_HEARING to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-9329 | The story adds TO_WRITE_OFF to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9330 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9331 | HTTP errors with no message ID: 401 no session; 404 unknown or out-of-scope reference; 409 a status or an action type that refuses the step, or a case that is not in `JUDGMENT_DISMISSED`; 503 the decision-record library or a consumed contract unavailable. The hearing operation API-S4-005 and the notice approval API-S4-001 belong to other stories of this service and are not served here. The request and answer shapes are declared by `RWB-S4-E5014-CON`, which this story consumes as its first build dependency | X5 | Missing | Business analyst |
| CG-ALL-9332 | Workflow ID form and start rule of LitigationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9333 | Activity openAppeal is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9334 | Activity recordDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9335 | Activity requestApproval is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9336 | Activity instructFirm is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9337 | Activity recordFiling is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9338 | Activity announceCaseRoute is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9339 | Test cases not in Test Cases v8: TC-E5-014-01, TC-E5-014-02, TC-E5-014-03, TC-E5-014-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9340 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9341 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9342 | SCR-19 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9343 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X11: A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table (covered by 'BR4' only) | Not specified in the source documents | |
| AC4 | §8 BR1, BR2, BR4, BR5, BR6, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC5 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC6 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
