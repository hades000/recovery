# Build-readiness review (script) — RWB-P4-E1023-APP Case record view v1, read only

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1023-APP (RWB P4 E1023 APP Case record view v1, read only v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-023 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 15 (2 P1). AC review rows: 3. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'case owner, a team manager, a collector, a specialist or an auditor who opens the case record view' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 19 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by 'BR3', not by a criterion; exception X5 is covered by 'BR5', not by a criterion; exception X6 is covered by 'BR10', not by a criterion; exception X8 is covered by 'BR10', not by a criterion; exception X9 is covered by 'BR3', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 4 of 10 rules are covered by no criterion and no test case: BR3, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 8 data rows; detcheck: P2 Name `id_no_token` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `value_token` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-4960, CG-ALL-4961, CG-ALL-4972 |
| 8 | Contract | Fail | detcheck: P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data; P2 Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-4962, CG-ALL-4963, CG-ALL-4964 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P4-006 is used with another meaning than the standard's | CG-ALL-4965 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-4973 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-4970 |
| 12 | Test cases | Fail | AC2 has no test case in §16; AC5 has no test case in §16; AC9 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-023-12, TC-E1-023-13; P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC2, AC5, AC9; P3 §18 test lists differ from RTM v7 | CG-ALL-4966, CG-ALL-4967, CG-ALL-4968, CG-ALL-4969 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E1023-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4962 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-4964 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4960 | Name `id_no_token` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4961 | Name `value_token` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4963 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4965 | MSG-P4-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-4966 | Test cases not in Test Cases v8: TC-E1-023-12, TC-E1-023-13 | X9 | Missing | QA |
| CG-ALL-4968 | Criteria with no test case: AC2, AC5, AC9 | X9 | Missing | QA |
| CG-ALL-4970 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-4972 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4967 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-4969 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4971 | Flyway file V1023_1__case_record_read_path.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-4973 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4974 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | no test case in §16 |  |
| AC5 | no test case in §16 |  |
| AC9 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X3: The token carries no Recovery role, or no second factor (covered by 'BR3' only) | Not specified in the source documents | |
| AC12 | §5 X5: The caller asks for the identity number in clear (covered by 'BR5' only) | Not specified in the source documents | |
| AC13 | §5 X6: Two roles of the caller conflict (for example RW-SECADM with a business role) (covered by 'BR10' only) | Not specified in the source documents | |
| AC14 | §5 X8: The reference list of scope or capability is not available (covered by 'BR10' only) | Not specified in the source documents | |
| AC15 | §5 X9: The caller is an agent or a service identity, not a person (covered by 'BR3' only) | Not specified in the source documents | |
| AC16 | §8 BR3, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
