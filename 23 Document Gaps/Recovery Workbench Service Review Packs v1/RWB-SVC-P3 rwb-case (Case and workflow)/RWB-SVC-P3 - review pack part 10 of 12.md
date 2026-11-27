# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 10 of 12 (RWB-P3-E2024-APP to RWB-P3-E2042-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 166 |
| Cross-document (pending in another document) | 171 |
| Not applied (value not in the sources) | 45 |
| Open business decisions | 28 |
| Register gaps linked | 108 |
| Unconfirmed assumptions | 0 |
| Lint findings | 11 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E2024-APP | 17 | 21 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2024 APP Field app photos and bills into the document hub v2.md |
| RWB-P3-E2033-APP | 14 | 14 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2033 APP Case and queue list with status, owner and ageing v2.md |
| RWB-P3-E2034-APP | 20 | 18 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2034 APP Interaction ledger on the case and from every channel v2.md |
| RWB-P3-E2035-APP | 19 | 27 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2035 APP Next action on the case v2.md |
| RWB-P3-E2036-APP | 26 | 14 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2036 APP Queue write interface for models and agents v2.md |
| RWB-P3-E2041-APP | 23 | 20 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2041 APP Rule change governance and audit report v2.md |
| RWB-P3-E2041-CON | 23 | 24 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2041 CON Rule change governance and audit report - contract v2.md |
| RWB-P3-E2042-APP | 24 | 32 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2042 APP Epic 2 rule packages in Drools v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E2033-APP | R-00970 | CG-ALL-4290 | Script gap | Product owner | The story adds CAR to the closed list LOV-CASE-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-E2033-APP | R-00971 | CG-ALL-4291 | Script gap | Product owner | The story adds CAR to the closed list LOV-PRODUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-E2033-APP | R-10449 | CG-ALL-4301 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-P3-E2035-APP | R-10457 | CG-ALL-4324 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2035-APP | R-10458 | CG-ALL-4333 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-P3-E2036-APP | R-10465 | CG-ALL-4347 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2041-APP | R-10470 | CG-ALL-4364 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2042-APP | R-10478 | CG-ALL-4398 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2024-APP, RWB-P5-E2024-APP, RWB-P5-E2024-CON, RWB-P7-E2024-APP | R-22594 | GAP-0950 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masking rows and the mask version for the capture position are not specified | Record the DF-DOC-028 and DF-DOC-029 rows per role in the MASK-SIT-01 pack, with unmasked true for RW-CASEOWN and RW-RESTRUCT, false for RW-FIELDCOL and RW-PHONECOL and no row for SY-OCR, and let the platform masking library own one rendering per field type |
| RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2024-APP, RWB-P5-E2024-APP, RWB-P5-E2024-CON, RWB-P7-E2024-APP | R-22596 | GAP-1281 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P5 business analyst and the business owner | The field-capture decision record's payload, read shape, message id set, panel id, parameter names and login name have no source | At design time of wave 2 the solution architect, the data steward, the P5 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the capture columns of decision_log_entry (new columns or jsonb members), the object-reference filter of the read and the answer field set, the message ids and their texts, the panel id of the decision-log view, the parameter names and version labels of the ingest target and the chain check, and the per-service login name; until then the story holds the assumed shape of ASM-B-P7-03-E2024-1, ASM-B-P7-03-E2024-2 and ASM-B-P7-03-E2024-3 and its seven criteria stand on that shape |
| RWB-ITG-E2041-ITG, RWB-P3-E2041-APP, RWB-P3-E2041-CON, RWB-P4-E2041-APP, RWB-P7-E2041-APP | R-22719 | GAP-0963 | Register gap | Solution architect with internal audit | The record code and the field shape of a rule-change authority and of an audit export inside a decision-record entry are not specified | Carry the capability area, the right, the action, the version label, the author reference, the period, the package, the format, the row count and the matrix version in the actions list of the decision-record entry, reuse AC-READ, AC-DENY and AC-EXPT rather than minting a fourth code, and add the fields in the next LDM version with audit. |
| RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28853 | GAP-1560 | Register gap | AI product owner | The queue write interface for models and agents has no approved consumer and no flag removal date | Name the first approved consumer and the flag removal date before the wave 2 release. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-P3-E2033-APP | R-33437 | ASM-ALL-4301 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-P3-E2035-APP | R-33439 | ASM-ALL-4333 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-P3-E2042-APP | R-33442 | ASM-ALL-4398 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E2024-APP | R-00968 | CG-ALL-4283 | 1 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Catalog v1 line 65 and ADR v4 line 564 both give package ...recovery.case; no architect ruling or alternative segment in sources. Line 37 is blank, so no edit. |
| RWB-P3-E2024-APP | R-00969 | CG-ALL-4284 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.context uses the reserved word 'case' | Same package rule as CG-ALL-4283 (Catalog v1 line 65; ADR v4 line 564); no architect ruling for the context package. Line 337 is blank, so no edit. |
| RWB-P3-E2024-APP | R-16217 | DOR-RWB-P3-E2024-APP-10 | 9 and 10 | Definition of Ready item 10 Screens and states: Partial | Screen-state text for SCR-03, SCR-04 and SCR-30 is in sections 9 and 10, which are not in this chunk; cannot edit without that text. |
| RWB-P3-E2024-APP | R-16219 | DOR-RWB-P3-E2024-APP-15 | header | Definition of Ready item 15 INVEST: Partial | Fit within two weeks is a squad sizing judgement made at refinement, not in sources. The Size row marks it as not specified; no size is invented. |
| RWB-P3-E2024-APP | R-25130 | Test cases cover other criteria in Test Cases v8 | 16 | Test cases cover other criteria in Test Cases v8 | Test Cases v8 numbering is not in the sources. TC-02 to TC-15 keep their legacy AC covers. Needs a v8 mapping. |
| RWB-P3-E2024-APP | R-25132 | CG-ALL-4285 | 13 | Flyway file V2024_1__checklist_task.sql is not in the V0001..Vnnnn form | Migration file name is not in the chunk (line 371 is the DP-07 row). No next Vnnnn number for the rwb-case sequence in sources (ADR v4 ADR-021); no number invented. |
| RWB-P3-E2033-APP | R-00973 | CG-ALL-4298 | 1 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | The Solution architect's package segment ruling is not in the sources. Service Template Spec v2 gives 'case' with no reserved-word rule. No segment invented. |
| RWB-P3-E2033-APP | R-05302 | DOR-RWB-P3-E2033-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record or sign-off reference in the story or sources. Recording one would invent it. |
| RWB-P3-E2033-APP | R-05305 | DOR-RWB-P3-E2033-APP-22 |  | Definition of Ready item 22 Fake published: Fail | Contract Catalog v2 gives no published fake version, so a fake version cannot be written without inventing it. |
| RWB-P3-E2033-APP | R-16224 | DOR-RWB-P3-E2033-APP-15 |  | Definition of Ready item 15 INVEST: Partial | The Size row has no sizing data and nothing in the sources says Small fits two weeks. The fit cannot be written without invention. |
| RWB-P3-E2034-APP | R-00976 | CG-ALL-4308 |  | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | No Service Template Specification v1 naming ruling or replacement segment found in sources; package line is not in the supplied story text. Nothing invented. |
| RWB-P3-E2034-APP | R-00977 | CG-ALL-4309 |  | Java package th.co.scb.ace.workbench.recovery.case.timeline uses the reserved word 'case' | No architect ruling or replacement package segment in sources; package line is not in the supplied story text. Nothing invented. |
| RWB-P3-E2034-APP | R-05309 | DOR-RWB-P3-E2034-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or sources. Grep hits were only _work escalation scratch files, not sources. Sign-off cannot be confirmed. |
| RWB-P3-E2034-APP | R-10450 | CG-ALL-4304 | 12.1 | HTTP errors with no message ID: 503 the case store down. A slow ledger is not a 5xx here: the case events return with 200 and the missing source is named by the timeline contract (BR12). The operation is the Ownership Map's `GET /cases/{caseId}/timeline` (owner P3) on the rwb-case base, the re-based form of API-P3-003 of TSD P3 v3 T-A.1 | Error and Message Standard v4 MSG-GEN-006 is the only system-unavailable ID, but its text promises queuing and retry a read does not do. No fitting ID; 503 keeps placeholder. |
| RWB-P3-E2034-APP | R-22570 | GAP-2321 | 3 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Masking version label, covered field IDs, access-log granularity, parameter rows and login name are not in sources (PRD P4 rwb-access v1 Q-P4-11 still open). No value; no edit. |
| RWB-P3-E2034-APP | R-25142 | CG-ALL-4306 | 16 | Test cases cover other criteria in Test Cases v8 | Test Cases v8 is not in the sources. The new Covers values pointed at criteria with other content, so they were reverted. |
| RWB-P3-E2034-APP | R-25144 | CG-ALL-4310 | 12.7 | Flyway file V2016_1__timeline_indexes.sql is not in the V0001..Vnnnn form | Service Template Spec v1 gives only V0001 as baseline and no next free number. Migration line is not in the supplied story text; no number invented. |
| RWB-P3-E2035-APP | R-00981 | CG-ALL-4325 | 12.8 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | No replacement segment for 'case' in Service Template Specification v1 or Service Catalog v1. Needs Solution architect ruling; no value invented. |
| RWB-P3-E2035-APP | R-00982 | CG-ALL-4326 | 12.8 | Java package th.co.scb.ace.workbench.recovery.case.nextaction uses the reserved word 'case' | Same as CG-ALL-4325: no replacement segment for 'case' in the sources. The nextaction package depends on the Solution architect ruling; no value invented. |
| RWB-P3-E2035-APP | R-05315 | DOR-RWB-P3-E2035-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record or sign-off reference in the story or in 03 Requirements and specifications (Grep). No value to cite. |
| RWB-P3-E2035-APP | R-16235 | DOR-RWB-P3-E2035-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | The Screens section holding SCR-02, SCR-03 and SCR-09 is not in the chunk, so the empty, loading, error and no-access states cannot be placed. |
| RWB-P3-E2035-APP | R-16236 | DOR-RWB-P3-E2035-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The Guardrails section is not in the chunk, so the personal-data classes for the P2 fields cannot be placed. |
| RWB-P3-E2035-APP | R-16239 | DOR-RWB-P3-E2035-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR15 is in section 8, but the criterion in section 7 and the test row in section 16 are not in the chunk, so no exact old text exists to add them. |
| RWB-P3-E2035-APP | R-25150 | CG-ALL-4327 | 3 | Flyway file V2035_1__next_action.sql is not in the V0001..Vnnnn form | Next Vnnnn number of the rwb-case Flyway sequence is not in the sources (searched the folder; no value found). The filename line (RWB-P3-E2035-APP line 423) is outside the supplied story parts. |
| RWB-P3-E2036-APP | R-05322 | DOR-RWB-P3-E2036-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-SVC-P3 found in the source documents; sign-off cannot be confirmed from sources. Placeholder unchanged, no edit. |
| RWB-P3-E2036-APP | R-05326 | DOR-RWB-P3-E2036-APP-23 | 3 | Definition of Ready item 23 Contract version fixed: Fail | No contract version for RWB-P2-E2036-CON in the sources (22 Microservice Realignment, 05 Technical architecture). Header placeholder kept; no version invented. |
| RWB-P3-E2036-APP | R-10462 | CG-ALL-4342 | 4, 12.1 | HTTP errors with no message ID: 401 no valid session | Error and Message Standard v4 has no 401 or session message; MSG-GEN-006 does not fit a 401. No message ID invented; placeholder kept for business analyst. |
| RWB-P3-E2036-APP | R-16243 | DOR-RWB-P3-E2036-APP-11 | 3 | Definition of Ready item 11 Guardrails: Partial | Detail names no field, and the Data Classification class of the P2 fields is not in sources. No personal-data edit made. |
| RWB-P3-E2036-APP | R-25157 | CG-ALL-4350 | 3, 3.1 | Flyway file V2036_1__placement_index.sql is not in the V0001..Vnnnn form | Next free number of the rwb-case Flyway sequence is not in sources. Migration line is in section 13, outside this chunk. No edit made. |
| RWB-P3-E2041-APP | R-00995 | CG-ALL-4365 | 12.2 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment needs a solution architect ruling. Service Catalog v1 gives only 'case' (lines 65, 250); no alternative segment in sources. Not invented. |
| RWB-P3-E2041-APP | R-00996 | CG-ALL-4366 | 12.2 | Java package th.co.scb.ace.workbench.recovery.case.rulechangeaudit uses the reserved word 'case' | Same reserved-word segment 'case' as CG-ALL-4365. Package not in chunk text; no alternative in sources. Needs solution architect ruling. |
| RWB-P3-E2041-APP | R-05329 | DOR-RWB-P3-E2041-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in story or sources; sign-off is in the epic design record, which is not in this chunk. Not invented. |
| RWB-P3-E2041-APP | R-05333 | DOR-RWB-P3-E2041-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version in chunk or sources (searched). Owner must record the version. Not invented. |
| RWB-P3-E2041-APP | R-16248 | DOR-RWB-P3-E2041-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 text is not in this chunk, so SCR-39 empty, loading, error and no-access states cannot be placed without it. |
| RWB-P3-E2041-APP | R-16249 | DOR-RWB-P3-E2041-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | detcheck names no field; the personal-data fields are not in this chunk, so the guardrail cannot be corrected. |
| RWB-P3-E2041-APP | R-25163 | CG-ALL-4367 | 3 | Flyway file V2041_1__rule_change_audit_index.sql is not in the V0001..Vnnnn form | Next rwb_case V-number not in sources (checked Service Template Spec v1 6.4, ADR v4, TSD P3 v4). Migration line 367 is not in the chunk text, so no edit. |
| RWB-P3-E2041-CON | R-28856 | GAP-1302 |  | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Story text for the affected parts was not in the chunk and no story file matched. MSG-P3-015 text found in error standard v4 line 139, not applied here. |
| RWB-P3-E2042-APP | R-01006 | CG-ALL-4393 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | R4 (Story Template and Rules v1) sets the package to th.co.scb.ace.workbench.recovery.<short>, which yields 'case'. No replacement segment is in the sources. Solution architect must rule it. |
| RWB-P3-E2042-APP | R-01007 | CG-ALL-4394 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.rules.epic2 uses the reserved word 'case' | Same as CG-ALL-4393: R4 yields 'case' for the package and no replacement segment is in the sources. Solution architect must rule it; not invented. |
| RWB-P3-E2042-APP | R-05341 | DOR-RWB-P3-E2042-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record is in the story or the sources read. Sign-off must be confirmed from the epic design record; the value is not written here. |
| RWB-P3-E2042-APP | R-05343 | DOR-RWB-P3-E2042-APP-17 | 5 | Definition of Ready item 17 Dependencies: Fail | Three build dependencies are still open and cannot be cleared here. The dependency list lies outside this chunk. Missing RWB-P7-E1073-CON is tracked under CG-ALL-4388. |
| RWB-P3-E2042-APP | R-16264 | DOR-RWB-P3-E2042-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | DL24 answer (A, allocation, assignment and transfer only) is in open-decisions.csv, decision log v10. Section 18 text is not in this chunk, so the assumption is not written. |
| RWB-P3-E2042-APP | R-28865 | GAP-1298 |  | The decision code of a rule-governance entry is not named in any source this key may read | No LOV-DECISION value is in the sources read. Resolve from LOV-DECISION via DP-07 at run time, with no literal written, once the decision_log_entry text is in the chunk. |
| RWB-P3-E2042-APP | R-28866 | GAP-1299 |  | The name of the rwb-decision database login is not specified | Database section text is not in this chunk, so the old text cannot be copied. Needs a chunk that includes the Database section to write 'the rwb-decision login (DP-02)'. |
| RWB-P3-E2042-APP | R-28871 | GAP-2034 |  | The UNIVERSAL package has no single owning service | UNIVERSAL package text is not in this chunk, so no edit could be made. Needs a chunk including the UNIVERSAL text to record the per-service evaluation rule. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06944 | RWB-P3-E2024-APP | CG-ALL-4275 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's story RWB-P4-E1037-CON. |
| CDC-06963 | RWB-P3-E2033-APP | CG-ALL-4292 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or name a published operation. |
| CDC-06966 | RWB-P3-E2033-APP | DOR-RWB-P3-E2033-APP-8 | not located | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml, as for CG-ALL-4292. |
| CDC-06977 | RWB-P3-E2034-APP | CG-ALL-4302 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-06978 | RWB-P3-E2034-APP | CG-ALL-4303 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through the provider's CON story. |
| CDC-06979 | RWB-P3-E2034-APP | DOR-RWB-P3-E2034-APP-8 | 12.1 | Publish POST /api/recovery/access/v1/authorise and GET /api/recovery/access/v1/masking-policies (CG-ALL-4302, CG-ALL-4303). |
| CDC-06995 | RWB-P3-E2035-APP | CG-ALL-4314 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the rwb-access provider CON story; story 12.2 left as is. |
| CDC-07022 | RWB-P3-E2036-APP | CG-ALL-4341 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. No story edit. |
| CDC-07037 | RWB-P3-E2041-APP | CG-ALL-4356 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the rwb-access provider's CON story |
| CDC-07056 | RWB-P3-E2041-CON | CG-ALL-4372 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the P4 rwb-access CON story, or this story consumes a published operation instead. |
| CDC-07060 | RWB-P3-E2041-CON | DOR-RWB-P3-E2041-CON-8 | 13 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml (see CG-ALL-4372). P2 CaseWorkflow ID forms are not in these parts. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06961 | RWB-P3-E2024-APP | CG-ALL-4282 | 18 | Align the REQ-DCM-013 trace with §18 (TC-E2-024-01 to TC-E2-024-18) or with the RTM list in its next version. |
| CDC-06975 | RWB-P3-E2033-APP | CG-ALL-4297 | 18 | Align RTM v7 test lists for REQ-WKM-002, REQ-DVH-006 and the third requirement to section 18 of this story in the next RTM version. |
| CDC-06993 | RWB-P3-E2034-APP | CG-ALL-4307 | 18 | Align the test lists of the nine requirement rows with section 18 of this story in the next RTM version. |
| CDC-07014 | RWB-P3-E2035-APP | CG-ALL-4323 | 18 | Align the test lists of the five differing requirements (including REQ-WKM-012 and REQ-WKM-013) with section 18 of this story in the next RTM version. |
| CDC-07035 | RWB-P3-E2036-APP | CG-ALL-4346 | 18 | Align the test case lists for the five requirements with section 18 of this story at the next RTM version. |
| CDC-07052 | RWB-P3-E2041-APP | CG-ALL-4363 | 18 | Align the test lists of REQ-CWC-013 and REQ-DRI-011 with section 18 of RWB-P3-E2041-APP in the next RTM version. |
| CDC-07077 | RWB-P3-E2041-CON | CG-ALL-4381 | 18 | Align the REQ-CWC-013 and REQ-DRI-011 test lists with section 18 of RWB-P3-E2041-CON in the next RTM version. |
| CDC-07088 | RWB-P3-E2042-APP | DOR-RWB-P3-E2042-APP-12 | 16 | Align its test lists for this story with the test cases of RWB-P3-E2042-APP §16 (TC-E2-042-01 to TC-E2-042-12). |
| CDC-07092 | RWB-P3-E2042-APP | GAP-2503 |  | Declare the nine consumed operations on the per-service bases with one hop and a 2 s timeout; name the workflow matchPayments with its four activities; record in the RTM that AC1, AC3, AC4 and AC5 of the legacy key have no story in this split. |
| CDC-07104 | RWB-P3-E2042-APP | CG-ALL-4392 | 18 | Align the REQ-CWC-013 test list with §18 of this story (TC-E2-042-01, -02, -03, -06), or correct §18 if the RTM list is right. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06942 | RWB-P3-E2024-APP | CG-ALL-4273 | 12.1 | Publish GET /api/recovery/case/v1/cases/{caseId} in rwb-case.yaml through the CON story. The story path is already single; no story edit. |
| CDC-06943 | RWB-P3-E2024-APP | CG-ALL-4274 | 12.1 | Publish GET /api/recovery/case/v1/cases/{caseId}/timeline in rwb-case.yaml through the CON story. The story path is already single; no story edit. |
| CDC-06945 | RWB-P3-E2024-APP | CG-ALL-4276 | 2 | Remove the fixed discretion enum so LOV-DISCRETION values are data accepted without a code change. |
| CDC-06946 | RWB-P3-E2024-APP | CG-ALL-4277 | 2 | Remove the fixed elementType enum so LOV-ELEMENT values are data accepted without a code change. |
| CDC-06947 | RWB-P3-E2024-APP | CG-ALL-4278 | 2 | Remove the closed status enum so LOV-TASK-STATUS values are data. Which list the status field carries per resource is Not specified in the source documents (CG-ALL-4278). |
| CDC-06948 | RWB-P3-E2024-APP | CG-ALL-4279 | 2 | Remove the closed status enum so LOV-VERSION-STATUS values are data. Which list the status field carries per resource is Not specified in the source documents (CG-ALL-4279). |
| CDC-07036 | RWB-P3-E2041-APP | CG-ALL-4355 | 12.1 | Publish GET /api/recovery/case/v1/admin/rule-change-audit in rwb-case.yaml through RWB-P3-E2041-CON, or remove the operation from section 12.1 |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06967 | RWB-P3-E2033-APP | CG-ALL-4294 | 14 | Add a new message ID for the authorise budget refusal and cite it in section 14 in place of the placeholder. |
| CDC-07042 | RWB-P3-E2041-APP | CG-ALL-4362 | 14 | Add a new message ID for no package version in force on the business date; MSG-P3-027 keeps its load-failure text. |
| CDC-07043 | RWB-P3-E2041-APP | DOR-RWB-P3-E2041-APP-9 | 14 | MSG-P4-001 trigger 'no Workbench role' conflicts with 12.1 (401 no session). Standard owner or BA to rule on the trigger. |
| CDC-07061 | RWB-P3-E2041-CON | CG-ALL-4377 | 4, 14 | Add a new message ID for 'A request body or query fails schema validation' with text 'The request could not be read: {detail}.'; the story then cites it. |
| CDC-07062 | RWB-P3-E2041-CON | CG-ALL-4379 | 4, 14 | Add a new message ID for 'No session' with text 'Your session has ended. Sign in again to continue.'; the story then cites it. |
| CDC-07066 | RWB-P3-E2041-CON | DOR-RWB-P3-E2041-CON-9 | 14 | Story keeps MSG-P3-030 for the request row; the standard uses it for a scheduled job, so a new ID is needed (CG-ALL-4377). |
| CDC-07089 | RWB-P3-E2042-APP | DOR-RWB-P3-E2042-APP-9 | 14 | Align the P2 MSG-P3-027 text to the Error and Message Standard v4 wording. This story's section 14 text is kept unchanged. |

### RWB-P2-E2035-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06998 | RWB-P3-E2035-APP | DOR-RWB-P3-E2035-APP-21 | header | Publish the NextAction contract as the contract dependency named in metadata; no RWB-P3-E2035-CON story is added. |
| CDC-06999 | RWB-P3-E2035-APP | DOR-RWB-P3-E2035-APP-22 | header | Record a published contract fake library version for the NextAction contract; version not specified in the sources. |
| CDC-07007 | RWB-P3-E2035-APP | GAP-0668 | 12 | Baseline the three operation names, nine consumed shapes, split note, Schedule contract and error mapping; confirm the five message texts; record the read path ruling in the Ownership Map. |
| CDC-07017 | RWB-P3-E2035-APP | GAP-2409 |  | Mark packageVersion required on GET /api/recovery/decision/v1/rule-catalog/{ruleId}; keep the MSG-GEN-001 refusal. |
| CDC-07097 | RWB-P3-E2042-APP | GAP-0668 | 12 | Baseline the three operation names, the nine consumed shapes, the split note, the workflow and Schedule contract and the error mapping; contract owners of rwb-case, rwb-access and rwb-decision confirm element names; record the read path ruling in the Ownership Map. |

### RWB-P2-E2033-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06964 | RWB-P3-E2033-APP | DOR-RWB-P3-E2033-APP-21 | not located | Provide the published contract story the story depends on, or confirm RWB-P2-E2033-CON as the dependency at a fixed version. |
| CDC-06969 | RWB-P3-E2033-APP | GAP-0661 | 4 | Baseline the two read-only composed operations on the integration base with their columns, filters, order, paging envelope and problem body; state that GET /cases and GET /cases/export stay with rwb-case. |
| CDC-06971 | RWB-P3-E2033-APP | GAP-2224 | 7 | Fix row and envelope names in contract v1, confirm page bounds and export limit as parameter rows with RWB-P3-E2011-APP, drop the duplicate timer index, and name the login and flag owner. |
| CDC-06973 | RWB-P3-E2033-APP | GAP-2320 | Metadata | Fix session element list, authorise branch and batch bound, and extract record fields in baseline review with the rwb-access contract owner. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06965 | RWB-P3-E2033-APP | DOR-RWB-P3-E2033-APP-5 | 9 | Confirm CAR is already in LOV-CASE-STATUS and LOV-PRODUCT, or add it there. This story adds no value to either list. |
| CDC-07013 | RWB-P3-E2035-APP | GAP-2323 | 3 | Add CUSTOMER_PARTY as a fourth LOV-ROLE-CLASS value in the load that carries the roles, and confirm it with the role catalogue owner before wave 2 policy pack. |
| CDC-07019 | RWB-P3-E2035-APP | GAP-2407 |  | Publish LOV-DECISION with state-change codes marked and let the filter read the mark; until then take the newest case entry with a rule ID and rule version. |
| CDC-07026 | RWB-P3-E2036-APP | DOR-RWB-P3-E2036-APP-5 | 9 | Confirm New and Assigned as values of LOV-CASE-STATUS. The flagged labels are not in section 9 and are not added. |

### RWB-P2-E2034-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06987 | RWB-P3-E2034-APP | GAP-0664 | 12 | Approve the login, element names, admin bodies, per-type mapping, retry intervals (1 minute, 10 minutes, 1 hour; three attempts) and the ledger split. |
| CDC-06988 | RWB-P3-E2034-APP | GAP-0665 | 12 | Fix wire shapes of the append, the two P1 reads, the five fact answers and the two admin operations; set dedupe key, state moves and append-before-inbox order. |
| CDC-06991 | RWB-P3-E2034-APP | GAP-2225 | 3 | Confirm element names, paths and field shapes at contract review; rename in this story only if they differ. |
| CDC-06992 | RWB-P3-E2034-APP | GAP-3149 | find it | Declare the partner fact and seven ledger attributes with placeholders; agree EV-20 and EV-21 payload names at contract review. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06990 | RWB-P3-E2034-APP | GAP-2184 | 3 | Publish the retention class list and periods; add PARTNER_RESULT and OFFER to LOV-LEDGER-EVENT in one version; confirm uuid type of the two link columns. |
| CDC-07028 | RWB-P3-E2036-APP | CG-ALL-4338 | 3, 8, 12.7 | Record uk_assignment_open_case as a unique index on assignment (case_id) in the rwb_case schema, outside the field dictionary. |
| CDC-07029 | RWB-P3-E2036-APP | CG-ALL-4339 | 12.7 | Record permission_matrix as an rwb-access table, not a dictionary field. |
| CDC-07030 | RWB-P3-E2036-APP | CG-ALL-4340 | 12.7 | Record interface_catalogue as an rwb-integration table, not a dictionary field. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06996 | RWB-P3-E2035-APP | CG-ALL-4316 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that carries the rule-package contract for DP-04. |
| CDC-06997 | RWB-P3-E2035-APP | DOR-RWB-P3-E2035-APP-17 | 13 | Create story RWB-P7-E1073-CON, or name the existing story for the DP-04 rule-package dependency. |
| CDC-07038 | RWB-P3-E2041-APP | CG-ALL-4358 | 13 | Create story RWB-P7-E1073-CON or name the existing story that carries the rwb-decision rule package contract |
| CDC-07057 | RWB-P3-E2041-CON | CG-ALL-4373 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story that carries the rwb-decision contract and correct the dependency to that key. |

### RWB-P7-E2042-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07009 | RWB-P3-E2035-APP | GAP-2406 | find it | Set the valid-from date of RES-2026.12 to 2026-12-01, the named candidate, and align the legacy fixtures before the wave-2 freeze. |
| CDC-07099 | RWB-P3-E2042-APP | GAP-2406 | 4, 7, 13 | Reconcile one valid-from date for RES-2026.12 before the wave-2 fixture freeze; the ITG harness and RWB-P3-E2035-APP use 2026-12-01, which is the recommended value. |
| CDC-07101 | RWB-P3-E2042-APP | GAP-0722 | 12 | Publish the model and catalog resources with packageCode, versionLabel, checksum (SHA-256), model content, compiler version and valid-from date; and ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code and outputs; property types stay with the owner. |
| CDC-07111 | RWB-P3-E2042-APP | GAP-1296 | n/a | Carry the eight H and three C DP-added dependencies in that story; keep its metadata rows as written. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07047 | RWB-P3-E2041-APP | GAP-0718 | 11 | Publish GET /api/recovery/case/v1/admin/rule-change-audit with the section 11 entry fields and Rules and parameters R; add the ownership map row before the wave 2 baseline. |
| CDC-07053 | RWB-P3-E2041-APP | GAP-0203 | 19 | Add a payment_match_rule row with owner P7, target schema rwb_decision, the retired basis per D-RCV-36 T10, and the rule in the PAYMENT_MATCH package; keep all 13 fields. |
| CDC-07078 | RWB-P3-E2041-CON | GAP-0203 | - | Add a payment_match_rule row: owning service P7, target schema rwb_decision, all 13 fields kept, note that the table is retired by D-RCV-36 T10 and the rule lives in the PAYMENT_MATCH rule package. |
| CDC-07109 | RWB-P3-E2042-APP | GAP-1994 | n/a | Add an owner row for payment_match_rule as the PAYMENT_MATCH package in rwb-decision; keep the proceeds rows in rwb-payment. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07001 | RWB-P3-E2035-APP | CG-ALL-4321 | 16 | Add a row for TC-E2-035-14 with Given, When and Then copied from AC12, plus rows for TC-E2-035-15 and TC-E2-035-16 added to story section 16. |
| CDC-07065 | RWB-P3-E2041-CON | DOR-RWB-P3-E2041-CON-12 | 12.7, 16, 18 | Add TC-P3-E2041-CON-01 to -06 to Test Cases v8 and align the section 18 test lists to RTM v7 (content not in the source text). A boundary test is added in section 16 as TC-P3-E2041-CON-07. |
| CDC-07076 | RWB-P3-E2041-CON | CG-ALL-4380 | 16 | Add rows TC-P3-E2041-CON-01 to TC-P3-E2041-CON-06 with Given, When and Then copied from the criterion each covers. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06949 | RWB-P3-E2024-APP | DOR-RWB-P3-E2024-APP-14 | Metadata | Record the signed epic design sign-off for RWB-P3-E2024-APP |
| CDC-07059 | RWB-P3-E2041-CON | DOR-RWB-P3-E2041-CON-14 | header | Confirm the signed epic design for EP02 and record its sign-off reference against this story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06951 | RWB-P3-E2024-APP | Definition of Ready item 12 Test cases: Partial | 16 | Boundary test TC-E2-024-16 added to section 16; section 18 range set to TC-E2-024-01 to TC-E2-024-20 |
| CDC-07002 | RWB-P3-E2035-APP | DOR-RWB-P3-E2035-APP-12 | 12, 16 | Add TC-E2-035-14 (AC12 Given/When/Then), TC-E2-035-15 and TC-E2-035-16; align RTM v7 test lists to story section 18. |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06955 | RWB-P3-E2024-APP | GAP-0952 | - | Publish the authorise, me-permissions and masking-policies shapes, and state whether a sync is authorised once per manifest or once per item |
| CDC-07090 | RWB-P3-E2042-APP | GAP-0966 |  | Add the rule-package action, request and answer fields and a change decision code to POST /authorise; agree the code with the RWB-E1-039 access-log owner and stub both in the contract fake. |

### OTHER:Open decisions register (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06968 | RWB-P3-E2033-APP | DOR-RWB-P3-E2033-APP-18 | header | Give DL31 an assumption ID or record that none applies; confirm the assumptions listed against DL10, DL11, DL22 and DL31. |
| CDC-07003 | RWB-P3-E2035-APP | DOR-RWB-P3-E2035-APP-18 | find it | Record an assumption ID against DL24, or record that none applies so the item passes on that basis. |

### RWB-P2-E2033-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06970 | RWB-P3-E2033-APP | GAP-0660 | 4 | Keep GET /cases and GET /cases/export with rwb-case; add the composed read and export on the integration base as additional and read-only, one hop each with a 2 s budget. |
| CDC-06972 | RWB-P3-E2033-APP | GAP-3101 | 4, 8 | Add read GET /api/recovery/deviation/v1/deviation-flags to rwb-deviation (read only, one hop, page bound as a parameter row of rwb-case); add it to the consumed set of RWB-P2-E2033-CON at its next revision. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07005 | RWB-P3-E2035-APP | GAP-3177 | find it | Register the five-minute next-action Temporal Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables. |
| CDC-07086 | RWB-P3-E2042-APP | CG-ALL-4390 | 12.5 | Add activity swapRuleModel (task queue rwb-case) to the Activities sheet, or name a catalogued activity in RWB-P3-E2042-APP §12.5. |

### RWB-P2-E2035-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07008 | RWB-P3-E2035-APP | GAP-0669 | 13 | Fix the next-action identity and secret reference; add a next-action-check job catalogue row with run book path; record the read path ruling in the Ownership Map. |
| CDC-07098 | RWB-P3-E2042-APP | GAP-0669 | 13 | Fix the identity, secret reference and probe checks in RWB-P2-E2035-OPS; create the next-action-check row with its run book path in the job catalogue; take catch-up, overlap, backfill and thresholds as environment values; record the read path ruling in the Ownership Map. |

### RWB-P3-E2042-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07010 | RWB-P3-E2035-APP | GAP-2405 | 3 | Fix the row answer (packageCode, packageVersion, versionState, inForce, ruleId, ruleVersion, actionText, ownerRole, timerSpec, toState, droolsRuleName, outputs) and the latest-state-change answer (entryId, ruleId, ruleVersion, decidedAt, missing, 200 with missing true when none); add 404 and 422 entries of MSG-P3-027 and MSG-GEN-001 for these reads. |
| CDC-07084 | RWB-P3-E2042-APP | DOR-RWB-P3-E2042-APP-21 | header | Build RWB-P3-E2042-CON to Done so the contract counts as published. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07012 | RWB-P3-E2035-APP | GAP-2322 | 3 | Add GET /api/recovery/access/v1/role-catalogue/{roleCode} with its answer schema, stub it in the RWB-P4-E1037-CON fake, fix the authorise request and answer, fix the rwb-access login, and add the unknown or inactive role code message. |
| CDC-07049 | RWB-P3-E2041-APP | GAP-0964 | 12 | Add GET /api/recovery/access/v1/rule-authority and POST /api/recovery/access/v1/rule-report-exports as P4 operations with their query, body and answer fields, and freeze the action set and refusal reasons at the RWB-P3-E2041-CON contract review. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07023 | RWB-P3-E2036-APP | CG-ALL-4348 | 12.8 | Solution architect rules the Java package segment for rwb-case in place of the reserved word 'case' and adds a reserved-word rule to section 4 naming; the story then copies that segment. |
| CDC-07024 | RWB-P3-E2036-APP | CG-ALL-4349 | 12.8 | Solution architect rules the Java package segment for rwb-case in place of the reserved word 'case' and adds a reserved-word rule to section 4 naming; the story then copies that segment. |

### RWB-P2-E2036-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07025 | RWB-P3-E2036-APP | DOR-RWB-P3-E2036-APP-22 | header | Record the published contract fake library version. |
| CDC-07034 | RWB-P3-E2036-APP | GAP-2412 |  | Publish the placement fact element names, key and envelope on rwb.decision-record.v1; publish P3 case-read and P4 authorise shapes and the reference-data operation in their CON stories at wave 2 entry; MSG-P7-009 text by the business analyst; login and secret store in the platform DB story. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07027 | RWB-P3-E2036-APP | DOR-RWB-P3-E2036-APP-8 | 12.1, 12.3 | rwb-access API yaml: publish POST /api/recovery/access/v1/authorise. Kafka Catalog v1: state the CaseTransferred.v1 payload for EV-04. |
| CDC-07033 | RWB-P3-E2036-APP | GAP-3102 |  | Publish the hold element with case reference, deviation reference, code, open count, handler, return point, contact-stop flag and rule version, additive within major version 1. Declare the event-driven set and clear of recovery_case.deviation_open in rwb-case, and keep the metadata rows as the plan gives them. |

### RWB-P3-E2041-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07040 | RWB-P3-E2041-APP | DOR-RWB-P3-E2041-APP-21 | header | Complete the build of RWB-P3-E2041-CON to Done |
| CDC-07075 | RWB-P3-E2041-CON | GAP-2413 | - | Agree ChangeReportPage and RulePackageChangeEntry shapes, rulesChanged element (ruleId, added, changed, removed), CSV column order equal to JSON field order, LOV-DECISION and checklist item-list codes, package-version count, load and approve answers with legacy flag off, and rwb-decision login name. |

### OTHER:TSD P4 v3 T6.1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07048 | RWB-P3-E2041-APP | GAP-0962 | 16 | Publish one RULES_AND_PARAMETERS matrix row set giving the letter of every role a rule change touches, and restate the reference data administrator's allowed actions without a C letter. |
| CDC-07050 | RWB-P3-E2041-APP | GAP-0965 | 3 | Add the rwb-decision service identity and the gateway-bff route with the R letter in RULES_AND_PARAMETERS only; confirm with the security administrator before the authorise contract is frozen. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07055 | RWB-P3-E2041-APP | GAP-2415 | 7 | Record the rename of rwb.p3.rule-change-report and the move of the checklist, two operations and the report to rwb-decision; keep the legacy flag as a parameter read. |
| CDC-07079 | RWB-P3-E2041-CON | GAP-2415 | Register | Record the rename of legacy flag rwb.p3.rule-change-report as a rwb-decision parameter; checklist column, two amended operations and change report owned by rwb-decision (P7) |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07063 | RWB-P3-E2041-CON | DOR-RWB-P3-E2041-CON-1 | 1 | Confirm a role code or name for the persona 'tech lead', or the story names a role that Users Roles and Permissions v5 lists. The value is not specified in the source documents. |
| CDC-07102 | RWB-P3-E2042-APP | GAP-0967 | 9 | Publish the service-identity rows for the fourteen capability areas; confirm each service runs as one non-human actor; record the area each package serves as a rwb-decision package attribute. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07080 | RWB-P3-E2042-APP | CG-ALL-4386 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in rwb-decision.yaml through the provider's CON story. |
| CDC-07081 | RWB-P3-E2042-APP | CG-ALL-4387 | 12.2 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId} with query parameter packageVersion in rwb-decision.yaml through the provider's CON story. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07100 | RWB-P3-E2042-APP | GAP-2396 | 4 | Correct the P6 Comms to P7 Decision cell in the next diagram issue so it matches the event route used by RWB-P6-E1073-APP; no second notice-path consumer is added. |
| CDC-07105 | RWB-P3-E2042-APP | GAP-1620 | 3 | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime, that a package version names its format, and that conversion is a version change with its own test evidence. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06950 | RWB-P3-E2024-APP | DOR-RWB-P3-E2024-APP-8 | Metadata | Publish GET /api/recovery/case/v1/cases/{caseId} and GET .../timeline in rwb-case.yaml; publish POST /api/recovery/access/v1/authorise in rwb-access; resolve discretion LOV-DISCRETION closed enum versus data and the four further detcheck mismatches |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06952 | RWB-P3-E2024-APP | GAP-3194 | - | Raise an ACE DB story for the column drop in S2, S4, S5, S6, S7, P6 and P8, or attach the drop to the APP story that creates the table; cite the chosen story on row 121 |

### RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06953 | RWB-P3-E2024-APP | GAP-2223 | - | Add stageCode and routeCode to the Case resource; record the authorise shape in the rwb-access API specification; name the checklist contract story in the Ownership Map; load task data via rwb-case admin stories |

### OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06954 | RWB-P3-E2024-APP | GAP-0949 | - | Add the five DOCUMENTS rows (RW-FIELDCOL CR, RW-CASEOWN CRU, RW-RESTRUCT CRU, SY-OCR CRU, RW-PHONECOL R) to the PM-2026.12 permission file under RWB-P4-AD002-APP, and add a Documents column to the RBAC matrix |

### RWB-P5-E1024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06956 | RWB-P3-E2024-APP | GAP-1018 | - | The store takes an optional capture block as an additive change within major version 1; the intake submit of RWB-P5-E1057-CON creates the intake item; the P3 parameters and reference-data contracts publish the parameter and list names |

### OTHER:Wave 2 harness pack (QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06957 | RWB-P3-E2024-APP | GAP-0406 | - | Specify the field-app test client, capture fixtures, intake test profile, SIT seeding, evidence report format and the wave 2 pass and fail gate |

### RWB-P5-E2024-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06958 | RWB-P3-E2024-APP | GAP-1019 | - | Declare the manifest part, the item properties and required set, 415 for non-multipart requests only, REFUSED items at 201 with MSG-P5-001, and the placeholder window values |

### OTHER:rwb-case reference-data register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06959 | RWB-P3-E2024-APP | GAP-1283 | none | Record DOCATT as the LOV-DECISION value on every document-attach entry; keep D6.5 as the routing tag of the legacy story, not the entry code. |

### RWB-ITG-E2024-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06960 | RWB-P3-E2024-APP | GAP-1284: No source settles whether an item the store refuses leaves a DOCATT entry | 12.2, 12.8 | The integration story owns sections 12.2 and 12.8. Section 16 has no failed-log-write test, so this story needs no edit. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06962 | RWB-P3-E2024-APP | GAP-0951 | none | State the field app route: capture sync as a composed call beside the rwb-document call, and the SCR-30 panel as a parallel read through the gateway-bff composite route. |

### OTHER:Wave 2 release record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06974 | RWB-P3-E2033-APP | GAP-0415 | 16 | Ratify harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence/gate format as one appendix before RWB-ITG-E2033-ITG claims Done. |

### OTHER:Plan (RWB-E2-033 to RWB-E2-036 primary assignment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06976 | RWB-P3-E2033-APP | GAP-3187 | Metadata | Keep rwb-integration primary for RWB-E2-033 to RWB-E2-036 in this version and record the P2/P3 tension for the assembly step. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06980 | RWB-P3-E2034-APP | GAP-1844 | header | Align RWB-S9-E2034-APP wave 2 with rwb-case service creation in wave 4 per the EP02 contract-first ruling; this story keeps wave 2 as the ledger slice. |

### OTHER:Recovery Workbench FSD P7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06981 | RWB-P3-E2034-APP | GAP-1612 | 12 | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012 under rwb-source-data. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06982 | RWB-P3-E2034-APP | GAP-3175 | 13 | Name EV-26 AceDataReady, producer rwb-source-data, on rwb.source-data.events.v1, with LoadCompleted as legacy alias. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06983 | RWB-P3-E2034-APP | GAP-3176 | 12 | Confirm no Epic 2 step depends on JOB-01; entry points are AceIngestCheck (JOB-04) and AceDataReady (EV-26) only. |

### RWB-P2-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06984 | RWB-P3-E2034-APP | GAP-0590 | 12 | Publish key EFS:<efs_record_key>; RWB-P1-E1066-APP ledger writer owns the repeat hit count; the run reports both counts in its summary. |

### RWB-P2-E2034-CON; RWB-P1-E2001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06985 | RWB-P3-E2034-APP | GAP-2186 | 12 | Publish contact-fact read with path, contact-key parameter and masked members; confirm EFS outcome operation; realign the two consumed rows. |

### OTHER:Ledger harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06986 | RWB-P3-E2034-APP | GAP-0416 | 16 | Hold composite route, environment, seeding, evidence format, retention and pass/fail gate as harness data, agreed at the wave 2 entry check. |

### RWB-P2-E2034-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06989 | RWB-P3-E2034-APP | GAP-0666 | 16 | Approve consumer groups, offset policy, scan and retry intervals, lag and alert thresholds, build ID format and fixture ownership as environment values. |

### RWB-P1-E1066-CON; RWB-P1-E1066-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06994 | RWB-P3-E2034-APP | GAP-2185 | 12.1 | Settle one case-scoped path family for the ledger and realign the append row and its fake to POST /cases/{caseId}/interactions. |

### OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07000 | RWB-P3-E2035-APP | DOR-RWB-P3-E2035-APP-8 | 12.7 | Publish POST /api/recovery/access/v1/authorise or drop the reference; the story does not name this path. Story 12.7 now names rwb.decision.DecisionRecorded.v1 per Kafka Catalog v1. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07004 | RWB-P3-E2035-APP | GAP-2395 | find it | Read the three Epic 2 package codes and version labels as the fixture set; assign rwb-comms to a package only after the rule registry owner settles it; invent no fourth code. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P2-E2035-CON; OTHER:rwb-case, rwb-access and rwb-decision contracts; OTHER:timer register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07006 | RWB-P3-E2035-APP | GAP-0667 | 4, 7 | Correct the next-action row so P2 owns the read and P3 the write; fix consumed field and operation names, Schedule values and message texts; record JOB-05 retired. |

### OTHER:TSD P4 T6.1 (RBAC matrix) and the policy pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07011 | RWB-P3-E2035-APP | GAP-2324 | 3 | Add a Case record column for every role in T6.1, publish the full 14-area matrix through RWB-P4-AD002-APP, and fix the default scope of the specialist roles with the security administrator before PM-2026.12. |

### OTHER:Programme plan (rwb-integration backlog for RWB-E2-033 to RWB-E2-036) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07015 | RWB-P3-E2035-APP | GAP-3187 |  | Keep rwb-integration primary for RWB-E2-033 to RWB-E2-036 and record the P3 code tension for the assembly step. |

### OTHER:rwb-comms story for the notice copy (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07016 | RWB-P3-E2035-APP | GAP-2400 |  | Read action_text, owner_role and timer_spec in rwb-comms only for notices decided by a route-set rule, tested with R-RES-04 legacy values. |

### OTHER:TSD P4 T3.1 (role table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07018 | RWB-P3-E2035-APP | GAP-2325 |  | State that role rows are versioned by the matrix version they load with, or add a role_version label; set the cache lifetime as a DP-06 parameter; test the version-keyed drop. |

### OTHER:rwb-case reference data (timer_spec list of values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07020 | RWB-P3-E2035-APP | GAP-2408 |  | Publish the timer spec shapes as a list of values with a parsing rule, extended with 'payment due 30 days' and 'deadline driven'. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07021 | RWB-P3-E2035-APP | GAP-2411 |  | Name the per-service login for rwb-decision and keep the migration and application roles apart; reference the name from stories once set. |

### OTHER:Wave 2 queue-placement harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07031 | RWB-P3-E2036-APP | GAP-0419 |  | Hold the composite route path and merge order, harness repository, SIT environment, seeded callers and queues, evidence format and retention, and pass/fail gate as data, agreed by the integration lead and QA at wave 2 entry. |

### OTHER:rwb-access service contract document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07032 | RWB-P3-E2036-APP | GAP-0958 |  | Fix five reason codes with one status each: 403 for RIGHT_NOT_HELD, CALLER_KIND and SCOPE_NOT_ALL; the 422 and 503 codes keep MSG-GEN-001, MSG-GEN-002 and MSG-P7-003; MSG-P4-002 is the message of every 403. |

### RWB-P3-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07039 | RWB-P3-E2041-APP | DOR-RWB-P3-E2041-APP-17 | header | Complete the RWB-P3-E1073-APP build before this story starts; the RWB-P7-E1073-CON gap is tracked under CG-ALL-4358 |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07041 | RWB-P3-E2041-APP | DOR-RWB-P3-E2041-APP-8 | 12.1 | rwb-case.yaml: add GET /admin/rule-change-audit under /api/recovery/case/v1. rwb-access: publish POST /api/recovery/access/v1/authorise or drop it from the story. |

### OTHER:TSD P7 rwb-decision; OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07044 | RWB-P3-E2041-APP | GAP-1615 | find it | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule-version and rule-package operations; remove them from TSD P3 and TSD P4; set x-module of nine rule paths to P7. |

### API:(service not named); OTHER:rwb-decision documents for FEAT-ADM-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07045 | RWB-P3-E2041-APP | GAP-1565 | find it | Re-issue TSD P4 without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 to rwb-decision documents; set x-module of six paths to P7. |

### OTHER:Rule-change report harness pack (integration lead with QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07046 | RWB-P3-E2041-APP | GAP-0420 | find it | Record SIT environment, seeding of ALLOC-2026.11 to ALLOC-2026.14, RES-2026.12, PMT-2026.12, 96 and 1,204 entries, evidence format and retention, pass/fail gate and composite route detail at wave 2 entry check. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07051 | RWB-P3-E2041-APP | GAP-2413 | 3 | Placeholder line states the shapes are Not specified and to be confirmed at the wave 2 re-check of RWB-P3-E2041-CON. |

### OTHER:Contract README (case-side audit read contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07054 | RWB-P3-E2041-APP | GAP-0720 | 8 | Invented section 8 retention sentence removed. Audit read retention stays Not specified (GAP-0720); the other two windows stay open. |

### OTHER:05 Technical architecture/Recovery Workbench Service Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07058 | RWB-P3-E2041-CON | CG-ALL-4382 | none | P3 rwb-case row: replace the package segment 'case' in th.co.scb.ace.workbench.recovery.case with the segment the Solution architect rules under the Service Template Specification v1 naming rule |

### RWB-P3-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07064 | RWB-P3-E2041-CON | DOR-RWB-P3-E2041-CON-10 | find it | Add empty, loading, error and no-access states for SCR-02 and SCR-39 to the screen specification. |

### OTHER:TSD P7 rwb-decision; OTHER:TSD P3 v3; OTHER:TSD P4 v3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07067 | RWB-P3-E2041-CON | GAP-1615 | find it | Re-issue TSD P7 with T3.1 entries for rule_package, rule_package_version, rule_row and rule_test_case and appendix T-A rule-version and package operations; remove these from TSD P3 and TSD P4; set x-module of the nine rule paths to P7. |

### OTHER:TSD P3 v3; OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07068 | RWB-P3-E2041-CON | GAP-1993 | find it | Remove the claim on rule_package, rule_package_version, rule_row and rule_test_case from TSD P3 v3 and TSD P4 v3; read the package and catalogue through the P7 contract (DP-04). |

### OTHER:TSD P4 v3; OTHER:FEAT-ADM-02; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07069 | RWB-P3-E2041-CON | GAP-1565 | find it | Re-issue TSD P4 without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 to rwb-decision documents; set x-module of the six paths to P7. |

### OTHER:Harness pack (integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07070 | RWB-P3-E2041-CON | GAP-0420 | find it | At wave 2 entry check agree SIT environment, seeding of ALLOC-2026.11 to ALLOC-2026.14, RES-2026.12, PMT-2026.12, 96 and 1,204 decision log entries, evidence format, retention, pass/fail gate and gateway-bff route detail. |

### OTHER:openapi/rwb-case-v1.yaml; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07071 | RWB-P3-E2041-CON | GAP-0718 | find it | Publish GET /api/recovery/case/v1/admin/rule-change-audit with the section 11 entry fields and Rules and parameters R; add the ownership map row before the wave 2 contract baseline tag. |

### OTHER:TSD P4 v3 T6.1; 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07072 | RWB-P3-E2041-CON | GAP-0962 | find it | Publish one RULES_AND_PARAMETERS matrix row set stating each role letter for rule changes, restate reference data administrator limits, and correct TC-E2-041-11 to a dash-letter role. |

### API:(service not named); OTHER:TSD P4 v3 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07073 | RWB-P3-E2041-CON | GAP-0964 | find it | Add GET /api/recovery/access/v1/rule-authority and POST /api/recovery/access/v1/rule-report-exports as P4 operations with their query, body and answer fields; freeze action set and refusal reasons at contract review. |

### OTHER:TSD P4 v3 T6.1 (permission data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07074 | RWB-P3-E2041-CON | GAP-0965 | - | Add the rwb-decision service identity and the gateway-bff route with the R letter in RULES_AND_PARAMETERS and no other right; confirm with the security administrator before the authorise contract is frozen. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07082 | RWB-P3-E2042-APP | CG-ALL-4388 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that carries the DP-04 rule-package capability. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07083 | RWB-P3-E2042-APP | CG-ALL-4389 | 12.5 | Add a row for workflow RuleModelSwap on task queue rwb-case, or name the catalogued workflow to use in §12.5. |

### OTHER:rwb-decision API yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07085 | RWB-P3-E2042-APP | DOR-RWB-P3-E2042-APP-8 | 12.5 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} and GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=; add workflow RuleModelSwap and activity swapRuleModel to Temporal Catalog v1. |

### OTHER:22 Microservice Realignment/aisdlc/docs/prds/recovery-workbench-fsd-p4-access-and-administration-v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07087 | RWB-P3-E2042-APP | DOR-RWB-P3-E2042-APP-10 |  | Add empty, loading, error and no access states to SCR-39 Rules and parameters; the current entry lists only rule versions, route sets, thresholds and timers, with the load and approval. |

### OTHER:RWB-P7 technical specification; OTHER:TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07091 | RWB-P3-E2042-APP | GAP-1615 |  | Re-issue TSD P7 with T3.1 entries for the four rule tables and the rule-version and package operations; remove them from TSD P3 and TSD P4; set the x-module of the nine rule paths to P7. |

### RWB-P2-E2007-APP; RWB-P2-E2007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07093 | RWB-P3-E2042-APP | GAP-0657 |  | Keep JOB-08 with rwb-integration and record the Architecture v5 slide 44 owner row as superseded; read ACE facts through the rwb-source-data contract; fix the six consumed paths and shapes; allocate the rwb-integration login in RWB-PLT-DB. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07094 | RWB-P3-E2042-APP | GAP-1292 |  | Reconcile PM-2026.12 from 2026-12-01 and PMT-2026.12 from 2026-12-15 into one label and one valid-from date before PAYMENT_MATCH is promoted in SIT. |

### OTHER:RWB-E2-027 build notes (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07095 | RWB-P3-E2042-APP | GAP-3179 |  | Drop the payment_match_rule table from the service schema and load the rows only through the rule package endpoints. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P2-E2035-CON; RWB-P2-E2035-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07096 | RWB-P3-E2042-APP | GAP-0667 | 4, 7, 12 | Serve GET /cases/{caseId}/next-action from /api/recovery/integration/v1 under DP-13; rwb-case keeps the case row and the write; fix field names, operation names, Schedule values and message texts in RWB-P2-E2035-CON; correct the Ownership Map row to P2 read and P3 write; retire JOB-05 in the timer register. |

### OTHER:FSD P6 v3 A2.1.4.2 and A2.1.4.3 (notice states and hold reasons) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07103 | RWB-P3-E2042-APP | GAP-2399 | 5 | Refuse the request with MSG-GEN-006, create no notice row, dispatch nothing and add no hold reason of this service, for the notice path owner. |

### RWB-P3-E2042-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07106 | RWB-P3-E2042-APP | GAP-0723 | 9 | Set the container to write-once with no deletion and reviewed audit retention per environment; size the pod by a load test caching 20 versions; expose alert windows, replica counts and probe timings as reviewed values. |

### OTHER:TSD P4 v3 T3.1 and T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07107 | RWB-P3-E2042-APP | GAP-0968 | 3 | Move the four rule tables and the registry operations to P7 (rwb-decision); keep the P4 rows for the rights and the access log only. |

### OTHER:Parameters contract (DP-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07108 | RWB-P3-E2042-APP | GAP-0969 | n/a | Add a parameter row for the cached authorise-answer lifetime of rwb-access; keep the version-keyed AccessPolicyChanged.v1 refresh; confirm one access-log entry per dry run with the access-log owner. |

### OTHER:Decision-record publication (DP-03 decision record; OTHER:owner role Data steward) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07110 | RWB-P3-E2042-APP | GAP-2397 | 11 | Confirm the two field IDs that carry the package code and the SHA-256 checksum of a notice decision when the record is published. No column is added to notice, template or merge_field. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20710 | RWB-P3-E2041-CON | R-22286 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21918', 'R-22054', 'R-22286', 'R-22289', 'R-22316', 'R-28613'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0203 | The entity Payment match rule has no row in the Ownership Map and no target table | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0406 | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | Integration lead | Resolved (directive) |
| GAP-0415 | The SIT harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence format for the case-list journey are not specified in any source read | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0416 | Ledger harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0418 | Gateway-bff composite next-action route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0419 | Wave 2 queue-placement harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0420 | Rule-change report harness environment, seeding, evidence format, retention and composite route detail are not specified | Integration lead | Resolved (directive) |
| GAP-0421 | Rule package harness: repository, SIT environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0664 | The rwb-integration login, the entry and fact JSON field names, the admin bodies, the mapping detail, the retry intervals and the ownership split of the ledger intake are not fixed in the source documents | Solution architect | Resolved (directive) |
| GAP-0665 | The append, EFS and contact wire shapes, the admin operation bodies, the dedupe key of each type and the ordering of the append and the inbox are not stated for the intake contract | Solution architect | Resolved (directive) |
| GAP-0666 | The consumer group names, the offset policy, the retry scan interval, the lag and alert thresholds, the build ID format and the fixture owner of the intake deployment are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0669 | rwb-integration next action deployment: the login and secret reference, the next-action-check run values, the alert thresholds and the runbook ownership are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner | Resolved (directive) |
| GAP-0670 | rwb-integration queue-write adapter: the operation owner, the login, the consumed contract field names and the replay window are not fixed by one source | Solution architect | Resolved (directive) |
| GAP-0671 | rwb-integration queue-write adapter contract: the ownership of the placement path, the consumed contract shapes and the library table columns are not fixed by one source | Tech lead | Resolved (directive) |
| GAP-0718 | The case-side rule-change audit read has no row in the ownership map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0719 | FSD A2.16 reports reference-data changes while the legacy story and the test cases govern rule package versions | Business analyst | Resolved (directive) |
| GAP-0720 | Retention and lifecycle windows of the new audit read and its contract are not specified | Data steward | Resolved (directive) |
| GAP-0721 | The rule package registry is declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0722 | The rule-model and rule-catalog read operations have no published field-level shape | P7 rwb-decision owner | Resolved (directive) |
| GAP-0723 | Blob immutability period, pod memory for 20 KieBases, alert windows and probe timings are not specified | SCB IT infrastructure with the DevOps team | Resolved (directive) |
| GAP-0734 | The next-action slice leaves the legacy AC allocation, the daily check Schedule, the DL22 durations and the role-class field unspecified | Tech lead | Resolved (directive) |
| GAP-0735 | The placement slice leaves the legacy AC allocation, the approved callers list, the production matrix grant, the overflow shape, the caller mapping and the login name unspecified | Tech lead | Resolved (directive) |
| GAP-0949 | The Documents letters per role are not carried by the P4 access documents | Security administrator with the P4 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0951 | Whether the field app reaches the authorise path through gateway-bff or directly is not specified | Solution architect, P4 with the gateway-bff route owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0952 | The request and answer shape of the authorise call for a multi-item sync is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0957 | rwb-access queue-write authority: the request and answer element set of the placement admission part of POST /authorise and of the non-human part of GET /me/permissions is named by no source | Solution architect | Resolved (directive) |
| GAP-0958 | rwb-access queue-write authority: the refusal reason code vocabulary and the status each code answers with are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0959 | rwb-access queue-write authority: no source binds a role to a list of teams or regions, so a scope narrower than ALL cannot be resolved for a non-human caller | Security administrator | Resolved (directive) |
| GAP-0960 | rwb-access queue-write authority: how a caller code is bound to a Workbench role, and whether a caller code is itself a role, is fixed by no source | Security administrator | Resolved (directive) |
| GAP-0962 | The roles and letters of the rule-administration area differ between the work package line, the legacy authority table and TSD P4 v3 T6.1, and the legacy access test names a role the matrix gives the right | Security administrator with the P4 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0964 | The two operations of this slice, and their request and answer shapes, are absent from Architecture v5, the API Specification and the TSD P4 appendix | Solution architect with the API Specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0965 | Which right a service identity holds to ask this service about a person other than the session user is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0967 | rwb-access rule-package authority: the scope of a running service identity inside rwb-access and the capability area each rule package serves are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0968 | rwb-access rule-package authority: TSD P4 v3 gives P4 the four rule tables, while Architecture v5 and the ownership ruling put the rule registry in P7 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0969 | rwb-access rule-package authority: the lifetime of a cached authorise answer, the refresh trigger of the cached permission data and the granularity of the access-log entry of a dry run are not specified | Solution architect | Resolved (directive) |
| GAP-1018 | Field capture: the store capture block, the intake submit path, the parameter and list names, the service login name and the approval status are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1019 | Field capture contract: the manifest part and item field names, the stored-answer window, the not-found message and the 415 reading are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1283 | The decision code of a field-capture entry is D6.5 in the legacy metadata but DOCATT on the store path | Business analyst, P7, with the business analyst of P5 rwb-document and the data steward | Resolved (directive) |
| GAP-1284 | No source settles whether an item the store refuses leaves a DOCATT entry | Business analyst, P7, with the P5 business analyst and the integration lead of RWB-ITG-E2024-ITG | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1298 | The decision code of a rule-governance entry is not named in any source this key may read | Decision log owner | Resolved (directive) |
| GAP-1299 | The name of the rwb-decision database login is not specified | ACE database administrator | Resolved (directive) |
| GAP-1300 | The detail text of MSG-P3-027 for the two Epic 2 checks is not fixed | Business analyst | Resolved (directive) |
| GAP-1301 | The four rule registry tables are declared for P4 and P3 in their TSDs and are absent from the P7 TSD | Solution architect | Resolved (directive) |
| GAP-1302 | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | Business analyst | Resolved (directive) |
| GAP-1303 | The BRD section pointers copied from the legacy story no longer match BRD v2 and v4 | Business analyst | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1565 | The rule package registry, the rule-package operations and the change report are claimed by the P4 technical specification while the Ownership Map gives them to rwb-decision | Solution architect with the rwb-decision contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-1994 | payment_match_rule has no owner in the Ownership Map | Solution architect | Resolved (directive) |
| GAP-2026 | Owning service of the PAYMENT_MATCH package is not stated in one place | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2034 | The UNIVERSAL package has no single owning service | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2184 | The retention class list, the added event codes, the link column types and the feature IDs of four requirements are in no source | Data architect | Resolved (directive) |
| GAP-2185 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2186 | The EFS outcome read and the contact-fact read that the channel consumer calls are named by interface only, with no path, parameter or owning story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2223 | The case-side slice of the field-capture path rests on answers no source specifies: the stage and route fields of the case resource, the authorise call shape, the contract story of the checklist read, and the task data | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2224 | The case list is served twice in the target, and the row names, the bounds, the login and the flag mechanism of the owner's list have no source | Solution architect | Resolved (directive) |
| GAP-2225 | Element names of the interaction item, the append command and the intake result are not in the sources | TechX and rwb-source-data contract owner | Resolved (directive) |
| GAP-2226 | Legacy occurred-time order and the case timeline page order differ | TechX | Resolved (directive) |
| GAP-2320 | rwb-access answer behind the case and queue list: element names, the P2 attribution of the contract dependency, the authorise branch, the extract record, the login and the parameter and reference paths are not settled by any source read | Solution architect | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2322 | rwb-access next action: the role-catalogue operation, the authorise request and answer of a next-action read, the rwb-access login and the message for an unknown role code are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2323 | rwb-access next action: the role class list has no customer-party value, while the legacy waiting text is produced for a customer party or a partner user | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2324 | rwb-access next action: the RBAC matrix tabulates three capability areas and gives no Case record letter, so the R rights and the scopes the next-action read needs are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2325 | rwb-access next action: a role row carries no version label of its own and the lifetime of a cached access or role answer is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2396 | Architecture v5 slide 13 gives P6 to P7 a Temporal cell and no event cell, while RWB-P6-E1073-APP consumes RulePackageInForce from rwb.decision.events.v1 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2397 | No source states where the package version and checksum of a notice decision are stored, and the legacy story adds no column for them | Data steward | Resolved (directive) |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2399 | No source states the state a notice rests in, or the message, when no package version is in force | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2400 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Business analyst | Resolved (directive) |
| GAP-2405 | rwb-decision next action: the answer shape of the rule-catalog and latest-state-change reads, and their not-found and malformed-parameter messages, are not specified | Solution architect | Resolved (directive) |
| GAP-2406 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Business analyst, P7 | Resolved (directive) |
| GAP-2407 | rwb-decision next action: no source enumerates the decision codes or final calls that count as a state change for the latestStateChange filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2408 | rwb-decision next action: rule_row.timer_spec has no list of values, and two legacy specs are outside the four shapes the legacy rule enumerates | Business analyst, Epic 2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2409 | The published catalogue path shows packageVersion as an optional query parameter and no source says what an absent value answers | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2411 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2413 | No source gives the field-level shapes this story needs: the change-report element beyond its legacy field names, the CSV column order, the rulesChanged element, the decision-code and item-list values, the reconciliation read and the DP-02 login name | Solution architect | Resolved (directive) |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2415 | The legacy story places the change checklist and the report in module P3 and the P4 package recovery.accessadmin.rulepackages with a P3 feature flag, while the target puts the registry, the checklist column and the decision log in rwb-decision | Solution architect | Resolved (directive) |
| GAP-2416 | Legacy AC1 approves ALLOCATION version ALLOC-2026.12 on 2026-12-02 while AC5 loads the same version on 2026-12-08 and approves it on 2026-12-09, so BR4 (verify on or after the load and before the approval) cannot hold in both readings | Business analyst P7 | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3101 | rwb-deviation case and queue list slice: no read in the Ownership Map, no seam with the composed page, no path, field names or page bound, the flag derived twice and the pause projection without the rule package | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3102 | RWB-S8-E2036-APP: the deviation hold that the queue-write interface obeys has no published element names, no case-event names, no case-side setter for deviation_open and no placement-half criteria, and the pattern set adds dependencies the metadata rows do not carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3149 | rwb-partner interaction-ledger slice: no ledger column or operation in S9, no published payload for EV-20 or EV-21, the seam with RWB-P2-E2034-CON undefined, the list members, the retry bound and the holder-reference form unpublished, and an empty H row against ten platform contracts | Solution architect; rwb-integration contract owner (RWB-P2-E2034-CON); rwb-source-data ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC11 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC12 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC13 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC14 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC15 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC16 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC17 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC18 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC19 is new and no section 16 row covers it |
| RWB-P3-E2041-APP | new AC without TC row | 481 | AC20 is new and no section 16 row covers it |
| RWB-P3-E2042-APP | date added | 1 | 2026-12-01 |
