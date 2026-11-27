# Build-readiness review (script) — RWB-S6-E6012-APP Apply the debt sale cap

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S6-E6012-APP (RWB S6 E6012 APP Apply the debt sale cap v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-debtsale |
| Legacy key | RWB-E6-012 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 15 (6 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'debt sale officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E6-012-03', not by a criterion; exception X8 is covered by 'Section 17', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DS-19' has no BR ID; rule row 'R-DS-23' has no BR ID; 9 of 11 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 12 transitions | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 13 data rows; detcheck: P2 Name `account_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `case_list` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-10820, CG-ALL-10821, CG-ALL-10832 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 No API Specification v5 yaml has the base of /api/recovery/access/v1 (+3 more) | CG-ALL-10822, CG-ALL-10823, CG-ALL-10824, CG-ALL-10825, CG-ALL-10826, CG-ALL-10827, CG-ALL-10828, CG-ALL-10829 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-10830 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-26 has no empty, loading, error, no access state in the story | CG-ALL-10833 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-012-01, TC-E6-012-02, TC-E6-012-03, TC-E6-012-04 | CG-ALL-10831 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 2 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10822 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10823 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10824 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-10825 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-10826 | No API Specification v5 yaml has the base of /api/recovery/access/v1 | X5 | Missing | Solution architect |
| CG-ALL-10827 | Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10820 | Name `account_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10821 | Name `case_list` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10828 | Workflow ID form and start rule of DebtSaleWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10829 | Activity applyDebtSaleCap is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10831 | Test cases not in Test Cases v8: TC-E6-012-01, TC-E6-012-02, TC-E6-012-03, TC-E6-012-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10830 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-10832 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10833 | SCR-26 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10834 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X2: The caller's identity does not hold the right in the capability area (covered by 'TC-E6-012-03' only) | Not specified in the source documents | |
| AC6 | §5 X8: A component, a statement or a test reaches another service's schema or a `v_ace_*` view (covered by 'Section 17' only) | Not specified in the source documents | |
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
