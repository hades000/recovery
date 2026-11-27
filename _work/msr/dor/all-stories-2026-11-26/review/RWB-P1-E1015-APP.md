# Build-readiness review (script) — RWB-P1-E1015-APP Freshness stamp per data product

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1015-APP (RWB P1 E1015 APP Freshness stamp per data product v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-015 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 19 (3 P1). AC review rows: 0. Missing criteria: 13.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward and data product owner (RW-DATASTEW)' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by AC2, which this story neither owns nor names as owned by another story; exception X2 is covered by AC4, which this story neither owns nor names as owned by another story; exception X3 is covered by AC5, which this story neither owns nor names as owned by another story; exception X4 is covered by AC6, which this story neither owns nor names as owned by another story; exception X5 is covered by AC7, which this story neither owns nor names as owned by another story; exception X7 is covered by AC11, which this story neither owns nor names as owned by another story; exception X8 is covered by AC10, which this story neither owns nor names as owned by another story; exception X9 is covered by 'TC-E1-015-09', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 3 of 11 rules are covered by no criterion and no test case: BR9, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 24 data rows; detcheck: P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2103 |
| 8 | Contract | Fail | POST `/business-days/{date}/ready` has no idempotency key; detcheck: P1 GET /freshness is not in rwb-source-data.yaml; P1 POST /business-days/{date}/ready is not in rwb-source-data.yaml; P2 Payload of rwb.source-data.AceDataReady.v1 differs from Kafka Catalog v1; P2 Payload of rwb.source-data.AceDataLate.v1 differs from Kafka Catalog v1 (+5 more) | CG-ALL-2104, CG-ALL-2105, CG-ALL-2106, CG-ALL-2107, CG-ALL-2108, CG-ALL-2109, CG-ALL-2110, CG-ALL-2111, CG-ALL-2112 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P4-001 is used with another meaning than the standard's | CG-ALL-2113, CG-ALL-2114 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-2119, CG-ALL-2120 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2118 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-015-10, TC-E1-015-11, TC-E1-015-12; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-2115, CG-ALL-2116, CG-ALL-2117 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1015-OPS, RWB-P1-E1069-APP); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL06 (assumptions: ASM-0189, ASM-2559, ASM-2608, ASM-2776); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P1-E1015-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1001-APP, RWB-P1-E1069-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2104 | GET /freshness is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2105 | POST /business-days/{date}/ready is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2108 | Workflow AceIngestCheckWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2103 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2106 | Payload of rwb.source-data.AceDataReady.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2107 | Payload of rwb.source-data.AceDataLate.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2109 | Activity stampProducts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2110 | Activity markStale is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2111 | Activity publishAceDataReady, publishAceDataLate is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2112 | Activity checkDailyCompleteness is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2114 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-2115 | Test cases not in Test Cases v8: TC-E1-015-10, TC-E1-015-11, TC-E1-015-12 | X9 | Missing | QA |
| CG-ALL-2118 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2113 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2116 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-2117 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2119 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2120 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2121 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X1: No COMPLETED batch for the expected business date by the expected-by time (covered by AC2, which exist nowhere in this story) | Not specified in the source documents | |
| AC13 | §5 X2: The batch row is FAILED (covered by AC4, which exist nowhere in this story) | Not specified in the source documents | |
| AC14 | §5 X3: The same COMPLETED batch row is read twice (covered by AC5, which exist nowhere in this story) | Not specified in the source documents | |
| AC15 | §5 X4: A late batch arrives after the stale flag (covered by AC6, which exist nowhere in this story) | Not specified in the source documents | |
| AC16 | §5 X5: A batch completes one minute before the expected-by time (covered by AC7, which exist nowhere in this story) | Not specified in the source documents | |
| AC17 | §5 X7: One source of a multi-source product is late (covered by AC11, which exist nowhere in this story) | Not specified in the source documents | |
| AC18 | §5 X8: A source that the day's jobs do not read is late (covered by AC10, which exist nowhere in this story) | Not specified in the source documents | |
| AC19 | §5 X9: A role without the right reads the stamps (covered by 'TC-E1-015-09' only) | Not specified in the source documents | |
| AC20 | §8 BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC21 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC22 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC23 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC24 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
