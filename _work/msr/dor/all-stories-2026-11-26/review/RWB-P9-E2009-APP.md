# Build-readiness review (script) — RWB-P9-E2009-APP Steering dashboard v1 data set

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P9-E2009-APP (RWB P9 E2009 APP Steering dashboard v1 data set v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-reporting |
| Legacy key | RWB-E2-009 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 15 (1 P1). AC review rows: 0. Missing criteria: 11.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'TC-E2-009-10, BR7', not by a criterion; exception X7 is covered by 'BR12', not by a criterion; exception X8 is covered by 'BR9', not by a criterion; exception X9 is covered by 'BR10', not by a criterion; exception X10 is covered by 'Section 17', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 6 of 13 rules are covered by no criterion and no test case: BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-7829, CG-ALL-7840 |
| 8 | Contract | Fail | detcheck: P1 Workflow reportingMeasuresDaily` (JOB-15; name Not specified in the source documents (GAP-2576; ASM-4244)) is not in Temporal Catalog v1; P2 Activity checkFreshness is not in Temporal Catalog v1; P2 Activity loadReadModel is not in Temporal Catalog v1; P2 Activity loadAgentFacts is not in Temporal Catalog v1 (+3 more) | CG-ALL-7830, CG-ALL-7831, CG-ALL-7832, CG-ALL-7833, CG-ALL-7834, CG-ALL-7835, CG-ALL-7836 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P7-003 text differs from the Error and Message Standard v4; P3 MSG-GEN-006 text differs from the Error and Message Standard v4 | CG-ALL-7837, CG-ALL-7838 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-37 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-7841, CG-ALL-7842 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-7839 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P9-E1013-APP, RWB-P9-E2009-OPS); 10 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P9-E2009-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P9-E1013-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7830 | Workflow reportingMeasuresDaily` (JOB-15; name Not specified in the source documents (GAP-2576; ASM-4244)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7829 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7831 | Activity checkFreshness is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7832 | Activity loadReadModel is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7833 | Activity loadAgentFacts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7834 | Activity computeMeasures is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7835 | Activity reconcileCounts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7836 | Activity publishDay is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7837 | MSG-P7-003 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7838 | MSG-GEN-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-7839 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7840 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-7841 | SCR-37 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7842 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7843 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X6: The role lacks Reporting R (covered by 'TC-E2-009-10, BR7' only) | Not specified in the source documents | |
| AC11 | §5 X7: The local decision record cannot be written (covered by 'BR12' only) | Not specified in the source documents | |
| AC12 | §5 X8: The case-facts contract does not answer inside 2 s, or its breaker is open (covered by 'BR9' only) | Not specified in the source documents | |
| AC13 | §5 X9: The extract hand-over to rwb-integration fails (covered by 'BR10' only) | Not specified in the source documents | |
| AC14 | §5 X10: A component, a statement or a test reaches another service's schema, a `v_ace_*` view or the data lake (covered by 'Section 17' only) | Not specified in the source documents | |
| AC15 | §8 BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC18 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC19 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC20 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
