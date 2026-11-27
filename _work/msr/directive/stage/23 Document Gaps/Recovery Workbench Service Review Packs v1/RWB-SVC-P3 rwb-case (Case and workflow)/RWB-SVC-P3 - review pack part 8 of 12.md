# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 8 of 12 (RWB-P3-E2007-APP to RWB-P3-E2013-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 183 |
| Cross-document (pending in another document) | 179 |
| Not applied (value not in the sources) | 28 |
| Open business decisions | 30 |
| Register gaps linked | 89 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E2007-APP | 28 | 39 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2007 APP Booking confirmation from the ALS load v2.md |
| RWB-P3-E2009-APP | 28 | 25 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2009 APP Steering dashboard v1 data set v2.md |
| RWB-P3-E2011-APP | 22 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2011 APP Queue view screens my queue, team queues, filters and ageing v2.md |
| RWB-P3-E2011-CON | 15 | 11 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2011 CON Queue view screens my queue, team queues, filters and ageing - contract v2.md |
| RWB-P3-E2012-APP | 22 | 20 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2012 APP Manual transfer and reassignment screen with reason v2.md |
| RWB-P3-E2012-CON | 20 | 18 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2012 CON Manual transfer and reassignment screen with reason - contract v2.md |
| RWB-P3-E2012-OPS | 19 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2012 OPS Manual transfer and reassignment screen with reason - deployment v2.md |
| RWB-P3-E2013-APP | 29 | 33 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2013 APP Approval routing with the delegation of authority table v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E2013-APP | R-00912 | CG-ALL-4161 | Script gap | Product owner | The story adds DECLINED_BY_APPROVER_SET to the closed list LOV-CASE-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-E2007-APP | R-10405 | CG-ALL-4066 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2009-APP | R-10412 | CG-ALL-4084 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2012-APP | R-10419 | CG-ALL-4125 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2012-CON | R-10422 | CG-ALL-4143 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2013-APP | R-10429 | CG-ALL-4173 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22435 | GAP-1663 | Register gap | Solution architect with the AI product owner | No event source is named for the agent acceptance and override measures | Count the two rates from the decision record, which carries the agent and prompt version, the recommendation, the approval and the outcome |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22439 | GAP-3178 | Register gap | Reporting and BI lead with the data product owner | RWB-E2-009 writes an INT-19 extract for a data lake that the target removes | Name the read model or event topic the Power BI data set subscribes to after the data lake removal, and update the acceptance criteria of RWB-E2-009 once. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22463 | GAP-1616 | Register gap | Risk and model risk officer with the rwb-access owner | The delegation of authority table is loaded and approved inside P7 while the ownership ruling gives the table to rwb-access | Keep in this service only the lookup at the moment of the decision and the recording of the row ID and version; move A2.24 with AC-P7-024-01 to AC-EXC-P7-024-05 to rwb-access, and confirm the lookup answer shape (level, row ID, version, NOT_COVERED, RELATED_PARTY reason) in the access contract. Until then this PRD reads the limits and records the version, and OQ-P7-05 stays open. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22470 | GAP-1253 | Register gap | Business lead with the Center of excellence | The escalation ceiling and the service level values of an approval are not specified | Fix three values as data owned by RW-COE: the service level per decision and per default, the escalation step in working days, and a maximum escalation count with its ceiling behaviour (hold, incident to RW-RISK, or committee). Carry them as rwb.approval.service-level.*, rwb.approval.escalation.step and rwb.approval.escalation.max-levels and close DL22. |
| RWB-P3-E2011-APP, RWB-P3-E2011-CON | R-22994 | GAP-0707 | Register gap | Product owner for queue and caseload rules | The cap a per-owner queue count is measured against: the queue capacity or the member's personal capacity | Fix the cap in force per queue as a rule of the queue reference data: read queue.capacity_cap when the queue sets one, otherwise queue_member.capacity; until that rule is settled the app story reads queue.capacity_cap, which is the cap AC2 fixes at 150. |
| RWB-ITG-E1013-ITG, RWB-ITG-E2009-ITG, RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E2009-APP, RWB-P9-E1013-APP, RWB-P9-E1013-CON, RWB-P9-E1013-OPS, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-P9-E8001-APP, RWB-P9-E8001-CON, RWB-P9-E8002-APP, RWB-P9-E8002-CON, RWB-S8-E2009-APP | R-28480 | GAP-1644 | Register gap | Business lead | The program BRD has no requirement section for P9 reporting | Keep the epic-level keys as the trace target and state the coverage basis in section 11.2 until a P9 requirement section exists |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-28752 | GAP-1659 | Register gap | Risk and model risk officer | No target is set for agent acceptance and override | Publish the two rates per agent and version and set no threshold until one is agreed |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28761 | GAP-3094 | Register gap | Business lead | The handler rows R-DEV-04 to R-DEV-06 and the SCR-05 deviation fragment layout are not in the sources | Read the four rows from the Business Rules and Routing Logic workbook at build time, render the fragment as a table of code, handler, paused state, contact stop and rule ID, and confirm the layout with the screen owner. |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28763 | GAP-3097 | Register gap | Business lead | The transfer reason codes R01 to R06 are an assumed set pending DL23 | Read the list at its version on the rwb-case reference-data contract, render whatever is in force, and hold the six codes as the default set until DL23 closes. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P3-E2011-APP, RWB-P3-E2011-CON | R-36379 | ASM-1254 | Register assumption |  | The cap a per-owner queue count is measured against is queue.capacity_cap when the queue sets one, and queue_member.capacity otherwise; the 150 of the legacy criteria is a queue cap, not a personal one. | Product owner for queue and caseload rules, at the baseline review of RWB-P3-E2011-CON. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E2007-APP | R-00871 | CG-ALL-4067 | 12.5 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment for rwb-case is not ruled in the sources; the line naming the package (L297) is outside this chunk. Needs the solution architect's ruling; no name invented. |
| RWB-P3-E2007-APP | R-00872 | CG-ALL-4068 | 12.5 | Java package th.co.scb.ace.workbench.recovery.case.bookingconfirmation uses the reserved word 'case' | No replacement package segment for the bookingconfirmation package is in the sources (L297 outside chunk). Needs the solution architect's ruling; no name invented. |
| RWB-P3-E2007-APP | R-16106 | DOR-RWB-P3-E2007-APP-10 | 4 | Definition of Ready item 10 Screens and states: Partial | Screen states are not in the sources (FSD P3 l.4512 and S2 l.1500 give only purpose). SCR-29 is not in this chunk, so its states cannot be marked here. |
| RWB-P3-E2007-APP | R-25054 | CG-ALL-4069 | 13 | Flyway file V2007_1__booking_confirmation.sql is not in the V0001..Vnnnn form | Next free rwb-case Flyway number is not in the sources; migration name line (L339) is outside this chunk. Needs the solution architect. |
| RWB-P3-E2007-APP | R-28728 | GAP-2491 | 8 | The timezone, overlap, retry and fallback of the JOB-08 run and the behaviour of the legacy feature flag when off are in no source | Run rules are not in any source, so no business rule is stated; the item is not resolved by the story. |
| RWB-P3-E2009-APP | R-00874 | CG-ALL-4085 | 12.4 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment for 'case' is the solution architect's ruling. Service Template Specification v1 is not in the folder; no rwb_case package name found. Not invented. |
| RWB-P3-E2009-APP | R-00875 | CG-ALL-4086 | 12.4 | Java package th.co.scb.ace.workbench.recovery.case.casefacts uses the reserved word 'case' | Same as CG-ALL-4085: package segment awaits the solution architect's ruling; Service Template Specification v1 absent from the folder. Not invented. |
| RWB-P3-E2009-APP | R-25062 | CG-ALL-4087 | 12.9 | Flyway file V2009_1__case_fact_read_index.sql is not in the V0001..Vnnnn form | Next Vnnnn of the rwb_case Flyway sequence needs the Service Template Specification v1 (absent from folder). No number invented; migration name left as is. |
| RWB-P3-E2011-APP | R-00880 | CG-ALL-4097 | not located | Java package th.co.scb.ace.workbench.recovery.case.queueview uses the reserved word 'case' | Package segment replacing 'case' is not in any source document (grep found no match for queueview or the Service Template Specification naming rule). Needs Solution architect ruling; no name invented. |
| RWB-P3-E2011-CON | R-05225 | DOR-RWB-P3-E2011-CON-14 | Header | Definition of Ready item 14 Epic design: Fail | Placeholder row added to header table. No signed epic design record in 04 User stories (searched 'epic design', 'sign-off'); sign-off cannot be confirmed from sources. |
| RWB-P3-E2011-CON | R-16129 | DOR-RWB-P3-E2011-CON-10 | Not located in chunk | Definition of Ready item 10 Screens and states: Partial | SCR-02 and SCR-07 state rows are outside this chunk; exact text needed to add Error and No access (SCR-02) and Empty, Error, No access (SCR-07) states. |
| RWB-P3-E2012-APP | R-00892 | CG-ALL-4126 | 1 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Segment ruling from Solution architect is not in sources. Service Template Spec v1 is not in 03 folder. PRD and FSD P3 repeat 'case'. No segment invented. |
| RWB-P3-E2012-APP | R-00893 | CG-ALL-4127 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.transfer uses the reserved word 'case' | Segment ruling from Solution architect is not in sources. Service Template Spec v1 is not in 03 folder. PRD and FSD P3 repeat 'case'. No segment invented. |
| RWB-P3-E2012-APP | R-05229 | DOR-RWB-P3-E2012-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in story or sources. Sign-off must be confirmed in the epic design record, not written into the story. |
| RWB-P3-E2012-APP | R-05231 | DOR-RWB-P3-E2012-APP-17 |  | Definition of Ready item 17 Dependencies: Fail | Text naming RWB-P7-E1073-CON is not in the supplied parts. RWB-P3-E2012-OPS build dependency is not done and an edit cannot change that. |
| RWB-P3-E2012-APP | R-16134 | DOR-RWB-P3-E2012-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-05, SCR-07 and SCR-09 state text is outside the supplied parts. Empty, loading and error text is not in the sources. |
| RWB-P3-E2012-APP | R-22452 | GAP-0396 | 16 | Gateway-bff composite transfer route, harness environment, seeding, evidence format and gate not specified | Route, harness, seeding, evidence and gate are not in the sources. Section 16 placeholder needs its current text, which is not in this chunk. |
| RWB-P3-E2012-APP | R-25078 | CG-ALL-4128 | 7 | Criteria and tests keep legacy job and decision-log wording | L156, L226 and L252 are identical, so old text needs the preceding lines, which are not in this chunk. AC1 and AC3 lines are truncated. Needs those lines. |
| RWB-P3-E2012-CON | R-00899 | CG-ALL-4137 |  | rwb-case.yaml holds transferReasonCode as a closed enum while the story reads LOV-TRANSFER-REASON as data | Ruling is closed list (Reference Data v5 Lists); rwb-case.yaml enum stays. The story sentence treating LOV-TRANSFER-REASON as data is outside this chunk, so it cannot be copied exactly. |
| RWB-P3-E2012-CON | R-05236 | DOR-RWB-P3-E2012-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | Not specified in the source documents (DOR-RWB-P3-E2012-CON-14). No signed epic design record is in the sources; section 14 text is outside this chunk. |
| RWB-P3-E2012-CON | R-16142 | DOR-RWB-P3-E2012-CON-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Empty, loading, error and no-access states are not in the sources. Section 10 text is outside this chunk, so no exact old text can be copied. |
| RWB-P3-E2012-CON | R-22452 | GAP-0396 |  | Gateway-bff composite transfer route, harness environment, seeding, evidence format and gate not specified | No route, harness, seeding or gate values in the sources. Integration lead fixes them at the wave 2 entry check. No copyable story text in this chunk. |
| RWB-P3-E2012-CON | R-22458 | GAP-2501 | 13 | The DP table adds platform and published contracts that the metadata rows do not carry | Metadata rows kept as the plan gives them. Dependency Map and section 13 text for the DP-added H and C entries is outside this chunk, so it cannot be copied exactly. |
| RWB-P3-E2013-APP | R-05248 | DOR-RWB-P3-E2013-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in 01 Decisions and governance or the story. Sign-off cannot be confirmed from sources; story unchanged. |
| RWB-P3-E2013-APP | R-05249 | DOR-RWB-P3-E2013-APP-16 | Header | Definition of Ready item 16 Size: Fail | Size is not in the sources, so the item cannot be resolved here. |
| RWB-P3-E2013-APP | R-16158 | DOR-RWB-P3-E2013-APP-10 | 12 | Definition of Ready item 10 Screens and states: Partial | Screen states for SCR-01, 02, 03, 10 are in section 12, outside this chunk. No state text in sources to copy; story unchanged. |
| RWB-P3-E2013-APP | R-16159 | DOR-RWB-P3-E2013-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | No personal-data classification for P3 fields in the PRD or FSD. Marking fields would invent it; story unchanged. |
| RWB-P3-E2013-APP | R-25090 | CG-ALL-4176 | 12.9 | Flyway file V2013_1__case_approval_task.sql is not in the V0001..Vnnnn form | Next number of the rwb-case Flyway sequence is not in PRD P3, FSD P3 or the sources searched. Migration name at line 417 is outside this chunk. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06635 | RWB-P3-E2007-APP | NEWAC-RWB-P3-E2007-APP-AC12 | 7, 12.2, 14 | MSG-P4-001 and MSG-P4-003 rows marked Not specified until their text is copied from the target |
| CDC-06662 | RWB-P3-E2011-APP | CG-ALL-4092 | 1 | Remove the fixed status enum and declare status as a string whose values are read from LOV-CASE-STATUS. |
| CDC-06663 | RWB-P3-E2011-APP | CG-ALL-4093 | 1 | Remove the fixed routeCode enum and declare routeCode as a string whose values are read from LOV-ROUTE. |
| CDC-06664 | RWB-P3-E2011-APP | CG-ALL-4094 | 1 | Remove the fixed stageCode enum and declare stageCode as a string whose values are read from LOV-STAGE. |
| CDC-06667 | RWB-P3-E2011-APP | DOR-RWB-P3-E2011-APP-8 | none | rwb-access must publish POST /api/recovery/access/v1/authorise; rwb-case.yaml must hold status, routeCode and stageCode as LOV-read data, not closed enums. |
| CDC-06672 | RWB-P3-E2011-CON | CG-ALL-4104 | 3 | Remove the closed enum on status so LOV-CASE-STATUS values are data, as the story states at the rwb-case contract line. |
| CDC-06673 | RWB-P3-E2011-CON | CG-ALL-4105 | 3 | Remove the closed enum on routeCode so LOV-ROUTE values are data, as the story states. |
| CDC-06674 | RWB-P3-E2011-CON | CG-ALL-4106 | 3 | Remove the closed enum on stageCode so LOV-STAGE values are data, as the story states. |
| CDC-06686 | RWB-P3-E2012-APP | CG-ALL-4118 | 3 | Remove the fixed enum on transferReasonCode so LOV-TRANSFER-REASON values are data read through the reference-list operation. |
| CDC-06742 | RWB-P3-E2013-APP | CG-ALL-4163 | 10 | Remove the fixed status enum so status is validated against LOV-CASE-STATUS as data, matching the story and Reference Data v5. |
| CDC-06743 | RWB-P3-E2013-APP | CG-ALL-4164 | 10 | Remove the fixed elementType enum so it is validated against LOV-ELEMENT as data, matching the story and Reference Data v5. |
| CDC-06744 | RWB-P3-E2013-APP | CG-ALL-4165 | 10 | Remove the fixed status enum for the task so it is validated against LOV-TASK-STATUS as data, matching the story and Reference Data v5. |
| CDC-06745 | RWB-P3-E2013-APP | CG-ALL-4166 | 10 | Remove the fixed timerType enum so it is validated against LOV-TIMER as data, matching the story and Reference Data v5. |
| CDC-06750 | RWB-P3-E2013-APP | DOR-RWB-P3-E2013-APP-8 | Header | Hold status, elementType and timerType as LOV references (LOV-CASE-STATUS, LOV-ELEMENT, LOV-TIMER) instead of closed enums, matching the story's data reads; also the other listed fields. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06630 | RWB-P3-E2007-APP | CG-ALL-4065 | 18 | Align REQ-CHO-008 test list to section 18: TC-E2-007-01 to -09 and -11 to -15; check TC-E2-006-01, -02, -08 against their owning story. |
| CDC-06655 | RWB-P3-E2009-APP | CG-ALL-4083 | 18 | Align the test case lists for REQ-WKM-009 and REQ-WKM-006 to RWB-P3-E2009-APP section 18. |
| CDC-06668 | RWB-P3-E2011-APP | DOR-RWB-P3-E2011-APP-12 | 12, 12.7, 16, 18 | Align section 18 test lists to RTM v7 once TC-E2-011-14 to TC-E2-011-16 are present in section 16. |
| CDC-06670 | RWB-P3-E2011-APP | CG-ALL-4096 | 18 | Align the test lists of REQ-WKM-001, REQ-WKM-002, REQ-WKM-006 and REQ-CWC-011 in the RTM to the test case lists of story section 18. |
| CDC-06678 | RWB-P3-E2011-CON | DOR-RWB-P3-E2011-CON-12 | 12.7, 16, 18 | Align §18 test lists with RTM v7 where they differ and add TC-P3-E2011-CON-10 to TC-P3-E2011-CON-12 there. |
| CDC-06681 | RWB-P3-E2011-CON | CG-ALL-4109 | 18 | Trace the same test cases as section 18 of RWB-P3-E2011-CON for each requirement whose list differs, replacing the legacy TC-E2-011 and TC-TE IDs with this story's TC IDs. |
| CDC-06699 | RWB-P3-E2012-APP | CG-ALL-4124 | 18 | Align the test-case lists for the five requirements with section 18 of this story in the next RTM version. |
| CDC-06716 | RWB-P3-E2012-CON | CG-ALL-4142 | 18 | Align the RTM test lists for REQ-WKM-003, REQ-WKM-007 and REQ-WKM-008 with section 18 of this story. |
| CDC-06735 | RWB-P3-E2012-OPS | CG-ALL-4155 | 18 | Align the traces of REQ-WKM-003, REQ-WKM-007 and REQ-WKM-008 to the TC-P3-E2012-OPS IDs in section 18 of this story. |
| CDC-06770 | RWB-P3-E2013-APP | CG-ALL-4172 | find it | Align the test lists of the nine differing requirements with section 18 of RWB-P3-E2013-APP in the next RTM version. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06608 | RWB-P3-E2007-APP | CG-ALL-4063 | 16 | Add a row for TC-E2-007-11 with Given, When and Then copied from AC8 (decision record write fails) and BR5, the criterion it covers. |
| CDC-06680 | RWB-P3-E2011-CON | CG-ALL-4108 | 16 | Add Story test cases rows for TC-P3-E2011-CON-01 to TC-P3-E2011-CON-12 with Given, When and Then copied from their criteria. |
| CDC-06691 | RWB-P3-E2012-APP | CG-ALL-4123 | 16 | Add a Story test cases row for TC-E2-012-15 with Given, When and Then copied from AC13. |
| CDC-06710 | RWB-P3-E2012-CON | DOR-RWB-P3-E2012-CON-12 | 12.7, 16 | Register TC-P3-E2012-CON-01 to TC-P3-E2012-CON-13 in Test Cases v8, and align the §18 test lists with RTM v7. |
| CDC-06715 | RWB-P3-E2012-CON | CG-ALL-4141 | 16 | Add rows for TC-P3-E2012-CON-01 to TC-P3-E2012-CON-12 with Given, When and Then copied from the criterion each covers. |
| CDC-06719 | RWB-P3-E2012-CON | GAP-3098 | 16 | Keep one row per legacy TC ID, record both slices against it, take End to end from the P3 slice and Component from this slice. |
| CDC-06734 | RWB-P3-E2012-OPS | CG-ALL-4154 | 16 | Add rows for TC-P3-E2012-OPS-01 to 06 with Given, When and Then copied from the criteria AC1 to AC6 they cover. |
| CDC-06740 | RWB-P3-E2012-OPS | GAP-3098 | find it | Keep one row per legacy TC ID (TC-E2-012-01 to 15); record both slices; End to end from the P3 slice, Component from this slice. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06598 | RWB-P3-E2007-APP | CG-ALL-4053 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story |
| CDC-06636 | RWB-P3-E2009-APP | CG-ALL-4076 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or re-point the consumer to a published operation (provider ruling). |
| CDC-06661 | RWB-P3-E2011-APP | CG-ALL-4091 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider's CON story, or have the story consume a published operation instead. |
| CDC-06671 | RWB-P3-E2011-CON | CG-ALL-4103 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's (P4 rwb-access) CON story. |
| CDC-06682 | RWB-P3-E2012-APP | CG-ALL-4114 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the rwb-access CON story. |
| CDC-06702 | RWB-P3-E2012-CON | CG-ALL-4132 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-06720 | RWB-P3-E2012-OPS | CG-ALL-4146 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access CON story, or agree a published operation to consume |

### RWB-P2-E2007-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06602 | RWB-P3-E2007-APP | DOR-RWB-P3-E2007-APP-21 | header | Publish the contract and bring the CON stories it depends on to Done |
| CDC-06603 | RWB-P3-E2007-APP | DOR-RWB-P3-E2007-APP-22 | header | Publish the contract fake library and record its version as published; the story cites RWB-P2-E2007-CON as its contract dependency. |
| CDC-06623 | RWB-P3-E2007-APP | GAP-0598 | 13 | DP-05 boundary marked Not specified in the source documents (GAP-0598) |
| CDC-06624 | RWB-P3-E2007-APP | GAP-0658 | 12 | Baseline result shape, task table, envelope, rerun operation, twelve consumed operations and seven fakes; record JOB-08 ownership and the TSD P2 v3 T5.2 supersession in the gap register; confirm seven message texts. |
| CDC-06626 | RWB-P3-E2007-APP | GAP-0730 | 13 | Fix the rwb-case login in the platform DB story; publish the composite route, treatment booking fields and raiseTask result schema with RWB-P2-E2007-CON and the S2 contract. |
| CDC-06627 | RWB-P3-E2007-APP | GAP-2486 | 12 | Take the operation set from the six legacy interfaces on the DP-13 base with one hop and a 2 s timeout; take the decision code from LOV-DECISION; fix read filters, page size, ordering and MSG-GEN-006 text before SIT. |

### RWB-P3-E2012-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06688 | RWB-P3-E2012-APP | DOR-RWB-P3-E2012-APP-21 |  | Publish the contract and set its build status from Not started to Done. |
| CDC-06689 | RWB-P3-E2012-APP | DOR-RWB-P3-E2012-APP-22 |  | Record the published contract fake library version in the contract story. |
| CDC-06725 | RWB-P3-E2012-OPS | DOR-RWB-P3-E2012-OPS-21 | header | Move build status of RWB-P3-E2012-CON from Not started to Done |
| CDC-06726 | RWB-P3-E2012-OPS | DOR-RWB-P3-E2012-OPS-22 | header | Record the contract fake library version as published in the contract document. |
| CDC-06730 | RWB-P3-E2012-OPS | GAP-0710 |  | Define one selection element in the rwb-case contract: an ordered array with caseId, assignment or refusal messageId, and done and total counts; order is the caller's order; summary derives from the array. |
| CDC-06731 | RWB-P3-E2012-OPS | GAP-0711 |  | Define a refusal element with reason code, owner list with open-case count and cap each, and current and target state; cap and hold are read inside the operation before the first write. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06597 | RWB-P3-E2007-APP | CG-ALL-4052 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{n}/{v} in rwb-decision.yaml through the provider's CON story |
| CDC-06684 | RWB-P3-E2012-APP | CG-ALL-4116 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in rwb-decision.yaml through the rwb-decision CON story. |
| CDC-06704 | RWB-P3-E2012-CON | CG-ALL-4134 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in rwb-decision.yaml through the provider's CON story. |
| CDC-06705 | RWB-P3-E2012-CON | CG-ALL-4135 | 12.2 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= in rwb-decision.yaml through the provider's CON story. |
| CDC-06722 | RWB-P3-E2012-OPS | CG-ALL-4148 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} through the rwb-decision CON story, or agree a published operation to consume |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06599 | RWB-P3-E2007-APP | CG-ALL-4055 | 13 | Create story RWB-P7-E1073-CON, or name the existing story of the same capability, and align the DP-04 dependency to that key |
| CDC-06601 | RWB-P3-E2007-APP | DOR-RWB-P3-E2007-APP-17 | header | Create story RWB-P7-E1073-CON, or name the existing story of the same capability, so the 10 named dependencies resolve |
| CDC-06685 | RWB-P3-E2012-APP | CG-ALL-4117 | 13 | Create story RWB-P7-E1073-CON for the DP-04 rule kit contract, or name the existing rwb-decision CON story in the DP-04 row. |
| CDC-06706 | RWB-P3-E2012-CON | CG-ALL-4136 | 13 | Create story RWB-P7-E1073-CON, or the story that replaces it under an existing key, so the dependency resolves. |
| CDC-06723 | RWB-P3-E2012-OPS | CG-ALL-4149 | 13 | Create RWB-P7-E1073-CON or name the existing story for the rwb-decision rule-package capability, then align the DP-04 reference |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06606 | RWB-P3-E2007-APP | CG-ALL-4059 | 12.5 | Add activity BookingConfirmation to the Activities sheet with task queue rwb-case. |
| CDC-06607 | RWB-P3-E2007-APP | CG-ALL-4060 | 12.5 | Add activity raiseTask (published contract) to the Activities sheet with task queue rwb-case. |
| CDC-06687 | RWB-P3-E2012-APP | CG-ALL-4120 | 12.5 | Add a Workflows row for ManualTransferWorkflow: task queue rwb-case, namespace rwb-recovery, one execution per manual request, as named in RWB-P3-E2012-APP section 12.5. |
| CDC-06756 | RWB-P3-E2013-APP | GAP-3177 | find it | Register the five-minute next-action Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06675 | RWB-P3-E2011-CON | CG-ALL-4110 | Not located in chunk | Solution architect to rule a Java package segment for rwb-case that is not a reserved word; replace 'recovery.case' in the rwb-case row (P3) of the Java package column (line 354) and the package in the Service Catalog. Story copies the ruled value. |
| CDC-06707 | RWB-P3-E2012-CON | CG-ALL-4144 | find it | Solution architect to rule the rwb-case package segment: rule at line 116 and row P3 at line 354 give 'case', a Java reserved word; no replacement name is in the sources. Story copies the ruling. |
| CDC-06746 | RWB-P3-E2013-APP | CG-ALL-4174 | 1 | Rule the package segment that replaces the reserved word 'case' in th.co.scb.ace.workbench.recovery.case (story line 37). |
| CDC-06747 | RWB-P3-E2013-APP | CG-ALL-4175 | 12.5 | Rule the package segment that replaces the reserved word 'case' in th.co.scb.ace.workbench.recovery.case.approval (story line 378). |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06718 | RWB-P3-E2012-CON | GAP-3095 | 14 | Publish event names, schemas and topic rows for the case status and legal-hold change events this service consumes. |
| CDC-06739 | RWB-P3-E2012-OPS | GAP-3095 | find it | Publish event names, schemas and topic rows for the case status and legal-hold changes this service consumes. |
| CDC-06752 | RWB-P3-E2013-APP | CG-ALL-4169 | 12.4 | Add rwb-case as a consumer of rwb.decision.ApprovalRequested.v1 (and its ACL), or drop the handler. |
| CDC-06753 | RWB-P3-E2013-APP | CG-ALL-4170 | 12.4 | Add rwb-case as a consumer of rwb.decision.ApprovalDecided.v1 (and its ACL), or drop the handler. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06620 | RWB-P3-E2007-APP | GAP-0922 | 13 | Add POST /authorise with its request and answer schema; publish with RWB-P4-E1037-CON, stub it in the contract fake, fix the rwb-access login and publish the composite route with gateway-bff (DP-19). |
| CDC-06697 | RWB-P3-E2012-APP | GAP-3093 | 12.2 | Publish GET /cases/{caseId}/deviations as the read used by the move and SCR-05; keep DeviationRaised and DeviationCleared for the event-fed flag; fix the read schema. |
| CDC-06762 | RWB-P3-E2013-APP | GAP-0928 | find it | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with the query and response fields this story uses; correct the omission in favour of Architecture v5 under R-PREC. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06634 | RWB-P3-E2007-APP | GAP-3232 | Header | State the template baseline once on the Dependency classes sheet and use the catalog as the source of the v5 graph; story files keep their rows. |
| CDC-06660 | RWB-P3-E2009-APP | GAP-3232 | find it | State the template baseline once on the Dependency classes sheet; the catalog remains the source of the v5 graph. |
| CDC-06774 | RWB-P3-E2013-APP | GAP-3232 |  | Keep the catalog as source of the v5 graph and state the template baseline once on the Dependency classes sheet; no story re-cut. |

### RWB-S8-E2009-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06652 | RWB-P3-E2009-APP | GAP-3088 | find it | Drop the INT-19 extract, keep the freshness stamp on the 07:30 screen refresh, move the Power BI data set to the rwb-reporting read model built from events; confirm path with reporting owner. |
| CDC-06653 | RWB-P3-E2009-APP | GAP-3089 | find it | Keep acs empty; restate AC1 to AC9 as new under D-RCV-60 with legacy values; carry TC-E2-009-01 to -10 unchanged; map TC-E2-009-10 to access refusal; record mapping in section 18. |
| CDC-06654 | RWB-P3-E2009-APP | GAP-3087 | find it | Record slice as secondary serving of the steering set in S8; keep C row and empty H row; publish seven consumed operation names with owners before tagging; confirm load-time edge with P9 and S8 owners. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06677 | RWB-P3-E2011-CON | DOR-RWB-P3-E2011-CON-1 | 1 | Add 'tech lead' as a role code or role name in Users Roles and Permissions v5 |
| CDC-06709 | RWB-P3-E2012-CON | DOR-RWB-P3-E2012-CON-1 | 1 | Name a role code or role name for the case service consumer (gateway-bff composite route, transfer screen, test stories of RWB-P3-E2012-CON), or confirm it is a system consumer and not a user role. |
| CDC-06764 | RWB-P3-E2013-APP | GAP-0930 | find it | Add the rwb-decision service identity with Approval check R and no other Recovery right, confirmed by the security administrator before the authorise contract is frozen. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06683 | RWB-P3-E2012-APP | CG-ALL-4115 | 12.2 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/deviations in rwb-deviation.yaml through the rwb-deviation CON story. |
| CDC-06703 | RWB-P3-E2012-CON | CG-ALL-4133 | 12.2 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/deviations in rwb-deviation.yaml through the provider's CON story. |
| CDC-06721 | RWB-P3-E2012-OPS | CG-ALL-4147 | 12.2 | Publish GET /api/recovery/deviation/v1/cases/{caseId}/deviations through the rwb-deviation CON story, or agree a published operation to consume |

### RWB-P7-E2013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06748 | RWB-P3-E2013-APP | DOR-RWB-P3-E2013-APP-21 | Header | Create the contract story for legacy key RWB-E2-013 and move it and the CON stories this story depends on to Done. |
| CDC-06749 | RWB-P3-E2013-APP | DOR-RWB-P3-E2013-APP-22 | Header | Publish the contract fake library and record its published version. |
| CDC-06767 | RWB-P3-E2013-APP | GAP-1255 | find it | Baseline the five approval operations and the case-status operation with TSD P7 T3.1 field names in camelCase, page and error conventions, and the required property of each ApprovalAction call. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06600 | RWB-P3-E2007-APP | DOR-RWB-P3-E2007-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-P3 in the epic design record |
| CDC-06724 | RWB-P3-E2012-OPS | DOR-RWB-P3-E2012-OPS-14 | none | Record the signed epic design sign-off in the epic design record |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06642 | RWB-P3-E2009-APP | GAP-0255 |  | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate; queue measures stay with P3 rwb_case. |
| CDC-06658 | RWB-P3-E2009-APP | GAP-0258 | find it | Read Power BI wording as consumed through rwb-reporting; dashboards and reports served via GET /dashboards/{id} and GET /reports/{id}. |

### RWB-P3-E2011-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06665 | RWB-P3-E2011-APP | DOR-RWB-P3-E2011-APP-21 | header | Build the contract story to Done; its build status is currently Not started. |
| CDC-06666 | RWB-P3-E2011-APP | DOR-RWB-P3-E2011-APP-22 | header | Publish the contract fake library and record its version. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06693 | RWB-P3-E2012-APP | DOR-RWB-P3-E2012-APP-9 | 14 | Make MSG-P3-027 text match the standard, or record why it differs. Story section 14 text is not changed here. |
| CDC-06711 | RWB-P3-E2012-CON | DOR-RWB-P3-E2012-CON-9 | 14 | Align MSG-P3-027 text to the standard v4 wording; the v4 text is not in this chunk, so section 14 is unchanged. |

### OTHER:rwb-case API contract (transfer operation) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06695 | RWB-P3-E2012-APP | GAP-0710 | 14 | Add one ordered selection element: caseId, the assignment or messageId of the refusal, done and total counts; order is the caller's order. |
| CDC-06696 | RWB-P3-E2012-APP | GAP-0711 | 14 | Add a refusal element with reason code, owner list with open-case count and cap each, and current and target state. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06698 | RWB-P3-E2012-APP | GAP-2501 | 13 | Record the DP-added H and C contracts (DP-03, DP-04, DP-07, DP-09, DP-10, DP-14, DP-15, DP-19) as non-blocking, built against their fakes. |
| CDC-06733 | RWB-P3-E2012-OPS | GAP-2501 |  | Record H RWB-PLT-E1027-CON, H RWB-PLT-E1072-CON, C RWB-P7-E1073-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1047-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON as non-blocking, built against fakes. |

### RWB-S8-E2012-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06701 | RWB-P3-E2012-APP | GAP-3091 | header | Depends on (build) kept as the story's build list; plan build list to be aligned in the plan. |
| CDC-06741 | RWB-P3-E2012-OPS | GAP-3091 | find it | Add the eight platform H rows and the C row RWB-P7-E1073-CON as tracked dependencies; keep Depends on None and Ready to start Day 1. |

### RWB-P7-E2027-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06712 | RWB-P3-E2012-CON | GAP-2502 | find it | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 in section 12.3 instead of rwb.decision-record.DecisionRecorded.v1. |
| CDC-06728 | RWB-P3-E2012-OPS | GAP-2502 |  | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 instead of rwb.decision-record.DecisionRecorded.v1; ingest, chain and JOB-14 stay in RWB-P7-E1008-APP. |

### OTHER:CON story of rwb-deviation (S8) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06714 | RWB-P3-E2012-CON | GAP-3093 | find it | Publish GET /cases/{caseId}/deviations on /api/recovery/deviation/v1 with its read schema; keep DeviationRaised and DeviationCleared for the event-fed flag. |
| CDC-06732 | RWB-P3-E2012-OPS | GAP-3093 |  | Publish GET /cases/{caseId}/deviations on /api/recovery/deviation/v1 as the move and SCR-05 read; keep DeviationRaised and DeviationCleared for the event-fed flag; fix the read schema. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06751 | RWB-P3-E2013-APP | CG-ALL-4162 | Not located in chunk | Add list LOV-OVERRIDE-REASON to Lists, or name the existing Reference Data v5 list the story should use instead. |
| CDC-06754 | RWB-P3-E2013-APP | DOR-RWB-P3-E2013-APP-20 | find it | Add list LOV-OVERRIDE-REASON. |

### OTHER:rwb-decision API yaml; OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06604 | RWB-P3-E2007-APP | DOR-RWB-P3-E2007-APP-8 | 12.1 | Publish GET /api/recovery/decision/v1/rule-models/{n}/{v} in rwb-decision and POST /api/recovery/access/v1/authorise in rwb-access. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:FSD S2 (A2.6.3.1; OTHER:A2.13.2; OTHER:A2.10.2; OTHER:A2.17.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06605 | RWB-P3-E2007-APP | GAP-1696 | 4 | Add S2 to the P1 REST cell; FSD S2 reads source facts only through the rwb-source-data contract, not ACE views, ALS, COLLINS, NLEADS or CCMS. |

### RWB-P2-E2007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06609 | RWB-P3-E2007-APP | DOR-RWB-P3-E2007-APP-11 | 11 | Align the personal-data classification of the fields with the section 11 statement that none is carried, or change that statement. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06610 | RWB-P3-E2007-APP | GAP-3175 |  | Name EV-26 AceDataReady (producer rwb-source-data) as the target event on rwb.source-data.events.v1, with LoadCompleted listed as its legacy alias. |

### OTHER:FSD P6 v3; OTHER:TSD P6 v2; RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06611 | RWB-P3-E2007-APP | GAP-2395 |  | Read the three Epic 2 package codes and version labels through the contract as the fixture set. Settle the rwb-comms rule package assignment with the rule registry owner before integration. Invent no fourth code. |

### OTHER:FSD S2 A1.1 and A2 prerequisites; OTHER:service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06612 | RWB-P3-E2007-APP | GAP-1713 |  | Map each FEAT prerequisite to its owning service contract (approval P7, case P3, documents P5, communications P6, valuation S1) and record the mapping once. Carry duplicate FEAT-CHO-08 as written. |

### OTHER:FSD S2 A2.10; OTHER:A2.11; OTHER:A2.17; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:13; OTHER:44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06613 | RWB-P3-E2007-APP | GAP-1703 |  | Record the booking reference from TreatmentBooked and the break from PaymentMissed. rwb-payment owns booking, matching and posting. The release request leaves through the integration contract. |

### RWB-P2-E2007-APP; RWB-P2-E2007-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:TSD P2 Integration v3 T5.2; OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06614 | RWB-P3-E2007-APP | GAP-0657 |  | Keep JOB-08 with rwb-integration and mark the slide 44 rwb-payment row superseded. Read ACE facts via the rwb-source-data contract and supersede TSD P2 v3 T5.2. Settle the consumed paths, shapes and login. |

### RWB-P2-E2007-CON; OTHER:TSD P1 v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06615 | RWB-P3-E2007-APP | GAP-0596 | 3 | Answer each Section B field as AVAILABLE or NOT_AVAILABLE with no value on NOT_AVAILABLE. Name flag rwb.dataengine.booking-facts, off until the Section B migration is applied. Record the reading in TSD P1. |

### RWB-P2-E2007-CON; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06616 | RWB-P3-E2007-APP | GAP-0597 | 12 | Publish GET /batch-status keyed by sourceSystem and businessDate with status, isComplete, startedAt, completedAt, recordCount and feedVersion. Return 404 with MSG-P1-001 when no batch row exists. |

### RWB-P2-E2007-CON; API:(service not named); RWB-P1-E1015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06617 | RWB-P3-E2007-APP | GAP-0594 | 11 | Publish GET /booking-facts and GET /batch-status on /api/recovery/source-data/v1 with BookingFact, BookingFactsAnswer, FieldState and BatchStatusAnswer. Keep freshness as DataProductFreshness of RWB-P1-E1015-CON. |

### RWB-P2-E2007-CON; RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06618 | RWB-P3-E2007-APP | GAP-0595 |  | Read the account set and product group from case_list_row for the case and business date. If not accepted, add C RWB-P3-E1018-CON and declare GET /api/recovery/case/v1/cases/{caseId}/accounts as the source. |

### OTHER:TSD P4 RBAC matrix T6.1; RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06619 | RWB-P3-E2007-APP | GAP-0923 | 12.1 | Add Case record and Treatment and offer columns to T6.1 and publish the 14-area matrix via RWB-P4-AD002-APP. Confirm RW-RESTRUCT and RW-CREDITAD letters with the matrix owner. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06621 | RWB-P3-E2007-APP | GAP-2485 | 13 | Record that this slice evaluates BOOKING_MATCH on the version it holds through the embedded kit; treatment state, task, route move and posting stay with their owners. |

### OTHER:Booking confirmation harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06622 | RWB-P3-E2007-APP | GAP-0395 | 4 | Agree the composite route path and merge order with the platform edge story, and the harness environment, ALS fixture format, seed pack, evidence format, retention and gate at the wave 2 entry check. |

### RWB-P2-E2007-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06625 | RWB-P3-E2007-APP | GAP-0659 | 13 | Fix identity, secret reference and probe checks; register the workflow on rwb-integration and record the JOB-08 owner conflict; take thresholds, windows and backfill limit as environment values; write the JOB-08 catalogue row and review runbook entries. |

### OTHER:rwb-decision event contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06628 | RWB-P3-E2007-APP | GAP-2487 | 4 | Publish rwb.decision.BookingDecisionMade.v1 per treatment and business date on rwb.decision.events.v1, keyed by treatmentId, with outcome, row, package code and version, business date and difference terms. |

### RWB-S2-E3001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06629 | RWB-P3-E2007-APP | GAP-2691 | 13 | Add the three treatment operations and their element names at the wave 2 contract freeze; add a state check constraint with APPROVED and BOOKED; booking_difference as jsonb keyed by term; unique key per treatment and business date. |

### RWB-PLT-E1042-CON; OTHER:DP-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06631 | RWB-P3-E2007-APP | GAP-0924 | 3 | Add a parameter row for the cached authorise decision lifetime, value agreed at the wave 2 design review; add a test that a cached decision is dropped on pack version change. |

### OTHER:Platform secret store (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06632 | RWB-P3-E2007-APP | GAP-2489 | 3 | Allocate the rwb-decision login with schema rwb_decision and record it in the platform secret store; story keeps the phrase until then. |

### OTHER:Parameter and reference-data registers; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06633 | RWB-P3-E2007-APP | GAP-2692 | 1 | Add booking.missing.grace_loads and the treatment-type and outcome list codes; record TreatmentBooked ownership against rwb-payment; record the stage outcome contract of the parent. Confirm the split when RWB-P2-E2007-CON is published. |

### OTHER:rwb-access API contract (yaml not located in the folder) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06637 | RWB-P3-E2009-APP | DOR-RWB-P3-E2009-APP-8 | 12 | Publish POST /api/recovery/access/v1/authorise (P1). HTTP error message IDs and Kafka payload alignment stay Not specified in the source documents. |

### OTHER:Functional Specification Document P9 (FSD P9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06638 | RWB-P3-E2009-APP | GAP-1646 | 4 | Read every Power BI and data lake destination of A2.1, A2.3, A2.4, A2.5, A2.7 and A2.8, and the INT-19 lake tests, as the rwb-reporting read model on the gateway-bff route, and every lake delivery as a file delivered by rwb-integration. |

### OTHER:FSD P3 v4 A2.18 (queue-measure story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06639 | RWB-P3-E2009-APP | DOR-RWB-P3-E2009-APP-4 | 8 | Carry AC-ALT-P3-018-02 and its test case for BR8 in the queue-measure story. |

### OTHER:RWB-E6-037 and FSD P9 A2.6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06640 | RWB-P3-E2009-APP | GAP-2579 |  | Confirm the benefit-model measure set and its holder, the monthly business day and cut-off, the measure_snapshot month key, the benefit-view screen and the requirement ID; values Not specified in the source documents (GAP-2579). |

### OTHER:Recovery Workbench data model v3 (Facts sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06641 | RWB-P3-E2009-APP | GAP-0251 |  | Make the star schema the rwb_reporting read model fed from service topics; serve GET /dashboards/{id} and GET /reports/{id} behind gateway-bff; remove the data lake and Power BI feed. |

### OTHER:Recovery Workbench data model v3 (Dimensions and Facts sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06643 | RWB-P3-E2009-APP | GAP-0257 |  | Key owner and team by ID from events and resolve display names from P3 queue_member and assignment behind the rwb-access masking policy; no personal data on an event. |

### OTHER:FSD P9 AC-P9-001-01; OTHER:AC-P9-003-01; OTHER:AC-P9-008-01; OTHER:AC-ALT-P9-003-01 and AC-ALT-P9-003-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06644 | RWB-P3-E2009-APP | GAP-1649 |  | Publish the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED and the two agent measures; carry the count as an open question. |

### OTHER:Wave 1 contract for GET /reports/measures (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06645 | RWB-P3-E2009-APP | GAP-2570 |  | Declare the measures read shape for the harness and catalog consumer; keep the dashboard and SCR-37 in RWB-P9-E2009-APP; leave reporting client connection as a PRD-step open decision. |

### OTHER:Service contracts of rwb-case, rwb-agent, rwb-source-data and rwb-reporting (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06646 | RWB-P3-E2009-APP | GAP-2576 |  | Declare the three consumed operations and two owner-queue activities on per-service bases with one hop and 2 s timeout; replay day events into a run-scoped read model; hand the published extract to rwb-integration as INT-19 replacement; take agent rates from EV-28 and RWB-P10-E1063-CON; keep the three parent tables as RWB-P9-E1013-CON fixes them. |

### OTHER:rwb-reporting steering dashboard contract (v1 contract publication) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06647 | RWB-P3-E2009-APP | GAP-2577 | find it | Publish v1 contract: baselineValue delta, fixed dimension, three declarations, two activity contracts, eight subscriptions, JOB-15 registration, message map, fakes; placeholders with one review row; gate on contract tests and schema lint. |

### OTHER:Platform edge story (gateway-bff composite route) and wave 2 entry check record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06648 | RWB-P3-E2009-APP | GAP-0391 | find it | Integration lead and platform edge story agree composite route path and merge order, harness repo and SIT env, seeded measure day, evidence format and retention, pass/fail gate at wave 2 entry check. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06649 | RWB-P3-E2009-APP | GAP-0731 | find it | Agree case-fact read schema, cut-off rule and fact transport with the rwb-reporting owner; record the case-fact event projection in the case CON story and the catalogue. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06650 | RWB-P3-E2009-APP | GAP-1563 | 11 | Name the P3 duty (exception visibility on the case) in the P3 PRD and the P8 duty (matching rule) in the P8 PRD. |

### OTHER:rwb-reporting deployment chart and runbook (deployment slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06651 | RWB-P3-E2009-APP | GAP-2578 | find it | Ship one chart with api and worker, migration, Schedule, eight consumer groups, six alerts with runbook links, four series, flag, backfill and rollback; values from environment; allocate run message ID. |

### OTHER:Recovery Workbench fact model v3 (Facts sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06656 | RWB-P3-E2009-APP | GAP-0253 | find it | Facts F6, F10, F12, F13: replace nightly Workbench load with event-fed projections; 01:30 publish (JOB-15), rerun any business date, hold when count does not reconcile. |

### OTHER:Recovery Workbench fact model v3 (Read model sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06657 | RWB-P3-E2009-APP | GAP-0256 | find it | Each Read model row carries inbox dedupe, business-date order, reopen-until-frozen rule and rebuild from retained topic history. |

### RWB-S8-E2009-APP; RWB-P9-E2009-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06659 | RWB-P3-E2009-APP | GAP-3090 | find it | Publish schedule id, calendar, catch-up policy, rerun input, two Measure fields, dimension format, alert channel and two recipients. |

### RWB-P2-E2033-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06669 | RWB-P3-E2011-APP | GAP-2224 | find it | State SCR-02 reads rwb-integration; fix row and envelope names in contract v1; set page bounds and export limit as parameter rows; keep ageDays and add ageInStateDays; drop duplicate timer index; name login and flag owner. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06676 | RWB-P3-E2011-CON | DOR-RWB-P3-E2011-CON-8 | 12.2 | Publish the authorise operation (CG-ALL-4103) and make status, routeCode and stageCode LOV data (CG-ALL-4104 to CG-ALL-4106). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06679 | RWB-P3-E2011-CON | GAP-3101 | find it | Declare GET /api/recovery/deviation/v1/deviation-flags on rwb-deviation as a read with a gap; add it to the RWB-P2-E2033-CON consumed set at its next revision. |

### OTHER:rwb-access, rwb-deviation and rwb-decision API yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; RWB-P3-E1021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06690 | RWB-P3-E2012-APP | DOR-RWB-P3-E2012-APP-8 | 4 | Publish the four named paths, add Idempotency-Key to POST /cases/{caseId}/transfer, and make transferReasonCode read as LOV-TRANSFER-REASON data. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06692 | RWB-P3-E2012-APP | DOR-RWB-P3-E2012-APP-12 | 16 | Add TC-E2-012-15 to Test Cases v8. Align RTM v7 test lists with story section 18. Story adds TC-E2-012-16 (contract) and TC-E2-012-17 (boundary, ASM-3438). |

### RWB-P7-E2027-APP; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06694 | RWB-P3-E2012-APP | GAP-2502 | 8, 12.7 | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 in place of rwb.decision-record.DecisionRecorded.v1, or filter the other form. |

### OTHER:rwb-case deployment values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06700 | RWB-P3-E2012-APP | GAP-0713 | 13 | Record the confirmed start-to-close and schedule-to-close values of EvaluateRules and RecordAndApply and the five alert thresholds, confirmed by the service owner, not defaults. |

### OTHER:rwb-access, rwb-deviation, rwb-decision API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06708 | RWB-P3-E2012-CON | DOR-RWB-P3-E2012-CON-8 | 12.1 | Publish POST /api/recovery/access/v1/authorise; GET /api/recovery/deviation/v1/cases/{caseId}/deviations; GET /api/recovery/decision/v1/rule-models/{packageCode}/{version}; GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=; and the 3 further paths in the detcheck. |

### OTHER:P7 decision-log read contract (TSD P7 v2 T3.1 and FSD P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06713 | RWB-P3-E2012-CON | GAP-2500 | find it | Add DecisionLogPage and DecisionLogEntry element shape, MSG-P7-009 text as R9 placeholder, and the DP-02 login phrase; this story now reads the decision code from LOV-DECISION. |

### OTHER:CON stories of the owning services (rwb-decision, rwb-access, rwb-source-data, reference data owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06717 | RWB-P3-E2012-CON | GAP-3092 | 12 | Publish operation names, paths and schemas for the LOV-TRANSFER-REASON read, the rwb-decision package read, the rwb-access authorise call and the rwb-source-data case-facts read. |

### OTHER:rwb-access, rwb-deviation, rwb-decision API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06727 | RWB-P3-E2012-OPS | DOR-RWB-P3-E2012-OPS-8 | 12 | Publish POST /api/recovery/access/v1/authorise, GET /api/recovery/deviation/v1/cases/{caseId}/deviations and GET /api/recovery/decision/v1/rule-models/{packageCode}/{version}; align event type rwb.decision-record.DecisionRecorded.v1 with Kafka Catalog v1 name, plus the two other detcheck items. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06729 | RWB-P3-E2012-OPS | GAP-0396 | find it | GAP-0396: record the agreement at the wave 2 entry check (integration lead with the platform edge story) of the gateway-bff composite transfer route path and merge order, the harness repository and SIT environment, the seeded test data, the per-run evidence format and retention, and the pass/fail gate. Not specified in the source documents (GAP-0396). |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:data steward) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06736 | RWB-P3-E2012-OPS | GAP-0712 | find it | Name the data steward as the role that may add or retire a transfer reason code; a change is a dated reference load approved by a second person. |

### OTHER:rwb-case values files (environment values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06737 | RWB-P3-E2012-OPS | GAP-0713 | find it | Record confirmed start-to-close and schedule-to-close values for EvaluateRules and RecordAndApply, and the five alert thresholds, before UAT. |

### OTHER:CON stories of owning services (rwb-decision, rwb-access, rwb-source-data; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06738 | RWB-P3-E2012-OPS | GAP-3092 | find it | Publish operation names, paths and schemas for the reference-data read, the rwb-decision package read, the rwb-access authorise call and the rwb-source-data case-facts read. |

### RWB-P7-E2013-CON; OTHER:FSD P7 A2.15 and A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06755 | RWB-P3-E2013-APP | GAP-1623 | find it | Record in the rwb-case contract that P3 moves the case to Waiting approval and raises the approval task on ApprovalRequested; align FSD A2.15 and A2.16 to that choice. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P4-E1038-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06757 | RWB-P3-E2013-APP | GAP-0842 | find it | Serve the DoA lookup once from rwb-access on the ownership map path; RWB-P4-AD016-APP owns the answer; the routing story consumes it with no second copy of the path. |

### RWB-P4-E1037-CON; RWB-P7-E2013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06758 | RWB-P3-E2013-APP | GAP-1251 | find it | Keep the DoA table in rwb-access; state the level lookup as a read with a 2 s budget; approval stores delegation_limit_id, approval_level and limit_version only, with no join or foreign key. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06759 | RWB-P3-E2013-APP | GAP-1252 | find it | Add GET /api/recovery/access/v1/doa-limits with P4 as owner to the API catalogue and to the operation list of RWB-P4-E1037-CON, with query and answer fields. |

### RWB-P4-E1037-CON; RWB-P7-E2013-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06760 | RWB-P3-E2013-APP | GAP-1256 | find it | Fix one rule: a local read-through cache of the delegation version, warmed at start before readiness, refreshed on DoaLimitChanged, with an alert when the cached version is older than the version in force. |

### OTHER:Harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06761 | RWB-P3-E2013-APP | GAP-0397 | find it | Hold the composite route, merge order, harness environment, seeding, evidence format, retention and pass/fail gate as data in the harness pack, not in the story. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06763 | RWB-P3-E2013-APP | GAP-0929 | find it | Freeze the DoA request and response field set at contract review, with the five outcome values and requiredLevel on a refused authority decision. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-decision AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06765 | RWB-P3-E2013-APP | GAP-1221 | find it | Add rwb-comms as consumer of rwb.decision.ApprovalRequested.v1 carrying the raised escalation level and new due time; no ApprovalEscalated event; TimerBreached stays a legacy reference. |

### OTHER:TSD P6 v2 T3.1 (notice table and message request) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06766 | RWB-P3-E2013-APP | GAP-1222 | find it | Add approval reference, escalation level, recipient role, recipient user reference and send time to the notice record, matching section 12.1 of RWB-P3-E2013-APP. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06768 | RWB-P3-E2013-APP | GAP-1257 | find it | Either add ApprovalDecided to the event catalogue with a number and consumers, or delete it from slide 14 and use DecisionRecorded as the outcome event. |

### RWB-P7-E2013-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06769 | RWB-P3-E2013-APP | GAP-0732 | find it | Fix case-side defaults: approval event fields consumed, task fields written (approval and preparer references), escalation representation, status mapping, composite route fields, rwb-case login name. |

### OTHER:Technical Specification P7 v2 (TSD P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06771 | RWB-P3-E2013-APP | GAP-1263 | 15 | In next version, map REQ-APD-002 and REQ-APD-006 to FEAT-APD-01 with RWB-E2-013 (routing) and keep FEAT-APD-08 with RWB-E2-014 (screen). |

### OTHER:Edge and gateway design (gateway-bff composition, platform edge owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06772 | RWB-P3-E2013-APP | GAP-1621 | 15 | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from rwb-case operations and record the four screen contracts there. |

### OTHER:TSD P7 next version; OTHER:P7 stories; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06773 | RWB-P3-E2013-APP | GAP-1254 |  | Mark INT-19, INT-20, lake partition, manifest and watermark retired; rwb-reporting builds read model from rwb.decision-record.v1; keep EV-08 unchanged. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20824 | RWB-P3-E2009-APP | R-16120 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09171', 'R-16120', 'R-22565'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0251 | The nine fact tables are defined in a data lake; the target has no data lake | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0253 | The refresh wording has no schedule in the target | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0255 | The read-model control tables and the queue measures are absent | Data architecture team | Resolved (directive) |
| GAP-0256 | No late-arrival, freeze or replay rule on any fact table | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0257 | dim_org holds an owner while events carry no personal data | Data steward | Resolved (directive) |
| GAP-0258 | The LDM and the FSD still publish to Power BI, which is removed | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0391 | Gateway-bff composite steering route, harness environment, measure-day seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0395 | Booking confirmation integration harness: composite booking and treatment route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0396 | Gateway-bff composite transfer route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0397 | Approval-routing harness environment, composite queue route and evidence format are not specified | Integration lead | Resolved (directive) |
| GAP-0594 | The shapes and property names of the two booking-fact reads are in no source document | Tech lead | Resolved (directive) |
| GAP-0595 | The case's account set and its product group have no P1 read in the target | Solution architect | Resolved (directive) |
| GAP-0596 | How the read answers the three Section B columns, and which flag holds it back, is stated nowhere | Data architect | Resolved (directive) |
| GAP-0597 | The batch-status answer has two values in the legacy interface and nine fields in the view, and no source fixes which of them it returns | Tech lead | Resolved (directive) |
| GAP-0598 | No source says where the account read ends and the built match facts begin | Solution architect | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0658 | rwb-integration booking confirmation (contract slice): the JOB-08 ownership and consumer lists, the ACE read boundary, the rerun placement and the twelve consumed shapes are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0659 | rwb-integration booking confirmation (deployment slice): the login and secret reference, the JOB-08 ownership, the alert thresholds, the runbook ownership and the backfill limit are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner; business on-call owner for the package alerts | Resolved (directive) |
| GAP-0708 | The queue summary fields, their types, and whether the summary is read live or from the queue_measure snapshot | Solution architect | Resolved (directive) |
| GAP-0709 | The freshness answer, the X-Data-As-Of header and the value of the product placeholder in the stale banner | Solution architect | Resolved (directive) |
| GAP-0710 | The partial-success shape of a selection and its summary message are not typed | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0711 | The at-cap and legal-hold pre-check answers have no typed shape | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0712 | Who may add or retire a transfer reason code is not specified | Centre of excellence; data steward | Resolved (directive) |
| GAP-0713 | The activity timeouts and the alert thresholds of the manual move are not specified | DevOps lead; service owner of rwb-case | Resolved (directive) |
| GAP-0730 | rwb-case booking confirmation: login, composite route, treatment booking fields, match-result shape and route-rule evaluator owner are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0731 | Case-fact read shape, cut-off rule and the reporting hand-off are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
| GAP-0922 | rwb-access booking confirmation: the authorise request and answer shapes, the contract entry of the authorise path and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0923 | rwb-access booking confirmation: the TSD RBAC matrix has no Case record column, so the CASE_RECORD R and U letters the booking tasks need are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0924 | rwb-access booking confirmation: the lifetime of a cached authorise decision is not specified | Solution architect | Resolved (directive) |
| GAP-0928 | GET /doa-limits is named in Architecture v5 and API v3 but absent from API Specification v4 | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0929 | The DoA lookup and authority-decision request and response shape is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0930 | The scope of the rwb-decision service identity inside rwb-access is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1220 | The template code, channel, notice kind, state vocabulary, retry limit, template owner and MSG-GEN-006 text of the escalation notice are not specified in any source | Solution architect | Resolved (directive) |
| GAP-1221 | The event catalogue lists gateway-bff as the only consumer of ApprovalRequested and carries no ApprovalEscalated event, yet this story also consumes the event for the escalation notice | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1222 | No source names the notice and message operations or the notice fields that carry an approval reference, an escalation level, a recipient and a sent time | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1251 | The delegation of authority table is P4 rwb-access's while the routing rules and the approval resource are P7 rwb-decision | Solution architect | Resolved (directive) |
| GAP-1252 | The delegation limits operation has no row in the Ownership Map API catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1254 | The data lake copy of the decision record is removed under DP-17 while the legacy log path streams to it | Solution architect | Resolved (directive) |
| GAP-1255 | The request and answer field lists of the five approval operations and the case-status operation are not enumerated in any source | Tech lead of rwb-decision with the Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1256 | The delegation snapshot and its cache refresh have no named operation, store or interval | Solution architect | Resolved (directive) |
| GAP-1257 | ApprovalDecided is named on the service contract slide but has no event catalogue row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1263 | REQ-APD-002 and REQ-APD-006 are mapped to two different features and stories | Business analyst | Resolved (directive) |
| GAP-1563 | The BRD assigns payment matching to rwb-case while Architecture v5 gives it to rwb-payment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1621 | Four screens are attributed to P7 while the edge ruling composes every screen in gateway-bff | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1646 | The data lake and the Power BI connection are removed but the whole reporting FSD is built on them | Solution architect | Resolved (directive) |
| GAP-1649 | The measure set is six definitions in one acceptance criterion and seven measures in another | Tribe lead with the Reporting and BI analyst | Resolved (directive) |
| GAP-1658 | SCR-37 has no owner and no serving path | Solution architect | Resolved (directive) |
| GAP-1662 | RWB-E2-009 promises a Power BI data set, which ADR-018 removes | Solution architect | Resolved (directive) |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-2224 | The case list is served twice in the target, and the row names, the bounds, the login and the flag mechanism of the owner's list have no source | Solution architect | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2485 | The booking-confirmation decision is placed in rwb-decision while DP-04 and the registry story keep the evaluation in the owning service and state that rwb-decision never evaluates | Solution architect, with the decision service owner | Resolved (directive) |
| GAP-2486 | The operation set, paths and payloads of the batch, account, treatment, task, parameter and list contracts, the decision code, the record's snapshot and actions shape and several read and message details are in no source | Solution architect, with the owners of rwb-integration, rwb-treatment and rwb-case | Resolved (directive) |
| GAP-2487 | No source names the event that carries a booking decision out of rwb-decision, because the legacy TreatmentBooked is rwb-payment's and is raised after the treatment is booked | Solution architect, with the event platform owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2489 | The name of the rwb-decision database login is in no source | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2490 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its eleven legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2491 | The timezone, overlap, retry and fallback of the JOB-08 run and the behaviour of the legacy feature flag when off are in no source | Solution architect, with the workflow platform owner | Resolved (directive) |
| GAP-2492 | The legacy run writes the REC-03 result to reconciliation_result, and no table or owner of that name exists in the target and no source assigns the break list | Solution architect, with the reporting owner | Resolved (directive) |
| GAP-2500 | Transfer decision record and ledger read: the decision code, the MSG-P7-009 text, the answer element, the no-version answer and the DP-02 login name are not specified | P7 business analyst and solution architect, with the API specification owner | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2502 | Decision-record event naming and the boundary with RWB-P7-E1008-APP and RWB-P7-E2027-APP | P7 solution architect, with the event platform owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2570 | RWB-E1-013: the Power BI refresh that AC3 asserts has no mechanism once the data lake is removed, and the measures read is assigned to Epic 2 by the legacy story | Solution architect | Resolved (directive) |
| GAP-2576 | rwb-reporting steering dashboard (application slice): the consumed operation names, the workflow and activity names, the read-model design, the INT-19 replacement and the agent fact source are fixed by no single source | Solution architect, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the reporting service | Resolved (directive) |
| GAP-2577 | rwb-reporting steering dashboard (contract slice): the element names of the consumed declarations, the event envelope naming, the Measure delta, the schema increments and the file shape of the extract are fixed by no single source | Contract owner of rwb-reporting, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the event platform | Resolved (directive) |
| GAP-2578 | rwb-reporting steering dashboard (deployment slice): the login and secret reference, the replica and threshold values, the consumer offset and retention policy, the catch-up window, the backfill limit and the message ID of the run alert are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2579 | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2692 | The rwb-treatment share of the key is stated by no S2 source, the P2 contract shapes it follows are unpublished, and the trigger, the task-raising and the event ownership are split across stories | Solution architect with the rwb-integration, rwb-treatment and rwb-case tech leads and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-3101 | rwb-deviation case and queue list slice: no read in the Ownership Map, no seam with the composed page, no path, field names or page bound, the flag derived twice and the pause projection without the rule package | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3232 | The story catalog carries 2,534 dependency rows while the story files carry 2,609 for the same 1,034 stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E2009-APP | skipped AC ID | 101 | missing: AC1, AC3, AC5, AC6, AC7, AC9, AC13 |
| RWB-P3-E2012-CON | new AC without TC row | 437 | AC13 is new and no section 16 row covers it |
