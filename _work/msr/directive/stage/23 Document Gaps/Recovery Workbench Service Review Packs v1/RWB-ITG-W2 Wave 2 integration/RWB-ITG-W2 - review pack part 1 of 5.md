# RWB-ITG-W2 Wave 2 integration - review pack, part 1 of 5 (RWB-ITG-E2001-ITG to RWB-ITG-E2007-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 145 |
| Cross-document (pending in another document) | 165 |
| Not applied (value not in the sources) | 18 |
| Open business decisions | 30 |
| Register gaps linked | 129 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E2001-ITG | 28 | 32 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2001 ITG EFS hand-over with full history - integration v2.md |
| RWB-ITG-E2002-ITG | 14 | 26 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2002 ITG ACE plan status on the case - integration v2.md |
| RWB-ITG-E2003-ITG | 15 | 11 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2003 ITG Customer's other products on the case - integration v2.md |
| RWB-ITG-E2004-ITG | 17 | 34 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2004 ITG Treatment entity and plan timers data model - integration v2.md |
| RWB-ITG-E2005-ITG | 19 | 8 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2005 ITG Decision log query API for audit - integration v2.md |
| RWB-ITG-E2006-ITG | 21 | 22 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2006 ITG Credit approval pack for NLEADS - integration v2.md |
| RWB-ITG-E2007-ITG | 31 | 31 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2007 ITG Booking confirmation from the ALS load - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E2001-ITG | R-09421 | CG-ALL-537 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-ITG-E2001-ITG | R-09422 | CG-ALL-538 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-ITG-E2002-ITG | R-09425 | CG-ALL-547 | Script gap | Product owner | Open decision DL21 has no assumption | Owner rules DL21; until then build on the recommended option. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2001-ITG, RWB-P1-E1011-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22306 | GAP-0591 | Register gap | Data steward and data product owner, P1 | The REC-05 break list row for a hand-over key is defined only for keys on an existing Workbench table, not for a candidate that has no row yet | Answer the break in the candidate-facts read as {check: REC-05, keyType: PERSON_KEY or ACCOUNT_KEY, key: <value>} with resolution HELD, write no row and invent no fact, and let RWB-P1-E1011-APP's REC-05 step carry the row for the business date so the data steward and the ACE team read one list. Fix the answer in RWB-P2-E2001-CON. |
| RWB-ITG-E2001-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22309 | GAP-0588 | Register gap | Data steward and data product owner, P1 | The collection period of an account's EFS history is named by no source, so the boundary of the history read is undefined | Fix the period as the EFS assignment window of the account: it opens at v_ace_efs_assignment.assignment_start_date and closes at assignment_end_date, or at the business date of the read for the open assignment; when the account has no assignment row the period opens at its earliest contact_at. Publish the rule in RWB-P2-E2001-CON with the answer so the run and this service read the same boundary, and ask the data steward to confirm it with the ACE team before wave 2 exit. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-AD004-APP, RWB-P4-E2003-APP | R-22343 | GAP-0910 | Register gap | Compliance and PDPA officer (RW-COMPLY) | The roster of roles that see the other-products account number unmasked is an assumption of the legacy story | Confirm the five clear roles and that every other role holding Case record R is masked, then load the roster through the masking load path of RWB-P4-AD004-APP. |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E1038-APP, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22353 | GAP-0919 | Register gap | Business lead | Which delegation limit version is in force on the approval date of a treatment is a data state, not a document value | Decide the version in force per environment at the DoA load (RWB-P4-E1038-APP) and keep it out of code; the lookup always answers the version whose window covers the date asked, and the answer names it |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22357 | GAP-0704 | Register gap | Data product owner | The 01:30 treatment extract has no owner in the target and its DP04 read path and freshness element are not in the Ownership Map | Record the owner of the treatment extract as P9 rwb-reporting on JOB-15 with the DP04 copy in rwb_source_data, publish the case-facing read GET /api/recovery/source-data/v1/data-products/DP04/records with its freshness element in the Ownership Map and the P1 API file, and state in the event catalogue that the copy is built from the treatment events. |
| RWB-ITG-E2005-ITG, RWB-P4-E1037-CON, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-22366 | GAP-1243 | Register gap | Compliance and PDPA officer, with the P4 access owner | Whether the audit role may see unmasked person keys in an entry or an export | The audit read and the export carry the masked value under the policy of rwb-access in force, with no unmasking operation on either read; Compliance either confirms that reading or publishes an audit-specific policy row before the wave 2 exit. |
| RWB-ITG-E2005-ITG, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-22368 | GAP-1241 | Register gap | Compliance and PDPA officer, with the P7 business lead | Decision log retention period is not set | Compliance fixes the retention period and the archive rule for decision_log_entry as reference data before the wave 2 exit; until then the store keeps every entry, the query purges nothing and archives nothing, and the value is read as a parameter when it arrives. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-E2003-APP | R-28706 | GAP-0911 | Register gap | Compliance and PDPA officer (RW-COMPLY) | No source fixes the masking version label in force for the wave-2 release, or the rule for two valid versions on one day | Name the masking version of the wave-2 release in the masking load file and confirm the latest-valid-from rule for a day with two valid versions. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-E2003-APP | R-28707 | GAP-0912 | Register gap | Data steward and data product owner (RW-DATASTEW) | No source states whether the other-products account number is the only personal field of the panel | Record the personal-data classification of the seven v_ace_party_product fields in the data dictionary, and add a masking row or an explicit unmasked false for any further personal field. |
| RWB-ITG-E2005-ITG, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-28719 | GAP-1244 | Register gap | Business analyst, P7, with Compliance | REQ-ACA-006 and NFR-042 still name a data-lake copy that DP-17 removes | Read REQ-ACA-006 and NFR-042 as covering the case store, the document store and the reporting read model; drop the lake wording at the next BRD and NFR version, retire the lake analysis with no target path and no dependency, and write the AC-READ/AC-EXPT record for the query path only. |
| RWB-ITG-E2001-ITG | R-33384 | ASM-ALL-537 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-ITG-E2001-ITG | R-33385 | ASM-ALL-538 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E2002-ITG | R-33386 | ASM-ALL-547 | Script assumption |  | Built on the recommended option of DL21: A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead rules DL21 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E2001-ITG | R-03670 | DOR-RWB-ITG-E2001-ITG-14 | header | Definition of Ready item 14 Epic design: Fail | No signed design for epic RWB-ITG-W2 found: grep of all .md files (BR Epic 2 v3, story files, check reports) shows only references. A sign-off is an approval and cannot be invented. |
| RWB-ITG-E2002-ITG | R-03676 | DOR-RWB-ITG-E2002-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed EP02 or RWB-ITG-W2 epic design found in the 22 Microservice Realignment E2002 files or in earlier searches. Recording a sign-off would invent it. |
| RWB-ITG-E2002-ITG | R-03677 | DOR-RWB-ITG-E2002-ITG-16 | header | Definition of Ready item 16 Size: Fail | Size row added with the not-specified placeholder; no size is in the sources, so DoR item 16 stays open until refinement. |
| RWB-ITG-E2002-ITG | R-03680 | DOR-RWB-ITG-E2002-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published fake library version found in the E2002 story files or the P2 CON story; section 13 still says FakePack is to be built. A version would be invented. |
| RWB-ITG-E2002-ITG | R-03681 | DOR-RWB-ITG-E2002-ITG-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Contract version row added with the not-specified placeholder; only the /v1 path is given, so DoR item 23 stays open. |
| RWB-ITG-E2003-ITG | R-03684 | DOR-RWB-ITG-E2003-ITG-16 | header | Definition of Ready item 16 Size: Fail | No source gives a size for this story, so none is recorded. |
| RWB-ITG-E2003-ITG | R-14191 | DOR-RWB-ITG-E2003-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | Whether the story is Small cannot be shown from the sources; the squad confirms it at refinement. |
| RWB-ITG-E2003-ITG | R-29885 | NEWAC-RWB-ITG-E2003-ITG-AC10 | 7, 16 | AC10: a status change the model does not allow is refused (no criterion covers a disallowed transition) | The story only reads product status; it has no status change operation or status model, so there is no transition to refuse. |
| RWB-ITG-E2004-ITG | R-03690 | DOR-RWB-ITG-E2004-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size value in the sources (searched 04 User stories Size rows; folders 04, 09-11, 21). Size is set by the squad at refinement and cannot be invented. |
| RWB-ITG-E2004-ITG | R-03691 | DOR-RWB-ITG-E2004-ITG-17 | 13 | Definition of Ready item 17 Dependencies: Fail | Named dependencies are not built yet; text cannot change that. No replacement key for RWB-P7-E1073-CON is given (CG-ALL-554), so section 13 keeps it. |
| RWB-ITG-E2004-ITG | R-03693 | DOR-RWB-ITG-E2004-ITG-22 | 12 | Definition of Ready item 22 Fake published: Fail | No published fake library version in md, py, csv, json or yaml sources. The version exists only once the fake is published, so none can be recorded now. |
| RWB-ITG-E2005-ITG | R-03697 | DOR-RWB-ITG-E2005-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is given by the sources, so the item stays open until the squad sizes the story at refinement. |
| RWB-ITG-E2005-ITG | R-14209 | DOR-RWB-ITG-E2005-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | The Small criterion of INVEST cannot be confirmed until the squad sizes the story at refinement. |
| RWB-ITG-E2006-ITG | R-09433 | CG-ALL-571 | 11 | Field IDs DF-TRT-024 are not all fields of treatment in LDM v9 | LDM v9, sheet ACE mapping: DF-TRT-024 is treatment.credit_result. ID and entity are correct, so no change is needed. |
| RWB-ITG-E2006-ITG | R-09434 | CG-ALL-572 | 11 | Field IDs DF-TRT-025 are not all fields of treatment in LDM v9 | LDM v9, sheet ACE mapping: DF-TRT-025 is treatment.credit_result_reason. ID and entity are correct, so no change is needed. |
| RWB-ITG-E2006-ITG | R-14217 | DOR-RWB-ITG-E2006-ITG-15 | section header | Definition of Ready item 15 INVEST: Partial | No size is given in the sources, so 'Small' cannot be asserted; the squad sizes the story at refinement. |
| RWB-ITG-E2006-ITG | R-14218 | DOR-RWB-ITG-E2006-ITG-17 | section header | Definition of Ready item 17 Dependencies: Partial | The five stories block the ITG run and stay under Integration dependencies; Depends on (build) stays None, consistent with Ready to start Day 1. |
| RWB-ITG-E2007-ITG | R-03710 | DOR-RWB-ITG-E2007-ITG-17 | header | Definition of Ready item 17 Dependencies: Fail | The nine named dependencies are not done yet. That is build state, and a story edit cannot change it. RWB-P7-E1073-CON is not in the story text supplied, so nothing was edited for it. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01072 | RWB-ITG-E2001-ITG | CG-ALL-531 | 18 | Align the test lists of the four differing requirements with section 18 of RWB-ITG-E2001-ITG at the next version. |
| CDC-01101 | RWB-ITG-E2002-ITG | CG-ALL-543 | 18 | Align the REQ-DRI-013 and REQ-CHO-002 test case lists in RTM v7 with section 18 of RWB-ITG-E2002-ITG in its next version. |
| CDC-01112 | RWB-ITG-E2003-ITG | CG-ALL-550 | 18 | Align the test lists of REQ-CHO-003 and REQ-RDF-010 with section 18 of RWB-ITG-E2003-ITG in the RTM's next version. |
| CDC-01124 | RWB-ITG-E2004-ITG | DOR-RWB-ITG-E2004-ITG-12 | 12, 16, 18 | Align the section 18 test lists with the section 16 test cases of this story, including TC-E2-004-17-ITG. |
| CDC-01128 | RWB-ITG-E2004-ITG | GAP-2503 | find it | Record that AC1, AC3, AC4 and AC5 of legacy RWB-E2-008 are carried by no story of this split, and declare the nine consumed operations on the per-service bases. |
| CDC-01144 | RWB-ITG-E2004-ITG | CG-ALL-558 | 18 | Align the test lists of the four requirements in section 18 with the test lists of RWB-ITG-E2004-ITG section 18 in the next RTM version. |
| CDC-01154 | RWB-ITG-E2005-ITG | DOR-RWB-ITG-E2005-ITG-12 | 16, 18 | Section 16 has 14 cases. The P3 section 18 lists differ from RTM v7, which is outside this story. |
| CDC-01156 | RWB-ITG-E2005-ITG | CG-ALL-566 | 18 | Align the test lists of the four requirements (REQ-DRI-012, REQ-DRI-003, REQ-ACA-006, REQ-DRI-002) with RWB-ITG-E2005-ITG section 18 in the next RTM version. |
| CDC-01163 | RWB-ITG-E2006-ITG | DOR-RWB-ITG-E2006-ITG-12 | 16 | Story side: TC-E2-006-14-ITG covers AC12 and BR4. Foreign-criteria rows are marked 'run by owner story'. RTM v7 checked, sheet RTM. |
| CDC-01174 | RWB-ITG-E2006-ITG | CG-ALL-578 | 18 | Align the trace lists of REQ-CHO-008, REQ-CHO-006 and REQ-RDF-009 with section 18 of this story in its next version. |
| CDC-01205 | RWB-ITG-E2007-ITG | CG-ALL-591 | 18 | The RTM is a separate workbook and needs the change. Story section 18 now lists TC-E2-007-01-ITG to TC-E2-007-14-ITG. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01052 | RWB-ITG-E2001-ITG | DOR-RWB-ITG-E2001-ITG-1 | 1 | Add a role code and name for 'member of the integration and test team (QA)', or confirm an existing role to use in section 1. |
| CDC-01082 | RWB-ITG-E2002-ITG | DOR-RWB-ITG-E2002-ITG-1 | 1 | Add a role code and name for the integration and test team (QA), or name the existing role code that section 1 should use. |
| CDC-01108 | RWB-ITG-E2003-ITG | DOR-RWB-ITG-E2003-ITG-1 | 1 | Add a role code or name for the member of the integration and test team (QA), or name the existing role that section 1 uses. |
| CDC-01122 | RWB-ITG-E2004-ITG | DOR-RWB-ITG-E2004-ITG-1 | 1 | Provide a role code for the integration and test team (QA) member. The code is Not specified in the source documents (DOR-RWB-ITG-E2004-ITG-1). |
| CDC-01153 | RWB-ITG-E2005-ITG | DOR-RWB-ITG-E2005-ITG-1 | 1 | Add the role 'member of the integration and test team (QA)' or record its role code |
| CDC-01162 | RWB-ITG-E2006-ITG | DOR-RWB-ITG-E2006-ITG-1 | 1 | Add a role code or role name for 'member of the integration and QA team', or confirm the existing role that section 1 should name. |
| CDC-01164 | RWB-ITG-E2006-ITG | DOR-RWB-ITG-E2006-ITG-6 | 10 | Add role RW-ADMIN (Platform administrator) to the role list |
| CDC-01187 | RWB-ITG-E2007-ITG | DOR-RWB-ITG-E2007-ITG-1 | 1 | Name a role code or name for the integration and QA team member, or add that role, so §1 matches; no code is given in the source documents. |

### RWB-P2-E2007-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01192 | RWB-ITG-E2007-ITG | GAP-0596 | 3 | Answer each Section B field as fieldState AVAILABLE or NOT_AVAILABLE with no value on NOT_AVAILABLE; name flag rwb.dataengine.booking-facts, off until the Section B migration is applied; record the reading in the next TSD P1 version and Section B notes. |
| CDC-01193 | RWB-ITG-E2007-ITG | GAP-0597 | 12, 12.1 | Publish GET /batch-status with key pair sourceSystem and businessDate and six values status, isComplete, startedAt, completedAt, recordCount, feedVersion; 404 with MSG-P1-001 when no batch row; state it is the gate read; add to next API Specification version. |
| CDC-01194 | RWB-ITG-E2007-ITG | GAP-0594 | 11, 12 | Publish GET /booking-facts and GET /batch-status on /api/recovery/source-data/v1 with BookingFact, BookingFactsAnswer, FieldState, BatchStatusAnswer per RWB-P1-E2007-APP section 11; freshness as DataProductFreshness of RWB-P1-E1015-CON; add to next API Specification. |
| CDC-01195 | RWB-ITG-E2007-ITG | GAP-0595 | 4 | Read account set and product group from case_list_row for case and business date; if not accepted, add C RWB-P3-E1018-CON and declare GET /api/recovery/case/v1/cases/{caseId}/accounts; do not read rwb_case.case_account. |
| CDC-01198 | RWB-ITG-E2007-ITG | GAP-0598 | 4, 12, 13 | Fix the read answer as account facts only, with no treatment term, outcome, difference, tolerance or package version; state BookingMatchFacts is built by the calling slice; add a contract test failing on any outcome-shaped field. |
| CDC-01201 | RWB-ITG-E2007-ITG | GAP-0730 | 4 | Publish the gateway-bff composite route field list, hop list and masking, the rwb-treatment booking fields and the raiseTask result schema; fix the rwb-case login in the platform DB story. |
| CDC-01202 | RWB-ITG-E2007-ITG | GAP-2486 | 12 | Publish the operation set, paths and payloads from the six legacy interfaces on the DP-13 per-service base with one hop and 2 s timeout; fix the LOV-DECISION code, read filters, page size, ordering and MSG-GEN-006 text with owners before SIT. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01047 | RWB-ITG-E2001-ITG | CG-ALL-526 | 12.2 | Publish GET /api/recovery/source-data/v1/admin/data-quality/exceptions in rwb-source-data.yaml through the provider's CON story. |
| CDC-01049 | RWB-ITG-E2001-ITG | DOR-RWB-ITG-E2001-ITG-8 | 12.2 | Publish GET /api/recovery/source-data/v1/admin/data-quality/exceptions in rwb-source-data.yaml. |
| CDC-01116 | RWB-ITG-E2004-ITG | CG-ALL-553 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP04/records through the provider's CON story. |
| CDC-01119 | RWB-ITG-E2004-ITG | DOR-RWB-ITG-E2004-ITG-8 | 12.4 | Publish GET /api/recovery/source-data/v1/data-products/DP04/records (CG-ALL-553). The event-type part is fixed in this story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01051 | RWB-ITG-E2001-ITG | CG-ALL-529 | 16 | Add rows for TC-ITG-E2001-01, -02, -03 and -04 with Given, When and Then copied from AC9, AC10, AC11 and AC12. |
| CDC-01081 | RWB-ITG-E2002-ITG | CG-ALL-542 | 16 | Add rows for TC-E2-002-11-ITG with Given, When and Then copied from ITG AC7 (decision record write fails on the R-RES-29 move). |
| CDC-01121 | RWB-ITG-E2004-ITG | CG-ALL-557 | 16 | Add TC-E2-004-15-ITG and TC-E2-004-16-ITG to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-01186 | RWB-ITG-E2007-ITG | CG-ALL-589 | 16 | Add a row for TC-E2-007-11-ITG (Principle 5, NFR) with Given, When and Then copied from the criterion it covers. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01077 | RWB-ITG-E2001-ITG | GAP-2468 | find it | Carry the six platform CON rows and RWB-P7-E2005-CON in the dependency map; keep lane L-ITG-W2 at Day 1 because each added H row is a platform contract. |
| CDC-01078 | RWB-ITG-E2001-ITG | GAP-1335 | header | The header now lists the platform CON dependencies. The sequencing in the dependency map sits outside this story. |
| CDC-01104 | RWB-ITG-E2002-ITG | GAP-1337 |  | Sequencing of the pattern-added platform and published dependencies belongs in the wave 2 dependency map; they are not added to the metadata rows. |
| CDC-01173 | RWB-ITG-E2006-ITG | GAP-1343 |  | Publish the six DP-added dependencies with this story as consumer in the Story Build Order and Dependency Map; confirm RWB-P4-E1037-CON in the wave 2 contract review. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01079 | RWB-ITG-E2002-ITG | CG-ALL-539 | 13 | Create story RWB-P7-E1073-CON, or give the existing P7 rule-package story key to name in the header and section 13 DP-04. |
| CDC-01117 | RWB-ITG-E2004-ITG | CG-ALL-554 | 13 | Create the story file RWB-P7-E1073-CON, or name the existing story that holds this capability. |
| CDC-01181 | RWB-ITG-E2007-ITG | CG-ALL-584 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story that carries this capability in the DP-04 row. |
| CDC-01183 | RWB-ITG-E2007-ITG | DOR-RWB-ITG-E2007-ITG-21 | header | The Contract dependencies row names RWB-P2-E2007-CON (GAP-2488). Publication of that contract is outside this story. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01086 | RWB-ITG-E2002-ITG | GAP-0908 |  | Add the POST /authorise path and the GET /me/permissions view with request and answer schemas, state whether the plan reference travels in the authorise request, and stub them in the contract fake. |
| CDC-01109 | RWB-ITG-E2003-ITG | GAP-0915 | find it | Fix the masking answer schema: the per-role row, marker values clear and masked, last-four shape and masking version. |
| CDC-01132 | RWB-ITG-E2004-ITG | GAP-0917 | find it | Freeze the authorise and doa-limits request and answer schemas at contract review and load the two capability areas into the policy pack as rows (RWB-P4-AD002-APP). |
| CDC-01197 | RWB-ITG-E2007-ITG | GAP-0922 | find it | Add POST /authorise with request and answer schemas to the API specification and TSD P4 appendix T-A; stub it in the contract fake; fix rwb-access login in the platform DB story; publish the composite route with gateway-bff (DP-19). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01120 | RWB-ITG-E2004-ITG | GAP-2474 | none | Add GET /rule-catalog/{ruleId}?packageVersion= as a P7 row before the wave 2 baseline tag; record the entry read as API-P7-007 of RWB-P7-E2005-APP. |
| CDC-01127 | RWB-ITG-E2004-ITG | GAP-1713 | find it | Map each FEAT prerequisite to the owning service contract (P7, P3, P5, P6, S1) and record the mapping once in the service contract; carry the duplicate FEAT-CHO-08 as written. |
| CDC-01139 | RWB-ITG-E2004-ITG | GAP-1698 | 6 | Add rows for the contracts, the settlement and deed-in-lieu agreements and the plan timers, owner S2, alongside the existing treatment row. |
| CDC-01168 | RWB-ITG-E2006-ITG | GAP-2478 |  | Assign delegation_limit to rwb-access and publish the level read there; correct the DP-07 row of Template and Rules v1 section R5.5 to rwb-access. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01166 | RWB-ITG-E2006-ITG | GAP-1713 |  | Prerequisites are feature codes with no owning service. The service mapping belongs in the Service Contract Catalog. No story edit. |
| CDC-01167 | RWB-ITG-E2006-ITG | GAP-0663 | 7 | At wave 2 contract review publish the rwb-integration login, resource placement, operation names and field sets for the credit pack reads and result, ownership split and reference-data read path. |
| CDC-01176 | RWB-ITG-E2006-ITG | GAP-2690 | 12 | Record the two treatment operations and credit-result element set against rwb-treatment; level comparison and delegation version against rwb-access; ledger entry and sealing order against rwb-decision; SCR-14 merge against the edge contract. |
| CDC-01177 | RWB-ITG-E2006-ITG | GAP-2482 | 12 | Fix source_type CREDIT_APPROVAL and source_ref as the treatment id for a D5 row; state that a credit result is recorded through approve or refuse on that row. |

### RWB-P2-E2001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01064 | RWB-ITG-E2001-ITG | GAP-2259 | 12 | Publish the candidate page and EFS history page operations (paths, request and response shapes, error envelopes). The rwb-source-data contract stories must publish the ledger append, REC-05 break and REC-01 result. |
| CDC-01066 | RWB-ITG-E2001-ITG | GAP-2463 | 7 | Confirm at contract review the repeat-count mechanism: a meter of rwb-decision on the operational dashboard and a response header on record submission, read by rwb-integration run summary. |
| CDC-01074 | RWB-ITG-E2001-ITG | GAP-0589 | 12.2 | Answer one account and business date per call with a configured row cap and no page parameter; answer a held read with 409 and a problem body naming MSG-P1-001 and the load date. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01067 | RWB-ITG-E2001-ITG | GAP-2466 | 12 | Record the move of the EFS history append out of recovery.decision.api to rwb-source-data (DP-18); history items stay on the P7 entry as evidence. |
| CDC-01136 | RWB-ITG-E2004-ITG | GAP-1341 | 12 | Record the legacy TimerScheduler, JOB-05 and TimerDue wording of RWB-E2-004 as superseded by Architecture v5 slides 42 and 44. |
| CDC-01148 | RWB-ITG-E2004-ITG | GAP-2476 | - | Record how an INSTALLMENT_DUE or CURE_PERIOD timer running at cut-over is carried into the workflow that owns the wait, and remove legacy Quartz timer steps and assertions from the target test set. |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01069 | RWB-ITG-E2001-ITG | GAP-1332 | 12 | Fix the DecisionRecorded payload and inputs snapshot with business date, queue and owner identifiers, hand-over reference, actions and composite idempotency key; confirm with the hand-over contract owner before wave 2 build. |
| CDC-01096 | RWB-ITG-E2002-ITG | GAP-1336 | 12 | Fix the model answer, inputs snapshot and announcement element names in RWB-P7-E1073-CON and RWB-PLT-E1027-CON, and publish the per-service login, before the wave 2 build. |
| CDC-01097 | RWB-ITG-E2002-ITG | GAP-1338 | 12 | Settle in the ledger contract whether a route move running two rules is one entry with the second rule in its actions or two entries; then align this harness and the case story to that answer. |

### RWB-P7-E2002-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01093 | RWB-ITG-E2002-ITG | GAP-2469 |  | Publish the registry version answer and decision-log item field names, the artifact column and checksum coverage, the read page size, the service login and one refusal message identifier. |
| CDC-01095 | RWB-ITG-E2002-ITG | GAP-2472 | 12 | Keep the plan read with rwb-integration under RWB-P2-E2002-CON; restate the legacy endpoint on the rwb-decision registry and decision-record slice only, on that service's base. |
| CDC-01100 | RWB-ITG-E2002-ITG | GAP-2470 | 13 | Complete the Depends on (build) and contract rows of the P7 APP metadata from the DP table, or state in R5.5 that platform H rows and self-referential C rows are not repeated on the APP line. |

### RWB-PLT-N001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01098 | RWB-ITG-E2002-ITG | GAP-0386 | 15 | Publish the gateway-bff composite case-record route path and merge order; integration lead and QA agree harness repository, environments, seed values, evidence format, retention and gate at wave 2 entry check. |
| CDC-01099 | RWB-ITG-E2002-ITG | GAP-0773 | 15 | Publish the SCR-03 composite route: path, the two parallel calls, live-answer-wins merge with MSG-P2-008 fallback, masking rule and 2 s budget split. |
| CDC-01115 | RWB-ITG-E2003-ITG | GAP-0913 | 15 | Publish the composite route for SCR-03 and its other products panel with its field list and its masking step. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01105 | RWB-ITG-E2003-ITG | DOR-RWB-ITG-E2003-ITG-14 | find it | Record the signed epic design sign-off in the epic design record. |
| CDC-01118 | RWB-ITG-E2004-ITG | DOR-RWB-ITG-E2004-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-E2004-ITG in the epic design record. |
| CDC-01150 | RWB-ITG-E2005-ITG | DOR-RWB-ITG-E2005-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-W2 |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01113 | RWB-ITG-E2003-ITG | GAP-0914 | 16 | Confirm the PII access event of the other-products read is written once by rwb-integration through ACE Common on INT-22, and that rwb-access writes no audit event for it. |
| CDC-01134 | RWB-ITG-E2004-ITG | GAP-0389 | 13 | Publish the composite case-record route path and its merge order for gateway-bff. Story harness text in section 13 now states the agreed harness approach. |
| CDC-01191 | RWB-ITG-E2007-ITG | GAP-0657 |  | Record the slide 44 JOB-08 rwb-payment row as superseded for rwb-integration; record TSD P2 v3 T5.2 as superseded; read every ACE fact through the rwb-source-data contract. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01135 | RWB-ITG-E2004-ITG | GAP-0703 | 12 | Add rwb-case as a consumer of rwb.treatment.TreatmentApproved.v1; confirm rwb-case consumes rwb.payment.PaymentMissed.v1 and holds the route state and durable plan timer in CaseWorkflow. |
| CDC-01178 | RWB-ITG-E2006-ITG | GAP-2483 | 12 | Section 12.4 names rwb.decision.DecisionRecorded.v1 per Kafka Catalog v1. Confirming it as the D5 carrier belongs to the catalogue. |
| CDC-01210 | RWB-ITG-E2007-ITG | GAP-2692 | find it | Add booking.missing.grace_loads and the treatment-type and outcome list codes to the registers; record TreatmentBooked ownership against rwb-payment in the event catalogue; record the parent stage outcome contract in the rwb-case baseline; confirm the split when RWB-P2-E2007-CON is published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01159 | RWB-ITG-E2006-ITG | CG-ALL-575 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-01180 | RWB-ITG-E2007-ITG | CG-ALL-583 | 12.2 | Publish POST /api/recovery/access/v1/authorise (owner P4 rwb-access) through the provider's CON story. |
| CDC-01184 | RWB-ITG-E2007-ITG | DOR-RWB-ITG-E2007-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml (CG-ALL-583). Event type part is resolved in §12.4 (CG-ALL-585). |

### RWB-ITG-E2001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01048 | RWB-ITG-E2001-ITG | DOR-RWB-ITG-E2001-ITG-21 | header | RWB-ITG-E2001-CON is not a story of the set, so it is not listed as a dependency. The contract must be published by its provider and added to the set. |
| CDC-01060 | RWB-ITG-E2001-ITG | GAP-0652 |  | Fix the workflow, nine activities, twelve summary elements and retry policy. Fix the six P1 elements and the P3 element with this story's names as default, use placeholders for unsourced paths and fields, and publish six fakes from owners' OpenAPI with drift failing the build. |

### RWB-P7-E2005-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01068 | RWB-ITG-E2001-ITG | GAP-2464 | 12 | Fix GET /decision-log parameters caseId, decision, ruleId, ruleVersion, approver, from, to, page and size; page size 1 to 500; order by decided_at. |
| CDC-01070 | RWB-ITG-E2001-ITG | GAP-2462 | 7 | Add the element lists of decision_log_entry.actions and decision_log_entry.outcome to the DecisionLogEntry resource and the RWB-PLT-E1027-CON record shape at contract review. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01075 | RWB-ITG-E2001-ITG | GAP-1334 | find it | Fix the LedgerChainCheckWorkflow, activity and JOB-14 Schedule names before wave 2 build; publish the per-service login of rwb_decision with the database platform story. |
| CDC-01130 | RWB-ITG-E2004-ITG | GAP-3177 | find it | Register the five-minute next-action Temporal Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01085 | RWB-ITG-E2002-ITG | GAP-0907 | 7 | This story's AC9 already states RW-REFADM holds no Case record right; the matrix change is outside this story. |
| CDC-01196 | RWB-ITG-E2007-ITG | GAP-0923 | find it | Add Case record and Treatment and offer columns; publish the 14-area matrix as data; confirm RW-RESTRUCT and RW-CREDITAD letters (CASE_RECORD R and U, TREATMENT_AND_OFFER R) with the matrix owner. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01133 | RWB-ITG-E2004-ITG | GAP-0918 | 12.1 | Add API-P4-022 GET /doa-limits with the request and answer fields of story section 12.1 and the outcome value set; RWB-P4-E2013-APP consumes the same operation. |
| CDC-01169 | RWB-ITG-E2006-ITG | GAP-2479 |  | Add GET /api/recovery/access/v1/doa-limits with decisionCode, regulationItem, productGroup, amount, asOfDate to the rwb-access contract; publish texts of MSG-P7-010, MSG-GEN-006, MSG-P4-003. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01160 | RWB-ITG-E2006-ITG | DOR-RWB-ITG-E2006-ITG-21 | section header | Contract dependencies row reads Not specified in the source documents (DOR-RWB-ITG-E2006-ITG-21) |
| CDC-01161 | RWB-ITG-E2006-ITG | DOR-RWB-ITG-E2006-ITG-8 | header | Publish the credit-result POST in rwb-integration.yaml and the authorise POST in rwb-access.yaml (CG-ALL-574, CG-ALL-575). |

### OTHER:FSD P3 (Functional Specification, module P3); OTHER:A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01050 | RWB-ITG-E2001-ITG | GAP-1549 | find it | Restate the A1.5 read path for ACE data as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01053 | RWB-ITG-E2001-ITG | DOR-RWB-ITG-E2001-ITG-12 | 16, 18 | Add TC-ITG-E2001-01 to 05 to Test Cases v8; align section 18 test lists with RTM v7. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01054 | RWB-ITG-E2001-ITG | DOR-RWB-ITG-E2001-ITG-9 | 14 | Align the P3 text of MSG-P2-006 to Standard v4. The standard wording is Not specified in the source documents (DOR-RWB-ITG-E2001-ITG-9), so the section 14 row is not changed here. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01055 | RWB-ITG-E2001-ITG | GAP-3175 |  | Keep AceDataReady (EV-26) as the target event name on rwb.source-data.events.v1 and list LoadCompleted as its legacy alias. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01056 | RWB-ITG-E2001-ITG | GAP-3176 |  | Confirm no Epic 2 step depends on JOB-01 and carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### RWB-P2-E2001-CON; RWB-P1-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01057 | RWB-ITG-E2001-ITG | GAP-0592 |  | Keep the split. P1 answers GET /entry-candidates; this story answers GET /entry-candidate-facts?businessDate= as one row per candidate account key with personKey, productGroup and REC-05. Publish both and correct the per-candidate wording. |

### OTHER:Harness pack (values held as data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01058 | RWB-ITG-E2001-ITG | GAP-0388 |  | Agree the composite route paths and merge order with the platform edge story; agree the harness repository, SIT and UAT environments, seeding for 2026-12-14 to 2026-12-17 and A-0001 to A-0004, evidence format, retention and pass/fail gate with QA at wave 2 entry. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:TSD P2 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01059 | RWB-ITG-E2001-ITG | GAP-0651 |  | Mark TSD P2 v3 T5.2 and the P2 inbound exclusion as superseded by DP-05 and ADR-010. Hold the run summary in the activity result and one local decision record, with REC-01 written through P1 and no rwb-integration table. Login name Not specified in the source documents (GAP-0651). |

### RWB-P2-E2001-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01061 | RWB-ITG-E2001-ITG | GAP-0653 |  | Keep chart, consumer group, registration, migration, six series, four alerts and four runbook entries there; environment values in a values file; unnamed message IDs as placeholders; on-call review. |

### OTHER:TSD P7 API-P7-006 and the decision-log contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01062 | RWB-ITG-E2001-ITG | GAP-1333 |  | Add the businessDate filter, the full DecisionLogPage and DecisionLogEntry field set and the page-size limit, and name one screen or panel for a decision entry beside the case with the audit query story and gateway-bff owner. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01063 | RWB-ITG-E2001-ITG | GAP-2258 | 5, 12.2 | Sections 5 and 12.2 state the recommended option. The operation and its path must be published in rwb-case.yaml. The P1 rerun stays for the role refusal. |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01065 | RWB-ITG-E2001-ITG | GAP-2260 | 11 | Mark the interaction object in T3.1 as owned by rwb-source-data under DP-18 and re-scope the P3 ledger store story to the P1 contract. |

### RWB-PLT-E1047-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01071 | RWB-ITG-E2001-ITG | GAP-2262 | 12 | Fix the envelope and retry settings of rwb.case.events.v1 with RWB-PLT-TE006-CON; limit the CaseCreated payload to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate and dpdAtEntry. |

### OTHER:RWB-PLT-OBS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01073 | RWB-ITG-E2001-ITG | GAP-2465 | none | Register ingest lag as a metric with the threshold as a parameter; route the gap alert to RW-PLATADM under RWB-P7-E1027-APP. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01076 | RWB-ITG-E2001-ITG | GAP-2467 |  | No story edit. The story names no decision value; the exact list value is for RW-COE to confirm and load as data. |

### RWB-P2-E2002-CON; RWB-P3-E2042-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01080 | RWB-ITG-E2002-ITG | DOR-RWB-ITG-E2002-ITG-21 | header, 13 | Contract dependencies row and section 13 now name the two CON stories; publishing them (Done and catalogued) belongs to those stories. P2 CON is Not started. |

### OTHER:Screen specification of SCR-03; OTHER:SCR-14 and SCR-38 (owning document not named in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01083 | RWB-ITG-E2002-ITG | DOR-RWB-ITG-E2002-ITG-10 | 15 | Section 15 now lists the missing states as not-specified rows (CG-ALL-544 to 546); the state assertions belong to the screen owner. |

### OTHER:rwb-comms (P6) story of legacy RWB-E2-042 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01084 | RWB-ITG-E2002-ITG | GAP-2395 |  | Fixtures: RESTRUCTURE RES-2026.12, PAYMENT_MATCH PMT-2026.12, BOOKING_MATCH BKG-2026.12. Settle the rwb-comms package with the rule registry owner before integration. |

### RWB-P2-E2002-CON; RWB-P2-E2002-OPS; RWB-P3-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01087 | RWB-ITG-E2002-ITG | GAP-0654 |  | Settle in the wave 2 contract review: the rwb-integration login, the case read and its contract story, the field sets, the owner of live and messageCode, the two settings, the connection-matrix rows and one daily step. |

### RWB-P2-E2002-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01088 | RWB-ITG-E2002-ITG | GAP-0655 |  | Approve the four assumptions (answer shape with accountNo, live and messageCode rule, interface contract, consumed read shapes) before the baseline is tagged; reconcile the interface-versus-view wording. |

### RWB-P2-E2002-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01089 | RWB-ITG-E2002-ITG | GAP-0656 |  | Approve the three assumptions in the release readiness review; carry every threshold and endpoint as an environment value, never as code. |

### OTHER:P7 contract story (rwb-decision /api/recovery/decision/v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01090 | RWB-ITG-E2002-ITG | GAP-0770 |  | Publish the catalog-row read by rule ID and package version returning action_text, owner_role, timer_spec, target queue code and outputs. |

### OTHER:Reference-data story of the service; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01091 | RWB-ITG-E2002-ITG | GAP-0771 |  | Add a table code for the plan event map to LOV-REF-TABLE and load its rows as reference_row under a reference_version, one row per ACE status and route state pair. |

### OTHER:Platform database story (19-schema list); OTHER:Key Vault and Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01092 | RWB-ITG-E2002-ITG | GAP-0774 |  | Allocate the rwb-case login with its schema, derive the name from the schema, hold the secret in Key Vault and record it in the Service Catalog before first deployment. |

### OTHER:rwb-decision decision-record contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01094 | RWB-ITG-E2002-ITG | GAP-2471 |  | State one entry per case, business date and rule identity, with one entry per rule in a two-rule transaction; publish the content model of the inputs snapshot and actions payload. |

### OTHER:P1 contract story for rwb-source-data (reconciliation_result) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01102 | RWB-ITG-E2002-ITG | GAP-0772 | 5 | Publish a break operation (product, check, key, detail, owner role) on the rwb-source-data contract and have the plan-status step call it once per rejected or missing plan. |

### OTHER:Platform DB story (rwb-access login) and gateway-bff composite route for SCR-03 (DP-19) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01103 | RWB-ITG-E2002-ITG | GAP-0909 |  | Name the rwb-access per-service login and publish the SCR-03 composite route field list, hop list, merge order and masking rule. |

### RWB-ITG-E2003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01106 | RWB-ITG-E2003-ITG | DOR-RWB-ITG-E2003-ITG-21 | header | Contract dependencies row reads Not specified in the source documents. |

### OTHER:Contract fake library (WireMock fakes from owning services' OpenAPI, section 12.8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01107 | RWB-ITG-E2003-ITG | DOR-RWB-ITG-E2003-ITG-22 | find it | Publish the contract fake library and record its version as published. |

### OTHER:P1; OTHER:P3 and P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01110 | RWB-ITG-E2003-ITG | GAP-0662 | find it | Keep the endpoint on base /api/recovery/integration/v1 (DP-13). Read holding and freshness via rwb-source-data, parties and accounts via rwb-case, authorise and masking via rwb-access, PII event via ACE Common (INT-22). Keep flag rwb.integration.customer-products. Fix contract field names in the P1, P3 and P4 contract stories. |

### RWB-PLT-N001-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01111 | RWB-ITG-E2003-ITG | GAP-0390 | find it | Integration lead and QA agree harness repository, SIT and UAT environments, seed data, evidence format, gate. RWB-PLT-N001-CON publishes the gateway-bff composite route and merge order. The next LDM version publishes the field IDs of permission, masking_rule, rwb_case reference rows and rwb_source_data freshness tables. |

### RWB-PLT-E1044-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01114 | RWB-ITG-E2003-ITG | GAP-0916 | 16 | Name the rwb_access login and grant it SELECT on its own schema only. |

### RWB-P3-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01123 | RWB-ITG-E2004-ITG | DOR-RWB-ITG-E2004-ITG-10 | none | Add empty, loading, error and no access states to SCR-03, SCR-09, SCR-14 and SCR-38. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01125 | RWB-ITG-E2004-ITG | GAP-2404 | find it | Record the five platform contracts and the seven contract entries named for DP-03, DP-06, DP-07, DP-09 and DP-19 in the metadata; this story needs no edit. |

### OTHER:FSD P6 v3 and TSD P6 v2 (rules component package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01126 | RWB-ITG-E2004-ITG | GAP-2395 | find it | Name which of the six Epic 2 packages a notice of rwb-comms reads and assign the package code; no fourth package code is to be invented. |

### RWB-P8-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01129 | RWB-ITG-E2004-ITG | GAP-1346 | find it | Name the seven consumed rows in section 12.2 with the placeholder until each owner publishes its operation; confirm scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON. |

### OTHER:rwb-case OpenAPI file (GET /cases/{caseId}/timers) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01131 | RWB-ITG-E2004-ITG | GAP-0705 | find it | Record treatmentId, timerType, startedAt, expiresAt, warnAt, paused and status as optional within major version 1, with expiresAt as an offset date-time, after review with RWB-P3-E1028-CON. |

### RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01137 | RWB-ITG-E2004-ITG | GAP-2473 | 12.2 | Publish the catalogue answer element names and media type, the decision record payload fields, the MSG-P7-009 text and field list, the system actor value and the four registry table columns. |

### OTHER:TSD S2 v2 T3.1 and context pack S2 ownership rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01138 | RWB-ITG-E2004-ITG | GAP-2687 | 12 | State the plan facts the treatment row carries for the case clock; remove the timer entity, Quartz job and TimerDue topic from S2 deliverables; keep the fourteen legacy criteria with RWB-P3-E2004-APP. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01140 | RWB-ITG-E2004-ITG | GAP-1709 | Header | State in the release slicing that the wave 2 contract and treatment record with its data date ship in wave 2 and the offer, settlement, plan and deed-in-lieu capabilities ship with E3. |

### OTHER:FSD S2 field catalogs (A2.2.3.2 and related) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01141 | RWB-ITG-E2004-ITG | GAP-1712 | 6 | Add field catalogs for the contract, agreement, plan timer and booking reference entities, keeping the eight existing catalog fields as written; the data architect fixes the physical field list. |

### RWB-P7-E1073-CON; RWB-PLT-E1027-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; RWB-P7-E2005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01142 | RWB-ITG-E2004-ITG | GAP-1339 | 13 | Fix the model and catalogue answer shapes and envelope field names; add MSG-P7-009 and MSG-P7-012 wording to the P7 message table; name the panels on SCR-38 and SCR-03; state in the build order that platform stories hold the DP-added dependencies. |

### OTHER:Template and Rules (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01143 | RWB-ITG-E2004-ITG | GAP-2475 | header | State in R5.5 that a platform H row and a self-referential C row are held by the platform and contract stories and not repeated on a secondary APP line; this story keeps the plan rows meanwhile. |

### OTHER:rwb-case values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01145 | RWB-ITG-E2004-ITG | GAP-0706 | - | Add provisional default values for the plan-timer projection lag, subscription lag, .dlt count, exception-queue count and DP04 freshness alerts, to confirm at UAT. |

### OTHER:gateway-bff route catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01146 | RWB-ITG-E2004-ITG | GAP-0920 | - | Publish the SCR-14 treatment record and SCR-03 timer panel composite routes with their field lists, and confirm no field is a personal field. |

### OTHER:Platform DB story of DP-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01147 | RWB-ITG-E2004-ITG | GAP-0921 | - | Fix the rwb-access login name, its grants and its schema owner, and let P4 stories reference them. |

### RWB-P3-E2004-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01149 | RWB-ITG-E2004-ITG | GAP-2688 |  | Name the parameters and reference-data read operations for CURE_PERIOD_DAYS, plan.warn-days and the seven lists; state field-level types, lengths and required flags of TreatmentApproved payload; publish the fake set; state the one-running-plan guard as a partial unique index on the treatment row, at major version 1. |

### OTHER:Decision-log query contract story of rwb-decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01151 | RWB-ITG-E2005-ITG | DOR-RWB-ITG-E2005-ITG-21 | header | Contract dependency named in the header without a story key. |

### OTHER:Contract fake library for the decision-log query contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01152 | RWB-ITG-E2005-ITG | DOR-RWB-ITG-E2005-ITG-22 |  | No fake library version is in the sources; the fake must be published in its own library. |

### OTHER:RWB-E2-031 app slice (agent monitoring dashboard v2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01155 | RWB-ITG-E2005-ITG | GAP-0629 |  | The app slice belongs to another story, and this story does not carry agent monitoring. No edit here. |

### OTHER:Platform message catalogue (authorise contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01157 | RWB-ITG-E2005-ITG | GAP-1249 | 12 | No source gives the message ID of the 401 answer. The platform message catalogue must assign it before the story can cite it. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01158 | RWB-ITG-E2006-ITG | CG-ALL-574 | 12.2 | Publish POST /api/recovery/integration/v1/treatments/{treatmentId}/credit-result through the provider's CON story. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01165 | RWB-ITG-E2006-ITG | DOR-RWB-ITG-E2006-ITG-7 | 11 | Add DF-ACC-009 and DF-ACC-010 to v_ace_account and DF-TRT-023 to DF-TRT-026 to treatment |

### OTHER:Decision-record schema document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01170 | RWB-ITG-E2006-ITG | GAP-2480 |  | Fix D5 actions keys as requiredLevel, delegationLimitId, limitVersion, nleadsRef, resultDate; take inputs_ref from the pack read reference; confirm NLEADS pattern with SCB IT before the wave 2 test cycle. |

### OTHER:RBAC matrix (T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01171 | RWB-ITG-E2006-ITG | GAP-2481 |  | Declare Decision log right A on the two recording operations, add A rows for result-recording roles, keep Treatment and offer right U on the rwb-integration pack endpoint. |

### OTHER:TSD S2 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01172 | RWB-ITG-E2006-ITG | GAP-2689 |  | Add the credit-result variant of the treatment PATCH with element names, If-Match and once-only rule; add SUBMITTED, APPROVED, REFUSED to the state constraint; add four credit columns with rules and refusal message. |

### OTHER:Requirement traceability register (v7 row for REQ-RDF-004) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01175 | RWB-ITG-E2006-ITG | GAP-3213 | 18 | Record REQ-RDF-004 with legacy slices RWB-E1-069, RWB-E1-018 and RWB-E2-006 and citing stories RWB-ITG-E3013-ITG, RWB-ITG-E3017-ITG and RWB-ITG-E3026-ITG; E3 trace accepted. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01179 | RWB-ITG-E2006-ITG | GAP-2484 | header | Assign GET /cases/{caseId}/recommendation read to the P7 story that serves the decision screen; treat the four platform contracts as published before Day 1. |

### RWB-ITG-E2007-ITG; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01182 | RWB-ITG-E2007-ITG | DOR-RWB-ITG-E2007-ITG-14 | find it | Record the signed epic design sign-off for this story in the epic design record. |

### OTHER:FSD S2 (A2.6.3.1; OTHER:A2.13.2; OTHER:A2.10.2; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01185 | RWB-ITG-E2007-ITG | GAP-1696 | 4, 11 | Obtain each source fact through the rwb-source-data contract; add S2 to the P1 REST cell of the connection matrix. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01188 | RWB-ITG-E2007-ITG | DOR-RWB-ITG-E2007-ITG-12 | 18 | Test Cases v8: add TC-E2-007-11-ITG to TC-E2-007-14-ITG as in story §16. RTM v7 REQ-CHO-008: add TC-E2-007-01-ITG to TC-E2-007-14-ITG. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01189 | RWB-ITG-E2007-ITG | GAP-3175 |  | Name EV-26 AceDataReady as target event on rwb.source-data.events.v1, producer rwb-source-data, with LoadCompleted listed as its legacy alias. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:44) and FSD S2 (A2.10; OTHER:A2.11; OTHER:A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01190 | RWB-ITG-E2007-ITG | GAP-1703 |  | Show rwb-payment as owner of booking, matching and posting; S2 records the booking reference from TreatmentBooked and the break from PaymentMissed, and sends the release request through the integration contract. |

### RWB-P2-E2007-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:TSD P2 Integration v3 T5.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01199 | RWB-ITG-E2007-ITG | GAP-0658 | find it | Baseline the contract shape, task table, rerun operation, twelve consumed operations and seven fakes; record JOB-08 ownership and TSD P2 v3 T5.2 supersession; confirm the seven message texts. |

### RWB-P2-E2007-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01200 | RWB-ITG-E2007-ITG | GAP-0659 | 4 | Fix the rwb-integration login, secret reference, worker identity and probe checks; write the JOB-08 job catalogue row with run book path; set the four thresholds, series windows and backfill limit as environment values; review the four runbook entries with the on-call rota. |

### OTHER:P7 context pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01203 | RWB-ITG-E2007-ITG | GAP-2487 | 4 | Step 5 marks the booking-decision event as Not specified (GAP-2487). The event name belongs in the P7 context pack. TreatmentBooked and CaseStateChanged stay with their owners. |

### RWB-S2-E3001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01204 | RWB-ITG-E2007-ITG | GAP-2691 | 4 | Add the approved-not-booked read, mark-booked write and booking-difference write with element names at the wave 2 freeze; add APPROVED and BOOKED to the state check constraint; define booking_difference as jsonb keyed by term; enforce one confirmation per treatment and business date. |

### OTHER:Parameters contract (DP-06) and TSD P4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01206 | RWB-ITG-E2007-ITG | GAP-0924 | find it | Add the cached authorise lifetime as a parameter with its value agreed at the wave 2 design review; value not specified in the source documents (GAP-0924). The story tests the version-keyed drop, not the clock. |

### OTHER:Platform secret store (ACE team allocation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01207 | RWB-ITG-E2007-ITG | GAP-2489 | find it | Allocate the rwb-decision database login with schema rwb_decision and record it in the platform secret store; login name not specified in the source documents (GAP-2489). |

### OTHER:Solution architecture register (JOB-08 workflow and schedule) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01208 | RWB-ITG-E2007-ITG | GAP-2491 | find it | Record the event-started BookingConfirmationWorkflow on queue rwb-decision at Asia/Bangkok, one run per business date, second start refused with MSG-P2-006, failed gate retried on next AceDataReady, no fallback Schedule, and the flag off stops the start with records readable. |

### OTHER:TSD P7 v2 (reporting read model for REC-03) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01209 | RWB-ITG-E2007-ITG | GAP-2492 | find it | Create no reconciliation_result table in rwb_decision; name the rwb-reporting read model that builds the REC-03 break list from events; carry field IDs as values until named. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20840 | RWB-ITG-E2002-ITG | R-22336 |  | Ledger granularity and inputs/actions payload model are set in the P7 decision-record contract, not in this AsyncAPI file. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0386 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0387 | Harness repository, environments, seeding, evidence, gate and gateway route for the decision-log audit query harness | Integration lead | Resolved (directive) |
| GAP-0388 | EFS hand-over harness: repository, environments, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0389 | The harness repository, environments, seeding, business clock, evidence format and retention, pass/fail gate and the gateway-bff composite case-record route are not defined in the source documents | Integration lead | Resolved (directive) |
| GAP-0390 | Customer other-products harness pack: repository, environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0394 | Credit approval pack integration harness: composite credit-pack route, harness environment, seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0395 | Booking confirmation integration harness: composite booking and treatment route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0589 | The history read is one operation or a paged read, and the HTTP answer of a held read, are stated by no source | Solution architect, P1 | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0592 | No source splits the hand-over facts between the candidate rule and the borrower and product-group facts, and the run's contract names a per-candidate customer read | Solution architect, P1 and P2 | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0594 | The shapes and property names of the two booking-fact reads are in no source document | Tech lead | Resolved (directive) |
| GAP-0595 | The case's account set and its product group have no P1 read in the target | Solution architect | Resolved (directive) |
| GAP-0596 | How the read answers the three Section B columns, and which flag holds it back, is stated nowhere | Data architect | Resolved (directive) |
| GAP-0597 | The batch-status answer has two values in the legacy interface and nine fields in the view, and no source fixes which of them it returns | Tech lead | Resolved (directive) |
| GAP-0598 | No source says where the account read ends and the built match facts begin | Solution architect | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0651 | rwb-integration EFS hand-over: the mount of the step, the split across four owners, the consumed contract paths, the run summary store and the level of the decision record are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0652 | rwb-integration EFS hand-over contract: the activity contract, the consumed element shapes, the provided surface and the fakes have no source text | Tech lead | Resolved (directive) |
| GAP-0653 | rwb-integration EFS hand-over deployment: the values, the alert identifiers, the dashboard series and the runbook have no source | DevOps lead | Resolved (directive) |
| GAP-0654 | rwb-integration ACE plan status: the login, the account resolution, the interface field types, the meaning of live and messageCode, the two settings, the connection-matrix rows and the ownership split are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0655 | The plan-status contract baseline: the accountNo field, the meaning and owner of live and messageCode, the interface null rules, the consumed read shapes, the composite route and the two specification conflicts are not fixed by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0656 | The plan-status deployment values, the ACE endpoint and certificate references, the two setting values at run time, the trigger wiring, the alert thresholds, the mapping of the no-package condition and the fixture owner are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0658 | rwb-integration booking confirmation (contract slice): the JOB-08 ownership and consumer lists, the ACE read boundary, the rerun placement and the twelve consumed shapes are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0659 | rwb-integration booking confirmation (deployment slice): the login and secret reference, the JOB-08 ownership, the alert thresholds, the runbook ownership and the backfill limit are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner; business on-call owner for the package alerts | Resolved (directive) |
| GAP-0662 | rwb-integration customer products read: login, contract field names, ACE view owner, endpoint and route names, masking rows and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0663 | rwb-integration credit approval pack: login, contract field names, NLEADS read, the ownership split, the integration-base resource placement and the approval-level values are not settled by any one source | Solution architect | Resolved (directive) |
| GAP-0703 | The treatment entity moves to S2 while the legacy story holds it in P3, and the case side consumes TreatmentApproved which the event catalogue does not list for rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0705 | No source fixes the plan-timer fields, types or required flags of the timers answer behind GET /cases/{caseId}/timers | Tech lead of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0706 | No source gives the alert values for the plan-timer projection, the subscription lag, the DP04 freshness or the exception-queue count | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0729 | rwb-case credit approval: login, edge route and the NLEADS and treatment contract shapes are not specified | TechX | Resolved (directive) |
| GAP-0730 | rwb-case booking confirmation: login, composite route, treatment booking fields, match-result shape and route-rule evaluator owner are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-0917 | rwb-access treatment and plan-timer slice: the authorise request and answer, the Treatment and offer and Case record letters and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0918 | The delegation lookup GET /doa-limits and its request and answer fields exist only on Architecture v5 slide 14, not in the TSD P4 appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0920 | The composite route field list for SCR-14 Treatment record and the SCR-03 timer panel is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0921 | The per-service login of rwb-access is named by DP-02 and by no document | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0922 | rwb-access booking confirmation: the authorise request and answer shapes, the contract entry of the authorise path and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0923 | rwb-access booking confirmation: the TSD RBAC matrix has no Case record column, so the CASE_RECORD R and U letters the booking tasks need are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0924 | rwb-access booking confirmation: the lifetime of a cached authorise decision is not specified | Solution architect | Resolved (directive) |
| GAP-1242 | Audit export: a synchronous full-result CSV against a 2 s one-hop budget | Solution architect, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1246 | Approver index migration sits on a table created by another story | ACE team, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1247 | First-page performance target over 10,000 entries is assumed and not fixed | Solution architect, with the QA lead | Resolved (directive) |
| GAP-1248 | Element list of the audit answer beyond the legacy names, and the element that carries the warning | Solution architect, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1249 | Message identifier of the 401 answer is not given by any source | Solution architect, with the platform library owner | Resolved (directive) |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1332 | Envelope and payload element names of DecisionRecorded, and the shape of the inputs snapshot | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1333 | Answer field set and business-date filter of the decision-log read, and the screen that shows an entry beside the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1334 | Per-service login of rwb_decision, the chain-check workflow and activity names, and the Schedule identifier of JOB-14 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1336 | Shape of the model answer, of the inputs snapshot and of the announcement, with the carrier names of the plan-status move | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1338 | One ledger entry per route move or per case and business date, for a move that runs two rules | Solution architect | Resolved (directive) |
| GAP-1339 | Values of the RESTRUCTURE catalogue and plan-timer ledger slice that no source fixes | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1341 | TimerDue and the five-minute JOB-05 check are retired in the target but kept by the legacy story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1342 | rwb-decision credit approval slice: the decide path, the delegation answer shape, the actions keys, the comparison site, the message texts, the decision sub-code, the per-service login and the screen identity are not fixed by any one source | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1344 | The delegation of authority table is ruled to rwb-access by the Ownership Map while the integration story of this key attributes the required level to rwb-decision | Solution architect | Resolved (directive) |
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1698 | The Ownership Map lists one table for rwb-treatment, although Architecture v5 gives it four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1709 | The service is wave 2 and EP02 while every requirement of the module is an Epic 3 requirement | Solution architect | Resolved (directive) |
| GAP-1712 | The field catalog covers eight fields and none of them describes a contract, an agreement, a plan timer or a booking | Data architect | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-2258 | No rerun operation for the entry run after JOB-02 becomes a workflow | TechX | Resolved (directive) |
| GAP-2259 | Paths and payloads of the P2 hand-over and P1 ledger contracts | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2260 | Interaction ledger ownership conflicts with the legacy write and the P3 data model | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2262 | CaseCreated payload and the resume of a held run are not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
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
| GAP-2473 | RWB-P7-E2004-APP: the wire shape of the rule-catalogue answer, the payload fields of the plan-timer decision record, the text of MSG-P7-009, the ledger writer identity and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2474 | RWB-P7-E2004-APP: the rule-catalogue read that two stories consume is attributed to no owner in the Ownership Map, while the entry read the same map attributes to this service is served by RWB-P7-E2005-APP | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2476 | RWB-P7-E2004-APP: the legacy plan timers run on the Quartz timer check and publish a timer-due event, both retired in the target, and no source says what happens to a plan timer already running at cut-over | Solution architect with the rwb-case service owner and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2478 | delegation_limit has no owner in the P7 rows, and three sources name three different homes for the level | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2479 | The delegation read of rwb-access has no named path, request, answer or message text | P4 and P7 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2480 | The field set of a D5 credit entry and the format of the NLEADS reference are not specified | P7 solution architect and the ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2481 | The legacy story requires the Treatment and offer right while the endpoint of this service declares the Decision log right | P4 access owner and the P7 solution architect | Resolved (directive) |
| GAP-2482 | How a D5 credit approval is identified, and whether a result is an approve or a dedicated credit-result action, is not stated | P7 solution architect and the routing story owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2483 | The event name that carries the D5 record on the service topic is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2485 | The booking-confirmation decision is placed in rwb-decision while DP-04 and the registry story keep the evaluation in the owning service and state that rwb-decision never evaluates | Solution architect, with the decision service owner | Resolved (directive) |
| GAP-2486 | The operation set, paths and payloads of the batch, account, treatment, task, parameter and list contracts, the decision code, the record's snapshot and actions shape and several read and message details are in no source | Solution architect, with the owners of rwb-integration, rwb-treatment and rwb-case | Resolved (directive) |
| GAP-2487 | No source names the event that carries a booking decision out of rwb-decision, because the legacy TreatmentBooked is rwb-payment's and is raised after the treatment is booked | Solution architect, with the event platform owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2489 | The name of the rwb-decision database login is in no source | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2490 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its eleven legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2491 | The timezone, overlap, retry and fallback of the JOB-08 run and the behaviour of the legacy feature flag when off are in no source | Solution architect, with the workflow platform owner | Resolved (directive) |
| GAP-2492 | The legacy run writes the REC-03 result to reconciliation_result, and no table or owner of that name exists in the target and no source assigns the break list | Solution architect, with the reporting owner | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2687 | The legacy treatment entity, its plan timers and its DP04 extract are split across three services, and no source states what the plan-timer data model holds on the S2 side once the clock moves to rwb-case | Solution architect with the data owner of rwb-treatment and the owners of rwb-case and rwb-source-data | Resolved (directive) |
| GAP-2688 | The parameters and reference-data operation names, the contract fake set, the field-level type of the event payload and the guard that limits a case to one running plan are not published for rwb-treatment | Contract owner of rwb-treatment with the parameters and reference-data owner of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2689 | The treatment-side credit-result record has no operation, no element names, no state values and no column rule in the S2 sources | Solution architect, S2, with the rwb-treatment tech lead and the rwb-integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2690 | The rwb-treatment share of the key is stated by no S2 source, and the caller contract, the level comparison, the case move and the record ownership are split across four stories | Solution architect with the rwb-integration, rwb-treatment, rwb-case and rwb-access tech leads and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2692 | The rwb-treatment share of the key is stated by no S2 source, the P2 contract shapes it follows are unpublished, and the trigger, the task-raising and the event ownership are split across stories | Solution architect with the rwb-integration, rwb-treatment and rwb-case tech leads and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E2006-ITG | skipped AC ID | 105 | missing: AC5, AC6, AC7, AC8, AC9, AC10, AC11 |
| RWB-ITG-E2007-ITG | skipped AC ID | 119 | missing: AC2, AC3, AC4, AC6, AC8, AC9 |
