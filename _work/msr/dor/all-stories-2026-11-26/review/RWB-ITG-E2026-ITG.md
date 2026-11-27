# Build-readiness review (script) — RWB-ITG-E2026-ITG Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2026-ITG (RWB ITG E2026 ITG Document generation engine for contract, CA and mortgage templates - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-026 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 7, Fail 5. Detcheck rows: 3 (1 P1). AC review rows: 0. Missing criteria: 9.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'member of the integration and QA team' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by 'TC-E2-026-05-ITG', not by a criterion; exception X7 is covered by 'TC-E2-026-09-ITG', not by a criterion; exception X8 is covered by 'TC-E2-026-10-ITG', not by a criterion; exception X9 is covered by 'TC-E2-026-11-ITG', not by a criterion; exception X11 is covered by 'TC-E2-026-12-ITG', not by a criterion; exception X12 is covered by 'TC-E2-026-15-ITG', not by a criterion; exception X13 is covered by 'All', not by a criterion; exception X14 is covered by 'All', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 14 exception paths | — |
| 4 | Business rules | Partial | 1 of 11 rules are covered by no criterion and no test case: BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 1 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Pass | §11 has 13 data rows | — |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-715 |
| 9 | Messages | Pass | §14 lists 10 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story | CG-ALL-717 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 16 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-716 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 7 build dependencies are not done yet (RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E2026-APP, RWB-P7-E2026-APP); 7 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2026-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Pass | — | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-715 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-716 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-717 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X3: The template is withdrawn with no approved successor (covered by 'TC-E2-026-05-ITG' only) | Not specified in the source documents | |
| AC10 | §5 X7: Two requests for the same treatment and template run at once (covered by 'TC-E2-026-09-ITG' only) | Not specified in the source documents | |
| AC11 | §5 X8: A template body cannot be rendered (covered by 'TC-E2-026-10-ITG' only) | Not specified in the source documents | |
| AC12 | §5 X9: No template exists for the product group or language (covered by 'TC-E2-026-11-ITG' only) | Not specified in the source documents | |
| AC13 | §5 X11: The case is outside the caller's scope (covered by 'TC-E2-026-12-ITG' only) | Not specified in the source documents | |
| AC14 | §5 X12: The caller lacks Documents C (covered by 'TC-E2-026-15-ITG' only) | Not specified in the source documents | |
| AC15 | §5 X13: The seed pack cannot be loaded, or a seeded template is not approved or a treatment has no decision_log_id where the sce (covered by 'All' only) | Not specified in the source documents | |
| AC16 | §5 X14: Another run holds the environment lock (covered by 'All' only) | Not specified in the source documents | |
| AC17 | §8 BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
