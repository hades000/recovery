# Build-readiness review (script) — RWB-ITG-E1063-ITG Agent monitoring dashboard v1 [E2c]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1063-ITG (RWB ITG E1063 ITG Agent monitoring dashboard v1 [E2c] - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-063 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 7, Fail 5. Detcheck rows: 3 (0 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer** proving the legacy agent monitoring dashboard end to end on the real SIT services of the plan's integration list - rwb-integration (P2), rwb-agent (P10), rwb-access (P4) and rwb-comms (P6), with rwb-source-data (P1) and rwb-reporting (P9) as wave-1 published-contract preconditions -' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 18 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'Section 12.8', not by a criterion; exception X11 is covered by 'Section 17', not by a criterion; §7 holds 13 owned criteria in Gherkin; §5 has 14 exception paths | — |
| 4 | Business rules | Partial | 4 of 16 rules are covered by no criterion and no test case: BR11, BR12, BR15, BR16; §8 has 16 rules | — |
| 5 | State transitions | Pass | §9 has 19 transitions | — |
| 6 | Authority | Pass | §10 has 14 roles | — |
| 7 | Data | Pass | §11 has 26 data rows | — |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-392 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1063-ITG-09, TC-ITG-E1063-ITG-10, TC-ITG-E1063-ITG-11, TC-ITG-E1063-ITG-12, TC-ITG-E1063-ITG-13; P3 §18 test lists differ from RTM v7 | CG-ALL-390, CG-ALL-391 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 4 build dependencies are not done yet (RWB-P10-E1063-APP, RWB-P2-E1007-APP, RWB-P4-E1063-APP, RWB-P6-E1063-APP); 4 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602); open decision DL33 (assumptions: ASM-0135, ASM-0140, ASM-0890) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1063-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-390 | Test cases not in Test Cases v8: TC-ITG-E1063-ITG-09, TC-ITG-E1063-ITG-10, TC-ITG-E1063-ITG-11, TC-ITG-E1063-ITG-12, TC-ITG-E1063-ITG-13 | X9 | Missing | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-391 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-392 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §5 X9: A fake is configured for P1, P2, P4, P6, P9 or P10 (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC15 | §5 X11: A suite step tries to read a service schema directly (covered by 'Section 17' only) | Not specified in the source documents | |
| AC16 | §8 BR11, BR12, BR15, BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
