# Build-readiness review (script) — RWB-P4-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2036-APP (RWB P4 E2036 APP Queue write interface for models and agents v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-036 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 5, Fail 7. Detcheck rows: 12 (3 P1). AC review rows: 3. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'security administrator (RW-SECADM), a risk and model risk officer (RW-RISK), and the model or agent that writes to a queue' is in the roles table | — |
| 2 | Links | Pass | §18 has 18 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 4 of 12 rules are covered by no criterion and no test case: BR7, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-5394, CG-ALL-5402 |
| 8 | Contract | Fail | detcheck: P1 rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data; P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-5395, CG-ALL-5396, CG-ALL-5397 |
| 9 | Messages | Partial | §14 lists 12 messages; detcheck: P2 MSG-P4-001 is used with another meaning than the standard's | CG-ALL-5398 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-07 has no empty, loading, error, no access state in the story | CG-ALL-5403, CG-ALL-5404 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC3 has no test case in §16; AC4 has no test case in §16; AC7 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC3, AC4, AC7; P3 §18 test lists differ from RTM v7 | CG-ALL-5399, CG-ALL-5400, CG-ALL-5401 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E2036-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5395 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-5396 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-5397 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5394 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5398 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5400 | Criteria with no test case: AC3, AC4, AC7 | X9 | Missing | QA |
| CG-ALL-5402 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5399 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5401 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5403 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5404 | SCR-07 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5405 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC3 | no test case in §16 |  |
| AC4 | no test case in §16 |  |
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR7, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
