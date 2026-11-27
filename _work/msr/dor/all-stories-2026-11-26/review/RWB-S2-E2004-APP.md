# Build-readiness review (script) — RWB-S2-E2004-APP Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S2-E2004-APP (RWB S2 E2004 APP Treatment entity and plan timers data model v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-treatment |
| Legacy key | RWB-E2-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 16 (7 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 8 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR6, BR7, BR8, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | 2 row(s) of §11 have no BR Field ID; BR Field IDs not in LDM v9: DF-TRT-023; §11 has 9 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-8264 |
| 8 | Contract | Fail | detcheck: P1 rwb-treatment.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data; P1 rwb-treatment.yaml holds proposedBy as a closed enum while the story reads LOV-PROPOSER as data; P1 rwb-treatment.yaml holds treatmentType as a closed enum while the story reads LOV-TREATMENT as data; P1 rwb-treatment.yaml holds outcome as a closed enum while the story reads LOV-TRT-OUTCOME as data (+4 more) | CG-ALL-8265, CG-ALL-8266, CG-ALL-8267, CG-ALL-8268, CG-ALL-8269, CG-ALL-8270, CG-ALL-8271, CG-ALL-8272 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4; P3 MSG-P4-003 text differs from the Error and Message Standard v4 | CG-ALL-8273, CG-ALL-8274 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story; P3 SCR-14 has no empty, loading, error, no access state in the story | CG-ALL-8277, CG-ALL-8278, CG-ALL-8279 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-S2-E2004-APP-01, TC-S2-E2004-APP-02, TC-S2-E2004-APP-03, TC-S2-E2004-APP-04, TC-S2-E2004-APP-05, TC-S2-E2004-APP-06, TC-S2-E2004-APP-07, TC-S2-E2004-APP-08, TC-S2-E2004-APP-09, TC-S2-E2004-APP-10; P3 §18 test lists differ from RTM v7 | CG-ALL-8275, CG-ALL-8276 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S2-E2004-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.7 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8265 | rwb-treatment.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data | X5 | Conflict | Solution architect |
| CG-ALL-8266 | rwb-treatment.yaml holds proposedBy as a closed enum while the story reads LOV-PROPOSER as data | X5 | Conflict | Solution architect |
| CG-ALL-8267 | rwb-treatment.yaml holds treatmentType as a closed enum while the story reads LOV-TREATMENT as data | X5 | Conflict | Solution architect |
| CG-ALL-8268 | rwb-treatment.yaml holds outcome as a closed enum while the story reads LOV-TRT-OUTCOME as data | X5 | Conflict | Solution architect |
| CG-ALL-8269 | rwb-treatment.yaml holds signatureStatus as a closed enum while the story reads LOV-TRT-SIGNATURE as data | X5 | Conflict | Solution architect |
| CG-ALL-8270 | rwb.treatment.TreatmentApproved.v1 is on topic rwb.treatment.events.v1 in the catalog, not rwb.treatment.events.v1, with the retry and `.dlt` topics | X6 | Conflict | Solution architect |
| CG-ALL-8271 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8264 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8272 | rwb-treatment is not a consumer of rwb.case.CaseStateChanged.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-8273 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8275 | Test cases not in Test Cases v8: TC-S2-E2004-APP-01, TC-S2-E2004-APP-02, TC-S2-E2004-APP-03, TC-S2-E2004-APP-04, TC-S2-E2004-APP-05, TC-S2-E2004-APP-06, TC-S2-E2004-APP-07, TC-S2-E2004-APP-08, TC-S2-E2004-APP-09, TC-S2-E2004-APP-10 | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8274 | MSG-P4-003 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8276 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-8277 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8278 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8279 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §8 BR1, BR2, BR3, BR4, BR6, BR7, BR8, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC18 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
