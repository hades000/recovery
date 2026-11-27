# Build-readiness review (script) — RWB-ITG-E1002-ITG Case list v1 with case ID, owner and queue — integration

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1002-ITG (RWB ITG E1002 ITG Case list v1 with case ID, owner and queue - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 17 (4 P1). AC review rows: 4. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 20 Reference data; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'squad member (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 3 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'TC-E1-002-11-ITG', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 3 of 12 rules are covered by no criterion and no test case: BR8, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 17 data rows; detcheck: P2 Name `file_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-127, CG-ALL-139, CG-ALL-140 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data; P2 Payload of rwb.integration.FileDelivered.v1 differs from Kafka Catalog v1; P2 Payload of rwb.integration.FileFailed.v1 differs from Kafka Catalog v1; P1 Workflow ReconciliationWorkflow (JOB-04) with the case list step is not in Temporal Catalog v1 | CG-ALL-130, CG-ALL-131, CG-ALL-132, CG-ALL-133 |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-134 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story | CG-ALL-141 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-138 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 15 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1002-01, TC-ITG-E1002-02, TC-ITG-E1002-03, TC-ITG-E1002-04; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-135, CG-ALL-136, CG-ALL-137 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 5 build dependencies are not done yet (RWB-P1-E1002-APP, RWB-P2-E1007-APP, RWB-P3-E1002-APP, RWB-P3-E1018-APP, RWB-P3-E1020-APP); 5 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL17 (assumptions: none); detcheck: P2 Open decision DL17 has no assumption | CG-ALL-143 |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Fail | detcheck: P1 parameter-catalog.csv is empty, so no parameter key can be checked; P1 Parameter case.entry.dpd is also written as case.entry.dpd_threshold | CG-ALL-128, CG-ALL-129 |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1002-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_reporting, rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-128 | parameter-catalog.csv is empty, so no parameter key can be checked | X4 | Missing | Business analyst |
| CG-ALL-129 | Parameter case.entry.dpd is also written as case.entry.dpd_threshold | X4 | ID collision | Business analyst |
| CG-ALL-130 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-133 | Workflow ReconciliationWorkflow (JOB-04) with the case list step is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-127 | Name `file_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-131 | Payload of rwb.integration.FileDelivered.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-132 | Payload of rwb.integration.FileFailed.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-135 | Test cases not in Test Cases v8: TC-ITG-E1002-01, TC-ITG-E1002-02, TC-ITG-E1002-03, TC-ITG-E1002-04 | X9 | Missing | QA |
| CG-ALL-138 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-139 | Criteria and test data read ACE views directly | X12 | Outdated | QA |
| CG-ALL-143 | Open decision DL17 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-134 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-136 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-137 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-140 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-141 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-142 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC4 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC5 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC10 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X8: A role without the right lists the JOB-04 runs (covered by 'TC-E1-002-11-ITG' only) | Not specified in the source documents | |
| AC17 | §8 BR8, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
