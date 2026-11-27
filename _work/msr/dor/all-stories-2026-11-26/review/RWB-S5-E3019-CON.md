# Build-readiness review (script) — RWB-S5-E3019-CON Take a repossessed vehicle onto the books — contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E3019-CON (RWB S5 E3019 CON Take a repossessed vehicle onto the books - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E3-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Pass (not applicable) 2, Partial 8, Fail 5. Detcheck rows: 12 (1 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | 8 row(s) of §11 have no BR Field ID; §11 has 8 data rows; detcheck: P2 Name `collateral_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `holding_status` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `holding_cost_to_date` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-9617, CG-ALL-9618, CG-ALL-9619, CG-ALL-9620 |
| 8 | Contract | Fail | detcheck: P1 rwb.asset.AssetTakenOn.v1 is on topic rwb.asset.events.v1 in the catalog, not rwb.asset.events.v1`, with `.retry` and `.dlt; P2 Workflow ID form and start rule of AssetDisposalWorkflow are not stated; P2 Activity takeOnAsset is not in Temporal Catalog v1 | CG-ALL-9621, CG-ALL-9622, CG-ALL-9623 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-9624 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, loading, error, no access state in the story; P3 SCR-22 has no empty, loading, error, no access state in the story | CG-ALL-9626, CG-ALL-9627 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E3-019-01, TC-E3-019-02, TC-E3-019-03, TC-E3-019-04, TC-E3-019-05, TC-E3-019-06, TC-S5-E3019-CON-01, TC-S5-E3019-CON-02, TC-S5-E3019-CON-03 | CG-ALL-9625 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9621 | rwb.asset.AssetTakenOn.v1 is on topic rwb.asset.events.v1 in the catalog, not rwb.asset.events.v1`, with `.retry` and `.dlt | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9617 | Name `collateral_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9618 | Name `holding_status` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9619 | Name `holding_cost_to_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9620 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9622 | Workflow ID form and start rule of AssetDisposalWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9623 | Activity takeOnAsset is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9624 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-9625 | Test cases not in Test Cases v8: TC-E3-019-01, TC-E3-019-02, TC-E3-019-03, TC-E3-019-04, TC-E3-019-05, TC-E3-019-06, TC-S5-E3019-CON-01, TC-S5-E3019-CON-02, TC-S5-E3019-CON-03 | X9 | Missing | QA |
| CG-ALL-9626 | SCR-21 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9627 | SCR-22 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9628 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
