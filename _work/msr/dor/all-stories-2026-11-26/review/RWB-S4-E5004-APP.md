# Build-readiness review (script) — RWB-S4-E5004-APP Assemble the litigation pack

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S4-E5004-APP (RWB S4 E5004 APP Assemble the litigation pack v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-litigation |
| Legacy key | RWB-E5-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 11 (4 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X11 is covered by 'BR6', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-LIT-04' has no BR ID; rule row 'R-LIT-16' has no BR ID; rule row 'R-LIT-15' has no BR ID; rule row 'R-LIT-17' has no BR ID; rule row 'R-LIT-21' has no BR ID; 8 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 10 transitions; detcheck: P1 The story adds NOTICE_BLOCKED to the closed list LOV-LEGAL-STATUS; P1 The story adds PACK_VERIFIED to the closed list LOV-LEGAL-STATUS; P1 The story adds PACK_ASSEMBLY to the closed list LOV-LEGAL-STATUS; P1 The story adds PACK_DEFECT_HOLD to the closed list LOV-LEGAL-STATUS | CG-ALL-9072, CG-ALL-9073, CG-ALL-9074, CG-ALL-9075 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 6 data rows; detcheck: P2 Name `period_expires_at` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-9076, CG-ALL-9077 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-9078 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-19 has no empty, loading, error, no access state in the story | CG-ALL-9080, CG-ALL-9081 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E5-004-01, TC-E5-004-02, TC-E5-004-03, TC-E5-004-04, TC-E5-004-05, TC-E5-004-06 | CG-ALL-9079 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S4-E5004-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case, rwb-document; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9072 | The story adds NOTICE_BLOCKED to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-9073 | The story adds PACK_VERIFIED to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-9074 | The story adds PACK_ASSEMBLY to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |
| CG-ALL-9075 | The story adds PACK_DEFECT_HOLD to the closed list LOV-LEGAL-STATUS | X1 | Conflict | Product owner |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9076 | Name `period_expires_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9077 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9079 | Test cases not in Test Cases v8: TC-E5-004-01, TC-E5-004-02, TC-E5-004-03, TC-E5-004-04, TC-E5-004-05, TC-E5-004-06 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9078 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-9080 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9081 | SCR-19 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9082 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X11: A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table (covered by 'BR6' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC9 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
