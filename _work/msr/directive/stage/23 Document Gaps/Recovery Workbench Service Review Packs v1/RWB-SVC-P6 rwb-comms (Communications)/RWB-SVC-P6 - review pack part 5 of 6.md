# RWB-SVC-P6 rwb-comms (Communications) - review pack, part 5 of 6 (RWB-P6-E2026-APP to RWB-P6-E4041-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 15 |
| Resolved in the stories | 323 |
| Cross-document (pending in another document) | 242 |
| Not applied (value not in the sources) | 28 |
| Open business decisions | 26 |
| Register gaps linked | 113 |
| Unconfirmed assumptions | 0 |
| Lint findings | 4 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P6-E2026-APP | 13 | 16 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2026 APP Document generation engine for contract, CA and mortgage templates v2.md |
| RWB-P6-E2042-APP | 23 | 35 | 9 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2042 APP Epic 2 rule packages in Drools v2.md |
| RWB-P6-E4035-APP | 22 | 20 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4035 APP View the offer on LINE and web v2.md |
| RWB-P6-E4035-CON | 20 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4035 CON View the offer on LINE and web - contract v2.md |
| RWB-P6-E4036-APP | 23 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4036 APP Accept an offer in self-service v2.md |
| RWB-P6-E4036-CON | 19 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4036 CON Accept an offer in self-service - contract v2.md |
| RWB-P6-E4037-APP | 23 | 16 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4037 APP Pay in self-service v2.md |
| RWB-P6-E4037-CON | 21 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4037 CON Pay in self-service - contract v2.md |
| RWB-P6-E4038-APP | 21 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4038 APP Raise a dispute in self-service v2.md |
| RWB-P6-E4038-CON | 18 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4038 CON Raise a dispute in self-service - contract v2.md |
| RWB-P6-E4039-APP | 34 | 9 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4039 APP Maintain the contact repository v2.md |
| RWB-P6-E4039-CON | 21 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4039 CON Maintain the contact repository - contract v2.md |
| RWB-P6-E4040-APP | 23 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4040 APP Record a custody movement of a document v2.md |
| RWB-P6-E4040-CON | 13 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4040 CON Record a custody movement of a document - contract v2.md |
| RWB-P6-E4041-APP | 29 | 10 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4041 APP Answer a legal or audit document request v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P6-E4035-APP | R-01701 | CG-ALL-6633 | Script gap | Product owner | The story adds WEB to the closed list LOV-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P6-E4035-CON | R-01705 | CG-ALL-6646 | Script gap | Product owner | The story adds WEB to the closed list LOV-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P6-E2042-APP | R-11077 | CG-ALL-6628 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4035-APP | R-11083 | CG-ALL-6642 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4035-CON | R-11086 | CG-ALL-6653 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4036-APP | R-11092 | CG-ALL-6665 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4036-CON | R-11097 | CG-ALL-6677 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4037-APP | R-11102 | CG-ALL-6689 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4037-CON | R-11105 | CG-ALL-6699 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4038-APP | R-11110 | CG-ALL-6709 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4038-CON | R-11114 | CG-ALL-6720 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4039-APP | R-11118 | CG-ALL-6729 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4039-CON | R-11120 | CG-ALL-6738 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4040-APP | R-11124 | CG-ALL-6747 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4040-CON | R-11126 | CG-ALL-6757 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4041-APP | R-11132 | CG-ALL-6770 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4040-APP, RWB-P6-E4040-CON, RWB-P6-E4041-APP, RWB-P6-E4041-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22551 | GAP-1607 | Register gap | Product owner | Seven features in the Communications functional specification belong to other services in Architecture v5 | Keep the seven features in the source with their identifiers, mark them as not carried in section 5.1 of this PRD with their owning service, and raise the story-level split in the service work packages. |
| RWB-ITG-E2022-ITG, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4039-APP, RWB-P6-E4039-CON, RWB-P7-E2022-APP | R-22574 | GAP-2091 | Register gap | Service owners of P6 rwb-comms and P1 rwb-source-data; product owner | The contact point and its consent state are a P6 feature but a P1 table, and no endpoint carries them | Keep the contact point and its consent in P1 rwb_source_data.contact_point_ext as the owner of record, and have rwb-comms read and maintain it through a P1 contract that the P1 API specification publishes. |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-22619 | GAP-1287 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The generation record's payload, value sets, read shape, message set and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the container of the template code, the template version, the treatment reference and the requesting role on decision_log_entry, the shape of the merge snapshot reference, the decision code D6.4 as a value of LOV-DECISION, the final-call list that holds GENERATED, the message ids and texts of a refused record and a duplicate append, the page-size parameter name, the search index and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2026-1 to ASM-B-P7-03-E2026-5 and its nine criteria stand on that shape |
| RWB-P6-E4039-APP, RWB-P6-E4039-CON | R-23104 | GAP-1121 | Register gap | Compliance and PDPA officer | The consent state set, the verification rule and the failed-count threshold are not given by any source | Carry the consent set, the verification rule, the failed-count threshold and the decision code as parameters and reference data read with the version in force, with the placeholder in the contract, and let the compliance and PDPA officer confirm the values before the baseline review closes. |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-28820 | GAP-0940 | Register gap | Compliance and PDPA officer | The masking version label and the DF-PTY-007 rows on the generation path are not specified | Load the DF-PTY-007 masking rows with unmasked false for RW-RESTRUCT, RW-CASEOWN, RW-TEAMMGR and SY-CASEWF under the SIT masking version, name the version in the policy pack load record, and leave the format to the one masking library every screen uses. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-P6-E4039-APP, RWB-P6-E4039-CON | R-37323 | ASM-2069 | Register assumption |  | The consent state set, the verification rule, the failed-count threshold and the decision code of a consent change are parameters and reference data read with the version in force, and their values are left to the compliance and PDPA officer. | The compliance and PDPA officer confirms the consent set, the verification rule, the failed-count threshold and the decision code before the baseline review closes. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P6-E2026-APP | R-17702 | DOR-RWB-P6-E2026-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | AC16 needs a unique test row or an added AC16 reference on the existing TC-E2-026-16 row. |
| RWB-P6-E2026-APP | R-22616 | GAP-0408 |  | The generation harness pack, the template fixtures and the PDF/A conformance check are not specified | Fixtures, PDF/A check, font pack, harness, seeding and evidence format are in no source; ownership.json gives owners only. Needs P5, P6 and QA agreement. |
| RWB-P6-E2026-APP | R-26110 | CG-ALL-6616 |  | Story cites document versions that are not the highest | The Test Cases v7 citation is not in the supplied story parts, so no old text exists to edit. Document Index v14 gives the highest version. |
| RWB-P6-E2026-APP | R-28784 | GAP-1704 |  | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | A2.8, A2.15 and A2.18 are not in this chunk; the P5 and P6 routing cannot be written without their text. |
| RWB-P6-E2042-APP | R-06525 | DOR-RWB-P6-E2042-APP-14 | Not located in chunk | Definition of Ready item 14 Epic design: Fail | No epic design sign-off is in the story text or the 03 Requirements sources searched. Confirming it would invent a value. |
| RWB-P6-E2042-APP | R-06526 | Definition of Ready item 16 Size: Fail | header | Definition of Ready item 16 Size: Fail | No size is in the sources; the unsourced squad sizing claim is removed. |
| RWB-P6-E2042-APP | R-06528 | DOR-RWB-P6-E2042-APP-22 | Not located in chunk | Definition of Ready item 22 Fake published: Fail | No contract fake library version is recorded as published in the story text or the sources searched. Recording one would invent a value. |
| RWB-P6-E2042-APP | R-17703 | DOR-RWB-P6-E2042-APP-10 | Not located in chunk | Definition of Ready item 10 Screens and states: Partial | SCR-33 and SCR-39 rows sit outside this chunk, so the empty, loading, error and no-access states cannot be anchored or added. |
| RWB-P6-E2042-APP | R-17704 | DOR-RWB-P6-E2042-APP-11 | Not located in chunk | Definition of Ready item 11 Guardrails: Partial | The guardrail text is outside this chunk and no source classifies the fields as personal data, so no value can be set. |
| RWB-P6-E2042-APP | R-17707 | DOR-RWB-P6-E2042-APP-4 | Not located in chunk | Definition of Ready item 4 Business rules: Partial | Section 7 criteria and section 16 test rows are outside this chunk. BR1 to BR12 criteria and tests cannot be numbered or anchored without them. |
| RWB-P6-E2042-APP | R-22325 | GAP-2395 | Not located in chunk | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | The proof needs AC1 and AC5 text in section 7, which is outside this chunk. Package assignment for rwb-comms stays with the rule registry owner; no code is invented. |
| RWB-P6-E2042-APP | R-26114 | CG-ALL-6629 Criteria and tests keep legacy job and decision-log wording | 7 | Criteria and tests keep legacy job and decision-log wording | AC3 is outside this chunk, so its JOB-nn wording stays. The AC2 change is a wording alignment only. |
| RWB-P6-E2042-APP | R-28856 | GAP-1302 | not found in story | The package title, the dry-run breakdown, the MSG-P3-015 text and the switch-off answer are not specified | DF-REF-276, DF-REF-293, MSG-P3-015 and the rollback and flag-off answers do not appear in the story text; no edit point exists. Source is the legacy story. |
| RWB-P6-E4035-APP | R-06531 | DOR-RWB-P6-E4035-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No epic design sign-off record in the story or sources (searched Decision Log and story files). A sign-off cannot be recorded without inventing one; needs the record. |
| RWB-P6-E4035-APP | R-11081 | CG-ALL-6639 | 12.1 | HTTP errors with no message ID: 401 no session; 404 the notice is absent or out of scope | Error and Message Standard v4 has no 401 or 404 message ID (grep of the standard found none). MSG-GEN-006 does not fit. Needs a new ID from the BA; not invented. |
| RWB-P6-E4035-APP | R-26118 | CG-ALL-6643 | 3 | Flyway file V4035_1__notice_view.sql is not in the V0001..Vnnnn form | Sibling rwb-comms stories use V<story number>_1, but the service's next Flyway number is not in the sources (Service Template Spec v1 sec 3.1). Line 203 is not in the supplied story text, so it cannot be edited here. |
| RWB-P6-E4036-APP | R-11090 | CG-ALL-6661 | 4, 12.1 | HTTP errors with no message ID: 401 no session; 404 the notice is absent or out of scope | Error and Message Standard v4 has no 401 or 404 message; MSG-GEN-006 covers system unavailable only. No message ID invented; BA decision needed. |
| RWB-P6-E4036-APP | R-26124 | CG-ALL-6666 | 3, 3.1 | Flyway file V4036_1__notice_response.sql is not in the V0001..Vnnnn form | No next Vnnnn number for the rwb-comms Flyway sequence in the sources. The V4036_1 name sits in section 13, outside the supplied text. |
| RWB-P6-E4036-CON | R-23080 | GAP-1106 | Change log | The two response operations of a notice are in no source inventory | Change log was not edited; the two operations are stated only in section 15, without the Idempotency-Key rule or error set. |
| RWB-P6-E4037-APP | R-17745 | DOR-RWB-P6-E4037-APP-11 | 13 | Definition of Ready item 11 Guardrails: Partial | No source names the field detcheck classes as personal data. Story says no personal data (lines 237, 374). Story left unchanged; a field name cannot be invented. |
| RWB-P6-E4037-APP | R-26130 | CG-ALL-6690 | 12.8 | Flyway file V4037_1__payment_intent.sql is not in the V0001..Vnnnn form | Next rwb-comms Vnnnn number is not in the sources (no sibling migration numbers found). Supplied text at line 311 is blank. Solution architect to confirm. |
| RWB-P6-E4039-APP | R-26142 | CG-ALL-6730 | 3, 3.1 | Flyway file V4039_1__contact_stop.sql is not in the V0001..Vnnnn form | Story does not name V4039_1; the service's current Flyway number is not in any source (grep found none). Solution architect to confirm. |
| RWB-P6-E4039-CON | R-11121 | CG-ALL-6739 | 12.8 | Criteria and test data read ACE views directly | Fake row added to 12.8. AC6 Given lines are in section 7, outside this chunk, so whether they still read ACE views is not verified. Answers are not specified in the sources. |
| RWB-P6-E4040-APP | R-26148 | CG-ALL-6748 | 3, 3.1 | Flyway file V4040_1__notice_custody_ref.sql is not in the V0001..Vnnnn form | Next Flyway number is not in the sources (V0001 is only the baseline, Service Template §3). Migration name is on line 297, outside this chunk; no number invented. |
| RWB-P6-E4041-APP | R-01744 | CG-ALL-6766 |  | rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data | Ruling recorded from Reference Data v5 Lists. The LOV-DELIVERY sentence is not in this chunk, so the story cannot be edited here. The yaml needs no change. |
| RWB-P6-E4041-APP | R-01745 | CG-ALL-6767 |  | rwb-comms.yaml holds sentType as a closed enum while the story reads LOV-SENT-TYPE as data | Ruling recorded from Reference Data v5 Lists. The LOV-SENT-TYPE sentence is not in this chunk, so the story cannot be edited here. The yaml needs no change. |
| RWB-P6-E4041-APP | R-11130 | CG-ALL-6765 | 12.1 | HTTP errors with no message ID: 401 no session; 404 the case or the request is absent or out of scope | Standard v4 has no 401 or 404 message. MSG-GEN-006 fits store failure only. New IDs need BA confirmation and none is invented, so the placeholders stand. |
| RWB-P6-E4041-APP | R-17811 | DOR-RWB-P6-E4041-APP-10 | 4 | Definition of Ready item 10 Screens and states: Partial | FSD P6 Communications v3 defines SCR-33 as Template approval, not this screen. No state definitions found in sources, so the placeholder stands. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (55)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11311 | RWB-P6-E4035-APP | CG-ALL-6637 | 12.1 | Publish GET /api/recovery/comms/v1/notices/{noticeId}/channel-view?channel={channel} through RWB-P6-E4035-CON, or remove it from this story. |
| CDC-11312 | RWB-P6-E4035-APP | CG-ALL-6638 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/views through RWB-P6-E4035-CON, or remove it from this story. |
| CDC-11316 | RWB-P6-E4035-APP | DOR-RWB-P6-E4035-APP-8 | find it | Publish GET channel-view and POST views paths through RWB-P6-E4035-CON; the topic is fixed in §12.3. |
| CDC-11331 | RWB-P6-E4035-CON | CG-ALL-6649 | 12.1 | Publish GET /api/recovery/comms/v1/notices/{noticeId}/channel-view (channel query required, 200 NoticeChannelView, errors 401, 403, 404, 409, 422, 503). |
| CDC-11332 | RWB-P6-E4035-CON | CG-ALL-6650 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/views (NoticeViewRequest, 201 NoticeView, Idempotency-Key required; errors 401, 403, 404, 409, 422, 503). |
| CDC-11333 | RWB-P6-E4035-CON | DOR-RWB-P6-E4035-CON-8 | 12.1 | Publish GET channel-view and POST views operations as in CG-ALL-6649 and CG-ALL-6650. Topic defect fixed in story §12.3. |
| CDC-11345 | RWB-P6-E4036-APP | CG-ALL-6659 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/responses through RWB-P6-E4036-CON |
| CDC-11346 | RWB-P6-E4036-APP | CG-ALL-6660 | 12.1 | Publish GET /api/recovery/comms/v1/notices/{noticeId}/responses through RWB-P6-E4036-CON |
| CDC-11347 | RWB-P6-E4036-APP | DOR-RWB-P6-E4036-APP-8 | 12.1 | Publish both notice response paths and resolve the closed deliveryStatus enum; 401 and 404 message IDs are not in the sources |
| CDC-11360 | RWB-P6-E4036-CON | CG-ALL-6673 | 12.1 | Add path POST /api/recovery/comms/v1/notices/{noticeId}/responses with the ResponseRequest and Response schemas as declared in section 12.1. |
| CDC-11361 | RWB-P6-E4036-CON | CG-ALL-6674 | 12.1 | Add path GET /api/recovery/comms/v1/notices/{noticeId}/responses with the Response list shape as declared in section 12.1. |
| CDC-11363 | RWB-P6-E4036-CON | DOR-RWB-P6-E4036-CON-8 | 12.1, 12.3 | Add the POST and GET /api/recovery/comms/v1/notices/{noticeId}/responses paths; the story-side event name is already fixed in 12.3. |
| CDC-11373 | RWB-P6-E4037-APP | CG-ALL-6682 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/payment-intents through RWB-P6-E4037-CON, or remove it from RWB-P6-E4037-APP section 12.1. |
| CDC-11374 | RWB-P6-E4037-APP | CG-ALL-6683 | 12.1 | Publish GET /api/recovery/comms/v1/notices/{noticeId}/payment-intents through RWB-P6-E4037-CON, or remove it from RWB-P6-E4037-APP section 12.1. |
| CDC-11378 | RWB-P6-E4037-APP | DOR-RWB-P6-E4037-APP-8 | 12.1 | Add paths POST and GET /notices/{noticeId}/payment-intents; make deliveryStatus match LOV-DELIVERY reference data; the two 401 and 404 message IDs are placeholders in 12.1 (CG-ALL-6684). |
| CDC-11389 | RWB-P6-E4037-CON | CG-ALL-6695 | 12.1 | Add path /api/recovery/comms/v1/notices/{noticeId}/payment-intents with the POST operation as declared in RWB-P6-E4037-CON section 12.1 |
| CDC-11390 | RWB-P6-E4037-CON | CG-ALL-6696 | 12.1 | Add path /api/recovery/comms/v1/notices/{noticeId}/payment-intents with the GET operation as declared in RWB-P6-E4037-CON section 12.1 |
| CDC-11391 | RWB-P6-E4037-CON | DOR-RWB-P6-E4037-CON-8 | header | Add the POST and GET paths /api/recovery/comms/v1/notices/{noticeId}/payment-intents; the event type is already fixed in the story (CG-ALL-6697). |
| CDC-11397 | RWB-P6-E4038-APP | CG-ALL-6704 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/disputes through RWB-P6-E4038-CON, or remove it. |
| CDC-11398 | RWB-P6-E4038-APP | CG-ALL-6705 | 12.1 | Publish GET /api/recovery/comms/v1/notices/{noticeId}/disputes through RWB-P6-E4038-CON, or remove it. |
| CDC-11401 | RWB-P6-E4038-APP | DOR-RWB-P6-E4038-APP-8 | 12.1 | Publish the two dispute paths (CG-ALL-6704, CG-ALL-6705). Story-side message IDs for 401, 404 and 409 and the P1 event type are fixed. |
| CDC-11416 | RWB-P6-E4038-CON | CG-ALL-6716 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/disputes in rwb-comms.yaml, or remove the operation |
| CDC-11417 | RWB-P6-E4038-CON | CG-ALL-6717 | 12.1 | Publish GET /api/recovery/comms/v1/notices/{noticeId}/disputes in rwb-comms.yaml, or remove the operation |
| CDC-11419 | RWB-P6-E4038-CON | DOR-RWB-P6-E4038-CON-8 | 12.1 | Publish POST and GET /api/recovery/comms/v1/notices/{noticeId}/disputes in rwb-comms.yaml, or remove them |
| CDC-11429 | RWB-P6-E4039-APP | CG-ALL-6724 | 12.1 | Publish GET /api/recovery/comms/v1/parties/{partyId}/contact-points through RWB-P6-E4039-CON, or remove the operation. |
| CDC-11430 | RWB-P6-E4039-APP | CG-ALL-6725 | 12.1 | Publish PUT /api/recovery/comms/v1/contact-points/{contactKey} through RWB-P6-E4039-CON, or remove the operation. |
| CDC-11434 | RWB-P6-E4039-APP | DOR-RWB-P6-E4039-APP-8 | 4, 12.1, 12.3 | Publish the GET and PUT contact-point paths. Error message IDs (CG-ALL-6726) remain open. |
| CDC-11438 | RWB-P6-E4039-CON | CG-ALL-6734 | n/a | Add path GET /api/recovery/comms/v1/parties/{partyId}/contact-points with its operation |
| CDC-11439 | RWB-P6-E4039-CON | CG-ALL-6735 | n/a | Add path PUT /api/recovery/comms/v1/contact-points/{contactKey} with its operation |
| CDC-11441 | RWB-P6-E4039-CON | DOR-RWB-P6-E4039-CON-8 | n/a | Publish the GET and PUT contact-point operations; the event name is already corrected in 12.3 |
| CDC-11450 | RWB-P6-E4040-APP | CG-ALL-6742 | 12.1 | Publish POST /notices/{noticeId}/custody-movements under /api/recovery/comms/v1 through RWB-P6-E4040-CON. |
| CDC-11451 | RWB-P6-E4040-APP | CG-ALL-6743 | 12.1 | Publish GET /notices/{noticeId}/custody-movements under /api/recovery/comms/v1 through RWB-P6-E4040-CON. |
| CDC-11456 | RWB-P6-E4040-APP | DOR-RWB-P6-E4040-APP-8 | 4, 12.1, 12.3 | Publish both custody-movements paths through RWB-P6-E4040-CON; error message IDs follow CG-ALL-6744. |
| CDC-11461 | RWB-P6-E4040-CON | CG-ALL-6753 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/custody-movements in rwb-comms.yaml, or remove it from the story. |
| CDC-11462 | RWB-P6-E4040-CON | CG-ALL-6754 | 12.1 | Publish GET /api/recovery/comms/v1/notices/{noticeId}/custody-movements in rwb-comms.yaml, or remove it from the story. |
| CDC-11464 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-8 | 12.1, 12.3 | Publish both custody-movement operations in rwb-comms.yaml; the event type is already corrected in 12.3. |
| CDC-11474 | RWB-P6-E4041-APP | CG-ALL-6763 | 12.1 | Publish POST /api/recovery/comms/v1/cases/{caseId}/document-requests through RWB-P6-E4041-CON. |
| CDC-11475 | RWB-P6-E4041-APP | CG-ALL-6764 | 12.1 | Publish GET /api/recovery/comms/v1/document-requests/{requestId} through RWB-P6-E4041-CON. |
| CDC-11479 | RWB-P6-E4041-APP | DOR-RWB-P6-E4041-APP-8 | 12.1 | Add POST /cases/{caseId}/document-requests and GET /document-requests/{requestId}; align deliveryStatus with LOV-DELIVERY as data, not a closed enum; add message IDs for 401 and 404 (CG-ALL-6765). |
| CDC-20793 | RWB-P6-E4035-APP | R-01702 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01675', 'R-01689', 'R-01690', 'R-01695', 'R-01702', 'R-06468', 'R-06469', 'R-06508', 'R-22347', 'R-22484', 'R-2 |
| CDC-20827 | RWB-P6-E4037-APP | R-01716 |  | POST payment-intents path absent from rwb-comms.yaml. Its PaymentIntent schemas are not defined here; owner CON story must publish them first. |
| CDC-20828 | RWB-P6-E4037-APP | R-01717 |  | GET payment-intents path absent from rwb-comms.yaml. Its PaymentIntent list schema is not defined here; owner CON story must publish it first. |
| CDC-20829 | RWB-P6-E4037-APP | R-06558 |  | deliveryStatus enum already matches LOV-DELIVERY (L616-624). Payment-intents paths need undefined schemas; the 401/404 IDs are story-side. |
| CDC-20830 | RWB-P6-E4037-CON | R-01721 |  | POST payment-intents addition needs PaymentIntentRequest and PaymentIntent schemas not defined in this document; owner CON story publishes it. |
| CDC-20831 | RWB-P6-E4037-CON | R-01722 |  | GET payment-intents addition needs the PaymentIntent list schema not defined in this document; owner CON story publishes it. |
| CDC-20832 | RWB-P6-E4037-CON | R-06562 |  | Contract check depends on the payment-intents paths, which need undefined schemas here; owner CON story publishes them. |
| CDC-20833 | RWB-P6-E4038-APP | R-01724 |  | POST disputes path absent from rwb-comms.yaml. Its DisputeRequest and Dispute schemas are not defined here; owner CON story publishes them. |
| CDC-20834 | RWB-P6-E4038-APP | R-01725 |  | GET disputes path absent from rwb-comms.yaml. Its Dispute list schema is not defined here; owner CON story publishes it. |
| CDC-20835 | RWB-P6-E4038-APP | R-06568 |  | Two dispute paths need DisputeRequest and Dispute schemas not defined in this document; story-side IDs are already fixed. |
| CDC-20836 | RWB-P6-E4038-CON | R-01727 |  | POST disputes operation absent from rwb-comms.yaml. Schemas are not defined here; owner CON story publishes it. |
| CDC-20837 | RWB-P6-E4038-CON | R-01728 |  | GET disputes operation absent from rwb-comms.yaml. Dispute list schema is not defined here; owner CON story publishes it. |
| CDC-20838 | RWB-P6-E4038-CON | R-06572 |  | Both dispute paths need schemas not defined in this document; the event name is fixed in the story, and the yaml paths stay with the owner. |
| CDC-20909 | RWB-P6-E4041-APP | R-01743 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20913 | RWB-P6-E4041-APP | R-06599 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20916 | RWB-P6-E4041-APP | R-01742 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (21)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11282 | RWB-P6-E2042-APP | CG-ALL-6625 | 16 | Add rows TC-E2-042-07 (covers AC2) and TC-E2-042-08 (covers AC3, AC4), with Given, When and Then copied from those criteria. |
| CDC-11319 | RWB-P6-E4035-APP | CG-ALL-6641 | 16 | Add rows for TC-E4-035-01 to TC-E4-035-04 with Given, When and Then copied from the criteria they cover. |
| CDC-11335 | RWB-P6-E4035-CON | DOR-RWB-P6-E4035-CON-12 | 12.7, 16 | Boundary test for the 12.7 tables added as TC-P6-E4035-CON-07; TC-07, TC-08 and TC-09 are missing from Test Cases v8 with the other section 16 IDs. |
| CDC-11343 | RWB-P6-E4035-CON | CG-ALL-6652 | 16 | The test case IDs listed in section 16, including TC-P6-E4035-CON-07 to -09 added here, have no row in Test Cases v8; add them in the next version. |
| CDC-11350 | RWB-P6-E4036-APP | CG-ALL-6664 | 16 | Add rows for TC-E4-036-01 to TC-E4-036-04 and TC-E4-036-05 and TC-E4-036-06, with Given, When and Then copied from the criteria they cover. |
| CDC-11369 | RWB-P6-E4036-CON | DOR-RWB-P6-E4036-CON-12 | 12.7, 16 | Add Story test cases rows for TC-E4-036-01 to TC-E4-036-04 and TC-P6-E4036-CON-01 to TC-P6-E4036-CON-07. |
| CDC-11371 | RWB-P6-E4036-CON | CG-ALL-6676 | 16 | Add rows for TC-E4-036-01 to -04 and TC-P6-E4036-CON-01 to -06 with Given, When and Then copied from the criterion each covers. |
| CDC-11381 | RWB-P6-E4037-APP | CG-ALL-6688 | 16 | Add rows TC-E4-037-01 to TC-E4-037-04 to tab Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-11383 | RWB-P6-E4037-APP | DOR-RWB-P6-E4037-APP-12 | 16 | Add the rows of TC-E4-037-01 to TC-E4-037-04 to Story test cases (CG-ALL-6688). |
| CDC-11394 | RWB-P6-E4037-CON | DOR-RWB-P6-E4037-CON-12 | 16 | Add the ten listed TC IDs and TC-P6-E4037-CON-07 to tab Story test cases under the same test case IDs. |
| CDC-11396 | RWB-P6-E4037-CON | CG-ALL-6698 | 16 | Add rows for TC-E4-037-01 to TC-E4-037-04 and TC-P6-E4037-CON-01 to TC-P6-E4037-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-11405 | RWB-P6-E4038-APP | CG-ALL-6708 | 16 | Add rows TC-E4-038-01 to TC-E4-038-04 with Given, When and Then copied from the criteria they cover. |
| CDC-11425 | RWB-P6-E4038-CON | DOR-RWB-P6-E4038-CON-12 | 16 | Add rows for TC-E4-038-01 to TC-E4-038-04 and TC-P6-E4038-CON-01 to TC-P6-E4038-CON-08 under the same IDs in the Story test cases tab. |
| CDC-11428 | RWB-P6-E4038-CON | CG-ALL-6719 | 16 | Add tab Story test cases rows for TC-E4-038-01 to -04 and TC-P6-E4038-CON-01 to -06 with Given, When and Then copied from the covered criterion. |
| CDC-11435 | RWB-P6-E4039-APP | CG-ALL-6728 | 16 | Add rows TC-E4-039-01 to TC-E4-039-04 with Given, When and Then copied from the criteria they cover (AC1, AC2, Access, Principle 5) |
| CDC-11445 | RWB-P6-E4039-CON | DOR-RWB-P6-E4039-CON-12 | 12.7, 16 | Add TC-E4-039-01 to TC-E4-039-04, TC-P6-E4039-CON-01 to TC-P6-E4039-CON-07 under tab Story test cases with their Given, When and Then. |
| CDC-11448 | RWB-P6-E4039-CON | CG-ALL-6737 | 16 | Add rows for TC-E4-039-01 to TC-E4-039-04 and TC-P6-E4039-CON-01 to TC-P6-E4039-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-11458 | RWB-P6-E4040-APP | CG-ALL-6746 | 16 | Add rows for TC-E4-040-01 to TC-E4-040-04 to tab Story test cases, with Given, When and Then copied from the criteria and data they cover. |
| CDC-11469 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-12 | 16 | Add the story test cases TC-E4-040-01 to -04 and TC-P6-E4040-CON-01 to -08 to tab Story test cases. |
| CDC-11473 | RWB-P6-E4040-CON | CG-ALL-6756 | 16 | Add rows on tab Story test cases for TC-E4-040-01 to TC-E4-040-04 and TC-P6-E4040-CON-01 to TC-P6-E4040-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-11480 | RWB-P6-E4041-APP | CG-ALL-6769 | 16 | Add rows TC-E4-041-01 to TC-E4-041-04 to tab Story test cases, with Given, When and Then copied from the criteria they cover. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11283 | RWB-P6-E2042-APP | DOR-RWB-P6-E2042-APP-7 | 11 | Confirm DF-REF-274 to DF-REF-299 are all rule_package fields and DF-DEC-001 to DF-DEC-031 all decision_log_entry fields; replace legacy job and decision-log wording in criteria and tests. |
| CDC-11317 | RWB-P6-E4035-APP | CG-ALL-6634 | 4, 12.1 | Record the field viewed_at of notice_view in LDM v9 Fields, or name its dictionary equivalent; nearest names moved_at, filed_at, ended_at are not the same field. |
| CDC-11318 | RWB-P6-E4035-APP | CG-ALL-6635 | 4, 9, 11, 13 | Record the table notice_view (rwb_comms, P6) in LDM v9 Fields, or name its dictionary table, as created by migration V4035_1. |
| CDC-11322 | RWB-P6-E4035-APP | DOR-RWB-P6-E4035-APP-7 | 11 | Add entity notice_view (rwb_comms, P6) with fields id, notice_id, case_id, channel, viewed_at, session_ref; add field viewed_at; confirm treatment_plan is an S2 rwb-treatment entity. |
| CDC-11348 | RWB-P6-E4036-APP | CG-ALL-6657 | 4, 12.7 | Add notice_response (table of rwb_comms, P6, created by V4036_1__notice_response.sql) to LDM v9 Fields, or give the dictionary name the story should use. |
| CDC-11349 | RWB-P6-E4036-APP | CG-ALL-6658 | 3, 11 | Add party_id as a field of notice (rwb_comms, P6) to LDM v9 Fields, or give the dictionary name the story should use in its place. |
| CDC-11364 | RWB-P6-E4036-CON | CG-ALL-6669 | none | Record notice_response as a new table of rwb_comms owned by RWB-P6-E4036-CON, with id, notice_id, case_id, response_code, channel, responded_at, decision_record_id. |
| CDC-11365 | RWB-P6-E4036-CON | CG-ALL-6670 | none | Record party_id as the identifier column of notice in rwb_comms, referring to the party of P1 without a cross-schema foreign key. |
| CDC-11366 | RWB-P6-E4036-CON | CG-ALL-6671 | none | Record decision_record as the platform library object created in rwb_comms by the decision-record library (DP-03). |
| CDC-11367 | RWB-P6-E4036-CON | CG-ALL-6672 | find it | Record `notice_id` as the physical column of notice_response (DF-LEG-015) or map it to its dictionary name in Fields. |
| CDC-11370 | RWB-P6-E4036-CON | DOR-RWB-P6-E4036-CON-7 | 11 | Map or add Fields for notice_response, notice_id, party_id and decision_record, which are in neither LDM v9 nor Data Classification v5. |
| CDC-11392 | RWB-P6-E4037-CON | CG-ALL-6693 | 11 | Record payment_intent as a P6 object of the rwb_comms schema (one row per POST, indexes ix_payment_intent_notice_id and ix_payment_intent_case_id) as declared in the story |
| CDC-11393 | RWB-P6-E4037-CON | CG-ALL-6694 | 11 | Record decision_record as a platform library object applied in rwb_comms by the decision-record library migration (DP-03) |
| CDC-11402 | RWB-P6-E4038-APP | CG-ALL-6702 | 11 | Record notice_dispute as a new P6 table of rwb_comms in LDM v9 Fields, or use its dictionary name. |
| CDC-11403 | RWB-P6-E4038-APP | CG-ALL-6703 | 3, 11 | Record notice.party_id as a field of the notice entity, or name the dictionary field that holds the party of the notice (nearest names partner_id, party_ext, party_role). |
| CDC-11446 | RWB-P6-E4039-CON | DOR-RWB-P6-E4039-CON-7 | 11 | Add decision_record as an entity or confirm the name of the rwb_comms library object it refers to. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11263 | RWB-P6-E2026-APP | DOR-RWB-P6-E2026-APP-1 | 1 | Confirm RW-RESTRUCT restructuring officer (FCR) is listed as a role code or name |
| CDC-11269 | RWB-P6-E2026-APP | GAP-0939 | find it | Add SY-CASEWF role row with role_class NON_HUMAN_ACTOR, DOCUMENTS C and default_scope ALL; record it in the reference data load with its own approver. |
| CDC-11320 | RWB-P6-E4035-APP | DOR-RWB-P6-E4035-APP-1 | 1 | Add a role code or name for customer (borrower), or confirm it as an external actor outside the role list. |
| CDC-11326 | RWB-P6-E4035-APP | GAP-1134 | 12.1 | §12.1 states the Litigation R and C rights as inherited from the legacy notice endpoints and records that no source declares the offer-view right; gateway-bff customer identity; web maps to PORTAL. |
| CDC-11334 | RWB-P6-E4035-CON | DOR-RWB-P6-E4035-CON-1 | 1 | Add the role contract owner of rwb-comms (P6) as a role code or role name, or confirm the code this story should use. |
| CDC-11351 | RWB-P6-E4036-APP | DOR-RWB-P6-E4036-APP-1 | 1 | Add 'customer (borrower)' as a role name, the actor of section 1 named in FSD P6 A2.15.3.3. |
| CDC-11368 | RWB-P6-E4036-CON | DOR-RWB-P6-E4036-CON-1 | 1 | Add 'contract owner of rwb-comms (P6)' as a role name, or give the role code used in section 1. |
| CDC-11382 | RWB-P6-E4037-APP | DOR-RWB-P6-E4037-APP-1 | 1 | Add a role code or role name for customer (borrower), or confirm the existing role it maps to. |
| CDC-11406 | RWB-P6-E4038-APP | DOR-RWB-P6-E4038-APP-1 | 1 | Add a role code or role name for the customer (borrower) on LINE OA or HOME.SCB, or name the role the actor maps to. |
| CDC-11423 | RWB-P6-E4038-CON | DOR-RWB-P6-E4038-CON-1 | 1 | Add 'contract owner of rwb-comms (P6)' as a role name, or confirm its existing equivalent; section 1 of RWB-P6-E4038-CON uses it as written. |
| CDC-11443 | RWB-P6-E4039-CON | DOR-RWB-P6-E4039-CON-1 | n/a | Add role contract owner of rwb-comms (P6), or name the existing role code that holds it |
| CDC-11466 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-1 | 1 | Add a role for the contract owner of rwb-comms (P6), or map section 1 to an existing role name in that document. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11336 | RWB-P6-E4035-CON | DOR-RWB-P6-E4035-CON-7 | 11 | Add entries for notice_view and decision_record, or record them as service-owned library objects. BR Field IDs for section 11 rows are not in the source documents. |
| CDC-11353 | RWB-P6-E4036-APP | DOR-RWB-P6-E4036-APP-7 | 11 | Add entity notice_response (new table in rwb_comms, P6) and field party_id of notice to LDM v9 and Data Classification v5. |
| CDC-11379 | RWB-P6-E4037-APP | CG-ALL-6681 | 12.7 | Add the payment_intent entity as a new object of RWB-P6-E4037-APP (rwb_comms, P6) with its fields, or record it in the owning document. |
| CDC-11384 | RWB-P6-E4037-APP | DOR-RWB-P6-E4037-APP-7 | 11 | Add the payment_intent entity of rwb_comms with its fields to LDM v9 and register it in Data Classification v5. |
| CDC-11395 | RWB-P6-E4037-CON | DOR-RWB-P6-E4037-CON-7 | 11 | Declare payment_intent (rwb_comms row of this story, section 11) and decision_record (platform library object) as entities or fields. |
| CDC-11408 | RWB-P6-E4038-APP | DOR-RWB-P6-E4038-APP-7 | 11 | Add entity notice_dispute of rwb_comms and field party_id of notice (DF-LEG-030) so both resolve in LDM v9 and Data Classification v5 |
| CDC-11420 | RWB-P6-E4038-CON | CG-ALL-6713 | 11 | Add notice_dispute as an entity, or record it as the new rwb_comms table declared by RWB-P6-E4038-CON |
| CDC-11421 | RWB-P6-E4038-CON | CG-ALL-6714 | 9 | Confirm the dictionary name for DF-LEG-030 or record party_id as the notice party identifier |
| CDC-11422 | RWB-P6-E4038-CON | CG-ALL-6715 | 9 | Record decision_record as the platform decision-record library table applied in rwb_comms (DP-03), or confirm a dictionary name |
| CDC-11426 | RWB-P6-E4038-CON | DOR-RWB-P6-E4038-CON-7 | 11 | Add the entity notice_dispute and the names party_id and decision_record, or confirm them as P6 contract names; the BR Field IDs are placeholders in section 11. |
| CDC-11471 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-7 | 11 | Assign BR Field IDs to the 14 rows of section 11 and add decision_record as a library object of rwb_comms. |
| CDC-11481 | RWB-P6-E4041-APP | DOR-RWB-P6-E4041-APP-7 | 11 | Register document_request and document_request_entry in rwb_comms and field notice_id, or confirm they remain objects owned by RWB-P6-E4041-APP. |

### Epic design record (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11260 | RWB-P6-E2026-APP | DOR-RWB-P6-E2026-APP-14 |  | Confirm the signed epic design sign-off for EP02 and record it in the epic design record |
| CDC-11375 | RWB-P6-E4037-APP | DOR-RWB-P6-E4037-APP-14 | none | Record the signed epic design sign-off for RWB-P6-E4037-APP. |
| CDC-11399 | RWB-P6-E4038-APP | DOR-RWB-P6-E4038-APP-14 | header | Record the signed epic design sign-off for the epic of this story. |
| CDC-11418 | RWB-P6-E4038-CON | DOR-RWB-P6-E4038-CON-14 | Definition of Ready | Record the signed epic design sign-off for RWB-P6-E4038-CON |
| CDC-11431 | RWB-P6-E4039-APP | DOR-RWB-P6-E4039-APP-14 |  | Record the signed epic design sign-off for RWB-P6-E4039-APP in the epic design record. |
| CDC-11440 | RWB-P6-E4039-CON | DOR-RWB-P6-E4039-CON-14 | n/a | Record the signed epic design sign-off for RWB-P6-E4039-CON |
| CDC-11452 | RWB-P6-E4040-APP | DOR-RWB-P6-E4040-APP-14 |  | Record the signed epic design sign-off for EP04. |
| CDC-11476 | RWB-P6-E4041-APP | DOR-RWB-P6-E4041-APP-14 | find it | Record the signed epic design sign-off for RWB-P6-E4041-APP; no signed epic design is in the story or source documents. |

### RWB-P6-E4040-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11453 | RWB-P6-E4040-APP | DOR-RWB-P6-E4040-APP-21 |  | Set build status to Done with the contract published. |
| CDC-11454 | RWB-P6-E4040-APP | DOR-RWB-P6-E4040-APP-22 |  | Publish a fake library version of the contract and record it. |
| CDC-11455 | RWB-P6-E4040-APP | DOR-RWB-P6-E4040-APP-23 | 12.1 | Record the contract version the two custody operations are fixed at, so this story can name it in 12.1. |
| CDC-11459 | RWB-P6-E4040-APP | GAP-1157 | 18 | Fix two operations under /api/recovery/comms/v1: POST and GET /notices/{noticeId}/custody-movements, with Documents right C and R and scope applied, the platform error set, and placeholder message IDs. |
| CDC-11463 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-14 | header | Record the signed epic design sign-off for EP04 in the epic design record. |
| CDC-11467 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-10 | 14 | Declare the empty, loading, error and no access states of SCR-33 in its screen specification. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11280 | RWB-P6-E2042-APP | CG-ALL-6622 | 4, 14 | Add a new message ID for a downstream read unavailable beyond the retry or no version in force, with text 'The service is unavailable. Try again later.'; this story then cites it. |
| CDC-11281 | RWB-P6-E2042-APP | CG-ALL-6623 | 4, 14 | Add a new message ID for 'A rule row is incomplete at the catalog read'; MSG-P3-027 text is copied from the standard where its use matches. |
| CDC-11300 | RWB-P6-E2042-APP | GAP-2399 | 4 | Step 3 refusal message marked Not specified (GAP-2399); MSG-GEN-006 removed |
| CDC-11380 | RWB-P6-E4037-APP | CG-ALL-6684 | 12.1 | Add a message ID for 401 no session and one for 404 notice absent or case outside scope (404 must not name the case). BA to confirm. Story keeps placeholders. |
| CDC-11404 | RWB-P6-E4038-APP | CG-ALL-6706 | 12.1 | Add message IDs for 401 no session, for 404 where the notice is absent or the data contract does not return the party, and for 409 where the notice is not sent or a dispute is already open. MSG-P4-003 fits only the out-of-scope 404. |

### RWB-P6-E4035-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11313 | RWB-P6-E4035-APP | DOR-RWB-P6-E4035-APP-21 | find it | Set its build status from Not started to Done once the contract is published. |
| CDC-11314 | RWB-P6-E4035-APP | DOR-RWB-P6-E4035-APP-22 | find it | Record the published contract fake library version in its build record. |
| CDC-11323 | RWB-P6-E4035-APP | GAP-1130 | 4 | Add rows for GET /notices/{noticeId}/channel-view and POST /notices/{noticeId}/views on /api/recovery/comms/v1, marked new. |
| CDC-11328 | RWB-P6-E4035-APP | GAP-2366 | 3 | Close the OfferView field list with the channel owners and data steward, limited to identifiers, codes, dates and one claim-check reference; confirm consent-proof contact-point fields with the rwb-source-data owner. |
| CDC-11329 | RWB-P6-E4035-APP | GAP-2367 | 3 | Declare and confirm the capability area and right of the two offer-view operations with the rwb-access owner at baseline review; add customer-channel screens and masking to RWB-PLT-N001-CON. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11321 | RWB-P6-E4035-APP | DOR-RWB-P6-E4035-APP-11 | 11 | Reconcile the personal-data class of the P2 fields the detcheck names with the guardrail that this story carries no personal data field; the field names are not in the item. |
| CDC-11352 | RWB-P6-E4036-APP | DOR-RWB-P6-E4036-APP-11 | 11, 12.1 | Confirm the class of the fields this story reads or writes (notice_response; notice party_id and case_id) against the statement that none is personal data. |
| CDC-11424 | RWB-P6-E4038-CON | DOR-RWB-P6-E4038-CON-11 | 11 | Confirm the classification of the P2 fields the detcheck names; if any is personal data, correct the 'Personal data: None' statement in section 11 of RWB-P6-E4038-CON. |
| CDC-11444 | RWB-P6-E4039-CON | DOR-RWB-P6-E4039-CON-11 | 11 | Confirm the class of the party reference and the contact key, which this contract carries only as identifiers; the story states no personal data. |
| CDC-11468 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-11 | 11 | Confirm or reclassify each P2 field carried by section 11 that Data Classification v5 classes as personal data; the story declares none. |

### RWB-P6-E4036-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11354 | RWB-P6-E4036-APP | GAP-1106 | find it | Declare POST and GET /notices/{noticeId}/responses under /api/recovery/comms/v1 with Idempotency-Key on POST and statuses 401, 403, 404, 409, 422, 503. |
| CDC-11355 | RWB-P6-E4036-APP | GAP-1107 | find it | Declare notice_response with id, notice_id, case_id, response_code, channel, responded_at, decision_record_id and standard columns; fix names, types and required flags. |
| CDC-11356 | RWB-P6-E4036-APP | GAP-1108 | find it | Declare capability area Litigation with right C on POST and right R on GET, scope applied, enforced at gateway-bff; role lists stay rwb-access data. |
| CDC-11357 | RWB-P6-E4036-APP | GAP-1109 | find it | Declare treatment, case and contact-point shapes and events TreatmentApproved and CaseStateChanged as consumed and faked; paths as placeholders; add C rows when owners plan contracts. |
| CDC-11358 | RWB-P6-E4036-APP | GAP-2369 | find it | Fix POST and GET /cases/{caseId}/offer-acceptances with capability area Case record (right C POST, right R GET); declare consumed rows; no acceptance event; fix refusal texts. |

### RWB-P6-E4037-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11376 | RWB-P6-E4037-APP | DOR-RWB-P6-E4037-APP-21 | none | Move build status from Not started to Done, with the contract published. |
| CDC-11377 | RWB-P6-E4037-APP | DOR-RWB-P6-E4037-APP-22 | none | Publish the contract fake library and record its published version. |
| CDC-11385 | RWB-P6-E4037-APP | GAP-1125 | 12.1 | Declare POST and GET /notices/{noticeId}/payment-intents under /api/recovery/comms/v1 with Idempotency-Key on the POST and statuses 401, 403, 404, 409, 422 and 503. |
| CDC-11387 | RWB-P6-E4037-APP | GAP-1126 | 11 | Fix the names, types, widths and required flags of payment_intent (intent id, case_id, notice_id, target, channel, owner reference, owner state, requested_at, standard columns), DF field ids as placeholder. |
| CDC-11388 | RWB-P6-E4037-APP | GAP-1128 | 12.1 | Declare one customer-facing capability area (name Not specified in the source documents (GAP-1128)) with right C on the POST and right R on the GET; keep role lists in rwb-access; confirm with gateway-bff and ACE Common owners. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11264 | RWB-P6-E2026-APP | DOR-RWB-P6-E2026-APP-12 | 18 | Align test case lists for REQ-DCM-012 and REQ-OCC-002 with section 18 of this story |
| CDC-11272 | RWB-P6-E2026-APP | CG-ALL-6614 | 18 | Align REQ-DCM-012 to RWB-P6-E2026-APP section 18 (TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-16) and REQ-OCC-002 (TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11). |
| CDC-11287 | RWB-P6-E2042-APP | GAP-2503 | find it | Declare the nine consumed operations on per-service bases (one hop, 2 s timeout); name workflow matchPayments and its four activities; record in RTM that AC1, AC3, AC4 and AC5 have no story in this split. |
| CDC-11301 | RWB-P6-E2042-APP | CG-ALL-6627 | 18 | Align the REQ-CWC-013 and REQ-CWC-014 test lists with story section 18 in the next RTM version, removing other stories' test IDs that this story does not own. |

### RWB-P6-E4038-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11400 | RWB-P6-E4038-APP | DOR-RWB-P6-E4038-APP-21 | header | Publish the contract and set its build status to Done. |
| CDC-11409 | RWB-P6-E4038-APP | GAP-1112 | 11 | Publish the two operations, the DisputeRequest and Dispute schemas and the notice_dispute row on Day 1 with the section 11 placeholders; element detail to the data steward |
| CDC-11412 | RWB-P6-E4038-APP | GAP-2374 | 3 | Fix the two operations, the request and answer shapes and the notice_dispute table; confirm the deviation operation and customer authorisation at baseline review |
| CDC-11413 | RWB-P6-E4038-APP | GAP-2375 | 3 | Baseline the two operations, shapes and notice_dispute table as declared; rwb-deviation owner publishes deviation open and read; gateway-bff declares customer session and scope |

### RWB-P5-E2026-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11261 | RWB-P6-E2026-APP | DOR-RWB-P6-E2026-APP-21 | Header | CON dependency recorded in Contract dependencies. |
| CDC-11270 | RWB-P6-E2026-APP | GAP-1878 | find it | Add two nullable treatment columns (document reference and pinned template version) with index. Take the generation operation and its shapes from RWB-P5-E2026-CON. |
| CDC-11271 | RWB-P6-E2026-APP | GAP-2393 | find it | Add a rwb_comms table for the generation request key and request lock (name not specified in the source documents (GAP-2393)). Record the rwb-document create operation in the P6 API specification when RWB-P5-E2026-CON is written. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11276 | RWB-P6-E2042-APP | CG-ALL-6619 | 12.2 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= through the provider's CON story, or the story consumes a published operation. |
| CDC-11277 | RWB-P6-E2042-APP | CG-ALL-6620 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} through the provider's CON story, or the story consumes a published operation. |
| CDC-11279 | RWB-P6-E2042-APP | DOR-RWB-P6-E2042-APP-8 | 12.2 | Publish the rule-catalog and rule-models GET operations in rwb-decision.yaml. P2 NoticeDispatchWorkflow workflow ID form and start rule are not specified in the source documents. |

### RWB-P6-E4039-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11432 | RWB-P6-E4039-APP | DOR-RWB-P6-E4039-APP-21 | header | Reach build status Done (contract published) before RWB-P6-E4039-APP starts. |
| CDC-11433 | RWB-P6-E4039-APP | DOR-RWB-P6-E4039-APP-22 |  | Record the contract fake library version as published. |
| CDC-11437 | RWB-P6-E4039-APP | GAP-2380 | 11 | Hold the closed consent set GIVEN and WITHDRAWN as data with a version. The story side is set in section 11. |

### RWB-P6-E4041-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11477 | RWB-P6-E4041-APP | DOR-RWB-P6-E4041-APP-21 | header | Set build status to Done once the contract is published; it is Not started today. |
| CDC-11478 | RWB-P6-E4041-APP | DOR-RWB-P6-E4041-APP-22 | find it | Publish a contract fake library version for RWB-P6-E4041-CON and record it. |
| CDC-11483 | RWB-P6-E4041-APP | GAP-1152 | 3 | Publish POST /cases/{caseId}/document-requests and GET /document-requests/{requestId} under /api/recovery/comms/v1, the DocumentRequest and DocumentRequestAnswer shapes, the two tables and the record element; confirm field types, decision code and rule id. |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11267 | RWB-P6-E2026-APP | GAP-0938 |  | Add the request and answer schema of POST /api/recovery/access/v1/authorise to the API specification, TSD P4 appendix T-A and RWB-P4-E1037-CON; stub generation facts in RWB-P5-E2026-CON. |
| CDC-11285 | RWB-P6-E2042-APP | GAP-0966 | find it | Add rule-package action names, request and answer fields and a change decision code to the authorise contract; agree the code with the RWB-E1-039 access-log owner; stub both in the contract fake. |

### RWB-P2-E2035-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11293 | RWB-P6-E2042-APP | GAP-0667 | none | Serve the read from /api/recovery/integration/v1 (DP-13); fix contract names, operation names, Schedule values and message texts; correct the Ownership Map row. |
| CDC-11294 | RWB-P6-E2042-APP | GAP-0668 | none | Baseline the three operation names and nine consumed shapes; confirm element names with rwb-case, rwb-access and rwb-decision owners; record the read path ruling in the Ownership Map. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11306 | RWB-P6-E2042-APP | GAP-0969 | n/a | Add a key for the rwb-access authorise cache lifetime (DP-06); value not specified in the source documents (GAP-0969). |
| CDC-11470 | RWB-P6-E4040-CON | DOR-RWB-P6-E4040-CON-20 | 8 | BR9 names DP-06 and DP-07; the parameter name is replaced by a Not specified placeholder. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11262 | RWB-P6-E2026-APP | DOR-RWB-P6-E2026-APP-22 | 12.8 | Publish the contract fake library version and record it as published |

### RWB-P6-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11265 | RWB-P6-E2026-APP | GAP-1713 |  | Record once in the service contract the owner of each FEAT prerequisite: approval P7, case P3, documents P5, communications P6, valuation S1. |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11266 | RWB-P6-E2026-APP | GAP-1580 |  | Add a generation section in the next version carrying FR-P5-026 and AC-P5-019 from REQ-DCM-012, so the behaviour has one functional statement. |

### OTHER:PM-2026.12 policy pack load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11268 | RWB-P6-E2026-APP | GAP-0937 |  | Load Documents letters: C for RW-RESTRUCT, RW-CASEOWN and SY-CASEWF; R for RW-TEAMMGR; no row for RW-PHONECOL; confirm at policy pack review. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P5 API-P5-016; RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11273 | RWB-P6-E2026-APP | GAP-1024 | find it | Declare path POST /cases/{caseId}/generated-documents (slide 16 name is the loser, ASM-115). Fix the three resources as schema constraints (ASM-111). Publish the four provider interfaces and the decision record as typed contracts (ASM-112). Declare one event with five payload fields (ASM-113). |

### RWB-P6-E2026-CON; OTHER:TSD P6 T-A.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11274 | RWB-P6-E2026-APP | GAP-2394 | find it | Allocate the next API-P6-nnn ID at D1 and add the generated-documents operation to the P6 API specification with the gateway-bff route. |

### OTHER:Next story-set version (DP table and service baseline metadata) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11275 | RWB-P6-E2026-APP | GAP-1288 | Header | Metadata correction belongs to the next story-set version. Ready to start stays Day 1. No text edit in this story. |

### OTHER:RWB-P6 contract story (not in the set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11278 | RWB-P6-E2042-APP | DOR-RWB-P6-E2042-APP-21 | header | Contract dependencies keeps RWB-P3-E2042-CON only |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; OTHER:P2 and P3 story documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11284 | RWB-P6-E2042-APP | DOR-RWB-P6-E2042-APP-9 | 14 | Align P2 MSG-GEN-006 meaning, P2 MSG-P3-027 text and P3 MSG-P7-003 text to the standard; no change to this story's section 14. |

### OTHER:TSD P7; OTHER:TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11286 | RWB-P6-E2042-APP | GAP-1615 | find it | Re-issue TSD P7 with T3.1 entries for the four rule tables and operations in appendix T-A; remove them from TSD P3 and P4; set x-module P7 on the nine rule paths. |

### RWB-P2-E2007-APP; RWB-P2-E2007-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11288 | RWB-P6-E2042-APP | GAP-0657 | find it | Keep JOB-08 with rwb-integration and mark slide 44 owner row superseded; read ACE facts via rwb-source-data; fix six consumed paths in RWB-P2-E2007-CON; allocate rwb-integration login in RWB-PLT-DB. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11289 | RWB-P6-E2042-APP | GAP-1292 | find it | Keep PM-2026.12 from 2026-12-01 as the RWB-E2-027 value; record PMT-2026.12 from 2026-12-15 as the E2-042 value; reconcile into one label and date before SIT promotion. |

### OTHER:RWB-E2-027 (owner reconciliation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11290 | RWB-P6-E2042-APP | GAP-1297 | find it | Reconcile PM-2026.12 (2026-12-01) with PMT-2026.12 (2026-12-15) into one version row before SIT. This story carries PMT-2026.12 from 2026-12-15 as its legacy value. |

### OTHER:RWB-E2-027 build notes and service schemas (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11291 | RWB-P6-E2042-APP | GAP-3179 | find it | Drop the payment_match_rule table from every service schema; keep PAYMENT_MATCH as the only home of match rows, loaded through the rule package endpoints. |

### OTHER:RWB-E2-027 build notes and PAYMENT_MATCH scenario set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11292 | RWB-P6-E2042-APP | GAP-3180 | find it | Adopt the priority order EXACT, then PARTIAL, then WINDOW from the Drools design; carry it in the PAYMENT_MATCH scenario set; confirm with Credit Administration. |

### RWB-P2-E2035-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11295 | RWB-P6-E2042-APP | GAP-0669 | none | Fix the identity, secret reference and probe checks; create the next-action-check job row with its run book path; review runbook entries with the on-call rota. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11296 | RWB-P6-E2042-APP | GAP-2396 | 7 | Correct the P6 Comms to P7 Decision cell from T to E for rwb.decision.events.v1 in the next diagram issue. |

### OTHER:rwb-decision contract (P7 owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11297 | RWB-P6-E2042-APP | GAP-0722 | 4, 12 | Publish model and catalog resources with packageCode, versionLabel, checksum, valid-from, ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code and outputs. |

### OTHER:rwb-access permission matrix (P4) and rwb-decision contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11298 | RWB-P6-E2042-APP | GAP-0967 | none | Publish service-identity rows for the fourteen capability areas; record the area each package serves as a rwb-decision package attribute. |

### OTHER:TSD P7 v2 (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11299 | RWB-P6-E2042-APP | GAP-1301 | none | Add rule_package, rule_package_version, rule_row and rule_test_case to the P7 TSD at its next version; record the R-PREC reading as P7. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11302 | RWB-P6-E2042-APP | GAP-1620 |  | Record that the registry accepts an XLS decision table and a DMN 1.6 model as two package formats on one runtime, that a package version names its format, and that conversion is a version change with its own test evidence. |

### OTHER:rwb-decision version list; RWB-P3-E2042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11303 | RWB-P6-E2042-APP | GAP-1357 | 16 | TC-E2-042-02 reverted to PMT-2026.12 to match AC1 |

### RWB-P3-E2042-APP; RWB-P3-E2042-INF; RWB-P3-E2042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11304 | RWB-P6-E2042-APP | GAP-0723 |  | Set the rule-packages container to write-once with no deletion and reviewed audit retention per environment (Not specified in the source documents (GAP-0723)). Size the pod by a load test that caches 20 versions. Expose alert windows, replica counts and probe timings as reviewed values files. Confirm all three with the platform and audit owners before the wave 2 release. |

### OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11305 | RWB-P6-E2042-APP | GAP-0968 | n/a | Correct T3.1 and T6.1 so the four rule tables and registry operations belong to P7; keep P4 rows for rights and access log only. |

### RWB-P7-E2042-APP; OTHER:decision_log_entry decision_code) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11307 | RWB-P6-E2042-APP | GAP-1298 |  | Resolve decision_code from LOV-DECISION at run time through DP-07. Write no literal in the story or the code. Confirm the value with the LOV-DECISION owner before SIT. |

### RWB-P7-E2042-APP; OTHER:DP-02); OTHER:platform DB story that creates the login and grants (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11308 | RWB-P6-E2042-APP | GAP-1299 |  | Refer to the login only as 'the rwb-decision login (DP-02)'. Leave the login name to the platform DB story that creates the login and the grants. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11309 | RWB-P6-E2042-APP | GAP-1994 | n/a | Build payment_match_rule as the PAYMENT_MATCH package in rwb-decision; keep proceeds rows in rwb-payment. |

### OTHER:Temporal and Drools Design Text Extract v1 (slide 18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11310 | RWB-P6-E2042-APP | GAP-2026 | n/a | State that S2 rwb-treatment owns and evaluates PAYMENT_MATCH; P8 matchPayments asks S2 via its contract; recorded as assumption. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11315 | RWB-P6-E4035-APP | DOR-RWB-P6-E4035-APP-5 | 9 | Add WEB to the closed list LOV-CHANNEL, as the story's channel set requires. |

### OTHER:Split plan WP B-P6-02 (C list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11324 | RWB-P6-E4035-APP | GAP-1131 | 11 | §11 consumes both reads one hop with a timeout and breaker; the timeout is Not specified in the source documents (GAP-1131). C rows still pending. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11325 | RWB-P6-E4035-APP | GAP-1133 | 11 | Create notice_view in rwb_comms with id, notice_id, case_id, channel, viewed_at, session_ref; add table and field IDs at next version. |

### OTHER:Requirement list P6 (FEAT-COM-01) and split plan WP B-P6-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11327 | RWB-P6-E4035-APP | GAP-2364 | 11 | Add the FEAT-COM-01 requirement row with this story and its test; add the S2 and P1 contract stories to the C list when planned. |

### RWB-P6-E4035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11330 | RWB-P6-E4035-APP | GAP-2368 | 3 | When planned, add the S2 and P1 contract stories to the C list and the S8 event rows to the I list; keep the drift test as the guard until then. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11337 | RWB-P6-E4035-CON | GAP-1132 | 11 | State the once-per-notice rule for rwb.comms.NoticeDelivered.v1 when the catalogue is next versioned. |

### API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11338 | RWB-P6-E4035-CON | GAP-1130 | 12.1 | Add rows for GET /notices/{noticeId}/channel-view and POST /notices/{noticeId}/views on /api/recovery/comms/v1, marked new. |

### RWB-P6-E4035-APP; RWB-P6-E4035-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11339 | RWB-P6-E4035-CON | GAP-1131 | find it | Add the S2 rwb-treatment and P1 rwb-source-data contract rows to the C list when planned; name the data product code and offer fields when published. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7; OTHER:TSD P6 v2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11340 | RWB-P6-E4035-CON | GAP-1133 | find it | Create notice_view with id, notice_id, case_id, channel, viewed_at and session_ref; move DF-LEG-022 to DELIVERED and DF-LEG-021 to the view date; add the table and field IDs at the next version. |

### OTHER:TSD P6 v2 T6.1 and T3.2; OTHER:rwb-access (P4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11341 | RWB-P6-E4035-CON | GAP-1134 | find it | Add a customer role or channel service identity to rwb-access and map the web channel to PORTAL in LOV-CHANNEL at the next version. |

### OTHER:P6 requirements list (FEAT-COM-01 row) and the API file of this key (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11342 | RWB-P6-E4035-CON | GAP-2364 | find it | Add the FEAT-COM-01 requirement row with its story and test; record in the API file the surface each read is faked from; add the S2 and P1 contract stories to C when planned. |

### OTHER:FSD P6 v3; OTHER:A2.14 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11344 | RWB-P6-E4035-CON | GAP-1135 | find it | Give the feature a screen identifier and a field list in the next FSD version. |

### OTHER:rwb-comms OpenAPI document; OTHER:TSD P6 v2 T-A; 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11359 | RWB-P6-E4036-APP | GAP-2371 | find it | Publish the two operations and their closed sets in the rwb-comms OpenAPI document; declare the three consumed rows consumed and faked; carry the stage-to-decision mapping as a versioned configuration row; fix the two unnamed refusal texts |

### Epic design record; OTHER:not in the source set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11362 | RWB-P6-E4036-CON | DOR-RWB-P6-E4036-CON-14 |  | Provide the signed epic design sign-off for EP04 / RWB-SVC-P6 so DoR item 14 (Epic design, signed before build starts) can pass. No story text change. |

### OTHER:Epic 4 BRD (requirement owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11372 | RWB-P6-E4036-CON | GAP-2370 | header | Assign a requirement ID to FEAT-COM-02 in the P6 requirement list at the next revision |

### RWB-P6-E4037-CON; OTHER:rwb-payment contract (P8); OTHER:rwb-source-data contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11386 | RWB-P6-E4037-APP | GAP-1124 | 12.2, 12.8 | Declare as consumed and faked rows the payment-intent registration of rwb-payment and the consent and contact-stop read of rwb-source-data, one hop with a 2 s budget; add C rows when P8 and P1 publish. |

### OTHER:P3 rwb-case screen specification for SCR-33 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11407 | RWB-P6-E4038-APP | DOR-RWB-P6-E4038-APP-10 | find it | State the empty, loading, error and no-access states of SCR-33. |

### OTHER:TSD P6 v2 T6.1 rights matrix and the rwb-access contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11410 | RWB-P6-E4038-APP | GAP-1114 | 14 | Add the customer principal row with the edge's coarse permission; no role code is written in the story |

### RWB-P6-E4038-CON; OTHER:S8 rwb-deviation owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11411 | RWB-P6-E4038-APP | GAP-1116 | 12.4 | Fix the consumer element of DeviationRaised and DeviationCleared and the hold_reason carrier; S8 owner publishes payload and key before the app story is done |

### OTHER:TSD P6 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11414 | RWB-P6-E4038-APP | GAP-1115 | find it | Correct the T8 mapping of REQ-OCC-011 from FEAT-COM-01 to FEAT-COM-04 in the next TSD version. |

### OTHER:Reference data and message list owned by the configuration owner and the message-list owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11415 | RWB-P6-E4038-APP | GAP-1117 | find it | Publish the dispute reason-code list, dispute state list, decision code, rule id and refusal texts as reference data and message-list rows before the wave 3 readiness review. |

### OTHER:TSD P6 v2 T6.1 (rights matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11427 | RWB-P6-E4038-CON | GAP-1114 | 15 | Add a customer (borrower) principal row carried by gateway-bff's sign-in and coarse permission; no role code in the story. Story side done in section 15. |

### OTHER:Not specified in the source documents (GAP-1487) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11436 | RWB-P6-E4039-APP | GAP-1487 | none | Record the labelled sample and its size with the first NFR-017 measurement; publish later measurements against the same sample definition. |

### OTHER:PLT library objects (decision-record library) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11442 | RWB-P6-E4039-CON | CG-ALL-6733 | n/a | Record decision_record as an rwb_comms library table in the library object list; no LDM v9 field is added |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11447 | RWB-P6-E4039-CON | GAP-1118 | 11, 12.7 | Record the move of contact_point_ext and the consent state to rwb-source-data (DP-05) and the removal of P6 contact data from rwb_comms. |

### OTHER:03 Requirements and specifications/Recovery Workbench Non Functional Specification v4.md (NFR-017 source; OTHER:scratch copy seen under _work/msr/docs/B-REQ-SPEC-28) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11449 | RWB-P6-E4039-CON | GAP-1487 | 19 | Record the labelled classification sample and its size with the first measurement, and publish each later measurement against the same sample definition for NFR-017. |

### OTHER:Standard v4 section 4 (message IDs for 401 and the absent notice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11457 | RWB-P6-E4040-APP | CG-ALL-6744 | 4, 12.1 | MSG-P4-003 for out-of-scope 404 and MSG-P3-005 for 409 mapped in section 12.1; 401 and absent-notice placeholders stay open. |

### OTHER:P5 rwb-document custody contract (story not yet planned) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11460 | RWB-P6-E4040-APP | GAP-1156 | 3 | Add the C row of the custody contract and its fake to both stories when the P5 contract story is planned; section 3 already fixes P5 ownership. |

### OTHER:Not specified in the source documents (CG-ALL-6752) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11465 | RWB-P6-E4040-CON | CG-ALL-6752 | 11 | Record decision_record as a library object of the decision-record library (DP-03) in its owning document, or use the LDM name. |

### OTHER:TSD P5 v2 T3.1 (rwb-document owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11472 | RWB-P6-E4040-CON | GAP-1158 | 11 | Publish the types and the seventh element of document_custody; the story keeps the placeholders until then. |

### OTHER:RWB-P5 rwb-document API (/api/recovery/document/v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11482 | RWB-P6-E4041-APP | GAP-1151 | 3 | Publish one discovery operation with its request and answer, then add its C row to RWB-P6-E4041-APP. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_decision.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20605 | RWB-P6-E2042-APP | R-28865 |  | The decision_code runtime-lookup change belongs to story RWB-P7-E2042-APP, not this DDL. No LOV-DECISION value is in the sources, so none is written. Owner confirmation stays open before SIT. |

### 04 User stories/Recovery Workbench Technical Enabler Stories v8.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20609 | RWB-P6-E2042-APP | R-28866 |  | RWB-P6-E2042-APP and DP-02 login text are not in this document (no E2042 or DP-02 match). Belongs in the owning story file and the platform DB story. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0408 | The generation harness pack, the template fixtures and the PDF/A conformance check are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0421 | Rule package harness: repository, SIT environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0669 | rwb-integration next action deployment: the login and secret reference, the next-action-check run values, the alert thresholds and the runbook ownership are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner | Resolved (directive) |
| GAP-0721 | The rule package registry is declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0722 | The rule-model and rule-catalog read operations have no published field-level shape | P7 rwb-decision owner | Resolved (directive) |
| GAP-0723 | Blob immutability period, pod memory for 20 KieBases, alert windows and probe timings are not specified | SCB IT infrastructure with the DevOps team | Resolved (directive) |
| GAP-0937 | The Documents letters per role are not in the P4 RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0938 | The authorise request and answer for a document generation request are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0939 | The role row, class and scope of the SY-CASEWF service identity are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0967 | rwb-access rule-package authority: the scope of a running service identity inside rwb-access and the capability area each rule package serves are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0968 | rwb-access rule-package authority: TSD P4 v3 gives P4 the four rule tables, while Architecture v5 and the ownership ruling put the rule registry in P7 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0969 | rwb-access rule-package authority: the lifetime of a cached authorise answer, the refresh trigger of the cached permission data and the granularity of the access-log entry of a dry run are not specified | Solution architect | Resolved (directive) |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1024 | The generation contract baseline has no settled operation name, no published provider shapes and two consumed contracts outside the plan | Solution architect | Resolved (directive) |
| GAP-1106 | The two response operations of a notice are in no source inventory | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1107 | No source declares the row that holds the response of the customer to a notice | Data steward | Resolved (directive) |
| GAP-1108 | The capability area and the right of a customer-facing answer are not given | Solution architect | Resolved (directive) |
| GAP-1109 | The three consumed shapes and the two consumed events have no contract story on this key | Solution architect | Resolved (directive) |
| GAP-1110 | The decision code, the response-code list and the source of the rule version are not given | Business analyst | Resolved (directive) |
| GAP-1111 | The response surface and the refusals beyond the two module messages are not given | Business analyst | Resolved (directive) |
| GAP-1112 | RWB-P6-E4038: no dispute operation, request, answer or table exists in the P6 sources | Tech lead of rwb-comms at the contract baseline review | Resolved (directive) |
| GAP-1113 | RWB-P6-E4038: no published rwb-deviation operation raises X1 for a customer dispute, and TSD P6 T5.2 does not list S8 | Owner of rwb-deviation and the Tech lead of rwb-comms | Resolved (directive) |
| GAP-1114 | RWB-P6-E4038: the rights matrix has no customer row, so a self-service dispute has no declared principal | Platform route owner and the security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1115 | RWB-E4-038: the legacy screen, permission and endpoint rows describe notice administration, not a customer dispute, and TSD P6 T8 maps its requirement to another feature | Business analyst, P6, at the story review | Resolved (directive) |
| GAP-1116 | RWB-P6-E4038: the contact stop and its lift are named by two events whose payload, key and local projection are not specified | Owner of rwb-deviation with the Tech lead of rwb-comms | Resolved (directive) |
| GAP-1117 | RWB-P6-E4038: no source gives the dispute reason codes, the dispute state list, the decision code, the rule id or the refusal texts | Configuration owner and the owner of the message list | Resolved (directive) |
| GAP-1118 | contact_point_ext and the consent state are P1 extension tables while the legacy story and the FSD hold them as P6 data | Solution architect | Resolved (directive) |
| GAP-1119 | No source names a published operation of the rwb-source-data contract for the contact read or the consent write | Tech lead | Resolved (directive) |
| GAP-1120 | No operation and no screen of the contact repository exist in the P6 sources | Tech lead | Resolved (directive) |
| GAP-1122 | The legacy Litigation C and R rights cannot serve the primary role of the feature | Solution architect | Resolved (directive) |
| GAP-1123 | The composite contact key, the eight unnamed contact_point_ext fields and the local stop projection are not specified | Tech lead | Resolved (directive) |
| GAP-1124 | The registration of a payment intent and the contact read of this capability are in no source and have no contract story | Solution architect with the owner of rwb-payment | Resolved (directive) |
| GAP-1125 | No source names an operation or a screen for FEAT-COM-03: the endpoint inventory stops at API-P6-011 and the legacy story copies the two notice operations | Tech lead | Resolved (directive) |
| GAP-1126 | No source declares the row or the element set that holds a self-service payment intent | Data steward | Resolved (directive) |
| GAP-1127 | No source gives the value sets of a self-service payment: the eligible notice states, the targets, the owner state, the decision code and the rule id | Business analyst | Resolved (directive) |
| GAP-1128 | The role matrix of the module names no capability area and no right for a customer-facing self-service payment | Solution architect | Resolved (directive) |
| GAP-1129 | No source names the event that reports a completed payment and no source gives the refusal messages of a payment intent | Business analyst with the owner of the message list | Resolved (directive) |
| GAP-1130 | No operation in the P6 endpoint inventory serves an offer view on a digital channel | P6 service owner and solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1131 | The offer and the customer, contact point and consent are other services facts with no contract story to depend on | Integration architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1132 | No source states which event a digital view raises, and the proof-of-delivery element has two possible paths | P6 service owner and event owner | Resolved (directive) |
| GAP-1133 | No field of the notice carries the channel of a digital delivery or the fact of a view | Data steward and P6 service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1134 | No source declares the right of an offer view, a customer role, or a web channel value distinct from PORTAL | Access architect and P4 rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1135 | The legacy screen cannot show an offer and the feature has no screen identifier in the module | P6 business analyst and edge owner | Resolved (directive) |
| GAP-1151 | No published rwb-document operation for the discovery production, and no C row for the document contract this key reads | Solution architect | Resolved (directive) |
| GAP-1152 | No document-request operation, answer shape, decision code or rule id in any source | Tech lead | Resolved (directive) |
| GAP-1153 | Selector conflict: REQ-DCM-017 asks for a named population and the legacy story answers per case | Solution architect | Resolved (directive) |
| GAP-1154 | The legacy rows of RWB-E4-041 are carried over from notice generation | Business analyst | Resolved (directive) |
| GAP-1155 | The answer format and the protection of a produced document are not stated | Solution architect | Resolved (directive) |
| GAP-1156 | document_custody is a P6 module table in the legacy story and a P5 rwb-document table in the target, and the P5 custody contract has no C row and no contract story | solution architect with the P5 rwb-document owner | Resolved (directive) |
| GAP-1157 | No custody operation and no requirement exist for the custody movement in the P6 specification, so both operations, their rights and their message IDs are new | rwb-comms tech lead with the P6 module owner | Resolved (directive) |
| GAP-1158 | The movement field set of the rwb-comms answer is not specified: the seventh document_custody field, the field types and required flags, and the notice-side reference column | rwb-comms tech lead with the P5 rwb-document owner | Resolved (directive) |
| GAP-1159 | The decision code and the rule id of a custody movement are not stated in any source | P7 rwb-decision owner with the P6 module owner | Resolved (directive) |
| GAP-1160 | Whether a movement is allowed on a closed case, on a case under legal hold and in which notice states is not stated | P6 module owner with the P3 rwb-case owner | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1289 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Solution architect, with the platform team and the P7 rwb-decision owner | Resolved (directive) |
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
| GAP-1487 | Document classification accuracy has a target and no baseline | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1605 | The contact repository and the consent state are held in an extension table the source-data service owns | Solution architect | Resolved (directive) |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1878 | The treatment-side generation call, its two columns, the merge-field set and the generation event are not specified | Solution architect | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-1994 | payment_match_rule has no owner in the Ownership Map | Solution architect | Resolved (directive) |
| GAP-2026 | Owning service of the PAYMENT_MATCH package is not stated in one place | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2034 | The UNIVERSAL package has no single owning service | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2363 | The legacy screen, endpoints and rights of RWB-E4-035 serve an officer's notice screen, not a customer's offer view | Solution architect | Resolved (directive) |
| GAP-2364 | No offer-view operation exists in the P6 inventory and the plan declares no C row for the two reads the view needs | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2365 | The decision code of an offer view and the shape of the contact-stop picture are not stated by any source | Solution architect | Resolved (directive) |
| GAP-2366 | No source fixes which offer fields a customer channel is shown or which contact-point fields prove consent | Data steward | Resolved (directive) |
| GAP-2367 | No source gives the capability area or the right of an offer-view operation, and the legacy story names the Litigation rights of another surface | Solution architect | Resolved (directive) |
| GAP-2368 | The two contracts and the contact-stop events the view depends on carry no C row and no source shape in this key's plan | Solution architect | Resolved (directive) |
| GAP-2369 | The self-service acceptance has no named operation, no access right and no declared owner of its cross-service rows, and the legacy key carries a screen and a permission check of the module template | Tech lead of rwb-comms, with the rwb-case, rwb-source-data, rwb-deviation and gateway-bff owners and the access owner of rwb-access | Resolved (directive) |
| GAP-2370 | No requirement row covers FEAT-COM-02, so the acceptance has no requirement ID to trace to | Business analyst of P6, with the requirement owner of the Epic 4 BRD | Resolved (directive) |
| GAP-2371 | The contract baseline of the acceptance fixes two operations, one access right, one decision mapping and five error conditions for which no source gives a name, a type or a message | Tech lead of rwb-comms and solution architect, with the rwb-case, rwb-source-data, rwb-deviation, rwb-decision and gateway-bff owners | Resolved (directive) |
| GAP-2372 | Self-service payment of RWB-E4-037 has no operation, resource, right, owner path, state set, message or event name in the sources | Solution architect | Resolved (directive) |
| GAP-2373 | Contract baseline of the self-service payment surface cannot state its right, its owner paths, its state set or its consumed event name from any source | Solution architect | Resolved (directive) |
| GAP-2374 | RWB-P6-E4038-APP: no dispute operation, dispute table, deviation operation or customer principal is specified for rwb-comms | Tech lead, with the rwb-deviation owner and the platform route owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2375 | RWB-P6-E4038-CON: the dispute contract baseline rests on an unspecified operation, table and deviation row, and the legacy rows of the key are a conflict | Tech lead, with the solution architect for the Ownership Map rows | Resolved (directive) |
| GAP-2376 | No source names a contact-repository operation, its path, its body or its status codes | Tech lead | Resolved (directive) |
| GAP-2377 | The legacy data table gives contact_point_ext to the P6 module while the Ownership Map gives it to P1 rwb-source-data | Solution architect | Resolved (directive) |
| GAP-2378 | The rwb-source-data contact operations have no published path, body or status code and no C row in this key's plan | Solution architect | Resolved (directive) |
| GAP-2379 | No source names a screen for the contact repository and the legacy screen is the template screen | Business analyst | Resolved (directive) |
| GAP-2380 | The module specification states no consent-state list and no consent-evidence rule, and the catalogue holds no contact event | Business analyst | Resolved (directive) |
| GAP-2381 | The legacy story declares Litigation C and R while the module matrix gives the primary role Documents RU | Solution architect | Resolved (directive) |
| GAP-2382 | RWB-P6-E4040-CON: no custody operation, custody table, field types, notice column, decision code or rule id is specified for rwb-comms | Tech lead of rwb-comms, with the rwb-document owner, the decision-library owner and the solution architect for the Ownership Map rows | Resolved (directive) |
| GAP-2393 | rwb-comms generation request key and P5 document-create operation are not specified | Service owner, rwb-comms; service owner, rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2394 | Generated-documents endpoint is not in the P6 operation inventory | Architecture owner; service owner, rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2396 | Architecture v5 slide 13 gives P6 to P7 a Temporal cell and no event cell, while RWB-P6-E1073-APP consumes RulePackageInForce from rwb.decision.events.v1 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2397 | No source states where the package version and checksum of a notice decision are stored, and the legacy story adds no column for them | Data steward | Resolved (directive) |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2399 | No source states the state a notice rests in, or the message, when no package version is in force | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2400 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Business analyst | Resolved (directive) |
| GAP-2406 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Business analyst, P7 | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P6-E2026-APP | new AC without TC row | 416 | AC16 is new and no section 16 row covers it |
| RWB-P6-E2042-APP | date added | 1 | 2026-12-01 |
| RWB-P6-E4035-APP | new AC without TC row | 424 | AC3 is new and no section 16 row covers it |
| RWB-P6-E4035-APP | new AC without TC row | 424 | AC4 is new and no section 16 row covers it |
