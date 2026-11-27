# RWB-SVC-P2 rwb-integration (Integration) - review pack, part 2 of 4 (RWB-P2-E2001-CON to RWB-P2-E2006-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 100 |
| Cross-document (pending in another document) | 205 |
| Not applied (value not in the sources) | 7 |
| Open business decisions | 24 |
| Register gaps linked | 71 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P2-E2001-CON | 17 | 42 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2001 CON EFS hand-over with full history - contract v2.md |
| RWB-P2-E2001-OPS | 15 | 34 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2001 OPS EFS hand-over with full history - deployment v2.md |
| RWB-P2-E2002-APP | 16 | 27 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2002 APP ACE plan status on the case v2.md |
| RWB-P2-E2002-CON | 9 | 25 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2002 CON ACE plan status on the case - contract v2.md |
| RWB-P2-E2002-OPS | 13 | 25 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2002 OPS ACE plan status on the case - deployment v2.md |
| RWB-P2-E2003-APP | 19 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2003 APP Customer's other products on the case v2.md |
| RWB-P2-E2006-APP | 11 | 33 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2006 APP Credit approval pack for NLEADS v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P2-E2002-APP | R-10053 | CG-ALL-3069 | Script gap | Product owner | Open decision DL21 has no assumption | Owner rules DL21; until then build on the recommended option. |
| RWB-P2-E2002-CON | R-10056 | CG-ALL-3076 | Script gap | Product owner | Open decision DL21 has no assumption | Owner rules DL21; until then build on the recommended option. |
| RWB-P2-E2003-APP | R-10058 | CG-ALL-3088 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P2-E2006-APP | R-10063 | CG-ALL-3103 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2001-ITG, RWB-P1-E1011-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22306 | GAP-0591 | Register gap | Data steward and data product owner, P1 | The REC-05 break list row for a hand-over key is defined only for keys on an existing Workbench table, not for a candidate that has no row yet | Answer the break in the candidate-facts read as {check: REC-05, keyType: PERSON_KEY or ACCOUNT_KEY, key: <value>} with resolution HELD, write no row and invent no fact, and let RWB-P1-E1011-APP's REC-05 step carry the row for the business date so the data steward and the ACE team read one list. Fix the answer in RWB-P2-E2001-CON. |
| RWB-ITG-E2001-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22309 | GAP-0588 | Register gap | Data steward and data product owner, P1 | The collection period of an account's EFS history is named by no source, so the boundary of the history read is undefined | Fix the period as the EFS assignment window of the account: it opens at v_ace_efs_assignment.assignment_start_date and closes at assignment_end_date, or at the business date of the read for the open assignment; when the account has no assignment row the period opens at its earliest contact_at. Publish the rule in RWB-P2-E2001-CON with the answer so the run and this service read the same boundary, and ask the data steward to confirm it with the ACE team before wave 2 exit. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-AD004-APP, RWB-P4-E2003-APP | R-22343 | GAP-0910 | Register gap | Compliance and PDPA officer (RW-COMPLY) | The roster of roles that see the other-products account number unmasked is an assumption of the legacy story | Confirm the five clear roles and that every other role holding Case record R is masked, then load the roster through the masking load path of RWB-P4-AD004-APP. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-E2003-APP | R-28706 | GAP-0911 | Register gap | Compliance and PDPA officer (RW-COMPLY) | No source fixes the masking version label in force for the wave-2 release, or the rule for two valid versions on one day | Name the masking version of the wave-2 release in the masking load file and confirm the latest-valid-from rule for a day with two valid versions. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-E2003-APP | R-28707 | GAP-0912 | Register gap | Data steward and data product owner (RW-DATASTEW) | No source states whether the other-products account number is the only personal field of the panel | Record the personal-data classification of the seven v_ace_party_product fields in the data dictionary, and add a masking row or an explicit unmasked false for any further personal field. |
| RWB-P2-E2002-APP | R-33397 | ASM-ALL-3069 | Script assumption |  | Built on the recommended option of DL21: A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead rules DL21 |
| RWB-P2-E2002-CON | R-33398 | ASM-ALL-3076 | Script assumption |  | Built on the recommended option of DL21: A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead rules DL21 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P2-E2002-CON | R-04803 | DOR-RWB-P2-E2002-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed EP02 epic design record in the source .md files (DoR v3 item 14, DT05, Ways of Working, Decision Log v11). Sign-off cannot be stated without inventing it. |
| RWB-P2-E2002-CON | R-04804 | DOR-RWB-P2-E2002-CON-16 | header | Definition of Ready item 16 Size: Fail | Size row added reading Not specified in the source documents. No size invented; the item stays open until the squad sizes the story at refinement. |
| RWB-P2-E2002-CON | R-15619 | DOR-RWB-P2-E2002-CON-7 | 11 | Definition of Ready item 7 Data: Partial | BR Field ID column added, with all 7 rows Not specified in the source documents. The item stays open until the field IDs are supplied. |
| RWB-P2-E2006-APP | R-04817 | DOR-RWB-P2-E2006-APP-14 | header | Definition of Ready item 14 Epic design: Fail | The epic design sign-off is a delivery record that story text cannot supply. The placeholder only records that it is open. |
| RWB-P2-E2006-APP | R-04818 | DOR-RWB-P2-E2006-APP-16 | header | Definition of Ready item 16 Size: Fail | Size is set at refinement and no size is invented. The placeholder only records that it is open. |
| RWB-P2-E2006-APP | R-04819 | DOR-RWB-P2-E2006-APP-21 |  | Definition of Ready item 21 Contract published: Fail | Needs the CON stories to be Done, a delivery record not in the story or sources. Story text cannot supply it. Header lists only RWB-P3-E1043-CON and RWB-P3-E2004-CON. |
| RWB-P2-E2006-APP | R-04820 | DOR-RWB-P2-E2006-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake version is recorded in the story, its DoR review or 05 Technical architecture. Writing one would invent a version number. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04578 | RWB-P2-E2001-CON | CG-ALL-3036 | 12.5 | Add a Workflows row for EfsHandoverWorkflow: rwb-integration, task queue rwb-integration, started by AceDataReady, workflow ID efs-handover-<businessDate>, activities as in RWB-P2-E2001-CON 12.5. |
| CDC-04587 | RWB-P2-E2001-CON | CG-ALL-3040 | 12.5 | Add an Activities row for buildGroups, or confirm a catalogued activity to use in its place. |
| CDC-04588 | RWB-P2-E2001-CON | CG-ALL-3041 | 12.5 | Add an Activities row for createOrLinkCase, or confirm a catalogued activity to use in its place. |
| CDC-04589 | RWB-P2-E2001-CON | CG-ALL-3042 | 12.5 | Add an Activities row for appendEfsHistory, or confirm a catalogued activity to use in its place. |
| CDC-04590 | RWB-P2-E2001-CON | CG-ALL-3043 | 12.5 | Add an Activities row for writeRunSummary, or confirm a catalogued activity to use in its place. |
| CDC-04591 | RWB-P2-E2001-CON | CG-ALL-3044 | 12.5 | Add an Activities row for recordRunDecision, or confirm a catalogued activity to use in its place. |
| CDC-04592 | RWB-P2-E2001-CON | CG-ALL-3045 | 12.5 | Add an Activities row for releaseRunLock, or confirm a catalogued activity to use in its place. |
| CDC-04615 | RWB-P2-E2001-CON | GAP-1334 | find it | Fix workflow LedgerChainCheckWorkflow, activities readDayEntries, verifyChain, reportBreak and Schedule identifier for JOB-14 at 02:00 in queue rwb-decision; publish rwb_decision login with the database platform story. |
| CDC-04619 | RWB-P2-E2001-OPS | CG-ALL-3055 | 12.5 | Add to Workflows: EfsHandoverWorkflow, rwb-integration, queue rwb-integration, started by AceDataReady, ID efs-handover-<businessDate>, one run per business date, with its nine activities. |
| CDC-04623 | RWB-P2-E2001-OPS | DOR-RWB-P2-E2001-OPS-8 | 12.5 | Add the EfsHandoverWorkflow row and its nine activities, as for CG-ALL-3055. |
| CDC-04649 | RWB-P2-E2001-OPS | GAP-1334 | find it | Publish the per-service login of rwb_decision with the database platform story. Fix the chain-check names in the catalog before wave 2 build: LedgerChainCheckWorkflow, activities readDayEntries, verifyChain and reportBreak, and the Temporal Schedule for JOB-14 at 02:00 in queue rwb-decision. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04612 | RWB-P2-E2001-CON | CG-ALL-3050 | 18 | Align the test lists of the four differing requirements (REQ-DRI-013, REQ-CHO-001, REQ-CHO-005 and one more) with section 18 of this story. |
| CDC-04646 | RWB-P2-E2001-OPS | CG-ALL-3059 | 18 | Align the test lists for REQ-DRI-013, REQ-CHO-001, REQ-CHO-005 and REQ-RDF-003 with the test case IDs of story section 16. |
| CDC-04675 | RWB-P2-E2002-APP | CG-ALL-3065 | 18 | In the next RTM version align REQ-DRI-013 and REQ-CHO-002 test lists to the TC-E2-002 tests this story's section 18 lists. |
| CDC-04703 | RWB-P2-E2002-CON | CG-ALL-3072 | 18 | Align the test lists of REQ-DRI-013 and REQ-CHO-002 to TC-P2-E2002-CON-01, -02 and -03 as traced in section 18 of this story. |
| CDC-04726 | RWB-P2-E2002-OPS | CG-ALL-3079 | 18 | Align REQ-DRI-013 and REQ-CHO-002 test lists in the RTM to the TC-P2-E2002-OPS IDs listed in section 18. |
| CDC-04743 | RWB-P2-E2003-APP | CG-ALL-3087 | 18 | REQ-CHO-003 row in section 18 now also lists TC-E2-003-08 and 09; the RTM is another workbook and must be aligned there. |
| CDC-04759 | RWB-P2-E2006-APP | DOR-RWB-P2-E2006-APP-12 | 12, 12.7, 16, 18 | Align the test case lists for REQ-CHO-008, REQ-CHO-006 and REQ-RDF-009 with section 18 of RWB-P2-E2006-APP, which now includes TC-E2-006-14 and TC-E2-006-15. |
| CDC-04774 | RWB-P2-E2006-APP | CG-ALL-3102 | 18 | Adds TC-E2-006-14 and TC-E2-006-15 to the REQ-CHO-008 row in section 18. |

### RWB-P2-E2001-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04621 | RWB-P2-E2001-OPS | DOR-RWB-P2-E2001-OPS-21 | header | Complete the build and publish the contract. Build status is Not started and must reach Done. |
| CDC-04622 | RWB-P2-E2001-OPS | DOR-RWB-P2-E2001-OPS-22 | header | Publish a contract fake library version for the contract. |
| CDC-04629 | RWB-P2-E2001-OPS | GAP-0590 | find it | Fix key format EFS:<efs_record_key>; publish it as the run key set with the view-row count and the ledger writer hit count. |
| CDC-04630 | RWB-P2-E2001-OPS | GAP-0592 | find it | Publish GET /entry-candidate-facts?businessDate= as the batched customer read with personKey, productGroup and REC-05 resolution; correct the per-candidate wording. |
| CDC-04633 | RWB-P2-E2001-OPS | GAP-0652 | 12.5 | Fix in contract/handover-run-activities.yaml the workflow, nine activities, twelve summary elements and retry policy; fix the consumed P1 and P3 elements; publish six fakes with drift check. |
| CDC-04636 | RWB-P2-E2001-OPS | GAP-2259 |  | Publish the candidate page and EFS history page paths in RWB-P2-E2001-CON; publish the ledger append, REC-05 break and REC-01 result in the rwb-source-data contract. |
| CDC-04638 | RWB-P2-E2001-OPS | GAP-2463 |  | Keep the R-UNI-40 repeat count as a meter of rwb-decision on its operational dashboard, returned in the record-submission response header; confirm at contract review. |
| CDC-04648 | RWB-P2-E2001-OPS | GAP-0589 | find it | Record one call per account and business date with a configured row cap and no page parameter, and a held read answering 409 with a problem body that names MSG-P1-001 and the date of the load in use. |

### RWB-P2-E2002-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04654 | RWB-P2-E2002-APP | DOR-RWB-P2-E2002-APP-21 | find it | Set build status to Done once the contract is published. |
| CDC-04655 | RWB-P2-E2002-APP | DOR-RWB-P2-E2002-APP-22 | find it | Record the published fake library version for RWB-P2-E2002-CON. |
| CDC-04662 | RWB-P2-E2002-APP | GAP-0654 | find it | Settle the rwb-integration login, the case read contract, the field sets, the owner of live and messageCode, the settings owner, the connection-matrix rows and the daily step; record in RWB-P2-E2002-OPS and RWB-P3-E2002-APP. |
| CDC-04663 | RWB-P2-E2002-APP | GAP-0655 | find it | Approve the four assumptions: answer shape with accountNo, live and messageCode rule, interface contract with batch, budget and answer rules, and consumed read shapes; reconcile interface-versus-view wording in the Service Contract Catalog. |
| CDC-04706 | RWB-P2-E2002-OPS | DOR-RWB-P2-E2002-OPS-21 | header | Build status from Not started to Done once the contract is published |
| CDC-04707 | RWB-P2-E2002-OPS | DOR-RWB-P2-E2002-OPS-22 | header | Record the published contract fake library version |
| CDC-04713 | RWB-P2-E2002-OPS | GAP-0655 | find it | Approve the four assumptions (accountNo in the answer, live and messageCode rule, interface batch and budget rules, consumed read shapes) before the baseline is tagged. |
| CDC-04719 | RWB-P2-E2002-OPS | GAP-2472 |  | Confirm plan read and stored status stay with rwb-integration and rwb-case, restate the legacy endpoint on the owner per-service base, and keep rwb-decision to registry version and decision record. |

### RWB-PLT-N001-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04673 | RWB-P2-E2002-APP | GAP-0386 | 15 | Publish the gateway-bff composite case-record route path and merge order; integration lead agrees harness repository, SIT and UAT environments, seeded values, evidence format, retention and gate at wave 2 entry. |
| CDC-04674 | RWB-P2-E2002-APP | GAP-0773 | 15 | Publish the SCR-03 composite route: path, two parallel calls, merge rule (live wins; stored with MSG-P2-008 when live is missing or not live), masking rule and 2 s budget split. |
| CDC-04677 | RWB-P2-E2002-APP | GAP-0909 | 15 | Fix the rwb-access per-service login name in the platform DB story; publish the SCR-03 composite route field list, hop list, merge order and masking rule. |
| CDC-04699 | RWB-P2-E2002-CON | GAP-0386 | n/a | Agree harness repository, SIT and UAT environments, seeded case, plan and package versions, evidence format, retention and pass or fail gate; publish gateway-bff composite route path and merge order. |
| CDC-04700 | RWB-P2-E2002-CON | GAP-0773 | n/a | Publish the SCR-03 composite route with path, two parallel calls, merge rule (live wins, MSG-P2-008 fallback), masking rule and 2 s budget split. |
| CDC-04722 | RWB-P2-E2002-OPS | GAP-0386 |  | Agree harness repository, SIT and UAT environments, seeded case, plan and package versions, evidence format, retention and pass or fail gate with QA at wave-2 entry. |
| CDC-04723 | RWB-P2-E2002-OPS | GAP-0773 |  | Publish the composite route path, two parallel calls, merge rule (live answer wins; stored answer with MSG-P2-008 when live is missing or not live), masking rule and 2 s budget split. |
| CDC-04745 | RWB-P2-E2003-APP | GAP-0913 | 15 | Publish the SCR-03 other products composite route with its field list, merge order and masking step. |

### RWB-PLT-E1027-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04608 | RWB-P2-E2001-CON | GAP-1332 | 12 | Fix the DecisionRecorded payload and inputs snapshot element names: business date, queue and owner identifiers, hand-over reference, actions and composite idempotency key. Confirm before wave 2 build. |
| CDC-04641 | RWB-P2-E2001-OPS | GAP-1332 | find it | Fix the DecisionRecorded payload and inputs snapshot with business date, hand-over queue and owner IDs, hand-over reference, actions and composite idempotency key; confirm with the hand-over contract owner before wave 2 build. |
| CDC-04669 | RWB-P2-E2002-APP | GAP-2471 | find it | State one entry per case, business date and rule identity; publish the content models of the inputs snapshot and actions payload with plan reference, status and date. |
| CDC-04672 | RWB-P2-E2002-APP | GAP-1338 | find it | Settle whether a route move running two rules is one entry with the second rule in its actions or two entries per date; align the harness and case story. |
| CDC-04695 | RWB-P2-E2002-CON | GAP-2471 | n/a | State one entry per case, business date and rule identity; a transaction running two rules writes one entry per rule; publish inputs snapshot and actions content models. |
| CDC-04698 | RWB-P2-E2002-CON | GAP-1338 | n/a | Settle whether a two-rule route move is one entry or two entries per date, then align RWB-ITG-E2002-ITG and the case story. |
| CDC-04718 | RWB-P2-E2002-OPS | GAP-2471 |  | State one entry per case, business date and rule identity, one entry per rule when a transaction runs two rules, and publish the inputs snapshot and actions content model. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04611 | RWB-P2-E2001-CON | CG-ALL-3049 | 16 | Add rows for TC-P2-E2001-CON-01 to TC-P2-E2001-CON-08 with Given, When and Then copied from the criteria they cover. |
| CDC-04645 | RWB-P2-E2001-OPS | CG-ALL-3058 | 16 | Add rows TC-P2-E2001-OPS-01 to TC-P2-E2001-OPS-06 with Given, When and Then copied from the criteria they cover. |
| CDC-04656 | RWB-P2-E2002-APP | CG-ALL-3064 | 16 | Add TC-E2-002-11 to tab Story test cases with Given, When and Then from its criterion. |
| CDC-04681 | RWB-P2-E2002-CON | DOR-RWB-P2-E2002-CON-12 | 16, 18 | Add rows for TC-P2-E2002-CON-01 to TC-P2-E2002-CON-07 in tab Story test cases; align the section 18 test lists with RTM v7. |
| CDC-04702 | RWB-P2-E2002-CON | CG-ALL-3071 | 16 | Add rows TC-P2-E2002-CON-01 to TC-P2-E2002-CON-06 with Given, When and Then copied from AC1 to AC6 of this story. |
| CDC-04708 | RWB-P2-E2002-OPS | DOR-RWB-P2-E2002-OPS-12 | 16 | Add rows for TC-P2-E2002-OPS-01 to -07 under tab Story test cases; align section 18 test lists with RTM v7 |
| CDC-04725 | RWB-P2-E2002-OPS | CG-ALL-3078 | 16 | Add rows TC-P2-E2002-OPS-01 to TC-P2-E2002-OPS-06 with Given, When and Then copied from AC1 to AC6. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04617 | RWB-P2-E2001-CON | GAP-2468 | find it | Carry RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON and RWB-P7-E2005-CON; keep lane Day 1. |
| CDC-04618 | RWB-P2-E2001-CON | GAP-1335 | find it | Sequencing visibility sits in the wave 2 map. The story's dependency rows were edited under GAP-2261 and GAP-0593, not under this item. |
| CDC-04651 | RWB-P2-E2001-OPS | GAP-2468 | find it | Carry the six platform CON rows (DP-03, DP-06, DP-07, DP-09, DP-10, DP-19) and RWB-P7-E2005-CON in the dependency map. The lane stays at Day 1 because each added H row is a platform contract. |
| CDC-04652 | RWB-P2-E2001-OPS | GAP-1335 | find it | Carry the six platform contracts and the two rwb-case contracts in the wave 2 dependency map so the sequencing is visible. Keep the metadata rows as the story object fixes them. |
| CDC-04678 | RWB-P2-E2002-APP | GAP-1337 | 13 | Carry the platform H contracts and the rule-package, parameters and reference-data contracts of rwb-case in the dependency map; metadata rows unchanged. |
| CDC-04704 | RWB-P2-E2002-CON | GAP-1337 | none | Carry the platform contracts and the rwb-case rule-package, parameters and reference-data contracts listed in the item as dependencies, leaving the story metadata rows unchanged. |
| CDC-04729 | RWB-P2-E2002-OPS | GAP-1337 | Not specified in the source documents (GAP-1337) | Carry the platform contracts and the rule-package, parameters and reference-data contracts of rwb-case in the wave 2 dependency map; metadata rows unchanged. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04599 | RWB-P2-E2001-CON | GAP-0651 | find it | Mark TSD P2 v3 T5.2 and the P2 inbound exclusion as superseded by DP-05 and ADR-010, and name the login before the rwb_integration baseline is created |
| CDC-04632 | RWB-P2-E2001-OPS | GAP-0651 |  | Mark TSD P2 v3 T5.2 and the P2 inbound exclusion as superseded by DP-05 and ADR-010; keep the four-owner split as recorded in RWB-ITG-E2001-ITG and the Ownership Map. |
| CDC-04688 | RWB-P2-E2002-CON | GAP-0655 | find it | Approve the four assumptions at the contract review, reconcile the interface-versus-view wording of the technical specification, and record the re-basing on the integration base. |
| CDC-04765 | RWB-P2-E2006-APP | GAP-0663 | find it | Settle the rwb-integration login, the field sets of the source-data, treatment, document, case and access reads, the NLEADS read operation, the resource placement, and the AC2 and AC7 levels against doa.txt item 2.1.1. |
| CDC-04766 | RWB-P2-E2006-APP | GAP-0729 | find it | Agree the rwb-case login with the ACE DB story, the SCR-14 route with the edge story, the NLEADS read and treatment result fields with the P1 and S2 contract stories, and the AC2 and AC7 levels before wave 2 build. |
| CDC-04777 | RWB-P2-E2006-APP | GAP-2482 | 12 | Fix source_type CREDIT_APPROVAL and source_ref as the treatment id for a D5 row; state that a credit result is recorded through approve or refuse on that row. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04579 | RWB-P2-E2001-CON | DOR-RWB-P2-E2001-CON-14 | n/a | Record the signed epic design sign-off and confirm it covers this story's epic. |
| CDC-04620 | RWB-P2-E2001-OPS | DOR-RWB-P2-E2001-OPS-14 | header | Record the signed epic design sign-off covering RWB-P2-E2001-OPS. |
| CDC-04653 | RWB-P2-E2002-APP | DOR-RWB-P2-E2002-APP-14 | find it | Confirm and record the signed sign-off of the epic design. |
| CDC-04705 | RWB-P2-E2002-OPS | DOR-RWB-P2-E2002-OPS-14 | header | Record the signed epic design sign-off for EP02 in the epic design record |
| CDC-04733 | RWB-P2-E2003-APP | DOR-RWB-P2-E2003-APP-14 | header | Record the signed epic design sign-off for EP02 and cite it in the story. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04593 | RWB-P2-E2001-CON | CG-ALL-3048 | 14 | Add a new message ID for a consumed source that did not answer inside the budget, with text '{source} could not be read. Try again in a few minutes.', then the story cites it. |
| CDC-04595 | RWB-P2-E2001-CON | DOR-RWB-P2-E2001-CON-9 | 14 | MSG-P1-001 and MSG-P2-006 texts in §14 were replaced under CG-ALL-3046 and CG-ALL-3047. The remaining message gap sits with the standard. |
| CDC-04683 | RWB-P2-E2002-CON | DOR-RWB-P2-E2002-CON-9 | 14 | MSG-P3-027 text now follows Standard v4 (see R-10054). The When use is unchanged; if it differs from the Standard's use, the BA adds a new message ID there. |
| CDC-04757 | RWB-P2-E2006-APP | CG-ALL-3101 | 14 | Business analyst adds a new message ID for a source contract that did not answer; section 14 then cites it in place of MSG-GEN-006. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04601 | RWB-P2-E2001-CON | GAP-1333 | 12 | Add the business-date filter, the full DecisionLogPage and DecisionLogEntry field set, the page-size limit, and one panel identifier for a decision entry beside the case. Values are not in the sources; confirm with the owners. |
| CDC-04614 | RWB-P2-E2001-CON | GAP-0589 | 7 | Held-read answer and history-read shape marked Not specified in section 7 (AC4), section 12.2 and TC-04 |
| CDC-04686 | RWB-P2-E2002-CON | GAP-0908 | find it | Add POST /authorise and GET /me/permissions with request and answer schemas, stub them in the RWB-P4-E1037-CON fake, and record whether the plan reference travels in the authorise request. |
| CDC-04711 | RWB-P2-E2002-OPS | GAP-0908 | find it | Add the authorise path and resolved permission view with request and answer schemas, publish with RWB-P4-E1037-CON, and record whether the plan reference travels in the authorise request. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04616 | RWB-P2-E2001-CON | GAP-2467 | find it | Confirm the hand-over entry decision value with RW-COE when LOV-DECISION rows are loaded; load it as a reference row. |
| CDC-04650 | RWB-P2-E2001-OPS | GAP-2467 | find it | Confirm the hand-over LOV-DECISION value with RW-COE when the LOV-DECISION rows are loaded, and hold it as a reference row so a correction is a data change and not a release. |
| CDC-04666 | RWB-P2-E2002-APP | GAP-0771 | find it | Add a table code for the plan event map to LOV-REF-TABLE and load its rows as reference_row under a reference_version, one row per ACE status and route state pair. |
| CDC-04692 | RWB-P2-E2002-CON | GAP-0771 | n/a | Add a table code for the plan event map to LOV-REF-TABLE, load its rows as reference_row under a reference_version, one row per ACE status and route state pair. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04730 | RWB-P2-E2003-APP | CG-ALL-3082 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness through the rwb-source-data CON story, as Architecture v5 gives P1 the data product read. |
| CDC-04749 | RWB-P2-E2006-APP | CG-ALL-3096 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} in paths, through the provider's CON story. |
| CDC-04750 | RWB-P2-E2006-APP | CG-ALL-3097 | 12.2 | Publish GET /api/recovery/source-data/v1/collateral/{id} in paths, through the provider's CON story. |
| CDC-04751 | RWB-P2-E2006-APP | CG-ALL-3098 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness in paths, through the provider's CON story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04731 | RWB-P2-E2003-APP | CG-ALL-3083 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access CON story. |
| CDC-04732 | RWB-P2-E2003-APP | CG-ALL-3084 | 12.2 | Publish GET /api/recovery/access/v1/masking-policies in the rwb-access contract baseline, with the row shape from Architecture v5 slide 14. |
| CDC-04752 | RWB-P2-E2006-APP | CG-ALL-3099 | 12.2 | Publish GET /api/recovery/access/v1/doa-limits in paths, through the provider's CON story. |
| CDC-04753 | RWB-P2-E2006-APP | CG-ALL-3100 | 12.2 | Publish POST /api/recovery/access/v1/authorise in paths, through the provider's CON story. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04584 | RWB-P2-E2001-CON | CG-ALL-3037 | 12.5 | Add activity acceptAceDataReady with the input and output given in 12.5. |
| CDC-04585 | RWB-P2-E2001-CON | CG-ALL-3038 | 12.5 | Add activity readFreshness with the input and output given in 12.5. |
| CDC-04586 | RWB-P2-E2001-CON | CG-ALL-3039 | 12.5 | Add activity listCandidates with the input and output given in 12.5. |

### RWB-P7-E2005-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04607 | RWB-P2-E2001-CON | GAP-2464 | 12 | Fix the parameters caseId, decision, ruleId, ruleVersion, approver, from, to, page and size, with page size 1 to 500, ordered by decided_at; RWB-P7-E2005-APP implements and tests them. |
| CDC-04634 | RWB-P2-E2001-OPS | GAP-1333 |  | Add the businessDate filter, the full DecisionLogPage and DecisionLogEntry answer field set and the page-size limit; name one screen or panel for a decision entry beside the case. |
| CDC-04640 | RWB-P2-E2001-OPS | GAP-2464 |  | Fix caseId, decision, ruleId, ruleVersion, approver, from, to, page and size as the GET /decision-log parameters; page size 1 to 500; order by decided_at. |

### RWB-P6-E1073-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04659 | RWB-P2-E2002-APP | GAP-2395 | find it | Name the rwb-comms rule package codes and version labels read through the contract as the fixture set, and settle package assignment with the rule registry owner before integration. |
| CDC-04684 | RWB-P2-E2002-CON | GAP-2395 | find it | Read the three package codes and version labels as the fixture set, prove AC1 and AC5, and settle rwb-comms package assignment with the rule registry owner before integration. |
| CDC-04709 | RWB-P2-E2002-OPS | GAP-2395 | find it | Record the three package codes and version labels read through the contract as the fixture set, and settle rwb-comms package assignment with the rule registry owner before integration. |

### RWB-P7-E2002-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04670 | RWB-P2-E2002-APP | GAP-2472 | find it | Confirm the rwb-decision slice is the registry version and decision record, with the plan read kept on rwb-integration and rwb-case; restate the legacy endpoint on the owning service base. |
| CDC-04696 | RWB-P2-E2002-CON | GAP-2472 | 12 | Restate the legacy plan-status endpoint on the rwb-integration base; limit the rwb-decision slice to the registry version and the decision record. |
| CDC-04701 | RWB-P2-E2002-CON | GAP-2470 | n/a | Complete the metadata dependency rows from the DP table, or confirm the DP rows as added dependencies, and state the platform H and self-referential C rule in R5.5. |

### RWB-P7-E1073-CON; RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04671 | RWB-P2-E2002-APP | GAP-1336 | find it | Fix the model answer, inputs snapshot and announcement payload shapes; name the plan-status section of the decision log screen; publish the per-service login. |
| CDC-04697 | RWB-P2-E2002-CON | GAP-1336 | n/a | Fix the model answer, inputs snapshot and announcement payload, element names for plan reference, status, date and route state, and the per-service login. |
| CDC-04720 | RWB-P2-E2002-OPS | GAP-1336 |  | Fix the model answer, inputs snapshot, DecisionRecorded envelope element names and actions payload elements carrying plan reference, status, date and route state. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04577 | RWB-P2-E2001-CON | CG-ALL-3035 | 12.2 | Publish GET /api/recovery/case/v1/cases and GET /api/recovery/case/v1/cases/{caseId} as paths in rwb-case.yaml. |
| CDC-04748 | RWB-P2-E2006-APP | CG-ALL-3095 | 12.2 | Publish POST /api/recovery/case/v1/cases/{caseId}/actions in paths, through the provider's CON story. |

### OTHER:Functional Specification Document P3, section A1.5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04583 | RWB-P2-E2001-CON | GAP-1549 | n/a | Restate the A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |
| CDC-04624 | RWB-P2-E2001-OPS | GAP-1549 | header | Restate the ACE read path as a read through the rwb-source-data contract. Keep the business-key link rules unchanged. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04594 | RWB-P2-E2001-CON | DOR-RWB-P2-E2001-CON-12 | 12.7, 16, 18 | Register TC-P2-E2001-CON-01 to -12 in Test Cases v8 and align the §18 test lists with RTM v7 |
| CDC-04626 | RWB-P2-E2001-OPS | DOR-RWB-P2-E2001-OPS-12 | 12, 12.7, 16, 18 | Add rows TC-P2-E2001-OPS-01 to -09 to Test Cases v8; align the §18 test lists of P3 to RTM v7. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04596 | RWB-P2-E2001-CON | GAP-3175 | find it | Record AceDataReady (EV-26) on rwb.source-data.events.v1 with producer rwb-source-data and list LoadCompleted (EV-26) as its legacy alias |
| CDC-04627 | RWB-P2-E2001-OPS | GAP-3175 | find it | List LoadCompleted (EV-26) as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1. |

### OTHER:Batch and Scheduling next version (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04597 | RWB-P2-E2001-CON | GAP-3176 | find it | Confirm no Epic 2 step depends on JOB-01 and carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points |
| CDC-04628 | RWB-P2-E2001-OPS | GAP-3176 | find it | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### OTHER:EFS hand-over harness pack (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04598 | RWB-P2-E2001-CON | GAP-0388 | find it | Hold the composite route paths and merge order, harness repository, SIT and UAT environments, seeding, evidence format, retention and pass/fail gate as data, agreed with platform edge and QA |
| CDC-04631 | RWB-P2-E2001-OPS | GAP-0388 | find it | Hold the harness repository, SIT and UAT environments, seeding, evidence format, retention, pass/fail gate and gateway-bff route paths as data. |

### RWB-P7-E2005-CON; RWB-PLT-E1027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04609 | RWB-P2-E2001-CON | GAP-2462 | 4 | Add the element list of the actions and outcome columns of DecisionLogEntry (DF-DEC-014, DF-DEC-015) at the contract review. |
| CDC-04642 | RWB-P2-E2001-OPS | CG-ALL-3425 | find it | Add the element lists of decision_log_entry.actions and decision_log_entry.outcome at contract review. |

### RWB-PLT-E1047-CON; RWB-PLT-TE006-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04610 | RWB-P2-E2001-CON | GAP-2262 | 4 | Fix the rwb.case.events.v1 envelope and its retry and dead-letter settings; the story payload is limited to the eight listed fields. |
| CDC-04643 | RWB-P2-E2001-OPS | GAP-2262 | find it | Fix the envelope and retry settings of rwb.case.events.v1; limit the CaseCreated payload to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate and dpdAtEntry. |

### RWB-P3-E2002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04657 | RWB-P2-E2002-APP | DOR-RWB-P2-E2002-APP-10 | find it | Add empty, loading, error and no access states for SCR-03 and SCR-14. |
| CDC-04679 | RWB-P2-E2002-APP | NEWAC-RWB-P2-E2002-APP-AC13 | find it | This story's operation is a read that changes no status, so a refused transition cannot be a criterion here. It belongs to the case side that writes the status. |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04661 | RWB-P2-E2002-APP | GAP-0908 | find it | Add the authorise path and the resolved permission view with request and answer schemas, stub them in the contract fake, and record whether the plan reference travels in the authorise request. |
| CDC-04740 | RWB-P2-E2003-APP | GAP-0915 | 4 | Fix the masking answer schema: per-role row, marker values clear and masked, last-four shape and masking version. |

### RWB-P2-E2002-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04664 | RWB-P2-E2002-APP | GAP-0656 | find it | Record in the release readiness review the approved assumptions: identity and environment values, trigger wiring with ACE-or-stub record, five series, four alerts, no-package row, four runbook entries. |
| CDC-04689 | RWB-P2-E2002-CON | GAP-0656 | find it | Approve the three assumptions of RWB-P2-E2002-OPS; carry every threshold and endpoint as an environment value, never as code. |

### RWB-P7-E1073-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04665 | RWB-P2-E2002-APP | GAP-0770 | find it | Publish a catalog-row read on /api/recovery/decision/v1 by rule ID and package version, returning action_text, owner_role, timer_spec, target queue code and outputs. |
| CDC-04668 | RWB-P2-E2002-APP | GAP-2469 | find it | Publish the registry version answer and decision-log item fields, the artifact column and checksum coverage, the read page size, the service login and one refusal message ID. |

### OTHER:Platform database story (19-schema list) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04667 | RWB-P2-E2002-APP | GAP-0774 | find it | Allocate the rwb-case database login with its schema, hold the secret in Key Vault and record it in the Service Catalog before the first deployment. |
| CDC-04693 | RWB-P2-E2002-CON | GAP-0774 | n/a | Allocate the rwb-case database login with its schema, derive its name from the schema, hold the secret in Key Vault, record it in the Service Catalog before first deployment. |

### OTHER:Squad refinement record for this story (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04734 | RWB-P2-E2003-APP | DOR-RWB-P2-E2003-APP-16 | header | Header marks size as Not specified; the squad must size the story at refinement. |
| CDC-04738 | RWB-P2-E2003-APP | DOR-RWB-P2-E2003-APP-15 | Header | INVEST Small cannot be confirmed until the squad sizes the story. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04756 | RWB-P2-E2006-APP | CG-ALL-3093 | 12.7 | Record decision_record as the rwb_integration library table created by the PLT library, as stated in section 12.7. |
| CDC-04760 | RWB-P2-E2006-APP | DOR-RWB-P2-E2006-APP-7 | 11 | Register DF-ACC-009, DF-ACC-010, DF-TRT-023, DF-TRT-024, DF-TRT-025, DF-TRT-026 and the names credit_result_at and decision_record, or give their registered IDs and names. |

### OTHER:Squad refinement record (not in the source set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04580 | RWB-P2-E2001-CON | DOR-RWB-P2-E2001-CON-16 | Header | Size left as Not specified |

### OTHER:rwb-integration contract publication (not in the source set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04581 | RWB-P2-E2001-CON | DOR-RWB-P2-E2001-CON-23 | Header | Contract version left as Not specified |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04582 | RWB-P2-E2001-CON | DOR-RWB-P2-E2001-CON-8 | 12.5 | Close CG-ALL-3035 to CG-ALL-3039 and the seven further detcheck findings in those two documents. |

### RWB-P2-E2001-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04600 | RWB-P2-E2001-CON | GAP-0653 | 19 | Fix chart, one consumer group, registration and migration steps, six series, four alerts, four runbook entries; environment values in a values file; placeholders for missing message ids; on-call review. |

### OTHER:rwb-case REST API contract (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04602 | RWB-P2-E2001-CON | GAP-2258 | 12.2 | Add an admin rerun operation for a business date on the rwb-case base, answering 409 MSG-P2-006 while that date's workflow runs; path Not specified in the source documents (GAP-2258). |

### OTHER:rwb-source-data contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04603 | RWB-P2-E2001-CON | GAP-2259 | 12 | Publish the ledger append, the REC-05 break write and the REC-01 result paths and shapes; this story then names the paths and error envelopes once published. |

### OTHER:P3 ledger story and TSD P3 v3 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04604 | RWB-P2-E2001-CON | GAP-2260 | 4 | Re-scope the P3 ledger story to the P1 contract and mark the TSD P3 interaction object as owned by rwb-source-data under DP-18. |

### OTHER:rwb-decision operational dashboard and rwb-integration run summary (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04605 | RWB-P2-E2001-CON | GAP-2463 | 7 | Keep the repeat count as a rwb-decision meter returned in the record submission response header; rwb-integration run summary reads it. Confirm at the RWB-P2-E2001-CON contract review. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04606 | RWB-P2-E2001-CON | GAP-2466 | 4 | Keep the interaction ledger with rwb-source-data under DP-18; keep the EFS history items on the P7 entry as evidence; record the move in the Change Register. |

### OTHER:RWB-PLT-OBS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04613 | RWB-P2-E2001-CON | GAP-2465 | find it | Register ingest lag as a metric with the threshold as a parameter; raise the gap alert to RW-PLATADM under RWB-P7-E1027-APP. |

### OTHER:P3 screen specification (SCR-02; OTHER:SCR-04; OTHER:SCR-45) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04625 | RWB-P2-E2001-OPS | DOR-RWB-P2-E2001-OPS-10 | header | Add empty, loading, error and no-access states to SCR-02, SCR-04 and SCR-45. |

### OTHER:Service P3 REST operations list (rwb-case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04635 | RWB-P2-E2001-OPS | GAP-2258 |  | Add an admin rerun operation on the rwb-case base, POST /admin/jobs/{jobId}/rerun, answering 409 MSG-P2-006 while the workflow for the business date runs. |

### OTHER:TSD P3 v3 T3.1 and the P3 ledger story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04637 | RWB-P2-E2001-OPS | GAP-2260 |  | Keep the interaction ledger in rwb-source-data under DP-18; mark the P3 interaction object as owned by rwb-source-data and re-scope the P3 ledger story to the P1 contract. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04639 | RWB-P2-E2001-OPS | GAP-2466 |  | Record the move of InteractionLedger.appendEfsHistory from recovery.decision.api to rwb-source-data under DP-18, with history items kept on the P7 entry. |

### OTHER:Work Package B2-P3-020 (lane L-P2-E and Day-1 allocation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04644 | RWB-P2-E2001-OPS | GAP-2261 | find it | Assembler adds RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON to the lane and Day-1 allocation; metadata row unchanged. |

### RWB-P7-E1027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04647 | RWB-P2-E2001-OPS | GAP-2465 | find it | Register the five-minute ingest lag of rwb-decision as an RWB-PLT-OBS metric with the threshold held as a parameter, and raise the gap alert to RW-PLATADM under RWB-P7-E1027-APP. This story keeps only the sealed entry and writes no alert. |

### RWB-P2-E2001-APP; RWB-P2-E2002-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04658 | RWB-P2-E2002-APP | DOR-RWB-P2-E2002-APP-17 | find it | Complete the build of both dependencies before this story starts. |

### RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04660 | RWB-P2-E2002-APP | GAP-0907 | find it | Add a Case record column for all roles to TSD P4 T6.1, publish the 14-area matrix as data, and confirm CASE_RECORD letters and default scopes with the matrix owner. |

### OTHER:rwb-source-data contract (P1 contract story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04676 | RWB-P2-E2002-APP | GAP-0772 | 5 | Publish a break operation (product, check, key, detail, owner role) on the rwb-source-data contract and have the plan-status step call it once per rejected or missing plan. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04680 | RWB-P2-E2002-CON | DOR-RWB-P2-E2002-CON-1 | 1 | Confirm a role code or role name for the section 1 story statement, or add the 'tech lead' role; 'tech lead' is not in the list. |

### OTHER:Recovery Workbench Assumptions Register v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04682 | RWB-P2-E2002-CON | DOR-RWB-P2-E2002-CON-18 | 3 | Add an assumption row for open decision DL21 (option A for Epics 1 and 2) for RWB-P2-E2002-CON, then cite its ID in section 3. |

### OTHER:Technical Specification P4 (T6.1 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04685 | RWB-P2-E2002-CON | GAP-0907 | find it | Add a Case record column for all roles, publish the 14-area matrix as data with RWB-P4-AD002-APP, and confirm the CASE_RECORD letters and default scopes with the matrix owner. |

### RWB-P2-E2002-CON; RWB-P2-E2002-OPS; RWB-P3-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04687 | RWB-P2-E2002-CON | GAP-0654 | find it | Settle the rwb-integration login, the case read, the field sets, the live and messageCode owner, the settings owner, the connection-matrix rows and the daily step; record the outcome. |

### OTHER:P2 owner (batch operation confirmation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04690 | RWB-P2-E2002-CON | GAP-0769 | 11 | Section 11 states the per-case read in readPlanStatus and the batch size and timeout parameters; the 'once per case' wording is removed. |

### OTHER:P7 decision contract on /api/recovery/decision/v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04691 | RWB-P2-E2002-CON | GAP-0770 | find it | Publish the rule-catalog row read by rule ID and package version, returning action_text, owner_role, timer_spec, target queue code and outputs. |

### RWB-P7-E1073-CON; RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04694 | RWB-P2-E2002-CON | GAP-2469 | n/a | Publish the registry version answer, decision-log item fields, artifact column and checksum coverage, page size, service login and one refusal message identifier before wave-2 baseline. |

### OTHER:Technical Specification TSD P4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04710 | RWB-P2-E2002-OPS | GAP-0907 | find it | Add a Case record column to T6.1 for every role and confirm the CASE_RECORD letters and default scopes with the matrix owner before PM-2026.12. |

### RWB-P2-E2002-CON; RWB-P3-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04712 | RWB-P2-E2002-OPS | GAP-0654 | find it | Add the P2-to-ACE-Common and P3-to-P2 matrix rows; record the login name, case read contract, field sets, live and messageCode owner with merge rule, and settings owner and read path. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04714 | RWB-P2-E2002-OPS | GAP-0770 |  | Publish GET of the rule catalog row on /api/recovery/decision/v1 by rule ID and package version, returning action_text, owner_role, timer_spec, target queue code and outputs. |

### OTHER:Reference-data story of the service; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04715 | RWB-P2-E2002-OPS | GAP-0771 |  | Add a table code for the plan event map to LOV-REF-TABLE and load its rows as reference_row under a reference_version, one row per ACE status and route state pair. |

### OTHER:Platform database story (19-schema list) and Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04716 | RWB-P2-E2002-OPS | GAP-0774 |  | Allocate the rwb-case login with its schema, derive its name from the schema, hold the secret in Key Vault and record it in the Service Catalog before first deployment. |

### OTHER:rwb-decision contract (Service owner of rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04717 | RWB-P2-E2002-OPS | GAP-2469 |  | Publish the registry version answer, decision-log item field names, artifact column and checksum basis, page size, service login and one refusal message identifier before the wave-2 contract baseline. |

### RWB-PLT-E1027-CON; RWB-ITG-E2002-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04721 | RWB-P2-E2002-OPS | GAP-1338 |  | Settle whether a two-rule route move is one entry with the second rule in its actions or two entries, and align the harness and case story to that answer. |

### RWB-P7-E2002-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04724 | RWB-P2-E2002-OPS | GAP-2470 |  | The gap concerns the DP table and metadata rows of RWB-P7-E2002-APP. No edit in this story. |

### OTHER:P1 rwb-source-data contract story (ID not specified in the source documents (GAP-0772)) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04727 | RWB-P2-E2002-OPS | GAP-0772 | 8 | Publish a break operation (product, check, key, detail, owner role) on the rwb-source-data contract and have the plan-status step call it once per rejected or missing plan. |

### OTHER:Platform DB story (rwb-access login) and gateway-bff composite route publication (DP-19) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04728 | RWB-P2-E2002-OPS | GAP-0909 | Not specified in the source documents (GAP-0909) | Fix the rwb-access per-service login and publish the SCR-03 composite route with its field list, hop list, merge order and field-level masking rule. |

### OTHER:Backlog for the CON stories in Depends on and Contract dependencies (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04735 | RWB-P2-E2003-APP | DOR-RWB-P2-E2003-APP-21 | header | Bring the CON stories listed in Depends on and Contract dependencies to Done so the contract is published. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04736 | RWB-P2-E2003-APP | DOR-RWB-P2-E2003-APP-22 | 12.8 | Publish a contract fake library version covering the fakes in section 12.8 and record its version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04737 | RWB-P2-E2003-APP | DOR-RWB-P2-E2003-APP-8 | 12.2 | Publish GET freshness, POST authorise and GET masking-policies in the two yaml files, as set out in CG-ALL-3082 to 3084. |

### OTHER:Backlog status of the stories in Depends on (build) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04739 | RWB-P2-E2003-APP | DOR-RWB-P2-E2003-APP-17 | Header | Dependencies are named in the header; their completion is tracked in the backlog. No status is asserted in the story. |

### OTHER:RWB-P1; OTHER:RWB-P3 and RWB-P4 contract stories; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04741 | RWB-P2-E2003-APP | GAP-0662 | 4 | Fix the contract field names of the product, party, freshness, authorise and masking answers; register rwb.integration.customer-products on the platform flag library. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; RWB-PLT-N001-CON; OTHER:integration harness plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04742 | RWB-P2-E2003-APP | GAP-0390 | 15 | Publish the composite route path and merge order; publish field IDs of permission, masking_rule, rwb_case and rwb_source_data freshness tables; agree harness repository, environments, seed data, evidence format and pass gate with QA. |

### RWB-PLT-E1044-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04744 | RWB-P2-E2003-APP | GAP-0916 | 4 | Name the rwb_access database login and grant it SELECT on its own schema only. |

### OTHER:Case service story and Status transitions sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04746 | RWB-P2-E2003-APP | NEWAC-RWB-P2-E2003-APP-AC10 | 7, 16 | AC10 and TC-E2-003-15 added: the read changes no status; refusal of a disallowed transition belongs to the case service. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04747 | RWB-P2-E2006-APP | CG-ALL-3094 | 12.1 | Publish POST /treatments/{treatmentId}/credit-result in paths, through the owner's CON story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml; OTHER:rwb-case API yaml; OTHER:rwb-source-data API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04754 | RWB-P2-E2006-APP | DOR-RWB-P2-E2006-APP-8 | 4 | Publish POST /api/recovery/integration/v1/treatments/{treatmentId}/credit-result in rwb-integration.yaml; POST /api/recovery/case/v1/cases/{caseId}/actions in rwb-case; GET accounts/{id} and collateral/{id} in rwb-source-data. Three more detcheck paths are not in this chunk. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04755 | RWB-P2-E2006-APP | CG-ALL-3092 | 4 | Record credit_result_at as a field of the treatment entity in LDM v9 and Data Classification v5, as the rwb-treatment column named in the story. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04758 | RWB-P2-E2006-APP | DOR-RWB-P2-E2006-APP-11 | header | Re-check the personal-data class of the fields the story carries against its statement that it carries no personal data, and correct whichever side is wrong. |

### OTHER:Message catalogue standard (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04761 | RWB-P2-E2006-APP | DOR-RWB-P2-E2006-APP-9 | 14 | Confirm the standard meaning of MSG-GEN-006; if it differs from source contract not answering, the story moves that case to the standard ID. |

### OTHER:Service contract of rwb-integration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04762 | RWB-P2-E2006-APP | GAP-1713 | find it | Record the owning-service contract for FEAT-APD-01, FEAT-CHO-02, -06, -07, -08 (twice as written), FEAT-DCM-12, FEAT-OCC-01, -07, -09, -11, FEAT-TRT-04, FEAT-VAL-06: approval P7, case P3, documents P5, communications P6, valuation S1. |

### RWB-ITG-E2006-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04763 | RWB-P2-E2006-APP | GAP-1344 | find it | Attribute the required level to rwb-access (P4), not rwb-decision; add the DoA limit read to the Ownership Map API catalogue with P4 owner and P7, P3, P2 consumers. |

### OTHER:Credit approval pack harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04764 | RWB-P2-E2006-APP | GAP-0394 | find it | Record the composite route path and merge order, harness environment and repository, seed data, evidence format and retention, and pass/fail gate, agreed at the wave 2 entry check. |

### OTHER:Recovery Workbench contract review, wave 2 (rwb-access, rwb-integration and rwb-case contract owners) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04767 | RWB-P2-E2006-APP | GAP-1342 | 3 | Settle the rwb-decision login, the decide path and field names, the delegation read shape and catalogue row, one level-comparison owner, and the actions key names. |

### OTHER:Template and Rules v1, section R5.5 (DP-07 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04768 | RWB-P2-E2006-APP | GAP-2478 | 3 | Correct the DP-07 reference-data row so delegation_limit is read from rwb-access (RWB-P4-E1037-CON), not from rwb-case. |

### RWB-P4-E1037-CON; OTHER:next message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04769 | RWB-P2-E2006-APP | GAP-2479 | 3 | Add GET /api/recovery/access/v1/doa-limits (decisionCode, regulationItem, productGroup, amount, asOfDate) answering level, delegationLimitId, limitVersion or NOT_COVERED; publish texts of MSG-P7-010, MSG-GEN-006, MSG-P4-003. |

### OTHER:P7 decision-record schema document (D5 actions key set); OTHER:SCB IT (NLEADS pattern) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04770 | RWB-P2-E2006-APP | GAP-2480 |  | Fix the D5 actions keys as requiredLevel, delegationLimitId, limitVersion, nleadsRef, resultDate; confirm the nleadsRef pattern with SCB IT before the wave 2 test cycle. |

### OTHER:RWB TSD P7 v2 (T-A.2) and RBAC matrix (T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04771 | RWB-P2-E2006-APP | GAP-2481 |  | Declare Decision log right A on API-P7-003 and API-P7-005 and add A rows to the RBAC matrix for recording roles; keep Treatment and offer U on the rwb-integration pack endpoint. |

### OTHER:RWB TSD S2 v2 (T3.0 to T3.2; OTHER:T-A.1); OTHER:FSD S2 v3 (A2; OTHER:Screens) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04772 | RWB-P2-E2006-APP | GAP-2689 |  | Baseline the credit-result PATCH variant, its element names, SUBMITTED/APPROVED/REFUSED states, the four credit columns, one-result rule and state-refusal message at the wave 2 contract freeze. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:wave 2 contract review (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04773 | RWB-P2-E2006-APP | GAP-1343 |  | Publish the six DP-added dependencies with this story as consumer; confirm RWB-P4-E1037-CON as a contract dependency of this story. |

### OTHER:Section 18 of the RWB-E1-069 and RWB-E1-018 slices (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04775 | RWB-P2-E2006-APP | GAP-3213 | 18 | Add REQ-RDF-004 to section 18 of RWB-E1-069 and RWB-E1-018; list legacy slices and citing stories in the v7 row. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04776 | RWB-P2-E2006-APP | GAP-2690 | 1, 12.2 | Record the treatment operations and credit-result elements against rwb-treatment, the level comparison against rwb-access, the ledger entry against rwb-decision, and the SCR-14 merge against the edge contract. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04778 | RWB-P2-E2006-APP | GAP-2483 | 12 | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision.events.v1 as well as the shared ledger topic, keyed by case id, and map it to the free identifier of EV-08, EV-09 and EV-30. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-04779 | RWB-P2-E2006-APP | GAP-2484 | Header | Give GET /cases/{caseId}/recommendation to the P7 story that serves the decision screen. Keep the metadata rows as the work package gives them. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20574 | RWB-P2-E2003-APP | R-22345 |  | Contract field names and flag registration belong to the RWB-P1, RWB-P3 and RWB-P4 contract stories and RWB-PLT-N001-CON, not this PRD. |

### 02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20613 | RWB-P2-E2003-APP | R-30455 |  | AC10 and TC-E2-003-15 belong to the case service story. The Status transitions sheet needs event and state values not in the sources; target not read (docview unavailable). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0386 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0388 | EFS hand-over harness: repository, environments, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0390 | Customer other-products harness pack: repository, environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0394 | Credit approval pack integration harness: composite credit-pack route, harness environment, seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0589 | The history read is one operation or a paged read, and the HTTP answer of a held read, are stated by no source | Solution architect, P1 | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0592 | No source splits the hand-over facts between the candidate rule and the borrower and product-group facts, and the run's contract names a per-candidate customer read | Solution architect, P1 and P2 | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0651 | rwb-integration EFS hand-over: the mount of the step, the split across four owners, the consumed contract paths, the run summary store and the level of the decision record are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0652 | rwb-integration EFS hand-over contract: the activity contract, the consumed element shapes, the provided surface and the fakes have no source text | Tech lead | Resolved (directive) |
| GAP-0653 | rwb-integration EFS hand-over deployment: the values, the alert identifiers, the dashboard series and the runbook have no source | DevOps lead | Resolved (directive) |
| GAP-0654 | rwb-integration ACE plan status: the login, the account resolution, the interface field types, the meaning of live and messageCode, the two settings, the connection-matrix rows and the ownership split are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0655 | The plan-status contract baseline: the accountNo field, the meaning and owner of live and messageCode, the interface null rules, the consumed read shapes, the composite route and the two specification conflicts are not fixed by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0656 | The plan-status deployment values, the ACE endpoint and certificate references, the two setting values at run time, the trigger wiring, the alert thresholds, the mapping of the no-package condition and the fixture owner are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0662 | rwb-integration customer products read: login, contract field names, ACE view owner, endpoint and route names, masking rows and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0663 | rwb-integration credit approval pack: login, contract field names, NLEADS read, the ownership split, the integration-base resource placement and the approval-level values are not settled by any one source | Solution architect | Resolved (directive) |
| GAP-0729 | rwb-case credit approval: login, edge route and the NLEADS and treatment contract shapes are not specified | TechX | Resolved (directive) |
| GAP-0769 | The hand-over of the plan status between rwb-integration and rwb-case, and its batching, are not specified | Solution architect | Resolved (directive) |
| GAP-0770 | No published operation reads a rule catalog row by rule ID and package version | P7 decision owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0771 | The plan event map has no table code in LOV-REF-TABLE and no target table or column | Reference data owner (RW-COE) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0772 | The delivery path of a plan-status break to the data-quality console is not specified | P1 source data owner | Resolved (directive) |
| GAP-0773 | The gateway-bff composite route of the case record plan section is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0774 | The per-service database login name of rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0907 | rwb-access plan status: the TSD RBAC matrix has no Case record column, so the CASE_RECORD letters this slice decides are not tabulated for any role | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0908 | rwb-access plan status: the authorise request and answer shapes and the resolved permission view are absent from the TSD P4 appendix, including whether the plan reference travels in the authorise request | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0909 | rwb-access plan status: the per-service login name and the gateway-bff composite route field list behind SCR-03 and the plan status panel are not specified | Solution architect | Resolved (directive) |
| GAP-0913 | The field list and the masking step of the gateway-bff composite route for the other-products panel are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0914 | It is not settled who writes the PII access event for the composed other-products read | Solution architect | Resolved (directive) |
| GAP-0915 | The field names of the masking answer inside the authorise reply and the masking-policies read are not specified | Solution architect | Resolved (directive) |
| GAP-0916 | The per-service database login name of rwb-access is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1332 | Envelope and payload element names of DecisionRecorded, and the shape of the inputs snapshot | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1333 | Answer field set and business-date filter of the decision-log read, and the screen that shows an entry beside the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1334 | Per-service login of rwb_decision, the chain-check workflow and activity names, and the Schedule identifier of JOB-14 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1336 | Shape of the model answer, of the inputs snapshot and of the announcement, with the carrier names of the plan-status move | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1338 | One ledger entry per route move or per case and business date, for a move that runs two rules | Solution architect | Resolved (directive) |
| GAP-1342 | rwb-decision credit approval slice: the decide path, the delegation answer shape, the actions keys, the comparison site, the message texts, the decision sub-code, the per-service login and the screen identity are not fixed by any one source | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1344 | The delegation of authority table is ruled to rwb-access by the Ownership Map while the integration story of this key attributes the required level to rwb-decision | Solution architect | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-2258 | No rerun operation for the entry run after JOB-02 becomes a workflow | TechX | Resolved (directive) |
| GAP-2259 | Paths and payloads of the P2 hand-over and P1 ledger contracts | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2260 | Interaction ledger ownership conflicts with the legacy write and the P3 data model | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2262 | CaseCreated payload and the resume of a held run are not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2462 | The inner shape of the actions and outcome columns of a hand-over decision entry is not in any source | Solution architect with the data steward | Resolved (directive) |
| GAP-2463 | Where the R-UNI-40 repeat count of a hand-over record is kept and reported is not stated | P7 and P2 solution architects | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2464 | No source fixes the query parameters and paging of GET /decision-log | P7 contract owner | Resolved (directive) |
| GAP-2465 | The five-minute ledger completeness target has no named alert, owner or threshold | Platform observability owner with the P7 solution architect | Resolved (directive) |
| GAP-2466 | The legacy story puts the EFS history append in the decision module while the Ownership Map and DP-18 put the interaction ledger in rwb-source-data | Solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2467 | The exact LOV-DECISION value of the hand-over entry is not stated | P7 business analyst with RW-COE | Resolved (directive) |
| GAP-2468 | The story line carries one C row and no H row while the pattern table adds six platform H rows and the guard | Coordinator of the realignment with the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2469 | RWB-P7-E2002-APP: the values of the version answer, the entry payload, the artifact reference, the service login, the page size and the model-refusal message are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2471 | RWB-P7-E2002-APP: the width of one ledger entry is ambiguous where a move runs two rules in one transaction, and no source fixes the payload that carries the plan facts | Service owner of rwb-decision with the rwb-case service owner and the data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2472 | RWB-P7-E2002-APP: the legacy story sits in Module P2 Integration and names the plan-status endpoint on the monolith base, while the plan gives this APP slice to rwb-decision and the read to rwb-integration | Solution architect with the rwb-decision and rwb-integration service owners | Resolved (directive) |
| GAP-2478 | delegation_limit has no owner in the P7 rows, and three sources name three different homes for the level | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2479 | The delegation read of rwb-access has no named path, request, answer or message text | P4 and P7 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2480 | The field set of a D5 credit entry and the format of the NLEADS reference are not specified | P7 solution architect and the ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2481 | The legacy story requires the Treatment and offer right while the endpoint of this service declares the Decision log right | P4 access owner and the P7 solution architect | Resolved (directive) |
| GAP-2482 | How a D5 credit approval is identified, and whether a result is an approve or a dedicated credit-result action, is not stated | P7 solution architect and the routing story owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2483 | The event name that carries the D5 record on the service topic is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2689 | The treatment-side credit-result record has no operation, no element names, no state values and no column rule in the S2 sources | Solution architect, S2, with the rwb-treatment tech lead and the rwb-integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2690 | The rwb-treatment share of the key is stated by no S2 source, and the caller contract, the level comparison, the case move and the record ownership are split across four stories | Solution architect with the rwb-integration, rwb-treatment, rwb-case and rwb-access tech leads and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
