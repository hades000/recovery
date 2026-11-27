# Build-readiness review (script) — RWB-S2-E3004-APP Offer a TDR plan

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E3004-APP (RWB S2 E3004 APP Offer a TDR plan v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E3-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 13 (2 P1). AC review rows: 0. Missing criteria: 13.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'restructuring officer (FCR)' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'TC-E3-004-05', not by a criterion; exception X2 is covered by 'TC-E3-004-01, TC-S2-E3004-CON-04', not by a criterion; exception X3 is covered by 'TC-S2-E3004-CON-03', not by a criterion; exception X5 is covered by 'TC-S2-E3004-CON-04', not by a criterion; exception X6 is covered by 'Section 8, BR4', not by a criterion; exception X7 is covered by 'TC-E3-004-01', not by a criterion; exception X8 is covered by 'TC-E3-004-01', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 9 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 22 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `counter_amount` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8516, CG-ALL-8517, CG-ALL-8525 |
| 8 | Contract | Fail | detcheck: P1 POST /treatments/{treatmentId}/offer` (the plan form) is not in rwb-treatment.yaml; P1 Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog; P2 Activity buildPlanOffer is not in Temporal Catalog v1; P2 Activity applyBand is not in Temporal Catalog v1 (+1 more) | CG-ALL-8518, CG-ALL-8519, CG-ALL-8520, CG-ALL-8521, CG-ALL-8522 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-15 has no empty, loading, error, no access state in the story | CG-ALL-8526, CG-ALL-8527 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8524 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E3-004-01, TC-E3-004-02, TC-E3-004-03, TC-E3-004-04, TC-E3-004-05, TC-E3-004-06 | CG-ALL-8523 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S2-E3004-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8518 | POST /treatments/{treatmentId}/offer` (the plan form) is not in rwb-treatment.yaml | X5 | Missing | Solution architect |
| CG-ALL-8519 | Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8516 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8517 | Name `counter_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8520 | Activity buildPlanOffer is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8521 | Activity applyBand is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8522 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8523 | Test cases not in Test Cases v8: TC-E3-004-01, TC-E3-004-02, TC-E3-004-03, TC-E3-004-04, TC-E3-004-05, TC-E3-004-06 | X9 | Missing | QA |
| CG-ALL-8524 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8525 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8526 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8527 | SCR-15 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8528 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X1: A role without the right in capability area Treatment and offer calls the offer (covered by 'TC-E3-004-05' only) | Not specified in the source documents | |
| AC6 | §5 X2: A required plan property is missing or out of its domain (covered by 'TC-E3-004-01, TC-S2-E3004-CON-04' only) | Not specified in the source documents | |
| AC7 | §5 X3: The body names a band column or a band as a stored value (covered by 'TC-S2-E3004-CON-03' only) | Not specified in the source documents | |
| AC8 | §5 X5: A record field is refused by the library (covered by 'TC-S2-E3004-CON-04' only) | Not specified in the source documents | |
| AC9 | §5 X6: The affordability result is absent, superseded or carries no band (covered by 'Section 8, BR4' only) | Not specified in the source documents | |
| AC10 | §5 X7: The offer clock reaches the validity date (covered by 'TC-E3-004-01' only) | Not specified in the source documents | |
| AC11 | §5 X8: The same submit arrives twice with one `Idempotency-Key` (covered by 'TC-E3-004-01' only) | Not specified in the source documents | |
| AC12 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC15 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC16 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC17 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
