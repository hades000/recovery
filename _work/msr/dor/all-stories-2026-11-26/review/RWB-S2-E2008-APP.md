# Build-readiness review (script) — RWB-S2-E2008-APP Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E2008-APP (RWB S2 E2008 APP Payment matching with the missed payment event v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E2-008 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 21 (7 P1). AC review rows: 1. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'BR6', not by a criterion; exception X6 is covered by 'Section 17', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Partial | 3 of 8 rules are covered by no criterion and no test case: BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 16 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-8317, CG-ALL-8333 |
| 8 | Contract | Fail | detcheck: P1 GET /treatments/{treatmentId}` (API-S2-002) is not in rwb-treatment.yaml; P1 PATCH /treatments/{treatmentId}` (API-S2-003) is not in rwb-treatment.yaml; P1 rwb.payment.ProceedsMatched.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, owner P8; P2 rwb-treatment is not a consumer of rwb.payment.ProceedsMatched.v1 in Kafka Catalog v1 (+7 more) | CG-ALL-8318, CG-ALL-8319, CG-ALL-8321, CG-ALL-8322, CG-ALL-8323, CG-ALL-8324, CG-ALL-8325, CG-ALL-8326, CG-ALL-8327, CG-ALL-8328, CG-ALL-8329 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-28 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-8334, CG-ALL-8335, CG-ALL-8336 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8332 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-S2-E2008-APP-01, TC-S2-E2008-APP-02, TC-S2-E2008-APP-03, TC-S2-E2008-APP-04, TC-S2-E2008-APP-05; P3 §18 test lists differ from RTM v7 | CG-ALL-8330, CG-ALL-8331 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-8320 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S2-E2008-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8318 | GET /treatments/{treatmentId}` (API-S2-002) is not in rwb-treatment.yaml | X5 | Missing | Solution architect |
| CG-ALL-8319 | PATCH /treatments/{treatmentId}` (API-S2-003) is not in rwb-treatment.yaml | X5 | Missing | Solution architect |
| CG-ALL-8320 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-8321 | rwb.payment.ProceedsMatched.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, owner P8 | X6 | Conflict | Solution architect |
| CG-ALL-8323 | rwb.payment.PaymentMissed.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, owner P8 | X6 | Conflict | Solution architect |
| CG-ALL-8324 | rwb.decision.RulePackageInForce.v1 is on topic rwb.decision.events.v1 in the catalog, not rwb.decision.events.v1`, owner P7 | X6 | Conflict | Solution architect |
| CG-ALL-8325 | Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8317 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8322 | rwb-treatment is not a consumer of rwb.payment.ProceedsMatched.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-8326 | Workflow ID form and start rule of TreatmentWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8327 | Activity applyProceedsMatched` (name Not specified in the source documents (GAP-2693; ASM-4452)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8328 | Activity holdMissedInstallment` (name as above) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8329 | Activity RecordAndApply` (the design's activity) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8330 | Test cases not in Test Cases v8: TC-S2-E2008-APP-01, TC-S2-E2008-APP-02, TC-S2-E2008-APP-03, TC-S2-E2008-APP-04, TC-S2-E2008-APP-05 | X9 | Missing | QA |
| CG-ALL-8332 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-8333 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8331 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-8334 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8335 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8336 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8337 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X5: The parameters or the reference-data read does not answer inside the budget, or its breaker is open (covered by 'BR6' only) | Not specified in the source documents | |
| AC12 | §5 X6: A component, a statement or a test reaches a payment, proceeds, rule, case or timer table (covered by 'Section 17' only) | Not specified in the source documents | |
| AC13 | §8 BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC16 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
