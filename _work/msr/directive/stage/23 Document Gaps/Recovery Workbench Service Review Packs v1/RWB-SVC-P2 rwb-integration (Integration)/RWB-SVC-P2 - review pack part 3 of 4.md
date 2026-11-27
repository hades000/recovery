# RWB-SVC-P2 rwb-integration (Integration) - review pack, part 3 of 4 (RWB-P2-E2007-APP to RWB-P2-E2034-OPS)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 161 |
| Cross-document (pending in another document) | 247 |
| Not applied (value not in the sources) | 7 |
| Open business decisions | 25 |
| Register gaps linked | 50 |
| Unconfirmed assumptions | 0 |
| Lint findings | 4 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P2-E2007-APP | 39 | 40 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2007 APP Booking confirmation from the ALS load v2.md |
| RWB-P2-E2007-CON | 20 | 39 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2007 CON Booking confirmation from the ALS load - contract v2.md |
| RWB-P2-E2007-OPS | 21 | 42 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2007 OPS Booking confirmation from the ALS load - deployment v2.md |
| RWB-P2-E2033-APP | 17 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2033 APP Case and queue list with status, owner and ageing v2.md |
| RWB-P2-E2033-CON | 12 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2033 CON Case and queue list with status, owner and ageing - contract v2.md |
| RWB-P2-E2034-APP | 26 | 34 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2034 APP Interaction ledger on the case and from every channel v2.md |
| RWB-P2-E2034-CON | 17 | 30 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2034 CON Interaction ledger on the case and from every channel - contract v2.md |
| RWB-P2-E2034-OPS | 9 | 29 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2034 OPS Interaction ledger on the case and from every channel - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P2-E2033-APP | R-00588 | CG-ALL-3180 | Script gap | Product owner | The story adds CAR to the closed list LOV-PRODUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P2-E2033-APP | R-00589 | CG-ALL-3181 | Script gap | Product owner | The story adds CAR to the closed list LOV-CASE-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P2-E2033-APP | R-00590 | CG-ALL-3182 | Script gap | Product owner | The story adds CAR to the closed list LOV-STAGE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P2-E2033-CON | R-00594 | CG-ALL-3192 | Script gap | Product owner | The story adds CAR to the closed list LOV-CASE-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P2-E2033-CON | R-00595 | CG-ALL-3193 | Script gap | Product owner | The story adds CAR to the closed list LOV-PRODUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P2-E2033-CON | R-00596 | CG-ALL-3194 | Script gap | Product owner | The story adds CAR to the closed list LOV-STAGE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P2-E2034-CON | R-00603 | CG-ALL-3227 | Script gap | Product owner | The story adds RESOLVE_OUTBOX_DELIVERY to the closed list LOV-OUTBOX-DELIVERY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P2-E2007-APP | R-10079 | CG-ALL-3130 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2007-OPS | R-10101 | CG-ALL-3174 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2033-APP | R-10103 | CG-ALL-3189 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2033-CON | R-10106 | CG-ALL-3203 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2034-APP | R-10118 | CG-ALL-3221 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2034-APP | R-10119 | CG-ALL-3226 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-P2-E2034-APP | R-33399 | ASM-ALL-3226 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P2-E2007-APP | R-04825 | DOR-RWB-P2-E2007-APP-17 | 12.6 | Definition of Ready item 17 Dependencies: Fail | Delivery status of RWB-P2-E1007-APP and RWB-P2-E2007-OPS is not story text. RWB-P7-E1073-CON is only in the DP-04 row (12.6); RWB-P7-E1073-APP is another work type; re-pointing is a decision. |
| RWB-P2-E2007-CON | R-04830 | DOR-RWB-P2-E2007-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design for RWB-P2-E2007-CON or EP02/RWB-SVC-P2 in the story or the project .md files (grep 'epic design' rechecked, no match). The sign-off needs the epic design record, so it cannot be recorded without an invented value. |
| RWB-P2-E2033-APP | R-04840 | DOR-RWB-P2-E2033-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed E2 epic design record in the sources (stakeholder-map shows only a design sign-off pack, no signed status). Confirm in the epic design record. |
| RWB-P2-E2033-CON | R-04847 | DOR-RWB-P2-E2033-CON-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record for EP02 or RWB-SVC-P2 in the story or in the .md/.csv sources. A sign-off cannot be invented; no edit made. |
| RWB-P2-E2034-CON | R-15693 | DOR-RWB-P2-E2034-CON-1 | 1 | Definition of Ready item 1 Story: Partial | The item and the story give no replacement actor role, so the actor stays 'tech lead'. |
| RWB-P2-E2034-OPS | R-04864 | DOR-RWB-P2-E2034-OPS-16 | Header | Definition of Ready item 16 Size: Fail | No size value is in the sources; the item stays open. |
| RWB-P2-E2034-OPS | R-22570 | GAP-2321 | 3 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Masking label, covered field IDs, access-log granularity, parameter rows and DB login are not in the sources (parameter catalog, P4 stories, Gap Register). Needs owner settlement; no story text provided to edit. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (35)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04781 | RWB-P2-E2007-APP | CG-ALL-3115 | 12.5 | Add Workflows row for BookingMatchWorkflow (workflow ID prefix booking-match-, task queue rwb-integration) as specified in section 12.5. |
| CDC-04793 | RWB-P2-E2007-APP | CG-ALL-3116 | 12.5 | Add an Activities row for readBookedTerms (task queue rwb-integration) with its input and output contract. |
| CDC-04794 | RWB-P2-E2007-APP | CG-ALL-3117 | 12.5 | Add an Activities row for listApprovedTreatments (task queue rwb-integration) with its input and output contract. |
| CDC-04795 | RWB-P2-E2007-APP | CG-ALL-3118 | 12.5 | Add an Activities row for evaluateBookingMatch (task queue rwb-integration) with its input and output contract. |
| CDC-04821 | RWB-P2-E2007-CON | CG-ALL-3141 | 12.5 | Add a Workflows row for BookingMatchWorkflow (workflow ID prefix booking-match-, task queue rwb-integration). |
| CDC-04826 | RWB-P2-E2007-CON | CG-ALL-3142 | 12.5 | Add an Activities row for readBookedTerms (task queue rwb-integration). |
| CDC-04827 | RWB-P2-E2007-CON | CG-ALL-3143 | 12.5 | Add activity listApprovedTreatments to the Activities sheet with the input and output of 12.5, or name a catalogued activity in 12.5. |
| CDC-04828 | RWB-P2-E2007-CON | CG-ALL-3144 | 12.5 | Add activity evaluateBookingMatch to the Activities sheet with the input and output of 12.5, or name a catalogued activity in 12.5. |
| CDC-04829 | RWB-P2-E2007-CON | CG-ALL-3145 | 12.5 | Add activity applyBookingOutcome to the Activities sheet with the input and output of 12.5, or name a catalogued activity in 12.5. |
| CDC-04830 | RWB-P2-E2007-CON | CG-ALL-3146 | 12.5 | Add activity raiseBookingTasks to the Activities sheet with the input and output of 12.5, or name a catalogued activity in 12.5. |
| CDC-04831 | RWB-P2-E2007-CON | CG-ALL-3147 | 12.5 | Add activity writeRunSummary to the Activities sheet with the input and output of 12.5, or name a catalogued activity in 12.5. |
| CDC-04859 | RWB-P2-E2007-OPS | CG-ALL-3162 | 12.5 | Name the JOB-08 placeholder row BookingMatchWorkflow, workflow ID prefix booking-match-, service and task queue rwb-integration (the row now shows rwb-payment). |
| CDC-04868 | RWB-P2-E2007-OPS | CG-ALL-3163 | 12.5 | Add activity readBookedTerms with task queue rwb-integration to the Activities sheet. |
| CDC-04869 | RWB-P2-E2007-OPS | CG-ALL-3164 | 12.5 | Add activity listApprovedTreatments with task queue rwb-integration to the Activities sheet. |
| CDC-04870 | RWB-P2-E2007-OPS | CG-ALL-3165 | 12.5 | Add activity evaluateBookingMatch with task queue rwb-integration to the Activities sheet. |
| CDC-04871 | RWB-P2-E2007-OPS | CG-ALL-3166 | 12.5 | Add activity applyBookingOutcome with task queue rwb-integration to the Activities sheet. |
| CDC-04872 | RWB-P2-E2007-OPS | CG-ALL-3167 | 12.5 | Add activity raiseBookingTasks with task queue rwb-integration to the Activities sheet. |
| CDC-04873 | RWB-P2-E2007-OPS | CG-ALL-3168 | 12.5 | Add activity writeRunSummary with task queue rwb-integration to the Activities sheet. |
| CDC-04939 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-8 | 12.2 | Catalog mapChannelEvent and resolveChannelFacts, and the remaining detcheck items not listed here, then clear the rwb-access path gap. |
| CDC-04942 | RWB-P2-E2034-APP | CG-ALL-3209 | 12.5 | Add an Activities row for mapChannelEvent on task queue rwb-integration. |
| CDC-04943 | RWB-P2-E2034-APP | CG-ALL-3210 | 12.5 | Add an Activities row for resolveChannelFacts on task queue rwb-integration. |
| CDC-04944 | RWB-P2-E2034-APP | CG-ALL-3211 | 12.5 | Add an Activities row for appendLedgerEntry on task queue rwb-integration. |
| CDC-04945 | RWB-P2-E2034-APP | CG-ALL-3212 | 12.5 | Add an Activities row for parkDeliveryInException on task queue rwb-integration. |
| CDC-04946 | RWB-P2-E2034-APP | CG-ALL-3214 | 12.5 | Add an Activities row for readEfsOutcomes on task queue rwb-integration. |
| CDC-04947 | RWB-P2-E2034-APP | CG-ALL-3215 | 12.5 | Add an Activities row for appendEfsEntries on task queue rwb-integration. |
| CDC-04948 | RWB-P2-E2034-APP | CG-ALL-3216 | 12.5 | Add an Activities row for writeEfsReadSummary on task queue rwb-integration. |
| CDC-04968 | RWB-P2-E2034-CON | CG-ALL-3230 | 12.5 | Add a Workflows row for LedgerChannelIntakeWorkflow (task queue rwb-integration, one execution per consumed event, workflow ID = CloudEvents id), as in RWB-P2-E2034-CON 12.5. |
| CDC-04969 | RWB-P2-E2034-CON | CG-ALL-3235 | 12.5 | Add a Workflows row for EfsLedgerReadWorkflow (task queue rwb-integration, started by AceDataReady for the EFS source), as in RWB-P2-E2034-CON 12.5. |
| CDC-04973 | RWB-P2-E2034-CON | CG-ALL-3231 | 12.5 | Add an Activities row for mapChannelEvent. |
| CDC-04974 | RWB-P2-E2034-CON | CG-ALL-3232 | 12.5 | Add an Activities row for resolveChannelFacts. |
| CDC-04975 | RWB-P2-E2034-CON | CG-ALL-3233 | 12.5 | Add an Activities row for appendLedgerEntry. |
| CDC-04976 | RWB-P2-E2034-CON | CG-ALL-3234 | 12.5 | Add an Activities row for parkDeliveryInException. |
| CDC-04977 | RWB-P2-E2034-CON | CG-ALL-3236 | 12.5 | Add an Activities row for readEfsOutcomes. |
| CDC-04978 | RWB-P2-E2034-CON | CG-ALL-3237 | 12.5 | Add an Activities row for appendEfsEntries. |
| CDC-04979 | RWB-P2-E2034-CON | CG-ALL-3238 | 12.5 | Add an Activities row for writeEfsReadSummary. |

### RWB-P2-E2007-CON (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04783 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-21 | header | Complete the build and publish the contract; set build status to Done. |
| CDC-04784 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-22 | header | Publish a contract fake library version and record it as published. |
| CDC-04807 | RWB-P2-E2007-APP | GAP-1713 | 8 | Record the owning-service contract for each prerequisite: FEAT-APD-01, FEAT-CHO-02, FEAT-CHO-06, FEAT-CHO-07, FEAT-CHO-08, FEAT-DCM-12, FEAT-OCC-01, FEAT-OCC-07, FEAT-OCC-09, FEAT-OCC-11, FEAT-TRT-04, FEAT-VAL-06; carry the duplicate FEAT-CHO-08 as written. |
| CDC-04808 | RWB-P2-E2007-APP | GAP-0657 |  | Settle the six unsettled consumed paths and shapes with their owners and record TSD P2 Integration v3 T5.2 as superseded; allocate the rwb-integration login in RWB-PLT-DB. |
| CDC-04811 | RWB-P2-E2007-APP | GAP-0658 | 3, 12.1 | Baseline the result shape, task table, envelope, rerun operation, twelve consumed operations and seven fakes, with contract-owner confirmation. Record the JOB-08 ownership correction and the TSD P2 Integration v3 T5.2 supersession in the gap register. |
| CDC-04813 | RWB-P2-E2007-APP | GAP-0730 | 12 | Publish the gateway-bff composite route fields and hops, the treatment booking fields, and the raiseTask result schema; fix the rwb-case login in the platform DB story. |
| CDC-04814 | RWB-P2-E2007-APP | GAP-2486 | 12 | The operation set, payloads and filters are owned by the contract story and the named service owners. |
| CDC-04815 | RWB-P2-E2007-APP | GAP-2487 | 4 | Add rwb.decision.BookingDecisionMade.v1 on rwb.decision.events.v1, keyed by treatmentId, with outcome, row, package code and version, business date and difference terms; leave TreatmentBooked, CaseStateChanged and posting with their owners. |
| CDC-04833 | RWB-P2-E2007-CON | DOR-RWB-P2-E2007-CON-10 | none | Add empty, loading, error and no access states for SCR-01 and SCR-14 in the P3 screen specification. |
| CDC-04861 | RWB-P2-E2007-OPS | DOR-RWB-P2-E2007-OPS-21 | header | Dependency on RWB-P2-E2007-CON is recorded in the header; the contract is not yet Done and must be published in the contract story. |
| CDC-04862 | RWB-P2-E2007-OPS | DOR-RWB-P2-E2007-OPS-22 | header | Publish a contract fake library version and record it as published. |
| CDC-04880 | RWB-P2-E2007-OPS | GAP-0596 | 3 | Answer each of the three Section B fields as fieldState AVAILABLE or NOT_AVAILABLE with no value on NOT_AVAILABLE; name flag rwb.dataengine.booking-facts, kept off until the Section B migration is applied; record the reading in the next TSD P1 version and the Section B notes. |
| CDC-04881 | RWB-P2-E2007-OPS | GAP-0597 | 12 | Publish GET /batch-status with key pair sourceSystem and businessDate and values status, isComplete, startedAt, completedAt, recordCount and feedVersion; answer 404 with MSG-P1-001 when no batch row exists; state it is the gate read distinct from the RWB-P1-E1015-APP freshness reads; add to the next API Specification version. |
| CDC-04882 | RWB-P2-E2007-OPS | GAP-0594 | 11, 12 | Publish GET /booking-facts and GET /batch-status on /api/recovery/source-data/v1 with BookingFact, BookingFactsAnswer, FieldState and BatchStatusAnswer; keep freshness as DataProductFreshness of RWB-P1-E1015-CON; add both to the next API Specification version. |
| CDC-04883 | RWB-P2-E2007-OPS | GAP-0595 | 4 | Read the account set and product group from this service's case_list_row for the case and business date; if not accepted, add C RWB-P3-E1018-CON and declare GET /api/recovery/case/v1/cases/{caseId}/accounts. Do not read rwb_case.case_account. |
| CDC-04888 | RWB-P2-E2007-OPS | GAP-0598 | 12 | Fix the answer as account facts only, with no treatment term, outcome, difference, tolerance or package version; state that BookingMatchFacts is built by the calling slice; add a contract test that fails on any outcome-shaped field. |
| CDC-04889 | RWB-P2-E2007-OPS | GAP-0658 | 4 | Baseline the contract with result shape, task table, envelope statement, rerun operation, twelve consumed operations and seven fakes; contract owners confirm element names; record JOB-08 ownership and the TSD P2 v3 T5.2 supersession in the gap register; confirm the seven message texts. |
| CDC-04891 | RWB-P2-E2007-OPS | GAP-2486 |  | Publish the operation set from the six legacy interfaces on the DP-13 per-service base with one hop and 2 s timeout; take decision code and outcomes from LOV-DECISION; fix read filters, page size, ordering and MSG-GEN-006 text. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04799 | RWB-P2-E2007-APP | CG-ALL-3126 | 4, 14 | Add a new message ID for a consumed contract that did not answer, with the text '{source} could not be read. Try again in a few minutes.'; the story then cites that ID. |
| CDC-04804 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-9 | 14 | Align the text of MSG-P2-011, MSG-P1-001, MSG-P3-027 and MSG-P2-006, plus the one further detcheck message, with the standard. |
| CDC-04832 | RWB-P2-E2007-CON | CG-ALL-3152 | 14 | Text follows the standard under R-15660. The story's other meaning still needs a new message ID from the business analyst. |
| CDC-04907 | RWB-P2-E2033-APP | CG-ALL-3187 | 4, 14 | Add a new message ID for 'A consumed contract does not answer inside the budget' (X10, section 14) and keep MSG-GEN-006 for R-UNI-33; the story then cites that ID. |
| CDC-04909 | RWB-P2-E2033-APP | DOR-RWB-P2-E2033-APP-9 | 14 | Align the text of MSG-GEN-007 with the standard v4 text, and resolve MSG-GEN-006 meaning per CG-ALL-3187. |
| CDC-04921 | RWB-P2-E2033-CON | CG-ALL-3200 | 4, 14 | Add a new message ID for 'A consumed contract does not answer inside the budget', then cite it in sections 12.1 and 14 in place of MSG-GEN-006. |
| CDC-04924 | RWB-P2-E2033-CON | DOR-RWB-P2-E2033-CON-9 | 14 | Align the text of MSG-GEN-007 with the standard and confirm the standard's meaning of MSG-GEN-006 for the platform unavailable answer. |
| CDC-04949 | RWB-P2-E2034-APP | CG-ALL-3217 | 4, 14 | Add a new message ID for the delivery-in-exception-queue message, so the story can cite it in place of MSG-P2-001. |
| CDC-04950 | RWB-P2-E2034-APP | CG-ALL-3218 | 4, 14 | Add a new message ID for 'A resend is accepted', distinct from MSG-GEN-005 (which holds 'Saved'); the story then cites that ID in section 14. |
| CDC-04954 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-9 | 14 | Name MSG-P2-001 and MSG-GEN-005 with the standard's meaning and text, or align the two rows of section 14 to it. |
| CDC-04980 | RWB-P2-E2034-CON | CG-ALL-3239 | 4, 14 | Add a new message ID for 'A delivery is in the exception queue after its retries' so section 14 can cite it. |
| CDC-04981 | RWB-P2-E2034-CON | CG-ALL-3240 | 4, 14 | Add a new message ID for 'A resend is accepted' so section 14 can cite it. |
| CDC-04983 | RWB-P2-E2034-CON | DOR-RWB-P2-E2034-CON-9 | 14 | Confirm or rename MSG-P2-001 and MSG-GEN-005, whose meanings in this contract differ from the standard's. |
| CDC-05003 | RWB-P2-E2034-OPS | CG-ALL-3246 | 4, 14 | Add a new message ID for the exception-queue or P1 append failure case, with its text, for the story to cite. |
| CDC-05004 | RWB-P2-E2034-OPS | CG-ALL-3247 | 14 | Add a message ID for the text 'A resend is accepted in the smoke run'; the story cites it in place of MSG-GEN-005, which the standard keeps for 'Saved.' |
| CDC-05010 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-9 | 14 | Confirm the meaning of MSG-P2-001 for the exception queue or re-issue it; MSG-GEN-005 is handled under CG-ALL-3247. |

### RWB-P2-E2034-CON (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04937 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-21 | Header | Move the contract story build status from Not started to Done with the contract published. |
| CDC-04938 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-22 | Header | Publish a contract fake library version and record its version number. |
| CDC-04960 | RWB-P2-E2034-APP | GAP-0664 | find it | Record at contract review before app start: ACE DB login, append and fact element names, admin bodies and RESOLVE_OUTBOX_DELIVERY task, mapping, retries of 1 minute, 10 minutes and 1 hour with three attempts. |
| CDC-04961 | RWB-P2-E2034-APP | GAP-0665 | find it | Approve wire shapes of the append, two P1 reads, five fact answers and two admin operations; dedupe key, state moves, append-before-inbox order and repeated-key success. |
| CDC-04962 | RWB-P2-E2034-APP | GAP-2225 | find it | Confirm element names, paths and field shapes of the interaction item, append command and intake result at contract review. |
| CDC-04963 | RWB-P2-E2034-APP | GAP-3149 | find it | Declare the partner fact, seven ledger attributes and read-only view with placeholders; agree EV-20 and EV-21 payloads and the seam at contract review. |
| CDC-05000 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-21 | find it | Set the build status to Done once the contract is published. |
| CDC-05015 | RWB-P2-E2034-OPS | GAP-2186 | 12 | Publish the contact-fact read with its path, contact-key parameter and masked members, and realign the two consumed rows to RWB-P1-E2001-APP's EFS history read. |
| CDC-05017 | RWB-P2-E2034-OPS | GAP-0664 | 12 | Approve the five assumptions at contract review: login, append and fact element names, admin bodies, mapping detail, retry intervals of 1 minute, 10 minutes and 1 hour with three attempts, and the ledger split. |
| CDC-05018 | RWB-P2-E2034-OPS | GAP-0665 | 12 | Approve the append, EFS and contact wire shapes, admin operations, dedupe keys, state moves and append-before-inbox order at contract review. |
| CDC-05021 | RWB-P2-E2034-OPS | GAP-2225 | 12 | Confirm element names, paths and field shapes of the interaction item, append command and intake result at contract review. |
| CDC-05022 | RWB-P2-E2034-OPS | GAP-3149 | 8 | BR9 states that the ledger, its retention class and its ordered read belong to rwb-source-data. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04817 | RWB-P2-E2007-APP | CG-ALL-3129 | 18 | Section 18 of the story now lists TC-E2-007-01 to -17. The RTM is a separate workbook and must align in its next version. |
| CDC-04853 | RWB-P2-E2007-CON | CG-ALL-3154 | 18 | Align the REQ-CHO-008 test list with section 18 of RWB-P2-E2007-CON (TC-P2-E2007-CON-01 to -03), or record the legacy TC IDs in the story. |
| CDC-04895 | RWB-P2-E2007-OPS | CG-ALL-3173 | 18 | Trace REQ-CHO-008 to TC-P2-E2007-OPS-01 and TC-P2-E2007-OPS-03 in place of the TC-E2-006 and TC-E2-007 rows. |
| CDC-04908 | RWB-P2-E2033-APP | DOR-RWB-P2-E2033-APP-12 | 12, 12.7, 16, 18 | Align the test case list of RWB-P2-E2033-APP with section 18 of the story, now TC-E2-033-01 to TC-E2-033-18. |
| CDC-04915 | RWB-P2-E2033-APP | CG-ALL-3188 | 18 | Align the test lists for REQ-WKM-002, REQ-DVH-006 and REQ-ACA-006 between the RTM and section 18 in their next versions. |
| CDC-04932 | RWB-P2-E2033-CON | CG-ALL-3202 | 18 | Align the test lists of REQ-WKM-002, REQ-DVH-006 and REQ-ACA-006 with section 18 of this story. |
| CDC-04951 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-12 | 12, 12.7, 16, 18 | Align the test case list per requirement REQ-ILG-006 to REQ-ILG-014 with story section 18. |
| CDC-04964 | RWB-P2-E2034-APP | CG-ALL-3220 | 18 | Align the test lists for the nine requirements that differ between section 18 and RTM v7. |
| CDC-04995 | RWB-P2-E2034-CON | CG-ALL-3242 | 18 | Align the test lists of the nine requirements with RWB-P2-E2034-CON section 18 in the next RTM version; section 18 is not changed here. |
| CDC-05024 | RWB-P2-E2034-OPS | CG-ALL-3249 | 18 | Align the test lists for the 9 requirements with RWB-P2-E2034-OPS section 18, for example REQ-ILG-009 and REQ-ILG-010. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04790 | RWB-P2-E2007-APP | CG-ALL-3110 | 13 | Record decision_record as a PLT library table created in rwb_integration (DP-03) in the owning document, as already stated in the story. |
| CDC-04803 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-7 | 11 | Add principal_outstanding, settlement_booked_date and settlement_booked_amount (DF-ACC-009, DF-ACC-030, DF-ACC-031) and the decision_record entity, or record them in Data Classification v5; two further detcheck names are pending. |
| CDC-04940 | RWB-P2-E2034-APP | CG-ALL-3205 | 1 | Record trigger tr_interaction_append_only as an append-only database object of the ledger table, with its dictionary name. |
| CDC-04941 | RWB-P2-E2034-APP | CG-ALL-3206 | 13 | Record decision_record as the PLT library table in schema rwb_integration, as sections 12.8 and 13 already state. |
| CDC-04953 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-7 | 11 | Add DF-INT-036 and name decision_record and tr_interaction_append_only as LDM fields or entities, or confirm them as library objects. |
| CDC-04992 | RWB-P2-E2034-CON | GAP-2184 | 3 | Publish retention class list and periods with a version; add PARTNER_RESULT and OFFER to LOV-LEDGER-EVENT in the same version; confirm uuid type of the two link columns. |
| CDC-05009 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-7 | 11 | Assign BR Field IDs to the ten section 11 items, or confirm that none applies to them. |
| CDC-05020 | RWB-P2-E2034-OPS | GAP-2184 | 3 | Publish the retention class list and periods, add PARTNER_RESULT and OFFER to LOV-LEDGER-EVENT, confirm uuid link column types, and name the four feature IDs in Business Requirements Epic 2. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04780 | RWB-P2-E2007-APP | CG-ALL-3111 | 12.1 | Add path /api/recovery/integration/v1/admin/jobs/{jobId}/rerun with the POST operation, published through RWB-P2-E2007-CON. |
| CDC-04820 | RWB-P2-E2007-CON | CG-ALL-3138 | 12.1 | Add POST /api/recovery/integration/v1/admin/jobs/{jobId}/rerun with the operation described in section 12.1. |
| CDC-04901 | RWB-P2-E2033-APP | CG-ALL-3183 | 12.1 | Publish GET /api/recovery/integration/v1/case-list (owner rwb-integration, RWB-P2-E2033-APP section 12.1) through RWB-P2-E2033-CON. |
| CDC-04902 | RWB-P2-E2033-APP | CG-ALL-3184 | 12.1 | Publish GET /api/recovery/integration/v1/case-list/export (owner rwb-integration, RWB-P2-E2033-APP section 12.1) through RWB-P2-E2033-CON. |
| CDC-04916 | RWB-P2-E2033-CON | CG-ALL-3195 | 12.1 | Add path GET /api/recovery/integration/v1/case-list as the operation in section 12.1, with its access, paging and filter parameters. |
| CDC-04917 | RWB-P2-E2033-CON | CG-ALL-3196 | 12.1 | Add path GET /api/recovery/integration/v1/case-list/export as the operation in section 12.1, with its export parameters. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04791 | RWB-P2-E2007-APP | CG-ALL-3113 | 12.4 | Add rwb-integration as a consumer of rwb.source-data.AceDataReady.v1 (EV-26) in the Events row, with its ACL. |
| CDC-04792 | RWB-P2-E2007-APP | CG-ALL-3114 | 12.4 | Add rwb-integration as a consumer of rwb.treatment.TreatmentApproved.v1 (EV-10) in the Events row, with its ACL. |
| CDC-04824 | RWB-P2-E2007-CON | CG-ALL-3139 | 12.4 | Add rwb-integration as a consumer of rwb.source-data.AceDataReady.v1. |
| CDC-04825 | RWB-P2-E2007-CON | CG-ALL-3140 | 12.4 | Add rwb-integration as a consumer of rwb.treatment.TreatmentApproved.v1. |
| CDC-04866 | RWB-P2-E2007-OPS | CG-ALL-3160 | 12.4 | Add rwb-integration as consumer of rwb.source-data.AceDataReady.v1 (Events row EV-26) and add its ACL. |
| CDC-04867 | RWB-P2-E2007-OPS | CG-ALL-3161 | 12.4 | Add rwb-integration as a consumer of rwb.treatment.TreatmentApproved.v1 in the catalog, with its ACL. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04800 | RWB-P2-E2007-APP | CG-ALL-3127 | 16 | Add TC-E2-007-11 rows with Given, When and Then copied from the criterion it covers (Principle 5, NFR). |
| CDC-04852 | RWB-P2-E2007-CON | CG-ALL-3153 | 16 | Add rows TC-P2-E2007-CON-01 to TC-P2-E2007-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-04894 | RWB-P2-E2007-OPS | CG-ALL-3172 | 16 | Add rows TC-P2-E2007-OPS-01 to TC-P2-E2007-OPS-06 with Given, When and Then copied from the criterion each covers. |
| CDC-04931 | RWB-P2-E2033-CON | CG-ALL-3201 | 16 | Add rows TC-P2-E2033-CON-01 to TC-P2-E2033-CON-06 with Given, When and Then copied from AC1 to AC6. |
| CDC-04994 | RWB-P2-E2034-CON | CG-ALL-3241 | 16 | Add rows TC-P2-E2034-CON-01 to TC-P2-E2034-CON-06 with Given, When and Then copied from the criterion each covers. |
| CDC-05023 | RWB-P2-E2034-OPS | CG-ALL-3248 | 16 | Add rows TC-P2-E2034-OPS-01 to TC-P2-E2034-OPS-06 to Story test cases, with Given, When and Then copied from AC1 to AC6. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04782 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-P2 / EP02 in the epic design record. |
| CDC-04860 | RWB-P2-E2007-OPS | DOR-RWB-P2-E2007-OPS-14 | header | Record the signed epic design sign-off for RWB-SVC-P2 (EP02) so the readiness check can cite it. |
| CDC-04936 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-14 | Header | Confirm and record the signed epic design sign-off for RWB-P2-E2034-APP. |
| CDC-04970 | RWB-P2-E2034-CON | DOR-RWB-P2-E2034-CON-14 |  | Confirm and record the signed epic design sign-off for this story's epic. |
| CDC-04999 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-14 | find it | Confirm that the signed epic design sign-off for EP02 is recorded in the epic design record. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04934 | RWB-P2-E2034-APP | CG-ALL-3208 | 12.5 | Add a row for LedgerChannelIntakeWorkflow (service rwb-integration, task queue rwb-integration, one execution per consumed event, workflow ID = CloudEvents id), as in RWB-P2-E2034-APP §12.5. |
| CDC-04935 | RWB-P2-E2034-APP | CG-ALL-3213 | 12.5 | Add a row for EfsLedgerReadWorkflow (service rwb-integration, task queue rwb-integration, started by AceDataReady for the EFS source, returns EfsReadSummary), as in RWB-P2-E2034-APP §12.5. |
| CDC-04997 | RWB-P2-E2034-OPS | CG-ALL-3244 | 12.5 | Add a row for LedgerChannelIntakeWorkflow: service and task queue rwb-integration, one execution per consumed event, workflow ID = CloudEvents id, as in RWB-P2-E2034-OPS section 12.5. |
| CDC-04998 | RWB-P2-E2034-OPS | CG-ALL-3245 | 12.5 | Add a row for EfsLedgerReadWorkflow: service and task queue rwb-integration, started by AceDataReady for the EFS source, no Schedule, as in RWB-P2-E2034-OPS section 12.5. |
| CDC-05002 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-8 | 12.5 | Add rows for LedgerChannelIntakeWorkflow and EfsLedgerReadWorkflow (rwb-integration), as set out for CG-ALL-3244 and CG-ALL-3245. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04835 | RWB-P2-E2007-CON | GAP-3175 | find it | List LoadCompleted (EV-26) as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1. |
| CDC-04875 | RWB-P2-E2007-OPS | GAP-3175 | find it | List LoadCompleted as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1. |
| CDC-04956 | RWB-P2-E2034-APP | GAP-3175 | find it | List LoadCompleted (EV-26) as the legacy alias of AceDataReady (EV-26) with rwb-source-data as producer. |
| CDC-05012 | RWB-P2-E2034-OPS | GAP-3175 | 12.4 | List LoadCompleted (EV-26) as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04903 | RWB-P2-E2033-APP | CG-ALL-3185 | 12.2 | Publish POST /api/recovery/access/v1/authorise as given by Architecture v5 slide 14, through the rwb-access provider's CON story. |
| CDC-04918 | RWB-P2-E2033-CON | CG-ALL-3197 | 12.2 | Add path POST /api/recovery/access/v1/authorise, as Architecture v5 slide 14 assigns it to rwb-access. |
| CDC-04933 | RWB-P2-E2034-APP | CG-ALL-3207 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider CON story, or the story consumes a published operation. |
| CDC-04967 | RWB-P2-E2034-CON | CG-ALL-3228 | 12.2 | Publish POST /api/recovery/access/v1/authorise (role and scope check of the two provided operations) through the provider's CON story. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04786 | RWB-P2-E2007-APP | GAP-1696 | 11 | Add S2 (rwb-treatment) to the P1 (rwb-source-data) REST cell in the connection matrix (slide 13). This story already reads source facts only through the rwb-source-data contract (DF-ACC-009, DF-ACC-030, DF-ACC-031). |
| CDC-04864 | RWB-P2-E2007-OPS | GAP-1696 | find it | Add S2 to the P1 REST cell of the connection matrix (slide 13); FSD S2 sources all ACE, ALS, COLLINS, NLEADS and CCMS facts via the rwb-source-data contract. |
| CDC-04878 | RWB-P2-E2007-OPS | GAP-1703 | find it | Record the booking reference from TreatmentBooked and the break from PaymentMissed; rwb-payment owns booking, matching and posting; the release request goes through the integration contract. |

### RWB-P1-E2007-APP; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04787 | RWB-P2-E2007-APP | CG-ALL-3107 | 11 | Record principal_outstanding as a field of v_ace_account in the owning document (RWB-ACE-001 Section B) and in LDM v9 Fields, or the dictionary name to use. |
| CDC-04788 | RWB-P2-E2007-APP | CG-ALL-3108 | 11 | Record settlement_booked_date as a field of v_ace_account in the owning document (RWB-ACE-001 Section B) and in LDM v9 Fields, or the dictionary name to use. |
| CDC-04789 | RWB-P2-E2007-APP | CG-ALL-3109 | 11 | Record settlement_booked_amount as a field of v_ace_account in the owning document (RWB-ACE-001 Section B) and in LDM v9 Fields, or the dictionary name to use. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04796 | RWB-P2-E2007-APP | CG-ALL-3119 | 12.5 | Add a row for activity applyBookingOutcome to the Activities sheet, or name a catalogued activity in 12.5. |
| CDC-04797 | RWB-P2-E2007-APP | CG-ALL-3120 | 12.5 | Add a row for activity raiseBookingTasks to the Activities sheet, or name a catalogued activity in 12.5. |
| CDC-04798 | RWB-P2-E2007-APP | CG-ALL-3121 | 12.5 | Add a row for activity writeRunSummary to the Activities sheet, or name a catalogued activity in 12.5. |

### RWB-P4-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04810 | RWB-P2-E2007-APP | GAP-0922 | 13 | Add POST /authorise with request and answer schemas to T-A and the TSD P4 object list. Publish and stub it in RWB-P4-E1037-CON. Fix the rwb-access login in the platform DB story. Publish the composite route through gateway-bff (DP-19). |
| CDC-04844 | RWB-P2-E2007-CON | GAP-0922 | 4 | Add POST /authorise with its request and answer schema, stub it in the contract fake, fix the rwb-access login in the platform DB story, and publish the composite route with gateway-bff (DP-19). |
| CDC-04885 | RWB-P2-E2007-OPS | GAP-0922 | 11 | Add the POST /authorise path with request and answer schema to the API specification and TSD P4 appendix T-A; publish with RWB-P4-E1037-CON and stub it in the contract fake; fix the rwb-access login in the platform DB story; publish the composite route with gateway-bff (DP-19). |

### RWB-S2-E3001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04816 | RWB-P2-E2007-APP | GAP-2691 | 12 | Add the approved-not-booked read, mark-booked write and booking-difference write with element names; add APPROVED and BOOKED to the state check; make booking_difference a jsonb object keyed by term; add a unique key per treatment and business date. |
| CDC-04851 | RWB-P2-E2007-CON | GAP-2691 | 4 | Add the approved-not-booked read, mark-booked write and booking-difference write with element names at the wave 2 freeze; add APPROVED and BOOKED to the state check; make booking_difference a jsonb object keyed by term; add a unique key per treatment and business date. |
| CDC-04893 | RWB-P2-E2007-OPS | GAP-2691 |  | Add the approved-not-booked read, mark-booked write and booking-difference write with element names at the wave 2 freeze; add APPROVED and BOOKED to the state check; define booking_difference as jsonb keyed by term; unique key per treatment and business date. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04834 | RWB-P2-E2007-CON | DOR-RWB-P2-E2007-CON-12 | 16 | Add TC-P2-E2007-CON-01 to -07 to Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-04923 | RWB-P2-E2033-CON | DOR-RWB-P2-E2033-CON-12 | 16 | Add TC-P2-E2033-CON-01 to -10 to Test Cases v8 and align the section 18 test lists with RTM v7. |
| CDC-05007 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-12 | 16 | Add rows TC-P2-E2034-OPS-01 to TC-P2-E2034-OPS-10 to Test Cases v8; align the section 18 test lists with RTM v7. |

### RWB-P2-E2033-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04904 | RWB-P2-E2033-APP | DOR-RWB-P2-E2033-APP-21 | find it | Reach Done build status (currently Not started). |
| CDC-04905 | RWB-P2-E2033-APP | DOR-RWB-P2-E2033-APP-22 | find it | Publish a fake library version of the RWB-P2-E2033-CON contract. |
| CDC-04913 | RWB-P2-E2033-APP | GAP-2320 | find it | Section 2 records rwb-access as a build-against dependency that is also called at run time; element list and extract fields are outside this story. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04922 | RWB-P2-E2033-CON | DOR-RWB-P2-E2033-CON-1 | 1 | Confirm a role code or name for the build-team role this story names, or add it to the role list, then replace the placeholder in section 1. |
| CDC-04952 | RWB-P2-E2034-APP | DOR-RWB-P2-E2034-APP-6 | 10 | Add role SY-INTGR as the rwb-integration service identity. |
| CDC-05005 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-1 | 1 | Add a role code or role name for 'platform engineer', the role used in section 1. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04802 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-12 | 18 | Add story test cases TC-E2-007-11 to TC-E2-007-17; reconcile TC-E2-007-10 (v8 data differs from story §16); align REQ-CHO-008 tests for RWB-E2-007 with story §18. |
| CDC-04982 | RWB-P2-E2034-CON | DOR-RWB-P2-E2034-CON-12 | 12.7, 16, 18 | Add TC-P2-E2034-CON-01 to -17 to Test Cases v8; align the RTM v7 test lists for REQ-ILG-006 to -014 and ADR-020 with section 18. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04805 | RWB-P2-E2007-APP | GAP-3175 |  | List LoadCompleted (EV-26) as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1; mirror the alias in Kafka Topic and Event Catalog v1. |
| CDC-04985 | RWB-P2-E2034-CON | GAP-3175 | 8 | Carry AceDataReady (EV-26) with LoadCompleted as legacy alias; the same alias goes in Kafka Topic and Event Catalog v1. |

### RWB-P2-E2007-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04812 | RWB-P2-E2007-APP | GAP-0659 | 4 | Fix the rwb-integration login, secret reference and probe checks; write the JOB-08 catalogue row with its run book path; review the four runbook entries with the on-call rota; take thresholds, series windows and backfill limit as environment values. |
| CDC-04848 | RWB-P2-E2007-CON | GAP-0659 | 11 | Fix the rwb-integration login, secret reference and probe checks; take thresholds, series windows and backfill limit as environment values; write the JOB-08 catalogue row with its runbook path. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04843 | RWB-P2-E2007-CON | GAP-0923 | 4 | Add Case record and Treatment and offer columns to T6.1, publish the 14-area matrix as data, and confirm the RW-RESTRUCT and RW-CREDITAD letters with the matrix owner. |
| CDC-04884 | RWB-P2-E2007-OPS | GAP-0923 | 11 | Extend T6.1 with Case record and Treatment and offer columns; publish the full 14-area matrix as data with RWB-P4-AD002-APP; confirm CASE_RECORD R and U and TREATMENT_AND_OFFER R for RW-RESTRUCT and RW-CREDITAD with the matrix owner. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04845 | RWB-P2-E2007-CON | GAP-2485 | 13 | Record that this slice evaluates BOOKING_MATCH on the version it holds through the embedded kit, and restate the RWB-P7-E2042-APP boundary once. |
| CDC-04886 | RWB-P2-E2007-OPS | GAP-2485 | 13 | Keep the Work Package placement: this slice evaluates BOOKING_MATCH on the version it holds through the embedded kit and publishes the outcome; record the placement in the Change Register and restate the RWB-P7-E2042-APP boundary once. |

### OTHER:Platform secret store (ACE team) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04855 | RWB-P2-E2007-CON | GAP-2489 | none | Allocate the rwb-decision login with schema rwb_decision and record it in the platform secret store. |
| CDC-04897 | RWB-P2-E2007-OPS | GAP-2489 | find it | Allocate the rwb-decision login with schema rwb_decision and record it in the platform secret store. |

### OTHER:Work Package B2-P7-021 story line (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04898 | RWB-P2-E2007-OPS | GAP-2490 | find it | Record tcs_legacy in the order TC-E2-007-10, TC-E2-007-01 to TC-E2-007-09, TC-E2-007-11, with Covers naming this slice's criteria; map System to Component, Access to Contract, Resilience to NFR. |
| CDC-04900 | RWB-P2-E2007-OPS | GAP-2488 | Header; 3; 12.2; 12.8; 13 | Metadata rows kept as the Work Package fixes them; build dependencies and consumed contracts not added as rows here. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04906 | RWB-P2-E2033-APP | DOR-RWB-P2-E2033-APP-8 | find it | Publish GET case-list, GET case-list/export and POST authorise as in CG-ALL-3183, CG-ALL-3184 and CG-ALL-3185. |
| CDC-04920 | RWB-P2-E2033-CON | DOR-RWB-P2-E2033-CON-8 | n/a | Publish the operations under CG-ALL-3195, CG-ALL-3196 and CG-ALL-3197; the 404 finding is handled under CG-ALL-3198. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04910 | RWB-P2-E2033-APP | GAP-0661 | find it | Add rows for GET /api/recovery/integration/v1/case-list and /case-list/export; fix the eight consumed paths in the P3 and P4 contract stories; slide 13 to show the composed read. |
| CDC-04925 | RWB-P2-E2033-CON | GAP-0661 | 11 | Add rows for GET /api/recovery/integration/v1/case-list and its export to the Ownership Map; draw the P2 Integration REST connections to the P3 and P4 contracts on slide 13. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04928 | RWB-P2-E2033-CON | GAP-3101 | 8 | Add a GET read of the deviation state of a page of cases on rwb-deviation (S8), beside its two write operations, on GET /api/recovery/deviation/v1/deviation-flags. |
| CDC-05008 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-24 | 12.4 | Name the owning service of topics rwb.treatment.events.v1, rwb.comms.events.v1, rwb.partner.events.v1 and rwb.payment.events.v1 for the section 12.4 owner column. |

### OTHER:Functional Specification P7 (FSD P7) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04955 | RWB-P2-E2034-APP | GAP-1612 | find it | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; rwb-source-data owns the one ledger. |
| CDC-05011 | RWB-P2-E2034-OPS | GAP-1612 | 18 | After the wave 1 contract review confirms rwb-source-data owns the one ledger, re-issue FSD P7 without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35. |

### OTHER:Batch and Scheduling next version (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04957 | RWB-P2-E2034-APP | GAP-3176 | find it | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |
| CDC-04986 | RWB-P2-E2034-CON | GAP-3176 | 8 | Confirm no Epic 2 step depends on JOB-01; list AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### RWB-P1-E1066-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04966 | RWB-P2-E2034-APP | GAP-2185 | 12.1 | Settle one ledger path family and realign the append row of RWB-P1-E1066-APP and its fake to POST /cases/{caseId}/interactions. This story already publishes that form in section 12.1. |
| CDC-05025 | RWB-P2-E2034-OPS | GAP-2185 | 8 | Settle one ledger path family and realign the append row of RWB-P1-E1066-APP and its fake to POST /cases/{caseId}/interactions. |

### RWB-P2-E2001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04987 | RWB-P2-E2034-CON | GAP-0590 | 8 | BR5 states the counting party is Not specified in the source documents (GAP-0590); the EFS key format is kept as recorded |
| CDC-05014 | RWB-P2-E2034-OPS | GAP-0590 | 12 | Publish key format EFS:<efs_record_key>, the view-row fold count, the ledger writer hit count and the run summary with both counts as the run key set. |

### OTHER:Ledger harness pack (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04990 | RWB-P2-E2034-CON | GAP-0416 | 16 | Hold composite route, merge order, SIT environment, seeding, evidence format, retention and pass/fail gate as harness data agreed at wave-2 entry. |
| CDC-05016 | RWB-P2-E2034-OPS | GAP-0416 | 16 | Hold the composite route, merge order, SIT environment, seeding, evidence format, retention and pass/fail gate as data in the harness pack. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04785 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-8 | 12.1; 12.5; 13 | Register rwb-integration as consumer of rwb.source-data.AceDataReady.v1 and rwb.treatment.TreatmentApproved.v1; add BookingMatchWorkflow row; publish the rerun path. |

### RWB-P2-E2007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04801 | RWB-P2-E2007-APP | DOR-RWB-P2-E2007-APP-10 | Not specified in the source documents (DOR-RWB-P2-E2007-APP-10) | Add empty, loading, error and no access states for screens SCR-01, SCR-14 and SCR-29 in the screen specification. |

### OTHER:Functional Specification Document P6 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04806 | RWB-P2-E2007-APP | GAP-2395 |  | Name which of the three Epic 2 package codes the rwb-comms notice reads and its version label, settled with the rule registry owner; no fourth code and no assumed assignment. |

### OTHER:TSD P4 (T6.1 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04809 | RWB-P2-E2007-APP | GAP-0923 | 13 | Add Case record and Treatment and offer columns to T6.1 with CASE_RECORD R and U and TREATMENT_AND_OFFER R for RW-RESTRUCT and RW-CREDITAD. Publish the 14-area matrix with RWB-P4-AD002-APP after matrix-owner confirmation. |

### OTHER:ACE team database login allocation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04818 | RWB-P2-E2007-APP | GAP-2489 |  | The rwb-decision database login name is in no source. The ACE team must allocate it; no story edit. |

### OTHER:Parameter and reference-data registers; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04819 | RWB-P2-E2007-APP | GAP-2692 | 1 | Add booking.missing.grace_loads and treatment-type and outcome list codes; record TreatmentBooked ownership against rwb-payment; record the parent stage outcome contract in the rwb-case baseline. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04822 | RWB-P2-E2007-CON | DOR-RWB-P2-E2007-CON-8 | 12 | Clear each detcheck failure: the rerun path, the rwb-integration consumer rows for EV-26 and EV-10, the BookingMatchWorkflow and readBookedTerms rows, and the 6 more listed. |

### OTHER:Functional Specification Document S2 (A2.6.3.1; OTHER:A2.13.2; OTHER:A2.10.2; OTHER:A2.17.2); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04823 | RWB-P2-E2007-CON | GAP-1696 | 12 | Route ACE and ALS, COLLINS, NLEADS and CCMS facts through rwb-source-data; add S2 to the P1 REST cell of the connection matrix; no direct view or table read. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04836 | RWB-P2-E2007-CON | GAP-2395 | find it | Read the three Epic 2 package codes and version labels through the contract as the fixture set; settle the rwb-comms package assignment with the rule registry owner. |

### OTHER:FSD S2 (Services and Dependencies) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04837 | RWB-P2-E2007-CON | GAP-1713 | find it | Record each feature-code prerequisite once as the owning service contract: approval to P7, case to P3, documents to P5, communications to P6, valuation to S1. |

### OTHER:FSD S2 (A2.10; OTHER:A2.11; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04838 | RWB-P2-E2007-CON | GAP-1703 | find it | Let rwb-payment own booking, payment matching and posting; this service records the booking reference from TreatmentBooked and the break from PaymentMissed. |

### OTHER:RWB-PLT-DB; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:TSD P2 Integration v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04839 | RWB-P2-E2007-CON | GAP-0657 | find it | Allocate the rwb-integration login in RWB-PLT-DB; record the Architecture v5 slide 44 rwb-payment owner row and TSD P2 v3 T5.2 as superseded; fix the six unsettled consumed paths and shapes with their owners. |

### OTHER:TSD P1 v3 note; OTHER:Section B notes (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04840 | RWB-P2-E2007-CON | GAP-0596 | 3, 11 | Answer shape and flag set to Not specified; no value invented |

### API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04841 | RWB-P2-E2007-CON | GAP-0597 | 11 | Query, answer fields, error and right set to Not specified |

### RWB-P1-E2007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04842 | RWB-P2-E2007-CON | GAP-0594 | 11, 12 | Publish the property names of BookingFact, FieldState and BatchStatusAnswer and add GET /booking-facts and GET /batch-status to the next API Specification version. |

### OTHER:Booking confirmation harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04846 | RWB-P2-E2007-CON | GAP-0395 | 13 | At the wave 2 entry check, agree the composite route path and merge order, the harness environment, ALS fixture format, seed pack, evidence format, retention and pass or fail gate. |

### OTHER:Gap register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04847 | RWB-P2-E2007-CON | GAP-0658 | 4 | Record the JOB-08 owner conflict and the TSD P2 v3 T5.2 supersession; contract owners confirm element names and the seven message texts at review. |

### OTHER:rwb-case booking confirmation story and S2 contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04849 | RWB-P2-E2007-CON | GAP-0730 | 11 | Fix the rwb-case login in the platform DB story; publish the composite route, treatment booking fields and raiseTask result schema with the S2 contract. |

### OTHER:rwb-decision event contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04850 | RWB-P2-E2007-CON | GAP-2487 | 4 | Publish rwb.decision.BookingDecisionMade.v1 on rwb.decision.events.v1 per treatment and business date, keyed by treatmentId, with outcome, row, package code and version, business date and difference terms. |

### OTHER:Parameters contract (DP-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04854 | RWB-P2-E2007-CON | GAP-0924 | 7 | Register the cache lifetime as a parameter with its value agreed at the wave 2 design review. |

### OTHER:Gap register (GAP-2491) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04856 | RWB-P2-E2007-CON | GAP-2491 | 7 | Timezone, overlap, retry, fallback and flag-off behaviour set to Not specified |

### OTHER:TSD P7 v2 and rwb-reporting read model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04857 | RWB-P2-E2007-CON | GAP-2492 | 8 | BR3 routes the REC-03 break list through rwb-reporting read models. |

### OTHER:Parameters and reference-data registers; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04858 | RWB-P2-E2007-CON | GAP-2692 | none | Add booking.missing.grace_loads and the treatment-type and outcome list codes; record TreatmentBooked owner rwb-payment; record the parent stage outcome contract. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04863 | RWB-P2-E2007-OPS | DOR-RWB-P2-E2007-OPS-8 | 12.4, 12.5 | Add rwb-integration as consumer of rwb.source-data.AceDataReady.v1 and rwb.treatment.TreatmentApproved.v1; register BookingMatchWorkflow, readBookedTerms and the other detcheck items. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04865 | RWB-P2-E2007-OPS | CG-ALL-3159 | 3, 7, 12.7 | Record decision_record as the PLT library table in rwb_integration in the owning dictionary. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04874 | RWB-P2-E2007-OPS | DOR-RWB-P2-E2007-OPS-11 | find it | Name the P2 fields classed as personal data that this story does not carry and align their classification with the story. Field names are not in the source documents. |

### RWB-P6-E1073-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04876 | RWB-P2-E2007-OPS | GAP-2395 | find it | Read the three package codes and version labels through the contract as the fixture set; prove AC1 and AC5 against them; settle rwb-comms package assignment with the rule registry owner. |

### OTHER:FSD S2 and service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04877 | RWB-P2-E2007-OPS | GAP-1713 | find it | Map each FEAT prerequisite to its owning service contract (approval to P7, case to P3, documents to P5, communications to P6, valuation to S1); carry duplicate FEAT-CHO-08 as written. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:TSD P2 Integration v3; RWB-P2-E2007-CON; OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04879 | RWB-P2-E2007-OPS | GAP-0657 | find it | Record Arch v5 slide 44 rwb-payment JOB-08 row and TSD P2 v3 T5.2 as superseded; read ACE facts via rwb-source-data contract; fix the six consumed paths in RWB-P2-E2007-CON; allocate rwb-integration login in RWB-PLT-DB. |

### OTHER:Booking confirmation integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04887 | RWB-P2-E2007-OPS | GAP-0395 | 4 | Integration lead and QA lead agree the composite route path and merge order with the platform edge story, and the harness environment, ALS fixture format, seed pack, evidence format, retention and pass or fail gate at the wave 2 entry check; record in the harness pack. |

### RWB-P2-E2007-CON; RWB-S2-E3001-CON; OTHER:platform DB story for the rwb-case login (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04890 | RWB-P2-E2007-OPS | GAP-0730 |  | Publish the rwb-case login, the gateway-bff composite route with its field list, the treatment booking fields, and the raiseTask result schema. |

### RWB-P2-E2007-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04892 | RWB-P2-E2007-OPS | GAP-2487 |  | Publish rwb.decision.BookingDecisionMade.v1 per treatment and business date on rwb.decision.events.v1, keyed by treatmentId, carrying outcome, row, package code and version, business date and difference terms. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04896 | RWB-P2-E2007-OPS | GAP-0924 | find it | Add a cached-authorise lifetime parameter for rwb-access, value agreed at the wave 2 design review; the version-keyed drop test sits in section 16, not in this chunk. |

### parameter-catalog.csv; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04899 | RWB-P2-E2007-OPS | GAP-2692 | find it | Add booking.missing.grace_loads and the treatment-type and outcome list codes to the registers; record TreatmentBooked owner as rwb-payment; record the stage outcome contract in the rwb-case baseline. |

### OTHER:P3 and P4 contract stories (ageing read, reference-data read, access-log operation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04911 | RWB-P2-E2033-APP | GAP-0660 | find it | Fix the ageing read, the reference-data read and the access-log operation in the P3 and P4 contract stories; the ownership, paths and one-hop reads are already stated in this story (sections 4 and 12.2). |

### RWB-P2-E2033-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04912 | RWB-P2-E2033-APP | GAP-3101 | find it | Add GET /api/recovery/deviation/v1/deviation-flags as a read-only rwb-deviation row in the Ownership Map and to the consumed set of RWB-P2-E2033-CON at its next revision. |

### OTHER:Wave 2 release record (appendix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04914 | RWB-P2-E2033-APP | GAP-0415 | find it | Integration lead and QA lead ratify the harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence and gate format as one appendix before RWB-ITG-E2033-ITG claims Done. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:owner P3 rwb-case; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04919 | RWB-P2-E2033-CON | DOR-RWB-P2-E2033-CON-5 | 9 | Remove CAR from, or confirm CAR as a value of, LOV-CASE-STATUS, LOV-PRODUCT and LOV-STAGE; this story adds no LOV value. |

### RWB-P3-E2011-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04926 | RWB-P2-E2033-CON | GAP-0660 | 1 | Fix the ageing read, reference-data read and access-log operation in the P3 and P4 contract stories; keep GET /cases and its export with rwb-case. |

### RWB-P3-E2011-APP; parameter-catalog.csv; OTHER:RWB-E2-033 legacy story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04927 | RWB-P2-E2033-CON | GAP-2224 | 11 | Confirm page bounds and export limit as parameter rows, fix row and envelope names in v1, drop the duplicate timer index and name the login and flag owner in the rwb-case baseline. |

### OTHER:rwb-access contract baseline (rwb-access owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04929 | RWB-P2-E2033-CON | GAP-2320 | header | The P2 attribution is recorded in the header as a build-against dependency. Element names stay open until the baseline review with the rwb-access owner. |

### OTHER:wave 2 release record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04930 | RWB-P2-E2033-CON | GAP-0415 | none | Add one appendix ratifying the SIT harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence and gate format, signed by the integration lead and QA lead. |

### RWB-P2-E2034-CON; RWB-P1-E2001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04958 | RWB-P2-E2034-APP | GAP-2186 | 12 | Publish the contact-fact read with its path, contact-key parameter and masked members; confirm the EFS outcome read as GET /efs-history or name its operation; realign the two consumed rows. |

### OTHER:Ledger harness pack (SIT) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04959 | RWB-P2-E2034-APP | GAP-0416 | find it | Record composite route path and merge order, SIT environment, EFS batch seeding, evidence format and retention, and pass/fail gate agreed at wave 2 entry check. |

### OTHER:Recovery Workbench plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04965 | RWB-P2-E2034-APP | GAP-3187 | find it | Keep rwb-integration as primary for RWB-E2-033 to RWB-E2-036 and record the tension for the assembly step. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:rwb-access API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04971 | RWB-P2-E2034-CON | DOR-RWB-P2-E2034-CON-8 | 12.5 | Catalog: add the 2 workflows and 7 activities of RWB-P2-E2034-CON 12.5. rwb-access: publish POST /api/recovery/access/v1/authorise. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04972 | RWB-P2-E2034-CON | GAP-1844 |  | Keep wave 2 for RWB-E2-019 partner identity slice RWB-S9-E2019-APP, with the partner_user binding and FAPI 2.0 route published before panel work. Ledger slice stays on P1. |

### OTHER:FSD P7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04984 | RWB-P2-E2034-CON | GAP-1612 | 8 | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012. |

### OTHER:Wave-2 masking policy load and access-log design (Compliance; OTHER:Internal audit) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04988 | RWB-P2-E2034-CON | GAP-2321 | 3 | Settle masking version label, covered field IDs, AC-READ granularity and parameter rows; confirm the authorise element against RWB-P4-E1037-CON at contract review. |

### RWB-P1-E2001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04989 | RWB-P2-E2034-CON | GAP-2186 | 12.2 | Confirm GET /efs-history answers the EFS outcome list, or name the operation that does; publish the contact-fact read on the P1 base with path, key parameter and masked members. |

### RWB-P2-E2034-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04991 | RWB-P2-E2034-CON | GAP-0666 |  | Carry consumer groups, offset policy, commit point, scan and retry intervals, lag and alert thresholds, build ID format and smoke fixture owner as environment values, not code. |

### OTHER:rwb-partner interaction-ledger slice (S9) story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04993 | RWB-P2-E2034-CON | GAP-3149 |  | Declare the partner fact, its seven ledger attributes, the transaction rule and a read-only view with placeholders; claim no ledger row, retention class or timeline read. |

### RWB-P1-E1066-CON; RWB-P1-E1066-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04996 | RWB-P2-E2034-CON | GAP-2185 | none | Settle one ledger path family in RWB-P1-E1066-CON and realign the append row and its fake in RWB-P1-E1066-APP to POST /cases/{caseId}/interactions. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05001 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-22 | find it | Publish a contract fake library version and record it as published. |

### OTHER:P3 screen specification (SCR-09; OTHER:SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05006 | RWB-P2-E2034-OPS | DOR-RWB-P2-E2034-OPS-10 | 12.7 | State the empty, loading, error and no-access states of SCR-09 and SCR-44 in the screen specification. |

### OTHER:Batch and Scheduling, next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05013 | RWB-P2-E2034-OPS | GAP-3176 | 12.5 | Confirm that no Epic 2 step depends on JOB-01 and carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### OTHER:Release readiness review (environment values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05019 | RWB-P2-E2034-OPS | GAP-0666 | 12 | Approve consumer groups, offset policy, commit point, scan and retry intervals, lag thresholds, build ID format and fixture owner as environment values. |

### 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20595 | RWB-P2-E2034-OPS | R-22304 |  | JOB-01 already retired (D-RCV-35); data jobs start on the ACE batch-complete record. No AceIngestCheck name in sources; JOB-04 is Daily reconciliation. No change. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0395 | Booking confirmation integration harness: composite booking and treatment route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0415 | The SIT harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence format for the case-list journey are not specified in any source read | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0416 | Ledger harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0594 | The shapes and property names of the two booking-fact reads are in no source document | Tech lead | Resolved (directive) |
| GAP-0595 | The case's account set and its product group have no P1 read in the target | Solution architect | Resolved (directive) |
| GAP-0596 | How the read answers the three Section B columns, and which flag holds it back, is stated nowhere | Data architect | Resolved (directive) |
| GAP-0597 | The batch-status answer has two values in the legacy interface and nine fields in the view, and no source fixes which of them it returns | Tech lead | Resolved (directive) |
| GAP-0598 | No source says where the account read ends and the built match facts begin | Solution architect | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0658 | rwb-integration booking confirmation (contract slice): the JOB-08 ownership and consumer lists, the ACE read boundary, the rerun placement and the twelve consumed shapes are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0659 | rwb-integration booking confirmation (deployment slice): the login and secret reference, the JOB-08 ownership, the alert thresholds, the runbook ownership and the backfill limit are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner; business on-call owner for the package alerts | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0664 | The rwb-integration login, the entry and fact JSON field names, the admin bodies, the mapping detail, the retry intervals and the ownership split of the ledger intake are not fixed in the source documents | Solution architect | Resolved (directive) |
| GAP-0665 | The append, EFS and contact wire shapes, the admin operation bodies, the dedupe key of each type and the ordering of the append and the inbox are not stated for the intake contract | Solution architect | Resolved (directive) |
| GAP-0666 | The consumer group names, the offset policy, the retry scan interval, the lag and alert thresholds, the build ID format and the fixture owner of the intake deployment are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0730 | rwb-case booking confirmation: login, composite route, treatment booking fields, match-result shape and route-rule evaluator owner are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0922 | rwb-access booking confirmation: the authorise request and answer shapes, the contract entry of the authorise path and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0923 | rwb-access booking confirmation: the TSD RBAC matrix has no Case record column, so the CASE_RECORD R and U letters the booking tasks need are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0924 | rwb-access booking confirmation: the lifetime of a cached authorise decision is not specified | Solution architect | Resolved (directive) |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-2184 | The retention class list, the added event codes, the link column types and the feature IDs of four requirements are in no source | Data architect | Resolved (directive) |
| GAP-2185 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2186 | The EFS outcome read and the contact-fact read that the channel consumer calls are named by interface only, with no path, parameter or owning story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2224 | The case list is served twice in the target, and the row names, the bounds, the login and the flag mechanism of the owner's list have no source | Solution architect | Resolved (directive) |
| GAP-2225 | Element names of the interaction item, the append command and the intake result are not in the sources | TechX and rwb-source-data contract owner | Resolved (directive) |
| GAP-2226 | Legacy occurred-time order and the case timeline page order differ | TechX | Resolved (directive) |
| GAP-2320 | rwb-access answer behind the case and queue list: element names, the P2 attribution of the contract dependency, the authorise branch, the extract record, the login and the parameter and reference paths are not settled by any source read | Solution architect | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2485 | The booking-confirmation decision is placed in rwb-decision while DP-04 and the registry story keep the evaluation in the owning service and state that rwb-decision never evaluates | Solution architect, with the decision service owner | Resolved (directive) |
| GAP-2486 | The operation set, paths and payloads of the batch, account, treatment, task, parameter and list contracts, the decision code, the record's snapshot and actions shape and several read and message details are in no source | Solution architect, with the owners of rwb-integration, rwb-treatment and rwb-case | Resolved (directive) |
| GAP-2487 | No source names the event that carries a booking decision out of rwb-decision, because the legacy TreatmentBooked is rwb-payment's and is raised after the treatment is booked | Solution architect, with the event platform owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2489 | The name of the rwb-decision database login is in no source | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2490 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its eleven legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2491 | The timezone, overlap, retry and fallback of the JOB-08 run and the behaviour of the legacy feature flag when off are in no source | Solution architect, with the workflow platform owner | Resolved (directive) |
| GAP-2492 | The legacy run writes the REC-03 result to reconciliation_result, and no table or owner of that name exists in the target and no source assigns the break list | Solution architect, with the reporting owner | Resolved (directive) |
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2692 | The rwb-treatment share of the key is stated by no S2 source, the P2 contract shapes it follows are unpublished, and the trigger, the task-raising and the event ownership are split across stories | Solution architect with the rwb-integration, rwb-treatment and rwb-case tech leads and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3101 | rwb-deviation case and queue list slice: no read in the Ownership Map, no seam with the composed page, no path, field names or page bound, the flag derived twice and the pause projection without the rule package | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3149 | rwb-partner interaction-ledger slice: no ledger column or operation in S9, no published payload for EV-20 or EV-21, the seam with RWB-P2-E2034-CON undefined, the list members, the retry bound and the holder-reference form unpublished, and an empty H row against ten platform contracts | Solution architect; rwb-integration contract owner (RWB-P2-E2034-CON); rwb-source-data ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P2-E2033-APP | Not specified without item ID | 236 | Then with the ageing flag off (name Not specified in the source documents, GAP-2224) the breached parameter is ignored and the case-side columns are kept |
| RWB-P2-E2033-APP | Not specified without item ID | 540 | \| TC-E2-033-17 \| BR12 \| End to end \| Ageing flag off (name Not specified in the source documents, GAP-2224); breached parameter ignored and case-side columns ke |
| RWB-P2-E2033-APP | Not specified without item ID | 542 | \| TC-E2-033-19 \| AC13, BR8, BR9, BR10, BR11, BR12, BR13 \| End to end \| Contract mocks as in AC13; ageing flag off and on (Not specified in the source documents, |
| RWB-P2-E2034-APP | skipped AC ID | 115 | missing: AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9, AC10, AC11, AC17 |
