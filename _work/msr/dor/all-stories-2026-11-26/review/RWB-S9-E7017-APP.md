# Build-readiness review (script) — RWB-S9-E7017-APP Manage extra costs and services on an asset

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E7017-APP (RWB S9 E7017 APP Manage extra costs and services on an asset v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E7-017 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 15 (3 P1). AC review rows: 0. Missing criteria: 13.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'partner and agency manager' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 19 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E7-017-03', not by a criterion; exception X3 is covered by 'TC-S9-E7017-APP-02', not by a criterion; exception X4 is covered by 'BR8', not by a criterion; exception X5 is covered by 'TC-S9-E7017-APP-02', not by a criterion; exception X6 is covered by '§9, BR5', not by a criterion; exception X7 is covered by 'TC-S9-E7017-APP-01', not by a criterion; exception X8 is covered by 'TC-S9-E7017-APP-01', not by a criterion; exception X9 is covered by 'TC-S9-E7017-APP-03, BR6', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row '' has no BR ID; rule row '' has no BR ID; rule row '' has no BR ID; rule row '' has no BR ID; 9 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR7, BR8, BR9, BR10; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-12131, CG-ALL-12142 |
| 8 | Contract | Fail | detcheck: P1 POST /partner/instructions/{instructionId}/results` (API-S9-005) is not in rwb-partner.yaml; P1 POST /partner/instructions/{instructionId}/invoices` (API-S9-006) is not in rwb-partner.yaml; P1 Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of InstructionWorkflow are not stated (+3 more) | CG-ALL-12132, CG-ALL-12133, CG-ALL-12134, CG-ALL-12135, CG-ALL-12136, CG-ALL-12137, CG-ALL-12138 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-34 has no empty, error, no access state in the story; P3 SCR-35 has no empty, error, no access state in the story | CG-ALL-12143, CG-ALL-12144 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-12141 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E7-017-01, TC-E7-017-02, TC-E7-017-03, TC-E7-017-04, TC-S9-E7017-APP-01, TC-S9-E7017-APP-02, TC-S9-E7017-APP-03; P3 Test cases listed for criteria this story does not own | CG-ALL-12139, CG-ALL-12140 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S9-E7017-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12132 | POST /partner/instructions/{instructionId}/results` (API-S9-005) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-12133 | POST /partner/instructions/{instructionId}/invoices` (API-S9-006) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-12134 | Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12131 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-12135 | Workflow ID form and start rule of InstructionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-12136 | Activity recordCostClaim is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-12137 | Activity writeCostDecisionRecord is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-12138 | Activity approveCostInvoice is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-12139 | Test cases not in Test Cases v8: TC-E7-017-01, TC-E7-017-02, TC-E7-017-03, TC-E7-017-04, TC-S9-E7017-APP-01, TC-S9-E7017-APP-02, TC-S9-E7017-APP-03 | X9 | Missing | QA |
| CG-ALL-12141 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-12140 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-12142 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-12143 | SCR-34 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-12144 | SCR-35 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-12145 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The caller lacks the partner-portal right of the operation (covered by 'TC-E7-017-03' only) | Not specified in the source documents | |
| AC4 | §5 X3: The same claim is submitted twice, or the instruction already carries it (covered by 'TC-S9-E7017-APP-02' only) | Not specified in the source documents | |
| AC5 | §5 X4: The instruction belongs to a partner of another firm (covered by 'BR8' only) | Not specified in the source documents | |
| AC6 | §5 X5: A result file is outside the allowed set (covered by 'TC-S9-E7017-APP-02' only) | Not specified in the source documents | |
| AC7 | §5 X6: The claim reaches an instruction already `DONE` or `RECALLED` (covered by '§9, BR5' only) | Not specified in the source documents | |
| AC8 | §5 X7: The claim is refused (covered by 'TC-S9-E7017-APP-01' only) | Not specified in the source documents | |
| AC9 | §5 X8: An approval arrives for an instruction with no recorded claim (covered by 'TC-S9-E7017-APP-01' only) | Not specified in the source documents | |
| AC10 | §5 X9: A statement reaches a `v_ace_*` view, an `rwb_asset` row or another schema (covered by 'TC-S9-E7017-APP-03, BR6' only) | Not specified in the source documents | |
| AC11 | §8 BR1, BR2, BR3, BR4, BR5, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC14 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
