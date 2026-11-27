# Build-readiness review (script) — RWB-P2-E1007-CON Integration adapters for outbound files

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E1007-CON (RWB P2 E1007 CON Integration adapters for outbound files - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E1-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Pass (not applicable) 2, Partial 6, Fail 4. Detcheck rows: 21 (7 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 13 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | 10 row(s) of §11 have no BR Field ID; §11 has 10 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2966, CG-ALL-2967, CG-ALL-2968 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data; P1 POST /api/recovery/document/v1/documents is not published by rwb-document (+8 more) | CG-ALL-2969, CG-ALL-2970, CG-ALL-2971, CG-ALL-2972, CG-ALL-2973, CG-ALL-2974, CG-ALL-2975, CG-ALL-2976, CG-ALL-2977, CG-ALL-2978, CG-ALL-2979, CG-ALL-2980 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P2-001 text differs from the Error and Message Standard v4; P3 MSG-P4-003 text differs from the Error and Message Standard v4 | CG-ALL-2981, CG-ALL-2982, CG-ALL-2983 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-2986 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P2-E1007-CON-01, TC-P2-E1007-CON-02, TC-P2-E1007-CON-03, TC-P2-E1007-CON-04, TC-P2-E1007-CON-05, TC-P2-E1007-CON-06; P3 §18 test lists differ from RTM v7 | CG-ALL-2984, CG-ALL-2985 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2969 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-2970 | GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-2971 | GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-2972 | POST /api/recovery/document/v1/documents is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-2973 | POST /api/recovery/case/v1/cases/{caseId}/actions is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2974 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2976 | Workflow OutboundFileWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2966 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2967 | Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2968 | Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2975 | Activity deliverFile(manifest) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2977 | Activity buildOutboundFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2978 | Activity storeOutboundFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2979 | Activity sendFileOverMft is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2980 | Activity parkItemInException is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2982 | MSG-P2-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2981 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2983 | MSG-P4-003 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2984 | Test cases not in Test Cases v8: TC-P2-E1007-CON-01, TC-P2-E1007-CON-02, TC-P2-E1007-CON-03, TC-P2-E1007-CON-04, TC-P2-E1007-CON-05, TC-P2-E1007-CON-06 | X9 | Missing | QA |
| CG-ALL-2985 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2986 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
