# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 5 of 12 (RWB-P3-E1043-CON to RWB-P3-E1054-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 5 |
| Resolved in the stories | 122 |
| Cross-document (pending in another document) | 214 |
| Not applied (value not in the sources) | 4 |
| Open business decisions | 17 |
| Register gaps linked | 152 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E1043-CON | 31 | 93 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1043 CON Reference data service with versioned tables - contract v2.md |
| RWB-P3-E1045-APP | 20 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1045 APP Multi-product parameters for Mortgage, HP and SSME v2.md |
| RWB-P3-E1050-APP | 17 | 33 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1050 APP Document classification v2.md |
| RWB-P3-E1052-APP | 24 | 47 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1052 APP Notice generation v1 v2.md |
| RWB-P3-E1054-APP | 30 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1054 APP Review queue for low-confidence documents v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1049-ITG, RWB-ITG-E1050-ITG, RWB-P3-E1050-APP, RWB-P5-E1049-APP, RWB-P5-E1049-CON, RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1053-CON, RWB-P6-E1049-APP | R-09185 | GAP-1586 | Register gap | Solution architect with the AI product owner | The OCR, classification and extraction services are named as external pieces but no source names them or their owner | The PRD keeps the pipeline behaviour in P5 and states the OCR, classification and extraction engines as an external contract reached as an AgentRunCompleted event or a Temporal child run, with the provider, the contract and the version scheme carried as OQ-P5-06. |
| RWB-P3-E1054-APP | R-10324 | CG-ALL-3847 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1025-APP, RWB-P5-E1052-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-22159 | GAP-2347 | Register gap | Data steward and document type owner, with the Legal counsel and the P5 TechX squad | The notice-type to document-type mapping, the retention class and the write-once flag of each notice document type are not specified in any source read here | The document type load of RWB-P5-E1025-APP carries the DEMAND_LETTER and GUARANTOR_NOTICE rows with their class and flag, and the notice-type mapping row is added to the type or mapping table before the wave-1 test data is loaded |
| RWB-ITG-E1057-ITG, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-P5-E1057-APP, RWB-P5-E1057-CON, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-S9-E1057-APP | R-22197 | GAP-3146 | Register gap | Business lead; solution architect; rwb-partner tech lead; rwb-access owner; programme lead | RWB-S9-E1057-APP: the split plan gives this secondary slice no legacy criterion and no build row while the P5 slice of the same key hands the partner criteria to it, no source publishes a partner-by-code read or the code filter of GET /partners, the two refusal reasons and the not-found behaviour are not published, the constraint on partner_code and the panel transition table are not specified, the DP-07 rows cannot be carried in an empty H row, and EP01 wave 1 is earlier than the service wave 4 | Serve the partner panel read as the code filter of the published GET /partners under base /api/recovery/partner/v1 with right R and the scope applied, answer the six published properties from partner in rwb_partner, answer an empty list for an unknown code and the stored panel status for a partner that is not ACTIVE, leave BR4 and the two reasons with the caller, read LOV-PANEL and LOV-PARTNER-TYPE through DP-07, write nothing and publish nothing, keep wave 1 and record the DP-07 rows, the constraint on the partner code, the panel transition table and the criteria assignment of the two slices as open items. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1052-ITG, RWB-P3-E1052-APP, RWB-P5-E1052-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P7-E1052-APP | R-28611 | GAP-2088 | Register gap | Business lead with Legal and Compliance; document owner | DL10 is listed open with one answer and is recorded as answered with another | Keep the source row word for word, record in section 6.1 that DL10 is answered on 5 November 2026 with answer A, and add no Thai wording in this document. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1043-CON, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-28792 | GAP-2097 | Register gap | Service owners of P3 rwb-case and P4 rwb-access; business lead | Reference data is read from P4 in TSD P6 and from P3 in the plan default ruling | Follow R3 and DP-07: contact times and frequency are reference data of P3 rwb-case, read through C RWB-P3-E1043-CON. Access data, roles and DoA stay with P4. |
| RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1043-APP, RWB-P3-E1043-CON | R-29035 | GAP-0222 | Register gap | Data steward and data product owner | The Owner column is a stewardship role, not a service, and it is kept unchanged | Read column D as the stewardship owner that approves a value, and the appended 'Owning service (D-RCV-60)' as the service that loads and serves it; the Key sheet gains the two terms that say so. |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E1050-APP | R-05101 | DOR-RWB-P3-E1050-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | Section 14 text is not in this chunk, so no exact old text can be matched. Sign-off date and owner are not in the sources (Not specified in the source documents). |
| RWB-P3-E1050-APP | R-05102 | DOR-RWB-P3-E1050-APP-16 | 14 | Definition of Ready item 16 Size: Fail | Section 14 text is not in this chunk, so no exact old text can be matched. No size exists in the story or sources; the placeholder needs the DoR row text to be placed. |
| RWB-P3-E1050-APP | R-05104 | DOR-RWB-P3-E1050-APP-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | Section 12.8 text is not in this chunk, so no exact old text can be matched. No published version of the rwb-document WireMock fake exists in the sources. |
| RWB-P3-E1054-APP | R-24984 | CG-ALL-3845 | 16 | Test cases cover other criteria in Test Cases v8 | Covers cells cite AC11 to AC17, which the story does not contain; the criteria text is not in the sources, so the story cannot be aligned here. |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (26)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06073 | RWB-P3-E1045-APP | DOR-RWB-P3-E1045-APP-7 | 11 | Add field valid_from to parameter_value, which the story's index on parameter_value.valid_from DESC requires; the story is otherwise unchanged. |
| CDC-06086 | RWB-P3-E1050-APP | CG-ALL-3769 | 3, 7, 13 | Record entity case_document_link in schema rwb_case, created by RWB-P3-E1032-APP, with its fields, or give the dictionary name the owner uses. |
| CDC-06087 | RWB-P3-E1050-APP | CG-ALL-3770 | 11 | Add field `document_type_code` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06088 | RWB-P3-E1050-APP | CG-ALL-3771 | 11 | Add field `candidate_one_type` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06089 | RWB-P3-E1050-APP | CG-ALL-3772 | 11 | Add field `candidate_one_confidence` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06090 | RWB-P3-E1050-APP | CG-ALL-3773 | 11 | Add field `candidate_two_type` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06091 | RWB-P3-E1050-APP | CG-ALL-3774 | 11 | Add field `candidate_two_confidence` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06092 | RWB-P3-E1050-APP | CG-ALL-3775 | 11 | Add field `classification_state` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06093 | RWB-P3-E1050-APP | CG-ALL-3776 | 11 | Add field `checklist_item_state` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06094 | RWB-P3-E1050-APP | CG-ALL-3777 | 11 | Add field `classified_at` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06095 | RWB-P3-E1050-APP | CG-ALL-3778 | 11 | Add field `source_event_id` to LDM v9 for rwb_case.case_document_link, or record it as a rwb-case column in the owning document. |
| CDC-06100 | RWB-P3-E1050-APP | DOR-RWB-P3-E1050-APP-7 | 11 | Add entity case_document_link and the classification fields named in §11 (GAP-0765) to LDM v9 or Data Classification v5. |
| CDC-06103 | RWB-P3-E1050-APP | GAP-0765 | find it | Register rwb_case.case_document_link with its field IDs, including the classification columns added in V1050_1; rwb-case writes no P5 table. |
| CDC-06114 | RWB-P3-E1052-APP | CG-ALL-3794 | 13 | Index keeps recovery_case.notice_ref; the column must be registered in LDM v9. |
| CDC-06127 | RWB-P3-E1052-APP | DOR-RWB-P3-E1052-APP-7 | 11 | Add field IDs for the seven recovery_case notice columns (GAP-0749; ASM-1370): notice_ref, notice_state, notice_hold_reason, notice_template_code, notice_template_version, notice_document_id, notice_delivered_at. |
| CDC-06129 | RWB-P3-E1052-APP | CG-ALL-3795 | 11 | Register notice_state as a recovery_case field (GAP-0749; ASM-1370), or record it as a gap in the owning document. |
| CDC-06130 | RWB-P3-E1052-APP | CG-ALL-3796 | 11 | Register notice_hold_reason as a recovery_case field (GAP-0749; ASM-1370), or record it as a gap in the owning document. |
| CDC-06131 | RWB-P3-E1052-APP | CG-ALL-3797 | 13 | Record recovery_case column notice_template_code under a field ID, or confirm its dictionary name (nearest: template_code) |
| CDC-06132 | RWB-P3-E1052-APP | CG-ALL-3798 | 13 | Record recovery_case column notice_template_version under a field ID, or confirm its dictionary name (nearest: template_version) |
| CDC-06133 | RWB-P3-E1052-APP | CG-ALL-3799 | 13 | Record recovery_case column notice_document_id under a field ID, or confirm its dictionary name (nearest: document_id) |
| CDC-06134 | RWB-P3-E1052-APP | CG-ALL-3800 | 13 | Record recovery_case column notice_delivered_at under a field ID, or confirm its dictionary name (nearest: delivered_at) |
| CDC-06161 | RWB-P3-E1054-APP | CG-ALL-3834 | 13 | Add field document_ref on entity task (varchar(40), document ID of the review link) so the index in section 13 resolves. outcome_code holds the outcome, not the document ID, so it is not a substitute. |
| CDC-06170 | RWB-P3-E1054-APP | DOR-RWB-P3-E1054-APP-7 | 11 | Register task.document_ref, task.review_state, task.item_version (task columns added by migration V1054_1) and case_account.account_id as Fields, or name their dictionary equivalents. |
| CDC-06172 | RWB-P3-E1054-APP | CG-ALL-3835 | 4, 11, 13 | Record task.review_state (varchar(15), added by migration V1054_1, values PENDING_REVIEW, CONFIRMED, CORRECTED) as a task column in Fields. |
| CDC-06173 | RWB-P3-E1054-APP | CG-ALL-3836 | 11, 13 | Record task.item_version (integer, added by migration V1054_1) as a task column in Fields. |
| CDC-06174 | RWB-P3-E1054-APP | CG-ALL-3837 | 17 | Record case_account.account_id as the account business key field in Fields. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05974 | RWB-P3-E1043-CON | CG-ALL-3747 | 11 | Remove the fixed enum on status; read LOV-VERSION-STATUS values as data, as RWB-P3-E1043-CON states. |
| CDC-05976 | RWB-P3-E1043-CON | DOR-RWB-P3-E1043-CON-8 | 11 | Remove the fixed enum on status; read LOV-VERSION-STATUS values as data, as RWB-P3-E1043-CON states. |
| CDC-06067 | RWB-P3-E1045-APP | CG-ALL-3757 | 13 | Remove the fixed enum on status so that LOV-CASE-STATUS values are read as data; the story already states they are data. |
| CDC-06081 | RWB-P3-E1050-APP | CG-ALL-3779 | 13 | Remove the closed enum on status so LOV-CASE-STATUS values are accepted as data, as the story states. |
| CDC-06115 | RWB-P3-E1052-APP | CG-ALL-3803 | 12.1 | Publish GET /api/recovery/case/v1/me/tasks (API-P3-008) through the case CON story. Story already lists it as provided; no story edit. |
| CDC-06116 | RWB-P3-E1052-APP | CG-ALL-3804 | 12.1 | Publish PATCH /api/recovery/case/v1/tasks/{taskId} (API-P3-009) through the case CON story. Story already lists it as provided; no story edit. |
| CDC-06117 | RWB-P3-E1052-APP | CG-ALL-3805 | 12.1 | Publish GET /api/recovery/case/v1/cases/{caseId} (API-P3-002) through the case CON story. Story already lists it as provided; no story edit. |
| CDC-06118 | RWB-P3-E1052-APP | CG-ALL-3806 | 12.1 | Publish GET /api/recovery/case/v1/cases/{caseId}/next-action (API-P3-016) through the case CON story. Story already lists it as provided; no story edit. |
| CDC-06128 | RWB-P3-E1052-APP | DOR-RWB-P3-E1052-APP-8 | 12.1 | Add the paths GET /me/tasks, PATCH /tasks/{taskId}, GET /cases/{caseId}, GET /cases/{caseId}/next-action and the other listed API-P3 paths. |
| CDC-06162 | RWB-P3-E1054-APP | CG-ALL-3838 | 3 | Remove the fixed enum on status so LOV-CASE-STATUS values load as data, as the story rule (BR9) requires; no story change. |
| CDC-06163 | RWB-P3-E1054-APP | CG-ALL-3839 | 3 | Remove the closed enum on status and validate status against LOV-TASK-STATUS from Reference Data v5 Lists, so new list values need no code change. |
| CDC-06171 | RWB-P3-E1054-APP | DOR-RWB-P3-E1054-APP-8 | 12.1 | Add an Idempotency-Key header to PATCH /tasks/{taskId}; hold task status as a reference value, not a closed enum; align the DecisionRecorded event type to rwb.decision.DecisionRecorded.v1 per Kafka Catalog v1. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05995 | RWB-P3-E1043-CON | GAP-1206 | 13 | Update the plan to the DP table: six H rows (RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) and three C rows (RWB-P3-E1042-CON, RWB-P3-E1043-CON, the rwb-case read contract). |
| CDC-06016 | RWB-P3-E1043-CON | GAP-2354 | Header | Record the platform CONs named in the Detail (RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) as wave-0 prerequisites; add RWB-P3-E1043-CON to the contract rows of DP-07 stories. |
| CDC-06023 | RWB-P3-E1043-CON | GAP-1291 | 13 | Record the DP-added H and C platform and published contracts as non-blocking, built against their fakes. Metadata rows stay as the plan gives them. DP-04 and DP-14 rows remain in section 13. |
| CDC-06024 | RWB-P3-E1043-CON | GAP-2317 | 13 | Add the four platform contracts (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) to H and RWB-P3-E1043-CON to C. Keep the Work Package metadata unchanged. |
| CDC-06037 | RWB-P3-E1043-CON | GAP-2335 | 13 | Section 13 states that C RWB-P3-E1018-CON and C RWB-P4-E1037-CON never block and are built against their published fakes from Day 1. The header's Contract dependencies stay None as the plan fixes them. |
| CDC-06046 | RWB-P3-E1043-CON | GAP-1885 |  | Carry the five consumed items as non-blocking rows; the approval contract as C of wave 2, case and partner contracts built against fakes. |
| CDC-06047 | RWB-P3-E1043-CON | GAP-2751 |  | Carry API-P5-002, API-P5-008 and API-P3-002 as non-blocking consumed rows and the reference read as C of RWB-P3-E1043-CON. |
| CDC-06048 | RWB-P3-E1043-CON | GAP-2801 |  | Carry the four appeal surfaces as consumed rows: approval as C of its wave, case and partner contracts on fakes, reference read as C of RWB-P3-E1043-CON. |
| CDC-06054 | RWB-P3-E1043-CON | GAP-1212 | none in this story | Add the eight DP-added platform and P3 rows to the dependency lists, or record the wave-0 baseline and fake-based reads per ASM-B-P6-05-E1063-3. |
| CDC-06055 | RWB-P3-E1043-CON | GAP-1335 | none in this story | Carry the six platform contracts and the two rwb-case contracts in the dependency map so sequencing is visible outside the metadata table. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06068 | RWB-P3-E1045-APP | CG-ALL-3763 | 13 | Rule the package segment for rwb-case that replaces the Java reserved word 'case' in th.co.scb.ace.workbench.recovery.case (and in th.co.scb.ace.workbench.recovery.case.refdata); line 371 names the reserved word today, and the story copies the ruled segment into section 13. |
| CDC-06069 | RWB-P3-E1045-APP | CG-ALL-3764 | 13 | Rule the package segment for rwb-case that replaces the Java reserved word 'case' in th.co.scb.ace.workbench.recovery.case.refdata; the story copies the ruled segment into section 13 beside the module name. |
| CDC-06083 | RWB-P3-E1050-APP | CG-ALL-3788 | 13 | The naming-rule row for P3 rwb-case (L371) needs the Java package segment the solution architect rules in place of the Java reserved word 'case'; RWB-P3-E1050-APP then copies the ruled package in section 13. |
| CDC-06084 | RWB-P3-E1050-APP | CG-ALL-3789 | 13 | The naming-rule row for P3 rwb-case (L371) needs the Java package segment the solution architect rules in place of the Java reserved word 'case', applied to the module package too; section 13 copies the ruled package. |
| CDC-06112 | RWB-P3-E1050-APP | CG-ALL-3790 Flyway file V1050_1__case_document_classification.sql is not in the V0001..Vnnnn form | 13 | Migration named without a number in the Vnnnn form; the number is not in the sources. |
| CDC-06122 | RWB-P3-E1052-APP | CG-ALL-3818 | 13 | Rule the package segment that replaces the Java reserved word `case` for service rwb-case under the §3.1 naming rule, so `th.co.scb.ace.workbench.recovery.<segment>` compiles. |
| CDC-06123 | RWB-P3-E1052-APP | CG-ALL-3819 | 13 | Apply the same ruled segment to the module package `th.co.scb.ace.workbench.recovery.<segment>.noticerequest` so §13 names a package that compiles. |
| CDC-06165 | RWB-P3-E1054-APP | CG-ALL-3848 | 13 | Rule and record the package segment for rwb-case that is not the Java reserved word 'case'; RWB-P3-E1054-APP §13 copies it |
| CDC-06166 | RWB-P3-E1054-APP | CG-ALL-3849 | 13 | The same ruled segment covers the reviewqueue sub-package th.co.scb.ace.workbench.recovery.case.reviewqueue; record it for the module too |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06075 | RWB-P3-E1045-APP | CG-ALL-3760 | 4, 12.5 | Add activity CalculateDueDate, task queue rwb-case, as named in RWB-P3-E1045-APP §4 and §12.5. |
| CDC-06096 | RWB-P3-E1050-APP | CG-ALL-3781 | 12.5 | Add activity ApplyClassification (type Activity, task queue rwb-case) to the Activities sheet. |
| CDC-06097 | RWB-P3-E1050-APP | CG-ALL-3782 | 12.5 | Add activity RaiseReviewTask (type Activity, task queue rwb-case) to the Activities sheet. |
| CDC-06121 | RWB-P3-E1052-APP | CG-ALL-3812 | 12.5 | Add a Workflows row for the workflow template 'Notify (workflow kit template)', task queue rwb-case, so the workflow of §12.5 and build step 7 is catalogued. |
| CDC-06135 | RWB-P3-E1052-APP | CG-ALL-3813 | 12.5 | Add activity RequestNotice on task queue rwb-case with the purpose given in the section 12.5 row |
| CDC-06175 | RWB-P3-E1054-APP | CG-ALL-3843 | 12.5 | Add activity RaiseReviewTask to the Activities sheet on task queue rwb-case, with the purpose given in section 12.5. |
| CDC-06176 | RWB-P3-E1054-APP | CG-ALL-3844 | 12.5 | Add activity RecordReviewOutcome to the Activities sheet on task queue rwb-case, with the purpose given in section 12.5. |

### RWB-P6-E1052-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06125 | RWB-P3-E1052-APP | DOR-RWB-P3-E1052-APP-21 | header | Publish the contract story; the story already names it as the contract dependency. |
| CDC-06126 | RWB-P3-E1052-APP | DOR-RWB-P3-E1052-APP-23 | header | State the contract version this story builds against; the header now shows the gap explicitly. |
| CDC-06139 | RWB-P3-E1052-APP | GAP-0357 | 12 | Publish the five admin template operations under /api/recovery/comms/v1/admin/templates in the registry, with the SCR-33 composite route and the P1 freshness source named. |
| CDC-06142 | RWB-P3-E1052-APP | GAP-0364 | 12 | Carry the notice path: POST /cases/{caseId}/notices on P6; ACE facts and stale-batch signal via the P1 data-product contract; PDF via P5; merge snapshot as references in P6; decision record local in P6 and central in P7 within five minutes. |
| CDC-06146 | RWB-P3-E1052-APP | GAP-1086 |  | Publish one error row per condition for API-P6-001: withdrawn-template hold as notice state Held, repeat with a different key as 409, missing field as 422. |
| CDC-06147 | RWB-P3-E1052-APP | GAP-2454 |  | Fix the generation-record payload in RWB-P6-E1052-CON and Service Contract Catalog v1: template code and version and merge snapshot reference in inputs_ref with ACE data date; notice reference and type in actions; hold reason or refusal message and freshness message in outcome; final-call set GENERATED, HELD, REFUSED as a reference list. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06051 | RWB-P3-E1043-CON | CG-ALL-3750 | 18 | Align the test lists for REQ-DRI-011 and the other differing requirements with section 18 of this story in the next RTM version. |
| CDC-06079 | RWB-P3-E1045-APP | CG-ALL-3762 | 18 | Align the REQ-DRI-010 and REQ-CWC-011 test lists with RWB-P3-E1045-APP section 18 in the next RTM version. |
| CDC-06111 | RWB-P3-E1050-APP | CG-ALL-3787 | 18 | Section 18 ranges extended to TC-E1-050-16. |
| CDC-06148 | RWB-P3-E1052-APP | CG-ALL-3817 |  | Align the REQ-OCC-001 test list with RWB-P3-E1052-APP §18 (TC-E1-052-01 to TC-E1-052-14) in the next RTM version. |
| CDC-06180 | RWB-P3-E1054-APP | CG-ALL-3846 | 18 | Align the REQ-DCM-005 test list with RWB-P3-E1054-APP section 18 at the next RTM version; the RTM currently lists tests of other stories. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05975 | RWB-P3-E1043-CON | DOR-RWB-P3-E1043-CON-14 |  | Record the signed epic design sign-off for RWB-P3-E1043-CON (Definition of Ready item 14) so the story can cite it. |
| CDC-06070 | RWB-P3-E1045-APP | DOR-RWB-P3-E1045-APP-14 |  | Record the signed epic design for RWB-P3-E1045-APP in the epic design record, so Definition of Ready item 14 Epic design passes. |
| CDC-06124 | RWB-P3-E1052-APP | DOR-RWB-P3-E1052-APP-14 | header | Record the signed epic design sign-off for RWB-P3-E1052-APP. |
| CDC-06167 | RWB-P3-E1054-APP | DOR-RWB-P3-E1054-APP-14 | header | Record the signed epic design sign-off for RWB-P3-E1054-APP. |

### RWB-P5-E1050-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05996 | RWB-P3-E1043-CON | GAP-1002 | 13 | Build the classifier as a service-internal capability behind ClassifierClient with a stub and a route property, no new dependency id. Confirm provider, endpoint and model version before SIT evaluation. Add the rwb-agent C row only if the satellite stays. |
| CDC-06104 | RWB-P3-E1050-APP | GAP-1002 | find it | Build the classifier as a service-internal capability behind ClassifierClient with a stub and a route property; confirm provider, endpoint and model version string before SIT; add the rwb-agent C row to the plan if the satellite stays. |
| CDC-06106 | RWB-P3-E1050-APP | GAP-0363 | find it | Run the classify step as a child run of rwb-agent; keep CLASSIFY_THRESHOLD, CLASSIFY_MAX_PAGES and CLASSIFY_TIMEOUT_SECONDS as data rows in document_hub_parameter; keep the 0.80 threshold, 90 percent target and type labels. |
| CDC-06107 | RWB-P3-E1050-APP | GAP-1004 | find it | Pin the classifier artefact by digest and promote or roll back it with its chart as one pair; gate on the 162 of 180 report; set alert shares, windows, replica counts, KEDA thresholds, probe timings and report container as values entries at SIT entry. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06050 | RWB-P3-E1043-CON | CG-ALL-3749 | 16 | Add rows TC-P3-E1043-CON-01 to TC-P3-E1043-CON-07 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-06110 | RWB-P3-E1050-APP | CG-ALL-3786 Test cases cover other criteria in Test Cases v8 | 16 | Section 7 holds AC1 to AC11 only; the workbook rows cover other criteria than the story's and need their next version. |
| CDC-06136 | RWB-P3-E1052-APP | CG-ALL-3815 | 16 | Add a Story test cases row for TC-E1-052-11 with Given, When and Then from AC4 and BR6 |
| CDC-06137 | RWB-P3-E1052-APP | DOR-RWB-P3-E1052-APP-12 | 16 | Add TC-E1-052-11 (missing today) and story cases TC-E1-052-12 to TC-E1-052-14 with Given, When and Then; align the RWB-P3-E1052-APP test lists in RTM v7 to section 18. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06119 | RWB-P3-E1052-APP | CG-ALL-3807 | 12.2 | Publish POST /api/recovery/comms/v1/cases/{caseId}/notices (API-P6-001) in rwb-comms.yaml through the provider CON story, as accepted in Architecture v5 slide 17. |
| CDC-06120 | RWB-P3-E1052-APP | CG-ALL-3808 | 12.2 | Publish GET /api/recovery/comms/v1/notices/{noticeId} (API-P6-002) in rwb-comms.yaml through the provider CON story, matching the Notice resource of RWB-P6-E1052-CON. |
| CDC-20674 | RWB-P3-E1052-APP | R-00782 |  | POST /cases/{caseId}/notices (API-P6-001) is already published in rwb-comms.yaml (paths, line 44). |
| CDC-20675 | RWB-P3-E1052-APP | R-00783 |  | GET /notices/{noticeId} (API-P6-002) is already published in rwb-comms.yaml (line 88). |

### RWB-P5-E1054-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06168 | RWB-P3-E1054-APP | DOR-RWB-P3-E1054-APP-21 | header | Publish the contract so RWB-P3-E1054-APP can cite it as published. The header already names RWB-P5-E1054-CON as the contract dependency. |
| CDC-06169 | RWB-P3-E1054-APP | DOR-RWB-P3-E1054-APP-22 | header | Record the published contract fake library version for the contract the story builds against. |
| CDC-06177 | RWB-P3-E1054-APP | GAP-1010 | 8 | Read the four review rows from document_hub_parameter in rwb_document; publish the by-number case read on RWB-P3-E1035-CON; take role, team and scope from the cached permission decision until a P4 CON row is added; fix field-level names and the three platform message texts before wave 1 entry check. |
| CDC-06179 | RWB-P3-E1054-APP | GAP-0365 | 12 | Keep queue, resolve, field-review and document-review operations under /api/recovery/document/v1; read case status via P3 and scope via P4; prove attach, the DOCATT record and the labeled example end to end. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06038 | RWB-P3-E1043-CON | GAP-1558 | Not in chunk | Realign the x-module of the five list and reference-load paths, including GET /admin/lists/{listCode} and POST /admin/reference-loads, to P3. |
| CDC-06145 | RWB-P3-E1052-APP | GAP-1082 |  | Publish NoticeRequest and Notice schemas with required flags and the NoticeGenerated payload element list, and confirm them with the app stories of this key. |
| CDC-06181 | RWB-P3-E1054-APP | GAP-0988 |  | Publish the review-item authorise request and answer schema; record matrix and masking version labels with valid-from dates and environment; list masking review-field IDs with the pack version. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06039 | RWB-P3-E1043-CON | GAP-0217 | Not in chunk | Keep all 25 LOV-REF-TABLE values unchanged in v5. The rwb-case contract names its twelve codes as a subset of the same list. No value is removed. |
| CDC-06109 | RWB-P3-E1050-APP | GAP-1007 | find it | Add EXTRACTION_FAILED to LOV-INTAKE-REVIEW in the next approved list load; keep MODEL_UNAVAILABLE for the classification fallback; change no code. |
| CDC-06156 | RWB-P3-E1052-APP | GAP-1087 | header | Add LOV-HOLD-REASON carrying POSTAL_ADDRESS and TEMPLATE_WITHDRAWN and any later value; read it through the reference-data contract. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06056 | RWB-P3-E1043-CON | GAP-2690 | 1 | Record the treatment resource operations and credit-result element set against rwb-treatment, the level comparison and delegation version against rwb-access, the ledger entry and sealing order against rwb-decision, and the SCR-14 merge against the edge contract. |
| CDC-06159 | RWB-P3-E1052-APP | GAP-1083 | 8 | Record that the Litigation right and scope test of the notice operations are enforced at the edge under RWB-PLT-N001-CON. DP-08 and RWB-P4-E1037-CON not added, as enforcement stays at the edge. |
| CDC-06160 | RWB-P3-E1052-APP | GAP-2455 | 12.7 | Confirm rwb-decision appends every DecisionRecorded fact to decision_log_entry; producer local record is working record and ledger entry is record of record; RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0 and wave-1 baseline outside the H row. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06078 | RWB-P3-E1045-APP | GAP-0760 | find it | Default to NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL. Service-level owner (RW-COE) confirms before the first SERVICE_LEVEL load. ON_HOLD and CLOSED stay out unless added. |
| CDC-06113 | RWB-P3-E1050-APP | GAP-0766 | find it | Add one boolean key for the rwb-case classification switch, value agreed with RW-COE. The daily re-drive time is a schedule value, not a parameter key. |
| CDC-06155 | RWB-P3-E1052-APP | GAP-0753 | header | Add the login name for the rwb-case service identity; add the case-side notice-request switch key with default on, owner RW-COE. Key name: Not specified in the source documents (GAP-0753). |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06098 | RWB-P3-E1050-APP | CG-ALL-3784 | 4, 14 | Business analyst adds a new message ID for a task write with a task version other than the one in force; the story then cites it in §14. |
| CDC-06099 | RWB-P3-E1050-APP | CG-ALL-3785 | 4, 14 | Business analyst adds a new message ID for rwb-document not answering inside the 2 s budget; the story then cites it in §14. |
| CDC-06138 | RWB-P3-E1052-APP | DOR-RWB-P3-E1052-APP-9 | 14 | Confirm the MSG-P1-001 text against the standard; the story keeps the legacy text until then. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05978 | RWB-P3-E1043-CON | DOR-RWB-P3-E1043-CON-12 | 12.7, 16, 18 | Add rows for TC-P3-E1043-CON-01 to -08 as section 16 defines them, and align the test lists with RTM v7. |
| CDC-06076 | RWB-P3-E1045-APP | DOR-RWB-P3-E1045-APP-12 | 12, 12.7, 16, 18 | Story §16 now has 15 test cases, including contract and boundary tests; the workbook and RTM must match. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05992 | RWB-P3-E1043-CON | GAP-0779 | n/a | Publish /masking-policies with Reference data R; publish AccessPolicyChanged with change kind, version and effective date and no personal value; settle the owner of reference-load paths between P3 and P4. |
| CDC-06108 | RWB-P3-E1050-APP | GAP-2133 | find it | Seed valuation inputs in rwb_source_data (valuation_ext) and the RouteDecided outcome as a decision record in rwb_decision; the valuation schema holds only platform library objects until a technical specification adds a table. |

### RWB-S4-E2025-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06020 | RWB-P3-E1043-CON | GAP-1903 | n/a | Fix the fill trigger as the document type in the request for create and patch; derive the write key from action, type, versions and values; make one hearing per action and date a uniqueness rule in rwb_litigation; take parameter and list calls from RWB-P3-E1042-CON and RWB-P3-E1043-CON. |
| CDC-06021 | RWB-P3-E1043-CON | GAP-1898 | n/a | Keep the plan lists; keep Day 1 with RWB-P5-E2025-CON as the sole contract dependency; build against the five fakes; remove DP-09 and DP-10 from the story's pattern list. |

### OTHER:Reference data starter workbook (v5) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06040 | RWB-P3-E1043-CON | GAP-0219 | 13 | Add rows for S1 rwb-valuation and S7 rwb-writeoff at the next revision, naming the lists each service reads. |
| CDC-06041 | RWB-P3-E1043-CON | GAP-0220 | 13 | Keep the derivation rule stated on the sheet; service stories confirm their starter rows at design review. |

### RWB-P10-TE013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06062 | RWB-P3-E1043-CON | GAP-1319 | 13 | Carry the seven platform H rows, three published C rows and the P4 authorise answer in its dependency map as DP-added; keep Ready to start Day 1. |
| CDC-06102 | RWB-P3-E1050-APP | GAP-1005 | find it | Name the extractor provider, model, model version and field-extraction route for extraction_method MODEL; keep the route a property of rwb-document with no model name in code. |

### OTHER:P3 screen specification for SCR-39; OTHER:SCR-40 and SCR-42 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05977 | RWB-P3-E1043-CON | DOR-RWB-P3-E1043-CON-10 |  | Add empty, loading, error and no-access states for SCR-39, SCR-40 and SCR-42. |

### OTHER:P2 story carrying MSG-P3-027 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05979 | RWB-P3-E1043-CON | DOR-RWB-P3-E1043-CON-9 | 14 | Align the MSG-P3-027 text in the P2 story with Error and Message Standard v4. |

### RWB-P6-E1011-APP; API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05980 | RWB-P3-E1043-CON | GAP-1168 | 13 | Add RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-source-data contract to the C list of RWB-P6-E1011-APP; add the reference-data read GET /api/recovery/case/v1/admin/lists/{listCode} to the API Specification and Ownership Map. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05981 | RWB-P3-E1043-CON | GAP-1946 |  | Apply the proposed fix: keep H and C at None, record the nine platform and rwb-case CONs as wave-0 prerequisites and fakes, serve the ACE check and quality facts from the rwb-source-data DP06 product and the quality endpoints. |

### RWB-P9-E1013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05982 | RWB-P3-E1043-CON | GAP-2567 |  | Keep the metadata rows as stated; declare the payments and freshness rows and the two rwb-case rows as class C in 12.2 with fakes; add the two rwb-source-data rows to the wave dependency map. |

### OTHER:Recovery Workbench P9 rwb-reporting contract for measure_definition (RWB-E1-013 reference-load element) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05983 | RWB-P3-E1043-CON | GAP-2568 | n/a | Declare the reference-load element of measure_definition on the rwb-reporting base with its path and right; keep list values on the rwb-case reference-data contract; rwb-case owner confirms framework or service load. |

### RWB-P6-E1019-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05984 | RWB-P3-E1043-CON | GAP-1174 | n/a | Add H RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and C RWB-P3-E1042-CON, RWB-P3-E1043-CON to its dependency rows, or record them in the platform release train. |

### RWB-S8-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05985 | RWB-P3-E1043-CON | GAP-3075 | n/a | Reissue the plan row with the eight H and two C rows from the DP table, or let the assembler correct the metadata; platform owner confirms which platform contracts publish before release. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05986 | RWB-P3-E1043-CON | GAP-2404 | n/a | Read H as None plus the five platform contracts named by the DP table; read C as RWB-P10-E2032-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and the published P4 authorise contract. |

### RWB-P5-E1032-CON; OTHER:IntakeItemPage; OTHER:IntakeAttachRequest, not-found answer) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05987 | RWB-P3-E1043-CON | GAP-0992 | n/a | Fix the four shapes as the smallest superset of the legacy list, declare the consumed rwb-case reads with fakes, and keep unnamed elements behind the placeholder until owner documents confirm them. |

### RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05988 | RWB-P3-E1043-CON | GAP-2448 | n/a | Keep metadata rows as fixed by the work package; record the DP-table dependencies in section 13, built against fakes on Day 1. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05989 | RWB-P3-E1043-CON | GAP-1198 | n/a | Add the seven platform H contracts and the two P3 C contracts from the DP table to its dependency rows, or record them in the platform release train. |

### OTHER:Template screen story of the service carrying the reference lists (plan key and contract rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05990 | RWB-P3-E1043-CON | GAP-1147 | n/a | Add DP07 to its pattern set with H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON at the next plan revision; read the four lists through the rwb-case reference-data contract. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05991 | RWB-P3-E1043-CON | GAP-2414 | n/a | Read H as None plus the eight platform contracts from the DP table; read C as RWB-P3-E2041-CON plus RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05993 | RWB-P3-E1043-CON | GAP-1023 | 13 | Use POST /cases/{caseId}/generated-documents on /api/recovery/document/v1 as the operation (API-P5-016, ASM-101). Read template version and merge fields only through RWB-P6-E1046-CON (ASM-102). Add template_code and template_version to document with the partial unique index (ASM-103). |

### OTHER:Work Package plan; RWB-P6-E1046-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05994 | RWB-P3-E1043-CON | GAP-1064 | 13 | Add the rwb-source-data data-dictionary contract story to the C list of RWB-P6-E1046-APP, or confirm the published source-data admin surface covers GET /admin/data-dictionary/fields. |

### RWB-P5-E1054-CON; RWB-P5-E1024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05997 | RWB-P3-E1043-CON | GAP-1010 | 13 | Read the four review rows from document_hub_parameter. Publish the by-number case read on RWB-P3-E1035-CON. Take role, team and scope from the cached permission decision until a P4 CON row is added. RWB-P5-E1054-CON fixes field names and message texts. |

### RWB-P5-E1057-CON; RWB-P5-E1057-INF; RWB-P5-E1057-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05998 | RWB-P3-E1043-CON | GAP-1012 | 13 | Publish the three admin operations and the run record in RWB-P5-E1057-CON. Carry channel properties as environment values in -INF and -OPS. Consume the partner read via the rwb-partner contract with a fake and no C row. Schedule owner confirms the window, overlap and catch-up before wave 1. |

### OTHER:RWB-P4 FSD and TSD (REQ-ACA-006; OTHER:NFR-042) and the plan H and C rows of the key named in the item (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05999 | RWB-P3-E1043-CON | GAP-2333 | 13 | Keep the Reporting R check in the route and Rules and parameters R at the metric owner. Record Reporting letters in the matrix load. Correct REQ-ACA-006 and NFR-042 in the next FSD and TSD. Add five platform contracts to H and two rwb-case contracts to C. |

### RWB-P1-E1065-CON; RWB-S8-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06000 | RWB-P3-E1043-CON | GAP-3086 | 13 | Publish a deviation seed profile in RWB-P1-E1065-CON with case references, shapes and routed states. Publish deviation counts per case and the shape-to-code mapping. Name the stage contract read operations and fields. Publish codes and owner roles of R-DEV-05 and R-DEV-06. Keep the S8 H row empty. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06001 | RWB-P3-E1043-CON | GAP-1328 | 13 | Either complete the metadata rows from the DP table (eight H rows, the C rows of DP-04, DP-06 and DP-07, and DP-09 in the pattern list) or state in R5.5 that platform H and self-referential C rows are held by the platform and contract stories. |

### OTHER:Work Package plan line of the account-grouping story (legacy RWB-E2-001) and its dependency list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06002 | RWB-P3-E1043-CON | GAP-0593 | 13 | Read the product group map through the client library of RWB-PLT-E1043-CON with contract C RWB-P3-E1043-CON, added at the next plan revision. Until then no group is guessed and an unmapped code is answered as unresolved. |

### RWB-P7-E2002-APP; OTHER:Template and Rules v1 R5.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06003 | RWB-P3-E1043-CON | GAP-2470 | 13 | Complete the metadata rows of RWB-P7-E2002-APP from the DP table, or state in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories and not repeated on the APP line. |

### RWB-P8-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06004 | RWB-P3-E1043-CON | GAP-1346 | 12 | Name the seven consumed operations in section 12.2 with placeholders until each owner publishes; confirm the scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON with the solution architect. |

### RWB-P7-E2004-APP; OTHER:Template and Rules v1 R5.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06005 | RWB-P3-E1043-CON | GAP-2475 | 13 | State in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories, or complete the RWB-P7-E2004-APP metadata rows from the DP table. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; RWB-P7-E2006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06006 | RWB-P3-E1043-CON | GAP-1343 | 13 | Publish the six DP-added dependencies with RWB-P7-E2006-APP as consumer; optionally add C row RWB-P4-E1037-CON to that story object in the next run. |

### RWB-P1-E2008-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06007 | RWB-P3-E1043-CON | GAP-0604 | 12 | Add RWB-P3-E1043-CON to the contract dependencies of RWB-P1-E2008-APP at the wave 2 freeze and serve the data product and source-system lists from rwb-case reference data, or record the ownership ruling and drop the dependency. |

### RWB-P1-E2010-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06008 | RWB-P3-E1043-CON | GAP-0509 | 13 | Add the guarantee claim read as a C dependency with its fake, returning no claim until S3 is built, and take the case-existence answer from the rwb-case case contract, faked the same way. |

### RWB-P3-E2012-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06009 | RWB-P3-E1043-CON | GAP-2501 | 13 | Keep the metadata rows as given and record the DP-added H and C contracts in the Dependency Map as non-blocking platform and published contracts built against fakes. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06010 | RWB-P3-E1043-CON | GAP-1223 | 13 | Read the H list as None plus the platform contracts named in the DP table, and the C list as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON; story stays Day 1. |

### RWB-P7-E2014-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06011 | RWB-P3-E1043-CON | GAP-2216 | 12 | Fix the case-facts projection with inputAsOf on API-P3-002, the refusal and return events on rwb.decision.events.v1, the task code with its reference row, and the dated contact read on rwb-source-data. |

### RWB-S4-E5001-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD S4 v2; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06012 | RWB-P3-E1043-CON | GAP-2743 | 13 | Record the two consumed rows as C dependencies with placeholders; declare notice and template ownership in the Ownership Map; name the P6 operations; add REQ-S4-001 to the trace; decide the D7.1 gate in the EP05 PRD. |

### RWB-P7-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06013 | RWB-P3-E1043-CON | GAP-1265 | n/a | Add C rows RWB-P1-E1015-CON and RWB-P3-E1018-CON to the Contract dependencies of RWB-P7-E2014-APP, or record both reads as route-level composites of RWB-PLT-N001-CON. |

### OTHER:TSD P6 v2 (T-A.2; RWB-P6-E1046-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06014 | RWB-P3-E1043-CON | GAP-2392 | n/a | Add treatment-type and product-group filters to API-P6-003; add an application/json representation of API-P6-005 as an additive change in major version 1; add the locked attribute to merge_field; publish the set rows as rwb-case reference data under RWB-P3-E1043-CON. |

### OTHER:Work Package plan (rwb-treatment contract story, wave 2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06015 | RWB-P3-E1043-CON | GAP-1183 | 12.8 | Add an rwb-treatment contract story to the plan that publishes the signature record operation and its field names; consume it on /api/recovery/treatment/v1 with the PATCH until published. |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06017 | RWB-P3-E1043-CON | GAP-1070 | n/a | Name the contact-point read, consent and verified fields, failed-count update, and ledger record and delivery-update operations, or add a P1 ledger contract to the rwb-comms key's Contract dependencies. |

### OTHER:rwb-comms story carrying SCR-03 (metadata key) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06018 | RWB-P3-E1043-CON | GAP-1075 | n/a | Declare Case record right C on the gateway-bff composite route to SCR-03, answer MSG-P4-002 and MSG-P4-003 there, keep a local refuse-closed guard, and record the T6.1 Case record area reconciliation. |

### RWB-P5-E1025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06019 | RWB-P3-E1043-CON | GAP-1020 | n/a | Publish the checked-fields read on /api/recovery/document/v1/cases/{caseId}/checked-fields with CheckedField and CheckedFieldSet shapes; apply the DOCTYPE-2026.12 load through the type table; keep EXTRACT_ACCURACY_PASS in document_hub_parameter. |

### OTHER:RWB-B2-P8-002 payment-matching story (rwb-payment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06022 | RWB-P3-E1043-CON | GAP-2506 | n/a | Add C RWB-P7-E1073-CON to the DP-04 contract rows; publish row order as the ordering column name with priority as its legacy name; reconcile PMT-2026.12 to one version row; declare DecisionRecorded read only. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06025 | RWB-P3-E1043-CON | GAP-2412 | 13 | Publish the placement fact element names, the P3 case-read and P4 authorise shapes, the reference-data operation, MSG-P7-009 text and the login name; carry the two C and seven H rows in the Dependency Map. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06026 | RWB-P3-E1043-CON | GAP-2654 | 13 | No story edit; DP-05 left as it was |

### OTHER:TSD S2 (T5.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06027 | RWB-P3-E1043-CON | GAP-2652 | 13 | Correct T5.2 so reference data is read from P3 rwb-case through RWB-P3-E1043-CON. Publish set identifiers, the four values and the freshness limit before wave 2 tag. |

### RWB-S9-E6029-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06028 | RWB-P3-E1043-CON | GAP-3107 |  | Baseline the onboarding write method, path and request element, publish partner_user field catalogue, name the reference-data operation, add RWB-P3-E1043-CON to C, bind 409 to a message ID and publish EV-20 and EV-21 names. |

### RWB-S9-E6029-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06029 | RWB-P3-E1043-CON | GAP-3106 |  | Publish the onboarding write in the rwb-partner contract, add partner_user to the TSD field catalogue, add C RWB-P3-E1043-CON and RWB-PLT-TE006-CON rows, and bind the 409 to a message ID. |

### RWB-S9-E6030-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06030 | RWB-P3-E1043-CON | GAP-3109 |  | Publish the fragment as a tagged addendum with the two reads and the consumed RWB-P3-E1043-CON row. Publish no write operation, bind each status to a message ID, and raise partner_user and version column in next revision. |

### OTHER:Work Package B2-P7-007 story line (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06031 | RWB-P3-E1043-CON | GAP-2419 | 13 | Treat seven platform contracts and RWB-P3-E1043-CON as wave 0 contract fakes, treat the authorise answer as the platform guard, and replace the agent fake with RWB-P10-TE013-CON when it lands. |

### RWB-P4-AD013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06032 | RWB-P3-E1043-CON | GAP-0844 | Not in chunk | Publish the P7 rule-package rollback contract and its fake, and add the missing C dependency for it to the metadata at D1. The rule arm is built against that contract. |

### RWB-P4-E8008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06033 | RWB-P3-E1043-CON | GAP-0869 | Not in chunk | Fix the two paths on /api/recovery/access/v1/doa-limits/{delegationLimitId}, the field set, the state set PENDING_APPROVAL, IN_FORCE and SUPERSEDED, and the message ID MSG-P7-002. |

### RWB-P4-E8010-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06034 | RWB-P3-E1043-CON | GAP-0871 | Not in chunk | Publish the template-approval paths on /api/recovery/access/v1/admin/template-approvals and the request and answer field set. Add the P6 template contract dependency at D1. |

### RWB-P5-E1041-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06035 | RWB-P3-E1043-CON | GAP-0995 | Not in chunk | Publish the eight scan and retention operations with paths, query parameters, field sets and statuses on /api/recovery/document/v1 before the wave-1 harness. Add the P3 case contract C row, or state the hold read is faked by ruling. |

### OTHER:rwb-document, rwb-comms, rwb-case and rwb-decision contracts (wave 3 freeze) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06036 | RWB-P3-E1043-CON | GAP-2765 | Not in chunk | Publish the pack and defect-list read, the notice and template-status read, the case read with task raise and route fact, and the D7 approval raise. Also add the reference-data read of RWB-P3-E1043-CON to the freeze. |

### OTHER:Platform library baseline (RWB-PLT-TPL) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06042 | RWB-P3-E1043-CON | GAP-1409 | 11 | Story side: the cache time to live stays the catalog entry at 300, assumed under the open decision DL11; refresh on expiry only because no change event is published. Coordinates sit in RWB-PLT-TPL. |

### OTHER:Platform reference-data client contract artefact (RWB-PLT) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06043 | RWB-P3-E1043-CON | GAP-1410 | 12 | Publish client surface v1, version and row projection, the twelve LOV-REF-TABLE codes and MSG-P3-027 as a checked exception. |

### RWB-P1-DM014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06044 | RWB-P3-E1043-CON | GAP-0544 |  | P1 hands versions, rows and LOVs to rwb-case via the published contract; rule rows go to rwb-decision; P1 writes no reference row. |

### OTHER:TSD P5 Document hub v2 (appendix T-A) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06045 | RWB-P3-E1043-CON | GAP-2337 | 12 | Add one batch missing-count operation or query parameter for up to 500 cases; name the case read and DOCUMENT_CHECKLIST reference-load operation. |

### RWB-S6-E5025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06049 | RWB-P3-E1043-CON | GAP-3014 | none in this story | Keep the H, C, I and X rows as stated; read the masking rule set and tape spec as versioned reference data; record the PII service as an unmapped component; state missing values as not specified. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:12.2; OTHER:12.8; OTHER:13) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06052 | RWB-P3-E1043-CON | GAP-2429 | 3, 12.2, 12.8, 13 | Keep the metadata rows as the Work Package fixes them; name the added H and C rows in the pattern table and the fakes of 12.8. |

### OTHER:rwb-case reference tables (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06053 | RWB-P3-E1043-CON | GAP-0746 | none in this story | Hold the case review task code, element type and task status values as reference data and load them with RWB-P3-E1043-CON before the review queue story starts. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06057 | RWB-P3-E1043-CON | GAP-2389 | 13 | At the next plan revision, add the six platform contracts and the two rwb-case contracts to the C list of slice RWB-P6-E2014-APP. Keep the H list empty. |

### OTHER:Work Package (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06058 | RWB-P3-E1043-CON | GAP-2410 | 13 | Record in the build sequence that the secondary slice builds against platform contracts and published fakes and reads wave-1 rows through its own schema. |

### OTHER:RWB-E2-041 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06059 | RWB-P3-E1043-CON | GAP-0719 | 1 | Record the rule-package scope for RWB-E2-041. The reference-data checklist and its report stay with RWB-E1-043. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06060 | RWB-P3-E1043-CON | GAP-1296 | 13 | Keep its metadata as written and carry the eight platform H and three published C DP-added rows in its dependency map as build-against items. |

### RWB-P3-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06061 | RWB-P3-E1043-CON | GAP-2398 | 13 | Carry the eleven DP-added rows in its section 13 and section 18 and leave the metadata rows as the Work Package fixes them. |

### OTHER:source holding section 3 (model version in force) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06063 | RWB-P3-E1043-CON | GAP-0081 | 3 | Name rwb-case (P3) as owner of the model version in force and the champion and challenger shares, reached through RWB-P3-E1043-CON. Keep the rule package registry with P7. Table name stays the R9 placeholder. |

### OTHER:Lists sheet of the Recovery Workbench (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06064 | RWB-P3-E1043-CON | GAP-0221 | 1 | Keep every list row and its Source cell. Record the holding service in the new Owning service (D-RCV-60) and Owning schema (D-RCV-60) columns, and state the serving contract in the route column. |

### OTHER:Reference tables workbook; OTHER:Reference tables sheet rows 11; OTHER:13; OTHER:14; OTHER:15 and 16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06065 | RWB-P3-E1043-CON | GAP-0223 |  | Record the owner of each of the five 'Reference table' rows from its Ownership Map item; name reference_row as the carrier of the message catalogue; leave the Table cells unchanged. |

### OTHER:Work Package plan: wp/B-P4-04.md and wp/B2-P4-010.md (plus split_plan.json and checks/run_all.py) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06066 | RWB-P3-E1043-CON | GAP-2278 |  | Keep one Work Package owner for RWB-AD-016 and number its CG and ASM rows once; add a plan-uniqueness check on Write only paths. |

### RWB-PLT-E1027-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-E1047-CON; RWB-PLT-E1072-CON; RWB-PLT-N001-CON; RWB-P3-E1042-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06071 | RWB-P3-E1045-APP | DOR-RWB-P3-E1045-APP-21 | Item table | Each CON story in Depends on (build) reaches Done and publishes its contract, so Definition of Ready item 21 Contract published passes; this story's own contract dependencies stay None. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06072 | RWB-P3-E1045-APP | DOR-RWB-P3-E1045-APP-22 | Item table, 12.8 | Publish the contract fake library version of the parameters and reference-data contracts of rwb-case, so the `Contract fake library version` row can name it; the row keeps its Not specified placeholder until then. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06074 | RWB-P3-E1045-APP | DOR-RWB-P3-E1045-APP-8 | 4, 12.5 | rwb-case.yaml: hold status as a reference to LOV-CASE-STATUS, not a closed enum. Temporal Catalog v1: add activity CalculateDueDate (CG-ALL-3760). |

### OTHER:TSD P1 v3, rwb-source-data contract (P1 contract owner; OTHER:TechX) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06077 | RWB-P3-E1045-APP | GAP-0759 | find it | Publish one holiday calendar read (Temporal activity or GET on the source-data base path) returning the holiday dates of a date range. rwb-case consumes it in CalculateDueDate and reads no ACE view. |

### OTHER:Recovery Workbench reference-data workbook; OTHER:Reference tables sheet rows 11; OTHER:13; OTHER:14; OTHER:15; OTHER:16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06080 | RWB-P3-E1045-APP | GAP-0223 | find it | Record the owner of each of the five rows from the Ownership Map item behind it. Name reference_row in rwb_case as the versioned carrier of the message catalogue. Leave the Table cells of v4 unchanged. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06082 | RWB-P3-E1050-APP | CG-ALL-3783 | 12.5 | Add a row for workflow RedriveClassificationLinks (task queue rwb-case, started by the daily Schedule), or confirm the catalogued name. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities and Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06085 | RWB-P3-E1050-APP | DOR-RWB-P3-E1050-APP-8 | header | Add rows for ApplyClassification and RaiseReviewTask (task queue rwb-case); confirm a single CaseWorkflow workflow ID form. |

### OTHER:Message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06101 | RWB-P3-E1050-APP | DOR-RWB-P3-E1050-APP-9 | 14 | Realign the meanings of MSG-GEN-004 (a task write with a stale task version, 409) and MSG-GEN-006 (a dependency that does not answer) with the standard message catalogue. |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06105 | RWB-P3-E1050-APP | GAP-1003 | find it | Declare the classify and classification operations on the service base after architect confirmation; settle resource field names; add DocumentClassified.v1 to the event catalogue and amend the event count and AC8. |

### RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06140 | RWB-P3-E1052-APP | GAP-1085 | 13 | Publish the rwb-case task-raise operation (or the event that creates a task) and record it in the ownership map. |

### OTHER:TSD P6 v2 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06141 | RWB-P3-E1052-APP | GAP-1084 | 11 | Give the party reference its own field ID and keep person_key as the notice business key of DF-LEG-030, or correct the legacy field list. |

### OTHER:Data dictionary (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06143 | RWB-P3-E1052-APP | GAP-0749 | 13 | Assign field IDs to the seven notice columns of recovery_case; the columns, indexes and LOV-LEDGER-EVENT notice codes are already in this story. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06144 | RWB-P3-E1052-APP | GAP-1081 |  | Name the merge snapshot store (a snapshot table or a column on the local decision record) and publish it in the next physical-schema version. |

### API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06149 | RWB-P3-E1052-APP | GAP-2094 | find it | Settle the path of the case-level notice list as a P6 operation and add it to the Endpoints sheet; until then the story reads per notice via GET /notices/{noticeId}. |

### RWB-P1-E1015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06150 | RWB-P3-E1052-APP | GAP-1080 | find it | Publish the data-product record shape of DP01 Account and arrears and DP07 Legal, naming each returned field and its source column. |

### RWB-P5-E2026-CON; OTHER:RWB-PLT-DB; OTHER:P5 document type load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06151 | RWB-P3-E1052-APP | GAP-2348 | find it | Publish request and reason fields, answer shape, rwb-document login names, container name, index, migration step, feature flag and MSG-P5-006 text. |

### OTHER:Recovery Workbench Notification and Correspondence Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06152 | RWB-P3-E1052-APP | GAP-2087 | find it | Adopt version 3 from the file name; add a Source version row (1, 28 October 2026) and log both readings in the change log. |

### OTHER:TSD P3 v3 T3.1 and T3.2 (case model task rows through reference-data contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06153 | RWB-P3-E1052-APP | GAP-0751 | 8 | Load request task code, Complete notice data task code, element type HUMAN_TASK, discretion REQUIRED and task status values as case model rows via reference-data contract. Story BR3 now states the held-answer creation and dedupe rule. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:P6 column) and slide 17 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06154 | RWB-P3-E1052-APP | GAP-0752 | header | Record P3 as a consumer of P6 (E cell) for the REST notice request made from a CaseWorkflow activity, one hop, as the story already states. |

### OTHER:AsyncAPI document of rwb-comms (NoticeGenerated schema) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06157 | RWB-P3-E1052-APP | GAP-1088 | 12 | Publish NoticeGenerated with noticeId, caseId, templateId, templateVersion, noticeType and generatedAt; confirm with rwb-decision and rwb-reporting consumers. |

### RWB-P5-E1052-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06158 | RWB-P3-E1052-APP | GAP-2349 | 16 | Record one owning story per legacy criterion and mark this slice as test-case-bearing but criterion-free so traceability reports do not expect matching lists. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06164 | RWB-P3-E1054-APP | CG-ALL-3842 | 12.5 | Add the Workflows row for the workflow kit template Human task with SLA (RWB-PLT-E1071-CON) that RWB-P3-E1054-APP §12.5 names, with task queue rwb-case |

### OTHER:rwb-document OpenAPI and AsyncAPI documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06178 | RWB-P3-E1054-APP | GAP-1011 | 12 | Freeze seven operations, nine resources, five value sets, the IntakeResolution envelope, the If-Match lock with idempotent repeat, the declared document read reference and the event schema; keep the three message texts and the by-number path as recorded placeholders. |

### OTHER:FSD P5 v3 (AC-P5-010-01; OTHER:AC-P5-011-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06182 | RWB-P3-E1054-APP | GAP-1593 |  | Add one distinct criterion for the correction feed; the PRD reads A2.10 and A2.11 as one behaviour delivered by CAP-P5-010, FR-P5-017 and FR-P5-018. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06183 | RWB-P3-E1054-APP | GAP-0758 |  | Login name is not in the source documents; agreed with the platform DB story, no name invented here. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_case.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20560 | RWB-P3-E1043-CON | R-28560 |  | Task code and status values are not in the sources. Task columns exist at rwb_case.sql 220-238, but no reference values are added. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20712 | RWB-P3-E1052-APP | R-28613 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21918', 'R-22054', 'R-22286', 'R-22289', 'R-22316', 'R-28613'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0081 | Owner and table of the model version in force are not stated | ACE | Resolved (directive) |
| GAP-0217 | LOV-REF-TABLE carries 25 table codes in v4 but the rwb-case reference-data contract fixes twelve | Reference data administrator | Resolved (directive) |
| GAP-0219 | Two services derive no starter row: S1 rwb-valuation and S7 rwb-writeoff | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0220 | No source states which lists a service needs at its first deployment | Data architecture team | Resolved (directive) |
| GAP-0221 | Four source lists are held in another service's table although the sheet calls every list Workbench-held | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0223 | Five reference-data rows name no table, and no message table exists in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0363 | Classifier route, parameter home and agent run evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0364 | Cross-service notice path, merge snapshot home and stale-batch signal are not named for the target | Tech lead | Resolved (directive) |
| GAP-0365 | Review queue operation names, scope source and attach evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0509 | The guarantee claim read of rwb-guarantee and the case-existence answer are not in the Work Package's contract list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0544 | The reference versions, their rows and the lists of values are P3's, the rule rows and their test cases are P7's, and the legacy story names a reference data service that exists in no source | Solution architect | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0696 | Legacy AC2 and BR1 load DELEGATION_LIMIT through the reference-data service, but the Ownership Map keeps delegation_limit with P4 rwb-access | Solution architect | Resolved (directive) |
| GAP-0697 | The column definitions of each reference table code and the element types of the reference resources have no source field by field | Data steward | Resolved (directive) |
| GAP-0698 | The answer of a dated read with no version in force, and the rights of the verify and the rollback, are not stated | Solution architect | Resolved (directive) |
| GAP-0719 | FSD A2.16 reports reference-data changes while the legacy story and the test cases govern rule package versions | Business analyst | Resolved (directive) |
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
| GAP-0759 | The holiday calendar read on the rwb-source-data contract has no named operation | P1 contract owner (TechX) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0760 | The required service-level status list is not in the target sources | RW-COE (value owner), RW-REFADM (loader) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0761 | The classification answer the case needs is not carried by the published document contract or by EV-16 and EV-17 | Solution architect | Resolved (directive) |
| GAP-0762 | The rwb-case login name is not in the sources | Tech lead | Resolved (directive) |
| GAP-0763 | The texts of MSG-GEN-004 and MSG-GEN-006 are not in the source extracts | Solution architect | Resolved (directive) |
| GAP-0764 | No source names a classifier version label or its format | Solution architect | Resolved (directive) |
| GAP-0765 | The case document link is not an Owner row and has no field IDs | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0766 | The rwb-case switch key and the re-drive time of day are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0767 | The decision record is written here although DP-03 and its library story are not applied | Solution architect | Resolved (directive) |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0844 | rwb-access rollback gate: the rule arm calls the P7 rule-package rollback, but the story's contract-dependency list carries only P3 contracts | Solution architect | Resolved (directive) |
| GAP-0869 | The limit-move writes, their fields, the state set and the reference-list check are not in the sources | Tech lead | Resolved (directive) |
| GAP-0871 | The rwb-comms template dependency, the two template operations, the approval fields and the approval-reference shape are not in the sources | Tech lead | Resolved (directive) |
| GAP-0988 | The review-item authorise request shape, the label of the matrix and masking versions in force at the release date, and the review-field roster of the masking pack are fixed by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0992 | The intake-match contract baseline fixes shapes and paths the sources do not name at field level, and the plan's C list omits the two rwb-case reads | Tech lead | Resolved (directive) |
| GAP-0995 | The target retention and virus-scan surface of rwb-document, the scan attributes of an upload and the C row of the P3 case contract are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1002 | The classify run is drawn as an rwb-agent child while the legacy story calls the P10 model gateway in process, and no source names the model provider, endpoint or model version | Solution architect with the TechX tech lead of rwb-document and the rwb-agent owner | Resolved (directive) |
| GAP-1003 | No source names a classification operation, path or field-level name, a 404 message identifier is absent, and a classification event would be a third event for rwb-document | Solution architect with the TechX contract owner of rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1004 | The classifier artefact production and versioning, the evaluation report container, the alert thresholds and the deployment topology values are named by no source | DevOps engineer with the platform administrator and the data steward | Resolved (directive) |
| GAP-1005 | The extractor provider, model name and model version behind extraction_method MODEL are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1007 | The review reason EXTRACTION_FAILED is not a value of LOV-INTAKE-REVIEW | Data steward with the P5 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1011 | No source fixes the field-level names of the nine review resources, the one resolve answer, the field-patch idempotency, the document read position or the three platform message texts | Tech lead of rwb-document with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1012 | The channel pickup has no target shape of its own: the run record, the rerun operation, the channel property layout, the single-run rule and the cross-service partner read are named by the legacy story only | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1064 | The data-dictionary read has no contract dependency in the plan | Solution architect | Resolved (directive) |
| GAP-1070 | The interaction ledger write and the contact-point failed count are not named in this key's contracts | Solution architect | Resolved (directive) |
| GAP-1075 | DP-08 is not in the pattern set and the case facts of the conduct check are not in the contract dependencies | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1147 | The reference lists the template screen needs have no contract row and no DP-07 in this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1168 | RWB-P6-E1011-APP: the parameters and reference-data contracts of rwb-case and the rwb-source-data contract the run reads are missing from the story's C list | Solution architect | Resolved (directive) |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1183 | No rwb-treatment contract story is in the plan, although the story reads the treatment and writes its signature record | Solution architect | Resolved (directive) |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1409 | Reference-data client artefact coordinates, the cache time-to-live catalog entry, the refresh rule with no change event and the client-to-kit boundary are not specified | Platform team (PLT) architect with the rwb-case and rwb-decision owners | Resolved (directive) |
| GAP-1410 | The published reference-data client contract, the version and row data contract, the LOV-REF-TABLE code list and the no-version failure surface are not specified in a technical specification | Platform team (PLT) contract owner with the rwb-case owner | Resolved (directive) |
| GAP-1558 | The parameter and reference-data load interface is claimed by P4 in the API specification and by P3 in the default ruling | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1593 | Two FSD features assert the same review-queue criteria and the correction feed has no distinct criterion | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2087 | The source reads version 1 in its metadata table and v2 in its file name | Document owner of the notification and correspondence design | Resolved (directive) |
| GAP-2094 | The case-level list of notices is named by Architecture v5 but has no endpoint row | Service owner of P6 rwb-comms; API owner | Resolved (directive) |
| GAP-2133 | rwb-valuation owns no table, so the plan does not say where a route decision is kept | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2179 | The reference versions, their rows and the lists of values belong to rwb-case, the rule registry to rwb-decision, and the legacy story names a reference data service that exists in no source | Solution architect | Resolved (directive) |
| GAP-2216 | No source fixes the case-facts field list behind the D7.1 approval screen, the names of the two approval outcome events, the naming of the redress task, or the business date of the postal address input | Solution architect | Resolved (directive) |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2335 | The two DP-11 contract reads of the legacy in-process calls are absent from the Work Package dependency rows and DP-08 is not among the patterns | Solution architect | Resolved (directive) |
| GAP-2337 | The rwb-case side of the checklist story is not fixed: the case read operation, the reference-load operation, the batch missing-count operation and the DocumentChecklist field names | Solution architect, with the P5 TechX squad and the P3 rwb-case squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2348 | The rwb-document login, the request and answer field names of the generation path, the message text of MSG-P5-006, the container name, the index name, the Flyway step name and the P5 feature flag are not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2349 | This slice owns no legacy acceptance criterion while the Work Package lists all eleven legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2350 | The dependency rows of this slice name one contract only, while the pattern set names five platform contracts, the rwb-case reference-data contract and the generation contract of the service | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2454 | The D7.1 generation record has no field layout, no final-call set and no message text in the sources | TechX | Resolved (directive) |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2456 | The review decision codes and outcome values, the placement of the review facts in the record, and the rwb-decision login name are in no source | Solution architect with the reference-data owner and the ACE team | Resolved (directive) |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-2567 | RWB-E1-013: the plan's C row names two rwb-case contracts and omits the two rwb-source-data rows the run consumes | Solution architect | Resolved (directive) |
| GAP-2568 | RWB-E1-013: the definition load of table measure_definition has no target operation, because the table is P9's while the reference-load framework is rwb-case's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2652 | The reference set that holds the band, the floor and the freshness limit, and the operation that reads it, are not published | P3 rwb-case owner, with the P4 rwb-access owner confirming the superseded row | Resolved (directive) |
| GAP-2654 | Architecture v5 says the recovery.v_ace_* views are read only by rwb-source-data while DP-05 allows the service's own views | ACE DB owner, with the P1 rwb-source-data owner and the platform data owner | Resolved (directive) |
| GAP-2690 | The rwb-treatment share of the key is stated by no S2 source, and the caller contract, the level comparison, the case move and the record ownership are split across four stories | Solution architect with the rwb-integration, rwb-treatment, rwb-case and rwb-access tech leads and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2751 | The four consumed reads and the two handed-over operations of the pack carry no dependency row, and two of the operations have no published name | Solution architect, S4 rwb-litigation, with the P5 rwb-document, P3 rwb-case and P4 rwb-access architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2765 | No source publishes the four consumed surfaces the pack step needs: the pack and defect-list read of rwb-document, the notice and template-status read of rwb-comms, the case read with its task raise and route fact of rwb-case, and the D7 approval item of rwb-decision | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2801 | Four consumed surfaces of the appeal have no dependency row, and the plan carries no contract, integration or external dependency for either slice | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case, S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3014 | RWB-S6-E5025: the masking rule set, the tape layout, the tape's storage reference, the PII service mapping and the six consumed contracts are given by no source and sit outside the plan's empty C row | Solution architect | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3086 | RWB-S8-E1065-APP: the deviation slice of the sandbox has no published case-reference source, no deviation count per case or per code, no operation or field names for the stage contract read, no codes or owner roles for R-DEV-05 and R-DEV-06, no test level for the ten legacy cases and an empty H row for eight patterns | Solution architect, with the rwb-deviation owner, the rwb-case and rwb-document owners, the rwb-source-data sandbox owner, the rule-set owner of the Deviations package, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3106 | RWB-S9-E6029-APP: the onboarding write has no published operation, partner_user has no field list, the terms have no linking column, and the reference-data read has no plan row | Solution architect with the rwb-partner tech lead, the rwb-case reference-data owner and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3107 | RWB-S9-E6029-CON: the onboarding operation, the partner_user shape, the terms link, the consumed operation name and the conflict message have no published baseline | Solution architect with the rwb-partner tech lead and the rwb-case reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3109 | RWB-S9-E6030-CON: the panel baseline has no published write operation, no path for the reference-data read, no status-to-message mapping and no level on the legacy cases | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E1054-APP | skipped AC ID | 101 | missing: AC11, AC12, AC13, AC14, AC15, AC16, AC17 |
