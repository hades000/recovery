# Build-readiness review (script) — RWB-S2-E3006-APP Calculate the plan installment

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E3006-APP (RWB S2 E3006 APP Calculate the plan installment v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E3-006 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 9, Fail 5. Detcheck rows: 12 (0 P1). AC review rows: 2. Missing criteria: 9.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X4 is covered by 'Section 12.8', not by a criterion; exception X5 is covered by 'Section 14', not by a criterion; exception X6 is covered by 'Section 10', not by a criterion; exception X7 is covered by 'Section 4', not by a criterion; exception X8 is covered by 'Section 12.5', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 16 data rows; detcheck: P2 Name `settlement_range_low` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `settlement_range_high` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `payoff_as_at` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-8547, CG-ALL-8548, CG-ALL-8549, CG-ALL-8550, CG-ALL-8555 |
| 8 | Contract | Partial | detcheck: P2 Activity calculatePlanInstallment is not in Temporal Catalog v1 | CG-ALL-8551 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-8552 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-15 has no empty, loading, error, no access state in the story | CG-ALL-8556, CG-ALL-8557 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8554 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E3-006-01, TC-E3-006-03, TC-E3-006-04, TC-E3-006-05 | CG-ALL-8553 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 5 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S2-E3006-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8547 | Name `settlement_range_low` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8548 | Name `settlement_range_high` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8549 | Name `payoff_as_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8550 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8551 | Activity calculatePlanInstallment is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8553 | Test cases not in Test Cases v8: TC-E3-006-01, TC-E3-006-03, TC-E3-006-04, TC-E3-006-05 | X9 | Missing | QA |
| CG-ALL-8554 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-8555 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8552 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8556 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8557 | SCR-15 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8558 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |
| AC3 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X4: The record is refused for a missing or invalid field (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC5 | §5 X5: A required value is missing on the treatment, for example the installment count (covered by 'Section 14' only) | Not specified in the source documents | |
| AC6 | §5 X6: A role without the right tries to re-run the step or read its result (covered by 'Section 10' only) | Not specified in the source documents | |
| AC7 | §5 X7: The payoff on the case is older than the freshness limit (covered by 'Section 4' only) | Not specified in the source documents | |
| AC8 | §5 X8: A second case signal arrives while the branch is running (covered by 'Section 12.5' only) | Not specified in the source documents | |
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
