# Build-readiness review (script) — RWB-P8-E4049-CON Apply proceeds to the case balance - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P8-E4049-CON (RWB P8 E4049 CON Apply proceeds to the case balance - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-payment |
| Legacy key | RWB-E4-049 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Pass (not applicable) 2, Partial 9, Fail 4. Detcheck rows: 15 (4 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead of rwb-payment' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'BR-P8-010' has no BR ID; rule row 'CBR1' has no BR ID; rule row 'CBR2' has no BR ID; rule row 'CBR3' has no BR ID; rule row 'CBR4' has no BR ID; rule row 'CBR5' has no BR ID; rule row 'CBR6' has no BR ID; rule row 'CBR7' has no BR ID; rule row 'CBR8' has no BR ID; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 6 data rows; detcheck: P2 Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ce_source` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ce_subject` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-7764, CG-ALL-7765, CG-ALL-7766, CG-ALL-7767, CG-ALL-7768, CG-ALL-7769 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 Workflow The JOB-07 event-started run (name Not specified in the source documents (GAP-2530; ASM-4183)) is not in Temporal Catalog v1 (+1 more) | CG-ALL-7770, CG-ALL-7771, CG-ALL-7772, CG-ALL-7773, CG-ALL-7774 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-7775 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, loading, error, no access state in the story | CG-ALL-7777 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P8-E4049-CON-01, TC-P8-E4049-CON-02, TC-P8-E4049-CON-03, TC-P8-E4049-CON-04, TC-P8-E4049-CON-05 | CG-ALL-7776 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7770 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-7771 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-7772 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-7773 | Workflow The JOB-07 event-started run (name Not specified in the source documents (GAP-2530; ASM-4183)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7764 | Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7765 | Name `ce_source` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7766 | Name `ce_subject` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7767 | Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7768 | Name `ce_specversion` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7769 | Name `ce_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7774 | Activity The application step of JOB-07 (activity name Not specified in the source documents (GAP-2530; ASM-4183)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7775 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7776 | Test cases not in Test Cases v8: TC-P8-E4049-CON-01, TC-P8-E4049-CON-02, TC-P8-E4049-CON-03, TC-P8-E4049-CON-04, TC-P8-E4049-CON-05 | X9 | Missing | QA |
| CG-ALL-7777 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7778 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
