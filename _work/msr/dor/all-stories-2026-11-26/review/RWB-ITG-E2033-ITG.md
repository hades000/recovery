# Build-readiness review (script) — RWB-ITG-E2033-ITG Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2033-ITG (RWB ITG E2033 ITG Case and queue list with status, owner and ageing - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-033 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 9 (4 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Partial | §18 names no feature; §18 has 3 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'TC-E2-033-12-ITG', not by a criterion; exception X10 is covered by 'All', not by a criterion; §7 holds 11 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Pass | §8 has 7 rules | — |
| 5 | State transitions | Fail | §9 has no transition (no status change in this story); detcheck: P1 The story adds CAR to the closed list LOV-CASE-STATUS; P1 The story adds CAR to the closed list LOV-PRODUCT; P1 The story adds CAR to the closed list LOV-STAGE; P1 The story adds CAR to the closed list LOV-TIMER-STATUS | CG-ALL-750, CG-ALL-751, CG-ALL-752, CG-ALL-753 |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 20 data rows | — |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-GEN-007 text differs from the Error and Message Standard v4 | CG-ALL-754 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story | CG-ALL-756 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 12 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-755 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 7 build dependencies are not done yet (RWB-P2-E2033-APP, RWB-P3-E1018-APP, RWB-P3-E1031-APP, RWB-P3-E2011-APP, RWB-P3-E2033-APP, RWB-P4-E2033-APP); 7 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL31 (assumptions: none); detcheck: P2 Open decision DL31 has no assumption | CG-ALL-758 |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2033-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-750 | The story adds CAR to the closed list LOV-CASE-STATUS | X1 | Conflict | Product owner |
| CG-ALL-751 | The story adds CAR to the closed list LOV-PRODUCT | X1 | Conflict | Product owner |
| CG-ALL-752 | The story adds CAR to the closed list LOV-STAGE | X1 | Conflict | Product owner |
| CG-ALL-753 | The story adds CAR to the closed list LOV-TIMER-STATUS | X1 | Conflict | Product owner |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-758 | Open decision DL31 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-754 | MSG-GEN-007 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-755 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-756 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-757 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X9: The caller's role does not hold Case record R, or the session is no longer valid (covered by 'TC-E2-033-12-ITG' only) | Not specified in the source documents | |
| AC13 | §5 X10: The seed pack cannot be loaded or the evidence cannot be attached (covered by 'All' only) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
