# Build-readiness review (script) — RWB-S3-E4020-APP File an insurance claim on a collateral event

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S3-E4020-APP (RWB S3 E4020 APP File an insurance claim on a collateral event v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-guarantee |
| Legacy key | RWB-E4-020 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 14 (2 P1). AC review rows: 0. Missing criteria: 14.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-020-03', not by a criterion; exception X3 is covered by 'TC-E4-020-01, TC-S3-E4020-APP-01', not by a criterion; exception X4 is covered by 'TC-S3-E4020-APP-01', not by a criterion; exception X5 is covered by 'TC-S3-E4020-APP-02', not by a criterion; exception X6 is covered by 'TC-S3-E4020-APP-02', not by a criterion; exception X7 is covered by 'TC-S3-E4020-APP-01, s17', not by a criterion; exception X8 is covered by 'Sections 8, 11, 12 and 13', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-S3-008-1' has no BR ID; rule row 'BR-S3-008' has no BR ID; rule row 'R-DEV-06' has no BR ID; rule row 'R-LIT-79' has no BR ID; rule row 'R-DEV-09' has no BR ID; 10 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8951, CG-ALL-8962 |
| 8 | Contract | Fail | detcheck: P1 rwb.decision.RulePackageInForce.v1 is on topic rwb.decision.events.v1 in the catalog, not The rwb-decision topic, with `.retry` and `.dlt`; its topic name is not published for this key (GAP-2736); P2 rwb-guarantee is not a consumer of rwb.decision.RulePackageInForce.v1 in Kafka Catalog v1; P1 Workflow GuaranteeClaimWorkflow task queue rwb-guarantee` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of GuaranteeClaimWorkflow are not stated (+4 more) | CG-ALL-8952, CG-ALL-8953, CG-ALL-8954, CG-ALL-8955, CG-ALL-8956, CG-ALL-8957, CG-ALL-8958, CG-ALL-8959 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-17 has no empty, loading, error, no access state in the story | CG-ALL-8963 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8961 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-020-01, TC-E4-020-02, TC-E4-020-03, TC-E4-020-04, TC-S3-E4020-APP-01, TC-S3-E4020-APP-02 | CG-ALL-8960 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S3-E4020-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8952 | rwb.decision.RulePackageInForce.v1 is on topic rwb.decision.events.v1 in the catalog, not The rwb-decision topic, with `.retry` and `.dlt`; its topic name is not published for this key (GAP-2736) | X6 | Conflict | Solution architect |
| CG-ALL-8954 | Workflow GuaranteeClaimWorkflow task queue rwb-guarantee` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8951 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8953 | rwb-guarantee is not a consumer of rwb.decision.RulePackageInForce.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-8955 | Workflow ID form and start rule of GuaranteeClaimWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8956 | Activity readCollateralFacts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8957 | Activity evaluateClaimRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8958 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8959 | Activity reportCollateralEvent is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8960 | Test cases not in Test Cases v8: TC-E4-020-01, TC-E4-020-02, TC-E4-020-03, TC-E4-020-04, TC-S3-E4020-APP-01, TC-S3-E4020-APP-02 | X9 | Missing | QA |
| CG-ALL-8961 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8962 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8963 | SCR-17 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8964 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The role does not hold right C or U of Treatment and offer, or the caller is out of scope (covered by 'TC-E4-020-03' only) | Not specified in the source documents | |
| AC4 | §5 X3: A required element of the claim, the collateral fact or the appraisal is absent or invalid (covered by 'TC-E4-020-01, TC-S3-E4020-APP-01' only) | Not specified in the source documents | |
| AC5 | §5 X4: The collateral of the case or its last appraisal is missing, stale or not readable through the owner's contract (covered by 'TC-S3-E4020-APP-01' only) | Not specified in the source documents | |
| AC6 | §5 X5: The claim's `version` is stale, or the same create arrives twice with one `Idempotency-Key` (covered by 'TC-S3-E4020-APP-02' only) | Not specified in the source documents | |
| AC7 | §5 X6: The case signal is not accepted by the parent, or the workflow is waiting and the record is behind (covered by 'TC-S3-E4020-APP-02' only) | Not specified in the source documents | |
| AC8 | §5 X7: A component, a statement or a test reaches `recovery_case`, `v_ace_collateral`, `v_ace_valuation`, another service's sch (covered by 'TC-S3-E4020-APP-01, s17' only) | Not specified in the source documents | |
| AC9 | §5 X8: No rule row, deadline source, claimed-amount source or insurer interface is stated for this claim type (covered by 'Sections 8, 11, 12 and 13' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC13 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC14 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC15 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC16 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
