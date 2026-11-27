# Build-readiness review (script) — RWB-P2-E2035-APP Next action on the case

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E2035-APP (RWB P2 E2035 APP Next action on the case v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E2-035 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 23 (9 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 14 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 2 of 13 rules are covered by no criterion and no test case: BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 20 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-3252, CG-ALL-3269 |
| 8 | Contract | Fail | detcheck: P1 POST /next-actions:resolve is not in rwb-integration.yaml; P1 GET /cases/{caseId}/next-action is not in rwb-integration.yaml; P1 POST /cases/{caseId}/next-action is not in rwb-integration.yaml; P1 GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= is not published by rwb-decision (+8 more) | CG-ALL-3253, CG-ALL-3254, CG-ALL-3255, CG-ALL-3256, CG-ALL-3257, CG-ALL-3258, CG-ALL-3259, CG-ALL-3260, CG-ALL-3261, CG-ALL-3262, CG-ALL-3263, CG-ALL-3264 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-001; §14 lists 7 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-3265, CG-ALL-3266 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-3270, CG-ALL-3271, CG-ALL-3272 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-035-14; P3 §18 test lists differ from RTM v7 | CG-ALL-3267, CG-ALL-3268 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P2-E2033-APP, RWB-P2-E2035-OPS); 16 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL24 (assumptions: none); detcheck: P2 Open decision DL24 has no assumption | CG-ALL-3274 |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P2-E2035-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P2-E2033-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3253 | POST /next-actions:resolve is not in rwb-integration.yaml | X5 | Missing | Solution architect |
| CG-ALL-3254 | GET /cases/{caseId}/next-action is not in rwb-integration.yaml | X5 | Missing | Solution architect |
| CG-ALL-3255 | POST /cases/{caseId}/next-action is not in rwb-integration.yaml | X5 | Missing | Solution architect |
| CG-ALL-3256 | GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= is not published by rwb-decision | X5 | Missing | Solution architect |
| CG-ALL-3257 | GET /api/recovery/case/v1/reference-data/role-classes/{roleCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-3258 | GET /api/recovery/case/v1/reference-data/service-levels/{toState} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-3259 | GET /api/recovery/case/v1/parameters/rwb.calendar.bank-holidays is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-3260 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3261 | Workflow NextActionCheckWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3252 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3262 | Activity findCasesWithoutNextAction is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3263 | Activity resolveNextAction is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3264 | Activity fillNextAction is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3265 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3266 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3267 | Test cases not in Test Cases v8: TC-E2-035-14 | X9 | Missing | QA |
| CG-ALL-3274 | Open decision DL24 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3268 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3269 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3270 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3271 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3272 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3273 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §8 BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC17 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
