# Build-readiness review (script) — RWB-ITG-E1007-ITG Integration adapters for outbound files — integration

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1007-ITG (RWB ITG E1007 ITG Integration adapters for outbound files - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 21 (6 P1). AC review rows: 2. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | AC15 has no When; exception X2 is covered by 'TC-E1-007-03-ITG', not by a criterion; exception X4 is covered by 'TC-E1-007-05-ITG', not by a criterion; exception X5 is covered by 'TC-E1-007-06-ITG', not by a criterion; exception X7 is covered by 'TC-E1-007-10-ITG', not by a criterion; §7 holds 5 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 2 of 12 rules are covered by no criterion and no test case: BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 12 roles | — |
| 7 | Data | Partial | §11 has 13 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-161 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/document/v1/documents is not published by rwb-document; P1 GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data (+5 more) | CG-ALL-144, CG-ALL-145, CG-ALL-146, CG-ALL-147, CG-ALL-148, CG-ALL-149, CG-ALL-150, CG-ALL-151, CG-ALL-152 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P2-001 text differs from the Error and Message Standard v4; P2 MSG-P4-001 is used with another meaning than the standard's; P3 MSG-P4-003 text differs from the Error and Message Standard v4 | CG-ALL-153, CG-ALL-154, CG-ALL-155, CG-ALL-156 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-09 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-162, CG-ALL-163 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-160 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 14 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1007-01, TC-ITG-E1007-02, TC-ITG-E1007-03, TC-ITG-E1007-04; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-157, CG-ALL-158, CG-ALL-159 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 8 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1015-APP, RWB-P1-E1069-APP, RWB-P2-E1007-APP, RWB-P3-E1007-APP, RWB-P4-E1007-APP); 8 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL06 (assumptions: ASM-0189, ASM-2559, ASM-2608, ASM-2776) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1007-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-access, rwb-case, rwb-document, rwb-integration, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-144 | POST /api/recovery/document/v1/documents is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-145 | GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-146 | GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-147 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-148 | POST /api/recovery/case/v1/cases/{caseId}/actions is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-149 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-150 | Payload of rwb.integration.FileDelivered.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-151 | Payload of rwb.integration.FileFailed.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-152 | Activity deliverFile(manifest) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-154 | MSG-P2-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-155 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-157 | Test cases not in Test Cases v8: TC-ITG-E1007-01, TC-ITG-E1007-02, TC-ITG-E1007-03, TC-ITG-E1007-04 | X9 | Missing | QA |
| CG-ALL-160 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-161 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-153 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-156 | MSG-P4-003 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-158 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-159 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-162 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-163 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-164 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC15 | no When: the trigger is not stated |  |
| AC4 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X2: The outbound transfer fails on an attempt (covered by 'TC-E1-007-03-ITG' only) | Not specified in the source documents | |
| AC17 | §5 X4: The same requesting event arrives twice with the same key (covered by 'TC-E1-007-05-ITG' only) | Not specified in the source documents | |
| AC18 | §5 X5: Two worker instances pick the same due item (covered by 'TC-E1-007-06-ITG' only) | Not specified in the source documents | |
| AC19 | §5 X7: A role without the right lists or resends exception items (covered by 'TC-E1-007-10-ITG' only) | Not specified in the source documents | |
| AC20 | §8 BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC21 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
