# Build-readiness review (script) — RWB-ITG-E2008-ITG Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2008-ITG (RWB ITG E2008 ITG Payment matching with the missed payment event - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-008 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 12 (4 P1). AC review rows: 3. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'member of the integration and QA team' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 4 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR8; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 2 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 26 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-604 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/admin/data-quality/exceptions is not published by rwb-source-data; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-596, CG-ALL-597, CG-ALL-599 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P7-003; §14 lists 5 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-600 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-28 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-605, CG-ALL-606, CG-ALL-607 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 10 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-008-10-ITG; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-601, CG-ALL-602, CG-ALL-603 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 8 build dependencies are not done yet (RWB-P1-E1069-APP, RWB-P1-E2008-APP, RWB-P3-E2004-APP, RWB-P3-E2042-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP); 8 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-598 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2008-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-596 | GET /api/recovery/source-data/v1/admin/data-quality/exceptions is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-597 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-598 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-599 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-600 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-601 | Test cases not in Test Cases v8: TC-E2-008-10-ITG | X9 | Missing | QA |
| CG-ALL-604 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-602 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-603 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-605 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-606 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-607 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC3 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC4 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
