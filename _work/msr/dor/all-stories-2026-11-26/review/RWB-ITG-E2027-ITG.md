# Build-readiness review (script) — RWB-ITG-E2027-ITG Payment matching rules with the data team

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2027-ITG (RWB ITG E2027 ITG Payment matching rules with the data team - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-027 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 6, Fail 7. Detcheck rows: 9 (2 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 1 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by 'TC-E2-027-06-ITG', not by a criterion; exception X4 is covered by 'TC-E2-027-07-ITG', not by a criterion; exception X7 is covered by 'TC-E2-027-10-ITG', not by a criterion; exception X8 is covered by 'All', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 2 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Pass | §11 has 23 data rows | — |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-719 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-720 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, error, no access state in the story; P3 SCR-39 has no empty, loading, error, no access state in the story | CG-ALL-724, CG-ALL-725 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-027-12-ITG, TC-E2-027-13-ITG; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-721, CG-ALL-722, CG-ALL-723 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 5 build dependencies are not done yet (RWB-P3-E2042-APP, RWB-P4-E2027-APP, RWB-P7-E2027-APP, RWB-P8-E2027-APP, RWB-S2-E2027-APP); 5 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-718 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2027-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-718 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-719 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-720 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-721 | Test cases not in Test Cases v8: TC-E2-027-12-ITG, TC-E2-027-13-ITG | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-722 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-723 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-724 | SCR-28 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-725 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-726 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X3: A package version is loaded with two rows of the same row order or a tolerance above 100 (covered by 'TC-E2-027-06-ITG' only) | Not specified in the source documents | |
| AC12 | §5 X4: The decision log write fails for a match (covered by 'TC-E2-027-07-ITG' only) | Not specified in the source documents | |
| AC13 | §5 X7: No PAYMENT_MATCH version is in force on the business date (covered by 'TC-E2-027-10-ITG' only) | Not specified in the source documents | |
| AC14 | §5 X8: The seed pack cannot be loaded, another run holds the environment lock, or the evidence pack cannot be attached to the r (covered by 'All' only) | Not specified in the source documents | |
| AC15 | §8 BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC17 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC18 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
