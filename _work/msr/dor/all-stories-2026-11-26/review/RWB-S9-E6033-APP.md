# Build-readiness review (script) — RWB-S9-E6033-APP Receive a partner result into the case

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E6033-APP (RWB S9 E6033 APP Receive a partner result into the case v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E6-033 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 11 (3 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'BR6', not by a criterion; exception X6 is covered by 'BR7', not by a criterion; exception X7 is covered by 'Section 17', not by a criterion; §7 holds 5 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 3 of 10 rules are covered by no criterion and no test case: BR6, BR7, BR8; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | role SY-PARTNER in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 13 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-11861, CG-ALL-11869 |
| 8 | Contract | Fail | detcheck: P1 POST /partner/instructions/{instructionId}/results` (API-S9-005) is not in rwb-partner.yaml; P1 GET /partner/instructions` (API-S9-003) is not in rwb-partner.yaml; P1 Workflow InstructionWorkflow task queue rwb-partner`, namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of InstructionWorkflow are not stated (+1 more) | CG-ALL-11862, CG-ALL-11863, CG-ALL-11864, CG-ALL-11865, CG-ALL-11866 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-11867 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-34 has no empty, loading, error, no access state in the story; P3 SCR-35 has no empty, loading, error, no access state in the story | CG-ALL-11870, CG-ALL-11871 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-033-02, TC-E6-033-04, TC-S9-E6033-APP-01, TC-S9-E6033-APP-02, TC-S9-E6033-APP-03, TC-S9-E6033-APP-04 | CG-ALL-11868 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S9-E6033-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11862 | POST /partner/instructions/{instructionId}/results` (API-S9-005) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11863 | GET /partner/instructions` (API-S9-003) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11864 | Workflow InstructionWorkflow task queue rwb-partner`, namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11861 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11865 | Workflow ID form and start rule of InstructionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11866 | Activity recordPartnerResult` (name is this story's design choice) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11868 | Test cases not in Test Cases v8: TC-E6-033-02, TC-E6-033-04, TC-S9-E6033-APP-01, TC-S9-E6033-APP-02, TC-S9-E6033-APP-03, TC-S9-E6033-APP-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11867 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-11869 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11870 | SCR-34 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11871 | SCR-35 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §5 X5: A list or parameter read misses the 2 s budget, or its breaker is open (covered by 'BR6' only) | Not specified in the source documents | |
| AC8 | §5 X6: A data product is stale for the business date (covered by 'BR7' only) | Not specified in the source documents | |
| AC9 | §5 X7: A component or test reaches a case, rule, ledger or document table (covered by 'Section 17' only) | Not specified in the source documents | |
| AC10 | §8 BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
