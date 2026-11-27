# Build-readiness review (script) — RWB-P7-E1021-APP Transfer rules and engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E1021-APP (RWB P7 E1021 APP Transfer rules and engine v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E1-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 4, Fail 8. Detcheck rows: 11 (2 P1). AC review rows: 1. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR), a litigation officer (RW-LITOFF) and the central ledger itself' is in the roles table | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 1 of 9 rules are covered by no criterion and no test case: BR4; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Pass | §11 has 14 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /rule-models/{packageCode}/{version} is not in rwb-decision.yaml; P2 Payload of rwb.decision.RulePackageInForce.v1 differs from Kafka Catalog v1 | CG-ALL-6906, CG-ALL-6908 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's; P2 MSG-P7-012 is used with another meaning than the standard's | CG-ALL-6909, CG-ALL-6910 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-6915 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC6 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC6; P3 §18 test lists differ from RTM v7 | CG-ALL-6911, CG-ALL-6912, CG-ALL-6913 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-6907 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E1021-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6906 | GET /rule-models/{packageCode}/{version} is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-6907 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6908 | Payload of rwb.decision.RulePackageInForce.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6909 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6910 | MSG-P7-012 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6912 | Criteria with no test case: AC6 | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6911 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6913 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6914 | Flyway file V1021_1__transfer_record.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6915 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6916 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §8 BR4 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
