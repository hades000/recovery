# Build-readiness review (script) — RWB-P4-E1016-APP Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1016-APP (RWB P4 E1016 APP Access control per data product and catalog entries v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-016 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 6, Fail 6. Detcheck rows: 13 (4 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'security administrator (RW-SECADM), a compliance and PDPA officer (RW-COMPLY) and every caller of the authorise contract' is in the roles table | — |
| 2 | Links | Pass | §18 has 3 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 6 of 15 rules are covered by no criterion and no test case: BR1, BR11, BR12, BR13, BR14, BR15; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 22 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-4885 |
| 8 | Contract | Fail | detcheck: P1 GET /masking-policies is not in rwb-access.yaml; P1 POST /authorise is not in rwb-access.yaml; P2 HTTP errors with no message ID: 503 the reference lists are unavailable; P1 rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data (+1 more) | CG-ALL-4876, CG-ALL-4877, CG-ALL-4878, CG-ALL-4879, CG-ALL-4880 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-43 has no empty, loading, error, no access state in the story; P3 SCR-47 has no empty, loading, error, no access state in the story | CG-ALL-4886, CG-ALL-4887 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4884 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-016-10, TC-E1-016-11, TC-E1-016-12; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-4881, CG-ALL-4882, CG-ALL-4883 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E1016-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4876 | GET /masking-policies is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4877 | POST /authorise is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4879 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-4880 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4878 | HTTP errors with no message ID: 503 the reference lists are unavailable | X5 | Missing | Business analyst |
| CG-ALL-4881 | Test cases not in Test Cases v8: TC-E1-016-10, TC-E1-016-11, TC-E1-016-12 | X9 | Missing | QA |
| CG-ALL-4884 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-4885 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4882 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-4883 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4886 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4887 | SCR-47 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4888 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR1, BR11, BR12, BR13, BR14, BR15 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
