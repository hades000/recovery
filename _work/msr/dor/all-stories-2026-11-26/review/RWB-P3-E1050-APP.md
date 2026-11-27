# Build-readiness review (script) — RWB-P3-E1050-APP Document classification

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1050-APP (RWB P3 E1050 APP Document classification v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-050 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 7, Fail 5. Detcheck rows: 25 (4 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 2 of 9 rules are covered by no criterion and no test case: BR6, BR8; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 13 data rows; detcheck: P2 Name `case_document_link` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `document_type_code` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `candidate_one_type` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `candidate_one_confidence` is not a field or entity in LDM v9 or Data Classification v5 (+6 more) | CG-ALL-3769, CG-ALL-3770, CG-ALL-3771, CG-ALL-3772, CG-ALL-3773, CG-ALL-3774, CG-ALL-3775, CG-ALL-3776, CG-ALL-3777, CG-ALL-3778 |
| 8 | Contract | Fail | detcheck: P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data; P2 Two workflow ID forms for CaseWorkflow in the sources; P2 Activity ApplyClassification is not in Temporal Catalog v1; P2 Activity RaiseReviewTask is not in Temporal Catalog v1 (+1 more) | CG-ALL-3779, CG-ALL-3780, CG-ALL-3781, CG-ALL-3782, CG-ALL-3783 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 5 messages; detcheck: P2 MSG-GEN-004 is used with another meaning than the standard's; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-3784, CG-ALL-3785 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, error, no access state in the story; P3 SCR-30 has no error, no access state in the story | CG-ALL-3791, CG-ALL-3792 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-3786, CG-ALL-3787 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E1050-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Pass | — | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3779 | rwb-case.yaml holds status as a closed enum while the story reads LOV-CASE-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-3783 | Workflow RedriveClassificationLinks is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3788 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3789 | Java package th.co.scb.ace.workbench.recovery.case.classification uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 15 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3769 | Name `case_document_link` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3770 | Name `document_type_code` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3771 | Name `candidate_one_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3772 | Name `candidate_one_confidence` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3773 | Name `candidate_two_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3774 | Name `candidate_two_confidence` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3775 | Name `classification_state` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3776 | Name `checklist_item_state` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3777 | Name `classified_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3778 | Name `source_event_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3780 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-3781 | Activity ApplyClassification is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3782 | Activity RaiseReviewTask is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3784 | MSG-GEN-004 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3785 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3786 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-3787 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3790 | Flyway file V1050_1__case_document_classification.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3791 | SCR-03 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3792 | SCR-30 has no error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3793 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §8 BR6, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
