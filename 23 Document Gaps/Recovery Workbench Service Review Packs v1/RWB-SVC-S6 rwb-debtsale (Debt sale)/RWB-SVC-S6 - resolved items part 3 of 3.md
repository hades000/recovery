# RWB-SVC-S6 rwb-debtsale (Debt sale) - resolved items, part 3 of 3 (RWB-S6-E6012-APP to RWB-S6-E6012-APP)

Decision: D-RCV-60. Date: 26 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Every item resolved inside these stories, to spot-check the fixes against the staged files.

| Story | Ruling | Item | Section | Title | Change made |
|---|---|---|---|---|---|
| RWB-S6-E6012-APP | R-02864 | CG-ALL-10827 | 12.5 | Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog | Task queue in 12.5 and the section 1 line now read rwb-debtsale, as in the Temporal catalog, with no namespace. |
| RWB-S6-E6012-APP | R-08581 | DOR-RWB-S6-E6012-APP-16 | header | Definition of Ready item 16 Size: Fail | Added a Size row stating the size is Not specified in the source documents. |
| RWB-S6-E6012-APP | R-08584 | DOR-RWB-S6-E6012-APP-23 | 12 | Definition of Ready item 23 Contract version fixed: Fail | Added contract version v1 (major version of /api/recovery/debtsale/v1) under section 12; minor version Not specified. |
| RWB-S6-E6012-APP | R-13177 | CG-ALL-10828 | 12.5 | Workflow ID form and start rule of DebtSaleWorkflow are not stated | Added the DebtSaleWorkflow start rule from the catalog; workflow ID form and duplicate-start policy marked Not specified. |
| RWB-S6-E6012-APP | R-20782 | DOR-RWB-S6-E6012-APP-10 | 18 | Definition of Ready item 10 Screens and states: Partial | Added a Screen states row for SCR-26 Award: no-access and error states cited to existing test cases; empty and loading marked Not specified. |
| RWB-S6-E6012-APP | R-20783 | DOR-RWB-S6-E6012-APP-12 | 16 | Definition of Ready item 12 Test cases: Partial | Added TC-E6-012-05 (contract test of section 12) and TC-E6-012-06 (boundary test of section 12.7 tables, ASM-3438). |
| RWB-S6-E6012-APP | R-20784 | DOR-RWB-S6-E6012-APP-2 | 18 | Definition of Ready item 2 Links: Partial | Added Feature and L3 process columns to the traceability table; Feature FEAT-DBS-16, L3 process Not specified. |
| RWB-S6-E6012-APP | R-20785 | DOR-RWB-S6-E6012-APP-3 | 5, 7, 16 | Definition of Ready item 3 Acceptance criteria: Partial | AC3 covers X2 and AC4 covers X8, with TC-E6-012-07 and TC-E6-012-08; the section 5 Covered by cells now name them. |
| RWB-S6-E6012-APP | R-20786 | DOR-RWB-S6-E6012-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR10 and BR11 added for the route rows; AC5 to AC10 and TC-E6-012-09 to 14 cover BR1 to BR11 with a coverage line. |
| RWB-S6-E6012-APP | R-20788 | DOR-RWB-S6-E6012-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | MSG-P1-001 text now copied from Error and Message Standard v4 section 4; the section 14 note says no other message changed. |
| RWB-S6-E6012-APP | R-27608 | CG-ALL-10830 | 14 | MSG-P1-001 text differs from the Error and Message Standard v4 | MSG-P1-001 uses the standard text; the story's stale-data use matches the standard's use, so no new message ID is needed. |
| RWB-S6-E6012-APP | R-27609 | CG-ALL-10832 | 7, 16 | Criteria and tests keep legacy job and decision-log wording | AC1, AC2 and TC-E6-012-04 now say decision record in place of decision log; the criteria keep their legacy wording otherwise. |
| RWB-S6-E6012-APP | R-27610 | CG-ALL-10833 | 15 | SCR-26 has no empty, loading, error, no access state in the story | Empty and loading added as Not specified in the source documents; error maps to MSG-P7-003 and no access to MSG-P4-002. |
| RWB-S6-E6012-APP | R-29214 | GAP-1785 | 11 | Two state vocabularies describe the same lot: the routing ladder and the status list | DF-SAL-030 names the five-value LOV as the business status; the routing state in state is not read and is never inferred from status. |
| RWB-S6-E6012-APP | R-32889 | NEWAC-RWB-S6-E6012-APP-AC10 | 7, 16 | AC10: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Added as AC5, the next free number after AC3 and AC4, with TC-E6-012-09. The story writes no lot status, so the criterion refuses a status write. |
| RWB-S6-E6012-APP | R-32890 | NEWAC-RWB-S6-E6012-APP-AC5 | 5, 7, 16 | AC5: §5 X2: The caller's identity does not hold the right in the capability area (covered by 'TC-E6-012-03' only) | AC3 added for X2; section 5 Covered by cell names AC3, TC-E6-012-03 and TC-E6-012-07. |
| RWB-S6-E6012-APP | R-32891 | NEWAC-RWB-S6-E6012-APP-AC6 | 5, 7, 16 | AC6: §5 X8: A component, a statement or a test reaches another service's schema or a `v_ace_*` view (covered by 'Section 17' only) | AC4 added for X8; section 5 Covered by cell names AC4, TC-E6-012-06 and TC-E6-012-08. |
| RWB-S6-E6012-APP | R-32892 | NEWAC-RWB-S6-E6012-APP-AC7 | 8 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Coverage line added in section 8 mapping BR1 to BR11 to AC5 to AC10 and TC-E6-012-09 to TC-E6-012-14. |
| RWB-S6-E6012-APP | R-32893 | NEWAC-RWB-S6-E6012-APP-AC8 | 7, 16 | AC8: activity retry and timeout (no criterion covers a retried or timed-out activity) | Added AC11 (2 s non-answer retried, nothing written) in section 7 and TC-E6-012-15 in section 16; caller response Not specified. |
| RWB-S6-E6012-APP | R-32894 | NEWAC-RWB-S6-E6012-APP-AC9 | 7, 16 | AC9: a consumed call fails or does not answer (no criterion covers a failed call) | Added AC12 (failed consumed call returns no verdict and writes nothing) in section 7 and TC-E6-012-16 in section 16. |
