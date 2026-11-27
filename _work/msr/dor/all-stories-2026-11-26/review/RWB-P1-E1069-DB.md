# Build-readiness review (script) — RWB-P1-E1069-DB Read-only ACE source views, grants and boundary rule - ACE DB

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1069-DB (RWB P1 E1069 DB Read-only ACE source views, grants and boundary rule - ACE DB v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-069 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 9, Fail 5. Detcheck rows: 6 (0 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'ACE database engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 8 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | 9 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | 2 row(s) of §11 have no BR Field ID; §11 has 7 data rows; detcheck: P2 Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ck_contact_point_ext_type` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-2344, CG-ALL-2345, CG-ALL-2346 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 0 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-2348 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 8 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2347 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816) | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P1-E1069-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_no_grant | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2344 | Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2345 | Name `ck_contact_point_ext_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2346 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2347 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2348 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2349 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
