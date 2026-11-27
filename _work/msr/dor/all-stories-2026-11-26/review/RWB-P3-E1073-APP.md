# Build-readiness review (script) — RWB-P3-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1073-APP (RWB P3 E1073 APP Rule authoring, validation, test scenarios, approval and rollback in Drools v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-073 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 16 (3 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X13 is covered by 'BR10, TC-E1-073-01', not by a criterion; exception X14 is covered by 'TC-E1-073-16', not by a criterion; exception X15 is covered by 'BR11', not by a criterion; §7 holds 15 owned criteria in Gherkin; §5 has 15 exception paths | — |
| 4 | Business rules | Partial | 2 of 14 rules are covered by no criterion and no test case: BR2, BR14; §8 has 14 rules; detcheck: P2 Rule R-ALLOC-014 is not in Business Rules v4; P2 Rule ID ALLOC-032 used in the criteria exists in no current source; P2 Rule ID ALLOC-040 used in the criteria exists in no current source; P2 Rule ID ALLOC-041 used in the criteria exists in no current source | CG-ALL-3912, CG-ALL-3913, CG-ALL-3914, CG-ALL-3915 |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 21 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-3922 |
| 8 | Contract | Partial | detcheck: P2 Two workflow ID forms for CaseWorkflow in the sources | CG-ALL-3911 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-3916 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story | CG-ALL-3923 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3918 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 20 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-3917 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 build dependencies are not done yet (RWB-P3-E1073-INF); 12 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-3910 |
| 18 | Open decisions | Partial | open decision DL24 (assumptions: none); detcheck: P2 Open decision DL24 has no assumption | CG-ALL-3925 |
| 19 | Test data | Pass | every test case in §16 names its data (20) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P3-E1073-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.2 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3910 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-3919 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3920 | Java package th.co.scb.ace.workbench.recovery.case.rules uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3911 | Two workflow ID forms for CaseWorkflow in the sources | X6 | Ambiguous | Solution architect |
| CG-ALL-3912 | Rule R-ALLOC-014 is not in Business Rules v4 | X7 | Missing | Business analyst |
| CG-ALL-3913 | Rule ID ALLOC-032 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-3914 | Rule ID ALLOC-040 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-3915 | Rule ID ALLOC-041 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-3916 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3918 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3925 | Open decision DL24 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3917 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3921 | Flyway file V1073_1__rule_version_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3922 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3923 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3924 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X13: No version of a package is in force on the business date (covered by 'BR10, TC-E1-073-01' only) | Not specified in the source documents | |
| AC17 | §5 X14: A role without Rules and parameters calls an authoring operation (covered by 'TC-E1-073-16' only) | Not specified in the source documents | |
| AC18 | §5 X15: rwb-decision does not answer inside the 2 s budget (covered by 'BR11' only) | Not specified in the source documents | |
| AC19 | §8 BR2, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC20 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
