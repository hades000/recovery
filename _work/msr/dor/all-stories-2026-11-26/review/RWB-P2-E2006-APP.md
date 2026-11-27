# Build-readiness review (script) — RWB-P2-E2006-APP Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E2006-APP (RWB P2 E2006 APP Credit approval pack for NLEADS v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E2-006 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 15 (7 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 3 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'TC-E2-006-12', not by a criterion; §7 holds 11 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 5 of 13 rules are covered by no criterion and no test case: BR4, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-ACC-009, DF-ACC-010, DF-TRT-023, DF-TRT-024, DF-TRT-025, DF-TRT-026; §11 has 30 data rows; detcheck: P2 Name `credit_result_at` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-3092, CG-ALL-3093 |
| 8 | Contract | Fail | detcheck: P1 POST /treatments/{treatmentId}/credit-result is not in rwb-integration.yaml; P1 POST /api/recovery/case/v1/cases/{caseId}/actions is not published by rwb-case; P1 GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/collateral/{id} is not published by rwb-source-data (+3 more) | CG-ALL-3094, CG-ALL-3095, CG-ALL-3096, CG-ALL-3097, CG-ALL-3098, CG-ALL-3099, CG-ALL-3100 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001, MSG-P4-003; §14 lists 11 messages; detcheck: P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-3101 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story | CG-ALL-3105 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3103 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-3102 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P2-E1007-APP); 7 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL18 (assumptions: ASM-2569, ASM-2839, ASM-2859, ASM-2883); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P2-E1007-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3094 | POST /treatments/{treatmentId}/credit-result is not in rwb-integration.yaml | X5 | Missing | Solution architect |
| CG-ALL-3095 | POST /api/recovery/case/v1/cases/{caseId}/actions is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-3096 | GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3097 | GET /api/recovery/source-data/v1/collateral/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3098 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3099 | GET /api/recovery/access/v1/doa-limits is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3100 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3092 | Name `credit_result_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3093 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3101 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3103 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3102 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3104 | Flyway file V2006_1__credit_result_record.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3105 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3106 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X10: A role without the Treatment and offer right opens the pack or records a result (covered by 'TC-E2-006-12' only) | Not specified in the source documents | |
| AC13 | §8 BR4, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
