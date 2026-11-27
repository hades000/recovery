# RWB-SVC-S8 rwb-deviation (Deviation) - review pack, part 1 of 3 (RWB-S8-E1020-APP to RWB-S8-E2029-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 248 |
| Cross-document (pending in another document) | 196 |
| Not applied (value not in the sources) | 18 |
| Open business decisions | 38 |
| Register gaps linked | 140 |
| Unconfirmed assumptions | 0 |
| Lint findings | 6 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S8-E1020-APP | 32 | 27 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E1020 APP Allocation and assignment engine v1 v2.md |
| RWB-S8-E1021-APP | 37 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E1021 APP Transfer rules and engine v1 v2.md |
| RWB-S8-E1023-APP | 26 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E1023 APP Case record view v1, read only v2.md |
| RWB-S8-E1062-APP | 19 | 28 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E1062 APP Deviation screening agent in shadow [E2b] v2.md |
| RWB-S8-E1065-APP | 23 | 29 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E1065 APP Sandbox database with synthetic recovery data v2.md |
| RWB-S8-E2009-APP | 25 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E2009 APP Steering dashboard v1 data set v2.md |
| RWB-S8-E2012-APP | 32 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E2012 APP Manual transfer and reassignment screen with reason v2.md |
| RWB-S8-E2015-APP | 26 | 19 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E2015 APP Timers, escalation and the deviation flag on the case record view v2.md |
| RWB-S8-E2029-APP | 28 | 12 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E2029 APP Deviation screening agent evaluation and L1 on one segment [E3b] v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S8-E1065-APP | R-03026 | CG-ALL-11319 | Script gap | Product owner | The story adds DEV_FLAGGED to the closed list LOV-RAISED-BY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S8-E2029-APP | R-03039 | CG-ALL-11370 | Script gap | Product owner | The story adds DEV_FLAGGED to the closed list LOV-DEVIATION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S8-E2029-APP | R-03040 | CG-ALL-11371 | Script gap | Product owner | The story adds DEV_FLAGGED to the closed list LOV-RAISED-BY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S8-E1020-APP | R-13349 | CG-ALL-11272 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E1062-APP | R-13363 | CG-ALL-11314 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E2015-APP | R-13381 | CG-ALL-11364 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E2029-APP | R-13384 | CG-ALL-11377 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-22002 | GAP-0685 | Register gap | Business owner; reference data administrator | The source of the caseload cap is not fixed: parameter row or reference data | Keep the cap as versioned reference data on queue.capacity_cap and queue_member.capacity, as the legacy data model does, and add a parameter key only if a product-level override is wanted; state the ruling in the Reference Data and Parameters design. |
| RWB-ITG-E1021-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-22012 | GAP-3078 | Register gap | P7 rwb-decision owner with the business owner of module S8 | The TRANSFER rows that fire on the deviation triggers and the text of R-DEV-04 to R-DEV-06 are not published | The rule owner publishes the DEV transfer rows and the text of R-DEV-04 to R-DEV-06 with the package version; the story then reads them unchanged and no code changes. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1039-APP, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22216 | GAP-2330 | Register gap | Internal audit role and the solution architect, P4 | The access entry of an agent read has no source row, element list or decision-code vocabulary of its own | Fix the entry members of a non-human read in the access-entry writer of RWB-P4-E1039-APP and publish them once for every service identity, so an audit query by agent code and policy version answers from the same chain as the screen entries. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22221 | GAP-2328 | Register gap | Compliance and PDPA officer and the security administrator role | Which of the run's fields are personal for a non-human actor, and the mask format served to an agent, are not specified | Fix the personal field list of the four agent reads and the mask format served to a non-human caller with the masking owner, load it as a masking version rather than as code, and prove it with a synthetic value that must appear in no answer, no log and no span. |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22435 | GAP-1663 | Register gap | Solution architect with the AI product owner | No event source is named for the agent acceptance and override measures | Count the two rates from the decision record, which carries the agent and prompt version, the recommendation, the approval and the outcome |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22439 | GAP-3178 | Register gap | Reporting and BI lead with the data product owner | RWB-E2-009 writes an INT-19 extract for a data lake that the target removes | Name the read model or event topic the Power BI data set subscribes to after the data lake removal, and update the acceptance criteria of RWB-E2-009 once. |
| RWB-ITG-E2015-ITG, RWB-ITG-E7006-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON | R-22499 | GAP-1827 | Register gap | Business lead | The deviation service level is 'set with DL22' and has no number, and the ten working day escalation comes only from the design | Carry the service level, the escalation period and the skip trace window as versioned reference data read at run time, assert no number, and take the values from DL22 when the business lead sets them. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22503 | GAP-0935 | Register gap | Business lead | Precedence between a role's default scope and an escalation grant is not specified | Rule that the wider of the two scopes is named, that the reason ESCALATED_TO_ROLE is carried while the escalation is open, and that the grant never exceeds Case record R on that one case. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22504 | GAP-0936 | Register gap | Compliance and PDPA officer | The masking version in force for SIT and the answer when two versions overlap are not specified | Record MASK-SIT-01 as the SIT version in the policy pack, and rule that the version with the latest valid_from on or before the business date is used, the answer naming the version it used. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22506 | GAP-3099 | Register gap | Solution architect, with the rwb-deviation owner, the rwb-case contract and reference-data owners, the product owner of the deviation service level, the rule-set owner of the Deviations package and the QA lead | RWB-S8-E2015-APP: the deviation section of the case record view has no read operation, no published view field names, no label for a code other than X3, no published value for the deviation service level and no escalation target | Publish the case deviation read as a service operation with a catalogue row, or amend the Ownership Map to carry GET /cases/{caseId}/deviations; freeze the deviation view field names in RWB-P3-E2015-CON; publish LOV-DEVIATION with a label per code and LOV-DEV-OUTCOME with a label per value; publish the deviation service level, its calendar and the row that holds it; publish the escalation target and the codes R-DEV-20 covers; record the six platform contracts as template dependencies of S8 beside the H row of the secondary slice; publish a level for each legacy test case. |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-ITG-E2029-ITG, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P7-E2029-APP, RWB-S8-E2029-APP | R-22656 | GAP-1828 | Register gap | Risk and model risk officer | The confidence threshold for the low-confidence review and the evidence required to run the agent at L1 are not stated | Read the threshold and the autonomy policy from versioned reference data held by rwb-agent and rwb-decision, assert no number, and leave the evidence pack and the approval of a level change to Q-014 and BR-084. |
| RWB-ITG-E1013-ITG, RWB-ITG-E2009-ITG, RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E2009-APP, RWB-P9-E1013-APP, RWB-P9-E1013-CON, RWB-P9-E1013-OPS, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-P9-E8001-APP, RWB-P9-E8001-CON, RWB-P9-E8002-APP, RWB-P9-E8002-CON, RWB-S8-E2009-APP | R-28480 | GAP-1644 | Register gap | Business lead | The program BRD has no requirement section for P9 reporting | Keep the epic-level keys as the trace target and state the coverage basis in section 11.2 until a P9 requirement section exists |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-28522 | GAP-0686 | Register gap | Business owner, Shared operations; platform team, Temporal | The exact cadence of the rebalancing trigger is not defined for rwb-case | Run JOB-06 as its own Temporal Schedule at 06:30 Asia/Bangkok, after DailyCaseRun has finished, with overlap policy SKIP and a catch-up window; confirm the order with the operations owner and record it in the Temporal Workflow and Activity Catalog. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1023-ITG, RWB-ITG-E2016-ITG, RWB-P3-E1023-APP, RWB-P3-E1023-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P4-E1023-APP, RWB-P5-E2016-APP, RWB-S8-E1023-APP | R-28538 | GAP-1577 | Register gap | Business analyst with the P3 product owner | The case record view and its history timeline are listed as P4 features while the screen and its endpoints belong to rwb-case | Move FEAT-ACA-11 and FEAT-ACA-12 with their acceptance criteria to FSD P3 in the next version, and leave in FSD P4 only the authorise, scope and masking behaviour the screen consumes, so each feature has one owner and one acceptance set. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-28752 | GAP-1659 | Register gap | Risk and model risk officer | No target is set for agent acceptance and override | Publish the two rates per agent and version and set no threshold until one is agreed |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28761 | GAP-3094 | Register gap | Business lead | The handler rows R-DEV-04 to R-DEV-06 and the SCR-05 deviation fragment layout are not in the sources | Read the four rows from the Business Rules and Routing Logic workbook at build time, render the fragment as a table of code, handler, paused state, contact stop and rule ID, and confirm the layout with the screen owner. |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28763 | GAP-3097 | Register gap | Business lead | The transfer reason codes R01 to R06 are an assumed set pending DL23 | Read the list at its version on the rwb-case reference-data contract, render whatever is in force, and hold the six codes as the default set until DL23 closes. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-S8-E1021-APP | R-38772 | ASM-5239 | Register assumption |  | The TRANSFER package is read at its version in force, TRF-2026.11 or later, and its DEV trigger rows and row order are data of rwb-decision. The tests use the rule IDs and queues the legacy story publishes (TRF-001 to TRF-009 and the named queues) as package data, and no row, row order or target queue is written in code. The text of R-DEV-04 to R-DEV-06 is stated as a placeholder in the rule table until the rule owner publishes it. | The P7 rwb-decision owner and the business owner of module S8 at the release date |
| RWB-S8-E2012-APP | R-38811 | ASM-5283 | Register assumption |  | The conditions, actions and target owners of R-DEV-04 to R-DEV-06 come from the Business Rules and Routing Logic workbook at build time, and the SCR-05 deviation fragment is rendered as a table of code, handler, paused state, contact stop and rule ID, with the refusal message beneath it and the cleared row shown as history. | Business lead and the screen owner |
| RWB-S8-E2012-APP | R-38814 | ASM-5286 | Register assumption |  | LOV-TRANSFER-REASON carries R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue as the intended set pending DL23, read at its version on the rwb-case reference-data contract and never written in code. | Business lead when DL23 closes |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S8-E1020-APP | R-21073 | DOR-RWB-S8-E1020-APP-11 | 14 | Definition of Ready item 11 Guardrails: Partial | No detcheck report names the flagged P2 field, so it cannot be identified without guessing. Story §14 (line 438) already states no personal data is carried. |
| RWB-S8-E1020-APP | R-27729 | CG-ALL-11273 | 3 | Flyway file V1020_1__placement_indexes.sql is not in the V0001..Vnnnn form | Next free Flyway number of rwb-deviation is not in sources; only V0001 is named (Service Template Spec v1 §3). Story line 383 left unchanged. |
| RWB-S8-E1021-APP | R-21081 | DOR-RWB-S8-E1021-APP-10 | 12.7 | Definition of Ready item 10 Screens and states: Partial | SCR-02, SCR-03 and SCR-05 state lines sit in 12.7 (L401-411), not in the supplied parts. Re-supply that text to add the states. |
| RWB-S8-E1023-APP | R-21091 | DOR-RWB-S8-E1023-APP-18 | Not in chunk | Definition of Ready item 18 Open decisions: Partial | The section holding open decision DL26 is outside this chunk. Its text cannot be copied as old, so no edit was made. |
| RWB-S8-E1062-APP | R-21100 | DOR-RWB-S8-E1062-APP-11 | none | Definition of Ready item 11 Guardrails: Partial | No personal-data classification of the P2 fields is in the sources; grep finds only generic PRD P2 BR-P2-003. Not specified in the source documents (DOR-RWB-S8-E1062-APP-11). |
| RWB-S8-E1062-APP | R-21104 | DOR-RWB-S8-E1062-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR1, BR2, BR4 to BR8 need section 7 ACs and section 16 TCs, which are outside this chunk. BR IDs for the R-DEV rows would be invented. |
| RWB-S8-E1062-APP | R-27747 | CG-ALL-11315 | 3, 3.1 | Flyway file V1062_1__screening_deviation_read.sql is not in the V0001..Vnnnn form | The next free rwb-deviation Flyway number is not in the sources; Service Template Spec v1 section 3 names only V0001. Not specified in the source documents (CG-ALL-11315). |
| RWB-S8-E1062-APP | R-33045 | NEWAC-RWB-S8-E1062-APP-AC10 | 5 | AC10: §5 X2: The `caseId` query is absent or is not a case reference (covered by 'Section 14' only) | Section 7 is outside this chunk, so the AC10 criterion and its test row cannot be inserted. Proposed test data Not specified in the source documents (NEWAC-RWB-S8-E1062-APP-AC10). |
| RWB-S8-E1062-APP | R-33046 | NEWAC-RWB-S8-E1062-APP-AC11 | 7 | AC11: §5 X3: The reference-data or the package read does not answer inside the budget, or the registry has no package version in forc (covered by 'Section 14' only) | Section 7 tail and section 16 table are not in the chunk, so no exact anchor exists. The current story is not on disk (4-applied v2 has no AC13). AC11 is free. Needs current text. |
| RWB-S8-E1062-APP | R-33047 | NEWAC-RWB-S8-E1062-APP-AC12 | 7 | AC12: §5 X6: The rwb-agent policy read does not answer, so the mode in force is unknown (covered by 'Section 14' only) | Section 7 tail and section 16 table are not in the chunk, so no exact anchor exists. The current story is not on disk (4-applied v2 has no AC13). AC12 is free. Needs current text. |
| RWB-S8-E2009-APP | R-08809 | DOR-RWB-S8-E2009-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-S8-E2009-APP in the sources (Grep of .md files, 26 Nov 2026). Sign-off value not specified in the source documents (DOR-RWB-S8-E2009-APP-14); section 14 not in chunk. |
| RWB-S8-E2012-APP | R-08815 | DOR-RWB-S8-E2012-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No epic design record in 03 Requirements and specifications (Grep 'epic design' found no match). Sign-off not specified in the source documents (DOR-RWB-S8-E2012-APP-14). |
| RWB-S8-E2015-APP | R-27765 | CG-ALL-11363 | 18 | §18 test lists differ from RTM v7 | REQ-DRI-001 kept at TC-E2-015-02; the item's RTM v7 list is truncated, so the row awaits the full RTM v7 list. |
| RWB-S8-E2015-APP | R-27766 | CG-ALL-11365 | 3, 3.1 | Flyway file V2015_1__case_deviation_read.sql is not in the V0001..Vnnnn form | The story text given names no migration file, and the next number of the service Flyway sequence is not in the sources (Service Template Specification v1 §3.1 checked, no value). Cannot number without inventing one. |
| RWB-S8-E2015-APP | R-28777 | GAP-0715 | find it | No source gives the alert values for the timer projection, the degradation rate or the breach volume | No threshold, window or band for the timer lag, MSG-GEN-006 degradation rate or TimerBreached volume in Architecture v5 slides 28 and 44, FSD P3 v4 or TSD P3 v3. Values would be invented. |
| RWB-S8-E2029-APP | R-08829 | DOR-RWB-S8-E2029-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (grep of 04 User stories for 'epic design' has no match). Sign-off reference would be invented. |
| RWB-S8-E2029-APP | R-08835 | DOR-RWB-S8-E2029-APP-8 | 3 | Definition of Ready item 8 Contract: Fail | Topic rwb.deviation.events.v1 with retry and .dlt is already in section 3. The 401 message ID and the payload-vs-catalog difference are not in the supplied text (PRD S8 FR-S8-013; OQ-S8-11). Nothing to anchor. |
| RWB-S8-E2029-APP | R-27773 | CG-ALL-11378 | 3 | Flyway file V2029_1__deviation_raise_index.sql is not in the V0001..Vnnnn form | Line L339 is not in the supplied story text, so it cannot be edited. Sources give only V0001 for rwb_deviation (PLT E1044 APP-2); the next free number is not specified. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19387 | RWB-S8-E1023-APP | CG-ALL-11296 | 12.1 | Publish GET /api/recovery/deviation/v1/cases/{caseId} in rwb-deviation.yaml through RWB-P3-E1023-CON, or remove it from section 12.1. |
| CDC-19388 | RWB-S8-E1023-APP | CG-ALL-11297 | 12.1 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/accounts in rwb-deviation.yaml through RWB-P3-E1023-CON, or remove it from section 12.1. |
| CDC-19389 | RWB-S8-E1023-APP | CG-ALL-11298 | 12.1 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/parties in rwb-deviation.yaml through RWB-P3-E1023-CON, or remove it from section 12.1. |
| CDC-19390 | RWB-S8-E1023-APP | CG-ALL-11299 | 12.1 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/contact-history in rwb-deviation.yaml through RWB-P3-E1023-CON, or remove it from section 12.1. |
| CDC-19391 | RWB-S8-E1023-APP | CG-ALL-11300 | 12.1 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/documents in rwb-deviation.yaml through RWB-P3-E1023-CON, or remove it from section 12.1. |
| CDC-19393 | RWB-S8-E1023-APP | DOR-RWB-S8-E1023-APP-8 | 12.1 | Add paths GET /cases/{caseId}, GET /cases/{caseId}/accounts, GET /cases/{caseId}/parties, GET /cases/{caseId}/contact-history and the fifth read path named in the detcheck. |
| CDC-19405 | RWB-S8-E1062-APP | CG-ALL-11308 | 12.1 | Publish GET /api/recovery/deviation/v1/deviations with query caseId through the RWB-S8-E1062-CON contract story |
| CDC-19411 | RWB-S8-E1062-APP | DOR-RWB-S8-E1062-APP-8 | 12.1 | add GET /api/recovery/deviation/v1/deviations with query caseId (CG-ALL-11308) |
| CDC-19433 | RWB-S8-E1065-APP | CG-ALL-11322 | 13 | Remove the fixed enum on outcome so LOV-DEV-OUTCOME values are read as data at the version in force, per DP-07 (lists are data). |
| CDC-19434 | RWB-S8-E1065-APP | CG-ALL-11323 | 13 | Remove the fixed enum on deviationCode so LOV-DEVIATION values are read as data at the version in force, per DP-07. |
| CDC-19435 | RWB-S8-E1065-APP | CG-ALL-11324 | 13 | Remove the fixed enum on raisedBy so LOV-RAISED-BY values are read as data at the version in force, per DP-07. |
| CDC-19437 | RWB-S8-E1065-APP | DOR-RWB-S8-E1065-APP-8 |  | Replace the closed enums for outcome, deviationCode and raisedBy with the LOV-DEV-OUTCOME, LOV-DEVIATION and LOV-RAISED-BY lists read as data. |
| CDC-19462 | RWB-S8-E2009-APP | CG-ALL-11332 | 12.1 | Add GET path /reports/measures under base /api/recovery/deviation/v1 (Measure[] answer), published through RWB-S8-E2009-CON. |
| CDC-19463 | RWB-S8-E2009-APP | DOR-RWB-S8-E2009-APP-8 | 12.1 | Add GET path /reports/measures under base /api/recovery/deviation/v1, published through RWB-S8-E2009-CON. |
| CDC-19485 | RWB-S8-E2012-APP | CG-ALL-11338 | 12.1 | Add the GET method on path /cases/{caseId}/deviations (DeviationSummary list, right R); the path lists POST only. |
| CDC-19487 | RWB-S8-E2012-APP | CG-ALL-11340 | n/a | Remove the fixed enum on outcome; LOV-DEV-OUTCOME is read as reference data (DP-07). |
| CDC-19488 | RWB-S8-E2012-APP | CG-ALL-11341 | n/a | Remove the fixed enum on deviationCode; LOV-DEVIATION is read as reference data. |
| CDC-19508 | RWB-S8-E2015-APP | CG-ALL-11358 | 12.1 | Add the GET operation for /cases/{caseId}/deviations with the answer and errors of section 12.1, or remove the read from this story. |
| CDC-19510 | RWB-S8-E2015-APP | DOR-RWB-S8-E2015-APP-8 | 12.1 | Publish GET /cases/{caseId}/deviations in the yaml (see CG-ALL-11358). The 401 message ID is Not specified in the source documents. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19350 | RWB-S8-E1020-APP | CG-ALL-11260 | 9, 12.1, 12.7 | Add decision_record as the platform-library record object in rwb_deviation (written before the deviation row, DP-03), or name the dictionary field it maps to. Lines 250 and 308 are outside this chunk. |
| CDC-19374 | RWB-S8-E1021-APP | CG-ALL-11278 | Not in supplied parts (lines 250, 324) | Data owner to confirm the dictionary name for decision_record, or to record the decision object in its owning document. Nearest names are decision_code and decision_log_id. |
| CDC-19399 | RWB-S8-E1023-APP | DOR-RWB-S8-E1023-APP-7 | 11 | Add decision_record as an entity or field of the platform decision-record library in rwb_deviation, so the section 11 row resolves to a model entry. |
| CDC-19413 | RWB-S8-E1062-APP | DOR-RWB-S8-E1062-APP-7 | 11 | Register v_open_deviation as a read-only view entity of rwb_deviation over deviation, with its fields, and classify it in Data Classification v5. The view is created by this story's migration (L355). |
| CDC-19467 | RWB-S8-E2009-APP | DOR-RWB-S8-E2009-APP-7 | 11 | Add decision_record, the provenance table of the platform decision-record library (DP-03), as an entity |
| CDC-19494 | RWB-S8-E2012-APP | CG-ALL-11336 | 11, 12.7 | Record decision_record as an object, or confirm the dictionary field name the story uses (e.g. decision_log_id) so story lines 251 and 325 resolve. |
| CDC-19495 | RWB-S8-E2012-APP | CG-ALL-11337 | 11, 12.7 | Record inbox_event as an object, or confirm the dictionary name (nearest outbox_event) so story lines 252 and 326 resolve. |
| CDC-19501 | RWB-S8-E2012-APP | DOR-RWB-S8-E2012-APP-7 | 11 | Add decision_record and inbox_event as platform library tables of rwb_deviation (DP-03, DP-09), or record them as outside entity scope. |
| CDC-19517 | RWB-S8-E2015-APP | DOR-RWB-S8-E2015-APP-7 | 11 | Register v_case_deviation (read-only view over deviation, created by migration V2015_1__case_deviation_read.sql, ASM-5295) and confirm DF-WRK-027 to DF-WRK-044 are all timer fields. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19351 | RWB-S8-E1020-APP | CG-ALL-11265 | 12.5 | Add activity evaluateHandlerRules on queue rwb-deviation, or name a catalogued activity in the story. |
| CDC-19352 | RWB-S8-E1020-APP | CG-ALL-11266 | 12.5 | Add activity recordAndApplyPlacement on queue rwb-deviation, or name a catalogued activity in the story. |
| CDC-19375 | RWB-S8-E1021-APP | CG-ALL-11283 | 12.5 | Add activity evaluateTransferRules to the Activities sheet on queue rwb-deviation, or name the catalogued activity to use. |
| CDC-19376 | RWB-S8-E1021-APP | CG-ALL-11284 | 12.5 | Add activity requestCaseTransfer to the Activities sheet on queue rwb-deviation, or name the catalogued activity to use. |
| CDC-19377 | RWB-S8-E1021-APP | CG-ALL-11285 | 12.5 | Add activity recordAndApplyTransfer to the Activities sheet on queue rwb-deviation, or name the catalogued activity to use. |
| CDC-19497 | RWB-S8-E2012-APP | CG-ALL-11345 | 12.5 | Add activity readOpenDeviations on queue rwb-deviation, or use a catalogued activity. |
| CDC-19498 | RWB-S8-E2012-APP | CG-ALL-11346 | 12.5 | Add activity applyCaseTransfer on queue rwb-deviation, or use a catalogued activity. |
| CDC-19499 | RWB-S8-E2012-APP | CG-ALL-11347 | 12.5 | Add activity recordDeviationMove on queue rwb-deviation, or use a catalogued activity. |
| CDC-19519 | RWB-S8-E2015-APP | GAP-3177 | find it | Register the five-minute next-action Schedule in rwb-case, and delete TimerDue (EV-18) from the Epic 2 contract tables. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19343 | RWB-S8-E1020-APP | CG-ALL-11261 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story key that carries the DEV package registry, so the DP-04 dependency resolves. |
| CDC-19346 | RWB-S8-E1020-APP | DOR-RWB-S8-E1020-APP-17 | 13 | Create story file RWB-P7-E1073-CON or name the existing key, as in CG-ALL-11261. |
| CDC-19370 | RWB-S8-E1021-APP | CG-ALL-11279 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story that carries the DP-04 rule-package capability |
| CDC-19372 | RWB-S8-E1021-APP | DOR-RWB-S8-E1021-APP-17 | 13 | Create RWB-P7-E1073-CON, or name the existing story carrying the DP-04 rule-package dependency |
| CDC-19406 | RWB-S8-E1062-APP | CG-ALL-11310 | 13 | Create RWB-P7-E1073-CON, or name the existing story of the same capability in the DP-04 row of section 13 |
| CDC-19408 | RWB-S8-E1062-APP | DOR-RWB-S8-E1062-APP-17 | 13 | Create RWB-P7-E1073-CON, or name the existing story of the same capability in the DP-04 row of section 13 |
| CDC-19409 | RWB-S8-E1062-APP | DOR-RWB-S8-E1062-APP-21 | header | Create contract story RWB-S8-E1062-CON for GET /deviations and its CON dependency |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19359 | RWB-S8-E1020-APP | GAP-2439 | 11 | Take the rule_package_version columns for state, valid-from, approver, DRL and checksum; confirm the served payload with the embedded Drools kit of RWB-PLT-E1072-CON. |
| CDC-19378 | RWB-S8-E1021-APP | DOR-RWB-S8-E1021-APP-7 | 11 | Add entity decision_record or record it as platform-library scope; story §11 already marks it as a library table. |
| CDC-19395 | RWB-S8-E1023-APP | CG-ALL-11294 | 11, 12.7 | Record decision_record as a platform library table in rwb_deviation (an object, not a field or entity) in the owning document. |
| CDC-19412 | RWB-S8-E1062-APP | CG-ALL-11307 | 13 | Record view v_open_deviation in rwb_deviation as a read-only object over deviation, created by migration V1062_1 of RWB-S8-E1062-APP. |
| CDC-19465 | RWB-S8-E2009-APP | CG-ALL-11331 | 11, 12.7 | Record decision_record as the platform library table in rwb_deviation (DP-03) so the object is named in the owning document. |
| CDC-19471 | RWB-S8-E2009-APP | GAP-0255 | find it | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate; queue measures stay with P3 rwb_case. |
| CDC-19512 | RWB-S8-E2015-APP | CG-ALL-11356 | 13 | Record the view v_case_deviation (read-only view over deviation, created by the migration of RWB-S8-E2015-APP) as an object, or give the dictionary name the model uses. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19396 | RWB-S8-E1023-APP | CG-ALL-11295 | not in chunk | Add list LOV-CONTACT-TYPE to Lists with the contact-type values the story uses. |
| CDC-19398 | RWB-S8-E1023-APP | DOR-RWB-S8-E1023-APP-20 | not in chunk | Add list LOV-CONTACT-TYPE to Lists with the contact-type values the story uses. |
| CDC-19438 | RWB-S8-E1065-APP | CG-ALL-11320 | 7 | Add list LOV-DEV-BAND to the Lists tab, or name an existing Reference Data v5 list in AC3 and TC-E1-065-03. |
| CDC-19439 | RWB-S8-E1065-APP | DOR-RWB-S8-E1065-APP-20 | 7 | Add list LOV-DEV-BAND to the Lists tab, or name an existing Reference Data v5 list in AC3 and TC-E1-065-03. |
| CDC-19528 | RWB-S8-E2029-APP | DOR-RWB-S8-E2029-APP-5 | 9 | Register DEV_FLAGGED in the closed lists LOV-DEVIATION and LOV-RAISED-BY, or remove it from the story's closed-list use. |
| CDC-19535 | RWB-S8-E2029-APP | GAP-2402 | 12 | Append path and shapes marked Not specified |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19355 | RWB-S8-E1020-APP | GAP-2443 | 12 | Add GET /rule-models/{packageCode}/{version} with the model-owner identity and the checksum to the P7 row and to the API Specification at the next version. |
| CDC-19422 | RWB-S8-E1062-APP | GAP-3085 |  | Declare a deviation estate read as a service operation with a catalogue row; publish the agent-policy read operation name; publish R-DEV-05 and R-DEV-06 codes and owner roles with the package version; set the answer limit value; record the six platform contracts as S8 template dependencies with H row empty. |
| CDC-19523 | RWB-S8-E2015-APP | GAP-0714 | find it | Add GET /cases/{caseId}/deviations to the S8 rows of the Ownership Map and to the S8 API file. |
| CDC-19525 | RWB-S8-E2015-APP | GAP-0428 |  | List the rwb-deviation case deviation read as a GET path. Harness pack, seeded data, business date, evidence format, gate and composite route path are Not specified in the source documents (GAP-0428). |
| CDC-19531 | RWB-S8-E2029-APP | GAP-1819 | 12 | Add S8 rows for screening run, screening score, contact stop, agent feedback and breach record in rwb_deviation; no physical name beyond the one held. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19344 | RWB-S8-E1020-APP | DOR-RWB-S8-E1020-APP-12 | 12, 12.7, 16, 18 | Align the section 18 test lists of RWB-S8-E1020-APP to the section 16 set, including TC-E1-020-16 to TC-E1-020-19. |
| CDC-19361 | RWB-S8-E1020-APP | CG-ALL-11271 | 18 | Align the test lists of the four requirements with section 18 of RWB-S8-E1020-APP at the RTM's next version. |
| CDC-19452 | RWB-S8-E1065-APP | CG-ALL-11327 |  | In the next RTM version, align REQ-RDF-001 and REQ-RDF-010 test lists with section 18 of RWB-S8-E1065-APP. |
| CDC-19538 | RWB-S8-E2029-APP | CG-ALL-11376 | 18 | Align REQ-DVH-006 and REQ-DVH-001 test lists with section 18 of RWB-S8-E2029-APP: REQ-DVH-006 TC-E2-029-02, -07, -08; REQ-DVH-001 TC-E2-029-02, -03, -09, -12; remove TC-E2-029-04, TC-E2-033-01 to -03 and TC-E1-062-01, -02 from these rows. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19360 | RWB-S8-E1020-APP | CG-ALL-11269 | 16 | TC-E1-020-06 and TC-E1-020-07 kept on AC1, AC2 and AC1, AC2, AC3, AC6, matching their data. |
| CDC-19397 | RWB-S8-E1023-APP | CG-ALL-11302 | 16 | Add rows TC-E1-023-12 and TC-E1-023-13 with Given, When and Then copied from AC11 and AC12 of the story. |
| CDC-19500 | RWB-S8-E2012-APP | CG-ALL-11349 | 16 | Add a row for TC-E2-012-15 with Given, When and Then copied from AC1 and AC6 of RWB-S8-E2012-APP section 7. |
| CDC-19537 | RWB-S8-E2029-APP | CG-ALL-11375 | 16 | Covers column kept in this story's AC numbering |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19365 | RWB-S8-E1020-APP | GAP-0687 | find it | Expose replicas, autoscaling bounds, node pool, connection pool size and closed-history archive as chart values with documented defaults; record SIT findings there. Capacity review stays with the platform observability story. |
| CDC-19457 | RWB-S8-E1065-APP | GAP-0897 | none | Publish the DEV-only read-only role and its grant list (SELECT on role and permission only, no access-entry read); fix the rwb-access login in the platform DB story; record retirement of the single-schema grant with DP-15. |
| CDC-19459 | RWB-S8-E1065-APP | GAP-1052 | 1 | Fix the synthetic file naming pattern next to the sandbox file properties; state that file content is derived from seed value, case ID and type so the hash is stable. |
| CDC-19461 | RWB-S8-E1065-APP | GAP-1053 | 1 | Record the DEV storage account, the DEV containers, the rwb-document login and the DEV read-only role; publish the SCR-30 and SCR-31 composite route with RWB-PLT-N001-CON. |

### RWB-P10-E1062-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19410 | RWB-S8-E1062-APP | DOR-RWB-S8-E1062-APP-22 | 12.8 | Fake named with the contract; library version stays Not specified |
| CDC-19419 | RWB-S8-E1062-APP | GAP-0615 | find it | Declare one run-start and one run-read operation on /api/recovery/agent/v1 with their request members and answer resource, the three event payloads with case ID key, and the consumed paths. Mark the three unnamed paths with the placeholder. |
| CDC-19423 | RWB-S8-E1062-APP | GAP-0614 |  | Publish the run-start operation on /api/recovery/agent/v1 with request members and refusal codes, the parameter and ledger read paths, the two added events, the screening feature flag and the boundary status of a failed tool call. |
| CDC-19428 | RWB-S8-E1062-APP | GAP-1047 | find it | Map the agent case read to API-P5-002 and the document read to API-P5-003, with API-P5-009 for an extracted-field filter; publish the tool call field names in the rwb-document AsyncAPI and OpenAPI. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19466 | RWB-S8-E2009-APP | CG-ALL-11333 | 4, 14 | Add a message ID for the X7 text '{service} is not available now. Try again in a few minutes.'; MSG-GEN-006 keeps its R-UNI-33 text |
| CDC-19468 | RWB-S8-E2009-APP | DOR-RWB-S8-E2009-APP-9 | 14 | Align MSG-GEN-006 to the standard meaning or rename the story message to a distinct code. |
| CDC-19513 | RWB-S8-E2015-APP | CG-ALL-11359 | 4, 12.1 | Add a message ID for 401 no Workbench identity (HTTP 401, no Workbench identity). The standard has no identity or 401 message today; the story keeps its placeholder until one exists. |
| CDC-19514 | RWB-S8-E2015-APP | CG-ALL-11360 | 14 | Add a new message ID for the escalation decision-record write failure (X4); the story then cites it in section 14 and section 5. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19353 | RWB-S8-E1020-APP | GAP-0345 | find it | Publish the JOB-03 step state on the rwb-case run result and fix the rerun facade for a workflow step in the P1 job-catalogue contract before wave 1 exit. |
| CDC-19418 | RWB-S8-E1062-APP | GAP-2326 | find it | Add a POST /authorise row for the role, scope and delegation of authority check, with its request and answer shape confirmed at the wave 1 contract review and kept inside RWB-P4-E1037-CON. |
| CDC-19505 | RWB-S8-E2012-APP | GAP-2500 |  | Keep T3.1 entry fields as contract; decision code from LOV-DECISION as reference data; MSG-P7-009 and REQ-CWC-010 text as R9 placeholder; version list answers the finding and MSG-P3-027 when none in force; page-size guard as service configuration; write the DP-02 login as the rwb-decision login (DP-02). |

### RWB-P1-E1065-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19443 | RWB-S8-E1065-APP | GAP-3086 | find it | Publish the deviation seed profile with case references, shapes and routed states; the deviation count per case and shape-to-code mapping; stage contract operation and field names; R-DEV-05 and R-DEV-06 codes and owner roles; and the test level of the ten legacy cases. |
| CDC-19447 | RWB-S8-E1065-APP | GAP-0502 |  | Publish the stage interface and its input and output profile, with four fixtures (full seed, empty seed, refused seed, timeout) and drift detection as a build failure. |
| CDC-19456 | RWB-S8-E1065-APP | GAP-0503 | 4 | Read-only role name set to Not specified in the source documents |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19486 | RWB-S8-E2012-APP | CG-ALL-11339 | 13 | Create story file RWB-P7-E1073-CON for the rwb-decision rule-package contract used by DP-04, or name the existing key in section 13. |
| CDC-19489 | RWB-S8-E2012-APP | DOR-RWB-S8-E2012-APP-17 | 13 | Create story file RWB-P7-E1073-CON for the rwb-decision rule-package contract, or name the existing key in section 13. |
| CDC-19490 | RWB-S8-E2012-APP | DOR-RWB-S8-E2012-APP-21 | header | Create story RWB-S8-E2012-CON publishing the rwb-deviation GET, POST and PATCH shapes, error list and fakes (section 12.1). |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19345 | RWB-S8-E1020-APP | DOR-RWB-S8-E1020-APP-14 | - | Record the signed epic design sign-off for RWB-SVC-S8 and this story. |
| CDC-19407 | RWB-S8-E1062-APP | DOR-RWB-S8-E1062-APP-14 | header | Record the signed epic design sign-off for RWB-S8-E1062-APP in the epic design record |

### RWB-P3-E1020-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19348 | RWB-S8-E1020-APP | DOR-RWB-S8-E1020-APP-22 | - | Record the published version of the contract fake library for RWB-P3-E1020-CON. |
| CDC-19356 | RWB-S8-E1020-APP | GAP-3072 | 3, 4 | Publish the case element, the stage outcome and the queue-and-members element with field names; confirm the four handler role codes against TSD S8 T6.1. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19366 | RWB-S8-E1020-APP | GAP-0987 | find it | Record the authorise request attributes for summary and case reads, the PM-2026.11 version in force at 30 November 2026 with PM-2026.12 from 2026-12-01, and the Queue and allocation role roster as the defaults set in the item. |
| CDC-19432 | RWB-S8-E1062-APP | GAP-2329 | find it | Set the default scope of SY-AGENT to ALL (LOV-SCOPE) in the matrix version in force; state the scope rule for every non-human actor role in the access and administration documentation. |

### RWB-PLT-NF06-DB (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19381 | RWB-S8-E1021-APP | GAP-0688 | none | Name the rwb-case database login with its owner and grant set; the chart then takes it by vault secret reference. |
| CDC-19451 | RWB-S8-E1065-APP | GAP-2251 |  | Set the rwb-case login name here; keep rwb_sandbox_read as DEV read role; confirm field identifiers of queue, queue_member, assignment, task, timer, case_entry_exclusion and reference_version against LDM and Data Dictionary v8. |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19445 | RWB-S8-E1065-APP | GAP-0895 | find it | Fix the seed file as a migration resource in rwb-access with path, format, version label and row count; state in the Service Contract Catalog whether the DEV seed carries the SIT matrix version. |
| CDC-19521 | RWB-S8-E2015-APP | GAP-0934 | find it | Fix the authorise request as v1 with caseId, teamCode, ownerUserRef, escalatedToRole and escalatedAt, with BACKWARD compatibility. |

### RWB-P3-E1065-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19448 | RWB-S8-E1065-APP | GAP-2249 |  | Seed one open task and one active timer per active case; set remaining timer offsets as timer table rows at load review; no criterion change if counts differ. |
| CDC-19449 | RWB-S8-E1065-APP | GAP-2250 |  | Distribute 2,812 cases by product group to queue rows of the seed file; cap every member at 40 open cases; tune via seed-file rows. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19458 | RWB-S8-E1065-APP | GAP-0899 | none | Publish the 54-role list with administration and non-human roles marked; reconcile it with the 42 rows of TSD P4 T6.1; fix the role count the DEV seed carries. |
| CDC-19478 | RWB-S8-E2009-APP | GAP-0731 | find it | Agree the case-fact read schema, cut-off rule and fact transport with the rwb-reporting owner; record the case-fact event projection in the case CON story and the Service Contract Catalog. |

### RWB-S8-E2009-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19475 | RWB-S8-E2009-APP | GAP-2576 | find it | Declare three consumed operations and two owner-queue activities on per-service bases with one hop and a 2 s timeout; replay the day's events into a run-scoped read model; hand the published extract to rwb-integration as the INT-19 replacement; take agent rates from EV-28 and RWB-P10-E1063-CON. |
| CDC-19476 | RWB-S8-E2009-APP | GAP-2577 | find it | Publish v1 as an increment: baselineValue delta, dimension fixing, three declarations, two activity contracts, eight subscriptions with groups, JOB-15 registration contract, message map and fakes; placeholders with one review row; gate on contract tests and schema lint. |

### RWB-S8-E2012-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19492 | RWB-S8-E2012-APP | DOR-RWB-S8-E2012-APP-23 | 1 | State the contract version the story builds against. Story row now records that it is Not specified and builds against the /v1 path. |
| CDC-19506 | RWB-S8-E2012-APP | GAP-3093 | 15 | Fix the read schema of GET /cases/{caseId}/deviations on /api/recovery/deviation/v1; the P3 slice RWB-P3-E2012-APP reads this one answer and keeps the event-fed flag from DeviationRaised and DeviationCleared. |

### RWB-P3-E2012-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19503 | RWB-S8-E2012-APP | GAP-0710 |  | Add one ordered selection element to the rwb-case contract with caseId, assignment or refusal messageId, and done and total counts; the summary is derived from the array. |
| CDC-19504 | RWB-S8-E2012-APP | GAP-0711 |  | Add a refusal element with reason code, owner list with open-case count and cap each, and current and target state; read cap and hold before the first write. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19511 | RWB-S8-E2015-APP | GAP-1816 | 16 | Route the ACE and batch-status reads through rwb-source-data and name its fields in FSD A1.1. Confirm party-flag, deceased-marker and freshness fields with P1 before the wave 2 system test. |
| CDC-19529 | RWB-S8-E2029-APP | GAP-1816 | header | Slide 13 S8 row: add the rwb-source-data read as a data cell; slide 45: name rwb-deviation as a reader through that contract. Story side: field names come from the rwb-source-data contract. |

### RWB-P10-E2029-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19527 | RWB-S8-E2029-APP | DOR-RWB-S8-E2029-APP-21 | header | Confirm RWB-P10-E2029-CON as the published contract for rwb-deviation; no RWB-S8-E2029-CON story exists in the source set. Header already names RWB-P10-E2029-CON. |
| CDC-19534 | RWB-S8-E2029-APP | GAP-2194 | 12 | Publish raise and entry-read shapes, completion payload subject, five score-row members and gateway-bff route; placeholders used here until then. |

### RWB-S8-E1020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19347 | RWB-S8-E1020-APP | DOR-RWB-S8-E1020-APP-21 | header | Publish contract story RWB-S8-E1020-CON for the two operations of section 12, or confirm the plan publishes none. |

### OTHER:rwb-deviation API contract (/api/recovery/deviation/v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19349 | RWB-S8-E1020-APP | DOR-RWB-S8-E1020-APP-8 | 7 | Add an Idempotency-Key header to PATCH /deviations/{deviationId}. Story AC1 event name corrected to rwb.deviation.DeviationRaised.v1 on topic rwb.deviation.events.v1. |

### OTHER:Service Catalog and RWB-PLT-DB stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19354 | RWB-S8-E1020-APP | GAP-0684 | find it | Allocate the rwb-case service login with schema rwb_case, store it in Key Vault and record its name in the Service Catalog and the RWB-PLT-DB stories before the first deployment. |

### OTHER:RWB-PLT-DB and the rwb-case DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19357 | RWB-S8-E1020-APP | GAP-3207 | 3 | Publish the per-service login name of rwb-case; the placeholder stays in this story. The cap stays queue data with its default from the parameter contract. |

### RWB-P3-E1020-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19358 | RWB-S8-E1020-APP | GAP-3208 | 17 | Fix the Temporal cron expression, the timezone handling and the rule for a date with no run for DailyCaseRun; keep the AceDataReady event start and the 07:00 Asia/Bangkok deadline. |

### OTHER:BRD v4 section 3 (requirement headings) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19362 | RWB-S8-E1020-APP | GAP-1457 | find it | Renumber the section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### OTHER:Work package C-WEX (work package index) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19363 | RWB-S8-E1020-APP | GAP-3206 | find it | Correct the heading label (E1-018) to the E1-020 worked example subject at the next run; keep RWB-E1-020 as the subject of the document. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19364 | RWB-S8-E1020-APP | GAP-3209 | find it | Add one criterion-ownership column listing for each legacy criterion the single new story that owns it; until then the story files' division is the record. |

### OTHER:Reference data package ALLOCATION ALLOC-2026.11 (workbook load) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19367 | RWB-S8-E1020-APP | GAP-2440 | find it | Load the row once with the rule ID the workbook carries and record the other label as the row description; no code or criterion change. |

### OTHER:P7 message catalogue (FSD P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19368 | RWB-S8-E1020-APP | GAP-2442 | find it | Approve the text of MSG-P7-009 and the chain-break warning and name the per-entry chain result field; the ID and the same-day Compliance report stay unchanged. |

### OTHER:Not specified in the source documents (GAP-2150) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19369 | RWB-S8-E1020-APP | GAP-2150 | header | Confirm the added RWB-P3-E1042-CON worked example and decide whether a microservice example replaces RWB-E1-020 or stands beside it. |

### RWB-S8-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19371 | RWB-S8-E1021-APP | DOR-RWB-S8-E1021-APP-14 | header | Record the signed epic design sign-off for this story in the epic design record |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19373 | RWB-S8-E1021-APP | DOR-RWB-S8-E1021-APP-8 | 12.1 | Catalog: list rwb.deviation.DeviationRaised.v1 and rwb.deviation.DeviationCleared.v1 on topic rwb.deviation.events.v1 with .retry and .dlt rows, as in rwb-deviation.asyncapi.yaml. Temporal Catalog v1: add activity evaluateTransferRules. |

### OTHER:Business Requirements Document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19379 | RWB-S8-E1021-APP | GAP-1456 | find it | State in section 8.2 that the business-epic wave is kept over the service wave; delivery lead confirms the wave per story at build sequencing. |

### OTHER:TSD S8 T5.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19380 | RWB-S8-E1021-APP | GAP-3079 | 4 | Publish the Kafka event names of the case triggers on rwb.case.events.v1 and of the source-data events on rwb.source-data.events.v1 before release; the consumer groups then bind to them. |

### OTHER:BRD v4 section 3.1 to 3.9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19382 | RWB-S8-E1021-APP | GAP-1457 | 3 | Renumber the section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### RWB-P4-E1037-CON; OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19383 | RWB-S8-E1021-APP | GAP-0990 |  | Publish the authorise request and answer schema with the legalHold attribute; confirm the matrix version label in force at 30 November 2026 with the matrix owner; tabulate the Queue and allocation letters in TSD P4 T6.1. |

### OTHER:Platform chart values for rwb-case (platform team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19384 | RWB-S8-E1021-APP | GAP-0691 |  | Publish cluster, node pool, replica counts per environment, ingress host, resource limits and disruption budget as chart values; no environment default; two-replica start values are proposals. |

### OTHER:P5 contract baseline story for rwb-document (rwb.document.events.v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19385 | RWB-S8-E1021-APP | GAP-1036 |  | Publish the producer-side AsyncAPI 3.0 and registered JSON schemas for DocumentStored.v1 and DocumentFieldsExtracted.v1 with required fields and BACKWARD rule; hand the DocumentStored schema to RWB-P3-E1021-CON. |

### RWB-PLT-NF06-DB; OTHER:service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19386 | RWB-S8-E1021-APP | GAP-1037 |  | Allocate the rwb-document login name, its grants (schema rwb_document only, no privilege on another schema) and its secret reference; record them in the service catalogue. |

### RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19392 | RWB-S8-E1023-APP | DOR-RWB-S8-E1023-APP-21 | header | none |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19394 | RWB-S8-E1023-APP | GAP-0693 | 14 | Publish the gateway-bff composite route for SCR-03: path, parallel calls to rwb-case GET /v1/cases/{id} and rwb-source-data GET /v1/customers/{id} and /v1/accounts/{id}, merge field map, 2 s budget split, partial-failure rule. Keep the five rwb-case reads unchanged. |

### OTHER:Business Requirements Document section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19400 | RWB-S8-E1023-APP | GAP-1456 | find it | State that Epic 1 stories keep the business-epic wave while the service starts in its own epic wave; delivery lead confirms the wave per story at build sequencing. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19401 | RWB-S8-E1023-APP | GAP-0348 | find it | Ownership map lacks the case-scoped read; no story change for this item. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19402 | RWB-S8-E1023-APP | GAP-0694 | 8 | Publish the masking policy request and response keyed by view field ID, with a masked flag and the source column per field; rwb-case sends the field list it read. |

### OTHER:BRD v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19403 | RWB-S8-E1023-APP | GAP-1457 | 3 | Renumber section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19404 | RWB-S8-E1023-APP | GAP-3084 | 13 | Add a row for caserecord.section.timeout.ms (legacy assumed 3000, owner to confirm) and the six reference lists as rwb-case parameters. |

### OTHER:Business Requirements Document Epic 1 v5, section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19414 | RWB-S8-E1062-APP | GAP-1456 | find it | State the rule that Epic 1 requirement stories keep their business-epic wave while the receiving service epic starts in a later wave, and that the delivery lead confirms the wave per story at build sequencing. |

### OTHER:Functional Specification Document S8; OTHER:A2.2.4 to A2.9.4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19415 | RWB-S8-E1062-APP | GAP-1823 | find it | Rewrite each repeated AC-S8-00n-01 'Timers shown' row and its alternate and exception rows as one criterion per behaviour, with the owner and the QA lead. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19416 | RWB-S8-E1062-APP | GAP-1826 | find it | Carry the 12 named R-DEV rules and the 22-rule route set as the requirement set, and name R-DEV-19 to R-DEV-21 from the design. Package authoring and promotion stay with rwb-decision. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Tables sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19417 | RWB-S8-E1062-APP | GAP-1819 | find it | Add S8 rows in rwb_deviation for screening runs with mode, score rows per code with precision, recall and sample size, contact stop, agent feedback and breach record, stated as entity groups with key fields. |

### OTHER:FSD P10 v3; OTHER:A2.8.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19420 | RWB-S8-E1062-APP | GAP-1532 | find it | Retitle A2.8 so the mode is read from the policy row. The Epic 1 shadow run and the Epic 2 L1 run are one code path with mode SHADOW or L1. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19421 | RWB-S8-E1062-APP | GAP-2327 |  | Publish CALLER_KIND, RIGHT_NOT_HELD and SCOPE_NOT_ALL as the refusal reasons of the authorise operation with their statuses, confirmed for every caller service. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; OTHER:REQ-DVH-003 and REQ-DVH-007 rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19424 | RWB-S8-E1062-APP | CG-ALL-11313 |  | Align the test lists to section 18: REQ-DVH-001 to TC-E1-062-01 and TC-E1-062-11; REQ-DVH-003 to TC-E1-062-04; REQ-DVH-007 to TC-E1-062-05. |

### OTHER:BRD v4 section 3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19425 | RWB-S8-E1062-APP | GAP-1457 |  | Renumber the section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### OTHER:FSD S8 (document control and version history) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19426 | RWB-S8-E1062-APP | GAP-1834 |  | Add the v1 and v2 change notes, dates and contents to the FSD S8 document control when the folder is completed. |

### OTHER:Platform NFR document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19427 | RWB-S8-E1062-APP | GAP-1833 | 16 | Volume figures replaced with Not specified in the source documents (GAP-1833) |

### OTHER:AsyncAPI document of rwb.document.events.v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19429 | RWB-S8-E1062-APP | GAP-1048 | find it | Fix the DocumentStored payload as documentId, caseId, documentType, source and storedAt; state the idempotency key is the outbox event ID; mirror in RWB-P10-E1062-CON. |

### OTHER:rwb-access masking contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19430 | RWB-S8-E1062-APP | GAP-1049 | find it | Publish the mask format and the per-role list of personal document fields; state SY-AGENT holds Documents R with every personal field masked and no clear value in answer, log or trace. Format and list: Not specified in the source documents (GAP-1049). |

### RWB-P5-E1062-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19431 | RWB-S8-E1062-APP | GAP-1050 | find it | State that a stored document is served with the type on its row and is never re-typed on read, and that the 422 MSG-P5-006 unknown-type refusal applies at store time only. |

### OTHER:Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19436 | RWB-S8-E1065-APP | DOR-RWB-S8-E1065-APP-21 | 1 | Create contract story RWB-S8-E1065-CON, or confirm RWB-P1-E1065-CON (already named in the header) as this story's contract. |

### OTHER:Wave 1 contract-test harness pack (not in the source set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19440 | RWB-S8-E1065-APP | GAP-0384 | find it | Agree with QA, integration lead and DevOps the harness repository, environment, namespace, pipeline stage, tooling beyond the standards, fixture composition, reset, report format and all-green gate; pin the stub set per build. |

### RWB-ITG-W1J01-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19441 | RWB-S8-E1065-APP | GAP-2154 | find it | Keep seed, business date, volumes and identifiers as configuration of RWB-ITG-W1J01-ITG, set by the QA lead; write the Template and Rules R9 placeholder until then. |

### RWB-P4-E1022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19442 | RWB-S8-E1065-APP | GAP-0896 | 8 | BR6 records the owner as Not specified |

### OTHER:TSD P4 (RBAC matrix T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19444 | RWB-S8-E1065-APP | GAP-0900 | find it | Extend the T6.1 matrix to the 14 capability areas of LOV-CAPABILITY and publish the full matrix version with pack load story RWB-P4-AD002-APP. |

### OTHER:TSD P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19446 | RWB-S8-E1065-APP | GAP-0898 | find it | Add POST /authorise and GET /me/permissions with request and answer schemas to the API specification and TSD P4 appendix T-A, stub them in the contract fake, and publish the SCR-43 composite route with gateway-bff (DP-19). |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19450 | RWB-S8-E1065-APP | GAP-2252 |  | Confirm at decision-record contract review the decision code for seeded raises and for seeded exclusions; the seed and criteria stay unchanged if codes differ. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19453 | RWB-S8-E1065-APP | GAP-1051 | 1 | Publish the per-case document count and the version depth of a seeded document as seed parameters, also kept as seed parameters of RWB-P5-E1025-APP. This story seeds no documents (section 1). |

### OTHER:Work Package plan generator (B-P1-02; OTHER:B2-P1-001) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19454 | RWB-S8-E1065-APP | GAP-2161 | none | Remove RWB-E1-064 from B-P1-02 fanout or retire B2-P1-001 for this key; number CG-B-P1-02-E1064-101, -201, -301 once; add a plan-uniqueness check to checks/run_all.py. |

### RWB-P1-E1065-CON; RWB-P5-E1049-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19455 | RWB-S8-E1065-APP | GAP-1054 | 1 | Fix held intake item count per exception shape and pages per item as seed parameters in RWB-P1-E1065-CON; name the review reasons the DEV queue must show in the test data section of RWB-P5-E1049-APP. |

### RWB-P1-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19460 | RWB-S8-E1065-APP | GAP-3168 | 4 | Build the sandbox from the 19 Flyway sequences plus the two view migrations and state the seeding order per schema, replacing the three-migration sandbox. |

### OTHER:FSD P9 (Recovery Workbench FSD; OTHER:Reporting) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19464 | RWB-S8-E2009-APP | GAP-1646 | 1 | Rewrite A2.1.2, A2.3.2, A2.4.2, A2.5.2, A2.7.2, A2.8.2 and AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01, AC-ALT-P9-004-01: Power BI and lake become the gateway-bff read model and rwb-integration file delivery. |

### OTHER:RWB-E6-037 (benefit realisation story) and FSD P9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19469 | RWB-S8-E2009-APP | GAP-2579 | find it | Confirm the benefit-model measure set and its holder, the monthly business day and cut-off, the measure_snapshot month key, the screen carrying the benefit view and the requirement ID. |

### OTHER:Recovery Workbench fact-table workbook v3 (Facts sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19470 | RWB-S8-E2009-APP | GAP-0251 | find it | Re-point the nine fact tables to the rwb_reporting read model fed from service topics; serve dashboards and reports via GET /dashboards/{id} and GET /reports/{id} behind gateway-bff; drop the data lake and Power BI feed. |

### OTHER:Recovery Workbench fact-table workbook v3 (Dimensions and Facts sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19472 | RWB-S8-E2009-APP | GAP-0257 | find it | Key owner and team by ID from events; resolve display names from P3 queue_member and assignment behind the rwb-access masking policy; no personal data on any event. |

### OTHER:FSD P9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19473 | RWB-S8-E2009-APP | GAP-1649 | find it | Publish the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE; carry the measure count as an open question across AC-P9-001-01, AC-P9-003-01, AC-P9-008-01 and the AC-ALT rows. |

### RWB-P9-E1013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19474 | RWB-S8-E2009-APP | GAP-2570 | find it | Declare the measures read in the wave 1 contract for the harness and catalog consumer; keep the dashboard and its data set in RWB-P9-E2009-APP; leave any reporting client connection as an open decision for the PRD step. |

### OTHER:Wave 2 entry check record (integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19477 | RWB-S8-E2009-APP | GAP-0391 | find it | Agree the gateway-bff composite steering route path and merge order, harness repository and SIT environment, seeded measure day, evidence format and retention, and the pass/fail gate. |

### OTHER:rwb-case (P3) PRD and rwb-payment (P8) PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19479 | RWB-S8-E2009-APP | GAP-1563 | find it | Name the P3 duty (exception visibility on the case) and the P8 duty (the matching rule) in both PRDs. |

### OTHER:rwb-reporting deployment slice story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19480 | RWB-S8-E2009-APP | GAP-2578 | find it | Ship one chart with api and worker deployments, migration, Schedule, eight consumer groups, six alerts with runbook links, four dashboard series, the flag, backfill and rollback; take thresholds and offsets as environment values; allocate the missing run message ID; review six runbook entries with on-call. |

### OTHER:Recovery Workbench measure workbook v3; OTHER:Facts sheet F6; OTHER:F10; OTHER:F12 and F13 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19481 | RWB-S8-E2009-APP | GAP-0253 | find it | Each refresh cell reads event-fed projections with the 01:30 publish (JOB-15); rebuild by rerun for any business date; measure_publish decides publish or hold. |

### OTHER:Recovery Workbench measure workbook v3; OTHER:Read model sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19482 | RWB-S8-E2009-APP | GAP-0256 | find it | Each row carries inbox dedupe, business-date order, reopen-until-frozen rule and rebuild from retained topic history. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:Functional Specification Document P3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19483 | RWB-S8-E2009-APP | GAP-0258 | 8 | Replace the Power BI publication of case_list_row and queue_measure with consumption through rwb-reporting GET /dashboards/{id} and GET /reports/{id} |

### OTHER:Workflow kit owner (schedule id, calendar, catch-up policy, rerun input); OTHER:reporting owner (two Measure fields, dimension format); OTHER:rwb-comms (channel and two recipients) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19484 | RWB-S8-E2009-APP | GAP-3090 | 8 | Publish the schedule, Measure field, dimension format and alert channel values; story side: filter lists read as rwb-case reference data |

### RWB-P3-E2012-CON; RWB-S8-E2012-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19491 | RWB-S8-E2012-APP | DOR-RWB-S8-E2012-APP-22 | 1 | Record the contract fake library version as published. Story row now shows it as Not specified in the source documents. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19493 | RWB-S8-E2012-APP | DOR-RWB-S8-E2012-APP-8 | 12.1 | Add GET /cases/{caseId}/deviations; make outcome and deviationCode data, not closed enums; align DeviationRaised.v1 topic to the catalog. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:EV-04) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19496 | RWB-S8-E2012-APP | CG-ALL-11344 | 12.4 | Add rwb-deviation as a consumer of rwb.case.CaseTransferred.v1, with its ACL. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19502 | RWB-S8-E2012-APP | GAP-2502 |  | Publish the decision event as rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 and drop rwb.decision-record.DecisionRecorded.v1 before the Kafka Topic and Event Catalog freeze. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19507 | RWB-S8-E2012-APP | GAP-2501 | 13 | Record the DP-added platform and published contracts as non-blocking H and C entries built against their fakes; keep the metadata rows as given. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19509 | RWB-S8-E2015-APP | DOR-RWB-S8-E2015-APP-21 | header | RWB-S8-E2015-CON is not a story in the set; the contract dependency is shown as Not specified pending the contract story key. |

### RWB-P3-E2015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19515 | RWB-S8-E2015-APP | DOR-RWB-S8-E2015-APP-10 | 4 | State the empty, loading, error and no access states of SCR-06 and SCR-08, and the loading state of SCR-03. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19516 | RWB-S8-E2015-APP | DOR-RWB-S8-E2015-APP-11 | 11 | Confirm the class of handler_user_id (DF-CAS-042) and of each field in section 11 against the no-personal-data statement. |

### OTHER:Error Handling and Resilience Standard (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19518 | RWB-S8-E2015-APP | DOR-RWB-S8-E2015-APP-9 | 14 | Reconcile the meaning of MSG-P7-003 with the standard; reassign the decision-record write failure to its own message ID where the standard uses MSG-P7-003 for another meaning. |

### RWB-S8-E2015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19520 | RWB-S8-E2015-APP | GAP-1832 | find it | Carry DeviationRaised (EV-06) and DeviationCleared (EV-07) on rwb.deviation.events.v1 keyed by case, with code, state, contact stop flag, return point and decision record reference; no personal or financial value. |

### OTHER:Wave 2 case-record harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19522 | RWB-S8-E2015-APP | GAP-0399 | find it | Record the composite route path, merge order, timer and deviation fixtures with fixed clocks, environment and seeding, evidence format and retention, and pass/fail gate. |

### OTHER:Functional Specification S8 (A2.2.2; OTHER:A2.3.2; OTHER:A2.6.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19524 | RWB-S8-E2015-APP | GAP-1817 | find it | Replace the Quartz scheduler integration point with durable timers inside DeviationWorkflow through the workflow kit for the pause, prescription clock and resume. |

### OTHER:FSD S8 document control (Functional Specification S8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19526 | RWB-S8-E2015-APP | GAP-1834 |  | Add v1 and v2 change-note rows to the inherited history, marked Not specified in the source documents, until the v6 extract folder is completed. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19530 | RWB-S8-E2029-APP | DOR-RWB-S8-E2029-APP-12 Test cases: Partial | 16, 12.7, 18 | Story §16 now has 20 test cases incl. contract, boundary and AC7 to AC12 rows; the other workbooks need the same IDs. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19532 | RWB-S8-E2029-APP | GAP-1832 | 12 | Event payload limited to catalog fields; other envelope fields Not specified |

### RWB-P10-E2029-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19533 | RWB-S8-E2029-APP | GAP-2193 | 12 | Fix rwb-agent login, S8 raise story, three parameter keys, gateway-bff route and rwb_agent Flyway position there; placeholders used here until then. |

### RWB-P10-E2029-CON; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19536 | RWB-S8-E2029-APP | GAP-3100 | 12 | Publish raise request with return point, agent version and segment pair; name agent-policy read; add open-code partial unique index; publish envelope type; assign levels to legacy cases. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0064 | Wave conflict S8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0251 | The nine fact tables are defined in a data lake; the target has no data lake | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0253 | The refresh wording has no schedule in the target | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0255 | The read-model control tables and the queue measures are absent | Data architecture team | Resolved (directive) |
| GAP-0256 | No late-arrival, freeze or replay rule on any fact table | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0257 | dim_org holds an owner while events carry no personal data | Data steward | Resolved (directive) |
| GAP-0258 | The LDM and the FSD still publish to Power BI, which is removed | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0345 | JOB-03 run surface and exact rerun facade are not specified for an ITG suite | Service owner of rwb-case with the service owner of rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0346 | Route-decided transfer trigger has no wave 1 owner event | Tech lead | Resolved (directive) |
| GAP-0348 | RWB-E1-023 integration slice: the S8 deviation read path, the wave of rwb-deviation and the fixture composition are not fixed by the sources | TechX | Resolved (directive) |
| GAP-0371 | Rule-row owner lookup, interaction ledger read and deviation-absence evidence are not named for the target | P10 agent owner, P7 decision owner, P1 source data owner, S8 deviation owner and P4 access owner | Resolved (directive) |
| GAP-0374 | The per-schema seed volumes, the seeding order across the 19 baselines and the cutover from the one recovery schema are not stated | Solution architect | Resolved (directive) |
| GAP-0384 | The wave 1 contract-test harness, its pipeline wiring and the synthetic test data set are not specified | QA lead | Resolved (directive) |
| GAP-0391 | Gateway-bff composite steering route, harness environment, measure-day seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0396 | Gateway-bff composite transfer route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0399 | Wave 2 case-record harness: composite route, timer and deviation fixtures, environment and evidence format undefined | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0411 | SIT harness environment, SCREEN-S2 fixture pack, Enterprise AI test profile, evidence format and gate for the deviation-screening journey are not specified in any source read | Integration lead | Resolved (directive) |
| GAP-0428 | The wave 2 journey harness environment, seeded data, evidence format and release gate are not specified | QA lead | Resolved (directive) |
| GAP-0501 | The sandbox scope per service and the placement of the generator module are not specified | Solution architect | Resolved (directive) |
| GAP-0502 | The contract of a build tool is not described by any source document | Tech lead | Resolved (directive) |
| GAP-0503 | The sandbox database scope and its read-only role name are not specified | ACE data architect | Resolved (directive) |
| GAP-0614 | The screening slice in rwb-agent: the run-start path, the parameter and ledger operation paths, the two added events, the screening feature flag, the boundary status of a failed tool call and the route in front of the reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-deviation, rwb-case, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0615 | The screening contract slice: the run-start path and request members, the member types of the proposal payload, the two added event names and payloads, the consumed paths no source names and the route name are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0625 | The app slice of the deviation screening evaluation and L1 on one segment: the service login, the S8 raise contract story, the parameter keys of the floor and the promotion condition, the sealed decision-entry read, the gateway-bff route path and the migration numbering are not fixed by any source | TechX with the rwb-deviation (S8) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0626 | The contract slice of the deviation screening evaluation and L1 on one segment: the S8 raise path and members, the parameter keys, the member types of a consumed answer, the sealed decision-entry read, the service login and the route path are not specified by any source | TechX with the rwb-deviation (S8) owner, the rwb-decision (P7) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0684 | The rwb-case service login name is not given in any source | ACE team, DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0687 | The deployment topology of the rwb-case allocation worker is not specified | Platform team; DevOps | Resolved (directive) |
| GAP-0688 | Per-service database login name for rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0691 | Deployment topology of the transfer capability is not specified | Platform team | Resolved (directive) |
| GAP-0692 | The per-service database login name for rwb-case is not given | ACE DB owner | Resolved (directive) |
| GAP-0693 | The gateway-bff composite route specification for SCR-03 is not given | Solution architect | Resolved (directive) |
| GAP-0694 | The exact field masking contract shape is not given | P4 access owner | Resolved (directive) |
| GAP-0695 | The timeline paging and the interaction ledger read operation are not given | P1 source data owner | Resolved (directive) |
| GAP-0710 | The partial-success shape of a selection and its summary message are not typed | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0711 | The at-cap and legal-hold pre-check answers have no typed shape | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0712 | Who may add or retire a transfer reason code is not specified | Centre of excellence; data steward | Resolved (directive) |
| GAP-0713 | The activity timeouts and the alert thresholds of the manual move are not specified | DevOps lead; service owner of rwb-case | Resolved (directive) |
| GAP-0714 | Deviation read path is absent from the Ownership Map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0715 | No source gives the alert values for the timer projection, the degradation rate or the breach volume | DevOps lead | Resolved (directive) |
| GAP-0731 | Case-fact read shape, cut-off rule and the reporting hand-off are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0895 | rwb-access sandbox seed: the access seed file's location, format, version label and row count are not specified, and whether the DEV matrix version must equal the SIT version is not stated | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0896 | rwb-access sandbox seed: the owner, the key format and the retirement rule of the DEV synthetic test identity per role are not specified | Platform administrator | Resolved (directive) |
| GAP-0897 | rwb-access sandbox seed: the per-service login name and the DEV-only read-only role over rwb_access are not fixed for the target schema | Platform DB owner | Resolved (directive) |
| GAP-0898 | rwb-access sandbox seed: the authorise and me/permissions request and answer shapes, and the screen route that shows the seeded rows, are absent from the TSD appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0899 | rwb-access sandbox seed: the legacy seed loads 54 roles, while the TSD P4 RBAC matrix tabulates 42 role rows, and the difference is not enumerated | Business analyst, P4 | Resolved (directive) |
| GAP-0900 | rwb-access sandbox seed: the matrix letters for 11 of the 14 capability areas are not tabulated, so the seed content has no source table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0934 | The object attributes an authorise request carries are not specified | Solution architect | Resolved (directive) |
| GAP-0987 | Authority attributes, matrix version label and role roster for an allocation and queue read | Solution architect of rwb-access | Resolved (directive) |
| GAP-0989 | The authorise attribute set, the policy version labels and the full field-ID roster of the read-only case record view are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1036 | Producer-side AsyncAPI and JSON schema of rwb.document.events.v1 are not assigned to a contract story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1047 | The agent's document-read tool contract is not defined in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1048 | The idempotency-key format of DocumentStored and the event field names the agent reads are not defined | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1049 | The mask format and the per-role list of personal fields for SY-AGENT are not defined | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1050 | The read behaviour for a stored document whose type has left the version in force is not defined | Business analyst, P5 | Resolved (directive) |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1052 | The file-name pattern of the synthetic documents is not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1054 | The count of held intake items per exception shape and the pages each held item carries are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1532 | The screening feature is titled at L1 and its main criterion stores a shadow run that creates no deviation | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1563 | The BRD assigns payment matching to rwb-case while Architecture v5 gives it to rwb-payment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1646 | The data lake and the Power BI connection are removed but the whole reporting FSD is built on them | Solution architect | Resolved (directive) |
| GAP-1649 | The measure set is six definitions in one acceptance criterion and seven measures in another | Tribe lead with the Reporting and BI analyst | Resolved (directive) |
| GAP-1658 | SCR-37 has no owner and no serving path | Solution architect | Resolved (directive) |
| GAP-1662 | RWB-E2-009 promises a Power BI data set, which ADR-018 removes | Solution architect | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1817 | Three FSD integration points name the Quartz scheduler, which Architecture v5 and the Temporal design replace with durable timers in DeviationWorkflow | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1820 | The FSD records an approver on a deviation while the S8 row has no rwb-decision cell and no approval workflow is named for this service | Solution architect with the S8 business analyst | Resolved (directive) |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1830 | The two deviation screens have no owner cell in the Architecture screen matrix and no recorded route at the edge | Solution architect | Resolved (directive) |
| GAP-1831 | The wording, the Thai version and the approver of the eight messages the service shows are not in the FSD | Business analyst, S8 | Resolved (directive) |
| GAP-1832 | The two deviation events have a catalogue row and a topic but no field list, while the criteria expect an agent verdict and a decision log entry to travel with them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-1834 | The change notes of FSD S8 versions 1 and 2 are not in the sources read | Business analyst, S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2137 | Which service seeds which rows of the shared case set is not specified | QA | Resolved (directive) |
| GAP-2150 | The worked example is a monolith story key with no service and no realignment equivalent | Document owner; analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2154 | The seed, business date, volumes and identifiers of the synthetic fixture set are not stated | QA lead | Resolved (directive) |
| GAP-2161 | Two Work Packages write the same three story files and three fragments for legacy RWB-E1-064 on rwb-source-data | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2193 | RWB-P10-E2029-APP: values the sources leave open for the screening L1 app slice | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2194 | RWB-P10-E2029-CON: contract detail the sources leave open for the screening key | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2249 | Task and timer counts per seeded case, and the timer offsets beyond the FSD P3 AC-ALT-P3-011 offsets, are not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2250 | The distribution of the 2,812 seeded cases across the 12 queues and 48 members is not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2251 | The rwb-case login name, the DEV read-only role name and the field identifiers of six seeded tables are not in the sources | TechX and the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2252 | The decision code and the payload of the decision records the seed writes are not in the sources | TechX and the rwb-decision contract owner | Resolved (directive) |
| GAP-2326 | The agent-authority part of POST /authorise has no operation row, request shape or answer shape in any source | Solution architect, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2327 | The reason-code vocabulary of a refusal and the status of each code are not specified | Solution architect, P4 and the security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2329 | The default scope of the agent service identity is not specified for this legacy key | Security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2402 | No source gives the wire shapes, the value sets or the dependency rows this story needs: the append request and answer, the evaluation and run reads, the case-less approval row, the promotion decision code, the text of MSG-P7-009, the name behind EV-30 and the DP-02 login name | Solution architect, P7 rwb-decision, with the P10 rwb-agent owner, the rwb-case owner, the data steward and the delivery lead | Resolved (directive) |
| GAP-2439 | The physical columns of rule_package_version and the payload a compiled package is served in are not in the sources | TechX and the P7 solution architect | Resolved (directive) |
| GAP-2440 | The rule ID of the same allocation row is ALLOC-014 in the legacy story and ALLOC-MTG-BKK-01 in the FSD | P7 business analyst and the reference data administrator | Resolved (directive) |
| GAP-2441 | How the business date, the queue identifier and the owner identifier travel in the decision record is not in the sources | P7 and P3 contract owners | Resolved (directive) |
| GAP-2442 | The text of MSG-P7-009, the text of the chain-break warning and the field name of the per-entry chain result are not in the sources | P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2443 | No provided operation of the Ownership Map serves a compiled rule package version to the owning service | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2500 | Transfer decision record and ledger read: the decision code, the MSG-P7-009 text, the answer element, the no-version answer and the DP-02 login name are not specified | P7 business analyst and solution architect, with the API specification owner | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2502 | Decision-record event naming and the boundary with RWB-P7-E1008-APP and RWB-P7-E2027-APP | P7 solution architect, with the event platform owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2570 | RWB-E1-013: the Power BI refresh that AC3 asserts has no mechanism once the data lake is removed, and the measures read is assigned to Epic 2 by the legacy story | Solution architect | Resolved (directive) |
| GAP-2576 | rwb-reporting steering dashboard (application slice): the consumed operation names, the workflow and activity names, the read-model design, the INT-19 replacement and the agent fact source are fixed by no single source | Solution architect, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the reporting service | Resolved (directive) |
| GAP-2577 | rwb-reporting steering dashboard (contract slice): the element names of the consumed declarations, the event envelope naming, the Measure delta, the schema increments and the file shape of the extract are fixed by no single source | Contract owner of rwb-reporting, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the event platform | Resolved (directive) |
| GAP-2578 | rwb-reporting steering dashboard (deployment slice): the login and secret reference, the replica and threshold values, the consumer offset and retention policy, the catch-up window, the backfill limit and the message ID of the run alert are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2579 | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-3072 | RWB-S8-E1020-APP: the allocation-to-deviation boundary, the handler roster, the assignment method and any handler cap have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3073 | RWB-S8-E1020-APP: the key has no contract story of its own, the event names are taken from the TSD, and the business wave is earlier than the service wave | Programme lead and solution architect | Resolved (directive) |
| GAP-3074 | The business epic places the story in wave 1 while the service sits in wave 2 | Programme planner with the S8 service owner | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3076 | No source publishes the operation names of the six rows this slice consumes | P1 rwb-source-data owner, P3 rwb-case owner, P4 rwb-access owner, P7 rwb-decision owner and the S8 service owner | Resolved (directive) |
| GAP-3077 | No source says which service hosts the TRANSFER package evaluation after the split | Solution architect with the S8 service owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-3079 | The event names of the P3 and P1 subscriptions are not published | P3 rwb-case owner, P1 rwb-source-data owner and the S8 service owner | Resolved (directive) |
| GAP-3080 | No source fixes where this slice records the rule ID and the package version of a transfer | S8 service owner with the data steward of module S8 and the P3 rwb-case owner | Resolved (directive) |
| GAP-3081 | RWB-S8-E1023-APP: the five read operations and the four consumed operation names of the case record view have no published baseline, and the freshness, scope and mask answers of the owners are unnamed | Solution architect | Resolved (directive) |
| GAP-3082 | RWB-S8-E1023-APP: a P3 Case and workflow module story is placed in rwb-deviation with an empty build row, and the plan gives the slice no platform dependency although seven pattern rows add one | Solution architect | Resolved (directive) |
| GAP-3083 | RWB-S8-E1023-APP: the plan assigns the slice no legacy acceptance criterion while it keeps thirteen legacy test cases, and the legacy criteria lose their owned ids | Solution architect | Resolved (directive) |
| GAP-3084 | RWB-S8-E1023-APP: the story wave is 1 by the business-epic map while the service wave is 2 in Arch v5, and the section timeout and the six lists have no published values for this page | Solution architect | Resolved (directive) |
| GAP-3085 | RWB-S8-E1062-APP: the deviation estate the shadow screening run reads has no read operation, no published agent-policy read, no owner role for R-DEV-05 and R-DEV-06, no value for the answer limit and no test level | Solution architect, with the rwb-deviation owner, the rule-set owner of the Deviations package, the rwb-agent contract owner, the rwb-case parameter and reference-data owners, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3086 | RWB-S8-E1065-APP: the deviation slice of the sandbox has no published case-reference source, no deviation count per case or per code, no operation or field names for the stage contract read, no codes or owner roles for R-DEV-05 and R-DEV-06, no test level for the ten legacy cases and an empty H row for eight patterns | Solution architect, with the rwb-deviation owner, the rwb-case and rwb-document owners, the rwb-source-data sandbox owner, the rule-set owner of the Deviations package, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3087 | RWB-S8-E2009-APP: a P9 Reporting story is placed in rwb-deviation with one C row and an empty build row, and the seven owner reads, the matrix edge and the platform prerequisites are unpublished | Solution architect | Resolved (directive) |
| GAP-3088 | RWB-S8-E2009-APP: DP-17 removes the data lake, so the INT-19 extract and the Power BI data set of the story have no target owner and no replacement path in this service | Solution architect | Resolved (directive) |
| GAP-3089 | RWB-S8-E2009-APP: the plan assigns the slice no legacy acceptance criterion while it keeps ten legacy test cases, and the legacy criteria lose their owned ids | Solution architect | Resolved (directive) |
| GAP-3090 | RWB-S8-E2009-APP: the schedule time, the dimension format, the two added Measure fields and the alert recipients have no published values for the deviation serving | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3092 | The operation names and shapes of the consumed contracts other than RWB-P3-E2012-CON are not published | Solution architect | Resolved (directive) |
| GAP-3093 | The open-deviation read the P3 slice names is not a row of the Ownership Map, and the S8 event subscription already carries the same fact | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3095 | The event names of the case status and legal-hold changes this service consumes are not published | Solution architect | Resolved (directive) |
| GAP-3096 | deviation has no transfer reason, rule ID or rule-version column, and the legacy write set is on the rwb-case tables | Solution architect | Resolved (directive) |
| GAP-3098 | The fifteen legacy test case IDs of RWB-E2-012 are carried by both slices | QA lead | Resolved (directive) |
| GAP-3100 | RWB-S8-E2029-APP: the confirmed-proposal raise has no published request shape beyond the legacy Java signature, no operation name for the agent-policy read, no published constraint for one open code, no envelope type for the decision-record entry and no test level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3168 | The sandbox story applies three migrations where 19 schemas now need their own sequence | ACE DB lead | Resolved (directive) |
| GAP-3173 | Service S8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3207 | No source names the rwb-case database login or where the caseload cap is stored | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3208 | The schedule expression of the DailyCaseRun (legacy JOB-03) is not stated by any source | Solution architect | Resolved (directive) |
| GAP-3209 | No single source divides the thirteen legacy criteria of RWB-E1-020 across its seven stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S8-E1021-APP | skipped AC ID | 126 | missing: AC16, AC17 |
| RWB-S8-E1021-APP | new AC without TC row | 493 | AC11 is new and no section 16 row covers it |
| RWB-S8-E1062-APP | skipped AC ID | 112 | missing: AC10, AC11, AC12 |
| RWB-S8-E2009-APP | unknown story key | 24 | RWB-S8-E2009-CON is not a story of the set: \| Contract dependencies \| RWB-S8-E2009-CON; RWB-P9-E2009-CON; builds against contract version v1 (path /api/recovery/deviation/v1, DP-13) \| |
| RWB-S8-E2012-APP | unknown story key | 24 | RWB-S8-E2012-CON is not a story of the set: \| Contract dependencies \| RWB-P3-E2012-CON, RWB-S8-E2012-CON (built against the /v1 path; contract version Not specified in the source docum |
| RWB-S8-E2015-APP | skipped AC ID | 115 | missing: AC10, AC11, AC12 |
