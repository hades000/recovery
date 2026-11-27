# Build-readiness review (script) — RWB-ITG-E1018-ITG Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1018-ITG (RWB ITG E1018 ITG Case ID issuance and case record v1 - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-018 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 8, Fail 8. Detcheck rows: 14 (4 P1). AC review rows: 3. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 20 Reference data; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'TC-E1-018-11-ITG, owned by RWB-P3-E1018-APP', not by a criterion; exception X6 is covered by 'TC-E1-018-10-ITG, owned by RWB-P3-E1018-APP', not by a criterion; exception X10 is covered by 'Section 17', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 7 of 18 rules are covered by no criterion and no test case: BR9, BR10, BR14, BR15, BR16, BR17, BR18; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 35 data rows; detcheck: P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-229, CG-ALL-230 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/source-data/v1/business-days/{date}/ready is not published by rwb-source-data; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-221, CG-ALL-223 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-224, CG-ALL-225 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no error, no access state in the story; P3 SCR-03 has no empty, error, no access state in the story | CG-ALL-231, CG-ALL-232 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 16 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-018-15-ITG, TC-E1-018-16-ITG; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-226, CG-ALL-227, CG-ALL-228 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 8 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1016-APP, RWB-P1-E1018-APP, RWB-P1-E1069-APP, RWB-P3-E1018-APP, RWB-P4-E1018-APP); 8 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-222 |
| 18 | Open decisions | Partial | open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL17 (assumptions: none); detcheck: P2 Open decision DL17 has no assumption | CG-ALL-233 |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Fail | detcheck: P1 Parameter case.entry.dpd is also written as case.entry.dpd_threshold | CG-ALL-220 |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1018-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case, rwb-decision, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-220 | Parameter case.entry.dpd is also written as case.entry.dpd_threshold | X4 | ID collision | Business analyst |
| CG-ALL-221 | POST /api/recovery/source-data/v1/business-days/{date}/ready is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-222 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-223 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-225 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-226 | Test cases not in Test Cases v8: TC-E1-018-15-ITG, TC-E1-018-16-ITG | X9 | Missing | QA |
| CG-ALL-229 | Criteria and test data read ACE views directly | X12 | Outdated | QA |
| CG-ALL-233 | Open decision DL17 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-224 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-227 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-228 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-230 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-231 | SCR-02 has no error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-232 | SCR-03 has no empty, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC9 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC13 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X5: The yearly case number range is used up (covered by 'TC-E1-018-11-ITG, owned by RWB-P3-E1018-APP' only) | Not specified in the source documents | |
| AC17 | §5 X6: The decision of the creation cannot be recorded (covered by 'TC-E1-018-10-ITG, owned by RWB-P3-E1018-APP' only) | Not specified in the source documents | |
| AC18 | §5 X10: A suite step tries to read a service schema directly (covered by 'Section 17' only) | Not specified in the source documents | |
| AC19 | §8 BR9, BR10, BR14, BR15, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC20 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC21 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC22 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
