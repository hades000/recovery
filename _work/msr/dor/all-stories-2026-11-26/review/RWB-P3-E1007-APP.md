# Build-readiness review (script) — RWB-P3-E1007-APP Integration adapters for outbound files

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1007-APP (RWB P3 E1007 APP Integration adapters for outbound files v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 16 (7 P1). AC review rows: 3. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'TC-E1-007-10', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 8 of 15 rules are covered by no criterion and no test case: BR1, BR3, BR8, BR10, BR11, BR12, BR14, BR15; §8 has 15 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 Status 'ANY_ACTIVE' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'Unchanged; one skip entry, no task' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'RETRY_QUEUE' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-3376, CG-ALL-3377, CG-ALL-3378, CG-ALL-3379, CG-ALL-3380 |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 17 data rows; detcheck: P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-3381, CG-ALL-3382, CG-ALL-3389 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P2-001 text differs from the Error and Message Standard v4 | CG-ALL-3383 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-3390 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC5 has no test case in §16; AC6 has no test case in §16; AC8 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC5, AC6, AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-3384, CG-ALL-3385, CG-ALL-3386 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL06 (assumptions: ASM-0189, ASM-2559, ASM-2608, ASM-2776) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E1007-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_integration | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3376 | Status 'ANY_ACTIVE' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3377 | Status 'ANY_ACTIVE' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3378 | Status 'Unchanged; one skip entry, no task' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3379 | Status 'RETRY_QUEUE' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3380 | Status 'RETRY_QUEUE' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-3387 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3388 | Java package th.co.scb.ace.workbench.recovery.case.fileoutcome uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3381 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3382 | Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3383 | MSG-P2-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3385 | Criteria with no test case: AC5, AC6, AC8 | X9 | Missing | QA |
| CG-ALL-3389 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3384 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-3386 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3390 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3391 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no test case in §16 |  |
| AC6 | no test case in §16 |  |
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X9: A holder of another role reads the task list of RW-PLATADM (covered by 'TC-E1-007-10' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR3, BR8, BR10, BR11, BR12, BR14, BR15 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
