# Build-readiness review (script) — RWB-S5-E4032-APP Arrange a customer buy-back

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E4032-APP (RWB S5 E4032 APP Arrange a customer buy-back v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E4-032 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 11, Fail 6. Detcheck rows: 11 (2 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'sale officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 5 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | rule row 'R-DIS-24' has no BR ID; rule row 'R-DIS-66' has no BR ID; rule row 'VR-S5-023-1' has no BR ID; rule row 'BR-S5-023' has no BR ID; rule row 'R-DIS-61' has no BR ID; rule row 'R-DIS-62' has no BR ID; §8 has 6 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 3 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-COL-028, DF-COL-042; §11 has 9 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/asset/v1/assets is not in rwb-asset.yaml; P1 GET /api/recovery/asset/v1/assets/{assetId} is not in rwb-asset.yaml | CG-ALL-10223, CG-ALL-10224 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P2 MSG-S5-001 is used with another meaning than the standard's; P2 MSG-S5-002 is used with another meaning than the standard's; P2 MSG-GEN-001 is used with another meaning than the standard's; P2 MSG-P4-002 is used with another meaning than the standard's (+1 more) | CG-ALL-10225, CG-ALL-10226, CG-ALL-10227, CG-ALL-10228, CG-ALL-10229 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, loading, error, no access state in the story; P3 SCR-22 has no empty, loading, error, no access state in the story | CG-ALL-10231, CG-ALL-10232 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-032-01, TC-E4-032-02, TC-E4-032-03, TC-E4-032-04, TC-E4-032-05, TC-S5-E4032-APP-01, TC-S5-E4032-APP-02 | CG-ALL-10230 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S5-E4032-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.7 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10223 | GET /api/recovery/asset/v1/assets is not in rwb-asset.yaml | X5 | Missing | Solution architect |
| CG-ALL-10224 | GET /api/recovery/asset/v1/assets/{assetId} is not in rwb-asset.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10225 | MSG-S5-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10226 | MSG-S5-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10227 | MSG-GEN-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10228 | MSG-P4-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10229 | MSG-P7-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10230 | Test cases not in Test Cases v8: TC-E4-032-01, TC-E4-032-02, TC-E4-032-03, TC-E4-032-04, TC-E4-032-05, TC-S5-E4032-APP-01, TC-S5-E4032-APP-02 | X9 | Missing | QA |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10231 | SCR-21 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10232 | SCR-22 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10233 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC6. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC6 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
