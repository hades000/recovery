# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 4 of 12 (RWB-P3-E1032-APP to RWB-P3-E1043-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 106 |
| Cross-document (pending in another document) | 158 |
| Not applied (value not in the sources) | 3 |
| Open business decisions | 13 |
| Register gaps linked | 114 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E1032-APP | 32 | 41 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1032 APP Automatic attach from the OCR intake v2.md |
| RWB-P3-E1035-APP | 15 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1035 APP Case record view v1.1 with documents and history timeline v2.md |
| RWB-P3-E1035-CON | 11 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1035 CON Case record view v1.1 with documents and history timeline - contract v2.md |
| RWB-P3-E1042-APP | 11 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1042 APP Central configuration service and parameter catalog v2.md |
| RWB-P3-E1042-CON | 17 | 57 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1042 CON Central configuration service and parameter catalog - contract v2.md |
| RWB-P3-E1043-APP | 20 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1043 APP Reference data service with versioned tables v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1043-APP, RWB-P3-E1043-CON | R-29035 | GAP-0222 | Register gap | Data steward and data product owner | The Owner column is a stewardship role, not a service, and it is kept unchanged | Read column D as the stewardship owner that approves a value, and the appended 'Owning service (D-RCV-60)' as the service that loads and serves it; the Key sheet gains the two terms that say so. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1019-ITG, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P4-E1022-APP, RWB-P5-E1025-APP, RWB-P5-E1025-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP | R-35406 | ASM-1988 | Register assumption |  | The approver of a document-type load is the legal counsel who owns the type table, holding Reference data A, as the legacy story assumes under DL01; the loader holds Reference data C and may not approve | Business lead with Legal confirms the role that approves the type list |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-ITG-TE010-ITG, RWB-ITG-E1047-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P3-E1042-APP | R-35662 | ASM-3199 | Register assumption |  | The six open-point rows that named an individual (DL03, DL04, DL05, DL06, DL07, DL37) carry the Template and Rules R9 placeholder in the Owner column, with the organisation the same row already stated kept after it, and the five roles of section 9 are left as the only owner labels in the document. | Confirm the role that owns each of the six open points. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E1032-APP | R-00754 | CG-ALL-3707 | 12.5 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment is a solution architect ruling; none in sources (Service Template Spec v1 L371 shows only the reserved word). Placeholder not invented. |
| RWB-P3-E1032-APP | R-00755 | CG-ALL-3708 | 12.5 | Java package th.co.scb.ace.workbench.recovery.case.casedocument uses the reserved word 'case' | casedocument segment needs the solution architect ruling; sources give only th.co.scb.ace.workbench.recovery.case (Service Template Spec v1 L371). Not invented. |
| RWB-P3-E1032-APP | R-10280 | CG-ALL-3700 | 12.1 | HTTP errors with no message ID: 401 no session | Error Standard v4 MSG-P1-001 is a stale-data warning, not system-unavailable or session. No 401 session message ID found. Business analyst to confirm; placeholder kept. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05844 | RWB-P3-E1032-APP | GAP-3144 | 7 | Record the primary/secondary AC split so AC1 to AC15 are counted once against RWB-P5-E1032-APP; this slice owns seven new criteria and eight new test cases. |
| CDC-05848 | RWB-P3-E1032-APP | CG-ALL-3706 | 18 | Align the test lists for REQ-DCM-007, REQ-DRI-004 and REQ-DCM-005 with story section 18 in the RTM's next version. |
| CDC-05866 | RWB-P3-E1035-APP | CG-ALL-3716 | 18 | Align the test lists for the four requirements with section 18 in the next RTM version. |
| CDC-05880 | RWB-P3-E1035-CON | CG-ALL-3724 | 18 | Align the test cases traced to the four differing requirements in RTM v7 with §18 of RWB-P3-E1035-CON (for REQ-CWC-016, §18 lists TC-P3-E1035-CON-02 and -03; RTM v7 lists TC-E1-018-01 to -03 and others). |
| CDC-05890 | RWB-P3-E1042-APP | DOR-RWB-P3-E1042-APP-12 | 12, 12.7, 16, 18 | Align the REQ-DRI-010 test list to TC-E1-042-01 to -11, -13 and -14 as section 18 now states |
| CDC-05898 | RWB-P3-E1042-APP | CG-ALL-3730 | 18 | Align the REQ-DRI-010 test list in RTM v7 with section 18 (TC-E1-042-01 to -11, -13, -14); remove other stories' tests. |
| CDC-05947 | RWB-P3-E1042-CON | CG-ALL-3738 | 18 | Align the test lists for REQ-DRI-010 and the second differing requirement between section 18 of this story and RTM v7 in the next versions of both documents. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05819 | RWB-P3-E1032-APP | DOR-RWB-P3-E1032-APP-14 | header | Record the signed epic design sign-off for RWB-P3-E1032-APP. |
| CDC-05858 | RWB-P3-E1035-APP | DOR-RWB-P3-E1035-APP-14 | 18 | Record the signed sign-off of the epic design for RWB-P3-E1035-APP. Story §18 now shows the placeholder Epic design row. |
| CDC-05870 | RWB-P3-E1035-CON | DOR-RWB-P3-E1035-CON-14 | Header | Record the signed epic design sign-off for RWB-SVC-P3, which this story must cite. |
| CDC-05902 | RWB-P3-E1042-CON | DOR-RWB-P3-E1042-CON-14 | n/a | Record the signed epic design sign-off and its reference for RWB-SVC-P3 |
| CDC-05958 | RWB-P3-E1043-APP | DOR-RWB-P3-E1043-APP-14 | header | Record the signed epic design sign-off for RWB-P3-E1043-APP. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05821 | RWB-P3-E1032-APP | CG-ALL-3693 | 4, 11 | Register the new rwb_case table case_document_link in LDM v9 Fields or Data Classification v5 Fields, or record it as an object in the owning document. |
| CDC-05822 | RWB-P3-E1032-APP | CG-ALL-3694 | 11 | Register field checklist_state in the rwb_case table case_document_link in LDM v9 Fields or Data Classification v5 Fields, or record it as an object in the owning document. |
| CDC-05823 | RWB-P3-E1032-APP | CG-ALL-3695 | 11 | Register field extracted_field_count in the rwb_case table case_document_link in LDM v9 Fields or Data Classification v5 Fields, or record it as an object in the owning document. |
| CDC-05824 | RWB-P3-E1032-APP | CG-ALL-3696 | 11 | Register field linked_at in the rwb_case table case_document_link in LDM v9 Fields or Data Classification v5 Fields, or record it as an object in the owning document. |
| CDC-05825 | RWB-P3-E1032-APP | CG-ALL-3697 | 11 | Register field source_event_id in the rwb_case table case_document_link in LDM v9 Fields or Data Classification v5 Fields, or record it as an object in the owning document. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05882 | RWB-P3-E1042-APP | CG-ALL-3729 | 12.3 | Add rwb.case.ParameterVersionApproved.v1 to the Events sheet on topic rwb.case.events.v1 with payload paramKeys, versionNo, validFrom, environment and CloudEvents envelope. |
| CDC-05888 | RWB-P3-E1042-APP | DOR-RWB-P3-E1042-APP-8 | 12.3 | Add rwb.case.ParameterVersionApproved.v1 to the Events sheet on topic rwb.case.events.v1 with payload paramKeys, versionNo, validFrom, environment and CloudEvents envelope. |
| CDC-05895 | RWB-P3-E1042-APP | GAP-2212 | 12 | Event named rwb.case.ParameterVersionApproved.v1 added with payload; topic Not specified in the source documents (GAP-2212) |
| CDC-05901 | RWB-P3-E1042-CON | CG-ALL-3736 | 12.3 | Add event type rwb.case.ParameterVersionApproved.v1 to the Events sheet |
| CDC-05903 | RWB-P3-E1042-CON | DOR-RWB-P3-E1042-CON-8 | 12.3 | Add event type rwb.case.ParameterVersionApproved.v1 to the Events sheet |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05916 | RWB-P3-E1042-CON | GAP-1206 | n/a | Add to the plan and dependency map for this key: build H rows RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON; contract C rows RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-case contract read of case number and owner. |
| CDC-05949 | RWB-P3-E1042-CON | GAP-1212 | 13 | Add to this story's dependency lists the eight DP-added rows: H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON. Metadata rows unchanged. |
| CDC-05950 | RWB-P3-E1042-CON | GAP-1335 | 13 | Carry RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON in the wave 2 dependency map. Metadata rows unchanged. |
| CDC-05951 | RWB-P3-E1042-CON | GAP-1337 | 13 | Carry the platform contracts and the rwb-case rule-package, parameters and reference-data contracts (C RWB-P7-E1073-CON, C RWB-P3-E1042-CON, C RWB-P3-E1043-CON) in the wave 2 dependency map. Metadata rows unchanged. |
| CDC-05953 | RWB-P3-E1042-CON | GAP-1288 | 13 | Add RWB-P3-E1042-CON as DP-added with H RWB-PLT-E1027-CON (DP-03), H RWB-PLT-E1042-CON and C RWB-P3-E1042-CON (DP-06), H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON (DP-07), H RWB-PLT-TE006-CON (DP-09), H RWB-PLT-E1044-CON (DP-15) and H RWB-PLT-N001-CON (DP-19), with the store baseline and the rwb-access authorise contract; Ready to start stays Day 1; the story metadata rows are corrected at the next version of the story set. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05835 | RWB-P3-E1032-APP | GAP-1201 | 16 | Record that the attach proof of TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP and that the P6 copy proves the service side, and note the access case TC-E1-032-16 as the notice-read refusal. |
| CDC-05879 | RWB-P3-E1035-CON | CG-ALL-3723 | 16 | Add rows TC-P3-E1035-CON-01 to TC-P3-E1035-CON-06 with Given, When and Then copied from the criterion each covers. |
| CDC-05906 | RWB-P3-E1042-CON | DOR-RWB-P3-E1042-CON-12 | 12.7, 16, 18 | Add TC-P3-E1042-CON-01 to -08 to Test Cases v8; align RTM v7 test lists with section 18 |
| CDC-05946 | RWB-P3-E1042-CON | CG-ALL-3737 | 16 | Add rows for TC-P3-E1042-CON-01 to TC-P3-E1042-CON-07 in the next Test Cases version, with Given, When and Then copied from the criterion each one covers. |

### parameter-catalog.csv (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05849 | RWB-P3-E1032-APP | GAP-0745 |  | Add an rwb-case parameter for the case-side document switch, default on, owner RW-COE; key Not specified in the source documents (GAP-0745). Off means the case side writes nothing from an event. |
| CDC-05852 | RWB-P3-E1032-APP | GAP-1200 |  | Name the business-owned notice values of the communications module with defaults in a parameter catalog row, or state the module has none and DP-06 applies as a path without a value. |
| CDC-05881 | RWB-P3-E1042-APP | CG-ALL-3728 |  | Record one entry-DPD parameter key, case.entry.dpd (the key this story reads), in parameter-catalog.csv; align case.entry.dpd_threshold in Assumptions Register v1 and Test Cases v8. |
| CDC-05885 | RWB-P3-E1042-APP | DOR-RWB-P3-E1042-APP-20 |  | Record one entry-DPD parameter key, case.entry.dpd (the key this story reads), in parameter-catalog.csv; align case.entry.dpd_threshold in Assumptions Register v1 and Test Cases v8. |

### RWB-PLT-E1042-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05892 | RWB-P3-E1042-APP | GAP-1406 | 12 | Build-check rule set replaced by Not specified in the source documents (GAP-1406); contract reference kept. |
| CDC-05940 | RWB-P3-E1042-CON | GAP-1406 |  | Publish the artefact coordinates from the platform baseline and the two build-check rule sets (0, 1, -1 allowed; test code by path and annotation) as its contract; this story reads refdata.cache.ttl-seconds only. |
| CDC-05941 | RWB-P3-E1042-CON | GAP-1407 |  | Publish one versioned contract artefact at major version 1 with the interface, four types, key set, DF-REF-132 to DF-REF-158, four P3 operations with status codes, cache and refresh rule, start-up rule, build-check contracts and a fake. |
| CDC-05942 | RWB-P3-E1042-CON | GAP-1408 |  | Fix the chart values RWB_ENV, RWB_PARAMETER_CATALOG and RWB_PARAMETER_TTL_KEY; add one parameter-catalog-seed hook before rollout; probe the start-up check; one page for a missing value and two warnings from the library metrics. |

### RWB-P3-E1043-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05959 | RWB-P3-E1043-APP | DOR-RWB-P3-E1043-APP-21 | header | Set the build status to Done (currently In build). |
| CDC-05961 | RWB-P3-E1043-APP | DOR-RWB-P3-E1043-APP-23 | header | Fix the contract version this story builds against and record it in the story. |
| CDC-05969 | RWB-P3-E1043-APP | GAP-1410 |  | Publish the client surface as one versioned contract at major version 1; publish the version and row projection with the three-value status vocabulary; fix the code set as the twelve LOV-REF-TABLE codes with the rule-package and holiday exclusions; publish the refusal as a non-retryable checked exception carrying MSG-P3-027, the table code and the business date. |
| CDC-05972 | RWB-P3-E1043-APP | GAP-0698 |  | A dated read with no version in force answers 404 with MSG-P3-027 naming the table code and the date, never an older version, default row or empty list; verify and rollback require Reference data A. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05827 | RWB-P3-E1032-APP | DOR-RWB-P3-E1032-APP-7 | 11 | Add entity case_document_link in rwb_case with fields case_id, document_id, checklist_state, extracted_field_count, linked_at, source_event_id (GAP-0742). Story already flags it. |
| CDC-05830 | RWB-P3-E1032-APP | GAP-0742 | 11, 12.7, 13 | Add entity case_document_link (owner P3, schema rwb_case) with field IDs for case_id, document_id, checklist_state, extracted_field_count, linked_at and source_event_id |
| CDC-05846 | RWB-P3-E1032-APP | GAP-0765 | Header | Add the classification columns of rwb_case.case_document_link in V1050_1 and register the table with its field IDs in the next data dictionary version. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05829 | RWB-P3-E1032-APP | GAP-0356 | 12 | Keep CASE_NO_PATTERN, ACCOUNT_NO_PATTERN and CLASSIFY_THRESHOLD as document_hub_parameter rows read as data; intake starts from DocumentStored with KEDA workers; /review-items and /resolve with item version. |
| CDC-05896 | RWB-P3-E1042-APP | GAP-2213 | 7 | Add the run-time catalog read with its operation, right, scope and the keys artefact the platform client publishes for service identities. |
| CDC-05944 | RWB-P3-E1042-CON | GAP-2213 | 12.2 | Add the run-time catalog read to the Ownership Map with the right a service identity holds, and record the keys artefact the platform client publishes. Until then ASM-3640 serves the key-prefix query of GET /admin/parameters to a service identity holding Rules and parameters R. |

### RWB-P3-E1035-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05859 | RWB-P3-E1035-APP | DOR-RWB-P3-E1035-APP-21 | 18 | Move the build status of RWB-P3-E1035-CON from Not started to Done. |
| CDC-05860 | RWB-P3-E1035-APP | DOR-RWB-P3-E1035-APP-22 | 18 | Publish the contract fake library and record its version as published. |
| CDC-05861 | RWB-P3-E1035-APP | DOR-RWB-P3-E1035-APP-23 | 18 | Fix and record the contract version this story builds against. Story §18 now shows the placeholder Contract version row. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05862 | RWB-P3-E1035-APP | CG-ALL-3715 | 14 | Add a new message ID for 'No session or an expired session' with text 'You are not signed in. Sign in to continue.' Story §14 cites it after it exists. |
| CDC-05863 | RWB-P3-E1035-APP | DOR-RWB-P3-E1035-APP-9 | 14 | Align the P2 use of MSG-P4-001 with the standard meaning; section 14 keeps the session meaning until then. |
| CDC-05872 | RWB-P3-E1035-CON | CG-ALL-3722 | 14 | Add a new message ID for 'No session or an expired session' with the text 'You are not signed in. Sign in to continue.'; then the story cites it. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05869 | RWB-P3-E1035-CON | CG-ALL-3725 | 3 | The story still carries th.co.scb.ace.workbench.recovery.case in §3, §8 CB1 and §13; the package rename belongs to the Service Template Specification, not the story. |
| CDC-05883 | RWB-P3-E1042-APP | CG-ALL-3731 | 13 | Package segment recorded as Not specified in the source documents (CG-ALL-3731). |
| CDC-05887 | RWB-P3-E1042-APP | DOR-RWB-P3-E1042-APP-22 | 12.8 | Record the published contract fake library version and its artefact coordinates for the rwb-case parameters fake, pinned from the platform library baseline at version freeze. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05897 | RWB-P3-E1042-APP | GAP-1558 | 12 | Set x-module to P3 for GET /admin/lists/{listCode}, POST /admin/reference-loads and the three sibling paths. |
| CDC-05945 | RWB-P3-E1042-CON | GAP-1558 | 12 | Realign the x-module of GET /admin/lists/{listCode}, POST /admin/reference-loads and the three sibling paths to P3 rwb-case, matching ownership.json and the R-PREC default ruling. |
| CDC-05965 | RWB-P3-E1043-APP | GAP-1558 | find it | Set x-module to P3 for the five list and reference-load paths in ownership.json: GET /admin/lists/{listCode}, POST /admin/reference-loads and three sibling paths. |

### RWB-P5-E1032-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05828 | RWB-P3-E1032-APP | GAP-0992 | 12 | Fix the four shapes as the smallest superset of the legacy list, declare the four consumed rows with fakes, and add the two rwb-case case-read contracts the baseline consumes to the C list. |
| CDC-05911 | RWB-P3-E1042-CON | GAP-0992 | find it | Fix the four shapes as the smallest superset of the legacy list; declare the four consumed rows and the two rwb-case reads in C with fakes; keep unnamed elements behind the placeholder until confirmed. |

### RWB-P7-E1032-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05837 | RWB-P3-E1032-APP | GAP-2444 |  | Carry the document reference, the intake item and the match method in actions, the classifier version in model_version, the confidence and the type candidates in recommendation, the message id of a refusal in outcome, and final_call ATTACHED; add the columns by migration V1032_1 in rwb_decision. |
| CDC-05854 | RWB-P3-E1032-APP | GAP-2449 | 3 | Use 'the rwb-decision login (DP-02)'; keep placeholders for the ledger ingest target and chain-check time parameter names and for the texts of MSG-P7-009 and MSG-GEN-006; read the parameters through the rwb-case parameters contract. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05845 | RWB-P3-E1032-APP | GAP-1198 | Header | Add H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON, C RWB-P3-E1042-CON and C RWB-P3-E1043-CON to the dependency rows. |
| CDC-05913 | RWB-P3-E1042-CON | GAP-1198 | find it | Add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON to its dependency rows, or record in the release train. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05847 | RWB-P3-E1032-APP | CG-ALL-3705 | 16 | Rows 340-349 carry the legacy AC numbering; the shifted covers cited criteria the tests do not exercise (TC-10 cited a nonexistent AC10), so the story keeps its own covers and the register is realigned to them. |
| CDC-05873 | RWB-P3-E1035-CON | DOR-RWB-P3-E1035-CON-12 | 16 | Add TC-P3-E1035-CON-01 to -07 to Test Cases v8; align RWB-P3-E1035-CON test lists in RTM v7 with section 18 of the story. |

### RWB-P7-E1027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05865 | RWB-P3-E1035-APP | GAP-2210 | 8 | Publish the decision-record query path, filter and field list. |
| CDC-05876 | RWB-P3-E1035-CON | GAP-2210 | 11 | Publish the decision-record query path, filter and field list in C RWB-P7-E1027-CON. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05868 | RWB-P3-E1035-CON | CG-ALL-3721 | 3 | Remove the fixed enum on transferReasonCode so that LOV-TRANSFER-REASON values load as data without a schema change. |
| CDC-05871 | RWB-P3-E1035-CON | DOR-RWB-P3-E1035-CON-8 | 3 | Remove the fixed enum on transferReasonCode so that LOV-TRANSFER-REASON values load as data without a schema change. |

### RWB-P3-E1042-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05886 | RWB-P3-E1042-APP | DOR-RWB-P3-E1042-APP-21 |  | Set build status to Done; it is currently In build. |
| CDC-05893 | RWB-P3-E1042-APP | GAP-1407 | 12 | Contract members, DF-REF range, status codes and freeze rule recorded as Not specified in the source documents (GAP-1407). |

### RWB-S4-E2025-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05928 | RWB-P3-E1042-CON | GAP-1903 |  | Fix fill trigger as the document type in the request; derive the write key from action, type, document versions and values; one hearing per action and date as a uniqueness rule in rwb_litigation; take parameter and list calls from RWB-P3-E1042-CON and RWB-P3-E1043-CON. |
| CDC-05929 | RWB-P3-E1042-CON | GAP-1898 |  | Keep plan lists; stay Day 1 with RWB-P5-E2025-CON as sole contract dependency; build against fakes; remove DP-09 and DP-10 from the pattern list; add H and C rows when published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05817 | RWB-P3-E1032-APP | CG-ALL-3698 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the provider CON story, or the consumer moves to a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05818 | RWB-P3-E1032-APP | CG-ALL-3699 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story, or the consumer moves to a published operation. |

### OTHER:rwb-source-data API yaml; OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05820 | RWB-P3-E1032-APP | DOR-RWB-P3-E1032-APP-8 | 12.1 | Publish GET /api/recovery/source-data/v1/accounts/{id} in rwb-source-data and POST /api/recovery/access/v1/authorise in rwb-access; align the event type to rwb.decision.DecisionRecorded.v1 or record the rename. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05826 | RWB-P3-E1032-APP | CG-ALL-3703 | 12.5 | Add activity LinkDocument on task queue rwb-case to the Activities sheet. |

### RWB-P5-E1032-CON; RWB-P5-E1032-APP; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05831 | RWB-P3-E1032-APP | GAP-0991 | 12.4 | Publish /resolve as the attach operation with the Documents right C applied to the chosen case and the legacy 201 Document answer; declare rwb.document.DocumentAttached.v1 on rwb.document.events.v1, or have the event catalogue owner confirm DocumentStored in row 16 before the wave 1 release. |

### RWB-P5-E1032-INF; RWB-P5-E1032-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05832 | RWB-P3-E1032-APP | GAP-0993 |  | Provision the shape of each value: worker replica count, request and limit set, KEDA ceiling, document_text growth and index budget, rwb-quarantine clearing age, hold container capacity and scan rate per hour; set the numbers per environment from the SIT measurement of one business-hour window and the scan product's throughput. |

### RWB-P5-E1032-CON; RWB-P6-E1032-APP; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05833 | RWB-P3-E1032-APP | GAP-1197 |  | Publish the generated-document request and answer of P5 with the intake item it creates; name the document type and source a notice letter copy takes; register the notice parameters with their names; extend the event catalogue row to its payload; allocate the notice screen identifier. |

### RWB-P5-E1032-CON; RWB-P6-E1032-APP; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05834 | RWB-P3-E1032-APP | GAP-1199 |  | State whether the hub creates an intake item from a generated document and which fields of the request it needs, so that the handoff and the item are specified once. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-P5-E1032-APP; RWB-ITG-E1032-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05836 | RWB-P3-E1032-APP | GAP-1202 |  | Decide once whether the document hub consumes rwb.comms.NoticeGenerated.v1 or is called by rwb-comms, and align the event catalogue row, the P5 story and the integration suite to that decision. |

### RWB-P3-E1043-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:TSD P7 v2 T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05838 | RWB-P3-E1032-APP | GAP-2445 |  | Hold DOCATT as a value of LOV-DECISION in force and read it through the rwb-case reference-data contract at the version in force; an unknown code is refused with MSG-P7-009. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md; RWB-S9-E1032-APP; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05839 | RWB-P3-E1032-APP | GAP-3137 | Header | Confirm the secondary partner slice in the Change Register and publish the rwb_partner frame (base /api/recovery/partner/v1, topic rwb.partner.events.v1, queue rwb-partner, package th.co.scb.ace.workbench.recovery.partner) for RWB-S9-E1032-APP. |

### OTHER:RWB-S9 contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05840 | RWB-P3-E1032-APP | GAP-3138 | 2 | Publish the partner file channel: rwb_partner submission row, PartnerDocumentSubmitted fact, attach event consumed, and item read used to copy the match state. |

### RWB-S9-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05841 | RWB-P3-E1032-APP | GAP-3141 | 12 | Publish POST and GET /partner/instructions/{instructionId}/documents, the document-hub intake creation, the rwb.partner.PartnerDocumentSubmitted.v1 payload, and the 404 and 409 bodies in RFC 9457 shape. |

### parameter-catalog.csv; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05842 | RWB-P3-E1032-APP | GAP-3142 | 3 | Publish the intake bound parameter row, the acceptance decision code with its version, and LOV-DOC-TYPE; keep every value out of code. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05843 | RWB-P3-E1032-APP | GAP-3143 | 11 | Add partner_intake with its field IDs (id, partner_id, instruction_id, case_id, document_type, file_sha256, intake_item_id, state, candidate_case_ids, received_at, audit columns, version) before the wave 1 entry check. |

### OTHER:Platform DB story (RWB-PLT) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05850 | RWB-P3-E1032-APP | GAP-0748 |  | Name one database login per service for rwb-case and rwb-document; logins Not specified in the source documents (GAP-0748). Story keeps role names until then. |

### RWB-P5-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05851 | RWB-P3-E1032-APP | GAP-0994 | 12.6 | Register the intake Schedule every 15 minutes from 08:00 to 18:00 Asia/Bangkok on working days, overlap policy skip and a catch-up of one run; hold the run-failure, held-item age, KEDA and consumer-lag thresholds as environment values; keep a placeholder message ID for the lag alert until the Error and Message Standard names it. |

### OTHER:FSD P6 Communications v3 and TSD P6 Communications v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05853 | RWB-P3-E1032-APP | GAP-1203 |  | Approve both documents, or record that wave 1 builds on the reviewed versions and any approved-text change is a change request. |

### OTHER:rwb-source-data (P1) ledger specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05855 | RWB-P3-E1032-APP | GAP-2450 | 12.6 | State the trigger of the ledger completeness check: it runs on the ledger ingest window of DP-06, with no Temporal Schedule and no cron entry of the service. |

### OTHER:FSD S9 Screens table (PRT-01 to PRT-04) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05856 | RWB-P3-E1032-APP | GAP-3145 | 19 | Name PRT-02 Instruction as the screen that carries the document submission of an instruction; keep the service answer POST /documents unchanged. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05857 | RWB-P3-E1032-APP | GAP-3174 | header | Record wave 1 delivery of rwb-partner in the service epic and wave plan, with one conflict row per service and business epic (R5.6); rwb-partner service wave 4 governs its later stories. |

### OTHER:rwb-source-data contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05864 | RWB-P3-E1035-APP | GAP-0695 | 5, 18 | Add the interaction read operation with its path and page and size parameters. |

### RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05867 | RWB-P3-E1035-APP | GAP-2211 | find it | Publish the timeline addition as v1.1, an additive minor version inside major version 1, with item detail fields reasonCode, fromQueueCode, toQueueCode, ruleId, the TimelineSection state on a 200 response and the page total. Leave type order, section timeout and page size as rwb-case parameters. |

### OTHER:rwb-source-data contract (P1 source data owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05874 | RWB-P3-E1035-CON | GAP-0695 | 8 | Story side done: CB6 keeps the order, timeout and page size as parameters; the timeline read and the interaction ledger data belong to the P1 source data owner. |

### RWB-P5-E1054-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05875 | RWB-P3-E1035-CON | GAP-1010 | 8 | Fix field-level queue names and the three platform message texts before the wave 1 entry check; read the four review rows from document_hub_parameter in rwb_document. |

### OTHER:rwb-agent story set (legacy RWB-E2-028) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05877 | RWB-P3-E1035-CON | GAP-2190 | find it | Apply the proposed fix of GAP-2190 in the rwb-agent story set. |

### OTHER:rwb-agent contract story set (legacy RWB-E2-028) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05878 | RWB-P3-E1035-CON | GAP-2191 | find it | Apply the proposed fix of GAP-2191 in the rwb-agent contract story set. |

### RWB-P3-E1042-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05884 | RWB-P3-E1042-APP | DOR-RWB-P3-E1042-APP-14 |  | Record the signed epic design for RWB-P3-E1042-APP so DoR item 14 (Epic design) is confirmed against the epic design record. |

### OTHER:Screen catalogue entry SCR-39 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05889 | RWB-P3-E1042-APP | DOR-RWB-P3-E1042-APP-10 | none | Add empty, loading, error and no-access states to SCR-39; the no-access reply is 403 MSG-P4-002 per section 12 |

### OTHER:Wave-1 design at the rwb-decision and rwb-comms contract review (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05891 | RWB-P3-E1042-APP | GAP-1214 | none | Fix the five points: local copy table and columns, parameter rows and read path, two check values with message text, scenario set and run result shape, 300 ms measurement point |

### OTHER:Platform library baseline (chart values, seed ordering, probe, alert thresholds) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05894 | RWB-P3-E1042-APP | GAP-1408 | 12 | Chart values, seed ordering, probe and alert thresholds recorded as Not specified in the source documents (GAP-1408). |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:Flyway sequence) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05899 | RWB-P3-E1042-APP | GAP-2214 | 13 | Fix the five names: the target package segment, the used_by convention per parameter, the feature-flag name the platform library allocates for rwb.p3.configservice, the next free numbers of the rwb-case Flyway sequence for the two migrations, and one primary key for parameter_catalog. |

### OTHER:Authorise model of rwb-access (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05900 | RWB-P3-E1042-APP | GAP-2215 | 12 | Confirm capability area and right of the three write operations and whether a service identity may hold them; record them in the authorise model. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05904 | RWB-P3-E1042-CON | DOR-RWB-P3-E1042-CON-1 | 1 | Add the role consumer of the rwb-case parameters contract as a role code or role name |

### RWB-P3-E1042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05905 | RWB-P3-E1042-CON | DOR-RWB-P3-E1042-CON-10 | n/a | Add empty, loading, error and no-access states to SCR-39 |

### RWB-P6-E1011-APP; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05907 | RWB-P3-E1042-CON | GAP-1168 | find it | Add RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-source-data contract to C; name the reference-data read operation in RWB-P3-E1043-CON. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05908 | RWB-P3-E1042-CON | GAP-1946 | find it | Keep H and C at None; record the nine platform and rwb-case CONs as wave-0 prerequisites with fakes; read the ACE-side check from the DP06 rwb-source-data contract; serve facts from the /api/recovery/asset/v1 quality endpoints. |

### RWB-P6-E1019-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05909 | RWB-P3-E1042-CON | GAP-1174 | find it | Add RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON and RWB-PLT-E1044-CON to its dependency rows, or record in the platform release train. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05910 | RWB-P3-E1042-CON | GAP-2404 | find it | Read H as None plus the five platform contracts the DP table names; read C as RWB-P10-E2032-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and the P4 authorise contract; story stays Day 1. |

### OTHER:work package WP story line and section 13 of the P7 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05912 | RWB-P3-E1042-CON | GAP-2448 | find it | Keep the metadata rows as the work package fixes them; record the DP-table dependencies in section 13, built against their fakes on Day 1. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05914 | RWB-P3-E1042-CON | GAP-2414 | n/a | Set Depends on (build) H list to None plus platform contracts RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON. Set Contract dependencies C list to RWB-P3-E2041-CON, RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. Read RWB-P7-E2042-APP as the published registry set; keep Ready to start Day 1. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P5 (API-P5-016; OTHER:T3.1) and the rwb-document story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05915 | RWB-P3-E1042-CON | GAP-1023 | n/a | Use path /cases/{caseId}/generated-documents on base /api/recovery/document/v1 and record architecture slide 16 POST /documents/generate as the loser (ASM-101). Read template version and merge fields only via RWB-P6-E1046-CON (ASM-102). Add template_code varchar(30) and template_version integer beside template_id and treatment_id, with the partial unique index on (treatment_id, template_id) where state is DRAFT and is_active (ASM-103). |

### RWB-P5-E1050-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05917 | RWB-P3-E1042-CON | GAP-1002 | n/a | Build the classifier as a service-internal capability behind ClassifierClient with a stub and a route property, with no new dependency id. Track the agent and model-gateway satellite as external work. Confirm provider, endpoint and model version before SIT evaluation; add the C row only if the satellite stays. |

### RWB-P5-E1057-CON; RWB-P5-E1057-INF; RWB-P5-E1057-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05918 | RWB-P3-E1042-CON | GAP-1012 | n/a | Publish the three admin operations and the run record in RWB-P5-E1057-CON. Read the legacy intake container as the hold container rwb-quarantine. Carry the channel property layout as environment values of RWB-P5-E1057-INF and RWB-P5-E1057-OPS. Consume the partner read through the rwb-partner contract with a fake and no C row. Schedule owner confirms business-hours window, overlap policy and catch-up window before wave 1 release. |

### OTHER:Legacy RWB-E1-063; OTHER:FSD P4 v3; OTHER:TSD P4 v3 T6.1 and the data-lake copy of the access rule (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05919 | RWB-P3-E1042-CON | GAP-2333 | n/a | Keep Reporting R for the route check and Rules and parameters R at the metric owner. Record Reporting letters for remaining roles in the matrix load. Replace the lake copy of the access rule with the served-read access entry and correct REQ-ACA-006 and NFR-042 in the next FSD and TSD version. Add the five platform contracts to H and the two rwb-case contracts to C in the plan. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05920 | RWB-P3-E1042-CON | GAP-1214 | n/a | Fix at wave-1 design: the local copy table name and columns, the two parameter rows and their read path, the two added check values with message text, the scenario set and local run result shape, and the 300 ms measurement point. Until then keep legacy values (50 scenarios, cache 20, MSG-P3-027, MSG-GEN-006, MSG-P4-002, MSG-P7-003) and build against fakes. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05921 | RWB-P3-E1042-CON | GAP-1328 | n/a | Complete the metadata rows from the DP table: eight H rows (RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) and the C row of DP-06 and DP-07; add DP-09 to the pattern list. Or state in R5.5 that platform H and self-referential C rows are held by platform and contract stories. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05922 | RWB-P3-E1042-CON | GAP-2470 | n/a | Complete the metadata rows from the DP table: H rows RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON; C rows RWB-P7-E1073-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON. Say in R5.5 that platform H and self-referential C rows are held by platform and contract stories. |

### RWB-P8-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05923 | RWB-P3-E1042-CON | GAP-1346 | n/a | Keep plan H, C, I and X rows as given. Name the seven consumed rows in section 12.2 of RWB-P8-E2008-APP with the placeholder. Build against owner fakes on Day 1. Solution architect confirms the scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON. |

### RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05924 | RWB-P3-E1042-CON | GAP-2475 |  | State in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories and are not repeated on a secondary APP line. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05925 | RWB-P3-E1042-CON | GAP-1223 |  | Read H as None plus the platform contracts named by the DP table; read C as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON; story stays Day 1. |

### RWB-P7-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05926 | RWB-P3-E1042-CON | GAP-1265 |  | Add RWB-P1-E1015-CON and RWB-P3-E1018-CON as C rows, or record the two reads as route-level composites of RWB-PLT-N001-CON; consume against fakes until closed. |

### RWB-P5-E1025-APP; OTHER:TSD P5 v2 T-A.1 and RWB-E2-025 section 12 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05927 | RWB-P3-E1042-CON | GAP-1020 |  | Publish checked-fields read on /api/recovery/document/v1/cases/{caseId}/checked-fields with CheckedField and CheckedFieldSet shapes; apply DOCTYPE-2026.12 load via the type table; confirm with S4 and S2 before wave 2. |

### OTHER:Work package B2-P8-002 story line and RWB-E2-027 section 7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05930 | RWB-P3-E1042-CON | GAP-2506 |  | Add C RWB-P7-E1073-CON to the C row; read AC6 through the rwb-decision contract mock; name the ordering column as target name with priority as its legacy name; reconcile PMT-2026.12 to one version row before SIT. |

### RWB-P8-E2027-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05931 | RWB-P3-E1042-CON | GAP-1291 |  | Keep metadata rows as planned; record the DP-added H and C rows in the Dependency Map as non-blocking platform and published contracts built against fakes. |

### OTHER:RWB-E8-012 and the rwb-access publish story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05932 | RWB-P3-E1042-CON | GAP-2281 |  | Provide POST and GET /api/recovery/access/v1/admin/panel-changes; hand the workbook to the P3 reference-load operation with table code partner_panel and validFrom; read the rule version from the P7 rule-package contract. |

### RWB-P4-AD013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05933 | RWB-P3-E1042-CON | GAP-0844 |  | Add the P7 rule-package rollback contract as a C dependency at D1; build the rule arm against its fake and publish with the P7 contract story. |

### RWB-P4-AD011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05934 | RWB-P3-E1042-CON | GAP-0821 |  | Add the P7 rule-package contract (RWB-P7-AD011-CON or the id the P7 split allocates) as a C dependency in the metadata at D1; build the ingest and read against that contract and its fake. |

### RWB-P4-AD012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05935 | RWB-P3-E1042-CON | GAP-0826 |  | Add the P7 rule-package contract to its contract-dependency list at D1; fix the approve and version-list operations with the P7 owner; build the gate against that contract and its fake. |

### OTHER:rwb-access rule-change request story (key not in chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05936 | RWB-P3-E1042-CON | GAP-0868 |  | Declare the two registry reads as consumed against the P7 rule-package contract and fake; fix the seven checklist codes and seven version states as TSD P4 v3 T6.3 and T4 constants; raise the missing C dependency at D1. |

### RWB-P4-E8009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05937 | RWB-P3-E1042-CON | GAP-0870 |  | Raise the missing P3 reference-load contract as a C dependency at D1 and build against it and its fake; fix table code, sheet names, upload cap and record code with the owner at contract review. |

### RWB-P4-E8013-APP; RWB-P4-E8013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05938 | RWB-P3-E1042-CON | GAP-2284 |  | Add the rwb-decision decision-log and rule-catalog CON story to the contract-dependency list; publish the two reads with paths and query names; name the sample-size and tolerance parameter codes with the owners. |

### OTHER:legacy search story (key not in chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05939 | RWB-P3-E1042-CON | GAP-2335 |  | Add C RWB-P3-E1018-CON and C RWB-P4-E1037-CON to its dependency map at D1; state in its Build Sequence that the search is buildable from Day 1 against the two fakes. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05943 | RWB-P3-E1042-CON | GAP-2212 |  | Add the parameter event to the rwb-case catalogue with its number, key and payload, or rule that the cache time to live is the only refresh; until then publish rwb.case.ParameterVersionApproved.v1 on rwb.case.events.v1. |

### OTHER:Template and Rules v1 (section 1 worked example) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05948 | RWB-P3-E1042-CON | GAP-2150 | 1 | No story edit made; the worked example stays with Template and Rules v1 section 1. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05952 | RWB-P3-E1042-CON | GAP-2389 | 13 | At next plan revision add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON to the C list. Keep H empty. |

### OTHER:Not specified in the source documents (GAP-2410) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05954 | RWB-P3-E1042-CON | GAP-2410 | 13 | Record that a secondary slice builds against the platform contracts and published fakes and reads same-service wave-1 rows through its own schema. |

### OTHER:rwb-case repository and service template (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05955 | RWB-P3-E1042-CON | GAP-2214 |  | Fix five legacy names: target package, used_by convention, flag name, next free rwb-case migration numbers, one parameter_catalog primary key. |

### OTHER:rwb-access authorise model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05956 | RWB-P3-E1042-CON | GAP-2215 |  | Record capability area and right of the three reference-load write operations, confirmed with the rwb-access owner. |

### OTHER:Work Package plan (wp/B-P4-04.md, wp/B2-P4-010.md, checks/run_all.py) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05957 | RWB-P3-E1042-CON | GAP-2278 |  | Remove RWB-AD-016 from B-P4-04 fanout so B2-P4-010 alone owns it; number CG and ASM rows once; add plan-uniqueness check. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05960 | RWB-P3-E1043-APP | DOR-RWB-P3-E1043-APP-22 | header | Publish the contract fake library version and record it as published. |

### OTHER:P3 screen specification (SCR-40) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05962 | RWB-P3-E1043-APP | DOR-RWB-P3-E1043-APP-10 | 15 | State the empty, loading, error and no access states of SCR-40 so section 15 of RWB-P3-E1043-APP can copy them |

### OTHER:Recovery Workbench P2 criteria and test data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05963 | RWB-P3-E1043-APP | DOR-RWB-P3-E1043-APP-7 | 11 | Replace direct reads of ACE views with reads through the published rwb-case reference interface. |

### API:(service not named); RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05964 | RWB-P3-E1043-APP | GAP-0779 | find it | Keep /admin/reference-loads and /admin/reference-loads/{loadId}/approve for this service's permission and masking tables on /api/recovery/access/v1, with the generic reference-load path for lists, queues, timers, templates and parameters with rwb-case. Publish /api/recovery/access/v1/masking-policies with Reference data R. Publish AccessPolicyChanged with change kind, version and effective date and no personal value. Answer the matrix read from both role slices under one contract. |

### OTHER:Reference data starter sheet of the workbook (v5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05966 | RWB-P3-E1043-APP | GAP-0219 | find it | Add the S1 rwb-valuation and S7 rwb-writeoff rows at the next revision. Until then record both services as open. |

### OTHER:Recovery Workbench v5 workbook, reference data starter sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05967 | RWB-P3-E1043-APP | GAP-0220 |  | Keep the derivation rule on the starter sheet; each service story confirms its rows at design review; a later revision replaces derived rows with confirmed ones. |

### OTHER:RWB-PLT-TPL (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05968 | RWB-P3-E1043-APP | GAP-1409 | 13 | Record the artefact group, artefact name and publication channel of the reference-data client library in the platform library baseline. |

### OTHER:RWB-E2-041 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05970 | RWB-P3-E1043-APP | GAP-0719 |  | Record the rule-package scope (LOADED, APPROVED, IN_FORCE) for RWB-E2-041; the FSD A2.16 reference-data checklist stays with RWB-E1-043, this story. |

### OTHER:Recovery Workbench lists workbook; OTHER:Lists sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05971 | RWB-P3-E1043-APP | GAP-0221 |  | Keep every list row and its Source cell; add Owning service (D-RCV-60) and Owning schema (D-RCV-60) values: rule_row in rwb_decision, document_type and retention_rule in rwb_document, role in rwb_access; the route column names the contract that serves the list. |

### OTHER:refdata source; OTHER:Reference tables sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05973 | RWB-P3-E1043-APP | GAP-0223 | 8 | Record the owner of each of the five 'Reference table' rows from its map item (LOV-DOC-TYPE, LOV-RETENTION, service levels, masking_rule, reference_row); name reference_row in rwb_case as the message catalogue carrier; leave Table cells unchanged. |

### 07 Screens and experience/Recovery Workbench Screen Inventory and Navigation v2.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20581 | RWB-P3-E1042-APP | R-15966 |  | SCR-39 empty, loading, error and no-access states are not confirmed in the sources. Adding them needs a decision. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0065 | Wave conflict S9 / EP01 | Tech lead | Resolved (directive) |
| GAP-0081 | Owner and table of the model version in force are not stated | ACE | Resolved (directive) |
| GAP-0217 | LOV-REF-TABLE carries 25 table codes in v4 but the rwb-case reference-data contract fixes twelve | Reference data administrator | Resolved (directive) |
| GAP-0219 | Two services derive no starter row: S1 rwb-valuation and S7 rwb-writeoff | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0220 | No source states which lists a service needs at its first deployment | Data architecture team | Resolved (directive) |
| GAP-0221 | Four source lists are held in another service's table although the sheet calls every list Workbench-held | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0223 | Five reference-data rows name no table, and no message table exists in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0356 | Intake trigger, attach operation and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0692 | The per-service database login name for rwb-case is not given | ACE DB owner | Resolved (directive) |
| GAP-0695 | The timeline paging and the interaction ledger read operation are not given | P1 source data owner | Resolved (directive) |
| GAP-0696 | Legacy AC2 and BR1 load DELEGATION_LIMIT through the reference-data service, but the Ownership Map keeps delegation_limit with P4 rwb-access | Solution architect | Resolved (directive) |
| GAP-0697 | The column definitions of each reference table code and the element types of the reference resources have no source field by field | Data steward | Resolved (directive) |
| GAP-0698 | The answer of a dated read with no version in force, and the rights of the verify and the rollback, are not stated | Solution architect | Resolved (directive) |
| GAP-0719 | FSD A2.16 reports reference-data changes while the legacy story and the test cases govern rule package versions | Business analyst | Resolved (directive) |
| GAP-0742 | No case-side document link table or field IDs in the sources | RW-DATASTEW | Resolved (directive) |
| GAP-0743 | No named rwb-source-data operation for the ACE account number | RW-COE | Resolved (directive) |
| GAP-0744 | Cadence and time of the daily reconcile Schedule not specified | RW-COE | Resolved (directive) |
| GAP-0745 | The rwb-case feature switch key is not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0747 | Decision code and final call for the case document link are not specified | RW-COE | Resolved (directive) |
| GAP-0748 | Per-service login names for rwb-case and rwb-document are not specified | RW-SECADM | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0765 | The case document link is not an Owner row and has no field IDs | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0821 | rwb-access rule-version load: the rule registry is P7's but the story's contract-dependency list carries no P7 rule-package contract | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0826 | rwb-access rule-version approval: the registry's approve contract is not in the story's dependency list | Solution architect | Resolved (directive) |
| GAP-0844 | rwb-access rollback gate: the rule arm calls the P7 rule-package rollback, but the story's contract-dependency list carries only P3 contracts | Solution architect | Resolved (directive) |
| GAP-0868 | The rule-change request record while the registry, the load gate and the approval belong to other stories | Tech lead of rwb-access | Resolved (directive) |
| GAP-0870 | Treatment policy edition: the P3 reference-load contract is not a declared dependency, the table code, the workbook part names, the field detail and the record code are unspecified, and the four sources conflict on who holds the right | Solution architect | Resolved (directive) |
| GAP-0991 | The attach operation, its right and the attach event name differ between the legacy story, the TSD and the Arch v5 event catalogue | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0992 | The intake-match contract baseline fixes shapes and paths the sources do not name at field level, and the plan's C list omits the two rwb-case reads | Tech lead | Resolved (directive) |
| GAP-0993 | The compute, storage, hold-container and scanning capacity values of the intake-match path are not specified | SCB IT infrastructure | Resolved (directive) |
| GAP-0994 | The Schedule window, the catch-up policy, the alert thresholds and the lag-alert identifier of the intake path are not specified | DevOps team | Resolved (directive) |
| GAP-1002 | The classify run is drawn as an rwb-agent child while the legacy story calls the P10 model gateway in process, and no source names the model provider, endpoint or model version | Solution architect with the TechX tech lead of rwb-document and the rwb-agent owner | Resolved (directive) |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1012 | The channel pickup has no target shape of its own: the run record, the rerun operation, the channel property layout, the single-run rule and the cross-service partner read are named by the legacy story only | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1168 | RWB-P6-E1011-APP: the parameters and reference-data contracts of rwb-case and the rwb-source-data contract the run reads are missing from the story's C list | Solution architect | Resolved (directive) |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1197 | The request and answer shape of the letter-copy handoff, the document type and source the hub assigns, the notice parameters, the P1 recipient field IDs, the payload field names of the event and the notice screen identifier are all unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1199 | No source describes the letter copy becoming an intake item at the document hub, and FSD P6 keeps a generated document as a stored document on the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1200 | The P6 module declares no notice parameter, so DP-06 has no named value to read | Business analyst | Resolved (directive) |
| GAP-1201 | The legacy access case and the legacy attach cases have no subject in rwb-comms, so the carried test cases prove the notice read instead | Test lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1202 | The event catalogue names rwb-decision as the only consumer of NoticeGenerated, while the document hub is expected to turn the copy into an intake item | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1203 | The base documents of the story are in review, not approved | Business analyst | Resolved (directive) |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1214 | RWB-P6-E1073-APP: the local copy table and its columns, the parameter read path, the two added check names and the local run record are not specified in the source documents | Solution architect | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1406 | The client artefact coordinates, the owner of the cache time to live, the refresh event name and the exact build-check rule set are not specified | Platform team (PLT) architect with rwb-case (P3) and the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1407 | The published catalog and value contract, the operation status codes as a library contract, the refresh event name and the start-up error surface are not specified | Platform team (PLT) contract owner with rwb-case (P3) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1408 | The chart values, the seed ordering, the probe and the alert thresholds of the library are not specified | Platform team (PLT) DevOps engineer with rwb-case (P3) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1409 | Reference-data client artefact coordinates, the cache time-to-live catalog entry, the refresh rule with no change event and the client-to-kit boundary are not specified | Platform team (PLT) architect with the rwb-case and rwb-decision owners | Resolved (directive) |
| GAP-1410 | The published reference-data client contract, the version and row data contract, the LOV-REF-TABLE code list and the no-version failure surface are not specified in a technical specification | Platform team (PLT) contract owner with the rwb-case owner | Resolved (directive) |
| GAP-1558 | The parameter and reference-data load interface is claimed by P4 in the API specification and by P3 in the default ruling | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2150 | The worked example is a monolith story key with no service and no realignment equivalent | Document owner; analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2190 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the acceptance event name, the list codes, the case-decision proposal path, the route path, the feature flag home, the topic and migration values and the policy values the gate reads are not specified | Solution architect with the P10 service owner and the owners of rwb-case, rwb-decision and rwb-source-data | Resolved (directive) |
| GAP-2191 | Case intake agent at L1 contract in rwb-agent: the member types of the answer and of the request, the acceptance event name, the case-decision proposal path, the route path, the 409 rule, the item key set, the invalid-verdict refusal and the policy values are not specified | Tech lead of rwb-agent with the solution architect and the owners of rwb-case and rwb-decision | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2210 | No source gives the case status history, the transfer from-queue or the decision-record read behind the timeline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2211 | No source fixes the v1.1 timeline item shape, the section state or its version against the RWB-P3-E1023-CON baseline | Solution architect | Resolved (directive) |
| GAP-2212 | The parameter version event has no place in the rwb-case event catalogue | Solution architect | Resolved (directive) |
| GAP-2213 | The run-time read of the catalog by the other 18 services has no published operation, right or key artefact | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2214 | The target form of the names, migration numbers and catalog key that survived the monolith is not restated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2215 | The rights of the four operations are not republished under the rwb-case ownership | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2241 | The list code and the table code of the age-band reference list are not named | TechX, with the data steward RW-DATASTEW | Resolved (directive) |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2281 | The panel-change operation, its fields, the table code, the record code, the compensation, the screen and two owner contracts are not in the sources | Tech lead of rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2284 | The rwb-decision decision-log and rule-catalog contract this QA sample consumes is not in the WP contract-dependency list, and four of its values are named nowhere in the read sources | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2335 | The two DP-11 contract reads of the legacy in-process calls are absent from the Work Package dependency rows and DP-08 is not among the patterns | Solution architect | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2444 | DOCATT attach entry has no defined field set for the document reference, the intake item, the match method, the confidence, the final call and the message id | Solution architect, P7 | Resolved (directive) |
| GAP-2445 | The decision code list in force does not enumerate DOCATT in any source readable here | Reference data administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2446 | Whether an item held for a person leaves a decision record is not stated | Business analyst, P7 | Resolved (directive) |
| GAP-2447 | The DecisionRecorded payload of an attach has no defined field set | Solution architect, integration | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2449 | Login name, parameter names and message texts are not written in any source readable here | Tech lead, P7 | Resolved (directive) |
| GAP-2450 | The trigger of the ledger completeness check is not stated | Solution architect, P7 | Resolved (directive) |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-3137 | The partner slice of RWB-E1-032 and its target service frame are not stated in any source | Solution architect | Resolved (directive) |
| GAP-3138 | The partner-origin channel of an intake item and its attach state are a boundary no source states | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3139 | Wave conflict: EP01 puts this story in wave 1 while rwb-partner is wave 4 in Arch v5 | Tech lead | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3141 | The two partner submission operations, the intake creation path and the PartnerDocumentSubmitted event are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3142 | The intake bound, the decision code and version, and the two lists in force are not named | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3143 | No data model carries a partner-side submission row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3144 | No source states how the legacy criteria split between the document-hub and partner slices | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3145 | The partner portal screen that submits a file is not fixed | Business analyst | Resolved (directive) |
| GAP-3174 | Service S9 takes Epic 1 stories in wave 1 although its Arch v5 wave is 4 | Delivery lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
