# Build-readiness review (script) — RWB-P2-E2033-CON Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E2033-CON (RWB P2 E2033 CON Case and queue list with status, owner and ageing - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E2-033 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 7, Fail 5. Detcheck rows: 13 (6 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 12 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 The story adds CAR to the closed list LOV-CASE-STATUS; P1 The story adds CAR to the closed list LOV-PRODUCT; P1 The story adds CAR to the closed list LOV-STAGE | CG-ALL-3192, CG-ALL-3193, CG-ALL-3194 |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | 9 row(s) of §11 have no BR Field ID; §11 has 9 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /case-list is not in rwb-integration.yaml; P1 GET /case-list/export is not in rwb-integration.yaml; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 404 a case read that names no case | CG-ALL-3195, CG-ALL-3196, CG-ALL-3197, CG-ALL-3198 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P3 MSG-GEN-007 text differs from the Error and Message Standard v4; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-3199, CG-ALL-3200 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story | CG-ALL-3204 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3203 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P2-E2033-CON-01, TC-P2-E2033-CON-02, TC-P2-E2033-CON-03, TC-P2-E2033-CON-04, TC-P2-E2033-CON-05, TC-P2-E2033-CON-06; P3 §18 test lists differ from RTM v7 | CG-ALL-3201, CG-ALL-3202 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3192 | The story adds CAR to the closed list LOV-CASE-STATUS | X1 | Conflict | Product owner |
| CG-ALL-3193 | The story adds CAR to the closed list LOV-PRODUCT | X1 | Conflict | Product owner |
| CG-ALL-3194 | The story adds CAR to the closed list LOV-STAGE | X1 | Conflict | Product owner |
| CG-ALL-3195 | GET /case-list is not in rwb-integration.yaml | X5 | Missing | Solution architect |
| CG-ALL-3196 | GET /case-list/export is not in rwb-integration.yaml | X5 | Missing | Solution architect |
| CG-ALL-3197 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3198 | HTTP errors with no message ID: 404 a case read that names no case | X5 | Missing | Business analyst |
| CG-ALL-3200 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3203 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3199 | MSG-GEN-007 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3201 | Test cases not in Test Cases v8: TC-P2-E2033-CON-01, TC-P2-E2033-CON-02, TC-P2-E2033-CON-03, TC-P2-E2033-CON-04, TC-P2-E2033-CON-05, TC-P2-E2033-CON-06 | X9 | Missing | QA |
| CG-ALL-3202 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3204 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
