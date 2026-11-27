# RWB-SVC-P9 rwb-reporting (Reporting) - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 12 |
| Resolved in the stories | 222 |
| Cross-document (pending in another document) | 253 |
| Not applied (value not in the sources) | 43 |
| Open business decisions | 11 |
| Register gaps linked | 57 |
| Unconfirmed assumptions | 0 |
| Lint findings | 3 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P9-E1013-APP | 31 | 33 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E1013 APP Baseline measures v2.md |
| RWB-P9-E1013-CON | 14 | 32 | 14 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E1013 CON Baseline measures - contract v2.md |
| RWB-P9-E1013-OPS | 11 | 34 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E1013 OPS Baseline measures - deployment v2.md |
| RWB-P9-E2009-APP | 30 | 32 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E2009 APP Steering dashboard v1 data set v2.md |
| RWB-P9-E2009-CON | 21 | 31 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E2009 CON Steering dashboard v1 data set - contract v2.md |
| RWB-P9-E2009-OPS | 18 | 31 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E2009 OPS Steering dashboard v1 data set - deployment v2.md |
| RWB-P9-E6037-APP | 20 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E6037 APP Track benefit realisation v2.md |
| RWB-P9-E6037-CON | 15 | 8 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E6037 CON Track benefit realisation - contract v2.md |
| RWB-P9-E8001-APP | 18 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E8001 APP Produce regulatory returns v2.md |
| RWB-P9-E8001-CON | 12 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E8001 CON Produce regulatory returns - contract v2.md |
| RWB-P9-E8002-APP | 19 | 7 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E8002 APP Classify, stage and re-age an account v2.md |
| RWB-P9-E8002-CON | 13 | 13 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E8002 CON Classify, stage and re-age an account - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P9-E1013-OPS | R-11526 | CG-ALL-7826 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22435 | GAP-1663 | Register gap | Solution architect with the AI product owner | No event source is named for the agent acceptance and override measures | Count the two rates from the decision record, which carries the agent and prompt version, the recommendation, the approval and the outcome |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22439 | GAP-3178 | Register gap | Reporting and BI lead with the data product owner | RWB-E2-009 writes an INT-19 extract for a data lake that the target removes | Name the read model or event topic the Power BI data set subscribes to after the data lake removal, and update the acceptance criteria of RWB-E2-009 once. |
| RWB-P9-E8002-APP, RWB-P9-E8002-CON | R-23167 | GAP-2586 | Register gap | rwb-reporting service owner with the rwb-case service owner and the business owner of the universal rules | The legacy story puts the classification and re-ageing of an account in module P9 Reporting, while rule R-UNI-22 assigns the same recompute to the Workbench | Keep the case-side recompute, the route reopen and the hard-gate re-run with rwb-case under R-UNI-22 and R-UNI-37, keep the reported classification and its rule-versioned record with rwb-reporting as this story delivers, join the two by the case and rule events, and record the reading in the Change Register so the two service epics cite the same split. |
| RWB-ITG-E1013-ITG, RWB-ITG-E2009-ITG, RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E2009-APP, RWB-P9-E1013-APP, RWB-P9-E1013-CON, RWB-P9-E1013-OPS, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-P9-E8001-APP, RWB-P9-E8001-CON, RWB-P9-E8002-APP, RWB-P9-E8002-CON, RWB-S8-E2009-APP | R-28480 | GAP-1644 | Register gap | Business lead | The program BRD has no requirement section for P9 reporting | Keep the epic-level keys as the trace target and state the coverage basis in section 11.2 until a P9 requirement section exists |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-28752 | GAP-1659 | Register gap | Risk and model risk officer | No target is set for agent acceptance and override | Publish the two rates per agent and version and set no threshold until one is agreed |
| RWB-P9-E6037-APP, RWB-P9-E6037-CON | R-29023 | GAP-1483 | Register gap | Finance and CFO delegate | The benefit model measures and baselines are named but not given | Report the eight program measures from section 2 until the benefit model is supplied, and label the report as the program measure set, not the benefit model. |
| RWB-P9-E6037-APP, RWB-P9-E6037-CON | R-29024 | GAP-1656 | Register gap | Finance and CFO delegate | No benefit model measures, baselines or targets are set for benefit realisation | Report each measured value against the frozen baseline and state where no target exists |
| RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-S7-E6013-APP, RWB-S7-E6013-CON | R-29025 | GAP-1815 | Register gap | Product Owner | No approval is recorded for the BRD or the FSD this PRD is built from, and this version is Draft | Carry the PRD as Draft, leave the approval table empty, and record the missing approval as an assumption so that no approval is claimed for a document nobody signed. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-P9-E8002-APP, RWB-P9-E8002-CON | R-37768 | ASM-4281 | Register assumption |  | The case-side recompute of the segment, the route reopen and the hard-gate re-run of rules R-UNI-22 and R-UNI-37 stay with rwb-case, and rwb-reporting keeps only the reported classification and the record that names the rule version; the two services are joined by the case and rule events and by no shared table. | rwb-case service owner, rwb-reporting service owner and the business owner of the universal rules |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P9-E1013-APP | R-07086 | DOR-RWB-P9-E1013-APP-14 | none | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story, chunk or sources. Sign-off not recorded: Not specified in the source documents (DOR-RWB-P9-E1013-APP-14). |
| RWB-P9-E1013-APP | R-21932 | GAP-2579 | none | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Benefit-model measure set, monthly business day, month key, screen and requirement ID are in no source. Not in this story. Not specified in the source documents (GAP-2579). |
| RWB-P9-E1013-APP | R-21942 | GAP-0558 | 7 | DP-17 removes the INT-19 lake extract and the Power BI feed that legacy AC3 and AC7 assert | AC3 and AC7 text is in section 7, which is not in this chunk. Section 18 and BR8 already record the lake removal. No section 7 edit without its text. |
| RWB-P9-E1013-APP | R-21953 | GAP-2569 | 12.3, 12.4 | RWB-E1-013: the Ownership Map gives rwb-reporting no event while the wave 1 harness names rwb.reporting.ReportPublished.v1 on the service topic | The exact current wording of 12.3 and 12.4 is outside this chunk, so the None declarations cannot be written as exact edits. Nothing was invented. |
| RWB-P9-E1013-APP | R-22429 | GAP-2576 | 12.1, 12.2, 12.5, 7, 16 | rwb-reporting steering dashboard (application slice): the consumed operation names, the workflow and activity names, the read-model design, the INT-19 replacement and the agent fact source are fixed by no single source | 12.5 already has one hop, the 2 s timeout (ADR-020), queue Not specified (GAP-2576) and owner review. Consumption, read-model and agent text is outside this chunk. |
| RWB-P9-E1013-APP | R-26548 | CG-ALL-7806 | 7, 16 | Criteria and tests keep legacy job and decision-log wording | The nine JOB-nn, decision log and job record lines sit in sections 7 and 16, which are outside this chunk. Their exact text was not provided. |
| RWB-P9-E1013-CON | R-02002 | CG-ALL-7815 | 12.5 | Workflow MeasureRunWorkflow is not in Temporal Catalog v1 | Temporal Catalog v1 has no P9 workflow; only AceIngestCheck and reconciliation, both P1. Using either would be wrong, and a substitute would be invented. Name kept as declared. |
| RWB-P9-E1013-CON | R-07092 | DOR-RWB-P9-E1013-CON-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | Searched the project folder for 'signed epic design' and 'epic design record'. Only DOR review and work files matched, with no sign-off record. Sign-off would be invented. |
| RWB-P9-E1013-CON | R-21932 | GAP-2579 | not in chunk | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Benefit-model measure set, monthly day, month key, screen and requirement ID are in no source. The story sections for this item are not in the chunk, so there is no old text to edit. |
| RWB-P9-E1013-CON | R-21934 | GAP-0255 | not in chunk | The read-model control tables and the queue measures are absent | The Read-model controls section is not in this chunk, so no exact old text can be matched. Re-issue with that section. |
| RWB-P9-E1013-CON | R-21935 | GAP-0257 | not in chunk | dim_org holds an owner while events carry no personal data | The dim_org and owner-key text is not in this chunk, so no exact old text can be matched. Re-issue with that section. |
| RWB-P9-E1013-CON | R-21940 | GAP-0252 | not in chunk | The reporting layer reads recovery.v_ace_* views directly | The recovery.v_ace_* refresh cells and dimension rows are not in this chunk, so no exact old text can be matched. Re-issue with those sections. |
| RWB-P9-E1013-CON | R-21942 | GAP-0558 | not in chunk | DP-17 removes the INT-19 lake extract and the Power BI feed that legacy AC3 and AC7 assert | Legacy AC3 and AC7 text is not in this chunk, so no exact old text can be matched. Re-issue with the criteria section. |
| RWB-P9-E1013-CON | R-21943 | GAP-0560 | not in chunk | RWB-E1-013 is split across four stories and no single source assigns each legacy acceptance criterion | Sections 1 and 2 text is not in this chunk, so no exact old text exists to edit. Re-issue with sections 1 and 2. |
| RWB-P9-E1013-CON | R-21948 | GAP-2566 | 7 | RWB-E1-013: DP-17 removes the data lake while the two criteria this service owns assert the INT-19 extract, its trailer and the lake hold | AC3, AC7 and their TC rows in sections 7 and 16 are not in the chunk, so no anchored text to rewrite. Section 12.5 already states no lake path (DP-17). Needs that text. |
| RWB-P9-E1013-CON | R-21949 | GAP-2572 | 12.2 | RWB-E1-013: no source gives the path or the shape of the definitions read that RWB-P3-E1013-APP consumes across the service boundary | Section 12.2 text is not in the chunk, so no anchor exists for the GET /measure-definitions declaration with onDate. Needs that text. |
| RWB-P9-E1013-CON | R-21951 | GAP-2568 | 12 | RWB-E1-013: the definition load of table measure_definition has no target operation, because the table is P9's while the reference-load framework is rwb-case's | The reference-load element of measure_definition in section 12 is not in the chunk, so no anchored edit is possible. Needs that text. |
| RWB-P9-E1013-CON | R-26553 | CG-ALL-7818 | 16 | Test cases cover other criteria in Test Cases v8 | AC7 and AC8 are not criteria of this story, so the alignment to Test Cases v8 cannot be written here. |
| RWB-P9-E1013-CON | R-26555 | CG-ALL-7820 | 7 | Criteria and tests keep legacy job and decision-log wording | AC5 (section 7) and TC-E1-013-03 and TC-E1-013-05 (section 16) are not in the chunk; section 12.5 has no JOB-nn wording. Needs that text. |
| RWB-P9-E1013-CON | R-28488 | GAP-2571 | 12 | RWB-E1-013: the approver of a definition is typed uuid by the TSD while the legacy criteria and the FSD name the reference TRB-0001 | The approved_by declaration in section 12 and AC1 in section 7 are not in the chunk, so no anchored edit is possible. Needs that text. |
| RWB-P9-E1013-OPS | R-18436 | DOR-RWB-P9-E1013-OPS-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 text is not in the chunk and the story file is not on disk, so there is no exact text to anchor the SCR-37 and SCR-44 state rows. |
| RWB-P9-E1013-OPS | R-18437 | DOR-RWB-P9-E1013-OPS-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Section 11 text is not in the chunk and the story file is not on disk, so there is no exact text to anchor the P2 personal-data rows. |
| RWB-P9-E1013-OPS | R-18439 | DOR-RWB-P9-E1013-OPS-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in the chunk and no AC or TC IDs were supplied, so BR1 to BR9 cannot be linked without invented IDs or unanchored rows. |
| RWB-P9-E1013-OPS | R-21948 | GAP-2566 | 7 | RWB-E1-013: DP-17 removes the data lake while the two criteria this service owns assert the INT-19 extract, its trailer and the lake hold | AC3 and AC7 sit in section 7 and section 16, which are not in this chunk, so they cannot be copied or edited. BR5 and the change log already record no lake path and no extract. |
| RWB-P9-E1013-OPS | R-31696 | NEWAC-RWB-P9-E1013-OPS-AC9 | 8 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | The new AC needs a section 7 criterion and a section 16 test row, and neither is in this chunk. The sources give no proposed test: Not specified in the source documents (NEWAC-RWB-P9-E1013-OPS-AC9). |
| RWB-P9-E2009-APP | R-22431 | GAP-0391 |  | Gateway-bff composite steering route, harness environment, measure-day seeding, evidence format and pass/fail gate not specified | Route path, merge order, harness, seed, evidence format and gate are in no source read. Not specified in the source documents (GAP-0391); to be agreed at the wave 2 entry check. |
| RWB-P9-E2009-APP | R-22438 | GAP-3089 | 7 | RWB-S8-E2009-APP: the plan assigns the slice no legacy acceptance criterion while it keeps ten legacy test cases, and the legacy criteria lose their owned ids | Restating AC1 to AC9 as new (D-RCV-60) and the section 18 mapping need legacy section 7 text and section 18, outside this chunk. No criterion was added. |
| RWB-P9-E2009-APP | R-28491 | GAP-2580 | 9 | Benefit realisation: the variance fields, the variance rule, the row ceiling, the event absence and the baseline date default are not fixed by any source | Not in PRD P9 v2 or Contract Catalog v2: variance fields, arithmetic, row ceiling, baseline date default. Event found (PRD FR-P9-023 ReportPublished). Section 9 text not supplied; no edit. |
| RWB-P9-E2009-CON | R-18456 | DOR-RWB-P9-E2009-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Coverage needs AC IDs in section 7 and TC IDs in section 16, which are not in this chunk. Section 8 has 13 rules (BR1-BR13), not 11. No edit made. |
| RWB-P9-E2009-CON | R-21932 | GAP-2579 | find it | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Measure set, business day, month key, screen and requirement ID are business decisions with no value in the sources. No value written; no benefit text in this chunk. |
| RWB-P9-E2009-CON | R-22438 | GAP-3089 | find it | RWB-S8-E2009-APP: the plan assigns the slice no legacy acceptance criterion while it keeps ten legacy test cases, and the legacy criteria lose their owned ids | Section 7 and section 18 text is not in this chunk, so the AC1-AC9 restatement and TC-E2-009-10 mapping cannot be anchored as edits. No edit made. |
| RWB-P9-E2009-CON | R-26572 | CG-ALL-7858 | 3, 3.1 | Flyway file V2_009__measure_publish.sql is not in the V0001..Vnnnn form | Migration name and section 3.1 row are not in this chunk. Next rwb-reporting Flyway number not found in a folder search; no value written. |
| RWB-P9-E2009-OPS | R-11544 | CG-ALL-7862 | 12.4 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | Section 12.4 is in this document and its events table was edited. The decision_record name was not located in this chunk; locate it and check against LDM v9 or Data Classification v5. |
| RWB-P9-E2009-OPS | R-18464 | DOR-RWB-P9-E2009-OPS-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in this chunk, and the on-disk story differs from the chunk (e.g. DL25 text). No anchored AC/TC edit is safe; re-run with current sections 7 and 16. |
| RWB-P9-E2009-OPS | R-28753 | GAP-3090 | find it | RWB-S8-E2009-APP: the schedule time, the dimension format, the two added Measure fields and the alert recipients have no published values for the deviation serving | Schedule id, calendar, catch-up policy, rerun input, Measure fields, dimension format and alert recipients are owner values not in the sources (GAP-3090). No values invented. |
| RWB-P9-E6037-APP | R-07119 | DOR-RWB-P9-E6037-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in 22 Microservice Realignment or 23 Document Gaps. Sign-off cannot be confirmed from sources; no value invented. |
| RWB-P9-E6037-CON | R-18477 | DOR-RWB-P9-E6037-CON-10 |  | Definition of Ready item 10 Screens and states: Partial | No empty, loading, error or no-access state for SCR-37 is in any source (03 Requirements per prior search). Adding them would invent UI behaviour. Needs a source. |
| RWB-P9-E6037-CON | R-21932 | GAP-2579 |  | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Benefit-model measure set, monthly cut-off, month key, screen and requirement ID are in no source. Needs a Solution architect value; none invented. Story body not in chunk. |
| RWB-P9-E8001-APP | R-18492 | DOR-RWB-P9-E8001-APP-6 Authority: Partial | 10 | Definition of Ready item 6 Authority: Partial | No rwb-access authorise check name in any source document (searched). Added row removed as it names a check not in the sources and duplicates the placeholder; no value invented. |
| RWB-P9-E8002-APP | R-07141 | DOR-RWB-P9-E8002-APP-23 | find it | Definition of Ready item 23 Contract version fixed: Fail | Sources give only the /v1 path; no contract version for RWB-P9-E8002-CON found in the project documents. Not invented, no edit. |
| RWB-P9-E8002-CON | R-18511 | DOR-RWB-P9-E8002-CON-1 | 1 | Definition of Ready item 1 Story: Partial | No Users Roles and Permissions v5 role code or name for the tech lead is given in the sources; naming one would invent a value. |
| RWB-P9-E8002-CON | R-18513 | DOR-RWB-P9-E8002-CON-12 | 12.7, 16 | Definition of Ready item 12 Test cases: Partial | Section 7 is not in this chunk, so the boundary AC and its TC row cannot be added; TC IDs also need registering in Test Cases v8. |
| RWB-P9-E8002-CON | R-18516 | DOR-RWB-P9-E8002-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Section 7 is not in this chunk; new criteria and TC rows covering BR1 to BR10 need a section 7 edit first. |

## 5. Cross-document changes (pending in the target document)


### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (26)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13438 | RWB-P9-E1013-APP | GAP-0565 | n/a | Use the sentence {product} is from {date}. Today's ACE batch has not arrived. in place of the load wording, following the higher FSD P1 and TSD P1 source. |
| CDC-13506 | RWB-P9-E1013-OPS | GAP-0565 | find it | Set the second sentence of MSG-P1-001 to Today's ACE batch has not arrived. in every copy. |
| CDC-13549 | RWB-P9-E2009-CON | CG-ALL-7850 | 4, 14 | Add a new message ID for the dashboard count differs case list with the held-publish text; the story cites it once the ID exists. |
| CDC-13550 | RWB-P9-E2009-CON | CG-ALL-7851 | 4, 14 | Add a new message ID for a source is stale with the product and date text; the story cites it once the ID exists. |
| CDC-13551 | RWB-P9-E2009-CON | CG-ALL-7852 | 4, 14 | Add a new message ID for dates in the wrong order with the two-field text; the story cites it once the ID exists. |
| CDC-13552 | RWB-P9-E2009-CON | CG-ALL-7853 | 4, 14 | Add a new message ID for the role lacks Reporting R with the refused-action text; the story cites it once the ID exists. |
| CDC-13553 | RWB-P9-E2009-CON | CG-ALL-7854 | 4, 14 | Add a new message ID for a named system is unavailable with the system-name text; the story cites it once the ID exists. |
| CDC-13554 | RWB-P9-E2009-CON | CG-ALL-7855 | 4, 14 | Add a new message ID for the local record cannot be written with the nothing-changed text; the story cites it once the ID exists. |
| CDC-13577 | RWB-P9-E2009-OPS | CG-ALL-7864 | 4, 14 | Add a new message ID for 'The dashboard count differs from the case list' and hold MSG-P9-002 for the standard text; the story then cites the new ID in section 14. |
| CDC-13578 | RWB-P9-E2009-OPS | CG-ALL-7865 | 4, 14 | Add a new message ID for 'A source is stale' and keep MSG-P1-001 for the standard text; the story then cites the new ID in section 14. |
| CDC-13579 | RWB-P9-E2009-OPS | CG-ALL-7866 | 4, 14 | Add a new message ID for 'The hand-over or a named system is unavailable' and keep MSG-GEN-006 for the standard text; the story then cites the new ID in section 14. |
| CDC-13580 | RWB-P9-E2009-OPS | CG-ALL-7867 | 4, 14 | Add a new message ID for 'The record cannot be written' and keep MSG-P7-003 for the standard text; the story then cites the new ID in section 14. |
| CDC-13581 | RWB-P9-E2009-OPS | CG-ALL-7868 | 4, 14 | Add a new message ID for 'The role lacks Reporting R' and keep MSG-P4-002 for the standard text; the story then cites the new ID in section 14. |
| CDC-13625 | RWB-P9-E8001-APP | CG-ALL-7893 | 4, 14 | Add a new message ID for 'A measure of the return has no definition in force'; the story then cites it. |
| CDC-13626 | RWB-P9-E8001-APP | CG-ALL-7894 | 4, 14 | Add a new message ID for 'The counts behind the publish do not match'; the story then cites it. |
| CDC-13629 | RWB-P9-E8001-APP | DOR-RWB-P9-E8001-APP-9 | 14 | Confirm MSG-P1-001 text and the meanings of MSG-P9-002 and MSG-P9-003 against the standard; align the story rows |
| CDC-13634 | RWB-P9-E8001-CON | CG-ALL-7899 | 14 | Add a new message ID for the publish-counts condition of RWB-P9-E8001-CON; the story cites it once it exists |
| CDC-13635 | RWB-P9-E8001-CON | CG-ALL-7900 | 14 | Add a new message ID for the no-definition-in-force condition of RWB-P9-E8001-CON; the story cites it once it exists |
| CDC-13639 | RWB-P9-E8001-CON | DOR-RWB-P9-E8001-CON-9 | 14 | MSG-P1-001 text aligned; MSG-P9-002 and MSG-P9-003 rows restored to not-specified text |
| CDC-13652 | RWB-P9-E8002-CON | CG-ALL-7912 | 4, 14 | Add a new message ID for 'A data product behind the case facts is stale' (503), then the story cites it |
| CDC-13653 | RWB-P9-E8002-CON | CG-ALL-7913 | 4, 14 | Add a new message ID for 'The change record cannot be written' (500), then the story cites it |
| CDC-13654 | RWB-P9-E8002-CON | CG-ALL-7914 | 4, 14 | Add a new message ID for 'The role lacks Reporting R' (403), then the story cites it |
| CDC-13655 | RWB-P9-E8002-CON | CG-ALL-7915 | 4, 14 | Add a new message ID for 'A field is missing on a request' (400), then the story cites it |
| CDC-13656 | RWB-P9-E8002-CON | CG-ALL-7916 | 4, 14 | Add a new message ID for 'A period has from after to' (422), then the story cites it |
| CDC-13657 | RWB-P9-E8002-CON | CG-ALL-7917 | 14 | Add a new message ID for 'The rule read or another named system is unavailable' (503, system name only); section 14 then cites it. |
| CDC-13658 | RWB-P9-E8002-CON | CG-ALL-7918 | 14 | Add a new message ID for 'No rule version is in force on the business date' (409 on a read); section 14 then cites it. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13418 | RWB-P9-E1013-APP | CG-ALL-7804 | 12.5 | Add an activity row measureRun on task queue rwb-reporting for RWB-P9-E1013-APP. |
| CDC-13450 | RWB-P9-E1013-CON | CG-ALL-7816 | 12.5 | Add activity measureRun to the Activities sheet on task queue rwb-reporting, as the contract element of section 12.5 names it. |
| CDC-13509 | RWB-P9-E2009-APP | CG-ALL-7830 | 12.5 | Add a Workflows row for reportingMeasuresDaily (JOB-15, Schedule at 01:30, queue rwb-reporting) or name the catalogued workflow that JOB-15 uses |
| CDC-13513 | RWB-P9-E2009-APP | DOR-RWB-P9-E2009-APP-8 | 12.5 | Add Workflows rows for reportingMeasuresDaily and activities checkFreshness, loadReadModel, loadAgentFacts, computeMeasures, reconcileCounts, publishDay on rwb-reporting, or name catalogued equivalents |
| CDC-13515 | RWB-P9-E2009-APP | CG-ALL-7831 | 12.5 | Add activity checkFreshness, task queue rwb-reporting, to the Activities sheet. |
| CDC-13516 | RWB-P9-E2009-APP | CG-ALL-7832 | 12.5 | Add activity loadReadModel, task queue rwb-reporting, to the Activities sheet. |
| CDC-13517 | RWB-P9-E2009-APP | CG-ALL-7833 | 12.5 | Add activity loadAgentFacts, task queue rwb-reporting, to the Activities sheet. |
| CDC-13518 | RWB-P9-E2009-APP | CG-ALL-7834 | 12.5 | Add activity computeMeasures, task queue rwb-reporting, to the Activities sheet. |
| CDC-13519 | RWB-P9-E2009-APP | CG-ALL-7835 | 12.5 | Add activity reconcileCounts, task queue rwb-reporting, to the Activities sheet. |
| CDC-13520 | RWB-P9-E2009-APP | CG-ALL-7836 | 12.5 | Add activity publishDay, task queue rwb-reporting, to the Activities sheet. |
| CDC-13541 | RWB-P9-E2009-CON | CG-ALL-7849 | 12.5 | Add a Workflows row for reportingMeasuresDaily (JOB-15): type workflow, task queue rwb-reporting, namespace rwb-recovery, started by its Schedule. |
| CDC-13572 | RWB-P9-E2009-OPS | CG-ALL-7863 | 12.5 | Catalogue has no reportingMeasuresDaily Workflows row. Story AC5 and section 15 now name reportingMeasuresDaily per PRD P9; the catalogue row is the open fix. |
| CDC-13575 | RWB-P9-E2009-OPS | DOR-RWB-P9-E2009-OPS-8 | 12.5 | Add a Workflows row for `reportingMeasuresDaily` (JOB-15), registered on queue rwb-reporting, and a Schedules row for JOB-15 that starts it. |
| CDC-13614 | RWB-P9-E6037-CON | CG-ALL-7886 | 12.5 | Add a row for workflow reportingMeasuresDaily (JOB-15, owned by RWB-P9-E2009-APP) on task queue rwb-reporting. |
| CDC-13616 | RWB-P9-E6037-CON | DOR-RWB-P9-E6037-CON-8 | 12.5 | Add workflow reportingMeasuresDaily (JOB-15, owned by RWB-P9-E2009-APP) and activity 'The data-product readiness of a month' on rwb-source-data. |
| CDC-13618 | RWB-P9-E6037-CON | CG-ALL-7887 | 12.5 | Add activity 'The data-product readiness of a month' on queue rwb-source-data at the owner's queue. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13464 | RWB-P9-E1013-CON | CG-ALL-7817 | 16 | Add rows TC-P9-E1013-CON-01 to TC-P9-E1013-CON-05 with Given, When and Then copied from the criteria they cover |
| CDC-13500 | RWB-P9-E1013-OPS | CG-ALL-7824 | 16 | Add rows for TC-P9-E1013-OPS-01 to -06 with Given, When and Then copied from the criteria they cover in section 7 of RWB-P9-E1013-OPS. |
| CDC-13566 | RWB-P9-E2009-CON | CG-ALL-7856 | 16 | Add rows for TC-P9-E2009-CON-01 to TC-P9-E2009-CON-08 with Given, When and Then copied from the criterion each covers. |
| CDC-13598 | RWB-P9-E2009-OPS | CG-ALL-7869 | 16 | Add rows for TC-P9-E2009-OPS-01 to -07 with Given, When and Then copied from the criterion each covers. |
| CDC-13612 | RWB-P9-E6037-APP | CG-ALL-7881 | 16 | Workbook change needed |
| CDC-13621 | RWB-P9-E6037-CON | CG-ALL-7889 | 16 | Add rows TC-P9-E6037-CON-01 to TC-P9-E6037-CON-09 with Given, When and Then copied from the criteria they cover. |
| CDC-13627 | RWB-P9-E8001-APP | CG-ALL-7895 | 16 | Add rows TC-E8-001-01 to TC-E8-001-04 to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-13628 | RWB-P9-E8001-APP | DOR-RWB-P9-E8001-APP-12 | 16 | On tab Story test cases add rows TC-E8-001-01 to TC-E8-001-04 and new TC-E8-001-05 to TC-E8-001-07 with Given, When and Then |
| CDC-13638 | RWB-P9-E8001-CON | DOR-RWB-P9-E8001-CON-12 | 16 | Add rows for TC-E8-001-01 to TC-E8-001-04 and TC-P9-E8001-CON-01 to TC-P9-E8001-CON-08 in tab Story test cases |
| CDC-13641 | RWB-P9-E8001-CON | CG-ALL-7901 | 16 | Add a row for each of TC-E8-001-01 to TC-E8-001-04 and TC-P9-E8001-CON-01 to TC-P9-E8001-CON-08, with Given, When and Then copied from the criterion each covers. |
| CDC-13646 | RWB-P9-E8002-APP | CG-ALL-7907 |  | Add rows TC-E8-002-01 to TC-E8-002-04 to Story test cases with Given, When and Then from their criteria |
| CDC-13661 | RWB-P9-E8002-CON | CG-ALL-7919 | 16 | Add rows TC-P9-E8002-CON-01 to TC-P9-E8002-CON-07 to the story test cases, with Given, When and Then copied from AC1 to AC7 of RWB-P9-E8002-CON. |

### RWB-P9-E1013-CON (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13415 | RWB-P9-E1013-APP | DOR-RWB-P9-E1013-APP-21 |  | Publish the contract and set the build status to Done; this story's contract dependency holds until then. |
| CDC-13416 | RWB-P9-E1013-APP | DOR-RWB-P9-E1013-APP-22 |  | Publish the contract fake library and record its published version in the CON story. |
| CDC-13431 | RWB-P9-E1013-APP | GAP-2572 | 12.2 | Declare GET /measure-definitions with query parameter onDate and a definition list answer, as a target declaration pending the P3 team's confirmation of path and field list. |
| CDC-13432 | RWB-P9-E1013-APP | GAP-2568 | 4 | Declare the reference-load element of table measure_definition on the rwb-reporting base; list values stay on the rwb-case reference-data contract; rwb-case owner confirms whether the load belongs to the framework. |
| CDC-13440 | RWB-P9-E1013-APP | GAP-2571 | n/a | Declare approved_by as uuid and approved_at as timestamptz as the TSD types them, and carry TRB-0001 as a comment on the element. |
| CDC-13476 | RWB-P9-E1013-OPS | DOR-RWB-P9-E1013-OPS-21 | Header | Finish the build and publish the contract so its build status is Done |
| CDC-13477 | RWB-P9-E1013-OPS | DOR-RWB-P9-E1013-OPS-22 | Header | Publish a contract fake library version and record it |
| CDC-13487 | RWB-P9-E1013-OPS | GAP-2570 | find it | Declare the measures read in the wave 1 contract for the harness and catalogue consumer; keep the dashboard and SCR-37 with RWB-P9-E2009-APP; leave reporting client connection open for the PRD. |
| CDC-13498 | RWB-P9-E1013-OPS | GAP-2572 | none | Declare GET /measure-definitions with query parameter onDate and a definition list answer as a target declaration; confirm the path and field list with the P3 team in baseline review. |
| CDC-13499 | RWB-P9-E1013-OPS | GAP-2568 | none | Declare the reference-load element of table measure_definition on the rwb-reporting base; keep list values on the rwb-case contract; rwb-case owner confirms who loads a P9 table. |
| CDC-13508 | RWB-P9-E1013-OPS | GAP-2571 | find it | Declare measure_definition.approved_by as uuid per TSD P9 T3.1, with TRB-0001 as a comment; RWB-P9-E1013-APP keeps both legacy values in AC1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13483 | RWB-P9-E1013-OPS | GAP-0251 | find it | Replace the data-lake landing of the nine fact tables with the rwb_reporting read model fed from service topics; serve via GET /dashboards/{id} and GET /reports/{id}. |
| CDC-13485 | RWB-P9-E1013-OPS | GAP-0257 | find it | Key owner and team by ID and resolve display names from P3 queue_member and assignment behind rwb-access masking; no personal data on events. |
| CDC-13538 | RWB-P9-E2009-APP | GAP-0258 | 8 | Read the Power BI consumer as rwb-reporting serving GET /dashboards/{id} and GET /reports/{id}, and correct the Power BI wording in both documents |
| CDC-13545 | RWB-P9-E2009-CON | CG-ALL-7844 | 12.8 | Record decision_record as a PLT library table created in rwb_reporting (DP-03), so the story name resolves to a recorded object. |
| CDC-13588 | RWB-P9-E2009-OPS | GAP-0255 | find it | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate; state queue measures stay with P3 rwb_case. |
| CDC-13607 | RWB-P9-E6037-APP | CG-ALL-7874 | lines 236, 303 | Add an entity or field for the local decision record, or confirm the dictionary name to use in place of decision_record (owner: Data). |
| CDC-13617 | RWB-P9-E6037-CON | CG-ALL-7885 | 12.7 | Name the PLT library table decision_record created in rwb_reporting in the dictionary, or record it in the owning document. |
| CDC-13645 | RWB-P9-E8002-APP | CG-ALL-7904 |  | Record decision_record as a PLT library object created in rwb_reporting, or name its dictionary field |
| CDC-13659 | RWB-P9-E8002-CON | DOR-RWB-P9-E8002-CON-7 | 11 | Register decision_record as a field or entity in LDM v9 or Data Classification v5; section 11 BR Field IDs are placeholders until then. |

### RWB-P9-E2009-CON (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13511 | RWB-P9-E2009-APP | DOR-RWB-P9-E2009-APP-21 |  | Publish the contract and set its build status to Done |
| CDC-13512 | RWB-P9-E2009-APP | DOR-RWB-P9-E2009-APP-22 |  | Publish the contract fake library and record its published version |
| CDC-13527 | RWB-P9-E2009-APP | GAP-2570 |  | Declare GET /reports/measures as the wave 1 measures read for the harness and catalog consumer; leave connection of any reporting client as an open decision for the PRD step. |
| CDC-13528 | RWB-P9-E2009-APP | GAP-2576 | 11 | Declare the three consumed case, agent and source-data operations and the two owner-queue activities on the per-service bases and queues, one hop, 2 s timeout; take element names from owners at review. |
| CDC-13529 | RWB-P9-E2009-APP | GAP-2577 |  | Publish v1 contract increment: baselineValue delta, fixed dimension, three declarations, two activity contracts, eight subscriptions with groups, JOB-15 registration, message map and fakes; placeholders with one review row; gate on contract tests and schema lint. |
| CDC-13573 | RWB-P9-E2009-OPS | DOR-RWB-P9-E2009-OPS-21 | header | Set build status to Done and publish the contract. |
| CDC-13574 | RWB-P9-E2009-OPS | DOR-RWB-P9-E2009-OPS-22 | header | Publish a contract fake library version. |
| CDC-13591 | RWB-P9-E2009-OPS | GAP-2570 | find it | Declare the measures read operation in the wave 1 contract for the harness and P3 catalog consumer; keep the dashboard and its data set in RWB-P9-E2009-APP; leave reporting client connection as a PRD open decision. |
| CDC-13593 | RWB-P9-E2009-OPS | GAP-2577 | find it | Publish version v1 as an increment: baselineValue delta, dimension fix, three declarations, two activity contracts, eight subscriptions, JOB-15 registration contract, message map and fakes; mark unsettled elements with placeholders; gate on contract tests and schema lint. |

### Epic design record (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13475 | RWB-P9-E1013-OPS | DOR-RWB-P9-E1013-OPS-14 | Header | Confirm the signed epic design sign-off and record it in the epic design record |
| CDC-13510 | RWB-P9-E2009-APP | DOR-RWB-P9-E2009-APP-14 |  | Record the signed epic design sign-off for this story's epic |
| CDC-13542 | RWB-P9-E2009-CON | DOR-RWB-P9-E2009-CON-14 | find it | Record the signed epic design sign-off so the story can cite it; the sign-off is not in the source documents. |
| CDC-13615 | RWB-P9-E6037-CON | DOR-RWB-P9-E6037-CON-14 | n/a | Record the signed epic design sign-off for RWB-SVC-P9 under EP06. |
| CDC-13622 | RWB-P9-E8001-APP | DOR-RWB-P9-E8001-APP-14 | header | Record the signed epic design sign-off for EP08 in the epic design record. |
| CDC-13632 | RWB-P9-E8001-CON | DOR-RWB-P9-E8001-CON-14 | header | Record the signed sign-off of the epic design; no signed design is in the story or source documents |
| CDC-13642 | RWB-P9-E8002-APP | DOR-RWB-P9-E8002-APP-14 |  | Confirm the signed epic design sign-off is recorded for RWB-SVC-P9 |
| CDC-13649 | RWB-P9-E8002-CON | DOR-RWB-P9-E8002-CON-14 | Header | Confirm and record the signed epic design sign-off for EP08 / RWB-SVC-P9 |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13419 | RWB-P9-E1013-APP | DOR-RWB-P9-E1013-APP-12 | 16, 18 | TC-E1-013-10, -11 and TC-E1-013-12 to -19 added in section 16 |
| CDC-13433 | RWB-P9-E1013-APP | CG-ALL-7805 | 18 | Align the REQ-RDF-012 test list with RWB-P9-E1013-APP section 18 (TC-E1-013-01, -03, -04, -05, -07, -08) in the next RTM version. |
| CDC-13501 | RWB-P9-E1013-OPS | CG-ALL-7825 | 18 | Align the REQ-RDF-012 test list with section 18 of RWB-P9-E1013-OPS (TC-P9-E1013-OPS-01, -03, -06) in the next RTM version. |
| CDC-13521 | RWB-P9-E2009-APP | DOR-RWB-P9-E2009-APP-12 | 16 | Align test lists of REQ-WKM-006 and REQ-WKM-009 in story section 18 with section 16, including TC-E2-009-11. |
| CDC-13535 | RWB-P9-E2009-APP | CG-ALL-7839 | 18 | Align the REQ-WKM-009 and REQ-WKM-006 test lists with section 18 of RWB-P9-E2009-APP in the next RTM version. |
| CDC-13567 | RWB-P9-E2009-CON | CG-ALL-7857 | 18 | Align the REQ-WKM-009 and REQ-WKM-006 test lists with section 18 of RWB-P9-E2009-CON in the next RTM version. |
| CDC-13599 | RWB-P9-E2009-OPS | CG-ALL-7870 | 18 | Align the REQ-WKM-009 and REQ-WKM-006 test lists with section 18 of this story in the next RTM version. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13429 | RWB-P9-E1013-APP | GAP-2239 | 12 | Publish GET /api/recovery/case/v1/cases/facts with businessDate, page and size, and the legacy response fields, provisional until confirmed at the next revision. |
| CDC-13430 | RWB-P9-E1013-APP | GAP-2240 | 12 | Publish the measure-catalog read under RWB-P9-E1013-CON as GET on the rwb-reporting base with an onDate parameter, and name it in the catalog. |
| CDC-13461 | RWB-P9-E1013-CON | GAP-2239 | 4 | Publish GET /api/recovery/case/v1/cases/facts with businessDate, page and size, and the fields of CaseReportingApi.caseFacts, marked provisional. |
| CDC-13462 | RWB-P9-E1013-CON | GAP-2240 | 12.2 | Name the measure-catalog read as a GET on the rwb-reporting base with an onDate parameter and its response fields. |
| CDC-13496 | RWB-P9-E1013-OPS | GAP-2239 | 12 | Publish GET /api/recovery/case/v1/cases/facts with businessDate, page and size and the legacy response fields, marked provisional until the next revision. |
| CDC-13562 | RWB-P9-E2009-CON | GAP-0731 | n/a | Record the case-fact read schema, cut-off rule, fact transport, queue_measure dimension set and gateway-bff route detail agreed with the rwb-reporting owner. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13543 | RWB-P9-E2009-CON | DOR-RWB-P9-E2009-CON-8 | 12.4 | Fix the consumer mismatches: add rwb-reporting consumers for rwb.treatment.TreatmentApproved.v1, rwb.comms.NoticeDelivered.v1 and rwb.agent.AgentRunCompleted.v1; the event-name mismatch is resolved in the story. |
| CDC-13546 | RWB-P9-E2009-CON | CG-ALL-7846 | 12.4 | Add rwb-reporting as a consumer of rwb.treatment.TreatmentApproved.v1 (EV-10) and add its ACL. |
| CDC-13547 | RWB-P9-E2009-CON | CG-ALL-7847 | 12.4 | Add rwb-reporting as a consumer of rwb.comms.NoticeDelivered.v1 (EV-15) and add its ACL. |
| CDC-13548 | RWB-P9-E2009-CON | CG-ALL-7848 | 12.4 | Add rwb-reporting as a consumer of rwb.agent.AgentRunCompleted.v1 (EV-28) and grant its ACL. |
| CDC-13651 | RWB-P9-E8002-CON | CG-ALL-7911 | 12.4 | Add rwb-reporting as a consumer of rwb.decision.RulePackageInForce.v1 (EV-30) in the Events row and in its ACL |
| CDC-13660 | RWB-P9-E8002-CON | DOR-RWB-P9-E8002-CON-8 | 7 | Add rwb-reporting as a consumer of rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1, owner P7, matching AC4 of this story. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13558 | RWB-P9-E2009-CON | DOR-RWB-P9-E2009-CON-7 | 11 | Add decision_record as an entity, or record it as a PLT library record outside the LDM; the story names it in section 12. |
| CDC-13584 | RWB-P9-E2009-OPS | DOR-RWB-P9-E2009-OPS-7 | 11 | Add decision_record as an entity or field (PLT library table in rwb_reporting) in LDM v9 and Data Classification v5. |
| CDC-13613 | RWB-P9-E6037-APP | DOR-RWB-P9-E6037-APP-7 | 11 | Add entity decision_record (owner rwb_reporting, PLT library) to LDM v9 and Data Classification v5, or confirm the name of the local record |
| CDC-13620 | RWB-P9-E6037-CON | DOR-RWB-P9-E6037-CON-7 | 11 | Register decision_record as an entity created in rwb_reporting by the PLT library, or confirm the name in both documents. |
| CDC-13647 | RWB-P9-E8002-APP | DOR-RWB-P9-E8002-APP-7 | 11 | Add or confirm the entity name decision_record (local record per changed account, DP-03) in both documents. |
| CDC-13650 | RWB-P9-E8002-CON | CG-ALL-7910 | 12.7 | Record decision_record as a PLT library table in the owning document, or add the field or entity to LDM v9 under the dictionary name |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13451 | RWB-P9-E1013-CON | DOR-RWB-P9-E1013-CON-1 | 1 | Add the role name 'tech lead of rwb-reporting' with its role code, so that section 1 and section 10 resolve to a listed role. |
| CDC-13479 | RWB-P9-E1013-OPS | DOR-RWB-P9-E1013-OPS-1 | 1 | Add 'platform engineer' as a role code or role name, or name the existing role that §1 should use |
| CDC-13555 | RWB-P9-E2009-CON | DOR-RWB-P9-E2009-CON-1 | 1 | Add the role contract owner of the reporting service as a role code or name, or name the existing role code that section 1 must cite. |
| CDC-13619 | RWB-P9-E6037-CON | DOR-RWB-P9-E6037-CON-1 | 1 | Add 'tech lead' as a role code or name, or name the existing role code the story persona maps to. |
| CDC-13636 | RWB-P9-E8001-CON | DOR-RWB-P9-E8001-CON-1 | 1 | Add the role 'tech lead' as a role code or role name |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13411 | RWB-P9-E1013-APP | CG-ALL-7800 | 12.2 | Publish GET /api/recovery/case/v1/cases/facts through the rwb-case provider CON story (RWB-P3-E1013-APP provides the facts read). |
| CDC-13412 | RWB-P9-E1013-APP | CG-ALL-7801 | 12.2 | Publish the GET /api/recovery/case/v1/cases/{caseId} operation through the rwb-case provider CON story (RWB-P3-E1018-CON). |
| CDC-13445 | RWB-P9-E1013-CON | CG-ALL-7812 | 12.2 | Publish GET /api/recovery/case/v1/cases/facts in rwb-case.yaml through the provider's CON story. |
| CDC-13446 | RWB-P9-E1013-CON | CG-ALL-7813 | 12.2 | Publish GET /api/recovery/case/v1/cases/{caseId} in rwb-case.yaml through the provider's CON story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13410 | RWB-P9-E1013-APP | CG-ALL-7799 | 12.1 | Publish GET /api/recovery/reporting/v1/measure-definitions as declared in 12.1 through RWB-P9-E1013-CON, or remove the operation. |
| CDC-13443 | RWB-P9-E1013-CON | CG-ALL-7810 | 12.1 | Publish GET /api/recovery/reporting/v1/measure-definitions in rwb-reporting.yaml through the CON story. |
| CDC-13444 | RWB-P9-E1013-CON | CG-ALL-7811 | 12.1 | Publish the reference-load operation (operation name and path Not specified in the source documents (GAP-2568; ASM-4234)) under /api/recovery/reporting/v1 in rwb-reporting.yaml. |

### RWB-P3-E1043-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13425 | RWB-P9-E1013-APP | GAP-2241 | 12 | Name the age-band list with a list code and a table code in the reference-data catalog, then use that code in the band read and on the band list screen. Codes not in source: needs TechX and data steward RW-DATASTEW. |
| CDC-13458 | RWB-P9-E1013-CON | GAP-2241 |  | Name the age-band list with a list code and a table code, then use that code in this read and on the band list screen. No code is given in the sources. |
| CDC-13489 | RWB-P9-E1013-OPS | GAP-2241 | 12 | Name the age-band list with a list code and a table code, and use that code on the read and the band list screen. Codes Not specified in the source documents (GAP-2241). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13427 | RWB-P9-E1013-APP | GAP-0339 | 8 | Add the v5 measure_definition load path and the numbered catalogue entry for ReportPublished; rwb-reporting publishes on rwb.reporting.events.v1 and rwb-integration delivers the regulatory extract. |
| CDC-13459 | RWB-P9-E1013-CON | GAP-0339 |  | Add the v5 measure_definition load path and the numbered catalogue entry for ReportPublished. |
| CDC-13491 | RWB-P9-E1013-OPS | GAP-0339 | 12 | Add the v5 measure_definition load path and the numbered catalogue entry for ReportPublished, with rwb-integration delivering the regulatory extract. |

### OTHER:FSD P9 (AC-P9-001-01; OTHER:AC-P9-003-01; OTHER:AC-P9-008-01; OTHER:AC-ALT-P9-003-01; OTHER:AC-ALT-P9-003-02) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13456 | RWB-P9-E1013-CON | GAP-1649 |  | Publish the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE, and state the count as an open question. |
| CDC-13486 | RWB-P9-E1013-OPS | GAP-1649 | find it | Name one measure set: six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE; replace each of the 7 measures; carry the count as an open question. |
| CDC-13590 | RWB-P9-E2009-OPS | GAP-1649 | find it | Publish the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE; carry the seventh-measure count as an open question. |

### RWB-P9-E1013-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13474 | RWB-P9-E1013-CON | GAP-2575 | find it | Carry measure_definition, measure_snapshot and measure_publish, their unique keys and the frozen-row trigger in V1013__measures.sql. The deployment story replays the same sequence. |
| CDC-13490 | RWB-P9-E1013-OPS | GAP-0252 | not in chunk | Refresh cells and dimension rows for the 11 ACE-fed areas read from the rwb-source-data contract and snapshot(page) activity, not recovery.v_ace_* views; no view grant on rwb_reporting. |
| CDC-13492 | RWB-P9-E1013-OPS | GAP-0558 | not in chunk | Record AC3 and AC7 as superseded by DP-17: lake extract, trailer, Power BI feed and resend removed with no wave 1 replacement; publish and hold move to the ReportPublished event. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13480 | RWB-P9-E1013-OPS | DOR-RWB-P9-E1013-OPS-12 | 12.7, 16, 18 | Adds boundary test TC-P9-E1013-OPS-07 for the section 12.7 tables in section 16 and section 18 |
| CDC-13557 | RWB-P9-E2009-CON | DOR-RWB-P9-E2009-CON-12 | 12.7, 16, 18 | Add TC-P9-E2009-CON-01 to TC-P9-E2009-CON-09 to Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-13583 | RWB-P9-E2009-OPS | DOR-RWB-P9-E2009-OPS-12 | 12, 12.7, 16, 18 | Add TC-P9-E2009-OPS-01 to -07 to Test Cases v8; align the section 18 test lists of RWB-P9-E2009-OPS with RTM v7. |

### OTHER:FSD P9 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13544 | RWB-P9-E2009-CON | GAP-1646 | find it | Replace Power BI and data lake integration points in A2.1, A2.3, A2.4, A2.5, A2.7, A2.8 with the reporting read model on the gateway-bff route, and lake deliveries with files delivered by rwb-integration; rewrite AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01, AC-ALT-P9-004-01 to match. |
| CDC-13561 | RWB-P9-E2009-CON | GAP-1649 | n/a | Name the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE in AC-P9-001-01, AC-P9-003-01, AC-P9-008-01, AC-ALT-P9-003-01 and AC-ALT-P9-003-02; carry the count as an open question. |
| CDC-13576 | RWB-P9-E2009-OPS | GAP-1646 | none | Read every Power BI and data lake destination in A2.1 to A2.8 as the reporting read model on the gateway-bff route, and each lake delivery as a file delivered by rwb-integration. |

### RWB-P9-E8001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13623 | RWB-P9-E8001-APP | DOR-RWB-P9-E8001-APP-21 | header | Build RWB-P9-E8001-CON to Done and publish its contract before this story is ready. |
| CDC-13624 | RWB-P9-E8001-APP | DOR-RWB-P9-E8001-APP-22 | header | Publish the contract fake library and record its published version. |
| CDC-13631 | RWB-P9-E8001-APP | GAP-2583 | 4 | Define the closed eleven-member Measure answer with definitionVersion and frozen; additive filters within major version 1; pin consumed event names; consume and fake the P7 decision-log read; no file element; JOB-15 registration stays with the platform. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13413 | RWB-P9-E1013-APP | CG-ALL-7802 | 12.2 | Publish GET /api/recovery/source-data/v1/payments?accountId={accountId} through the rwb-source-data provider CON story (RWB-P1-E1013-APP). |
| CDC-13447 | RWB-P9-E1013-CON | CG-ALL-7814 | 12.2 | Publish GET /api/recovery/source-data/v1/payments?accountId={accountId} in rwb-source-data.yaml through the provider's CON story. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13424 | RWB-P9-E1013-APP | GAP-2567 | 12.2, 13 | Add the rwb-source-data payments read and freshness answer as consumed rows of RWB-P9-E1013-APP; keep the metadata as the plan states it. |
| CDC-13457 | RWB-P9-E1013-CON | GAP-2567 |  | Add the two rwb-source-data rows (payments since entry, daily completeness gate) to the wave dependency map. Keep the plan's C row as stated. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13428 | RWB-P9-E1013-APP | GAP-0563 | 12 | Fix the readiness, status and payments paths, the 202 response and the three status values, and the snapshot(page) cursor shape. Use the path names RWB-ITG-E1013-ITG already calls. |
| CDC-13460 | RWB-P9-E1013-CON | GAP-0563 | 12.2 | Fix paths for readiness, status and payments, the 202 answer and the three status values; field names follow P1 logical data model IDs. |

### OTHER:project-context.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13434 | RWB-P9-E1013-APP | GAP-0016 | n/a | Retire the v2 Case volume and Staff rows and carry the v5 Volume and Scale Forecast v3 figures (Architecture v5 slide 33). |
| CDC-13502 | RWB-P9-E1013-OPS | GAP-0016 | none | Retire the v2 Case volume and Staff rows and use the Volume and Scale Forecast v3 figures from Architecture v5. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13437 | RWB-P9-E1013-APP | GAP-0564 | n/a | Add the gate pair COMPLETE and HOLD to the list of values in the next TSD P1 version so one vocabulary per level is documented. |
| CDC-13470 | RWB-P9-E1013-CON | GAP-0564 | find it | Add the gate pair COMPLETE and HOLD to the list of values. Keep the stamp as LOADED or STALE per product and the gate as COMPLETE or HOLD per date. |

### OTHER:rwb-case message catalogue and SCR-44 screen specification (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13439 | RWB-P9-E1013-APP | GAP-2242 | 15 | Add one message for a held facts release to the rwb-case catalogue and name the release columns of SCR-44 in the screen specification. |
| CDC-13507 | RWB-P9-E1013-OPS | GAP-2242 | find it | Add one message for a held facts release and name the SCR-44 release state columns for the run state and the two counts. |

### OTHER:RWB-E6-037 and FSD P9 A2.6 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13482 | RWB-P9-E1013-OPS | GAP-2579 | find it | Confirm the benefit measure set, monthly business day and cut-off, month key in measure_snapshot, benefit screen and requirement ID; not specified in the source documents (GAP-2579). |
| CDC-13586 | RWB-P9-E2009-OPS | GAP-2579 | find it | Confirm the benefit-model measure set and its holder, the monthly business day and cut-off, the measure_snapshot month key, the benefit screen and the requirement ID. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13534 | RWB-P9-E2009-APP | GAP-3087 | find it | Record RWB-P9-E2009-APP as secondary serving of the steering data set in S8 with C RWB-P9-E2009-CON; add or confirm the S8-P9 REST and P9-S8 subscription edge; publish the seven consumed operations and owners. |
| CDC-13648 | RWB-P9-E8002-APP | GAP-1653 | find it | Add classification, staging and re-ageing to P9 scope; name the service holding the duty (case or source-data service); owner Solution architect. |

### OTHER:Recovery Workbench v3 workbook; OTHER:Read model sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13537 | RWB-P9-E2009-APP | GAP-0256 | 8 | Each row of the Read model sheet carries inbox dedupe, business-date order, the reopen-until-frozen rule and rebuild from retained topic history |
| CDC-13601 | RWB-P9-E2009-OPS | GAP-0256 | find it | Each row carries the inbox dedupe, the business-date order, the reopen-until-frozen rule and the rebuild from the retained topic history. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:FSD P3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13570 | RWB-P9-E2009-CON | GAP-0258 | find it | Replace the Power BI publication wording with consumption through rwb-reporting via GET /dashboards/{id} and GET /reports/{id}. |
| CDC-13602 | RWB-P9-E2009-OPS | GAP-0258 | find it | Replace the Power BI wording with consumption through rwb-reporting via GET /dashboards/{id} and GET /reports/{id}. |

### RWB-P9-E6037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13604 | RWB-P9-E6037-APP | DOR-RWB-P9-E6037-APP-21 | 14 | Set the build status to Done once the contract is published; it is currently Not started. |
| CDC-13605 | RWB-P9-E6037-APP | DOR-RWB-P9-E6037-APP-22 | 14 | Record a published contract fake library version. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13608 | RWB-P9-E6037-APP | CG-ALL-7876 | 12.5 | Add an Activities row for loadBenefitModel (Activity, task queue rwb-reporting), or name a catalogued activity. |
| CDC-13609 | RWB-P9-E6037-APP | CG-ALL-7877 | 12.5 | Add an Activities row for loadBenefitReadModel (Activity, task queue rwb-reporting), or name a catalogued activity. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13610 | RWB-P9-E6037-APP | CG-ALL-7878 | 12.5 | Add activity computeBenefit to the Activities sheet, or name a catalogued activity in place of it |
| CDC-13611 | RWB-P9-E6037-APP | CG-ALL-7879 | 12.5 | Add activity recordAndPublishBenefit to the Activities sheet, or name a catalogued activity in place of it |

### RWB-P9-E8002-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13643 | RWB-P9-E8002-APP | DOR-RWB-P9-E8002-APP-21 |  | Move build status from Not started to Done |
| CDC-13644 | RWB-P9-E8002-APP | DOR-RWB-P9-E8002-APP-22 |  | Publish a contract fake library version and record it |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13414 | RWB-P9-E1013-APP | CG-ALL-7803 | 12.5 | Add a row for MeasureRunWorkflow (one execution per business date; task queue rwb-reporting; namespace rwb-recovery) so the workflow is catalogued. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml; OTHER:rwb-case contract; OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13417 | RWB-P9-E1013-APP | DOR-RWB-P9-E1013-APP-8 | 12.2 | Publish GET /measure-definitions in rwb-reporting.yaml; publish GET /api/recovery/case/v1/cases/facts and the cases/{caseId} family in rwb-case; publish GET /api/recovery/source-data/v1/payments in rwb-source-data; publish the two further paths named by detcheck. |

### RWB-P3-E1013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13420 | RWB-P9-E1013-APP | DOR-RWB-P9-E1013-APP-7 | 11 | Replace legacy job and decision-log wording in its criteria and tests with the terms used in section 11 of this story. |

### OTHER:FSD P1 A2.12; OTHER:A2.19 and A2.20 (Data lake and Power BI integration points) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13421 | RWB-P9-E1013-APP | GAP-1499 | find it | Drop the Data lake integration points, the INT-19 extract in AC-ALT-P1-019-02 and the lake copy in A2.20 and AC-P1-020-01; reporting goes to the rwb-reporting snapshot and read model. |

### OTHER:Data model workbook v3 (Facts sheet, nine fact tables) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13422 | RWB-P9-E1013-APP | GAP-0251 | find it | Define the star schema as the read model in rwb_reporting fed from service topics; remove the data lake and Power BI landing; serve reports via GET /dashboards/{id} and GET /reports/{id} behind gateway-bff. |

### OTHER:FSD P9 AC-P9-001-01; OTHER:AC-P9-003-01; OTHER:AC-P9-008-01; OTHER:AC-ALT-P9-003-01 and AC-ALT-P9-003-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13423 | RWB-P9-E1013-APP | GAP-1649 | find it | Name the measure set as the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE; align the counts and carry the count as an open question. |

### OTHER:v3 workbook: Facts F5; OTHER:F7; OTHER:F8; OTHER:F9; OTHER:F11; OTHER:F13; OTHER:Dimensions B5; OTHER:B6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13426 | RWB-P9-E1013-APP | GAP-0252 | 8, 12.7 | Feed each ACE-fed row from the rwb-source-data contract snapshot(page) activity; no recovery.v_ace_* grant; P9 never reads ACE views. |

### OTHER:Recovery Workbench data model v3 (Facts; OTHER:Dimensions; OTHER:Measures) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13435 | RWB-P9-E1013-APP | GAP-0254 | n/a | Add an owner and schema to every fact, dimension and measure row from the Ownership Map (P9, rwb_reporting), and add the star schema schema. |

### OTHER:RWB-P1 FSD and TSD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13436 | RWB-P9-E1013-APP | GAP-0559 | n/a | In the next FSD and TSD versions of P1, mark the lake steps, the INT-19 row and lake_copy_watermark removed; keep the publish status of the case list and reconciliation result. |

### RWB-P9-E1013-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13441 | RWB-P9-E1013-APP | GAP-2574 | n/a | Keep alert thresholds, channels and owners as catalogue or values-file entries, take the 15-minute failed-run target from NFR-068, and name the caller of MSG-GEN-006 in the run book. |

### RWB-ITG-E1013-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13442 | RWB-P9-E1013-APP | NEWAC-RWB-P9-E1013-APP-AC9 | 5 | X3 row now names RWB-ITG-E1013-ITG as owner of AC6 |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13448 | RWB-P9-E1013-CON | DOR-RWB-P9-E1013-CON-8 | 12 | Publish the operations of CG-ALL-7810 to CG-ALL-7814 in their owner yamls; the contract check passes when they are in place. |

### OTHER:Recovery Workbench FSD P9 Reporting v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13449 | RWB-P9-E1013-CON | GAP-1646 | 8 | Read the Power BI and data lake integration points of A2.1, A2.3, A2.4, A2.5, A2.7 and A2.8 as the rwb-reporting read model on gateway-bff, and lake deliveries as files from rwb-integration; rewrite AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01 and AC-ALT-P9-004-01 to match. |

### OTHER:RWB-P3 screen stories for SCR-37 and SCR-44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13452 | RWB-P9-E1013-CON | DOR-RWB-P9-E1013-CON-10 | 18 | Add empty, loading, error and no-access states to SCR-37 and SCR-44. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13453 | RWB-P9-E1013-CON | DOR-RWB-P9-E1013-CON-12 | 16 | Add TC-P9-E1013-CON-01 to -06 to Test Cases v8 under the story; align the RTM v7 test lists to section 18. |

### OTHER:Recovery Workbench FSD P1 Reporting v3 (A2.12; OTHER:A2.19; OTHER:A2.20) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13454 | RWB-P9-E1013-CON | GAP-1499 | 8 | Drop the data lake copy and the INT-19 extract; serve results through the rwb-reporting snapshot activity and read model; confirm the output channel and six measure definitions with the data steward before wave 2. |

### OTHER:Recovery Workbench v3 workbook (Facts and Dimensions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13455 | RWB-P9-E1013-CON | GAP-0251 |  | Restate Facts!A2 so the star schema is the rwb_reporting read model fed from service topics, not a data lake for Power BI. Story-side read-model text is not in this chunk. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13463 | RWB-P9-E1013-CON | GAP-2577 | 12.5 | Publish v1 increment with the baselineValue delta, fixed dimension, eight subscriptions, JOB-15 registration contract and fakes; gate on contract tests and schema lint |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; OTHER:REQ-RDF-012 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13465 | RWB-P9-E1013-CON | CG-ALL-7819 | 18 | Align REQ-RDF-012 to section 18 of RWB-P9-E1013-CON; RTM lists TC-E1-013-02 (owned by RWB-ITG-E1013-ITG) and TC-E1-030-01, -02, -09 that the story does not |

### OTHER:project-context.md v2 (Case volume and Staff rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13466 | RWB-P9-E1013-CON | GAP-0016 |  | Retire the v2 volume rows and use the Volume and Scale Forecast v3 figures from Architecture v5 slides 33 and 48 |

### OTHER:Recovery Workbench data model v3 (Facts; OTHER:Dimensions; OTHER:Measures sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13467 | RWB-P9-E1013-CON | GAP-0254 | find it | Add Owner and schema values to every Facts and Dimensions row and an Owner column to Measures, taken from the Ownership Map (P9, rwb_reporting). |

### OTHER:FSD P1 and TSD P1 (next versions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13468 | RWB-P9-E1013-CON | GAP-0559 | find it | Mark the lake steps, the INT-19 row and lake_copy_watermark removed. Keep the publish status of the case list and the reconciliation result. |

### OTHER:RWB-E1-013 legacy story (P1 slice); RWB-P9-E1013-APP; RWB-ITG-E1013-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13469 | RWB-P9-E1013-CON | GAP-0562 | find it | Limit the P1 slice to facts and gate. Remove measure codes, definition versions, baseline values and totals; leave measure figures with APP and ITG. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; OTHER:RWB-E1-013 section 14; OTHER:integration story section 14 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13471 | RWB-P9-E1013-CON | GAP-0565 | find it | Use the FSD P1 and TSD P1 wording: '{product} is from {date}. Today's ACE batch has not arrived.' in the standard and in the legacy and integration copies. |

### OTHER:rwb-case message catalogue; OTHER:SCR-44 screen specification (JOB-15 run states) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13472 | RWB-P9-E1013-CON | GAP-2242 | find it | Add one message for a held facts release. Name the release state and the two count columns on SCR-44. Column names: Not specified in the source documents (GAP-2242). |

### OTHER:RWB-OPS story and JOB-15 run book (DevOps team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13473 | RWB-P9-E1013-CON | GAP-2574 | find it | Keep thresholds, channels and owners as catalogue and values-file entries. Name the caller of MSG-GEN-006 in the run book. Take the 15-minute target from NFR-068. |

### OTHER:FSD P9 Reporting v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13478 | RWB-P9-E1013-OPS | GAP-1646 | 18 | Read the Power BI and data lake destinations of A2.1, A2.3, A2.4, A2.5, A2.7 and A2.8 as the rwb-reporting read model on the gateway-bff route; read lake deliveries as files delivered by rwb-integration; rewrite AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01 and AC-ALT-P9-004-01 to match |

### OTHER:Functional Specification P1 and P9 (A2.12; OTHER:A2.19; OTHER:A2.20) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13481 | RWB-P9-E1013-OPS | GAP-1499 | find it | Remove the data lake and INT-19 extract from A2.12, A2.19 and A2.20; serve reconciliation, freshness and measures via rwb-reporting. Story already states no lake path (section 11, BR5). |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13484 | RWB-P9-E1013-OPS | GAP-0255 | find it | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate; state that queue measures stay with P3 rwb_case. |

### OTHER:WP B2-P9-001 (plan) and story section 12.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13488 | RWB-P9-E1013-OPS | GAP-2567 | find it | Add the two rwb-source-data rows (payments read, freshness answer) to the wave dependency map; declare them and the two rwb-case rows as class C in section 12.2 with their fakes. |

### RWB-P9-E1013-APP; RWB-P3-E1013-APP; RWB-P1-E1013-APP; RWB-ITG-E1013-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13493 | RWB-P9-E1013-OPS | GAP-0560 | not in chunk | Assign AC1, AC4, AC5, AC8 to RWB-P9-E1013-APP; AC2 and AC6 to RWB-ITG-E1013-ITG; case facts to RWB-P3-E1013-APP; readiness, gate, payments, events, activities and JOB-04 to RWB-P1-E1013-APP; AC3 and AC7 removed by DP-17. |

### OTHER:P1 OpenAPI document of the epic contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13494 | RWB-P9-E1013-OPS | GAP-0563 | 12 | Fix the readiness, status and payments paths, the 202 answer and the three status values; field names follow the P1 logical data model. Exact paths Not specified in the source documents (GAP-0563). |

### RWB-P1-E1013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13495 | RWB-P9-E1013-OPS | GAP-1503 | not in chunk | Confirm the frozen baseline is not written back to rwb-source-data; rwb-reporting alone publishes and freezes it. |

### RWB-P9-E1013-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13497 | RWB-P9-E1013-OPS | GAP-2240 | 12 | Publish the catalog read as GET on the rwb-reporting base with an onDate parameter. |

### OTHER:Recovery Workbench Facts; OTHER:Dimensions and Measures workbook v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13503 | RWB-P9-E1013-OPS | GAP-0254 | find it | Add Owner and schema columns to Facts, Dimensions and Measures with P9 rwb-reporting and schema rwb_reporting, values from the Ownership Map. |

### OTHER:FSD P1 and TSD P1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13504 | RWB-P9-E1013-OPS | GAP-0559 | find it | Mark lake steps, INT-19 row and lake_copy_watermark removed in next versions; keep case list and reconciliation publish status. |

### OTHER:P1 TSD next version, list of values (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13505 | RWB-P9-E1013-OPS | GAP-0564 | find it | Add the gate pair COMPLETE and HOLD to the list of values beside LOADED and STALE so each level has one vocabulary. |

### OTHER:03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P9 R (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13514 | RWB-P9-E2009-APP | GAP-1646 | 12 | Replace the Power BI and data lake destinations in A2.1, A2.3, A2.4, A2.5, A2.7 and A2.8, and in AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01 and AC-ALT-P9-004-01, with the reporting read model served on the gateway-bff route. Each lake delivery becomes a file delivered by rwb-integration. |

### OTHER:RWB-E6-037 benefit realisation story (FSD P9 A2.6; OTHER:TSD P9 T3.1 and T3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13522 | RWB-P9-E2009-APP | GAP-2579 |  | Confirm the benefit-model measure set and its membership, the monthly business day and cut-off, the measure_snapshot month key, the benefit screen, and the requirement ID. None is in the source documents (GAP-2579). |

### OTHER:Star schema workbook v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13523 | RWB-P9-E2009-APP | GAP-0251 | find it | Facts!A2 to name the star schema as the read model in rwb_reporting (P9), fed from service topics, served via GET /dashboards/{id} and GET /reports/{id} behind gateway-bff, with no data lake or Power BI connection |

### OTHER:Star schema workbook v3 (Measures) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13524 | RWB-P9-E2009-APP | GAP-0255 | find it | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate, and stating that queue measures stay with P3 rwb_case |

### OTHER:Star schema workbook v3 (Dimensions and Facts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13525 | RWB-P9-E2009-APP | GAP-0257 | find it | dim_org and fact_case_daily key owner and team by ID; display name resolved from P3 queue_member and assignment behind the rwb-access masking policy; no personal data on an event |

### OTHER:Open question register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13526 | RWB-P9-E2009-APP | GAP-1649 | 7 | AC1 Then line no longer states a count or a ten-code list; it refers to the published set. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13530 | RWB-P9-E2009-APP | GAP-0731 |  | Record the case-fact read schema, cut-off rule and case-fact event projection agreed with the rwb-reporting owner, including the 01:30 measure-run transport. |

### OTHER:BRD Program v5 and the PRDs of rwb-case and rwb-payment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13531 | RWB-P9-E2009-APP | GAP-1563 | 11 | Name the P3 duty (matched payment and unmatched exception visible on the case) and the P8 duty (the matching rule) in both PRDs and the BRD row. |

### RWB-P9-E2009-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13532 | RWB-P9-E2009-APP | GAP-2578 |  | Ship chart with api and worker, migration increment, Schedule, eight consumer groups, six alerts with runbook links, four series, flag, backfill and rollback; take all thresholds and limits as environment values; allocate the missing run message ID. |

### OTHER:Reporting owner (replacement path) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13533 | RWB-P9-E2009-APP | GAP-3088 | 11 | INT-19 extract dropped from this slice; freshness stamp kept for SCR-37; Power BI path moved to the read model. |

### OTHER:Recovery Workbench facts workbook v3 (sheet Facts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13536 | RWB-P9-E2009-APP | GAP-0253 | find it | Set refresh cells F6, F10, F12 and F13 to event-fed projections with the 01:30 JOB-15 publish and a rerun for any business date. |

### OTHER:Functional Specification P9 (FSD P9); OTHER:SCR-37 row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13539 | RWB-P9-E2009-APP | GAP-1658 |  | Name rwb-reporting as owner and serving service of SCR-37 and its dashboard data set, served on its resources behind the gateway-bff route |

### OTHER:Legacy RWB-E2-009 (sections 4; OTHER:12; OTHER:13; OTHER:14; OTHER:15) and the owning teams' sources (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13540 | RWB-P9-E2009-APP | GAP-3090 |  | Publish the schedule id, calendar, catch-up policy, rerun input, two Measure fields, dimension format and alert channel and recipients; read the three filter lists as rwb-case reference data at their version |

### OTHER:P3 screen specification (SCR-37; OTHER:SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13556 | RWB-P9-E2009-CON | DOR-RWB-P9-E2009-CON-10 | none (no screen section in story) | Add empty, loading, error and no-access states to SCR-37 and SCR-44. |

### OTHER:RWB-E2-009 (legacy story) section 14 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13559 | RWB-P9-E2009-CON | DOR-RWB-P9-E2009-CON-9 | 14 | Supply English text for MSG-P9-002, MSG-P1-001, MSG-GEN-003, MSG-P4-002, MSG-GEN-006, MSG-P7-003; confirm each ID's meaning against the message standard. |

### OTHER:rwb-reporting API yaml and its ownership row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13560 | RWB-P9-E2009-CON | GAP-0251 | 11 | Add GET /dashboards/{id} and GET /reports/{id} behind gateway-bff only if the ownership row carries them. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13563 | RWB-P9-E2009-CON | GAP-1563 | n/a | Name the P3 duty (exception visibility on the case) and the P8 duty (the matching rule) in both PRDs. |

### OTHER:rwb-reporting deployment chart and runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13564 | RWB-P9-E2009-CON | GAP-2578 | n/a | Ship the chart, migration, Schedule, eight consumer groups, six alerts, four series, flag, backfill and rollback with every threshold and limit as an environment value; allocate the run alert message ID with the catalogue owner. |

### OTHER:Connection matrix and split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13565 | RWB-P9-E2009-CON | GAP-3087 | 3 | Add the S8 REST call to P9 and the P9 subscription to S8 for the steering data set; keep the rwb-deviation H row empty. Story side recorded in section 3. |

### OTHER:Data model v3 (Facts sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13568 | RWB-P9-E2009-CON | GAP-0253 | find it | Replace the nightly and monthly refresh wording with event-fed projections, the 01:30 publish (JOB-15), a rerun for any business date and the hold when the dashboard count does not reconcile. |

### OTHER:Data model v3 (Read model sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13569 | RWB-P9-E2009-CON | GAP-0256 | find it | Each row carries the inbox dedupe, business-date order, reopen-until-frozen rule and rebuild from retained topic history. |

### OTHER:Workflow kit, reporting owner, rwb-comms contract and rwb-case reference data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13571 | RWB-P9-E2009-CON | GAP-3090 | 8 | Publish the JOB-15 schedule id, calendar, catch-up policy and rerun input; publish the two Measure fields and dimension format; confirm the alert channel and two recipients; hold the three filter lists as rwb-case reference data. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P9 rwb-reporting (Reporting)/RWB P9 E2009 APP Steering (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13582 | RWB-P9-E2009-OPS | DOR-RWB-P9-E2009-OPS-10 | none in this story | Add empty, loading, error and no-access states for SCR-37 and SCR-44. SCR-37 states are in legacy RWB-E2-009 section 15. SCR-44 states: Not specified in the source documents (DOR-RWB-P9-E2009-OPS-10). |

### OTHER:Message catalogue (owner standard) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13585 | RWB-P9-E2009-OPS | DOR-RWB-P9-E2009-OPS-9 | 14 | Supply English text for MSG-P9-002, MSG-P1-001, MSG-GEN-006, MSG-P7-003, MSG-P4-002 and the run alert, and align their meanings with the standard. |

### OTHER:Recovery Workbench data model v3 (Facts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13587 | RWB-P9-E2009-OPS | GAP-0251 | find it | Restate the nine fact tables as the rwb_reporting read model fed from service topics, served via GET /dashboards/{id} and GET /reports/{id}; remove the data lake and Power BI feed. |

### OTHER:Recovery Workbench data model v3 (Dimensions; OTHER:Facts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13589 | RWB-P9-E2009-OPS | GAP-0257 | find it | Key owner and team by ID from events; resolve display names from P3 queue_member and assignment behind the rwb-access masking policy; no personal data on events. |

### RWB-P9-E2009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13592 | RWB-P9-E2009-OPS | GAP-2576 | find it | Declare the three consumed operations and two owner-queue activities; replay the day's events into a run-scoped read model; hand the published extract to rwb-integration as the INT-19 replacement; take agent rates from EV-28 and RWB-P10-E1063-CON. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:case CON story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13594 | RWB-P9-E2009-OPS | GAP-0731 | find it | Record the case-fact read schema, the cut-off rule and the fact transport agreed with the rwb-reporting owner, and the case-fact event projection. |

### OTHER:BRD Program v5 section 11; OTHER:P3 and P8 PRDs (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13595 | RWB-P9-E2009-OPS | GAP-1563 | 11 | Name the P3 duty (exception visibility on the case) and the P8 duty (the matching rule) for REQ-CHO-009 in both PRDs. |

### RWB-S8-E2009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13596 | RWB-P9-E2009-OPS | GAP-3089 | find it | Keep acs empty; restate AC1 to AC9 as new (D-RCV-60) with legacy values; carry TC-E2-009-01 to -10 unchanged, map -10 to access refusal, record in section 18. |

### RWB-S8-E2009-APP; OTHER:Connection matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13597 | RWB-P9-E2009-OPS | GAP-3087 | find it | Keep plan service, lane, C row and empty H row; record secondary serving of the steering data set; publish seven consumed operations with owners; confirm load-time edge with P9 and S8 owners. |

### OTHER:Recovery Workbench v3 workbook; OTHER:Facts sheet (F6; OTHER:F10; OTHER:F12; OTHER:F13) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13600 | RWB-P9-E2009-OPS | GAP-0253 | find it | Replace the nightly Workbench load wording with event-fed projections, the 01:30 publish as JOB-15 and a rerun for any business date; measure_publish decides publish or hold. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13603 | RWB-P9-E6037-APP | CG-ALL-7875 | 12.5 | Add a Workflows row for reportingMeasuresDaily (JOB-15, owned by RWB-P9-E2009-APP), or confirm the catalogued workflow name it uses. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows and Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13606 | RWB-P9-E6037-APP | DOR-RWB-P9-E6037-APP-8 | 14 | Add rows for reportingMeasuresDaily (JOB-15), loadBenefitModel, loadBenefitReadModel, computeBenefit and recordAndPublishBenefit, or catalogued equivalents for the detcheck failures. |

### OTHER:FSD P9 A2.1 and A2.7.2; OTHER:TSD P9 T5.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13630 | RWB-P9-E8001-APP | GAP-2584 | 8 | Keep INT-19 and the Power BI and data lake points as a documented retirement, not a target. Story side fixed in BR3: read through GET /reports/measures, no file or lake copy. |

### OTHER:Feature list entry FEAT-RPT-07 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13633 | RWB-P9-E8001-CON | GAP-1481 | 4 | Read FEAT-RPT-07 from the reporting read model and the central decision log, with no data lake; keep requirement ID and measure unchanged |

### OTHER:P3 screen specification for SCR-37 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13637 | RWB-P9-E8001-CON | DOR-RWB-P9-E8001-CON-10 | header | Add empty, loading, error and no-access states for SCR-37 |

### OTHER:FSD P9 A2.7.2 and A2.1; OTHER:TSD P9 T5.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13640 | RWB-P9-E8001-CON | GAP-2584 | 4 | Keep the INT-19 rows, the Power BI copy and the data lake integration points as a documented retirement, not a target, per Architecture v5. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20854 | RWB-P9-E1013-CON | R-28487 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09171', 'R-22565', 'R-28487'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0016 | Volumes differ between the v2 context and v5 | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0251 | The nine fact tables are defined in a data lake; the target has no data lake | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0252 | The reporting layer reads recovery.v_ace_* views directly | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0253 | The refresh wording has no schedule in the target | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0254 | No fact, dimension or measure carries an owner or a schema | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0255 | The read-model control tables and the queue measures are absent | Data architecture team | Resolved (directive) |
| GAP-0256 | No late-arrival, freeze or replay rule on any fact table | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0257 | dim_org holds an owner while events carry no personal data | Data steward | Resolved (directive) |
| GAP-0258 | The LDM and the FSD still publish to Power BI, which is removed | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0339 | E1013 integration path after the data-lake removal | Solution architect | Resolved (directive) |
| GAP-0391 | Gateway-bff composite steering route, harness environment, measure-day seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0558 | DP-17 removes the INT-19 lake extract and the Power BI feed that legacy AC3 and AC7 assert | Business analyst, P1 and P9 | Resolved (directive) |
| GAP-0559 | The P1 functional and technical specifications still describe the lake publish that DP-17 removes | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0560 | RWB-E1-013 is split across four stories and no single source assigns each legacy acceptance criterion | Business analyst, P1, P3 and P9 | Resolved (directive) |
| GAP-0561 | The 05:30 late check and the worker and queue registration have no story in the build dependencies of this slice | DevOps team and platform workflow owner | Resolved (directive) |
| GAP-0562 | No measure value, definition or snapshot is produced or read by the P1 slice of RWB-E1-013 | Business analyst, P1 and P9 | Resolved (directive) |
| GAP-0563 | The readiness and status operation shapes are fixed only in part by the architecture text | Solution architect and TechX contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0564 | The gate answers COMPLETE or HOLD while the freshness list of values holds LOADED and STALE | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0565 | MSG-P1-001 now names the ACE batch where the legacy story and the integration copy name a load | Business analyst, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0731 | Case-fact read shape, cut-off rule and the reporting hand-off are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1481 | The regulatory return feature names a data lake that the target architecture removes | Solution architect | Resolved (directive) |
| GAP-1499 | The data lake and the dashboard connection are removed, so the reporting destinations of three FSD features have no home | Solution architect | Resolved (directive) |
| GAP-1503 | The baseline measure job has two owners, one in the FSD and one in the architecture | Center of excellence | Resolved (directive) |
| GAP-1563 | The BRD assigns payment matching to rwb-case while Architecture v5 gives it to rwb-payment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1646 | The data lake and the Power BI connection are removed but the whole reporting FSD is built on them | Solution architect | Resolved (directive) |
| GAP-1649 | The measure set is six definitions in one acceptance criterion and seven measures in another | Tribe lead with the Reporting and BI analyst | Resolved (directive) |
| GAP-1653 | Classification, staging and re-ageing sit in P9's FSD but not in the architecture's P9 scope | Solution architect | Resolved (directive) |
| GAP-1657 | The regulatory extract has no agreed source after the data lake is removed | Solution architect | Resolved (directive) |
| GAP-1658 | SCR-37 has no owner and no serving path | Solution architect | Resolved (directive) |
| GAP-1662 | RWB-E2-009 promises a Power BI data set, which ADR-018 removes | Solution architect | Resolved (directive) |
| GAP-2239 | The case-facts REST operation of rwb-case is not in the API Specification or the ownership map | TechX, with the API owner of P3 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2240 | The measure-catalog read of rwb-reporting has no path or shape in the sources | TechX, with the API owner of P9 reporting | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2241 | The list code and the table code of the age-band reference list are not named | TechX, with the data steward RW-DATASTEW | Resolved (directive) |
| GAP-2242 | No message is defined for a held facts release, and SCR-44 shows no release state | TechX, with the data steward RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2566 | RWB-E1-013: DP-17 removes the data lake while the two criteria this service owns assert the INT-19 extract, its trailer and the lake hold | Solution architect | Resolved (directive) |
| GAP-2567 | RWB-E1-013: the plan's C row names two rwb-case contracts and omits the two rwb-source-data rows the run consumes | Solution architect | Resolved (directive) |
| GAP-2568 | RWB-E1-013: the definition load of table measure_definition has no target operation, because the table is P9's while the reference-load framework is rwb-case's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2569 | RWB-E1-013: the Ownership Map gives rwb-reporting no event while the wave 1 harness names rwb.reporting.ReportPublished.v1 on the service topic | Solution architect | Resolved (directive) |
| GAP-2570 | RWB-E1-013: the Power BI refresh that AC3 asserts has no mechanism once the data lake is removed, and the measures read is assigned to Epic 2 by the legacy story | Solution architect | Resolved (directive) |
| GAP-2571 | RWB-E1-013: the approver of a definition is typed uuid by the TSD while the legacy criteria and the FSD name the reference TRB-0001 | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2572 | RWB-E1-013: no source gives the path or the shape of the definitions read that RWB-P3-E1013-APP consumes across the service boundary | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2573 | RWB-E1-013: JOB-15 has two candidate triggers, the Temporal Schedule of DP-10 and the Airflow chain that triggers report extracts | Solution architect | Resolved (directive) |
| GAP-2574 | RWB-E1-013: the alert thresholds, the channel names and the run-book identifiers of JOB-15 have no source, and MSG-GEN-006 loses its caller with the lake | DevOps team | Resolved (directive) |
| GAP-2575 | RWB-E1-013: the three measure tables' DDL sits with no DB story of this key, so the app story's migration carries it | ACE team | Resolved (directive) |
| GAP-2576 | rwb-reporting steering dashboard (application slice): the consumed operation names, the workflow and activity names, the read-model design, the INT-19 replacement and the agent fact source are fixed by no single source | Solution architect, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the reporting service | Resolved (directive) |
| GAP-2577 | rwb-reporting steering dashboard (contract slice): the element names of the consumed declarations, the event envelope naming, the Measure delta, the schema increments and the file shape of the extract are fixed by no single source | Contract owner of rwb-reporting, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the event platform | Resolved (directive) |
| GAP-2578 | rwb-reporting steering dashboard (deployment slice): the login and secret reference, the replica and threshold values, the consumer offset and retention policy, the catch-up window, the backfill limit and the message ID of the run alert are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2579 | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-2580 | Benefit realisation: the variance fields, the variance rule, the row ceiling, the event absence and the baseline date default are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-2582 | RWB-E8-001 app slice: the step name inside JOB-15, the return layout, the decision code, the texts of MSG-P9-002 and MSG-P9-003 and the fate of the legacy document and rule entities are not fixed by any source | Tech lead of rwb-reporting with the solution architect and the reporting owner | Resolved (directive) |
| GAP-2583 | RWB-E8-001 contract slice: the answer member names and page limits, the decision code, the consumed event names beyond the first, the additive query filters, the decision-log read element and the Schedule registration detail are not fixed by any source | Tech lead of rwb-reporting with the owners of rwb-decision and gateway-bff | Resolved (directive) |
| GAP-2584 | The data lake and Power BI copy of the regulatory return (INT-19) is named by the FSD and the TSD and removed by Architecture v5 | Solution architect with the reporting owner and the BI owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2585 | RWB-E8-002: the source and member names of the classification rule set, the name of the upstream reclassification event, the step name inside JOB-15, the decision reference of the record and the place the reported classification is held are not fixed by any source | rwb-reporting service owner with the rule registry owner of rwb-decision and the source-data owner of rwb-source-data | Resolved (directive) |
| GAP-3087 | RWB-S8-E2009-APP: a P9 Reporting story is placed in rwb-deviation with one C row and an empty build row, and the seven owner reads, the matrix edge and the platform prerequisites are unpublished | Solution architect | Resolved (directive) |
| GAP-3088 | RWB-S8-E2009-APP: DP-17 removes the data lake, so the INT-19 extract and the Power BI data set of the story have no target owner and no replacement path in this service | Solution architect | Resolved (directive) |
| GAP-3089 | RWB-S8-E2009-APP: the plan assigns the slice no legacy acceptance criterion while it keeps ten legacy test cases, and the legacy criteria lose their owned ids | Solution architect | Resolved (directive) |
| GAP-3090 | RWB-S8-E2009-APP: the schedule time, the dimension format, the two added Measure fields and the alert recipients have no published values for the deviation serving | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P9-E1013-CON | skipped AC ID | 95 | missing: AC7, AC8 |
| RWB-P9-E1013-CON | new AC without TC row | 374 | AC9 is new and no section 16 row covers it |
| RWB-P9-E6037-CON | new AC without TC row | 364 | AC10 is new and no section 16 row covers it |
