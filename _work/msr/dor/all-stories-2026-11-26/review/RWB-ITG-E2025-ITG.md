# Build-readiness review (script) — RWB-ITG-E2025-ITG Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2025-ITG (RWB ITG E2025 ITG Extraction for the stage 2 and 3 document types - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-025 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 6, Fail 6. Detcheck rows: 5 (1 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'TC-E2-025-12-ITG', not by a criterion; exception X9 is covered by 'All', not by a criterion; exception X10 is covered by 'All', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Pass | §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Pass | §11 has 17 data rows | — |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-710 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-712, CG-ALL-713 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 12 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-711 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 4 build dependencies are not done yet (RWB-P5-E2025-APP, RWB-P7-E2025-APP, RWB-S2-E2025-APP, RWB-S4-E2025-APP); 4 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2025-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-710 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-711 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-712 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-713 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-714 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X8: A role without Documents R reads the document (covered by 'TC-E2-025-12-ITG' only) | Not specified in the source documents | |
| AC10 | §5 X9: The seeded data cannot be loaded (type table row missing, sample document absent, case not as the scenario states) (covered by 'All' only) | Not specified in the source documents | |
| AC11 | §5 X10: The evidence pack cannot be attached to the release record (covered by 'All' only) | Not specified in the source documents | |
| AC12 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC13 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
