# Build-readiness review (script) — RWB-ITG-E5009-ITG Instruct the firm through the portal

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E5009-ITG (RWB ITG E5009 ITG Instruct the firm through the portal - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E5-009 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 7 (2 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'member of the integration and QA team' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X4 is covered by 'TC-E5-009-01-ITG', not by a criterion; exception X11 is covered by 'TC-E5-009-05-ITG', not by a criterion; exception X12 is covered by 'TC-E5-009-01-ITG, BR6', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 13 exception paths | — |
| 4 | Business rules | Partial | 1 of 7 rules are covered by no criterion and no test case: BR7; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has 2 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 9 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-922, CG-ALL-923 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-19 has no empty, loading, error, no access state in the story | CG-ALL-927 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-926 |
| 12 | Test cases | Partial | §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E5-009-01-ITG, TC-E5-009-02-ITG, TC-E5-009-03-ITG, TC-E5-009-04-ITG, TC-E5-009-05-ITG, TC-E5-009-06-ITG; P3 §18 test lists differ from RTM v7 | CG-ALL-924, CG-ALL-925 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-S4-E5009-APP); 1 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E5009-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-922 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-923 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-924 | Test cases not in Test Cases v8: TC-E5-009-01-ITG, TC-E5-009-02-ITG, TC-E5-009-03-ITG, TC-E5-009-04-ITG, TC-E5-009-05-ITG, TC-E5-009-06-ITG | X9 | Missing | QA |
| CG-ALL-926 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-925 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-927 | SCR-19 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-928 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §5 X4: The instruction is issued but no `InstructionIssued` fact arrives on `rwb.partner.events.v1` (covered by 'TC-E5-009-01-ITG' only) | Not specified in the source documents | |
| AC8 | §5 X11: A role that does not include Litigation C is authorised, or a caller outside the case scope passes (covered by 'TC-E5-009-05-ITG' only) | Not specified in the source documents | |
| AC9 | §5 X12: The re-driven instruction with the same key creates a second instruction, a second clock or a second record (covered by 'TC-E5-009-01-ITG, BR6' only) | Not specified in the source documents | |
| AC10 | §8 BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
