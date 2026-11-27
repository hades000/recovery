# Build-readiness review (script) — RWB-S9-E1032-APP Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E1032-APP (RWB S9 E1032 APP Automatic attach from the OCR intake v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E1-032 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 20 (6 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'partner portal user of an instructed firm (PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X4 is covered by 'BR6', not by a criterion; exception X7 is covered by 'Section 17', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 1 of 9 rules are covered by no criterion and no test case: BR6; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | role SY-PARTNER in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 13 data rows; detcheck: P2 Name `partner_intake` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `instruction_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `intake_item_id` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-11729, CG-ALL-11730, CG-ALL-11731, CG-ALL-11732, CG-ALL-11733, CG-ALL-11745 |
| 8 | Contract | Fail | detcheck: P1 POST /partner/instructions/{instructionId}/documents is not in rwb-partner.yaml; P1 GET /partner/instructions/{instructionId}/documents is not in rwb-partner.yaml; P1 Event type rwb.partner.PartnerDocumentSubmitted.v1 is not in Kafka Catalog v1; P1 Event type rwb.document.DocumentAttached.v1 is not in Kafka Catalog v1 (+4 more) | CG-ALL-11734, CG-ALL-11735, CG-ALL-11736, CG-ALL-11737, CG-ALL-11738, CG-ALL-11739, CG-ALL-11740, CG-ALL-11741 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story; P3 SCR-35 has no empty, loading, error, no access state in the story | CG-ALL-11746, CG-ALL-11747, CG-ALL-11748 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-S9-E1032-APP-01, TC-S9-E1032-APP-02, TC-S9-E1032-APP-03, TC-S9-E1032-APP-04, TC-S9-E1032-APP-05, TC-S9-E1032-APP-06, TC-S9-E1032-APP-07, TC-S9-E1032-APP-08; P3 §18 test lists differ from RTM v7 | CG-ALL-11742, CG-ALL-11743 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S9-E1032-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-document; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11734 | POST /partner/instructions/{instructionId}/documents is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11735 | GET /partner/instructions/{instructionId}/documents is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11736 | Event type rwb.partner.PartnerDocumentSubmitted.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11737 | Event type rwb.document.DocumentAttached.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11738 | Workflow PartnerInstructionWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11741 | Workflow PartnerIntakeReconcileWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11729 | Name `partner_intake` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11730 | Name `instruction_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11731 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11732 | Name `intake_item_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11733 | Name `uk_partner_intake_instr_hash` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11739 | Activity recordPartnerDocument` (name is this story's design choice) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11740 | Activity reconcilePartnerIntake is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-11742 | Test cases not in Test Cases v8: TC-S9-E1032-APP-01, TC-S9-E1032-APP-02, TC-S9-E1032-APP-03, TC-S9-E1032-APP-04, TC-S9-E1032-APP-05, TC-S9-E1032-APP-06, TC-S9-E1032-APP-07, TC-S9-E1032-APP-08 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11743 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11744 | Flyway file V1032_1__partner_intake.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-11745 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-11746 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11747 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11748 | SCR-35 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X4: The intake creation misses the 2 s budget or its breaker is open (covered by 'BR6' only) | Not specified in the source documents | |
| AC17 | §5 X7: A component or test reaches a document, intake, case or ledger table (covered by 'Section 17' only) | Not specified in the source documents | |
| AC18 | §8 BR6 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC19 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC20 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC21 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
