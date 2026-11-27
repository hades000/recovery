# Build-readiness review (script) — RWB-S3-E4013-APP Prepare a TCG guarantee claim

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S3-E4013-APP (RWB S3 E4013 APP Prepare a TCG guarantee claim v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-guarantee |
| Legacy key | RWB-E4-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 10, Fail 5. Detcheck rows: 10 (0 P1). AC review rows: 0. Missing criteria: 12.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'guarantee officer (RW-GUARANT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'Section 12.8', not by a criterion; exception X3 is covered by 'R-GUA-02', not by a criterion; exception X4 is covered by 'R-GUA-08 read; GAP-2708', not by a criterion; exception X5 is covered by 'Section 10', not by a criterion; exception X6 is covered by 'Section 12.8', not by a criterion; exception X7 is covered by 'Section 12.5', not by a criterion; exception X8 is covered by 'Section 9', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 12 roles | — |
| 7 | Data | Partial | §11 has 14 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `guarantee_type` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `scheme_code` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-8827, CG-ALL-8828, CG-ALL-8829 |
| 8 | Contract | Partial | PATCH `/guarantee-claims/{claimId}` has no idempotency key; detcheck: P2 rwb-guarantee is not a consumer of rwb.decision.RulePackageInForce.v1 in Kafka Catalog v1; P2 Activity assembleChecklist is not in Temporal Catalog v1; P2 Activity recordPreparation is not in Temporal Catalog v1 | CG-ALL-8830, CG-ALL-8831, CG-ALL-8832 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-17 has no empty, loading, error, no access state in the story | CG-ALL-8835 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-8834 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-013-01, TC-E4-013-02, TC-E4-013-03, TC-E4-013-04, TC-E4-013-05, TC-E4-013-06 | CG-ALL-8833 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S3-E4013-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8827 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8828 | Name `guarantee_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8829 | Name `scheme_code` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8830 | rwb-guarantee is not a consumer of rwb.decision.RulePackageInForce.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-8831 | Activity assembleChecklist is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8832 | Activity recordPreparation is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8833 | Test cases not in Test Cases v8: TC-E4-013-01, TC-E4-013-02, TC-E4-013-03, TC-E4-013-04, TC-E4-013-05, TC-E4-013-06 | X9 | Missing | QA |
| CG-ALL-8834 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8835 | SCR-17 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8836 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X2: A required claim value is missing — the guarantee type, the scheme code or the claim amount (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC6 | §5 X3: The scheme default conditions are not satisfied (covered by 'R-GUA-02' only) | Not specified in the source documents | |
| AC7 | §5 X4: The scheme checklist is incomplete at the preparation window (covered by 'R-GUA-08 read; GAP-2708' only) | Not specified in the source documents | |
| AC8 | §5 X5: A role without the right in the capability area tries the action (covered by 'Section 10' only) | Not specified in the source documents | |
| AC9 | §5 X6: The document references cannot be resolved inside the retry budget (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC10 | §5 X7: A second case signal arrives while the branch is running (covered by 'Section 12.5' only) | Not specified in the source documents | |
| AC11 | §5 X8: The date the default conditions are met is absent from the signal (covered by 'Section 9' only) | Not specified in the source documents | |
| AC12 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC16 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
