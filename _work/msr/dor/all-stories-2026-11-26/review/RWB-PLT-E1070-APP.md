# Build-readiness review (script) — RWB-PLT-E1070-APP Temporal platform on the ACE AKS clusters

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1070-APP (RWB PLT E1070 APP Temporal platform on the ACE AKS clusters v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-070 |

## R1. Verdict

**NOT READY.** Checklist: Pass 14, Partial 5, Fail 6. Detcheck rows: 23 (1 P1). AC review rows: 1. Missing criteria: 0.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Partial | §18 has 12 traceability rows; detcheck: P2 FR-PLT-001 has 2 meanings in the PRD; P2 FR-PLT-009 has 2 meanings in the PRD; P2 FR-PLT-010 has 2 meanings in the PRD; P2 FR-PLT-011 has 2 meanings in the PRD (+13 more) | CG-ALL-1630, CG-ALL-1631, CG-ALL-1632, CG-ALL-1633, CG-ALL-1634, CG-ALL-1635, CG-ALL-1636, CG-ALL-1637, CG-ALL-1638, CG-ALL-1639, CG-ALL-1640, CG-ALL-1641 (+5) |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 4 exception paths | — |
| 4 | Business rules | Pass | §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | 3 row(s) of §11 have no BR Field ID; §11 has 3 data rows; detcheck: P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `temporal_svc` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `temporal_visibility` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-1625, CG-ALL-1626, CG-ALL-1627 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 1 messages | — |
| 10 | Screens and states | Partial | §15 names no screen and does not say there is none | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-1629 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 build dependencies are not done yet (RWB-PLT-E1056-OPS); 11 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-1628 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E1070-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1628 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 20 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1625 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1626 | Name `temporal_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1627 | Name `temporal_visibility` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1630 | FR-PLT-001 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1631 | FR-PLT-009 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1632 | FR-PLT-010 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1633 | FR-PLT-011 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1634 | FR-PLT-012 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1635 | FR-PLT-013 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1636 | FR-PLT-016 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1637 | FR-PLT-017 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1638 | FR-PLT-018 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1639 | FR-PLT-021 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1640 | FR-PLT-022 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1641 | FR-PLT-023 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1642 | FR-PLT-024 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1643 | FR-PLT-025 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1644 | FR-PLT-026 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1645 | FR-PLT-028 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1646 | FR-PLT-029 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1629 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1647 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
