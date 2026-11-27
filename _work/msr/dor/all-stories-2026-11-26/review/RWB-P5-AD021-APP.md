# Build-readiness review (script) — RWB-P5-AD021-APP Retention classes and legal hold

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-AD021-APP (RWB P5 AD021 APP Retention classes and legal hold v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-AD-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 10, Fail 5. Detcheck rows: 7 (0 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'Compliance and PDPA officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no L3 process column; §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by 'TC-AD-021-01', not by a criterion; exception X4 is covered by 'TC-AD-021-01', not by a criterion; exception X5 is covered by 'TC-AD-021-02', not by a criterion; exception X6 is covered by 'TC-AD-021-03', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Partial | 1 of 8 rules are covered by no criterion and no test case: BR5; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | role SY-DOCUMENT in §10 is not in Users Roles and Permissions v5; role SY-P7 in §10 is not in Users Roles and Permissions v5; §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 12 data rows; detcheck: P2 Name `party_id` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-5708 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-002, MSG-P7-003; §14 lists 8 messages; detcheck: P2 MSG-P1-020 is used with another meaning than the standard's | CG-ALL-5709 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-31 has no empty, loading, error, no access state in the story; P3 SCR-32 has no empty, loading, error, no access state in the story | CG-ALL-5712, CG-ALL-5713 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5711 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 3 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-5710 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (3) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P5-AD021-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5708 | Name `party_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5709 | MSG-P1-020 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5711 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5710 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5712 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5713 | SCR-32 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5714 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X3: The run of the month has not yet happened, so no `retention_action` row exists for the document (covered by 'TC-AD-021-01' only) | Not specified in the source documents | |
| AC4 | §5 X4: The decision record cannot be read, or a `retention_action` row has no `decision_log_id` where the run decided (covered by 'TC-AD-021-01' only) | Not specified in the source documents | |
| AC5 | §5 X5: The P3 case contract does not answer within 2 s, or the breaker is open (covered by 'TC-AD-021-02' only) | Not specified in the source documents | |
| AC6 | §5 X6: The caller holds no Documents right R, or the case is outside the scope (covered by 'TC-AD-021-03' only) | Not specified in the source documents | |
| AC7 | §8 BR5 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
