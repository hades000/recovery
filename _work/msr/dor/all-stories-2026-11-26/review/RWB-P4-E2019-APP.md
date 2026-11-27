# Build-readiness review (script) — RWB-P4-E2019-APP Partner identities through the external gateway

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2019-APP (RWB P4 E2019 APP Partner identities through the external gateway v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 9 (5 P1). AC review rows: 0. Missing criteria: 10.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'partner and agency manager (RW-AGENCYMG)** and the **rwb-access service' is in the roles table | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by 'RWB-ITG-E2019-ITG', not by a criterion; exception X4 is covered by 'RWB-ITG-E2019-ITG', not by a criterion; exception X5 is covered by 'RWB-ITG-E2019-ITG', not by a criterion; exception X6 is covered by 'RWB-ITG-E2019-ITG', not by a criterion; exception X7 is covered by 'RWB-ITG-E2019-ITG', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 10 of 13 rules are covered by no criterion and no test case: BR2, BR3, BR5, BR6, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 The story adds BANK_IDENTITY_ON_PARTNER_ROUTE to the closed list LOV-SCOPE; P1 The story adds PLACED to the closed list LOV-SCOPE | CG-ALL-5253, CG-ALL-5254 |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 6 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/partner-identities/resolve is not in rwb-access.yaml; P2 HTTP errors with no message ID: 400 a claim set of the wrong shape (no message id); P1 rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data; P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | CG-ALL-5255, CG-ALL-5256, CG-ALL-5257, CG-ALL-5258 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P7-003; §14 lists 6 messages | — |
| 10 | Screens and states | Partial | §15 names no screen and does not say there is none | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-019-01 to TC-E2-019-11; P3 §18 test lists differ from RTM v7 | CG-ALL-5259, CG-ALL-5260 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P4-E1022-APP, RWB-P4-E1039-APP, RWB-P4-E2019-INF); 13 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL03 (assumptions: ASM-0189, ASM-0193, ASM-0578, ASM-2567); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL40 (assumptions: ASM-0422, ASM-2705) | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P4-E2019-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_partner | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P4-E1022-APP, RWB-P4-E1039-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5253 | The story adds BANK_IDENTITY_ON_PARTNER_ROUTE to the closed list LOV-SCOPE | X1 | Conflict | Product owner |
| CG-ALL-5254 | The story adds PLACED to the closed list LOV-SCOPE | X1 | Conflict | Product owner |
| CG-ALL-5255 | POST /api/recovery/access/v1/partner-identities/resolve is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5257 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-5258 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5256 | HTTP errors with no message ID: 400 a claim set of the wrong shape (no message id) | X5 | Missing | Business analyst |
| CG-ALL-5259 | Test cases not in Test Cases v8: TC-E2-019-01 to TC-E2-019-11 | X9 | Missing | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5260 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5261 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X3: `amr` holds `pwd` only (covered by 'RWB-ITG-E2019-ITG' only) | Not specified in the source documents | |
| AC11 | §5 X4: The claims name no partner role, or an unknown role code, or a role of class `BANK_USER` (covered by 'RWB-ITG-E2019-ITG' only) | Not specified in the source documents | |
| AC12 | §5 X5: The claims name two partner roles, or a partner role and a bank role (covered by 'RWB-ITG-E2019-ITG' only) | Not specified in the source documents | |
| AC13 | §5 X6: The firm state claim is `SUSPENDED` or `EXITED`, or the contract end is before today (covered by 'RWB-ITG-E2019-ITG' only) | Not specified in the source documents | |
| AC14 | §5 X7: The claim asserts no active binding of the identity to a firm (covered by 'RWB-ITG-E2019-ITG' only) | Not specified in the source documents | |
| AC15 | §8 BR2, BR3, BR5, BR6, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC18 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC19 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
