# Build-readiness review (script) — RWB-P1-DM001-APP Migrate account and arrears

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-DM001-APP (RWB P1 DM001 APP Migrate account and arrears v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-DM-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 9, Fail 5. Detcheck rows: 12 (0 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward (RW-DATASTEW) and a squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'Component test', not by a criterion; exception X6 is covered by 'Not a legacy AC; the legacy "Later home" row', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 3 of 10 rules are covered by no criterion and no test case: BR3, BR5, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Partial | role RW-CUSTSERV in §10 is not in Users Roles and Permissions v5; §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 5 data rows; detcheck: P2 Name `loan_account` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `account_payment` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `collections_history` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `load_run` is not a field or entity in LDM v9 or Data Classification v5 (+4 more) | CG-ALL-1880, CG-ALL-1881, CG-ALL-1882, CG-ALL-1883, CG-ALL-1884, CG-ALL-1885, CG-ALL-1886, CG-ALL-1887 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-1888 |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-1890 |
| 12 | Test cases | Partial | §16 has 2 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-DM-001-01, TC-DM-001-04 | CG-ALL-1889 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (2) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1880 | Name `loan_account` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1881 | Name `account_payment` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1882 | Name `collections_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1883 | Name `load_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1884 | Name `dq_exception` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1885 | Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1886 | Name `ace_to_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1887 | Name `ace_to_boolean` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1889 | Test cases not in Test Cases v8: TC-DM-001-01, TC-DM-001-04 | X9 | Missing | QA |
| CG-ALL-1890 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1888 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1891 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §5 X5: The request carries no `account_key` (covered by 'Component test' only) | Not specified in the source documents | |
| AC8 | §5 X6: The read would need a column that `v_ace_account` does not carry (covered by 'Not a legacy AC; the legacy "Later home" row' only) | Not specified in the source documents | |
| AC9 | §8 BR3, BR5, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
