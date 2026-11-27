# Build-readiness review (script) — RWB-P1-E1018-APP Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1018-APP (RWB P1 E1018 APP Case ID issuance and case record v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-018 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 7, Fail 9. Detcheck rows: 13 (5 P1). AC review rows: 2. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 20 Reference data; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case-creation job of rwb-case (SY-CASEWF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 17 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'Section 12.1', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 2 of 7 rules are covered by no criterion and no test case: BR2, BR6; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Pass | §11 has 27 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /entry-candidates?businessDate={date}&threshold={n}&page={p}&size={s} is not in rwb-source-data.yaml; P1 PUT /extension-facts/parties/{personKey} is not in rwb-source-data.yaml; P1 PUT /extension-facts/accounts/{accountKey} is not in rwb-source-data.yaml | CG-ALL-2212, CG-ALL-2213, CG-ALL-2214 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P3 MSG-GEN-006 text differs from the Error and Message Standard v4 | CG-ALL-2216, CG-ALL-2217 |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2222 |
| 12 | Test cases | Fail | AC3 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-018-15, TC-E1-018-16; P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC3; P3 §18 test lists differ from RTM v7 | CG-ALL-2218, CG-ALL-2219, CG-ALL-2220, CG-ALL-2221 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-2215 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Fail | detcheck: P1 Parameter case.entry.dpd is also written as case.entry.dpd_threshold | CG-ALL-2211 |
| 21 | Contract published | Fail | no contract story RWB-P1-E1018-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2211 | Parameter case.entry.dpd is also written as case.entry.dpd_threshold | X4 | ID collision | Business analyst |
| CG-ALL-2212 | GET /entry-candidates?businessDate={date}&threshold={n}&page={p}&size={s} is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2213 | PUT /extension-facts/parties/{personKey} is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2214 | PUT /extension-facts/accounts/{accountKey} is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2215 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2218 | Test cases not in Test Cases v8: TC-E1-018-15, TC-E1-018-16 | X9 | Missing | QA |
| CG-ALL-2220 | Criteria with no test case: AC3 | X9 | Missing | QA |
| CG-ALL-2222 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2216 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2217 | MSG-GEN-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2219 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-2221 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2223 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC3 | no test case in §16 |  |
| AC6 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X5: An ACE view raises an error or the statement exceeds its timeout (covered by 'Section 12.1' only) | Not specified in the source documents | |
| AC17 | §8 BR2, BR6 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC18 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC19 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
