# Build-readiness review (script) — RWB-P4-E2019-CON Partner identities through the external gateway

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2019-CON (RWB P4 E2019 CON Partner identities through the external gateway - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 7, Fail 5. Detcheck rows: 6 (2 P1). AC review rows: 4. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead of rwb-access with the external gateway owner' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Partial | AC2 has no When; AC3 has no When; AC4 has no When; AC5 has no When; §7 holds 6 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 13 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 The story adds PLACED to the closed list LOV-SCOPE | CG-ALL-5262 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 6 row(s) of §11 have no BR Field ID; §11 has 6 data rows | — |
| 8 | Contract | Fail | POST `/partner-identities/resolve` has no idempotency key; detcheck: P1 POST /partner-identities/resolve is not in rwb-access.yaml; P2 HTTP errors with no message ID: 400 a claim set of the wrong shape with the field named and no message id | CG-ALL-5263, CG-ALL-5264 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | §15 names no screen and does not say there is none | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E2-019-CON-01, TC-E2-019-CON-02, TC-E2-019-CON-03, TC-E2-019-CON-04, TC-E2-019-CON-05, TC-E2-019-CON-06; P3 §18 test lists differ from RTM v7 | CG-ALL-5265, CG-ALL-5266 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5262 | The story adds PLACED to the closed list LOV-SCOPE | X1 | Conflict | Product owner |
| CG-ALL-5263 | POST /partner-identities/resolve is not in rwb-access.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5264 | HTTP errors with no message ID: 400 a claim set of the wrong shape with the field named and no message id | X5 | Missing | Business analyst |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5265 | Test cases not in Test Cases v8: TC-E2-019-CON-01, TC-E2-019-CON-02, TC-E2-019-CON-03, TC-E2-019-CON-04, TC-E2-019-CON-05, TC-E2-019-CON-06 | X9 | Missing | QA |
| CG-ALL-5266 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5267 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | no When: the trigger is not stated |  |
| AC3 | no When: the trigger is not stated |  |
| AC4 | no When: the trigger is not stated |  |
| AC5 | no When: the trigger is not stated |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
