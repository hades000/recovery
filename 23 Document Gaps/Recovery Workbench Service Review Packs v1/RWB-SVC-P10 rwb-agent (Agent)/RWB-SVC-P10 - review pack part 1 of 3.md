# RWB-SVC-P10 rwb-agent (Agent) - review pack, part 1 of 3 (RWB-P10-AD020-APP to RWB-P10-E1063-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 14 |
| Resolved in the stories | 273 |
| Cross-document (pending in another document) | 262 |
| Not applied (value not in the sources) | 10 |
| Open business decisions | 19 |
| Register gaps linked | 67 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P10-AD020-APP | 12 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 AD020 APP Autonomy level per decision step v2.md |
| RWB-P10-AD020-CON | 15 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 AD020 CON Autonomy level per decision step - contract v2.md |
| RWB-P10-E1058-APP | 28 | 28 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1058 APP Agent platform set-up [E1a] v2.md |
| RWB-P10-E1058-CON | 26 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1058 CON Agent platform set-up [E1a] - contract v2.md |
| RWB-P10-E1058-INF | 12 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1058 INF Agent platform set-up [E1a] - infrastructure v2.md |
| RWB-P10-E1058-OPS | 21 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1058 OPS Agent platform set-up [E1a] - deployment v2.md |
| RWB-P10-E1059-APP | 22 | 18 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1059 APP Case intake agent in shadow [E1b] v2.md |
| RWB-P10-E1059-CON | 16 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1059 CON Case intake agent in shadow [E1b] - contract v2.md |
| RWB-P10-E1060-APP | 19 | 5 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1060 APP Extraction evaluation [E1c] v2.md |
| RWB-P10-E1061-APP | 15 | 9 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1061 APP Intake agent evaluation and L1 proposal [E2a] v2.md |
| RWB-P10-E1061-CON | 17 | 9 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1061 CON Intake agent evaluation and L1 proposal [E2a] - contract v2.md |
| RWB-P10-E1062-APP | 24 | 33 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1062 APP Deviation screening agent in shadow [E2b] v2.md |
| RWB-P10-E1062-CON | 21 | 31 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1062 CON Deviation screening agent in shadow [E2b] - contract v2.md |
| RWB-P10-E1063-APP | 25 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1063 APP Agent monitoring dashboard v1 [E2c] v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P10-E1058-CON | R-00439 | CG-ALL-2510 | Script gap | Product owner | The story adds ECHO to the closed list LOV-AGENT-RUN | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P10-E1062-APP | R-00456 | CG-ALL-2605 | Script gap | Product owner | The story adds PR1 to the closed list LOV-DEVIATION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P10-AD020-APP | R-09811 | CG-ALL-2484 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E1058-APP | R-09822 | CG-ALL-2506 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E1058-CON | R-09833 | CG-ALL-2528 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E1059-APP | R-09844 | CG-ALL-2557 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E1059-CON | R-09857 | CG-ALL-2581 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E1061-CON | R-09863 | CG-ALL-2602 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E1062-APP | R-09873 | CG-ALL-2623 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P10-E1062-CON | R-09883 | CG-ALL-2644 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1058-ITG, RWB-P10-E1058-APP, RWB-P10-E1058-CON, RWB-P10-E1058-INF, RWB-P10-E1058-OPS | R-22204 | GAP-1521 | Register gap | Business lead | The P10 message codes are referenced in the acceptance criteria but their wording is in no source document | The PRD refers to the codes and to the message that the source names, and states no wording. The wording is taken from the Error and Message Standard at build time; a code with no entry there is a defect of the message standard and not of this PRD. |
| RWB-ITG-E1058-ITG, RWB-P10-E1058-APP, RWB-P10-E1058-CON, RWB-P10-E1058-INF, RWB-P10-E1058-OPS | R-22205 | GAP-1522 | Register gap | Product owner | The FSD P10 requirement table is empty, so no FSD requirement ID exists to map a product requirement to | This PRD maps each FR to the FSD section and acceptance criteria it serves, and to the feature code where the FSD carries one. The FSD is asked to fill its Requirements served table in its next version; no requirement ID is invented here. |
| RWB-ITG-E1058-ITG, RWB-P10-E1058-APP, RWB-P10-E1058-CON, RWB-P10-E1058-INF, RWB-P10-E1058-OPS | R-22206 | GAP-1524 | Register gap | Compliance | No retention period is stated for an agent run, a guardrail result, a feedback row, an evaluation or a sample | The PRD requires that the record is retained for the period set for it, is answerable to audit before a purge and is never removed silently, and writes the value as the R9 placeholder until Compliance sets it in DL26. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1039-APP, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22216 | GAP-2330 | Register gap | Internal audit role and the solution architect, P4 | The access entry of an agent read has no source row, element list or decision-code vocabulary of its own | Fix the entry members of a non-human read in the access-entry writer of RWB-P4-E1039-APP and publish them once for every service identity, so an audit query by agent code and policy version answers from the same chain as the screen entries. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22221 | GAP-2328 | Register gap | Compliance and PDPA officer and the security administrator role | Which of the run's fields are personal for a non-human actor, and the mask format served to an agent, are not specified | Fix the personal field list of the four agent reads and the mask format served to a non-human caller with the masking owner, load it as a masking version rather than as code, and prove it with a synthetic value that must appear in no answer, no log and no span. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E1063-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P4-E1063-APP, RWB-P6-E1063-APP | R-28650 | GAP-1213 | Register gap | data steward, data product owner and architecture owner | REQ-DRI-009 still requires a daily copy to the data lake, which DP-17 and Arch v5 slide 37 remove | Reword REQ-DRI-009 in the next BRD version as the daily agent measures being available for reporting from rwb-reporting with the row counts matched against the P10 source, keep the requirement identifier, and record that the P6 slice carries only the cost-alert notification, as ASM-B-P6-05-E1063-6 sets out. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P10-AD020-APP | R-04546 | DOR-RWB-P10-AD020-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-P10-AD020-APP found in story text or file names; grep hits were scratch or other stories. Sign-off not invented. |
| RWB-P10-E1059-APP | R-04578 | DOR-RWB-P10-E1059-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources; sign-off cannot be invented. Searched Markdown sources; only process text (DT05) found. No edit. |
| RWB-P10-E1059-APP | R-24526 | CG-ALL-2558 | 3 | Flyway file V10_004__intake_run_key.sql is not in the V0001..Vnnnn form | No V0001-form number for rwb-agent's sequence is in the sources (Service Template 3.1, 05 Technical architecture). Change log is not editable, so no file name change made. |
| RWB-P10-E1060-APP | R-04590 | DOR-RWB-P10-E1060-APP-21 | Header (story key table) | Definition of Ready item 21 Contract published: Fail | Contract story is Done only when the CON dependencies (RWB-P3-E1042-CON, RWB-P3-E1043-CON) are Done. Their status sits in their own documents, and no text edit here can change it. |
| RWB-P10-E1061-APP | R-24540 | CG-ALL-2593 | 3 | Flyway file V10_004__policy_promotion.sql is not in the V0001..Vnnnn form | Cannot apply without inventing a number. Folder grep found no rwb-agent V0001-form sequence; V0001 hits are monolith schema rulings (01 Decisions). |
| RWB-P10-E1061-APP | R-24541 | CG-ALL-2594 | 3 | Flyway file V10_003__evaluation_proposal.sql is not in the V0001..Vnnnn form | Cannot apply without inventing a number. No P10 Flyway sequence number for V10_003 in the folder; V0001 hits are monolith schema rulings (01 Decisions). |
| RWB-P10-E1061-CON | R-04600 | DOR-RWB-P10-E1061-CON-16 | section header | Definition of Ready item 16 Size: Fail | No size is given in the item or story; the squad sizes the story at refinement, so the DoR item stays open. |
| RWB-P10-E1062-CON | R-04609 | DOR-RWB-P10-E1062-CON-14 | 3 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or the source documents; the sign-off cannot be invented. Left open for the epic design record owner. |
| RWB-P10-E1062-CON | R-24554 | CG-ALL-2645 | 3, 3.1 | Flyway file V10_005__evaluation_review_count.sql is not in the V0001..Vnnnn form | No V0001-form number for this migration in Service Template Specification v1 §3 or the story set; the next number cannot be invented. Story name left unchanged. |
| RWB-P10-E1063-APP | R-24556 | CG-ALL-2653 | 3 | Flyway file V10_006__agent_alert.sql is not in the V0001..Vnnnn form | Next V-number not in sources: DP-15 rows in E1058/E1063 stories give only V0001 baseline. Not specified in the source documents (CG-ALL-2653). |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (30)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03709 | RWB-P10-E1058-APP | CG-ALL-2499 | 12.5 | Add activity ResolveAgentConfig on queue rwb-agent with the input and output of section 12.5. |
| CDC-03710 | RWB-P10-E1058-APP | CG-ALL-2500 | 12.5 | Add activity GatherInputs on queue rwb-agent with the input and output of section 12.5. |
| CDC-03711 | RWB-P10-E1058-APP | CG-ALL-2501 | 12.5 | Add activity MaskInputs on queue rwb-agent with the input and output of section 12.5. |
| CDC-03712 | RWB-P10-E1058-APP | CG-ALL-2502 | 12.5 | Add activity CallModelGateway on queue rwb-agent with the input and output of section 12.5. |
| CDC-03713 | RWB-P10-E1058-APP | CG-ALL-2503 | 12.5 | Add an Activities row CheckGuardrail on task queue rwb-agent with the input and output defined in section 12.5 of RWB-P10-E1058-APP |
| CDC-03714 | RWB-P10-E1058-APP | CG-ALL-2504 | 12.5 | Add an Activities row RecordAgentRun on task queue rwb-agent as a workflow kit activity with the input defined in section 12.5 of RWB-P10-E1058-APP |
| CDC-03735 | RWB-P10-E1058-CON | CG-ALL-2520 | 12.5 | Add activity ResolveAgentConfig to the Activities sheet, or name the catalogued activity to use. |
| CDC-03736 | RWB-P10-E1058-CON | CG-ALL-2521 | 12.5 | Add activity GatherInputs to the Activities sheet, or name the catalogued activity to use. |
| CDC-03737 | RWB-P10-E1058-CON | CG-ALL-2522 | 12.5 | Add activity MaskInputs to the Activities sheet, or name the catalogued activity to use. |
| CDC-03738 | RWB-P10-E1058-CON | CG-ALL-2523 | 12.5 | Add activity CallModelGateway to the Activities sheet, or name the catalogued activity to use. |
| CDC-03739 | RWB-P10-E1058-CON | CG-ALL-2524 | 12.5 | Add activity CheckGuardrail to the Activities sheet, or name the catalogued activity to use. |
| CDC-03740 | RWB-P10-E1058-CON | CG-ALL-2525 | 12.5 | Add a row for activity RecordAgentRun (task queue rwb-agent, workflow kit) to the Activities sheet. |
| CDC-03790 | RWB-P10-E1059-APP | CG-ALL-2549 | 12.5 | Story states one execution per run key. Workflow ID form and duplicate-start policy are marked Not specified; the catalog must state them. |
| CDC-03855 | RWB-P10-E1062-APP | CG-ALL-2616 | 12.5 | Add activity AssembleScreeningInputs, task queue rwb-agent, with the output stated for it in section 12.5. |
| CDC-03856 | RWB-P10-E1062-APP | CG-ALL-2617 | 12.5 | Add activity ResolveOwnerRole to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-03857 | RWB-P10-E1062-APP | CG-ALL-2618 | 12.5 | Add activity CallModelGateway to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-03858 | RWB-P10-E1062-APP | CG-ALL-2619 | 12.5 | Add activity CheckScreeningGuardrail to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-03859 | RWB-P10-E1062-APP | CG-ALL-2620 | 12.5 | Add activity RecordScreeningRun to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-03860 | RWB-P10-E1062-APP | CG-ALL-2621 | 12.5 | Add activity PublishScreeningEvents to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-03883 | RWB-P10-E1062-CON | CG-ALL-2636 | 12.5 | Add an Activities row for AssembleScreeningInputs (queue rwb-agent) with the input and output in section 12.5, or name a catalogued activity. |
| CDC-03884 | RWB-P10-E1062-CON | CG-ALL-2637 | 12.5 | Add an Activities row for ResolveOwnerRole (queue rwb-agent) with the input and output in section 12.5, or name a catalogued activity. |
| CDC-03885 | RWB-P10-E1062-CON | CG-ALL-2638 | 12.5 | Add an Activities row for CallModelGateway (queue rwb-agent) with the input and output in section 12.5, or name a catalogued activity. |
| CDC-03886 | RWB-P10-E1062-CON | CG-ALL-2639 | 12.5 | Add an Activities row for CheckScreeningGuardrail (queue rwb-agent) with the input and output in section 12.5, or name a catalogued activity. |
| CDC-03887 | RWB-P10-E1062-CON | CG-ALL-2640 | 12.5 | Add activity RecordScreeningRun to the Activities sheet, or agree a catalogued replacement with the solution architect. |
| CDC-03888 | RWB-P10-E1062-CON | CG-ALL-2641 | 12.5 | Add activity PublishScreeningEvents to the Activities sheet, or agree a catalogued replacement with the solution architect. |
| CDC-03908 | RWB-P10-E1063-APP | CG-ALL-2648 | 12.5 | Add a Workflows row for AgentRunDailyRollupWorkflow on task queue rwb-agent, or name its catalogued equivalent |
| CDC-03912 | RWB-P10-E1063-APP | DOR-RWB-P10-E1063-APP-8 | 12.1, 12.5 | Catalogue rows are missing. The 401 message ID is not in the sources and remains open under CG-ALL-2647. |
| CDC-03914 | RWB-P10-E1063-APP | CG-ALL-2649 | 12.5 | Add activity aggregateAgentRuns on task queue rwb-agent to the Activities sheet, as named in section 12.5 |
| CDC-03915 | RWB-P10-E1063-APP | CG-ALL-2650 | 12.5 | Add activity raiseCostAlerts on task queue rwb-agent to the Activities sheet, as named in section 12.5 |
| CDC-03916 | RWB-P10-E1063-APP | CG-ALL-2651 | 12.5 | Add activity dispatchAgentAlerts on task queue rwb-agent to the Activities sheet, as named in section 12.5 |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (22)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03708 | RWB-P10-E1058-APP | CG-ALL-2490 | 4, 12.2, 13 | Record read_case as a tool identifier of the allow-list in the owning document, not as a data entity or field; no dictionary rename. |
| CDC-03718 | RWB-P10-E1058-APP | GAP-1520 | find it | State the base /api/recovery/agent/v1 and the operations in product terms; leave exact path names to the service contract (API Specification v4 and Ownership Map). |
| CDC-03719 | RWB-P10-E1058-APP | GAP-1528 | find it | Require a read-only tool gateway for waves 1 and 2; treat the allowed tool list as a narrowing allow list; record any write tool as an open question. |
| CDC-03725 | RWB-P10-E1058-APP | GAP-1525 | find it | Write the placeholder in the release date cell of the platform slice and state that no capability starts before its platform enablers exist. |
| CDC-03726 | RWB-P10-E1058-APP | GAP-1530 | find it | Give each of the four features its own criterion for its behaviour; keep the repeated source criteria as shared background. |
| CDC-03727 | RWB-P10-E1058-APP | GAP-1533 | find it | Slice the sixteen agent features by wave from their epic, take dates from BRD Program v5 section 8 unchanged, and mark every date tentative. |
| CDC-03750 | RWB-P10-E1058-CON | GAP-1525 | find it | Write the placeholder in the release date cell of the platform slice and state that no capability starts before its platform enablers exist. |
| CDC-03751 | RWB-P10-E1058-CON | GAP-1530 | find it | Give each of the four features its own behaviour criterion and keep the repeated source criteria as shared background. |
| CDC-03760 | RWB-P10-E1058-INF | GAP-1520 | find it | State the service base /api/recovery/agent/v1 and the operations in product terms; exact paths belong to the service contract (API Specification v4 and Ownership Map). |
| CDC-03761 | RWB-P10-E1058-INF | GAP-1528 | find it | Require a read-only tool gateway for waves 1 and 2; treat the allowed tool list as an allow list that only narrows reads; record any write tool as an open question. |
| CDC-03766 | RWB-P10-E1058-INF | GAP-1525 | find it | In the release date cell of the platform slice, give November 2026 as the wave month, write Not specified in the source documents (GAP-1525) for the day, and state that no capability starts before its platform enablers exist. |
| CDC-03767 | RWB-P10-E1058-INF | GAP-1530 | find it | Give each of the four features its own criterion (guardrail rejects, fallback returns rule result, harness scores, set-up produces run row and event) and keep the repeated criteria as shared background. |
| CDC-03782 | RWB-P10-E1058-OPS | GAP-1530 | none | Keep the criteria stated once; give each feature its own behaviour criterion (guardrail rejects, fallback returns rule result, harness scores, set-up produces run row and event); repeated source criteria stay as shared background. |
| CDC-03893 | RWB-P10-E1062-CON | GAP-1826 |  | Name all 22 R-DEV rules as the S8 requirement set and add R-DEV-19 to R-DEV-21 from the design. Package authoring, version label and promotion stay in rwb-decision. |
| CDC-20541 | RWB-P10-E1058-CON | R-28637 |  | PRD AC-P10-003, 004, 008 and 001 give guardrail, fallback, harness and set-up each its own scenario; shared Background kept. FSD part belongs to FSD P10 v3. |
| CDC-20542 | RWB-P10-E1058-INF | R-22203 |  | Section 2.2 and the interface table state REST base /api/recovery/agent/v1 at product level; exact paths left to API Specification v4. |
| CDC-20543 | RWB-P10-E1058-CON | R-28637 |  | PRD AC-P10-003, 004, 008 and 001 give each of the four features its own scenario; shared Background kept. |
| CDC-20544 | RWB-P10-E1058-APP | R-28638 |  | Section 10 maps all sixteen FEAT-AGT features to waves 1 to 4 and carries the copied dates marked tentative. |
| CDC-20545 | RWB-P10-E1058-CON | R-28637 |  | PRD scenarios AC-P10-001 to 004 and 008 hold one criterion per feature; shared Background already separate. |
| CDC-20546 | RWB-P10-E1058-INF | R-22203 |  | PRD carries base /api/recovery/agent/v1 in section 2.3 and the integration table; no path names needed here. |
| CDC-20553 | RWB-P10-E1058-OPS | R-28637 |  | PRD P10 has per-feature scenarios: AC-P10-003 guardrail, AC-P10-004 fallback, AC-P10-008 evaluation scores, AC-P10-001 run row and event. No edit. |
| CDC-20554 | RWB-P10-E1062-CON | R-22213 |  | R-DEV rule set belongs to the S8 FSD (rwb-deviation); PRD P10 holds no R-DEV rules. No edit here. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03715 | RWB-P10-E1058-APP | DOR-RWB-P10-E1058-APP-12 | 12.7, 16, 18 | Boundary test TC-E1-058-17 and test rows TC-E1-058-17 to TC-E1-058-26 added |
| CDC-03723 | RWB-P10-E1058-APP | CG-ALL-2505 | 18 | Align the test case lists for the three differing requirements between section 18 of RWB-P10-E1058-APP and RTM v7 in their next versions. |
| CDC-03749 | RWB-P10-E1058-CON | CG-ALL-2527 | 18 | Align the test lists for REQ-ACA-010, REQ-ACA-005 and the third differing requirement with section 18 of RWB-P10-E1058-CON in the next RTM version. |
| CDC-03764 | RWB-P10-E1058-INF | CG-ALL-2532 | 18 | Align the test lists for REQ-ACA-010, REQ-ACA-005 and the third differing requirement with section 18 of RWB-P10-E1058-INF. |
| CDC-03781 | RWB-P10-E1058-OPS | CG-ALL-2540 | 18 | Align the test lists for REQ-ACA-010, REQ-ACA-005 and the third requirement in the evidence with section 18 of this story. |
| CDC-03796 | RWB-P10-E1059-APP | DOR-RWB-P10-E1059-APP-12 Test cases: Partial | 12.7, 16, 18 | Test rows added in section 16 |
| CDC-03798 | RWB-P10-E1059-APP | CG-ALL-2556 | 18 | In the next RTM version, align the test lists of REQ-ACA-005 and the second differing requirement with section 18 of RWB-P10-E1059-APP. |
| CDC-03819 | RWB-P10-E1059-CON | CG-ALL-2580 | 18 | Align the REQ-ACA-005 test list and the second requirement's test list with section 18 of RWB-P10-E1059-CON (TC-P10-E1059-CON-03, -04 for REQ-ACA-005). |
| CDC-03825 | RWB-P10-E1060-APP | CG-ALL-2587 | 18 | Align the REQ-DCM-005 and REQ-DCM-006 test lists with section 18 of RWB-P10-E1060-APP in the RTM's next version. |
| CDC-03833 | RWB-P10-E1061-APP | CG-ALL-2592 | 18 | Align the REQ-DRI-010 test list to RWB-P10-E1061-APP section 18 (TC-E1-061-01 to TC-E1-061-06) in the next RTM version. |
| CDC-03842 | RWB-P10-E1061-CON | CG-ALL-2601 | 18 | Align the test list of REQ-DRI-010 and of the second differing requirement to RWB-P10-E1061-CON section 18 (REQ-DRI-010: TC-P10-E1061-CON-02, TC-P10-E1061-CON-05). |
| CDC-03871 | RWB-P10-E1062-APP | CG-ALL-2622 | 18 | Existing section 18 traces are kept and only the new test case IDs are added; RTM v7 is aligned in its next version. |
| CDC-03902 | RWB-P10-E1062-CON | CG-ALL-2643 | 18 | Align its test IDs for REQ-DVH-001, REQ-DVH-003 and REQ-DVH-007 to the section 18 lists of this story. |
| CDC-03917 | RWB-P10-E1063-APP | DOR-RWB-P10-E1063-APP-12 | 18 | REQ-DRI-009 test cases: add TC-E1-063-04, TC-E1-063-05, TC-E1-063-06, TC-E1-063-07, TC-E1-063-08 to match section 18 of RWB-P10-E1063-APP. |
| CDC-03924 | RWB-P10-E1063-APP | CG-ALL-2652 | 18 | Set the REQ-DRI-009 trace to TC-E1-063-01 to TC-E1-063-08 as section 18 lists, and remove TC-E1-014-01 to 03 and TC-E2-031-03 from that requirement. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03687 | RWB-P10-AD020-APP | CG-ALL-2483 | 16 | Add rows TC-AD-020-05 to TC-AD-020-13 with Given, When and Then copied from the criteria AC3 to AC11 they cover. |
| CDC-03688 | RWB-P10-AD020-APP | DOR-RWB-P10-AD020-APP-12 | 16 | Add rows TC-AD-020-05 to TC-AD-020-14 under the same IDs as §16 of this story. |
| CDC-03698 | RWB-P10-AD020-CON | DOR-RWB-P10-AD020-CON-12 | 16 | Register TC-P10-AD020-CON-01 to -08 in Test Cases v8 |
| CDC-03699 | RWB-P10-AD020-CON | CG-ALL-2488 | 16 | Add rows TC-P10-AD020-CON-01 to TC-P10-AD020-CON-07 with Given, When and Then copied from AC1 to AC7 of section 7. |
| CDC-03742 | RWB-P10-E1058-CON | DOR-RWB-P10-E1058-CON-12 | 12.7, 16, 18 | Add TC-P10-E1058-CON-01 to -07 as listed in section 16 of RWB-P10-E1058-CON; align the section 18 test lists with RTM v7. |
| CDC-03748 | RWB-P10-E1058-CON | CG-ALL-2526 | 16 | Add a Story test cases row for each of TC-P10-E1058-CON-01 to TC-P10-E1058-CON-06 with Given, When and Then copied from the criterion each covers. |
| CDC-03763 | RWB-P10-E1058-INF | CG-ALL-2531 | 16 | Add rows for TC-P10-E1058-INF-01 to TC-P10-E1058-INF-08 to the Story test cases table, with Given, When and Then copied from the criterion each covers. |
| CDC-03780 | RWB-P10-E1058-OPS | CG-ALL-2539 | 16 | Add rows for TC-P10-E1058-OPS-01 to TC-P10-E1058-OPS-09, with Given, When and Then copied from the criterion each row covers. |
| CDC-03818 | RWB-P10-E1059-CON | CG-ALL-2579 | 16 | Story section 16 already lists the ten test cases TC-01 to TC-10. The missing rows are in Test Cases v8, which is another document. |
| CDC-03824 | RWB-P10-E1060-APP | CG-ALL-2586 | 16 | In the next version, add rows TC-E1-060-10 to TC-E1-060-15 with Given, When and Then copied from the criteria they cover. |
| CDC-03841 | RWB-P10-E1061-CON | CG-ALL-2600 | 16 | Add rows TC-P10-E1061-CON-01 to TC-P10-E1061-CON-06 in the next version, with Given, When and Then copied from their criteria. |
| CDC-03890 | RWB-P10-E1062-CON | DOR-RWB-P10-E1062-CON-12 | 12.7, 16, 18 | Register TC-P10-E1062-CON-01 to -09 in Test Cases v8 and align the section 18 test lists with RTM v7. |
| CDC-03901 | RWB-P10-E1062-CON | CG-ALL-2642 | 16 | Add rows TC-P10-E1062-CON-01 to TC-P10-E1062-CON-08 with Given, When and Then copied from the criteria they cover. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03693 | RWB-P10-AD020-CON | CG-ALL-2487 | 12.2 | Publish POST /api/recovery/access/v1/authorise, consumed in section 12.2; no story edit |
| CDC-03695 | RWB-P10-AD020-CON | DOR-RWB-P10-AD020-CON-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise, consumed in section 12.2; no story edit |
| CDC-03702 | RWB-P10-E1058-APP | CG-ALL-2493 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story; this story keeps the row unchanged |
| CDC-03703 | RWB-P10-E1058-APP | CG-ALL-2494 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies through the provider CON story; this story keeps the row unchanged |
| CDC-03730 | RWB-P10-E1058-CON | CG-ALL-2514 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer uses a published operation. |
| CDC-03731 | RWB-P10-E1058-CON | CG-ALL-2515 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies through the provider's CON story, or the consumer uses a published operation. |
| CDC-03771 | RWB-P10-E1058-OPS | CG-ALL-2536 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or consume a published operation instead. |
| CDC-03772 | RWB-P10-E1058-OPS | CG-ALL-2537 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies through the provider's CON story, or consume a published operation instead. |
| CDC-03783 | RWB-P10-E1059-APP | CG-ALL-2547 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider's CON story. |
| CDC-03804 | RWB-P10-E1059-CON | CG-ALL-2570 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-03821 | RWB-P10-E1060-APP | CG-ALL-2584 | 12.2 | Publish POST /api/recovery/access/v1/authorise in paths via the rwb-access CON story, or this story consumes a published operation. |
| CDC-03822 | RWB-P10-E1060-APP | DOR-RWB-P10-E1060-APP-8 |  | P1 is a provider path gap. P2 is not applied here because its message IDs are not in the sources. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03801 | RWB-P10-E1059-CON | CG-ALL-2567 | 12.1 | Publish POST /api/recovery/agent/v1/agent-runs in rwb-agent.yaml through the CON story. |
| CDC-03802 | RWB-P10-E1059-CON | CG-ALL-2568 | 12.1 | Publish GET /api/recovery/agent/v1/agent-runs/{runId} in rwb-agent.yaml through the CON story. |
| CDC-03877 | RWB-P10-E1062-CON | CG-ALL-2626 | 12.1 | Publish POST /api/recovery/agent/v1/agent-runs in rwb-agent.yaml through the CON story; the story already documents the operation in section 12.1. |
| CDC-03878 | RWB-P10-E1062-CON | CG-ALL-2627 | 12.1 | Publish GET /api/recovery/agent/v1/agent-runs/{runId} in rwb-agent.yaml through the CON story; the story already documents the operation in section 12.1. |
| CDC-20640 | RWB-P10-E1058-APP | R-22208 |  | Completion event name and member types are decided at contract review. Event contract is in asyncapi/rwb-agent.asyncapi.yaml, not this document (GAP-0613). |
| CDC-20641 | RWB-P10-E1059-CON | R-00451 |  | POST /agent-runs is not in rwb-agent.yaml. Request and response schema not specified in the source documents (CG-ALL-2567). |
| CDC-20642 | RWB-P10-E1059-CON | R-00452 |  | GET /agent-runs/{runId} is not in rwb-agent.yaml. Parameters and response schema not specified in the source documents (CG-ALL-2568). |
| CDC-20643 | RWB-P10-E1059-CON | R-04587 |  | Unpublished paths for rwb-case and rwb-access belong to those yamls. Agent-run paths here lack schema in the source documents (DOR-RWB-P10-E1059-CON-8). |
| CDC-20644 | RWB-P10-E1062-APP | R-00457 |  | POST /agent-runs is not in rwb-agent.yaml. Request and response schema not specified in the source documents (CG-ALL-2606). |
| CDC-20645 | RWB-P10-E1062-APP | R-00458 |  | GET /agent-runs/{runId} is not in rwb-agent.yaml. Parameters and response schema not specified in the source documents (CG-ALL-2607). |
| CDC-20646 | RWB-P10-E1062-APP | R-04608 |  | Agent-run paths lack schema in the source documents. rwb-deviation and rwb-document paths belong to those yamls (DOR-RWB-P10-E1062-APP-8). |
| CDC-20647 | RWB-P10-E1062-CON | R-00464 |  | POST /agent-runs is not in rwb-agent.yaml. Request and response schema not specified in the source documents; story 12.1 was not read (CG-ALL-2626). |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03684 | RWB-P10-AD020-APP | DOR-RWB-P10-AD020-APP-8 | 12.3, 12.5 | Add activities ResolveStepLevel and RunAgentStep on task queue rwb-agent, or the story uses catalogued names. |
| CDC-03685 | RWB-P10-AD020-APP | CG-ALL-2481 | 12.5 | Add activity ResolveStepLevel (task queue rwb-agent) to the Activities sheet. |
| CDC-03686 | RWB-P10-AD020-APP | CG-ALL-2482 | 12.5 | Add activity RunAgentStep (task queue rwb-agent) to the Activities sheet. |
| CDC-03791 | RWB-P10-E1059-APP | CG-ALL-2550 | 12.5 | Add activity BuildIntakeInputs to the Activities sheet or name a catalogued activity. |
| CDC-03792 | RWB-P10-E1059-APP | CG-ALL-2551 | 12.5 | Add activity CallModelGateway to the Activities sheet or name a catalogued activity. |
| CDC-03793 | RWB-P10-E1059-APP | CG-ALL-2552 | 12.5 | Add activity CheckGuardrail to the Activities sheet or name a catalogued activity. |
| CDC-03794 | RWB-P10-E1059-APP | CG-ALL-2553 | 12.5 | Add activity RecordShadowRun to the Activities sheet or name a catalogued activity. |
| CDC-03811 | RWB-P10-E1059-CON | CG-ALL-2574 | 12.5 | Add activity BuildIntakeInputs on task queue rwb-agent, or name a catalogued activity in its place. |
| CDC-03812 | RWB-P10-E1059-CON | CG-ALL-2575 | 12.5 | Add activity CallModelGateway on task queue rwb-agent, or name a catalogued activity in its place. |
| CDC-03813 | RWB-P10-E1059-CON | CG-ALL-2576 | 12.5 | Add activity CheckGuardrail on task queue rwb-agent, or name a catalogued activity in its place. |
| CDC-03814 | RWB-P10-E1059-CON | CG-ALL-2577 | 12.5 | Add activity RecordShadowRun on task queue rwb-agent, or name a catalogued activity in its place. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03696 | RWB-P10-AD020-CON | DOR-RWB-P10-AD020-CON-1 | 1 | Add 'tech lead of rwb-agent' as a role code or role name, or give the code to use in section 1 |
| CDC-03741 | RWB-P10-E1058-CON | DOR-RWB-P10-E1058-CON-1 | 1 | Add the role named in section 1 of RWB-P10-E1058-CON (tech lead of rwb-agent) as a role code or role name. |
| CDC-03756 | RWB-P10-E1058-INF | DOR-RWB-P10-E1058-INF-1 | 1 | Add the infrastructure engineer role with its role code, or confirm the existing role code to use in section 1. |
| CDC-03777 | RWB-P10-E1058-OPS | DOR-RWB-P10-E1058-OPS-1 | 1 | Confirm or add the role 'platform engineer' (name or role code) so that section 1 of RWB-P10-E1058-OPS uses a listed role. |
| CDC-03815 | RWB-P10-E1059-CON | DOR-RWB-P10-E1059-CON-1 | 1 | Add the role code and role name of the rwb-agent contract owner that §1 of RWB-P10-E1059-CON calls 'tech lead', so §1 can cite the code instead of the plain title. |
| CDC-03837 | RWB-P10-E1061-CON | DOR-RWB-P10-E1061-CON-1 | 1 | Add 'tech lead' as a role name, or name the role code this story's persona maps to |
| CDC-03876 | RWB-P10-E1062-APP | GAP-2329 |  | Set the default scope of SY-AGENT (the agent service identity) to ALL in the matrix version in force, and state the rule for every non-human actor role. |
| CDC-03889 | RWB-P10-E1062-CON | DOR-RWB-P10-E1062-CON-1 | 1 | Add 'tech lead' as a role code or role name, or map the story role to an existing one. |
| CDC-03907 | RWB-P10-E1062-CON | GAP-2329 |  | Set the service identity of the agent platform to scope ALL in the matrix version in force and state the rule for every non-human actor role |

### Epic design record (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03694 | RWB-P10-AD020-CON | DOR-RWB-P10-AD020-CON-14 | n/a | Record the signed epic design sign-off for RWB-SVC-P10 under EP08 |
| CDC-03752 | RWB-P10-E1058-INF | DOR-RWB-P10-E1058-INF-14 | find it | Record the signed epic design sign-off for EP01 in the epic design record. |
| CDC-03773 | RWB-P10-E1058-OPS | DOR-RWB-P10-E1058-OPS-14 |  | record the signed epic design of RWB-P10-E1058-OPS and its sign-off date; no story text or source excerpt holds a signed epic design |
| CDC-03805 | RWB-P10-E1059-CON | DOR-RWB-P10-E1059-CON-14 | header | Confirm the signed epic design sign-off and record it in the epic design record. |
| CDC-03826 | RWB-P10-E1061-APP | DOR-RWB-P10-E1061-APP-14 |  | Record the signed sign-off of the epic design that covers RWB-P10-E1061-APP. |
| CDC-03835 | RWB-P10-E1061-CON | DOR-RWB-P10-E1061-CON-14 | header | Record the signed epic design sign-off for EP01 and RWB-SVC-P10 so DOR item 14 can pass |
| CDC-03849 | RWB-P10-E1062-APP | DOR-RWB-P10-E1062-APP-14 | header | Record the signed epic design sign-off for EP01 so the story can confirm it. |
| CDC-03909 | RWB-P10-E1063-APP | DOR-RWB-P10-E1063-APP-14 | none | Record the signed epic design sign-off for this story |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03700 | RWB-P10-E1058-APP | CG-ALL-2491 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{key} through the provider CON story; this story keeps the row unchanged |
| CDC-03701 | RWB-P10-E1058-APP | CG-ALL-2492 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/{lovCode} through the provider CON story; this story keeps the row unchanged |
| CDC-03728 | RWB-P10-E1058-CON | CG-ALL-2512 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{key} through the provider's CON story, or the consumer uses a published operation. |
| CDC-03729 | RWB-P10-E1058-CON | CG-ALL-2513 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/{lovCode} through the provider's CON story, or the consumer uses a published operation. |
| CDC-03769 | RWB-P10-E1058-OPS | CG-ALL-2534 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{key} through the provider's CON story, or consume a published operation instead. |
| CDC-03770 | RWB-P10-E1058-OPS | CG-ALL-2535 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/{lovCode} through the provider's CON story, or consume a published operation instead. |
| CDC-03803 | RWB-P10-E1059-CON | CG-ALL-2569 | 12.2 | Split the /accounts and /parties paths into one row each; paths unchanged |

### RWB-P10-E1058-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03704 | RWB-P10-E1058-APP | DOR-RWB-P10-E1058-APP-21 | n/a | Move the contract story build status from Not started to Done |
| CDC-03705 | RWB-P10-E1058-APP | DOR-RWB-P10-E1058-APP-22 | n/a | Publish a contract fake library version and record it as published |
| CDC-03716 | RWB-P10-E1058-APP | GAP-0607 | find it | Declare EV-28 as the only event member; leave report and metric element types to owner review; keep the legacy sample key; leave agent_run_daily to the monitor story; name the route as a one-hop pass-through. |
| CDC-03753 | RWB-P10-E1058-INF | DOR-RWB-P10-E1058-INF-21 | header | Complete the contract story build to Done and publish the contract; this story now names it as a contract dependency. |
| CDC-03754 | RWB-P10-E1058-INF | DOR-RWB-P10-E1058-INF-22 | header | Publish the contract fake library version and record it as published. |
| CDC-03762 | RWB-P10-E1058-INF | GAP-0613 | find it | Agree the open contract elements at the contract review (no evaluation-completed event declared; promotion and watch member names and types; report member types; route path) and rewrite the document and fakes. |
| CDC-03774 | RWB-P10-E1058-OPS | DOR-RWB-P10-E1058-OPS-21 | header | Set build status to Done once the contract is published. |

### RWB-P10-E1061-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03743 | RWB-P10-E1058-CON | GAP-0613 | 12 | Agree at contract review: no evaluation-completed event, nested types of promotion_conditions and watch_measures, report member types, route path. Update contract and fakes. |
| CDC-03827 | RWB-P10-E1061-APP | DOR-RWB-P10-E1061-APP-21 |  | Move build status from Not started to Done. |
| CDC-03828 | RWB-P10-E1061-APP | DOR-RWB-P10-E1061-APP-22 |  | Publish a contract fake library version and record its version number. |
| CDC-03831 | RWB-P10-E1061-APP | GAP-0613 |  | Declare no evaluation-completed event; keep rwb.agent.AgentRunCompleted.v1 (EV-28) as the only business event on rwb.agent.events.v1; agree the promotion and report member names and types with their owners; route path /api/recovery/agent/v1; no behaviour change. |
| CDC-03832 | RWB-P10-E1061-APP | GAP-0612 | 3, 10, 15 | Login is stated as the rwb-agent login (DP-02) per ASM-0869. Minimum sample and lists come via rwb-case contracts; no promotion flag is named. The exact gateway-bff route path stays Not specified and belongs to the contract story. Legacy disposition stays Moved (no impact). |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03820 | RWB-P10-E1059-CON | GAP-0611 | 8 | Publish the start operation POST /agent-runs next to GET /agent-runs/{id}; agree the four consumed paths with the rwb-case and rwb-source-data owners; fix the member types; name the edge route. |
| CDC-03865 | RWB-P10-E1062-APP | GAP-2326 | find it | Add the POST /authorise operation with the agent-authority part (role, scope, delegation) and its element names at the next revision, inside RWB-P4-E1037-CON. |
| CDC-03868 | RWB-P10-E1062-APP | GAP-2327 | find it | Publish CALLER_KIND, RIGHT_NOT_HELD and SCOPE_NOT_ALL as the refusal reasons of the authorise operation with their statuses, and confirm them for every caller service. |
| CDC-03895 | RWB-P10-E1062-CON | GAP-2326 |  | Add a POST /authorise row with the agent-authority part. Confirm its element names at the wave 1 contract review with the P10 owner. |
| CDC-03897 | RWB-P10-E1062-CON | GAP-2327 |  | Fix CALLER_KIND, RIGHT_NOT_HELD and SCOPE_NOT_ALL as refusal reasons with their statuses. Confirm them once for every caller service. |

### RWB-P10-E1062-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03850 | RWB-P10-E1062-APP | DOR-RWB-P10-E1062-APP-21 | header | Complete the build of RWB-P10-E1062-CON and publish its contract; build status must reach Done. |
| CDC-03851 | RWB-P10-E1062-APP | DOR-RWB-P10-E1062-APP-22 | header | No fake library is published; the story records the version as Not specified until the contract story publishes it. |
| CDC-03870 | RWB-P10-E1062-APP | GAP-0614 | 3 | Add the run-start operation on /api/recovery/agent/v1 with its request members and refusal codes; name the case, parameter, deviation, ledger and document read paths with a 2 s budget each; publish the run and proposal events on rwb.agent.events.v1; publish the screening feature flag and the failed tool-call status. |
| CDC-03873 | RWB-P10-E1062-APP | GAP-1047 | 3 | State that the agent's case read maps to API-P5-002 and its document read to API-P5-003, with API-P5-009 for an extracted-field filter; publish the tool call field names in the rwb-document specifications. |
| CDC-03874 | RWB-P10-E1062-APP | GAP-1048 | 3 | Fix the DocumentStored payload as documentId, caseId, documentType, source and storedAt, and state the idempotency key as the outbox event ID. |

### RWB-P10-AD020-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03682 | RWB-P10-AD020-APP | DOR-RWB-P10-AD020-APP-21 | header | Build status Done (contract published) before this story starts. |
| CDC-03683 | RWB-P10-AD020-APP | DOR-RWB-P10-AD020-APP-22 | header | Publish the contract fake and record its library version; the version is not in the source documents. |
| CDC-03691 | RWB-P10-AD020-APP | GAP-0641 | 3 | Fix the approval-gated version-change contract on the agreed readings: approval_ref as the backward-compatible approval reference holding the rwb-decision approval id (ASM-5); ApprovalDetail carrying approval id, LOV-APPROVAL-STATUS status, decision code and approved autonomy level under agreed names (ASM-11); 409 and 404 meanings with repeat under the same Idempotency-Key (ASM-9); authorise caller and repeat-call test. |
| CDC-03692 | RWB-P10-AD020-APP | GAP-0637 | 3 | Fix the three /admin/agent-configs operations as the contract, record the Arch v5 slide 16 label as a summary, name the configuration version in the rule-version element of the record, fix kind as POLICY and PROMPT, take approval instant from updated_at and approver role from rwb-access, accept only LOV-AUTONOMY values, and settle file columns and messages at wave 2 freeze. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03734 | RWB-P10-E1058-CON | CG-ALL-2516 | 12.1 | Add message IDs for 401 no session, 404 unknown version, evaluation, run or case, and 503 store or consumed contract unavailable, or confirm the platform code alone. |
| CDC-03823 | RWB-P10-E1060-APP | CG-ALL-2585 | 12.1, 14 | Add a message for 401 no session. Confirm MSG-GEN-006 wording (queued and retried) for a synchronous 503, or add a message without it. |
| CDC-03836 | RWB-P10-E1061-CON | CG-ALL-2599 | 14 | Add a message ID for 'The version is already approved'; section 14 then cites it |
| CDC-03839 | RWB-P10-E1061-CON | DOR-RWB-P10-E1061-CON-9 | 14 | Business analyst to confirm the standard's meaning of MSG-GEN-004 or give 'The version is already approved' its own message ID. MSG-P10-008 text now copied from the standard. |

### RWB-P10-E1063-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03744 | RWB-P10-E1058-CON | GAP-0617 | 12 | Declare page size and cursor, AgentMetric members, held-date status, Schedule AgentRunDailyRollup, route and notification operation per the GAP-0617 proposed fix. |
| CDC-03910 | RWB-P10-E1063-APP | DOR-RWB-P10-E1063-APP-21 | none | Set the contract story build status to Done with the contract published |
| CDC-03911 | RWB-P10-E1063-APP | DOR-RWB-P10-E1063-APP-22 | none | Record the published contract fake library version |
| CDC-03919 | RWB-P10-E1063-APP | GAP-0617 | 12 | Declare page size and cursor, AgentRunDailyRollup member types, held-date status members and answer code, and the notification operation in the contract; five query parameters on /api/recovery/agent/v1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03808 | RWB-P10-E1059-CON | CG-ALL-2564 | 2 | Add read_documents as a dictionary name, or record it as the rwb-document read object in the owning document (nearest name: document). |
| CDC-03809 | RWB-P10-E1059-CON | CG-ALL-2565 | 2, 12.2 | Add read_valuations as a dictionary name, or record it as the rwb-source-data tool read object in the owning document (nearest name: valuation). |
| CDC-03810 | RWB-P10-E1059-CON | CG-ALL-2566 | 2, 12.2 | Add read_contact_points as a dictionary name, or record it as the rwb-source-data tool read object in the owning document (nearest name: contact_point_ext). |
| CDC-03913 | RWB-P10-E1063-APP | CG-ALL-2646 | 2, 7, 11, 12.7, 13 | Record agent_run_daily as a retired legacy table with no target (DP-17) so its references resolve |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03847 | RWB-P10-E1062-APP | CG-ALL-2612 | 12.3 | Add rwb.agent.AgentRunStarted.v1 on rwb.agent.events.v1 with owner P10. |
| CDC-03848 | RWB-P10-E1062-APP | CG-ALL-2614 | 12.3 | Add rwb.agent.ScreeningProposalRaised.v1 on rwb.agent.events.v1 with owner P10. |
| CDC-03880 | RWB-P10-E1062-CON | CG-ALL-2632 | 12.3 | Add rwb.agent.AgentRunStarted.v1 to the Events sheet on topic rwb.agent.events.v1, owner P10. |
| CDC-03881 | RWB-P10-E1062-CON | CG-ALL-2634 | 12.3 | Add rwb.agent.ScreeningProposalRaised.v1 to the Events sheet on topic rwb.agent.events.v1, owner P10. |

### RWB-P10-E1058-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03690 | RWB-P10-AD020-APP | GAP-0640 | 13 | If an approval_ref column replaces the jsonb member, add it to agent_policy with its number from the rwb-agent Flyway sequence at build time. |
| CDC-03732 | RWB-P10-E1058-CON | DOR-RWB-P10-E1058-CON-5 | 9 | Carry ECHO in the closed list LOV-AGENT-RUN; this key names no run state and §9 keeps its six transitions. |
| CDC-03765 | RWB-P10-E1058-INF | GAP-0610 | header | Agree the login and gateway-bff route names; keep AC5 and TC-E1-059-05 with RWB-ITG-E1059-ITG; add RWB-P5-E1053-CON when published; agree who serves sample and evaluation operations. |

### RWB-P10-TE013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03721 | RWB-P10-E1058-APP | GAP-2187 | 3 | Publish the run-submit and run-to-record link operations with their members in the rwb-agent contract baseline; name the rwb-agent login; record the 60 s budget as the single DP-11 exception in ADR-020. |
| CDC-03722 | RWB-P10-E1058-APP | GAP-0619 | 3 | Fix POST /api/recovery/agent/v1/agent-steps and PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record with legacy members unchanged; 60 s step budget as the single 2 s exception. |
| CDC-03746 | RWB-P10-E1058-CON | GAP-2188 | 12 | Fix member names and JSON spelling; settle types, refusal set and record reference with rwb-decision and rwb-case; name the route with RWB-PLT-N001-CON. |

### OTHER:FSD P10 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03755 | RWB-P10-E1058-INF | GAP-1518 | 7 | Remove direct ACE integration from agent platform integration points (A2.1.2, A2.10.2); route case facts through rwb-source-data and document fields through rwb-document. |
| CDC-03768 | RWB-P10-E1058-INF | GAP-1533 | find it | The story already states Wave 1 from EP01 with the release date marked tentative. The missing wave and release for the sixteen agent features must be added in the FSD. |

### RWB-P10-E1059-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03784 | RWB-P10-E1059-APP | DOR-RWB-P10-E1059-APP-21 | header | Set the build status to Done so the contract is published (currently Not started). |
| CDC-03785 | RWB-P10-E1059-APP | DOR-RWB-P10-E1059-APP-22 | none | Publish a contract fake library version and record it as published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03787 | RWB-P10-E1059-APP | CG-ALL-2543 | 12.2 | Record the read_accounts tool read as a named operation of the rwb-source-data contract with its path. |
| CDC-03788 | RWB-P10-E1059-APP | CG-ALL-2544 | 12.2 | Record the read_valuations tool read as a named operation of the rwb-source-data contract with its path. |

### RWB-P10-E1059-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03816 | RWB-P10-E1059-CON | DOR-RWB-P10-E1059-CON-10 | find it | State the empty, loading, error and no-access states of SCR-46 in the app story. |
| CDC-03830 | RWB-P10-E1061-APP | DOR-RWB-P10-E1061-APP-17 |  | Move build status to Done before RWB-P10-E1061-APP starts. |

### RWB-P10-E1062-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03844 | RWB-P10-E1062-APP | CG-ALL-2606 | 12.1 | Publish POST /api/recovery/agent/v1/agent-runs in rwb-agent.yaml. |
| CDC-03845 | RWB-P10-E1062-APP | CG-ALL-2607 | 12.1 | Publish GET /api/recovery/agent/v1/agent-runs/{runId} in rwb-agent.yaml. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03869 | RWB-P10-E1062-APP | GAP-3085 | 3 | Publish the deviation read as a service operation with a catalogue row; publish the agent-policy read operation name and fields; bind the shadow refusal to one status; publish codes and owner roles of R-DEV-05 and R-DEV-06 with package version; set the answer limit and the test level of the ten legacy cases. |
| CDC-03898 | RWB-P10-E1062-CON | GAP-3085 |  | Publish the deviation estate read and the agent-policy read with operation names, the R-DEV-05 and R-DEV-06 codes and owner roles, the answer limit and the test level split. |

### OTHER:FSD S8 document control and inherited history (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03872 | RWB-P10-E1062-APP | GAP-1834 |  | Add the v1 and v2 change-note rows, or record them as Not specified in the source documents (GAP-1834). |
| CDC-03903 | RWB-P10-E1062-CON | GAP-1834 | find it | Add the v1 and v2 change-note rows, or record them as Not specified in the source documents (GAP-1834). |

### OTHER:rwb-access masking contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03875 | RWB-P10-E1062-APP | GAP-1049 | 3 | Publish the mask format and the per-role personal field list; section 3 now states SY-AGENT holds Documents R with every personal field masked. |
| CDC-03906 | RWB-P10-E1062-CON | GAP-1049 | 3 | Publish the mask format and the per-role list of personal document fields for SY-AGENT. |

### RWB-P6-E1063-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03921 | RWB-P10-E1063-APP | GAP-1209 | 11 | Seed template code, channel, notice type and retry window as P6 parameter and reference rows; publish request and answer fields; declare the guard right per ASM-B-P6-05-E1063-4. |
| CDC-03922 | RWB-P10-E1063-APP | GAP-1210 | 11 | Drop agent_run_daily, the lake copy, the count check and the Power BI page from the rwb-comms slice; keep the P9 measures read; record the dashboard as P9 and P10 work per ASM-B-P6-05-E1063-5. |

### RWB-P10-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03689 | RWB-P10-AD020-APP | DOR-RWB-P10-AD020-APP-17 | section 17 | No story edit made: the dependencies are named and the start gate is in the header; the gate story's build status belongs to RWB-P10-E1063-APP. |

### OTHER:SCR-46 screen specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03697 | RWB-P10-AD020-CON | DOR-RWB-P10-AD020-CON-10 | n/a | Specify empty, loading, error and no access states of SCR-46 |

### OTHER:rwb-case API yaml; OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03706 | RWB-P10-E1058-APP | DOR-RWB-P10-E1058-APP-8 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{key}, GET /api/recovery/case/v1/reference-data/{lovCode}, POST /api/recovery/access/v1/authorise, GET /api/recovery/access/v1/masking-policies and the 10 further detcheck paths. |

### OTHER:Functional Specification P10 v3 (A2.1.2; OTHER:A2.10.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03707 | RWB-P10-E1058-APP | GAP-1518 | 12.2 | Name the rwb-source-data tool contract for case facts and rwb-document for extracted fields in the integration points; state no ACE read by rwb-agent and no rwb_agent grant on the recovery schema. |

### RWB-P10-E1058-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03717 | RWB-P10-E1058-APP | GAP-0608 | find it | Record reviewed per-environment values for the INT-23 path, Key Vault entries, service login, topic partitions and retention, worker concurrency, budgets and alarms; create no table or bucket. |

### OTHER:Agent evaluation contract (rwb-agent contract baseline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03720 | RWB-P10-E1058-APP | GAP-0613 | find it | Agree the completion event name, the nested promotion and watch member types, the report member types and the route path at contract review; update the contract and fakes. |

### RWB-P10-E1058-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03724 | RWB-P10-E1058-APP | GAP-0609 | 13 | Keep replica, resource, probe, threshold and window values as reviewed per-environment values; admin operations on a second colour behind the gateway-bff route; flags read from the platform library. |

### OTHER:rwb-case and rwb-access published contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03733 | RWB-P10-E1058-CON | DOR-RWB-P10-E1058-CON-8 | 12.1 | Publish the consumed paths named in the item: case parameters/{key} and reference-data/{lovCode}; access authorise and masking-policies (CG-ALL-2512 to 2515). |

### RWB-P10-E2032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03745 | RWB-P10-E1058-CON | GAP-0634 | 12 | Fix the suggestion operation path and request, record mapping, EV-28 payload, INT-23 request and status mapping, and admin reads and route per GAP-0634. |

### RWB-P10-E8003-APP; OTHER:rwb-source-data contract; OTHER:Epic 8 BRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03747 | RWB-P10-E1058-CON | GAP-0645 | 11 | Add measure, sample floor and threshold policy rows; one GET for v_ace_score; migration number; evaluation-run name; FEAT-AGT-14 requirement row. |

### OTHER:P3 screen specification (SCR-46) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03757 | RWB-P10-E1058-INF | DOR-RWB-P10-E1058-INF-10 | find it | Add empty, loading, error and no access states to SCR-46. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03758 | RWB-P10-E1058-INF | DOR-RWB-P10-E1058-INF-12 | 16, 18 | Section 16 lists nine test cases, including TC-P10-E1058-INF-09 for AC9; the gaps are in Test Cases v8 and RTM v7. |

### OTHER:the app slice story of RWB-E1-058 (INT-23 client, admin reads and masking tests) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03759 | RWB-P10-E1058-INF | GAP-0368 | find it | Prove the platform via P10 admin and run contracts; reach INT-23 via ModelGatewayClient with a deterministic stub; assert masking on the captured request; keep prompt text and model answers out of responses and logs. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03775 | RWB-P10-E1058-OPS | DOR-RWB-P10-E1058-OPS-22 | header | Publish a contract fake library version and record it as published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03776 | RWB-P10-E1058-OPS | DOR-RWB-P10-E1058-OPS-8 | 12.2 | Publish the four operations in CG-ALL-2534 to CG-ALL-2537 (two in rwb-case.yaml, two in rwb-access.yaml). |

### OTHER:Recovery Workbench P3 screen set (SCR-46 owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03778 | RWB-P10-E1058-OPS | DOR-RWB-P10-E1058-OPS-10 | 10 | Add empty, loading, error and no access states for SCR-46. |

### OTHER:RWB-E1-058 application slice (rwb-agent application stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03779 | RWB-P10-E1058-OPS | GAP-0368 | none | Prove the platform through P10 admin and run contracts; reach INT-23 only through ModelGatewayClient with a deterministic stub; assert masking on the captured request; keep prompt text and model answers out of responses and logs. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03786 | RWB-P10-E1059-APP | DOR-RWB-P10-E1059-APP-8 | 12.5 | EV-28: align payload with CON story's 12 members. AgentRunWorkflow: give ID form and duplicate-start policy; add BuildIntakeInputs, CallModelGateway, CheckGuardrail, RecordShadowRun. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx; OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03789 | RWB-P10-E1059-APP | CG-ALL-2545 | 11 | read_contact_points is a tool name in the policy, not a dictionary field. The owning document must record it. |

### OTHER:RWB-E2-031 story owning SCR-46 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03795 | RWB-P10-E1059-APP | DOR-RWB-P10-E1059-APP-10 Screens and states: Partial | 15 | SCR-46 is not changed by this story; its empty, loading, error and no access states are marked Not specified and belong to the RWB-E2-031 story. |

### RWB-ITG-E1059-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03797 | RWB-P10-E1059-APP | GAP-0369 | 4, 11, 12 | Prove the CaseCreated to AgentRunCompleted event and AgentRunWorkflow path as set out in ASM-B-ITG-W1-08-E1059-1 to -6. Story sections already route each read through its owner. |

### OTHER:Owning documents of the open login and gateway-bff route points (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03799 | RWB-P10-E1059-APP | GAP-0610 | header | RWB-P5-E1053-CON added to contract dependencies and AC5 stays with RWB-ITG-E1059-ITG. The login and route points stay open under GAP-0610. |

### API:(service not named); OTHER:rwb-case and rwb-source-data contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03800 | RWB-P10-E1059-APP | GAP-0611 | 12.2 | Publish the start operation POST /agent-runs beside GET /agent-runs/{id}; agree the four consumed read paths of rwb-case and rwb-source-data; fix the member types; name the gateway-bff route with the edge owner. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03806 | RWB-P10-E1059-CON | DOR-RWB-P10-E1059-CON-8 | 12.1 | Publish the unpublished operations named in the detcheck (items 1 to 4 and the seven further paths) in their owners' yaml. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03807 | RWB-P10-E1059-CON | CG-ALL-2563 | 12.2 | Record read_accounts as a tool-read object in the owning document, or use its dictionary name. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03817 | RWB-P10-E1059-CON | DOR-RWB-P10-E1059-CON-11 | find it | Reconcile the personal-data class of the fields detcheck flags with the story's statement that the intake answer carries no personal field; name the flagged field and its class. |

### OTHER:Recovery Workbench P3 screen SCR-46 (rwb-case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03829 | RWB-P10-E1061-APP | DOR-RWB-P10-E1061-APP-10 |  | Add empty, loading, error and no access states to SCR-46. |

### OTHER:Recovery Workbench P3 screen specification; OTHER:SCR-46 (rwb-case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03834 | RWB-P10-E1061-APP | CG-ALL-2595 | 15 | States of SCR-46 (empty, loading, error, no access) are recorded as Not specified in section 15 (CG-ALL-2595); the states belong to the P3 screen specification. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03838 | RWB-P10-E1061-CON | DOR-RWB-P10-E1061-CON-12 | 16 | List TC-P10-E1061-CON-01 to -07 in Test Cases v8 and align the section 18 test lists with RTM v7 |

### RWB-P10-E1061-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03840 | RWB-P10-E1061-CON | GAP-2190 | 10 | Apply the GAP-2190 values in the app slice: rwb-agent login (DP-02), D6 as LOV-DECISION value, freshness date source, acceptance event, seven lists, path, flag and topic values. |

### OTHER:rwb-agent Flyway sequence (V10 numbering) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03843 | RWB-P10-E1061-CON | CG-ALL-2603 | 3 | No V0001-form number is assigned (checked Service Template v1/v2, P10 stories). P10 uses V10_nnn; E1059 also uses V10_004, so the whole sequence needs renumbering. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03846 | RWB-P10-E1062-APP | CG-ALL-2609 | 12.2 | Publish GET /api/recovery/document/v1/documents/{documentId}; confirm GET /api/recovery/document/v1/cases/{caseId}/documents is published. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03852 | RWB-P10-E1062-APP | DOR-RWB-P10-E1062-APP-5 | 9 | Remove PR1 from the closed list LOV-DEVIATION, or confirm it is not a deviation value; section 9 keeps its nine transitions. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml; OTHER:rwb-deviation API yaml; OTHER:rwb-document API yaml; OTHER:twelve further detcheck paths (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03853 | RWB-P10-E1062-APP | DOR-RWB-P10-E1062-APP-8 | 12.1 | Publish POST and GET /agent-runs (GET /agent-runs/{runId}) in rwb-agent.yaml; GET /api/recovery/deviation/v1/deviations in rwb-deviation; both rwb-document paths; and the twelve further paths. |

### OTHER:Call-note data product and its owner: Not specified in the source documents (GAP-1822) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03854 | RWB-P10-E1062-APP | GAP-1822 | 4 | Call-note read recorded as Not specified; document read kept as a rwb-document contract dependency |

### OTHER:Business requirements document; OTHER:Epic 1 v5 (section 8.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03861 | RWB-P10-E1062-APP | GAP-1456 | find it | State that a requirement story keeps its business epic wave under Template and Rules R5.6 and that the service starts in its own epic wave; delivery lead confirms the wave per story at build sequencing. |

### OTHER:Functional specification FSD S8 (A2.2.4 to A2.9.4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03862 | RWB-P10-E1062-APP | GAP-1823 | find it | Rewrite each main criterion AC-S8-00n-01 and the repeated alternate and exception rows with the owner, adding step criteria for pause, contact stop, routing and clear. |

### OTHER:Functional specification FSD S8 (feature tables) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03863 | RWB-P10-E1062-APP | GAP-1826 | find it | Name R-DEV-04 and R-DEV-19 to R-DEV-21 in the feature tables; keep the 22-rule package and its version label in rwb-decision. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Tables sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03864 | RWB-P10-E1062-APP | GAP-1819 | find it | Add S8 rows in schema rwb_deviation for the shadow screening run, the score per code, the contact stop, the agent feedback and the breach record, with key fields; no new physical table name. |

### OTHER:TSD P10 v2 (T-A.1 and T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03866 | RWB-P10-E1062-APP | GAP-0615 | 12 | Add the run-start and run-read operations on /api/recovery/agent/v1, declare the three event payloads keyed by case ID with the .dlt route, and publish the consumed owner paths, marking the three unnamed paths with the placeholder. |

### OTHER:Functional specification FSD P10 v3 (A2.8.1 and AC-P10-008-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03867 | RWB-P10-E1062-APP | GAP-1532 | find it | Retitle A2.8.1 to the shadow mode of Epic 1 and read the mode from agent_policy.autonomy_mode; align AC-P10-008-01 with one code path for both modes. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03879 | RWB-P10-E1062-CON | CG-ALL-2630 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{n}/{v} in rwb-decision.yaml through the provider's CON story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03882 | RWB-P10-E1062-CON | DOR-RWB-P10-E1062-CON-8 | 12.1, 12.2 | Deviation and document reads in 12.2 now use published paths; the run operations and the rule-model read must be published by their owners. |

### OTHER:Business Requirements Document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03891 | RWB-P10-E1062-CON | GAP-1456 | find it | State the wave rule in section 8.2: business-epic wave is kept and each story's wave is confirmed at build sequencing. |

### OTHER:FSD S8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03892 | RWB-P10-E1062-CON | GAP-1823 | find it | Groomer and owner rewrite each E2 'Timers shown' and alternate/exception criterion, adding the step criterion for behaviour not asserted. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:S8 deviation rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03894 | RWB-P10-E1062-CON | GAP-1819 |  | Add rows for the shadow screening run, score per code, contact stop, agent feedback and breach record, with key fields. Keep the existing rwb_deviation row. |

### OTHER:FSD P10 v3 A2.8 and A1.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03896 | RWB-P10-E1062-CON | GAP-1532 |  | Align the A2.8 heading and AC-P10-008-01 on one mode read from the policy row. The Epic 1 shadow run is mode SHADOW of the same run. |

### RWB-P10-E1062-APP; RWB-P5-E2025-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03899 | RWB-P10-E1062-CON | GAP-0627 |  | Fix the document, OCR-text, checklist and legal-action reads, the run-start on POST /agent-runs, the parameter keys and the service login in the app slice. |

### OTHER:Legal document agent contract (legacy RWB-E2-030 section 12, rwb-agent) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03900 | RWB-P10-E1062-CON | GAP-0628 | find it | Declare the run operations, pack members, consumed reads, EV-28 scope and route as the proposed fix states. |

### OTHER:rwb-document AsyncAPI and OpenAPI documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03904 | RWB-P10-E1062-CON | GAP-1047 | 3 | Publish the tool call field names of the document read in the AsyncAPI and OpenAPI documents of rwb-document. |

### OTHER:rwb.document.events.v1 AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03905 | RWB-P10-E1062-CON | GAP-1048 | 3 | Fix the DocumentStored payload members and state that the idempotency key is the outbox event ID. |

### OTHER:Story RWB-E2-031 (agent monitoring dashboard v2 app slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03918 | RWB-P10-E1063-APP | GAP-0629 | 12 | Apply the proposed fix: drift step in the v1 Schedule workflow, segment from run row, rwb-decision read with agent-version filter, watch_measures policy values, migration V10_007, range limits as configuration, login rwb-agent (DP-02), route under RWB-PLT-N001-CON, API-P10-009 right. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03920 | RWB-P10-E1063-APP | GAP-2332 | not in this story | Publish the two access-event codes, the entry field list, the page bounds, the read index on rwb_access, the Flyway step and the two parameter codes in the access-log contract. |

### OTHER:FSD P4 v3 (REQ-ACA-006; OTHER:NFR-042); OTHER:TSD P4 v3 (T6.1); OTHER:role matrix load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03923 | RWB-P10-E1063-APP | GAP-2333 | 15 | Keep Reporting R and Rules and parameters R as they are; record Reporting letters for the other roles in the matrix load; replace the lake copy of the access rule with the served read's access entry and correct REQ-ACA-006 and NFR-042 in the next FSD and TSD versions; keep the two access event names; add the five platform contracts to H and the two rwb-case contracts to C in the plan. |

### OTHER:rwb-agent deployment configuration (Platform administrator) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03925 | RWB-P10-E1063-APP | GAP-0618 | 15 | Expose every topology value as a chart value; register schedule AgentRunDailyRollup at 01:30 in namespace rwb-recovery on queue rwb-agent with overlap SKIP; provision rwb.agent.events.v1 with retry and .dlt topics and the publish right of rwb-agent; publish the metric read and baseline reads behind the gateway-bff route; wire the four alerts to MSG-P10-004. |

### OTHER:_work/msr/wp/B-P6-05.md (plan line for this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03926 | RWB-P10-E1063-APP | GAP-1212 | 3 | Add the eight DP-added rows to the plan dependency lists: H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_agent.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20624 | RWB-P10-E1061-CON | R-24547 |  | rwb_agent.sql has no Flyway sequence or V10 name. README section 9 already sets one V0001 baseline per schema (DP-15). Numbering belongs to the migration scripts. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0368 | Model endpoint path, masking route and agent run evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0369 | Stale-input signal, tool-path ownership and shadow-output exposure are not named for the target | P10 agent owner, P1 source data owner, P3 case owner, P4 access owner and P5 document owner | Resolved (directive) |
| GAP-0370 | Document-type reference data owner, extraction field reads and the proposal column are not named for the target | P10 agent owner, P5 document owner and P3 case owner | Resolved (directive) |
| GAP-0371 | Rule-row owner lookup, interaction ledger read and deviation-absence evidence are not named for the target | P10 agent owner, P7 decision owner, P1 source data owner, S8 deviation owner and P4 access owner | Resolved (directive) |
| GAP-0372 | Data lake removed: agent daily read model, reporting read and job rerun owner are not named for the target | P10 agent owner, P9 reporting owner, P1 source data owner, P6 comms owner and P2 integration owner | Resolved (directive) |
| GAP-0606 | The app slice of the agent platform set-up: the service login, the tool reads of the two owners, the parameter keys and lists, the sample key, the migration numbering and the route in front of the admin reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-case, rwb-document and rwb-access | Resolved (directive) |
| GAP-0607 | The contract baseline of the agent platform: the event family beyond EV-28, the member types of the report and the metrics, the inputs reference of the record, the sample key and the assignment of agent_run_daily are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0608 | The infrastructure slice of the agent platform: the INT-23 host, port, certificate and Key Vault entry names, the login name, the partition and retention values, the worker concurrency, the budget measurement points and the alarm thresholds are not specified by any source | SCB IT infrastructure with the ACE platform team and security | Resolved (directive) |
| GAP-0609 | The deployment slice of the agent platform: the replica, resource, probe and rollout values, the alert thresholds, the ordering of the later migrations and the blue-green mechanism of the admin path are not specified by any source | DevOps team with the ACE platform team and the owner of rwb-agent | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0611 | Open points of the intake run contract: the start path, four consumed read paths and the field-level members | Tech lead and platform architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0612 | Intake agent evaluation and L1 proposal in rwb-agent: service login, owner of the minimum sample, split of the evaluation operations, route path, source of the three lists and the promotion flag | Solution architect, with the rwb-case owner and the platform library owner | Resolved (directive) |
| GAP-0613 | Intake agent evaluation contract: name of an evaluation-completed event, nested types of the promotion members, type detail of the report members and the route path in front of the operations | Tech lead of rwb-agent, with the solution architect and the platform library owner | Resolved (directive) |
| GAP-0614 | The screening slice in rwb-agent: the run-start path, the parameter and ledger operation paths, the two added events, the screening feature flag, the boundary status of a failed tool call and the route in front of the reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-deviation, rwb-case, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0615 | The screening contract slice: the run-start path and request members, the member types of the proposal payload, the two added event names and payloads, the consumed paths no source names and the route name are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0616 | Agent monitoring dashboard in rwb-agent: the data lake of the legacy story is removed, and the schedule name, the service login, the route path, the notification operation and the home of the daily aggregate are not specified | Solution architect | Resolved (directive) |
| GAP-0617 | Agent monitoring contract in rwb-agent: the page size and cursor, the member types of the aggregate element, the held-date status members, the Schedule name, the route path and the notification operation are not specified | Solution architect | Resolved (directive) |
| GAP-0618 | Agent monitoring deployment in rwb-agent: the topology, host, SKU, budget, route path, login, feed retention and alert thresholds are not specified | Platform administrator | Resolved (directive) |
| GAP-0619 | The app slice of the agent runtime client: the two operations the legacy Java interface spans, the call type and the budget of a step, the login, the record write and its link, the guardrail check-code list and the route in front of the run read are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-decision, rwb-case and rwb-access | Resolved (directive) |
| GAP-0627 | The app slice of the legal document agent in shadow: the document, OCR-text and checklist operations and members, the legal-action read, the run-start path, the parameter keys, the service login, the route, the BRD section of REQ-DCM-011 and the pack member types are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0628 | The contract baseline of the legal document agent: the OCR-text and checklist operations and member names, the legal-action read, the run-start path, the route, the paging and member types, and the event family beyond EV-28 are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0634 | The TDR offer-suggestion contract slice: the operation path and request members, the record member types, the boundary answer and error mapping, the admin read route and the two-wait exception are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision, rwb-treatment, rwb-case and rwb-source-data | Resolved (directive) |
| GAP-0636 | The decision scope of a version, the autonomy value set, the right of the change, the record rule version, the load file and the approval instant are not fixed by any source | Solution architect with the service owner of rwb-agent and the owners of rwb-decision, rwb-access and rwb-case | Resolved (directive) |
| GAP-0637 | The operation path of a configuration change, the record payload members, the approval instant, the kind value set and the state mapping are not fixed by one source | Solution architect with the service owner of rwb-agent and the owners of rwb-decision and rwb-access | Resolved (directive) |
| GAP-0638 | RWB-AD-020 in rwb-agent: the step scope of a policy version, the L2 value, the approval reference column, the take-effect rule, the route agent code, the P1 fact read, the response field names, the record members, the no-version case, the login and the requirement row are not specified | Solution architect | Resolved (directive) |
| GAP-0639 | The per-step autonomy contract slice: the four element names, the record member names, the recommendation marker, the route-output operation, the contract artefact names and the types are not specified by any source | Solution architect | Resolved (directive) |
| GAP-0640 | RWB-E8-004 in rwb-agent: the autonomy level set, the approval reference column, which approval element carries the approved level, the evidence and the breach behind a change, the right the change needs against the legacy permission list, the route, the decision code, the message for a level outside the list and the migration number are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0641 | The approval-gated version-change contract of rwb-agent: the field detail of the consumed approval answer, the name and type of the approval reference, the meaning of each 409 and 404, who calls the authorise operation, the record element map of a change with no rule, and the test of a repeated call are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0644 | Extraction evaluation in rwb-agent: service login, document-type owner, admin operation set, route path and score read path | Solution architect | Resolved (directive) |
| GAP-0645 | RWB-E8-003 in rwb-agent: the champion/challenger request fields, the comparison measure and its policy row, the P1 score-fact read, the version of a score row, the proposal shape, the migration number, the evaluation-run name and the requirement row are not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1047 | The agent's document-read tool contract is not defined in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1048 | The idempotency-key format of DocumentStored and the event field names the agent reads are not defined | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1049 | The mask format and the per-role list of personal fields for SY-AGENT are not defined | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1050 | The read behaviour for a stored document whose type has left the version in force is not defined | Business analyst, P5 | Resolved (directive) |
| GAP-1209 | Template code, channel, notice type, field names, recipient role holders, guard right and retry window are not named for the target | P6 comms owner, P10 agent owner and platform notification path owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1210 | The legacy data lake copy and the agent monitoring dashboard have no target, and P6 has no replacement for the dashboard | P6 comms owner, P9 reporting owner and architecture owner | Resolved (directive) |
| GAP-1211 | The agent alert event name, the alert notification operation name and the non-case binding of the cost alert are not named for the target | P10 agent owner and P6 comms owner | Resolved (directive) |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1516 | FSD P10 v3 publishes the agent dashboard through a data lake write and Power BI, both removed by Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1517 | The daily aggregate table the FSD acceptance criteria name is not in the Logical Data Model v8 entity list | Solution architect | Resolved (directive) |
| GAP-1518 | FSD P10 v3 has the agent read ACE and case facts directly, while Architecture v5 and ADR-010 reserve every ACE read to rwb-source-data | Solution architect | Resolved (directive) |
| GAP-1519 | JOB-15 is the reporting extract of rwb-reporting in the Ownership Map, but the FSD uses its completion as the trigger of the P10 dashboard | Platform administrator | Resolved (directive) |
| GAP-1520 | The admin configuration paths differ between the FSD and Architecture v5, and no source states the service REST base explicitly | Tech lead | Resolved (directive) |
| GAP-1525 | No date is stated for the platform wave that this service depends on | Program manager | Resolved (directive) |
| GAP-1528 | The tool gateway is stated as read-only and the guardrail is stated against an allowed action list, without saying whether an agent may ever act | Solution architect | Resolved (directive) |
| GAP-1530 | Four P10 features carry the same main success criterion, so the criterion does not distinguish the feature it belongs to | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1532 | The screening feature is titled at L1 and its main criterion stores a shadow run that creates no deviation | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1533 | The FSD states no wave or release for any of the sixteen agent features | Program manager | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-1834 | The change notes of FSD S8 versions 1 and 2 are not in the sources read | Business analyst, S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2187 | The agent runtime client has no published operation, no call type and no target-side home for the record write | Solution architect | Resolved (directive) |
| GAP-2188 | The client contract has no source member types, refusal detail or record reference shape | Solution architect | Resolved (directive) |
| GAP-2190 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the acceptance event name, the list codes, the case-decision proposal path, the route path, the feature flag home, the topic and migration values and the policy values the gate reads are not specified | Solution architect with the P10 service owner and the owners of rwb-case, rwb-decision and rwb-source-data | Resolved (directive) |
| GAP-2326 | The agent-authority part of POST /authorise has no operation row, request shape or answer shape in any source | Solution architect, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2327 | The reason-code vocabulary of a refusal and the status of each code are not specified | Solution architect, P4 and the security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2329 | The default scope of the agent service identity is not specified for this legacy key | Security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2332 | The access-event codes of a dashboard read, the entry field list, the page bounds, the read index and the Flyway step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-3085 | RWB-S8-E1062-APP: the deviation estate the shadow screening run reads has no read operation, no published agent-policy read, no owner role for R-DEV-05 and R-DEV-06, no value for the answer limit and no test level | Solution architect, with the rwb-deviation owner, the rule-set owner of the Deviations package, the rwb-agent contract owner, the rwb-case parameter and reference-data owners, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
