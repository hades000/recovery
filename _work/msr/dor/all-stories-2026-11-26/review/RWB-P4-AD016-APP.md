# Build-readiness review (script) — RWB-P4-AD016-APP Load the delegation of authority table

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-AD016-APP (RWB P4 AD016 APP Load the delegation of authority table v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-AD-016 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 12 (5 P1). AC review rows: 3. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'reference data administrator, with the Risk and model risk officer who approves the version and the access service that answers the approval router' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | AC11 has no When; §7 holds 11 owned criteria in Gherkin; §5 has 13 exception paths | — |
| 4 | Business rules | Partial | 1 of 13 rules are covered by no criterion and no test case: BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 15 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 10 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /admin/doa-loads is not in rwb-access.yaml; P1 POST /admin/doa-loads/{loadId}/approve is not in rwb-access.yaml; P1 GET /admin/doa-loads/{loadId} is not in rwb-access.yaml; P1 GET /doa-limits is not in rwb-access.yaml (+2 more) | CG-ALL-4815, CG-ALL-4816, CG-ALL-4817, CG-ALL-4818, CG-ALL-4819, CG-ALL-4820 |
| 9 | Messages | Partial | §14 lists 10 messages; detcheck: P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-4821 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-41 has no empty, loading, error, no access state in the story | CG-ALL-4824, CG-ALL-4825 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-AD-016-05, TC-AD-016-06, TC-AD-016-07, TC-AD-016-08, TC-AD-016-09; P3 §18 test lists differ from RTM v7 | CG-ALL-4822, CG-ALL-4823 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P4-E1038-APP); 8 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL18 (assumptions: ASM-2569, ASM-2839, ASM-2859, ASM-2883) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P4-AD016-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P4-E1038-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4815 | POST /admin/doa-loads is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4816 | POST /admin/doa-loads/{loadId}/approve is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4817 | GET /admin/doa-loads/{loadId} is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4818 | GET /doa-limits is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4819 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4820 | Payload of rwb.access.DoaLimitChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4821 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-4822 | Test cases not in Test Cases v8: TC-AD-016-05, TC-AD-016-06, TC-AD-016-07, TC-AD-016-08, TC-AD-016-09 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4823 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4824 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4825 | SCR-41 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4826 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC11 | no When: the trigger is not stated |  |
| AC9 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |
| AC10 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
