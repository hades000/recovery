# Build-readiness review (script) — RWB-P1-DM005-APP Migrate contact and promises

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-DM005-APP (RWB P1 DM005 APP Migrate contact and promises v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-DM-005 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 10, Fail 5. Detcheck rows: 11 (0 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward (RW-DATASTEW)** and a **squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 1 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 5 of 11 rules are covered by no criterion and no test case: BR2, BR4, BR8, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `collections_history` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `party_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `contact_point_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-1915, CG-ALL-1916, CG-ALL-1917, CG-ALL-1918 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-1919 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-1922, CG-ALL-1923 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-1921 |
| 12 | Test cases | Partial | §16 has 2 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-DM-005-03, TC-DM-005-04 | CG-ALL-1920 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1069-APP); 4 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602); open decision DL29 (assumptions: none); detcheck: P2 Open decision DL29 has no assumption | CG-ALL-1925 |
| 19 | Test data | Pass | every test case in §16 names its data (2) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1001-APP, RWB-P1-E1069-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1915 | Name `collections_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1916 | Name `party_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1917 | Name `contact_point_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1918 | Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1920 | Test cases not in Test Cases v8: TC-DM-005-03, TC-DM-005-04 | X9 | Missing | QA |
| CG-ALL-1921 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-1925 | Open decision DL29 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1919 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1922 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1923 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1924 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §8 BR2, BR4, BR8, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC5 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
