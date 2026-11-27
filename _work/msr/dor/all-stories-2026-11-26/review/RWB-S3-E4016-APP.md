# Build-readiness review (script) — RWB-S3-E4016-APP Record the subrogation position

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S3-E4016-APP (RWB S3 E4016 APP Record the subrogation position v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-guarantee |
| Legacy key | RWB-E4-016 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 15 (4 P1). AC review rows: 1. Missing criteria: 11.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'guarantee officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-016-05', not by a criterion; exception X3 is covered by 'TC-E4-016-01', not by a criterion; exception X5 is covered by 'TC-S3-E4016-APP-02', not by a criterion; exception X6 is covered by 'TC-S3-E4016-APP-02', not by a criterion; exception X7 is covered by 'TC-S3-E4016-APP-02', not by a criterion; exception X8 is covered by 's17, BR7, BR9, TC-S3-E4016-APP-01', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-S3-004-1' has no BR ID; rule row 'BR-S3-004' has no BR ID; rule row 'R-GUA-22' has no BR ID; rule row 'R-GUA-23' has no BR ID; rule row 'R-GUA-24' has no BR ID; 10 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 15 rules | — |
| 5 | State transitions | Fail | §9 has 11 transitions; detcheck: P1 The story adds CLAIM_PAID to the closed list LOV-CLAIM-STATUS | CG-ALL-8874 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 7 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8875, CG-ALL-8886 |
| 8 | Contract | Fail | detcheck: P1 rwb-guarantee.yaml holds status as a closed enum while the story reads LOV-CLAIM-STATUS as data; P1 rwb-guarantee.yaml holds claimType as a closed enum while the story reads LOV-CLAIM-TYPE as data; P1 Workflow GuaranteeClaimWorkflow task queue rwb-guarantee` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of GuaranteeClaimWorkflow are not stated (+3 more) | CG-ALL-8876, CG-ALL-8877, CG-ALL-8878, CG-ALL-8879, CG-ALL-8880, CG-ALL-8881, CG-ALL-8882 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-8883 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-17 has no empty, loading, error, no access state in the story | CG-ALL-8887 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8885 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-016-01, TC-E4-016-02, TC-E4-016-03, TC-E4-016-04, TC-E4-016-05, TC-E4-016-06, TC-S3-E4016-APP-01, TC-S3-E4016-APP-02 | CG-ALL-8884 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S3-E4016-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8874 | The story adds CLAIM_PAID to the closed list LOV-CLAIM-STATUS | X1 | Conflict | Product owner |
| CG-ALL-8876 | rwb-guarantee.yaml holds status as a closed enum while the story reads LOV-CLAIM-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-8877 | rwb-guarantee.yaml holds claimType as a closed enum while the story reads LOV-CLAIM-TYPE as data | X5 | Conflict | Solution architect |
| CG-ALL-8878 | Workflow GuaranteeClaimWorkflow task queue rwb-guarantee` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8875 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8879 | Workflow ID form and start rule of GuaranteeClaimWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8880 | Activity matchFullPayment is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8881 | Activity evaluateSubrogationRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8882 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8884 | Test cases not in Test Cases v8: TC-E4-016-01, TC-E4-016-02, TC-E4-016-03, TC-E4-016-04, TC-E4-016-05, TC-E4-016-06, TC-S3-E4016-APP-01, TC-S3-E4016-APP-02 | X9 | Missing | QA |
| CG-ALL-8885 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8883 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8886 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8887 | SCR-17 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8888 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X2: The role does not hold right U of Treatment and offer, or the caller is out of scope (covered by 'TC-E4-016-05' only) | Not specified in the source documents | |
| AC6 | §5 X3: A required element of the claim, the payment fact or the share is absent or invalid (covered by 'TC-E4-016-01' only) | Not specified in the source documents | |
| AC7 | §5 X5: The claim's `version` is stale, or the same posted-payment fact arrives again (covered by 'TC-S3-E4016-APP-02' only) | Not specified in the source documents | |
| AC8 | §5 X6: rwb-payment publishes no fact inside the workflow's wait, or the inbox is behind (covered by 'TC-S3-E4016-APP-02' only) | Not specified in the source documents | |
| AC9 | §5 X7: The data product behind the claim is stale, or the rules row in force is missing (covered by 'TC-S3-E4016-APP-02' only) | Not specified in the source documents | |
| AC10 | §5 X8: A component, a statement or a test reaches `recovery_case`, `v_ace_payment`, another service's schema or a `v_ace_*` vie (covered by 's17, BR7, BR9, TC-S3-E4016-APP-01' only) | Not specified in the source documents | |
| AC11 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC13 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC14 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
