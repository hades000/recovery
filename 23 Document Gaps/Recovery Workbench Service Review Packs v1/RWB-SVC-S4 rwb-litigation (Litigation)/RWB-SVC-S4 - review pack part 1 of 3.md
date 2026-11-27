# RWB-SVC-S4 rwb-litigation (Litigation) - review pack, part 1 of 3 (RWB-S4-E2025-APP to RWB-S4-E5007-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 14 |
| Resolved in the stories | 295 |
| Cross-document (pending in another document) | 229 |
| Not applied (value not in the sources) | 10 |
| Open business decisions | 30 |
| Register gaps linked | 75 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S4-E2025-APP | 34 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E2025 APP Extraction for the stage 2 and 3 document types v2.md |
| RWB-S4-E5001-APP | 29 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5001 APP Issue demand and recall notices v2.md |
| RWB-S4-E5001-CON | 18 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5001 CON Issue demand and recall notices - contract v2.md |
| RWB-S4-E5002-APP | 25 | 29 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5002 APP Record proof of delivery on a notice v2.md |
| RWB-S4-E5002-CON | 20 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5002 CON Record proof of delivery on a notice - contract v2.md |
| RWB-S4-E5003-APP | 23 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5003 APP Run the notice period timer v2.md |
| RWB-S4-E5003-CON | 12 | 10 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5003 CON Run the notice period timer - contract v2.md |
| RWB-S4-E5004-APP | 16 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5004 APP Assemble the litigation pack v2.md |
| RWB-S4-E5004-CON | 9 | 15 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5004 CON Assemble the litigation pack - contract v2.md |
| RWB-S4-E5005-APP | 24 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5005 APP Check the pack against the defect list v2.md |
| RWB-S4-E5005-CON | 16 | 8 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5005 CON Check the pack against the defect list - contract v2.md |
| RWB-S4-E5006-APP | 27 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5006 APP Recover a missing or lost document v2.md |
| RWB-S4-E5006-CON | 16 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5006 CON Recover a missing or lost document - contract v2.md |
| RWB-S4-E5007-APP | 26 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5007 APP Verify the pack and approve filing v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S4-E2025-APP | R-02265 | CG-ALL-8969 | Script gap | Product owner | The story adds EXTRACT_FIELD_THRESHOLD to the closed list LOV-HEARING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E2025-APP | R-02266 | CG-ALL-8970 | Script gap | Product owner | The story adds EXTRACT_ACCURACY_PASS to the closed list LOV-HEARING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5001-APP | R-02269 | CG-ALL-8989 | Script gap | Product owner | The story adds NOTICE_GENERATED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5001-APP | R-02270 | CG-ALL-8990 | Script gap | Product owner | The story adds NOTICE_DISPATCHED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5001-APP | R-02271 | CG-ALL-8991 | Script gap | Product owner | The story adds NOTICE_BLOCKED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5001-APP | R-02272 | CG-ALL-8992 | Script gap | Product owner | The story adds NOTICE_UNSERVED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-APP | R-02289 | CG-ALL-9072 | Script gap | Product owner | The story adds NOTICE_BLOCKED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-APP | R-02290 | CG-ALL-9073 | Script gap | Product owner | The story adds PACK_VERIFIED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-APP | R-02291 | CG-ALL-9074 | Script gap | Product owner | The story adds PACK_ASSEMBLY to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-APP | R-02292 | CG-ALL-9075 | Script gap | Product owner | The story adds PACK_DEFECT_HOLD to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-CON | R-02293 | CG-ALL-9083 | Script gap | Product owner | The story adds PACK_ASSEMBLY to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-CON | R-02294 | CG-ALL-9084 | Script gap | Product owner | The story adds PACK_VERIFIED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-CON | R-02295 | CG-ALL-9085 | Script gap | Product owner | The story adds NOTICE_BLOCKED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5004-CON | R-02296 | CG-ALL-9086 | Script gap | Product owner | The story adds PACK_DEFECT_HOLD to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5001-APP, RWB-S4-E5001-CON, RWB-S4-E5003-APP, RWB-S4-E5003-CON | R-09241 | GAP-1467 | Register gap | Legal counsel | The statutory notice periods and the litigation step service levels are not specified | Hold the legal periods and the litigation service levels in the legal periods reference table, load the periods Legal signs, and test the timer against the loaded version rather than a literal. |
| RWB-S4-E2025-APP | R-12476 | CG-ALL-8984 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5001-APP | R-12481 | CG-ALL-9000 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5003-CON | R-12512 | CG-ALL-9068 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5004-CON | R-12517 | CG-ALL-9090 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5005-APP | R-12522 | CG-ALL-9099 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5006-APP | R-12530 | CG-ALL-9122 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5007-APP | R-12544 | CG-ALL-9148 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2025-ITG, RWB-P5-E2025-APP, RWB-P5-E2025-CON, RWB-P5-E2025-OPS, RWB-P7-E2025-APP, RWB-S2-E2025-APP, RWB-S4-E2025-APP | R-22604 | GAP-1285 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The extraction decision record's payload, value sets, read shape and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the extraction column set of decision_log_entry (new columns or jsonb members), the decision code of an extraction decision, the final-call value set, the threshold parameter names and version labels, the message ids and their texts, the document filter of the read and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2025-1 and its eight criteria stand on that shape |
| RWB-ITG-E5002-ITG, RWB-P3-E5002-APP, RWB-P6-E5002-APP, RWB-S4-E5002-APP, RWB-S4-E5002-CON | R-22803 | GAP-2746 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case architect and the business owner of the notice period | The notice-period timer has no stated home and the notice period has no value in any source | Declare the proof window of 7 days and the notice period as two durable timers of LitigationWorkflow, the first started at dispatch and the second at delivered_at under R-LIT-07; read the notice period as a versioned reference row per product and notice type, carry its content as the placeholder until the business owner publishes it, hold the timer and answer no move when the row is missing, and keep the case-stage timer and the officer task rows with rwb-case on the stage outcome. |
| RWB-S4-E5003-APP, RWB-S4-E5003-CON, RWB-S4-E5010-APP, RWB-S4-E5010-CON, RWB-S4-E5017-APP, RWB-S4-E5017-CON, RWB-S4-E5021-APP, RWB-S4-E5021-CON | R-23420 | GAP-1746 | Register gap | Product Owner | REQ-S4-009 (prescription warnings) has no BRD requirement row, and BR-038 and BR-042 carry no program requirement ID | Carry REQ-S4-009 into this PRD as FR-S4-051 and FR-S4-052 under BR-034, the requirement that owns the statutory clock, and record the gap so the E5 BRD can add the row. Carry BR-038 and BR-042 from the FSD features and the RWB-E5 story keys. Nothing is dropped and no requirement is merged. |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-S4-E5002-APP, RWB-S4-E5002-CON | R-38195 | ASM-4566 | Register assumption |  | The proof window of 7 days and the notice period are two durable timers of LitigationWorkflow: the first starts at dispatch, the second at delivered_at under R-LIT-07 and never under R-LIT-08 or R-LIT-09. The notice period is a versioned reference row per product and notice type whose content is not published; when the row is missing the step records the decision, holds the timer and answers no move. The case-stage timer and the officer task stay rwb-case's rows, requested on the stage outcome. | Business owner of the notice period with the S4 and P3 solution architects |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S4-E5001-APP | R-19716 | DOR-RWB-S4-E5001-APP-10 | not in chunk | Definition of Ready item 10 Screens and states: Partial | SCR-18 and SCR-20 state text sits in story sections outside this chunk, so no anchor to edit. FSD S4 v4 (Functional Specifications v7) has no empty, loading, error or no-access text. No state invented. |
| RWB-S4-E5001-APP | R-19717 | DOR-RWB-S4-E5001-APP-11 | not in chunk | Definition of Ready item 11 Guardrails: Partial | Field personal-data classes need the story's field section, which is outside this chunk. PRD S4 v1 near line 419 classes the screen, partner and agent fields as personal data. Story edit deferred; no class invented. |
| RWB-S4-E5003-CON | R-19761 | DOR-RWB-S4-E5003-CON-11 | 17 | Definition of Ready item 11 Guardrails: Partial | The field classed as personal data is not named in the story, the chunk or the detcheck text. Cannot fix without the field name. |
| RWB-S4-E5003-CON | R-29123 | GAP-2750 | 4, 5, 7 | The notice-period contract: no period element behind a column, no index set, no operation name for the four consumed services, no notice table of this service and no text for the 409 or the 400 | Fix targets operations, schemas, DDL and error rows in sections 4 and 5 that are not in this chunk. Handle in the chunk that holds them. |
| RWB-S4-E5004-APP | R-07936 | DOR-RWB-S4-E5004-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off in the source documents (searched 03 and the wider folder; only scratch and work files matched). Sign-off cannot be recorded without inventing it. Confirm with the epic design record. |
| RWB-S4-E5004-CON | R-19775 | DOR-RWB-S4-E5004-CON-10 | 10 | Definition of Ready item 10 Screens and states: Partial | SCR-18 and SCR-19 rows are in section 10, which is not in this chunk. Glob found no story file under 22 Microservice Realignment. Re-run with section 10. |
| RWB-S4-E5004-CON | R-19779 | DOR-RWB-S4-E5004-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Covering AC and TC IDs are in sections 7 and 16, not in this chunk; the story file was not found. BR1-BR12 cannot be mapped without inventing IDs. Re-run with sections 7 and 16. |
| RWB-S4-E5004-CON | R-23424 | GAP-1739 | 11 | legal_action.case_id is a uuid in the FSD, while ADR-014 and DP-01 forbid a cross-schema foreign key and require a varchar(255) business key | Section 12 DDL template is outside this chunk and still has to match the varchar(255) business key (ADR-014, DP-01). Re-run with section 12. |
| RWB-S4-E5004-CON | R-32399 | NEWAC-RWB-S4-E5004-CON-AC9 | 7 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | No anchor text for section 7 or 16 in this chunk; story file not found. The proposed test is Not specified in the source documents (NEWAC-RWB-S4-E5004-CON-AC9). Re-run with sections 7 and 16. |
| RWB-S4-E5005-CON | R-22804 | GAP-1748 | 14 | The message wording and the Thai and English versions of the S4 messages are not in the FSD | The inserted paragraph split the message table and was removed; the DL10 note still needs a place outside the table. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (25)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16903 | RWB-S4-E5001-APP | DOR-RWB-S4-E5001-APP-8 | 12.5 | Register activity issueDemandAndRecallNotices on task queue rwb-litigation and state the workflow ID form and start rule of LitigationWorkflow. |
| CDC-16906 | RWB-S4-E5001-APP | CG-ALL-8997 | 12.5 | Add activity issueDemandAndRecallNotices to the Activities sheet, or use a catalogued activity. |
| CDC-16914 | RWB-S4-E5001-CON | CG-ALL-9008 | 12.5 | Add an Activities row for issueDemandAndRecallNotices (Activity, task queue rwb-litigation), or use a catalogued activity instead. |
| CDC-16929 | RWB-S4-E5002-APP | CG-ALL-9019 | 12.5 | Namespace `rwb-recovery` restored in 12.5 and the scope line |
| CDC-16962 | RWB-S4-E5002-CON | CG-ALL-9036 | 12.5 | Add activity recordNoticeDelivery (queue rwb-litigation) to the Activities sheet, or name a catalogued activity instead. |
| CDC-16987 | RWB-S4-E5003-APP | CG-ALL-9049 | 12.5 | Add activity openNoticeAction to the Activities sheet on task queue rwb-litigation. |
| CDC-16988 | RWB-S4-E5003-APP | CG-ALL-9050 | 12.5 | Add activity evaluateNoticePeriodRule to the Activities sheet on task queue rwb-litigation. |
| CDC-16989 | RWB-S4-E5003-APP | CG-ALL-9051 | 12.5 | Add activity recordDecision to the Activities sheet on task queue rwb-litigation. |
| CDC-16990 | RWB-S4-E5003-APP | CG-ALL-9052 | 12.5 | Add activity attachProof to the Activities sheet on task queue rwb-litigation. |
| CDC-16991 | RWB-S4-E5003-APP | CG-ALL-9053 | 12.5 | Add activity startNoticePeriod to the Activities sheet on task queue rwb-litigation. |
| CDC-16992 | RWB-S4-E5003-APP | CG-ALL-9054 | 12.5 | Add activity announceCaseRoute to the Activities sheet on task queue rwb-litigation. |
| CDC-16993 | RWB-S4-E5003-APP | CG-ALL-9055 | 12.5 | Add activity announceNoticeUnserved to the Activities sheet on task queue rwb-litigation. |
| CDC-16994 | RWB-S4-E5003-APP | CG-ALL-9056 | 12.5 | Add activity expireNoticePeriod to the Activities sheet with the contract element of section 12.5 |
| CDC-16995 | RWB-S4-E5003-APP | CG-ALL-9057 | 12.5 | Add activity prescriptionWarning to the Activities sheet with the contract element of section 12.5 |
| CDC-16997 | RWB-S4-E5003-APP | DOR-RWB-S4-E5003-APP-8 | 12.5 | Add rows for the nine activities of 12.5: openNoticeAction, evaluateNoticePeriodRule, recordDecision, attachProof, startNoticePeriod, announceCaseRoute, announceNoticeUnserved, expireNoticePeriod, prescriptionWarning. |
| CDC-17021 | RWB-S4-E5004-APP | GAP-2756 | 7 | Name the PACK_ASSEMBLY trigger (case-state fact of R-LIT-15 or explicit start signal), the assembly activity and its queue; record whether any catalogue event has this producer. |
| CDC-17036 | RWB-S4-E5004-CON | GAP-2756 | find it | Name the pack assembly trigger as the case-state fact of R-LIT-15 (notice period expiry) and record that the assembly raises none of the three catalogue events. |
| CDC-17044 | RWB-S4-E5005-APP | DOR-RWB-S4-E5005-APP-8 | find it | Add activity checkPackDefects to the Activities sheet or the story must name a catalogued activity. Task queue and ID rules are now in the story. |
| CDC-17078 | RWB-S4-E5006-CON | CG-ALL-9131 | 12.5 | Add an Activities row for recoverMissingDocument on task queue rwb-litigation. |
| CDC-17088 | RWB-S4-E5007-APP | DOR-RWB-S4-E5007-APP-8 | 12.1 | Catalog: LitigationWorkflow on task queue rwb-litigation in namespace rwb-recovery; state its workflow ID form and start rule; add Activity verifyPack on rwb-litigation. |
| CDC-17090 | RWB-S4-E5007-APP | CG-ALL-9142 | 12.5 | Add an Activities row for verifyPack (type Activity, task queue rwb-litigation) or name a catalogued activity in the story. |
| CDC-17091 | RWB-S4-E5007-APP | CG-ALL-9143 | 12.5 | Add an Activities row for recordDecision (Activity through the library, task queue rwb-litigation) or name a catalogued activity in the story. |
| CDC-17092 | RWB-S4-E5007-APP | CG-ALL-9144 | 12.5 | Add an Activities row for raiseOfficerTask (type Activity, task queue rwb-litigation) or name a catalogued activity in the story. |
| CDC-17093 | RWB-S4-E5007-APP | CG-ALL-9145 | 12.5 | Add an Activities row for announceCaseRoute (type Activity, task queue rwb-litigation) or name a catalogued activity in the story. |
| CDC-17094 | RWB-S4-E5007-APP | CG-ALL-9146 | 12.5 | Add an Activities row for authoriseFiling (type Activity, task queue rwb-litigation) or name a catalogued activity in the story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (22)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16885 | RWB-S4-E2025-APP | CG-ALL-8982 | 16 | Add rows TC-S4-E2025-APP-01, -02, -03 and -04 with Given, When and Then copied from the criteria they cover (AC1, AC4, AC6, AC7 and AC8). |
| CDC-16887 | RWB-S4-E2025-APP | DOR-RWB-S4-E2025-APP-12 | 16 | Add rows TC-S4-E2025-APP-01 to -06 on tab Story test cases; align section 18 test lists with RTM v7. |
| CDC-16907 | RWB-S4-E5001-APP | CG-ALL-8999 | 16 | Add rows TC-E5-001-01 to TC-E5-001-05 to the next version under Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-16916 | RWB-S4-E5001-CON | DOR-RWB-S4-E5001-CON-12 | 12.7, 16 | Boundary test TC-S4-E5001-CON-04 added for §12.7 tables; TC-05 and TC-06 added; §16 lists 11 cases. |
| CDC-16923 | RWB-S4-E5001-CON | CG-ALL-9010 | 16 | No story edit; the 11 IDs are listed for the next Test Cases version. |
| CDC-16939 | RWB-S4-E5002-APP | CG-ALL-9023 | 16 | Add rows TC-E5-002-01 to TC-E5-002-06 with Given, When and Then copied from the criteria they cover. |
| CDC-16940 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-12 | 16 | Add the full Given/When/Then rows of TC-E5-002-01 to -06 and of the new TC-E5-002-07 to -12 under tab Story test cases. |
| CDC-16963 | RWB-S4-E5002-CON | DOR-RWB-S4-E5002-CON-12 | 16 | Add rows TC-E5-002-01 to -06 and TC-S4-E5002-CON-01 to -05 under the same IDs. |
| CDC-16972 | RWB-S4-E5002-CON | CG-ALL-9038 | 16 | Add TC-E5-002-01 to -06 and TC-S4-E5002-CON-01 to -04 as rows in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-16996 | RWB-S4-E5003-APP | CG-ALL-9058 | 16 | Add rows TC-E5-003-01 to TC-E5-003-09 with Given, When and Then copied from the criteria they cover (AC1 to AC6) |
| CDC-17008 | RWB-S4-E5003-CON | CG-ALL-9067 | 16 | Add rows for TC-E5-003-01 to -06, TC-S4-E5003-CON-01 to -06 with Given, When and Then copied from the criteria they cover |
| CDC-17013 | RWB-S4-E5004-APP | CG-ALL-9079 | 16 | Add rows TC-E5-004-01 to TC-E5-004-06 with Given, When and Then copied from the criteria they cover. |
| CDC-17015 | RWB-S4-E5004-APP | DOR-RWB-S4-E5004-APP-12 | 16 | Add tab Story test cases rows TC-E5-004-01 to TC-E5-004-06 under the same IDs. Story rows TC-E5-004-07 to -18 added in section 16. |
| CDC-17038 | RWB-S4-E5004-CON | CG-ALL-9089 | 16 | Add rows to the next Test Cases version for TC-E5-004-01 to TC-E5-004-06 and TC-S4-E5004-CON-01 to TC-S4-E5004-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-17047 | RWB-S4-E5005-APP | CG-ALL-9098 | 16 | Add rows TC-E5-005-01 to TC-E5-005-06 with Given, When and Then copied from AC1 to AC5, and rows TC-E5-005-07 to TC-E5-005-11 from section 16. |
| CDC-17059 | RWB-S4-E5005-CON | DOR-RWB-S4-E5005-CON-12 | 16 | Add the Story test cases rows for TC-E5-005-01 to TC-E5-005-06 and TC-S4-E5005-CON-01 to TC-S4-E5005-CON-04. |
| CDC-17060 | RWB-S4-E5005-CON | CG-ALL-9109 | 16 | Add rows for TC-E5-005-01 to TC-E5-005-06 and TC-S4-E5005-CON-01 to TC-S4-E5005-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-17069 | RWB-S4-E5006-APP | CG-ALL-9121 | 16 | Add rows TC-E5-006-01 to TC-E5-006-06 with Given, When and Then copied from the criteria they cover. |
| CDC-17081 | RWB-S4-E5006-CON | DOR-RWB-S4-E5006-CON-12 Test cases: Partial | 12.7, 16 | Boundary test TC-S4-E5006-CON-05 added to §16 for the §12.7 tables; §13 count updated to ten. |
| CDC-17084 | RWB-S4-E5006-CON | CG-ALL-9132 | 16 | Add rows for TC-E5-006-01 to -04 and TC-S4-E5006-CON-01 to -04, with Given, When and Then copied from the criteria they cover. |
| CDC-17095 | RWB-S4-E5007-APP | CG-ALL-9147 | 16 | Add rows TC-E5-007-01 to TC-E5-007-06 with Given, When and Then copied from the criteria they cover (AC1 to AC4, Access, Principle 5). |
| CDC-17096 | RWB-S4-E5007-APP | DOR-RWB-S4-E5007-APP-12 | 12, 12.7, 16 | Add rows for TC-E5-007-01 to TC-E5-007-08 under this story; the six existing IDs are not in the tab. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (20)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16877 | RWB-S4-E2025-APP | CG-ALL-8972 | 2, 7, 8, 12 | Record `party_names` as a source-only field code of RWB-P5-E2025-CON for type CONTRACT, or give it a dictionary name. Story already leaves it unmapped. |
| CDC-16878 | RWB-S4-E2025-APP | CG-ALL-8973 | 2, 7, 12 | Record `contract_amount` as a source-only field code of RWB-P5-E2025-CON for type CONTRACT, or give it a dictionary name. |
| CDC-16879 | RWB-S4-E2025-APP | CG-ALL-8974 | 2, 12 | Record `approval_no` as a source-only field code of RWB-P5-E2025-CON for type CREDIT_APPROVAL, or give it a dictionary name. |
| CDC-16880 | RWB-S4-E2025-APP | CG-ALL-8975 | 2, 12 | Record `approved_amount` as a source-only field code of RWB-P5-E2025-CON for type CREDIT_APPROVAL, or give it a dictionary name. |
| CDC-16881 | RWB-S4-E2025-APP | CG-ALL-8976 | 2, 12 | Record `approval_date` as a source-only field code of RWB-P5-E2025-CON for type CREDIT_APPROVAL, or give it a dictionary name. |
| CDC-16882 | RWB-S4-E2025-APP | CG-ALL-8977 | 2, 7, 12 | Record `mortgage_amount` as a source-only field code of RWB-P5-E2025-CON for type MORTGAGE_DOCUMENT, or give it a dictionary name. |
| CDC-16883 | RWB-S4-E2025-APP | CG-ALL-8978 | 2, 7, 12 | Record `registration_date` as a source-only field code of RWB-P5-E2025-CON for type MORTGAGE_DOCUMENT, or give it a dictionary name. |
| CDC-16884 | RWB-S4-E2025-APP | CG-ALL-8979 | 2, 7, 12 | Record `land_office` as a source-only field code of RWB-P5-E2025-CON for type MORTGAGE_DOCUMENT, or give it a dictionary name. |
| CDC-16888 | RWB-S4-E2025-APP | DOR-RWB-S4-E2025-APP-7 | 11 | Register or confirm the rwb-document field codes named in section 11 (filing_date, party_names, contract_amount, approval_no and the other unmapped codes) as LDM or Data Classification names. |
| CDC-16942 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-7 | 7, 11, 16 | Add served_result and decision_record as fields or entities, or align the story names to LDM v9. Story side: v_ace_pod read moved to rwb-source-data contract; decision-log wording changed to decision record. |
| CDC-16964 | RWB-S4-E5002-CON | DOR-RWB-S4-E5002-CON-7 | 11 | Add served_result as a field of notice, or name the existing LDM field that carries the served result; the story now has a BR Field ID column on every §11 row. |
| CDC-17004 | RWB-S4-E5003-CON | CG-ALL-9064 | 11 | Record decision_record as a platform library object owned by RWB-PLT-E1027-CON and applied in rwb_litigation, or add it to the dictionary. |
| CDC-17007 | RWB-S4-E5003-CON | DOR-RWB-S4-E5003-CON-7 | section 11 | Six element rows carry no BR Field ID; their BR Field ID stays Not specified (DOR-RWB-S4-E5003-CON-7). The two P2 names belong to LDM v9 and Data Classification v5. |
| CDC-17016 | RWB-S4-E5004-APP | DOR-RWB-S4-E5004-APP-7 | 11 | Register field period_expires_at of the notice period and entity decision_record (the library object of RWB-PLT-E1027-CON) with their owners, or confirm their names as they stand. |
| CDC-17031 | RWB-S4-E5004-CON | DOR-RWB-S4-E5004-CON-7 | 11 | Register decision_record as the platform library entity of DP-03 so that the P2 name check resolves. |
| CDC-17050 | RWB-S4-E5005-APP | DOR-RWB-S4-E5005-APP-7 | 11, 7, 16 | Add decision_record as the platform library entity of rwb_litigation, or confirm the name the story uses. |
| CDC-17066 | RWB-S4-E5006-APP | CG-ALL-9114 | 4, 8 | Record prescription_days_remaining as a dictionary field or as a named derived value of prescription_date in its owning document, or use the dictionary name. |
| CDC-17067 | RWB-S4-E5006-APP | CG-ALL-9115 | 11 | Record decision_record as a PLT library object of rwb_litigation (DP-03) in its owning document, or use the dictionary name. |
| CDC-17071 | RWB-S4-E5006-APP | DOR-RWB-S4-E5006-APP-7 | 11 | Add prescription_days_remaining and decision_record as a field or entity, each with its personal-data class. |
| CDC-17097 | RWB-S4-E5007-APP | DOR-RWB-S4-E5007-APP-7 | 11 | Terms note: legacy term kept in the legacy data block; section 7 reads decision record in AC1 and AC4 |

### API:(service not named) (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16898 | RWB-S4-E5001-APP | CG-ALL-8994 | 12.2 | Declare REST base /api/recovery/comms/v1 for the generate-and-send operation, using the provider's REST base from the Document Index service table. |
| CDC-16912 | RWB-S4-E5001-CON | CG-ALL-9005 | 12.2 | Declare the REST base /api/recovery/comms/v1 for rwb-comms, using the provider's base from the Document Index service table. |
| CDC-16925 | RWB-S4-E5002-APP | CG-ALL-9015 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the rwb-source-data provider |
| CDC-16926 | RWB-S4-E5002-APP | CG-ALL-9016 | 12.2 | Declare REST base /api/recovery/comms/v1 for the rwb-comms provider |
| CDC-16927 | RWB-S4-E5002-APP | CG-ALL-9017 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider |
| CDC-16928 | RWB-S4-E5002-APP | CG-ALL-9018 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rwb-decision provider |
| CDC-16934 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-8 | Header | Add the base paths /api/recovery/source-data/v1, /api/recovery/comms/v1, /api/recovery/case/v1 and /api/recovery/decision/v1, and the three further missing bases, to the API Specification v5 yaml. |
| CDC-16954 | RWB-S4-E5002-CON | CG-ALL-9030 | 12.2 | Declare REST base /api/recovery/source-data/v1 from the Document Index service table |
| CDC-16955 | RWB-S4-E5002-CON | CG-ALL-9031 | 12.2 | Declare REST base /api/recovery/comms/v1 from the Document Index service table |
| CDC-16956 | RWB-S4-E5002-CON | CG-ALL-9032 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table |
| CDC-16957 | RWB-S4-E5002-CON | CG-ALL-9033 | 12.2 | Declare REST base /api/recovery/decision/v1 from the Document Index service table |
| CDC-16968 | RWB-S4-E5002-CON | GAP-1189 | none | Name the proof-record operation with its request, answer, error envelope and no-response answer before the S4 client is built |
| CDC-16970 | RWB-S4-E5002-CON | GAP-1195 | none | Publish the proof-record write path, its request and answer fields and its Litigation right once the S4 contract is settled |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16874 | RWB-S4-E2025-APP | CG-ALL-8980 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/checked-fields in rwb-document.yaml through the provider contract RWB-P5-E2025-CON. |
| CDC-17053 | RWB-S4-E5005-CON | CG-ALL-9104 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/document-checklist (API-P5-008) in paths, or the consumer switches to a published operation |
| CDC-17054 | RWB-S4-E5005-CON | CG-ALL-9105 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/documents (API-P5-002) in paths, or the consumer switches to a published operation |
| CDC-17056 | RWB-S4-E5005-CON | DOR-RWB-S4-E5005-CON-8 | 12.2 | Publish the two rwb-document operations API-P5-008 and API-P5-002; catalog items resolved in the story |
| CDC-17061 | RWB-S4-E5006-APP | CG-ALL-9116 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/document-checklist (API-P5-008 of RWB-P5-E1040-APP) through the provider's CON story. |
| CDC-17062 | RWB-S4-E5006-APP | CG-ALL-9117 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/documents (API-P5-002 of RWB-P5-E1026-APP) through the provider's CON story. |
| CDC-17065 | RWB-S4-E5006-APP | DOR-RWB-S4-E5006-APP-8 | 1 | No edit. The P5 paths are not published by rwb-document, so the contract row keeps the P5 operations and the status is cross-document. |
| CDC-17074 | RWB-S4-E5006-CON | CG-ALL-9127 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/document-checklist (API-P5-008 of RWB-P5-E1040-APP) through the provider's CON story. |
| CDC-17075 | RWB-S4-E5006-CON | CG-ALL-9128 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/documents (API-P5-002 of RWB-P5-E1026-APP) through the provider's CON story. |
| CDC-17077 | RWB-S4-E5006-CON | CG-ALL-9127 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/document-checklist and GET /api/recovery/document/v1/cases/{caseId}/documents so both consumed operations resolve. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16905 | RWB-S4-E5001-APP | CG-ALL-8993 | 12.7 | Add decision_record as a dictionary entity, or record it as the PLT library object of DP-03 in the owning document. |
| CDC-16936 | RWB-S4-E5002-APP | CG-ALL-9013 | 4, 12.8 | Record served_result as a field of the rwb-comms notice answer (NoticeDelivered) or give it a dictionary name; no LDM name is near (credit_result, test_result, scan_result). |
| CDC-16961 | RWB-S4-E5002-CON | CG-ALL-9029 |  | Record served_result under its dictionary name in LDM v9 or Data Classification v5; no dictionary name is given in the sources. |
| CDC-16982 | RWB-S4-E5003-APP | CG-ALL-9043 | 4 | Add served_result as a field for the WIN delivery result, or record the object in the owning document. |
| CDC-16983 | RWB-S4-E5003-APP | CG-ALL-9044 | 4 | Add period_expires_at as a field, or confirm expires_at as the dictionary name for the notice period end. |
| CDC-16984 | RWB-S4-E5003-APP | CG-ALL-9045 | 8 | Add prescription_days_remaining as a field, or record the derived object for the warning threshold in the owning document. |
| CDC-16985 | RWB-S4-E5003-APP | CG-ALL-9046 | 11 | Section 11 names decision_record as the platform library object of DP-03 with LDM status Not specified. |
| CDC-17011 | RWB-S4-E5004-APP | CG-ALL-9076 | 8, 9 | Record period_expires_at as a field or object in LDM v9 Fields (Data owner), or name its dictionary equivalent. expires_at is only the nearest name and is not used. |
| CDC-17045 | RWB-S4-E5005-APP | CG-ALL-9094 | find it | Record decision_record as the platform library object created in rwb_litigation by RWB-PLT-E1027-CON (DP-03), or use the dictionary name. |
| CDC-17082 | RWB-S4-E5006-CON | GAP-2761 | find it | Add the recovery outcome element, the reason element and the reason list, with the list owned by the business; rewrite the §11 placeholder rows when they exist. |

### Epic design record (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16899 | RWB-S4-E5001-APP | DOR-RWB-S4-E5001-APP-14 | header | Record the signed epic design sign-off for this story's epic. |
| CDC-16913 | RWB-S4-E5001-CON | DOR-RWB-S4-E5001-CON-14 | n/a | Record the signed epic design sign-off for this story's epic; no source document holds it. |
| CDC-16930 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-14 | header | Record the signed epic design sign-off for RWB-S4-E5002-APP |
| CDC-16958 | RWB-S4-E5002-CON | DOR-RWB-S4-E5002-CON-14 | header | Record the signed epic design sign-off |
| CDC-16977 | RWB-S4-E5003-APP | DOR-RWB-S4-E5003-APP-14 | Header | Record the signed sign-off of the RWB-SVC-S4 epic design so that DOR item 14 can pass. |
| CDC-17027 | RWB-S4-E5004-CON | DOR-RWB-S4-E5004-CON-14 | Header | Record the signed epic design sign-off for RWB-S4-E5004-CON; no signed design is in the story or source documents |
| CDC-17042 | RWB-S4-E5005-APP | DOR-RWB-S4-E5005-APP-14 | find it | Record the signed epic design sign-off for EP05 / RWB-SVC-S4; no signed design is in the story or source documents. |
| CDC-17055 | RWB-S4-E5005-CON | DOR-RWB-S4-E5005-CON-14 | none | Record the signed epic design sign-off for RWB-S4-E5005-CON |
| CDC-17076 | RWB-S4-E5006-CON | DOR-RWB-S4-E5006-CON-14 Epic design: Fail | Header | Epic design sign-off row added as a placeholder: Not specified in the source documents (DOR-RWB-S4-E5006-CON-14). |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16908 | RWB-S4-E5001-APP | DOR-RWB-S4-E5001-APP-6 | 10 | Add SY-DATALOAD with the Litigation R right of TSD S4 T6.1, or remove the role from section 10 of this story. |
| CDC-16915 | RWB-S4-E5001-CON | DOR-RWB-S4-E5001-CON-1 | 1 | Confirm 'tech lead' as a role code or role name in Users Roles and Permissions v5, or add the role there. |
| CDC-16941 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-6 | 10 | Add role SY-DATALOAD, which section 10 already names, to Users Roles and Permissions v5. |
| CDC-17005 | RWB-S4-E5003-CON | DOR-RWB-S4-E5003-CON-1 | 1 | Add the role 'contract owner of rwb-litigation (S4)' as a role code or role name, or the story names the role already held there |
| CDC-17029 | RWB-S4-E5004-CON | DOR-RWB-S4-E5004-CON-1 | 1 | Add the role 'contract owner of rwb-litigation (S4)' or map it to an existing role code |
| CDC-17049 | RWB-S4-E5005-APP | DOR-RWB-S4-E5005-APP-6 | 10 | Add role SY-DATALOAD with Litigation R or U as TSD S4 T6.1 gives it. |
| CDC-17058 | RWB-S4-E5005-CON | DOR-RWB-S4-E5005-CON-1 | 1 | Confirm a role code or name for the section 1 actor; story actor is a placeholder until then |
| CDC-17070 | RWB-S4-E5006-APP | DOR-RWB-S4-E5006-APP-6 | 10 | Add role SY-DATALOAD with the Litigation R or U right of TSD S4 T6.1. |
| CDC-17079 | RWB-S4-E5006-CON | DOR-RWB-S4-E5006-CON-1 | 1 | Register 'tech lead' as a role name for rwb-litigation; role code Not specified in the source documents (DOR-RWB-S4-E5006-CON-1) |

### RWB-S4-E5002-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16932 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-21 | header | Move build status from Not started to Done |
| CDC-16933 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-22 | header | Publish the contract fake and record its library version as published |
| CDC-16943 | RWB-S4-E5002-APP | GAP-0437 | 13 | Publish the proof-record operation with path, shapes and error envelopes; add the notice proof write to the rwb-comms baseline; add LDM field IDs for the notice lifecycle state and the three case notice facts; fix LOV-DELIVERY to notice-state mapping; version the notice-period duration and proof window as reference rows with codes; record in P6 and S4 appendices that the v_ace_pod loop is the Epic 2 dispatch story; attach the requirement ID to FEAT-LIT-02 in the EP05 PRD. |
| CDC-16945 | RWB-S4-E5002-APP | GAP-0737 | 4 | Publish the rwb-litigation delivery-outcome operation on /api/recovery/litigation/v1; store notice reference, delivery date and outcome on recovery_case; notice-period duration as SERVICE_LEVEL row owned by RW-COE; attach REQ ID in EP05 PRD. |
| CDC-16946 | RWB-S4-E5002-APP | GAP-1189 | 12 | Name the proof-record operation with its request, answer, error envelope and no-response answer before the S4 client is built; agree the shape at wave 3 contract review. |
| CDC-16947 | RWB-S4-E5002-APP | GAP-1192 | 4 | Step 5 refuses PENDING and defers the REFUSED/PENDING meaning and the LOV-DELIVERY contract. |
| CDC-16948 | RWB-S4-E5002-APP | GAP-1195 | 12.1 | Publish the proof-of-delivery write path, its request and answer fields and its Litigation C right in the service API specification and contract story, sharing one shape with edge, tests and S4. |
| CDC-16976 | RWB-S4-E5002-CON | GAP-1190 | header | When the plan is regenerated, add RWB-PLT-E1027-CON and RWB-PLT-N001-CON to Depends on (build) of RWB-S4-E5002-CON. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16909 | RWB-S4-E5001-APP | GAP-2743 | header, 13 | PRD reference row carries a Not specified placeholder for the requirement ID, not REQ-S4-001 |
| CDC-16910 | RWB-S4-E5001-APP | GAP-2742 | header, 13 | Record notice and template rows as P6 rwb_comms owned, name P6 generate and send and case answer operations, and decide once in EP05 PRD whether D7.1 approval gates the step. |
| CDC-16911 | RWB-S4-E5001-APP | GAP-1738 |  | Add Tables sheet rows, owner S4, for judgment, enforcement record, auction round, pack, notice state, deferral and decision record, with their key fields as product requirements. |
| CDC-16920 | RWB-S4-E5001-CON | GAP-1738 | 16 | Add rows for judgment, enforcement, auction round, pack, notice state and deferral, owner S4, with key fields as product requirements; no physical table name beyond legal_action and hearing. |
| CDC-16980 | RWB-S4-E5003-APP | GAP-1740 | 4 | Record rwb-comms as owner of the template, merge fields, delivery and proof of delivery, returning NoticeDelivered. This service keeps the notice decision, approval, notice period and case notice state. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16917 | RWB-S4-E5001-CON | DOR-RWB-S4-E5001-CON-9 | 14 | Give MSG-P1-001 the text of its Standard v4 entry, or update that entry to the §14 wording. |
| CDC-16922 | RWB-S4-E5001-CON | CG-ALL-9009 | 14 | MSG-P1-001 message cell left as it was |
| CDC-16971 | RWB-S4-E5002-CON | CG-ALL-9037 | 14 | No story text changed; the English MSG-P1-001 wording cannot be confirmed from the sources. |
| CDC-17017 | RWB-S4-E5004-APP | DOR-RWB-S4-E5004-APP-9 | 14 | Align MSG-P1-001 text with the standard, or record the FSD S4 VR-S4-004-1 text as the standard's exception. |
| CDC-17023 | RWB-S4-E5004-APP | CG-ALL-9078 | 14 | MSG-P1-001 text kept as in the story until the standard ruling |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16886 | RWB-S4-E2025-APP | DOR-RWB-S4-E2025-APP-11 | 11 | Confirm the personal-data class of party_names (marked personal in AC7) and of the other unmapped codes of section 11. |
| CDC-17030 | RWB-S4-E5004-CON | DOR-RWB-S4-E5004-CON-11 | 11 | Confirm the personal-data class of the flagged fields so it matches the story's no-personal-data statement |
| CDC-17048 | RWB-S4-E5005-APP | DOR-RWB-S4-E5005-APP-11 | 11 | Classify each field of section 11 and remove any field classed as personal data from the read or write list; the field is not named in the source documents. |

### RWB-S4-E5001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16900 | RWB-S4-E5001-APP | DOR-RWB-S4-E5001-APP-21 | header | Move build status from Not started to Done. |
| CDC-16901 | RWB-S4-E5001-APP | DOR-RWB-S4-E5001-APP-22 | header | Publish a contract fake library version and record it as published. |
| CDC-16902 | RWB-S4-E5001-APP | DOR-RWB-S4-E5001-APP-23 | header | State the fixed contract version this story builds against, beyond the /v1 path. |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16937 | RWB-S4-E5002-APP | CG-ALL-9014 | 11 | Record decision_record as the library table object created in rwb_litigation by the library migration (DP-03). |
| CDC-17012 | RWB-S4-E5004-APP | CG-ALL-9077 | 12.7 | Confirm decision_record as a PLT library object row in its shape document, or as a dictionary entry. |
| CDC-17028 | RWB-S4-E5004-CON | CG-ALL-9087 | 12.7 | Record decision_record as a library object with its columns in the owning document, so the name is defined there |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-litigation.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16999 | RWB-S4-E5003-CON | CG-ALL-9065 | 7 | Remove the fixed enum on status and bind it to LOV-LEGAL-STATUS as reference data, so a new list value needs no code change (ruling: data). |
| CDC-17000 | RWB-S4-E5003-CON | CG-ALL-9066 | 7 | Remove the fixed enum on actionType and bind it to LOV-LEGAL-TYPE as reference data, so a new list value needs no code change (ruling: data). |
| CDC-17001 | RWB-S4-E5003-CON | DOR-RWB-S4-E5003-CON-8 | 7 | Remove the closed status and actionType enums and bind both to LOV-LEGAL-STATUS and LOV-LEGAL-TYPE as reference data, per CG-ALL-9065 and CG-ALL-9066. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17025 | RWB-S4-E5004-APP | GAP-2755 | 12 | Record the pack as a read view of the legal action with no operation of its own; API-S4-001 is owned by the notice stories of this service. |
| CDC-17034 | RWB-S4-E5004-CON | GAP-2753 | 11 | State that the pack is derived on every read from API-P5-002, API-P5-008 and API-P3-002; add no pack table or snapshot object to the Ownership Map. |
| CDC-17040 | RWB-S4-E5004-CON | GAP-2755 | 8 | Record that the pack is a read view of the legal action with no operation of its own, and that API-S4-001 is owned by the notice stories of this service; any future pack path goes to the TSD inventory first. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17046 | RWB-S4-E5005-APP | CG-ALL-9097 | 12.5 | Add activity checkPackDefects with task queue rwb-litigation and its contract element, or name a catalogued activity in RWB-S4-E5005-APP 12.5. |
| CDC-17057 | RWB-S4-E5005-CON | CG-ALL-9108 | 12.5 | Add a checkPackDefects row to Activities, or name a catalogued activity |
| CDC-17068 | RWB-S4-E5006-APP | CG-ALL-9120 | 12.5 | Add a row for activity recoverMissingDocument on task queue rwb-litigation, or name a catalogued activity in section 12.5. |

### RWB-S4-E5006-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17063 | RWB-S4-E5006-APP | DOR-RWB-S4-E5006-APP-21 | header | Complete the contract build and set its build status from Not started to Done. |
| CDC-17064 | RWB-S4-E5006-APP | DOR-RWB-S4-E5006-APP-22 | header | Publish the contract fake library and record its version as published. |
| CDC-17072 | RWB-S4-E5006-APP | GAP-2761 | 11, 13 | Add the recovery element and the gap-reason element; if the reason is stored, add it to the LDM and the DB story with a business-owned reason list. |

### RWB-S4-E5007-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17086 | RWB-S4-E5007-APP | DOR-RWB-S4-E5007-APP-21 | header | Set build status to Done with the contract published before this story is ready |
| CDC-17087 | RWB-S4-E5007-APP | DOR-RWB-S4-E5007-APP-22 | header | Publish the contract fake library and record its version as published |
| CDC-17102 | RWB-S4-E5007-APP | GAP-2770 | 12.2 | Publish verification and filing authorisation as additive PATCH properties or separate schemas; route fact and task raise as consumed case-answer elements; placeholder for field lists no source gives; pack element consumed only, rwb-document owner named. |

### RWB-P5-E2025-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16891 | RWB-S4-E2025-APP | GAP-1020 | header | Publish checked-fields read on /api/recovery/document/v1/cases/{caseId}/checked-fields with CheckedField and CheckedFieldSet shapes as smallest superset of the legacy list; confirm names with S4 and S2 before wave 2 release. |
| CDC-16895 | RWB-S4-E2025-APP | GAP-1900 | header | Publish one GET on the rwb-document base with case and document type parameters, CheckedField list answer filtered by state and masked by role; keep legacy element names. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16894 | RWB-S4-E2025-APP | GAP-1877 | header | Align the S2 Treatment / P5 Document cell with the one-hop REST read of RWB-P5-E2025-CON, or record the Temporal alternative explicitly. |
| CDC-16924 | RWB-S4-E5001-CON | GAP-1747 | 15 | Route and this service's part for SCR-19 and SCR-20 set to Not specified |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16918 | RWB-S4-E5001-CON | GAP-2743 | header, 4 | Record the P6 notice generate and send and the rwb-case stage answer as non-blocking C dependencies with placeholders; record the notice and template rows as P6's; name the P6 operations in its contract story. |
| CDC-16919 | RWB-S4-E5001-CON | GAP-2742 | header, 4 | Carry the two consumed calls as non-blocking C rows; record the notice and template rows as P6's or correct the S4 row; decide the D7.1 gate in the EP05 PRD. |

### RWB-S4-E5003-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16978 | RWB-S4-E5003-APP | DOR-RWB-S4-E5003-APP-21 | Header | Set the build status to Done with the contract published before this story starts. |
| CDC-16998 | RWB-S4-E5003-APP | GAP-2750 | 12.4 | Publish the three operations on base /api/recovery/litigation/v1, the LegalActionRequest, LegalAction and NoticeActionUpdate schemas over DF-LEG-001 to DF-LEG-014, the legal_action DDL with the primary key only, the six error statuses with the problem envelope, the Idempotency-Key rule, the versioning rule and the fakes; the period element is declared on noticeDeliveryResult and the read answer; index set and period length Not specified (GAP-2750). |

### RWB-S4-E5004-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17009 | RWB-S4-E5004-APP | DOR-RWB-S4-E5004-APP-21 | header | Publish the contract so its build status moves from Not started to Done. |
| CDC-17010 | RWB-S4-E5004-APP | DOR-RWB-S4-E5004-APP-22 | 12.8 | Record the published contract fake library version for rwb-case and rwb-document. |

### OTHER:P3 story carrying MSG-P1-001 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17032 | RWB-S4-E5004-CON | DOR-RWB-S4-E5004-CON-9 | 14 | Set MSG-P1-001 text to the Error and Message Standard v4 English text: {product} is from {date}. Today's load has not arrived. This story's section 14 already matches it. |
| CDC-17037 | RWB-S4-E5004-CON | CG-ALL-9088 | 14 | No edit: MSG-P1-001 text in this story is left as it was. |

### OTHER:P3 rwb-case contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17033 | RWB-S4-E5004-CON | GAP-2751 | Header | Name the case-state announcement and the task raise operations with their answer shapes when the P3 contract is next versioned. |
| CDC-17035 | RWB-S4-E5004-CON | GAP-2754 | 11 | Name NOTICE_BLOCKED, PACK_ASSEMBLY, PACK_VERIFIED and PACK_DEFECT_HOLD in the case state list and publish the state-announcement operation and its answer shape. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17099 | RWB-S4-E5007-APP | GAP-2771 | 13 | List API-S4-001 notice approval under the E2 notice story, not rwb-litigation; record the E2 delivery in the Change Register. |
| CDC-17101 | RWB-S4-E5007-APP | GAP-2766 | 11 | Record the legacy RWB-E5-007 section 11 data block and section 4 endpoint block as Outdated. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16875 | RWB-S4-E2025-APP | CG-ALL-8981 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml through the provider contract RWB-P3-E1042-CON. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16876 | RWB-S4-E2025-APP | DOR-RWB-S4-E2025-APP-8 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/checked-fields in rwb-document.yaml (RWB-P5-E2025-CON) and GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml (RWB-P3-E1042-CON). |

### OTHER:Functional Specification Document S2 (FSD S2 A1.1; OTHER:A2.1.2 to A2.18.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16889 | RWB-S4-E2025-APP | GAP-1713 | find it | Record once in the service contract the owning service of each prerequisite code (P7, P3, P5, P6, S1); FEAT-CHO-08 stays as written. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16890 | RWB-S4-E2025-APP | GAP-3194 | find it | Raise an ACE DB story for the column drop of hearing and legal_action in rwb_litigation (S4), or cite the owning story, and record its ID on row 121 before wave 2. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16892 | RWB-S4-E2025-APP | GAP-0407 | 13 | Record GAP-0407 as owned by the Integration lead: agree classifier version, masked sample pack and extraction report with P5 and P10 owners, and wave 2 harness pack, seeding and evidence format with QA. |

### OTHER:TSD S2 v2 T3.1 (rwb-treatment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16893 | RWB-S4-E2025-APP | GAP-1876 | header | Add contract_amount, contract_date, mortgage_amount, registration_date, land_office, title_doc_no and source_document_id, source_doc_version, source_table_version to treatment; keep party_names masked and unstored; stamp reader tableVersion. |

### OTHER:TSD S2 v2 (rwb-treatment S2 story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16896 | RWB-S4-E2025-APP | GAP-2702 | header | Read via RWB-P5-E2025-CON; add fact and source columns named for extracted codes; map only same-name codes; stamp reader tableVersion; mask party_names and store none. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16897 | RWB-S4-E2025-APP | CG-ALL-8983 | 18 | Align the REQ-DCM-006 and REQ-DCM-005 test lists with RWB-S4-E2025-APP section 18 in the next version. |

### OTHER:rwb-decision (R-LIT-03 package code, version label and owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16904 | RWB-S4-E5001-APP | GAP-1742 | 12.5 | Story names the dependency; package code, version label and owner are not in the sources |

### OTHER:Recovery Workbench Functional Specification S4 (rows A2.1.4.1 to A2.22.4.4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16921 | RWB-S4-E5001-CON | GAP-1743 | 7 (not in chunk) | Write one step-specific criterion per feature from its named rules, citing the FSD row; add origin-tagged scenarios to section 7 and their test rows to section 16. |

### RWB-S4-E5002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16931 | RWB-S4-E5002-APP | DOR-RWB-S4-E5002-APP-16 | header | Size row kept as Not specified |

### OTHER:Recovery Workbench Business Requirements Program v5 (release plan and section 10.2 wave map) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16935 | RWB-S4-E5002-APP | GAP-1741 | Header | Publish the notice contract, its fake and its schema as slice 2.1 in wave 2 before RWB-SVC-S4 wave 3, so the EP02 notice stories keep wave 2. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16938 | RWB-S4-E5002-APP | CG-ALL-9021 | 12.5 | Add activity recordNoticeDelivery on task queue rwb-litigation, or name a catalogued activity in its place. |

### OTHER:Wave 3 journey harness pack (W3J01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16944 | RWB-S4-E5002-APP | GAP-0436 | none | Agree harness environment, seeding set, business date, product codes, unnamed operations, evidence format and gate thresholds at the wave 3 entry check with the integration and QA leads. |

### OTHER:Recovery Workbench FSD P6 Communications v3 (next version); OTHER:Epics 3 to 8 Specification v3 row FEAT-LIT-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16949 | RWB-S4-E5002-APP | GAP-1194 | find it | Record that the officer-recorded path of RWB-S4-E5002-APP is the manual correction path of the same notice; keep the automatic v_ace_pod read and unattended trigger in RWB-P6-E2021-APP and RWB-P6-E1055-APP on the rwb-source-data contract. |

### OTHER:split_plan.json (RWB-E5-002 split, next plan revision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16950 | RWB-S4-E5002-APP | GAP-1191 | find it | Add DP-11 to the pattern set of the RWB-E5-002 slices that consume or serve a contract; until then DP-11 is not claimed and no dependency row is added. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16951 | RWB-S4-E5002-APP | GAP-1193 | find it | Quote each criterion as '<story ID> ACn' in the registers, the RTM and the Covers column for secondary slices. |

### OTHER:Epics 3 to 8 PRD (EP05) and FSD S4 module trace (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16952 | RWB-S4-E5002-APP | GAP-2747 | find it | Add one requirement row for the proof of delivery as the start of the notice period; then rewrite the requirement column of both stories and fragments. REQ-S4-001 stays until then. |

### RWB-P6-E5002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16953 | RWB-S4-E5002-APP | GAP-1190 | find it | On plan regeneration, Depends on (build) for RWB-P6-E5002-APP carries RWB-PLT-E1027-CON and RWB-PLT-N001-CON; build against fakes until then. |

### API:(service not named); OTHER:P6; OTHER:P3; OTHER:P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16959 | RWB-S4-E5002-CON | DOR-RWB-S4-E5002-CON-8 | 12.2 | Declare REST bases of the four consumed paths |

### OTHER:Recovery Workbench Business Requirements Program v5 (release plan and R5.6 wave map) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16960 | RWB-S4-E5002-CON | GAP-1741 |  | Publish the notice contract, its fake and its schema as slice 2.1 in wave 2 before wave 3; notice stories keep EP02 wave 2 under R5.6. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:TSD P6 and S4 appendices; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16965 | RWB-S4-E5002-CON | GAP-0437 | find it | Add the notice lifecycle state and the three notice facts with field IDs; publish the proof-record operation with paths and shapes; version the LOV-DELIVERY mapping and the notice-period and proof-window reference rows; attach the requirement ID to FEAT-LIT-02. |

### OTHER:Wave 3 journey harness pack (W3J01) and its wave 3 entry-check record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16966 | RWB-S4-E5002-CON | GAP-0436 | none | Record the harness environment, seeded identifiers, business date, product codes, the three operation owners, evidence format and gate thresholds as agreed at the wave 3 entry check |

### OTHER:EP05 PRD; OTHER:TSD S4 and P6 appendices (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16967 | RWB-S4-E5002-CON | GAP-0737 | find it | Attach the REQ identifier to this feature in the EP05 PRD; publish the S4 delivery-outcome operation with its fields in the S4 appendix; add the notice-period duration as a SERVICE_LEVEL reference row of rwb-case, owner RW-COE. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16969 | RWB-S4-E5002-CON | GAP-1192 | 11 | PENDING is refused and leaves the notice unchanged until mapped; the meaning of REFUSED is open |

### OTHER:RWB FSD P6 Communications v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16973 | RWB-S4-E5002-CON | GAP-1194 |  | Record that the officer-recorded path of this story is the manual correction path of the same notice, next to the automatic v_ace_pod read in RWB-P6-E2021-APP and RWB-P6-E1055-APP. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16974 | RWB-S4-E5002-CON | GAP-1191 | 12 | At the next plan revision, add DP-11 to the pattern set of the RWB-E5-002 slices that consume or serve a contract. |

### OTHER:Epics 3 to 8 PRD (EP05) and the S4 module trace (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16975 | RWB-S4-E5002-CON | GAP-2747 | 18 | Add one requirement row covering the proof of delivery as the start of the notice period; then rewrite the requirement column of RWB-E5-002 and both stories and fragments. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16979 | RWB-S4-E5003-APP | DOR-RWB-S4-E5003-APP-22 | Header | Record a published fake library version for RWB-S4-E5003-CON. |

### OTHER:Recovery Workbench Business Requirements Program v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16981 | RWB-S4-E5003-APP | GAP-1741 | Header | Add slice 2.1 publishing the notice contract, fake and schema in wave 2 for EP02, before wave 3 for RWB-SVC-S4. |

### OTHER:Standard v4 (error message IDs) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16986 | RWB-S4-E5003-APP | CG-ALL-9047 | 12.1 | Error answers 401, 404, 409 and 503 read Not specified in the source documents (CG-ALL-9047; DOR-RWB-S4-E5003-APP-17). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17002 | RWB-S4-E5003-CON | GAP-1740 | 2 | Limit rwb-comms to template, merge fields, delivery and proof of delivery, returning NoticeDelivered with delivered_at; keep notice decision, approval and notice period with rwb-litigation, which alone writes the notice state on the case. |

### OTHER:Recovery Workbench Business Requirements Program v5 (section 10.2 and wave map R5.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17003 | RWB-S4-E5003-CON | GAP-1741 | header | Schedule the notice contract, its fake and its schema as slice 2.1 in wave 2, ahead of RWB-SVC-S4 in wave 3, and let the rest of the notice capability follow in wave 3. |

### RWB-S4-E5003-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17006 | RWB-S4-E5003-CON | DOR-RWB-S4-E5003-CON-10 | find it | Add empty, loading, error and no-access states for SCR-18 and SCR-19 |

### OTHER:Recovery Workbench Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17014 | RWB-S4-E5004-APP | DOR-RWB-S4-E5004-APP-10 | 15 | Add the empty, loading, error and no access states to SCR-18 Notice approval and SCR-19 Litigation workspace. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17018 | RWB-S4-E5004-APP | GAP-2751 | header | Add non-blocking rows for API-P5-002, API-P5-008 and API-P3-002 built against fakes; C dependency to RWB-P3-E1043-CON for the reference-data read; DP-08 declared right as edge and guard rule. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:S4 data model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17019 | RWB-S4-E5004-APP | GAP-2753 | 11 | State that the pack is derived on every read from API-P5-002, API-P5-008 and API-P3-002 and holds no table; no snapshot object unless the Ownership Map adds one. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17020 | RWB-S4-E5004-APP | GAP-2754 | 8 | Name NOTICE_BLOCKED, PACK_ASSEMBLY, PACK_VERIFIED and PACK_DEFECT_HOLD in the case state list and publish the state-announcement operation and its answer shape. |

### OTHER:FSD S4 field catalogue (A2.6.3.2 to A2.21.3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17022 | RWB-S4-E5004-APP | GAP-1739 | 12.7 | Type legal_action.case_id as a varchar(255) business key with no foreign key, keeping the field name. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17024 | RWB-S4-E5004-APP | GAP-2752 | header | Add one requirement row covering the pack assembly; then rewrite the requirement column of both stories and their fragments. |

### OTHER:Message catalogue; OTHER:TSD S4 v2; 06 Data/Recovery Workbench Physical Schema v7; RWB-S4-E5005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17026 | RWB-S4-E5004-APP | GAP-2757 | 14 | Publish the index set, the 400 and 409 message IDs and texts, and the defect-list items; then replace the placeholders in the stories. |

### OTHER:Epics 3 to 8 PRD; OTHER:FSD S4 v3 module trace (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17039 | RWB-S4-E5004-CON | GAP-2752 | header | Add one requirement row covering pack assembly as a composition of the document index and case facts with the withdrawn-template hold, then rewrite the requirement column of both stories and their fragments. |

### OTHER:TSD S4 v2 and the message catalogue; RWB-S4-E5005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17041 | RWB-S4-E5004-CON | GAP-2757 | 14 | Publish the legal_action index set with the rwb_litigation physical schema file; add the 400 and 409 message IDs and texts to the message catalogue; name the defect-list items in RWB-S4-E5005-APP and its reference data. |

### RWB-S4-E5005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17043 | RWB-S4-E5005-APP | DOR-RWB-S4-E5005-APP-21 | find it | Set build status to Done so the contract is published before this story can pass the contract gate. |

### OTHER:FSD S4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17051 | RWB-S4-E5005-APP | GAP-1739 | 12 | Field catalog rows A2.6.3.2 to A2.21.3.2: legal_action.case_id type uuid becomes varchar(255) business key with no foreign key; field name kept. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17052 | RWB-S4-E5005-APP | GAP-2757 | 14 | Publish legal_action index set beyond primary key; assign message IDs and text for the 400 and 409 rows; name the defect-list items in reference data. |

### OTHER:P5 rwb-document interface specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17073 | RWB-S4-E5006-APP | GAP-2764 | 13 | Record that the CCMS leg of the item request is reached only through the rwb-document contract. |

### RWB-S4-E5006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17080 | RWB-S4-E5006-CON | DOR-RWB-S4-E5006-CON-10 | find it | Declare empty, loading, error and no-access states for SCR-19 and SCR-20; this contract declares no screen. |

### OTHER:Recovery Workbench P5 rwb-document interface specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17083 | RWB-S4-E5006-CON | GAP-2764 | 12.2 | Record that CCMS is reached only through the rwb-document hub on the P5 contract; no CCMS path or dependency row is added to this story. |

### RWB-S4-E5007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17085 | RWB-S4-E5007-APP | DOR-RWB-S4-E5007-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S4 / EP05 in the epic design record |

### OTHER:PLT decision-record library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17089 | RWB-S4-E5007-APP | CG-ALL-9137 | 11 | Record decision_record as a library table object created in rwb_litigation |

### OTHER:Wave 3 contract freeze: rwb-document, rwb-comms, rwb-case and rwb-decision contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17098 | RWB-S4-E5007-APP | GAP-2765 | 13 | Publish the pack and defect-list read, the notice and template-status read, the case read with route fact and task raise, the D7 approval raise, and the reference-data read of RWB-P3-E1043-CON. |

### OTHER:FSD S4 field catalogues A2.6.3.2 to A2.21.3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17100 | RWB-S4-E5007-APP | GAP-1739 | 11 | Type legal_action.case_id as a varchar(255) business key with no foreign key, keeping the field name. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0068 | Wave conflict S4 / EP02 | Tech lead | Resolved (directive) |
| GAP-0407 | The extraction harness pack, the classifier version and the cross-service reader pack are not specified | Integration lead | Resolved (directive) |
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-0437 | The legacy delivery step is split across rwb-comms, rwb-litigation and rwb-case with no named hand-off operation and no named reference rows, so the end-to-end chain of RWB-E5-002 has no single source of record | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0737 | The split of the proof-of-delivery key between rwb-case, rwb-litigation and rwb-comms, the S4 answer, the notice-period duration and the requirement ID are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1021 | The published Java reader becomes a REST contract no source names, the extraction operations belong to another baseline of the same service, and the plan lists no C row for the case read | Tech lead | Resolved (directive) |
| GAP-1022 | The deployment values of the extension are not specified: the model name and the provider product behind the agent route, the alert thresholds and identifiers, the evaluation cadence, the business-hours window and the reader thresholds | DevOps team | Resolved (directive) |
| GAP-1189 | The proof-record operation of RWB-S4-E5002-CON is not named in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1190 | The platform contract rows that DP-03 and DP-19 add are not in this story's build list | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1191 | DP-11 is absent from the pattern set of a story that consumes one published operation | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1192 | The meaning of the two unexercised LOV-DELIVERY values, and the contract the list is read on, are not stated | Business analyst, P6 | Resolved (directive) |
| GAP-1193 | The labels AC1 to AC8 are reused by three documents of the same legacy key for different criteria | Business analyst, P6 | Resolved (directive) |
| GAP-1194 | The source reads the proof of delivery from v_ace_pod in process, and this story may read no ACE view | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1195 | The proof-record path, its fields and its right are this story's design, because no source names a proof-record operation | Solution architect | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1736 | FSD S4 reads the ACE views and the batch-status view directly, while Architecture v5 allows only rwb-source-data to read them and the connection matrix gives S4 no cell to P1 | Solution architect | Resolved (directive) |
| GAP-1737 | The connection matrix gives S4 no cell to rwb-document, rwb-payment or rwb-agent, while the FSD names the document hub, ALS and GL and the model gateway | Solution architect | Resolved (directive) |
| GAP-1738 | The Ownership Map gives rwb-litigation two tables, while Architecture v5 gives the schema judgments, enforcement and the LED auction ladder and the FSD holds notice, pack and deferral state | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1739 | legal_action.case_id is a uuid in the FSD, while ADR-014 and DP-01 forbid a cross-schema foreign key and require a varchar(255) business key | Data architect | Resolved (directive) |
| GAP-1740 | The notice and its proof of delivery sit in S4 in the FSD and in rwb-comms in Architecture v5 and the Ownership Map, and the three notice paths are split across the two services | Solution architect | Resolved (directive) |
| GAP-1741 | The notice capability is first needed in Epic 2 (wave 2, 31 December 2026 (tentative)) while the service is created in wave 3 | Solution architect | Resolved (directive) |
| GAP-1742 | Thirty-two of the seventy-nine R-LIT rules are named in the FSD and the litigation rule package is Phase 2 | Center of excellence analyst | Resolved (directive) |
| GAP-1743 | Every FSD acceptance criterion is the same generic sentence and there is no alternate flow and no background event for any of the twenty-two features | Business analyst, S4 | Resolved (directive) |
| GAP-1745 | R-LIT-01 starts litigation on route R4 while the case journeys call R4 the guarantee claim and R5 litigation | Business analyst, S4 | Resolved (directive) |
| GAP-1747 | The three S4 screens have no owner cell in the v5 screen matrix, and SCR-18's first-in is Epic 2 | Solution architect | Resolved (directive) |
| GAP-1748 | The message wording and the Thai and English versions of the S4 messages are not in the FSD | Business analyst, S4 | Resolved (directive) |
| GAP-1749 | The sources state no litigation, hearing or enforcement volume for this module, and no release date other than the program release plan | Solution architect | Resolved (directive) |
| GAP-1876 | The checked-fields operation and payload on the treatment side, the treatment columns that carry the contract and mortgage facts, the masking of the treatment read and who stamps the type-table version are not specified | Solution architect with the rwb-treatment and rwb-document squads | Resolved (directive) |
| GAP-1877 | Architecture v5 puts the S2 call to P5 in the Temporal column while the legacy published interface and DP-11 make the checked-fields read one REST hop | Solution architect with the platform workflow team, rwb-document and rwb-treatment | Resolved (directive) |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1899 | DP-09 and DP-10 are in the pattern list but this slice produces no event, consumes no event and registers no Schedule, and DocumentFieldsExtracted is consumed by rwb-case only | Solution architect | Resolved (directive) |
| GAP-1900 | The sources give only the Java interface of the field reader: no REST operation, path, transport or field-level name is named for the checked-fields read | Solution architect, with the rwb-document owner (P5) | Resolved (directive) |
| GAP-1901 | The mapping of an extracted field code onto an S4 column is not stated, and eleven codes, hearing_type and lawsuit_no have no counterpart of the same name | Business analyst and solution architect, with the rwb-document owner | Resolved (directive) |
| GAP-1902 | REQ-DCM-017 and REQ-DCM-018 are in the plan's requirement list for this story but in no row of the legacy traceability table, and legacy section 19 puts them out of scope | Business analyst | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1904 | SCR-19 Litigation workspace is listed with its first release in E5, while this story is a wave 2 story released on 31 December 2026 | Solution architect and the edge owner | Resolved (directive) |
| GAP-1905 | No approval of the realigned story or of the sources it consumes is recorded, so the story runs in Draft | Solution architect | Resolved (directive) |
| GAP-2702 | The treatment-side checked-field read, the fact columns it fills, the type-table version stamp and the unmapped field codes are not specified | Tech lead of rwb-treatment with the P5 owner of the checked-field contract and the rwb-treatment data owner | Resolved (directive) |
| GAP-2703 | Architecture v5 puts the S2 read of rwb-document on Temporal while the legacy interface and DP-11 make it one REST hop | Solution architect with the P5 contract owner and the platform Temporal owner | Resolved (directive) |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2744 | The delivery fact has no home in rwb-litigation and no published operation on any of the three services it crosses | Solution architect, S4 rwb-litigation, with the P1 rwb-source-data and P6 rwb-comms architects | Resolved (directive) |
| GAP-2745 | The proof of delivery is named as an event in the rules and the FSD, while the service publishes and consumes nothing and the case answer has no operation name | Solution architect, S4 rwb-litigation, with the P3 rwb-case and P6 rwb-comms architects and the event platform team | Resolved (directive) |
| GAP-2747 | The legacy master carries no requirement identifier for RWB-E5-002, so both stories trace to the feature and one module requirement | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2748 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |
| GAP-2749 | The notice period on the target: no period length, no timer home, no timer-ledger write path, no published operation of the four consumed services, no notice-period state value and no service event | Tech lead of rwb-litigation | Resolved (directive) |
| GAP-2750 | The notice-period contract: no period element behind a column, no index set, no operation name for the four consumed services, no notice table of this service and no text for the 409 or the 400 | Tech lead of rwb-litigation | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2751 | The four consumed reads and the two handed-over operations of the pack carry no dependency row, and two of the operations have no published name | Solution architect, S4 rwb-litigation, with the P5 rwb-document, P3 rwb-case and P4 rwb-access architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2752 | The legacy master carries no requirement identifier for RWB-E5-004, so both stories trace to the feature only | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2753 | The pack has no table in the Ownership Map and no object in TSD S4 T3.1, so where an assembled pack is held is not stated by any source | Solution architect and data steward, S4 rwb-litigation, with the P5 rwb-document data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2754 | NOTICE_BLOCKED, PACK_ASSEMBLY, PACK_VERIFIED and PACK_DEFECT_HOLD are moved by the litigation rules but are not values of LOV-LEGAL-STATUS, and no source says which object holds them | Solution architect, S4 rwb-litigation, with the P3 rwb-case analyst and the Business Rules owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2755 | The pack has no operation of its own in any source, and the legacy endpoint block names the notice approval, which belongs to the notice stories of the service | Solution architect, S4 rwb-litigation, with the API owner of the Service Contract Catalog | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2756 | No source names the trigger of the pack assembly, and the service owns no event although the catalogue lists three on its topic | Solution architect, S4 rwb-litigation, with the Temporal workflow owner and the event platform owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2757 | The index set of legal_action, the business text of the 400 and 409 answers, and the source of the defect-list items are not stated in any source read for this key | Solution architect and DB owner, S4 rwb-litigation, with the message catalogue owner and the RWB-S4-E5005-APP analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2758 | The known defect list has no element of its own in S4, and the two consumed rwb-document reads and the rwb-case answer publish no S4 contract row | S4 rwb-litigation service owner with the P5 rwb-document owner and the P3 rwb-case owner | Resolved (directive) |
| GAP-2759 | The trigger of the check, the item state, the missing-item element and the activity name have no source, and the legacy key carries no requirement id in the plan | S4 rwb-litigation service owner with the solution architect | Resolved (directive) |
| GAP-2760 | Three consumed contracts of the pack-recovery step have no dependency row, and the plan gives the two stories no contract or integration dependency | Solution architect, S4 rwb-litigation, with the P5 rwb-document and P3 rwb-case architects | Resolved (directive) |
| GAP-2761 | The recovery element, the gap reason and the list the reason is drawn from have no field list in any source | Tech lead, S4 rwb-litigation, with the P5 rwb-document analyst and the business analyst of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2762 | The legacy master carries no requirement identifier for RWB-E5-006, so both stories trace to the feature and to the nearest module requirement | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Resolved (directive) |
| GAP-2763 | The catalogue gives the litigation topic three events and none of them is the recovery of a pack item, so the step publishes and consumes nothing | Solution architect, S4 rwb-litigation, with the event platform owner and the P5 and P3 analysts | Resolved (directive) |
| GAP-2764 | The FSD integration point CCMS has no owner in the target and no external dependency row | Solution architect, with the P2 rwb-integration and P5 rwb-document architects and the interface owner of CCMS | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2765 | No source publishes the four consumed surfaces the pack step needs: the pack and defect-list read of rwb-document, the notice and template-status read of rwb-comms, the case read with its task raise and route fact of rwb-case, and the D7 approval item of rwb-decision | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2766 | The legacy data block and endpoint block give this story the case, the task, the timer, the notice and the decision ledger, which the target assigns to rwb-case, rwb-comms and rwb-decision | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2767 | No stored field or list value carries the pack verification, the filing authorisation, the defect-list result, the template status or the prescription days, and no status value names the two acts | Solution architect | Resolved (directive) |
| GAP-2768 | No source fixes how the template-withdrawn fact and the prescription warning reach the service, or who owns the 1-working-day and 2-working-day service levels of R-LIT-04 and R-LIT-16 | Solution architect | Resolved (directive) |
| GAP-2769 | The legacy story and the Epics 3 to 8 specification carry no requirement identifier for this feature | Business analyst | Resolved (directive) |
| GAP-2770 | No source gives the element names or the field lists of the pack verification, the filing authorisation, the case route fact or the task raise, and no source states which document publishes the pack element | Solution architect | Resolved (directive) |
| GAP-2771 | The legacy endpoint block gives the contract the notice approval operation, which the TSD places first in Epic 2 and which the ownership rows still list under rwb-litigation | Solution architect | Resolved (directive) |
| GAP-2835 | The litigation-side checked-field read, the fact columns it fills on legal_action and hearing, the source stamps and the unmapped field codes are not specified | Tech lead of rwb-litigation with the P5 owner of the checked-field contract and the rwb-litigation data owner | Resolved (directive) |
| GAP-2836 | No source says how an extracted hearing_date becomes a hearing row, which hearing_type that row carries, or what the apply does to an action in a closed status | Litigation business analyst with the rwb-litigation data owner and the S4 hearing story owner | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S4-E5005-APP | new AC without TC row | 465 | AC5 is new and no section 16 row covers it |
| RWB-S4-E5006-APP | Not specified without item ID | 435 | \| TC-E5-006-11 \| AC7 provided operation answers 403 or 404 and writes nothing; its 401 answer is Not specified in the source documents \| Component \| Not specifi |
