# Build-readiness review (script) — RWB-P1-E1017-APP Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1017-APP (RWB P1 E1017 APP Retention and archive rule for the data store v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-017 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 14 (3 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'Compliance and PDPA officer (RW-COMPLY)' is in the roles table | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Section 12.2', not by a criterion; exception X9 is covered by 'Section 12.1', not by a criterion; exception X10 is covered by 'Section 12.1', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 1 of 8 rules are covered by no criterion and no test case: BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 23 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /retention-runs is not in rwb-source-data.yaml; P1 GET /retention-runs/{runId} is not in rwb-source-data.yaml; P1 Workflow RetentionRunWorkflow is not in Temporal Catalog v1; P2 Activity validateRules is not in Temporal Catalog v1 (+5 more) | CG-ALL-2181, CG-ALL-2182, CG-ALL-2183, CG-ALL-2184, CG-ALL-2185, CG-ALL-2186, CG-ALL-2187, CG-ALL-2188, CG-ALL-2189 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P3 MSG-P2-006 text differs from the Error and Message Standard v4; P2 MSG-GEN-001 is used with another meaning than the standard's | CG-ALL-2190, CG-ALL-2191 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-47 has no empty, loading, error, no access state in the story | CG-ALL-2193 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2192 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 4 build dependencies are not done yet (RWB-P1-E1001-APP, RWB-P1-E1017-OPS, RWB-P1-E1064-APP, RWB-PLT-TE012-APP); 11 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P1-E1017-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1001-APP, RWB-P1-E1064-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2181 | POST /retention-runs is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2182 | GET /retention-runs/{runId} is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2183 | Workflow RetentionRunWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2184 | Activity validateRules is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2185 | Activity selectRows(page) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2186 | Activity archiveTable is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2187 | Activity verifyManifest is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2188 | Activity deleteArchivedRows is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2189 | Activity recordRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2191 | MSG-GEN-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2190 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2192 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2193 | SCR-47 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2194 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X8: The legal-hold answer does not arrive inside the 2 s budget (covered by 'Section 12.2' only) | Not specified in the source documents | |
| AC11 | §5 X9: The `Idempotency-Key` is replayed with a different body (covered by 'Section 12.1' only) | Not specified in the source documents | |
| AC12 | §5 X10: A rule names a table this story does not own (covered by 'Section 12.1' only) | Not specified in the source documents | |
| AC13 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC16 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
