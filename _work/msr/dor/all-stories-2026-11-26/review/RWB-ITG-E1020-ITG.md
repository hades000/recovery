# Build-readiness review (script) — RWB-ITG-E1020-ITG Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1020-ITG (RWB ITG E1020 ITG Allocation and assignment engine v1 - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-020 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 6, Fail 9. Detcheck rows: 19 (5 P1). AC review rows: 8. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 10 of 18 rules are covered by no criterion and no test case: BR7, BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18; §8 has 18 rules; detcheck: P2 Rule ID ALLOC-014 used in the criteria exists in no current source | CG-ALL-242 |
| 5 | State transitions | Fail | §9 has 9 transitions; detcheck: P1 Status 'New, in the deviation handler queue' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'New, in the exception queue' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'New, in the overflow queue' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-237, CG-ALL-238, CG-ALL-239 |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 35 data rows; detcheck: P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-249, CG-ALL-250 |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-241 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P3-012 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4; P2 MSG-GEN-004 is used with another meaning than the standard's | CG-ALL-243, CG-ALL-244, CG-ALL-245 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-251, CG-ALL-252, CG-ALL-253 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC14 has no test case in §16; AC15 has no test case in §16; AC16 has no test case in §16; AC17 has no test case in §16; AC18 has no test case in §16; AC19 has no test case in §16; AC20 has no test case in §16; no contract test for the operations, events and activities of §12; §16 has 15 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P2 Criteria with no test case: AC14, AC15, AC16, AC17, AC18, AC19, AC20; P3 §18 test lists differ from RTM v7 | CG-ALL-246, CG-ALL-247, CG-ALL-248 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 4 build dependencies are not done yet (RWB-P3-E1020-APP, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP); 4 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-240 |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560); open decision DL24 (assumptions: none); detcheck: P2 Open decision DL24 has no assumption | CG-ALL-255 |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1020-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-decision, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-237 | Status 'New, in the deviation handler queue' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-238 | Status 'New, in the exception queue' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-239 | Status 'New, in the overflow queue' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-240 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-241 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-242 | Rule ID ALLOC-014 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-244 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-245 | MSG-GEN-004 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-247 | Criteria with no test case: AC14, AC15, AC16, AC17, AC18, AC19, AC20 | X9 | Missing | QA |
| CG-ALL-249 | Criteria and test data read ACE views directly | X12 | Outdated | QA |
| CG-ALL-255 | Open decision DL24 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-243 | MSG-P3-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-246 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-248 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-250 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-251 | SCR-02 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-252 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-253 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-254 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC14 | no test case in §16 |  |
| AC15 | no test case in §16 |  |
| AC16 | no test case in §16 |  |
| AC17 | no test case in §16 |  |
| AC18 | no test case in §16 |  |
| AC19 | no test case in §16 |  |
| AC20 | no test case in §16 |  |
| AC10 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC21. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC21 | §8 BR7, BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC22 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC23 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
