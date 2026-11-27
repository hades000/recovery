# Build-readiness review (script) — RWB-P2-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E2001-APP (RWB P2 E2001 APP EFS hand-over with full history v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E2-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 25 (1 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by AC3, which this story neither owns nor names as owned by another story; exception X3 is covered by AC5, which this story neither owns nor names as owned by another story; exception X7 is covered by 'TC-E2-001-09', not by a criterion; exception X8 is covered by 'TC-E2-001-10, the CON contract tests', not by a criterion; exception X9 is covered by 'TC-E2-001-10', not by a criterion; exception X10 is covered by 'RWB-P2-E2001-OPS', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 5 of 13 rules are covered by no criterion and no test case: BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 11 row(s) of §11 have no BR Field ID; §11 has 47 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-3010, CG-ALL-3027, CG-ALL-3028 |
| 8 | Contract | Fail | detcheck: P1 Workflow EfsHandoverWorkflow is not in Temporal Catalog v1; P2 Activity acceptAceDataReady is not in Temporal Catalog v1; P2 Activity readFreshness is not in Temporal Catalog v1; P2 Activity listCandidates is not in Temporal Catalog v1 (+5 more) | CG-ALL-3011, CG-ALL-3012, CG-ALL-3013, CG-ALL-3014, CG-ALL-3015, CG-ALL-3016, CG-ALL-3017, CG-ALL-3018, CG-ALL-3019 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P3 MSG-P2-006 text differs from the Error and Message Standard v4; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-3020, CG-ALL-3021, CG-ALL-3022 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-3029, CG-ALL-3030, CG-ALL-3031 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3025 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-3023, CG-ALL-3024 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P2-E1007-APP, RWB-P2-E2001-OPS); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL06 (assumptions: ASM-0189, ASM-2559, ASM-2608, ASM-2776); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL17 (assumptions: none); open decision DL29 (assumptions: none); detcheck: P2 Open decision DL17 has no assumption; P2 Open decision DL29 has no assumption | CG-ALL-3033, CG-ALL-3034 |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P2-E2001-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P2-E1007-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3011 | Workflow EfsHandoverWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 14 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3010 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3012 | Activity acceptAceDataReady is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3013 | Activity readFreshness is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3014 | Activity listCandidates is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3015 | Activity buildGroups is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3016 | Activity createOrLinkCase is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3017 | Activity appendEfsHistory is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3018 | Activity writeRunSummary is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3019 | Activity recordRunDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3022 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3025 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3027 | Criteria and test data read ACE views directly | X12 | Outdated | QA |
| CG-ALL-3033 | Open decision DL17 has no assumption | X2 | Ambiguous | Product owner |
| CG-ALL-3034 | Open decision DL29 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3020 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3021 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3023 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-3024 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3026 | Flyway file V2001_1__handover_library_tables.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3028 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3029 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3030 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3031 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3032 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X2: The ACE batch for ALS and business date D is not COMPLETE by 09:00 (covered by AC3, which exist nowhere in this story) | Not specified in the source documents | |
| AC10 | §5 X3: The account's `person_key` has no row in the ACE customer data (covered by AC5, which exist nowhere in this story) | Not specified in the source documents | |
| AC11 | §5 X7: A role without the right requests the administrative rerun (covered by 'TC-E2-001-09' only) | Not specified in the source documents | |
| AC12 | §5 X8: rwb-source-data, rwb-case or rwb-access does not answer inside the 2 s budget (covered by 'TC-E2-001-10, the CON contract tests' only) | Not specified in the source documents | |
| AC13 | §5 X9: The run's own decision record cannot be written (covered by 'TC-E2-001-10' only) | Not specified in the source documents | |
| AC14 | §5 X10: A feature flag `rwb.integration.efs-handover` is off (covered by 'RWB-P2-E2001-OPS' only) | Not specified in the source documents | |
| AC15 | §8 BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
