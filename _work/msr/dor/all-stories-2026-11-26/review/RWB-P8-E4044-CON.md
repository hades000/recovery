# Build-readiness review (script) — RWB-P8-E4044-CON Match auction and enforcement proceeds

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P8-E4044-CON (RWB P8 E4044 CON Match auction and enforcement proceeds - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-payment |
| Legacy key | RWB-E4-044 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Pass (not applicable) 2, Partial 10, Fail 5. Detcheck rows: 16 (6 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 7 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | rule row 'BR-P8-004' has no BR ID; rule row 'VR-P8-004-1' has no BR ID; rule row 'R-UNI-39' has no BR ID; rule row 'R-UNI-40' has no BR ID; rule row 'DP-13, DP-14' has no BR ID; rule row 'DP-01' has no BR ID; §8 has 6 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `account_payment` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-7652, CG-ALL-7653, CG-ALL-7654, CG-ALL-7655, CG-ALL-7665 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 rwb.payment.TreatmentBooked.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, `.retry`, `.dlt; P1 rwb.payment.PaymentMissed.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, `.retry`, `.dlt (+3 more) | CG-ALL-7656, CG-ALL-7657, CG-ALL-7658, CG-ALL-7659, CG-ALL-7660, CG-ALL-7661, CG-ALL-7662 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-7663 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, loading, error, no access state in the story | CG-ALL-7666 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P8-E4044-CON-01, TC-P8-E4044-CON-02, TC-P8-E4044-CON-03, TC-P8-E4044-CON-04, TC-P8-E4044-CON-05, TC-P8-E4044-CON-06 | CG-ALL-7664 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7656 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-7657 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-7658 | rwb.payment.TreatmentBooked.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, `.retry`, `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-7659 | rwb.payment.PaymentMissed.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, `.retry`, `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-7660 | rwb.payment.ProceedsMatched.v1 is on topic rwb.payment.events.v1 in the catalog, not rwb.payment.events.v1`, `.retry`, `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-7661 | Workflow The JOB-07 payment-matching workflow (name Not specified in the source documents (GAP-2520; ASM-4170)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7652 | Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7653 | Name `account_payment` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7654 | Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7655 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7662 | Activity The matching activity, name Not specified in the source documents (GAP-2520; ASM-4170) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7665 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7663 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7664 | Test cases not in Test Cases v8: TC-P8-E4044-CON-01, TC-P8-E4044-CON-02, TC-P8-E4044-CON-03, TC-P8-E4044-CON-04, TC-P8-E4044-CON-05, TC-P8-E4044-CON-06 | X9 | Missing | QA |
| CG-ALL-7666 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7667 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
