# Build-readiness review (script) — RWB-ITG-E2031-ITG Agent monitoring dashboard v2 [E3d]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2031-ITG (RWB ITG E2031 ITG Agent monitoring dashboard v2 [E3d] - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-031 |

## R1. Verdict

**NOT READY.** Checklist: Pass 14, Partial 4, Fail 7. Detcheck rows: 5 (1 P1). AC review rows: 1. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'All', not by a criterion; exception X8 is covered by 'All', not by a criterion; exception X9 is covered by 'All', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Pass | §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 26 data rows | — |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-741 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-744 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC8 has no test case in §16; §16 has 8 test cases; detcheck: P2 Criteria with no test case: AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-742, CG-ALL-743 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P10-E2031-APP, RWB-P4-E2031-APP, RWB-P7-E2005-APP); 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2031-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-741 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-742 | Criteria with no test case: AC8 | X9 | Missing | QA |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-743 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-744 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-745 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X7: The seed pack cannot be loaded (agent absent, policy version absent, segment missing, counts off) (covered by 'All' only) | Not specified in the source documents | |
| AC11 | §5 X8: A fake answers a contract version other than the one the run locked (covered by 'All' only) | Not specified in the source documents | |
| AC12 | §5 X9: The evidence pack cannot be attached to the release record (covered by 'All' only) | Not specified in the source documents | |
| AC13 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
