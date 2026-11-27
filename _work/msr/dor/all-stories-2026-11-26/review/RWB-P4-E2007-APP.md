# Build-readiness review (script) — RWB-P4-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2007-APP (RWB P4 E2007 APP Booking confirmation from the ALS load v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 5, Fail 7. Detcheck rows: 18 (6 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT), a Credit Administration officer (RW-CREDITAD) and a platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 1 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 5 of 14 rules are covered by no criterion and no test case: BR2, BR5, BR9, BR12, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 16 data rows; detcheck: P2 Field IDs DF-REF-034 to DF-REF-039 are not all fields of role in LDM v9; P2 Criteria and test data read ACE views directly | CG-ALL-5169, CG-ALL-5182 |
| 8 | Contract | Fail | detcheck: P1 POST /authorise is not in rwb-access.yaml; P1 GET /me/permissions is not in rwb-access.yaml; P1 GET /masking-policies is not in rwb-access.yaml; P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data (+2 more) | CG-ALL-5170, CG-ALL-5171, CG-ALL-5172, CG-ALL-5174, CG-ALL-5175, CG-ALL-5176 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P2-011 text differs from the Error and Message Standard v4 | CG-ALL-5177 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-01 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-29 has no empty, loading, error, no access state in the story | CG-ALL-5183, CG-ALL-5184, CG-ALL-5185 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E2-007-11; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-5178, CG-ALL-5179, CG-ALL-5180 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-5173 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E2007-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5170 | POST /authorise is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5171 | GET /me/permissions is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5172 | GET /masking-policies is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5173 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-5174 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-5176 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5169 | Field IDs DF-REF-034 to DF-REF-039 are not all fields of role in LDM v9 | X3 | Conflict | Data |
| CG-ALL-5175 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5178 | Test cases not in Test Cases v8: TC-E2-007-11 | X9 | Missing | QA |
| CG-ALL-5182 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5177 | MSG-P2-011 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-5179 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5180 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5181 | Flyway file V2007_1__authorise_decision.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5183 | SCR-01 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5184 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5185 | SCR-29 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5186 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR2, BR5, BR9, BR12, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
