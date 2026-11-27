# Build-readiness review (script) — RWB-P7-E1046-APP Template and merge field catalog as data

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E1046-APP (RWB P7 E1046 APP Template and merge field catalog as data v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E1-046 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 5, Fail 7. Detcheck rows: 11 (2 P1). AC review rows: 2. Missing criteria: 0.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'internal audit lead (RW-AUDIT) and a decision approver inside their authority' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | rule row 'Only a version in state Approved, carryi' has no BR ID; rule row 'The version in force on a business date ' has no BR ID; rule row 'A withdrawn version has no current versi' has no BR ID; rule row 'Every merge code an answer uses exists i' has no BR ID; rule row 'A refused answer is refused in whole: no' has no BR ID; rule row 'A row is never updated or deleted, and a' has no BR ID; rule row 'Templates are Legal counsel's reference ' has no BR ID; rule row '`template` and `merge_field` are P6's in' has no BR ID; rule row 'The notice type and the product group ar' has no BR ID; rule row 'No business value in code: template code' has no BR ID; rule row 'Every catalog and list read is one hop w' has no BR ID; rule row 'The row carries codes, versions, identif' has no BR ID; rule row 'The row and the answer are one unit of w' has no BR ID; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 The story adds COURT_FILING to the closed list LOV-NOTICE; P1 The story adds COURT_FILING to the closed list LOV-PRODUCT | CG-ALL-6976, CG-ALL-6977 |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | 2 row(s) of §11 have no BR Field ID; §11 has 7 data rows; detcheck: P2 Name `template_use` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `entry_ref` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6978, CG-ALL-6979 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-33 has no empty, loading, error, no access state in the story; P3 SCR-40 has no empty, loading, error, no access state in the story | CG-ALL-6984, CG-ALL-6985 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC5 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC5; P3 §18 test lists differ from RTM v7 | CG-ALL-6980, CG-ALL-6981, CG-ALL-6982 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL28 (assumptions: ASM-1861, ASM-1925, ASM-2093, ASM-2727) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E1046-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6976 | The story adds COURT_FILING to the closed list LOV-NOTICE | X1 | Conflict | Product owner |
| CG-ALL-6977 | The story adds COURT_FILING to the closed list LOV-PRODUCT | X1 | Conflict | Product owner |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6978 | Name `template_use` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6979 | Name `entry_ref` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6981 | Criteria with no test case: AC5 | X9 | Missing | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6980 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6982 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6983 | Flyway file V_E1046__template_use.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6984 | SCR-33 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6985 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6986 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no test case in §16 |  |
| AC2 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
