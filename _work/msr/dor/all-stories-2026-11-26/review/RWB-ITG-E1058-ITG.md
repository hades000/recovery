# Build-readiness review (script) — RWB-ITG-E1058-ITG Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1058-ITG (RWB ITG E1058 ITG Agent platform set-up [E1a] - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-058 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 8, Fail 5. Detcheck rows: 5 (0 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer** proving the agent platform end to end on the real SIT services of rwb-agent (P10), rwb-source-data (P1), rwb-case (P3), rwb-access (P4) and rwb-document (P5)' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 22 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X13 is covered by 'Section 12.8', not by a criterion; exception X16 is covered by 'Section 17', not by a criterion; §7 holds 18 owned criteria in Gherkin; §5 has 16 exception paths | — |
| 4 | Business rules | Partial | 4 of 18 rules are covered by no criterion and no test case: BR11, BR16, BR17, BR18; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 20 transitions | — |
| 6 | Authority | Pass | §10 has 12 roles | — |
| 7 | Data | Partial | §11 has 11 data rows; detcheck: P2 Name `read_case` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `propose_deviation` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-365, CG-ALL-366 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-369 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 19 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1058-ITG-17, TC-ITG-E1058-ITG-18, TC-ITG-E1058-ITG-19; P3 §18 test lists differ from RTM v7 | CG-ALL-367, CG-ALL-368 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P10-E1058-APP); 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL33 (assumptions: ASM-0135, ASM-0140, ASM-0890) | — |
| 19 | Test data | Pass | every test case in §16 names its data (19) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1058-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-agent; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-365 | Name `read_case` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-366 | Name `propose_deviation` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-367 | Test cases not in Test Cases v8: TC-ITG-E1058-ITG-17, TC-ITG-E1058-ITG-18, TC-ITG-E1058-ITG-19 | X9 | Missing | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-368 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-369 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC19. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC19 | §5 X13: A fake is configured for P1, P3, P4 or P5 (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC20 | §5 X16: A suite step tries to read a service schema directly (covered by 'Section 17' only) | Not specified in the source documents | |
| AC21 | §8 BR11, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
