# Build-readiness review (script) — RWB-P7-E1039-APP Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E1039-APP (RWB P7 E1039 APP Access log into the decision log and break-glass admin v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E1-039 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 10 (2 P1). AC review rows: 1. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 2 of 11 rules are covered by no criterion and no test case: BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Name `break_glass_grant` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6966 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml; P1 GET /api/recovery/decision/v1/decision-log/{entryId} is not in rwb-decision.yaml | CG-ALL-6967, CG-ALL-6968 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-001, MSG-P4-007; §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-38 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-6973, CG-ALL-6974 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6971 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-6969, CG-ALL-6970 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL38 (assumptions: ASM-0245, ASM-1413, ASM-1424, ASM-1508) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E1039-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6967 | GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-6968 | GET /api/recovery/decision/v1/decision-log/{entryId} is not in rwb-decision.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6966 | Name `break_glass_grant` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6971 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6969 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6970 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6972 | Flyway file V1039_1__access_ledger.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6973 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6974 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6975 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | message MSG-GEN-001, MSG-P4-007 is not in §14 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
