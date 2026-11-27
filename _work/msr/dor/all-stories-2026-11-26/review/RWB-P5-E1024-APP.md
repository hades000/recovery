# Build-readiness review (script) — RWB-P5-E1024-APP Document store and index

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1024-APP (RWB P5 E1024 APP Document store and index v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-024 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 9 (2 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'TC-E1-024-13 (Access)', not by a criterion; exception X11 is covered by 'TC-E1-024-14 (Principle 5)', not by a criterion; exception X12 is covered by 'TC-E1-024-11 (target path)', not by a criterion; exception X13 is covered by 'TC-E1-024-08 (target path)', not by a criterion; §7 holds 12 owned criteria in Gherkin; §5 has 13 exception paths | — |
| 4 | Business rules | Partial | 1 of 9 rules are covered by no criterion and no test case: BR8; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | role SY-DOCUMENT in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Fail | §11 has 16 data rows; detcheck: P1 Index column document.created_at is not a field of document in LDM v9; P2 Name `uk_document_case_type_hash` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-5794, CG-ALL-5795 |
| 8 | Contract | Fail | detcheck: P1 rwb-document.yaml holds reviewStatus as a closed enum while the story reads LOV-REVIEW as data; P2 Payload of rwb.document.DocumentStored.v1 differs from Kafka Catalog v1 | CG-ALL-5796, CG-ALL-5797 |
| 9 | Messages | Pass | §14 lists 10 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story | CG-ALL-5801 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5799 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-5798 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P5-E1025-APP, RWB-PLT-TE012-APP); 13 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL27 (assumptions: ASM-1771, ASM-2532, ASM-2709, ASM-2716) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P5-E1025-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5794 | Index column document.created_at is not a field of document in LDM v9 | X3 | Conflict | Data |
| CG-ALL-5796 | rwb-document.yaml holds reviewStatus as a closed enum while the story reads LOV-REVIEW as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5795 | Name `uk_document_case_type_hash` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5797 | Payload of rwb.document.DocumentStored.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5799 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5798 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5800 | Flyway file V1024_1__document_store.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5801 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5802 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X10: The caller's role lacks the Documents right (covered by 'TC-E1-024-13 (Access)' only) | Not specified in the source documents | |
| AC14 | §5 X11: The decision record write fails (covered by 'TC-E1-024-14 (Principle 5)' only) | Not specified in the source documents | |
| AC15 | §5 X12: The `rwb-case` contract does not answer within 2 s, or the breaker is open (covered by 'TC-E1-024-11 (target path)' only) | Not specified in the source documents | |
| AC16 | §5 X13: The outbox relay is down when the store commits (covered by 'TC-E1-024-08 (target path)' only) | Not specified in the source documents | |
| AC17 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC18 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC19 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
