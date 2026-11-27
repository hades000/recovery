# Build-readiness review (script) — RWB-P7-E1001-APP Recovery tables for the 14 data products

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E1001-APP (RWB P7 E1001 APP Recovery tables for the 14 data products v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E1-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 15 (3 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'centre of excellence analyst (RW-COE) who authors rule packages, a risk and model risk officer (RW-RISK) who approves them, a data product owner (RW-DATASTEW) of DP12 and DP14, and the `rwb-decision` service that keeps the central ledger and the rule registry' is in the roles table | — |
| 2 | Links | Pass | §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 2 of 13 rules are covered by no criterion and no test case: BR3, BR9; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 6 data rows; detcheck: P2 Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `insufficient_privilege` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `v_data_dictionary` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-6807, CG-ALL-6808, CG-ALL-6809, CG-ALL-6817 |
| 8 | Contract | Fail | detcheck: P1 NONE None is not in rwb-decision.yaml; P1 rwb-decision.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data; P1 rwb-decision.yaml holds status as a closed enum while the story reads LOV-APPROVAL-STATUS as data | CG-ALL-6810, CG-ALL-6811, CG-ALL-6812 |
| 9 | Messages | Pass | §14 lists 1 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-10 has no empty, loading, error, no access state in the story; P3 SCR-11 has no empty, loading, error, no access state in the story; P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-6818, CG-ALL-6819, CG-ALL-6820 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6816 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-001-12; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-6813, CG-ALL-6814, CG-ALL-6815 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E1001-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6810 | NONE None is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-6811 | rwb-decision.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data | X5 | Conflict | Solution architect |
| CG-ALL-6812 | rwb-decision.yaml holds status as a closed enum while the story reads LOV-APPROVAL-STATUS as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6807 | Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6808 | Name `insufficient_privilege` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6809 | Name `v_data_dictionary` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6813 | Test cases not in Test Cases v8: TC-E1-001-12 | X9 | Missing | QA |
| CG-ALL-6816 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-6817 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6814 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6815 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6818 | SCR-10 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6819 | SCR-11 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6820 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6821 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR3, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
