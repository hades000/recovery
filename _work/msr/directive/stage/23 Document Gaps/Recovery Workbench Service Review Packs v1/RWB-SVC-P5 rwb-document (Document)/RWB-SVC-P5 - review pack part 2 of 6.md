# RWB-SVC-P5 rwb-document (Document) - review pack, part 2 of 6 (RWB-P5-E1025-APP to RWB-P5-E1040-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 196 |
| Cross-document (pending in another document) | 198 |
| Not applied (value not in the sources) | 24 |
| Open business decisions | 21 |
| Register gaps linked | 75 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P5-E1025-APP | 21 | 8 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1025 APP Document types and fields agreed v2.md |
| RWB-P5-E1026-APP | 16 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1026 APP Attach and search screen v2.md |
| RWB-P5-E1032-APP | 33 | 37 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1032 APP Automatic attach from the OCR intake v2.md |
| RWB-P5-E1032-CON | 17 | 39 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1032 CON Automatic attach from the OCR intake - contract v2.md |
| RWB-P5-E1032-INF | 28 | 29 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1032 INF Automatic attach from the OCR intake - infrastructure v2.md |
| RWB-P5-E1032-OPS | 26 | 33 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1032 OPS Automatic attach from the OCR intake - deployment v2.md |
| RWB-P5-E1033-APP | 17 | 9 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1033 APP Search across cases v2.md |
| RWB-P5-E1039-APP | 21 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1039 APP Access log into the decision log and break-glass admin v2.md |
| RWB-P5-E1040-APP | 17 | 12 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1040 APP Document checklist per case type as reference data v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1025-ITG, RWB-P5-E1025-APP, RWB-P5-E1053-APP, RWB-P5-E1053-CON | R-09182 | GAP-1585 | Register gap | Business lead with Legal counsel and the Head of NPA | The six document types are counted at 26 fields but only two types name their fields | FR-P5-011 and FR-P5-016 require the full field list to be delivered as the signed reference load and this PRD requires the count to reconcile, not a specific list. OQ-P5-01 and OQ-P5-14 carry the question. |
| RWB-P5-E1025-APP | R-10846 | CG-ALL-5805 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1032-APP | R-10849 | CG-ALL-5824 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1032-APP | R-10850 | CG-ALL-5829 | Script gap | Product owner | Open decision DL21 has no assumption | Owner rules DL21; until then build on the recommended option. |
| RWB-P5-E1032-CON | R-10852 | CG-ALL-5838 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1033-APP | R-10858 | CG-ALL-5855 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-22113 | GAP-1570 | Register gap | Compliance with the solution architect | The access log has no stated retention, no stated searchable period, no stated storage object and no stated cross-service read right, although it is the evidence for every access question | Answer DL26 for the access log in one row: the retention period, whether it equals the decision log period, which object answers the query (the local record, the central ledger, or a projection of both), which fields are searchable and for how far back, and which roles in other services may read it. Until then this PRD keeps the classification at PII and marks the retention as not set. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1025-APP, RWB-P5-E1052-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-22159 | GAP-2347 | Register gap | Data steward and document type owner, with the Legal counsel and the P5 TechX squad | The notice-type to document-type mapping, the retention class and the write-once flag of each notice document type are not specified in any source read here | The document type load of RWB-P5-E1025-APP carries the DEMAND_LETTER and GUARANTOR_NOTICE rows with their class and flag, and the notice-type mapping row is added to the type or mapping table before the wave-1 test data is loaded |
| RWB-ITG-E1025-ITG, RWB-P5-E1025-APP | R-28545 | GAP-1040 | Register gap | Business lead with Legal | No role holds Reference data A to approve a document-type load | Decide in DL01 which role holds Reference data A for the document-type table (the assumed answer is the legal counsel who owns the table) and record it in the rwb-access permission matrix; if the Head of NPA is intended as the approver, grant the right there instead |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28588 | GAP-1576 | Register gap | Compliance with the solution architect | REQ-ACA-006 still requires an access entry for every read of the data lake copy, which Architecture v5 removes | Re-issue REQ-ACA-006 and NFR-042 in the next business requirement version as 'every read of the case store, the document store and a data product', so the requirement, the functional specification and this PRD use one list of objects; nothing else in the requirement changes. |
| RWB-ITG-E1039-ITG, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28591 | GAP-1591 | Register gap | Compliance and PDPA officer | NFR-042 still requires logging the data lake copy of the document store although the data lake is removed | The PRD requires every read of a document and of its extracted fields to be logged and carries no lake clause. NFR-042 needs the same correction in its next version. |
| RWB-P5-E1040-APP | R-28995 | GAP-2338 | Register gap | Legal counsel as checklist co-owner, with the reference data administrator | No role holds Reference data A to approve the checklist load, and the items of checklist CHK-2026.11 are assumed until the bank list is signed | The permission matrix grants Reference data A to the legal counsel or a named approver role before go-live, and the signed bank checklist replaces CHK-2026.11 as a new version with its own valid-from date |
| RWB-P5-E1032-APP | R-33450 | ASM-ALL-5829 | Script assumption |  | Built on the recommended option of DL21: A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead rules DL21 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1019-ITG, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P4-E1022-APP, RWB-P5-E1025-APP, RWB-P5-E1025-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP | R-35406 | ASM-1988 | Register assumption |  | The approver of a document-type load is the legal counsel who owns the type table, holding Reference data A, as the legacy story assumes under DL01; the loader holds Reference data C and may not approve | Business lead with Legal confirms the role that approves the type list |
| RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1034-ITG, RWB-PLT-TE012-APP, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1041-APP, RWB-P6-AD017-APP, RWB-P6-E1034-APP | R-35419 | ASM-2709 | Register assumption |  | The values of the Non-Functional Specification v3 are the values this PRD is written against, with the status each one carries. A value marked Proposed is used as written until its owner confirms it under the decision named; a value marked Open is recorded as not set. | Solution architect with Risk at DL11 |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P5-E1040-APP | R-36958 | ASM-3890 | Register assumption |  | The checklist rows of version CHK-2026.11 and the approval of every load are carried from the legacy story as they stand, with the approval right A exercised by the legal counsel as co-owner of the checklist until the permission matrix grants it. | Legal counsel confirms the bank checklist and the approver role holds Reference data A |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P5-E1025-APP | R-10845 | CG-ALL-5803 | 14 | MSG-P3-027 text differs from the Error and Message Standard v4 | Standard v4 text not confirmed in this chunk; placeholder substitution is not supported by any source. |
| RWB-P5-E1032-APP | R-06126 | DOR-RWB-P5-E1032-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the chunk or the sources searched by Grep. Sign-off cannot be confirmed without inventing it. Needs the epic design record. |
| RWB-P5-E1032-APP | R-17147 | DOR-RWB-P5-E1032-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-30 and SCR-31 empty, loading, error and no-access state text is not in the chunk or the sources searched. Writing it would invent it. |
| RWB-P5-E1032-APP | R-17148 | DOR-RWB-P5-E1032-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The list of fields classed as personal data is not in the chunk or the sources searched. The story cannot be corrected without it. |
| RWB-P5-E1032-APP | R-25744 | CG-ALL-5825 | 3 | Flyway file V1032_1__intake_match.sql is not in the V0001..Vnnnn form | Story line 453 has no V1032_1 name in the chunk, and the service Flyway next number is not in the sources. Cannot rename without inventing a number (Solution architect). |
| RWB-P5-E1032-CON | R-22065 | GAP-2444 | 11, 12.3 | DOCATT attach entry has no defined field set for the document reference, the intake item, the match method, the confidence, the final call and the message id | Sections 11 and 12.3 are not in the chunk, so the DOCATT field mapping cannot be written. Re-issue with those sections. Migration V1032_1 is outside this story. |
| RWB-P5-E1032-CON | R-22075 | GAP-2448 | 13 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Header metadata rows already list the DP-table contracts and are kept. The section 13 record is not in the chunk. Re-issue with section 13. |
| RWB-P5-E1032-CON | R-28564 | GAP-0747 | not identified in chunk | Decision code and final call for the case document link are not specified | No decision code or final call for the case-side link is in the sources. Needs decision log owner agreement (RW-COE). Touched section not in chunk. |
| RWB-P5-E1032-CON | R-28566 | GAP-0994 | 12 | The Schedule window, the catch-up policy, the alert thresholds and the lag-alert identifier of the intake path are not specified | Section 12 schedule, thresholds and lag-alert text are not in the chunk. The business-hours window value is not in the sources. Re-issue with section 12. |
| RWB-P5-E1032-CON | R-28569 | GAP-2446 | 7, 16 | Whether an item held for a person leaves a decision record is not stated | Section 7 AC text is not in the chunk, so the new no-DOCATT criterion and its section 16 test row cannot be placed. Re-issue with section 7. |
| RWB-P5-E1032-CON | R-28570 | GAP-2449 | P7 sections not identified in chunk | Login name, parameter names and message texts are not written in any source readable here | Touched P7 sections are not in the chunk. Login phrase, parameter placeholders and MSG-P7-009 and MSG-GEN-006 texts cannot be applied here. Re-issue with those sections. |
| RWB-P5-E1032-CON | R-28571 | GAP-2450 | 12 | The trigger of the ledger completeness check is not stated | The section 12 job table is not in the chunk, so the ledger check trigger cannot be edited. Re-issue with the touched job text. |
| RWB-P5-E1032-INF | R-28564 | GAP-0747 | find it | Decision code and final call for the case document link are not specified | Story body text for the case-record section was not in this chunk, so no exact anchor exists. Searched the INF story and found no copy; no edit made. Resend with the section text. |
| RWB-P5-E1032-OPS | R-00663 | CG-ALL-3425 | 12.1 | Status 'Active' in the state table is not a value of LOV-CASE-STATUS | Not an item of this chunk; no change made here. |
| RWB-P5-E1032-OPS | R-17173 | DOR-RWB-P5-E1032-OPS-10 |  | Definition of Ready item 10 Screens and states: Partial | Screen-state text for SCR-31 and SCR-44 is outside this chunk and no anchor is available. Checked this story's output and the source docs; no screen-state text found. Needs the sections. |
| RWB-P5-E1033-APP | R-25760 | CG-ALL-5856 | 3 | Flyway file V1_5_033__document_search_indexes.sql is not in the V0001..Vnnnn form | Not specified in the source documents (CG-ALL-5856): Service Template Spec v1 §3.1 gives the V0001 to Vnnnn rule only, with no next free rwb-document number. V0002 is already claimed by E1025 and E1046. |
| RWB-P5-E1033-APP | R-25761 | CG-ALL-5857 | 3 | Flyway file V1033_1__document_search_indexes.sql is not in the V0001..Vnnnn form | Not specified in the source documents (CG-ALL-5857): Service Template Spec v1 §3.1 gives the V0001 to Vnnnn rule only, with no next free rwb-document number. V0002 is already claimed by E1025 and E1046. |
| RWB-P5-E1039-APP | R-28593 | GAP-2340 | 7 | The capability-area code, the result code and the field list of a document content read in an access entry are not specified | The field list of the content-read entry stays Not specified in the source documents (GAP-2340). |
| RWB-P5-E1039-APP | R-31122 | DOR-RWB-P5-E1039-APP-AC11 | 7, 16 | AC11: §8 BR7, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | BR7 and BR9 text is not in this chunk (R-17191); no criterion or test added. Needs that chunk. |
| RWB-P5-E1040-APP | R-06158 | DOR-RWB-P5-E1040-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources. Searched the story and sources again; the sign-off reference is not specified, so none was written. |
| RWB-P5-E1040-APP | R-17193 | DOR-RWB-P5-E1040-APP-10 | find it | Definition of Ready item 10 Screens and states: Partial | States for SCR-02 and SCR-30 are in section 8, outside this chunk. No source text for those states was found, so none was added. |
| RWB-P5-E1040-APP | R-17195 | DOR-RWB-P5-E1040-APP-15 | header | Definition of Ready item 15 INVEST: Partial | The size value is not in the sources, so INVEST sizing stays open until the squad confirms it. |
| RWB-P5-E1040-APP | R-23225 | GAP-2760 | 3 | Three consumed contracts of the pack-recovery step have no dependency row, and the plan gives the two stories no contract or integration dependency | Two of three consumed rows added (checklist read, case-move answer). The third contract's row is still missing and needs its source; metadata rows unchanged. The Dependency Map in 12.2 is outside this chunk. |
| RWB-P5-E1040-APP | R-25769 | CG-ALL-5870 | 3, 3.1 | Flyway file V1_5_040__document_checklist.sql is not in the V0001..Vnnnn form | Next V-number of the rwb-document Flyway sequence is not in the sources (Service Template Spec v1 §3.1 gives no value). Migration name sits outside this chunk. No number invented. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09615 | RWB-P5-E1025-APP | CG-ALL-5804 | 18 | Align the REQ-DCM-004 test case list in RTM v7 with section 18 of RWB-P5-E1025-APP in the next RTM version. |
| CDC-09629 | RWB-P5-E1026-APP | CG-ALL-5811 | 18 | Align the test-case trace rows of the four differing requirements (REQ-DCM-008, REQ-DCM-001 and two more) to section 18 of RWB-P5-E1026-APP. |
| CDC-09656 | RWB-P5-E1032-APP | GAP-3144 | none | Record the primary and secondary AC split so AC1 to AC15 are counted once against RWB-P5-E1032-APP. |
| CDC-09660 | RWB-P5-E1032-APP | CG-ALL-5823 | 18 | Align the REQ-DCM-005 and REQ-DCM-007 test lists in the RTM to the section 18 test cases of this story. |
| CDC-09694 | RWB-P5-E1032-CON | GAP-3144 | 7 | Record the primary and secondary AC split so AC1 to AC15 are counted once against RWB-P5-E1032-APP and the seven new criteria are recorded against this story. |
| CDC-09697 | RWB-P5-E1032-CON | CG-ALL-5837 | 18 | Align the REQ-DCM-007 and REQ-DCM-005 test lists to RWB-P5-E1032-CON section 18 in the next RTM version. |
| CDC-09726 | RWB-P5-E1032-INF | GAP-3144 |  | Record the primary and secondary AC split so the fifteen legacy criteria are counted once, against RWB-P5-E1032-APP. |
| CDC-09774 | RWB-P5-E1033-APP | DOR-RWB-P5-E1033-APP-12 | 16 | Test rows added in section 16 for AC11 to AC15 and contract tests; no story edit to section 18. |
| CDC-09777 | RWB-P5-E1033-APP | CG-ALL-5854 | 18 | Align the REQ-DCM-001 and REQ-ACA-006 test lists with RWB-P5-E1033-APP §18 in the next RTM version. |
| CDC-09779 | RWB-P5-E1039-APP | DOR-RWB-P5-E1039-APP-12 | 16 | Align the REQ-ACA-006 and REQ-ACA-008 test lists with section 18 of RWB-P5-E1039-APP, or the reverse. |
| CDC-09788 | RWB-P5-E1039-APP | CG-ALL-5860 | 18 | Align the test lists of REQ-ACA-006 and REQ-ACA-008 with RWB-P5-E1039-APP section 18 in the next RTM version. |
| CDC-09806 | RWB-P5-E1040-APP | CG-ALL-5869 | 18 | Align the REQ-DCM-011 test cases with RWB-P5-E1040-APP section 18 in the next RTM version. |

### RWB-P5-E1032-CON (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09638 | RWB-P5-E1032-APP | DOR-RWB-P5-E1032-APP-21 | header | Set build status to Done once the contract is published. |
| CDC-09641 | RWB-P5-E1032-APP | GAP-0992 | find it | Add the two rwb-case case reads to the C list; fix the four shapes as the smallest superset of the legacy list; declare the four consumed rows with fakes; keep unnamed elements behind the placeholder until confirmed. |
| CDC-09644 | RWB-P5-E1032-APP | GAP-1197 |  | Publish the request and answer of POST /cases/{caseId}/generated-documents, including the intake item created; name the document type and source for a notice letter copy; register the notice parameters; extend the rwb.comms.NoticeGenerated.v1 row to its payload; allocate the notice screen identifier. |
| CDC-09650 | RWB-P5-E1032-APP | GAP-2447 |  | Define the fact keyed by caseId with decisionCode, caseId, documentId, intakeItemId, matchMethod, classifierVersion, confidence, approverUserId, finalCall, messageId and inputsRef; no OCR text, file or account number; refuse a fact without a document reference. |
| CDC-09708 | RWB-P5-E1032-INF | DOR-RWB-P5-E1032-INF-21 | header | Complete the build and publish the contract so its build status is Done. |
| CDC-09711 | RWB-P5-E1032-INF | DOR-RWB-P5-E1032-INF-10 | 14 | Define the empty, loading, error and no-access states of SCR-31 Document review queue |
| CDC-09712 | RWB-P5-E1032-INF | GAP-0992 | n/a | Add the two rwb-case case reads the baseline consumes to the C list; fix the four shapes as the smallest superset of the legacy section 12 list, with fakes; keep unnamed elements behind the placeholder. |
| CDC-09729 | RWB-P5-E1032-INF | CG-ALL-5843 | 15 | SCR-31 state paragraph removed from this infrastructure story |
| CDC-09743 | RWB-P5-E1032-OPS | GAP-0992 | find it | Fix the four shapes as the smallest superset of the legacy list, keep unnamed elements behind the placeholder, and add the two rwb-case case reads the baseline consumes to the C list. |
| CDC-09752 | RWB-P5-E1032-OPS | GAP-2447 | 12.3 | Define the DecisionRecorded fact keyed by caseId with decisionCode, caseId, documentId, intakeItemId, matchMethod, classifierVersion, confidence, approverUserId, finalCall, messageId and inputsRef; refuse a fact without a document reference. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09631 | RWB-P5-E1032-APP | CG-ALL-5816 | 12.1 | Publish POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve through RWB-P5-E1032-CON. |
| CDC-09632 | RWB-P5-E1032-APP | CG-ALL-5817 | 12.1 | Publish GET /api/recovery/document/v1/intake-items through RWB-P5-E1032-CON. |
| CDC-09633 | RWB-P5-E1032-APP | CG-ALL-5818 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId} through RWB-P5-E1032-CON. |
| CDC-09634 | RWB-P5-E1032-APP | CG-ALL-5819 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/content through RWB-P5-E1032-CON. |
| CDC-09636 | RWB-P5-E1032-APP | CG-ALL-5821 | 12.2 | Remove the fixed enum on reviewStatus so LOV-REVIEW values are read as data. |
| CDC-09639 | RWB-P5-E1032-APP | DOR-RWB-P5-E1032-APP-8 | 12.1 | Add the paths named in 12.1 (POST intake-items/{intakeItemId}/resolve, GET intake-items, GET intake-items/{intakeItemId}, GET intake-items/{intakeItemId}/content and the three more listed) and the Idempotency-Key header on resolve |
| CDC-09668 | RWB-P5-E1032-CON | CG-ALL-5830 | 12.1 | Publish GET /api/recovery/document/v1/intake-items through the CON story of rwb-document, or remove the operation from this story. |
| CDC-09736 | RWB-P5-E1032-OPS | CG-ALL-5845 | 12.1 | Publish GET /api/recovery/document/v1/intake-items, GET /api/recovery/document/v1/intake-items/{intakeItemId}, GET /api/recovery/document/v1/intake-items/{intakeItemId}/content and POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve through RWB-P5-E1032-CON. |

### RWB-P3-E1043-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09661 | RWB-P5-E1032-APP | GAP-0746 | find it | Hold the case review task code, element type and task status values as reference data and load them before the review queue story starts. |
| CDC-09698 | RWB-P5-E1032-CON | GAP-0746 | Header | Hold the document review task code, element type and task status values as reference data and load them with RWB-P3-E1043-CON before the review queue story starts. |
| CDC-09730 | RWB-P5-E1032-INF | GAP-0746 |  | Hold the case review task code, element type and task status values as reference data and load them before the review queue story starts. |
| CDC-09761 | RWB-P5-E1032-OPS | GAP-0746 |  | Hold the case review task code, element type and task status values as reference data in the rwb-case reference tables and load them before the review queue story starts. |
| CDC-09795 | RWB-P5-E1040-APP | DOR-RWB-P5-E1040-APP-21 | 1 | Publish the contract and bring the story to Done. |
| CDC-09796 | RWB-P5-E1040-APP | DOR-RWB-P5-E1040-APP-22 | 1 | Publish a fake library version for RWB-P3-E1043-CON and record it as published. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09610 | RWB-P5-E1025-APP | DOR-RWB-P5-E1025-APP-14 | Metadata | Record the signed epic design sign-off for EP01 with its date and reference it from this story. |
| CDC-09618 | RWB-P5-E1026-APP | DOR-RWB-P5-E1026-APP-14 |  | Record the signed epic design sign-off for EP01; no signed epic design is in the story or sources. |
| CDC-09672 | RWB-P5-E1032-CON | DOR-RWB-P5-E1032-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-P5 and EP01 in the epic design record. |
| CDC-09707 | RWB-P5-E1032-INF | DOR-RWB-P5-E1032-INF-14 | header | Record the signed epic design sign-off for this story's epic in the epic design record. |
| CDC-09769 | RWB-P5-E1033-APP | DOR-RWB-P5-E1033-APP-14 | none | Record the signed epic design sign-off for this epic in the epic design record. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09621 | RWB-P5-E1026-APP | CG-ALL-5810 | 4, 14 | Add a new message ID for 'A service this screen calls does not answer' so section 14 can cite it; MSG-GEN-006 stays as is. |
| CDC-09624 | RWB-P5-E1026-APP | DOR-RWB-P5-E1026-APP-9 | 14 | MSG-GEN-006 row restored to its original text; no scan-specific meaning added. |
| CDC-09674 | RWB-P5-E1032-CON | CG-ALL-5834 | 14 | Add a new message ID for 'No authenticated caller' so MSG-P4-001 keeps its standard meaning; the story then cites the new ID. |
| CDC-09678 | RWB-P5-E1032-CON | DOR-RWB-P5-E1032-CON-9 | 14 | State the meaning and text of MSG-P4-001 for no authenticated caller, or assign a new message ID for that condition. |
| CDC-09802 | RWB-P5-E1040-APP | DOR-RWB-P5-E1040-APP-9 | 14 | Set MSG-P3-027 text to: The {table} load was refused: {check}. The version in force is unchanged. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09637 | RWB-P5-E1032-APP | CG-ALL-5822 | 12.3 | Add rwb.document.DocumentAttached.v1 to the Events sheet. |
| CDC-09671 | RWB-P5-E1032-CON | CG-ALL-5833 | 12.3 | Add the event type rwb.document.DocumentAttached.v1 to the Events sheet of the catalog. |
| CDC-09797 | RWB-P5-E1040-APP | CG-ALL-5865 | 12.4 | Add rwb-document as a consumer of rwb.document.DocumentStored.v1 and add its ACL. |
| CDC-09798 | RWB-P5-E1040-APP | CG-ALL-5866 | 12.4 | Add rwb-document as a consumer of rwb.case.CaseStateChanged.v1 and add its ACL. |
| CDC-09801 | RWB-P5-E1040-APP | DOR-RWB-P5-E1040-APP-8 | 12 | Add rwb-document as a consumer of rwb.document.DocumentStored.v1 and of rwb.case.CaseStateChanged.v1 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09640 | RWB-P5-E1032-APP | CG-ALL-5815 | 9 | Record the uk_document_case_type_hash unique key (case, type, hash) as an object on the owning table, or give it a dictionary name |
| CDC-09642 | RWB-P5-E1032-APP | GAP-0742 | 11 | Row now holds Not specified placeholders for table name and field list |
| CDC-09680 | RWB-P5-E1032-CON | GAP-0742 | n/a | Add field IDs for rwb_case.case_document_link (case_id, document_id, checklist_state, extracted_field_count, linked_at, source_event_id) in the next data dictionary version. |
| CDC-09739 | RWB-P5-E1032-OPS | CG-ALL-5844 | 12.7 | Record decision_record as an object (PLT library table in schema rwb_document, created by library migrations) or use the dictionary name; the owning PLT library document must name it. |
| CDC-09745 | RWB-P5-E1032-OPS | GAP-0742 | 11 | Case document link row now states the table and field IDs are Not specified. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09643 | RWB-P5-E1032-APP | GAP-0991 | find it | Set API-P5-013 right to C with 201 Document answer; add rwb.document.DocumentAttached.v1 on rwb.document.events.v1 or confirm DocumentStored before wave 1 release. |
| CDC-09647 | RWB-P5-E1032-APP | GAP-1202 |  | Align the consumers of rwb.comms.NoticeGenerated.v1 to the call-edge reading the directive accepts: rwb-comms calls rwb-document to generate the letter, and the event is for rwb-decision only. |
| CDC-09681 | RWB-P5-E1032-CON | GAP-0991 | n/a | Declare rwb.document.DocumentAttached.v1 on rwb.document.events.v1 or confirm DocumentStored; also align TSD P5 API-P5-013 right to C per the attach operation. |
| CDC-09714 | RWB-P5-E1032-INF | GAP-0991 | n/a | Declare rwb.document.DocumentAttached.v1 on rwb.document.events.v1 or confirm DocumentStored before the wave 1 release; publish /resolve as the attach operation with the Documents right C and the 201 Document answer. |
| CDC-09746 | RWB-P5-E1032-OPS | GAP-0991 | 12 | Publish /intake-items/{intakeItemId}/resolve as the attach operation (right C, 201 Document answer), declare rwb.document.DocumentAttached.v1, and confirm or add the name before wave 1 release. |

### parameter-catalog.csv (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09664 | RWB-P5-E1032-APP | GAP-0745 | find it | Add a rwb-case parameter for the case-side switch, default on, owned by RW-COE; off means the case side writes nothing from an event. Key Not specified in the source documents (GAP-0745). |
| CDC-09701 | RWB-P5-E1032-CON | GAP-0745 | Header | Add a rwb-case parameter for the case-side switch: key Not specified in the source documents (GAP-0745), default on, owner RW-COE; off means the case side writes nothing from an event. |
| CDC-09703 | RWB-P5-E1032-CON | GAP-1200 | - | Add the business-owned notice values with defaults, or state that the module has none so DP-06 applies as a path without a value. |
| CDC-09733 | RWB-P5-E1032-INF | GAP-0745 |  | Add an rwb-case parameter for the case-side switch, default on, owner RW-COE; key Not specified in the source documents (GAP-0745) |
| CDC-09764 | RWB-P5-E1032-OPS | GAP-0745 |  | Add a rwb-case parameter for the case-side switch, default on, owned by RW-COE; off means the case side writes nothing from an event. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09696 | RWB-P5-E1032-CON | CG-ALL-5835 | 16 | Add rows TC-P5-E1032-CON-01 to TC-P5-E1032-CON-08 with Given, When and Then copied from AC1 to AC8 of this story. |
| CDC-09728 | RWB-P5-E1032-INF | CG-ALL-5842 | 16 | Add rows TC-P5-E1032-INF-01 to TC-P5-E1032-INF-06 with Given, When and Then copied from the criteria they cover. |
| CDC-09741 | RWB-P5-E1032-OPS | DOR-RWB-P5-E1032-OPS-12 | 12, 12.7, 16 | Add TC-P5-E1032-OPS-01 to -06 and the new -07 to -11 rows from section 16. |
| CDC-09760 | RWB-P5-E1032-OPS | CG-ALL-5848 | 16 | Add rows for TC-P5-E1032-OPS-01 to TC-P5-E1032-OPS-06 under Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-09799 | RWB-P5-E1040-APP | CG-ALL-5868 | 16 | Add rows for TC-E1-040-01-ITG, -02-ITG, -05-ITG, -08-ITG; Given, When, Then copied from AC1, AC2, AC5, AC8. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09742 | RWB-P5-E1032-OPS | DOR-RWB-P5-E1032-OPS-7 | 11 | Add decision_record (PLT library table created in rwb_document, written by the app story and the relay) as a field or entity. |
| CDC-09771 | RWB-P5-E1033-APP | CG-ALL-5852 | none | Record gin_trgm_ops as the pg_trgm operator class of the trigram index, or add it to the dictionary. |
| CDC-09772 | RWB-P5-E1033-APP | CG-ALL-5853 | none | Record dochub_to_numeric as the function created by V1_5_033 in the owning document, or add it to the dictionary. |
| CDC-09776 | RWB-P5-E1033-APP | DOR-RWB-P5-E1033-APP-7 | 11 | Register or confirm gin_trgm_ops and dochub_to_numeric as SQL objects of the rwb-document migration, since they are not fields or entities. |
| CDC-09778 | RWB-P5-E1039-APP | CG-ALL-5859 | 12.7 | Record break_glass_grant as an rwb-access object with its index, library table or flag, or use its dictionary name. No story edit. |

### OTHER:Contract fake library (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09612 | RWB-P5-E1025-APP | DOR-RWB-P5-E1025-APP-22 | Metadata | Publish the rwb-case reference-data fake and record its library version against RWB-P5-E1025-APP. |
| CDC-09620 | RWB-P5-E1026-APP | DOR-RWB-P5-E1026-APP-22 |  | Publish a contract fake library version and record it. Version not specified in the source documents (DOR-RWB-P5-E1026-APP-22). |
| CDC-09709 | RWB-P5-E1032-INF | DOR-RWB-P5-E1032-INF-22 | header | Publish a contract fake library version for rwb-document /v1 and record its version. |
| CDC-09770 | RWB-P5-E1033-APP | DOR-RWB-P5-E1033-APP-22 | none | Record the published version of the contract fake library this story uses. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09655 | RWB-P5-E1032-APP | GAP-3143 | none | Add partner_intake with its field IDs before the wave 1 entry check. |
| CDC-09693 | RWB-P5-E1032-CON | GAP-3143 | 11 | Add partner_intake to the LDM with field IDs and to the physical schema rwb_partner before the wave 1 entry check. |
| CDC-09725 | RWB-P5-E1032-INF | GAP-3143 |  | Add partner_intake with its field IDs and types before the wave 1 entry check. |
| CDC-09757 | RWB-P5-E1032-OPS | GAP-3143 |  | Add partner_intake to the LDM and the rwb_partner physical schema with its field IDs before the wave 1 entry check. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09657 | RWB-P5-E1032-APP | GAP-1198 | none | Add the seven platform contracts and the two P3 contracts to the dependency rows, or record them in the platform release train. |
| CDC-09695 | RWB-P5-E1032-CON | GAP-1198 | Header | Contract dependencies row of the story lists the two P3 contracts and the platform contracts |
| CDC-09727 | RWB-P5-E1032-INF | GAP-1198 |  | Add H RWB-PLT-E1027-CON, E1042-CON, E1043-CON, TE006-CON, E1071-CON, E1044-CON, N001-CON and C RWB-P3-E1042-CON, RWB-P3-E1043-CON to its dependency rows, or record in the platform release train. |
| CDC-09759 | RWB-P5-E1032-OPS | GAP-1198 |  | Add the seven platform contracts (RWB-PLT-E1027-CON, E1042, E1043, TE006, E1071, E1044, N001) and the P3 contracts (RWB-P3-E1042-CON, RWB-P3-E1043-CON) to the dependency rows, or record them in the platform release train. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09679 | RWB-P5-E1032-CON | GAP-0356 | 3, 4, 5, 13 | Record the parameter home as the P3 rwb-case parameters contract read as data by DP-06, keeping the three document_hub_parameter rows. Story trigger and attach edits sit in sections outside this chunk. |
| CDC-09789 | RWB-P5-E1039-APP | GAP-2039 | find it | Add an access_log row in schema rwb_access with P4 rwb-access as owner and the ACE DBA as DBA, with its key and retention class, at the next revision. |
| CDC-09792 | RWB-P5-E1039-APP | GAP-0165 | 12.7 | Add an access log row to the Tables sheet: P4 table in rwb_access, append-only, created by RWB-P4-E1039-DB. |
| CDC-09793 | RWB-P5-E1039-APP | GAP-2069 | 12.7 | Add an access_log table in rwb_access owned by P4, append-only, behind GET /admin/access-log. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09635 | RWB-P5-E1032-APP | CG-ALL-5820 | 12.2 | Publish GET /api/recovery/case/v1/cases/by-no/{caseNo} in rwb-case.yaml through provider CON story RWB-P3-E1018-CON. |
| CDC-09669 | RWB-P5-E1032-CON | CG-ALL-5831 | 12.2 | Publish GET /api/recovery/case/v1/cases/by-no/{caseNo} in rwb-case.yaml through the provider's CON story. |
| CDC-09670 | RWB-P5-E1032-CON | CG-ALL-5832 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml through the provider's CON story. |

### OTHER:S9 reference data set (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09654 | RWB-P5-E1032-APP | GAP-3142 | 3 | Publish the intake bound parameter row, the acceptance decision code with its version and LOV-DOC-TYPE; keep values out of code. |
| CDC-09692 | RWB-P5-E1032-CON | GAP-3142 | 3 | Publish the intake bound parameter row, the acceptance decision code with its version, and LOV-DOC-TYPE with LOV-INSTR-STATUS; values Not specified in the source documents (GAP-3142). |
| CDC-09724 | RWB-P5-E1032-INF | GAP-3142 |  | Publish the intake bound parameter row, the acceptance decision code with its version, and LOV-DOC-TYPE; keep values out of code. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09675 | RWB-P5-E1032-CON | DOR-RWB-P5-E1032-CON-1 | 1 | Add a role code or role name for the tech lead of rwb-document, or confirm the existing role that sections 1 and 10 should use. |
| CDC-09710 | RWB-P5-E1032-INF | DOR-RWB-P5-E1032-INF-1 | 1 | Add a role code or name for 'infrastructure engineer' to Users Roles and Permissions v5. |
| CDC-09775 | RWB-P5-E1033-APP | DOR-RWB-P5-E1033-APP-6 | 10 | Add service identity role SY-DOCUMENT (runs the query and appends the access record), which v5 does not list. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09622 | RWB-P5-E1026-APP | DOR-RWB-P5-E1026-APP-12 | 16 | Added TC-E1-026-14 (contract) and TC-E1-026-15 (ASM-3438 boundary) to section 16; add their full tests to the workbook and align RTM v7 with section 18. |
| CDC-09676 | RWB-P5-E1032-CON | DOR-RWB-P5-E1032-CON-12 | 12.7, 16, 18 | Add rows TC-P5-E1032-CON-01 to -08 to Test Cases v8; align the section 18 test lists of REQ-DCM-007, REQ-DCM-005 and REQ-DRI-004 in RTM v7. |

### RWB-P5-E1032-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09645 | RWB-P5-E1032-APP | GAP-1199 |  | State whether the document hub creates an intake item from a generated document and which request fields it needs, so the handoff and the item are specified once. |
| CDC-09715 | RWB-P5-E1032-INF | GAP-1197 | not in chunk c03 | Publish the request and answer of POST /cases/{caseId}/generated-documents with the intake item it creates; name the document type and source for a notice letter copy; register notice parameters; extend NoticeGenerated.v1 to its payload; allocate the notice screen ID. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09649 | RWB-P5-E1032-APP | GAP-2445 |  | Hold DOCATT as a value of LOV-DECISION at the version in force; read it through the rwb-case reference-data contract; an unknown code is refused with MSG-P7-009. |
| CDC-09751 | RWB-P5-E1032-OPS | GAP-2445 | 11 | Enumerate DOCATT as a value of LOV-DECISION at the version in force; refuse an unknown code with MSG-P7-009. |

### OTHER:rwb-source-data contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09662 | RWB-P5-E1032-APP | GAP-0743 | find it | Agree the query form for the ACE account number in the contract story; use GET /api/recovery/source-data/v1/accounts/{id} with the account number as identifier. |
| CDC-09762 | RWB-P5-E1032-OPS | GAP-0743 |  | Name GET /api/recovery/source-data/v1/accounts/{id} with the ACE account number as identifier, and agree the query form in the contract story before integration. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09665 | RWB-P5-E1032-APP | GAP-0747 | find it | Agree the decision code and final call for the case document link with the decision log owner; until then the record names case, document and event id only. |
| CDC-09765 | RWB-P5-E1032-OPS | GAP-0747 |  | Agree the decision code and final call for the case document link; until then the record names the case, the document and the event id only. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09689 | RWB-P5-E1032-CON | GAP-3137 | 4 | Confirm the secondary partner slice in the Change Register and publish the rwb-partner S9 frame for RWB-S9-E1032-APP: schema rwb_partner, base /api/recovery/partner/v1, topic rwb.partner.events.v1, queue rwb-partner. |
| CDC-09748 | RWB-P5-E1032-OPS | GAP-1199 | 12.4 | State whether the document hub creates an intake item from a generated document and which request fields it needs. |

### OTHER:rwb-source-data contract story (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09699 | RWB-P5-E1032-CON | GAP-0743 | Header | Provide GET /api/recovery/source-data/v1/accounts/{id} with the ACE account number as identifier, and agree the query form before integration. |
| CDC-09731 | RWB-P5-E1032-INF | GAP-0743 |  | Name GET /api/recovery/source-data/v1/accounts/{id} with the ACE account number as identifier and agree the query form before integration. |

### OTHER:FSD P6 Communications v3 and TSD P6 Communications v2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09704 | RWB-P5-E1032-CON | GAP-1203 | header | Approve both documents, or record that wave 1 builds on the reviewed versions and any change in approved text is a change request. |
| CDC-09735 | RWB-P5-E1032-INF | GAP-1200 |  | Name the business-owned communications values with defaults in a parameter row, or state that the module has none |

### RWB-S9-E1032-CON; RWB-P5-E1032-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09723 | RWB-P5-E1032-INF | GAP-3141 |  | Publish POST and GET /partner/instructions/{instructionId}/documents, the document-hub intake creation, the PartnerDocumentSubmitted.v1 payload, and the 404 and 409 bodies in RFC 9457 shape. |
| CDC-09755 | RWB-P5-E1032-OPS | GAP-3141 |  | Publish POST and GET /partner/instructions/{instructionId}/documents, the document-hub intake creation, the rwb.partner.PartnerDocumentSubmitted.v1 payload and the 404 and 409 bodies in RFC 9457 shape. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09737 | RWB-P5-E1032-OPS | DOR-RWB-P5-E1032-OPS-8 | 12.1, 12.5 | Register activity matchStep on task queue rwb-document, owned by RWB-P5-E1032-APP, in the catalog. The NONE path is covered by CG-ALL-5845; the workflow ID and start rule by CG-ALL-5846. |
| CDC-09740 | RWB-P5-E1032-OPS | CG-ALL-5847 | 12.5 | Add an Activities row for matchStep on task queue rwb-document, owned by RWB-P5-E1032-APP, or name a catalogued activity. |

### RWB-S9-E1032-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09754 | RWB-P5-E1032-OPS | GAP-3138 |  | Publish the partner file channel: the rwb_partner submission row, the PartnerDocumentSubmitted fact, the attach event consumed and the item read used to copy the match state. |
| CDC-09767 | RWB-P5-E1032-OPS | GAP-3145 | 8 | Partner screen reference removed from BR8. |

### RWB-P4-E1039-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09786 | RWB-P5-E1039-APP | GAP-2339 | find it | Add to the session contract how the grant ID and incident reference reach a consuming service: a signed short-lived claim in the forwarded session envelope, its lifetime and reuse bound; a missing or expired claim means no grant. |
| CDC-09790 | RWB-P5-E1039-APP | GAP-2076 |  | The access row records the version the owning service applied at the event; the rwb-decision registry stays the source of the version and its effective date. |

### OTHER:owning contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09791 | RWB-P5-E1039-APP | GAP-2341 | 8 | Other reads' entry behaviour now reads Not specified. |
| CDC-09794 | RWB-P5-E1039-APP | GAP-2342 | 7, 8 | Queue name and session-answer reuse bound now read Not specified. |

### RWB-P3-E1043-CON; OTHER:P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09611 | RWB-P5-E1025-APP | DOR-RWB-P5-E1025-APP-21 | Metadata | Reach Done status for RWB-P3-E1043-CON; the Contract published gate stays Fail until then. |

### OTHER:rwb-document OpenAPI 3.1 document; OTHER:rwb-case reference-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09613 | RWB-P5-E1025-APP | GAP-1039 | 13 | Publish the document-type admin paths, request and response schemas, row-error schema, error codes and load template columns in the rwb-document OpenAPI 3.1 document; add the reference-version registration operation to the rwb-case reference-data contract. |

### OTHER:rwb-document OpenAPI 3.1 document; parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09614 | RWB-P5-E1025-APP | GAP-1020 | 13 | Publish the checked-fields read on /api/recovery/document/v1/cases/{caseId}/checked-fields with CheckedField and CheckedFieldSet shapes as the superset of the legacy list; keep EXTRACT_ACCURACY_PASS in document_hub_parameter; confirm names with S4 and S2 before wave 2. |

### RWB-PLT-E1044-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09616 | RWB-P5-E1025-APP | GAP-1041 | 3 | Allocate the rwb-document login name, secret reference and grants (schema rwb_document only, no privilege on rwb_case) and record them in the service catalogue. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09617 | RWB-P5-E1025-APP | GAP-1051 | 3 | Publish the per-case document count and the version depth of a seeded document, held as seed parameters. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON; RWB-P3-E1030-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09619 | RWB-P5-E1026-APP | DOR-RWB-P5-E1026-APP-21 |  | Bring these contract stories to Done; no contract story of key RWB-E1-026 exists. |

### RWB-P5-E1024-APP; RWB-P5-E1025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09623 | RWB-P5-E1026-APP | DOR-RWB-P5-E1026-APP-17 |  | Bring both build dependencies to Done. The ten dependencies are already named in the header. |

### RWB-P5-E1024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09625 | RWB-P5-E1026-APP | GAP-1033 | 10, 14 | Publish request and response field names for Document, DocumentPage and DocumentChecklist, the rwb_document login name (DP-02) and the MSG-GEN-006 text. |

### RWB-P5-E1041-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09626 | RWB-P5-E1026-APP | GAP-1034 | 5, 7 | Fix the scan operation path, verb, request, response CLEAN/INFECTED and error shape. |

### RWB-P5-E1040-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09627 | RWB-P5-E1026-APP | GAP-2758 | 12.2 | Keep the two metadata rows; step D1 decides whether the three consumed rows become C dependencies or a baseline is raised. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09628 | RWB-P5-E1026-APP | GAP-2760 | 12.2 | Carry the three consumed contracts as non-blocking rows; leave the metadata rows unchanged. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09630 | RWB-P5-E1026-APP | GAP-1035 | 15 | Publish the SCR-30 gateway-bff composite route with its browser path, merged screen-model fields, per-call timeout and breaker values, and the 2 s REST budget. |

### RWB-P5-E1032-APP; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09646 | RWB-P5-E1032-APP | GAP-1201 |  | Record that attach proof of TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP, that the P6 copy proves the service side, and that TC-E1-032-16 is the notice-read refusal. |

### OTHER:TSD P7 v2 decision_log_entry (rwb_decision migration V1032_1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09648 | RWB-P5-E1032-APP | GAP-2444 |  | Carry document reference, intake item and match method in actions; classifier version in model_version; confidence and type candidates in recommendation; message id in outcome; final_call ATTACHED; add the columns by migration V1032_1 in rwb_decision. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; RWB-S9-E1032-APP; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09651 | RWB-P5-E1032-APP | GAP-3137 |  | Confirm the secondary partner slice in the Change Register and publish the S9 frame (schema rwb_partner, base /api/recovery/partner/v1, topic rwb.partner.events.v1, queue rwb-partner, package th.co.scb.ace.workbench.recovery.partner). |

### OTHER:S9 contract baseline (rwb-partner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09652 | RWB-P5-E1032-APP | GAP-3138 |  | Publish the partner file channel: the rwb_partner submission row, the PartnerDocumentSubmitted fact, the consumed attach event, and the item read used to copy the match state. |

### RWB-S9-E1032-CON; OTHER:P5 contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09653 | RWB-P5-E1032-APP | GAP-3141 | none | Publish POST and GET /partner/instructions/{instructionId}/documents, the document-hub intake creation, the PartnerDocumentSubmitted.v1 payload and the 404 and 409 RFC 9457 bodies. |

### RWB-P5-E1032-CON; RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09658 | RWB-P5-E1032-APP | GAP-1003 | none | Declare the two classification operations and the three field names after architect confirmation; add DocumentClassified.v1 to the event catalogue and amend the event count and AC8 of RWB-P5-E2026-CON. |

### RWB-P5-E1054-CON; RWB-P3-E1035-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09659 | RWB-P5-E1032-APP | GAP-1010 | none | Read review rows from document_hub_parameter, publish the by-number case read on RWB-P3-E1035-CON, and fix field names and message texts in RWB-P5-E1054-CON. |

### RWB-P5-E1032-OPS; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09663 | RWB-P5-E1032-APP | GAP-0744 | n/a | Add a daily case-side reconcile Schedule with overlap policy SKIP and a catch-up window. Time of day: Not specified in the source documents (GAP-0744), to be set with operations before go-live. |

### OTHER:platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09666 | RWB-P5-E1032-APP | GAP-0748 | find it | Name one database login per service for rwb-case and rwb-document; the story keeps role names until then. |

### OTHER:Build Notes v6 (service epic and wave plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09667 | RWB-P5-E1032-APP | GAP-3174 |  | State wave 1 delivery of rwb-partner in the service epic and wave plan; the rwb-partner service wave (Arch v5 wave 4) governs its later stories. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09673 | RWB-P5-E1032-CON | DOR-RWB-P5-E1032-CON-8 | header | Resolve CG-ALL-5830, CG-ALL-5831, CG-ALL-5832 and CG-ALL-5833 in their owner documents. |

### OTHER:rwb-access API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09677 | RWB-P5-E1032-CON | DOR-RWB-P5-E1032-CON-6 | 10 | Declare the authorise check that DP-08 requires for the declared area and right, with its operation name. |

### OTHER:Environment files for rwb-document (path Not specified in the source documents (GAP-0993)) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09682 | RWB-P5-E1032-CON | GAP-0993 | not in chunk | Record per-environment values for worker replica count, request and limit, KEDA ceiling, document_text growth and index budget, rwb-quarantine clearing age, hold container capacity and scan rate per hour, set from SIT measurement. |

### OTHER:TSD P5 v2; OTHER:TSD P6 Communications v2; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09683 | RWB-P5-E1032-CON | GAP-1197 | n/a | Publish the generated-document request and answer with the intake item created, name the letter-copy document type and source, register the notice parameters, extend the NoticeGenerated payload, and allocate the notice screen ID. |

### OTHER:TSD P5 v2; OTHER:TSD P6 Communications v2; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09684 | RWB-P5-E1032-CON | GAP-1199 | n/a | State whether the hub creates an intake item from a generated document and which request fields it needs, so the handoff is specified once. |

### OTHER:Test case register (workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09685 | RWB-P5-E1032-CON | GAP-1201 | 16 | Record that attach proof for TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP, the P6 copy proves the service side, and TC-E1-032-16 is the notice-read refusal. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-ITG-E1032-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09686 | RWB-P5-E1032-CON | GAP-1202 | n/a | Record that rwb-document is called by rwb-comms over the call edge and that rwb.comms.NoticeGenerated.v1 stays a notification for rwb-decision only; align the integration suite row. |

### OTHER:TSD P7 v2 T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09687 | RWB-P5-E1032-CON | GAP-2445 | 7 | Add LOV-DECISION to the list of lists, with DOCATT as a value in force read through the rwb-case reference-data contract; an unknown code is refused with MSG-P7-009. |

### OTHER:rwb-document contract (rwb.decision-record.v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09688 | RWB-P5-E1032-CON | GAP-3134 | 12.3 | Publish the DecisionRecorded payload: caseId, decisionCode, documentId, intakeItemId, matchMethod, classifierVersion, confidence, approverUserId, finalCall, messageId, inputsRef; no OCR text, file or account number; a fact without documentId is refused. |

### OTHER:S9 contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09690 | RWB-P5-E1032-CON | GAP-3138 | 2 | Publish the partner file channel: the rwb_partner submission row, the PartnerDocumentSubmitted fact, the attach event consumed, and the item read used to copy the match state. |

### OTHER:S9 contract baseline and P5 contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09691 | RWB-P5-E1032-CON | GAP-3141 | 12 | Publish the two partner submission operations, the document-hub intake creation, the PartnerDocumentSubmitted payload, the 404 and 409 bodies and the RFC 9457 problem shape. |

### OTHER:Case-side document reconcile Schedule (owner RW-COE) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09700 | RWB-P5-E1032-CON | GAP-0744 | Header | Run the reconcile Schedule daily with overlap policy SKIP and a catch-up window; set the time of day with operations before go-live. |

### OTHER:Platform DB story (one login per service) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09702 | RWB-P5-E1032-CON | GAP-0748 | - | Name the rwb-case and rwb-document logins, one per service, and reference them here once agreed. |

### OTHER:FSD S9 Partner portal (PRT-02 Instruction) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09705 | RWB-P5-E1032-CON | GAP-3145 | - | Fix the screen that carries the document submission of an instruction when PRT-02 Instruction is specified. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09706 | RWB-P5-E1032-CON | GAP-3174 | - | State the wave 1 delivery of rwb-partner in the service epic and wave plan, and let the rwb-partner service wave govern its later stories. |

### OTHER:TSD P5 v2 (DocumentIntakeWorkflow trigger, /resolve and parameter home) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09713 | RWB-P5-E1032-INF | GAP-0356 | 8 | Start the intake from DocumentStored with KEDA workers; keep /review-items and /resolve with the item version; keep the three parameters as document_hub_parameter rows read as data; prove the P6 letter copy and S9 partner result on the same match path. BR2 and AC1 cadence wording follows the owner ruling. |

### OTHER:P5 and P6 contract documents; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09716 | RWB-P5-E1032-INF | GAP-1199 | not in chunk c03 | State whether the hub creates an intake item from a generated document and which request fields it needs, so the handoff and item are specified once. |

### OTHER:Test case register (TC-E1-032-01 to TC-E1-032-16) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09717 | RWB-P5-E1032-INF | GAP-1201 | not in chunk c03 | Record that attach proof of TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP and P6 proves the service side; note the access case as the notice-read refusal. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; RWB-P5-E1032-APP; OTHER:integration suite (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09718 | RWB-P5-E1032-INF | GAP-1202 | not in chunk c03 | Align to the recommended reading: rwb-comms calls the document hub; rwb-decision is the only event consumer of NoticeGenerated.v1. Update catalogue row and dependent stories. |

### OTHER:TSD P7 v2 T3.1 decision_log_entry (migration V1032_1 in rwb_decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09719 | RWB-P5-E1032-INF | GAP-2444 | not in chunk c03 | Carry document reference, intake item and match method in actions; classifier version in model_version; confidence and candidates in recommendation; refusal message ID in outcome; final_call ATTACHED; add columns by V1032_1. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:rwb-case reference-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09720 | RWB-P5-E1032-INF | GAP-2445 | not in chunk c03 | Hold DOCATT as a value of LOV-DECISION at the version in force, read through the rwb-case reference-data contract; unknown code refused with MSG-P7-009. |

### RWB-P5-E1032-CON; OTHER:TSD P7 v2 T5.3 DecisionRecorded (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09721 | RWB-P5-E1032-INF | GAP-2447 | not in chunk c03 | Fix the fact keyed by caseId with decisionCode, caseId, documentId, intakeItemId, matchMethod, classifierVersion, confidence, approverUserId, finalCall, messageId, inputsRef; no OCR text, file or account number; refuse a fact without a document reference. |

### OTHER:S9 contract baseline (partner file channel) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09722 | RWB-P5-E1032-INF | GAP-3138 | not in chunk c03 | Publish the partner file channel: submission row in rwb_partner, PartnerDocumentSubmitted fact, attach event consumed, and item read used to copy match state. |

### OTHER:rwb-case story that owns the case-side document reconcile Schedule (not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09732 | RWB-P5-E1032-INF | GAP-0744 | 12.6 | Daily reconcile Schedule with overlap policy SKIP and a catch-up window; time of day Not specified in the source documents (GAP-0744) |

### OTHER:RWB-PLT-DB platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09734 | RWB-P5-E1032-INF | GAP-0748 |  | Name one login each for rwb-case and rwb-document; logins Not specified in the source documents (GAP-0748) |

### OTHER:split_plan.json (EP01 wave 1 slices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09738 | RWB-P5-E1032-OPS | GAP-1843 | header | Keep RWB-S9-E1032-APP and RWB-S9-E1057-APP in wave 1 as contract-only slices; move the partner panel, allocation and fees to wave 4 in the split plan. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09744 | RWB-P5-E1032-OPS | GAP-0356 | find it | Trigger moved to DocumentStored with KEDA in 1, 8, 11, 12.5, TC-11; parameters stay as document_hub_parameter. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P5 contract and TSD P6 Communications v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09747 | RWB-P5-E1032-OPS | GAP-1197 | 12.4 | Publish the request and answer of POST /cases/{caseId}/generated-documents, the document type and source for a notice letter copy, the notice parameter names, the NoticeGenerated payload fields and the notice screen ID. |

### OTHER:Test case register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09749 | RWB-P5-E1032-OPS | GAP-1201 | 16 | Record that the attach proof of TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP, that the P6 copy proves the service side, and that the access case is the notice-read refusal. |

### RWB-ITG-E1032-ITG; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09750 | RWB-P5-E1032-OPS | GAP-1202 | 12.4 | Keep the call reading: rwb-comms calls rwb-document and rwb.comms.NoticeGenerated.v1 stays rwb-decision only; align the integration suite to that. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09753 | RWB-P5-E1032-OPS | GAP-3137 |  | Confirm the secondary partner slice in the Change Register and publish the S9 frame (schema rwb_partner, base /api/recovery/partner/v1, topic rwb.partner.events.v1, queue rwb-partner, package th.co.scb.ace.workbench.recovery.partner) for RWB-S9-E1032-APP in the Service Contract Catalog. |

### OTHER:S9 reference data set; parameter-catalog.csv; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09756 | RWB-P5-E1032-OPS | GAP-3142 |  | Publish the intake bound parameter row, the acceptance decision code with its version, and LOV-DOC-TYPE in the S9 reference data set. Keep all values out of code. |

### OTHER:AC Glossary; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09758 | RWB-P5-E1032-OPS | GAP-3144 |  | Record the primary/secondary AC split so the fifteen legacy criteria are counted once against RWB-P5-E1032-APP. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09763 | RWB-P5-E1032-OPS | GAP-0744 |  | Add a case-side document reconcile job: daily Schedule, overlap policy SKIP, catch-up window; set time of day with operations before go-live. |

### OTHER:Platform DB story (not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09766 | RWB-P5-E1032-OPS | GAP-0748 |  | Name one database login per service for rwb-case and rwb-document, then reference them in this story once agreed. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09768 | RWB-P5-E1032-OPS | GAP-3174 | 1 | State the wave 1 delivery of rwb-partner in the service epic and the wave plan; let the rwb-partner service wave govern its later stories. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09773 | RWB-P5-E1033-APP | DOR-RWB-P5-E1033-APP-11 | none | Confirm the personal-data class of the P2 fields detcheck names, and align it with the story's statement that no personal data is carried. |

### RWB-ITG-E1039-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09780 | RWB-P5-E1039-APP | GAP-0661 |  | Baseline GET and export on /api/recovery/integration/v1 with the twelve columns, filter set, breach filter, order, paging envelope and problem body; declare the eight consumed operations with their paths fixed in the P3 and P4 contract stories; state that GET /cases and GET /cases/export stay with rwb-case and the composition is additional and read-only; declare no table, event, workflow or Schedule. |

### RWB-ITG-E1039-ITG; OTHER:the P3 and P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09781 | RWB-P5-E1039-APP | GAP-0660 |  | Keep GET /cases and GET /cases/export with rwb-case; add the composed read and export on the integration base as additional, read-only, one hop each with a 2 s budget; fix the ageing read, reference-data read and access-log operation in the P3 and P4 contract stories; flag switch and parameters to be settled in those stories. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09782 | RWB-P5-E1039-APP | GAP-0966 |  | Add the rule-package action set, its request and answer fields and a change decision code to the POST /authorise contract; agree the code with the access-log owner of RWB-E1-039; stub both in the contract fake. |

### OTHER:TSD P4 v3 (T-A) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09783 | RWB-P5-E1039-APP | GAP-0781 | find it | Declare the end and read operations at /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end and /api/recovery/access/v1/admin/break-glass-grants/{grantId}, the grant state field and the expired-session message id. |

### OTHER:TSD P4 v3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09784 | RWB-P5-E1039-APP | GAP-0782 | find it | Name the grant table break_glass_grant in rwb_access with a unique partial constraint on the active grant of an actor; set the access-log retention as parameter rows with a partition drop. |

### OTHER:Deployment values files and platform secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09785 | RWB-P5-E1039-APP | GAP-0783 | find it | Record the two alert routes, the failed-write and break-glass thresholds as parameter rows, the Kafka ACL set and retry cadence for rwb.decision-record.v1, and the secret names and topology values. |

### OTHER:TSD P7 (API-P7-006; OTHER:API-P7-007) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09787 | RWB-P5-E1039-APP | GAP-2452 | find it | Add grantId, incidentReference and reviewDueAt as working names to the decision-log read answer until the service contract baseline publishes them; the message id format comes from the message catalogue owner. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09800 | RWB-P5-E1040-APP | DOR-RWB-P5-E1040-APP-12 | 12, 12.7, 16, 18 | Story has TC-11 to TC-19. Section 18 and the RTM row must list 01 to 19; workbook and RTM rows are still needed. |

### RWB-P5-E2025-CON; RWB-P10-E1062-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09803 | RWB-P5-E1040-APP | GAP-0627 | 12, 18 | Apply the proposed fix of GAP-0627 in the owner contracts and parameter sources; no edit in RWB-P5-E1040-APP |

### OTHER:Plan S4 contract rows (outside this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09804 | RWB-P5-E1040-APP | GAP-2758 | 3 | No story edit made. The S4 contract-row gap sits in the plan and needs an owner fix. |

### RWB-P3-E1043-CON; RWB-PLT-E1071-CON; OTHER:TSD P5 Document hub v2 (API-P5-008) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09805 | RWB-P5-E1040-APP | GAP-2337 | 3 | Publish the rwb-case case read (stage, route, owner), the DOCUMENT_CHECKLIST reference-load and approval with field names, a batch missing-count for up to 500 cases, DocumentChecklist field names, and the intake Schedule ID. |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20868 | RWB-P5-E1039-APP | R-22118 |  | Alert routes, thresholds, Kafka ACLs and secret names belong in deployment values files and the platform secret store. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0065 | Wave conflict S9 / EP01 | Tech lead | Resolved (directive) |
| GAP-0165 | The access log is named by Architecture v5 but is not itemised in the Ownership Map | ACE team | Resolved (directive) |
| GAP-0350 | E1025 document-type load path and field dictionary after the reference-data ruling | Solution architect | Resolved (directive) |
| GAP-0351 | E1026 attach and search screen as a gateway-bff composite over P5 and P3 | Solution architect | Resolved (directive) |
| GAP-0356 | Intake trigger, attach operation and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0359 | Break-glass grant operation, central ledger fault point and SIT evidence are not named for the 19-service target | Tech lead | Resolved (directive) |
| GAP-0627 | The app slice of the legal document agent in shadow: the document, OCR-text and checklist operations and members, the legal-action read, the run-start path, the parameter keys, the service login, the route, the BRD section of REQ-DCM-011 and the pack member types are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0742 | No case-side document link table or field IDs in the sources | RW-DATASTEW | Resolved (directive) |
| GAP-0743 | No named rwb-source-data operation for the ACE account number | RW-COE | Resolved (directive) |
| GAP-0744 | Cadence and time of the daily reconcile Schedule not specified | RW-COE | Resolved (directive) |
| GAP-0745 | The rwb-case feature switch key is not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0747 | Decision code and final call for the case document link are not specified | RW-COE | Resolved (directive) |
| GAP-0748 | Per-service login names for rwb-case and rwb-document are not specified | RW-SECADM | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0780 | Local decision-record table, legacy break-glass path and the composition of the entry actions are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0781 | The grant end and read paths, the 401 business message id and the full grant answer are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0782 | No source names the grant table, its two-person constraint, the retention period or the partition granularity of the access log | ACE database engineer | Resolved (directive) |
| GAP-0783 | Alert routes, thresholds, Kafka ACL set, retry cadence and secret names are not fixed by the sources | DevOps engineer | Resolved (directive) |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0991 | The attach operation, its right and the attach event name differ between the legacy story, the TSD and the Arch v5 event catalogue | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0992 | The intake-match contract baseline fixes shapes and paths the sources do not name at field level, and the plan's C list omits the two rwb-case reads | Tech lead | Resolved (directive) |
| GAP-0993 | The compute, storage, hold-container and scanning capacity values of the intake-match path are not specified | SCB IT infrastructure | Resolved (directive) |
| GAP-0994 | The Schedule window, the catch-up policy, the alert thresholds and the lag-alert identifier of the intake path are not specified | DevOps team | Resolved (directive) |
| GAP-1003 | No source names a classification operation, path or field-level name, a 404 message identifier is absent, and a classification event would be a third event for rwb-document | Solution architect with the TechX contract owner of rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1033 | Request and response field names of the three SCR-30 operations, the per-service login name and the text of MSG-GEN-006 are not fixed in the sources | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1034 | The scan operation path of the RWB-P5-E1041-CON malware-scan contract is not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1035 | The SCR-30 route specification in the gateway-bff composite route is not specified | Solution architect, with the gateway-bff squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1039 | The load, approve and in-force read shapes for document types are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1041 | The rwb-document login name and its grants are not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1197 | The request and answer shape of the letter-copy handoff, the document type and source the hub assigns, the notice parameters, the P1 recipient field IDs, the payload field names of the event and the notice screen identifier are all unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1199 | No source describes the letter copy becoming an intake item at the document hub, and FSD P6 keeps a generated document as a stored document on the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1200 | The P6 module declares no notice parameter, so DP-06 has no named value to read | Business analyst | Resolved (directive) |
| GAP-1201 | The legacy access case and the legacy attach cases have no subject in rwb-comms, so the carried test cases prove the notice read instead | Test lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1202 | The event catalogue names rwb-decision as the only consumer of NoticeGenerated, while the document hub is expected to turn the copy into an intake item | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1203 | The base documents of the story are in review, not approved | Business analyst | Resolved (directive) |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1571 | The break-glass duration, the minimum reason length and the review window appear only inside acceptance criteria and are open in the decision log | SCB IT security with the security administrator | Resolved (directive) |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-2039 | The access log is named as an rwb_access object but has no row in the Ownership Map | P4 rwb-access with the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2069 | The access log has an API and an owner but no table in the Ownership Map | Service owner P4 rwb-access | Resolved (directive) |
| GAP-2076 | The versions in force in the access log come from two services | Service owners P4 rwb-access and P7 rwb-decision | Resolved (directive) |
| GAP-2334 | The record code and the acknowledgement of the search access record, the case-list scope parameters, the page bounds and the screen ID are named in no source | Solution architect | Resolved (directive) |
| GAP-2335 | The two DP-11 contract reads of the legacy in-process calls are absent from the Work Package dependency rows and DP-08 is not among the patterns | Solution architect | Resolved (directive) |
| GAP-2336 | The FSD keeps the PII access log in the ACE common module while the Work Package applies DP-03 to the same record | Solution architect | Resolved (directive) |
| GAP-2337 | The rwb-case side of the checklist story is not fixed: the case read operation, the reference-load operation, the batch missing-count operation and the DocumentChecklist field names | Solution architect, with the P5 TechX squad and the P3 rwb-case squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2339 | How the active break-glass grant and its incident reach rwb-document on a document content read is not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2340 | The capability-area code, the result code and the field list of a document content read in an access entry are not specified | Data steward | Resolved (directive) |
| GAP-2341 | Which reads of the document hub other than the content read write an access entry in the target is not fixed | Solution architect | Resolved (directive) |
| GAP-2342 | The incident queue name and the session-answer reuse bound of the content read are not specified | DevOps team | Resolved (directive) |
| GAP-2444 | DOCATT attach entry has no defined field set for the document reference, the intake item, the match method, the confidence, the final call and the message id | Solution architect, P7 | Resolved (directive) |
| GAP-2445 | The decision code list in force does not enumerate DOCATT in any source readable here | Reference data administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2446 | Whether an item held for a person leaves a decision record is not stated | Business analyst, P7 | Resolved (directive) |
| GAP-2447 | The DecisionRecorded payload of an attach has no defined field set | Solution architect, integration | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2449 | Login name, parameter names and message texts are not written in any source readable here | Tech lead, P7 | Resolved (directive) |
| GAP-2450 | The trigger of the ledger completeness check is not stated | Solution architect, P7 | Resolved (directive) |
| GAP-2452 | No source gives the ledger's access shape: the element names inside the actions payload beyond the legacy list, the grant, incident and review-due elements of the decision-log read, the use of the access code AC-VERS, and the catalogue entry format of MSG-P7-009 | Business analyst P7 | Resolved (directive) |
| GAP-2758 | The known defect list has no element of its own in S4, and the two consumed rwb-document reads and the rwb-case answer publish no S4 contract row | S4 rwb-litigation service owner with the P5 rwb-document owner and the P3 rwb-case owner | Resolved (directive) |
| GAP-2760 | Three consumed contracts of the pack-recovery step have no dependency row, and the plan gives the two stories no contract or integration dependency | Solution architect, S4 rwb-litigation, with the P5 rwb-document and P3 rwb-case architects | Resolved (directive) |
| GAP-3137 | The partner slice of RWB-E1-032 and its target service frame are not stated in any source | Solution architect | Resolved (directive) |
| GAP-3138 | The partner-origin channel of an intake item and its attach state are a boundary no source states | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3139 | Wave conflict: EP01 puts this story in wave 1 while rwb-partner is wave 4 in Arch v5 | Tech lead | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3141 | The two partner submission operations, the intake creation path and the PartnerDocumentSubmitted event are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3142 | The intake bound, the decision code and version, and the two lists in force are not named | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3143 | No data model carries a partner-side submission row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3144 | No source states how the legacy criteria split between the document-hub and partner slices | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3145 | The partner portal screen that submits a file is not fixed | Business analyst | Resolved (directive) |
| GAP-3174 | Service S9 takes Epic 1 stories in wave 1 although its Arch v5 wave is 4 | Delivery lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P5-E1032-CON | skipped AC ID | 102 | missing: AC9, AC10, AC11, AC12, AC13, AC14, AC15 |
