# Build-readiness review (script) — RWB-PLT-E2037-APP Temporal observability and run books

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E2037-APP (RWB PLT E2037 APP Temporal observability and run books v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E2-037 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 6, Fail 6. Detcheck rows: 23 (1 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Partial | §18 has 14 traceability rows; detcheck: P2 FR-PLT-001 has 2 meanings in the PRD; P2 FR-PLT-009 has 2 meanings in the PRD; P2 FR-PLT-010 has 2 meanings in the PRD; P2 FR-PLT-011 has 2 meanings in the PRD (+10 more) | CG-ALL-1727, CG-ALL-1728, CG-ALL-1729, CG-ALL-1730, CG-ALL-1731, CG-ALL-1732, CG-ALL-1733, CG-ALL-1734, CG-ALL-1735, CG-ALL-1736, CG-ALL-1737, CG-ALL-1738 (+2) |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 4 exception paths | — |
| 4 | Business rules | Partial | 2 of 11 rules are covered by no criterion and no test case: BR6, BR10; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 3 data rows; detcheck: P2 Name `workflow_stuck` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `temporal_scanner_failures_total` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-1719, CG-ALL-1720, CG-ALL-1726 |
| 8 | Contract | Fail | detcheck: P1 Workflow StuckWorkflowScanner is not in Temporal Catalog v1; P2 Activity scanStuckWorkflows is not in Temporal Catalog v1; P2 Activity publishScannerMetrics is not in Temporal Catalog v1; P2 Activity recordScanRun is not in Temporal Catalog v1 | CG-ALL-1721, CG-ALL-1722, CG-ALL-1723, CG-ALL-1724 |
| 9 | Messages | Pass | §14 lists 1 messages | — |
| 10 | Screens and states | Partial | §15 names no screen and does not say there is none | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 10 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-1725 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-PLT-E1056-OPS); 12 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E2037-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1721 | Workflow StuckWorkflowScanner is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 19 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1719 | Name `workflow_stuck` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1720 | Name `temporal_scanner_failures_total` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1722 | Activity scanStuckWorkflows is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1723 | Activity publishScannerMetrics is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1724 | Activity recordScanRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1727 | FR-PLT-001 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1728 | FR-PLT-009 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1729 | FR-PLT-010 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1730 | FR-PLT-011 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1731 | FR-PLT-012 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1732 | FR-PLT-013 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1733 | FR-PLT-021 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1734 | FR-PLT-022 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1735 | FR-PLT-023 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1736 | FR-PLT-024 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1737 | FR-PLT-025 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1738 | FR-PLT-026 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1739 | FR-PLT-028 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1740 | FR-PLT-029 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1725 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1726 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-1741 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR6, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
