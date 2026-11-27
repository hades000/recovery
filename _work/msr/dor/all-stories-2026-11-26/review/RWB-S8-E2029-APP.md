# Build-readiness review (script) — RWB-S8-E2029-APP Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S8-E2029-APP (RWB S8 E2029 APP Deviation screening agent evaluation and L1 on one segment [E3b] v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-deviation |
| Legacy key | RWB-E2-029 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 14 (3 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'Section 14', not by a criterion; exception X8 is covered by 'Section 17, BR8', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Fail | §9 has 4 transitions; detcheck: P1 The story adds DEV_FLAGGED to the closed list LOV-DEVIATION; P1 The story adds DEV_FLAGGED to the closed list LOV-RAISED-BY | CG-ALL-11370, CG-ALL-11371 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 18 data rows | — |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no Workbench identity; P1 rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1` with retry and `.dlt; P2 Payload of rwb.deviation.DeviationRaised.v1 differs from Kafka Catalog v1 | CG-ALL-11372, CG-ALL-11373, CG-ALL-11374 |
| 9 | Messages | Pass | §14 lists 6 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-06 has no empty, loading, error, no access state in the story; P3 SCR-08 has no empty, loading, error, no access state in the story; P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-11379, CG-ALL-11380, CG-ALL-11381, CG-ALL-11382 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-11377 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-11375, CG-ALL-11376 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S8-E2029-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-agent; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11370 | The story adds DEV_FLAGGED to the closed list LOV-DEVIATION | X1 | Conflict | Product owner |
| CG-ALL-11371 | The story adds DEV_FLAGGED to the closed list LOV-RAISED-BY | X1 | Conflict | Product owner |
| CG-ALL-11373 | rwb.deviation.DeviationRaised.v1 is on topic rwb.deviation.events.v1 in the catalog, not rwb.deviation.events.v1` with retry and `.dlt | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11372 | HTTP errors with no message ID: 401 no Workbench identity | X5 | Missing | Business analyst |
| CG-ALL-11374 | Payload of rwb.deviation.DeviationRaised.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-11377 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11375 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11376 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11378 | Flyway file V2029_1__deviation_raise_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-11379 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11380 | SCR-06 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11381 | SCR-08 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11382 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11383 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X6: The policy read of RWB-P10-E2029-CON does not answer inside 2 s, so the version in force is unknown (covered by 'Section 14' only) | Not specified in the source documents | |
| AC12 | §5 X8: A component, a statement or a test reaches a `recovery_case` row, a `rwb_agent` or `rwb_decision` table, a `v_ace_*` vie (covered by 'Section 17, BR8' only) | Not specified in the source documents | |
| AC13 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
