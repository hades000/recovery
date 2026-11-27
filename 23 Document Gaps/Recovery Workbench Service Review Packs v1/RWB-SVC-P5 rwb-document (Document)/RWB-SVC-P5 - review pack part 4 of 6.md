# RWB-SVC-P5 rwb-document (Document) - review pack, part 4 of 6 (RWB-P5-E1050-OPS to RWB-P5-E1057-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 155 |
| Cross-document (pending in another document) | 212 |
| Not applied (value not in the sources) | 16 |
| Open business decisions | 33 |
| Register gaps linked | 93 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P5-E1050-OPS | 15 | 21 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1050 OPS Document classification - deployment v2.md |
| RWB-P5-E1052-APP | 21 | 32 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1052 APP Notice generation v1 v2.md |
| RWB-P5-E1053-APP | 19 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1053 APP Field extraction for the six types into the index v2.md |
| RWB-P5-E1053-CON | 6 | 24 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1053 CON Field extraction for the six types into the index - contract v2.md |
| RWB-P5-E1054-APP | 18 | 30 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1054 APP Review queue for low-confidence documents v2.md |
| RWB-P5-E1054-CON | 17 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1054 CON Review queue for low-confidence documents - contract v2.md |
| RWB-P5-E1055-APP | 23 | 35 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1055 APP Proof of delivery capture design with WIN v2.md |
| RWB-P5-E1057-APP | 22 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1057 APP Intake from branches, mailroom, partner SFTP and email v2.md |
| RWB-P5-E1057-CON | 14 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1057 CON Intake from branches, mailroom, partner SFTP and email - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P5-E1053-APP | R-01529 | CG-ALL-5982 | Script gap | Product owner | The story adds EXTRACT_MAX_ATTEMPTS to the closed list LOV-INTAKE-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1053-APP | R-01530 | CG-ALL-5983 | Script gap | Product owner | The story adds EXTRACT_TIMEOUT_SECONDS to the closed list LOV-INTAKE-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1053-CON | R-01531 | CG-ALL-5996 | Script gap | Product owner | The story adds EXTRACTION_FAILED to the closed list LOV-INTAKE-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1055-APP | R-01548 | CG-ALL-6041 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-DOC-SOURCE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1055-APP | R-01549 | CG-ALL-6042 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-DOC-SOURCE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1055-APP | R-01550 | CG-ALL-6043 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-SCAN-RESULT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1055-APP | R-01551 | CG-ALL-6044 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-SCAN-RESULT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E1025-ITG, RWB-P5-E1025-APP, RWB-P5-E1053-APP, RWB-P5-E1053-CON | R-09182 | GAP-1585 | Register gap | Business lead with Legal counsel and the Head of NPA | The six document types are counted at 26 fields but only two types name their fields | FR-P5-011 and FR-P5-016 require the full field list to be delivered as the signed reference load and this PRD requires the count to reconcile, not a specific list. OQ-P5-01 and OQ-P5-14 carry the question. |
| RWB-ITG-E1049-ITG, RWB-ITG-E1050-ITG, RWB-P3-E1050-APP, RWB-P5-E1049-APP, RWB-P5-E1049-CON, RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1053-CON, RWB-P6-E1049-APP | R-09185 | GAP-1586 | Register gap | Solution architect with the AI product owner | The OCR, classification and extraction services are named as external pieces but no source names them or their owner | The PRD keeps the pipeline behaviour in P5 and states the OCR, classification and extraction engines as an external contract reached as an AgentRunCompleted event or a Temporal child run, with the provider, the contract and the version scheme carried as OQ-P5-06. |
| RWB-P5-E1050-OPS | R-10890 | CG-ALL-5967 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1052-APP | R-10895 | CG-ALL-5976 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1053-APP | R-10903 | CG-ALL-5991 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1053-CON | R-10907 | CG-ALL-6005 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1054-APP | R-10911 | CG-ALL-6024 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1054-APP | R-10912 | CG-ALL-6029 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-P5-E1054-CON | R-10915 | CG-ALL-6037 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1055-APP | R-10919 | CG-ALL-6055 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1025-APP, RWB-P5-E1052-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-22159 | GAP-2347 | Register gap | Data steward and document type owner, with the Legal counsel and the P5 TechX squad | The notice-type to document-type mapping, the retention class and the write-once flag of each notice document type are not specified in any source read here | The document type load of RWB-P5-E1025-APP carries the DEMAND_LETTER and GUARANTOR_NOTICE rows with their class and flag, and the notice-type mapping row is added to the type or mapping table before the wave-1 test data is loaded |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-22191 | GAP-2245 | Register gap | Legal and the business lead | Whether a deviation pauses a statutory notice period is not settled by the sources | Keep the notice period unpaused as ASM-B2-P3-016-3 records; if Legal rules that it pauses, the deviation contract gains one signal to the notice clock and one criterion changes. |
| RWB-ITG-E1057-ITG, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-P5-E1057-APP, RWB-P5-E1057-CON, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-S9-E1057-APP | R-22197 | GAP-3146 | Register gap | Business lead; solution architect; rwb-partner tech lead; rwb-access owner; programme lead | RWB-S9-E1057-APP: the split plan gives this secondary slice no legacy criterion and no build row while the P5 slice of the same key hands the partner criteria to it, no source publishes a partner-by-code read or the code filter of GET /partners, the two refusal reasons and the not-found behaviour are not published, the constraint on partner_code and the panel transition table are not specified, the DP-07 rows cannot be carried in an empty H row, and EP01 wave 1 is earlier than the service wave 4 | Serve the partner panel read as the code filter of the published GET /partners under base /api/recovery/partner/v1 with right R and the scope applied, answer the six published properties from partner in rwb_partner, answer an empty list for an unknown code and the stored panel status for a partner that is not ACTIVE, leave BR4 and the two reasons with the caller, read LOV-PANEL and LOV-PARTNER-TYPE through DP-07, write nothing and publish nothing, keep wave 1 and record the DP-07 rows, the constraint on the partner code, the panel transition table and the criteria assignment of the two slices as open items. |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1052-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-28611 | GAP-2088 | Register gap | Business lead with Legal and Compliance; document owner | DL10 is listed open with one answer and is recorded as answered with another | Keep the source row word for word, record in section 6.1 that DL10 is answered on 5 November 2026 with answer A, and add no Thai wording in this document. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-28627 | GAP-2248 | Register gap | Business lead | The role that receives the expiry of a notice period is not named | Take the escalation role from the SERVICE_LEVEL row in force as ASM-B2-P3-016-6 records, and add a named default role for a missing row if the business lead asks for one. |
| RWB-P5-E1054-APP | R-33451 | ASM-ALL-6029 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P5-E1052-APP | R-36988 | ASM-3902 | Register assumption |  | A notice type is mapped to one document type of LOV-DOC-TYPE by a data row in force, and the retention class and the write-once flag of the stored notice are read from that document_type row and never typed in code; the fixture of the story maps DEMAND to DEMAND_LETTER and GUARANTOR_NOTICE to GUARANTOR_NOTICE and asserts the read, not a class or a flag value. | The document type load of RWB-P5-E1025-APP publishes the two type rows with their class and flag, and the mapping row is published with them |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P5-E1050-OPS | R-06213 | DOR-RWB-P5-E1050-OPS-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-P5-E1050-OPS in the story or sources (22 Microservice Realignment). Sign-off is a business act and cannot be recorded here. |
| RWB-P5-E1050-OPS | R-31156 | NEWAC-RWB-P5-E1050-OPS-AC10 | 8 | AC10: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 and section 16 text is not in this chunk, so no AC or test row can be written. Proposed test Not specified in the source documents (NEWAC-RWB-P5-E1050-OPS-AC10). |
| RWB-P5-E1053-CON | R-17312 | DOR-RWB-P5-E1053-CON-18 | Open decisions (outside chunk) | Definition of Ready item 18 Open decisions: Partial | DL10 is an open business decision (Thai field names, option A recommended; owner business lead with Legal and Compliance). It stays open. Its section is not in this chunk, so no edit. |
| RWB-P5-E1053-CON | R-22600 | GAP-1021 | 5, 16 (not in chunk) | The published Java reader becomes a REST contract no source names, the extraction operations belong to another baseline of the same service, and the plan lists no C row for the case read | Reader path, resource names, status set and operation name appear in no source, so declaring them would invent values. Needs S4, S2 and review queue confirmation. Sections 5 and 16 not in chunk. |
| RWB-P5-E1053-CON | R-31165 | AC15: a status change the model does not allow is refused (no criterion covers a disallowed transition) | 7 | AC15: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Refusing a disallowed transition conflicts with BR12 (no state machine). Conflict left open; no criterion added. |
| RWB-P5-E1054-APP | R-17319 | DOR-RWB-P5-E1054-APP-17 | none | Definition of Ready item 17 Dependencies: Partial | The gating statement is not in the source documents; the dependency list is unchanged. |
| RWB-P5-E1054-APP | R-25831 | CG-ALL-6025 | 3 | Flyway file V1054_1__review_outcome.sql is not in the V0001..Vnnnn form | Next Vnnnn for rwb-document is not in the sources. Service Template and Rules v1 (DP-15, line 140) gives only the V0001 baseline. Line 478 text is outside this chunk. |
| RWB-P5-E1054-CON | R-06242 | DOR-RWB-P5-E1054-CON-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources; the item is not resolved by a placeholder. |
| RWB-P5-E1054-CON | R-06243 | DOR-RWB-P5-E1054-CON-16 | header | Definition of Ready item 16 Size: Fail | Size is not in the sources; the story does not resolve it. |
| RWB-P5-E1054-CON | R-17325 | DOR-RWB-P5-E1054-CON-10 |  | Definition of Ready item 10 Screens and states: Partial | Section text for SCR-30/31 states is not in this chunk, so no exact anchor. Sources give no empty, error or no-access wording; only Loading; list; reviewed (AD021 APP) found. |
| RWB-P5-E1055-APP | R-17335 | DOR-RWB-P5-E1055-APP-11 | 3 | Definition of Ready item 11 Guardrails: Partial | Flagged P2 field list is not in the chunk. Data Classification v5 rwb-document rows DF-DOC-001 to 033 exist, but none can be matched to the flagged fields. No personal-data class set. |
| RWB-P5-E1055-APP | R-25843 | CG-ALL-6056 | 3 | Flyway file V1024_1__document_store.sql is not in the V0001..Vnnnn form | V1024_1 name is not in the story text. Service Template v1 §3 and 05 Technical architecture give only the V0001 baseline rule, with no next number for rwb-document. Not specified in the source documents (CG-ALL-6056). |
| RWB-P5-E1057-APP | R-25849 | CG-ALL-6067 | 3 | Flyway file V1057_1__intake_channels.sql is not in the V0001..Vnnnn form | Next number of the rwb-document Flyway sequence is not in the sources; Service Template v1 §3.1 gives only V0001 to Vnnnn. Searched the story folder and the build notes. File name unchanged. |
| RWB-P5-E1057-APP | R-25850 | CG-ALL-6068 | 3 | Flyway file V1_5_057__intake_channels.sql is not in the V0001..Vnnnn form | Next number of the rwb-document Flyway sequence is not in the sources; Service Template v1 §3.1 gives only V0001 to Vnnnn. Searched the story folder and the build notes. File name unchanged. |
| RWB-P5-E1057-CON | R-06259 | DOR-RWB-P5-E1057-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story, the DOR review or the source search, so no sign-off reference can be written without inventing one. |
| RWB-P5-E1057-CON | R-31184 | NEWAC-RWB-P5-E1057-CON-AC17 | 7 | AC17: §8 BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 text is not in this chunk, so AC17 and its test row have no anchor. Proposed test is not specified in the source documents. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (26)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10028 | RWB-P5-E1053-CON | CG-ALL-6000 | 12.1 | Publish POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract with request ExtractionRequest and 200 FieldSet, or remove it. |
| CDC-10029 | RWB-P5-E1053-CON | CG-ALL-6001 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction with 200 FieldSet, or remove it. |
| CDC-10030 | RWB-P5-E1053-CON | CG-ALL-6002 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId}/fields with 200 FieldSet, or remove it. |
| CDC-10033 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-8 | 12.1 | Publish the three operations: POST intake-items/{intakeItemId}/extract, GET intake-items/{intakeItemId}/extraction, GET documents/{documentId}/fields. |
| CDC-10053 | RWB-P5-E1054-APP | CG-ALL-6010 | 12.1 | Publish GET /api/recovery/document/v1/review-items in paths through RWB-P5-E1054-CON. |
| CDC-10054 | RWB-P5-E1054-APP | CG-ALL-6011 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId} in paths through RWB-P5-E1054-CON. |
| CDC-10055 | RWB-P5-E1054-APP | CG-ALL-6012 | 12.1 | Publish GET /api/recovery/document/v1/intake-items/{intakeItemId}/content in paths through RWB-P5-E1054-CON. |
| CDC-10056 | RWB-P5-E1054-APP | CG-ALL-6013 | 12.1 | Publish POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve in paths through RWB-P5-E1054-CON. |
| CDC-10057 | RWB-P5-E1054-APP | CG-ALL-6014 | 12.1 | Publish PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} in paths through RWB-P5-E1054-CON. |
| CDC-10058 | RWB-P5-E1054-APP | CG-ALL-6015 | 12.1 | Publish POST /api/recovery/document/v1/documents/{documentId}/review in paths through RWB-P5-E1054-CON. |
| CDC-10059 | RWB-P5-E1054-APP | CG-ALL-6016 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId} in paths through RWB-P5-E1054-CON, owned by the document read of RWB-P5-E1024-APP. |
| CDC-10061 | RWB-P5-E1054-APP | CG-ALL-6018 | 3 | Remove the fixed enum on reviewStatus so LOV-REVIEW values are accepted as data without a schema change. |
| CDC-10065 | RWB-P5-E1054-APP | DOR-RWB-P5-E1054-APP-8 | 4 | Add an Idempotency-Key header to POST resolve, PATCH fields and POST review; add the paths the detcheck lists as missing from the yaml. |
| CDC-10100 | RWB-P5-E1055-APP | CG-ALL-6046 | 12.1 | Publish POST /api/recovery/document/v1/cases/{caseId}/documents in rwb-document.yaml through the CON story, or remove it from section 12.1 |
| CDC-10101 | RWB-P5-E1055-APP | CG-ALL-6047 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId} in rwb-document.yaml through the CON story, or remove it from section 12.1 |
| CDC-10102 | RWB-P5-E1055-APP | CG-ALL-6048 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId}/content in rwb-document.yaml through the CON story, or remove it from section 12.1 |
| CDC-10103 | RWB-P5-E1055-APP | CG-ALL-6049 | 12.1 | Publish POST /api/recovery/document/v1/documents/{documentId}/versions in rwb-document.yaml through the CON story, or remove it from section 12.1 |
| CDC-10104 | RWB-P5-E1055-APP | CG-ALL-6050 | Not specified in the source documents (CG-ALL-6050) | Remove the closed enum on action so that LOV-RETENTION-ACTION values are accepted as data without a schema change |
| CDC-10107 | RWB-P5-E1055-APP | DOR-RWB-P5-E1055-APP-8 | 4 | Add the four paths named in the detail (POST cases/{caseId}/documents, GET documents/{documentId}, GET documents/{documentId}/content, POST documents/{documentId}/versions) and the two further paths the check reports. |
| CDC-10135 | RWB-P5-E1057-APP | CG-ALL-6062 | 12.1 | Publish GET /api/recovery/document/v1/admin/jobs through RWB-P5-E1057-CON, matching the 12.1 row, or remove the row from both documents. |
| CDC-10136 | RWB-P5-E1057-APP | CG-ALL-6063 | 12.1 | Publish GET /api/recovery/document/v1/admin/jobs/{jobId} through RWB-P5-E1057-CON, matching the 12.1 row, or remove the row from both documents. |
| CDC-10137 | RWB-P5-E1057-APP | CG-ALL-6064 | 12.1 | Publish POST /api/recovery/document/v1/admin/jobs/{jobId}/rerun through RWB-P5-E1057-CON, matching the 12.1 row, or remove the row from both documents. |
| CDC-10140 | RWB-P5-E1057-APP | DOR-RWB-P5-E1057-APP-8 | 12.1 | None in this story; the rerun row already states Idempotency-Key required with the same key. |
| CDC-10152 | RWB-P5-E1057-CON | CG-ALL-6072 | 12.1 | Publish GET /api/recovery/document/v1/admin/jobs in rwb-document.yaml through the RWB-P5-E1057-CON contract baseline. |
| CDC-10153 | RWB-P5-E1057-CON | CG-ALL-6073 | 12.1 | Publish GET /api/recovery/document/v1/admin/jobs/{jobId} in rwb-document.yaml through the RWB-P5-E1057-CON contract baseline. |
| CDC-10154 | RWB-P5-E1057-CON | CG-ALL-6074 | 12.1 | Publish POST /api/recovery/document/v1/admin/jobs/{jobId}/rerun in rwb-document.yaml through the RWB-P5-E1057-CON contract baseline. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09974 | RWB-P5-E1050-OPS | CG-ALL-5966 | 18 | TC-E1-050-12 and TC-E1-050-13 added to section 18; RTM row to be matched in its next version. |
| CDC-09998 | RWB-P5-E1052-APP | CG-ALL-5975 | 18 | Align the REQ-OCC-001 test list in RTM v7 to section 18 (TC-E1-052-01, -02, -04, -06, -07, -12, -13); remove TC-E1-046-01 to -03 unless they trace REQ-OCC-001. |
| CDC-10020 | RWB-P5-E1053-APP | DOR-RWB-P5-E1053-APP-12 | 16 | Align the RWB-P5-E1053-APP test list with TC-E1-053-01 to TC-E1-053-18 of section 16 (section 18 now states this range); the contract test TC-E1-053-15 and boundary test TC-E1-053-16 are added. |
| CDC-10026 | RWB-P5-E1053-APP | CG-ALL-5990 | 18 | Align the test trace of REQ-DCM-006 and REQ-DCM-001 with section 18 of RWB-P5-E1053-APP in the next RTM version. |
| CDC-10040 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-12 | 12.7, 16, 18 | Align §18 test lists with RTM v7, which must include TC-E1-053-15. |
| CDC-10047 | RWB-P5-E1053-CON | CG-ALL-6004 |  | Align the REQ-DCM-006 and REQ-DCM-001 test lists with section 18 of RWB-P5-E1053-CON in the next RTM version. |
| CDC-10068 | RWB-P5-E1054-APP | DOR-RWB-P5-E1054-APP-12 | 12.7, 16, 18 | Align REQ-DCM-005 test list to TC-E1-054-01 to TC-E1-054-21 as stated in section 18. |
| CDC-10075 | RWB-P5-E1054-APP | CG-ALL-6023 | 18 | Align the REQ-DCM-005 test list with section 18 of RWB-P5-E1054-APP at the next RTM version. |
| CDC-10094 | RWB-P5-E1054-CON | CG-ALL-6036 | 18 | Align the REQ-DCM-005 test list in RTM v7 with section 18 of RWB-P5-E1054-CON in the next version. |
| CDC-10128 | RWB-P5-E1055-APP | CG-ALL-6054 | 18 | Align the REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006 test lists with section 18 at the next RTM version. |
| CDC-10150 | RWB-P5-E1057-APP | CG-ALL-6066 | 18 | Align REQ-DCM-009 and REQ-DCM-010 test lists with section 18 of this story, which follows section 16. |
| CDC-10166 | RWB-P5-E1057-CON | CG-ALL-6079 | 18 | Align the REQ-DCM-009 and REQ-DCM-010 test lists with section 18 of RWB-P5-E1057-CON in the RTM's next version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09967 | RWB-P5-E1050-OPS | GAP-0765 | 12.7 | Register rwb_case.case_document_link with its field IDs and the classification columns added in V1050_1 in the next data dictionary version; rwb-case writes no P5 table |
| CDC-10034 | RWB-P5-E1053-CON | CG-ALL-5997 | 9, 11 | Record review_only as a field of document_type.field_definitions (DF-REF-224), or confirm the dictionary name to use. |
| CDC-10035 | RWB-P5-E1053-CON | CG-ALL-5998 | 11, 12.2 | Record extraction_method as a field or library value of document_type.field_definitions (DF-REF-224), or confirm the dictionary name. |
| CDC-10052 | RWB-P5-E1054-APP | CG-ALL-6009 | 12.7 | Index column shown as Not specified in the source documents |
| CDC-10133 | RWB-P5-E1055-APP | GAP-1105 |  | Publish hold_reason as a versioned reference list with TEMPLATE_WITHDRAWN as first row; other values Not specified in the source documents (GAP-1105). |
| CDC-10143 | RWB-P5-E1057-APP | CG-ALL-6061 | 13 | Record uk_intake_channel_ref as the unique constraint on document_intake (channel_code, source_ref, file_sha256), or confirm the constraint object name in the dictionary. |
| CDC-10144 | RWB-P5-E1057-APP | DOR-RWB-P5-E1057-APP-7 | 11 | Record uk_intake_channel_ref as the unique constraint on document_intake (channel_code, source_ref, file_sha256), or confirm the constraint object name in the dictionary. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09982 | RWB-P5-E1052-APP | CG-ALL-5973 | 14 | Add a new message ID for 'The notice type has no document type in force'; the story then cites it in §4 and §14. |
| CDC-10066 | RWB-P5-E1054-APP | CG-ALL-6021 | 14 | Add a new message ID for 'No authenticated caller'; the story then cites it in the §14 MSG-P4-001 row in place of the current placeholder. |
| CDC-10067 | RWB-P5-E1054-APP | CG-ALL-6022 | 4, 14 | Add a new message ID for 'A consumed read failed or timed out' and hold MSG-GEN-006 for 'System of record unavailable (R-UNI-33)'; the story then cites the new ID in section 14. |
| CDC-10069 | RWB-P5-E1054-APP | DOR-RWB-P5-E1054-APP-9 | 14 | Align the meaning of MSG-P4-001 ('No authenticated caller') with the standard or add a new ID; the story then cites it. |
| CDC-10084 | RWB-P5-E1054-CON | CG-ALL-6032 | 14 | Add a new message ID for 'No authenticated caller' so the story can cite it instead of MSG-P4-001. |
| CDC-10085 | RWB-P5-E1054-CON | CG-ALL-6033 | 14 | Add a new message ID for 'A consumed read failed or timed out' so the story can cite it instead of MSG-GEN-006. |
| CDC-10158 | RWB-P5-E1057-CON | CG-ALL-6076 | 4, 14 | Add a message ID for 'No authenticated caller' with its text; the story then cites that ID in section 14 in place of MSG-P4-001. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09973 | RWB-P5-E1050-OPS | GAP-1007 |  | Add EXTRACTION_FAILED to LOV-INTAKE-REVIEW in the next approved list load; keep MODEL_UNAVAILABLE for the classification fallback; no code change |
| CDC-10014 | RWB-P5-E1053-APP | DOR-RWB-P5-E1053-APP-5 | 9 | Remove EXTRACT_MAX_ATTEMPTS and EXTRACT_TIMEOUT_SECONDS from the closed list; they are parameters, not review values. |
| CDC-10023 | RWB-P5-E1053-APP | GAP-1007 | find it | Add EXTRACTION_FAILED to LOV-INTAKE-REVIEW in the next approved list load; keep MODEL_UNAVAILABLE for the classification fallback; no code change. |
| CDC-10032 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-5 | 9 | Add EXTRACTION_FAILED to the closed list LOV-INTAKE-REVIEW by data load (GAP-1007; ASM-1799). |
| CDC-10043 | RWB-P5-E1053-CON | GAP-1007 |  | Add EXTRACTION_FAILED to LOV-INTAKE-REVIEW at the next approved list load; keep MODEL_UNAVAILABLE for the classification fallback; no code change. |
| CDC-10092 | RWB-P5-E1054-CON | GAP-2456 | 7 | Removed the four invented decision-record keys; LOV-DECISION reference kept |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09958 | RWB-P5-E1050-OPS | CG-ALL-5959 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} through RWB-P5-E1050-CON, or consume a published operation. |
| CDC-10060 | RWB-P5-E1054-APP | CG-ALL-6017 | 12.2 | Publish GET /api/recovery/case/v1/cases/by-no/{caseNo} in paths through the provider story RWB-P3-E1035-CON. |
| CDC-10082 | RWB-P5-E1054-CON | CG-ALL-6030 | 12.2 | Publish GET /api/recovery/case/v1/cases/by-no/{caseNo} in rwb-case.yaml, or the consumer switches to a published operation. |
| CDC-10083 | RWB-P5-E1054-CON | DOR-RWB-P5-E1054-CON-8 | 12.2 | Publish GET /api/recovery/case/v1/cases/by-no/{caseNo} in rwb-case.yaml (CG-ALL-6030). Topic check passes as is. |
| CDC-10155 | RWB-P5-E1057-CON | CG-ALL-6075 | 12.2 | Publish GET /api/recovery/case/v1/admin/parameters/{paramCode} in rwb-case.yaml through the provider's story RWB-P3-E1042-CON. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09965 | RWB-P5-E1050-OPS | DOR-RWB-P5-E1050-OPS-1 | 1 | Add the DevOps engineer role with its role code to Users Roles and Permissions v5, or name the section 1 role by its code there. |
| CDC-10037 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-1 | 1 | Add 'tech lead' as a role name, or record it as a persona outside the role list. |
| CDC-10086 | RWB-P5-E1054-CON | DOR-RWB-P5-E1054-CON-1 | 1 | Add or confirm a role code or name for the tech lead actor in section 1. |
| CDC-10109 | RWB-P5-E1055-APP | DOR-RWB-P5-E1055-APP-6 | 10 | Add role SY-DATALOAD for the receipt load of the partner file. |
| CDC-10159 | RWB-P5-E1057-CON | DOR-RWB-P5-E1057-CON-1 | 1 | Add the tech lead of rwb-document as a role code or role name. Code: Not specified in the source documents (DOR-RWB-P5-E1057-CON-1). |

### RWB-P10-TE013-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09966 | RWB-P5-E1050-OPS | GAP-1005 | none | Name the extractor provider, model name, model version and field-extraction route for extraction_method MODEL; keep the route a property of rwb-document with no model name in code. |
| CDC-10022 | RWB-P5-E1053-APP | GAP-1005 | 3 | Name the extractor provider, model, model version and field-extraction route; keep the route as a property of rwb-document with no model name in code. |
| CDC-10024 | RWB-P5-E1053-APP | GAP-1009 | find it | Add the field-extraction route with the typed answer of AC8 to RWB-P10-TE013-CON, and publish it with its WireMock stub and the drift test. |
| CDC-10042 | RWB-P5-E1053-CON | GAP-1005 |  | Name the extractor provider, model, model version and field-extraction route; keep the route a property of rwb-document with no model name in code. |
| CDC-10044 | RWB-P5-E1053-CON | GAP-1009 |  | Add the field-extraction route with the typed answer of AC8; publish its WireMock and drift test. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09979 | RWB-P5-E1052-APP | DOR-RWB-P5-E1052-APP-14 | Header | Record the signed epic design sign-off for EP01 so the story can cite it. |
| CDC-10011 | RWB-P5-E1053-APP | DOR-RWB-P5-E1053-APP-14 | n/a | Record the signed epic design sign-off for EP01 in the epic design record and cite it from this story. |
| CDC-10031 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-14 | header | Record the signed epic design sign-off for EP01; no sign-off exists in the story or source documents. |
| CDC-10062 | RWB-P5-E1054-APP | DOR-RWB-P5-E1054-APP-14 | find it | Record the signed epic design sign-off, since no signed epic design is recorded in this story or the source documents. |
| CDC-10138 | RWB-P5-E1057-APP | DOR-RWB-P5-E1057-APP-14 | header | Record the signed epic design sign-off for EP01 in the epic design record. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09983 | RWB-P5-E1052-APP | CG-ALL-5974 | 16 | Add rows TC-E1-052-11 and TC-E1-052-12 with Given, When and Then copied from the criteria in their Covers column. |
| CDC-10046 | RWB-P5-E1053-CON | CG-ALL-6003 | 16 | Covers column kept on the story's own AC numbers; no v8 alignment applied |
| CDC-10093 | RWB-P5-E1054-CON | CG-ALL-6034 | 16 | Add rows TC-P5-E1054-CON-01 to TC-P5-E1054-CON-08 with Given, When and Then copied from the section 7 criteria they cover and the section 16 data. |
| CDC-10160 | RWB-P5-E1057-CON | DOR-RWB-P5-E1057-CON-12 | 12.7, 16, 18 | Add rows TC-P5-E1057-CON-01 to -08; move legacy rows for AC2, AC3, AC7, AC9, AC13 to owning story; align RTM v7 section 18 lists. |
| CDC-10165 | RWB-P5-E1057-CON | CG-ALL-6077 | 16 | Add rows for TC-P5-E1057-CON-01 to TC-P5-E1057-CON-08 with Given, When and Then copied from the criterion each covers. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10004 | RWB-P5-E1052-APP | GAP-0752 | n/a | Fill the E cell in the P3 row of the P6 column (slide 13) as consumer of the P6 answer; confirm REST POST /cases/{caseId}/notices inside a CaseWorkflow activity (slide 17). |
| CDC-10077 | RWB-P5-E1054-APP | GAP-0988 | find it | Publish the review-item authorise request and answer schema naming the review team attribute and every other attribute; record matrix and masking version labels with valid-from dates; list review-field IDs for the masking pack. |
| CDC-10112 | RWB-P5-E1055-APP | GAP-1597 | 11 | Keep proof of delivery as an rwb-comms product read through the rwb-source-data contract; the ACE team owns the v_ace_pod writer. |
| CDC-10114 | RWB-P5-E1055-APP | GAP-2096 | 8 | Add EV-15 NoticeDelivered published by rwb-comms on proof arrival, read through the P1 contract on the ACE batch business date. |
| CDC-10141 | RWB-P5-E1057-APP | GAP-1843 | header | Align RWB-S9-E1057-APP to a wave 1 contract-only slice for partner identity and partner document path; panel, allocation and fees move to wave 4. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10017 | RWB-P5-E1053-APP | CG-ALL-5986 | n/a | Add owner_name to the dictionary, or use the dictionary name in RWB-P5-E1025-APP. |
| CDC-10018 | RWB-P5-E1053-APP | CG-ALL-5987 | n/a | Add borrower_name to the dictionary, or use the dictionary name in RWB-P5-E1025-APP. |
| CDC-10036 | RWB-P5-E1053-CON | CG-ALL-5999 | find it | Use the dictionary name for area_sq_wa or record the object (TITLE_DEED field) in LDM v9 and Data Classification v5. |
| CDC-10041 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-7 | 11 | Record review_only, extraction_method and area_sq_wa in LDM v9 and Data Classification v5, or name their dictionary fields. |
| CDC-10110 | RWB-P5-E1055-APP | DOR-RWB-P5-E1055-APP-7 | 11 | Add uk_document_case_type_hash as a database index of document, or state it sits outside the field list. |

### RWB-P6-E1055-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10116 | RWB-P5-E1055-APP | GAP-0578 | 12.8 | Keep the delivery entry write with rwb-comms through POST /cases/{caseId}/interactions, the contract reading, or move it to the ledger owner. This story writes no ledger row. |
| CDC-10120 | RWB-P5-E1055-APP | GAP-0577 | 12 | Publish the proof-of-delivery read as GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= with the ten-field record, page parameters and error set, and align the consumed row and fake at the wave 1 freeze. |
| CDC-10121 | RWB-P5-E1055-APP | GAP-1043 | 12.2 | Publish the notice read by notice ID and the dispatch reference as one operation with named request and response fields, including the field carrying the document reference. |
| CDC-10123 | RWB-P5-E1055-APP | GAP-1100 | 12 | Attach the WIN owner INT-14 and INT-15 specifications to the contract baseline as versioned annexes and declare the file element as a shape until then. |
| CDC-10126 | RWB-P5-E1055-APP | GAP-2243 | 7 | Confirm element names of rwb.comms.NoticeDelivered.v1 and the notice read at contract review; rename in this story only if they differ. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09970 | RWB-P5-E1050-OPS | GAP-0363 | 13 | Keep CLASSIFY_THRESHOLD, CLASSIFY_MAX_PAGES and CLASSIFY_TIMEOUT_SECONDS as data rows of document_hub_parameter; record the rwb-agent child run; keep 0.80, 90 percent and type labels |
| CDC-09972 | RWB-P5-E1050-OPS | GAP-2133 | 16 | Seed valuation inputs in rwb_source_data (valuation_ext) and the RouteDecided outcome in rwb_decision; no S1 rwb-valuation table until a technical specification adds one |
| CDC-09999 | RWB-P5-E1052-APP | GAP-2094 | 12 | Settle the path of the case-level notice list as a P6 operation; until then read notices of a case through GET /notices/{noticeId} per notice. |
| CDC-10113 | RWB-P5-E1055-APP | GAP-2090 | 11 | Add barcode, callback date and delivery status to the notice row; no separate proof table unless a DB story needs one. |

### RWB-P6-E1052-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09980 | RWB-P5-E1052-APP | DOR-RWB-P5-E1052-APP-21 | Header | Publish the contract and confirm it as the contract dependency; the header already names RWB-P6-E1052-CON. |
| CDC-09981 | RWB-P5-E1052-APP | DOR-RWB-P5-E1052-APP-22 | 12.8 | Publish the contract fake and record its library version; the story then cites that version in 12.8. |
| CDC-09988 | RWB-P5-E1052-APP | GAP-0357 | find it | Publish the base and route of the five template operations under /api/recovery/comms/v1/admin/templates, the SCR-33 composite route, the freshness-stamp data product and the withdrawal generation hold point. |
| CDC-09991 | RWB-P5-E1052-APP | GAP-0364 | find it | Route generation through POST /cases/{caseId}/notices on P6, read ACE facts and the stale-batch signal through P1's data-product contract, store the PDF through P5, keep the merge snapshot in P6 as references only. |

### RWB-P5-E1054-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10063 | RWB-P5-E1054-APP | DOR-RWB-P5-E1054-APP-21 | find it | Set the build status to Done (currently Not started) so the contract is published before this story is ready. |
| CDC-10064 | RWB-P5-E1054-APP | DOR-RWB-P5-E1054-APP-22 | find it | Publish the contract fake library and record its version. |
| CDC-10072 | RWB-P5-E1054-APP | GAP-1011 | 3 | Freeze seven operations, nine resources, five value sets, IntakeResolution envelope, If-Match lock with idempotent repeat, document read reference and event schema; keep the three message texts and by-number path as placeholders. |
| CDC-10119 | RWB-P5-E1055-APP | GAP-1099 | 12.2 | Name the stored-letter read of the document hub and its claim-check handle. Until then a missing letter is held, not dispatched, on GET /api/recovery/document/v1/documents/{documentId} with a 2 s budget. |

### RWB-P5-E1057-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10139 | RWB-P5-E1057-APP | DOR-RWB-P5-E1057-APP-21 | header | Move the build status from Not started to Done once the contract is published. |
| CDC-10145 | RWB-P5-E1057-APP | GAP-1012 | 3 | Publish the three admin operations and the run record, read the legacy intake container as rwb-quarantine, and carry channel properties as INF and OPS values. |
| CDC-10147 | RWB-P5-E1057-APP | GAP-0367 | 3 | Declare the JOB-12 run read and rerun against the P1 admin job contract in the Ownership Map. Partner read via S9 and channel properties stay as in the story. |
| CDC-10148 | RWB-P5-E1057-APP | GAP-1013 | 12 | Fix the three operations and run resources as the smallest superset of the job record, publish six fakes and the drift test, keep unnamed elements behind a placeholder. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09960 | RWB-P5-E1050-OPS | CG-ALL-5961 | 12.3 | Add rwb.document.DocumentClassified.v1 to the Events sheet, or use a catalogued event type in the story. |
| CDC-09986 | RWB-P5-E1052-APP | DOR-RWB-P5-E1052-APP-8 |  | Align the payload of rwb.document.DocumentStored.v1 with AC1 fields (document ID, case ID, type, source), or record the difference |
| CDC-10021 | RWB-P5-E1053-APP | DOR-RWB-P5-E1053-APP-8 | 12.3 | Align the payload of rwb.document.DocumentFieldsExtracted.v1 with the catalogue v1 payload, and align section 12.3 of RWB-P5-E1053-APP to match it. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10005 | RWB-P5-E1052-APP | GAP-0753 | n/a | Add the case-side notice request switch key, default on, owner RW-COE. Platform DB story to name one login per service for rwb-case. |
| CDC-10078 | RWB-P5-E1054-APP | GAP-0756 | find it | Add the rwb-case review-queue switch as a parameter key, name Not specified in the source documents (GAP-0756), stored in the platform flag library; off means no review task is raised and the queue answers no row. |
| CDC-10096 | RWB-P5-E1054-CON | GAP-0756 |  | Add the rwb-case review-queue switch as a parameter key, stored in the platform flag library; off means no review task is raised and the queue answers no row. Key name Not specified in the source documents (GAP-0756). |

### RWB-P5-E1053-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10038 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-10 | find it | Add empty, loading, error and no-access states for SCR-30 and SCR-31. |
| CDC-10048 | RWB-P5-E1053-CON | CG-ALL-6006 | 15 | Four screen-state rows removed from the contract story |
| CDC-10049 | RWB-P5-E1053-CON | CG-ALL-6007 | 15 | Four screen-state rows removed from the contract story |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09963 | RWB-P5-E1050-OPS | CG-ALL-5963 | 12.5 | Add activity classifyStep to the Activities sheet with task queue rwb-document, or name a catalogued activity in section 12.5 instead. |
| CDC-09964 | RWB-P5-E1050-OPS | CG-ALL-5964 | 12.5 | Add activity evaluateClassifier to the Activities sheet with task queue rwb-document, or name a catalogued activity in section 12.5 instead. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09995 | RWB-P5-E1052-APP | GAP-1082 | find it | Publish the NoticeRequest and Notice schemas with required flags and the NoticeGenerated payload, and confirm them with the app stories of this key. |
| CDC-10095 | RWB-P5-E1054-CON | GAP-0988 |  | Publish the review-item authorise request and answer schema naming the review team attribute and every other attribute; record matrix and masking version labels with valid-from dates and environment; list review-field IDs for the masking pack with its version. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10009 | RWB-P5-E1052-APP | GAP-1083 | n/a | Record that the Litigation right and scope test of the notice operations are enforced at the edge under RWB-PLT-N001-CON. |
| CDC-10010 | RWB-P5-E1052-APP | GAP-2455 | 12.7 | Confirm that rwb-decision appends every DecisionRecorded fact of every service to decision_log_entry; the producer's local record is the working record and the ledger entry is the record of record; RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0 and wave-1 baseline and stay out of the H row. |

### RWB-P5-E1053-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10012 | RWB-P5-E1053-APP | DOR-RWB-P5-E1053-APP-21 | n/a | Bring the contract story to Done and publish the contract before this story starts. |
| CDC-10013 | RWB-P5-E1053-APP | DOR-RWB-P5-E1053-APP-22 | n/a | Publish the contract fake library and record its published version. |

### RWB-P5-E1025-APP; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10015 | RWB-P5-E1053-APP | CG-ALL-5984 | n/a | Add extraction_method to the dictionary, or record it as a field_definitions key in RWB-P5-E1025-APP. |
| CDC-10016 | RWB-P5-E1053-APP | CG-ALL-5985 | n/a | Add review_only to the dictionary, or record it as a field_definitions key in RWB-P5-E1025-APP. |

### RWB-P3-E1035-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10071 | RWB-P5-E1054-APP | GAP-1010 | 3 | Publish the by-number case read on RWB-P3-E1035-CON so both P5 keys consume one path; P5 keeps its own four review rows in rwb_document. |
| CDC-10089 | RWB-P5-E1054-CON | GAP-1010 | 10, 12.7 | Publish the by-number case read so both P5 keys consume one path; add a P4 CON row for role, team and scope. |

### RWB-P3-E1043-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10073 | RWB-P5-E1054-APP | GAP-0755 | 3 | Carry REVIEW_TEAM_UNATTACHED as a data row through the rwb-case parameters contract, with the value per environment agreed by RW-COE; P5 keeps its own row for its screen. |
| CDC-10076 | RWB-P5-E1054-APP | GAP-0746 | 3 | Case review task code, element type and status values Not specified |

### RWB-P5-E1057-INF (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10146 | RWB-P5-E1057-APP | GAP-1014 | 3 | Record channel inventory as environment configuration, hold credentials as key store references, and confirm the DMZ position and scan rate with network and security owners. |
| CDC-10162 | RWB-P5-E1057-CON | GAP-1014 | 12.1 | Record the channel inventory as environment configuration; hold key material and mailbox credential as secret references; provision scan capacity around RWB-P5-E1041-APP; network and security owners confirm DMZ position and scan rate. |

### RWB-P5-E1057-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10149 | RWB-P5-E1057-APP | GAP-1015 | 3 | Register the Schedule with a release-fixed ID, overlap policy skip and catch-up window of one run; deploy four channel blocks per environment; publish four alerts and five runbook entries. |
| CDC-10163 | RWB-P5-E1057-CON | GAP-1015 | 12.1 | Register the Temporal Schedule with overlap policy SKIP and a catch-up window of one run; deploy four channel blocks per environment; publish four alerts with one runbook entry each. Unknown values stay Not specified in the source documents (GAP-1015). |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20754 | RWB-P5-E1052-APP | R-22162 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |
| CDC-20758 | RWB-P5-E1054-APP | R-28624 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09959 | RWB-P5-E1050-OPS | CG-ALL-5960 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or consume a published operation. |

### RWB-P5-E1050-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09961 | RWB-P5-E1050-OPS | DOR-RWB-P5-E1050-OPS-21 | header | Set build status to Done once the contract is published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09962 | RWB-P5-E1050-OPS | DOR-RWB-P5-E1050-OPS-8 | find it | Publish the rwb-case and rwb-access operations and add the DocumentClassified event type (CG-ALL-5959 to CG-ALL-5961). |

### RWB-P5-E1050-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09968 | RWB-P5-E1050-OPS | GAP-1002 | 12.5 | Add a C row for rwb-agent or the model-gateway satellite if it stays external; the classifier stays behind ClassifierClient with a stub and a route property |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09969 | RWB-P5-E1050-OPS | GAP-1003 | 12.2 | Declare the two classify operations on the service base once the architect confirms them; add rwb.document.DocumentClassified.v1 to the event catalogue and amend the event count and AC8 of RWB-P5-E2026-CON |

### API:(service not named); 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:EV-17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09971 | RWB-P5-E1050-OPS | GAP-0761 | 12.5 | Extend Document and EV-16 with classifierVersion, reviewReason, candidateOneType and candidateTwoType with confidences, or add one agreed classified event and consume it |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09975 | RWB-P5-E1050-OPS | CG-ALL-5968 | 3 | Template gives V0001 as the baseline only; the next number is Not specified (CG-ALL-5968). Story file name kept until the template or migration register rules. |

### OTHER:service catalogue (ACE DB team; OTHER:DP-02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09976 | RWB-P5-E1050-OPS | GAP-0762 | find it | Record the rwb-case login name agreed with the ACE DB team under DP-02; until then it is named as the rwb-case login (DP-02). |

### OTHER:rwb-case parameters contract (RW-COE) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09977 | RWB-P5-E1050-OPS | GAP-0766 | find it | Agree one boolean parameter key for the rwb-case classification handler and set the daily re-drive time of day outside the case-creation and allocation windows. |

### RWB-P3-E1050-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09978 | RWB-P5-E1050-OPS | GAP-0767 | find it | Write the decision record as a local row in the rwb_case decision-record table, publish no DecisionRecorded event and claim no platform dependency. |

### OTHER:Recovery Workbench P3 screen specification (SCR-01; OTHER:SCR-18; OTHER:SCR-30) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09984 | RWB-P5-E1052-APP | DOR-RWB-P5-E1052-APP-10 |  | Add empty, loading, error and no-access states to SCR-01, SCR-18 and SCR-30 |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09985 | RWB-P5-E1052-APP | DOR-RWB-P5-E1052-APP-18 |  | State assumptions ASM-1861, ASM-1925, ASM-2093 and ASM-2727 against open decision DL28 and keep DL28 open |

### OTHER:P2 message catalogue (detcheck owner of MSG-P5-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09987 | RWB-P5-E1052-APP | DOR-RWB-P5-E1052-APP-9 | 14 | Align the P2 use of MSG-P5-006 to the meaning in section 14 of this story: the notice type has no document type in force (FSD P5). Eight messages are listed in section 14. |

### RWB-P3-E1018-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09989 | RWB-P5-E1052-APP | GAP-1085 | find it | Publish the task-raise operation of rwb-case, or the event that creates a task, and record it in the ownership map for the two tasks raised by the notice flow. |

### OTHER:TSD P6 v2 (T3.1) and legacy RWB-E1-052 field list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09990 | RWB-P5-E1052-APP | GAP-1084 | find it | Give the party reference its own field ID and keep person_key as the business key of the notice, then correct the module specification or the legacy field list. |

### OTHER:TSD P3 v3 (recovery_case) and the data dictionary (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09992 | RWB-P5-E1052-APP | GAP-0749 | find it | Add the seven notice fact columns to recovery_case and load the notice timeline event codes into LOV-LEDGER-EVENT. Data steward to issue field IDs in the next dictionary version. |

### RWB-P5-E1052-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09993 | RWB-P5-E1052-APP | GAP-1079 | header | No contract dependency row is added to the story; the invented RWB-P5-E1052-CON row is removed. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09994 | RWB-P5-E1052-APP | GAP-1081 | find it | Name the merge snapshot store, a snapshot table or a column on the local decision record, and publish it in the next physical-schema version. |

### OTHER:rwb-comms contract (API-P6-001 error rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09996 | RWB-P5-E1052-APP | GAP-1086 | find it | Publish one error row per condition for API-P6-001: withdrawn-template hold answered with notice state Held, repeat with different key answered 409, missing field answered 422. |

### RWB-P6-E1052-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09997 | RWB-P5-E1052-APP | GAP-2454 | 9 | Fix the generation record payload: template code and version and merge snapshot reference in inputs_ref with ACE data date; notice reference and type in actions; hold reason or refusal and freshness message in outcome; final-call set GENERATED, HELD, REFUSED as a reference list. |

### RWB-P1-E1015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10000 | RWB-P5-E1052-APP | GAP-1080 | 11 | Publish the data-product record shape of DP01 Account and arrears and DP07 Legal, naming each returned field and its source column. |

### OTHER:Story map; RWB-P5-E1055-APP; RWB-P5-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10001 | RWB-P5-E1052-APP | GAP-2351 | 12.6 | Record RWB-P5-E1017-APP as sole owner of JOB-17; correct RWB-P5-E1055-APP and RWB-P5-E1065-APP section 12.6; record this story as notice generation slice with no Schedule. |

### RWB-P5-E2026-CON; OTHER:RWB-PLT-DB and the document type load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10002 | RWB-P5-E1052-APP | GAP-2348 | 11 | Publish request and reason fields of GenerateRequest and RegenerateRequest and the answer shape; fix per-service login names; publish container name, index, migration step, feature flag and MSG-P5-006 text. |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10003 | RWB-P5-E1052-APP | GAP-0751 | n/a | Add the request task code and the hold task code as task rows of the case model (element type HUMAN_TASK, discretion REQUIRED, status values) via the reference-data contract; story side dedupes on case, task code and business date. |

### OTHER:TSD P6 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10006 | RWB-P5-E1052-APP | GAP-1087 | n/a | Add LOV-HOLD-REASON to T3.2 carrying POSTAL_ADDRESS and TEMPLATE_WITHDRAWN, read through the reference-data contract. |

### OTHER:rwb-comms AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10007 | RWB-P5-E1052-APP | GAP-1088 | n/a | Publish NoticeGenerated with noticeId, caseId, templateId, templateVersion, noticeType and generatedAt; confirm with rwb-decision and rwb-reporting. |

### OTHER:work package split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10008 | RWB-P5-E1052-APP | GAP-2349 | n/a | Record one owning story per legacy criterion and mark the secondary slice as test-case-bearing but criterion-free. |

### RWB-P5-E1025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10019 | RWB-P5-E1053-APP | CG-ALL-5988 | 424 | Record guarantor_name as the GUARANTOR_NOTICE field code of DOCTYPE-2026.11 in the owning document, or add the dictionary entry in LDM v9 or Data Classification v5 (owner Data). |

### OTHER:Service API catalogue (rwb-document) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10025 | RWB-P5-E1053-APP | GAP-1006 | 3 | Publish the three operations on the document base, record them in the service API catalogue, and retire the legacy Java FieldExtraction interface. |

### OTHER:RWB-API catalogue and AsyncAPI fragment of rwb-document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10027 | RWB-P5-E1053-APP | GAP-1008 | 12 | Publish the resource names, property sets, paths and DocumentFieldsExtracted payload of this baseline as version 1; allow additive change only within major version 1. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10039 | RWB-P5-E1053-CON | DOR-RWB-P5-E1053-CON-11 | find it | Align the personal class of each field name with the §11 personal list (account_no, owner_name, borrower_name, guarantor_name). |

### OTHER:Service API catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10045 | RWB-P5-E1053-CON | GAP-1006 |  | Record the three extraction operations on /api/recovery/document/v1 and treat the legacy RWB-E1-053 Java interface as retired. |

### RWB-ITG-E1059-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10050 | RWB-P5-E1053-CON | GAP-0610 |  | Keep AC5 and TC-E1-059-05 with RWB-ITG-E1059-ITG; agree login with ACE database team and route with edge owner; add RWB-P5-E1053-CON to contract dependencies when published. |

### OTHER:API catalogue of rwb-document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10051 | RWB-P5-E1053-CON | GAP-1008 No source fixes the field-level names of ExtractionRequest, ExtractedField and FieldSet, the extract operation paths or the event payload | 7 | No field-level edit; shapes stay as section 11 states |

### RWB-P5-E2026-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10070 | RWB-P5-E1054-APP | GAP-1003 | none | Add rwb.document.DocumentClassified.v1 to the event catalogue; amend event count and AC8; declare the two classify operations on the service base once the architect confirms them. |

### OTHER:TSD P7 v2 (decision_log_entry) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10074 | RWB-P5-E1054-APP | GAP-2456 | 3 | Attach code DOCATT recorded; actions and outcome keys Not specified |

### OTHER:TSD P3 v3 (data dictionary and reference-data contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10079 | RWB-P5-E1054-APP | GAP-0757 | find it | Load the review task code, review states and case-side decision code as reference rows; allocate field IDs for document_ref, review_reason, item_version and review_state at the next data dictionary version. |

### OTHER:FSD P5 v3 (A2.10 and A2.11 feature sections) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10080 | RWB-P5-E1054-APP | GAP-1593 | find it | Add one distinct criterion for the correction feed to the labelled set, separate from the duplicated queue criteria of AC-P5-010-01 and AC-P5-011-01. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10081 | RWB-P5-E1054-APP | GAP-0758 | find it | Agree the rwb-case login name, Not specified in the source documents (GAP-0758), and use it for grants, Flyway history and connection pool. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10087 | RWB-P5-E1054-CON | DOR-RWB-P5-E1054-CON-12 | 12.7, 16, 18 | Add TC-P5-E1054-CON-01 to TC-P5-E1054-CON-10 to Test Cases v8 tab Story test cases; align the P3 section 18 test lists with RTM v7. |

### OTHER:Platform message set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10088 | RWB-P5-E1054-CON | DOR-RWB-P5-E1054-CON-9 | 14 | Confirm the standard meanings of MSG-P4-001 and MSG-GEN-006 and their texts, then align section 14 to them. |

### OTHER:rwb-document OpenAPI and AsyncAPI documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10090 | RWB-P5-E1054-CON | GAP-1011 | 11 | Freeze the seven operations, nine resources, five value sets, IntakeResolution envelope, If-Match repeat and event schema; collect consumer sign-off. |

### OTHER:rwb-case parameters and reference contracts (DP-06; OTHER:DP-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10091 | RWB-P5-E1054-CON | GAP-0755 |  | Load REVIEW_TEAM_UNATTACHED as a data row read through the parameters contract, with the review team of each environment agreed by RW-COE; the rwb-case queue reads this row only. |

### OTHER:TSD P3 v3 reference rows and the data dictionary at its next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10097 | RWB-P5-E1054-CON | GAP-0757 |  | Load the review task code, the review states and the case-side decision code as reference rows; allocate field IDs for document_ref, review_reason, item_version and review_state. |

### OTHER:FSD P5 v3 (A2.10 and A2.11) and the PRD decision record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10098 | RWB-P5-E1054-CON | GAP-1593 |  | PRD reads the two sections as one behaviour delivered by CAP-P5-010 and FR-P5-017 and FR-P5-018 and adds the correction feed to the decision record; FSD adds one distinct criterion for the feed. |

### RWB-PLT-NF06-DB; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10099 | RWB-P5-E1054-CON | GAP-0758 |  | Agree the rwb-case login name with RWB-PLT-NF06-DB and record it for the grants, the Flyway history and the connection pool of rwb-case. Name Not specified in the source documents (GAP-0758). |

### OTHER:Contract backlog (CON story for rwb-document) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10105 | RWB-P5-E1055-APP | DOR-RWB-P5-E1055-APP-21 | header | Create contract story RWB-P5-E1055-CON covering the four section 12.1 operations, or confirm RWB-P6-E1055-CON covers them and record that dependency |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10106 | RWB-P5-E1055-APP | DOR-RWB-P5-E1055-APP-22 | header | Publish the contract fake library version for the rwb-document operations and record its version in the story |

### RWB-P5-E1024-APP; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10108 | RWB-P5-E1055-APP | CG-ALL-6045 | 13 | Record uk_document_case_type_hash as a unique partial index on document (case_id, document_type, content_sha256) where active, as an object of migration V1024_1. |

### OTHER:RWB-E1-055 section 4; OTHER:RWB-E1-011 section 19 and the check register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10111 | RWB-P5-E1055-APP | GAP-1169 | 16 | Give the notice barcode break its own code and keep REC-05 for the business-key orphan check. |

### OTHER:TSD P1 v3 T3.2 and FSD P1 v3 A2.1.4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10115 | RWB-P5-E1055-APP | GAP-0579 | 8 | State the proof answer: 200 with no row, ten fields not available with SECTION_B_NOT_DEPLOYED, DP07 STALE and MSG-P1-001, behind flag rwb.dataengine.pod-read. |

### RWB-P1-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10117 | RWB-P5-E1055-APP | GAP-0580 | 7 | Count each repeat of the proof-of-delivery read on data_product_load.duplicate_count for the DP07 business date, one increment per repeat, with no ledger row and no log-only hit. |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10118 | RWB-P5-E1055-APP | GAP-1097 | 12 | Add pod records, freshness and batch-status elements of the pod data product with business date, feed version, batch status and stale marker. Until then use the DP07 records and freshness reads. |

### OTHER:FSD P5 Document hub v3 (type table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10122 | RWB-P5-E1055-APP | GAP-1044 | 12.1 | Add a proof-of-delivery receipt type, or confirm which existing type it uses, with its retention class and write-once flag, and confirm the DEMAND to DEMAND_LETTER mapping at the next type table version. |

### RWB-P6-E1055-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10124 | RWB-P5-E1055-APP | GAP-1102 |  | Record host, port, zone, certificate subject and owner, container names, retention and file sizes as reviewed values per environment; confirm with WIN owner and Security before SIT. |

### RWB-P6-E1055-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10125 | RWB-P5-E1055-APP | GAP-1103 |  | Fix the rwb-comms deployment slot and namespace under DL35, name the Schedule, record the Airflow window call and assert both in the registration step. |

### RWB-P6-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10127 | RWB-P5-E1055-APP | GAP-1098 |  | Record that the declared area and right are enforced at gateway-bff on the screen path; add the P4 authorise contract as a C dependency or state the service identity case. |

### OTHER:Story map (work package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10129 | RWB-P5-E1055-APP | GAP-2351 | 3 | Record RWB-P5-E1017-APP as sole owner of JOB-17 and RWB-P5-E1052-APP as notice generation slice with no Schedule; correct section 12.6 of this story at next version. |

### OTHER:FSD P5 (A2 proof of delivery) and TSD P5 (T3.1 field_definitions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10130 | RWB-P5-E1055-APP | GAP-1045 | 7 | Name the four receipt fields (barcode, callback date, delivery status, sent type) in the receipt type's field_definitions and state the receipt granularity in the proof-of-delivery section A2. Names not in sources. |

### OTHER:Message catalogue (FSD P5 message list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10131 | RWB-P5-E1055-APP | GAP-1046 |  | Add the text of MSG-P5-016 (malware found) to the message catalogue. Text Not specified in the source documents (GAP-1046). |

### OTHER:rwb-comms values files and the alert runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10132 | RWB-P5-E1055-APP | GAP-1104 |  | Set the alert thresholds, the reviewed late-batch time and the Schedule state per environment, confirmed at UAT. Values Not specified in the source documents (GAP-1104). |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10134 | RWB-P5-E1055-APP | GAP-2246 |  | Allocate the Data Dictionary field ID for the nullable notice reference column on the timer table and add it to the ownership map. ID Not specified in the source documents (GAP-2246). |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10142 | RWB-P5-E1057-APP | GAP-1587 | 10 | Replace branch, SFTP and mailbox file paths in the P5 intake sections with rwb-integration handing each file to P5 as an intake item; P5 records source, channel, capture time, hash and duplicate rule only. |

### OTHER:Story dependencies v5 (Dependency classes sheet, check row X) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10151 | RWB-P5-E1057-APP | GAP-3234 |  | Record that platform technical-enabler work on the ten App development X rows is team-type work, tracked and never blocking; keep X on those rows |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10156 | RWB-P5-E1057-CON | DOR-RWB-P5-E1057-CON-8 | 12.1, 12.2 | Publish the three admin operations in rwb-document.yaml and the parameter-by-code GET in rwb-case.yaml, as in CG-ALL-6072 to CG-ALL-6075. |

### OTHER:FSD P5 v3 intake sections (AC-P5-013-01; OTHER:AC-ALT-P5-013-01; OTHER:AC-ALT-P5-013-02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10157 | RWB-P5-E1057-CON | GAP-1587 | header | Remove P5 reads of scanner folder, SFTP subfolders and mailbox; rwb-integration takes the file and hands P5 an intake item with source, channel, capture time, hash and duplicate rule. |

### RWB-P5-E1057-INF; RWB-P5-E1057-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10161 | RWB-P5-E1057-CON | GAP-1012 | 12.1 | Carry the channel property layout as environment values; the Schedule owner confirms the business-hours window, overlap policy and catch-up window before the wave 1 release. |

### RWB-P5-E1024-APP; RWB-P3-E1042-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10164 | RWB-P5-E1057-CON | GAP-1018 | 12.2 | Store request takes an optional capture block as an additive change within major version 1; the five parameters come from the P3 parameters contract under legacy codes; the four lists come from the P3 reference-data contract under TSD codes. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20578 | RWB-P5-E1052-APP | R-17296 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '`debt_sale_account` by `account_key`; account data from `v_ace_acc |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0363 | Classifier route, parameter home and agent run evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0364 | Cross-service notice path, merge snapshot home and stale-batch signal are not named for the target | Tech lead | Resolved (directive) |
| GAP-0365 | Review queue operation names, scope source and attach evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0366 | WIN file path, proof-of-delivery read and interaction ledger home move in the target | Tech lead | Resolved (directive) |
| GAP-0367 | Partner eligibility, channel configuration and job monitoring move in the target | Tech lead | Resolved (directive) |
| GAP-0577 | The address, the answer envelope and the paging of the proof-of-delivery read of rwb-source-data are not fixed by any source: the sources name a data-product records path, the contract of this key names another, and no source names the page parameters, the element types or the error set | Solution architect | Resolved (directive) |
| GAP-0578 | No source settles who writes the delivery entry on the interaction ledger, nor which case the entry belongs to: the legacy story writes it in rwb-comms, the contract and the app story of rwb-comms say rwb-comms calls the ledger writer, the work package of this key gives the write to rwb-source-data, and the pod row carries an account key and no case | Solution architect | Resolved (directive) |
| GAP-0579 | No source names what the proof-of-delivery read answers before RWB-ACE-001 deploys the Section B views, nor the flag that holds it: the sources require the feature to stay behind a flag and the product to show stale, and give neither the answer shape, the reason code nor the flag name | Solution architect | Resolved (directive) |
| GAP-0580 | No source says where the repeat of a proof-of-delivery read is counted when the read writes no second entry: R-UNI-40 asks for the hit to be recorded and names no counter, and the two candidate counters belong to two different mechanisms | Data architect | Resolved (directive) |
| GAP-0581 | No source fixes the render of MSG-P1-001 for the WIN proof of delivery: the legacy story names the product 'DP07 Legal', the FSD names the ACE batch and the product code, and the date is either the last complete business date or the due date | Business analyst | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0749 | No field IDs for the notice facts on recovery_case, and no event code list for the notice timeline entries | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0750 | The decision code and the final call of the case-side notice record are only partly specified | RW-COE | Resolved (directive) |
| GAP-0751 | The task model values of the request task and of the task Complete notice data are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0752 | Architecture v5 gives P3 as a listener of P6, while the P6 contract accepts a REST notice request | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0753 | The per-service login name and the case-side feature switch key are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0755 | Review team for a review item with no case: the legacy value is assumed and the parameter has no agreed owner | RW-COE | Resolved (directive) |
| GAP-0756 | The rwb-case feature switch of the review queue has no name in any source | RW-COE | Resolved (directive) |
| GAP-0757 | The review task code, the review state values, the case-side decision code and the field IDs of the review link columns are not specified | RW-COE | Resolved (directive) |
| GAP-0758 | The rwb-case per-service login name is not specified | RW-SECADM | Resolved (directive) |
| GAP-0761 | The classification answer the case needs is not carried by the published document contract or by EV-16 and EV-17 | Solution architect | Resolved (directive) |
| GAP-0762 | The rwb-case login name is not in the sources | Tech lead | Resolved (directive) |
| GAP-0763 | The texts of MSG-GEN-004 and MSG-GEN-006 are not in the source extracts | Solution architect | Resolved (directive) |
| GAP-0764 | No source names a classifier version label or its format | Solution architect | Resolved (directive) |
| GAP-0765 | The case document link is not an Owner row and has no field IDs | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0766 | The rwb-case switch key and the re-drive time of day are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0767 | The decision record is written here although DP-03 and its library story are not applied | Solution architect | Resolved (directive) |
| GAP-0988 | The review-item authorise request shape, the label of the matrix and masking versions in force at the release date, and the review-field roster of the masking pack are fixed by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1002 | The classify run is drawn as an rwb-agent child while the legacy story calls the P10 model gateway in process, and no source names the model provider, endpoint or model version | Solution architect with the TechX tech lead of rwb-document and the rwb-agent owner | Resolved (directive) |
| GAP-1003 | No source names a classification operation, path or field-level name, a 404 message identifier is absent, and a classification event would be a third event for rwb-document | Solution architect with the TechX contract owner of rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1004 | The classifier artefact production and versioning, the evaluation report container, the alert thresholds and the deployment topology values are named by no source | DevOps engineer with the platform administrator and the data steward | Resolved (directive) |
| GAP-1005 | The extractor provider, model name and model version behind extraction_method MODEL are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1006 | No source names a REST operation or a path for running extraction, for its state read or for its fields read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1007 | The review reason EXTRACTION_FAILED is not a value of LOV-INTAKE-REVIEW | Data steward with the P5 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1008 | No source fixes the field-level names of ExtractionRequest, ExtractedField and FieldSet, the extract operation paths or the event payload | Tech lead of rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1009 | The field-extraction route of the rwb-agent contract, its answer field names and its model version are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1011 | No source fixes the field-level names of the nine review resources, the one resolve answer, the field-patch idempotency, the document read position or the three platform message texts | Tech lead of rwb-document with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1012 | The channel pickup has no target shape of its own: the run record, the rerun operation, the channel property layout, the single-run rule and the cross-service partner read are named by the legacy story only | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1013 | The channel-intake contract baseline fixes operation names, shapes and enumerations the sources do not name, and the plan's C list omits the partner read | Tech lead | Resolved (directive) |
| GAP-1014 | The four pickup channels, their credentials, their folder lifecycle, the partner DMZ position and the scan capacity are environment facts no source states | SCB IT infrastructure | Resolved (directive) |
| GAP-1015 | The deployment of the channel pickup has no source for its values, its chart key names, its Schedule ID, its catch-up window, its alert thresholds and its runbook entries | DevOps engineer | Resolved (directive) |
| GAP-1018 | Field capture: the store capture block, the intake submit path, the parameter and list names, the service login name and the approval status are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1021 | The published Java reader becomes a REST contract no source names, the extraction operations belong to another baseline of the same service, and the plan lists no C row for the case read | Tech lead | Resolved (directive) |
| GAP-1043 | The rwb-comms operations and field names behind RWB-P6-E1055-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1044 | The document type of the WIN proof-of-delivery receipt and the notice-type to document-type mapping | Center of excellence analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1045 | The field names of the WIN receipt in document_field and the receipt granularity | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1046 | The text of MSG-P5-016 | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1079 | The rwb-document contract used for the write-once generated PDF has no contract dependency row | Solution architect | Resolved (directive) |
| GAP-1080 | The field names behind the rwb-source-data data-product contract are not specified | Solution architect | Resolved (directive) |
| GAP-1081 | Where the merge snapshot is persisted is not specified | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1082 | The request and answer field list of the notice operations is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1083 | The scope and right check of the notice operations has no rwb-access dependency row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1084 | Field DF-LEG-030 is party_id in the module specification and person_key in the legacy story | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1085 | No operation in the ownership map raises a task on rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1086 | The error code of each refusal condition on the notice POST is not fixed | Solution architect | Resolved (directive) |
| GAP-1087 | The hold reason value set is not enumerated in a list of values | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1088 | The NoticeGenerated payload element list is not enumerated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1097 | The pod and batch-status contract elements are not named in RWB-P1-E1066-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1098 | No access guard story covers the notice read of rwb-comms | Solution architect | Resolved (directive) |
| GAP-1099 | The stored letter retrieval is not named in RWB-P5-E1054-CON | Solution architect | Resolved (directive) |
| GAP-1100 | The INT-14 and INT-15 fixed layouts, their record keys and their transport are not in the source material | Solution architect | Resolved (directive) |
| GAP-1101 | The owner of REC-05 and of the References exception list is not named | Solution architect | Resolved (directive) |
| GAP-1102 | The WIN host, port, zone, certificate owner, container names and file sizes are not in the source material | SCB IT infrastructure | Resolved (directive) |
| GAP-1103 | The deployment slot and namespace of rwb-comms, and the exact form of the JOB-10 Airflow handoff, are not specified | DevOps lead | Resolved (directive) |
| GAP-1104 | No source gives the alert thresholds, the reviewed time of the late WIN batch or the Schedule state per environment | DevOps lead | Resolved (directive) |
| GAP-1105 | Only one hold reason is named for a notice | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1587 | FSD P5 takes branch, mailroom, SFTP and mailbox files inside P5 while Architecture v5 gives P5 no file interface | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1593 | Two FSD features assert the same review-queue criteria and the correction feed has no distinct criterion | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-2087 | The source reads version 1 in its metadata table and v2 in its file name | Document owner of the notification and correspondence design | Resolved (directive) |
| GAP-2090 | The proof of delivery is named as P6 data but has no table, no DDL and no owner row | Service owner of P6 rwb-comms, with the DB story of the service | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2096 | No event, job or window tells rwb-comms that a proof of delivery has arrived | Service owners of P6 rwb-comms and P1 rwb-source-data; integration owner | Resolved (directive) |
| GAP-2133 | rwb-valuation owns no table, so the plan does not say where a route decision is kept | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2243 | Element names of the delivery fact and of the notice answer are not in the sources read for this work package | TechX and rwb-comms contract owner | Resolved (directive) |
| GAP-2246 | The timer has no field for the notice it belongs to, and its field ID is unallocated | rwb-case data owner and the Data Dictionary owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2247 | The notice period is owned by two rwb-case stories of the same legacy loop | TechX | Resolved (directive) |
| GAP-2348 | The rwb-document login, the request and answer field names of the generation path, the message text of MSG-P5-006, the container name, the index name, the Flyway step name and the P5 feature flag are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2349 | This slice owns no legacy acceptance criterion while the Work Package lists all eleven legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2350 | The dependency rows of this slice name one contract only, while the pattern set names five platform contracts, the rwb-case reference-data contract and the generation contract of the service | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2454 | The D7.1 generation record has no field layout, no final-call set and no message text in the sources | TechX | Resolved (directive) |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2456 | The review decision codes and outcome values, the placement of the review facts in the record, and the rwb-decision login name are in no source | Solution architect with the reference-data owner and the ACE team | Resolved (directive) |
| GAP-3234 | Ten class X rows point at a platform application story rather than at a DB, INF or OPS story | TechX (platform) | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P5-E1054-CON | skipped AC ID | 113 | missing: AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17 |
