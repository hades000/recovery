# Build-readiness review (script) — RWB-P4-E2035-APP Next action on the case

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2035-APP (RWB P4 E2035 APP Next action on the case v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-035 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 8, Fail 9. Detcheck rows: 20 (7 P1). AC review rows: 3. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'case owner, a team manager or an internal auditor who reads the next action of a case' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X4 is covered by 'BR1', not by a criterion; exception X5 is covered by 'BR5', not by a criterion; exception X6 is covered by 'BR9', not by a criterion; exception X9 is covered by 'BR2', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 3 of 10 rules are covered by no criterion and no test case: BR3, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 The story adds CUSTOMER_PARTY to the closed list LOV-CAPABILITY; P1 The story adds CUSTOMER_PARTY to the closed list LOV-ROLE-CLASS; P1 The story adds CUSTOMER_PARTY to the closed list LOV-SCOPE | CG-ALL-5374, CG-ALL-5375, CG-ALL-5376 |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 8 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data; P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data; P2 Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-5378, CG-ALL-5379, CG-ALL-5380, CG-ALL-5381 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P4-006 is used with another meaning than the standard's | CG-ALL-5382 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-5389, CG-ALL-5390, CG-ALL-5391 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5387 |
| 12 | Test cases | Fail | AC6 has no test case in §16; AC7 has no test case in §16; AC9 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-035-14; P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC6, AC7, AC9; P3 §18 test lists differ from RTM v7 | CG-ALL-5383, CG-ALL-5384, CG-ALL-5385, CG-ALL-5386 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-5377 |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL24 (assumptions: none); detcheck: P2 Open decision DL24 has no assumption | CG-ALL-5393 |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E2035-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5374 | The story adds CUSTOMER_PARTY to the closed list LOV-CAPABILITY | X1 | Conflict | Product owner |
| CG-ALL-5375 | The story adds CUSTOMER_PARTY to the closed list LOV-ROLE-CLASS | X1 | Conflict | Product owner |
| CG-ALL-5376 | The story adds CUSTOMER_PARTY to the closed list LOV-SCOPE | X1 | Conflict | Product owner |
| CG-ALL-5377 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-5378 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-5379 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-5381 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5380 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5382 | MSG-P4-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5383 | Test cases not in Test Cases v8: TC-E2-035-14 | X9 | Missing | QA |
| CG-ALL-5385 | Criteria with no test case: AC6, AC7, AC9 | X9 | Missing | QA |
| CG-ALL-5387 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-5393 | Open decision DL24 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5384 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5386 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5388 | Flyway file V2035_1__nextaction_access_read_path.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5389 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5390 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5391 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5392 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | no test case in §16 |  |
| AC7 | no test case in §16 |  |
| AC9 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §5 X4: The token carries no Recovery role, or no second factor (covered by 'BR1' only) | Not specified in the source documents | |
| AC16 | §5 X5: The role code has no row in force, or is inactive (covered by 'BR5' only) | Not specified in the source documents | |
| AC17 | §5 X6: Two roles of the caller conflict, for example RW-SECADM with a business role (covered by 'BR9' only) | Not specified in the source documents | |
| AC18 | §5 X9: A reference list the answer needs is not available (covered by 'BR2' only) | Not specified in the source documents | |
| AC19 | §8 BR3, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
