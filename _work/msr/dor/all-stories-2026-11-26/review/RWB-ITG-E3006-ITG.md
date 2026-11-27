# Build-readiness review (script) — RWB-ITG-E3006-ITG Calculate the plan installment

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E3006-ITG (RWB ITG E3006 ITG Calculate the plan installment - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E3-006 |

## R1. Verdict

**NOT READY.** Checklist: Pass 14, Partial 4, Fail 7. Detcheck rows: 8 (2 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 1 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 1 of 7 rules are covered by no criterion and no test case: BR7; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has 1 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 6 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-812, CG-ALL-813 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-15 has no empty, loading, error, no access state in the story | CG-ALL-817, CG-ALL-818 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 5 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E3-006-01-ITG, TC-E3-006-02-ITG, TC-E3-006-03-ITG, TC-E3-006-04-ITG, TC-E3-006-05-ITG; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-814, CG-ALL-815, CG-ALL-816 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-S2-E3006-APP); 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E3006-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-812 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-813 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-814 | Test cases not in Test Cases v8: TC-E3-006-01-ITG, TC-E3-006-02-ITG, TC-E3-006-03-ITG, TC-E3-006-04-ITG, TC-E3-006-05-ITG | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-815 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-816 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-817 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-818 | SCR-15 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-819 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §8 BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC5 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC6 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC7 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
