# Build-readiness review (script) — RWB-S9-E2019-APP Partner identities through the external gateway

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E2019-APP (RWB S9 E2019 APP Partner identities through the external gateway v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E2-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 14, Partial 5, Fail 6. Detcheck rows: 8 (3 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'partner and agency manager (RW-AGENCYMG)** and the **rwb-partner service' is in the roles table | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 7 of 13 rules are covered by no criterion and no test case: BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Pass | §11 has 13 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/partner/v1/partner/instructions is not in rwb-partner.yaml; P1 GET /api/recovery/partner/v1/partners is not in rwb-partner.yaml; P1 POST /api/recovery/partner/v1/admin/reference-loads` (stated default) is not in rwb-partner.yaml; P2 HTTP errors with no message ID: 422 a load field that fails its rule, with the field named | CG-ALL-11755, CG-ALL-11756, CG-ALL-11757, CG-ALL-11758 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-11759 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-34 has no empty, loading, error, no access state in the story | CG-ALL-11761 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-11760 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL03 (assumptions: ASM-0189, ASM-0193, ASM-0578, ASM-2567); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL38 (assumptions: ASM-0245, ASM-1413, ASM-1424, ASM-1508); open decision DL40 (assumptions: ASM-0422, ASM-2705) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S9-E2019-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11755 | GET /api/recovery/partner/v1/partner/instructions is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11756 | GET /api/recovery/partner/v1/partners is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11757 | POST /api/recovery/partner/v1/admin/reference-loads` (stated default) is not in rwb-partner.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11758 | HTTP errors with no message ID: 422 a load field that fails its rule, with the field named | X5 | Missing | Business analyst |
| CG-ALL-11759 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11760 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11761 | SCR-34 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11762 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
