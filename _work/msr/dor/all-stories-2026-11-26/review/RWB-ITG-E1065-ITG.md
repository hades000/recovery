# Build-readiness review (script) — RWB-ITG-E1065-ITG Sandbox database with synthetic recovery data — integration

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1065-ITG (RWB ITG E1065 ITG Sandbox database with synthetic recovery data - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-065 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 25 (3 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 2 of 13 rules are covered by no criterion and no test case: BR6, BR7; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 21 data rows; detcheck: P2 Name `iam_user` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `loan_account` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `account_payment` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `contact_point` is not a field or entity in LDM v9 or Data Classification v5 (+14 more) | CG-ALL-399, CG-ALL-400, CG-ALL-401, CG-ALL-402, CG-ALL-403, CG-ALL-404, CG-ALL-405, CG-ALL-406, CG-ALL-407, CG-ALL-408, CG-ALL-409, CG-ALL-410 (+6) |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | CG-ALL-417, CG-ALL-418 |
| 9 | Messages | Pass | §14 lists 2 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 16 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1065-01, TC-ITG-E1065-02, TC-ITG-E1065-03, TC-ITG-E1065-04, TC-ITG-E1065-05, TC-ITG-E1065-06; P3 §18 test lists differ from RTM v7 | CG-ALL-420, CG-ALL-421 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 5 build dependencies are not done yet (RWB-P1-E1065-APP, RWB-P3-E1065-APP, RWB-P4-E1065-APP, RWB-P5-E1065-APP, RWB-S8-E1065-APP); 5 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-419 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL15 (assumptions: ASM-5264); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL39 (assumptions: ASM-1617, ASM-2705); open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Partial | detcheck: P2 List LOV-RISK-TIER is not in Reference Data v5 | CG-ALL-416 |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1065-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_access, rwb_decision, rwb_sandbox, rwb_sandbox_next, rwb_sandbox_read, rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-417 | GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-418 | GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-419 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 20 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-399 | Name `iam_user` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-400 | Name `loan_account` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-401 | Name `account_payment` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-402 | Name `contact_point` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-403 | Name `account_collateral` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-404 | Name `collections_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-405 | Name `load_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-406 | Name `dq_exception` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-407 | Name `dq_rule` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-408 | Name `source_field_map` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-409 | Name `source_code_map` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-410 | Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-411 | Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-412 | Name `tracker_inventory` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-413 | Name `tracker_row` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-414 | Name `risk_tier` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-415 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-416 | List LOV-RISK-TIER is not in Reference Data v5 | X4 | Missing | Business analyst |
| CG-ALL-420 | Test cases not in Test Cases v8: TC-ITG-E1065-01, TC-ITG-E1065-02, TC-ITG-E1065-03, TC-ITG-E1065-04, TC-ITG-E1065-05, TC-ITG-E1065-06 | X9 | Missing | QA |
| CG-ALL-422 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-421 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-423 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR6, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
