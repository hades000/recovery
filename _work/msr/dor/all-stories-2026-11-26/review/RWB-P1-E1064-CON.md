# Build-readiness review (script) — RWB-P1-E1064-CON Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1064-CON (RWB P1 E1064 CON Data dictionary for the 14 data products - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-064 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Pass (not applicable) 2, Partial 7, Fail 3. Detcheck rows: 7 (0 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'recovery developer and data steward' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 1 of 9 rules are covered by no criterion and no test case: BR8; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | 47 row(s) of §11 have no BR Field ID; §11 has 47 data rows; detcheck: P2 Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `v_data_dictionary` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2239, CG-ALL-2240 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P1-021 text differs from the Error and Message Standard v4 | CG-ALL-2241 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-40 has no empty, loading, error, no access state in the story | CG-ALL-2244 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 17 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E1-064-C01, TC-E1-064-C02, TC-E1-064-C03, TC-E1-064-C04, TC-E1-064-C05, TC-E1-064-C06, TC-E1-064-C07, TC-E1-064-C08; P3 §18 test lists differ from RTM v7 | CG-ALL-2242, CG-ALL-2243 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608) | — |
| 19 | Test data | Pass | every test case in §16 names its data (17) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2239 | Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2240 | Name `v_data_dictionary` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2241 | MSG-P1-021 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2242 | Test cases not in Test Cases v8: TC-E1-064-C01, TC-E1-064-C02, TC-E1-064-C03, TC-E1-064-C04, TC-E1-064-C05, TC-E1-064-C06, TC-E1-064-C07, TC-E1-064-C08 | X9 | Missing | QA |
| CG-ALL-2243 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2244 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2245 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
