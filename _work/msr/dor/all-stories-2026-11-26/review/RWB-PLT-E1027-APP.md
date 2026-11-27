# Build-readiness review (script) — RWB-PLT-E1027-APP Decision log writer v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1027-APP (RWB PLT E1027 APP Decision log writer v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-027 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 14 (1 P1). AC review rows: 0. Missing criteria: 0.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Partial | §18 has 13 traceability rows; detcheck: P2 FR-PLT-014 has 2 meanings in the PRD; P2 FR-PLT-015 has 2 meanings in the PRD | CG-ALL-1294, CG-ALL-1295 |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Pass | §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_log_repeats_total` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ce_specversion` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ce_id` is not a field or entity in LDM v9 or Data Classification v5 (+4 more) | CG-ALL-1282, CG-ALL-1283, CG-ALL-1284, CG-ALL-1285, CG-ALL-1286, CG-ALL-1287, CG-ALL-1288, CG-ALL-1289 |
| 8 | Contract | Fail | detcheck: P1 rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1 (shared topic) | CG-ALL-1290 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-1293 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-PLT-E1027-APP-01, TC-PLT-E1027-APP-02, TC-PLT-E1027-APP-03, TC-PLT-E1027-APP-04, TC-PLT-E1027-APP-05, TC-PLT-E1027-APP-06; P3 §18 test lists differ from RTM v7 | CG-ALL-1291, CG-ALL-1292 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 8 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E1027-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_decision | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1290 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1 (shared topic) | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1282 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1283 | Name `decision_log_repeats_total` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1284 | Name `ce_specversion` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1285 | Name `ce_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1286 | Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1287 | Name `ce_source` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1288 | Name `ce_subject` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1289 | Name `ce_time` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1291 | Test cases not in Test Cases v8: TC-PLT-E1027-APP-01, TC-PLT-E1027-APP-02, TC-PLT-E1027-APP-03, TC-PLT-E1027-APP-04, TC-PLT-E1027-APP-05, TC-PLT-E1027-APP-06 | X9 | Missing | QA |
| CG-ALL-1293 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-1294 | FR-PLT-014 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1295 | FR-PLT-015 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1292 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
