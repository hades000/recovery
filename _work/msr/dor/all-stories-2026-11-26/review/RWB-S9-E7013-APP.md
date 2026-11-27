# Build-readiness review (script) — RWB-S9-E7013-APP Hold a partner review

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E7013-APP (RWB S9 E7013 APP Hold a partner review v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E7-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 18 (7 P1). AC review rows: 0. Missing criteria: 11.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'partner and agency manager (RW-AGENCYMG)** — and as a role that holds the Partner portal write right where the matrix gives another role only the read —' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E7-013-03', not by a criterion; exception X4 is covered by 'Section 12.2', not by a criterion; exception X5 is covered by 'GAP-3125', not by a criterion; exception X6 is covered by 'ASM-5443', not by a criterion; exception X7 is covered by 'R-UNI-40', not by a criterion; exception X8 is covered by 'Section 19', not by a criterion; exception X9 is covered by 'Section 17, BR6, BR7', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-UNI-25' has no BR ID; rule row 'R-UNI-26' has no BR ID; rule row 'R-UNI-27' has no BR ID; rule row 'R-UNI-28' has no BR ID; rule row 'R-UNI-29' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; rule row 'R-UNI-45' has no BR ID; 9 of 17 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 17 rules | — |
| 5 | State transitions | Pass | §9 has 13 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `recovery_log` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-12010, CG-ALL-12011, CG-ALL-12023 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 rwb-partner.yaml holds status as a closed enum while the story reads LOV-INSTR-STATUS as data; P1 rwb-partner.yaml holds instructionType as a closed enum while the story reads LOV-INSTRUCTION as data (+5 more) | CG-ALL-12012, CG-ALL-12013, CG-ALL-12014, CG-ALL-12015, CG-ALL-12016, CG-ALL-12017, CG-ALL-12018, CG-ALL-12019, CG-ALL-12020 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-34 has no empty, loading, error, no access state in the story; P3 SCR-35 has no empty, loading, error, no access state in the story; P3 SCR-36 has no empty, loading, error, no access state in the story | CG-ALL-12024, CG-ALL-12025, CG-ALL-12026 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-013-01, TC-E7-013-02, TC-E7-013-03, TC-E7-013-04; P3 Test cases listed for criteria this story does not own | CG-ALL-12021, CG-ALL-12022 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S9-E7013-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12012 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-12013 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-12014 | rwb-partner.yaml holds status as a closed enum while the story reads LOV-INSTR-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-12015 | rwb-partner.yaml holds instructionType as a closed enum while the story reads LOV-INSTRUCTION as data | X5 | Conflict | Solution architect |
| CG-ALL-12016 | rwb-partner.yaml holds panelStatus as a closed enum while the story reads LOV-PANEL as data | X5 | Conflict | Solution architect |
| CG-ALL-12017 | rwb-partner.yaml holds partnerType as a closed enum while the story reads LOV-PARTNER-TYPE as data | X5 | Conflict | Solution architect |
| CG-ALL-12018 | Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12010 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-12011 | Name `recovery_log` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-12019 | Workflow ID form and start rule of InstructionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-12020 | Activity readReviewFacts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-12021 | Test cases not in Test Cases v8: TC-E7-013-01, TC-E7-013-02, TC-E7-013-03, TC-E7-013-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12022 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-12023 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-12024 | SCR-34 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-12025 | SCR-35 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-12026 | SCR-36 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-12027 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The role does not hold the Partner portal right of the act (covered by 'TC-E7-013-03' only) | Not specified in the source documents | |
| AC4 | §5 X4: The reference-data read or the rule-package read does not answer inside 2 s, or its breaker is open (covered by 'Section 12.2' only) | Not specified in the source documents | |
| AC5 | §5 X5: No list is published for the statuses or the actions of a point (covered by 'GAP-3125' only) | Not specified in the source documents | |
| AC6 | §5 X6: `partner.score` is empty because the monthly scorecard has not run (covered by 'ASM-5443' only) | Not specified in the source documents | |
| AC7 | §5 X7: The same partner and review date are submitted twice (covered by 'R-UNI-40' only) | Not specified in the source documents | |
| AC8 | §5 X8: The action recorded against a point would change the panel status, send a notice or end the contract (covered by 'Section 19' only) | Not specified in the source documents | |
| AC9 | §5 X9: A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row, a `rwb_decision` row or another service's (covered by 'Section 17, BR6, BR7' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
