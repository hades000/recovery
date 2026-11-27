# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 2 of 12 (RWB-P3-E1018-OPS to RWB-P3-E1021-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 206 |
| Cross-document (pending in another document) | 210 |
| Not applied (value not in the sources) | 4 |
| Open business decisions | 18 |
| Register gaps linked | 80 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E1018-OPS | 22 | 30 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1018 OPS Case ID issuance and case record v1 - deployment v2.md |
| RWB-P3-E1019-APP | 32 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1019 APP Roles, teams and queues as data v2.md |
| RWB-P3-E1019-CON | 21 | 21 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1019 CON Roles, teams and queues as data - contract v2.md |
| RWB-P3-E1019-DB | 20 | 25 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1019 DB Roles, teams and queues as data - ACE DB v2.md |
| RWB-P3-E1020-APP | 29 | 26 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1020 APP Allocation and assignment engine v1 v2.md |
| RWB-P3-E1020-CON | 20 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1020 CON Allocation and assignment engine v1 - contract v2.md |
| RWB-P3-E1020-OPS | 17 | 25 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1020 OPS Allocation and assignment engine v1 - deployment v2.md |
| RWB-P3-E1021-APP | 27 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1021 APP Transfer rules and engine v1 v2.md |
| RWB-P3-E1021-CON | 18 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1021 CON Transfer rules and engine v1 - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E1019-DB | R-10219 | CG-ALL-3509 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1020-CON | R-10226 | CG-ALL-3538 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1021-APP | R-10233 | CG-ALL-3559 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1021-CON | R-10239 | CG-ALL-3574 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-22002 | GAP-0685 | Register gap | Business owner; reference data administrator | The source of the caseload cap is not fixed: parameter row or reference data | Keep the cap as versioned reference data on queue.capacity_cap and queue_member.capacity, as the legacy data model does, and add a parameter key only if a product-level override is wanted; state the ruling in the Reference Data and Parameters design. |
| RWB-ITG-E1021-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-22012 | GAP-3078 | Register gap | P7 rwb-decision owner with the business owner of module S8 | The TRANSFER rows that fire on the deviation triggers and the text of R-DEV-04 to R-DEV-06 are not published | The rule owner publishes the DEV transfer rows and the text of R-DEV-04 to R-DEV-06 with the package version; the story then reads them unchanged and no code changes. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-28522 | GAP-0686 | Register gap | Business owner, Shared operations; platform team, Temporal | The exact cadence of the rebalancing trigger is not defined for rwb-case | Run JOB-06 as its own Temporal Schedule at 06:30 Asia/Bangkok, after DailyCaseRun has finished, with overlap policy SKIP and a catch-up window; confirm the order with the operations owner and record it in the Temporal Workflow and Activity Catalog. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1019-ITG, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P4-E1022-APP, RWB-P5-E1025-APP, RWB-P5-E1025-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP | R-35406 | ASM-1988 | Register assumption |  | The approver of a document-type load is the legal counsel who owns the type table, holding Reference data A, as the legacy story assumes under DL01; the loader holds Reference data C and may not approve | Business lead with Legal confirms the role that approves the type list |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS | R-36258 | ASM-1233 | Register assumption |  | JOB-06 rebalancing runs as its own Temporal Schedule at 06:30 Asia/Bangkok after DailyCaseRun, with overlap policy SKIP and a catch-up window, and its expression is a chart value rather than a constant. | Business owner, Shared operations |
| RWB-P3-E1021-APP, RWB-P3-E1021-OPS | R-36261 | ASM-1236 | Register assumption |  | A transfer refused by the TRANSFER rule, the cap check, the status check or the hold check is final in Epic 1: there is no override path, nothing changes, and the caller may retry with another target owner or queue. | Business owner, case and workflow |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E1020-APP | R-00704 | CG-ALL-3524 | 12.4 | Java package th.co.scb.ace.workbench.recovery.case.allocation uses the reserved word 'case' | No non-reserved package segment in sources. Service Template Spec v1 (L371) gives only the reserved 'case'. Needs the solution architect's ruling; no name invented. |
| RWB-P3-E1020-APP | R-00705 | CG-ALL-3525 | 12.4 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | No non-reserved base package segment in sources. Service Template Spec v1 (L371) gives only the reserved 'case'. Needs the solution architect's ruling; no name invented. |
| RWB-P3-E1020-APP | R-04978 | DOR-RWB-P3-E1020-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version for RWB-P3-E1020-CON in the story or sources; only the /v1 path is stated. Filling one would invent a version. |
| RWB-P3-E1021-CON | R-15856 | DOR-RWB-P3-E1021-CON-11 | 11; 17 | Definition of Ready item 11 Guardrails: Partial | Field not identifiable: detcheck X10 names no field, and the story text in §12.3/§17 was not supplied. Searched review file, audit and notapplied JSON; no field list found. |

## 5. Cross-document changes (pending in the target document)


### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05430 | RWB-P3-E1018-OPS | DOR-RWB-P3-E1018-OPS-14 | none | Record the signed epic design sign-off. |
| CDC-05457 | RWB-P3-E1019-APP | DOR-RWB-P3-E1019-APP-14 | 3 | Confirm and record the signed epic design sign-off for this story's epic; not recorded in the story or sources. |
| CDC-05470 | RWB-P3-E1019-CON | DOR-RWB-P3-E1019-CON-14 | 3 | Record the signed epic design sign-off for RWB-SVC-P3. |
| CDC-05492 | RWB-P3-E1019-DB | DOR-RWB-P3-E1019-DB-14 | 2 | Record the epic design sign-off for RWB-P3-E1019-DB so the story and its DOR item 14 cite the signed design. |
| CDC-05517 | RWB-P3-E1020-APP | DOR-RWB-P3-E1020-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-P3, so that this story can evidence Definition of Ready item 14. |
| CDC-05565 | RWB-P3-E1020-OPS | DOR-RWB-P3-E1020-OPS-14 |  | Record the signed epic design sign-off for the service epic RWB-SVC-P3, so the epic design record shows the signed design behind this story. |
| CDC-05591 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-14 | n/a | Record the signed epic design sign-off for EP01 so this story can cite it. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05450 | RWB-P3-E1018-OPS | CG-ALL-3487 | 18 | Align the test lists for the seven requirements with section 18 of RWB-P3-E1018-OPS. |
| CDC-05484 | RWB-P3-E1019-CON | CG-ALL-3500 | 18 | Align the REQ-CWC-006 and REQ-ACA-002 test lists in the RTM with section 18 of RWB-P3-E1019-CON in the next version. |
| CDC-05532 | RWB-P3-E1020-APP | CG-ALL-3523 | 18 | Align the trace test lists of the four requirements with section 18 in the RTM's next version. |
| CDC-05555 | RWB-P3-E1020-CON | CG-ALL-3537 | 18 | Align the test lists of REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and the fourth requirement with section 18 of RWB-P3-E1020-CON in the next RTM version. |
| CDC-05578 | RWB-P3-E1020-OPS | CG-ALL-3545 | 18 | Align the test lists for REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and REQ-CWC-016 with section 18 of this story in the next RTM version. |
| CDC-05606 | RWB-P3-E1021-APP | CG-ALL-3558 | 18 | Section 18 now lists TC-E1-021-17 and TC-E1-021-18 for REQ-CWC-010; the remaining test-list alignment with RTM v7 belongs to its next version. |
| CDC-05624 | RWB-P3-E1021-CON | CG-ALL-3573 | 18 | Align test lists for the four requirements that differ (REQ-CWC-010, REQ-CWC-016 and two more) with section 18 of this story. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05598 | RWB-P3-E1021-APP | CG-ALL-3554 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseStateChanged.v1 (EV-05), with its ACL. |
| CDC-05599 | RWB-P3-E1021-APP | CG-ALL-3555 | 12.4 | Add rwb-case as a consumer of rwb.decision.ApprovalRequested.v1 (EV-09), with its ACL. |
| CDC-05603 | RWB-P3-E1021-APP | GAP-3079 | 12.3 | Owners publish the Kafka event names of the case triggers on rwb.case.events.v1 and rwb.source-data.events.v1 before release, so consumer groups and fact mapping bind to them. |
| CDC-05612 | RWB-P3-E1021-CON | CG-ALL-3569 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseStateChanged.v1 and grant the matching ACL. |
| CDC-05613 | RWB-P3-E1021-CON | CG-ALL-3570 | 12.4 | Add rwb-case as a consumer of rwb.decision.ApprovalRequested.v1 and grant the matching ACL. |
| CDC-05615 | RWB-P3-E1021-CON | DOR-RWB-P3-E1021-CON-8 | 12.3, 12.4 | Aligned section 12.3 payloads; consumer entries remain for the catalog. |
| CDC-05619 | RWB-P3-E1021-CON | GAP-3079 | find it | Publish Kafka event names for trigger events EV-05, EV-06, EV-07, EV-09, EV-12, EV-16, EV-18 before the release date. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05449 | RWB-P3-E1018-OPS | CG-ALL-3486 | 16 | Add rows for TC-P3-E1018-OPS-01 to -05 with Given, When and Then copied from AC1 to AC6. |
| CDC-05483 | RWB-P3-E1019-CON | CG-ALL-3499 | 16 | Add rows TC-P3-E1019-CON-01 to TC-P3-E1019-CON-06 with Given, When and Then copied from AC1 to AC6 of this story. |
| CDC-05507 | RWB-P3-E1019-DB | CG-ALL-3507 | 16 | Add rows TC-P3-E1019-DB-01 to TC-P3-E1019-DB-06 with Given, When and Then copied from the criteria they cover. |
| CDC-05554 | RWB-P3-E1020-CON | CG-ALL-3536 | 16 | Add rows for TC-P3-E1020-CON-01 to TC-P3-E1020-CON-06 with Given, When and Then copied from the criteria they cover. |
| CDC-05577 | RWB-P3-E1020-OPS | CG-ALL-3544 | 16 | Add rows TC-P3-E1020-OPS-01 to -05 with Given, When and Then copied from AC1 to AC5. |
| CDC-05623 | RWB-P3-E1021-CON | CG-ALL-3572 | 16 | Add rows TC-P3-E1021-CON-01 to TC-P3-E1021-CON-06 with Given, When and Then copied from the criterion each covers. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05466 | RWB-P3-E1019-APP | GAP-0683 | 3, 10 | Record RW-TEAMMGR with Reference data A for TEAM, QUEUE and QUEUE_MEMBER as a confirmed grant; a refusal returns 403 MSG-P4-002. |
| CDC-05471 | RWB-P3-E1019-CON | DOR-RWB-P3-E1019-CON-1 | 1 | Add a role code and name for the consumer of the rwb-case case and workflow service; the source documents give none. |
| CDC-05495 | RWB-P3-E1019-DB | DOR-RWB-P3-E1019-DB-1 | 1 | Add 'ACE database engineer' as a role name or role code, or confirm the code that section 1 should use. |
| CDC-05512 | RWB-P3-E1019-DB | GAP-0683 | 3, 10 | Record the grant that RW-TEAMMGR holds Reference data A on TEAM, QUEUE and QUEUE_MEMBER, as confirmed by the access owner, in the rwb-access grant data. |
| CDC-05559 | RWB-P3-E1020-CON | GAP-0987 | find it | Record permission-matrix version PM-2026.11 in force at 30 November 2026 with PM-2026.12 from 2026-12-01, and the role roster: RW-TEAMMGR and RW-CAPACITY R (TEAM), RW-CASEOWN R (OWN), RW-AUDIT R (ALL), SY-CASEWF CRU, SY-RULES R, RW-REFADM none, RW-PLATADM U for rerun. |
| CDC-05614 | RWB-P3-E1021-CON | DOR-RWB-P3-E1021-CON-1 | 1 | Add a role code or name for the consumer of the case service (any service or the gateway-bff), or record it as a system actor outside the role list. |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05443 | RWB-P3-E1018-OPS | GAP-2433 | 14 | Write the text of MSG-P7-009 (naming the field and case reference) and MSG-P7-012 (naming the chain position) and add both rows. |
| CDC-05447 | RWB-P3-E1018-OPS | GAP-2434 | 12.8 | Add finalCall to the query parameters of API-P7-006 and fix the creation filter answer as a page of entries with the thirteen fields of this story. |
| CDC-05524 | RWB-P3-E1020-APP | GAP-0345 | 8, 10 | Fix the rerun facade for a DailyCaseRun workflow step (JOB-03) in the P1 contract before wave 1 exit |
| CDC-05546 | RWB-P3-E1020-CON | GAP-0345 | 12 | Publish the JOB-03 step state on the rwb-case run result; keep the catalogue read and rerun on the P1 job catalogue; fix the rerun facade for a workflow step in the P1 contract before wave 1 exit. |
| CDC-05570 | RWB-P3-E1020-OPS | GAP-0345 | find it | Publish JOB-03 step state on the rwb-case run result; fix the rerun facade for a workflow step in the P1 contract before wave 1 exit. |

### RWB-P4-E1037-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05459 | RWB-P3-E1019-APP | GAP-2273 | none | Add POST and GET /api/recovery/access/v1/admin/queue-file-checks with Reference data C for the check and R for the read; the cap maximum and seven finding codes stay in that contract document. |
| CDC-05474 | RWB-P3-E1019-CON | GAP-0679 | 11, 12 | Confirm the column list of the role and TEAM split with P4 in the rwb-access authorise contract; story section 12.7 records the split. |
| CDC-05479 | RWB-P3-E1019-CON | GAP-0775 | 3, 12.2, 12.7 | Resolve the role set, the scope with the team and region codes and the two version labels on every authorise call and return them; the edge keeps them on its session record in the gateway-bff Redis store until the session ends, cleared by the access event; the ROLE_CONFLICT refusal fact raises the incident to the security administrator queue. |
| CDC-05486 | RWB-P3-E1019-CON | GAP-1567 | find it | Drop lov_value and partner_user from TSD P4 T3.1; state in the rwb-access contract which list-of-values versions and partner identity attributes it reads and its refresh rule. |
| CDC-05625 | RWB-P3-E1021-CON | GAP-0990 | find it | Publish the authorise request and answer schema with the legalHold attribute; confirm the matrix version label in force at 30 November 2026 with the matrix owner; tabulate the Queue and allocation letters in TSD P4 T6.1. |

### RWB-P3-E1020-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05518 | RWB-P3-E1020-APP | DOR-RWB-P3-E1020-APP-21 | header | Build status is Not started; it must reach Done before this story is ready. |
| CDC-05519 | RWB-P3-E1020-APP | DOR-RWB-P3-E1020-APP-22 | header | Publish a contract fake library version and record it. |
| CDC-05527 | RWB-P3-E1020-APP | GAP-3072 | 4 | Section 4 step 3 marks the handler roster and the handler selection as Not specified (GAP-3072) and records that no handler cap applies. |
| CDC-05566 | RWB-P3-E1020-OPS | DOR-RWB-P3-E1020-OPS-21 | header | Set build status to Done once the contract is published. |
| CDC-05567 | RWB-P3-E1020-OPS | DOR-RWB-P3-E1020-OPS-22 | header | Publish the contract fake library and record its version. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05429 | RWB-P3-E1018-OPS | CG-ALL-3480 | 13 | Create the story file for RWB-P7-E1073-CON, the P7 rule-package contract named as C RWB-P7-E1073-CON in §13 DP-04, or point that cell at the existing story key that carries the same capability. |
| CDC-05431 | RWB-P3-E1018-OPS | DOR-RWB-P3-E1018-OPS-17 | 13 | Create the RWB-P7-E1073-CON story file so the §13 DP-04 dependency names an existing story; the story keeps Depends on (build) None (Day 1 by rule, §R5.7) with its platform contracts in §3. |
| CDC-05564 | RWB-P3-E1020-OPS | CG-ALL-3541 | 13 | Create story file RWB-P7-E1073-CON, or the solution architect names the existing story that replaces it in the section 13 DP-04 row. |
| CDC-05611 | RWB-P3-E1021-CON | CG-ALL-3566 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that carries the P7 decision capability, and update the reference. |

### RWB-P3-E1018-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05432 | RWB-P3-E1018-OPS | DOR-RWB-P3-E1018-OPS-21 | none | Complete the build and set status to Done so the contract is published. |
| CDC-05433 | RWB-P3-E1018-OPS | DOR-RWB-P3-E1018-OPS-22 | none | Publish a contract fake library version and record it as published. |
| CDC-05442 | RWB-P3-E1018-OPS | GAP-0676 | 12.1 | Record the field-level OpenAPI schema: required flags per operation, GET /cases page and sort parameters, caseNo pattern and error codes per operation. |
| CDC-05455 | RWB-P3-E1018-OPS | GAP-1038 | find it | Name the rwb_document login and its grants under DP-02; publish the case-read field names and the not-found message ID in RWB-P3-E1018-CON for citation in place of the placeholder. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05491 | RWB-P3-E1019-DB | CG-ALL-3504 |  | Higher-precedence source Reference Data v5 says closed list. BR6 names LOV-SNAPSHOT-STATUS, but the yaml enum is fixed in the other document, so no story edit. |
| CDC-05494 | RWB-P3-E1019-DB | DOR-RWB-P3-E1019-DB-8 |  | Keep status as the closed enum, as Reference Data v5 records LOV-SNAPSHOT-STATUS as 'Closed list'. |
| CDC-05520 | RWB-P3-E1020-APP | DOR-RWB-P3-E1020-APP-8 | find it | Hold assignmentMethod, reason and status as references to LOV-ASSIGN, LOV-ASSIGN-REASON and LOV-CASE-STATUS, not closed enums. |
| CDC-05589 | RWB-P3-E1021-APP | CG-ALL-3551 | 13 | Remove the closed enum on transferReasonCode and validate its values against LOV-TRANSFER-REASON as reference data, as the story states. |

### RWB-PLT-NF06-DB (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05605 | RWB-P3-E1021-APP | GAP-0688 | 3 | ACE DB team names the per-service database login of rwb-case and its grant set; chart takes it by vault secret reference. |
| CDC-05610 | RWB-P3-E1021-APP | GAP-1037 | find it | Allocate the rwb-document login name, its grants (schema rwb_document only) and its secret reference, and record them in the service catalogue. |
| CDC-05622 | RWB-P3-E1021-CON | GAP-0688 | find it | ACE DB team names the rwb-case database login and its grant set; chart then takes it by vault secret reference. |
| CDC-05629 | RWB-P3-E1021-CON | GAP-1037 | find it | Allocate the rwb-document login name, its grants (schema rwb_document only, no privilege on another schema) and its secret reference; record them in the service catalogue. |

### RWB-P3-E1019-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05458 | RWB-P3-E1019-APP | DOR-RWB-P3-E1019-APP-21 | 3 | Set the build status of RWB-P3-E1019-CON to Done (it is Not started) so the contract is published. |
| CDC-05493 | RWB-P3-E1019-DB | DOR-RWB-P3-E1019-DB-21 |  | Set the build status to Done once the contract is published. |
| CDC-05499 | RWB-P3-E1019-DB | GAP-0681 | 4, 12 | Publish the Queues template as an xlsx workbook with one header row per sheet (QUEUE, QUEUE_MEMBER), a column per queue and queue_member field, and one check per required column. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05522 | RWB-P3-E1020-APP | DOR-RWB-P3-E1020-APP-9 | 12, 14 | Supply v4 wording for MSG-P3-012 and MSG-P3-027 so section 14 can match it |
| CDC-05600 | RWB-P3-E1021-APP | CG-ALL-3556 | 14 | The v4 wording of MSG-P3-027 is Not specified in the source documents, so the story text is left unchanged and the standard owner must publish it. |
| CDC-05601 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-9 | 14 | Confirm the MSG-P3-027 entry wording against section 14 of RWB-P3-E1021-APP; section 14 text is kept until the v4 wording is supplied. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05526 | RWB-P3-E1020-APP | GAP-2443 | 3 | Add the package-artifact GET operation on the service base with model-owner identity and checksum in the answer, at the next version. |
| CDC-05548 | RWB-P3-E1020-CON | GAP-2443 | 11 | Add the package-artifact operation to the P7 provided operations with the model-owner identity and the checksum in the answer; keep the assumed path or fix it differently. |
| CDC-05572 | RWB-P3-E1020-OPS | GAP-2443 | find it | Add GET /rule-models/{packageCode}/{version} (or the fixed path) for the package artifact, with model-owner identity and checksum in the answer. |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05530 | RWB-P3-E1020-APP | GAP-2441 | 4 | Section 4 step 6 marks how the business date and the queue and owner identifiers travel in the decision record as Not specified (GAP-2441). |
| CDC-05552 | RWB-P3-E1020-CON | GAP-2441 | 12 | Carry the business date as a record attribute and the queue and owner identifiers as named members of the actions payload, fixed in the envelope at contract review. |
| CDC-05575 | RWB-P3-E1020-OPS | GAP-2441 |  | At contract review, add the business date as a record attribute and name the queue and owner identifiers in the actions payload. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05534 | RWB-P3-E1020-APP | GAP-3209 |  | Add one criterion-ownership column giving, for each legacy criterion AC1 to AC13, the single new story that owns it. |
| CDC-05557 | RWB-P3-E1020-CON | GAP-3209 | find it | Add one criterion-ownership column listing, for each legacy criterion AC1 to AC13, the single new story that owns it. |
| CDC-05582 | RWB-P3-E1020-OPS | GAP-3209 | header | Add one criterion-ownership column listing, for each of the thirteen legacy criteria, the single new story that owns it. |

### RWB-S8-E1020-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05539 | RWB-P3-E1020-APP | GAP-3073 |  | Take DeviationRaised and DeviationCleared with consumers from TSD S8 T0.2 and T5.2.1; keep wave 1; build behind the service baseline. |
| CDC-05561 | RWB-P3-E1020-CON | GAP-3073 | find it | Carry event names DeviationRaised and DeviationCleared with their consumers from TSD S8 T0.2 and T5.2.1; keep wave 1 and the tentative date; treat DP platform contracts as wave 0 preconditions. |
| CDC-05586 | RWB-P3-E1020-OPS | GAP-3073 | n/a | Take DeviationRaised and DeviationCleared for EV-06 and EV-07 from TSD S8 T0.2 and T5.2.1; build behind the service baseline with no element or tag of its own; keep wave 1; treat DP platform contracts as wave 0 preconditions. |

### RWB-P3-E1021-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05593 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-21 | n/a | Build the contract story to Done. |
| CDC-05594 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-22 | n/a | Publish a contract fake library version and record it as published. |
| CDC-05595 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-23 | header | No source fixes the contract version, so the header records it as Not specified; the contract story must fix it. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20632 | RWB-P3-E1018-OPS | R-21985 |  | RWB-E1-018 'What moves' already makes party_ext and account_ext P1 tables, read by P3 through contract (GAP-3162). |
| CDC-20633 | RWB-P3-E1019-DB | R-21996 |  | RWB-E1-019 'What moves' already makes role a P4 table, read by P3 through contract (GAP-3159). |
| CDC-20673 | RWB-P3-E1020-OPS | R-28528 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21890', 'R-28478', 'R-28528', 'R-28558', 'R-28573', 'R-28662'] |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05436 | RWB-P3-E1018-OPS | DOR-RWB-P3-E1018-OPS-12 Test cases: Partial | 16 | Added TC-06 (contract), TC-07 (boundary), TC-08 (AC7), TC-09 (AC8) and TC-10 (AC9) to section 16. |
| CDC-05473 | RWB-P3-E1019-CON | DOR-RWB-P3-E1019-CON-12 | 16, 18 | Register TC-P3-E1019-CON-01 to TC-P3-E1019-CON-07 in Test Cases v8 and align the RWB-P3-E1019-CON test list with RTM v7. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05468 | RWB-P3-E1019-APP | GAP-1177 | find it | Add a caching rule for reference readers: cache for one call only; a longer-lived cache is an owner contract with a version and an invalidation event. |
| CDC-05558 | RWB-P3-E1020-CON | GAP-0687 | find it | Expose replicas, autoscaling bounds, node pool, connection pool size and history archive as chart values with documented defaults; record SIT findings. |

### RWB-P3-E1019-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05472 | RWB-P3-E1019-CON | DOR-RWB-P3-E1019-CON-10 | 1 | Add empty, loading, error and no-access states for SCR-42 (P3). |
| CDC-05496 | RWB-P3-E1019-DB | DOR-RWB-P3-E1019-DB-10 | find it | Add empty, loading, error and no access states for screen SCR-42. |

### RWB-P6-E1019-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05476 | RWB-P3-E1019-CON | GAP-1178 | 12 | Carry TC-E1-019-13 in RWB-P6-E1019-APP as the guard test of the routing read, and record in the test case register that the load-path proof of the legacy case is owned by RWB-P3-E1019-APP. |
| CDC-05502 | RWB-P3-E1019-DB | GAP-1178 | find it | Carry TC-E1-019-13 as the guard test of the routing read; record that the load-path proof of the legacy case is owned by RWB-P3-E1019-APP. |

### RWB-P6-E1019-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05478 | RWB-P3-E1019-CON | GAP-1174 |  | Add RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON and RWB-PLT-E1044-CON to the H and C dependencies of RWB-P6-E1019-APP, or record them in the platform release train. |
| CDC-05505 | RWB-P3-E1019-DB | GAP-1174 | find it | Add RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON and RWB-PLT-E1044-CON to the dependency rows, or record them in the platform release train. |

### RWB-P2-E2036-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05480 | RWB-P3-E1019-CON | GAP-0670 | 12 | Serve POST /api/recovery/integration/v1/queues/{queueId}/placements as the admission and forwarding operation; treat POST /api/recovery/case/v1/queues/{queueId}/placements as P3-owned and consumed; read approved callers via the rwb-case parameter contract under rwb.casewf.placement.approved-callers. |
| CDC-05481 | RWB-P3-E1019-CON | GAP-0671 | 12 | Declare the integration-base placement as provided (four body fields, required Idempotency-Key, 201 shape); declare the case-base placement as consumed and owned by P3; mark consumed JSON element names as placeholders; take idempotency_key columns from TSD P2 v3 T3.1; state the 24-hour replay window as the platform rule. |

### OTHER:RWB-PLT-DB (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05528 | RWB-P3-E1020-APP | GAP-3207 | 3 | Section 3 keeps the login and the cap storage marked Not specified in the source documents (GAP-0684, GAP-0685, GAP-3207). |
| CDC-05574 | RWB-P3-E1020-OPS | GAP-3207 | 4 | Publish the per-service login name for rwb-case; keep the cap as data on the queue with its default delivered through the rwb-case parameter contract. |

### RWB-P3-E1020-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05529 | RWB-P3-E1020-APP | GAP-3208 | 4 | State the Temporal cron expression and the rule for a business date with no run. |
| CDC-05551 | RWB-P3-E1020-CON | GAP-3208 | 12 | Keep the AceDataReady event start as primary trigger; register one catch-up Schedule per business date with overlap policy SKIP; fix the cron expression where deployment is described; 07:00 Asia/Bangkok stays the alert deadline. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05531 | RWB-P3-E1020-APP | GAP-2439 | 11 | Take rule_package_version columns from the LDM; confirm the artifact payload with RWB-PLT-E1072-CON. |
| CDC-05576 | RWB-P3-E1020-OPS | GAP-2439 |  | Publish the rule_package_version columns for state, valid-from, approver, DRL and checksum, and confirm the artifact payload with RWB-PLT-E1072-CON. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05537 | RWB-P3-E1020-APP | GAP-2440 |  | Load the row once with the rule ID the workbook carries; record the other label as the row description. |
| CDC-05596 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-5 | 9 | Confirm 'On hold' is a LOV-CASE-STATUS value. Story §9 now names status_before_hold as a LOV-CASE-STATUS value. |

### OTHER:P7 message catalogue (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05538 | RWB-P3-E1020-APP | GAP-2442 |  | Approve text for MSG-P7-009 and the chain-break warning, and name the per-entry chain result field. |
| CDC-05560 | RWB-P3-E1020-CON | GAP-2442 | find it | Approve message text for MSG-P7-009 and the chain-break warning, and name the per-entry chain result field, with the ID and same-day Compliance report unchanged. |

### OTHER:Business Requirements Document (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05545 | RWB-P3-E1020-CON | GAP-1456 | 8 | State in section 8.2 that Epic 1 requirement stories keep wave 1 while service epics rwb-payment, rwb-asset and rwb-deviation start in wave 2 |
| CDC-05602 | RWB-P3-E1021-APP | GAP-1456 | 8 | State in section 8.2 that Epic 1 stories keep the business-epic wave; delivery lead confirms the wave per story at build sequencing. |

### OTHER:Service Catalog and RWB-PLT-DB stories (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05547 | RWB-P3-E1020-CON | GAP-0684 | 12 | Allocate the rwb-case service login with the rwb_case schema in the 19-schema list, derive it from the schema name, store it in Key Vault, and record the name before first deployment. |
| CDC-05571 | RWB-P3-E1020-OPS | GAP-0684 | find it | Record the rwb-case login name, derived from schema rwb_case and stored in Key Vault, before first deployment. |

### 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05563 | RWB-P3-E1020-CON | GAP-2150 | 1 | Confirm that RWB-E1-020 stays the worked example and that the contract story RWB-P3-E1042-CON, parameters, stands beside it as the realignment example showing every item of section 2 (DP-06; GAP-2150; ASM-3448). |
| CDC-20547 | RWB-P3-E1020-CON | R-28529 |  | Section 1 last paragraph already names RWB-E1-020 as the worked example and RWB-P3-E1042-CON beside it, not replacing it (GAP-2150). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05427 | RWB-P3-E1018-OPS | CG-ALL-3478 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05428 | RWB-P3-E1018-OPS | CG-ALL-3479 | 12.2 | No nearest published path is named in the source, so the story cannot be re-pointed; the provider must publish the operation. |

### OTHER:rwb-source-data, rwb-access and rwb-decision API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05434 | RWB-P3-E1018-OPS | DOR-RWB-P3-E1018-OPS-8 | 12 | Publish GET /api/recovery/source-data/v1/freshness, POST /api/recovery/access/v1/authorise and GET /api/recovery/decision/v1/rule-models/{n}/{v} in the named services' yaml, or drop them from the story; align the event name to rwb.decision.DecisionRecorded.v1 as in Kafka Catalog v1. |

### OTHER:Functional Specification Document P3 (FSD P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05435 | RWB-P3-E1018-OPS | GAP-1549 | none | Restate FSD P3 A1.5 read path as a read through the rwb-source-data contract, not the recovery.v_ace_* views; keep the business-key link rules. |

### OTHER:Service API document of rwb-source-data (P1 target API inventory) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05437 | RWB-P3-E1018-OPS | GAP-0571 | find it | Publish GET /api/recovery/source-data/v1/entry-candidates with businessDate and threshold required, page and size optional; response EntryCandidatePage (businessDate, threshold, asOf, page, size, total, candidates[], breaks[]); statuses 400, 401, 403, 409, 422, 503; OpenAPI 3.1 fragment of the three operations. |

### OTHER:Recovery Workbench FSD P1 v3 A2.11 (OQ-P1-06) and the rwb-source-data entry-candidate contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05438 | RWB-P3-E1018-OPS | GAP-0575 | find it | Return breaks in the candidate response: one row per key and view with no row, keyType ACCOUNT or PERSON, businessKey, viewName, businessDate; counted in the run log; no dq_ table; durable list stays with RWB-P1-E1011-APP. |

### OTHER:Database story of RWB-SVC-P3 and the service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05439 | RWB-P3-E1018-OPS | GAP-0675 | find it | Allocate the rwb-case login name and its grants (schema rwb_case only, no privilege on another schema) and record it in the service catalogue. |

### OTHER:rwb-source-data API document (account_ext and party_ext write operations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05440 | RWB-P3-E1018-OPS | GAP-0573 | find it | Expose two PUT operations by business key for account_ext.dispute_open and party_ext with all four party flags in the body; a changed body replaces the flags and increments the version; P1 validates the token and holds no role model. |

### OTHER:rwb-source-data entry-candidate contract (product_group field) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05441 | RWB-P3-E1018-OPS | GAP-0576 | find it | Return product_group as the product_category value read from the view, unvalidated and unmapped; values outside LOV-PRODUCT are returned as read; mapping and validation belong to the rwb-case reference-data contract. |

### OTHER:TSD P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05444 | RWB-P3-E1018-OPS | GAP-2435 | 12.7 | Restate DF-DEC-002 as an indexed business key with no foreign key, drop the recovery_case row of T3.3, and state in T3.1 that the ALS business date is carried in inputs_ref. |

### OTHER:Package ENTRY workbook (rule-row catalogue) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05445 | RWB-P3-E1018-OPS | GAP-2436 | 16 | Name the rule ID that admits a case and copy it into the registry fixture of this story. |

### OTHER:Build Notes v6 (RWB-E1-018 View note) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05446 | RWB-P3-E1018-OPS | GAP-3162 | 12.7 | Keep case tables in P3; write party_ext and account_ext rows in RWB-P1-E1018-APP and read them back by contract. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05448 | RWB-P3-E1018-OPS | GAP-0674 | 12.2 | Publish the gateway-bff composite route for SCR-02 and SCR-03 with its path, parallel calls, merge order, masking rules and 2 s budget. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05451 | RWB-P3-E1018-OPS | GAP-0982 | find it | Add the case-authority request and answer schema for POST /api/recovery/access/v1/authorise; record in TSD P4 T3.1 where caller teams and regions are held; list case-record personal field IDs and version for the masking pack. |

### RWB-P7-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05452 | RWB-P3-E1018-OPS | GAP-2437 | find it | Record that the secondary slice builds against the platform contracts and the fakes of section 12.8 and reads the same service's wave-1 tables in its own schema; no dependency row moves. |

### OTHER:ASM-B-P1-07-E1018-2 in the assumptions register and the published rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05453 | RWB-P3-E1018-OPS | GAP-0572 | find it | Fix one operation for the business date, paged by page and size, with default and maximum page size set in the published contract; refuse a per-account read as fan-out under DP-11. |

### OTHER:Platform deployment topology document for rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05454 | RWB-P3-E1018-OPS | GAP-0677 | find it | Publish the rwb-case cluster names, node pools, replica counts, resources, zone spread, ingress class and probe paths and timings as values files outside the chart defaults. |

### OTHER:RWB-PLT-DB story and the secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05456 | RWB-P3-E1018-OPS | GAP-2438 | find it | Fix the rwb-decision database login name, keep the migration and application roles apart, and reference the login from every P7 story. |

### OTHER:rwb-access OpenAPI document (GET /me/session) and rwb-comms OpenAPI document (POST /cases/{caseId}/notices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05460 | RWB-P3-E1019-APP | GAP-0344 | none | Publish the team scope field and the queue and team code fields before wave 1 exit, or record them in the Service Contract Catalog. |

### OTHER:Test case register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05461 | RWB-P3-E1019-APP | GAP-1178 | 5 | Record that the load-path proof of legacy TC-E1-019-13 is owned by RWB-P3-E1019-APP; carry TC-E1-019-13 in RWB-P6-E1019-APP as the routing guard test. |

### OTHER:TSD P6 Communications v2, module API file (T-A.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05462 | RWB-P3-E1019-APP | GAP-1179 |  | Add the routing read GET /admin/notice-routing to the P6 API file with an allocated API identifier at the next module API revision. |

### OTHER:RWB-E1-065 seed (decision_log_entry seed rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05463 | RWB-P3-E1019-APP | GAP-2252 |  | Seeded creation record uses the decision code of RWB-P3-E1018-APP; seeded exclusion record uses the code of RWB-P3-E1019-APP or the exclusion rule. |

### OTHER:Technical Specification P4 (TSD P4) T3.1 and the approved role conflict list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05464 | RWB-P3-E1019-APP | GAP-1574 | find it | Publish the role conflict list with its version label and effective dates; add valid-from and valid-to to matrix version; confirm role and permission row counts of the version in force. |

### OTHER:Technical Specification P4 (TSD P4) T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05465 | RWB-P3-E1019-APP | GAP-1567 | find it | Drop lov_value and partner_user; keep lists of values in TSD P3 and partner identity in TSD S9; the rwb-access contract states which list versions and partner identity attributes it reads and how often. |

### OTHER:Technical Specification P4 (TSD P4) T3.1 and the approved role file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05467 | RWB-P3-E1019-APP | GAP-0985 | find it | Record role and permission row counts, role file layout, conflict version label, matrix effective-date column, full conflict list and MSG-P4-006 text, confirmed by the security administrator. |

### OTHER:Control register (CTL-08 register row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05469 | RWB-P3-E1019-APP | GAP-1180 | find it | Register CTL-08 with its text, owner and evidence, and cite the register row from the stories that apply it. |

### OTHER:rwb-access OpenAPI (GET /me/session); OTHER:rwb-comms OpenAPI (POST /cases/{caseId}/notices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05475 | RWB-P3-E1019-CON | GAP-0344 | none | Publish the team scope field and the queue and team code fields of the notice response, or record them in the Service Contract Catalog, before wave 1 exit. |

### OTHER:TSD P6 Communications v2 Appendix T-A (P6 API file) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05477 | RWB-P3-E1019-CON | GAP-1179 |  | Add the routing read GET /admin/notice-routing to the P6 API file with an allocated API identifier at the next module API revision; keep the shape fixed in RWB-P6-E1019-APP until then. |

### RWB-P4-AD003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05482 | RWB-P3-E1019-CON | GAP-0791 |  | Publish GET /api/recovery/access/v1/admin/role-scopes and PATCH /api/recovery/access/v1/admin/role-scopes/{roleCode}; carry the scope predicate on the authorise answer of RWB-P4-E1037-CON as scope, teamCode, regionCode and caseOwnerRef; carry LOV-SCOPE as the service's own list constraint. |

### OTHER:TSD P4 T3.1 and the role conflict source (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05485 | RWB-P3-E1019-CON | GAP-1574 | find it | Publish the approved role conflict list with its version label and dates; add matrix effective-date columns to T3.1 or state the date lives on the load; confirm role and permission row counts. |

### OTHER:rwb-access access owner (P4) to confirm the RW-TEAMMGR grant (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05487 | RWB-P3-E1019-CON | GAP-0683 approver authority for a queues load is assumed, not confirmed | 10 | Section 10 records the RW-TEAMMGR grant as rwb-access data to be recorded by the access owner; refusal stays 403 MSG-P4-002. |

### OTHER:TSD P4 T3.1 and the approved role file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05488 | RWB-P3-E1019-CON | GAP-0985 | find it | Confirm with the security administrator the role file layout, row counts, conflict label, matrix date column, full conflict list and MSG-P4-006 text before the role version is frozen. |

### OTHER:Service template (Template and Rules) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05489 | RWB-P3-E1019-CON | GAP-1177 | 3 | State the reference-reader caching rule: a reader caches for one call only; a longer-lived cache is an owner contract with a version and an invalidation event. |

### OTHER:Control register (CTL-08 entry; OTHER:not in the source set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05490 | RWB-P3-E1019-CON | GAP-1180 | all | Register CTL-08 with its text, owner and evidence, then cite the register row from the stories that apply it (legacy, case and primary P3 slice). |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05497 | RWB-P3-E1019-DB | DOR-RWB-P3-E1019-DB-12 | 16, 18 | Register TC-P3-E1019-DB-01 to TC-P3-E1019-DB-07 in Test Cases v8; align RTM v7 test lists for REQ-CWC-006 and REQ-ACA-002 to section 18. |

### OTHER:rwb-access OpenAPI document (GET /me/session); OTHER:rwb-comms OpenAPI document (notice response) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05498 | RWB-P3-E1019-DB | GAP-0344 | find it | Publish the team scope field for GET /me/session and the queue and team code fields for the notice response before wave 1 exit, or record them in the Service Contract Catalog. |

### OTHER:rwb-case contract (later rwb-case contract story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05500 | RWB-P3-E1019-DB | GAP-0682 | 5, 12 | Publish POST /admin/reference-loads/{loadId}/rollback and .../verify as rwb-case operations in a later contract story. |

### RWB-P3-E1019-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05501 | RWB-P3-E1019-DB | GAP-1176 | find it | State that queue, team code, role code and version are read from P3 and role, rights and scope from P4; publish or withdraw a membership operation on P3. |

### OTHER:TSD P6 Communications v2 T-A.1 (P6 API file) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05503 | RWB-P3-E1019-DB | GAP-1179 | find it | Add the routing read GET /admin/notice-routing to the P6 API file with an allocated API identifier when the module API is next revised. |

### OTHER:RWB-E1-019 legacy build notes (reference-load story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05504 | RWB-P3-E1019-DB | GAP-3159 | find it | Load role in P4 and read it in P3 by contract; keep teams, queues and reference rows in P3. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx; OTHER:ACE DB work type) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05506 | RWB-P3-E1019-DB | GAP-3194 | find it | Raise one ACE DB column-drop story each for S2, S4, S5, S6, S7, P6 and P8, or attach the drop to their APP stories, and cite the chosen IDs on row 121 before wave 2. |

### RWB-P3-E1019-DB; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05508 | RWB-P3-E1019-DB | CG-ALL-3508 | 18 | Align the test lists for REQ-CWC-006 and REQ-ACA-002 so the RTM and section 18 name the same TC IDs. |

### OTHER:Recovery Workbench rwb-access story RWB-AD-014 (legacy) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05509 | RWB-P3-E1019-DB | GAP-0857 | find it | Replace the rule-version endpoints row with this story's two operations; read the RWB-E1-019 dependency as RWB-P3-E1019-APP and RWB-P3-E1019-CON. |

### OTHER:TSD P4 T3.1 and the approved role conflict list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05510 | RWB-P3-E1019-DB | GAP-1574 | find it | Publish the approved role conflict list with its version label and effective dates; add matrix-version effective-date columns or state where the date lives; confirm the role and permission row counts. |

### OTHER:TSD P4 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05511 | RWB-P3-E1019-DB | GAP-1567 | find it | Drop lov_value and partner_user from TSD P4 T3.1; keep lists of values in TSD P3 and partner identity in TSD S9; define in the rwb-access contract which list versions and partner attributes it reads and how often. |

### OTHER:Recovery Workbench TSD P4 and the approved role file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05513 | RWB-P3-E1019-DB | GAP-0985 | find it | Confirm with the security administrator the approved role file layout, role and permission row counts, conflict version label, matrix effective-date column, full conflict list and MSG-P4-006 text. |

### OTHER:Service template (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05514 | RWB-P3-E1019-DB | GAP-1177 | find it | State the caching rule for reference readers: a reader caches for one call only; a longer-lived cache is an owner contract with a version and an invalidation event. |

### OTHER:Control register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05515 | RWB-P3-E1019-DB | GAP-1180 | find it | Register CTL-08 with its text, owner and evidence, then cite the register row from the stories that apply it. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05516 | RWB-P3-E1020-APP | CG-ALL-3515 | 13 | Create story RWB-P7-E1073-CON, or the solution architect names the existing story that covers this contract dependency. |

### OTHER:Recovery Workbench decision register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05521 | RWB-P3-E1020-APP | DOR-RWB-P3-E1020-APP-18 | 14 | Carry open decisions DL10, DL11, DL15, DL22 and DL23 each with its assumptions: DL10 ASM-2250, ASM-2357, ASM-2377, ASM-2863; DL11 ASM-0553, ASM-0703, ASM-1051, ASM-1104; DL15 ASM-5264; DL22 ASM-1162, ASM-1304, ASM-2217, ASM-2569; DL23 ASM-1232, ASM-1237, ASM-1259, ASM-1560 |

### OTHER:Epic 1 Business Requirements Document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05523 | RWB-P3-E1020-APP | GAP-1456 | 8 | State in section 8.2 that Epic 1 stories keep the business-epic wave and the delivery lead confirms the wave per story at build sequencing |

### OTHER:ACE database schema and login allocation (ACE team; OTHER:DBA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05525 | RWB-P3-E1020-APP | GAP-1456 | 12.7 | Login marked Not specified (GAP-0684) in section 12.7 |

### OTHER:Work package C-WEX (work package index) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05533 | RWB-P3-E1020-APP | GAP-3206 |  | Correct heading '(E1-018)' to legacy story RWB-E1-020 at the next run; the scheduling-label reading is applied here. |

### RWB-P3-E1020-OPS; 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05535 | RWB-P3-E1020-APP | GAP-0687 |  | Expose replicas, autoscaling bounds, node pool, connection pool size and history archive as chart values with documented defaults; record SIT findings. |

### OTHER:FSD P4 A2.4 and TSD P4 T6.1 (permission matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05536 | RWB-P3-E1020-APP | GAP-0987 |  | Confirm PM-2026.11 in force at 30 Nov 2026, PM-2026.12 from 2026-12-01, and the roster: RW-TEAMMGR and RW-CAPACITY R TEAM; RW-CASEOWN R OWN; RW-AUDIT R ALL; SY-CASEWF CRU; SY-RULES R; RW-REFADM none; RW-PLATADM U. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05540 | RWB-P3-E1020-APP | GAP-3173 | Header | State wave 1 delivery of rwb-deviation in the service epic and wave plan; rwb-deviation service wave governs its later stories (Arch v5 slide 41 wave 2). |

### OTHER:Template and Rules (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05541 | RWB-P3-E1020-APP | GAP-2150 | 1 | Keep RWB-E1-020 word for word and add RWB-P3-E1042-CON as the worked example of section 2 including the published contract; microservice example stands beside it. |

### RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05542 | RWB-P3-E1020-CON | CG-ALL-3531 | 13 | Create the missing story file RWB-P7-E1073-CON, the rwb-decision rule-model contract that section 13 DP-04 names as contract dependency C; no other key for that capability appears in the sources. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:L371) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05543 | RWB-P3-E1020-CON | CG-ALL-3539 | 3 | Rule the Java package segment for rwb-case so it is not the Java reserved word 'case'; row P3 L371 currently gives th.co.scb.ace.workbench.recovery.case, and the story section 3 copies the ruled name. |

### OTHER:P2 personal-data field classification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05544 | RWB-P3-E1020-CON | DOR-RWB-P3-E1020-CON-11 | 11 | Reclassify the P2 fields marked as personal data so they agree with section 11, which states the contract carries no personal data |

### OTHER:TSD S8 (T5.2.1; RWB-S8-E1020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05549 | RWB-P3-E1020-CON | GAP-3072 | 12 | Publish the case input and stage outcome element names, the queue-and-members element, the handler choice by fewest open deviations, the DEV-HANDLER parameter row, and confirm the four handler role codes. |

### OTHER:RWB-PLT-DB stories and the rwb-case DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05550 | RWB-P3-E1020-CON | GAP-3207 | 12 | Publish the per-service rwb-case login there; this story keeps the placeholder. The caseload cap stays as data on queue.capacity_cap and queue_member.capacity, with the default delivered through the parameter contract. |

### RWB-PLT-E1072-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05553 | RWB-P3-E1020-CON | GAP-2439 | 11 | Take the rule_package_version columns at implementation; keep state, valid-from, approver, DRL and checksum as the minimum; confirm the artifact payload with the embedded Drools kit. |

### OTHER:Work package index (E1-018 label) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05556 | RWB-P3-E1020-CON | GAP-3206 | find it | No story text changed and the (E1-018) heading correction belongs to the work package index, so the fix is cross-document. |

### OTHER:Build Notes v6 (service epic and wave plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05562 | RWB-P3-E1020-CON | GAP-3173 | find it | State the wave 1 delivery of rwb-deviation in the service epic and wave plan, and let the rwb-deviation service wave govern its later stories. |

### OTHER:Screen specification for SCR-02 and SCR-09 (CG-ALL-3546; OTHER:CG-ALL-3547) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05568 | RWB-P3-E1020-OPS | DOR-RWB-P3-E1020-OPS-10 | 15 | Define the error state and the no access state of SCR-02, and the empty state, the error state and the no access state of SCR-09. |

### OTHER:BRD, section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05569 | RWB-P3-E1020-OPS | GAP-1456 | find it | State the wave rule in section 8.2: business-epic wave kept, service wave applies to its own epic, Template R5.6 retained; delivery lead confirms wave per story at build sequencing. |

### RWB-P3-E1020-CON; parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05573 | RWB-P3-E1020-OPS | GAP-3072 | find it | Publish case element and stage outcome field names; publish queue and members element; add DEV-HANDLER parameter key; confirm four handler role codes against TSD S8 T6.1. |

### OTHER:Screen specification for SCR-02 (CG-ALL-3546) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05579 | RWB-P3-E1020-OPS | CG-ALL-3546 | 15 | SCR-02 states marked Not specified in the source documents |

### OTHER:Screen specification for SCR-09 (CG-ALL-3547) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05580 | RWB-P3-E1020-OPS | CG-ALL-3547 | 15 | SCR-09 states marked Not specified in the source documents |

### OTHER:Work package C-WEX heading (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05581 | RWB-P3-E1020-OPS | GAP-3206 |  | Correct the (E1-018) heading to the scheduling reading; RWB-E1-020 stays the subject of the worked example. |

### OTHER:FSD P4 A2.4 and A2.14; OTHER:TSD P4 T6.1 (permission matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05583 | RWB-P3-E1020-OPS | GAP-0987 | n/a | Fix authorise attributes (area, right, team code, business date for summary read; case ID, team, owner reference for case read). State PM-2026.11 in force at 30 Nov 2026 and PM-2026.12 from 2026-12-01. Add the role roster: RW-TEAMMGR and RW-CAPACITY R TEAM; RW-CASEOWN R OWN; RW-AUDIT R ALL; SY-CASEWF CRU; SY-RULES R; RW-REFADM none; RW-PLATADM U for rerun. |

### OTHER:ALLOCATION reference data package ALLOC-2026.11 (row load) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05584 | RWB-P3-E1020-OPS | GAP-2440 | n/a | Load the row once with the rule ID the workbook carries, and record the other label as the row description. |

### OTHER:P7 message catalogue (FSD P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05585 | RWB-P3-E1020-OPS | GAP-2442 | n/a | Approve the texts of MSG-P7-009 and the chain-break warning with the P7 message catalogue; reuse the approved wording. |

### OTHER:Build Notes v6; 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05587 | RWB-P3-E1020-OPS | GAP-3173 | n/a | State the wave 1 delivery of rwb-deviation in the service epic and wave plan, and let the rwb-deviation service wave govern its later stories. |

### OTHER:Template and Rules (worked example, section 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05588 | RWB-P3-E1020-OPS | GAP-2150 | 1 | Keep RWB-E1-020 as the worked example and add RWB-P3-E1042-CON beside it as the microservice example of section 2. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:P3 row rwb-case; OTHER:Java package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05590 | RWB-P3-E1021-APP | CG-ALL-3560 | 1, 13 | Rule the package segment for the P3 row rwb-case so the Java package no longer uses the reserved word 'case', and publish the ruled package; the story copies it in sections 1 and 13. |

### RWB-P3-E1020-APP; RWB-P3-E1021-OPS; RWB-P3-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05592 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-17 | 13 | Bring the three open build dependencies to Done before this story starts. The non-existent dependency is fixed in section 13. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05597 | RWB-P3-E1021-APP | DOR-RWB-P3-E1021-APP-8 | find it | Make transferReasonCode read LOV-TRANSFER-REASON; align CaseTransferred and CaseStateChanged payloads; add rwb-case consumers for CaseStateChanged and ApprovalRequested. |

### RWB-P3-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05604 | RWB-P3-E1021-APP | GAP-3075 | 3 | Keep the H list empty and C as RWB-P3-E1021-CON; record the eight H and two C rows as DP pattern application; platform owner confirms published baselines. |

### RWB-P4-E1037-CON; OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05607 | RWB-P3-E1021-APP | GAP-0990 | find it | Publish the authorise request and answer schema with the legalHold attribute; confirm the matrix version label in force at 30 November 2026 with the matrix owner; tabulate Queue and allocation letters in T6.1. |

### OTHER:Platform team chart values for rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05608 | RWB-P3-E1021-APP | GAP-0691 | find it | Publish cluster, node pool, replica counts per environment, ingress host, resource limits and pod disruption budget as chart values; no environment default shipped. |

### OTHER:P5 contract baseline story for rwb.document.events.v1 (AsyncAPI 3.0 and JSON Schema registry) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05609 | RWB-P3-E1021-APP | GAP-1036 | find it | Publish the AsyncAPI 3.0 document and registered schemas for rwb.document.DocumentStored.v1 and DocumentFieldsExtracted.v1 with required fields and BACKWARD rule; hand DocumentStored schema to RWB-P3-E1021-CON. |

### OTHER:BRD (section 8.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05616 | RWB-P3-E1021-CON | GAP-1456 | find it | State in section 8.2 that Epic 1 stories keep wave 1 when their service starts in wave 2 (rwb-payment, rwb-asset, rwb-deviation), per Template and Rules R5.6. |

### OTHER:Owner service API documents (rwb-source-data, rwb-case, rwb-access, rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05617 | RWB-P3-E1021-CON | GAP-3076 | find it | Each owner publishes the operation name of its consumed row before the release date; placeholders replaced in a minor contract version. |

### OTHER:Solution architecture decision (S8 and P3 transfer evaluation split) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05618 | RWB-P3-E1021-CON | GAP-3077 | find it | Confirm deviation triggers are evaluated in S8 against the P7 package in force; manual and case-trigger paths stay in P3; one package, one version. |

### OTHER:S8 database story (table deviation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05620 | RWB-P3-E1021-CON | GAP-3080 | find it | If audit read per deviation row is required, add rule_id and rule_version columns to deviation; otherwise decision record stays the transfer record. |

### RWB-S8-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05621 | RWB-P3-E1021-CON | GAP-3075 | find it | Add the eight platform H rows and two C rows from the applied DP table when the plan is reissued; metadata here stays as copied from the plan. |

### OTHER:Platform team chart values for rwb-case api and worker deployments (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05626 | RWB-P3-E1021-CON | GAP-0691 | find it | Publish cluster, node pool, replica counts per environment, ingress host, resource limits and pod disruption budget as chart values; no environment default; two-replica start is a proposal. |

### OTHER:P5 contract baseline story for rwb.document.events.v1 or the rwb-document deployment story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05627 | RWB-P3-E1021-CON | GAP-1036 | find it | Publish the AsyncAPI 3.0 document of rwb.document.events.v1 with the registered JSON schemas for DocumentStored.v1 and DocumentFieldsExtracted.v1, their required fields and the BACKWARD rule; hand the DocumentStored schema to RWB-P3-E1021-CON as the trigger fixture. |

### OTHER:Business epic wave placement (BRD wave rule) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05628 | RWB-P3-E1021-CON | GAP-3074 | find it | The business epic places the story in wave 1 while the service sits in wave 2; the story keeps wave 1 and the rule belongs in the BRD, as in R-21907. |

### 04 User stories/Recovery Workbench ACE Team Stories v2.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20610 | RWB-P3-E1020-APP | R-22001 |  | Section 12.7 has no login entry and no GAP-0684 marker. Section 12.7 and rows 464 and 473 already place the rwb_source_data login with RWB-P1-E1069-DB. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_deviation.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20625 | RWB-P3-E1021-CON | R-22014 |  | No rule_id or rule_version column in table deviation (rwb_deviation.sql lines 98-153). Audit need not stated; the transfer record stays as is. Case-side rule label stays with rwb-case (P3). |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20863 | RWB-P3-E1021-CON | R-28532 |  | Cluster, replica, ingress and PDB chart values belong to the platform team chart. Values Not specified in the source documents (GAP-0691). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0064 | Wave conflict S8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0344 | Field names of the P4 session team scope and the P6 notice queue code are not fixed by any source | Service owner of rwb-access and service owner of rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0345 | JOB-03 run surface and exact rerun facade are not specified for an ITG suite | Service owner of rwb-case with the service owner of rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0346 | Route-decided transfer trigger has no wave 1 owner event | Tech lead | Resolved (directive) |
| GAP-0571 | The entry-candidate contract: the resource and parameter names, the response entity, its field names, the paging, the error status set and the access rule are not fixed by any source, and this legacy key has no contract story of its own | Tech lead of rwb-source-data with the solution architect and the P3 owner of the case contract | Resolved (directive) |
| GAP-0572 | Whether the entry read is one operation for a business date or one operation per account, and how a page of about 28,100 candidates is cut, are not specified | Tech lead of rwb-source-data with the owner of the rwb-case case creation job | Resolved (directive) |
| GAP-0573 | Which service writes account_ext.dispute_open and the party_ext flags, which right the confirmation needs, and where party_ext.vulnerable comes from on the first write are not settled | Solution architect with the P1 service owner, the P3 owner of the exclusion screen and the P4 owner of the role model | Resolved (directive) |
| GAP-0574 | The ALS batch gate before RWB-ACE-001 lands: v_ace_batch_status is a Section B view, and the behaviour of an entry read for a date whose batch record does not exist yet is not specified | Recovery tech lead with the ACE team lead and the platform team that owns the RWB-ACE-001 sequence | Resolved (directive) |
| GAP-0575 | The shape and the home of the REC-05 break list are not specified, and the table that held it leaves the schema | Data architect with the data steward and the P1 owner of the reconciliation job | Resolved (directive) |
| GAP-0576 | The product group of a candidate row: whether the ACE product_category value is passed through or mapped to the LOV-PRODUCT codes, and what happens to a value outside the list, is not specified | Business analyst, P1 with the center of excellence and the owner of the rwb-case reference data | Resolved (directive) |
| GAP-0670 | rwb-integration queue-write adapter: the operation owner, the login, the consumed contract field names and the replay window are not fixed by one source | Solution architect | Resolved (directive) |
| GAP-0671 | rwb-integration queue-write adapter contract: the ownership of the placement path, the consumed contract shapes and the library table columns are not fixed by one source | Tech lead | Resolved (directive) |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0675 | Per-service login name for rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0676 | Field-level OpenAPI schema of the case resource is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0677 | Deployment topology detail for rwb-case is not specified | DevOps engineer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0678 | The per-service database login name of rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0679 | The column-level split of the legacy role and permission tables between rwb-case and rwb-access is not defined | Solution architect | Resolved (directive) |
| GAP-0680 | The column-level definition of queue measures and of the remaining list-of-values columns is not specified | Technical lead, rwb-case | Resolved (directive) |
| GAP-0681 | The queues reference-load template format is not specified | Reference data owner (Shared operations) | Resolved (directive) |
| GAP-0682 | The rollback and verify operations of reference loads sit outside the rwb-case operation set given for this legacy key | Solution architect | Resolved (directive) |
| GAP-0683 | The approver authority for a queues load is assumed, not confirmed | Access owner, rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0684 | The rwb-case service login name is not given in any source | ACE team, DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0687 | The deployment topology of the rwb-case allocation worker is not specified | Platform team; DevOps | Resolved (directive) |
| GAP-0688 | Per-service database login name for rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0691 | Deployment topology of the transfer capability is not specified | Platform team | Resolved (directive) |
| GAP-0697 | The column definitions of each reference table code and the element types of the reference resources have no source field by field | Data steward | Resolved (directive) |
| GAP-0775 | The home of the resolved session labels, the target of the conflict incident and the team and region read behind the scope line are not specified for the sign-on app slice | rwb-access service owner with the architecture review | Resolved (directive) |
| GAP-0791 | The two scope operation paths, the scope predicate fields and the home of the LOV-SCOPE list are not specified for the scope app slice | rwb-access service owner with the contract owner and the architecture review | Resolved (directive) |
| GAP-0857 | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Business analyst, P4 | Resolved (directive) |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0985 | Role version: roster, row counts, role-file layout, matrix effective date, conflict list and MSG-P4-006 text not specified | Security administrator (RW-SECADM), with the reference data administrator (RW-REFADM) | Resolved (directive) |
| GAP-0987 | Authority attributes, matrix version label and role roster for an allocation and queue read | Solution architect of rwb-access | Resolved (directive) |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1036 | Producer-side AsyncAPI and JSON schema of rwb.document.events.v1 are not assigned to a contract story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1038 | The rwb-document login name, the not-found message ID of the case read and the case-read field names are not specified | Solution architect with the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1175 | DP-08 is claimed while the authorise contract and the guard library are in no dependency list | Solution architect | Resolved (directive) |
| GAP-1176 | The split of the legacy role, queue and membership data between rwb-case and rwb-access is not stated, and the membership read has no published operation | Solution architect | Resolved (directive) |
| GAP-1177 | No source decides whether a reader keeps a local cache of the role and queue data | Solution architect | Resolved (directive) |
| GAP-1178 | The legacy reference-load path has no rwb-comms target, so the legacy access case has no endpoint in this service | Test lead | Resolved (directive) |
| GAP-1179 | The P6 API specification has no operation that exposes the approver role and the approver queue of a notice | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1180 | Control CTL-08 is cited by the legacy story and the case story but is absent from the rules register | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-2150 | The worked example is a monolith story key with no service and no realignment equivalent | Document owner; analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2252 | The decision code and the payload of the decision records the seed writes are not in the sources | TechX and the rwb-decision contract owner | Resolved (directive) |
| GAP-2273 | The queue-file check surface, the last two queue columns, the member sheet, the cap limit key, the finding codes, the right of the load and the decision code are not specified in the sources | Solution architect | Resolved (directive) |
| GAP-2433 | The message text of MSG-P7-009 and of the chain warning MSG-P7-012 is named in the sources but never written | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2435 | TSD P7 still models decision_log_entry.case_id as a uuid with a relationship to recovery_case and gives the row no business-date column | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2436 | The literal rule ID of the ENTER rule of package ENTRY is named in no source | Business analyst, Epic 1 | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2438 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2439 | The physical columns of rule_package_version and the payload a compiled package is served in are not in the sources | TechX and the P7 solution architect | Resolved (directive) |
| GAP-2440 | The rule ID of the same allocation row is ALLOC-014 in the legacy story and ALLOC-MTG-BKK-01 in the FSD | P7 business analyst and the reference data administrator | Resolved (directive) |
| GAP-2441 | How the business date, the queue identifier and the owner identifier travel in the decision record is not in the sources | P7 and P3 contract owners | Resolved (directive) |
| GAP-2442 | The text of MSG-P7-009, the text of the chain-break warning and the field name of the per-entry chain result are not in the sources | P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2443 | No provided operation of the Ownership Map serves a compiled rule package version to the owning service | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3072 | RWB-S8-E1020-APP: the allocation-to-deviation boundary, the handler roster, the assignment method and any handler cap have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3073 | RWB-S8-E1020-APP: the key has no contract story of its own, the event names are taken from the TSD, and the business wave is earlier than the service wave | Programme lead and solution architect | Resolved (directive) |
| GAP-3074 | The business epic places the story in wave 1 while the service sits in wave 2 | Programme planner with the S8 service owner | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3076 | No source publishes the operation names of the six rows this slice consumes | P1 rwb-source-data owner, P3 rwb-case owner, P4 rwb-access owner, P7 rwb-decision owner and the S8 service owner | Resolved (directive) |
| GAP-3077 | No source says which service hosts the TRANSFER package evaluation after the split | Solution architect with the S8 service owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-3079 | The event names of the P3 and P1 subscriptions are not published | P3 rwb-case owner, P1 rwb-source-data owner and the S8 service owner | Resolved (directive) |
| GAP-3080 | No source fixes where this slice records the rule ID and the package version of a transfer | S8 service owner with the data steward of module S8 and the P3 rwb-case owner | Resolved (directive) |
| GAP-3159 | The role table is loaded by P3 in the story and owned by P4 in the Ownership Map | P4 access owner | Resolved (directive) |
| GAP-3162 | The case story writes the P1 extension tables | P3 case owner | Resolved (directive) |
| GAP-3173 | Service S8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3207 | No source names the rwb-case database login or where the caseload cap is stored | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3208 | The schedule expression of the DailyCaseRun (legacy JOB-03) is not stated by any source | Solution architect | Resolved (directive) |
| GAP-3209 | No single source divides the thirteen legacy criteria of RWB-E1-020 across its seven stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
