# Build-readiness review (script) — RWB-P4-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1020-APP (RWB P4 E1020 APP Allocation and assignment engine v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-020 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 12 (3 P1). AC review rows: 6. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'team manager, a capacity planner, a platform administrator or an auditor who works the morning allocation' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 19 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'BR9', not by a criterion; exception X8 is covered by 'BR9', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 6 of 10 rules are covered by no criterion and no test case: BR1, BR3, BR4, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 7 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data; P2 Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-4915, CG-ALL-4916, CG-ALL-4917 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P4-006 is used with another meaning than the standard's | CG-ALL-4918 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-4923, CG-ALL-4924 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC1 has no test case in §16; AC2 has no test case in §16; AC3 has no test case in §16; AC4 has no test case in §16; AC6 has no test case in §16; AC9 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC1, AC2, AC3, AC4, AC6, AC9; P3 §18 test lists differ from RTM v7 | CG-ALL-4919, CG-ALL-4920, CG-ALL-4921 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-4914 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E1020-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4914 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-4915 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-4917 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4916 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4918 | MSG-P4-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-4920 | Criteria with no test case: AC1, AC2, AC3, AC4, AC6, AC9 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4919 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-4921 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4922 | Flyway file V1020_1__allocation_authority_read_path.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4923 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4924 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4925 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | no test case in §16 |  |
| AC2 | no test case in §16 |  |
| AC3 | no test case in §16 |  |
| AC4 | no test case in §16 |  |
| AC6 | no test case in §16 |  |
| AC9 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X6: Two roles of the caller conflict (for example RW-SECADM with a business role) (covered by 'BR9' only) | Not specified in the source documents | |
| AC11 | §5 X8: The reference list of scope or capability is not available (covered by 'BR9' only) | Not specified in the source documents | |
| AC12 | §8 BR1, BR3, BR4, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
