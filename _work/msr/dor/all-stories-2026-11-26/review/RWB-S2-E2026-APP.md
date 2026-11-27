# Build-readiness review (script) — RWB-S2-E2026-APP Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E2026-APP (RWB S2 E2026 APP Document generation engine for contract, CA and mortgage templates v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E2-026 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 9, Fail 7. Detcheck rows: 16 (4 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'restructuring officer (FCR)' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'Section 8, BR1', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-UNI-38' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; rule row 'R-DIL-16' has no BR ID; rule row 'CTL-11' has no BR ID; rule row 'CTL-14' has no BR ID; 12 of 18 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 10 roles | — |
| 7 | Data | Fail | §11 has 22 data rows; detcheck: P1 Index column treatment.contract_document_id is not a field of treatment in LDM v9; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `transfer_price` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8407, CG-ALL-8408, CG-ALL-8409, CG-ALL-8419 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/document/v1/cases/{caseId}/generated-documents` (API-P5-016), operation identifier Not specified in the source documents (GAP-1878; ASM-3080) is not published by rwb-document; P1 Event type rwb.treatment.ContractDocumentGenerated.v1 is not in Kafka Catalog v1; P1 Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of TreatmentWorkflow are not stated (+2 more) | CG-ALL-8410, CG-ALL-8411, CG-ALL-8412, CG-ALL-8413, CG-ALL-8414, CG-ALL-8415 |
| 9 | Messages | Pass | §14 lists 10 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-15 has no empty, loading, error, no access state in the story | CG-ALL-8420, CG-ALL-8421 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8418 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 20 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-S2-E2026-APP-01, TC-S2-E2026-APP-02, TC-S2-E2026-APP-03, TC-S2-E2026-APP-04; P3 §18 test lists differ from RTM v7 | CG-ALL-8416, CG-ALL-8417 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (20) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S2-E2026-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_comms, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8407 | Index column treatment.contract_document_id is not a field of treatment in LDM v9 | X3 | Conflict | Data |
| CG-ALL-8410 | POST /api/recovery/document/v1/cases/{caseId}/generated-documents` (API-P5-016), operation identifier Not specified in the source documents (GAP-1878; ASM-3080) is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-8411 | Event type rwb.treatment.ContractDocumentGenerated.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8412 | Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8408 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8409 | Name `transfer_price` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8413 | Workflow ID form and start rule of TreatmentWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8414 | Activity generateContractDocument is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8415 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8416 | Test cases not in Test Cases v8: TC-S2-E2026-APP-01, TC-S2-E2026-APP-02, TC-S2-E2026-APP-03, TC-S2-E2026-APP-04 | X9 | Missing | QA |
| CG-ALL-8418 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8417 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-8419 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8420 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8421 | SCR-15 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8422 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §5 X10: A component, a statement or a test reaches a `rwb_document`, `rwb_comms` or `rwb_case` table, a template row or a `v_ace (covered by 'Section 8, BR1' only) | Not specified in the source documents | |
| AC16 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC18 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
