# Build-readiness review (script) — RWB-S5-E4032-CON Arrange a customer buy-back - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E4032-CON (RWB S5 E4032 CON Arrange a customer buy-back - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E4-032 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Pass (not applicable) 2, Partial 10, Fail 5. Detcheck rows: 12 (2 P1). AC review rows: 1. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'solution architect of rwb-asset' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 7 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 7 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | rule row 'BR-S5-023' has no BR ID; rule row 'R-DIS-24' has no BR ID; rule row 'R-DIS-66' has no BR ID; rule row 'R4 naming' has no BR ID; rule row 'DP13' has no BR ID; rule row 'DP19' has no BR ID; §8 has 6 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 3 roles | — |
| 7 | Data | Partial | 1 row(s) of §11 have no BR Field ID; BR Field IDs not in LDM v9: DF-COL-028, DF-COL-042; §11 has 5 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/asset/v1/assets is not in rwb-asset.yaml; P1 GET /api/recovery/asset/v1/assets/{assetId} is not in rwb-asset.yaml | CG-ALL-10234, CG-ALL-10235 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P2 MSG-S5-001 is used with another meaning than the standard's; P2 MSG-S5-002 is used with another meaning than the standard's; P2 MSG-GEN-001 is used with another meaning than the standard's; P2 MSG-P4-002 is used with another meaning than the standard's (+1 more) | CG-ALL-10236, CG-ALL-10237, CG-ALL-10238, CG-ALL-10239, CG-ALL-10240 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, loading, error, no access state in the story; P3 SCR-22 has no empty, loading, error, no access state in the story | CG-ALL-10243, CG-ALL-10244 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC4 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E4-032-01, TC-E4-032-02, TC-E4-032-03, TC-E4-032-04, TC-E4-032-05, TC-S5-E4032-CON-01, TC-S5-E4032-CON-02, TC-S5-E4032-CON-03, TC-S5-E4032-CON-04; P2 Criteria with no test case: AC4 | CG-ALL-10241, CG-ALL-10242 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.7 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10234 | GET /api/recovery/asset/v1/assets is not in rwb-asset.yaml | X5 | Missing | Solution architect |
| CG-ALL-10235 | GET /api/recovery/asset/v1/assets/{assetId} is not in rwb-asset.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10236 | MSG-S5-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10237 | MSG-S5-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10238 | MSG-GEN-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10239 | MSG-P4-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10240 | MSG-P7-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-10242 | Criteria with no test case: AC4 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10241 | Test cases not in Test Cases v8: TC-E4-032-01, TC-E4-032-02, TC-E4-032-03, TC-E4-032-04, TC-E4-032-05, TC-S5-E4032-CON-01, TC-S5-E4032-CON-02, TC-S5-E4032-CON-03, TC-S5-E4032-CON-04 | X9 | Missing | QA |
| CG-ALL-10243 | SCR-21 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10244 | SCR-22 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10245 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
