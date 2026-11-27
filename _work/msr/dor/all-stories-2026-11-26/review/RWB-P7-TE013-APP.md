# Build-readiness review (script) — RWB-P7-TE013-APP Agent runtime client with fallback

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-TE013-APP (RWB P7 TE013 APP Agent runtime client with fallback v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-TE-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 6, Fail 9. Detcheck rows: 14 (4 P1). AC review rows: 1. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'internal audit reader (RW-AUDIT) of the agent steps and of the decision service itself' is in the roles table | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 7 of 16 rules are covered by no criterion and no test case: BR1, BR2, BR11, BR12, BR13, BR14, BR16; §8 has 16 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Fail | §11 has 15 data rows; detcheck: P1 Index column decision_log_entry.decided_at DESC is not a field of decision_log_entry in LDM v9; P1 Index column decision_log_entry.(actions->>'fallback' is not a field of decision_log_entry in LDM v9 | CG-ALL-7470, CG-ALL-7471 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no session; 404 an unknown entry id; 503 the ledger was not read. Every error is an RFC 9457 problem response with `messageId` set; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-7472, CG-ALL-7474 |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's | CG-ALL-7475 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-38 has no empty, loading, error, no access state in the story; P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-7481, CG-ALL-7482 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7479 |
| 12 | Test cases | Fail | AC8 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-7476, CG-ALL-7477, CG-ALL-7478 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7473 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-TE013-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7470 | Index column decision_log_entry.decided_at DESC is not a field of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7471 | Index column decision_log_entry.(actions->>'fallback' is not a field of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7473 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7474 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7472 | HTTP errors with no message ID: 401 no session; 404 an unknown entry id; 503 the ledger was not read. Every error is an RFC 9457 problem response with `messageId` set | X5 | Missing | Business analyst |
| CG-ALL-7475 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7477 | Criteria with no test case: AC8 | X9 | Missing | QA |
| CG-ALL-7479 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7476 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-7478 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7480 | Flyway file V2026_11_02__declog_agent_step_profile.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7481 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7482 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7483 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR11, BR12, BR13, BR14, BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
