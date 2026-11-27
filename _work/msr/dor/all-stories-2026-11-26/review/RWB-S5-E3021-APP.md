# Build-readiness review (script) — RWB-S5-E3021-APP Take a property onto the books after an LED auction

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E3021-APP (RWB S5 E3021 APP Take a property onto the books after an LED auction v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E3-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 7, Partial 11, Fail 7. Detcheck rows: 24 (8 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'sale officer (RW-SALEOFF)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Section 17, BR4, BR5', not by a criterion; §7 holds 5 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DIS-03' has no BR ID; rule row 'R-DIS-01' has no BR ID; rule row 'R-DIS-02' has no BR ID; 10 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 9 transitions; detcheck: P1 The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-HOLDING; P1 The story adds ASSET_ON_BOOKS to the closed list LOV-HOLDING; P1 The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-TRANSFER-IN; P1 The story adds ASSET_ON_BOOKS to the closed list LOV-TRANSFER-IN | CG-ALL-9656, CG-ALL-9657, CG-ALL-9658, CG-ALL-9659 |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-COL-028, DF-COL-029, DF-COL-030, DF-COL-031, DF-COL-032, DF-COL-033, DF-COL-034, DF-COL-035, DF-COL-036, DF-COL-037, DF-COL-038, DF-COL-039; §11 has 21 data rows; detcheck: P2 Name `handed_over` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `holding_status` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `collateral_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 (+3 more) | CG-ALL-9660, CG-ALL-9661, CG-ALL-9662, CG-ALL-9663, CG-ALL-9664, CG-ALL-9675, CG-ALL-9676 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P2 Payload of rwb.asset.AssetTakenOn.v1 differs from Kafka Catalog v1; P1 rwb.litigation.AuctionResult.v1 is on topic rwb.litigation.events.v1 in the catalog, not rwb.litigation.events.v1`, with `.retry` and `.dlt (+3 more) | CG-ALL-9665, CG-ALL-9666, CG-ALL-9667, CG-ALL-9668, CG-ALL-9669, CG-ALL-9670, CG-ALL-9671 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-9672 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, loading, error, no access state in the story; P3 SCR-22 has no empty, loading, error, no access state in the story | CG-ALL-9677, CG-ALL-9678 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-9674 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E3-021-01, TC-E3-021-02, TC-E3-021-03, TC-E3-021-04, TC-E3-021-05, TC-E3-021-06, TC-S5-E3021-APP-01 | CG-ALL-9673 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S5-E3021-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_decision, rwb_litigation, rwb_payment | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9656 | The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-HOLDING | X1 | Conflict | Product owner |
| CG-ALL-9657 | The story adds ASSET_ON_BOOKS to the closed list LOV-HOLDING | X1 | Conflict | Product owner |
| CG-ALL-9658 | The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-TRANSFER-IN | X1 | Conflict | Product owner |
| CG-ALL-9659 | The story adds ASSET_ON_BOOKS to the closed list LOV-TRANSFER-IN | X1 | Conflict | Product owner |
| CG-ALL-9665 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-9666 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-9668 | rwb.litigation.AuctionResult.v1 is on topic rwb.litigation.events.v1 in the catalog, not rwb.litigation.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |
| CG-ALL-9669 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9660 | Name `handed_over` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9661 | Name `holding_status` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9662 | Name `collateral_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9663 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9664 | Name `inbox_event` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9667 | Payload of rwb.asset.AssetTakenOn.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-9670 | Workflow ID form and start rule of AssetDisposalWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9671 | Activity takeOnLedAuctionAsset is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-9673 | Test cases not in Test Cases v8: TC-E3-021-01, TC-E3-021-02, TC-E3-021-03, TC-E3-021-04, TC-E3-021-05, TC-E3-021-06, TC-S5-E3021-APP-01 | X9 | Missing | QA |
| CG-ALL-9674 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-9675 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9672 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-9676 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9677 | SCR-21 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9678 | SCR-22 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9679 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC6. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC6 | §5 X8: A component, a statement or a test reaches a `v_ace_*` view, a `litigation` row, a `recovery_case` row or another servic (covered by 'Section 17, BR4, BR5' only) | Not specified in the source documents | |
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
