# Build-readiness review (script) — RWB-P1-ACE001-DB ACE DB additions for the Recovery Workbench

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-ACE001-DB (RWB P1 ACE001 DB ACE DB additions for the Recovery Workbench - ACE DB v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-ACE-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 8, Fail 5. Detcheck rows: 17 (0 P1). AC review rows: 1. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'ACE database engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 7 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | 31 row(s) of §11 have no BR Field ID; BR Field IDs not in LDM v9: DF-ACC-006, DF-ACC-009, DF-ACC-010, DF-ACC-011, DF-ACC-015, DF-ACC-030, DF-ACC-031, DF-INT-035, DF-INT-036, DF-PTY-003, DF-PTY-006, DF-PTY-009; §11 has 43 data rows; detcheck: P2 Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `collateral_detail_key` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `business_unit` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5 (+9 more) | CG-ALL-1825, CG-ALL-1826, CG-ALL-1827, CG-ALL-1828, CG-ALL-1829, CG-ALL-1830, CG-ALL-1831, CG-ALL-1832, CG-ALL-1833, CG-ALL-1834, CG-ALL-1835, CG-ALL-1836 (+1) |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 0 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-1840 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 9 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-1838 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P1-ACE001-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_no_grant | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 13 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1825 | Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1826 | Name `collateral_detail_key` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1827 | Name `business_unit` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1828 | Name `principal_outstanding` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1829 | Name `interest_outstanding` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1830 | Name `fees_outstanding` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1831 | Name `daily_bucket` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1832 | Name `settlement_booked_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1833 | Name `settlement_booked_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1834 | Name `party_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1835 | Name `id_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1836 | Name `action_contact_status` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-1837 | Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1838 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1839 | Flyway file V027__rwb_ace_001_recovery_source_additions.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-1840 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1841 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
