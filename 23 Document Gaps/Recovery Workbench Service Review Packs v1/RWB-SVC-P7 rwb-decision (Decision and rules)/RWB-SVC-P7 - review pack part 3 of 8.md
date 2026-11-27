# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 3 of 8 (RWB-P7-E1052-APP to RWB-P7-E2005-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 129 |
| Cross-document (pending in another document) | 206 |
| Not applied (value not in the sources) | 24 |
| Open business decisions | 35 |
| Register gaps linked | 154 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-E1052-APP | 18 | 35 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1052 APP Notice generation v1 v2.md |
| RWB-P7-E1054-APP | 17 | 24 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1054 APP Review queue for low-confidence documents v2.md |
| RWB-P7-E1073-APP | 26 | 31 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1073 APP Rule authoring, validation, test scenarios, approval and rollback in Drools v2.md |
| RWB-P7-E2001-APP | 18 | 29 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2001 APP EFS hand-over with full history v2.md |
| RWB-P7-E2002-APP | 17 | 26 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2002 APP ACE plan status on the case v2.md |
| RWB-P7-E2004-APP | 11 | 36 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2004 APP Treatment entity and plan timers data model v2.md |
| RWB-P7-E2005-APP | 22 | 11 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2005 APP Decision log query API for audit v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P7-E1052-APP | R-11215 | CG-ALL-6997 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1054-APP | R-11224 | CG-ALL-7017 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1073-APP | R-11230 | CG-ALL-7029 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2001-APP | R-11232 | CG-ALL-7037 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2001-APP | R-11233 | CG-ALL-7040 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-P7-E2001-APP | R-11234 | CG-ALL-7041 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-P7-E2002-APP | R-11237 | CG-ALL-7047 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2004-APP | R-11241 | CG-ALL-7060 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2005-APP | R-11243 | CG-ALL-7068 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1025-APP, RWB-P5-E1052-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-22159 | GAP-2347 | Register gap | Data steward and document type owner, with the Legal counsel and the P5 TechX squad | The notice-type to document-type mapping, the retention class and the write-once flag of each notice document type are not specified in any source read here | The document type load of RWB-P5-E1025-APP carries the DEMAND_LETTER and GUARANTOR_NOTICE rows with their class and flag, and the notice-type mapping row is added to the type or mapping table before the wave-1 test data is loaded |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2001-ITG, RWB-P1-E1011-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22306 | GAP-0591 | Register gap | Data steward and data product owner, P1 | The REC-05 break list row for a hand-over key is defined only for keys on an existing Workbench table, not for a candidate that has no row yet | Answer the break in the candidate-facts read as {check: REC-05, keyType: PERSON_KEY or ACCOUNT_KEY, key: <value>} with resolution HELD, write no row and invent no fact, and let RWB-P1-E1011-APP's REC-05 step carry the row for the business date so the data steward and the ACE team read one list. Fix the answer in RWB-P2-E2001-CON. |
| RWB-ITG-E2001-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22309 | GAP-0588 | Register gap | Data steward and data product owner, P1 | The collection period of an account's EFS history is named by no source, so the boundary of the history read is undefined | Fix the period as the EFS assignment window of the account: it opens at v_ace_efs_assignment.assignment_start_date and closes at assignment_end_date, or at the business date of the read for the open assignment; when the account has no assignment row the period opens at its earliest contact_at. Publish the rule in RWB-P2-E2001-CON with the answer so the run and this service read the same boundary, and ask the data steward to confirm it with the ACE team before wave 2 exit. |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E1038-APP, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22353 | GAP-0919 | Register gap | Business lead | Which delegation limit version is in force on the approval date of a treatment is a data state, not a document value | Decide the version in force per environment at the DoA load (RWB-P4-E1038-APP) and keep it out of code; the lookup always answers the version whose window covers the date asked, and the answer names it |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22357 | GAP-0704 | Register gap | Data product owner | The 01:30 treatment extract has no owner in the target and its DP04 read path and freshness element are not in the Ownership Map | Record the owner of the treatment extract as P9 rwb-reporting on JOB-15 with the DP04 copy in rwb_source_data, publish the case-facing read GET /api/recovery/source-data/v1/data-products/DP04/records with its freshness element in the Ownership Map and the P1 API file, and state in the event catalogue that the copy is built from the treatment events. |
| RWB-ITG-E2005-ITG, RWB-P4-E1037-CON, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-22366 | GAP-1243 | Register gap | Compliance and PDPA officer, with the P4 access owner | Whether the audit role may see unmasked person keys in an entry or an export | The audit read and the export carry the masked value under the policy of rwb-access in force, with no unmasking operation on either read; Compliance either confirms that reading or publishes an audit-specific policy row before the wave 2 exit. |
| RWB-ITG-E2005-ITG, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-22368 | GAP-1241 | Register gap | Compliance and PDPA officer, with the P7 business lead | Decision log retention period is not set | Compliance fixes the retention period and the archive rule for decision_log_entry as reference data before the wave 2 exit; until then the store keeps every entry, the query purges nothing and archives nothing, and the value is read as a parameter when it arrives. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1052-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-28611 | GAP-2088 | Register gap | Business lead with Legal and Compliance; document owner | DL10 is listed open with one answer and is recorded as answered with another | Keep the source row word for word, record in section 6.1 that DL10 is answered on 5 November 2026 with answer A, and add no Thai wording in this document. |
| RWB-ITG-E1073-ITG, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28681 | GAP-0006 | Register gap | RW-COE and RW-RISK | Rule format XLS decision tables or DMN 1.6 | Keep XLS tables for the Phase 1 packages and convert one table at a time, with both formats on the same runtime |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28693 | GAP-2047 | Register gap | Solution architect with Risk and Internal Audit | The decision log is now written locally by each service and sealed centrally | Version 4 measures the local decision record of each service and the central ledger of P7 rwb-decision as two instances of the same two alerts, with the chain check read per service and once for the ledger. |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28694 | GAP-2051 | Register gap | P7 rwb-decision with Compliance and Internal Audit | The hash chain check now spans 19 local chains and one central ledger | Version 4 raises the alert on the local chain of each service and once on the central ledger, and attributes a break to the service whose chain fails; the run book of RWB-E1-073 and RWB-E2-037 names the check. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-ITG-E2005-ITG, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-28719 | GAP-1244 | Register gap | Business analyst, P7, with Compliance | REQ-ACA-006 and NFR-042 still name a data-lake copy that DP-17 removes | Read REQ-ACA-006 and NFR-042 as covering the case store, the document store and the reporting read model; drop the lake wording at the next BRD and NFR version, retire the lake analysis with no target path and no dependency, and write the AC-READ/AC-EXPT record for the query path only. |
| RWB-P7-E2001-APP | R-33453 | ASM-ALL-7040 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-P7-E2001-APP | R-33454 | ASM-ALL-7041 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P7-E2005-APP | R-37452 | ASM-2205 | Register assumption |  | decision_log_entry keeps every entry with no purge, no archive and no truncation in this story, and the retention period is read as a parameter when Compliance publishes it. | Compliance and PDPA officer, with the P7 business lead |
| RWB-P7-E2005-APP | R-37453 | ASM-2207 | Register assumption |  | The audit read returns the masked value of the free-text fields under the policy of rwb-access in force, offers no unmasking operation, and the export carries the same masking as the screen. | Compliance and PDPA officer |
| RWB-P7-E2005-APP | R-37454 | ASM-2208 | Register assumption |  | REQ-ACA-006 and NFR-042 are read as covering the case store, the document store and the reporting read model, and the legacy lake analysis is retired with no target path. | Business analyst, P7, with Compliance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-E1052-APP | R-06727 | DOR-RWB-P7-E1052-APP-7 | 11 | Definition of Ready item 7 Data: Fail | Cited faults sit in §13 (index), §7 and §16 (ACE view reads), outside this chunk. §11 already matches DF-DEC-016 decided_at in LDM v9. No edit made here. |
| RWB-P7-E1052-APP | R-11212 | CG-ALL-6991 | 4, 12.1 | HTTP errors with no message ID: 401 no session; 422 a query value is outside its list; 503 the ledger is unavailable. Every error is an RFC 9457 problem response with `messageId` set. The recommendation read and the approval operations of this service belong to its approval and recommendation stories and are declared neither as provided nor as consumed here | Error and Message Standard v4 has no message ID that fits 401 or 422; MSG-GEN-006 for 503 is a queue-and-retry message, not a read. Placeholders stand for the business analyst to confirm. |
| RWB-P7-E1052-APP | R-17973 | DOR-RWB-P7-E1052-APP-11 | 8, 11 | Definition of Ready item 11 Guardrails: Partial | Data Classification v5 flags every decision_log_entry field Yes, so no single field can be named as personal data without inventing one. |
| RWB-P7-E1052-APP | R-17977 | DOR-RWB-P7-E1052-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Criteria and test rows for BR1, BR3, BR5, BR10, BR13 and BR14 sit in §7 and §16, outside this chunk; no anchor text is available, so nothing was added unseen. |
| RWB-P7-E1052-APP | R-17978 | DOR-RWB-P7-E1052-APP-9 Messages: Partial | 14 | Definition of Ready item 9 Messages: Partial | MSG-P7-009 keeps its placeholder until the standard has a new ID (CG-ALL-6993). MSG-P1-001 was already matching and is unchanged. |
| RWB-P7-E1052-APP | R-26254 | CG-ALL-6998 | 13 | Flyway file V1052_1__decision_log_notice_index.sql is not in the V0001..Vnnnn form | Line 419 is outside this chunk and blank here. The next free number of the rwb_decision Flyway sequence is not in the sources found, so no number is invented. |
| RWB-P7-E1054-APP | R-26263 | CG-ALL-7018 | 3, 3.1 | Flyway file V1054_1__review_decisions.sql is not in the V0001..Vnnnn form | The next Flyway number for rwb-decision is not in the sources (Service Template v1 §3.1 and TSD P7 v3 DP-15 checked). No number set; the L361 rename is not made. |
| RWB-P7-E1073-APP | R-06736 | DOR-RWB-P7-E1073-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (Grep found none). A sign-off date or reference would be invented; left open. |
| RWB-P7-E1073-APP | R-06740 | DOR-RWB-P7-E1073-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version is recorded in sections 3 or 12.8 or in the sources. A version number would be invented; left open. |
| RWB-P7-E1073-APP | R-26268 | CG-ALL-7030 | 3, 3.1 | Flyway file V1073_1__rule_package_registry.sql is not in the V0001..Vnnnn form | Next free V-number of rwb_decision sequence is not in the sources; only V0001 is fixed. Line 369 text not in the supplied story parts, so no edit. |
| RWB-P7-E2001-APP | R-06747 | DOR-RWB-P7-E2001-APP-8 Contract: Fail | 4 | Definition of Ready item 8 Contract: Fail | P1 event type fixed in section 4 step 2 (CG-ALL-7034). P2 401 message ID is not in Error and Message Standard v4 (grep), so the placeholder stays. See CG-ALL-7033. |
| RWB-P7-E2001-APP | R-11231 | CG-ALL-7033 | 4, 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 has no message ID for 401 no session (checked earlier). 503 already maps to MSG-GEN-006. Placeholder kept; mapping needs business analyst input. |
| RWB-P7-E2001-APP | R-17997 | DOR-RWB-P7-E2001-APP-18 | Not in chunk | Definition of Ready item 18 Open decisions: Partial | DL06, DL10, DL16 assumptions already listed. DL17 and DL29 have no ASM ID in sources; ASM numbering belongs to step D1, so none added. Section text not in chunk. |
| RWB-P7-E2001-APP | R-22312 | GAP-0653 | 5, 13, 14 | rwb-integration EFS hand-over deployment: the values, the alert identifiers, the dashboard series and the runbook have no source | Sections 5, 13 and 14 text is not in this chunk, so no exact old text to edit. No source gives the environment values or message IDs; no change made. |
| RWB-P7-E2002-APP | R-06748 | DOR-RWB-P7-E2002-APP-14 | none | Definition of Ready item 14 Epic design: Fail | Recording sign-off needs a reference not in the sources. Searched 04 User stories for an epic design record; none found. Story unchanged. |
| RWB-P7-E2002-APP | R-26276 | CG-ALL-7048 | 3 | Flyway file V2002_1__plan_status_record.sql is not in the V0001..Vnnnn form | Next V-number for rwb-decision not in sources. Baseline is V0001; no other V-number found in P7 folder. Story migration name V2002_1 left unchanged. |
| RWB-P7-E2004-APP | R-06759 | DOR-RWB-P7-E2004-APP-22 | find it | Definition of Ready item 22 Fake published: Fail | No fake library version for RWB-P3-E2004-CON in sources. Stories say 'published with its fake' (P1 E2010 APP l.58; P3 E2004 OPS l.52) with no version. Version would be invented. |
| RWB-P7-E2004-APP | R-18009 | DOR-RWB-P7-E2004-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | Section 11 field list is not in the supplied story text, and no source gives a P2 personal-data class per field. Fields cannot be classed without inventing values. |
| RWB-P7-E2004-APP | R-22355 | GAP-0389 | find it | The harness repository, environments, seeding, business clock, evidence format and retention, pass/fail gate and the gateway-bff composite case-record route are not defined in the source documents | Harness repo, environments, seed, business clock, evidence, gate and gateway-bff route need agreement with QA and integration lead. Grep found no values in sources; none invented. |
| RWB-P7-E2005-APP | R-06762 | DOR-RWB-P7-E2005-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (grep of RWB-P7-E2005-CON review). Placeholder kept; the epic design record is needed. |
| RWB-P7-E2005-APP | R-06763 | DOR-RWB-P7-E2005-APP-16 Size: Fail | Header table | Definition of Ready item 16 Size: Fail | The sources give no size or squad sizing rule, so the row cannot state one. Placeholder kept until the squad records a size. |
| RWB-P7-E2005-APP | R-06765 | DOR-RWB-P7-E2005-APP-22 | header | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in the story or sources. Placeholder kept; needs the fake library publication record. |
| RWB-P7-E2005-APP | R-11242 | CG-ALL-7064 | 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 has no message ID for 401 no session. Mapping needs a new ID, which is not in the sources. Business analyst to supply it. |
| RWB-P7-E2005-APP | R-26286 | CG-ALL-7069 | 3.1 | Flyway file V2005_1__declog_approver_index.sql is not in the V0001..Vnnnn form | The next V-number of the rwb-decision Flyway sequence is not in the sources (DP-15 gives only V0001). Migration line L248 is outside this chunk. Solution architect to set it. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11906 | RWB-P7-E1052-APP | CG-ALL-6989 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log (API-P7-006) in the owner's yaml through the CON story, or remove it from 12.1. |
| CDC-11907 | RWB-P7-E1052-APP | CG-ALL-6990 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} (API-P7-007) in the owner's yaml through the CON story, or remove it from 12.1. |
| CDC-11912 | RWB-P7-E1052-APP | DOR-RWB-P7-E1052-APP-8 | 12.1 | Add paths GET /api/recovery/decision/v1/decision-log and GET /api/recovery/decision/v1/decision-log/{entryId}. Story Errors line now carries placeholders for the unmapped statuses. |
| CDC-11941 | RWB-P7-E1054-APP | CG-ALL-7011 |  | Remove the closed enum on status so LOV-CASE-STATUS values are accepted as data without a code change. |
| CDC-11945 | RWB-P7-E1054-APP | DOR-RWB-P7-E1054-APP-8 |  | The closed status enum is a rwb-decision.yaml change tracked under CG-ALL-7011; the story has no edit for it. |
| CDC-12051 | RWB-P7-E2004-APP | CG-ALL-7052 | 12.1 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId} with query packageVersion in the rwb-decision API yaml, through the CON story, or remove the path from section 12.1. |
| CDC-12056 | RWB-P7-E2004-APP | DOR-RWB-P7-E2004-APP-8 | 12.1 | Publish the GET /api/recovery/decision/v1/rule-catalog/{ruleId} operation with query packageVersion in the rwb-decision yaml, or remove it from section 12.1. |
| CDC-12087 | RWB-P7-E2005-APP | CG-ALL-7065 | 3 | Remove the closed enum on approvalLevel so LOV-APPROVAL-LEVEL values are accepted as data without a code change. |
| CDC-12089 | RWB-P7-E2005-APP | DOR-RWB-P7-E2005-APP-8 | Header table, 4, 12.1, 12.3 | Remove the closed approvalLevel enum so LOV-APPROVAL-LEVEL loads as data. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11926 | RWB-P7-E1052-APP | CG-ALL-6996 | 18 | Align REQ-OCC-001 test cases with section 18 of RWB-P7-E1052-APP in the next RTM version. |
| CDC-11958 | RWB-P7-E1054-APP | CG-ALL-7016 | 18 | Align the REQ-DCM-005 row with section 18 of RWB-P7-E1054-APP; the TC-E1-050, TC-E1-060 and TC-E2-025 entries belong to their own stories. |
| CDC-11984 | RWB-P7-E1073-APP | CG-ALL-7028 | 18 | Align the REQ-CWC-013 test list and the other three requirement traces with section 18 of RWB-P7-E1073-APP at the next version of the RTM. |
| CDC-12047 | RWB-P7-E2002-APP | CG-ALL-7046 | 18 | Align the test lists for REQ-DRI-013 and REQ-CHO-002 with section 18 of this story in the next RTM version. |
| CDC-12061 | RWB-P7-E2004-APP | DOR-RWB-P7-E2004-APP-12 | 12.7 | Reconcile its test lists with section 18 of this story; TC-E2-004-17 is added in section 16 and TC-15/16 are pending in Test Cases v8. |
| CDC-12066 | RWB-P7-E2004-APP | GAP-2503 |  | Declare the nine consumed operations on per-service bases with one hop and 2 s timeout; name workflow matchPayments and its four activities as design baseline; record in the RTM that AC1, AC3, AC4 and AC5 of the legacy key are carried by no story of this split. |
| CDC-12080 | RWB-P7-E2004-APP | CG-ALL-7059 | 18 | Align the test lists of the four requirements in the evidence with section 18 of this story in the next RTM version. |
| CDC-12097 | RWB-P7-E2005-APP | CG-ALL-7067 | 18 | Align the test lists of the four differing requirements with section 18 of this story in the next RTM version. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11947 | RWB-P7-E1054-APP | CG-ALL-7006 | 12.4 | Record ce_specversion as a CloudEvents binary-mode transport header outside LDM and Data Classification. |
| CDC-11948 | RWB-P7-E1054-APP | CG-ALL-7007 | 12.4 | Record ce_type as a CloudEvents binary-mode transport header outside LDM and Data Classification. |
| CDC-11949 | RWB-P7-E1054-APP | CG-ALL-7008 | 12.4 | Record ce_source as a CloudEvents binary-mode transport header outside LDM and Data Classification. |
| CDC-11950 | RWB-P7-E1054-APP | CG-ALL-7009 | 12.4 | Record ce_subject as a CloudEvents binary-mode transport header outside LDM and Data Classification. |
| CDC-11951 | RWB-P7-E1054-APP | CG-ALL-7010 | 12.4 | Record ce_time as a CloudEvents binary-mode transport header outside LDM and Data Classification. |
| CDC-11979 | RWB-P7-E1073-APP | GAP-2459 | 13 | Name rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1 keyed by package code, with package code, version label, in-force time and SHA-256; map to EV-08, EV-09 and EV-30. |
| CDC-12072 | RWB-P7-E2004-APP | GAP-0703 | find it | Add rwb-case as a consumer of rwb.treatment.TreatmentApproved.v1; confirm the S2 treatment and rwb-case route and timer split at the wave 2 architecture review. |

### RWB-P2-E2001-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11998 | RWB-P7-E2001-APP | DOR-RWB-P7-E2001-APP-22 | find it | Publish the contract fake library and record its version. |
| CDC-11999 | RWB-P7-E2001-APP | DOR-RWB-P7-E2001-APP-23 | find it | Fix and record the contract version this story builds against; the story row holds the gap until then. |
| CDC-12001 | RWB-P7-E2001-APP | DOR-RWB-P7-E2001-APP-11 | 8 | Reconcile the personal-data classification of its fields with BR12, which says no personal value is carried. |
| CDC-12004 | RWB-P7-E2001-APP | GAP-0590 | find it | Fix the key as EFS:<efs_record_key>; the ledger writer owns the repeat hit count; the run summary reports both counts. |
| CDC-12005 | RWB-P7-E2001-APP | GAP-0592 |  | Publish GET /entry-candidate-facts?businessDate= as a batched customer read: one row per candidate account key with personKey, productGroup and REC-05 resolution; correct per-candidate wording. |
| CDC-12013 | RWB-P7-E2001-APP | GAP-2463 |  | Confirm the repeat count as a rwb-decision meter on the operational dashboard, returned in the record-submission response header, and read by the rwb-integration run summary. |
| CDC-12021 | RWB-P7-E2001-APP | GAP-0589 | 7 | Record one account and one business date per history read in one call with a configured row cap and no page parameter; answer a held read with 409 and a problem body naming MSG-P1-001 and the load date in use. |

### 05 Technical architecture/Recovery Workbench Notification and Correspondence Design v3.docx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20488 | RWB-P7-E1052-APP | R-28610 |  | Version 3 is named in the title and Version row. Source version row (1, 28 October 2026) and change log row 1 with both readings are present in the md build source. |
| CDC-20489 | RWB-P7-E1052-APP | R-28610 |  | Version 3 is named in the title and Version row. Source version row (1, 28 October 2026) and change log row 1 with both readings are present in the md build source. |
| CDC-20490 | RWB-P7-E1052-APP | R-28610 |  | Version 3 is named in the title and Version row. Source version row (1, 28 October 2026) and change log row 1 with both readings are present in the md build source. |
| CDC-20491 | RWB-P7-E1052-APP | R-28610 |  | Version 3 is named in the title and Version row. Source version row (1, 28 October 2026) and change log row 1 with both readings are present in the md build source. |
| CDC-20492 | RWB-P7-E1052-APP | R-28610 |  | Version 3 is named in the title and Version row. Source version row (1, 28 October 2026) and change log row 1 with both readings are present in the md build source. |
| CDC-20493 | RWB-P7-E1052-APP | R-28610 |  | Version 3 is named in the title and Version row. Source version row (1, 28 October 2026) and change log row 1 with both readings are present in the md build source. |
| CDC-20494 | RWB-P7-E1052-APP | R-28610 |  | Version 3 is named in the title and Version row. Source version row (1, 28 October 2026) and change log row 1 with both readings are present in the md build source. |

### RWB-P6-E1052-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11909 | RWB-P7-E1052-APP | DOR-RWB-P7-E1052-APP-21 | header | Publish the contract story with its fakes; the story names it as its contract dependency. No RWB-P7-E1052-CON story exists in the sources. |
| CDC-11910 | RWB-P7-E1052-APP | DOR-RWB-P7-E1052-APP-22 | header | Publish the contract fake library and record its version as published. |
| CDC-11911 | RWB-P7-E1052-APP | DOR-RWB-P7-E1052-APP-23 | header | Fix the contract version this story builds against and record it in the header Contract version row. |
| CDC-11916 | RWB-P7-E1052-APP | GAP-0357 | find it | Publish base and route of the five template operations under /api/recovery/comms/v1/admin/templates, the SCR-33 composite route and the P1 freshness stamp source in the registry. This story consumes none of them (12.2). |
| CDC-11919 | RWB-P7-E1052-APP | GAP-0364 | find it | Name the notice path POST /cases/{caseId}/notices, the P1 data-product reads including the stale-batch signal, the P5 PDF store and the snapshot home in the P6 contract. This story reads no source table (BR14). |
| CDC-11924 | RWB-P7-E1052-APP | GAP-1086 | 14 | Publish one error row per condition: withdrawn-template hold answered with notice in state Held; repeat with a different key answered 409; missing field answered 422. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11927 | RWB-P7-E1052-APP | GAP-2094 | 12.1 | Add a case-level GET of notices to the P6 endpoints and settle its path in the P6 API specification. |
| CDC-11965 | RWB-P7-E1073-APP | GAP-1329 | 12.2 | Use one registry family: GET and POST /admin/rule-versions with /admin/rule-versions/{versionId}/approve and /rollback, per RWB-ITG-E1073-ITG section 12.2. Remove GET /rule-catalog from the consumed set and state that the catalogue travels with the model answer. |
| CDC-11973 | RWB-P7-E1073-APP | GAP-0700 | 12.1 | Add the seven operations to the P7 rows of the Ownership Map and the rwb-decision API file with rights, answers and error codes. Publish the model and catalog resource shapes with their named fields. |
| CDC-12057 | RWB-P7-E2004-APP | GAP-2474 | 12.1 | Add GET /rule-catalog/{ruleId}?packageVersion= as a P7 row before the wave 2 contract baseline is tagged, and state that the entry read is API-P7-007 of RWB-P7-E2005-APP. |
| CDC-12075 | RWB-P7-E2004-APP | GAP-1698 | find it | Add rows for the contracts, settlement and deed-in-lieu agreements and plan timers under rwb-treatment, stating entity groups and key fields without physical table names. |
| CDC-12090 | RWB-P7-E2005-APP | GAP-2474 | 12.1 | Add GET /rule-catalog/{ruleId}?packageVersion= as a P7 row before the wave 2 baseline tag; API-P7-007 is the entry read of this story. |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11923 | RWB-P7-E1052-APP | GAP-1082 | 3 | Publish NoticeRequest and Notice schemas with required flags and the NoticeGenerated payload, confirmed with the app stories of this key. |
| CDC-12009 | RWB-P7-E2001-APP | GAP-1333 |  | Add businessDate filter, full DecisionLogPage and DecisionLogEntry field set, page-size limit, and name one screen or panel for a decision entry beside the case. |
| CDC-12039 | RWB-P7-E2002-APP | GAP-2469 |  | Publish the registry version answer and decision-log item with field names, the artifact column and the checksum it covers, the page size of the read, the service login, and one message identifier for the two refusals, before the wave-2 contract baseline is tagged. |
| CDC-12071 | RWB-P7-E2004-APP | GAP-0918 | 12.1 | Add API-P4-022 GET /doa-limits with the request fields decisionCode, regulationItem, productGroup, principal, lossPct, lossAmount, onDate and the answer fields level, delegationLimitId, limitVersion, holderUserId, substituteUserId, outcome. |
| CDC-12091 | RWB-P7-E2005-APP | GAP-2434 | 12 | Add finalCall to the query parameters of API-P7-006 (Query: caseId, decision, ruleId, approver, from, to, page, size, finalCall). |

### RWB-P7-E2005-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12015 | RWB-P7-E2001-APP | GAP-2464 | 12 | Fix query parameters caseId, decision, ruleId, ruleVersion, approver, from, to, page and size, page size 1 to 500, ordered by decided_at, for GET /decision-log. |
| CDC-12088 | RWB-P7-E2005-APP | DOR-RWB-P7-E2005-APP-21 | Header table | Publish the contract and set its build status from Not started to Done. |
| CDC-12092 | RWB-P7-E2005-APP | GAP-0629 | 3 | Add the agent-version filter and the three override elements to GET /decision-log as an additive change; the drift step, segment, notice path, policy values, migration, limits, login, route and right are set in the agent dashboard v2 stories, not in this story. |
| CDC-12093 | RWB-P7-E2005-APP | GAP-2464 | 3 | Fix query parameters caseId, decision, ruleId, ruleVersion, approver, from, to, page and size; page size 1 to 500; order by decided_at. |
| CDC-12096 | RWB-P7-E2005-APP | GAP-1248 | 12 | Publish the eleven audit element names of AC2, the CSV column order and the page-size default, frozen at v1 by the architect; messageCodes on the page and chainVerified on each entry. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20796 | RWB-P7-E1052-APP | R-22162 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |
| CDC-20797 | RWB-P7-E1073-APP | R-22289 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |
| CDC-20798 | RWB-P7-E1052-APP | R-28613 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |
| CDC-20800 | RWB-P7-E1054-APP | R-28624 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |
| CDC-20802 | RWB-P7-E2001-APP | R-22316 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11908 | RWB-P7-E1052-APP | DOR-RWB-P7-E1052-APP-14 | header | Confirm and record the signed epic design sign-off; no signed epic design appears in the source documents. |
| CDC-11942 | RWB-P7-E1054-APP | DOR-RWB-P7-E1054-APP-14 |  | Record the signed epic design sign-off for RWB-P7-E1054-APP. |
| CDC-11996 | RWB-P7-E2001-APP | DOR-RWB-P7-E2001-APP-14 | find it | Record the signed epic design sign-off; no signed epic design is in the source documents. |
| CDC-12053 | RWB-P7-E2004-APP | DOR-RWB-P7-E2004-APP-14 | header | Record the signed epic design sign-off for RWB-P7-E2004-APP in the epic design record. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11914 | RWB-P7-E1052-APP | CG-ALL-6993 | 4, 14 | Add a new message ID for refusal of a missing or invalid field of this story; story then cites it in place of MSG-P7-009. |
| CDC-11966 | RWB-P7-E1073-APP | DOR-RWB-P7-E1073-APP-9 | 14 | Align the MSG-P3-027 wording to the v4 standard text, then update the section 14 row to match. |
| CDC-12058 | RWB-P7-E2004-APP | CG-ALL-7056 | 14 | Add a new message ID for a record refused for a missing or invalid field; the story then cites it in its MSG-P7-009 row. |
| CDC-12062 | RWB-P7-E2004-APP | DOR-RWB-P7-E2004-APP-9 | 14 | Add a new message ID for the missing or invalid field case so MSG-P7-009 in section 14 can cite it. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11915 | RWB-P7-E1052-APP | CG-ALL-6995 | 16 | Add row TC-E1-052-11 with Given, When and Then from AC1 and BR4 and the data in section 16. |
| CDC-11957 | RWB-P7-E1054-APP | CG-ALL-7014 Test cases cover other criteria in Test Cases v8 | 16 | TC-02 and TC-06 to TC-17 restored to their prior AC references |
| CDC-12027 | RWB-P7-E2002-APP | CG-ALL-7045 | 16 | Add rows for TC-E2-002-11 to Story test cases, with Given, When and Then copied from the criterion it covers (legacy Principle 5, BR5 AC4). |
| CDC-12059 | RWB-P7-E2004-APP | CG-ALL-7057 | 16 | Add rows TC-E2-004-15 and TC-E2-004-16 with Given, When and Then copied from the criteria they cover (AC1; AC5). |

### parameter-catalog.csv (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11935 | RWB-P7-E1052-APP | GAP-0753 | 12 | Add the case-side notice-request switch key with default on and owner RW-COE. The key is Not specified in the source documents (GAP-0753). |
| CDC-11955 | RWB-P7-E1054-APP | GAP-0755 | find it | Add REVIEW_TEAM_UNATTACHED as an rwb-case data row with the per-environment team agreed by RW-COE; production value not specified in the source documents (GAP-0755). |
| CDC-11961 | RWB-P7-E1054-APP | GAP-0756 | find it | Add the rwb-case review-queue switch as a parameter key stored in the platform flag library; its name is not specified in the source documents. |
| CDC-11991 | RWB-P7-E1073-APP | GAP-2460 | 7 | Add key rules.testcases.min with value 50, owned by rwb-case, and confirm the value with RW-COE at the first package load. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11946 | RWB-P7-E1054-APP | CG-ALL-7005 | 11 | No ce_id field or entity exists in LDM v9 or Data Classification v5. Section 11 states ce_id as a transport attribute. Owner role Data. |
| CDC-11981 | RWB-P7-E1073-APP | GAP-2457 | 11 | Supply column names, types and nullability for rule_package, rule_package_version, rule_row and rule_test_case on the legacy DF-REF field names; confirm artifact columns with RWB-PLT-E1072-CON. |
| CDC-11987 | RWB-P7-E1073-APP | GAP-0205 | find it | Keep rule_row as the entity name for 'Rule'; add rule_package and rule_package_version as entities owned by P7 in schema rwb_decision; rename no v6 row. |
| CDC-12028 | RWB-P7-E2002-APP | DOR-RWB-P7-E2002-APP-11 | find it | Reconcile the personal-data class of the P2 fields flagged by detcheck with this story, which carries no personal data. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11992 | RWB-P7-E1073-APP | GAP-2461 | 7 | Record the move of the five operations and the package list from access module recovery.accessadmin.rulepackages to rwb-decision (P7) per the Ownership Map. |
| CDC-12014 | RWB-P7-E2001-APP | GAP-2466 | 12 | Record that InteractionLedger.appendEfsHistory moves from recovery.decision.api to rwb-source-data under DP-18; the P7 entry keeps the history items as evidence. |
| CDC-12073 | RWB-P7-E2004-APP | GAP-1341 | find it | Record the legacy TimerScheduler, JOB-05 and TimerDue wording as superseded by Architecture v5 slides 42 and 44. |
| CDC-12084 | RWB-P7-E2004-APP | GAP-2476 | 7 | Record how INSTALLMENT_DUE and CURE_PERIOD timers running at cut-over are carried into the owning workflow; remove legacy steps 7 and 14 and AC2, AC12, AC14 timer assertions from the target tests. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11939 | RWB-P7-E1052-APP | GAP-1083 | find it | Record that the Litigation right and scope test of the notice operations are enforced at the edge under RWB-PLT-N001-CON; add DP-08 and RWB-P4-E1037-CON only if the check moves into the service |
| CDC-11940 | RWB-P7-E1052-APP | GAP-2455 | find it | Confirm rwb-decision appends every DecisionRecorded fact to decision_log_entry, local record is working record and ledger entry is record of record; RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON stay baseline outside the H row |
| CDC-11982 | RWB-P7-E1073-APP | GAP-0672 | 9 | Record the eight DP H rows as wave-0 platform prerequisites; publish the model fetch in RWB-P7-E1073-CON; name the rwb_integration login before its baseline is created. |

### RWB-P5-E1054-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11944 | RWB-P7-E1054-APP | DOR-RWB-P7-E1054-APP-22 |  | Publish a version of the P5 contract fake library and record it as published. |
| CDC-11953 | RWB-P7-E1054-APP | GAP-1011 | find it | Freeze seven operations, nine resources, five value sets, the IntakeResolution envelope, the If-Match lock, the document read reference and the event schema; keep the message texts as placeholders. |
| CDC-11954 | RWB-P7-E1054-APP | GAP-0365 | find it | Place the queue, resolve, field-review and document-review operations under /api/recovery/document/v1; read case status through P3 and scope through P4; keep legacy values unchanged. |

### RWB-P7-E1073-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11977 | RWB-P7-E1073-APP | GAP-1327 | 13 | Publish registry resource physical columns, the model answer, dry-run count shape, workbook container and object name, version-list panel id, service login and the two parameter codes. |
| CDC-12078 | RWB-P7-E2004-APP | GAP-1339 | find it | Fix the model and catalogue answer shape and envelope field names; add MSG-P7-009 and MSG-P7-012 to the P7 message table; name the SCR-38 and SCR-03 panels in RWB-P7-E2005-APP; state platform dependency holding in the build order. |
| CDC-12094 | RWB-P7-E2005-APP | GAP-1339 | 15 | Fix the model and catalogue answer in OpenAPI; fix envelope field names in RWB-PLT-E1027-CON; add MSG-P7-009 and MSG-P7-012 wording from the Error and Message Standard to the P7 message table; state in build order that section 13 DP dependencies are held by platform stories. |

### RWB-P6-E1073-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11993 | RWB-P7-E1073-APP | GAP-1215 |  | Reconcile the DP-04 row (H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON) with the RWB-P6-E1073-APP plan line (H none; C RWB-P3-E1073-CON) at the next rules-of-record pass. |
| CDC-11994 | RWB-P7-E1073-APP | GAP-1218 |  | State that platform CONs of the DP table are wave-0 prerequisites carried outside H for wave-1 APP stories, or add the eight platform CONs to H; keep Ready to start Day 1. |
| CDC-12064 | RWB-P7-E2004-APP | GAP-2395 |  | Prove AC1 and AC5 against the three Epic 2 package codes and version labels as fixture set; package assignment of rwb-comms is settled with the rule registry owner before integration. No fourth package code invented. |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12016 | RWB-P7-E2001-APP | GAP-1332 | 12 | Fix the DecisionRecorded payload and inputs snapshot with business date, queue and owner identifiers, hand-over reference, actions and composite idempotency key; confirm with hand-over contract owner before wave 2 build. |
| CDC-12042 | RWB-P7-E2002-APP | GAP-1336 | 3 | Fix the model answer, inputs snapshot and announcement payload shape and element names, and name the plan-status section route owner in the registry and record contracts. |
| CDC-12043 | RWB-P7-E2002-APP | GAP-1338 | 1 | Settle in the ledger contract whether a route move running two rules is one entry with the second rule in its actions or two entries; the story keeps one entry per case, business date and rule identity. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12023 | RWB-P7-E2001-APP | GAP-2468 | 7 | Carry the six platform CON rows and RWB-P7-E2005-CON in the dependency map; keep the lane at Day 1. |
| CDC-12024 | RWB-P7-E2001-APP | GAP-1335 | 7 | Show the six platform contracts and the two rwb-case contracts in the wave 2 dependency map; keep the metadata rows as they are. |
| CDC-12050 | RWB-P7-E2002-APP | GAP-1337 | header | Carry the platform contracts (DP-03, DP-04, DP-06, DP-07, DP-09, DP-10, DP-15, DP-19) and the rwb-case rule-package, parameters and reference-data contracts in the dependency map; metadata rows unchanged. |

### RWB-PLT-N001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12044 | RWB-P7-E2002-APP | GAP-0386 | 3 | Publish the gateway-bff composite case-record route path and merge order; harness repository, environments, seeding, evidence format and gate are agreed by the integration lead with QA. |
| CDC-12045 | RWB-P7-E2002-APP | GAP-0773 | 15 | Publish the composite route for SCR-03 with its path, two parallel calls, merge rule, masking rule and the 2 s budget split. |
| CDC-12095 | RWB-P7-E2005-APP | GAP-0387 | 15 | Publish the composite query route path and merge order in the gateway-bff contract before section 15 assertions run; integration lead agrees harness repository, SIT and UAT environments, seeding order, evidence format, retention and gate with QA. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12052 | RWB-P7-E2004-APP | CG-ALL-7053 | 13 | Create story file RWB-P7-E1073-CON (the rule-package contract named as C in the section 13 DP-04 row), or name the existing story that carries it. |
| CDC-12054 | RWB-P7-E2004-APP | DOR-RWB-P7-E2004-APP-17 | 13 | Create story file RWB-P7-E1073-CON or name the existing rule-package contract story in the section 13 DP-04 row. |
| CDC-12055 | RWB-P7-E2004-APP | DOR-RWB-P7-E2004-APP-21 | 13 | Create contract story RWB-P7-E2004-CON for the section 12.1 operations and name it as a contract dependency. |

### OTHER:TSD P3 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11920 | RWB-P7-E1052-APP | GAP-0749 | find it | Add seven notice columns with unique and timeline indexes to recovery_case in rwb_case, load timeline event codes into LOV-LEDGER-EVENT and assign field IDs in the next dictionary version. This story writes no case row (13). |
| CDC-11933 | RWB-P7-E1052-APP | GAP-0751 | 12 | Load both task codes, element type HUMAN_TASK, discretion REQUIRED and the status values as case task rows through the reference-data contract. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11934 | RWB-P7-E1052-APP | GAP-0752 | 12.1 | Fill the P3 consumer cell for P6 in the connection matrix (slide 13) and record the REST request as a permitted exception in the slide 17 note. |
| CDC-11975 | RWB-P7-E1073-APP | GAP-1216 | 13 | Publish the package-to-service map: one row per phase-1 package with owning service, version labels and target queues, including rwb-comms's assigned package. |

### RWB-P3-E1073-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11970 | RWB-P7-E1073-APP | GAP-1330 | 12.1 | State whether RWB-P3-E1073-CON publishes the case reads its consumers need, or move this story's contract dependency to RWB-P3-E1023-CON. |
| CDC-11978 | RWB-P7-E1073-APP | GAP-2458 | 13 | Add a paged open-case fact read filtered by status; the dry run uses it with the 2 s one-hop timeout. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12022 | RWB-P7-E2001-APP | GAP-1334 | 7 | Publish the per-service login of rwb_decision; fix the names of the 02:00 chain-check workflow, its activities and the JOB-14 Schedule identifier before wave 2 build. |
| CDC-12068 | RWB-P7-E2004-APP | GAP-3177 | header | Register the five-minute next-action Temporal Schedule in rwb-case and delete EV-18 (TimerDue) from the Epic 2 contract tables. |

### RWB-P2-E2002-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12026 | RWB-P7-E2002-APP | DOR-RWB-P7-E2002-APP-22 | header | Record a published fake library version for RWB-P2-E2002-CON. |
| CDC-12035 | RWB-P7-E2002-APP | GAP-0769 |  | Confirm with the P2 contract owner whether a batch operation for plan status is published. Until then keep the per-case read on rwb-integration, called inside the readPlanStatus activity with parameters rwb.ace.plan.batch-size = 500 and rwb.ace.plan.timeout-ms = 2000. |

### OTHER:TSD P7 v2 (owning document of the decision_log_entry baseline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11913 | RWB-P7-E1052-APP | CG-ALL-6988 | 3 | Record trigger tr_declog_append_only as a database object of decision_log_entry in T3.1, not as an LDM or Data Classification field. |

### RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11917 | RWB-P7-E1052-APP | GAP-1085 | find it | Publish the rwb-case task-raise operation or the event that creates a task, and record it in the Ownership Map v1 api list. This story raises no task (BR13). |

### OTHER:TSD P6 v2 T3.1 and RWB-E1-052 section 11 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11918 | RWB-P7-E1052-APP | GAP-1084 | find it | Give the party reference its own field ID and keep person_key as the notice business key, then correct the module specification or the legacy field list. Data steward to settle. |

### RWB-P5-E1052-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11921 | RWB-P7-E1052-APP | GAP-1079 | find it | Publish the generated-document operation with request, answer fields, failure shape and 2 s behaviour, and record it in the service contract catalog. This story calls no document operation (12.2, BR13), so no C row is added. |

### RWB-P6-E1052-CON; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11922 | RWB-P7-E1052-APP | GAP-1081 | find it | Name the merge snapshot store in the rwb_comms physical schema and publish it in the next physical-schema version. This story holds only the reference. |

### RWB-P6-E1052-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11925 | RWB-P7-E1052-APP | GAP-2454 | 3 | Fix generation record payload: template code and version and merge snapshot reference in inputs_ref with ACE data date on the entry; notice reference and type in actions; hold reason or refusal and freshness message in outcome; final-call set GENERATED, HELD, REFUSED. |

### RWB-P1-E1015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11928 | RWB-P7-E1052-APP | GAP-1080 | 12 | Publish the DP01 and DP07 record shape, naming each returned field and its source column, and the exact record and page shape. |

### OTHER:Story map (delivery plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11929 | RWB-P7-E1052-APP | GAP-2351 | 12.6 | Record RWB-P5-E1017-APP as the sole owner of JOB-17. Correct RWB-P5-E1055-APP and RWB-P5-E1065-APP section 12.6 at next version. |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11930 | RWB-P7-E1052-APP | GAP-2348 | 12.2 | Name the request and reason fields of GenerateRequest and RegenerateRequest and the DocumentPage and Document answer shape. |

### OTHER:Delivery plan (Work Package rows of this slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11931 | RWB-P7-E1052-APP | GAP-2350 | header | Add H or C rows for the DP-03, DP-07, DP-09, DP-15 and DP-19 platform contracts and RWB-P5-E2026-CON, or record them as implicit baseline. |

### OTHER:Recovery Workbench Notification and Correspondence Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11932 | RWB-P7-E1052-APP | GAP-2087 | header | Take the file name as the family version so the document becomes version 3. Add a Source version row: 1, 28 October 2026. The change log carries both readings. |

### OTHER:TSD P6 v2 (T3.2, list of values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11936 | RWB-P7-E1052-APP | GAP-1087 | find it | Add LOV-HOLD-REASON carrying POSTAL_ADDRESS and TEMPLATE_WITHDRAWN and any later value, read through the reference-data contract |

### OTHER:rwb-comms AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11937 | RWB-P7-E1052-APP | GAP-1088 | find it | Publish NoticeGenerated schema naming noticeId, caseId, templateId, templateVersion, noticeType and generatedAt; confirm with rwb-decision and rwb-reporting |

### OTHER:Work Package split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11938 | RWB-P7-E1052-APP | GAP-2349 | find it | Record one owning story per legacy criterion and mark secondary slices as test-case-bearing but criterion-free |

### RWB-P7-E1054-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11943 | RWB-P7-E1054-APP | DOR-RWB-P7-E1054-APP-21 Contract published: Fail | header | Contract dependencies kept at RWB-P5-E1054-CON; /v1 path row added |

### RWB-P5-E1054-CON; RWB-P3-E1035-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11952 | RWB-P7-E1054-APP | GAP-1010 | find it | Read the four review parameters from document_hub_parameter, publish the by-number case read on RWB-P3-E1035-CON, take role, team and scope from the cached permission decision. No edit here. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11956 | RWB-P7-E1054-APP | GAP-2456 | find it | Confirm review decision codes and final-call values, and allocate the rwb_decision login in the platform secret store. Story keys for actions and outcome set in section 11. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11959 | RWB-P7-E1054-APP | GAP-0746 | find it | Hold the review task code, element type and task status values as reference data in the rwb-case reference tables and load them before the review queue story starts. |

### OTHER:TSD P4 v3 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11960 | RWB-P7-E1054-APP | GAP-0988 | find it | Publish the review-item authorise request and answer schema naming the review team attribute; record matrix and masking version labels with valid-from dates and environment; list review-field IDs with the pack version. |

### OTHER:Recovery Workbench data dictionary (TSD P3 v3 field list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11962 | RWB-P7-E1054-APP | GAP-0757 | find it | Allocate field IDs for task columns document_ref, review_reason, item_version and review_state at the next data dictionary version; load the review task code, review states and decision code as reference rows. |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11963 | RWB-P7-E1054-APP | GAP-1593 | find it | Give A2.11 one distinct criterion for feeding the correction back to the labelled set; the PRD reads A2.10 and A2.11 as one behaviour delivered by CAP-P5-010. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11964 | RWB-P7-E1054-APP | GAP-0758 | find it | Agree the rwb-case per-service login name with the platform DB story and use it for grants, Flyway history and the connection pool; the name is not specified in the source documents. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11967 | RWB-P7-E1073-APP | GAP-2414 | header | Record Depends on (build) as None plus the eight platform contracts, and the contract list as the P3 and P7 contracts the DP table names, in that story's record. |

### OTHER:Technical Specification P7; OTHER:Technical Specification P3; OTHER:Technical Specification P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11968 | RWB-P7-E1073-APP | GAP-1615 | 3 | Re-issue TSD P7 with entries for the four rule tables and the rule operations. Remove those tables and operations from TSD P3 and TSD P4. Set x-module P7 on the nine rule paths. |

### OTHER:Technical Specification P3 v3; OTHER:Technical Specification P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11969 | RWB-P7-E1073-APP | GAP-1993 | 3 | Relabel rule_package, rule_package_version, rule_row and rule_test_case as owned by P7 rwb-decision in TSD P3 v3 and TSD P4 v3. Read the package and catalogue through the P7 contract (DP-04). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11971 | RWB-P7-E1073-APP | GAP-0383 | 14 | Assign one package code and version label each to rwb-comms and rwb-integration. Add GET /rule-models/{packageCode}/{versionLabel} under P7 with the checksum. Publish the refused load keeping MSG-P3-027 and its check values. |

### OTHER:Technical Specification P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11972 | RWB-P7-E1073-APP | GAP-0699 | 13 | Correct the TSD P3 v3 T3.1 ownership labels for rule_package, rule_package_version, rule_row and rule_test_case to P7 rwb-decision. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11974 | RWB-P7-E1073-APP | GAP-0701 |  | GAP-0701: size the rwb-case pod by a load test that holds the KieBase cache bound of 20 package versions under evaluation load. Record the heap request, heap limit and cache bound per environment as reviewed values, keep the evaluated copy in memory only, and have the platform owner confirm before wave 1 release. Owner: SCB IT infrastructure with the rwb-case owner team. |

### OTHER:rwb-decision API document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11976 | RWB-P7-E1073-APP | GAP-1217 | 13 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}: DRL, SHA-256, state, valid-from date, 404 for unknown label, 409 for unloadable version, 2 s budget. |

### OTHER:rwb-decision and rwb-comms contract review (wave-1 design and DB stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11980 | RWB-P7-E1073-APP | GAP-1214 | 13 | Fix the local copy table and columns, the two parameter rows and read path, the two {check} values with message text, the scenario-set transfer shape and the 300 ms measurement point. |

### OTHER:Template and Rules v1 (R5.5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11983 | RWB-P7-E1073-APP | GAP-1328 | 9 | State that the platform H rows and the self-referential C rows are held by the platform and contract stories and not repeated on the APP line. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11985 | RWB-P7-E1073-APP | GAP-1620 | find it | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime; a version names its format; conversion is a version change with its own test evidence; both formats stay in load checks and model fetch. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11986 | RWB-P7-E1073-APP | GAP-0118 | find it | Record amended T1: workflow runs on the task queue of the owning service. Record amended T2: each scheduled job becomes a Temporal Schedule or event-started workflow in the owning service, with JOB-05 behind the TimerScheduler port until Epic 3. |

### RWB-P3-E1073-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11988 | RWB-P7-E1073-APP | GAP-0702 | find it | Record readiness gate, probe timings, ports, certificate subject and image-scan window as reviewed per-environment values confirmed at SIT; keep them out of code and chart constants. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11989 | RWB-P7-E1073-APP | GAP-1219 | find it | Name rwb-comms as a consumer of RulePackageInForce, or publish the package-to-service map that completes the row; until then consume the event in rwb-comms per slide 20. |

### OTHER:Temporal and Drools design, slide 15 (version states) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11990 | RWB-P7-E1073-APP | GAP-1331 | find it | State that REFUSED is a state of a stored version that failed its promotion checks, and that a load refused at a check writes no version row and is proved by its decision log entry. |

### RWB-P7-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11995 | RWB-P7-E1073-APP | GAP-2410 |  | Record that a secondary slice builds against platform contracts and published fakes and reads same-service wave-1 rows through its own schema, within R5.7 rule 5. |

### RWB-P7-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11997 | RWB-P7-E2001-APP | DOR-RWB-P7-E2001-APP-21 Contract published: Fail | find it | RWB-P7-E2001-CON is not a story of this set and is not in the story header; the contract story is outside this story. |

### OTHER:Functional Specification Document P3; OTHER:A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12000 | RWB-P7-E2001-APP | GAP-1549 | find it | Restate the A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12002 | RWB-P7-E2001-APP | GAP-3175 | find it | List LoadCompleted (EV-26) as the legacy alias of AceDataReady (EV-26), with rwb-source-data as producer. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12003 | RWB-P7-E2001-APP | GAP-3176 | find it | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### OTHER:EFS hand-over harness pack (outside this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12006 | RWB-P7-E2001-APP | GAP-0388 |  | Hold the harness repository, SIT and UAT environments, ACE seeding for 2026-12-14 to 2026-12-17 and accounts A-0001 to A-0004, per-run evidence format and retention, pass/fail gate, and gateway-bff composite route paths and merge order. Owner: Integration lead; QA at wave 2 entry check. |

### OTHER:TSD P2 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12007 | RWB-P7-E2001-APP | GAP-0651 |  | Mark T5.2 and the P2 inbound exclusion as superseded by DP-05 and ADR-010; agree consumed operation paths at the P2 CON contract review. |

### OTHER:contract/handover-run-activities.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12008 | RWB-P7-E2001-APP | GAP-0652 |  | Fix the workflow, nine activities, twelve summary elements and retry policy. Fix six P1 elements and one P3 element in the two consumed contracts. Carry placeholders for unsourced paths and fields. Publish six fakes from owners' OpenAPI and fail the build on drift. Owner: Tech lead. |

### OTHER:rwb-case P3 REST operations (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12010 | RWB-P7-E2001-APP | GAP-2258 |  | Add admin rerun for the entry run on the rwb-case base, answering 409 MSG-P2-006 while the workflow for the business date runs. |

### RWB-P2-E2001-CON; OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12011 | RWB-P7-E2001-APP | GAP-2259 |  | Publish candidate page, EFS history page, ledger append, REC-05 break and REC-01 result operation paths, shapes and error envelopes. |

### OTHER:TSD P3 v3 T3.1; OTHER:P3 interaction ledger story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12012 | RWB-P7-E2001-APP | GAP-2260 |  | Mark the interaction object as owned by rwb-source-data under DP-18 and re-scope the P3 ledger story to the P1 contract. |

### RWB-PLT-E1047-CON; RWB-PLT-TE006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12017 | RWB-P7-E2001-APP | GAP-2262 | 12 | Fix the envelope and retry and dead-letter settings of rwb.case.events.v1; limit CaseCreated payload to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate and dpdAtEntry. |

### OTHER:Work Package B2-P3-020 lane L-P7-Q and Day-1 allocation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12018 | RWB-P7-E2001-APP | GAP-2261 | header | Assembler adds platform H dependencies RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON to the lane and Day-1 allocation; metadata row stays as delivered. |

### OTHER:Screen Specifications v1 (SCR-04) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12019 | RWB-P7-E2001-APP | CG-ALL-7038 | 15 | Add empty, loading, error and no-access states of SCR-04 with user actions; where a state is absent write Not specified in the source documents. |

### RWB-P7-E1027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12020 | RWB-P7-E2001-APP | GAP-2465 | 7 | Register the five-minute ingest lag as an RWB-PLT-OBS metric with its threshold as a parameter; route the gap alert to RW-PLATADM under RWB-P7-E1027-APP. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12025 | RWB-P7-E2002-APP | DOR-RWB-P7-E2002-APP-21 | header | Create contract story RWB-P7-E2002-CON, or name the existing contract story for this service, so the CON dependency resolves. |

### OTHER:Rule registry owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12029 | RWB-P7-E2002-APP | GAP-2395 | find it | Story reads only RESTRUCTURE and names no rwb-comms package or code; assignment is outside this story. |

### OTHER:TSD P4 (T6.1 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12030 | RWB-P7-E2002-APP | GAP-0907 | find it | Add a Case record column with letters for all roles, publish the 14-area matrix with RWB-P4-AD002-APP, and confirm CASE_RECORD letters and default scopes with the matrix owner. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12031 | RWB-P7-E2002-APP | GAP-0908 | find it | Add POST /authorise and GET /me/permissions with request and answer schemas, stub them in the contract fake, and record whether the plan reference travels in the authorise request. |

### RWB-P2-E2002-CON; RWB-P2-E2002-OPS; RWB-P3-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12032 | RWB-P7-E2002-APP | GAP-0654 |  | Settle in the wave 2 contract review: the rwb-integration login with the ACE DB owner; the case read and its contract story; the field sets of the case read, reference answers, authorise answer and remaining interface elements; the owner of live and messageCode with the composite route merge rule; the owner and read path of the two settings; the P2-to-ACE-Common and P3-to-P2 connection-matrix rows; and one daily step in rwb-case. Record the outcome in each named document. |

### RWB-P2-E2002-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12033 | RWB-P7-E2002-APP | GAP-0655 |  | Approve the four assumptions (answer shape with accountNo, live and messageCode rule, interface batch, budget and answer rules, consumed read shapes with the composite route) before tagging the baseline. Reconcile the interface-versus-view wording of the technical specification and record the re-basing on the integration base. |

### RWB-P2-E2002-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12034 | RWB-P7-E2002-APP | GAP-0656 |  | Approve the three assumptions in the release readiness review: identity and environment values with no Schedule and no migration; trigger wiring with the ACE-or-stub record and corrected harness row; five series, four alerts, the named no-package row and four runbook entries. Carry every threshold and endpoint as an environment value, never as code. |

### OTHER:rwb-decision P7 contract story (/api/recovery/decision/v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12036 | RWB-P7-E2002-APP | GAP-0770 |  | Publish the catalog-row read by rule ID and package version, returning action_text, owner_role, timer_spec, target queue code and outputs. Until then the story reads the row through the contract fake and the KieBase answer. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:TSD P3 v3 T3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12037 | RWB-P7-E2002-APP | GAP-0771 |  | Add a table code for the plan event map to LOV-REF-TABLE and load its rows as reference_row under a reference_version, one row per ACE status and route state pair; no map row in code. |

### OTHER:Platform database story (19-schema list) and Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12038 | RWB-P7-E2002-APP | GAP-0774 |  | Allocate the rwb-case database login with its schema in the 19-schema list, derive the name from the schema, hold it in Key Vault and record it in the Service Catalog before first deployment. |

### OTHER:rwb-decision decision-record contract (TSD P7 T3.1 and FSD P7 A2.2 and A2.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12040 | RWB-P7-E2002-APP | GAP-2471 |  | State that one entry is written per case, business date and rule identity, and that a transaction running two rules writes one entry per rule. Publish the content model of the inputs snapshot and actions payload, with plan reference, plan status and its date inside them. |

### OTHER:Legacy story in Module P2 Integration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12041 | RWB-P7-E2002-APP | GAP-2472 | Change log | The endpoint text sits in the legacy P2 story; this story's change log only records the plan move. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12046 | RWB-P7-E2002-APP | GAP-2470 | 13 | Complete the metadata rows from the DP table, or state in R5.5 that platform H and self-referential C rows are held by platform and contract stories and not repeated on the APP line. |

### OTHER:P1 contract story for rwb-source-data (reconciliation_result) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12048 | RWB-P7-E2002-APP | GAP-0772 | 9 | Publish a break operation on the rwb-source-data contract (product, check, key, detail, owner role) and have the plan-status step call it once per rejected or missing plan. |

### OTHER:Platform DB story (rwb-access login) and gateway-bff composite route for SCR-03 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12049 | RWB-P7-E2002-APP | GAP-0909 | 9 | Fix the rwb-access per-service login (DP-02) and publish the SCR-03 composite route with its field list, hop list, merge order and masking rule (DP-19). |

### OTHER:P3 story owning SCR-38 and SCR-39 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12060 | RWB-P7-E2004-APP | DOR-RWB-P7-E2004-APP-10 | find it | Add empty, loading, error and no access states for SCR-38 and SCR-39. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12063 | RWB-P7-E2004-APP | GAP-2404 |  | Set H to None plus RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON; set C to RWB-P10-E2032-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and the published P4 authorise contract. Platform contracts are delivery prerequisites, not per-story blockers. |

### OTHER:Functional Specification FSD S2 (feature dependency codes) and the service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12065 | RWB-P7-E2004-APP | GAP-1713 |  | Map each prerequisite feature code (approval to P7, case to P3, documents to P5, communications to P6, valuation to S1) to its owning service contract once in the service contract; carry the duplicate FEAT-CHO-08 as written. |

### RWB-P8-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12067 | RWB-P7-E2004-APP | GAP-1346 |  | Keep plan H, C, I and X rows as given; name the seven consumed rows in section 12.2 with placeholder until each owner publishes its operation; solution architect to confirm scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON. |

### OTHER:rwb-case OpenAPI file (GET /cases/{caseId}/timers response) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12069 | RWB-P7-E2004-APP | GAP-0705 | 12.1 | Define timer response properties treatmentId, timerType, startedAt, expiresAt (offset date-time), warnAt, paused and status, all optional within major version 1. |

### RWB-P4-E1037-CON; RWB-P4-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12070 | RWB-P7-E2004-APP | GAP-0917 | 12.2 | Freeze the POST /authorise request and answer fields at contract review; load the two capability areas into RWB-P4-AD002-APP; name the rwb-access login with the DP-02 platform DB story. |

### OTHER:rwb-decision contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12074 | RWB-P7-E2004-APP | GAP-2473 | find it | Publish the catalogue answer element names and media type, the decision record fields, the MSG-P7-009 text and fields, the system actor value and the four registry table columns. |

### OTHER:PRD release slicing (rwb-treatment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12076 | RWB-P7-E2004-APP | GAP-1709 | find it | State the split of rwb-treatment capabilities: contract and treatment record in wave 2, offer, settlement, plan and deed in lieu with E3. |

### OTHER:FSD S2 (field catalogue) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12077 | RWB-P7-E2004-APP | GAP-1712 | find it | Require the eight catalogue fields as written and add catalogue entries for contract, agreement, plan timer and booking reference, with the physical field list left to the data architect. |

### OTHER:Template and Rules R5.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12079 | RWB-P7-E2004-APP | GAP-2475 | find it | State that platform H rows and self-referential C rows are held by the platform and contract stories and are not repeated on a secondary APP line. |

### OTHER:rwb-case values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12081 | RWB-P7-E2004-APP | GAP-0706 | none | Set provisional default alert values for plan-timer projection lag, subscription lag, .dlt count, exception-queue count and DP04 freshness; confirm at UAT and record in runbook. |

### OTHER:gateway-bff route catalogue (DP-19) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12082 | RWB-P7-E2004-APP | GAP-0920 | 15 | Publish the SCR-14 and SCR-03 composite routes with their field lists and confirm that no field on either is a personal field. |

### OTHER:Platform DB story of DP-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12083 | RWB-P7-E2004-APP | GAP-0921 | none | Fix the login name of rwb-access, its grants and its schema owner; P4 stories reference it rather than repeating it. |

### OTHER:Service contract document of rwb-treatment (major version 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12085 | RWB-P7-E2004-APP | GAP-2688 | none | Name the two consumed operations, the member-level payload types and the fake set; state the one-running-plan guard as a partial unique index on the treatment row. |

### OTHER:Build-order assembly and WP metadata rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12086 | RWB-P7-E2004-APP | GAP-1340 | none | No story edit; metadata rows stay as the WP fixes them. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20856 | RWB-P7-E2001-APP | R-09171 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09171', 'R-22565', 'R-28487'] |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20903 | RWB-P7-E2001-APP | R-22310 |  | Item text not re-read in this run, so no fix was written. Not verified against this document. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0118 | The amendment of D-RCV-36 T1 and T2 has no wording in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0205 | The entity called Rule is rule_row, and the model holds neither rule_package nor rule_package_version | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0364 | Cross-service notice path, merge snapshot home and stale-batch signal are not named for the target | Tech lead | Resolved (directive) |
| GAP-0365 | Review queue operation names, scope source and attach evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0383 | The rule package of rwb-comms and of rwb-integration, the rule-model fetch path and its owner, and the message family of the refusal are not stated in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0386 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0387 | Harness repository, environments, seeding, evidence, gate and gateway route for the decision-log audit query harness | Integration lead | Resolved (directive) |
| GAP-0388 | EFS hand-over harness: repository, environments, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0389 | The harness repository, environments, seeding, business clock, evidence format and retention, pass/fail gate and the gateway-bff composite case-record route are not defined in the source documents | Integration lead | Resolved (directive) |
| GAP-0589 | The history read is one operation or a paged read, and the HTTP answer of a held read, are stated by no source | Solution architect, P1 | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0592 | No source splits the hand-over facts between the candidate rule and the borrower and product-group facts, and the run's contract names a per-candidate customer read | Solution architect, P1 and P2 | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0651 | rwb-integration EFS hand-over: the mount of the step, the split across four owners, the consumed contract paths, the run summary store and the level of the decision record are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0652 | rwb-integration EFS hand-over contract: the activity contract, the consumed element shapes, the provided surface and the fakes have no source text | Tech lead | Resolved (directive) |
| GAP-0653 | rwb-integration EFS hand-over deployment: the values, the alert identifiers, the dashboard series and the runbook have no source | DevOps lead | Resolved (directive) |
| GAP-0654 | rwb-integration ACE plan status: the login, the account resolution, the interface field types, the meaning of live and messageCode, the two settings, the connection-matrix rows and the ownership split are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0655 | The plan-status contract baseline: the accountNo field, the meaning and owner of live and messageCode, the interface null rules, the consumed read shapes, the composite route and the two specification conflicts are not fixed by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0656 | The plan-status deployment values, the ACE endpoint and certificate references, the two setting values at run time, the trigger wiring, the alert thresholds, the mapping of the no-package condition and the fixture owner are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0699 | The rule package registry and the workbook object are declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0700 | The five authoring operations and the two rule reads have no Ownership Map row and no field-level shape | P7 rwb-decision owner with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0701 | The KieBase cache sizing, the JVM heap and the storage of a local model artefact are not specified | SCB IT infrastructure with the rwb-case owner team | Resolved (directive) |
| GAP-0702 | No source gives the readiness gate, the probe timings, the ports, the certificate subject or the image-scan window | SCB IT infrastructure with the platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0703 | The treatment entity moves to S2 while the legacy story holds it in P3, and the case side consumes TreatmentApproved which the event catalogue does not list for rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0705 | No source fixes the plan-timer fields, types or required flags of the timers answer behind GET /cases/{caseId}/timers | Tech lead of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0706 | No source gives the alert values for the plan-timer projection, the subscription lag, the DP04 freshness or the exception-queue count | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-0769 | The hand-over of the plan status between rwb-integration and rwb-case, and its batching, are not specified | Solution architect | Resolved (directive) |
| GAP-0770 | No published operation reads a rule catalog row by rule ID and package version | P7 decision owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0771 | The plan event map has no table code in LOV-REF-TABLE and no target table or column | Reference data owner (RW-COE) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0772 | The delivery path of a plan-status break to the data-quality console is not specified | P1 source data owner | Resolved (directive) |
| GAP-0773 | The gateway-bff composite route of the case record plan section is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0774 | The per-service database login name of rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0907 | rwb-access plan status: the TSD RBAC matrix has no Case record column, so the CASE_RECORD letters this slice decides are not tabulated for any role | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0908 | rwb-access plan status: the authorise request and answer shapes and the resolved permission view are absent from the TSD P4 appendix, including whether the plan reference travels in the authorise request | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0909 | rwb-access plan status: the per-service login name and the gateway-bff composite route field list behind SCR-03 and the plan status panel are not specified | Solution architect | Resolved (directive) |
| GAP-0917 | rwb-access treatment and plan-timer slice: the authorise request and answer, the Treatment and offer and Case record letters and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0918 | The delegation lookup GET /doa-limits and its request and answer fields exist only on Architecture v5 slide 14, not in the TSD P4 appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0920 | The composite route field list for SCR-14 Treatment record and the SCR-03 timer panel is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0921 | The per-service login of rwb-access is named by DP-02 and by no document | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0988 | The review-item authorise request shape, the label of the matrix and masking versions in force at the release date, and the review-field roster of the masking pack are fixed by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1011 | No source fixes the field-level names of the nine review resources, the one resolve answer, the field-patch idempotency, the document read position or the three platform message texts | Tech lead of rwb-document with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1214 | RWB-P6-E1073-APP: the local copy table and its columns, the parameter read path, the two added check names and the local run record are not specified in the source documents | Solution architect | Resolved (directive) |
| GAP-1215 | RWB-P6-E1073-APP: the DP-04 row of the pattern table names H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON while the plan gives no H and C RWB-P3-E1073-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1216 | RWB-P6-E1073-APP: no source names the rule package rwb-comms is assigned, its version labels or its target queues | Solution architect | Resolved (directive) |
| GAP-1217 | RWB-P6-E1073-APP: the model fetch operation, its path segments, its request fields and its response fields are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1219 | RWB-P6-E1073-APP: Arch v5 slide 43 lists four consumers of RulePackageInForce while slide 20 says every service refreshes its cache on it, and the ITG story makes rwb-comms an evaluator | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1242 | Audit export: a synchronous full-result CSV against a 2 s one-hop budget | Solution architect, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1246 | Approver index migration sits on a table created by another story | ACE team, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1247 | First-page performance target over 10,000 entries is assumed and not fixed | Solution architect, with the QA lead | Resolved (directive) |
| GAP-1248 | Element list of the audit answer beyond the legacy names, and the element that carries the warning | Solution architect, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1249 | Message identifier of the 401 answer is not given by any source | Solution architect, with the platform library owner | Resolved (directive) |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1327 | RWB-P7-E1073-APP: the model answer, the dry-run report, the refusal of the model read, the workbook object, the version-list panel, the service login, the parameter codes and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1329 | RWB-P7-E1073-APP: the same rule registry is named as /admin/rule-versions by API Specification v4 and the integration story and as /admin/rule-package* by the legacy story and the Ownership Map, and a third read /rule-catalog is consumed but unowned | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1330 | RWB-P7-E1073-APP: the case read that feeds the dry run is attributed to RWB-P3-E1073-CON by the plan and to RWB-P3-E1023-CON by the P3 contract story, which serves no operation | Solution architect with the rwb-case contract owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1331 | RWB-P7-E1073-APP: REFUSED is one of the six version states while a load refused at a check writes no rule_package_version row, so no stored version ever reaches it | Solution architect with the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1593 | Two FSD features assert the same review-queue criteria and the correction feed has no distinct criterion | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1698 | The Ownership Map lists one table for rwb-treatment, although Architecture v5 gives it four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1709 | The service is wave 2 and EP02 while every requirement of the module is an Epic 3 requirement | Solution architect | Resolved (directive) |
| GAP-1712 | The field catalog covers eight fields and none of them describes a contract, an agreement, a plan timer or a booking | Data architect | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-2030 | Delivery ownership of E1-072 and E1-073 differs between the story set and the Ownership Map | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2031 | The effective-date job is a Quartz job owned by RW-COE in version 3 and a Temporal Schedule in rwb-decision in Architecture v5 | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2049 | The rule package compile alert names P3 while the registry is P7 and the load happens in every owning service | P7 rwb-decision with the centre of excellence | Resolved (directive) |
| GAP-2087 | The source reads version 1 in its metadata table and v2 in its file name | Document owner of the notification and correspondence design | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2258 | No rerun operation for the entry run after JOB-02 becomes a workflow | TechX | Resolved (directive) |
| GAP-2259 | Paths and payloads of the P2 hand-over and P1 ledger contracts | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2260 | Interaction ledger ownership conflicts with the legacy write and the P3 data model | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2262 | CaseCreated payload and the resume of a held run are not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2348 | The rwb-document login, the request and answer field names of the generation path, the message text of MSG-P5-006, the container name, the index name, the Flyway step name and the P5 feature flag are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2349 | This slice owns no legacy acceptance criterion while the Work Package lists all eleven legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2350 | The dependency rows of this slice name one contract only, while the pattern set names five platform contracts, the rwb-case reference-data contract and the generation contract of the service | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2454 | The D7.1 generation record has no field layout, no final-call set and no message text in the sources | TechX | Resolved (directive) |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2456 | The review decision codes and outcome values, the placement of the review facts in the record, and the rwb-decision login name are in no source | Solution architect with the reference-data owner and the ACE team | Resolved (directive) |
| GAP-2457 | The physical columns of rule_package, rule_package_version, rule_row and rule_test_case are not in any source | TechX and the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2458 | No provided operation of the case service returns the open case facts a dry run needs | P3 and P7 contract owners | Resolved (directive) |
| GAP-2459 | Which owned event announces a rule package version in force is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2460 | The value of rules.testcases.min is assumed and no parameter catalogue holds it | P3 parameter owner and the P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2461 | The legacy endpoints and their controller sit in the access module, while the Ownership Map gives them to P7 | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2687 | The legacy treatment entity, its plan timers and its DP04 extract are split across three services, and no source states what the plan-timer data model holds on the S2 side once the clock moves to rwb-case | Solution architect with the data owner of rwb-treatment and the owners of rwb-case and rwb-source-data | Resolved (directive) |
| GAP-2688 | The parameters and reference-data operation names, the contract fake set, the field-level type of the event payload and the guard that limits a case to one running plan are not published for rwb-treatment | Contract owner of rwb-treatment with the parameters and reference-data owner of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3157 | The rule tables are described as recovery-schema tables but are owned by rwb-decision | P7 rule owner | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
