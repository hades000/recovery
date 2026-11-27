# RWB-PLT-EDGE Edge and gateway - resolved items, part 1 of 2 (RWB-PLT-N001-APP to RWB-PLT-N001-APP)

Decision: D-RCV-60. Date: 26 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Every item resolved inside these stories, to spot-check the fixes against the staged files.

| Story | Ruling | Item | Section | Title | Change made |
|---|---|---|---|---|---|
| RWB-PLT-N001-APP | R-07289 | DOR-RWB-PLT-N001-APP-16 | Header | Definition of Ready item 16 Size: Fail | Added Size row stating the squad sizes at refinement |
| RWB-PLT-N001-APP | R-07292 | DOR-RWB-PLT-N001-APP-23 | Header | Definition of Ready item 23 Contract version fixed: Fail | Contract dependencies now names RWB-PLT-N001-CON v1 |
| RWB-PLT-N001-APP | R-18735 | DOR-RWB-PLT-N001-APP-2 | 18 | Definition of Ready item 2 Links: Partial | Added Feature and L3 process columns to requirement table |
| RWB-PLT-N001-APP | R-18736 | DOR-RWB-PLT-N001-APP-3 | 5, 7 | Definition of Ready item 3 Acceptance criteria: Partial | Covered by column added to section 5; AC7 and AC8 added |
| RWB-PLT-N001-APP | R-18738 | DOR-RWB-PLT-N001-APP-7 | 11 | Definition of Ready item 7 Data: Partial | Added a BR Field ID column; the seven rows carry Not specified in the source documents placeholders, since no field IDs exist in the sources. |
| RWB-PLT-N001-APP | R-21891 | GAP-1161 | find it | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Ruling keeps the plan lists as they stand; build against fakes and add the rows when the platform and reference-data stories publish. No story edit needed. |
| RWB-PLT-N001-APP | R-28805 | GAP-1277 | header | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Contract dependencies row now lists the six platform H dependencies (E1027, E1043, TE006, E1071, E1044, N001-CON) and the published C dependency RWB-P3-E1043-CON. Ready to start stays Day 1. |
| RWB-PLT-N001-APP | R-29058 | GAP-0078 | 1 | The screen for a run and its gateway route have no owner row | Section 1 now places the run screen GET /agent-runs/{id} on the RWB-PLT-N001-CON composite route, data owner P10. |
| RWB-PLT-N001-APP | R-29060 | GAP-1986 | 1 | gateway-bff and the partner gateway have no owner code, no wave and no service row | Section 1 names this story as the implementer of gateway-bff in RWB-PLT-EDGE and places the partner gateway with RWB-PLT-N007-INF; no schema, topic or task queue. |
| RWB-PLT-N001-APP | R-29061 | GAP-2379 | 1 | No source names a screen for the contact repository and the legacy screen is the template screen | Section 1 serves the party contact panel through this composite route and leaves SCR-33 with the template stories of the same service. |
| RWB-PLT-N001-APP | R-31797 | NEWAC-RWB-PLT-N001-APP-AC7 | 7, 16 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Added AC9 in section 7 (one hop, no chained call, public base) and TC-PLT-N001-APP-09 in section 16. AC1 to AC8 already cover BR2 to BR9. |
| RWB-PLT-N001-APP | R-31798 | NEWAC-RWB-PLT-N001-APP-AC8 | 7, 16 | AC8: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Added AC10 in section 7 (owner refusal of a disallowed status change relayed unchanged, per BR6) and TC-PLT-N001-APP-10 in section 16. |
