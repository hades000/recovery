# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 7 of 12 (RWB-P3-E2001-APP to RWB-P3-E2006-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 116 |
| Cross-document (pending in another document) | 220 |
| Not applied (value not in the sources) | 24 |
| Open business decisions | 29 |
| Register gaps linked | 93 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E2001-APP | 25 | 40 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2001 APP EFS hand-over with full history v2.md |
| RWB-P3-E2002-APP | 22 | 33 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2002 APP ACE plan status on the case v2.md |
| RWB-P3-E2004-APP | 20 | 34 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2004 APP Treatment entity and plan timers data model v2.md |
| RWB-P3-E2004-CON | 18 | 39 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2004 CON Treatment entity and plan timers data model - contract v2.md |
| RWB-P3-E2004-OPS | 12 | 38 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2004 OPS Treatment entity and plan timers data model - deployment v2.md |
| RWB-P3-E2006-APP | 19 | 31 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2006 APP Credit approval pack for NLEADS v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E2001-APP | R-10364 | CG-ALL-3953 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2001-APP | R-10365 | CG-ALL-3961 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-P3-E2001-APP | R-10366 | CG-ALL-3962 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-P3-E2002-APP | R-10377 | CG-ALL-3980 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2002-APP | R-10378 | CG-ALL-3987 | Script gap | Product owner | Open decision DL21 has no assumption | Owner rules DL21; until then build on the recommended option. |
| RWB-P3-E2004-APP | R-10385 | CG-ALL-3999 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2004-CON | R-10390 | CG-ALL-4018 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E2006-APP | R-10396 | CG-ALL-4045 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2001-ITG, RWB-P1-E1011-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22306 | GAP-0591 | Register gap | Data steward and data product owner, P1 | The REC-05 break list row for a hand-over key is defined only for keys on an existing Workbench table, not for a candidate that has no row yet | Answer the break in the candidate-facts read as {check: REC-05, keyType: PERSON_KEY or ACCOUNT_KEY, key: <value>} with resolution HELD, write no row and invent no fact, and let RWB-P1-E1011-APP's REC-05 step carry the row for the business date so the data steward and the ACE team read one list. Fix the answer in RWB-P2-E2001-CON. |
| RWB-ITG-E2001-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22309 | GAP-0588 | Register gap | Data steward and data product owner, P1 | The collection period of an account's EFS history is named by no source, so the boundary of the history read is undefined | Fix the period as the EFS assignment window of the account: it opens at v_ace_efs_assignment.assignment_start_date and closes at assignment_end_date, or at the business date of the read for the open assignment; when the account has no assignment row the period opens at its earliest contact_at. Publish the rule in RWB-P2-E2001-CON with the answer so the run and this service read the same boundary, and ask the data steward to confirm it with the ACE team before wave 2 exit. |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E1038-APP, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22353 | GAP-0919 | Register gap | Business lead | Which delegation limit version is in force on the approval date of a treatment is a data state, not a document value | Decide the version in force per environment at the DoA load (RWB-P4-E1038-APP) and keep it out of code; the lookup always answers the version whose window covers the date asked, and the answer names it |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22357 | GAP-0704 | Register gap | Data product owner | The 01:30 treatment extract has no owner in the target and its DP04 read path and freshness element are not in the Ownership Map | Record the owner of the treatment extract as P9 rwb-reporting on JOB-15 with the DP04 copy in rwb_source_data, publish the case-facing read GET /api/recovery/source-data/v1/data-products/DP04/records with its freshness element in the Ownership Map and the P1 API file, and state in the event catalogue that the copy is built from the treatment events. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2043-ITG, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P3-E2043-APP, RWB-P3-E2043-CON, RWB-P3-E2043-OPS, RWB-P7-E2001-APP, RWB-P7-E2043-APP | R-28696 | GAP-3186 | Register gap | Product owner | RWB-E2-020 is absent from the story set and the numbering skips it | State in the Change Register whether RWB-E2-020 was withdrawn or never written, and leave the identifier unused either way. |
| RWB-P3-E2001-APP | R-33422 | ASM-ALL-3961 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-P3-E2001-APP | R-33423 | ASM-ALL-3962 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-P3-E2002-APP | R-33425 | ASM-ALL-3987 | Script assumption |  | Built on the recommended option of DL21: A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead rules DL21 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS | R-36362 | ASM-1251 | Register assumption |  | The DP04 treatment product is P1 rwb-source-data's dated copy built from the treatment events and loaded by JOB-15 at 01:30 under the bank Airflow for rwb-reporting, with no data lake; the case side reads it through GET /api/recovery/source-data/v1/data-products/DP04/records and judges staleness from the freshness element of that answer, showing the previous business date with MSG-P1-001, and writes no row of it. | Data product owner with the P1 and P9 owners, at the RWB-P3-E2004-CON baseline review and the UAT run. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E2001-APP | R-16067 | DOR-RWB-P3-E2001-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | No source gives a personal-data class for the P2 fields. Section 11 rows DF-ACE-* carry no class, so none was set (would be an invented value). |
| RWB-P3-E2001-APP | R-16068 | DOR-RWB-P3-E2001-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | No source gives an assumption for DL17 or DL29, so no ASM ID is added. ASM numbering belongs to step D1, not this WP. |
| RWB-P3-E2002-APP | R-00838 | CG-ALL-3981 |  | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment ruling is not in the sources. Service Template Specification v1 is not found, and the package line is outside the supplied story text (line 364 cited only). |
| RWB-P3-E2002-APP | R-00839 | CG-ALL-3982 |  | Java package th.co.scb.ace.workbench.recovery.case.planstatus uses the reserved word 'case' | Package segment ruling is not in the sources. Service Template Specification v1 is not found, and the package line is outside the supplied story text (line 364 cited only). |
| RWB-P3-E2002-APP | R-05175 | DOR-RWB-P3-E2002-APP-17 |  | Definition of Ready item 17 Dependencies: Fail | RWB-P7-E1073-CON appears only in the DP-04 row, outside the supplied text. Header dependency rows hold only RWB-P2-E2002-CON. Cannot edit that row here. |
| RWB-P3-E2002-APP | R-10374 | CG-ALL-3975 | 4, 14 | MSG-P3-027 text differs from the Error and Message Standard v4 | Text alignment to Error and Message Standard v4 is left to that standard's owner (R-16076). |
| RWB-P3-E2002-APP | R-16072 | DOR-RWB-P3-E2002-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The guardrail personal-data statement is outside the supplied story text. The P2 personal-data conflict cannot be resolved here. |
| RWB-P3-E2002-APP | R-25029 | CG-ALL-3983 | 3 | Flyway file V2002_1__plan_status.sql is not in the V0001..Vnnnn form | Story text supplied has no V2002_1 name (section 3 and L404 checked). Service Template Spec v1 §3.1 gives V0001 to Vnnnn, but no rwb-case next number exists in sources. |
| RWB-P3-E2004-APP | R-00843 | CG-ALL-3991 | 13 | Story RWB-P7-E1073-CON named as a dependency does not exist | Only RWB-P7-E1073-APP exists (service folder RWB P7 E1073 APP). That key is not in this story or the item, so it cannot be named. Solution architect to choose the dependency key. |
| RWB-P3-E2004-APP | R-00844 | CG-ALL-4000 | 13 | Java package th.co.scb.ace.workbench.recovery.case.plantimer uses the reserved word 'case' | Package segment 'case' follows Template and Rules v1 §R4; no alternative segment in sources. Solution architect ruling needed; no name invented. |
| RWB-P3-E2004-APP | R-05180 | DOR-RWB-P3-E2004-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in 04 User stories or the source documents; sign-off cannot be asserted. |
| RWB-P3-E2004-APP | R-05184 | DOR-RWB-P3-E2004-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version recorded in the sources; the CON story records none. Cannot be invented. |
| RWB-P3-E2004-APP | R-16082 | DOR-RWB-P3-E2004-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR13 criterion in section 7 and its TC row in section 16 are outside this chunk; no anchor to edit. |
| RWB-P3-E2004-APP | R-16083 | DOR-RWB-P3-E2004-APP-7 | 11 | Definition of Ready item 7 Data: Partial | Legacy JOB and DLE wording sits in section 7 criteria, outside this chunk. Section 11 has 18 rows and needs no change. |
| RWB-P3-E2004-APP | R-25034 | CG-ALL-4001 | 7, 16 | Criteria and tests keep legacy job and decision-log wording | Partial: 14 visible criterion and test lines edited (AC1, AC5, AC6 area, TC-E2-004-05). Of 17 hits, 3 are not in the supplied text; send those lines to finish. |
| RWB-P3-E2004-CON | R-05187 | DOR-RWB-P3-E2004-CON-14 | 9 | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off record in the story or sources (earlier probe grep). Sign-off must come from the epic design record, which is not available. |
| RWB-P3-E2004-OPS | R-00856 | CG-ALL-4025 | 13 | Story RWB-P7-E1073-CON named as a dependency does not exist | No source names a replacement key; 04 User stories has no file for RWB-P7-E1073-CON. A new story ID is not allowed, so no edit. Solution architect to name the key. |
| RWB-P3-E2004-OPS | R-05194 | DOR-RWB-P3-E2004-OPS-17 | header, 13 | Definition of Ready item 17 Dependencies: Fail | Depends on CG-ALL-4025: the named dependency key is not in the sources, so no dependency can be named without inventing one. |
| RWB-P3-E2006-APP | R-00865 | CG-ALL-4046 | 12.3 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment needs Solution architect ruling. Service Template Spec v1 names none; PRD P3 rwb-case v1 line 64 has only the reserved-word name. No value invented. |
| RWB-P3-E2006-APP | R-00866 | CG-ALL-4047 | 12.3 | Java package th.co.scb.ace.workbench.recovery.case.creditapproval uses the reserved word 'case' | Same as CG-ALL-4046: Solution architect must rule the package segment. No source names one; PRD P3 rwb-case v1 line 64 has only the reserved-word name. |
| RWB-P3-E2006-APP | R-16098 | DOR-RWB-P3-E2006-APP-10 | Not specified in the source documents (DOR-RWB-P3-E2006-APP-10) | Definition of Ready item 10 Screens and states: Partial | No SCR-14 empty, loading, error or no-access state found in the sources. Sections 7 and 16 are not in the chunk, so no AC or TC row can be anchored. |
| RWB-P3-E2006-APP | R-16099 | DOR-RWB-P3-E2006-APP-11 | Not specified in the source documents (DOR-RWB-P3-E2006-APP-11) | Definition of Ready item 11 Guardrails: Partial | The DF-CAS personal-data class is in Data Classification v4/v5, but the story statement to correct is not in the chunk. No edit made. |
| RWB-P3-E2006-APP | R-25048 | CG-ALL-4048 | 3.1 | Flyway file V2006_1__credit_approval_read.sql is not in the V0001..Vnnnn form | Next Flyway number of rwb-case is not in the sources. Service Template Spec v1 §6.4 gives only the V0001 baseline. Section 3.1 text is not in the chunk. |
| RWB-P3-E2006-APP | R-30646 | NEWAC-RWB-P3-E2006-APP-AC13 | 7 | AC13: §5 X3: The reference is empty, or a refusal has no reason (covered by AC6, which exist nowhere in this story) | Section 7 and 16 text is not in the chunk, so AC13 and its test row cannot be anchored. Test is Not specified in the source documents. Section 5 X3 left unchanged. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06391 | RWB-P3-E2001-APP | CG-ALL-3943 | 12.5 | State one workflow ID form case-entry-{businessDate} started by EV-26 or EV-27; remove the competing form. |
| CDC-06392 | RWB-P3-E2001-APP | CG-ALL-3944 | 12.5 | Add activity readCandidates on task queue rwb-case. |
| CDC-06393 | RWB-P3-E2001-APP | CG-ALL-3945 | 12.5 | Add activity readEfsHistory to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-06394 | RWB-P3-E2001-APP | CG-ALL-3946 | 12.5 | Add activity CreateOrLinkCase to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-06395 | RWB-P3-E2001-APP | CG-ALL-3947 | 12.5 | Add activity AppendEfsHistory to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-06396 | RWB-P3-E2001-APP | CG-ALL-3948 | 12.5 | Add activity recordRunSummary to the Activities sheet, or name a catalogued activity in section 12.5 |
| CDC-06432 | RWB-P3-E2002-APP | CG-ALL-3973 | 12.5 | Add activity readPlanStatus to the Activities sheet. |
| CDC-06462 | RWB-P3-E2004-APP | CG-ALL-3995 | 12.5 | Add activity PlanTimerStep on task queue rwb-case with input caseId, treatmentId and businessDate. |
| CDC-06471 | RWB-P3-E2004-APP | GAP-3177 | 2 | Register the five-minute next-action Temporal Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables. |
| CDC-06497 | RWB-P3-E2004-CON | CG-ALL-4014 | 12.5 | Add activity PlanTimerStep to Activities (task queue rwb-case; input caseId, treatmentId, businessDate; output timerId, timerType, expiresAt, ruleId, ruleVersion). |
| CDC-06505 | RWB-P3-E2004-CON | GAP-3177 | n/a | Register the five-minute next-action Temporal Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables. |
| CDC-06537 | RWB-P3-E2004-OPS | CG-ALL-4029 | 12.5 | Add activity PlanTimerStep on task queue rwb-case to the Activities sheet. |
| CDC-06544 | RWB-P3-E2004-OPS | GAP-3177 | find it | Register the five-minute next-action Schedule in rwb-case in the catalog; delete EV-18 TimerDue from the Epic 2 contract tables. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06390 | RWB-P3-E2001-APP | CG-ALL-3942 | 12.4 | Add rwb-case as a consumer of rwb.source-data.AceDataLate.v1 and update its ACL. |
| CDC-06461 | RWB-P3-E2004-APP | CG-ALL-3993 | 12.4 | Add rwb-case as a consumer of rwb.treatment.TreatmentApproved.v1 and add its ACL entry. |
| CDC-06475 | RWB-P3-E2004-APP | GAP-0703 | 2 | Add rwb-case to the consumer list of rwb.treatment.TreatmentApproved.v1 so the subscription is contractual. |
| CDC-06496 | RWB-P3-E2004-CON | CG-ALL-4012 | 12.4 | Add rwb-case as a consumer of rwb.treatment.TreatmentApproved.v1 in the catalog and its ACL. |
| CDC-06510 | RWB-P3-E2004-CON | GAP-0703 | n/a | Add rwb-case as a consumer of rwb.treatment.TreatmentApproved.v1 and confirm at the wave 2 architecture review that treatment and its approval are S2's. |
| CDC-06536 | RWB-P3-E2004-OPS | CG-ALL-4027 | 12.4 | Add rwb-case as a consumer of rwb.treatment.TreatmentApproved.v1 in Events row EV-10, with its ACL. |
| CDC-06549 | RWB-P3-E2004-OPS | GAP-0703 | 12 | Add rwb-case to the consumer list of TreatmentApproved; confirm in the wave 2 architecture review that treatment ownership sits with rwb-treatment. |
| CDC-06594 | RWB-P3-E2006-APP | GAP-2483 | find it | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision.events.v1 as well as the shared ledger topic, keyed by case id with IDs, codes, levels and dates only; map it to the free identifier of EV-08, EV-09 and EV-30. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06460 | RWB-P3-E2004-APP | GAP-2474 | 4 | Add GET /rule-catalog/{ruleId}?packageVersion= as a P7 row and record the entry read as API-P7-007 of RWB-P7-E2005-APP. |
| CDC-06478 | RWB-P3-E2004-APP | GAP-1698 | 4 | Add rows for the contract, settlement and deed-in-lieu agreement and plan-timer entity groups of rwb-treatment, with their key fields as product requirements and no physical table name. |
| CDC-06495 | RWB-P3-E2004-CON | GAP-2474 | Header | Add GET /rule-catalog/{ruleId}?packageVersion= as a P7 row; state that the entry read is API-P7-007 of RWB-P7-E2005-APP. |
| CDC-06502 | RWB-P3-E2004-CON | GAP-1713 | n/a | Map each FEAT prerequisite to its owning service contract and record the mapping once |
| CDC-06514 | RWB-P3-E2004-CON | GAP-1698 | n/a | Add rows for rwb-treatment contracts, settlement and deed-in-lieu agreements, and plan timers, stating the four entity groups and their key fields. |
| CDC-06535 | RWB-P3-E2004-OPS | GAP-2474 | 12 | Add GET /rule-catalog/{ruleId}?packageVersion= as a P7 row, and record the entry read as API-P7-007 of RWB-P7-E2005-APP, before the wave 2 baseline tag. |
| CDC-06553 | RWB-P3-E2004-OPS | GAP-1698 | 5 | Add register rows for rwb-treatment contracts, settlement and deed-in-lieu agreements and plan timers; state the four entity groups without physical table names. |
| CDC-06585 | RWB-P3-E2006-APP | GAP-2478 | 7 | Rule delegation_limit to rwb-access, publish the level read with its fake, and correct the DP-07 pattern row. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06382 | RWB-P3-E2001-APP | CG-ALL-3938 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-06424 | RWB-P3-E2002-APP | CG-ALL-3967 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story |
| CDC-06457 | RWB-P3-E2004-APP | CG-ALL-3990 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer uses a published operation. |
| CDC-06491 | RWB-P3-E2004-CON | CG-ALL-4007 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml, or consume a published operation. |
| CDC-06530 | RWB-P3-E2004-OPS | CG-ALL-4024 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or agree a published operation to consume. |
| CDC-06571 | RWB-P3-E2006-APP | CG-ALL-4041 | 12.2 | Publish GET /api/recovery/access/v1/doa-limits in rwb-access.yaml through the provider's CON story. |
| CDC-06572 | RWB-P3-E2006-APP | CG-ALL-4042 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06415 | RWB-P3-E2001-APP | CG-ALL-3952 | 18 | Align trace rows for REQ-DRI-013, REQ-CHO-001, REQ-CHO-005 and the fourth listed requirement to section 18 of RWB-P3-E2001-APP at its next version. |
| CDC-06451 | RWB-P3-E2002-APP | CG-ALL-3979 | 18 | Align REQ-DRI-013 and REQ-CHO-002 test lists to story section 18: REQ-DRI-013 TC-E2-002-01, -04, -06, -07; REQ-CHO-002 TC-E2-002-02, -03, -05, -08, -09. |
| CDC-06483 | RWB-P3-E2004-APP | CG-ALL-3998 | 18 | Align the test lists of the four differing requirement rows (REQ-CHO-006, REQ-CHO-007 and two others) with RWB-P3-E2004-APP section 18 in the next RTM version. |
| CDC-06522 | RWB-P3-E2004-CON | CG-ALL-4017 | 18 | Align the test lists for the four differing requirements, including REQ-CHO-006 and REQ-CHO-007, with the story section 18 IDs. |
| CDC-06559 | RWB-P3-E2004-OPS | CG-ALL-4031 | 18 | Align the REQ-CHO-006 and REQ-CHO-007 test lists in the next RTM version with section 18 of RWB-P3-E2004-OPS. |
| CDC-06579 | RWB-P3-E2006-APP | DOR-RWB-P3-E2006-APP-12 | 12, 12.7, 16, 18 | Align the test lists of REQ-CHO-008, REQ-CHO-006 and REQ-RDF-009 with section 16 of this story, including TC-E2-006-14 and TC-E2-006-15. |
| CDC-06591 | RWB-P3-E2006-APP | CG-ALL-4044 | 18 | Align the test lists for REQ-CHO-008, REQ-CHO-006 and the third requirement row to the §18 lists of this story. |

### RWB-P2-E2001-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06387 | RWB-P3-E2001-APP | DOR-RWB-P3-E2001-APP-22 | find it | Record a contract fake library version as published. |
| CDC-06398 | RWB-P3-E2001-APP | GAP-0590 |  | Fix the key format EFS:<efs_record_key> and publish the run key set; state that the ledger writer of RWB-P1-E1066-APP counts repeated appends and the run reports both counts. |
| CDC-06399 | RWB-P3-E2001-APP | GAP-0592 |  | Publish GET /entry-candidates (RWB-P1-E1018-APP) and GET /entry-candidate-facts?businessDate= (this story) as the split, and correct the per-candidate customer read wording. |
| CDC-06406 | RWB-P3-E2001-APP | GAP-2259 | find it | Publish operation paths, request and response shapes and error envelopes for the candidate page and EFS history page; rwb-source-data contract stories to publish ledger append, REC-05 break and REC-01 result. |
| CDC-06408 | RWB-P3-E2001-APP | GAP-2463 | find it | Keep the repeat count as a meter of rwb-decision on the operational dashboard, returned in the record submission response header; rwb-integration run summary reads it. Confirm at contract review. |
| CDC-06417 | RWB-P3-E2001-APP | GAP-0589 | 3 | Precondition now says the read shape and held-read answer are Not specified (GAP-0589). |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06409 | RWB-P3-E2001-APP | GAP-2466 | find it | Record the move of the EFS history ledger write from recovery.decision.api to rwb-source-data under DP-18; keep history items on the P7 entry as evidence. |
| CDC-06476 | RWB-P3-E2004-APP | GAP-1341 | 2 | Record the legacy TimerScheduler and JOB-05 wording as superseded by Architecture v5 slides 42 and 44. |
| CDC-06487 | RWB-P3-E2004-APP | GAP-2476 | 7 | AC2 and AC14 state the CaseWorkflow durable timer; no JOB-05 or Quartz path. Sources do not say what happens to legacy timers already running at cut-over; Change Register entry still to be recorded. |
| CDC-06511 | RWB-P3-E2004-CON | GAP-1341 | n/a | Record the legacy TimerScheduler, JOB-05 and TimerDue wording as superseded by Architecture v5 slides 42 and 44. |
| CDC-06550 | RWB-P3-E2004-OPS | GAP-1341 | 12 | Record the legacy TimerScheduler, JOB-05 and TimerDue wording as superseded; the plan timer is a durable workflow timer with no topic and no Schedule. |
| CDC-06563 | RWB-P3-E2004-OPS | GAP-2476 | find it | Record how an INSTALLMENT_DUE or CURE_PERIOD timer running at cut-over is carried into the workflow that owns the wait; remove legacy steps 7 and 14 and AC2, AC12 and AC14 timer assertions from the target test set. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06456 | RWB-P3-E2004-APP | CG-ALL-3989 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP04/records through the provider's CON story, or the consumer uses a published operation. |
| CDC-06490 | RWB-P3-E2004-CON | CG-ALL-4006 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP04/records in rwb-source-data.yaml, or consume a published operation. |
| CDC-06529 | RWB-P3-E2004-OPS | CG-ALL-4023 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP04/records through the provider's CON story, or agree a published operation to consume. |
| CDC-06568 | RWB-P3-E2006-APP | CG-ALL-4038 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} in rwb-source-data.yaml through the provider's CON story. |
| CDC-06569 | RWB-P3-E2006-APP | CG-ALL-4039 | 12.2 | Publish GET /api/recovery/source-data/v1/collateral/{id} in rwb-source-data.yaml through the provider's CON story. |
| CDC-06570 | RWB-P3-E2006-APP | CG-ALL-4040 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness in rwb-source-data.yaml through the provider's CON story. |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06405 | RWB-P3-E2001-APP | GAP-2258 |  | Add an admin rerun operation on the rwb-case base that answers 409 MSG-P2-006 while the business date workflow runs, or drop manual rerun and keep the duplicate-start rule. |
| CDC-06474 | RWB-P3-E2004-APP | GAP-0918 |  | Add API-P4-022 GET /doa-limits with the request and answer of section 12.1; keep the outcome value set in the contract page; RWB-P4-E2013-APP consumes the same operation. |
| CDC-06508 | RWB-P3-E2004-CON | GAP-0918 | n/a | Add API-P4-022 GET /doa-limits with the request and answer fields of section 12.1 and the outcome value set; RWB-P4-E2013-APP consumes the same operation. |
| CDC-06547 | RWB-P3-E2004-OPS | GAP-0918 | 12.1 | Add API-P4-022 GET /doa-limits with the request and answer fields of section 12.1 and the outcome value set. |
| CDC-06586 | RWB-P3-E2006-APP | GAP-2479 | 12 | Add GET /api/recovery/access/v1/doa-limits with decisionCode, regulationItem, productGroup, amount and asOfDate; publish MSG-P7-010, MSG-GEN-006 and MSG-P4-003 texts. |

### RWB-P8-E2008-APP (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06470 | RWB-P3-E2004-APP | GAP-1346 |  | Keep plan H, C, I and X rows as given; name the seven consumed rows in section 12.2 with placeholder until owners publish; ask solution architect to confirm scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON, RWB-P7-E1073-CON. |
| CDC-06503 | RWB-P3-E2004-CON | GAP-2503 | n/a | Declare the consumed operations, name workflow matchPayments and record the AC1, AC3, AC4, AC5 gap in the RTM |
| CDC-06504 | RWB-P3-E2004-CON | GAP-1346 | n/a | Solution architect to confirm the scope of RWB-P3-E2004-CON within the plan C row |
| CDC-06542 | RWB-P3-E2004-OPS | GAP-2503 | find it | Declare the nine consumed operations on per-service bases with one hop and a 2 s timeout; name workflow matchPayments and its four activities; record in the RTM that legacy AC1, AC3, AC4 and AC5 are carried by no story. |
| CDC-06543 | RWB-P3-E2004-OPS | GAP-1346 | find it | Keep plan H, C, I and X rows as given; name the seven consumed rows in section 12.2 with the placeholder until each owner publishes; build on owner fakes on Day 1; solution architect confirms scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06385 | RWB-P3-E2001-APP | DOR-RWB-P3-E2001-APP-14 | All | Confirm the signed epic design sign-off and record it in the epic design record. |
| CDC-06426 | RWB-P3-E2002-APP | DOR-RWB-P3-E2002-APP-14 | header | Confirm and record the signed epic design sign-off for RWB-SVC-P3 |
| CDC-06531 | RWB-P3-E2004-OPS | DOR-RWB-P3-E2004-OPS-14 | Header | Record the signed epic design sign-off, then cite it in this story. |
| CDC-06573 | RWB-P3-E2006-APP | DOR-RWB-P3-E2006-APP-14 | 14 | Record the signed epic design sign-off for RWB-P3-E2006-APP; no signed design is in the story or source documents. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06401 | RWB-P3-E2001-APP | GAP-0651 |  | Mark TSD P2 v3 T5.2 and the P2 inbound exclusion as superseded by DP-05 and ADR-010; record the split from RWB-ITG-E2001-ITG and the Ownership Map. |
| CDC-06581 | RWB-P3-E2006-APP | GAP-1713 | n/a | Record once the mapping of FEAT-APD-01, FEAT-CHO-02, FEAT-CHO-06, FEAT-CHO-07, FEAT-CHO-08, FEAT-DCM-12, FEAT-OCC-01, FEAT-OCC-07, FEAT-OCC-09, FEAT-OCC-11, FEAT-TRT-04 and FEAT-VAL-06 to owning services: approval P7, case P3, documents P5, communications P6, valuation S1. Carry duplicate FEAT-CHO-08 as written. |
| CDC-06592 | RWB-P3-E2006-APP | GAP-2690 | find it | Record the treatment read and PATCH and the credit-result element set against rwb-treatment; the level comparison and its message against rwb-access and the caller; one ledger entry per record and its sealing order against rwb-decision; the SCR-14 merge against the edge contract. The split is confirmed in this story as written. |
| CDC-06593 | RWB-P3-E2006-APP | GAP-2482 | find it | Data dictionary: set source_type CREDIT_APPROVAL and source_ref as the treatment id for a D5 row. Service Contract Catalog: state that a credit result is recorded through approve or refuse on that row. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06420 | RWB-P3-E2001-APP | GAP-2468 | 8 | Carry platform H rows RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON and RWB-P7-E2005-CON; lane stays Day 1. |
| CDC-06421 | RWB-P3-E2001-APP | GAP-1335 | 8 | Show the six platform contracts and the two rwb-case contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON as sequencing dependencies. |
| CDC-06454 | RWB-P3-E2002-APP | GAP-1337 | 3 | Carry the platform contracts RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON. |
| CDC-06590 | RWB-P3-E2006-APP | GAP-1343 | Header | Publish the six DP-added dependencies with this story as consumer; RWB-P4-E1037-CON is now recorded in the Contract dependencies row. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06423 | RWB-P3-E2002-APP | CG-ALL-3966 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} through the provider CON story |
| CDC-06455 | RWB-P3-E2004-APP | CG-ALL-3988 | 12.2 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId} with query parameter packageVersion through the provider's CON story, or the consumer uses a published operation. |
| CDC-06489 | RWB-P3-E2004-CON | CG-ALL-4005 | 12.2 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= in rwb-decision.yaml, or consume a published operation. |
| CDC-06528 | RWB-P3-E2004-OPS | CG-ALL-4022 | 12.2 | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= through the provider's CON story, or agree a published operation to consume. |

### RWB-P2-E2002-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06428 | RWB-P3-E2002-APP | DOR-RWB-P3-E2002-APP-22 | header | Publish a fake library version for RWB-P2-E2002-CON and record its version as published. |
| CDC-06438 | RWB-P3-E2002-APP | GAP-0654 | find it | Settle in the wave 2 contract review: the rwb-integration login, the case read contract, the interface field sets, the live and messageCode owner, the two settings, the connection-matrix rows and the one daily step. Record in CON, OPS and this story. |
| CDC-06439 | RWB-P3-E2002-APP | GAP-0655 | find it | Approve the four assumptions before tagging the baseline: the accountNo answer field, the live and messageCode rule, the interface contract with its batch, budget and answer rules, and the consumed read shapes. Reconcile the TSD interface-versus-view wording. |
| CDC-06441 | RWB-P3-E2002-APP | GAP-0769 | find it | Confirm whether a batch plan-status operation is published. If not, read per case inside readPlanStatus, with page size from rwb.ace.plan.batch-size = 500 and timeout from rwb.ace.plan.timeout-ms = 2000. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06430 | RWB-P3-E2002-APP | CG-ALL-3963 | 4, 9, 13 | Record break_count as a field, or name the dictionary field it maps to (case break count); Data owner decides. |
| CDC-06431 | RWB-P3-E2002-APP | CG-ALL-3964 | 4, 7, 9 | Record prior_route as a field, or name the dictionary field it maps to; Data owner decides. |
| CDC-06434 | RWB-P3-E2002-APP | DOR-RWB-P3-E2002-APP-7 | 11 | Add break_count and prior_route as fields, or name the entity that holds them, so section 11 and the RestructureFacts builder can cite them. |
| CDC-06577 | RWB-P3-E2006-APP | CG-ALL-4034 | 11, 12.2 | Add the treatment credit result timestamp under its dictionary name, or record the object in the rwb-treatment document. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06433 | RWB-P3-E2002-APP | CG-ALL-3976 | 16 | TC-E2-002-11 row is in the story but not in Test Cases v8; the test case belongs in the next version of the workbook. |
| CDC-06463 | RWB-P3-E2004-APP | CG-ALL-3997 | 16 | Add TC-E2-004-15 and TC-E2-004-16 rows with Given, When and Then from the criteria they cover. |
| CDC-06521 | RWB-P3-E2004-CON | CG-ALL-4016 | 16 | Add rows TC-P3-E2004-CON-01 to TC-P3-E2004-CON-07 with Given, When and Then copied from the criteria they cover. |
| CDC-06558 | RWB-P3-E2004-OPS | CG-ALL-4030 | 16 | Add rows for TC-P3-E2004-OPS-01 to -06 to Story test cases in the next version, with Given, When and Then copied from the criterion each covers. |

### RWB-P3-E2004-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06472 | RWB-P3-E2004-APP | GAP-0705 |  | Add treatmentId, timerType, startedAt, expiresAt, warnAt, paused and status to the timers answer, all optional in major version 1, expiresAt as offset date-time. |
| CDC-06532 | RWB-P3-E2004-OPS | DOR-RWB-P3-E2004-OPS-21 | Header | Build status must reach Done; currently Not started. |
| CDC-06533 | RWB-P3-E2004-OPS | DOR-RWB-P3-E2004-OPS-22 | Header | Publish the contract fake library and record its published version. |
| CDC-06545 | RWB-P3-E2004-OPS | GAP-0705 | find it | Fix plan-timer properties treatmentId, timerType, startedAt, expiresAt, warnAt, paused and status, all optional in major version 1, with expiresAt as an offset date-time; record them in the rwb-case OpenAPI file. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06383 | RWB-P3-E2001-APP | CG-ALL-3954 |  | Rule a non-reserved package segment in place of 'case' in th.co.scb.ace.workbench.recovery.case, then the story copies it. |
| CDC-06384 | RWB-P3-E2001-APP | CG-ALL-3955 |  | Rule a non-reserved package segment in place of 'case' in th.co.scb.ace.workbench.recovery.case.handover, then the story copies it. |
| CDC-06493 | RWB-P3-E2004-CON | CG-ALL-4019 | 8 | Solution architect rules a Java package segment for rwb-case that is not the reserved word 'case', and updates the naming rule and the service table row. |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06411 | RWB-P3-E2001-APP | GAP-1332 | find it | Fix the DecisionRecorded payload and inputs snapshot (business date, queue and owner identifiers, hand-over reference, actions, composite idempotency key) and the rwb.decision-record.v1 AsyncAPI; confirm with hand-over contract owner before wave 2 build. |
| CDC-06446 | RWB-P3-E2002-APP | GAP-2471 | find it | State one entry per case, business date and rule identity, with one entry per rule when a transaction runs two rules; publish the content model of the inputs snapshot and actions payload including plan reference, plan status and date. |
| CDC-06448 | RWB-P3-E2002-APP | GAP-1338 | find it | Settle in the ledger contract that a route move running two rules writes one entry per case, business date and rule identity, and align the RWB-ITG-E2002-ITG harness and this story to that answer. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06422 | RWB-P3-E2002-APP | CG-ALL-3965 | 12.1 | Publish GET /cases/{caseId}/plan-status through the rwb-case CON story, or remove it from §12.1 |
| CDC-06566 | RWB-P3-E2006-APP | CG-ALL-4036 | 12.1 | Publish GET /api/recovery/case/v1/cases/{caseId}/credit-approval in rwb-case.yaml through the rwb-case CON story. |
| CDC-06567 | RWB-P3-E2006-APP | CG-ALL-4037 | 12.1 | Publish POST /api/recovery/case/v1/cases/{caseId}/credit-result in rwb-case.yaml through the rwb-case CON story. |

### RWB-P6-E1073-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06435 | RWB-P3-E2002-APP | GAP-2395 | find it | Settle rwb-comms package assignment with the rule registry owner. Read the three Epic 2 package codes through the contract as the fixture set and prove AC1 and AC5 on them. Do not invent a fourth code. |
| CDC-06501 | RWB-P3-E2004-CON | GAP-2395 | n/a | Settle rwb-comms package assignment with the rule registry owner; read the three package codes through the fixture set |
| CDC-06540 | RWB-P3-E2004-OPS | GAP-2395 | find it | Bind the three Epic 2 package codes and their version labels as the fixture set of this key; settle the rwb-comms package assignment with the rule registry owner before integration; invent no fourth code. |

### RWB-P7-E1073-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06445 | RWB-P3-E2002-APP | GAP-2469 | find it | Publish the registry version answer, decision-log item field names, artifact column and checksum coverage, page size, service login and one refusal message identifier before the wave-2 contract baseline is tagged. |
| CDC-06447 | RWB-P3-E2002-APP | GAP-1336 | find it | Fix the model answer shape, inputs snapshot and announcement payload in the registry contract, name the plan-status section of the decision log screen with the gateway-bff route owner, and publish the per-service login before wave 2 build. |
| CDC-06556 | RWB-P3-E2004-OPS | GAP-1339 | 13 | Fix the model and catalogue answer shape before wave 2 contract tests; add MSG-P7-009 and MSG-P7-012 to the P7 message table; name the SCR-38 and SCR-03 panels in RWB-P7-E2005-APP. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06465 | RWB-P3-E2004-APP | DOR-RWB-P3-E2004-APP-11 | 11 | Classify the personal-data fields among those listed in section 11, such as DF-DEC-010 approver_user_id, and align section 11 with that classification. |
| CDC-06578 | RWB-P3-E2006-APP | CG-ALL-4035 | 13, 12.7 | Record decision_record as the PLT library table in rwb_case in LDM v9. |
| CDC-06580 | RWB-P3-E2006-APP | DOR-RWB-P3-E2006-APP-7 | 11 | Add or confirm fields DF-ACC-009, DF-ACC-010, DF-TRT-023, DF-TRT-024, DF-TRT-025 and DF-TRT-026 so the section 11 rows resolve to LDM v9. |

### RWB-P7-E2004-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06477 | RWB-P3-E2004-APP | GAP-2473 |  | Publish the rule-catalogue answer element names and media type, decision record fields, MSG-P7-009 text and fields, system actor value and the four registry table columns. |
| CDC-06512 | RWB-P3-E2004-CON | GAP-2473 | n/a | Publish the catalogue answer element names and media type, the decision record fields, the MSG-P7-009 text and fields, the system actor value and the four registry table columns. |
| CDC-06551 | RWB-P3-E2004-OPS | GAP-2473 | 12 | Publish the catalogue answer element names and media type, decision-record field names, MSG-P7-009 text, system actor value and registry column names. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20841 | RWB-P3-E2006-APP | R-22378 |  | D5 actions key set and NLEADS pattern belong to the P7 decision-record schema and SCB IT. This file has no actions block. |
| CDC-20842 | RWB-P3-E2006-APP | R-22378 |  | D5 actions key set and NLEADS pattern belong to the P7 decision-record schema and SCB IT. This file has no actions block. |
| CDC-20843 | RWB-P3-E2006-APP | R-22378 |  | No actions key name is in the source set. The P7 decision-record schema and SCB IT confirmation are pending. This file is unchanged. |

### RWB-P7-E2005-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06410 | RWB-P3-E2001-APP | GAP-2464 | find it | Fix parameters caseId, decision, ruleId, ruleVersion, approver, from, to, page, size; page size 1 to 500; order by decided_at. RWB-P7-E2005-APP implements and tests them. |
| CDC-06412 | RWB-P3-E2001-APP | GAP-2462 | find it | Add the element list of decision_log_entry.actions and decision_log_entry.outcome to the DecisionLogEntry resource and the RWB-PLT-E1027-CON record shape at contract review. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06419 | RWB-P3-E2001-APP | GAP-2467 | 7 | No story edit; value confirmed from reference data at load. |
| CDC-06443 | RWB-P3-E2002-APP | GAP-0771 | find it | Add a table code for the plan event map to LOV-REF-TABLE in the reference-data story. Load one reference_row per ACE status and route state pair under a reference_version. No map row in code. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06449 | RWB-P3-E2002-APP | GAP-0386 | find it | Publish the gateway-bff composite case-record route path and merge order for the plan status section. Integration lead agrees harness repository, SIT and UAT environments, seed values, evidence format, retention and gate with QA. |
| CDC-06450 | RWB-P3-E2002-APP | GAP-0773 | find it | Publish the SCR-03 composite route with its path, the two parallel calls, the live-wins merge rule with MSG-P2-008 fallback, the masking rule and the 2 s budget split. |

### RWB-P4-E1037-CON; RWB-P4-E2004-APP; RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06473 | RWB-P3-E2004-APP | GAP-0917 |  | Freeze authorise and doa-limits request and answer at contract review; load the two capability areas as policy-pack rows; name the rwb-access login with the DP-02 platform DB story. |
| CDC-06507 | RWB-P3-E2004-CON | GAP-0917 | n/a | Freeze the authorise and doa-limits request and answer at contract review; load the two capability areas as policy pack rows; name the login with the platform DB story of DP-02. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06479 | RWB-P3-E2004-APP | GAP-1709 | header | In the release slicing, state that wave 2 publishes the contract and delivers the treatment record with its data date, and that offer, settlement, plan and deed in lieu capabilities release with E3. No requirement changes. |
| CDC-06515 | RWB-P3-E2004-CON | GAP-1709 | find it | State in the release slicing that the contract and the treatment record are wave 2 and the offer, settlement, plan and deed in lieu capabilities are E3; change no requirement. |

### RWB-P7-E1073-CON; RWB-PLT-E1027-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; RWB-P7-E2005-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06481 | RWB-P3-E2004-APP | GAP-1339 | 13 | Fix the model and catalogue answer shape in the OpenAPI; name the envelope fields; take MSG-P7-009 and MSG-P7-012 wording into the P7 message table; name the SCR-38 and SCR-03 panels. Story side: state in the section 13 build order that DP-added platform dependencies are held by platform stories. |
| CDC-06517 | RWB-P3-E2004-CON | GAP-1339 | find it | Fix the model and catalogue answer shape, the envelope field names, the MSG-P7-009 and MSG-P7-012 text and rows, and the SCR-38 and SCR-03 panel names. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06498 | RWB-P3-E2004-CON | CG-ALL-4015 | 4, 14 | Standard v4 row for MSG-P3-027 is not in the supplied parts; story text reverted to the original and the wording is cross-document. |
| CDC-06500 | RWB-P3-E2004-CON | DOR-RWB-P3-E2004-CON-9 | 14 | Message text left as it was until the standard row is supplied; the earlier no-edit claim is withdrawn. |

### RWB-P1-E2010-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06518 | RWB-P3-E2004-CON | GAP-0509 | find it | Add the rwb-guarantee claim read as a C dependency with its fake, and take the case-existence answer from the rwb-case contract with a fake. |
| CDC-06519 | RWB-P3-E2004-CON | GAP-2695 | find it | Name GET /treatments and GET /treatments/active-count on /api/recovery/treatment/v1 (rwb-treatment) instead of the case contract reads. |

### OTHER:gateway-bff route catalogue (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06524 | RWB-P3-E2004-CON | GAP-0920 | find it | Publish the SCR-14 treatment record and SCR-03 timer panel composite routes with their field lists, and confirm no field on either is a personal field. |
| CDC-06561 | RWB-P3-E2004-OPS | GAP-0920 | find it | Publish the SCR-14 treatment record and SCR-03 timer panel composite routes with their field lists, and confirm that no field on either is a personal field. |

### OTHER:Platform DB story of DP-02 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06525 | RWB-P3-E2004-CON | GAP-0921 | find it | Fix the rwb-access login name, its grants and its schema owner there, and have every P4 story reference it. |
| CDC-06562 | RWB-P3-E2004-OPS | GAP-0921 | find it | Fix the rwb-access login name, its grants and its schema owner, and have every P4 story reference it rather than repeat it. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06595 | RWB-P3-E2006-APP | GAP-2484 | find it | Keep the metadata rows as the work package gives them; treat the four platform contracts as published before Day 1 work starts; give GET /cases/{caseId}/recommendation to the P7 story serving the decision screen in the next version. |
| CDC-06596 | RWB-P3-E2006-APP | GAP-3232 | find it | Use the catalog Dependencies sheet as the source of the v5 graph; state the template baseline once on the Dependency classes sheet. Story files keep their rows; no story is re-cut. |

### RWB-P3-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06386 | RWB-P3-E2001-APP | DOR-RWB-P3-E2001-APP-21 | All | Create contract story RWB-P3-E2001-CON and list it as a contract dependency of this story. |

### OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06388 | RWB-P3-E2001-APP | DOR-RWB-P3-E2001-APP-8 | find it | Publish POST /api/recovery/access/v1/authorise. Other flagged items are covered by CG-ALL-3939, CG-ALL-3940 and CG-ALL-3942 or lie outside this chunk. |

### OTHER:FSD P3 A1.5 (Functional Specification; OTHER:P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06389 | RWB-P3-E2001-APP | GAP-1549 | find it | Restate the ACE read path as a read through the rwb-source-data contract, keeping the business-key link rules unchanged. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06397 | RWB-P3-E2001-APP | GAP-3176 |  | Confirm no Epic 2 step depends on JOB-01; list AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### OTHER:Harness pack (values held as data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06400 | RWB-P3-E2001-APP | GAP-0388 |  | Hold the harness repository, SIT and UAT environments, seeding, evidence format, retention, pass/fail gate and the gateway-bff route paths as data in the harness pack. |

### OTHER:contract/handover-run-activities.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06402 | RWB-P3-E2001-APP | GAP-0652 |  | Fix the workflow, nine activities, twelve summary elements and retry policy; fix the six P1 and one P3 consumed elements; publish six fakes from owner OpenAPI and fail the build on drift. |

### OTHER:rwb-integration EFS hand-over deployment story (story key not named in this story or in the sources read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06403 | RWB-P3-E2001-APP | GAP-0653 |  | Fix the chart, the one consumer group, the registration step, the migration step, the six series, the four alerts and the four runbook entries there; keep every environment value in a values file; keep each missing message id as Not specified in the source documents (GAP-0653) until the Error and Message Standard names it; review the runbook with the on-call rota before the release date. |

### OTHER:TSD P7 decision-log contract (API-P7-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06404 | RWB-P3-E2001-APP | GAP-1333 |  | Add the businessDate filter, the full DecisionLogPage and DecisionLogEntry field set, the page-size limit, and one panel name for a decision entry beside the case. |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06407 | RWB-P3-E2001-APP | GAP-2260 | find it | Mark the T3.1 interaction object as owned by rwb-source-data; re-scope the P3 ledger story to the P1 ledger contract. |

### RWB-PLT-E1047-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06413 | RWB-P3-E2001-APP | GAP-2262 | 12 | Fix envelope and retry and dead-letter settings of rwb.case.events.v1 (with RWB-PLT-TE006-CON); event payload limited to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate, dpdAtEntry. |

### OTHER:Work Package B2-P3-020 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06414 | RWB-P3-E2001-APP | GAP-2261 | Header | Add platform CON dependencies RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON to the lane and Day-1 allocation. |

### OTHER:RWB-PLT-OBS; RWB-P7-E1027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06416 | RWB-P3-E2001-APP | GAP-2465 | 4 | Register ingest lag of rwb.decision-record.v1 into the ledger as a metric of RWB-PLT-OBS with threshold as a parameter; raise gap alert to RW-PLATADM under RWB-P7-E1027-APP. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:database platform story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06418 | RWB-P3-E2001-APP | GAP-1334 | Not specified in the source documents (GAP-1334) | Publish the per-service login of rwb_decision with the database platform story; fix workflow, activity and Schedule identifier names for the 02:00 chain check in the Temporal Workflow and Activity Catalog before wave 2 build. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06425 | RWB-P3-E2002-APP | CG-ALL-3969 | 13 | Create story RWB-P7-E1073-CON for the rwb-decision rule-model contract used by DP-04 |

### RWB-P3-E2002-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06427 | RWB-P3-E2002-APP | DOR-RWB-P3-E2002-APP-21 | header | Create contract story RWB-P3-E2002-CON for the rwb-case operations of this story and name it as a contract dependency. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; OTHER:rwb-decision API yaml; OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06429 | RWB-P3-E2002-APP | DOR-RWB-P3-E2002-APP-8 | 4, 12.1 | Publish GET /cases/{caseId}/plan-status and GET /cases/{caseId}/timers in rwb-case; GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} in rwb-decision; POST /api/recovery/access/v1/authorise in rwb-access. |

### RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06436 | RWB-P3-E2002-APP | GAP-0907 | find it | Add a Case record column for all roles, publish the 14-area matrix as data, and confirm the CASE_RECORD letters and default scopes with the matrix owner before PM-2026.12. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06437 | RWB-P3-E2002-APP | GAP-0908 | find it | Add the authorise path and resolved permission view with request and answer schemas to the API specification and TSD P4 appendix T-A, stub them in the contract fake, and record whether the plan reference travels in the authorise request. |

### RWB-P2-E2002-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06440 | RWB-P3-E2002-APP | GAP-0656 | find it | Approve the three assumptions in the release readiness review: identity and environment values, trigger wiring with ACE-or-stub, and the five series, four alerts, no-package row and four runbook entries. Carry thresholds and endpoints as environment values. |

### OTHER:P7 decision contract on /api/recovery/decision/v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06442 | RWB-P3-E2002-APP | GAP-0770 | find it | Publish the catalog-row read by rule ID and package version, returning action_text, owner_role, timer_spec, target queue code and outputs. Until then read through the contract fake and KieBase answer. |

### OTHER:Service Catalog and Key Vault (platform database story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06444 | RWB-P3-E2002-APP | GAP-0774 | find it | Allocate the rwb-case login with its schema from the 19-schema list, derive its name from the schema, hold the secret in Key Vault and record the login in the Service Catalog before first deployment. |

### OTHER:P1 contract story for rwb-source-data (reconciliation_result) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06452 | RWB-P3-E2002-APP | GAP-0772 | 8 | BR14 reverted to the original text; the interim delivery path is not in the sources. |

### OTHER:Platform DB story (rwb-access login) and gateway-bff composite route for SCR-03 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06453 | RWB-P3-E2002-APP | GAP-0909 | 15 | Three-field panel statement removed; screen fields stay Not specified. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E2004 CON Treat (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06458 | RWB-P3-E2004-APP | DOR-RWB-P3-E2004-APP-21 | none | Build status of RWB-P3-E2004-CON is Not started; its owner sets it to Done once the contract is built and published. |

### OTHER:API yaml of rwb-decision, rwb-source-data and rwb-access; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06459 | RWB-P3-E2004-APP | DOR-RWB-P3-E2004-APP-8 | 4, 12.3 | Publish GET rule-catalog/{ruleId}, GET DP04 records and POST authorise in the owning API yaml; the event payload mismatch is fixed under CG-ALL-3992. |

### OTHER:P3 screen specification for SCR-03; OTHER:SCR-09 and SCR-14 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06464 | RWB-P3-E2004-APP | DOR-RWB-P3-E2004-APP-10 | none | Add empty, loading, error and no-access states to SCR-03, SCR-09 and SCR-14. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06466 | RWB-P3-E2004-APP | DOR-RWB-P3-E2004-APP-12 | 12, 12.7, 16, 18 | Added TC-E2-004-17 (section 12 contract test) and TC-E2-004-18 (12.7 boundary, ASM-3438); AC15 to AC18 added TC-E2-004-19 to 22 |

### OTHER:RWB-E2-042 legacy story and FSD P6 v3 with the rule registry owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06467 | RWB-P3-E2004-APP | GAP-2395 | find it | Name which rule package of the three Epic 2 packages rwb-comms reads, and the package code it is assigned, read as the fixture set of this key. |

### OTHER:Functional Specification Document S2 and the service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06468 | RWB-P3-E2004-APP | GAP-1713 | find it | Map each feature-code prerequisite to the owning service's contract, record the mapping once, and carry the duplicate FEAT-CHO-08 as written. |

### RWB-P8-E2008-APP; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06469 | RWB-P3-E2004-APP | GAP-2503 |  | Declare the nine consumed operations on per-service bases, one hop, 2 s timeout, element names from owners; name workflow matchPayments and its four activities; record in RTM that legacy AC1, AC3, AC4, AC5 are carried by no story of this split. |

### OTHER:Functional Specification S2 (FSD S2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06480 | RWB-P3-E2004-APP | GAP-1712 | 4 | Keep the eight-field catalogue as written; add the contract, agreement, plan timer and booking reference as held entities, with the physical field list left open until the data architect writes it. |

### OTHER:Template and Rules R5.5; OTHER:WP B2-P7-019 story line (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06482 | RWB-P3-E2004-APP | GAP-2475 | header | State in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories and not repeated on a secondary APP line, or complete the metadata rows. |

### OTHER:rwb-case values files and the runbook entry each alert links (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06484 | RWB-P3-E2004-APP | GAP-0706 | find it | Set provisional alert values for plan-timer projection lag, subscription lag, .dlt count, exception-queue count and DP04 freshness; confirm them at UAT with the service owner and platform observability owner. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06485 | RWB-P3-E2004-APP | GAP-0920 | find it | Publish the SCR-14 treatment record and SCR-03 timer panel composite routes with their field lists and confirm no field is a personal field. |

### OTHER:platform DB story of DP-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06486 | RWB-P3-E2004-APP | GAP-0921 | find it | Fix the rwb-access login name, its grants and its schema owner there, and reference it from P4 stories rather than repeating it. |

### OTHER:rwb-treatment service contract document, major version 1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06488 | RWB-P3-E2004-APP | GAP-2688 | find it | Name the parameters and reference-data operations, member-level payload types, fake set, and the one-running-plan guard as a partial unique index on the treatment row. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06492 | RWB-P3-E2004-CON | CG-ALL-4008 | 13 | Create RWB-P7-E1073-CON, or name the existing story that carries the DP-04 rule-package dependency. |

### OTHER:rwb-decision API yaml; OTHER:rwb-source-data API yaml; OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06494 | RWB-P3-E2004-CON | DOR-RWB-P3-E2004-CON-8 | Header | Publish GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= in rwb-decision; GET /api/recovery/source-data/v1/data-products/DP04/records in rwb-source-data; POST /api/recovery/access/v1/authorise in rwb-access; in rwb-case.yaml hold timerType as an LOV-TIMER reference, not a closed enum; resolve the 5 further detcheck findings. |

### RWB-P3-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06499 | RWB-P3-E2004-CON | DOR-RWB-P3-E2004-CON-10 | Header | Add empty, loading, error and no-access states for SCR-03. |

### OTHER:rwb-case OpenAPI file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06506 | RWB-P3-E2004-CON | GAP-0705 | 7 | Timers AC keeps no plan-timer property list; the next Then line names the fields |

### OTHER:Wave 2 integration harness pack (repository not specified in the source documents (GAP-0389)) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06509 | RWB-P3-E2004-CON | GAP-0389 | n/a | Agree with QA and the integration lead before the first SIT run: repository and pipeline, SIT and UAT namespaces, seed files, business clock, evidence report, pass/fail gate and gateway-bff composite route. |

### OTHER:S2 rwb-treatment data model (rwb_treatment treatment table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06513 | RWB-P3-E2004-CON | GAP-2687 | n/a | Hold the treatment and plan facts on one table, publish them on rwb.treatment.TreatmentApproved.v1, and keep no timer table, Quartz job, TimerDue topic or extract in S2. |

### OTHER:Functional Specification S2 (field catalogues A2.1 to A2.18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06516 | RWB-P3-E2004-CON | GAP-1712 | find it | Add field catalogue rows for contract, agreement, plan timer and booking reference; leave the physical field list open to the DB story. |

### RWB-P10-E2032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06520 | RWB-P3-E2004-CON | GAP-0633 | find it | Fix the suggestion operation path under /api/recovery/agent/v1, its media type and refusal codes, and the read routes and waits. |

### OTHER:rwb-case values files and the runbook entries each alert links (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06523 | RWB-P3-E2004-CON | GAP-0706 | find it | Set provisional default values for the plan-timer projection lag, subscription lag, .dlt count, exception-queue count and DP04 freshness, and confirm them at UAT with the service owner and platform observability owner. |

### RWB-P7-E2004-APP; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06526 | RWB-P3-E2004-CON | GAP-2476 | find it | Record how a running INSTALLMENT_DUE or CURE_PERIOD timer is carried into the workflow at cut-over; remove legacy steps 7 and 14 and AC2, AC12 and AC14 from the target test set. |

### OTHER:Service contract document of rwb-treatment at major version 1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06527 | RWB-P3-E2004-CON | GAP-2688 | find it | Name the two consumed operations, member-level types of the TreatmentApproved payload, the fake set, and the one-running-plan guard as a partial unique index on the treatment row. |

### OTHER:rwb-decision, rwb-source-data and rwb-access API yamls; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06534 | RWB-P3-E2004-OPS | DOR-RWB-P3-E2004-OPS-8 | 12 | Publish the named paths in their owning API yamls and align the event type rwb.decision-record.DecisionRecorded.v1 with Kafka Catalog v1, and clear the three further detcheck items. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06538 | RWB-P3-E2004-OPS | DOR-RWB-P3-E2004-OPS-1 | 1 | Add 'platform engineer' as a role code and name, or confirm the v5 role this story should name in section 1. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06539 | RWB-P3-E2004-OPS | GAP-2404 | find it | Read the H list as None plus RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON; the C list as RWB-P10-E2032-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and the P4 authorise contract. |

### OTHER:FSD S2 A1.1 and A2 prerequisites; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06541 | RWB-P3-E2004-OPS | GAP-1713 | find it | Map each feature-code prerequisite to its owning service contract (P7 approval, P3 case, P5 documents, P6 communications, S1 valuation) once in the service contract; carry duplicate FEAT-CHO-08 as written. |

### RWB-P4-E1037-CON; RWB-P4-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06546 | RWB-P3-E2004-OPS | GAP-0917 | find it | Freeze the authorise and doa-limits request and answer at contract review; load the two capability areas as rows in the policy pack RWB-P4-AD002-APP; name the rwb-access login with the platform DB story of DP-02. |

### OTHER:Integration test harness pack (QA and integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06548 | RWB-P3-E2004-OPS | GAP-0389 | 16 | Agree the harness repository, environments, seed files, business clock, evidence format and retention, pass/fail gate and composite case-record route before the first SIT run. |

### RWB-P3-E2004-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06552 | RWB-P3-E2004-OPS | GAP-2687 | 12 | Hold treatment and plan facts on one rwb_treatment table; keep no timer table, Quartz job, TimerDue topic or DP04 extract; the fourteen legacy criteria stay with RWB-P3-E2004-APP. |

### OTHER:PRD (release slicing) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06554 | RWB-P3-E2004-OPS | GAP-1709 | 3 | State in the release slicing that wave 2 delivers the treatment record and data date and E3 delivers offer, settlement, plan and deed in lieu; no requirement changes. |

### OTHER:FSD S2 (field catalogs A2.2.3.2 to A2.15.3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06555 | RWB-P3-E2004-OPS | GAP-1712 | 5 | Require the eight catalog fields as written and require the contract, agreement, plan timer and booking reference to be held, with the physical field list left open. |

### OTHER:Template and Rules (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06557 | RWB-P3-E2004-OPS | GAP-2475 | find it | In R5.5, state that a platform H row and a self-referential C row are held by the platform and contract stories and are not repeated on a secondary APP line, or complete the metadata rows from the table. |

### OTHER:rwb-case values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06560 | RWB-P3-E2004-OPS | GAP-0706 | find it | Set provisional default values for the plan-timer projection lag, subscription lag, .dlt count, exception-queue count and DP04 freshness; confirm at UAT; record agreed values in the linked runbook entries. |

### OTHER:rwb-treatment service contract document v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06564 | RWB-P3-E2004-OPS | GAP-2688 | find it | Name the two consumed operations, the member-level types of the TreatmentApproved payload and the fake set; state the one-running-plan guard as a partial unique index on the treatment row. |

### OTHER:Metadata rows of the WP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06565 | RWB-P3-E2004-OPS | GAP-1340 | 13 | Metadata rows stay as the WP fixes them; the twelve dependencies are read from section 13 at build-order; no story edit. |

### RWB-PLT-E1027-CON; RWB-PLT-E1043-CON; RWB-P3-E1043-CON; RWB-PLT-E1044-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06574 | RWB-P3-E2006-APP | DOR-RWB-P3-E2006-APP-21 | header | Bring the listed CON stories to Done so the contract is published. |

### OTHER:rwb-source-data, rwb-treatment, rwb-document and rwb-access WireMock fakes (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06575 | RWB-P3-E2006-APP | DOR-RWB-P3-E2006-APP-22 | 12.8 | Publish the fake library versions used in 12.8 and record the version as published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; OTHER:rwb-source-data yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06576 | RWB-P3-E2006-APP | DOR-RWB-P3-E2006-APP-8 | find it | Publish GET /cases/{caseId}/credit-approval and POST /cases/{caseId}/credit-result in rwb-case.yaml, and the source-data accounts, collateral and 3 further detcheck paths. |

### RWB-ITG-E2006-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06582 | RWB-P3-E2006-APP | GAP-1344 | n/a | Correct the third owning slice attribution: delegation_limit stays with P4 rwb-access, and rwb-decision holds only the level read and the version applied, per the Ownership Map ruling. |

### OTHER:rwb-case contract and doa.txt item 2.1.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06583 | RWB-P3-E2006-APP | GAP-0729 | 7 | Agree the rwb-case login, SCR-14 composite route, NLEADS read and treatment result field names; settle the AC2 and AC7 levels against doa.txt before wave 2 build. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06584 | RWB-P3-E2006-APP | GAP-1342 | 12 | Settle at wave 2 contract review: rwb-decision login, decide path, delegation read, actions keys, comparison site, message texts, sub-code and screen identity. |

### OTHER:P7 decision-record schema document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06587 | RWB-P3-E2006-APP | GAP-2480 | 7 | nleadsRef key reverted; AC2 holds the NLEADS reference only |

### OTHER:TSD P7 v2 T6.1 RBAC matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06588 | RWB-P3-E2006-APP | GAP-2481 | 7 | Declare Decision log right A on the two recording operations; add A rows for result-recording roles; keep Treatment and offer U on the rwb-integration pack endpoint. |

### OTHER:TSD S2 v2 and FSD S2 v3 (rwb-treatment contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06589 | RWB-P3-E2006-APP | GAP-2689 | 7, 12 | Add the credit-result variant of the treatment PATCH with element names, a SUBMITTED/APPROVED/REFUSED state check, four credit columns, one result per treatment and its own refusal message. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_treatment.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20626 | RWB-P3-E2004-CON | R-22360 |  | No writer for .sql files. Single treatment table and no timer objects already present; topic rwb.treatment.TreatmentApproved.v1 absent (doc uses rwb.treatment.events.v1). |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20715 | RWB-P3-E2001-APP | R-22316 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21918', 'R-22054', 'R-22286', 'R-22289', 'R-22316', 'R-28613'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0386 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0388 | EFS hand-over harness: repository, environments, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0389 | The harness repository, environments, seeding, business clock, evidence format and retention, pass/fail gate and the gateway-bff composite case-record route are not defined in the source documents | Integration lead | Resolved (directive) |
| GAP-0394 | Credit approval pack integration harness: composite credit-pack route, harness environment, seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0509 | The guarantee claim read of rwb-guarantee and the case-existence answer are not in the Work Package's contract list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0589 | The history read is one operation or a paged read, and the HTTP answer of a held read, are stated by no source | Solution architect, P1 | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0592 | No source splits the hand-over facts between the candidate rule and the borrower and product-group facts, and the run's contract names a per-candidate customer read | Solution architect, P1 and P2 | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0633 | The TDR offer-suggestion slice in rwb-agent: the operation path below the base, the treatment and account read operations, the parameter keys, the screen route, the run version fields, the inputs reference and the two waits of the call are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-treatment, rwb-case and rwb-decision | Resolved (directive) |
| GAP-0651 | rwb-integration EFS hand-over: the mount of the step, the split across four owners, the consumed contract paths, the run summary store and the level of the decision record are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0652 | rwb-integration EFS hand-over contract: the activity contract, the consumed element shapes, the provided surface and the fakes have no source text | Tech lead | Resolved (directive) |
| GAP-0653 | rwb-integration EFS hand-over deployment: the values, the alert identifiers, the dashboard series and the runbook have no source | DevOps lead | Resolved (directive) |
| GAP-0654 | rwb-integration ACE plan status: the login, the account resolution, the interface field types, the meaning of live and messageCode, the two settings, the connection-matrix rows and the ownership split are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0655 | The plan-status contract baseline: the accountNo field, the meaning and owner of live and messageCode, the interface null rules, the consumed read shapes, the composite route and the two specification conflicts are not fixed by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0656 | The plan-status deployment values, the ACE endpoint and certificate references, the two setting values at run time, the trigger wiring, the alert thresholds, the mapping of the no-package condition and the fixture owner are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0663 | rwb-integration credit approval pack: login, contract field names, NLEADS read, the ownership split, the integration-base resource placement and the approval-level values are not settled by any one source | Solution architect | Resolved (directive) |
| GAP-0703 | The treatment entity moves to S2 while the legacy story holds it in P3, and the case side consumes TreatmentApproved which the event catalogue does not list for rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0705 | No source fixes the plan-timer fields, types or required flags of the timers answer behind GET /cases/{caseId}/timers | Tech lead of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0706 | No source gives the alert values for the plan-timer projection, the subscription lag, the DP04 freshness or the exception-queue count | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-0917 | rwb-access treatment and plan-timer slice: the authorise request and answer, the Treatment and offer and Case record letters and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0918 | The delegation lookup GET /doa-limits and its request and answer fields exist only on Architecture v5 slide 14, not in the TSD P4 appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0920 | The composite route field list for SCR-14 Treatment record and the SCR-03 timer panel is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0921 | The per-service login of rwb-access is named by DP-02 and by no document | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1698 | The Ownership Map lists one table for rwb-treatment, although Architecture v5 gives it four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2687 | The legacy treatment entity, its plan timers and its DP04 extract are split across three services, and no source states what the plan-timer data model holds on the S2 side once the clock moves to rwb-case | Solution architect with the data owner of rwb-treatment and the owners of rwb-case and rwb-source-data | Resolved (directive) |
| GAP-2688 | The parameters and reference-data operation names, the contract fake set, the field-level type of the event payload and the guard that limits a case to one running plan are not published for rwb-treatment | Contract owner of rwb-treatment with the parameters and reference-data owner of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2689 | The treatment-side credit-result record has no operation, no element names, no state values and no column rule in the S2 sources | Solution architect, S2, with the rwb-treatment tech lead and the rwb-integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2690 | The rwb-treatment share of the key is stated by no S2 source, and the caller contract, the level comparison, the case move and the record ownership are split across four stories | Solution architect with the rwb-integration, rwb-treatment, rwb-case and rwb-access tech leads and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2695 | The owner of the treatment changed-window and active-count reads conflicts between the DP04 story and the service ownership | Solution architect | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3232 | The story catalog carries 2,534 dependency rows while the story files carry 2,609 for the same 1,034 stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E2006-APP | skipped AC ID | 113 | missing: AC4, AC5, AC6, AC7, AC8, AC10, AC13 |
| RWB-P3-E2006-APP | new AC without TC row | 452 | AC12 is new and no section 16 row covers it |
