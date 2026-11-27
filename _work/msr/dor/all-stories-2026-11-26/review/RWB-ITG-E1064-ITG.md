# Build-readiness review (script) — RWB-ITG-E1064-ITG Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1064-ITG (RWB ITG E1064 ITG Data dictionary for the 14 data products - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-064 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 10, Fail 5. Detcheck rows: 6 (0 P1). AC review rows: 2. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer** proving the data dictionary and its ACE read contract end to end on the real SIT services of rwb-source-data (P1) and rwb-access (P4) and their published contracts' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 16 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X11 is covered by 'Section 12.8', not by a criterion; exception X13 is covered by 'Section 17', not by a criterion; §7 holds 13 owned criteria in Gherkin; §5 has 13 exception paths | — |
| 4 | Business rules | Partial | 6 of 18 rules are covered by no criterion and no test case: BR8, BR11, BR12, BR16, BR17, BR18; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 17 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 22 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-396 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-021 text differs from the Error and Message Standard v4 | CG-ALL-393 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-40 has no empty, loading, error, no access state in the story | CG-ALL-397 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1064-ITG-10, TC-ITG-E1064-ITG-11, TC-ITG-E1064-ITG-12, TC-ITG-E1064-ITG-13; P3 §18 test lists differ from RTM v7 | CG-ALL-394, CG-ALL-395 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P1-E1064-APP, RWB-P4-E1064-APP); 2 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1064-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-394 | Test cases not in Test Cases v8: TC-ITG-E1064-ITG-10, TC-ITG-E1064-ITG-11, TC-ITG-E1064-ITG-12, TC-ITG-E1064-ITG-13 | X9 | Missing | QA |
| CG-ALL-396 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-393 | MSG-P1-021 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-395 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-397 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-398 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC13 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §5 X11: A fake is configured for P1, P3 or P4 (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC15 | §5 X13: A suite step tries to read a service schema or a `recovery.v_ace_*` view directly (covered by 'Section 17' only) | Not specified in the source documents | |
| AC16 | §8 BR8, BR11, BR12, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
