# RWB-SVC-P2 rwb-integration (Integration) - review pack, part 4 of 4 (RWB-P2-E2035-APP to RWB-P2-E4046-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 94 |
| Cross-document (pending in another document) | 161 |
| Not applied (value not in the sources) | 10 |
| Open business decisions | 12 |
| Register gaps linked | 39 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P2-E2035-APP | 16 | 40 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2035 APP Next action on the case v2.md |
| RWB-P2-E2035-CON | 12 | 31 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2035 CON Next action on the case - contract v2.md |
| RWB-P2-E2035-OPS | 9 | 30 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2035 OPS Next action on the case - deployment v2.md |
| RWB-P2-E2036-APP | 24 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2036 APP Queue write interface for models and agents v2.md |
| RWB-P2-E2036-CON | 11 | 18 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2036 CON Queue write interface for models and agents - contract v2.md |
| RWB-P2-E4046-APP | 22 | 25 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E4046 APP Post a settlement booking to ALS v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P2-E2035-APP | R-10139 | CG-ALL-3274 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-P2-E2036-APP | R-10152 | CG-ALL-3306 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E4046-APP | R-10170 | CG-ALL-3339 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28853 | GAP-1560 | Register gap | AI product owner | The queue write interface for models and agents has no approved consumer and no flag removal date | Name the first approved consumer and the flag removal date before the wave 2 release. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-P2-E2035-APP | R-33400 | ASM-ALL-3274 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P2-E2035-APP | R-04869 | DOR-RWB-P2-E2035-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed EP02 epic design record in numbered folders (grep 'epic design'). Only process rules found: DoR v3 item 14, governance v3, DT05. Needs the sign-off record. |
| RWB-P2-E2035-CON | R-22701 | GAP-0418 | 9 | Gateway-bff composite next-action route, harness environment, seeding, evidence format and gate not specified | Section 9 text is not in this chunk, so no exact anchor exists. Values are not in the sources (grepped the project; only _work/msr output mentions them). Needs the wave 2 entry check record from QA. |
| RWB-P2-E2035-OPS | R-04879 | DOR-RWB-P2-E2035-OPS-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources (prior search of numbered folders and 04 User stories found none). Sign-off cannot be stated without inventing it. No edit. |
| RWB-P2-E2035-OPS | R-04880 | DOR-RWB-P2-E2035-OPS-16 Size: Fail | Header | Definition of Ready item 16 Size: Fail | The Size row names no size; the squad sizes the story at refinement, so the item stays open. |
| RWB-P2-E2035-OPS | R-22702 | GAP-0734 | 4, 7 | The next-action slice leaves the legacy AC allocation, the daily check Schedule, the DL22 durations and the role-class field unspecified | Only the note that legacy criteria are proved by RWB-ITG-E2035-ITG was added. A daily DailyCaseRun step conflicts with the 5-minute Schedule in BR3, 12.6 and §11; needs a ruling. |
| RWB-P2-E2036-APP | R-04885 | DOR-RWB-P2-E2036-APP-14 | n/a | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or .md exports under _work/msr/directive/mp/out. The sign-off cannot be invented. |
| RWB-P2-E2036-APP | R-04888 | DOR-RWB-P2-E2036-APP-22 | n/a | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in the story, the CON story or 05 Technical architecture .md files. Cannot be invented. |
| RWB-P2-E2036-CON | R-04892 | DOR-RWB-P2-E2036-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source docs (story key searched). A sign-off cannot be invented; needs the epic design record. Story DoR text not in this chunk. |
| RWB-P2-E2036-CON | R-04893 | DOR-RWB-P2-E2036-CON-16 | 14 | Definition of Ready item 16 Size: Fail | Directive says squad sizes at refinement, so story can say so, but DoR table text (section 14) was not in this chunk to anchor the edit. No size value exists to enter. |
| RWB-P2-E4046-APP | R-04901 | DOR-RWB-P2-E4046-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version for this story found in folders 0*. Value not in sources; no edit made. Needs a version from the owning team. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (20)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05034 | RWB-P2-E2035-APP | CG-ALL-3261 | 12.5 | Add a Workflows row for NextActionCheckWorkflow, task queue rwb-integration, with the input and output of story section 12.5. |
| CDC-05039 | RWB-P2-E2035-APP | CG-ALL-3262 | 12.5 | Add activity findCasesWithoutNextAction to the Activities sheet, or use a catalogued activity. |
| CDC-05040 | RWB-P2-E2035-APP | CG-ALL-3263 | 12.5 | Add activity resolveNextAction to the Activities sheet, or use a catalogued activity. |
| CDC-05041 | RWB-P2-E2035-APP | CG-ALL-3264 | 12.5 | Add activity fillNextAction to the Activities sheet, or use a catalogued activity. |
| CDC-05050 | RWB-P2-E2035-APP | GAP-3177 | 7 | Register the five-minute next-action Schedule and delete TimerDue (EV-18) from the Epic 2 contract tables. |
| CDC-05069 | RWB-P2-E2035-CON | CG-ALL-3279 | 12.5 | Add a Workflows row for NextActionCheckWorkflow with task queue rwb-integration and the input and output in section 12.5. |
| CDC-05073 | RWB-P2-E2035-CON | CG-ALL-3280 | 12.5 | Add an Activities row for findCasesWithoutNextAction with task queue rwb-integration and the input and output in section 12.5. |
| CDC-05074 | RWB-P2-E2035-CON | CG-ALL-3281 | 12.5 | Add an Activities row for resolveNextAction on task queue rwb-integration, or the story names a catalogued activity |
| CDC-05075 | RWB-P2-E2035-CON | CG-ALL-3282 | 12.5 | Add an Activities row for fillNextAction on task queue rwb-integration, or the story names a catalogued activity |
| CDC-05079 | RWB-P2-E2035-CON | GAP-3177 | 7 | Register the five-minute next-action Schedule; delete EV-18 from the Epic 2 contract tables. |
| CDC-05097 | RWB-P2-E2035-OPS | CG-ALL-3289 | 12.5 | Add a Workflows row for NextActionCheckWorkflow, or the owning team names the catalogued workflow to use in 12.5. |
| CDC-05101 | RWB-P2-E2035-OPS | DOR-RWB-P2-E2035-OPS-8 | find it | Add Workflows and Activities rows for NextActionCheckWorkflow, findCasesWithoutNextAction, resolveNextAction and fillNextAction, or name catalogued equivalents. |
| CDC-05103 | RWB-P2-E2035-OPS | CG-ALL-3290 | 12.5 | Add an Activities row for findCasesWithoutNextAction, or name a catalogued activity to use in 12.5. |
| CDC-05104 | RWB-P2-E2035-OPS | CG-ALL-3291 | 12.5 | Add an Activities row for resolveNextAction, or name a catalogued activity to use in 12.5. |
| CDC-05105 | RWB-P2-E2035-OPS | CG-ALL-3292 | 12.5 | Add activity fillNextAction to the Activities sheet with task queue rwb-integration, or name a catalogued activity in §12.5. |
| CDC-05109 | RWB-P2-E2035-OPS | GAP-3177 | find it | Register Schedule next-action-check every 5 minutes for rwb-integration; delete TimerDue (EV-18) from the Epic 2 contract tables. |
| CDC-05169 | RWB-P2-E4046-APP | CG-ALL-3328 | 12.5 | Add a row for activity deliverFile(manifest) with task queue rwb-integration. |
| CDC-05170 | RWB-P2-E4046-APP | CG-ALL-3329 | 12.5 | Add a row for activity buildOutboundFile with task queue rwb-integration. |
| CDC-05171 | RWB-P2-E4046-APP | CG-ALL-3330 | 12.5 | Add a row for activity storeOutboundFile with task queue rwb-integration. |
| CDC-05172 | RWB-P2-E4046-APP | CG-ALL-3331 | 12.5 | Add a row for activity sendFileOverMft with task queue rwb-integration. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05026 | RWB-P2-E2035-APP | CG-ALL-3253 | 12.1 | Publish POST /api/recovery/integration/v1/next-actions:resolve through the owner's CON story RWB-P2-E2035-CON. |
| CDC-05027 | RWB-P2-E2035-APP | CG-ALL-3254 | 12.1 | Publish GET /api/recovery/integration/v1/cases/{caseId}/next-action through the owner's CON story RWB-P2-E2035-CON. |
| CDC-05028 | RWB-P2-E2035-APP | CG-ALL-3255 | 12.1 | Publish POST /api/recovery/integration/v1/cases/{caseId}/next-action through the owner's CON story RWB-P2-E2035-CON. |
| CDC-05037 | RWB-P2-E2035-APP | DOR-RWB-P2-E2035-APP-8 | 8 | Publish the paths named by detcheck: POST /next-actions:resolve, GET and POST /cases/{caseId}/next-action, GET /api/recovery/decision/v1/rule-catalog/{ruleId} with packageVersion, plus 8 more. |
| CDC-05066 | RWB-P2-E2035-CON | CG-ALL-3276 | 12.1 | Add path POST /next-actions:resolve under base /api/recovery/integration/v1 with the shape, access, idempotency and errors in section 12.1. |
| CDC-05067 | RWB-P2-E2035-CON | CG-ALL-3277 | 12.1 | Add path GET /cases/{caseId}/next-action under base /api/recovery/integration/v1 with the shape, access and errors in section 12.1. |
| CDC-05068 | RWB-P2-E2035-CON | CG-ALL-3278 | 12.1 | Add path POST /cases/{caseId}/next-action under base /api/recovery/integration/v1 with the shape, access, idempotency and errors in section 12.1. |
| CDC-05127 | RWB-P2-E2036-APP | CG-ALL-3302 | 3, 12.1 | Placement path kept in short form; long /api/recovery/integration/v1 prefix removed. |
| CDC-05130 | RWB-P2-E2036-APP | DOR-RWB-P2-E2036-APP-23 | header | Add path POST /api/recovery/integration/v1/queues/{queueId}/placements to rwb-integration.yaml (spec version 5.0.0) so the story can cite a contract version. Grep for placement finds only rwb-case.yaml. |
| CDC-05144 | RWB-P2-E2036-CON | CG-ALL-3313 | 12.1 | Publish POST /api/recovery/integration/v1/queues/{queueId}/placements with its request and response shape. |

### RWB-P2-E2035-CON (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05035 | RWB-P2-E2035-APP | DOR-RWB-P2-E2035-APP-21 | header | Set build status of RWB-P2-E2035-CON to Done by publishing the contract. |
| CDC-05036 | RWB-P2-E2035-APP | DOR-RWB-P2-E2035-APP-22 | header | Publish a contract fake library version and record it as published. |
| CDC-05051 | RWB-P2-E2035-APP | GAP-0667 | 12 | Fix the three operation names, the next-action-check Schedule values, the five message texts and the consumed field names; the Ownership Map row and timer register are corrected by their owners. |
| CDC-05052 | RWB-P2-E2035-APP | GAP-0668 | 12 | Baseline the three operation names, the nine consumed shapes, the split note, the workflow and Schedule contract and the error mapping; confirm the five message texts with the contract owners. |
| CDC-05060 | RWB-P2-E2035-APP | GAP-2409 |  | Mark packageVersion as required on GET /api/recovery/decision/v1/rule-catalog/{ruleId} and keep the refusal with MSG-GEN-001 when it is absent. |
| CDC-05098 | RWB-P2-E2035-OPS | DOR-RWB-P2-E2035-OPS-21 Contract published: Fail | Header | The contract is Not started; publishing it belongs to the contract document. The story names the dependency only. |
| CDC-05099 | RWB-P2-E2035-OPS | DOR-RWB-P2-E2035-OPS-22 | find it | Publish a contract fake library version and record its version in the contract story. |
| CDC-05100 | RWB-P2-E2035-OPS | DOR-RWB-P2-E2035-OPS-23 Contract version fixed: Fail | Header | The numbered contract version is Not specified in the source documents; /v1 is only the path base. |
| CDC-05111 | RWB-P2-E2035-OPS | GAP-0668 | 12 | §12 records read path ownership. Operation names, consumed shapes and the remaining contract values are to be confirmed in the contract document and owners' review. |
| CDC-05121 | RWB-P2-E2035-OPS | GAP-2409 | find it | Mark packageVersion as required on GET /api/recovery/decision/v1/rule-catalog/{ruleId} and keep the MSG-GEN-001 refusal. |

### RWB-P4-E1037-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05057 | RWB-P2-E2035-APP | GAP-2322 | 12 | Add GET /api/recovery/access/v1/role-catalogue/{roleCode} with its answer schema and stub it in the contract fake; fix the authorise request and answer of a next-action read; add the unknown or inactive role code message. |
| CDC-05115 | RWB-P2-E2035-OPS | GAP-2322 | find it | Add GET /api/recovery/access/v1/role-catalogue/{roleCode} with its answer schema to the API spec and TSD P4 appendix T-A, stub it in the contract fake, fix the authorise request and answer of a next-action read, fix the rwb-access login in the platform DB story, and add the unknown or inactive role code message. |
| CDC-05135 | RWB-P2-E2036-APP | GAP-0957 | 12 | Name the authorise request elements (caller code, caller type, service identity, target queue, queue team code, case, product group, reason, model or agent version, field IDs) and the answer elements |
| CDC-05137 | RWB-P2-E2036-APP | GAP-0958 | 12 | Fix five reason codes with one status each: 403 for RIGHT_NOT_HELD, CALLER_KIND, SCOPE_NOT_ALL; 422 and 503 codes keep MSG-GEN-001, MSG-GEN-002, MSG-P7-003 |
| CDC-05138 | RWB-P2-E2036-APP | GAP-0959 | 4 | Non-human scope rule stated as ALL-only with SCOPE_NOT_ALL refusal. |
| CDC-05139 | RWB-P2-E2036-APP | GAP-0960 | 3 | Role-class rule for the service identity left Not specified; caller code kept as a label only. |
| CDC-05153 | RWB-P2-E2036-CON | GAP-0957 | 12.2 | Carry the placement-admission request and answer elements of POST /authorise as baseline names; keep caller type as a value of the approved callers list and add no caller-type list to rwb_access |
| CDC-05155 | RWB-P2-E2036-CON | GAP-0958 | 14 | Fix the five reason codes with one status each: 403 for RIGHT_NOT_HELD, CALLER_KIND and SCOPE_NOT_ALL, all with MSG-P4-002; name the other two codes |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05038 | RWB-P2-E2035-APP | CG-ALL-3252 | 12.7 | Record decision_record as the rwb_integration library table object in the owning document, or use a dictionary name. |
| CDC-05047 | RWB-P2-E2035-APP | DOR-RWB-P2-E2035-APP-7 | 11 | Add decision_record as an entity or field, or align its name per LDM v9 and Data Classification v5; legacy wording in section 7 criteria follows the same change. |
| CDC-05078 | RWB-P2-E2035-CON | DOR-RWB-P2-E2035-CON-7 | 11 | Add decision_record as a field or entity, or name the entity that holds the decision record |
| CDC-05132 | RWB-P2-E2036-APP | CG-ALL-3301 | find it | Add decision_record as the rwb_integration library table (owner PLT library) with its field names, or give the dictionary name for it. |
| CDC-05134 | RWB-P2-E2036-APP | DOR-RWB-P2-E2036-APP-7 | 11 | Register decision_record as a library table of rwb_integration with TSD P2 v3 T3.1 fields, or confirm it is outside scope; keep DF-DEC-001 to DF-DEC-018 |
| CDC-05146 | RWB-P2-E2036-CON | CG-ALL-3312 | 9 | Record decision_record as the PLT library table in rwb_integration, or use the dictionary name. |
| CDC-05151 | RWB-P2-E2036-CON | DOR-RWB-P2-E2036-CON-7 | 11, 12.7 | Register decision_record as an entity of the decision-record library, or confirm its table name |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05044 | RWB-P2-E2035-APP | CG-ALL-3267 | 16 | Add TC-E2-035-14 rows with Given, When and Then copied from AC14 and BR11. |
| CDC-05087 | RWB-P2-E2035-CON | CG-ALL-3284 | 16 | Add rows TC-P2-E2035-CON-01 to TC-P2-E2035-CON-06 with Given, When and Then copied from AC1 to AC6. |
| CDC-05107 | RWB-P2-E2035-OPS | DOR-RWB-P2-E2035-OPS-12 | 12, 12.7, 16, 18 | Register TC-P2-E2035-OPS-01 to -08 in Test Cases v8; align the RTM v7 test lists for §18 to the §16 cases. |
| CDC-05118 | RWB-P2-E2035-OPS | CG-ALL-3294 | 16 | Add rows for TC-P2-E2035-OPS-01 to TC-P2-E2035-OPS-06 with Given, When and Then copied from AC1 to AC6 of RWB-P2-E2035-OPS. |
| CDC-05158 | RWB-P2-E2036-CON | CG-ALL-3316 | 16 | The rows belong in the next Test Cases version; section 16 lists TC-P2-E2036-CON-01 to 06 and the newly added 07 to 10, all to be registered. |
| CDC-05176 | RWB-P2-E4046-APP | CG-ALL-3336 | 16 | Add rows TC-E4-046-01 to TC-E4-046-04 with Given, When and Then copied from the criteria they cover (AC1 to AC4, AC6, AC7 of this story) |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05059 | RWB-P2-E2035-APP | CG-ALL-3268 | 18 | Align the trace rows of REQ-WKM-012, REQ-WKM-013 and the other differing requirements with section 18 of RWB-P2-E2035-APP in the next RTM version. |
| CDC-05088 | RWB-P2-E2035-CON | CG-ALL-3285 | 18 | Align the test lists of the five differing requirements with §18 of RWB-P2-E2035-CON, using TC-P2-E2035-CON IDs, in the next RTM version. |
| CDC-05119 | RWB-P2-E2035-OPS | CG-ALL-3295 | 18 | Align the test lists for REQ-WKM-012, REQ-WKM-013 and REQ-WKM-016 with RWB-P2-E2035-OPS §18 (TC-P2-E2035-OPS-01 to -06). |
| CDC-05142 | RWB-P2-E2036-APP | CG-ALL-3305 | 18 | Align the test case lists of REQ-CWC-017, REQ-CWC-018 and REQ-CWC-019 with RWB-P2-E2036-APP section 18 in the next RTM version. |
| CDC-05159 | RWB-P2-E2036-CON | CG-ALL-3317 | 18 | Align the RTM test lists for the five requirements with the section 18 test case IDs. |
| CDC-05183 | RWB-P2-E4046-APP | CG-ALL-3338 | 18 | In the next RTM version, align the test lists of the three differing requirements (REQ-DRI-006, REQ-DRI-007 and the third) with section 18 of RWB-P2-E4046-APP. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05042 | RWB-P2-E2035-APP | CG-ALL-3265 | 14 | Business analyst adds a new message ID for No RESTRUCTURE version is in force; the story then cites that ID instead of MSG-P3-027. |
| CDC-05043 | RWB-P2-E2035-APP | CG-ALL-3266 | 4, 14 | Business analyst adds a new message ID for the story's use of the R-UNI-33 text; the story then cites that ID in sections 4 and 14. |
| CDC-05048 | RWB-P2-E2035-APP | DOR-RWB-P2-E2035-APP-9 | 14 | Align MSG-P3-027 text with standard v4 and resolve the MSG-GEN-006 meaning per CG-ALL-3266. |
| CDC-05133 | RWB-P2-E2036-APP | CG-ALL-3304 | 4, 14 | Section 14 MSG-P4-001 row changed to the standard meaning under R-15733. |
| CDC-05147 | RWB-P2-E2036-CON | CG-ALL-3315 | 14 | Add a new message ID for 'No valid session or workload token'; the story then cites it. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05062 | RWB-P2-E2035-APP | GAP-2407 | 8 | Publish LOV-DECISION in the reference-data load with the state-change codes marked; the filter reads the mark. |
| CDC-05086 | RWB-P2-E2035-CON | GAP-2323 | find it | Add CUSTOMER_PARTY as a fourth value in the load that carries the roles; confirm with the role catalogue owner before the wave 2 policy pack goes in force. |
| CDC-05093 | RWB-P2-E2035-CON | GAP-2407 | find it | Publish LOV-DECISION in the reference-data load with state-change codes marked; the latestStateChange filter reads the mark. |
| CDC-05117 | RWB-P2-E2035-OPS | GAP-2323 | find it | Add CUSTOMER_PARTY as a fourth LOV-ROLE-CLASS value in the load that carries the roles, and confirm it with the role catalogue owner before the wave 2 policy pack is in force. |
| CDC-05123 | RWB-P2-E2035-OPS | GAP-2407 | find it | Add LOV-DECISION to T3.2 and publish it in the reference-data load with state-change codes marked; until then the read takes the newest entry with a rule ID and rule version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05030 | RWB-P2-E2035-APP | CG-ALL-3257 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/role-classes/{roleCode} through the rwb-case provider's CON story. |
| CDC-05031 | RWB-P2-E2035-APP | CG-ALL-3258 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/service-levels/{toState} through the rwb-case provider's CON story. |
| CDC-05032 | RWB-P2-E2035-APP | CG-ALL-3259 | 12.2 | Publish GET /api/recovery/case/v1/parameters/rwb.calendar.bank-holidays through the rwb-case provider's CON story. |
| CDC-05162 | RWB-P2-E4046-APP | CG-ALL-3323 | 12.2 | Publish POST /api/recovery/case/v1/cases/{caseId}/actions through the rwb-case CON story, or consume a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05033 | RWB-P2-E2035-APP | CG-ALL-3260 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider's CON story. |
| CDC-05128 | RWB-P2-E2036-APP | CG-ALL-3303 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider contract RWB-P4-E1037-CON. |
| CDC-05145 | RWB-P2-E2036-CON | CG-ALL-3314 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story, or consume a published operation. |
| CDC-05163 | RWB-P2-E4046-APP | CG-ALL-3324 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access CON story, or consume a published operation. |

### RWB-P7-E2042-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05054 | RWB-P2-E2035-APP | GAP-2406 | 7 | Set the valid-from date of RES-2026.12 to 2026-12-01, the date the ITG harness and RWB-P3-E2035-APP use, so the legacy criteria of this story hold. |
| CDC-05082 | RWB-P2-E2035-CON | GAP-2406 | 7 | Set the valid-from date of RES-2026.12 in section 3 to 2026-12-01, matching the ITG harness and RWB-P3-E2035-APP. |
| CDC-05112 | RWB-P2-E2035-OPS | GAP-2406 | find it | Section 3: set the valid-from date of RES-2026.12 to 2026-12-01, the date the ITG harness and RWB-P3-E2035-APP already use, instead of 2026-12-15. |

### OTHER:RWB-PLT-DB (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05064 | RWB-P2-E2035-APP | GAP-2411 |  | Fix the per-service login name for rwb-integration in RWB-PLT-DB and the secret store, keeping migration and application roles apart. |
| CDC-05095 | RWB-P2-E2035-CON | GAP-2411 | find it | Name the per-service login of rwb-decision, keep the migration role and application role apart, and register the secret in the secret store. |
| CDC-05125 | RWB-P2-E2035-OPS | GAP-2411 | find it | Fix the rwb-decision database login name in RWB-PLT-DB and the secret store, with migration and application roles kept apart; login name Not specified in the source documents (GAP-2411). |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05072 | RWB-P2-E2035-CON | CG-ALL-3275 | 9 | Record decision_record as the PLT library table created in rwb_integration (DP-03), as the owning document object. |
| CDC-05108 | RWB-P2-E2035-OPS | DOR-RWB-P2-E2035-OPS-7 | 11 | Register decision_record as an entity or field in LDM v9 and Data Classification v5, or rename it in §12.7. |
| CDC-05185 | RWB-P2-E4046-APP | GAP-2551 | find it | Record that the booking item is outbound_item in rwb_integration and rwb_payment holds no booking row; keep the item reference on TreatmentBooked as the booking reference the case records. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05077 | RWB-P2-E2035-CON | DOR-RWB-P2-E2035-CON-12 | 12.7, 16, 18 | Register TC-P2-E2035-CON-01 to 06 in Test Cases v8 and align the section 18 test lists with RTM v7 |
| CDC-05150 | RWB-P2-E2036-CON | DOR-RWB-P2-E2036-CON-12 | 12.7, 16, 18 | Register TC-P2-E2036-CON-01 to -10 in Test Cases v8 and align the section 18 test lists with RTM v7 |
| CDC-05164 | RWB-P2-E4046-APP | DOR-RWB-P2-E4046-APP-12 | 16 | Add this story's section 16 test cases TC-E4-046-01 to TC-E4-046-10 to Test Cases, and align the RTM test lists with story section 18. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05156 | RWB-P2-E2036-CON | GAP-3102 | 14 | Publish the deviation hold element (case ref, deviation ref, code, open count, handler, return point, contact-stop flag, rule version) and declare the rwb-case event-driven set and clear of recovery_case.deviation_open. |
| CDC-05167 | RWB-P2-E4046-APP | CG-ALL-3325 | 12.3 | Set the rwb.integration.FileDelivered.v1 payload to match RWB-P2-E4046-APP §12.3 (itemId, interfaceId, businessDate, documentId, sha256, recordCount, treatment id, requesting service), or record the difference. |
| CDC-05168 | RWB-P2-E4046-APP | CG-ALL-3326 | 12.3 | Set the rwb.integration.FileFailed.v1 payload to match RWB-P2-E4046-APP §12.3 (itemId, interfaceId, businessDate, attemptCount, last failure code, caseIds, treatment id, ownerRole), or record the difference. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05173 | RWB-P2-E4046-APP | CG-ALL-3332 | 12.5 | Add an Activities row for parkItemInException on rwb-integration, or name a catalogued activity in section 12.5 |
| CDC-05174 | RWB-P2-E4046-APP | CG-ALL-3333 | 12.5 | Add an Activities row for recordItemDecision on rwb-integration, or name a catalogued activity in section 12.5 |
| CDC-05175 | RWB-P2-E4046-APP | CG-ALL-3334 | 12.5 | Add an Activities row for resendItem on rwb-integration, or name a catalogued activity in section 12.5 |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05049 | RWB-P2-E2035-APP | GAP-2395 | find it | Name the rule package code rwb-comms reads once the rule registry owner settles the assignment; prove AC1 and AC5 against the three Epic 2 package codes as the fixture set. |
| CDC-05080 | RWB-P2-E2035-CON | GAP-0667 | 4 | Correct the GET /cases/{caseId}/next-action row to P2 read and P3 write; record the DP-13 ruling and the JOB-05 retirement in the timer register. |

### RWB-P2-E2035-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05053 | RWB-P2-E2035-APP | GAP-0669 | 13 | Fix the login, secret reference and worker identity; add the next-action-check job catalogue row with its run book path; review the three runbook entries with the on-call rota. |
| CDC-05081 | RWB-P2-E2035-CON | GAP-0669 | 7 | Fix the identity, secret reference and probe checks; create the next-action-check job_catalog row with its run book path. |

### RWB-P3-E2042-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05055 | RWB-P2-E2035-APP | GAP-2405 | 12 | Fix the row answer (packageCode, packageVersion, versionState, inForce, ruleId, ruleVersion, actionText, ownerRole, timerSpec, toState, droolsRuleName, outputs) and the latest-state-change answer (entryId, ruleId, ruleVersion, decidedAt, missing); add 404 and 422 for MSG-P3-027 and MSG-GEN-001. |
| CDC-05083 | RWB-P2-E2035-CON | GAP-2405 | 12 | Section 12.2 rule-catalog and decision-log rows carry the placeholder for the answer shape instead of invented field lists. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05056 | RWB-P2-E2035-APP | GAP-2324 | 7 | Add a Case record column for every role to the T6.1 matrix, publish the 14-area matrix as data, and fix the default scope of the specialist roles before PM-2026.12 is in force. |
| CDC-05084 | RWB-P2-E2035-CON | GAP-2324 | 12 | Extend T6.1 with a Case record column for every role; publish the 14-area matrix as data; fix the specialist default scope with the security administrator before PM-2026.12. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05070 | RWB-P2-E2035-CON | DOR-RWB-P2-E2035-CON-14 | header | Confirm and record the signed sign-off of the epic design for RWB-SVC-P2 in the epic design record. |
| CDC-05165 | RWB-P2-E4046-APP | DOR-RWB-P2-E4046-APP-14 | none | Record the signed epic design sign-off for this story and confirm it against the epic design record. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05085 | RWB-P2-E2035-CON | GAP-2322 | 12 | No story edit: section 12.2 reads the role class from rwb-case. The role-catalogue operation, authorise shapes, rwb-access login and unknown-role message belong to the target documents. |
| CDC-05091 | RWB-P2-E2035-CON | GAP-2409 | find it | Mark packageVersion required on GET /api/recovery/decision/v1/rule-catalog/{ruleId}; keep the MSG-GEN-001 refusal. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05106 | RWB-P2-E2035-OPS | DOR-RWB-P2-E2035-OPS-1 | 1 | Add role 'platform engineer' as a role code or name, or confirm the existing role code to use in §1. |
| CDC-05148 | RWB-P2-E2036-CON | DOR-RWB-P2-E2036-CON-1 | 1 | Add 'tech lead' as a role code or role name, or name the listed role that section 1 of RWB-P2-E2036-CON should use. |

### OTHER:Wave 3 entry check record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05178 | RWB-P2-E4046-APP | GAP-0436 | find it | Agree the W3J01 harness environment, seeding set, business date, product codes, evidence format, gate thresholds and the three unnamed operations with the integration and QA leads. |
| CDC-05179 | RWB-P2-E4046-APP | GAP-0432 | find it | Agree ALS interface ID, transport, layout, result codes, test endpoint, rwb-payment booking operation, data product code for v_ace_account and v_ace_payment, and outbound_item and interface_config field IDs. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05029 | RWB-P2-E2035-APP | CG-ALL-3256 | 12.2 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= through the provider's CON story RWB-P3-E2042-CON. |

### RWB-P2-E2033-APP; RWB-P2-E2035-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05045 | RWB-P2-E2035-APP | DOR-RWB-P2-E2035-APP-17 | find it | Deliver RWB-P2-E2033-APP and RWB-P2-E2035-OPS, the two build dependencies not yet done. |

### OTHER:Assumptions Register v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05046 | RWB-P2-E2035-APP | DOR-RWB-P2-E2035-APP-18 | find it | Add an assumption for open decision DL24 against RWB-P2-E2035-APP; DL24 text: Epic 1 loads allocation, assignment and transfer rules only (Business Requirements Epic 1 v5). |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:also FSD P4 A2.3 and A2.4 field catalogues) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05058 | RWB-P2-E2035-APP | GAP-2323 |  | Add CUSTOMER_PARTY as a fourth value of LOV-ROLE-CLASS in the load that carries the roles, and assign it to customer-party roles; confirm with the role catalogue owner before the wave 2 policy pack. |

### OTHER:TSD P4 (role rows; OTHER:DP-06 parameters contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05061 | RWB-P2-E2035-APP | GAP-2325 |  | Add a role_version label to the role load or state in T3.1 that role rows carry the matrix version; set the cache lifetime as a DP-06 parameter agreed at the wave 2 design review. |

### OTHER:rwb-case reference data (timer_spec list of values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05063 | RWB-P2-E2035-APP | GAP-2408 | 8 | Publish the timer spec shapes as a list of values with a parsing rule, extended with "payment due 30 days" and "deadline driven". |

### RWB-P7-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05065 | RWB-P2-E2035-APP | GAP-2410 |  | Record that a secondary slice builds against platform contracts and published fakes and reads wave-1 rows through its own schema within R5.7 rule 5. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05071 | RWB-P2-E2035-CON | DOR-RWB-P2-E2035-CON-8 | 12.1 | Publish the three REST operations in 12.1 in the yaml and catalog NextActionCheckWorkflow and findCasesWithoutNextAction in Temporal Catalog v1. |

### RWB-P3-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05076 | RWB-P2-E2035-CON | DOR-RWB-P2-E2035-CON-10 | find it | Add empty, loading, error and no access states for SCR-02 and SCR-03 |

### OTHER:Delivery plan (primary service of RWB-E2-033 to RWB-E2-036) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05089 | RWB-P2-E2035-CON | GAP-3187 | find it | Keep rwb-integration as primary for the four keys and record the RWB-E2-036 code-location tension for the assembly step; no story change. |

### OTHER:FSD P6 v3 and the rwb-comms story for RWB-E2-042 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05090 | RWB-P2-E2035-CON | GAP-2400 | find it | Read route-set fields in rwb-comms only where a notice is decided by a route-set rule; test the copy with R-RES-04 values; case next action stays with RWB-E2-035. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05092 | RWB-P2-E2035-CON | GAP-2325 | find it | Version role rows by matrix version or add a role_version label; add the cache lifetime as a DP-06 parameter with its value set at the wave 2 design review. |

### OTHER:rwb-case reference data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05094 | RWB-P2-E2035-CON | GAP-2408 | find it | Publish the timer spec shapes as a list of values with their parsing rule, and add 'payment due 30 days' and 'deadline driven' as legacy values. |

### OTHER:Work package (WP) build sequence (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05096 | RWB-P2-E2035-CON | GAP-2410 | find it | Record that the secondary slice of RWB-P7-E2035-APP builds against the platform contracts and published fakes, and reads wave-1 rows through its own schema. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; RWB-PLT-E1044-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05102 | RWB-P2-E2035-OPS | CG-ALL-3288 | find it | Record the decision_record library table as a dictionary object in LDM v9 or the owning platform document, or give its dictionary name. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:timer register; OTHER:rule registry values; RWB-P2-E2035-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05110 | RWB-P2-E2035-OPS | GAP-0667 | 12 | §12 records the read path under DP-13. The Ownership Map, timer register, registry rule values and contract names still have to change in their own documents. |

### RWB-P2-E2035-CON; RWB-P3-E2042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05113 | RWB-P2-E2035-OPS | GAP-2405 | find it | Fix the rule-catalog row answer (packageCode, packageVersion, versionState, inForce, ruleId, ruleVersion, actionText, ownerRole, timerSpec, toState, droolsRuleName, outputs) and the latest-state-change answer (entryId, ruleId, ruleVersion, decidedAt, missing; 200 with missing true when none); add 404 and 422 entries of MSG-P3-027 and MSG-GEN-001 for both reads. |

### OTHER:TSD P4 (T6.1 matrix; RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05114 | RWB-P2-E2035-OPS | GAP-2324 | find it | Add the Case record column for every role to T6.1, publish the full 14-area matrix as data through RWB-P4-AD002-APP, and fix the default scope of the specialist roles with the security administrator before PM-2026.12 is in force. |

### RWB-ITG-E2035-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05116 | RWB-P2-E2035-OPS | GAP-0418 | Header | The story row marks the route, harness and evidence values Not specified; the values belong to the ITG stage-check document. |

### OTHER:Build plan (primary service of RWB-E2-033 to RWB-E2-036) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05120 | RWB-P2-E2035-OPS | GAP-3187 | find it | Keep rwb-integration as primary for the four keys as the directive records, and record the tension for the assembly step. |

### OTHER:TSD P4 T3.1 and parameters contract DP-06 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05122 | RWB-P2-E2035-OPS | GAP-2325 | find it | State that role rows are versioned by the matrix version they are loaded with, or add a role_version label; set the cache lifetime as a DP-06 parameter agreed at wave 2 design review and test the version-keyed drop. |

### OTHER:rwb-case reference data and TSD P7 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05124 | RWB-P2-E2035-OPS | GAP-2408 | find it | Publish the timer spec shapes as a list of values in rwb-case reference data, extend it with 'payment due 30 days' and 'deadline driven', with parsing rule Not specified in the source documents (GAP-2408). |

### OTHER:11 Delivery and operations/Recovery Workbench Build Sequence Epic 1 and Epic 2 (workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05126 | RWB-P2-E2035-OPS | GAP-2410 |  | Record that a secondary slice builds against the platform contracts and published fakes and reads the same service's wave-1 rows through its own schema (R5.7 rule 5 lane depth). |

### RWB-P2-E2036-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05129 | RWB-P2-E2036-APP | DOR-RWB-P2-E2036-APP-21 | n/a | Set the build status of RWB-P2-E2036-CON to Done once the contract is published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml; OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05131 | RWB-P2-E2036-APP | DOR-RWB-P2-E2036-APP-8 | 4 | rwb-integration.yaml: add path POST /api/recovery/integration/v1/queues/{queueId}/placements. rwb-access: publish POST /api/recovery/access/v1/authorise. |

### OTHER:Wave 2 queue-placement harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05136 | RWB-P2-E2036-APP | GAP-0419 | none | Agree the composite route path and merge order with the platform edge story; hold repository, SIT environment, seeds, evidence format, retention and gate as harness data, agreed with QA at wave 2 entry |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05140 | RWB-P2-E2036-APP | GAP-3102 | 3 | Publish the hold element (case reference, deviation reference, code, open count, handler, return point, contact-stop flag, rule version) additively in major version 1; declare the case-event subscription against this catalogue; rwb-case owner declares the event-driven set and clear of recovery_case.deviation_open. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; RWB-P3-E1043-CON; RWB-P4-E1037-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05141 | RWB-P2-E2036-APP | GAP-2412 | 3 | Publish element names of rwb.decision-record.DecisionRecorded.v1, P3 case-read and P4 authorise shapes, reference-data operation, MSG-P7-009 text, per-service login name and platform contract rows. |

### OTHER:Delivery plan (primary P2 assignment for RWB-E2-033 to RWB-E2-036) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05143 | RWB-P2-E2036-APP | GAP-3187 |  | Keep rwb-integration primary for the four keys (no move to RWB-SVC-P3); record the code-location tension for the assembly step. |

### OTHER:P3 screen specification (SCR-02; OTHER:SCR-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05149 | RWB-P2-E2036-CON | DOR-RWB-P2-E2036-CON-10 | header | The screens belong to P3. This story builds no screen; section 15 only records the SCR-02 and SCR-07 states. |

### OTHER:Platform message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05152 | RWB-P2-E2036-CON | DOR-RWB-P2-E2036-CON-9 | 14 | Confirm the standard meaning of MSG-P4-001; the section 14 row keeps its current meaning until then |

### OTHER:Wave 2 integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05154 | RWB-P2-E2036-CON | GAP-0419 | 4 | Fix the composite route path and merge order with the platform edge story, and the repository, SIT environment, seeded data, evidence format, retention and pass/fail gate with QA |

### RWB-PLT-E1027-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05157 | RWB-P2-E2036-CON | GAP-2412 | 12.7 | Publish the decision-record fact element names, case-read and authorise shapes, reference-data operation, MSG-P7-009 text, service login name and platform rows as the item's fix lists. |

### OTHER:P3 screen specification (SCR-02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05160 | RWB-P2-E2036-CON | CG-ALL-3318 | 15 | SCR-02 states recorded as Not specified in the source documents; no states invented. |

### OTHER:P3 screen specification (SCR-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05161 | RWB-P2-E2036-CON | CG-ALL-3319 | 15 | SCR-07 states recorded as Not specified in the source documents; no states invented. |

### OTHER:rwb-case and rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05166 | RWB-P2-E4046-APP | DOR-RWB-P2-E4046-APP-8 | 12.1 | Publish POST /api/recovery/case/v1/cases/{caseId}/actions in rwb-case and POST /api/recovery/access/v1/authorise in rwb-access. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05177 | RWB-P2-E4046-APP | GAP-0673 | find it | Mark FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 INT-03 line superseded for legacy key RWB-E4-046, with date and decision; load the ALS interface_config row per environment. |

### OTHER:FSD P8 v3 A2.6 and the split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05180 | RWB-P2-E4046-APP | GAP-2547 | find it | Publish the FEAT-PAY-06 booking data set (case, treatment, account, accepted amount, business date, ALS interface) in A2.6 and add a requirement row for this slice in the next split-plan version. |

### OTHER:FSD P8 v3 (Data table and DP-05 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05181 | RWB-P2-E4046-APP | GAP-2549 | find it | Correct the Data table and DP-05 row so only rwb-source-data is drawn as reading recovery.v_ace_* views; retire the v_ace_account and v_ace_payment reads of this service. |

### RWB-P8-E4043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05182 | RWB-P2-E4046-APP | GAP-2548 | find it | Publish TreatmentBooked.v1 field list in BACKWARD mode, deliverFile manifest element set with booking branch, error envelope, fakes, ALS row values and data product code in TSD P8 appendix T-A. |

### OTHER:Split plan (work package lane L-P8-I; OTHER:C list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05184 | RWB-P2-E4046-APP | GAP-2550 | find it | Add to the C list of this slice: GET /treatments/{treatmentId} (RWB-S2), the rwb-source-data product read (RWB-P1), GET /admin/outbound-items and deliverFile(manifest) (RWB-P2), the rwb-case read (RWB-P3); keep the R5.7 Day-1 rule. |

### OTHER:Settlement route set (R-SET and R-RES rules) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05186 | RWB-P2-E4046-APP | GAP-2552 | find it | Fix the booking actor to rwb-payment's booking step after TreatmentApproved; add the settlement counterpart of R-RES-23 with its state, message and owner role. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0418 | Gateway-bff composite next-action route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0419 | Wave 2 queue-placement harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0432 | ALS interface, booking operation and wave 3 harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0669 | rwb-integration next action deployment: the login and secret reference, the next-action-check run values, the alert thresholds and the runbook ownership are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner | Resolved (directive) |
| GAP-0670 | rwb-integration queue-write adapter: the operation owner, the login, the consumed contract field names and the replay window are not fixed by one source | Solution architect | Resolved (directive) |
| GAP-0671 | rwb-integration queue-write adapter contract: the ownership of the placement path, the consumed contract shapes and the library table columns are not fixed by one source | Tech lead | Resolved (directive) |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0734 | The next-action slice leaves the legacy AC allocation, the daily check Schedule, the DL22 durations and the role-class field unspecified | Tech lead | Resolved (directive) |
| GAP-0735 | The placement slice leaves the legacy AC allocation, the approved callers list, the production matrix grant, the overflow shape, the caller mapping and the login name unspecified | Tech lead | Resolved (directive) |
| GAP-0957 | rwb-access queue-write authority: the request and answer element set of the placement admission part of POST /authorise and of the non-human part of GET /me/permissions is named by no source | Solution architect | Resolved (directive) |
| GAP-0958 | rwb-access queue-write authority: the refusal reason code vocabulary and the status each code answers with are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0959 | rwb-access queue-write authority: no source binds a role to a list of teams or regions, so a scope narrower than ALL cannot be resolved for a non-human caller | Security administrator | Resolved (directive) |
| GAP-0960 | rwb-access queue-write authority: how a caller code is bound to a Workbench role, and whether a caller code is itself a role, is fixed by no source | Security administrator | Resolved (directive) |
| GAP-2322 | rwb-access next action: the role-catalogue operation, the authorise request and answer of a next-action read, the rwb-access login and the message for an unknown role code are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2323 | rwb-access next action: the role class list has no customer-party value, while the legacy waiting text is produced for a customer party or a partner user | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2324 | rwb-access next action: the RBAC matrix tabulates three capability areas and gives no Case record letter, so the R rights and the scopes the next-action read needs are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2325 | rwb-access next action: a role row carries no version label of its own and the lifetime of a cached access or role answer is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2400 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Business analyst | Resolved (directive) |
| GAP-2405 | rwb-decision next action: the answer shape of the rule-catalog and latest-state-change reads, and their not-found and malformed-parameter messages, are not specified | Solution architect | Resolved (directive) |
| GAP-2406 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Business analyst, P7 | Resolved (directive) |
| GAP-2407 | rwb-decision next action: no source enumerates the decision codes or final calls that count as a state change for the latestStateChange filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2408 | rwb-decision next action: rule_row.timer_spec has no list of values, and two legacy specs are outside the four shapes the legacy rule enumerates | Business analyst, Epic 2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2409 | The published catalogue path shows packageVersion as an optional query parameter and no source says what an absent value answers | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2411 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2547 | The legacy key leaves this slice one generic criterion, its four test cases carry no booking data, the FSD success criterion is a single line and the plan gives the slice no requirement id | P8 business analyst and the FSD owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2548 | No contract story is allocated to this legacy key, and the outbound manifest, the event payload, the data product code and the ALS interface values are unpublished | P8 solution architect, the P2 integration owner and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2549 | The legacy story reads v_ace_account and v_ace_payment in process while the target gives the ACE views to rwb-source-data alone | P1 source-data owner and the P8 solution architect | Resolved (directive) |
| GAP-2550 | The work package gives the contract-dependency row as None while the story consumes four REST contracts and one activity contract, and it still starts on Day 1 | P8 solution architect and the split-plan owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2551 | The legacy key tracks the booking in outbound_item, a table this service owns in the monolith and rwb-integration owns in the target | P8 solution architect and the P2 integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2552 | No source says which service raises the booking call after the accepted treatment, and the settlement path has no rejection rule row of its own | P8 business analyst and the Settlement route set owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3102 | RWB-S8-E2036-APP: the deviation hold that the queue-write interface obeys has no published element names, no case-event names, no case-side setter for deviation_open and no placement-half criteria, and the pattern set adds dependencies the metadata rows do not carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
