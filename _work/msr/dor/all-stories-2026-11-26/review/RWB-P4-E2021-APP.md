# Build-readiness review (script) — RWB-P4-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2021-APP (RWB P4 E2021 APP Letter dispatch loop with proof of delivery from WIN v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 14 (5 P1). AC review rows: 3. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'litigation officer who requests a notice, reads it on SCR-18 and follows it through the WIN dispatch and the proof of delivery, and the recovery service identity that runs JOB-10' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'BR7', not by a criterion; §7 holds 10 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 4 of 10 rules are covered by no criterion and no test case: BR1, BR5, BR6, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-PTY-007, DF-PTY-016, DF-REF-039; §11 has 10 data rows; detcheck: P2 Name `contact_point` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-5270 |
| 8 | Contract | Fail | POST `/api/recovery/access/v1/authorise` has no idempotency key; detcheck: P1 POST /api/recovery/access/v1/authorise is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/me/permissions is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/masking-policies is not in rwb-access.yaml; P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data (+2 more) | CG-ALL-5271, CG-ALL-5272, CG-ALL-5273, CG-ALL-5274, CG-ALL-5275, CG-ALL-5276 |
| 9 | Messages | Pass | §14 lists 8 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story | CG-ALL-5281, CG-ALL-5282 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC5 has no test case in §16; AC6 has no test case in §16; AC8 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC5, AC6, AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-5277, CG-ALL-5278, CG-ALL-5279 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E2021-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5271 | POST /api/recovery/access/v1/authorise is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5272 | GET /api/recovery/access/v1/me/permissions is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5273 | GET /api/recovery/access/v1/masking-policies is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5274 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-5276 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5270 | Name `contact_point` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5275 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5278 | Criteria with no test case: AC5, AC6, AC8 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5277 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5279 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5280 | Flyway file V2021_1__access_dispatch_read_indexes.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5281 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5282 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5283 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no test case in §16 |  |
| AC6 | no test case in §16 |  |
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X8: A second call arrives with the same `Idempotency-Key` (covered by 'BR7' only) | Not specified in the source documents | |
| AC14 | §8 BR1, BR5, BR6, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
