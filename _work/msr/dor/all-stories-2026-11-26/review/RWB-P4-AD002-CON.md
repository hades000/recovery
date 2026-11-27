# Build-readiness review (script) — RWB-P4-AD002-CON Permission matrix as a versioned load

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-AD002-CON (RWB P4 AD002 CON Permission matrix as a versioned load - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-AD-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 6, Fail 6. Detcheck rows: 15 (8 P1). AC review rows: 6. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | AC2 has no When; AC3 has no When; AC4 has no When; AC5 has no When; §7 holds 7 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 14 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 The story adds MATRIX to the closed list LOV-CAPABILITY | CG-ALL-4542 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 11 row(s) of §11 have no BR Field ID; §11 has 11 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-4552 |
| 8 | Contract | Fail | POST `/admin/permission-matrix-loads` has no idempotency key; detcheck: P1 POST /admin/permission-matrix-loads is not in rwb-access.yaml; P1 GET /admin/permission-matrix is not in rwb-access.yaml; P1 GET /admin/permission-matrix-versions/{matrixVersion} is not in rwb-access.yaml; P1 GET /admin/permission-matrix-versions is not in rwb-access.yaml (+3 more) | CG-ALL-4543, CG-ALL-4544, CG-ALL-4545, CG-ALL-4546, CG-ALL-4547, CG-ALL-4548, CG-ALL-4549 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-004; §14 lists 7 messages; detcheck: P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-4550 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-40 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-4553, CG-ALL-4554, CG-ALL-4555 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC4 has no test case in §16; AC5 has no test case in §16; AC6 has no test case in §16; AC7 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P2 Criteria with no test case: AC4, AC5, AC6, AC7 | CG-ALL-4551 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4542 | The story adds MATRIX to the closed list LOV-CAPABILITY | X1 | Conflict | Product owner |
| CG-ALL-4543 | POST /admin/permission-matrix-loads is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4544 | GET /admin/permission-matrix is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4545 | GET /admin/permission-matrix-versions/{matrixVersion} is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4546 | GET /admin/permission-matrix-versions is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4547 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-4548 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-4549 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4550 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-4551 | Criteria with no test case: AC4, AC5, AC6, AC7 | X9 | Missing | QA |
| CG-ALL-4552 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4553 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4554 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4555 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4556 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | no When: the trigger is not stated |  |
| AC3 | no When: the trigger is not stated |  |
| AC4 | no When: the trigger is not stated; no test case in §16 |  |
| AC5 | no When: the trigger is not stated; no test case in §16 |  |
| AC6 | no test case in §16; message MSG-P4-004 is not in §14 |  |
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
