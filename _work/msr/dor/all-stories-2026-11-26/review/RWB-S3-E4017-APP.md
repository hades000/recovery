# Build-readiness review (script) — RWB-S3-E4017-APP Notify guarantors and co-borrowers

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S3-E4017-APP (RWB S3 E4017 APP Notify guarantors and co-borrowers v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-guarantee |
| Legacy key | RWB-E4-017 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 15 (3 P1). AC review rows: 0. Missing criteria: 12.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner' is in the roles table | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'TC-E4-017-03', not by a criterion; exception X2 is covered by 'TC-E4-017-01, TC-S3-E4017-CON-01', not by a criterion; exception X4 is covered by 'TC-S3-E4017-CON-04', not by a criterion; exception X5 is covered by 'TC-S3-E4017-CON-03', not by a criterion; exception X6 is covered by 'TC-S3-E4017-CON-03', not by a criterion; exception X7 is covered by 'TC-S3-E4017-CON-02', not by a criterion; exception X8 is covered by 'TC-E4-017-01', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 11 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 13 roles | — |
| 7 | Data | Partial | §11 has 13 data rows; detcheck: P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `guarantee_type` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-8897, CG-ALL-8898, CG-ALL-8899, CG-ALL-8909 |
| 8 | Contract | Fail | detcheck: P1 PATCH /guarantee-claims/{claimId}` (the notice form) is not in rwb-guarantee.yaml; P1 Workflow GuaranteeClaimWorkflow task queue rwb-guarantee` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of GuaranteeClaimWorkflow are not stated; P2 Activity resolveAddressees is not in Temporal Catalog v1 (+3 more) | CG-ALL-8900, CG-ALL-8901, CG-ALL-8902, CG-ALL-8903, CG-ALL-8904, CG-ALL-8905, CG-ALL-8906 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-8907 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-17 has no empty, loading, error, no access state in the story | CG-ALL-8910 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-017-01, TC-E4-017-02, TC-E4-017-03, TC-E4-017-04 | CG-ALL-8908 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-S3-E4017-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8900 | PATCH /guarantee-claims/{claimId}` (the notice form) is not in rwb-guarantee.yaml | X5 | Missing | Solution architect |
| CG-ALL-8901 | Workflow GuaranteeClaimWorkflow task queue rwb-guarantee` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |
| CG-ALL-8906 | Workflow armNoticeTimer is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8897 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8898 | Name `guarantee_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8899 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-8902 | Workflow ID form and start rule of GuaranteeClaimWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-8903 | Activity resolveAddressees is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8904 | Activity notifyGuarantor is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8905 | Activity recordAndApply is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-8908 | Test cases not in Test Cases v8: TC-E4-017-01, TC-E4-017-02, TC-E4-017-03, TC-E4-017-04 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-8907 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-8909 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-8910 | SCR-17 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-8911 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X1: A role without the right U or C in capability area Treatment and offer calls the notice form of the claim (covered by 'TC-E4-017-03' only) | Not specified in the source documents | |
| AC4 | §5 X2: A notice fact is incomplete: no addressee, no template code or no notice due date (covered by 'TC-E4-017-01, TC-S3-E4017-CON-01' only) | Not specified in the source documents | |
| AC5 | §5 X4: A record field is refused by the library (covered by 'TC-S3-E4017-CON-04' only) | Not specified in the source documents | |
| AC6 | §5 X5: rwb-comms answers refused for one addressee — the template is not current, or the party cannot be reached (covered by 'TC-S3-E4017-CON-03' only) | Not specified in the source documents | |
| AC7 | §5 X6: rwb-comms answers refused for every addressee (covered by 'TC-S3-E4017-CON-03' only) | Not specified in the source documents | |
| AC8 | §5 X7: A data product the notice rests on is stale after a late or failed ACE batch (covered by 'TC-S3-E4017-CON-02' only) | Not specified in the source documents | |
| AC9 | §5 X8: The same notice cycle is retried, or a consumer redelivers the signal (covered by 'TC-E4-017-01' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR3, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
