# RWB-SVC-P5 rwb-document (Document) - review pack, part 6 of 6 (RWB-P5-E2024-APP to RWB-P5-E2030-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 161 |
| Cross-document (pending in another document) | 165 |
| Not applied (value not in the sources) | 16 |
| Open business decisions | 21 |
| Register gaps linked | 62 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P5-E2024-APP | 24 | 20 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2024 APP Field app photos and bills into the document hub v2.md |
| RWB-P5-E2024-CON | 15 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2024 CON Field app photos and bills into the document hub - contract v2.md |
| RWB-P5-E2025-APP | 31 | 21 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2025 APP Extraction for the stage 2 and 3 document types v2.md |
| RWB-P5-E2025-CON | 19 | 30 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2025 CON Extraction for the stage 2 and 3 document types - contract v2.md |
| RWB-P5-E2025-OPS | 24 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2025 OPS Extraction for the stage 2 and 3 document types - deployment v2.md |
| RWB-P5-E2026-APP | 18 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2026 APP Document generation engine for contract, CA and mortgage templates v2.md |
| RWB-P5-E2026-CON | 17 | 19 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2026 CON Document generation engine for contract, CA and mortgage templates - contract v2.md |
| RWB-P5-E2030-APP | 13 | 16 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2030 APP Legal document agent in shadow on Epic 1 data [E3c] v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P5-E2030-APP | R-01634 | CG-ALL-6270 | Script gap | Product owner | The story adds MORTGAGE_CIVIL to the closed list LOV-ROUTE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E2030-APP | R-01635 | CG-ALL-6271 | Script gap | Product owner | The story adds MORTGAGE_CIVIL to the closed list LOV-STAGE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E2030-APP | R-01636 | CG-ALL-6272 | Script gap | Product owner | The story adds MORTGAGE_CIVIL to the closed list LOV-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E2024-APP | R-10947 | CG-ALL-6210 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2024-CON | R-10949 | CG-ALL-6222 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2025-APP | R-10954 | CG-ALL-6234 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2025-CON | R-10958 | CG-ALL-6248 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2026-APP | R-10963 | CG-ALL-6261 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2026-CON | R-10964 | CG-ALL-6267 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2024-APP, RWB-P5-E2024-APP, RWB-P5-E2024-CON, RWB-P7-E2024-APP | R-22594 | GAP-0950 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masking rows and the mask version for the capture position are not specified | Record the DF-DOC-028 and DF-DOC-029 rows per role in the MASK-SIT-01 pack, with unmasked true for RW-CASEOWN and RW-RESTRUCT, false for RW-FIELDCOL and RW-PHONECOL and no row for SY-OCR, and let the platform masking library own one rendering per field type |
| RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2024-APP, RWB-P5-E2024-APP, RWB-P5-E2024-CON, RWB-P7-E2024-APP | R-22596 | GAP-1281 | Register gap | Solution architect, P7 rwb-decision, with the data steward, the P5 business analyst and the business owner | The field-capture decision record's payload, read shape, message id set, panel id, parameter names and login name have no source | At design time of wave 2 the solution architect, the data steward, the P5 business analyst and the business owner agree and approve, as reference data and as the OpenAPI of the service: the capture columns of decision_log_entry (new columns or jsonb members), the object-reference filter of the read and the answer field set, the message ids and their texts, the panel id of the decision-log view, the parameter names and version labels of the ingest target and the chain check, and the per-service login name; until then the story holds the assumed shape of ASM-B-P7-03-E2024-1, ASM-B-P7-03-E2024-2 and ASM-B-P7-03-E2024-3 and its seven criteria stand on that shape |
| RWB-ITG-E2025-ITG, RWB-P5-E2025-APP, RWB-P5-E2025-CON, RWB-P5-E2025-OPS, RWB-P7-E2025-APP, RWB-S2-E2025-APP, RWB-S4-E2025-APP | R-22604 | GAP-1285 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The extraction decision record's payload, value sets, read shape and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the extraction column set of decision_log_entry (new columns or jsonb members), the decision code of an extraction decision, the final-call value set, the threshold parameter names and version labels, the message ids and their texts, the document filter of the read and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2025-1 and its eight criteria stand on that shape |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-22619 | GAP-1287 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The generation record's payload, value sets, read shape, message set and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the container of the template code, the template version, the treatment reference and the requesting role on decision_log_entry, the shape of the merge snapshot reference, the decision code D6.4 as a value of LOV-DECISION, the final-call list that holds GENERATED, the message ids and texts of a refused record and a duplicate append, the page-size parameter name, the search index and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2026-1 to ASM-B-P7-03-E2026-5 and its nine criteria stand on that shape |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-28820 | GAP-0940 | Register gap | Compliance and PDPA officer | The masking version label and the DF-PTY-007 rows on the generation path are not specified | Load the DF-PTY-007 masking rows with unmasked false for RW-RESTRUCT, RW-CASEOWN, RW-TEAMMGR and SY-CASEWF under the SIT masking version, name the version in the policy pack load record, and leave the format to the one masking library every screen uses. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P5-E2024-APP | R-06315 | DOR-RWB-P5-E2024-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the project .md files or the story (grep for 'epic design'). Sign-off value would be invented; left unresolved. |
| RWB-P5-E2024-APP | R-17430 | DOR-RWB-P5-E2024-APP-10 | 9, 10 | Definition of Ready item 10 Screens and states: Partial | SCR-30 and SCR-31 state rows sit in sections 9-10, outside this chunk. Empty, loading and error texts are not in the source documents. |
| RWB-P5-E2024-APP | R-25908 | CG-ALL-6211 | 3, 3.1 | Flyway file V2024_1__field_capture.sql is not in the V0001..Vnnnn form | Next free V-number of the rwb-document Flyway sequence is not in the sources (grep for V0001, V2024_1, Vnnnn found no match in Service Template Specification v1). Migration name line is outside this chunk. |
| RWB-P5-E2024-CON | R-22593 | GAP-0406 |  | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | No source gives the test client, capture pack, EICAR fixture, seeding, evidence format or gate values; ownership.json lists owners only. Agreement with P5 owner and QA is outside the story. No value invented. |
| RWB-P5-E2025-APP | R-28814 | GAP-1902 | 18 | REQ-DCM-017 and REQ-DCM-018 are in the plan's requirement list for this story but in no row of the legacy traceability table, and legacy section 19 puts them out of scope | Duplicate REQ-DCM-018 row removed; the existing REQ-DCM-018 row is kept. Nothing added. |
| RWB-P5-E2025-CON | R-06331 | DOR-RWB-P5-E2025-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the chunk or the story. Grep of the folder was incomplete (timed out), so no sign-off was found. Needs the record. |
| RWB-P5-E2025-CON | R-17462 | DOR-RWB-P5-E2025-CON-18 | 9 | Definition of Ready item 18 Open decisions: Partial | Section 9 with the DL10 row and its ASM links is not in the chunk, so there is no exact old text to edit. Needs section 9 text. |
| RWB-P5-E2025-CON | R-17463 | DOR-RWB-P5-E2025-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | New criteria belong in section 7 and test cases in section 16, neither in the chunk. Needs those sections' current text to anchor the edits. |
| RWB-P5-E2026-CON | R-06346 | DOR-RWB-P5-E2026-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (Decision Log v11 DT05 is a plan, not a sign-off). Sign-off reference cannot be invented. |
| RWB-P5-E2026-CON | R-17485 | DOR-RWB-P5-E2026-CON-11 |  | Definition of Ready item 11 Guardrails: Partial | The P2 fields flagged by detcheck are not named in this chunk or in the reports checked. Guardrail cannot be set without them. |
| RWB-P5-E2026-CON | R-22620 | GAP-1289 | 12.3 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Section 12.3 text is not in this chunk, so the producer-side write and MSG-P7-003 wording cannot be edited in. Needs §12.3 in a later chunk. |
| RWB-P5-E2026-CON | R-25931 | CG-ALL-6265 | 16 | Test cases cover other criteria in Test Cases v8 | v8 Covers values for three of the 11 rows are truncated in the cached export. TC-01 would also lose BR1 and BR6 if aligned to v8 AC1. |
| RWB-P5-E2026-CON | R-31229 | NEWAC-RWB-P5-E2026-CON-AC15 | 7 | AC15: §8 BR2, BR3, BR4, BR5, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 text is not in this chunk, so AC15 cannot be placed. The proposed test is Not specified in the source documents (NEWAC-RWB-P5-E2026-CON-AC15). |
| RWB-P5-E2030-APP | R-06349 | DOR-RWB-P5-E2030-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source set (earlier search). Sign-off cannot be confirmed without inventing a value; record needed. |
| RWB-P5-E2030-APP | R-06350 | DOR-RWB-P5-E2030-APP-16 | header table | Definition of Ready item 16 Size: Fail | Sources do not give the size; the story cannot state it. The invented refinement wording is removed. |
| RWB-P5-E2030-APP | R-06352 | DOR-RWB-P5-E2030-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version in the sources; rwb-document.yaml info.version 5.0.0 is the API version, not a fake version. Cannot state a published version. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10351 | RWB-P5-E2024-APP | CG-ALL-6201 | 12.1 | Add path POST /api/recovery/document/v1/cases/{caseId}/field-captures as specified in RWB-P5-E2024-CON, published through the CON story. |
| CDC-10352 | RWB-P5-E2024-APP | CG-ALL-6202 | 12.2 | Publish POST /api/recovery/document/v1/scans in rwb-document.yaml through RWB-P5-E1041-CON, the provider's CON story. |
| CDC-10353 | RWB-P5-E2024-APP | CG-ALL-6203 | 12.2 | Remove the fixed enum on captureKind so values come from LOV-CAPTURE-KIND as data. |
| CDC-10354 | RWB-P5-E2024-APP | CG-ALL-6204 | 12.2 | Remove the fixed enum on reviewStatus so values come from LOV-REVIEW as data. |
| CDC-10357 | RWB-P5-E2024-APP | DOR-RWB-P5-E2024-APP-8 | 12.1 | Add POST /api/recovery/document/v1/cases/{caseId}/field-captures with an Idempotency-Key header; add POST /api/recovery/document/v1/scans; make captureKind and reviewStatus LOV-backed (LOV-CAPTURE-KIND, LOV-REVIEW) not closed enums; resolve the three unlisted detcheck items. |
| CDC-10372 | RWB-P5-E2024-CON | CG-ALL-6216 | 12.2 | Publish POST /api/recovery/document/v1/scans in rwb-document.yaml, as the provider's CON story. |
| CDC-10388 | RWB-P5-E2025-APP | CG-ALL-6228 | 12.1 | Publish GET /api/recovery/document/v1/cases/{caseId}/checked-fields in rwb-document.yaml through RWB-P5-E2025-CON. |
| CDC-10389 | RWB-P5-E2025-APP | CG-ALL-6229 | 12.2 | Publish POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract in rwb-document.yaml through RWB-P5-E1053-CON, or consume a published operation. |
| CDC-10390 | RWB-P5-E2025-APP | CG-ALL-6230 | 12.2 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction in rwb-document.yaml through RWB-P5-E1053-CON, or consume a published operation. |
| CDC-10393 | RWB-P5-E2025-APP | DOR-RWB-P5-E2025-APP-8 | 12.1 | Publish the three named operations and align the DocumentFieldsExtracted topic, per CG-ALL-6228 to CG-ALL-6231. |
| CDC-10409 | RWB-P5-E2025-CON | CG-ALL-6241 | 12.1 | Add path GET /api/recovery/document/v1/cases/{caseId}/checked-fields (query documentType required, documentVersion optional; 200 CheckedFieldSet). |
| CDC-10411 | RWB-P5-E2025-CON | CG-ALL-6243 | 12.2 | Publish POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract as declared by RWB-P5-E1053-CON. |
| CDC-10412 | RWB-P5-E2025-CON | CG-ALL-6244 | 12.2 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction as declared by RWB-P5-E1053-CON. |
| CDC-10413 | RWB-P5-E2025-CON | CG-ALL-6245 | 12.2 | Publish GET /api/recovery/document/v1/documents/{documentId}/fields as declared by RWB-P5-E1053-CON. |
| CDC-10500 | RWB-P5-E2030-APP | CG-ALL-6274 | 9 | Remove the fixed enum on reviewStatus so LOV-REVIEW values are accepted as data without a code change. |
| CDC-10501 | RWB-P5-E2030-APP | DOR-RWB-P5-E2030-APP-8 | 12.1 | Remove the fixed enum on reviewStatus so LOV-REVIEW values are accepted as data (ruling R-01637). |

### RWB-P5-E2025-CON (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10391 | RWB-P5-E2025-APP | DOR-RWB-P5-E2025-APP-21 | header | Set build status to Done so the contract is published before this story starts. |
| CDC-10392 | RWB-P5-E2025-APP | DOR-RWB-P5-E2025-APP-23 | header | State the contract baseline version this story builds against. |
| CDC-10398 | RWB-P5-E2025-APP | GAP-1713 | find it | Record once the mapping of each FEAT prerequisite to its owning service contract (approval P7, case P3, documents P5, communications P6, valuation S1); carry duplicate FEAT-CHO-08 as written. |
| CDC-10400 | RWB-P5-E2025-APP | GAP-1020 | 10 | Checked-fields path and field-level names replaced with Not specified in the source documents (GAP-1900). |
| CDC-10402 | RWB-P5-E2025-APP | GAP-1900 | 12.1 | Define the checked-fields read as a GET on the rwb-document base with case and document type as parameters, a CheckedField list answer filtered by state and masked by role, keeping legacy element names. |
| CDC-10440 | RWB-P5-E2025-OPS | DOR-RWB-P5-E2025-OPS-21 | header | Complete the contract build and set its build status to Done so the contract is published. |
| CDC-10441 | RWB-P5-E2025-OPS | DOR-RWB-P5-E2025-OPS-22 | header | Publish the contract fake library and record its version as published. |
| CDC-10448 | RWB-P5-E2025-OPS | GAP-1713 | find it | Record once the mapping of FEAT-APD-01, FEAT-CHO-02/06/07/08, FEAT-DCM-12, FEAT-OCC-01/07/09/11, FEAT-TRT-04 and FEAT-VAL-06 to owning-service contracts; keep duplicate FEAT-CHO-08 as written |
| CDC-10450 | RWB-P5-E2025-OPS | GAP-1020 | 12 | Checked-fields path, operation and field names kept as Not specified (GAP-1900); no longer claimed as named. |
| CDC-10451 | RWB-P5-E2025-OPS | GAP-1021 |  | Declare the checked-fields read on the service base with its shape and status set. Name the three extraction operations as consumed from RWB-P5-E1053-CON and re-declare none. |
| CDC-10454 | RWB-P5-E2025-OPS | GAP-1900 |  | Publish the checked-fields read once as a GET on the rwb-document base, with case and document type as parameters, a CheckedField list answer, state filter and role masking. |
| CDC-10506 | RWB-P5-E2030-APP | GAP-0628 | 12.2 | Declare the OCR-text and checklist reads, the legal-action read, the run start, the route and the event scope as GAP-0628 proposes. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10369 | RWB-P5-E2024-APP | CG-ALL-6209 | 16, 18 | Test lists in sections 16 and 18 carry IDs 01 to 25 |
| CDC-10386 | RWB-P5-E2024-CON | CG-ALL-6221 | 18 | Align the REQ-DCM-013 and REQ-DRI-004 rows of the RTM with the section 18 lists of RWB-P5-E2024-CON in the next RTM version. |
| CDC-10407 | RWB-P5-E2025-APP | CG-ALL-6233 | 18 | Align the REQ-DCM-006 and REQ-DCM-005 test lists with the section 18 test lists in the next RTM version. |
| CDC-10420 | RWB-P5-E2025-CON | DOR-RWB-P5-E2025-CON-12 | 16, 18 | Align the test lists of REQ-DCM-006, REQ-DCM-005, REQ-DCM-017 and REQ-DCM-018 to section 18, with TC-E2-025-13 under REQ-DCM-006. |
| CDC-10438 | RWB-P5-E2025-CON | CG-ALL-6247 | 18 | Align the REQ-DCM-006 and REQ-DCM-005 test lists with section 18 of RWB-P5-E2025-CON. |
| CDC-10466 | RWB-P5-E2026-APP | DOR-RWB-P5-E2026-APP-12 | 16 | Align the test lists in its section 18 with the story section 18 rows, which now include TC-E2-026-17 and TC-E2-026-18. |
| CDC-10476 | RWB-P5-E2026-APP | CG-ALL-6260 | 18 | Align the REQ-DCM-012 and REQ-OCC-002 test lists in the RTM to the section 18 lists of this story in its next version. |
| CDC-10496 | RWB-P5-E2026-CON | CG-ALL-6266 | 18 | Align the test lists for REQ-DCM-012 and REQ-OCC-002 with section 18 of this story, which matches section 16. |
| CDC-10514 | RWB-P5-E2030-APP | CG-ALL-6277 | 18 | Trace REQ-DCM-011 to TC-E2-030-01, TC-E2-030-04, TC-P5-E2030-01 and TC-P5-E2030-02, as section 18 does. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10404 | RWB-P5-E2025-APP | GAP-2703 | 12.1 | Record the S2 Treatment to P5 Document cell (T) as an open amendment to the architecture review; the story keeps the REST one-hop read. |
| CDC-10408 | RWB-P5-E2025-APP | GAP-1704 | none (no story text) | Route generation, review and signature through the P5 and P6 contracts (POST /cases/{caseId}/generated-documents, POST /documents/{documentId}/review); hold the document reference on the treatment; keep no document content in rwb_treatment. |
| CDC-10425 | RWB-P5-E2025-CON | GAP-0068 | find it | Set rwb-litigation (S4) to wave 2 as kept in W-MAP. |
| CDC-10429 | RWB-P5-E2025-CON | GAP-1877 |  | Amend the S2 Treatment row, P5 Document column, from T to the one-hop REST contract of RWB-P5-E2025-CON with a 2 s timeout and a breaker, per DP-11; align slides 12 and 16. |
| CDC-10432 | RWB-P5-E2025-CON | GAP-2703 |  | Keep the read as one-hop REST with a 2 s timeout, a breaker and no retry chain; record the slide 13 P5 cell as an open amendment. |
| CDC-10452 | RWB-P5-E2025-OPS | GAP-0068 |  | Align rwb-litigation wave to 2 as W-MAP keeps it. This story stays wave 2 and needs no change. |
| CDC-10470 | RWB-P5-E2026-APP | GAP-0938 | 12 | Add the authorise request and answer schema, with case reference, treatment reference, template code list, request key and the answer fields, and publish it with RWB-P4-E1037-CON. |
| CDC-10486 | RWB-P5-E2026-CON | GAP-1003 | find it | Declare POST /api/recovery/document/v1/intake-items/{intakeItemId}/classify and GET /api/recovery/document/v1/intake-items/{intakeItemId}/classification after architect confirmation; add rwb.document.DocumentClassified.v1 to the event catalogue. Then amend BR5 and AC8 of RWB-P5-E2026-CON. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10362 | RWB-P5-E2024-APP | DOR-RWB-P5-E2024-APP-7 | 11 | Register bill_amount and due_date as fields, which AC3 and section 11 use, since neither is in LDM v9 or Data Classification v5. |
| CDC-10394 | RWB-P5-E2025-APP | CG-ALL-6225 | 2, 4, 8, 12.7 | Record extraction_method as a field of document_type or give the dictionary name it maps to |
| CDC-10395 | RWB-P5-E2025-APP | CG-ALL-6226 | 2, 4, 8, 9, 12.7 | Record review_only as a field of document_type or give the dictionary name it maps to |
| CDC-10396 | RWB-P5-E2025-APP | CG-ALL-6227 | 11 | Record party_names as a field of CONTRACT or give the dictionary name it maps to |
| CDC-10421 | RWB-P5-E2025-CON | DOR-RWB-P5-E2025-CON-7 | 11 | Declare party_names, review_only and contract_amount as fields or entities; none is in LDM v9 or Data Classification v5. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10385 | RWB-P5-E2024-CON | CG-ALL-6219 | 16 | Add rows for TC-P5-E2024-CON-01 to TC-P5-E2024-CON-07 with Given, When and Then copied from AC1 to AC7 of section 7. |
| CDC-10447 | RWB-P5-E2025-OPS | DOR-RWB-P5-E2025-OPS-12 | 12, 12.7, 16 | Add rows for TC-P5-E2025-OPS-01 to TC-P5-E2025-OPS-08 as in section 16 of the story |
| CDC-10459 | RWB-P5-E2025-OPS | CG-ALL-6256 | 16 | Add rows TC-P5-E2025-OPS-01 to TC-P5-E2025-OPS-06 with Given, When and Then copied from the criterion each row covers. |
| CDC-10503 | RWB-P5-E2030-APP | CG-ALL-6275 | 16 | Add rows TC-P5-E2030-01 and TC-P5-E2030-02 to tab Story test cases, with Given, When and Then copied from the criteria they cover (AC1, AC3, BR3, AC6, BR6). |
| CDC-10513 | RWB-P5-E2030-APP | CG-ALL-6276 | 16 | Map TC-E2-030-04 to AC2 and TC-E2-030-06 to AC4, as story section 16 does, since those criteria hold the covered behaviour. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10360 | RWB-P5-E2024-APP | CG-ALL-6208 | 14 | Add a new message ID for 'No authenticated caller' with its text; the story then cites that ID in section 14 in place of MSG-P4-001. |
| CDC-10375 | RWB-P5-E2024-CON | CG-ALL-6218 | 4, 14 | Add a new message ID for 'No authenticated caller' to the standard; the story then cites it in section 14 in place of MSG-P4-001. |
| CDC-10427 | RWB-P5-E2025-CON | GAP-1022 | 11 | Name the extraction-run alert, accuracy alert and reader alert identifiers; ship operating values as environment placeholders. |
| CDC-10502 | RWB-P5-E2030-APP | CG-ALL-6273 | 4, 12.1 | Add message IDs for 401 no Workbench identity and 404 no such case (owner: business analyst). Story keeps the Not specified placeholder until then. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10361 | RWB-P5-E2024-APP | DOR-RWB-P5-E2024-APP-11 | 12.3 | Align the personal-data class of the fields this story carries with its statement that no personal data is in any payload, or record the personal fields in the story. |
| CDC-10415 | RWB-P5-E2025-CON | CG-ALL-6238 | find it | Record `party_names` as the personal CONTRACT field code in field_definitions (DF-REF-224), or give the dictionary name it maps to. |
| CDC-10416 | RWB-P5-E2025-CON | CG-ALL-6239 | find it | Record `review_only` as a field_definitions attribute (DF-REF-224) with its boolean meaning, or give the dictionary name it maps to. |
| CDC-10417 | RWB-P5-E2025-CON | CG-ALL-6240 | 16 | Record `contract_amount` as a CONTRACT field code in field_definitions (DF-REF-224), or give the dictionary name it maps to. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10371 | RWB-P5-E2024-CON | CG-ALL-6215 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml, as the provider's CON story. |
| CDC-10410 | RWB-P5-E2025-CON | CG-ALL-6242 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} through the provider's CON story RWB-P3-E1042-CON. |
| CDC-10481 | RWB-P5-E2026-CON | CG-ALL-6264 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml, as the P3 parameters contract RWB-P3-E1042-CON requires. |
| CDC-10482 | RWB-P5-E2026-CON | DOR-RWB-P5-E2026-CON-8 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml, as the P3 parameters contract RWB-P3-E1042-CON requires. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10418 | RWB-P5-E2025-CON | DOR-RWB-P5-E2025-CON-1 | 1 | Add 'tech lead' as a role name with its role code, or have the owning document record the role this story uses. |
| CDC-10445 | RWB-P5-E2025-OPS | DOR-RWB-P5-E2025-OPS-1 | 1 | Add 'platform engineer' as a role code or role name, or confirm it maps to an existing role; section 1 of the story is unchanged |
| CDC-10465 | RWB-P5-E2026-APP | DOR-RWB-P5-E2026-APP-1 | 1 | Add the role restructuring officer (FCR) with its role code, or name the code it already has. |
| CDC-10483 | RWB-P5-E2026-CON | DOR-RWB-P5-E2026-CON-1 | 1 | Add a role row for tech lead with its role code and role name, or confirm the existing role that section 1 should name. |

### RWB-S4-E2025-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10456 | RWB-P5-E2025-OPS | GAP-2835 | n/a | Specify the litigation checked-field read, the source stamps and columns on legal_action, and the unmapped-code count in the S4 story, building against RWB-P5-E2025-CON. |
| CDC-10457 | RWB-P5-E2025-OPS | GAP-2836 | n/a | Add the hearing-from-extract rule, the closed-status 409 rule and the same-date rule to the S4 hearing story; confirm hearing_type with the litigation business analyst. |
| CDC-10458 | RWB-P5-E2025-OPS | GAP-1903 | n/a | Fix the fill trigger, write key, request and answer element names, hearing natural key and parameter calls in the S4 story from RWB-P3-E1042-CON and RWB-P3-E1043-CON. |
| CDC-10461 | RWB-P5-E2025-OPS | GAP-1902 | n/a | Record that the legacy table omits REQ-DCM-017 and REQ-DCM-018 and the legacy scope excludes them; let step D1 decide the correction. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10475 | RWB-P5-E2026-APP | GAP-2393 | 12 | Add a request key and request lock table to rwb_comms in the V-baseline migration; record the rwb-document create operation from RWB-P5-E2026-CON in the P6 API specification. |
| CDC-10479 | RWB-P5-E2026-APP | GAP-2394 | 12 | Allocate the next API-P6-nnn ID at D1 for POST /cases/{caseId}/generated-documents and add the operation with the gateway-bff route. |
| CDC-10494 | RWB-P5-E2026-CON | GAP-2393 |  | Add a rwb_comms table for the request key and request lock via the V-baseline migration. Record the rwb-document create operation in the P6 API specification when its contract story is written. |
| CDC-10499 | RWB-P5-E2026-CON | GAP-2394 | find it | Allocate the next API-P6-nnn ID at D1 and add the generated-documents operation with the gateway-bff route; the story keeps the legacy path under the per-service base. |

### RWB-P10-E2030-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10505 | RWB-P5-E2030-APP | GAP-0627 | 12.2 | Settle the agent-side reads, run start, parameter keys, service login and route as GAP-0627 proposes; the consumed operations are not fixed in this story. |
| CDC-10507 | RWB-P5-E2030-APP | GAP-2196 | 12.2 | Publish the consumed paths, parameter codes, list codes, gateway-bff route and member types as GAP-2196 proposes. |
| CDC-10509 | RWB-P5-E2030-APP | GAP-2197 | 12.2 | Fix the run-start path, the six policy members, the pack and score row types and the route as GAP-2197 proposes. |
| CDC-10510 | RWB-P5-E2030-APP | GAP-2358 | 12.2 | Publish the pack tool call as one operation per case with named per-item fields, the legal-pack-v1 item codes and the 503 to TOOL_UNAVAILABLE mapping with fallback true. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10358 | RWB-P5-E2024-APP | CG-ALL-6199 | 4 | Record bill_amount as a field of the UTILITY_BILL type in the owning document (RWB-P5-E1025-APP type table), or name its dictionary entry. |
| CDC-10359 | RWB-P5-E2024-APP | CG-ALL-6200 | 4 | Record due_date as a field of the UTILITY_BILL type in the owning document (RWB-P5-E1025-APP type table), or name its dictionary entry. |
| CDC-10485 | RWB-P5-E2026-CON | GAP-1023 | 11 | Add template_code varchar(30) and template_version integer to document beside template_id and treatment_id; build the partial unique index on (treatment_id, template_id) where state is DRAFT and is_active. |

### RWB-P4-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10366 | RWB-P5-E2024-APP | GAP-0952 | 10 | Publish the authorise, me-permissions and masking-policies shapes and state whether a sync is authorised once per manifest or once per item and how the field list is carried. |
| CDC-10382 | RWB-P5-E2024-CON | GAP-0952 | n/a | Publish the authorise, GET /me/permissions and masking-policies shapes; state whether a sync is authorised once per manifest or per item and how the field list is carried. |
| CDC-10489 | RWB-P5-E2026-CON | GAP-0938 |  | Add the authorise request schema (case reference, treatment reference, template code list, request key) and the answer schema (letters, roles, scope result, matrix version, masking version). Stub generation facts in RWB-P5-E2026-CON. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10373 | RWB-P5-E2024-CON | DOR-RWB-P5-E2024-CON-14 | header | Record the signed epic design sign-off for RWB-P5-E2024-CON. |
| CDC-10439 | RWB-P5-E2025-OPS | DOR-RWB-P5-E2025-OPS-14 | header | Record the signed epic design sign-off for RWB-P5-E2025-OPS. No sign-off is in the source documents. |
| CDC-10462 | RWB-P5-E2026-APP | DOR-RWB-P5-E2026-APP-14 |  | Record the signed epic design sign-off for EP02 and RWB-P5-E2026-APP. No signed design is in the story or sources. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10377 | RWB-P5-E2024-CON | DOR-RWB-P5-E2024-CON-12 | 12.7, 16, 18 | Add story test rows TC-P5-E2024-CON-01 to -07 to Test Cases v8 Story test cases; align the section 18 test lists of this story with RTM v7. |
| CDC-10484 | RWB-P5-E2026-CON | DOR-RWB-P5-E2026-CON-12 | 16 | Align the test lists of §18 with RTM v7 and the criteria covered in Test Cases v8; §18 is aligned to TC-E2-026-17 in this story. |
| CDC-10504 | RWB-P5-E2030-APP | DOR-RWB-P5-E2030-APP-12 | 12.7, 16, 18 | Add rows TC-P5-E2030-01, TC-P5-E2030-02 and TC-P5-E2030-06 to Test Cases v8; align the section 18 test list of REQ-DCM-011 with RTM v7. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10442 | RWB-P5-E2025-OPS | DOR-RWB-P5-E2025-OPS-8 | header | Add the activities extract and evaluateExtraction to the Activities sheet, or name catalogued activities. |
| CDC-10443 | RWB-P5-E2025-OPS | CG-ALL-6254 | 12.5 | Add activity extract to the Activities sheet on task queue rwb-document, or use a catalogued activity. |
| CDC-10444 | RWB-P5-E2025-OPS | CG-ALL-6255 | 12.5 | Add activity evaluateExtraction to the Activities sheet on task queue rwb-document, or use a catalogued activity. |

### RWB-P5-E2024-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10355 | RWB-P5-E2024-APP | DOR-RWB-P5-E2024-APP-21 | header | Move the contract story build status from Not started to Done. |
| CDC-10356 | RWB-P5-E2024-APP | DOR-RWB-P5-E2024-APP-22 | header | Publish the contract fake library and record its version as published. |

### RWB-ITG-E2024-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10368 | RWB-P5-E2024-APP | GAP-1284 | 3 | Correct sections 12.2 and 12.8 to assert one DOCATT entry per refused item carrying result REFUSED and its message ID, not the absence of an entry; DUPLICATE resolves to the first item's entry. |
| CDC-10384 | RWB-P5-E2024-CON | GAP-1284 | 7 | Story records one entry per stored document; refused-item entry marked Not specified (GAP-1284). |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10370 | RWB-P5-E2024-APP | GAP-0951 | 3 | State the field app route in the gateway-bff contract: capture sync as a composed call beside the rwb-document call, and the SCR-30 panel as a parallel read. |
| CDC-10387 | RWB-P5-E2024-CON | GAP-0951 | 7 | State the field app route in the gateway-bff contract: capture sync as a composed call beside the rwb-document call, and the SCR-30 panel as a parallel read. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10379 | RWB-P5-E2024-CON | GAP-3194 | find it | Raise an ACE DB story for the column drop in S2, S4, S5, S6, S7, P6 and P8, or attach it to the owning APP story; cite the chosen story on row 121. |
| CDC-10423 | RWB-P5-E2025-CON | GAP-3194 | find it | Raise one ACE DB column-drop story each for S2, S4, S5, S6, S7, P6 and P8, or attach the drop to the creating APP story; cite it on row 121. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10399 | RWB-P5-E2025-APP | GAP-3194 | find it | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the column drop, or attach the drop to the creating APP story, and cite it on row 121 before wave 2. |
| CDC-10449 | RWB-P5-E2025-OPS | GAP-3194 | find it | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the 42-column drop, or attach the drop to their APP stories; cite on row 121 |

### OTHER:S4 hearing story (rwb-litigation) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10406 | RWB-P5-E2025-APP | GAP-2836 | 11 | One hearing per legal action and hearing_date; create with hearing_type empty and is_active true, else update next_date only; closed or withdrawn action answers 409. |
| CDC-10434 | RWB-P5-E2025-CON | GAP-2836 |  | One hearing per legal action and hearing_date; create with empty hearing_type and is_active true, or update next_date only; closed or withdrawn actions answer 409 with the baseline conflict message. |

### OTHER:rwb-treatment story set (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10453 | RWB-P5-E2025-OPS | GAP-1876 |  | Add the six fact columns, the three source columns and the tableVersion stamp to treatment. Keep party_names masked and unstored. Take the read from RWB-P5-E2025-CON. |
| CDC-10455 | RWB-P5-E2025-OPS | GAP-2702 |  | Take the read from RWB-P5-E2025-CON, add the fact and source columns on the treatment Flyway sequence, map same-name codes only, stamp tableVersion, mask party_names. |

### OTHER:rwb-document service contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10468 | RWB-P5-E2026-APP | GAP-1713 | header | Record the mapping of each FEAT prerequisite to its owning service contract: approval P7, case P3, documents P5, communications P6, valuation S1; FEAT-CHO-08 carried twice as written. |
| CDC-10487 | RWB-P5-E2026-CON | GAP-1713 | find it | Record once the owning-service contract for each listed prerequisite feature code, using approval to P7, case to P3, documents to P5, communications to P6 and valuation to S1; carry the duplicate FEAT-CHO-08 as written. |

### OTHER:FSD P5 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10469 | RWB-P5-E2026-APP | GAP-1580 | 7 | Add a generation section stating REQ-DCM-012 and the POST /cases/{caseId}/generated-documents behaviour in its next version, carrying FR-P5-026 and AC-P5-019. |
| CDC-10488 | RWB-P5-E2026-CON | GAP-1580 | find it | Add a generation section for REQ-DCM-012 in the next version, carrying FR-P5-026 and AC-P5-019 as its functional statement. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10363 | RWB-P5-E2024-APP | GAP-3194 |  | Raise one ACE DB story per service without one (S2, S4, S5, S6, S7, P6, P8), or attach the column drop to the owning APP story, and cite the chosen story on row 121 before wave 2. |

### RWB-P3-E1018-CON; API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:rwb-case administration stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10364 | RWB-P5-E2024-APP | GAP-2223 | 10, 11 | Add stageCode and routeCode to the Case resource; record the authorise request and response shape; name the checklist contract story; load task code, owner role, discretion, due-date parameter and decision code as data rows. |

### RWB-P4-AD002-APP; OTHER:TSD P4 v3 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10365 | RWB-P5-E2024-APP | GAP-0949 | 10 | Add the five DOCUMENTS rows (RW-FIELDCOL CR, RW-CASEOWN CRU, RW-RESTRUCT CRU, SY-OCR CRU, RW-PHONECOL R) and a Documents column in the RBAC matrix. |

### OTHER:Reference-data register of rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10367 | RWB-P5-E2024-APP | GAP-1283 | 3 | Record DOCATT as the approved value of LOV-DECISION on every document-attach entry; D6.5 stays the routing-decision tag of the legacy story, not the entry code. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10374 | RWB-P5-E2024-CON | DOR-RWB-P5-E2024-CON-8 | 12.2, 12.3 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml and POST /api/recovery/document/v1/scans in rwb-document.yaml. |

### OTHER:SCR-30 screen definition (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10376 | RWB-P5-E2024-CON | DOR-RWB-P5-E2024-CON-10 | header | Add empty, loading, error and no-access states for SCR-30. |

### OTHER:Platform error envelope message set (platform library) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10378 | RWB-P5-E2024-CON | DOR-RWB-P5-E2024-CON-9 | 14 | Confirm that MSG-P4-001 means no authenticated caller (401), as used in section 14, against the message standard. |

### RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10380 | RWB-P5-E2024-CON | GAP-2223 | find it | Add stageCode and routeCode to the Case resource; record the authorise request and response shape; name the checklist contract story in the Ownership Map and C dependency set; load task data rows. |

### RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10381 | RWB-P5-E2024-CON | GAP-0949 | find it | Add five DOCUMENTS rows (RW-FIELDCOL CR, RW-CASEOWN CRU, RW-RESTRUCT CRU, SY-OCR CRU, RW-PHONECOL R); add a Documents column to TSD P4 T6.1. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10383 | RWB-P5-E2024-CON | GAP-1283 | n/a | Record DOCATT as the LOV-DECISION value on every document-attach entry; D6.5 stays the routing tag of the legacy story, not the entry code. |

### RWB-P5-E2025-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10397 | RWB-P5-E2025-APP | DOR-RWB-P5-E2025-APP-17 | Header | Complete RWB-P5-E2025-OPS before the build starts |

### OTHER:TSD S2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10401 | RWB-P5-E2025-APP | GAP-1876 | 10 | Add contract_amount, contract_date, mortgage_amount, registration_date, land_office, title_doc_no, source_document_id, source_doc_version and source_table_version to treatment using the numeric(18,2) and date conventions. |

### OTHER:rwb-treatment story set (S2 checked-field consumer) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10403 | RWB-P5-E2025-APP | GAP-2702 | 11 | Take the read operation, payload and element names from RWB-P5-E2025-CON. Add fact and source columns on its own Flyway sequence, map only same-name codes, stamp tableVersion, mask party_names. |

### OTHER:rwb-litigation story set (S4 consumer) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10405 | RWB-P5-E2025-APP | GAP-2835 | 11 | Build against RWB-P5-E2025-CON. Add source_document_id, source_doc_version and source_table_version to legal_action on its own Flyway sequence; map only same-name codes; record twelve unmapped codes. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10414 | RWB-P5-E2025-CON | DOR-RWB-P5-E2025-CON-8 | 12.1, 12.2 | Publish the paths in CG-ALL-6241 to CG-ALL-6245 in their yamls. The two further P1 items are not in this chunk. |

### OTHER:P3 screen specification (SCR-30; OTHER:SCR-31) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10419 | RWB-P5-E2025-CON | DOR-RWB-P5-E2025-CON-10 | find it | Record the empty, loading, error and no-access states of SCR-30 and SCR-31; the story then cites them. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10422 | RWB-P5-E2025-CON | GAP-1713 | find it | Map each FEAT prerequisite to its owning service contract (P7, P3, P5, P6, S1) once; carry the duplicate FEAT-CHO-08 as written. |

### RWB-P5-E1025-APP; parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10424 | RWB-P5-E2025-CON | GAP-1020 | 11 | Apply the DOCTYPE-2026.12 load through the RWB-P5-E1025-APP type table and hold EXTRACT_ACCURACY_PASS in document_hub_parameter; confirm field names with S4 and S2 before wave 2. |

### OTHER:Wave 2 harness pack (QA) with the P5 and P10 owners (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10426 | RWB-P5-E2025-CON | GAP-0407 | find it | Agree the classifier version, masked sample pack, DOCTYPE-2026.12 SIT seeding, evidence format and pass gate with P5, P10 and QA. |

### OTHER:rwb-treatment (S2) service contract and Flyway sequence (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10428 | RWB-P5-E2025-CON | GAP-1876 | 11 | Add contract_amount, contract_date, mortgage_amount, registration_date, land_office, title_doc_no and the source columns to treatment with the TSD S2 T3.1 conventions. |

### OTHER:S4 litigation story (legal_action mapping) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10430 | RWB-P5-E2025-CON | GAP-1901 |  | Map only the seven same-name pairs; record filing_date to filed_date as one name-difference mapping; leave the eleven unmatched codes, party_names, notice_date, hearing_type and lawsuit_no unmapped with their gap. |

### OTHER:Treatment (S2) story of the legacy RWB-E2-025 key (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10431 | RWB-P5-E2025-CON | GAP-2702 |  | Apply the checked-field read from the RWB-P5-E2025-CON contract, add the fact and source columns on the service Flyway sequence, map only same-name codes, stamp tableVersion, and mask party_names. |

### OTHER:Litigation (S4) story of the legacy RWB-E2-025 key (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10433 | RWB-P5-E2025-CON | GAP-2835 |  | Build against the RWB-P5-E2025-CON contract; add source_document_id, source_doc_version and source_table_version to legal_action; map only same-name codes; record the twelve unmapped codes in the apply result. |

### OTHER:S4 litigation story (rwb-litigation API and data design) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10435 | RWB-P5-E2025-CON | GAP-1903 |  | Fix the fill trigger as the document type in the request; derive the write key from action, type, document versions and values; make one hearing per action and date a DB uniqueness rule; take parameter and list calls from RWB-P3-E1042-CON and RWB-P3-E1043-CON. |

### RWB-P10-E1062-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10436 | RWB-P5-E2025-CON | GAP-0627 |  | Read facts, OCR text and checklist through the RWB-P5-E2025-CON contract with one hop and 2 s budget; mask field values before the model call; reach run start on POST /agent-runs per RWB-P10-E1062-CON; read minimum sample and promotion list from rwb-case parameters at load time. |

### OTHER:Legal document agent app slice story in rwb-agent (TSD P10 Agent runtime v2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10437 | RWB-P5-E2025-CON | GAP-2196 |  | Name the paths below /api/recovery/document/v1 for the three document reads, the by-case legal-action read path and member names, the parameter and list codes, the gateway-bff route, the pack and run answer member types, and the service login, settled with the owners before Done. This story has no such operations. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10446 | RWB-P5-E2025-OPS | DOR-RWB-P5-E2025-OPS-10 | 12, 15 | Empty, error and no-access states of SCR-30 and SCR-31 recorded as Not specified; section 12 no longer asserts them. |

### OTHER:FSD S2 (A2.18.2; OTHER:A2.15.2; OTHER:A2.8.3.1) and the S2 treatment story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10460 | RWB-P5-E2025-OPS | GAP-1704 | n/a | Route generation, review and signature through the P5 and P6 contracts, hold only the document reference on the treatment, and keep no content in rwb_treatment. |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10463 | RWB-P5-E2026-APP | DOR-RWB-P5-E2026-APP-21 |  | Set build status to Done once the contract is published. |

### RWB-P7-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10464 | RWB-P5-E2026-APP | DOR-RWB-P5-E2026-APP-22 | 12.8 | Publish the rwb-decision central ledger fake library version and record it as published. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10467 | RWB-P5-E2026-APP | DOR-RWB-P5-E2026-APP-8 | header | Align the P2 payload of rwb.document.DocumentStored.v1 to the Kafka Catalog v1 definition. |

### OTHER:Template catalog and QA harness pack (P6 and P5 owners; OTHER:QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10471 | RWB-P5-E2026-APP | GAP-0408 | 16 | Agree template fixtures for the four template codes, the PDF/A-2b check, the Thai font pack, merge snapshot method, SIT seeding and evidence format and retention. |

### OTHER:PM-2026.12 policy pack load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10472 | RWB-P5-E2026-APP | GAP-0937 | 2 | Carry Documents C for RW-RESTRUCT, RW-CASEOWN and SY-CASEWF, Documents R for RW-TEAMMGR, and no row for RW-PHONECOL; confirm at policy pack review. |

### OTHER:PM-2026.12 policy pack and reference data load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10473 | RWB-P5-E2026-APP | GAP-0939 | 2 | Add SY-CASEWF with role_class NON_HUMAN_ACTOR, DOCUMENTS C and default_scope ALL, recorded in the reference data load with its own approver. |

### OTHER:TSD S2 T3.1 and rwb_treatment schema (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10474 | RWB-P5-E2026-APP | GAP-1878 | 12.3 | Add two nullable treatment columns for the document reference and the pinned template version, with an index, and take the generation operation from RWB-P5-E2026-CON. |

### OTHER:FSD P5 v3 S2 A2.18.2; OTHER:A2.15.2; OTHER:A2.8.3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10477 | RWB-P5-E2026-APP | GAP-1704 | 1 | Restate the document integration points as rwb-document and rwb-comms contracts (P5 and P6 generation, review and signature) and remove the Workbench document hub. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P5 API-P5-016; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10478 | RWB-P5-E2026-APP | GAP-1024 | 8 | Declare POST /cases/{caseId}/generated-documents as the path and record slide 16 name as loser (ASM-115); publish the four provider interfaces as typed contracts; declare one event with five payload fields (ASM-111 to ASM-113). |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10480 | RWB-P5-E2026-APP | GAP-1288 | header | Carry the store baseline and the rwb-access authorise contract as DP-added dependencies; keep Ready to start as Day 1. Header metadata already lists the six H and two C dependencies. |

### OTHER:Wave 2 harness pack and template fixtures (P5 and P6 owners; OTHER:QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10490 | RWB-P5-E2026-CON | GAP-0408 |  | Agree template fixtures for DIL-CONTRACT, DIL-CA, DIL-MORTGAGE, RES-AGREEMENT, PDF/A-2b check, Thai font pack, merge snapshot method, SIT seeding and evidence format with owners. |

### OTHER:Policy pack PM-2026.12 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10491 | RWB-P5-E2026-CON | GAP-0937 |  | Load Documents letters: C for RW-RESTRUCT, RW-CASEOWN and SY-CASEWF; R for RW-TEAMMGR; no row for RW-PHONECOL. Confirm at policy pack review. |

### OTHER:Policy pack PM-2026.12 and reference data load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10492 | RWB-P5-E2026-CON | GAP-0939 |  | Add SY-CASEWF role row with role_class NON_HUMAN_ACTOR, DOCUMENTS C and default_scope ALL, recorded in the reference data load with its own approver. |

### OTHER:TSD S2 v2 T3.1 (rwb-treatment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10493 | RWB-P5-E2026-CON | GAP-1878 |  | Add two nullable treatment columns (document reference and pinned template version) with an index. Keep the generation operation and event name as this story's design until the event catalogue owner confirms. |

### RWB-S2-E2026-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10495 | RWB-P5-E2026-CON | GAP-2684 |  | Apply working read of ASM-B2-S2-013-1 to -3: set composed per treatment type from catalogue value; rendering via generateContractDocument; party set as keys and count; case status via parent signal; outcome in answer and decision record. |

### OTHER:TSD P5 Document hub v2 (T-A.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10497 | RWB-P5-E2026-CON | GAP-2348 | find it | Name the request and reason fields of GenerateRequest and RegenerateRequest and the answer shape; RWB-PLT-DB to fix the login names; document type load to publish the container name, MSG-P5-006 text, index, flag and step name. |

### OTHER:FSD P5 Document hub (A2.18.2; OTHER:A2.15.2; OTHER:A2.8.3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10498 | RWB-P5-E2026-CON | GAP-1704 | find it | Replace the Workbench document hub with rwb-document and rwb-comms per Architecture v5 slide 41; request generation, review and signature through the P5 and P6 contracts; hold the document reference on the treatment; keep no document content in rwb_treatment. |

### OTHER:Harness README (wave 2 entry check) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10508 | RWB-P5-E2030-APP | GAP-0412 | 16 | Record the harness environment, the two fixtures, the model stub, the evidence format and the pass gate at the wave 2 entry check. |

### OTHER:Functional Specification P5 (FSD P5); OTHER:A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10511 | RWB-P5-E2030-APP | GAP-2359 | 7 | State the case type to stage and route mapping in A2.16, or add case type as a key of the checklist, and name the version of the 9-item litigation checklist. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10512 | RWB-P5-E2030-APP | GAP-2360 | 12.2 | Fix the DocumentChecklist schema of API-P5-008 with per-item fields, document list per item and completeness reference. |

### OTHER:Business Requirements Program (BRD) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10515 | RWB-P5-E2030-APP | GAP-2362 | 18 | Name the BRD section and L3 process of REQ-DCM-011 so the section 18 traceability row can be completed. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0068 | Wave conflict S4 / EP02 | Tech lead | Resolved (directive) |
| GAP-0406 | The field-capture harness pack, the mobile capture fixtures and the intake test profile are not specified | Integration lead | Resolved (directive) |
| GAP-0407 | The extraction harness pack, the classifier version and the cross-service reader pack are not specified | Integration lead | Resolved (directive) |
| GAP-0408 | The generation harness pack, the template fixtures and the PDF/A conformance check are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0412 | Harness environment, seed fixtures, model stub, evidence format and pass gate for the legal document agent shadow journey are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0627 | The app slice of the legal document agent in shadow: the document, OCR-text and checklist operations and members, the legal-action read, the run-start path, the parameter keys, the service login, the route, the BRD section of REQ-DCM-011 and the pack member types are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0628 | The contract baseline of the legal document agent: the OCR-text and checklist operations and member names, the legal-action read, the run-start path, the route, the paging and member types, and the event family beyond EV-28 are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0937 | The Documents letters per role are not in the P4 RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0938 | The authorise request and answer for a document generation request are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0939 | The role row, class and scope of the SY-CASEWF service identity are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0949 | The Documents letters per role are not carried by the P4 access documents | Security administrator with the P4 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0951 | Whether the field app reaches the authorise path through gateway-bff or directly is not specified | Solution architect, P4 with the gateway-bff route owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0952 | The request and answer shape of the authorise call for a multi-item sync is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0998 | The pipeline publishes a third event name on rwb.document.events.v1 while the architecture catalogue lists two events for rwb-document | Solution architect | Resolved (directive) |
| GAP-1003 | No source names a classification operation, path or field-level name, a 404 message identifier is absent, and a classification event would be a third event for rwb-document | Solution architect with the TechX contract owner of rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1018 | Field capture: the store capture block, the intake submit path, the parameter and list names, the service login name and the approval status are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1019 | Field capture contract: the manifest part and item field names, the stored-answer window, the not-found message and the 415 reading are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1021 | The published Java reader becomes a REST contract no source names, the extraction operations belong to another baseline of the same service, and the plan lists no C row for the case read | Tech lead | Resolved (directive) |
| GAP-1022 | The deployment values of the extension are not specified: the model name and the provider product behind the agent route, the alert thresholds and identifiers, the evaluation cadence, the business-hours window and the reader thresholds | DevOps team | Resolved (directive) |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1024 | The generation contract baseline has no settled operation name, no published provider shapes and two consumed contracts outside the plan | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1283 | The decision code of a field-capture entry is D6.5 in the legacy metadata but DOCATT on the store path | Business analyst, P7, with the business analyst of P5 rwb-document and the data steward | Resolved (directive) |
| GAP-1284 | No source settles whether an item the store refuses leaves a DOCATT entry | Business analyst, P7, with the P5 business analyst and the integration lead of RWB-ITG-E2024-ITG | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1289 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Solution architect, with the platform team and the P7 rwb-decision owner | Resolved (directive) |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1876 | The checked-fields operation and payload on the treatment side, the treatment columns that carry the contract and mortgage facts, the masking of the treatment read and who stamps the type-table version are not specified | Solution architect with the rwb-treatment and rwb-document squads | Resolved (directive) |
| GAP-1877 | Architecture v5 puts the S2 call to P5 in the Temporal column while the legacy published interface and DP-11 make the checked-fields read one REST hop | Solution architect with the platform workflow team, rwb-document and rwb-treatment | Resolved (directive) |
| GAP-1878 | The treatment-side generation call, its two columns, the merge-field set and the generation event are not specified | Solution architect | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1899 | DP-09 and DP-10 are in the pattern list but this slice produces no event, consumes no event and registers no Schedule, and DocumentFieldsExtracted is consumed by rwb-case only | Solution architect | Resolved (directive) |
| GAP-1900 | The sources give only the Java interface of the field reader: no REST operation, path, transport or field-level name is named for the checked-fields read | Solution architect, with the rwb-document owner (P5) | Resolved (directive) |
| GAP-1901 | The mapping of an extracted field code onto an S4 column is not stated, and eleven codes, hearing_type and lawsuit_no have no counterpart of the same name | Business analyst and solution architect, with the rwb-document owner | Resolved (directive) |
| GAP-1902 | REQ-DCM-017 and REQ-DCM-018 are in the plan's requirement list for this story but in no row of the legacy traceability table, and legacy section 19 puts them out of scope | Business analyst | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1904 | SCR-19 Litigation workspace is listed with its first release in E5, while this story is a wave 2 story released on 31 December 2026 | Solution architect and the edge owner | Resolved (directive) |
| GAP-1905 | No approval of the realigned story or of the sources it consumes is recorded, so the story runs in Draft | Solution architect | Resolved (directive) |
| GAP-2196 | Legal document agent in shadow in rwb-agent (app slice): the consumed operation paths below the rwb-document base, the legal-action read path, the parameter codes and the list codes, the gateway-bff route path, the member types of the pack and of the run answer, and the service login are not specified | Solution architect with the owners of rwb-document, rwb-litigation and rwb-case, and the platform library owner for the route | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2197 | Legal document agent in shadow in rwb-agent (contract slice): the run-start path below the agent base, the consumed boundary paths and field names, the six policy members beyond the baseline, the member types of the pack and the score row, and the gateway-bff route path are not specified | Solution architect with the owners of rwb-document, rwb-litigation and rwb-case, and the platform library owner for the route | Resolved (directive) |
| GAP-2223 | The case-side slice of the field-capture path rests on answers no source specifies: the stage and route fields of the case resource, the authorise call shape, the contract story of the checklist read, and the task data | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2344 | The dependency rows of this slice name one contract only, and the request field names, the reason field, the index name and the migration step name are not specified | Solution architect, with the P5 TechX squad | Resolved (directive) |
| GAP-2348 | The rwb-document login, the request and answer field names of the generation path, the message text of MSG-P5-006, the container name, the index name, the Flyway step name and the P5 feature flag are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2350 | The dependency rows of this slice name one contract only, while the pattern set names five platform contracts, the rwb-case reference-data contract and the generation contract of the service | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2358 | The rwb-agent tool call, per-item field names and unavailable-read mapping behind RWB-P10-E2030-CON | Solution architect | Resolved (directive) |
| GAP-2359 | The checklist is keyed by stage and route while the legacy asks for the checklist of a case type | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2360 | The per-item fields of the document checklist answer the pack reader needs | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2361 | The defect status of a checklist item and the evidence it needs on the hub side | Business analyst, P5 | Resolved (directive) |
| GAP-2362 | The BRD section and L3 process of REQ-DCM-011 | Business analyst, programme | Resolved (directive) |
| GAP-2393 | rwb-comms generation request key and P5 document-create operation are not specified | Service owner, rwb-comms; service owner, rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2394 | Generated-documents endpoint is not in the P6 operation inventory | Architecture owner; service owner, rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2684 | The document-set result, the rendering hand-off, the party set and the case trigger are not specified for rwb-treatment | Tech lead of rwb-treatment with the P5 owner of the document contract, the P6 owner of the template catalogue and the P3 owner of the case contract | Resolved (directive) |
| GAP-2702 | The treatment-side checked-field read, the fact columns it fills, the type-table version stamp and the unmapped field codes are not specified | Tech lead of rwb-treatment with the P5 owner of the checked-field contract and the rwb-treatment data owner | Resolved (directive) |
| GAP-2703 | Architecture v5 puts the S2 read of rwb-document on Temporal while the legacy interface and DP-11 make it one REST hop | Solution architect with the P5 contract owner and the platform Temporal owner | Resolved (directive) |
| GAP-2835 | The litigation-side checked-field read, the fact columns it fills on legal_action and hearing, the source stamps and the unmapped field codes are not specified | Tech lead of rwb-litigation with the P5 owner of the checked-field contract and the rwb-litigation data owner | Resolved (directive) |
| GAP-2836 | No source says how an extracted hearing_date becomes a hearing row, which hearing_type that row carries, or what the apply does to an action in a closed status | Litigation business analyst with the rwb-litigation data owner and the S4 hearing story owner | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
