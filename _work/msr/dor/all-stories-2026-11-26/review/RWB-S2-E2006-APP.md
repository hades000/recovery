# Build-readiness review (script) — RWB-S2-E2006-APP Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E2006-APP (RWB S2 E2006 APP Credit approval pack for NLEADS v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E2-006 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 13 (1 P1). AC review rows: 1. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT) recording what NLEADS decided on a plan, and the case owner reading it back afterwards' is in the roles table | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR4; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-TRT-023, DF-TRT-024, DF-TRT-025, DF-TRT-026; §11 has 14 data rows; detcheck: P2 Name `credit_result_at` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Field IDs DF-TRT-023 are not all fields of treatment in LDM v9; P2 Field IDs DF-TRT-024 are not all fields of treatment in LDM v9 (+2 more) | CG-ALL-8280, CG-ALL-8281, CG-ALL-8282, CG-ALL-8283, CG-ALL-8284, CG-ALL-8285 |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-8286 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P2-018, MSG-P4-001; §14 lists 8 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story | CG-ALL-8291 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8290 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 22 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-S2-E2006-APP-01, TC-S2-E2006-APP-02, TC-S2-E2006-APP-03, TC-S2-E2006-APP-04, TC-S2-E2006-APP-05, TC-S2-E2006-APP-06, TC-S2-E2006-APP-07, TC-S2-E2006-APP-08, TC-S2-E2006-APP-09; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-8287, CG-ALL-8288, CG-ALL-8289 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL18 (assumptions: ASM-2569, ASM-2839, ASM-2859, ASM-2883); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810) | — |
| 19 | Test data | Pass | every test case in §16 names its data (22) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S2-E2006-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8286 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8280 | Name `credit_result_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8281 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8282 | Field IDs DF-TRT-023 are not all fields of treatment in LDM v9 | X3 | Conflict | Data |
| CG-ALL-8283 | Field IDs DF-TRT-024 are not all fields of treatment in LDM v9 | X3 | Conflict | Data |
| CG-ALL-8284 | Field IDs DF-TRT-025 are not all fields of treatment in LDM v9 | X3 | Conflict | Data |
| CG-ALL-8285 | Field IDs DF-TRT-026 are not all fields of treatment in LDM v9 | X3 | Conflict | Data |
| CG-ALL-8287 | Test cases not in Test Cases v8: TC-S2-E2006-APP-01, TC-S2-E2006-APP-02, TC-S2-E2006-APP-03, TC-S2-E2006-APP-04, TC-S2-E2006-APP-05, TC-S2-E2006-APP-06, TC-S2-E2006-APP-07, TC-S2-E2006-APP-08, TC-S2-E2006-APP-09 | X9 | Missing | QA |
| CG-ALL-8290 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8288 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-8289 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-8291 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8292 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | message MSG-P2-018 is not in §14 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR4 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
