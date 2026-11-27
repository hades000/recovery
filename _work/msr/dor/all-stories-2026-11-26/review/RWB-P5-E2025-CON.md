# Build-readiness review (script) — RWB-P5-E2025-CON Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E2025-CON (RWB P5 E2025 CON Extraction for the stage 2 and 3 document types - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E2-025 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Pass (not applicable) 2, Partial 9, Fail 4. Detcheck rows: 14 (6 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 8 of 12 rules are covered by no criterion and no test case: BR2, BR3, BR4, BR6, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 11 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | 7 row(s) of §11 have no BR Field ID; §11 has 7 data rows; detcheck: P2 Name `party_names` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `review_only` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `contract_amount` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6238, CG-ALL-6239, CG-ALL-6240 |
| 8 | Contract | Fail | detcheck: P1 GET /cases/{caseId}/checked-fields is not in rwb-document.yaml; P1 GET /api/recovery/case/v1/admin/parameters/{paramCode} is not published by rwb-case; P1 POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract is not published by rwb-document; P1 GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction is not published by rwb-document (+2 more) | CG-ALL-6241, CG-ALL-6242, CG-ALL-6243, CG-ALL-6244, CG-ALL-6245, CG-ALL-6246 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-6249, CG-ALL-6250 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6248 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-6247 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6241 | GET /cases/{caseId}/checked-fields is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6242 | GET /api/recovery/case/v1/admin/parameters/{paramCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-6243 | POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-6244 | GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-6245 | GET /api/recovery/document/v1/documents/{documentId}/fields is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-6246 | rwb.document.DocumentFieldsExtracted.v1 is on topic rwb.document.events.v1 in the catalog, not rwb.document.events.v1` with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6238 | Name `party_names` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6239 | Name `review_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6240 | Name `contract_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6248 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6247 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6249 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6250 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6251 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR2, BR3, BR4, BR6, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
