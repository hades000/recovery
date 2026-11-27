# Build-readiness review (script) — RWB-S9-E7015-CON End a partner contract and recall the work - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E7015-CON (RWB S9 E7015 CON End a partner contract and recall the work - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E7-015 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Pass (not applicable) 2, Partial 7, Fail 4. Detcheck rows: 14 (4 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 13 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | 9 row(s) of §11 have no BR Field ID; §11 has 9 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-12086 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/partner/v1/partners is not in rwb-partner.yaml; P1 GET /api/recovery/partner/v1/partner/instructions is not in rwb-partner.yaml; P1 Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of InstructionWorkflow are not stated (+5 more) | CG-ALL-12087, CG-ALL-12088, CG-ALL-12089, CG-ALL-12090, CG-ALL-12091, CG-ALL-12092, CG-ALL-12093, CG-ALL-12094, CG-ALL-12095 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-34 has no empty, loading, error, no access state in the story; P3 SCR-35 has no empty, loading, error, no access state in the story | CG-ALL-12097, CG-ALL-12098 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E7-015-01, TC-E7-015-02, TC-E7-015-03, TC-E7-015-04, TC-S9-E7015-CON-01, TC-S9-E7015-CON-02, TC-S9-E7015-CON-03, TC-S9-E7015-CON-04, TC-S9-E7015-CON-05, TC-S9-E7015-CON-06, TC-S9-E7015-CON-07 | CG-ALL-12096 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12087 | GET /api/recovery/partner/v1/partners is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-12088 | GET /api/recovery/partner/v1/partner/instructions is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-12089 | Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |
| CG-ALL-12091 | Workflow The `contractEnd` branch of `InstructionWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12086 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-12090 | Workflow ID form and start rule of InstructionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-12092 | Activity readOpenInstructions is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-12093 | Activity evaluateRecallRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-12094 | Activity recordAndApplyExit is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-12095 | Activity requestCaseReselection is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12096 | Test cases not in Test Cases v8: TC-E7-015-01, TC-E7-015-02, TC-E7-015-03, TC-E7-015-04, TC-S9-E7015-CON-01, TC-S9-E7015-CON-02, TC-S9-E7015-CON-03, TC-S9-E7015-CON-04, TC-S9-E7015-CON-05, TC-S9-E7015-CON-06, TC-S9-E7015-CON-07 | X9 | Missing | QA |
| CG-ALL-12097 | SCR-34 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-12098 | SCR-35 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-12099 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC9 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
