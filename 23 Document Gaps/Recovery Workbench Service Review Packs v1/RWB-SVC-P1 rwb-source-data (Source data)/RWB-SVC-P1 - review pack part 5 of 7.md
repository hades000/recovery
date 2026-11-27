# RWB-SVC-P1 rwb-source-data (Source data) - review pack, part 5 of 7 (RWB-P1-E1066-APP to RWB-P1-E2001-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 152 |
| Cross-document (pending in another document) | 208 |
| Not applied (value not in the sources) | 9 |
| Open business decisions | 22 |
| Register gaps linked | 96 |
| Unconfirmed assumptions | 0 |
| Lint findings | 3 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P1-E1066-APP | 20 | 20 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1066 APP Interaction ledger store and writer v2.md |
| RWB-P1-E1066-CON | 20 | 21 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1066 CON Interaction ledger store and writer - contract v2.md |
| RWB-P1-E1066-OPS | 7 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1066 OPS Interaction ledger store and writer - deployment v2.md |
| RWB-P1-E1067-APP | 17 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1067 APP Every Workbench action into the interaction ledger v2.md |
| RWB-P1-E1067-CON | 15 | 9 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1067 CON Every Workbench action into the interaction ledger - contract v2.md |
| RWB-P1-E1068-APP | 21 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1068 APP Interaction ledger read interface v2.md |
| RWB-P1-E1069-APP | 18 | 36 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1069 APP Read-only ACE source views, grants and boundary rule v2.md |
| RWB-P1-E1069-DB | 18 | 29 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1069 DB Read-only ACE source views, grants and boundary rule - ACE DB v2.md |
| RWB-P1-E2001-APP | 16 | 38 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E2001 APP EFS hand-over with full history v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P1-E1066-APP | R-00388 | CG-ALL-2286 | Script gap | Product owner | The story adds LEDGER_WRITE_FAILED to the closed list LOV-LEDGER-EVENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P1-E1066-APP | R-09748 | CG-ALL-2293 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1066-CON | R-09750 | CG-ALL-2304 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1066-OPS | R-09752 | CG-ALL-2310 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1068-APP | R-09755 | CG-ALL-2328 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1069-APP | R-09764 | CG-ALL-2341 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E2001-APP | R-09770 | CG-ALL-2358 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E2001-APP | R-09771 | CG-ALL-2362 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-P1-E2001-APP | R-09772 | CG-ALL-2363 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-ITG-E1066-ITG, RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1066-OPS, RWB-P3-E1066-APP | R-22263 | GAP-2253 | Register gap | rwb-case reference data owner and Compliance | LOV-LEDGER-EVENT carries 14 values in the TSD and 12 in the legacy story | Load the fourteen values of TSD P3 v3 T5.1 as the reference rows of LOV-LEDGER-EVENT, with PARTNER_RESULT and OFFER included and the Thai labels of DL10, and let RWB-P1-E1066-CON validate against the same list; the two extra values add no rule and remove none. |
| RWB-ITG-E1069-ITG, RWB-P1-E1069-APP, RWB-P1-E1069-DB, RWB-P4-E1069-APP | R-22278 | GAP-0901 | Register gap | Compliance and PDPA officer | rwb-access ACE masking pack: no source names which ACE view fields the masking rows must cover or at which field IDs | Publish the masking field map as part of the pack design: one row per personal field ID of the 30 views with the role that may see it, agreed by the Compliance and PDPA officer, and load it with the pack instead of leaving the set to the story. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2001-ITG, RWB-P1-E1011-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22306 | GAP-0591 | Register gap | Data steward and data product owner, P1 | The REC-05 break list row for a hand-over key is defined only for keys on an existing Workbench table, not for a candidate that has no row yet | Answer the break in the candidate-facts read as {check: REC-05, keyType: PERSON_KEY or ACCOUNT_KEY, key: <value>} with resolution HELD, write no row and invent no fact, and let RWB-P1-E1011-APP's REC-05 step carry the row for the business date so the data steward and the ACE team read one list. Fix the answer in RWB-P2-E2001-CON. |
| RWB-ITG-E2001-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22309 | GAP-0588 | Register gap | Data steward and data product owner, P1 | The collection period of an account's EFS history is named by no source, so the boundary of the history read is undefined | Fix the period as the EFS assignment window of the account: it opens at v_ace_efs_assignment.assignment_start_date and closes at assignment_end_date, or at the business date of the read for the open assignment; when the account has no assignment row the period opens at its earliest contact_at. Publish the rule in RWB-P2-E2001-CON with the answer so the run and this service read the same boundary, and ask the data steward to confirm it with the ACE team before wave 2 exit. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-P1-E2001-APP | R-33393 | ASM-ALL-2362 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-P1-E2001-APP | R-33394 | ASM-ALL-2363 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-P1-E2001-APP | R-35821 | ASM-0830 | Register assumption |  | The collection period of an account is the EFS assignment window: it opens at v_ace_efs_assignment.assignment_start_date and closes at assignment_end_date, or at the business date of the read when the assignment is still open. When the account has no assignment row, the period opens at the earliest contact_at of its v_ace_efs_action rows and closes at the business date of the read. The answer names the period it used. | Data steward and data product owner with the ACE team, before wave 2 exit and before RWB-P2-E2001-CON is tagged |
| RWB-P1-E2001-APP | R-35824 | ASM-0833 | Register assumption |  | A hand-over key that does not resolve is answered in the candidate-facts read as resolution HELD with check REC-05, the key type PERSON_KEY or ACCOUNT_KEY and the key value; no row is written and no borrower, product-group or account fact is invented; the key returns on the read for the next complete batch. The REC-05 result row and the break list of the business date are written by RWB-P1-E1011-APP and read by the data steward and the ACE team there. | Data steward and data product owner with the ACE team before wave 2 exit |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P1-E1066-APP | R-04449 | DOR-RWB-P1-E1066-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record found. Grep of the folder for 'epic design' finds only process text and scratch escalation files. Sign-off cannot be stated without inventing it. |
| RWB-P1-E1066-APP | R-04452 | DOR-RWB-P1-E1066-APP-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | rwb-case (RWB-P3-E1018-CON fake) and rwb-decision (RWB-P7-E1027-CON fake) are already named in 12.8. No published fake library version is recorded in 22 Microservice Realignment, so none can be stated. |
| RWB-P1-E1066-CON | R-04456 | DOR-RWB-P1-E1066-CON-14 | none | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or sources (Decision Log v11 searched for 'epic design'). A sign-off cannot be invented; no edit made. |
| RWB-P1-E1067-APP | R-30264 | NEWAC-RWB-P1-E1067-APP-AC12 | 7, 16 | AC12: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Proposed test is not specified in the source documents; the story changes no case status and states no refused transition, so an AC12 scenario would invent behaviour. No edit. |
| RWB-P1-E1067-CON | R-04471 | DOR-RWB-P1-E1067-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-P1-E1067 or EP01 found; grepped project .md files (only scratch caches, other stories). A sign-off cannot be invented. |
| RWB-P1-E1069-APP | R-04480 | DOR-RWB-P1-E1069-APP-16 | section header | Definition of Ready item 16 Size: Fail | No source gives a size. The row records it as not specified and the item stays open for the squad at refinement. |
| RWB-P1-E1069-APP | R-28507 | GAP-3213 |  | A requirement whose own legacy stories do not cite it | The requirement text is not in this story, so no section 18 row is added and no value is invented. |
| RWB-P1-E1069-DB | R-15183 | DOR-RWB-P1-E1069-DB-15 | header | Definition of Ready item 15 INVEST: Partial | Whether the story is Small cannot be stated from the sources; the squad confirms it at refinement. |
| RWB-P1-E2001-APP | R-04489 | DOR-RWB-P1-E2001-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design for EP02 or RWB-P1-E2001-APP in source .md files; only scratch/cache hits. Sign-off not invented. Section 14 text not in chunk. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03229 | RWB-P1-E1066-APP | DOR-RWB-P1-E1066-APP-12 | 16 | Align the test case lists of this story's requirement rows with section 18 of RWB-P1-E1066-APP; section 16 now adds TC-E1-066-10 (contract) and TC-E1-066-11 (boundary, ASM-3438). |
| CDC-03236 | RWB-P1-E1066-APP | CG-ALL-2292 | 18 | Align the test lists of the four requirements in the Detail with section 18 of RWB-P1-E1066-APP in the next RTM version. |
| CDC-03259 | RWB-P1-E1066-CON | CG-ALL-2303 | 18 | Align the test lists of REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and the fourth listed requirement with section 18 of RWB-P1-E1066-CON in the next RTM version. |
| CDC-03280 | RWB-P1-E1066-OPS | CG-ALL-2309 | 18 | Align the test lists of the five differing requirements (including REQ-ILG-001, REQ-ILG-002 and REQ-ILG-004) with section 18 of RWB-P1-E1066-OPS. |
| CDC-03287 | RWB-P1-E1067-APP | DOR-RWB-P1-E1067-APP-12 | 16 | Align the test case lists for REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007 with section 18 of RWB-P1-E1067-APP. |
| CDC-03293 | RWB-P1-E1067-APP | CG-ALL-2314 | 18 | Align the trace rows of REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007 with section 18 of this story in its next version. |
| CDC-03303 | RWB-P1-E1067-CON | CG-ALL-2319 | 18 | Align the test lists of REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007 with section 18 of RWB-P1-E1067-CON, which lists TC-P1-E1067-CON-01 to -09 for these requirements. |
| CDC-03318 | RWB-P1-E1068-APP | CG-ALL-2327 | 18 | Align the test lists of REQ-ILG-006, REQ-ILG-003 and REQ-ILG-014 with section 18 of RWB-P1-E1068-APP in the next version. |
| CDC-03337 | RWB-P1-E1069-APP | DOR-RWB-P1-E1069-APP-12 | 16, 18 | Section 16 now has 11 test cases |
| CDC-03351 | RWB-P1-E1069-APP | CG-ALL-2340 | 18 | Align the REQ-RDF-002 and REQ-DRI-006 trace rows with the TC lists in section 18 of this story (TC-E1-069-01 to -06 and -08). |
| CDC-03365 | RWB-P1-E1069-DB | DOR-RWB-P1-E1069-DB-12 | 18 | Next version, sheet RTM, row REQ-DRI-006: add TC-E1-069-04, TC-E1-069-05, TC-E1-069-07 and TC-E1-069-08 to its test list, keeping the tests already listed. REQ-RDF-002 already lists this story's 01, 02, 05, 06. |
| CDC-03379 | RWB-P1-E1069-DB | CG-ALL-2347 | 18 | Align RTM v7 rows for REQ-RDF-002 and REQ-DRI-006 with section 18 test lists; section 18 REQ-RDF-002 row now aligned, REQ-DRI-006 full RTM list not in evidence. |
| CDC-03381 | RWB-P1-E1069-DB | GAP-3213 | 18 | Record REQ-RDF-004 against RWB-ITG-E3013-ITG, RWB-ITG-E3017-ITG and RWB-ITG-E3026-ITG as the citing stories; this story's section 18 unchanged. |
| CDC-03398 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-12 Test cases: Partial | 16 | Added contract test (11), section 12.7 boundary test (12), AC7/AC8 tests (13, 14), AC9/AC10 tests (15, 16), AC11 test (17) |
| CDC-03419 | RWB-P1-E2001-APP | CG-ALL-2357 | 18 | Align the test lists of the four requirements in the evidence (incl. REQ-DRI-013, REQ-CHO-001, REQ-CHO-005) with the section 18 lists of RWB-P1-E2001-APP in the next version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03267 | RWB-P1-E1066-OPS | CG-ALL-2306 | 4, 16 | Record tr_interaction_append_only in the owning document as a trigger object of the interaction table. |
| CDC-03271 | RWB-P1-E1066-OPS | DOR-RWB-P1-E1066-OPS-7 | 11 | Register tr_interaction_append_only as a trigger object, or confirm it is outside the field and entity list. |
| CDC-03328 | RWB-P1-E1069-APP | CG-ALL-2332 | 1, 3, 4, 7, 8, 10 | Record `ace_view_owner` as the database role object that owns the 30 recovery.v_ace_* views, or supply the dictionary name. |
| CDC-03329 | RWB-P1-E1069-APP | CG-ALL-2333 | 3, 12, 18 | Record `v_data_dictionary` as the view in the rwb_source_data baseline delivered by RWB-P1-E1001-APP, or supply the dictionary name. |
| CDC-03330 | RWB-P1-E1069-APP | CG-ALL-2334 | 7, 8 | Record recovery_svc as the rwb_source_data login named in DP-02, or use its dictionary name in the story |
| CDC-03331 | RWB-P1-E1069-APP | CG-ALL-2335 | 8 | Record recovery.ace_to_date as a helper SQL function in schema recovery, shipped by the Section A migration (TSD P1 T3.2) |
| CDC-03332 | RWB-P1-E1069-APP | CG-ALL-2336 | 8 | Record recovery.ace_to_boolean as a helper SQL function in schema recovery, shipped by the Section A migration (TSD P1 T3.2) |
| CDC-03333 | RWB-P1-E1069-APP | CG-ALL-2337 | 8 | Record recovery.ace_mask_value as a helper SQL function in schema recovery, shipped by the Section A migration (TSD P1 T3.2) |
| CDC-03334 | RWB-P1-E1069-APP | CG-ALL-2338 | 11 | Record ck_contact_point_ext_type as a check constraint of RWB-P1-E1069-DB in the owning document, or use its dictionary name |
| CDC-03362 | RWB-P1-E1069-DB | CG-ALL-2344 | 1 | Record ace_view_owner as a database role object in the owning document, or confirm no LDM entry is needed; no dictionary name matches |
| CDC-03366 | RWB-P1-E1069-DB | DOR-RWB-P1-E1069-DB-7 | 11 | Record ace_view_owner (a database role), ck_contact_point_ext_type (a check constraint) and rwb_source_data (renamed from recovery_svc) as non-field objects, or add them to the dictionary. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03225 | RWB-P1-E1066-APP | CG-ALL-2290 | 3 | Remove the fixed enum on eventCode so LOV-LEDGER-EVENT values are accepted as data without a code change. |
| CDC-03227 | RWB-P1-E1066-APP | DOR-RWB-P1-E1066-APP-8 | 12.1 | Publish POST and GET /interactions operations and remove the closed eventCode enum so LOV-LEDGER-EVENT is data. |
| CDC-03243 | RWB-P1-E1066-CON | CG-ALL-2296 | 12.1 | Owner yaml must publish the append; the story documents it as POST /cases/{caseId}/interactions in 12.1. |
| CDC-03244 | RWB-P1-E1066-CON | CG-ALL-2297 | 12.1 | Owner yaml must publish the list operation; the story documents it as GET /cases/{caseId}/interactions in 12.1. |
| CDC-03245 | RWB-P1-E1066-CON | CG-ALL-2298 | 12.1 | Owner yaml must publish GET /cases/{caseId}/interactions/{entryId}; check that the 12.1 row shows this path. |
| CDC-03307 | RWB-P1-E1068-APP | CG-ALL-2324 | 4 | Remove the fixed enum on channel; LOV-CHANNEL is read as data from the rwb-case reference-data contract (DP-07). |
| CDC-03388 | RWB-P1-E2001-APP | CG-ALL-2351 | 12.1 | Add path GET /api/recovery/source-data/v1/efs-history to the yaml through the CON story, or remove the operation from section 12.1. |
| CDC-03389 | RWB-P1-E2001-APP | CG-ALL-2352 | 12.1 | Add path GET /api/recovery/source-data/v1/entry-candidate-facts to the yaml through the CON story, or remove the operation from section 12.1. |
| CDC-03393 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-8 | find it | Publish GET efs-history and GET entry-candidate-facts in the yaml, and resolve the closed sourceSystem enum against LOV-SOURCE. |

### RWB-P1-E1066-CON (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03226 | RWB-P1-E1066-APP | DOR-RWB-P1-E1066-APP-21 | header | Set the build status to Done once the contract is published; it is currently Not started. |
| CDC-03242 | RWB-P1-E1066-APP | GAP-2185 | 12.1 | Replace POST /interactions with POST /cases/{caseId}/interactions in ACs, section 12.1, API document and append fake, matching the Ownership Map; add no third path. |
| CDC-03265 | RWB-P1-E1066-OPS | DOR-RWB-P1-E1066-OPS-21 | header | Set the contract story build status to Done once the contract is published. |
| CDC-03266 | RWB-P1-E1066-OPS | DOR-RWB-P1-E1066-OPS-22 | header | Record the published contract fake library version, or confirm the version to publish. |
| CDC-03274 | RWB-P1-E1066-OPS | GAP-0375 | find it | Publish the append with request and response fields, the Idempotency-Key rule, the 201, 200, 409, 422 and 503 mapping, and the saga failure rule. |
| CDC-03275 | RWB-P1-E1066-OPS | GAP-0504 | find it | Publish the append path, 403 without Case record C, 404 with MSG-P4-003 for unknown or out-of-scope cases, and 409 for a reused key with a different body. |
| CDC-03276 | RWB-P1-E1066-OPS | GAP-0505 | find it | Fix /interactions on the service base, name the rwb_source_data login, take property names from API Specification v4, and settle the required flags at baseline review. |
| CDC-03314 | RWB-P1-E1068-APP | GAP-0583 | 5, 7 | Story keeps the legacy 404 and leaves the out-of-scope mapping to RWB-P3-E1018-CON; the contract record and the API-P3-014 correction sit outside this story. |
| CDC-03322 | RWB-P1-E1068-APP | GAP-2102 |  | List the ledger readers in the P1 contract before the wave 1 freeze: P6 rwb-comms (contact history), P3 rwb-case (case timeline) and S2 rwb-treatment (collections history). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03261 | RWB-P1-E1066-CON | GAP-0267 | 7 | Owner column: P1 rwb-source-data on the 29 interaction fields; P3 rwb-case reads the ledger through the P1 contract for the case timeline. |
| CDC-03281 | RWB-P1-E1066-OPS | GAP-0267 |  | Owner column: P1 rwb-source-data on the 29 interaction fields; P3 rwb-case reads the ledger through the P1 contract for the case timeline. |
| CDC-03320 | RWB-P1-E1068-APP | GAP-0267 |  | Owner column: P1 rwb-source-data on the 29 interaction fields; P3 rwb-case reads the ledger through the P1 contract for the case timeline. |
| CDC-03339 | RWB-P1-E1069-APP | GAP-0358 | none | Keep the matrix, role and masking tables and their load and approval with P4 rwb-access; keep the parameters and LOV load with P3. Name rwb-source-data as the masking point at the data read, with the masked read proven through the P1 data product contract. |
| CDC-03340 | RWB-P1-E1069-APP | GAP-0014 | none | Add the Architecture v5 tables for S1 (rwb_valuation object groups) and P8 (payment and proceeds matching, fees, bookings, posting files) to the Tables sheet. Populate the FK cuts sheet with ID references for each cross-schema key. |
| CDC-03341 | RWB-P1-E1069-APP | GAP-0259 | none | Set the Owner column on all 304 fields of the 30 recovery.v_ace_* views to P1 rwb-source-data (recovery view). Grant no other service login any privilege on a view. |
| CDC-03342 | RWB-P1-E1069-APP | GAP-0263 | none | Replace the recovery identity SELECT rule on recovery.v_ace_* (rows 7 and 22) with: only the rwb_source_data login holds SELECT on the 30 views; other services read through the P1 REST contract or a Temporal activity; the read audit is written through the ACE Common PII logging path. |
| CDC-03368 | RWB-P1-E1069-DB | GAP-0014 |  | Add the v5 tables for S1 and P8 and populate FK cuts as ID references in the next Ownership Map version. |
| CDC-03370 | RWB-P1-E1069-DB | GAP-0259 |  | Owner column reads P1 rwb-source-data (recovery view) on all 304 recovery.v_ace_* view fields; no other login holds a view grant. |

### API:(service not named) (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03235 | RWB-P1-E1066-APP | GAP-2256 |  | Retire API-P3-014 and API-P3-015; keep the ledger operations in the rwb-source-data document. |
| CDC-03237 | RWB-P1-E1066-APP | GAP-2072 | find it | Move the interaction table and its two endpoints to P1 rwb-source-data; rwb-case reads the ledger through the P1 contract; correct in the same wave. |
| CDC-03253 | RWB-P1-E1066-CON | GAP-2256 | 7 | Retire API-P3-014 and API-P3-015 from the rwb-case API specification; the two ledger operations stay in the rwb-source-data document. |
| CDC-03260 | RWB-P1-E1066-CON | GAP-2072 | 7 | Set the interaction table and the two interaction endpoints to P1 rwb-source-data, with rwb-case reading the ledger through the P1 contract, as the plan ruling states. |
| CDC-03278 | RWB-P1-E1066-OPS | GAP-2256 | find it | Retire API-P3-014 and API-P3-015; keep the two ledger operations in the rwb-source-data document. |
| CDC-03304 | RWB-P1-E1067-CON | GAP-2072 | section 12.7 | AC7 of this story names only interaction and processed_event as owned tables. The P3 module specifications must be corrected in the same wave. |
| CDC-03316 | RWB-P1-E1068-APP | GAP-0582 | 4, 12 | Correct API-P3-014 and API-P3-015 to x-module P1 on base /api/recovery/source-data/v1 in their next versions; rwb-case keeps the case record and timeline. |
| CDC-03408 | RWB-P1-E2001-APP | GAP-1333 |  | Add the businessDate filter, the full DecisionLogPage and DecisionLogEntry field set and the page-size limit; name one screen or panel for a decision entry beside the case. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03246 | RWB-P1-E1066-CON | CG-ALL-2300 | 14 | Add a new message ID, text 'The request could not be read: {detail}.', for failed body, query or header validation and unsupported major version; the story then cites it for MSG-GEN-004. |
| CDC-03249 | RWB-P1-E1066-CON | DOR-RWB-P1-E1066-CON-9 | 14 | Add a new message ID for the unreadable-request condition (same addition as CG-ALL-2300); then replace MSG-GEN-004 in this story with it. |
| CDC-03311 | RWB-P1-E1068-APP | CG-ALL-2325 | 4, 14 | Business analyst adds a new message ID for 'No session' with text 'Your session has ended. Sign in again.'; the story then cites it. |
| CDC-03312 | RWB-P1-E1068-APP | CG-ALL-2326 | 4, 14 | Add a message ID for the store or contract unavailable use of this read, with the text of section 14; the story then cites it in place of MSG-GEN-006. |
| CDC-03395 | RWB-P1-E2001-APP | CG-ALL-2355 | 4, 14 | Add a new message ID for the session-ended text of the story, so MSG-P4-001 keeps its sign-in-with-no-role meaning; the story cites the new ID once it exists. |
| CDC-03399 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-9 | 14 | MSG-P1-001 text in section 14 is aligned to the standard under CG-ALL-2354. A separate ID for the ALS batch use is still to be issued by the BA. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03231 | RWB-P1-E1066-APP | DOR-RWB-P1-E1066-APP-6 | 10 | Add role SY-DATALOAD (data load: Case record C over the writer contract) or map it to a role already listed in v5. |
| CDC-03247 | RWB-P1-E1066-CON | DOR-RWB-P1-E1066-CON-1 | 1 | Add a role row for 'tech lead' (role code and name) or confirm the existing role that §1 should use; the story role is not defined there. Story §1 left unchanged. |
| CDC-03268 | RWB-P1-E1066-OPS | DOR-RWB-P1-E1066-OPS-1 | 1 | Register the role 'platform engineer' with a role code and name, or confirm the role the story should use. |
| CDC-03296 | RWB-P1-E1067-CON | DOR-RWB-P1-E1067-CON-1 | 1 | Confirm a role code or name for the 'tech lead' persona of section 1, or confirm it as a team persona outside role-based access. |
| CDC-03364 | RWB-P1-E1069-DB | DOR-RWB-P1-E1069-DB-1 | 1 | Add 'ACE database engineer' as a role code or role name, or name the existing role used as the section 1 persona. |

### RWB-P1-E1067-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03285 | RWB-P1-E1067-APP | DOR-RWB-P1-E1067-APP-21 | Header | Build status must reach Done; it is currently Not started. |
| CDC-03286 | RWB-P1-E1067-APP | DOR-RWB-P1-E1067-APP-22 | Header | Publish the contract fake library and record its version; no version is recorded. |
| CDC-03290 | RWB-P1-E1067-APP | GAP-0507 | 8 | Fix intake map rows: EV-16 DocumentStored maps to rwb.document.DocumentStored.v1 and EV-19 TimerBreached maps to rwb.case.TimerBreached.v1 (Architecture v5 slide 15 rows 16 and 19), with producer sign-off. |
| CDC-03292 | RWB-P1-E1067-APP | GAP-2257 | 8 | BR2 and BR3 state the key, actor and idempotency-key attribute names are Not specified in the source documents; values sit in rwb-case. |
| CDC-03295 | RWB-P1-E1067-APP | GAP-0508 | 12 | Publish contract/ledger-intake-map-v1.yaml with one row per consumed event type, a version label field, and the six rows of section 12.4. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03248 | RWB-P1-E1066-CON | DOR-RWB-P1-E1066-CON-12 | 16 | Add Given/When/Then rows for TC-P1-E1066-CON-01 to -06 on tab Story test cases; align RTM v7 section 18 test lists with section 18 of this story. |
| CDC-03258 | RWB-P1-E1066-CON | CG-ALL-2301 | 16 | Add rows TC-P1-E1066-CON-01 to TC-P1-E1066-CON-06 in the next version, with Given, When and Then copied from the criterion each covers (AC1 to AC6). |
| CDC-03279 | RWB-P1-E1066-OPS | CG-ALL-2307 | 16 | Add rows TC-P1-E1066-OPS-01 to TC-P1-E1066-OPS-06 with Given, When and Then copied from the criteria AC1 to AC6. |
| CDC-03302 | RWB-P1-E1067-CON | CG-ALL-2317 | 16 | Add rows TC-P1-E1067-CON-01 to TC-P1-E1067-CON-06, with Given, When and Then copied from AC1 to AC6 of this story. |

### 06 Data/Recovery Workbench Physical Schema v7 (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03257 | RWB-P1-E1066-CON | GAP-0585 | 12, 13 | Add ix_interaction_case_actor on (case_id, actor_ref) to the Flyway sequence beside ix_interaction_case_time, and publish actor as an optional query parameter of the read in the next versions. |
| CDC-03283 | RWB-P1-E1066-OPS | GAP-2254 |  | Record the required flags of event_code, actor_type, actor_ref, source_ref and case_seq as the legacy migration states them, and the TSD difference for these five columns. |
| CDC-03363 | RWB-P1-E1069-DB | CG-ALL-2345 | 1 | Record ck_contact_point_ext_type as a check constraint of contact_point_ext in the owning document, or confirm no LDM entry is needed |
| CDC-03385 | RWB-P1-E1069-DB | GAP-0905 |  | Record masking_rule.field_id as a dictionary field ID value with no cross-schema key. The dictionary stays with the P1 data-dictionary API and is not duplicated. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03264 | RWB-P1-E1066-OPS | DOR-RWB-P1-E1066-OPS-14 | header | Record the signed epic design sign-off in the epic design record; no sign-off is recorded in the story or the source documents. |
| CDC-03284 | RWB-P1-E1067-APP | DOR-RWB-P1-E1067-APP-14 | Header | Record the signed epic design sign-off for RWB-P1-E1067-APP; none is recorded in the story or source documents. |
| CDC-03308 | RWB-P1-E1068-APP | DOR-RWB-P1-E1068-APP-14 |  | Record the signed epic design for RWB-SVC-P1 covering RWB-P1-E1068-APP. |
| CDC-03359 | RWB-P1-E1069-DB | DOR-RWB-P1-E1069-DB-14 | header | Record the signed epic design sign-off for RWB-P1-E1069-DB in the epic design record |

### RWB-P2-E2001-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03402 | RWB-P1-E2001-APP | GAP-0590 | 4 | Step 10 derives key EFS:<efs_record_key>; the repeat-count split is not stated |
| CDC-03403 | RWB-P1-E2001-APP | GAP-0592 |  | Publish GET /entry-candidate-facts?businessDate= as the batched customer read (one row per candidate account key with personKey, productGroup, REC-05 resolution) and correct the per-candidate wording. |
| CDC-03410 | RWB-P1-E2001-APP | GAP-2259 |  | Publish the candidate page and EFS history page in RWB-P2-E2001-CON; publish the ledger append, REC-05 break and REC-01 result in the rwb-source-data contract; then name the paths in this story. |
| CDC-03412 | RWB-P1-E2001-APP | GAP-2463 | 12 | Confirm at contract review the repeat-count meter of rwb-decision, its dashboard exposure and response-header return, and the run-summary read by rwb-integration. |

### RWB-P1-E1066-OPS (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03230 | RWB-P1-E1066-APP | DOR-RWB-P1-E1066-APP-17 | none | Complete the writer deliverables (chart, migration step, flag, five series, three alerts) so the not-done dependency is closed before this build starts. |
| CDC-03239 | RWB-P1-E1066-APP | GAP-0506 | find it | Carry all deployment values, alert threshold, probe timing and incident route as named chart value sets per environment; fail the release when tr_interaction_append_only is missing. Values Not specified in the source documents. |
| CDC-03262 | RWB-P1-E1066-CON | GAP-0506 | 13 | Carry deployment values, alert threshold, probe timing and incident route for the ledger writer as named chart value sets per environment; fail the release when the append-only trigger is missing. Values not specified in the source documents (GAP-0506). |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03238 | RWB-P1-E1066-APP | GAP-0267 | find it | Owner column of the 29 interaction fields shows P1 rwb-source-data; P3 rwb-case reads the ledger through the P1 contract for the case timeline. |
| CDC-03269 | RWB-P1-E1066-OPS | DOR-RWB-P1-E1066-OPS-11 | 11 | Confirm the personal-data class of the P2 fields flagged by detcheck and align it with the story statement that none is carried. |
| CDC-03397 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-11 |  | Re-check the personal-data class of the P2 fields flagged by detcheck against the story statement that none is carried. |

### OTHER:RWB-PLT-DB (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03327 | RWB-P1-E1069-APP | GAP-3156 | 3 | Split the V0002 and V0003 grant block into one grant per service login, keeping ace_view_owner and the 30 views with P1. |
| CDC-03360 | RWB-P1-E1069-DB | GAP-3155 | 19 | Fix the per-service login names of the ACE DB stories and state them in the Environment and Deployment Design next version |
| CDC-03361 | RWB-P1-E1069-DB | GAP-3156 | 13 | Split the V0002 and V0003 grant block into one grant per service login, keeping ace_view_owner and the 30 views with P1 |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20859 | RWB-P1-E1069-APP | R-09196 |  | Per-service login names Not specified in the source documents (GAP-3155); owned by RWB-PLT-DB. Target docx not readable in this run. |
| CDC-20860 | RWB-P1-E1069-DB | R-22275 |  | 19 rwb_* login names Not specified in the source documents (GAP-0377). Grants already stated in stories BR3, BR4 and BR8. |
| CDC-20862 | RWB-P1-E1069-DB | R-28673 |  | Fixed 19 login names Not specified in the source documents (GAP-0904). rwb-access placeholder edit waits for the fixed name. |

### RWB-P1-E1066-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03223 | RWB-P1-E1066-APP | CG-ALL-2288 | 12.1 | The operation must be published in the owner's yaml. The story now names the append as POST /cases/{caseId}/interactions (GAP-2185). |
| CDC-03224 | RWB-P1-E1066-APP | CG-ALL-2289 | 12.1 | Publish GET /api/recovery/source-data/v1/interactions/{entryId} in the yaml through the CON story. |

### RWB-P1-E1066-CON; 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03240 | RWB-P1-E1066-APP | GAP-2254 | find it | Record the legacy required flags: event_code, actor_type, actor_ref, source_ref and case_seq required; idempotency_key, decision_log_id and corrects_entry_id optional. |
| CDC-03315 | RWB-P1-E1068-APP | GAP-0585 | 12, 13 | Publish actor as an optional query parameter of the read and index ix_interaction_case_actor on (case_id, actor_ref) in the next API specification and Physical Schema versions. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03270 | RWB-P1-E1066-OPS | DOR-RWB-P1-E1066-OPS-12 | 12.7 | Add rows TC-P1-E1066-OPS-01 to -06 to Test Cases v8, and align section 18 test lists with RTM v7. |
| CDC-03298 | RWB-P1-E1067-CON | DOR-RWB-P1-E1067-CON-12 | 7, 12.7, 16, 18 | Add TC-P1-E1067-CON-01 to -09 to Test Cases v8; align section 18 test lists to RTM v7; confirm legacy rows TC-E1-067-07, -08, -09 belong to RWB-P1-E1067-APP. |

### OTHER:TSD P3 v3; API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03294 | RWB-P1-E1067-APP | GAP-2072 | 7 | Correct interaction table and the two interaction endpoints to P1 rwb-source-data ownership, with rwb-case reading through the P1 contract; x-module P1. |
| CDC-03319 | RWB-P1-E1068-APP | GAP-2072 | header | Correct the interaction table and the two interaction endpoints to P1 ownership, with rwb-case reading through the P1 contract (x-module P1). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03305 | RWB-P1-E1068-APP | CG-ALL-2322 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer uses a published operation. |
| CDC-03306 | RWB-P1-E1068-APP | CG-ALL-2323 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies through the provider's CON story, or the consumer uses a published operation. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03325 | RWB-P1-E1069-APP | DOR-RWB-P1-E1069-APP-22 |  | Record the publication of the contract fake library version. No published version is in the sources (searched the contract-fake sections of the Service Story Files), so the value is Not specified in the source documents (DOR-RWB-P1-E1069-APP-22). |
| CDC-03405 | RWB-P1-E2001-APP | GAP-0651 |  | Mark TSD P2 v3 T5.2 and the P2 inbound exclusion as superseded by DP-05 and ADR-010; hold run summary in activity result, one local decision record and REC-01 row via P1. |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03338 | RWB-P1-E1069-APP | GAP-0566 | 3, 4, 7 | Publish the three read operations with their response fields and problem body in RWB-P1-E1069-CON. Record in the Service Contract Catalog that the view SQL, helper functions and conformance test are rwb-source-data's application slice, the login, grants, view owner and four extension tables are the database slice, and the 19-login proof is the wave 1 integration slice. Story side: helper functions now arrive with V0002 (Background) |
| CDC-03367 | RWB-P1-E1069-DB | GAP-0566 |  | Publish the three read operations with response fields and problem body in RWB-P1-E1069-CON; record that view SQL, helper functions and conformance test are the application slice, the DB slice and 19-login proof are the other two. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03346 | RWB-P1-E1069-APP | GAP-0568 |  | Publish login creation and credential policy, exact grant and revoke list, and order of the three migrations relative to the two view migrations; RWB-PLT-E1044-CON already in header dependencies. |
| CDC-03376 | RWB-P1-E1069-DB | GAP-0568 | 12 | Publish login creation and credential policy, exact grant and revoke list with the order of the three migrations, and record RWB-PLT-E1044-CON as platform dependency of per-service DB stories. |

### RWB-P1-E1069-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03348 | RWB-P1-E1069-APP | GAP-0549 |  | Add GET /accounts/{id} on /api/recovery/source-data/v1 (one hop, 2 s) and its answer schema; add the operation to TSD P1 v3 Appendix T-A.1 in the next version. |
| CDC-03349 | RWB-P1-E1069-APP | GAP-0553 |  | Fix the read-path answer: customer fields of v_ace_customer, one row per contact_key of v_ace_contact, one row per account of v_ace_ca_relation, four party_ext flags as optional object, absent not defaulted. |

### OTHER:TSD P4 T3.1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03354 | RWB-P1-E1069-APP | GAP-0902 | find it | Record the masking version naming rule with the pack owner (year and month, as matrix version PM-2026.12) so no migration invents a label. |
| CDC-03383 | RWB-P1-E1069-DB | GAP-0902 |  | Record the masking version naming rule with the pack owner (year and month, as PM-2026.12). Label MASK-2026.12 stays until the pack owner confirms the real label at load time. |

### RWB-P3-E2001-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03409 | RWB-P1-E2001-APP | GAP-2258 |  | Add an admin rerun operation on the rwb-case base answering 409 MSG-P2-006 while the business-date workflow runs, or drop the manual rerun. |
| CDC-03425 | RWB-P1-E2001-APP | NEWAC-RWB-P1-E2001-APP-AC12 |  | Add a criterion that a case status change the case model does not allow is refused. |

### RWB-P7-E2005-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03414 | RWB-P1-E2001-APP | GAP-2464 | 12 | Fix parameters caseId, decision, ruleId, ruleVersion, approver, from, to, page and size, page size 1 to 500, ordered by decided_at, for GET /decision-log. |
| CDC-03416 | RWB-P1-E2001-APP | GAP-2462 | 12 | Add element lists of actions and outcome to the DecisionLogEntry resource, and the record shape to RWB-PLT-E1027-CON at contract review. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03423 | RWB-P1-E2001-APP | GAP-2468 | Header | Six platform H contracts carried in the Contract dependencies row |
| CDC-03424 | RWB-P1-E2001-APP | GAP-1335 | Header | Contract dependencies row carries the platform CON contracts |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_case.sql (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20557 | RWB-P1-E1066-OPS | R-22264 |  | The 12.7 column list for interaction_link was not found in the project documents searched, and the table is not in rwb_case.sql. |
| CDC-20558 | RWB-P1-E1066-OPS | R-22264 |  | Same change as the other R-22264 item. The 12.7 column list is not in the searched sources, so no table is added. |

### RWB-P3-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03228 | RWB-P1-E1066-APP | DOR-RWB-P1-E1066-APP-10 | none | Add empty, loading, error and no-access states for screen SCR-03 (recording screen) to that story; this story owns no screen. |

### RWB-P6-E1055-CON; RWB-P6-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03232 | RWB-P1-E1066-APP | GAP-0578 | 7 | Remove the delivery-entry write from section 12.2 row 3 of the contract and from section 4 step 7 of the app story; rwb-comms writes only the dispatch entry. |

### OTHER:P7 functional specification (RWB P7 FSD) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03233 | RWB-P1-E1066-APP | GAP-1612 |  | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012. |

### OTHER:rwb-case and rwb-integration module specifications (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03234 | RWB-P1-E1066-APP | GAP-1511 |  | Remove their ledger table definitions; rwb-case reads the timeline and rwb-integration writes intake outcomes through this service's contract. |

### RWB-P1-E1066-CON; RWB-P6-E2021-CON; RWB-P3-E2021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03241 | RWB-P1-E1066-APP | GAP-2182 | find it | Settle one case-scoped path family for the ledger (POST and GET /cases/{caseId}/interactions) and realign the fake and the consumed row to it. |

### RWB-ITG-E1055-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03250 | RWB-P1-E1066-CON | GAP-1097 | find it | Consume pod records and freshness at GET /api/recovery/source-data/v1/data-products/DP07/records and GET /api/recovery/source-data/v1/data-products/freshness, one hop, 2 s budget. |

### OTHER:Recovery Workbench P7 functional specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03251 | RWB-P1-E1066-CON | GAP-1612 | find it | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; rwb-source-data owns the ledger. |

### OTHER:rwb_case schema, table interaction_link (case-side story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03252 | RWB-P1-E1066-CON | GAP-2255 | 12.7 | Approve interaction_link in rwb_case with the columns of 12.7, the three states, one key per action reference and the append-before-commit order; the sequence owner assigns the Flyway version. |

### RWB-P1-E1016-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03254 | RWB-P1-E1066-CON | GAP-2181 | Target reading | Publish the DP02 contact-and-consent row and vocabulary in RWB-P1-E1016-CON; add UNSERVED to LOV-SEND-STATUS with its version, or confirm the FAILED mapping with the ACE result code. |

### RWB-P6-E2021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03255 | RWB-P1-E1066-CON | GAP-1089 |  | Fix the WIN file name, record layout, acknowledgement fields and INT-15 proof result record with the WIN owner and rwb-integration owner, and publish them there. |

### RWB-P1-E1066-CON; RWB-P1-E1016-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03256 | RWB-P1-E1066-CON | GAP-1070 |  | Ledger record is POST /cases/{caseId}/interactions; a delivery change is a second append per AC4, not an update. |

### RWB-P1-E1066-APP; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03263 | RWB-P1-E1066-CON | GAP-2254 | 13 | Record the difference between the legacy NOT NULL columns and the TSD optional columns; keep the required flags of the five values the ledger cannot do without. |

### OTHER:Functional Specification P7 (FSD P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03272 | RWB-P1-E1066-OPS | GAP-1612 | find it | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012. |

### OTHER:Case module specification and integration module specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03273 | RWB-P1-E1066-OPS | GAP-1511 | find it | Remove the interaction table and ledger intake rule table definitions; reference the rwb-source-data ledger contract with one writer per ledger. |

### OTHER:rwb-case schema design (rwb_case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03277 | RWB-P1-E1066-OPS | GAP-2255 | find it | Approve table interaction_link in rwb_case with the section 12.7 columns, the three states, one key per action reference, and the append-before-commit order; the sequence owner assigns the Flyway version. |

### OTHER:Source for deployment values, thresholds and routes (not specified in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03282 | RWB-P1-E1066-OPS | GAP-0506 | 8 | BR5 states the values are not specified in the source documents; no invented rule added |

### RWB-P1-E1066-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03288 | RWB-P1-E1067-APP | DOR-RWB-P1-E1067-APP-17 | Header | Reach Done before RWB-P1-E1067-APP starts; one build dependency is not done. |

### OTHER:Functional specification P7 (FSD P7) and wave 1 contract review (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03289 | RWB-P1-E1067-APP | GAP-1612 | 7 | Confirm rwb-source-data owns the one ledger (table, write, deduplication, ordered read, retention class) and rwb-case serves the timeline; re-issue FSD P7 without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012. |

### OTHER:Technical specification P5 (T5.3 header schema) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03291 | RWB-P1-E1067-APP | GAP-1055 | 8 | Add the DocumentStored idempotency key, derived from the document row, as a CloudEvents extension attribute read from configuration, with the key format stated. |

### OTHER:P3 screen specification (SCR-09) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03297 | RWB-P1-E1067-CON | DOR-RWB-P1-E1067-CON-10 | find it | Add empty, loading, error and no-access states for SCR-09. |

### OTHER:FSD P7 functional specification (ledger features and requirements) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03299 | RWB-P1-E1067-CON | GAP-1612 | find it | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; confirm at wave 1 review that rwb-source-data owns the one ledger. |

### OTHER:API and event specification of rwb-case (CloudEvents attribute names) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03300 | RWB-P1-E1067-CON | GAP-1056 | 7 | AC2 states that the actor and the key are read from the envelope; the attribute names are not applied. |

### OTHER:API and event specification of rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03301 | RWB-P1-E1067-CON | GAP-2257 | 7 | AC2 records the key shape and the envelope read; no attribute name is applied. |

### OTHER:Contract stories named in the header dependencies (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03309 | RWB-P1-E1068-APP | DOR-RWB-P1-E1068-APP-21 | - | Each CON story this build depends on must reach Done before this story's contract is published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03310 | RWB-P1-E1068-APP | DOR-RWB-P1-E1068-APP-8 | 12.2 | Resolve CG-ALL-2322, CG-ALL-2323 and CG-ALL-2324: publish both rwb-access paths and remove the channel enum. |

### OTHER:Functional specification P7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03313 | RWB-P1-E1068-APP | GAP-1612 | 13 | Remove FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35 from the ledger build; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; rwb-case serves the timeline over its contract. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03317 | RWB-P1-E1068-APP | GAP-0586 | 4 | Open one row in the P4 contract set for the access-log write operation, its payload and its retry rule. |

### RWB-P1-E1066-CON; RWB-P1-E1066-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P2-E2034-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03321 | RWB-P1-E1068-APP | GAP-2185 | 12.1 | Settle one case-scoped path family for the ledger in RWB-P1-E1066-CON; realign the append row and fake of RWB-P1-E1066-APP and the Ownership Map and P2 rows to it. |

### Epic design record; OTHER:EP01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03323 | RWB-P1-E1069-APP | DOR-RWB-P1-E1069-APP-14 | header | Record the signed epic design sign-off for RWB-P1-E1069-APP. |

### RWB-PLT-E1027-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-E1037-CON; RWB-PLT-E1044-CON; RWB-PLT-N001-CON; RWB-P3-E1042-CON; RWB-P3-E1043-CON; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03324 | RWB-P1-E1069-APP | DOR-RWB-P1-E1069-APP-21 | 4 | Bring the CON stories this story depends on to Done, then publish the contract for this story's ACE read contract. |

### OTHER:RWB-PLT-DB; OTHER:Environment and Deployment Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03326 | RWB-P1-E1069-APP | GAP-3155 | 3 | Fix the per-service login names in the ACE DB stories of RWB-PLT-DB and state them in the next version of the Environment and Deployment Design. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03335 | RWB-P1-E1069-APP | CG-ALL-2339 | 11 | Record ai_recommended_plan as an ACE source table in the owning document, or use its dictionary name in the story |

### OTHER:Screen Specifications v1 (SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03336 | RWB-P1-E1069-APP | DOR-RWB-P1-E1069-APP-10 | 15 | This is a back-end read story. Section 15 records the SCR-44 states as not specified; the screen's owner must define them. |

### OTHER:TSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03343 | RWB-P1-E1069-APP | GAP-0567 |  | Carry the Architecture v5 REST contract (base /api/recovery/source-data/v1, 2 s client budget, slides 15 and 41) into T2 and T5.2; keep AceSourceReadRepository internal; add change note. |

### OTHER:TSD P1 v3 (and FSD P1 v3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03344 | RWB-P1-E1069-APP | GAP-0569 |  | Rename service role to rwb_source_data; state per-service schema and USAGE on schema recovery in Service Template Specification row; record rename in Change Register against DP-02. |

### OTHER:rwb-access ACE masking pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03345 | RWB-P1-E1069-APP | GAP-0903 |  | Publish, for each personal field ID, the roles that see it unmasked as masking_rule rows, approved by the Compliance and PDPA officer and the security administrator. |

### RWB-P2-E2007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03347 | RWB-P1-E1069-APP | GAP-0596 |  | Answer the three Section B fields as fieldState AVAILABLE or NOT_AVAILABLE with no value on NOT_AVAILABLE; name flag rwb.dataengine.booking-facts, kept off until the Section B migration is applied; record in next TSD P1. |

### RWB-P1-E1069-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03350 | RWB-P1-E1069-APP | GAP-0556 | find it | Publish the customer and party answer schema with field names and not-found and stale shapes; record RWB-P1-E1069-APP and RWB-P1-E1069-DB as preconditions in the Dependency Map without an H edge; fix the read-path switch key and its off behaviour in the Service Template Specification. |

### OTHER:Security and Access Design v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03352 | RWB-P1-E1069-APP | GAP-2035 | find it | Write section 7 per service: one login rwb_<name> per service with grants on its own schema only; rwb_source_data is the only holder of the view grant; replace the recovery_svc row with a service login isolation row. |

### OTHER:FSD P1 A1.3; OTHER:TSD P1 T6.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03353 | RWB-P1-E1069-APP | GAP-0570 | find it | ACE team lead publishes the 21 Tier 1 table names or names the 22nd table; the legacy grant block stays the enumeration until then. |

### RWB-P1-E1069-DB; OTHER:Environment and Deployment Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03355 | RWB-P1-E1069-APP | GAP-0904 | find it | Fix the 19 per-service login names and replace the rwb-access login placeholder in the privilege test with the fixed name. |

### OTHER:TSD P4 T3.1; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03356 | RWB-P1-E1069-APP | GAP-0905 | find it | Record that masking_rule.field_id is a dictionary field ID held as a value with no cross-schema key, and keep the dictionary with P1's data-dictionary API without duplication. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:TSD P4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03357 | RWB-P1-E1069-APP | GAP-0906 | find it | Publish the per-service module map with an explicitly empty source-object list for the 18 services that read no view, and fix the BND-6 failure wording once in the service template. |

### OTHER:Legacy dependency trace sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03358 | RWB-P1-E1069-APP | GAP-3233 | find it | Keep the five Not carried rows (RWB-E1-056 to RWB-E1-007, RWB-E1-015, RWB-E1-069; RWB-TE-009 to RWB-TE-004; RWB-TE-010 to RWB-TE-003) visible with Status Not carried. Add an X row only if the run books or harness waits for the named story. |

### OTHER:recovery_views.sql (ACE view definitions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03369 | RWB-P1-E1069-DB | GAP-0110 |  | Keep the 30 v_ace_* views in schema recovery, read only; move v_data_dictionary to rwb_source_data. |

### OTHER:Handling tab of the source workbook (v4 rows 7 and 22) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03371 | RWB-P1-E1069-DB | GAP-0263 |  | Only rwb_source_data holds SELECT on the 30 views; other services read via P1 REST or Temporal; read audit via ACE Common PII logging. |

### OTHER:Environment and Deployment Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03372 | RWB-P1-E1069-DB | GAP-0377 |  | Issue the 19 login names; the other 18 logins get no privilege on public or the views; BND-6 becomes two build rules. |

### OTHER:TSD P1 (next version, change note on T2 and T5.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03373 | RWB-P1-E1069-DB | GAP-0567 |  | Adopt REST contract on base /api/recovery/source-data/v1 with 2 s client budget; keep AceSourceReadRepository internal; carry wording to TSD P1 change note. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03374 | RWB-P1-E1069-DB | GAP-0569 |  | Rename service role to rwb_source_data; state per-service schema and USAGE on schema recovery in one row; record rename against DP-02. |

### OTHER:rwb-access ACE masking pack (masking_rule rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03375 | RWB-P1-E1069-DB | GAP-0903 |  | Publish, for each personal field ID, the roles that see it unmasked, as masking_rule rows approved by the Compliance and PDPA officer and the security administrator, not as a matrix column. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03377 | RWB-P1-E1069-DB | GAP-3194 | 18 | Raise one ACE DB story per service lacking one (S2, S4, S5, S6, S7, P6, P8) for the column drop, or attach the drop to the creating APP story; cite it on row 121. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; RWB-P1-E1069-APP; 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03378 | RWB-P1-E1069-DB | GAP-0556 | 5 | Publish customer and party answer schema with field names and not-found and stale shapes; record APP and DB stories as preconditions without an H edge; fix read-path switch key and off behaviour. |

### RWB-P1-E1016-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03380 | RWB-P1-E1069-DB | GAP-0484 | 12 | Deliver only indexes, read model v_data_product_catalog, DPA-2026.11 seed, conformance check and schema checks; create no table already created by E1001-APP or E1069-DB. |

### OTHER:FSD P1 A1.3 and TSD P1 T6.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03382 | RWB-P1-E1069-DB | GAP-0570 |  | Publish the Tier 1 ACE table list (the 21 names, or the name of the 22nd table), confirmed by the ACE team lead. |

### OTHER:Platform DB story and Environment and Deployment Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03384 | RWB-P1-E1069-DB | GAP-0904 |  | Fix the 19 per-service login names and replace the rwb-access login placeholder in the privilege test with the fixed name. |

### OTHER:Per-service module map and service template (BND-6 wording) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03386 | RWB-P1-E1069-DB | GAP-0906 |  | Publish the module map with an explicitly empty source-object list for the 18 services that read no view. Fix the BND-6 failure wording once in the service template. |

### OTHER:Story dependencies v5 trace workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03387 | RWB-P1-E1069-DB | GAP-3233 |  | Keep the five version 4 dependency rows visible as Not carried. Add an X row later only if run books or the harness wait for the named story. |

### RWB-P1-E2001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03390 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-16 Size | Header | Size row records 'Not specified in the source documents' with no invented value |

### RWB-P1-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03391 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-21 | find it | Create the CON story for the rwb-source-data contract that publishes the two operations; then list it under Contract dependencies. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03392 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-22 | find it | Publish a contract fake library version covering GET efs-history and GET entry-candidate-facts, and record its version. |

### OTHER:Functional Specification Document P3, section A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03394 | RWB-P1-E2001-APP | GAP-1549 | find it | Restate the ACE read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### OTHER:Screen specification holding SCR-04 and SCR-45 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03396 | RWB-P1-E2001-APP | DOR-RWB-P1-E2001-APP-10 |  | Add empty, loading, error and no-access states to SCR-04 and SCR-45; this story owns no screen. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03400 | RWB-P1-E2001-APP | GAP-3175 | 4 | List LoadCompleted (EV-26) as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1. |

### OTHER:Recovery Workbench Batch and Scheduling (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03401 | RWB-P1-E2001-APP | GAP-3176 |  | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### OTHER:EFS hand-over harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03404 | RWB-P1-E2001-APP | GAP-0388 |  | Hold the composite route paths and merge order, harness repository, SIT and UAT environments, seeding, evidence format, retention and pass/fail gate as data, agreed at the wave 2 entry check. |

### OTHER:contract/handover-run-activities.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03406 | RWB-P1-E2001-APP | GAP-0652 |  | Fix the workflow, nine activities, twelve summary elements and retry policy; fix the P1 and P3 consumed element shapes; publish the six fakes from owners' OpenAPI and fail build on drift. |

### RWB-P2-E2001-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03407 | RWB-P1-E2001-APP | GAP-0653 |  | Keep the chart, consumer group, registration, migration, six series, four alerts and runbook entries there; environment values in a values file; missing message ids as placeholders; on-call rota reviews the runbook. |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03411 | RWB-P1-E2001-APP | GAP-2260 | Header | Mark interaction object T3.1 as owned by rwb-source-data and re-scope the P3 ledger story to the P1 contract. Story already writes only through the contract. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03413 | RWB-P1-E2001-APP | GAP-2466 | Header | Record the move of the EFS history append from the P7 decision module to the rwb-source-data ledger under DP-18. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03415 | RWB-P1-E2001-APP | GAP-1332 | 12 | Fix the DecisionRecorded payload and inputs snapshot with business date, queue and owner identifiers, hand-over reference, actions and composite idempotency key; AsyncAPI of rwb.decision-record.v1 to match. Confirm with hand-over contract owner before wave 2 build. |

### RWB-PLT-E1047-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03417 | RWB-P1-E2001-APP | GAP-2262 | Header | Fix the CaseCreated envelope and retry and dead-letter settings of rwb.case.events.v1 with RWB-PLT-TE006-CON; limit payload to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate and dpdAtEntry; define resume of a held run. |

### RWB-P2-E2034-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03418 | RWB-P1-E2001-APP | GAP-2186 | 12 | Realign the two consumed rows (EFS contact-outcome read and contact-key read) to the P1 base operation paths once published; publish contact-fact read on P1 base with path and masked members. |

### OTHER:RWB-PLT-OBS; RWB-P7-E1027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03420 | RWB-P1-E2001-APP | GAP-2465 |  | Register the ingest lag of rwb.decision-record.v1 into the ledger as a metric with its threshold as a parameter; route the gap alert to RW-PLATADM. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:database platform story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03421 | RWB-P1-E2001-APP | GAP-1334 |  | Publish the per-service login of rwb_decision; fix the LedgerChainCheckWorkflow, its activities and the JOB-14 Temporal Schedule identifier before wave 2 build. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03422 | RWB-P1-E2001-APP | GAP-2467 |  | Confirm the hand-over entry decision value with RW-COE and load it as a LOV-DECISION reference row. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0014 | Table inventory does not cover the v5 schema-per-service model and the FK cuts are empty | Solution architect and ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0110 | The map does not say which schema holds the 30 ACE views | ACE team | Resolved (directive) |
| GAP-0111 | The source grants use placeholder roles and do not create the 19 logins | ACE team | Resolved (directive) |
| GAP-0259 | The 30 ACE source views have no owner in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0263 | One recovery identity reads the ACE views; the target has one login and one schema per service | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0267 | The interaction ledger is defined by the case module but the Ownership Map gives it to P1 | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0358 | Matrix load owner, masking read path and the platform library boundary are not named for the target | Solution architect | Resolved (directive) |
| GAP-0375 | The cross-service ledger-write contract and its failure mapping are not defined | Solution architect | Resolved (directive) |
| GAP-0376 | The event-to-ledger map, the cross-topic ordering rule and the duplicate key after the split into per-service topics are not defined | Solution architect | Resolved (directive) |
| GAP-0377 | The 19 login names, the grant matrix on the 30 ACE views and the two-part boundary rule after the schema split are not stated | ACE database administrator | Resolved (directive) |
| GAP-0388 | EFS hand-over harness: repository, environments, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0484 | The DB slice of this legacy key cannot deliver the table DDL, because two other stories already create the tables | ACE database lead | Resolved (directive) |
| GAP-0504 | The append path, its authorisation handling and its 404 semantics are a target choice, not a legacy value | Solution architect | Resolved (directive) |
| GAP-0505 | The exact ledger resource path, the login wording and the field-level required flags are not specified | Tech lead | Resolved (directive) |
| GAP-0506 | No deployment value, alert threshold, probe timing or incident route exists for the ledger writer | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0507 | The mapping of the document fact and the timer fact onto the target event types is not specified | Solution architect | Resolved (directive) |
| GAP-0508 | The format and version label of the ledger intake map are not specified | Tech lead | Resolved (directive) |
| GAP-0547 | The account and arrears read path is given as a legacy row, not as a deliverable with an answer shape or a cut-off | Tech lead | Resolved (directive) |
| GAP-0549 | The account operation named by the architecture is absent from the TSD P1 endpoint inventory, and the answer field names are in no module specification | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0553 | The read path that replaces the migration is described in one legacy row only: no source fixes the fields the answer carries, the join of a person to many contact points, or the use of the two extension tables beyond their column list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0556 | The read operation, its request and answer field names, and the feature switch of the read path are owned elsewhere or named by no source, while the story must still build and be switched | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0557 | RWB-P1-E1001-APP: schema-split mechanics, login name, extension-table delivery boundary and Arch v5 against FSD and TSD P1 | Solution architect | Resolved (directive) |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0567 | The ACE read is a REST contract of rwb-source-data in Architecture v5 and an in-process Java interface in TSD P1 and legacy RWB-E1-069 | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0568 | rwb-source-data database slice: who creates the login and holds its credential, the exact grant names, the position of the three grant migrations on the sequence, and the platform sequence dependency of a Day-1 database story are not specified | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0569 | The service role is recovery_svc on one recovery schema in TSD P1 and legacy RWB-E1-069, and a per-service login rwb_source_data with its own schema under Architecture v5 | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0570 | The number of Tier 1 ACE tables is 21 in legacy RWB-E1-069 and 22 in FSD P1 and TSD P1, and the grant list is enumerated only in the legacy story | ACE team lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0578 | No source settles who writes the delivery entry on the interaction ledger, nor which case the entry belongs to: the legacy story writes it in rwb-comms, the contract and the app story of rwb-comms say rwb-comms calls the ledger writer, the work package of this key gives the write to rwb-source-data, and the pod row carries an account key and no case | Solution architect | Resolved (directive) |
| GAP-0580 | No source says where the repeat of a proof-of-delivery read is counted when the read writes no second entry: R-UNI-40 asks for the hit to be recorded and names no counter, and the two candidate counters belong to two different mechanisms | Data architect | Resolved (directive) |
| GAP-0582 | The interaction read is x-module P3 in the API specification and the TSD, while the ledger ruling gives the ledger and its read to P1 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0583 | The legacy read answers 404 for a case out of scope while the case contract distinguishes out of scope from missing | Tech lead | Resolved (directive) |
| GAP-0584 | Two sources give the masking of a ledger field to two different services | Tech lead | Resolved (directive) |
| GAP-0585 | The actor filter and the index behind it are legacy additions that the published endpoint inventory does not carry | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0586 | The PII access-log write has a rule and a metric but no contract, path or payload | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0587 | The edge rule forbids a service that calls another service, and this read calls two | Solution architect | Resolved (directive) |
| GAP-0589 | The history read is one operation or a paged read, and the HTTP answer of a held read, are stated by no source | Solution architect, P1 | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0592 | No source splits the hand-over facts between the candidate rule and the borrower and product-group facts, and the run's contract names a per-candidate customer read | Solution architect, P1 and P2 | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0596 | How the read answers the three Section B columns, and which flag holds it back, is stated nowhere | Data architect | Resolved (directive) |
| GAP-0651 | rwb-integration EFS hand-over: the mount of the step, the split across four owners, the consumed contract paths, the run summary store and the level of the decision record are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0652 | rwb-integration EFS hand-over contract: the activity contract, the consumed element shapes, the provided surface and the fakes have no source text | Tech lead | Resolved (directive) |
| GAP-0653 | rwb-integration EFS hand-over deployment: the values, the alert identifiers, the dashboard series and the runbook have no source | DevOps lead | Resolved (directive) |
| GAP-0902 | rwb-access ACE masking pack: no source names the masking version label | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0903 | rwb-access ACE masking pack: no source holds the roster of roles that see a personal field unmasked | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0904 | rwb-access: the per-service database login name is named by no source | ACE team lead and ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0905 | rwb-access: unclear whether this service may hold masking rows that key on the P1 field catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0906 | rwb-access: the boundary rule has no allowed-object list and no build-log wording for this service | Tech lead, rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1055 | The exact idempotency-key format of rwb.document.DocumentStored.v1 is not stated for the target topic | Tech lead | Resolved (directive) |
| GAP-1056 | The CloudEvents attribute names that carry the actor and the occurred time on rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
| GAP-1057 | The retry limit applied to the JOB-11 outbox relay of rwb-document is not stated | Platform administrator | Resolved (directive) |
| GAP-1058 | The JSON Schema registry subject name and the AsyncAPI document location for rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
| GAP-1070 | The interaction ledger write and the contact-point failed count are not named in this key's contracts | Solution architect | Resolved (directive) |
| GAP-1089 | The WIN dispatch file, its acknowledgement and the INT-15 proof result record have no layout and no owning operation in the sources | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1097 | The pod and batch-status contract elements are not named in RWB-P1-E1066-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1332 | Envelope and payload element names of DecisionRecorded, and the shape of the inputs snapshot | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1333 | Answer field set and business-date filter of the decision-log read, and the screen that shows an entry beside the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1334 | Per-service login of rwb_decision, the chain-check workflow and activity names, and the Schedule identifier of JOB-14 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1505 | The Section B views and every Tier 2 feature depend on ACE additions that the ACE team has not accepted | ACE team lead | Resolved (directive) |
| GAP-1509 | Which function writes the appraisal stale flag and age is not set | Business analyst, P1 and S1 | Resolved (directive) |
| GAP-1511 | Two module specifications define the ledger tables and the ownership map leaves both here | Solution architect | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2040 | The view conformance test of RWB-E1-069 is split across two services | P1 rwb-source-data with the ACE DBA | Resolved (directive) |
| GAP-2072 | The interaction ledger is claimed by rwb-case and by rwb-source-data | Service owner P1 rwb-source-data with P3 rwb-case | Resolved (directive) |
| GAP-2102 | The deck gives the interaction ledger to one module and names no reader | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2181 | The DP02 contact-and-consent row, the consent vocabulary, the members of the letter append and the unserved status are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2182 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2185 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2186 | The EFS outcome read and the contact-fact read that the channel consumer calls are named by interface only, with no path, parameter or owning story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2254 | The ledger columns are required in the legacy migration and optional in the TSD | rwb-source-data contract owner (TechX) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2255 | The case-side link table, its states, its key and the write order are not in the sources | TechX | Resolved (directive) |
| GAP-2256 | API-P3-015 and API-P3-014 of the TSD have no rwb-case counterpart after the split | rwb-source-data contract owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2257 | The CloudEvents key and actor attributes, the idempotency-key format, the relay publish limit and the registry subject of the case topic are not in the sources | rwb-case contract owner and the platform event library owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2258 | No rerun operation for the entry run after JOB-02 becomes a workflow | TechX | Resolved (directive) |
| GAP-2259 | Paths and payloads of the P2 hand-over and P1 ledger contracts | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2260 | Interaction ledger ownership conflicts with the legacy write and the P3 data model | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2262 | CaseCreated payload and the resume of a held run are not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2462 | The inner shape of the actions and outcome columns of a hand-over decision entry is not in any source | Solution architect with the data steward | Resolved (directive) |
| GAP-2463 | Where the R-UNI-40 repeat count of a hand-over record is kept and reported is not stated | P7 and P2 solution architects | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2464 | No source fixes the query parameters and paging of GET /decision-log | P7 contract owner | Resolved (directive) |
| GAP-2465 | The five-minute ledger completeness target has no named alert, owner or threshold | Platform observability owner with the P7 solution architect | Resolved (directive) |
| GAP-2466 | The legacy story puts the EFS history append in the decision module while the Ownership Map and DP-18 put the interaction ledger in rwb-source-data | Solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2467 | The exact LOV-DECISION value of the hand-over entry is not stated | P7 business analyst with RW-COE | Resolved (directive) |
| GAP-2468 | The story line carries one C row and no H row while the pattern table adds six platform H rows and the guard | Coordinator of the realignment with the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3155 | The per-service login names are not fixed in any source | ACE DB lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3156 | The V0002 and V0003 grant block gives one monolith login, not one login per service | ACE DB lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P1-E1066-APP | skipped AC ID | 108 | missing: AC1, AC2, AC3, AC4, AC8 |
| RWB-P1-E1066-CON | skipped AC ID | 93 | missing: AC7, AC8 |
| RWB-P1-E1066-OPS | skipped AC ID | 100 | missing: AC7, AC8 |
