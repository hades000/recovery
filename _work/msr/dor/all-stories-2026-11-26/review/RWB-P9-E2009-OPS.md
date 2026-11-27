# Build-readiness review (script) — RWB-P9-E2009-OPS Steering dashboard v1 data set — deployment

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P9-E2009-OPS (RWB P9 E2009 OPS Steering dashboard v1 data set - deployment v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-reporting |
| Legacy key | RWB-E2-009 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 12 (1 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | 6 row(s) of §11 have no BR Field ID; §11 has 6 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-7862, CG-ALL-7871 |
| 8 | Contract | Fail | detcheck: P1 Workflow reportingMeasuresDaily` (JOB-15) is not in Temporal Catalog v1 | CG-ALL-7863 |
| 9 | Messages | Partial | MSG-P9-002 has no English text in §14; MSG-P1-001 has no English text in §14; None (run alert) has no English text in §14; MSG-GEN-006 has no English text in §14; MSG-P7-003 has no English text in §14; MSG-P4-002 has no English text in §14; §14 lists 5 messages; detcheck: P2 MSG-P9-002 is used with another meaning than the standard's; P2 MSG-P1-001 is used with another meaning than the standard's; P2 MSG-GEN-006 is used with another meaning than the standard's; P2 MSG-P7-003 is used with another meaning than the standard's (+1 more) | CG-ALL-7864, CG-ALL-7865, CG-ALL-7866, CG-ALL-7867, CG-ALL-7868 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-37 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-7872, CG-ALL-7873 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P9-E2009-OPS-01, TC-P9-E2009-OPS-02, TC-P9-E2009-OPS-03, TC-P9-E2009-OPS-04, TC-P9-E2009-OPS-05, TC-P9-E2009-OPS-06, TC-P9-E2009-OPS-07; P3 §18 test lists differ from RTM v7 | CG-ALL-7869, CG-ALL-7870 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P9-E2009-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7863 | Workflow reportingMeasuresDaily` (JOB-15) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7862 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7864 | MSG-P9-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7865 | MSG-P1-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7866 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7867 | MSG-P7-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7868 | MSG-P4-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7869 | Test cases not in Test Cases v8: TC-P9-E2009-OPS-01, TC-P9-E2009-OPS-02, TC-P9-E2009-OPS-03, TC-P9-E2009-OPS-04, TC-P9-E2009-OPS-05, TC-P9-E2009-OPS-06, TC-P9-E2009-OPS-07 | X9 | Missing | QA |
| CG-ALL-7870 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7871 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7872 | SCR-37 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7873 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
