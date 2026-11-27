# Build-readiness review (script) — RWB-S9-E6033-CON Receive a partner result into the case - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E6033-CON (RWB S9 E6033 CON Receive a partner result into the case - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E6-033 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 8, Fail 4. Detcheck rows: 10 (3 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'contract owner of the partner service' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'Section 3', not by a criterion; §7 holds 5 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Pass | §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | 6 row(s) of §11 have no BR Field ID; §11 has 6 data rows; detcheck: P2 Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-11872, CG-ALL-11873 |
| 8 | Contract | Fail | detcheck: P1 POST /partner/instructions/{instructionId}/results` (API-S9-005) is not in rwb-partner.yaml; P1 GET /partner/instructions` (API-S9-003) is not in rwb-partner.yaml; P1 Workflow InstructionWorkflow task queue rwb-partner`, namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of InstructionWorkflow are not stated | CG-ALL-11874, CG-ALL-11875, CG-ALL-11876, CG-ALL-11877 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-34 has no empty, loading, error, no access state in the story; P3 SCR-35 has no empty, loading, error, no access state in the story | CG-ALL-11879, CG-ALL-11880 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 5 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E6-033-03, TC-S9-E6033-CON-01, TC-S9-E6033-CON-02, TC-S9-E6033-CON-03, TC-S9-E6033-CON-04 | CG-ALL-11878 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (5) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11874 | POST /partner/instructions/{instructionId}/results` (API-S9-005) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11875 | GET /partner/instructions` (API-S9-003) is not in rwb-partner.yaml | X5 | Missing | Solution architect |
| CG-ALL-11876 | Workflow InstructionWorkflow task queue rwb-partner`, namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11872 | Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11873 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11877 | Workflow ID form and start rule of InstructionWorkflow are not stated | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11878 | Test cases not in Test Cases v8: TC-E6-033-03, TC-S9-E6033-CON-01, TC-S9-E6033-CON-02, TC-S9-E6033-CON-03, TC-S9-E6033-CON-04 | X9 | Missing | QA |
| CG-ALL-11879 | SCR-34 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11880 | SCR-35 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11881 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC6. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC6 | §5 X6: A value the consumers need is named by no source — the multipart bound, the error bodies or the payload beyond three fie (covered by 'Section 3' only) | Not specified in the source documents | |
| AC7 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
