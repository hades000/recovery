# Build-readiness review (script) — RWB-P4-E8019-APP Control access by role and by agent

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E8019-APP (RWB P4 E8019 APP Control access by role and by agent v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E8-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 14, Partial 4, Fail 7. Detcheck rows: 15 (4 P1). AC review rows: 2. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'security administrator' is in the roles table | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 3 of 15 rules are covered by no criterion and no test case: BR3, BR9, BR15; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Pass | §10 has 12 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 9 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-5691 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 GET /api/recovery/source-data/v1/iam-groups is not published by rwb-source-data; P1 rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data; P2 Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 (+1 more) | CG-ALL-5681, CG-ALL-5682, CG-ALL-5683, CG-ALL-5684, CG-ALL-5685 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P2 MSG-P7-002 is used with another meaning than the standard's | CG-ALL-5686 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-41 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-5692, CG-ALL-5693, CG-ALL-5694 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC6 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E8-019-01, TC-E8-019-02, TC-E8-019-03, TC-E8-019-04, TC-E8-019-05, TC-E8-019-06, TC-E8-019-07, TC-E8-019-08, TC-E8-019-09; P2 Criteria with no test case: AC6; P3 §18 test lists differ from RTM v7 | CG-ALL-5687, CG-ALL-5688, CG-ALL-5689 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 5 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P4-E8019-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5681 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-5682 | GET /api/recovery/source-data/v1/iam-groups is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-5683 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-5685 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5684 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5686 | MSG-P7-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5687 | Test cases not in Test Cases v8: TC-E8-019-01, TC-E8-019-02, TC-E8-019-03, TC-E8-019-04, TC-E8-019-05, TC-E8-019-06, TC-E8-019-07, TC-E8-019-08, TC-E8-019-09 | X9 | Missing | QA |
| CG-ALL-5688 | Criteria with no test case: AC6 | X9 | Missing | QA |
| CG-ALL-5691 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5689 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5690 | Flyway file V8019_1__permission_change_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5692 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5693 | SCR-41 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5694 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5695 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | no test case in §16 |  |
| AC1 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR3, BR9, BR15 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
