# Build-readiness review (script) — RWB-P4-E1021-APP Transfer rules and engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1021-APP (RWB P4 E1021 APP Transfer rules and engine v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 6, Fail 8. Detcheck rows: 10 (3 P1). AC review rows: 3. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'team manager, a capacity planner, a litigation officer or a legal counsel who moves a case between queues or puts a case on legal hold' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 20 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'BR3, BR9', not by a criterion; exception X6 is covered by 'BR6', not by a criterion; exception X8 is covered by 'BR1, BR4', not by a criterion; exception X9 is covered by 'BR3', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 6 of 10 rules are covered by no criterion and no test case: BR2, BR3, BR6, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Pass | §11 has 7 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data; P2 Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-4927, CG-ALL-4928, CG-ALL-4929 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P3-001; §14 lists 6 messages; detcheck: P2 MSG-P4-006 is used with another meaning than the standard's | CG-ALL-4930 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-4934 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC3 has no test case in §16; AC4 has no test case in §16; AC7 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P2 Criteria with no test case: AC3, AC4, AC7; P3 §18 test lists differ from RTM v7 | CG-ALL-4931, CG-ALL-4932 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-4926 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E1021-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4926 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-4927 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-4929 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4928 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4930 | MSG-P4-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-4931 | Criteria with no test case: AC3, AC4, AC7 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4932 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4933 | Flyway file V1021_1__transfer_authority_path.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4934 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4935 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC3 | no test case in §16 |  |
| AC4 | no test case in §16 |  |
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X5: The LOV-TRANSFER-REASON list is not available (covered by 'BR3, BR9' only) | Not specified in the source documents | |
| AC10 | §5 X6: Two roles of the caller conflict (for example RW-SECADM with a business role) (covered by 'BR6' only) | Not specified in the source documents | |
| AC11 | §5 X8: A caller asks about both areas in one call (covered by 'BR1, BR4' only) | Not specified in the source documents | |
| AC12 | §5 X9: The transfer reason presented is not a value of the list in force (covered by 'BR3' only) | Not specified in the source documents | |
| AC13 | §8 BR2, BR3, BR6, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
