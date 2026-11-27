# Build-readiness review (script) — RWB-S2-E3003-APP Approve a settlement below the floor

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E3003-APP (RWB S2 E3003 APP Approve a settlement below the floor v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E3-003 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 17 (2 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'recovery developer (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 4 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 9 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 18 data rows; detcheck: P2 Name `price_below_floor` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `below_floor_refused` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `approver_role` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-8485, CG-ALL-8486, CG-ALL-8487, CG-ALL-8488, CG-ALL-8498 |
| 8 | Contract | Fail | detcheck: P1 rwb-treatment.yaml holds outcome as a closed enum while the story reads LOV-TRT-OUTCOME as data; P1 Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of TreatmentWorkflow are not stated; P2 Activity checkFloor is not in Temporal Catalog v1 (+3 more) | CG-ALL-8489, CG-ALL-8490, CG-ALL-8491, CG-ALL-8492, CG-ALL-8493, CG-ALL-8494, CG-ALL-8495 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-15 has no empty, loading, error, no access state in the story | CG-ALL-8499, CG-ALL-8500 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8497 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E3-003-01, TC-E3-003-02, TC-E3-003-03, TC-E3-003-04, TC-E3-003-05, TC-E3-003-06 | CG-ALL-8496 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S2-E3003-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8489 | rwb-treatment.yaml holds outcome as a closed enum while the story reads LOV-TRT-OUTCOME as data | X5 | Conflict | Solution architect |
| CG-ALL-8490 | Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8485 | Name `price_below_floor` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8486 | Name `below_floor_refused` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8487 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8488 | Name `approver_role` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8491 | Workflow ID form and start rule of TreatmentWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8492 | Activity checkFloor is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8493 | Activity requestSecondSignature is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8494 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8495 | Activity publishApproved is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8496 | Test cases not in Test Cases v8: TC-E3-003-01, TC-E3-003-02, TC-E3-003-03, TC-E3-003-04, TC-E3-003-05, TC-E3-003-06 | X9 | Missing | QA |
| CG-ALL-8497 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8498 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8499 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8500 | SCR-15 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8501 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC6 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
