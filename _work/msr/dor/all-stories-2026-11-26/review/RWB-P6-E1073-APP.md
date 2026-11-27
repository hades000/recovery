# Build-readiness review (script) — RWB-P6-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E1073-APP (RWB P6 E1073 APP Rule authoring, validation, test scenarios, approval and rollback in Drools v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E1-073 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 8, Fail 8. Detcheck rows: 13 (3 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'rwb-comms service identity (the SY-RULES evaluator inside rwb-comms)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'TC-E1-073-01 (the record and the outbox row in one transacti', not by a criterion; exception X10 is covered by 'TC-E1-073-16, TC-E1-073-20', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 2 of 14 rules are covered by no criterion and no test case: BR11, BR12; §8 has 14 rules; detcheck: P2 Rule ID ALLOC-014 used in the criteria exists in no current source; P2 Rule ID ALLOC-015 used in the criteria exists in no current source; P2 Rule ID ALLOC-999 used in the criteria exists in no current source | CG-ALL-6460, CG-ALL-6461, CG-ALL-6462 |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | 4 row(s) of §11 have no BR Field ID; §11 has 13 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} is not published by rwb-decision; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 rwb-comms is not a consumer of rwb.decision.RulePackageInForce.v1 in Kafka Catalog v1 | CG-ALL-6456, CG-ALL-6458, CG-ALL-6459 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-6463 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story | CG-ALL-6467 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC7 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 20 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC7 | CG-ALL-6464, CG-ALL-6465 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-6457 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (20) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P6-E1073-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6456 | GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-6457 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-6458 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6459 | rwb-comms is not a consumer of rwb.decision.RulePackageInForce.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6460 | Rule ID ALLOC-014 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-6461 | Rule ID ALLOC-015 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-6462 | Rule ID ALLOC-999 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-6463 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-6465 | Criteria with no test case: AC7 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6464 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6466 | Flyway file V1073_1__local_rule_copy.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6467 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6468 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X9: The local decision record cannot be written for an evaluation (covered by 'TC-E1-073-01 (the record and the outbox row in one transacti' only) | Not specified in the source documents | |
| AC17 | §5 X10: A caller without the read right asks for the local copy or calls the model fetch (covered by 'TC-E1-073-16, TC-E1-073-20' only) | Not specified in the source documents | |
| AC18 | §8 BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
