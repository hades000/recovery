# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 12 of 12 (RWB-P3-E5002-APP to RWB-P3-E6025-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 3 |
| Resolved in the stories | 49 |
| Cross-document (pending in another document) | 47 |
| Not applied (value not in the sources) | 18 |
| Open business decisions | 10 |
| Register gaps linked | 31 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E5002-APP | 22 | 26 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E5002 APP Record proof of delivery on a notice v2.md |
| RWB-P3-E6017-APP | 13 | 9 | 9 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E6017 APP Route the population to the committee and schedule it v2.md |
| RWB-P3-E6025-APP | 14 | 11 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E6025 APP Close the case after the retention period v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E6025-ITG, RWB-P3-E6025-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-09218 | GAP-1475 | Register gap | Compliance and PDPA officer | Retention periods and masking rules by record class and role are not set | Hold a retention class and a masking rule per record class and role as versioned reference data, apply the class at creation, and record every disposal as a decision so a period that is not yet set cannot be breached silently. |
| RWB-P3-E5002-APP | R-10510 | CG-ALL-4476 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E6017-APP | R-10517 | CG-ALL-4492 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E6025-APP | R-10523 | CG-ALL-4505 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E5002-ITG, RWB-P3-E5002-APP, RWB-P6-E5002-APP, RWB-S4-E5002-APP, RWB-S4-E5002-CON | R-22803 | GAP-2746 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case architect and the business owner of the notice period | The notice-period timer has no stated home and the notice period has no value in any source | Declare the proof window of 7 days and the notice period as two durable timers of LitigationWorkflow, the first started at dispatch and the second at delivered_at under R-LIT-07; read the notice period as a versioned reference row per product and notice type, carry its content as the placeholder until the business owner publishes it, hold the timer and answer no move when the row is missing, and keep the case-stage timer and the officer task rows with rwb-case on the stage outcome. |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-ITG-E6025-ITG, RWB-P3-E6025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28908 | GAP-1808 | Register gap | Compliance and PDPA officer | The case closes after a retention period that is not set, and the retention class behind a closure is not defined | Hold the closure on a retention class and a recorded period, make the period a versioned data row, and take the periods and the class list as an open question under DL26 and Q-012; no period is asserted here. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E5002-APP | R-01032 | CG-ALL-4477 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | No package segment ruling in any source read (searched 22 Microservice Realignment and Architecture v5 extract). No name invented; the story is unchanged. |
| RWB-P3-E5002-APP | R-01033 | CG-ALL-4478 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.noticedelivery uses the reserved word 'case' | Same as CG-ALL-4477: no segment ruling in sources, so no name invented. The story is unchanged. |
| RWB-P3-E5002-APP | R-10508 | CG-ALL-4474 | 4, 14 | MSG-P3-027 text differs from the Error and Message Standard v4 | Standard wording is not in the sources read, so the wording change could not be confirmed. BA to confirm; no new ID raised. |
| RWB-P3-E5002-APP | R-25198 | CG-ALL-4479 | 13 | Flyway file V5002_1__notice_delivery.sql is not in the V0001..Vnnnn form | The rwb-case next Flyway number is not in any source. V0004 in Data Migration Stories v4 is another service's proposal, so it is not used. No edit. |
| RWB-P3-E6017-APP | R-01035 | CG-ALL-4486 | not in chunk | rwb-case.yaml holds timerType as a closed enum while the story reads LOV-TIMER as data | Ruling is closed list (Reference Data v5, LOV-TIMER), so the story's data sentence must change. That sentence is not in this chunk; no anchor, no edit. Re-run with it. |
| RWB-P3-E6017-APP | R-01037 | CG-ALL-4493 | 4 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Template rule gives the segment 'case' (Service Template Spec v1 s4; Service Catalog v1 line 65), a reserved word. No alternative segment in sources; package line 319 not in chunk. Architect must rule. |
| RWB-P3-E6017-APP | R-01038 | CG-ALL-4494 | 4 | Java package th.co.scb.ace.workbench.recovery.case.committeerouting uses the reserved word 'case' | Same cause as CG-ALL-4493: template segment 'case' is reserved (Service Template Spec v1 s4; Service Catalog v1 line 125). No alternative in sources; package line not in chunk. Architect must rule. |
| RWB-P3-E6017-APP | R-10513 | CG-ALL-4487 | 12.3 | Payload of rwb.case.CaseStateChanged.v1 differs from Kafka Catalog v1 | Kafka Catalog v1 EV-05 payload is not in the sources given, so the change cannot be verified. Lowercased fields broke the table style. |
| RWB-P3-E6017-APP | R-10515 | CG-ALL-4490 | 14 | MSG-P3-027 text differs from the Error and Message Standard v4 | Story use (no rule version in force) differs from MSG-P3-027 Raised when, so copying standard text changes meaning. BA must add a new message ID; none invented. Section 14 not edited. |
| RWB-P3-E6017-APP | R-16318 | DOR-RWB-P3-E6017-APP-11 | not in chunk | Definition of Ready item 11 Guardrails: Partial | Detcheck does not name the personal-data fields and no field list is in this chunk, so no field can be dropped or reclassed. Needs the field list. |
| RWB-P3-E6017-APP | R-16320 | DOR-RWB-P3-E6017-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in this chunk, so no AC or TC anchor exists and no covering ID can be written. Re-run with sections 7 and 16. |
| RWB-P3-E6017-APP | R-16322 | DOR-RWB-P3-E6017-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | Same as CG-ALL-4490: the routing-answer use needs a new message ID from the BA. Copying the standard text would change the meaning. Section 14 not edited. |
| RWB-P3-E6017-APP | R-30745 | NEWAC-RWB-P3-E6017-APP-AC9 | 7, 16 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so no anchor for AC9 or its test row. The proposed test is Not specified in the source documents. Needs test or guardrail placement from the architect or BA. |
| RWB-P3-E6025-APP | R-01041 | CG-ALL-4506 | 1 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Sources name only 'case' (Service Catalog v1 6.3; Service Template Spec v1 Java package rule). No replacement segment is in the sources. Needs Solution architect ruling. |
| RWB-P3-E6025-APP | R-05407 | DOR-RWB-P3-E6025-APP-8 | not in chunk | Definition of Ready item 8 Contract: Fail | Story rows for event names and payloads are outside this chunk. Authorise path depends on CG-ALL-4499 provider ruling, not in this chunk. |
| RWB-P3-E6025-APP | R-16323 | DOR-RWB-P3-E6025-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 SCR-27 text is outside this chunk, so the empty, loading, error and no-access states cannot be edited here. |
| RWB-P3-E6025-APP | R-16324 | DOR-RWB-P3-E6025-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Detcheck names no flagged field, and section 11 rows are outside this chunk. No personal-data field can be identified from the sources. |
| RWB-P3-E6025-APP | R-16327 | DOR-RWB-P3-E6025-APP-4 | 7 | Definition of Ready item 4 Business rules: Partial | Section 7 criteria and section 16 test cases are outside this chunk. BR1 to BR12 coverage rows cannot be added here; section 8 is in the chunk. |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07338 | RWB-P3-E5002-APP | DOR-RWB-P3-E5002-APP-7 | 11 | Add recovery_case fields notice_ref, proof_delivered_at and notice_outcome as the three new columns of migration V5002_1. |
| CDC-07340 | RWB-P3-E5002-APP | CG-ALL-4465 | find it | Record served_result as a dictionary field or entity, or name the S4 answer object that carries it. |
| CDC-07341 | RWB-P3-E5002-APP | CG-ALL-4466 | find it | Add proof_delivered_at as a recovery_case field (new column in migration V5002_1). |
| CDC-07342 | RWB-P3-E5002-APP | CG-ALL-4467 | find it | Add notice_outcome as a recovery_case field (new column in migration V5002_1), validated by the service against the outcome list. |
| CDC-07360 | RWB-P3-E6017-APP | CG-ALL-4483 | 4 | Add recovery_case field committee_meeting_ref (varchar(40)) or the Data owner names the dictionary field. |
| CDC-07361 | RWB-P3-E6017-APP | CG-ALL-4484 | 4 | Add recovery_case field committee_meeting_date (date) or the Data owner names the dictionary field. |
| CDC-07363 | RWB-P3-E6017-APP | DOR-RWB-P3-E6017-APP-7 | 11 | Add committee_meeting_ref and committee_meeting_date to recovery_case with field IDs, or record them as new fields with IDs. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07334 | RWB-P3-E5002-APP | CG-ALL-4469 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-07358 | RWB-P3-E6017-APP | CG-ALL-4485 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider CON story |
| CDC-07367 | RWB-P3-E6025-APP | CG-ALL-4499 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story (provider ruling), or the consumer switches to a published operation |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07344 | RWB-P3-E5002-APP | CG-ALL-4475 | 16 | Add rows TC-E5-002-01 to TC-E5-002-06 with Given, When and Then copied from the criteria they cover. |
| CDC-07362 | RWB-P3-E6017-APP | CG-ALL-4491 | 16 | Add rows TC-E6-017-01 to TC-E6-017-06 with Given, When and Then copied from the criteria they cover. |
| CDC-07372 | RWB-P3-E6025-APP | CG-ALL-4504 | 16 | Add rows TC-E6-025-01 to TC-E6-025-06 with Given, When and Then copied from the criterion each row covers, as listed in section 16 of RWB-P3-E6025-APP. |

### RWB-S7-E6025-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07369 | RWB-P3-E6025-APP | DOR-RWB-P3-E6025-APP-21 | header | Publish the contract so that this story's existing contract dependency is published |
| CDC-07370 | RWB-P3-E6025-APP | DOR-RWB-P3-E6025-APP-22 | 12.2 | Publish the contract fake library and record its version as published |
| CDC-07374 | RWB-P3-E6025-APP | GAP-3042 | - | Publish the baseline with placeholders, message-id bindings, timer and placement elements, closure state values, closing-entry element and versioned retention reference data |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07333 | RWB-P3-E5002-APP | CG-ALL-4468 | 12.2 | Declare the REST base /api/recovery/litigation/v1 as given in the Document Index service table. |
| CDC-07350 | RWB-P3-E5002-APP | GAP-1195 | 12.1 | Publish the write path /notices/{noticeId}/proof-of-delivery, its request and answer fields, Idempotency-Key rule and Litigation C right so edge, tests and S4 share one shape. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07335 | RWB-P3-E5002-APP | DOR-RWB-P3-E5002-APP-14 | Header | Record the signed epic design sign-off for this story. |
| CDC-07368 | RWB-P3-E6025-APP | DOR-RWB-P3-E6025-APP-14 | header | Record the signed epic design sign-off covering this story |

### RWB-S4-E5002-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07337 | RWB-P3-E5002-APP | DOR-RWB-P3-E5002-APP-22 | Header | Publish the contract fake library version and record it as published. |
| CDC-07349 | RWB-P3-E5002-APP | GAP-1189 | 12.1 | Name the proof-record operation with its request fields, answer fields, error envelope and no-response answer before the S4 client is built; agree shape at wave 3 contract review. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07343 | RWB-P3-E5002-APP | CG-ALL-4473 | 12.5 | Add activity EvaluateAndApply (task queue rwb-case, called by CaseWorkflow) to the Activities sheet. |
| CDC-07371 | RWB-P3-E6025-APP | CG-ALL-4503 | 12.5 | Workflows row CaseWorkflow: replace 'workflow ID = case ID' with workflow ID case-{caseId}, as in ADR-011 and RWB-P3-E6025-APP section 12.5. |

### RWB-S7-E6025-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07375 | RWB-P3-E6025-APP | GAP-0741 | - | Add a retention timer type row to LOV-TIMER; publish the two S7 operations and element names in RWB-S7-E6025-CON; confirm the SCR-27 field order at edge review |
| CDC-07376 | RWB-P3-E6025-APP | GAP-2227 | - | Add the retention timer type to LOV-TIMER; confirm the two S7 operations, their element names, the closure reason and the SCR-27 field order at contract and reference-data review |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07332 | RWB-P3-E5002-APP | CG-ALL-4464 | 13 | Index kept on notice_ref; no move to plan_ref |

### OTHER:Recovery Workbench story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07336 | RWB-P3-E5002-APP | DOR-RWB-P3-E5002-APP-21 | Header | Publish contract story RWB-P3-E5002-CON, or confirm RWB-S4-E5002-CON as the contract dependency. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07339 | RWB-P3-E5002-APP | DOR-RWB-P3-E5002-APP-8 | find it | Publish base path /api/recovery/litigation/v1 (fixed by RWB-S4-E5002-CON) and POST /api/recovery/access/v1/authorise in rwb-access; the 12.3 event type already matches the catalog. |

### OTHER:Functional specification P6 (FSD) document control change note v3 and AC-ALT-P6-001-01 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07345 | RWB-P3-E5002-APP | GAP-1597 | 8 | State that proof of delivery is read from the rwb-comms proof rows, not v_ace_pod; ACE team confirms who writes v_ace_pod and the WIN return path. |

### RWB-S4-E5002-CON; OTHER:rwb-comms contract baseline; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:reference-data rows; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07346 | RWB-P3-E5002-APP | GAP-0437 | 12 | Publish proof-record operation on RWB-S4-E5002-CON and notice proof write on rwb-comms baseline; add notice state and three notice facts to LDM with IDs; fix LOV-DELIVERY mapping and versioned reference rows; record appendix note; attach requirement ID to FEAT-LIT-02 in EP05 PRD. |

### OTHER:W3J01 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07347 | RWB-P3-E5002-APP | GAP-0436 | find it | Agree and record the wave 3 harness values (environment, seeded identifiers, business date, product codes, unnamed operations, evidence format, gate thresholds); none are in sources read, so Not specified in the source documents (GAP-0436). |

### RWB-S4-E5002-CON; OTHER:EP05 PRD (C1); OTHER:rwb-case reference data (SERVICE_LEVEL) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07348 | RWB-P3-E5002-APP | GAP-0737 | 12 | Confirm S4 and P6 owners; publish S4 delivery-outcome operation path and fields; add notice-period duration as SERVICE_LEVEL reference row owned by RW-COE; attach REQ identifier to the feature in EP05 PRD. |

### OTHER:rwb-source-data ACE-data contract; OTHER:rwb-comms notice contract; RWB-S4-E5002-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07351 | RWB-P3-E5002-APP | GAP-2744 | 12.1 | Record legacy sentences with origin tags and the target reading: proof via P1 contract (one hop, 2 s, faked); notice read via P6 contract; no business row written; no sixth S4 operation added. |

### OTHER:rwb-case contract story (case read and stage answer) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07352 | RWB-P3-E5002-APP | GAP-2745 | 9 | Read PROOF_OF_DELIVERY_RECEIVED, PROOF_WINDOW_EXPIRED and DELIVERY_FAILED as workflow signals, not Kafka subscriptions; proof via P1 contract and case stage via rwb-case contract, one hop, 2 s; neither publishes nor consumes an event. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07353 | RWB-P3-E5002-APP | GAP-2748 | 3 | Header row names the LITIGATION rule package contract of rwb-decision as a non-blocking consumed read, without a story key |

### OTHER:FSD P6 Communications v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07354 | RWB-P3-E5002-APP | GAP-1194 | 7 | Record in next FSD version that the officer-recorded path is the manual correction path of the same notice; keep the v_ace_pod read in RWB-P6-E2021-APP and RWB-P6-E1055-APP. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07355 | RWB-P3-E5002-APP | GAP-1191 | 12.2, 13 | Add DP-11 to the pattern set of RWB-E5-002 slices that consume or serve a contract at the next plan revision. |

### OTHER:Epics 3 to 8 PRD and FSD S4 requirements table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07356 | RWB-P3-E5002-APP | GAP-2747 | 18 | Add one requirement row covering the proof of delivery as the start of the notice period, then rewrite the requirement column of both stories and their fragments. |

### OTHER:split_plan.json and WP B-P6-04 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07357 | RWB-P3-E5002-APP | GAP-1190 | 3 | Add H RWB-PLT-E1027-CON and H RWB-PLT-N001-CON to this story's build list at the next plan regeneration. |

### OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07359 | RWB-P3-E6017-APP | DOR-RWB-P3-E6017-APP-8 | 4 | rwb-access publishes POST /api/recovery/access/v1/authorise; rwb-case.yaml holds timerType as an LOV-TIMER reference, not a closed enum. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07364 | RWB-P3-E6017-APP | GAP-1795 | find it | Publish the write-off collection operations under /api/recovery/writeoff/v1 (read, create proposal, submit pack to committee) with x-module S7; keep the two existing paths. |

### RWB-S7-E6017-CON; OTHER:TSD S7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07365 | RWB-P3-E6017-APP | GAP-3026 | find it | Publish the baseline with placeholders, bind each error to a section 14 message ID, publish queue and deviation elements, publish the 27-state list, settle the meeting-booking attribute, confirm operation names with the owners. |

### RWB-S7-E6017-APP; OTHER:pattern set; OTHER:context pack S7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07366 | RWB-P3-E6017-APP | GAP-3025 | find it | Keep H, C, I and X rows; record consumed rows as class C with placeholders; add RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and a meeting-calendar element as tracked dependencies; add a routing-step requirement row at the next revision. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:S7 row) and FSD S7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07373 | RWB-P3-E6025-APP | GAP-1797 | - | Add a P5 cell and a Temporal or REST path for S7 to the document hub, or record the call type as an open question with the P5 owner |

### RWB-S7-E6025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07377 | RWB-P3-E6025-APP | GAP-3041 | - | Keep the H, C, I and X rows; record consumed rows as class C with placeholders; record RWB-PLT-E1072-CON, RWB-P7-E1073-CON and RWB-PLT-TE006-CON as tracked dependencies |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20679 | RWB-P3-E5002-APP | R-22555 |  | Proof-record operation belongs to RWB-S4-E5002-CON; LDM, reference-data and EP05 PRD changes sit in their own documents (GAP-0437). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-0437 | The legacy delivery step is split across rwb-comms, rwb-litigation and rwb-case with no named hand-off operation and no named reference rows, so the end-to-end chain of RWB-E5-002 has no single source of record | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0455 | The committee routing harness pack, the committee queue code and the committee meeting calendar are not specified | Integration lead | Resolved (directive) |
| GAP-0457 | The retention period, the closure evidence pack and the synthetic clock for the retention close are not specified | Integration lead | Resolved (directive) |
| GAP-0737 | The split of the proof-of-delivery key between rwb-case, rwb-litigation and rwb-comms, the S4 answer, the notice-period duration and the requirement ID are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0738 | The committee routing of RWB-E6-017 crosses two services with no operation, no committee queue code, no meeting timer type and no requirement ID in the sources | Solution architect | Resolved (directive) |
| GAP-0741 | The case side of the retention closure leaves the retention period, the retention timer type, the S7 contract element names, the route-set state names, the closure reason and the screen field names unspecified | Tech lead, with the rwb-writeoff contract owner and the rwb-case reference-data owner (RW-COE) | Resolved (directive) |
| GAP-1189 | The proof-record operation of RWB-S4-E5002-CON is not named in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1190 | The platform contract rows that DP-03 and DP-19 add are not in this story's build list | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1191 | DP-11 is absent from the pattern set of a story that consumes one published operation | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1192 | The meaning of the two unexercised LOV-DELIVERY values, and the contract the list is read on, are not stated | Business analyst, P6 | Resolved (directive) |
| GAP-1193 | The labels AC1 to AC8 are reused by three documents of the same legacy key for different criteria | Business analyst, P6 | Resolved (directive) |
| GAP-1194 | The source reads the proof of delivery from v_ace_pod in process, and this story may read no ACE view | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1195 | The proof-record path, its fields and its right are this story's design, because no source names a proof-record operation | Solution architect | Resolved (directive) |
| GAP-1554 | Case closure is one requirement with rwb-writeoff and one case state change with rwb-case | Solution architect | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1740 | The notice and its proof of delivery sit in S4 in the FSD and in rwb-comms in Architecture v5 and the Ownership Map, and the three notice paths are split across the two services | Solution architect | Resolved (directive) |
| GAP-1741 | The notice capability is first needed in Epic 2 (wave 2, 31 December 2026 (tentative)) while the service is created in wave 3 | Solution architect | Resolved (directive) |
| GAP-1748 | The message wording and the Thai and English versions of the S4 messages are not in the FSD | Business analyst, S4 | Resolved (directive) |
| GAP-1795 | Slide 20 names write-off collection operations that neither the Ownership Map nor the API specification holds | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1797 | The committee pack is a document in the document hub, and the matrix connects S7 to P5 on no path | Solution architect with the P5 owner | Resolved (directive) |
| GAP-2227 | Retention period, retention timer type, S7 contract element names, closure reason value and screen field names of the retention closure are not stated in the sources | TechX, rwb-writeoff contract owner and rwb-case reference-data owner (RW-COE) | Resolved (directive) |
| GAP-2247 | The notice period is owned by two rwb-case stories of the same legacy loop | TechX | Resolved (directive) |
| GAP-2744 | The delivery fact has no home in rwb-litigation and no published operation on any of the three services it crosses | Solution architect, S4 rwb-litigation, with the P1 rwb-source-data and P6 rwb-comms architects | Resolved (directive) |
| GAP-2745 | The proof of delivery is named as an event in the rules and the FSD, while the service publishes and consumes nothing and the case answer has no operation name | Solution architect, S4 rwb-litigation, with the P3 rwb-case and P6 rwb-comms architects and the event platform team | Resolved (directive) |
| GAP-2747 | The legacy master carries no requirement identifier for RWB-E5-002, so both stories trace to the feature and one module requirement | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2748 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |
| GAP-3025 | RWB-S7-E6017-APP: the routing slice has no plan row for its five consumed contracts, its rule kit, its event library, its meeting calendar, the operation it provides or the requirement it serves | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3026 | RWB-S7-E6017-CON: the consumed operation names, the queue and deviation elements, the unprinted state values and the meeting-booking element have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3041 | RWB-S7-E6025-APP: the closure slice has no plan row for its five consumed contracts, its rule kit, its event library, its scheduler marker, the retention period, the placement record or the closing amounts | Solution architect | Resolved (directive) |
| GAP-3042 | RWB-S7-E6025-CON: the consumed operation names, the placement element, the retention period and class, the closing amounts and the two unprinted rule rows have no published baseline | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
