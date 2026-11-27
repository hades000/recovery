# Build-readiness review (script) — RWB-S2-E2025-APP Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E2025-APP (RWB S2 E2025 APP Extraction for the stage 2 and 3 document types v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E2-025 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 25 (4 P1). AC review rows: 1. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'Section 8, BR9', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-UNI-38' has no BR ID; rule row 'CTL-08' has no BR ID; rule row 'CTL-11' has no BR ID; rule row 'CTL-12' has no BR ID; 12 of 16 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 16 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 11 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-TRT-023; §11 has 15 data rows; detcheck: P2 Name `party_names` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `contract_amount` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `approval_no` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `approved_amount` is not a field or entity in LDM v9 or Data Classification v5 (+7 more) | CG-ALL-8382, CG-ALL-8383, CG-ALL-8384, CG-ALL-8385, CG-ALL-8386, CG-ALL-8387, CG-ALL-8388, CG-ALL-8389, CG-ALL-8390, CG-ALL-8391, CG-ALL-8392 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/document/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of TreatmentWorkflow are not stated (+1 more) | CG-ALL-8393, CG-ALL-8394, CG-ALL-8395, CG-ALL-8396, CG-ALL-8397, CG-ALL-8398 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-15 has no empty, loading, error, no access state in the story; P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-8402, CG-ALL-8403, CG-ALL-8404, CG-ALL-8405 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8401 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-S2-E2025-APP-01, TC-S2-E2025-APP-02, TC-S2-E2025-APP-03, TC-S2-E2025-APP-04; P3 §18 test lists differ from RTM v7 | CG-ALL-8399, CG-ALL-8400 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S2-E2025-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8393 | No API Specification v5 yaml has the base of /api/recovery/document/v1 | X5 | Missing | Solution architect |
| CG-ALL-8394 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-8395 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-8396 | Workflow TreatmentWorkflow task queue rwb-treatment` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 15 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8382 | Name `party_names` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8383 | Name `contract_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8384 | Name `approval_no` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8385 | Name `approved_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8386 | Name `approval_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8387 | Name `mortgage_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8388 | Name `registration_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8389 | Name `land_office` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8390 | Name `source_document_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8391 | Name `source_doc_version` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8392 | Name `source_table_version` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8397 | Workflow ID form and start rule of TreatmentWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8398 | Activity applyDocumentFacts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8399 | Test cases not in Test Cases v8: TC-S2-E2025-APP-01, TC-S2-E2025-APP-02, TC-S2-E2025-APP-03, TC-S2-E2025-APP-04 | X9 | Missing | QA |
| CG-ALL-8401 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8400 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-8402 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8403 | SCR-15 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8404 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8405 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8406 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X10: A component, a statement or a test reaches a `rwb_document` table, a `document_type` row, a `document_hub_parameter` row (covered by 'Section 8, BR9' only) | Not specified in the source documents | |
| AC13 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
