# Build-readiness review (script) — RWB-P1-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E2021-APP (RWB P1 E2021 APP Letter dispatch loop with proof of delivery from WIN v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E2-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 8, Fail 8. Detcheck rows: 20 (11 P1). AC review rows: 1. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'dispatch loop of rwb-comms (service actor)' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by '§12.1', not by a criterion; exception X2 is covered by '§10', not by a criterion; exception X3 is covered by '§12.1', not by a criterion; exception X6 is covered by '§12.1', not by a criterion; exception X8 is covered by '§12.1', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 2 of 9 rules are covered by no criterion and no test case: BR6, BR8; §8 has 9 rules | — |
| 5 | State transitions | Fail | §9 has 3 transitions; detcheck: P1 The story adds POSTAL to the closed list LOV-SEND-STATUS; P1 The story adds RR223344556TH to the closed list LOV-SEND-STATUS; P1 The story adds CONTACT_STOP_X1 to the closed list LOV-SEND-STATUS; P1 The story adds POSTAL to the closed list LOV-CONDUCT (+4 more) | CG-ALL-2434, CG-ALL-2435, CG-ALL-2436, CG-ALL-2437, CG-ALL-2438, CG-ALL-2439, CG-ALL-2440, CG-ALL-2441 |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 24 data rows; detcheck: P2 Name `tr_interaction_append_only` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2442 |
| 8 | Contract | Fail | detcheck: P1 rwb-source-data.yaml holds conductCheck as a closed enum while the story reads LOV-CONDUCT as data; P1 rwb-source-data.yaml holds eventCode as a closed enum while the story reads LOV-LEDGER-EVENT as data; P1 rwb-source-data.yaml holds deliveryStatus as a closed enum while the story reads LOV-SEND-STATUS as data | CG-ALL-2443, CG-ALL-2444, CG-ALL-2445 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P3-004, MSG-P6-003; §14 lists 8 messages; detcheck: P2 MSG-GEN-004 is used with another meaning than the standard's | CG-ALL-2446 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story | CG-ALL-2451, CG-ALL-2452 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2450 |
| 12 | Test cases | Fail | AC7 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC7; P3 §18 test lists differ from RTM v7 | CG-ALL-2447, CG-ALL-2448, CG-ALL-2449 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P1-E2021-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2434 | The story adds POSTAL to the closed list LOV-SEND-STATUS | X1 | Conflict | Product owner |
| CG-ALL-2435 | The story adds RR223344556TH to the closed list LOV-SEND-STATUS | X1 | Conflict | Product owner |
| CG-ALL-2436 | The story adds CONTACT_STOP_X1 to the closed list LOV-SEND-STATUS | X1 | Conflict | Product owner |
| CG-ALL-2437 | The story adds POSTAL to the closed list LOV-CONDUCT | X1 | Conflict | Product owner |
| CG-ALL-2438 | The story adds OUT to the closed list LOV-CONDUCT | X1 | Conflict | Product owner |
| CG-ALL-2439 | The story adds POSTAL to the closed list LOV-LEDGER-EVENT | X1 | Conflict | Product owner |
| CG-ALL-2440 | The story adds OUT to the closed list LOV-LEDGER-EVENT | X1 | Conflict | Product owner |
| CG-ALL-2441 | The story adds OUT to the closed list LOV-SEND-STATUS | X1 | Conflict | Product owner |
| CG-ALL-2443 | rwb-source-data.yaml holds conductCheck as a closed enum while the story reads LOV-CONDUCT as data | X5 | Conflict | Solution architect |
| CG-ALL-2444 | rwb-source-data.yaml holds eventCode as a closed enum while the story reads LOV-LEDGER-EVENT as data | X5 | Conflict | Solution architect |
| CG-ALL-2445 | rwb-source-data.yaml holds deliveryStatus as a closed enum while the story reads LOV-SEND-STATUS as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2442 | Name `tr_interaction_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2446 | MSG-GEN-004 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-2448 | Criteria with no test case: AC7 | X9 | Missing | QA |
| CG-ALL-2450 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2447 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-2449 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2451 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2452 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2453 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC7 | no test case in §16; message MSG-P3-004, MSG-P6-003 is not in §14 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X1: `productCode` is not a product this service serves, or `caseId` is missing or malformed (covered by '§12.1' only) | Not specified in the source documents | |
| AC14 | §5 X2: A caller without the right calls the read or the append (covered by '§10' only) | Not specified in the source documents | |
| AC15 | §5 X3: A view, `contact_point_ext` or the stamp does not answer inside 5 s, or answers an error (covered by '§12.1' only) | Not specified in the source documents | |
| AC16 | §5 X6: The case of the append does not exist or is outside the caller's scope (covered by '§12.1' only) | Not specified in the source documents | |
| AC17 | §5 X8: The ledger cannot be written (covered by '§12.1' only) | Not specified in the source documents | |
| AC18 | §8 BR6, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC19 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
