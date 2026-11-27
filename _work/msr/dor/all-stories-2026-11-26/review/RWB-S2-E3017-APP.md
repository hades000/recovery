# Build-readiness review (script) — RWB-S2-E3017-APP Release the collateral after settlement

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E3017-APP (RWB S2 E3017 APP Release the collateral after settlement v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E3-017 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 17 (4 P1). AC review rows: 1. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner' is in the roles table | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'TC-E3-017-05', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `installments_due` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8776, CG-ALL-8777, CG-ALL-8789, CG-ALL-8790 |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.treatment.CollateralReleaseRequested.v1 is not in Kafka Catalog v1; P1 Event type rwb.treatment.CollateralReleased.v1 is not in Kafka Catalog v1; P1 Event type rwb.payment.PaymentCleared.v1 is not in Kafka Catalog v1; P1 Workflow TreatmentWorkflow` (collateral-release branch) is not in Temporal Catalog v1 (+4 more) | CG-ALL-8778, CG-ALL-8779, CG-ALL-8780, CG-ALL-8781, CG-ALL-8782, CG-ALL-8783, CG-ALL-8784, CG-ALL-8785 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-15 has no empty, loading, error, no access state in the story | CG-ALL-8791, CG-ALL-8792 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8788 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E3-017-01, TC-E3-017-02, TC-E3-017-03, TC-E3-017-04, TC-E3-017-05, TC-E3-017-06; P3 Test cases listed for criteria this story does not own | CG-ALL-8786, CG-ALL-8787 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S2-E3017-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8778 | Event type rwb.treatment.CollateralReleaseRequested.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8779 | Event type rwb.treatment.CollateralReleased.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8780 | Event type rwb.payment.PaymentCleared.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8781 | Workflow TreatmentWorkflow` (collateral-release branch) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8776 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8777 | Name `installments_due` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8782 | Activity readClearance is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8783 | Activity requestRelease is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8784 | Activity confirmRelease is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8785 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8786 | Test cases not in Test Cases v8: TC-E3-017-01, TC-E3-017-02, TC-E3-017-03, TC-E3-017-04, TC-E3-017-05, TC-E3-017-06 | X9 | Missing | QA |
| CG-ALL-8788 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-8789 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8787 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-8790 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8791 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8792 | SCR-15 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X1: The role does not hold right R on "Treatment and offer" (covered by 'TC-E3-017-05' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC8 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
