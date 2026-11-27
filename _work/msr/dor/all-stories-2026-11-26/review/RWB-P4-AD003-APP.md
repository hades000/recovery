# Build-readiness review (script) — RWB-P4-AD003-APP Scope per role

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-AD003-APP (RWB P4 AD003 APP Scope per role v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-AD-003 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 8 (5 P1). AC review rows: 0. Missing criteria: 10.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'application owner' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by 'TC-AD-003-03', not by a criterion; exception X4 is covered by 'X4', not by a criterion; exception X5 is covered by 'TC-AD-003-04', not by a criterion; exception X7 is covered by 'TC-AD-003-04', not by a criterion; exception X8 is covered by 'X8', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 11 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 The story adds SCOPE to the closed list LOV-SCOPE | CG-ALL-4557 |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | 2 row(s) of §11 have no BR Field ID; BR Field IDs not in LDM v9: DF-REF-039; §11 has 12 data rows | — |
| 8 | Contract | Fail | PATCH `/admin/role-scopes/{roleCode}` has no idempotency key; detcheck: P1 GET /admin/role-scopes is not in rwb-access.yaml; P1 PATCH /admin/role-scopes/{roleCode} is not in rwb-access.yaml; P2 HTTP errors with no message ID: 404 unknown or inactive role; 409 stale `If-Match` or a repeated key answered differently; P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data (+1 more) | CG-ALL-4558, CG-ALL-4559, CG-ALL-4560, CG-ALL-4561, CG-ALL-4562 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-006; §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-4563 |
| 11 | Guardrails | Partial | §17 does not state the personal data rule | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases | — |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 5 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P4-AD003-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4557 | The story adds SCOPE to the closed list LOV-SCOPE | X1 | Conflict | Product owner |
| CG-ALL-4558 | GET /admin/role-scopes is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4559 | PATCH /admin/role-scopes/{roleCode} is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4561 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-4562 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4560 | HTTP errors with no message ID: 404 unknown or inactive role; 409 stale `If-Match` or a repeated key answered differently | X5 | Missing | Business analyst |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4563 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4564 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X3: The posted value is outside `LOV-SCOPE`, or a required field is empty (covered by 'TC-AD-003-03' only) | Not specified in the source documents | |
| AC4 | §5 X4: The `If-Match` version is stale, or the role code does not exist or is inactive (covered by 'X4' only) | Not specified in the source documents | |
| AC5 | §5 X5: The decision-record library answers 503 while a change is being recorded (covered by 'TC-AD-003-04' only) | Not specified in the source documents | |
| AC6 | §5 X7: The refusal entry cannot be written (covered by 'TC-AD-003-04' only) | Not specified in the source documents | |
| AC7 | §5 X8: The access owner does not answer inside the 2 s budget while a consumer builds its predicate (covered by 'X8' only) | Not specified in the source documents | |
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC9 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC10 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
