# Build-readiness review (script) — RWB-ITG-E1021-ITG Transfer rules and engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1021-ITG (RWB ITG E1021 ITG Transfer rules and engine v1 - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 8, Fail 8. Detcheck rows: 12 (4 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'TC-E1-021-03-ITG', not by a criterion; exception X3 is covered by 'TC-E1-021-07-ITG', not by a criterion; exception X4 is covered by 'TC-E1-021-08-ITG', not by a criterion; exception X5 is covered by 'TC-E1-021-09-ITG, TC-E1-021-16-ITG', not by a criterion; exception X9 is covered by 'TC-E1-021-13-ITG', not by a criterion; §7 holds 10 owned criteria in Gherkin; §5 has 13 exception paths | — |
| 4 | Business rules | Partial | 9 of 18 rules are covered by no criterion and no test case: BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18; §8 has 18 rules | — |
| 5 | State transitions | Fail | §9 has 7 transitions; detcheck: P1 Status 'New, Assigned, In progress, any Waiting' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'The status it paused in' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-256, CG-ALL-257 |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 27 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-263 |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-259 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-260 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-05 has no empty, loading, error, no access state in the story | CG-ALL-264, CG-ALL-265, CG-ALL-266 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 16 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-261, CG-ALL-262 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 5 build dependencies are not done yet (RWB-P3-E1021-APP, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP); 5 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-258 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1021-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-decision; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-256 | Status 'New, Assigned, In progress, any Waiting' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-257 | Status 'The status it paused in' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-258 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-259 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-260 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-261 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-262 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-263 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-264 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-265 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-266 | SCR-05 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-267 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §5 X1: Two transfers reach the same case in the same second (covered by 'TC-E1-021-03-ITG' only) | Not specified in the source documents | |
| AC16 | §5 X3: A named target owner at the caseload cap (covered by 'TC-E1-021-07-ITG' only) | Not specified in the source documents | |
| AC17 | §5 X4: A transfer of a closed case (covered by 'TC-E1-021-08-ITG' only) | Not specified in the source documents | |
| AC18 | §5 X5: The decision record cannot be written (covered by 'TC-E1-021-09-ITG, TC-E1-021-16-ITG' only) | Not specified in the source documents | |
| AC19 | §5 X9: A legal hold is placed on a case already on hold (covered by 'TC-E1-021-13-ITG' only) | Not specified in the source documents | |
| AC20 | §8 BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC21 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
