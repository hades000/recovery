# Build-readiness review (script) — RWB-P2-E4046-APP Post a settlement booking to ALS

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E4046-APP (RWB P2 E4046 APP Post a settlement booking to ALS v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E4-046 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 6, Fail 8. Detcheck rows: 23 (3 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 11 of 11 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-3320, CG-ALL-3321, CG-ALL-3322 |
| 8 | Contract | Fail | POST `/admin/outbound-items/{itemId}/resend` has no idempotency key; detcheck: P1 POST /api/recovery/case/v1/cases/{caseId}/actions is not published by rwb-case; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 Payload of rwb.integration.FileDelivered.v1 differs from Kafka Catalog v1; P2 Payload of rwb.integration.FileFailed.v1 differs from Kafka Catalog v1 (+8 more) | CG-ALL-3323, CG-ALL-3324, CG-ALL-3325, CG-ALL-3326, CG-ALL-3327, CG-ALL-3328, CG-ALL-3329, CG-ALL-3330, CG-ALL-3331, CG-ALL-3332, CG-ALL-3333, CG-ALL-3334 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-004; §14 lists 5 messages; detcheck: P2 MSG-P2-001 text differs from the Error and Message Standard v4 | CG-ALL-3335 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-09 has no empty, loading, error, no access state in the story; P3 SCR-28 has no empty, loading, error, no access state in the story | CG-ALL-3340, CG-ALL-3341 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3339 |
| 12 | Test cases | Fail | AC5 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-046-01, TC-E4-046-02, TC-E4-046-03, TC-E4-046-04; P2 Criteria with no test case: AC5; P3 §18 test lists differ from RTM v7 | CG-ALL-3336, CG-ALL-3337, CG-ALL-3338 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story RWB-P2-E4046-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3323 | POST /api/recovery/case/v1/cases/{caseId}/actions is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-3324 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3327 | Workflow The settlement workflow of the caller (the settlement step of `TreatmentWorkflow` on `rwb-treatment`, or the booking step of rwb-payment where the posting runs there) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 16 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3320 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3321 | Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3322 | Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3325 | Payload of rwb.integration.FileDelivered.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3326 | Payload of rwb.integration.FileFailed.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-3328 | Activity deliverFile(manifest) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3329 | Activity buildOutboundFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3330 | Activity storeOutboundFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3331 | Activity sendFileOverMft is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3332 | Activity parkItemInException is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3333 | Activity recordItemDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3334 | Activity resendItem is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3335 | MSG-P2-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3336 | Test cases not in Test Cases v8: TC-E4-046-01, TC-E4-046-02, TC-E4-046-03, TC-E4-046-04 | X9 | Missing | QA |
| CG-ALL-3337 | Criteria with no test case: AC5 | X9 | Missing | QA |
| CG-ALL-3339 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3338 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3340 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3341 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3342 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC9 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
