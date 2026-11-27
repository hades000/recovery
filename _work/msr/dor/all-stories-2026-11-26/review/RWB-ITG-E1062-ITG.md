# Build-readiness review (script) — RWB-ITG-E1062-ITG Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1062-ITG (RWB ITG E1062 ITG Deviation screening agent in shadow [E2b] - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-062 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 7 (3 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer** proving the deviation screening agent in shadow end to end on the real SIT services of the plan's integration list - rwb-agent (P10), rwb-deviation (S8), rwb-document (P5) and rwb-access (P4), with rwb-case (P3), rwb-decision (P7) and rwb-source-data (P1) as wave-1 published-contract preconditions -' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 20 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'Section 12.8', not by a criterion; exception X13 is covered by 'Section 17', not by a criterion; §7 holds 15 owned criteria in Gherkin; §5 has 16 exception paths | — |
| 4 | Business rules | Partial | 1 of 16 rules are covered by no criterion and no test case: BR16; §8 has 16 rules | — |
| 5 | State transitions | Fail | §9 has 15 transitions; detcheck: P1 The story adds PR1 to the closed list LOV-DEVIATION | CG-ALL-383 |
| 6 | Authority | Pass | §10 has 12 roles | — |
| 7 | Data | Pass | §11 has 19 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access | CG-ALL-384 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-389 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 15 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1062-ITG-11, TC-ITG-E1062-ITG-12, TC-ITG-E1062-ITG-13, TC-ITG-E1062-ITG-14, TC-ITG-E1062-ITG-15; P3 §18 test lists differ from RTM v7 | CG-ALL-386, CG-ALL-387 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 4 build dependencies are not done yet (RWB-P10-E1062-APP, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP); 4 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-385 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1062-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_agent | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-383 | The story adds PR1 to the closed list LOV-DEVIATION | X1 | Conflict | Product owner |
| CG-ALL-384 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-385 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-386 | Test cases not in Test Cases v8: TC-ITG-E1062-ITG-11, TC-ITG-E1062-ITG-12, TC-ITG-E1062-ITG-13, TC-ITG-E1062-ITG-14, TC-ITG-E1062-ITG-15 | X9 | Missing | QA |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-387 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-388 | Flyway file V10_005__evaluation_review_count.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-389 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC15 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X10: A fake is configured for P1, P3, P4, P5, P7, P10 or S8 (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC17 | §5 X13: A suite step tries to read a service schema directly (covered by 'Section 17' only) | Not specified in the source documents | |
| AC18 | §8 BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
