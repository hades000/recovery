# Build-readiness review (script) — RWB-P8-E6036-APP Produce provision inputs

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P8-E6036-APP (RWB P8 E6036 APP Produce provision inputs v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-payment |
| Legacy key | RWB-E6-036 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 9 (1 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'finance and CFO delegate' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E6-036-03', not by a criterion; exception X7 is covered by 'Section 17', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | rule row 'VR-P8-008-1' has no BR ID; rule row 'BR-P8-008' has no BR ID; 12 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 1 row(s) of §11 have no BR Field ID; §11 has 7 data rows; detcheck: P2 Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-7790, CG-ALL-7791, CG-ALL-7796 |
| 8 | Contract | Fail | detcheck: P1 Workflow The ACE-batch-started run of the service (name Not specified in the source documents (GAP-2563; ASM-4229)) is not in Temporal Catalog v1; P2 Activity The provision-input build step (activity name Not specified in the source documents (GAP-2563; ASM-4229)) is not in Temporal Catalog v1 | CG-ALL-7792, CG-ALL-7793 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-7794 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, loading, error, no access state in the story | CG-ALL-7797 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E6-036-01, TC-E6-036-02, TC-E6-036-03, TC-E6-036-04 | CG-ALL-7795 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 2 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column; §13 names other schemas: rwb_asset, rwb_case, rwb_decision, rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7792 | Workflow The ACE-batch-started run of the service (name Not specified in the source documents (GAP-2563; ASM-4229)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7790 | Name `account_payment_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7791 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7793 | Activity The provision-input build step (activity name Not specified in the source documents (GAP-2563; ASM-4229)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7795 | Test cases not in Test Cases v8: TC-E6-036-01, TC-E6-036-02, TC-E6-036-03, TC-E6-036-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7794 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7796 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7797 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7798 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The role does not hold the Write-off and posting right R for the screen position the input set is built from (covered by 'TC-E6-036-03' only) | Not specified in the source documents | |
| AC4 | §5 X7: A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, an asset row or another `rwb_*` sche (covered by 'Section 17' only) | Not specified in the source documents | |
| AC5 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC6 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
