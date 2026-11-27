# Build-readiness review (script) — RWB-P7-E2027-APP Payment matching rules with the data team

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2027-APP (RWB P7 E2027 APP Payment matching rules with the data team v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-027 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 16 (2 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'center of excellence analyst (RW-COE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 1 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X4 is covered by 'TC-E2-027-07, TC-E2-027-13', not by a criterion; exception X6 is covered by 'TC-E2-027-06', not by a criterion; exception X7 is covered by 'TC-E2-027-06', not by a criterion; exception X8 is covered by 'TC-E2-027-11, TC-E2-027-12', not by a criterion; exception X9 is covered by 'TC-E2-027-10', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 4 of 13 rules are covered by no criterion and no test case: BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Field IDs DF-DEC-001 to DF-DEC-031 are not all fields of decision_log_entry in LDM v9 | CG-ALL-7319 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no session; 404 an unknown package code or version; P2 Payload of rwb.decision.RulePackageInForce.v1 differs from Kafka Catalog v1; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-7320, CG-ALL-7322, CG-ALL-7323 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4; P2 MSG-P3-015 is used with another meaning than the standard's | CG-ALL-7324, CG-ALL-7325 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-28 has no empty, loading, error, no access state in the story; P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-40 has no empty, loading, error, no access state in the story | CG-ALL-7330, CG-ALL-7331, CG-ALL-7332 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-027-12, TC-E2-027-13; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-7326, CG-ALL-7327, CG-ALL-7328 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7321 |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL24 (assumptions: none); detcheck: P2 Open decision DL24 has no assumption | CG-ALL-7334 |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2027-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7321 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7323 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7319 | Field IDs DF-DEC-001 to DF-DEC-031 are not all fields of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7320 | HTTP errors with no message ID: 401 no session; 404 an unknown package code or version | X5 | Missing | Business analyst |
| CG-ALL-7322 | Payload of rwb.decision.RulePackageInForce.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7324 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7325 | MSG-P3-015 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7326 | Test cases not in Test Cases v8: TC-E2-027-12, TC-E2-027-13 | X9 | Missing | QA |
| CG-ALL-7334 | Open decision DL24 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7327 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-7328 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7329 | Flyway file V2027_1__decision_payment_match_governance.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7330 | SCR-28 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7331 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7332 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7333 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X4: The decision record of an action cannot be written (covered by 'TC-E2-027-07, TC-E2-027-13' only) | Not specified in the source documents | |
| AC12 | §5 X6: A version label that already exists for the package is loaded again (covered by 'TC-E2-027-06' only) | Not specified in the source documents | |
| AC13 | §5 X7: An empty workbook, or a workbook without validFrom, is loaded (covered by 'TC-E2-027-06' only) | Not specified in the source documents | |
| AC14 | §5 X8: The caller holds no right for the operation, or the version is outside the caller's scope (covered by 'TC-E2-027-11, TC-E2-027-12' only) | Not specified in the source documents | |
| AC15 | §5 X9: No version has a valid-from date on or before the business date, so no version is in force for it (covered by 'TC-E2-027-10' only) | Not specified in the source documents | |
| AC16 | §8 BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC18 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
