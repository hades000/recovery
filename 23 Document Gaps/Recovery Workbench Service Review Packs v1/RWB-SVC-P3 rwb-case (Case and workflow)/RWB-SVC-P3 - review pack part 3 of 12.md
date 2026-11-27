# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 3 of 12 (RWB-P3-E1021-OPS to RWB-P3-E1031-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 173 |
| Cross-document (pending in another document) | 190 |
| Not applied (value not in the sources) | 9 |
| Open business decisions | 22 |
| Register gaps linked | 46 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E1021-OPS | 14 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1021 OPS Transfer rules and engine v1 - deployment v2.md |
| RWB-P3-E1023-APP | 27 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1023 APP Case record view v1, read only v2.md |
| RWB-P3-E1023-CON | 9 | 20 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1023 CON Case record view v1, read only - contract v2.md |
| RWB-P3-E1028-APP | 24 | 20 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1028 APP Service levels, timers, escalation and prescription dates v2.md |
| RWB-P3-E1028-CON | 16 | 25 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1028 CON Service levels, timers, escalation and prescription dates - contract v2.md |
| RWB-P3-E1028-OPS | 15 | 16 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1028 OPS Service levels, timers, escalation and prescription dates - deployment v2.md |
| RWB-P3-E1030-APP | 17 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1030 APP Daily rebalancing and queue measures v2.md |
| RWB-P3-E1030-CON | 7 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1030 CON Daily rebalancing and queue measures - contract v2.md |
| RWB-P3-E1030-OPS | 12 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1030 OPS Daily rebalancing and queue measures - deployment v2.md |
| RWB-P3-E1031-APP | 12 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1031 APP Queue and owner on the case list with filters v2.md |
| RWB-P3-E1031-CON | 20 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1031 CON Queue and owner on the case list with filters - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E1028-APP | R-10256 | CG-ALL-3616 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1031-APP | R-10270 | CG-ALL-3681 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-P3-E1031-CON | R-10273 | CG-ALL-3688 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1031-CON | R-10274 | CG-ALL-3692 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-ITG-E1021-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-22012 | GAP-3078 | Register gap | P7 rwb-decision owner with the business owner of module S8 | The TRANSFER rows that fire on the deviation triggers and the text of R-DEV-04 to R-DEV-06 are not published | The rule owner publishes the DEV transfer rows and the text of R-DEV-04 to R-DEV-06 with the package version; the story then reads them unchanged and no code changes. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1023-ITG, RWB-ITG-E2016-ITG, RWB-P3-E1023-APP, RWB-P3-E1023-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P4-E1023-APP, RWB-P5-E2016-APP, RWB-S8-E1023-APP | R-28538 | GAP-1577 | Register gap | Business analyst with the P3 product owner | The case record view and its history timeline are listed as P4 features while the screen and its endpoints belong to rwb-case | Move FEAT-ACA-11 and FEAT-ACA-12 with their acceptance criteria to FSD P3 in the next version, and leave in FSD P4 only the authorise, scope and masking behaviour the screen consumes, so each feature has one owner and one acceptance set. |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-28627 | GAP-2248 | Register gap | Business lead | The role that receives the expiry of a notice period is not named | Take the escalation role from the SERVICE_LEVEL row in force as ASM-B2-P3-016-6 records, and add a named default role for a missing row if the business lead asks for one. |
| RWB-P3-E1031-APP | R-33410 | ASM-ALL-3681 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-P3-E1031-CON | R-33411 | ASM-ALL-3692 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-P3-E1021-APP, RWB-P3-E1021-OPS | R-36261 | ASM-1236 | Register assumption |  | A transfer refused by the TRANSFER rule, the cap check, the status check or the hold check is final in Epic 1: there is no override path, nothing changes, and the caller may retry with another target owner or queue. | Business owner, case and workflow |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E1023-CON | R-15884 | DOR-RWB-P3-E1023-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | No BR ID for CB1 to CB6 exists in the story or the project sources (searched for the CB rows and BR ID). Assigning one would invent a value. |
| RWB-P3-E1028-APP | R-05018 | DOR-RWB-P3-E1028-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off date for RWB-SVC-P3 in the story or sources; a search found none. Sign-off cannot be confirmed, so nothing entered. |
| RWB-P3-E1028-APP | R-05019 | DOR-RWB-P3-E1028-APP-16 |  | Definition of Ready item 16 Size: Fail | No size in the story or sources; the squad sizes at refinement. Entering a size would invent a value. |
| RWB-P3-E1028-APP | R-05021 | DOR-RWB-P3-E1028-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version recorded as published in the story or sources; sections 3 and 12.8 name the fakes without a version. Nothing entered. |
| RWB-P3-E1028-CON | R-24903 | CG-ALL-3638 | 16 | Criteria and tests keep legacy job and decision-log wording | TC-06 corrected, but AC6 in section 7 still carries legacy job and decision-log wording; item remains open. |
| RWB-P3-E1028-OPS | R-05028 | DOR-RWB-P3-E1028-OPS-14 | Header (Item table) | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source documents. Placeholder row added; sign-off cannot be confirmed without an invented reference. |
| RWB-P3-E1028-OPS | R-05031 | DOR-RWB-P3-E1028-OPS-22 | Header (Item table) | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in the story or sources. Placeholder row added; the version cannot be invented. |
| RWB-P3-E1028-OPS | R-24908 | CG-ALL-3651 | 7, 16 | Criteria and tests keep legacy job and decision-log wording | TC-04 updated to workflow wording, but AC4 in section 7 still carries legacy job wording and needs its own edit; item not fully resolved. |
| RWB-P3-E1031-APP | R-15934 | DOR-RWB-P3-E1031-APP-18 | 8, 13, 15 | Definition of Ready item 18 Open decisions: Partial | DL31 is in Decision Log v11 row 57 with no ASM ID. No ASM ID exists in any source, so none can be cited. Story sections 8, 13 and 15 were not in this chunk, so no edit. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (20)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05635 | RWB-P3-E1021-OPS | CG-ALL-3577 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseStateChanged.v1 (EV-05) with its ACL, or drop the handler from section 12.4. |
| CDC-05636 | RWB-P3-E1021-OPS | CG-ALL-3578 | 12.4 | Add rwb-case as a consumer of rwb.decision.ApprovalRequested.v1 (EV-09) with its ACL, or drop the handler from section 12.4. |
| CDC-05639 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-8 | 12 | Add P2 rwb-case as consumer of rwb.case.CaseStateChanged.v1 and of rwb.decision.ApprovalRequested.v1 |
| CDC-05644 | RWB-P3-E1021-OPS | GAP-3079 | find it | Owners publish the case trigger event names before the release date; consumer groups and fact mapping then bind to the published names. |
| CDC-05692 | RWB-P3-E1028-APP | CG-ALL-3608 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseCreated.v1 on Events row EV-01 and extend its ACL. |
| CDC-05693 | RWB-P3-E1028-APP | CG-ALL-3609 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseAllocated.v1 on Events row EV-02 and extend its ACL. |
| CDC-05694 | RWB-P3-E1028-APP | CG-ALL-3610 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseTransferred.v1 on Events row EV-04 and extend its ACL. |
| CDC-05695 | RWB-P3-E1028-APP | CG-ALL-3611 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseStateChanged.v1 on Events row EV-05 and extend its ACL. |
| CDC-05712 | RWB-P3-E1028-CON | CG-ALL-3628 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseCreated.v1 (EV-01) and add its ACL. |
| CDC-05713 | RWB-P3-E1028-CON | CG-ALL-3629 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseAllocated.v1 (EV-02) and add its ACL. |
| CDC-05714 | RWB-P3-E1028-CON | CG-ALL-3630 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseTransferred.v1 (EV-04) and add its ACL. |
| CDC-05715 | RWB-P3-E1028-CON | CG-ALL-3631 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseStateChanged.v1 (EV-05) and add its ACL. |
| CDC-05728 | RWB-P3-E1028-CON | GAP-2203 |  | Add escalated_to_role and escalated_at rows and the TimerBreached payload field list; type, length and optionality Not specified in the source documents (GAP-2203) |
| CDC-05739 | RWB-P3-E1028-OPS | CG-ALL-3647 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseCreated.v1 in the Events catalog row EV-01, with its ACL. |
| CDC-05753 | RWB-P3-E1030-APP | CG-ALL-3654 | 12.4 | Add rwb-case as a consumer of rwb.case.TimerBreached.v1 (EV-19) and add its ACL. |
| CDC-05754 | RWB-P3-E1030-APP | DOR-RWB-P3-E1030-APP-8 | 8 | Register rwb-case as a consumer of rwb.case.TimerBreached.v1. |
| CDC-05766 | RWB-P3-E1030-CON | CG-ALL-3662 | 12.4 | Add rwb-case as a consumer of rwb.case.TimerBreached.v1 (EV-19) and its ACL. |
| CDC-05771 | RWB-P3-E1030-CON | DOR-RWB-P3-E1030-CON-8 | find it | Add P2 rwb-case as a consumer of rwb.case.TimerBreached.v1. |
| CDC-05784 | RWB-P3-E1030-OPS | CG-ALL-3666 | 12.4 | Add rwb-case as consumer of rwb.case.TimerBreached.v1 (Events row EV-19) and add its ACL. |
| CDC-05787 | RWB-P3-E1030-OPS | DOR-RWB-P3-E1030-OPS-8 | find it | Register P2 rwb-case as a consumer of rwb.case.TimerBreached.v1. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05648 | RWB-P3-E1021-OPS | CG-ALL-3581 | 18 | Align the test lists of REQ-CWC-010 and REQ-CWC-016 with section 18 using the TC-P3-E1021-OPS IDs. |
| CDC-05664 | RWB-P3-E1023-APP | CG-ALL-3589 | 18 | Align the traced test lists of the five requirements with RWB-P3-E1023-APP section 18 in the next RTM version. |
| CDC-05684 | RWB-P3-E1023-CON | CG-ALL-3597 | 18 | Align the test lists for the five requirements in section 18 of RWB-P3-E1023-CON and in RTM v7 in their next versions. |
| CDC-05702 | RWB-P3-E1028-APP | CG-ALL-3615 | 18 | REQ-CWC-011 (row 35) test case list to add TC-E1-028-07, TC-E1-028-08, TC-E1-028-10, TC-E1-028-11 and TC-E1-028-14 so it matches §18 of RWB-P3-E1028-APP; the REQ-CWC-012 and third-requirement rows were truncated in the evidence and are not in the excerpts. |
| CDC-05727 | RWB-P3-E1028-CON | CG-ALL-3636 | 18 | Align the test lists for REQ-CWC-011, REQ-CWC-012 and the third differing requirement to section 18 of RWB-P3-E1028-CON |
| CDC-05744 | RWB-P3-E1028-OPS | CG-ALL-3650 | 18 | Align the test lists for REQ-CWC-011, REQ-CWC-012 and the other listed requirement to section 18 of this story. |
| CDC-05757 | RWB-P3-E1030-APP | CG-ALL-3655 | 18 | Align REQ-CWC-015 and REQ-RDF-012 test-case lists to RWB-P3-E1030-APP section 18 in the next RTM version. |
| CDC-05776 | RWB-P3-E1030-CON | CG-ALL-3664 | 18 | Align the test lists of REQ-CWC-015 and REQ-RDF-012 between section 18 and the RTM in their next versions. |
| CDC-05791 | RWB-P3-E1030-OPS | CG-ALL-3668 | 18 | Align the REQ-CWC-015 and REQ-RDF-012 test lists to RWB-P3-E1030-OPS section 18 in the next RTM version. |
| CDC-05804 | RWB-P3-E1031-APP | DOR-RWB-P3-E1031-APP-12 | 12.7, 16 | Story side: added TC-E1-031-10 for the section 12.7 tables; section 18 was not changed; the RTM v7 test lists are not in this document (DOR-RWB-P3-E1031-APP-12). |
| CDC-05807 | RWB-P3-E1031-APP | CG-ALL-3675 | 18 | Align the test lists of REQ-CWC-007 and REQ-ACA-009 with RWB-P3-E1031-APP section 18 in the next RTM version |
| CDC-05816 | RWB-P3-E1031-CON | CG-ALL-3687 | 18 | Align the test lists of REQ-CWC-007, REQ-ACA-009, REQ-ACA-006 and REQ-ACA-005 with section 18 of RWB-P3-E1031-CON at the RTM's next version. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05640 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-9 | 14 | MSG-P3-027 now carries the standard text (CG-ALL-3579); the rest of the message catalogue is owned by the standard. |
| CDC-05671 | RWB-P3-E1023-CON | CG-ALL-3595 | 4, 14 | Add a new message ID, assigned by the standard owner, for 'No session or an expired session' with the text 'You are not signed in. Sign in to continue.' Then RWB-P3-E1023-CON §14 cites it. |
| CDC-05696 | RWB-P3-E1028-APP | CG-ALL-3613 | 14 | Add a new message ID for 'No session on a read' with text 'Your session has ended. Sign in again.'; story §14 then cites that ID in place of MSG-P4-001. |
| CDC-05716 | RWB-P3-E1028-CON | CG-ALL-3633 | 4, 14 | Add a new message ID for 'A request or a response fails schema validation' with text 'The request could not be read: {detail}.'; the story then cites it. |
| CDC-05717 | RWB-P3-E1028-CON | CG-ALL-3634 | 4, 14 | Add a new message ID for 'No session on a read' with text 'Your session has ended. Sign in again.'; the story then cites it. |
| CDC-05720 | RWB-P3-E1028-CON | DOR-RWB-P3-E1028-CON-9 | 14 | Align the meaning of MSG-P3-030 and MSG-P4-001 with the platform envelope use in section 14 of this story, or record the other meaning. |
| CDC-05803 | RWB-P3-E1031-APP | CG-ALL-3674 | 4, 14 | Add a message ID for 'No valid session' so MSG-P4-001 keeps its standard meaning; the story then cites the new ID. |
| CDC-05805 | RWB-P3-E1031-APP | DOR-RWB-P3-E1031-APP-9 | 14 | Add a message ID for 'No valid session' so the MSG-P4-001 use in section 14 matches the standard (see CG-ALL-3674). |
| CDC-05813 | RWB-P3-E1031-CON | DOR-RWB-P3-E1031-CON-9 | 14 | Confirm the meaning of MSG-P4-001 against the standard entry; this story uses only MSG-P4-002. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05647 | RWB-P3-E1021-OPS | CG-ALL-3580 | 16 | Add rows TC-P3-E1021-OPS-01 to TC-P3-E1021-OPS-05 with Given, When and Then copied from the criterion each covers. |
| CDC-05655 | RWB-P3-E1023-APP | CG-ALL-3587 | 16 | Add rows TC-E1-023-12 (A-7001 balance changed by 2026-12-03 ALS batch, BR8) and TC-E1-023-13 (case link A-7010 with no view row, AC14) with Given, When, Then |
| CDC-05683 | RWB-P3-E1023-CON | CG-ALL-3596 | 16 | Add rows TC-P3-E1023-CON-01 to TC-P3-E1023-CON-06 to the next Test Cases version, with Given, When and Then copied from the criterion each covers. |
| CDC-05697 | RWB-P3-E1028-APP | CG-ALL-3614 | 16 | Add TC-E1-028-14 to tab Story test cases with Given, When and Then copied from AC12 |
| CDC-05726 | RWB-P3-E1028-CON | CG-ALL-3635 | 16 | Add rows TC-P3-E1028-CON-01 to TC-P3-E1028-CON-06 with Given, When and Then copied from the criteria they cover |
| CDC-05743 | RWB-P3-E1028-OPS | CG-ALL-3649 | 16 | Add rows TC-P3-E1028-OPS-01 to TC-P3-E1028-OPS-06 with Given, When and Then copied from the criterion each covers. |
| CDC-05775 | RWB-P3-E1030-CON | CG-ALL-3663 | 16 | Add rows for TC-P3-E1030-CON-01 to TC-P3-E1030-CON-05 with Given, When and Then copied from the criterion each covers. |
| CDC-05790 | RWB-P3-E1030-OPS | CG-ALL-3667 | 16 | Add rows for TC-P3-E1030-OPS-01 to TC-P3-E1030-OPS-05 with Given, When and Then copied from AC1 to AC5 of section 7. |
| CDC-05815 | RWB-P3-E1031-CON | CG-ALL-3685 |  | TC-E1-031-07 keeps AC2, AC6 (the no-owner row) and TC-E1-031-08 keeps AC5, AC6 (the 10,000-row limit); the AC labels differ from Test Cases v8, so the correction sits in Test Cases v8. |

### RWB-S8-E1023-APP (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05662 | RWB-P3-E1023-APP | GAP-3081 |  | Publish the five read paths on /api/recovery/deviation/v1, declare the four consumed operations as placeholders, carry dataAsOf and freshness, and declare the rwb-access authorise, mask and AC-READ accept as one consumed operation. |
| CDC-05663 | RWB-P3-E1023-APP | GAP-3083 |  | Keep acs empty in the fragment; restate AC1 to AC12 as new (D-RCV-60) with the legacy values; keep TC-E1-023-01 to -13 unchanged; record the mapping in section 18. |
| CDC-05665 | RWB-P3-E1023-APP | GAP-3084 | 15 | Wave paragraph removed from this story |
| CDC-05666 | RWB-P3-E1023-APP | GAP-3082 | 15 | Rwb-deviation placement sentence removed; seven platform prerequisites kept |
| CDC-05676 | RWB-P3-E1023-CON | GAP-0348 | find it | Confirm case-scoped deviation read with S8 owner; treat rwb-deviation as SIT-available for wave 1; keep W1J01 synthetic fixture |
| CDC-05680 | RWB-P3-E1023-CON | GAP-3081 | find it | Publish five read paths on /api/recovery/deviation/v1; declare four consumed operations as placeholders; carry dataAsOf and per-product freshness; confirm with owners |
| CDC-05681 | RWB-P3-E1023-CON | GAP-3083 | 7, 16, 18 | Restate AC1 to AC12 as new (D-RCV-60) with the RWB-E1-023 section 7 values; carry TC-E1-023-01 to TC-E1-023-13 unchanged; map TC-E1-023-11 to the access refusal; record the mapping in section 18 |
| CDC-05685 | RWB-P3-E1023-CON | GAP-3084 |  | Keep wave 1 and release 30 November 2026 marked tentative; read caserecord.section.timeout.ms and the six lists as rwb-case parameters and reference data; confirm the parameter row with the P3 owner before tag. |
| CDC-05686 | RWB-P3-E1023-CON | GAP-3082 |  | Keep service, lane, C row and empty H row; record the slice as secondary serving with deviation block; declare the seven platform contracts as build prerequisites and fakes; keep wave 1 and mark release tentative. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05724 | RWB-P3-E1028-CON | GAP-2202 | 12.2 | Add rows for accountDates(List<UUID>) and holidays(LocalDate, LocalDate) with query and answer shape; record in the P3 contract which operation carries the wave 1 pause |
| CDC-05729 | RWB-P3-E1028-CON | GAP-0022 |  | Record PLT as owner of retired EV-18 TimerDue; keep P3 as owner of EV-19 TimerBreached |
| CDC-05742 | RWB-P3-E1028-OPS | GAP-2202 | 12.2 | Add two P1 rows: accountDates(List<UUID>) and holidays(LocalDate, LocalDate) with query and answer shape; record which P3 operation carries the wave 1 pause. |
| CDC-05746 | RWB-P3-E1028-OPS | GAP-0022 | none | Record PLT as owner of the retired TimerDue event (EV-18) and keep P3 as owner of TimerBreached (EV-19). |
| CDC-05756 | RWB-P3-E1030-APP | GAP-2205 | 8 | Add rows for the rwb-reporting feed, the delivery service of MSG-P3-028, MSG-P3-011 and MSG-P3-029, and the run record and rerun surface once agreed in the P9 contract. |
| CDC-05774 | RWB-P3-E1030-CON | GAP-2205 | find it | Name the reporting feed and its fields in the P9 contract before wave 1 closes; name the delivery service for MSG-P3-011, MSG-P3-028 and MSG-P3-029; state whether the run record and rerun are a workflow read plus Schedule trigger or a published operation; add the agreed rows to the Ownership Map. |
| CDC-05778 | RWB-P3-E1030-CON | GAP-2206 | find it | State whether a business date's run is readable as a document resource; if so, add the operation and ownership row, and publish the run record schema in v1 before the reporting consumer builds against it. |
| CDC-05788 | RWB-P3-E1030-OPS | GAP-1652 | find it | P9 stops computing queue depth, ageing and owner spread; P3 publishes the queue measures for the business date and P9 reads them, reconciled to the case list count. |
| CDC-05789 | RWB-P3-E1030-OPS | GAP-2205 | find it | Name the reporting feed fields, the three-message delivery service (ACE notification path or rwb-comms) and the run record and rerun surface before wave 1 closes. |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05631 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-14 | header | Record the signed epic design sign-off for this story's epic, or confirm that none exists, so DOR item 14 can be re-tested. |
| CDC-05668 | RWB-P3-E1023-CON | DOR-RWB-P3-E1023-CON-14 | none | Confirm and record the signed epic design sign-off. The story and its sources hold no sign-off reference or date. |
| CDC-05749 | RWB-P3-E1030-APP | DOR-RWB-P3-E1030-APP-14 | none | Record the signed epic design sign-off; none is recorded in the sources. |
| CDC-05764 | RWB-P3-E1030-CON | DOR-RWB-P3-E1030-CON-14 | Metadata | Record the signed epic design sign-off for service epic RWB-SVC-P3. |
| CDC-05781 | RWB-P3-E1030-OPS | DOR-RWB-P3-E1030-OPS-14 | header | Record the signed epic design sign-off for EP01. |
| CDC-05798 | RWB-P3-E1031-APP | DOR-RWB-P3-E1031-APP-14 | 14 | Record the signed epic design sign-off for RWB-P3-E1031-APP. |
| CDC-05810 | RWB-P3-E1031-CON | DOR-RWB-P3-E1031-CON-14 |  | Record the signed epic design sign-off. No signed epic design is in the source documents, so none is written into the story. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05637 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-1 | 1 | Add the role 'DevOps engineer' named in section 1, or give it a role code; no edit in this story |
| CDC-05718 | RWB-P3-E1028-CON | DOR-RWB-P3-E1028-CON-1 | 1 | Add 'tech lead' as a role name or role code, or point the §1 role at a role already listed there. |
| CDC-05740 | RWB-P3-E1028-OPS | DOR-RWB-P3-E1028-OPS-1 | 1 | Add a role named platform engineer, or map this story role to an existing role code in Users Roles and Permissions v5. |
| CDC-05767 | RWB-P3-E1030-CON | DOR-RWB-P3-E1030-CON-1 | 1 | Add a role code or name for the consumer of the case service (any service or the gateway-bff). |
| CDC-05785 | RWB-P3-E1030-OPS | DOR-RWB-P3-E1030-OPS-1 | 1 | Add a role code and role name for DevOps engineer, or name the role this story uses. |
| CDC-05811 | RWB-P3-E1031-CON | DOR-RWB-P3-E1031-CON-1 | 1 | Register 'tech lead' as a role code or role name, or name the existing role code the persona maps to. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05667 | RWB-P3-E1023-CON | CG-ALL-3598 | 3 | The P3 naming row must rule a rwb-case package segment that is not the Java reserved word case; the story then copies it |
| CDC-05710 | RWB-P3-E1028-CON | CG-ALL-3637 | 2 | Rule a Java package segment for rwb-case that is not the Java reserved word 'case' and update the package row (row 371, currently th.co.scb.ace.workbench.recovery.case); the story then copies the ruled name. |
| CDC-05763 | RWB-P3-E1030-CON | CG-ALL-3665 | 1 | Java package line now cites the Template Spec v1 package with no architect attribution |
| CDC-05796 | RWB-P3-E1031-APP | CG-ALL-3676 | 1, 13 | Rule the package segment that replaces the Java reserved word 'case' for the rwb-case service; sections 1 and 13 then copy it |
| CDC-05797 | RWB-P3-E1031-APP | CG-ALL-3677 | 13 | Rule the package segment for the caselist module under the rwb-case package (replaces the reserved word 'case'); section 13 then copies it |
| CDC-05809 | RWB-P3-E1031-CON | CG-ALL-3689 | 2 | Rule the Java package segment for the rwb-case service and publish the ruled package: the segment `case` in th.co.scb.ace.workbench.recovery.case is a Java reserved word, so that package does not compile. RWB-P3-E1031-CON copies the ruled segment. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05687 | RWB-P3-E1028-APP | CG-ALL-3601 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{accountId} through the provider's CON story. |
| CDC-05688 | RWB-P3-E1028-APP | CG-ALL-3602 | 12.2 | Publish GET /api/recovery/source-data/v1/calendar/holidays?from={from}&to={to} through the provider's CON story. |
| CDC-05707 | RWB-P3-E1028-CON | CG-ALL-3622 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{accountId} in paths through the provider CON story, or the consumer switches to a published operation. |
| CDC-05708 | RWB-P3-E1028-CON | CG-ALL-3623 | 12.2 | Publish GET /api/recovery/source-data/v1/calendar/holidays?from={from}&to={to} in paths through the provider CON story, or the consumer switches to a published operation. |
| CDC-05732 | RWB-P3-E1028-OPS | CG-ALL-3641 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{accountId} through the provider's CON story, or the consumer switches to a published operation. |
| CDC-05733 | RWB-P3-E1028-OPS | CG-ALL-3642 | 12.2 | Publish GET /api/recovery/source-data/v1/calendar/holidays through the provider's CON story, or the consumer switches to a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05689 | RWB-P3-E1028-APP | CG-ALL-3603 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-05709 | RWB-P3-E1028-CON | CG-ALL-3624 | 12.2 | Publish POST /api/recovery/access/v1/authorise in paths through the provider CON story, or the consumer switches to a published operation. |
| CDC-05734 | RWB-P3-E1028-OPS | CG-ALL-3643 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer switches to a published operation. |
| CDC-05794 | RWB-P3-E1031-APP | CG-ALL-3672 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider CON story. |
| CDC-05795 | RWB-P3-E1031-APP | CG-ALL-3673 | 12.2 | Publish operation POST /api/recovery/access/v1/access-events in rwb-access.yaml through the provider CON story. |
| CDC-05802 | RWB-P3-E1031-APP | DOR-RWB-P3-E1031-APP-8 | 14 | Publish POST /api/recovery/access/v1/authorise and POST /api/recovery/access/v1/access-events in rwb-access.yaml. |

### RWB-P3-E1030-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05750 | RWB-P3-E1030-APP | DOR-RWB-P3-E1030-APP-21 | none | Set build status to Done once the contract is published. |
| CDC-05752 | RWB-P3-E1030-APP | DOR-RWB-P3-E1030-APP-23 | 12.1 | No contract version in the sources; RWB-P3-E1030-CON must fix it. Story marks it Not specified. |
| CDC-05760 | RWB-P3-E1030-APP | GAP-2206 | 8 | Story marks the consumer read path Not specified; the contract still needs the run record shape. |
| CDC-05782 | RWB-P3-E1030-OPS | DOR-RWB-P3-E1030-OPS-21 | header | Set build status to Done once the contract is published. |
| CDC-05783 | RWB-P3-E1030-OPS | DOR-RWB-P3-E1030-OPS-22 | 12 | Publish a contract fake library version and record it as published. |
| CDC-05793 | RWB-P3-E1030-OPS | GAP-2206 | find it | Publish the run record schema in version 1 and state whether a business date's run is readable as a document resource; add the operation and ownership row if so. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05638 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-12 | 12, 12.7, 16, 18 | Register TC-P3-E1021-OPS-01 to -07 in Test Cases v8; align the section 18 test lists with RTM v7 |
| CDC-05672 | RWB-P3-E1023-CON | DOR-RWB-P3-E1023-CON-12 | 12.7, 16, 18 | Add TC-P3-E1023-CON-01 to -07 to Test Cases v8. Align the RWB-P3-E1023-CON test lists in RTM v7 with §18 of the story. |
| CDC-05768 | RWB-P3-E1030-CON | DOR-RWB-P3-E1030-CON-12 | 12.7, 16, 18 | Test Cases v8: add TC-P3-E1030-CON-01 to -07. RTM v7: align the P3 test lists in section 18 with section 16. |
| CDC-05786 | RWB-P3-E1030-OPS | DOR-RWB-P3-E1030-OPS-12 Test cases: Partial | 12, 12.7, 16, 18 | Story adds AC6 to AC11 and TC-06 to TC-11 for contract, tables, redelivery, status, and rule coverage; registry and RTM rows are outside this story. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05654 | RWB-P3-E1023-APP | CG-ALL-3584 | 13 | Confirm LOV-CONTACT-TYPE is a Reference Data v5 list or switch the story to an existing v5 list; no replacement list is named in the sources. |
| CDC-05656 | RWB-P3-E1023-APP | DOR-RWB-P3-E1023-APP-20 | 12.7 | Add LOV-CONTACT-TYPE so reference_row LOV-CONTACT-TYPE in §12.7 resolves |
| CDC-05670 | RWB-P3-E1023-CON | CG-ALL-3594 | 12.7 | Add the list LOV-CONTACT-TYPE, or name an existing Reference Data v5 list to use in its place. RWB-P3-E1023-CON §12.7 names LOV-CONTACT-TYPE. |
| CDC-05673 | RWB-P3-E1023-CON | DOR-RWB-P3-E1023-CON-20 | 11 | Add list LOV-CONTACT-TYPE (P2) to Reference Data v5 |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05630 | RWB-P3-E1021-OPS | CG-ALL-3576 | 13 | Create the story file RWB-P7-E1073-CON, or name the existing story that provides the rule-package contract, so the C RWB-P7-E1073-CON reference resolves. |
| CDC-05632 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-17 | header | Create the story file for RWB-P7-E1073-CON or name an existing story as the dependency, then record it in the header dependency rows. |

### RWB-P3-E1021-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05633 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-21 | header | Build RWB-P3-E1021-CON to Done and publish its contract, so the contract is published before this story starts. |
| CDC-05634 | RWB-P3-E1021-OPS | DOR-RWB-P3-E1021-OPS-22 | header | Publish the contract fake for RWB-P3-E1021-CON and record its library version. |

### OTHER:BRD section 8.2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05641 | RWB-P3-E1021-OPS | GAP-1456 | find it | State that Epic 1 stories keep the business-epic wave; delivery lead confirms the wave per story at build sequencing |
| CDC-05657 | RWB-P3-E1023-APP | GAP-1456 |  | State the rule that Epic 1 requirement stories keep business-epic wave 1 while the receiving service starts in its own Arch v5 wave; delivery lead confirms the wave per story at build sequencing. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05642 | RWB-P3-E1021-OPS | GAP-3076 | find it | Each owner publishes the operation name of its consumed row before the release date; a published name replaces the placeholder in a minor contract version. |
| CDC-05722 | RWB-P3-E1028-CON | GAP-2277 | 11 | Declare ServiceLevelLoad, ServiceLevelRow and RunningTimerEffect, the load state set, and the 422 and 409 bodies; then freeze them as the fake pack. |

### RWB-PLT-NF06-DB (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05646 | RWB-P3-E1021-OPS | GAP-0688 | find it | Name the rwb-case database login and its grant set; the chart then takes it by vault secret reference. |
| CDC-05651 | RWB-P3-E1021-OPS | GAP-1037 | none | Allocate the rwb-document login name, its grants (schema rwb_document only) and its secret reference, and record them in the service catalogue. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05653 | RWB-P3-E1023-APP | GAP-0693 | 13 | Publish the SCR-03 gateway-bff route: path, parallel call set, merge field map, 2 s budget split and partial-failure rule. Keep the five rwb-case read operations unchanged. |
| CDC-05669 | RWB-P3-E1023-CON | GAP-0693 | none | Publish the gateway-bff composite route for SCR-03 with its path, the parallel call set to rwb-case and rwb-source-data, the merge field map, the 2 s budget split and the partial-failure rule. Keep the five rwb-case read operations unchanged. |

### OTHER:RWB-PLT-DB (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05659 | RWB-P3-E1023-APP | GAP-0692 |  | Issue the rwb-case database login (DP-02) with its name published when RWB-PLT-DB issues it; grant SELECT, INSERT and UPDATE on schema rwb_case only. |
| CDC-05677 | RWB-P3-E1023-CON | GAP-0692 | 8 | Issue the rwb-case database login per DP-02 and grant SELECT, INSERT and UPDATE on schema rwb_case only |

### OTHER:rwb-source-data contract (P1) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05660 | RWB-P3-E1023-APP | GAP-0695 | 4 | §4 step 7 orders by time and names the rwb-source-data contract for the page size and interaction read (BR13); the contract's paging values are Not specified in the source documents (GAP-0695). |
| CDC-05678 | RWB-P3-E1023-CON | GAP-0695 | 11 | Timeline paging and order are fixed by no source; the row keeps paging Not specified in the source documents (GAP-0695) and the order and page size sit in the P1 contract. |

### RWB-P4-E1039-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05661 | RWB-P3-E1023-APP | GAP-0694 | 4 | §4 step 8 sends the field IDs read to GET /masking-policies; the shape of the answer is Not specified in the source documents (GAP-0694). |
| CDC-05679 | RWB-P3-E1023-CON | GAP-0694 | 8 | Publish masking policy request and response keyed by view field ID, with masked flag and source column per field |

### RWB-P3-E1028-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05690 | RWB-P3-E1028-APP | DOR-RWB-P3-E1028-APP-21 | header | Build RWB-P3-E1028-CON to Done so its contract is published. Current build status is Not started. |
| CDC-05737 | RWB-P3-E1028-OPS | DOR-RWB-P3-E1028-OPS-21 | Not specified in the source documents (DOR-RWB-P3-E1028-OPS-21) | Build status of RWB-P3-E1028-CON moves from Not started to Done once the contract is published. |

### OTHER:rwb-source-data API yaml; OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05691 | RWB-P3-E1028-APP | DOR-RWB-P3-E1028-APP-8 | 11 | Publish GET /api/recovery/source-data/v1/accounts/{accountId}, GET /api/recovery/source-data/v1/calendar/holidays and POST /api/recovery/access/v1/authorise; model timerType as LOV-TIMER data in rwb-case.yaml. Other listed paths remain to be checked. |
| CDC-05738 | RWB-P3-E1028-OPS | DOR-RWB-P3-E1028-OPS-8 | 12 | Publish GET /api/recovery/source-data/v1/accounts/{accountId} and GET /api/recovery/source-data/v1/calendar/holidays in rwb-source-data; publish POST /api/recovery/access/v1/authorise in rwb-access; in rwb-case.yaml replace the closed timerType enum with a reference to LOV-TIMER. |

### OTHER:rwb-case values files and runbook (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05706 | RWB-P3-E1028-APP | GAP-2204 | none | Set the poll window, catch-up window, breach band and record-failure rate in the values files, confirm them at UAT, and record the agreed values in the runbook entry each alert links. |
| CDC-05761 | RWB-P3-E1030-APP | GAP-2207 | find it | Set zone, catch-up, replicas, limits, host, alert and retry values per environment; confirm at the SIT dry run and record them in the runbook. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05735 | RWB-P3-E1028-OPS | CG-ALL-3644 | 3 | Keep timerType as an enum and set its values to the nine LOV-TIMER codes SERVICE_LEVEL, NOTICE_PERIOD, CURE_PERIOD, PRESCRIPTION, HEARING_DEADLINE, OFFER_VALIDITY, HOLDING_AGE, CLAIM_DEADLINE, INSTALLMENT_DUE; the list is closed, so the enum stays. |
| CDC-05736 | RWB-P3-E1028-OPS | CG-ALL-3645 | 3 | Keep status as an enum and set its values to the four LOV-TIMER-STATUS codes RUNNING, PAUSED, EXPIRED, STOPPED; the list is closed, so the enum stays. |

### RWB-P3-E1031-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05799 | RWB-P3-E1031-APP | DOR-RWB-P3-E1031-APP-21 | 14 | Build and publish RWB-P3-E1031-CON so its build status is Done. |
| CDC-05801 | RWB-P3-E1031-APP | DOR-RWB-P3-E1031-APP-23 | 12 | Fix and state the contract version of the two case-list operations so RWB-P3-E1031-APP can cite it beside the /v1 base path |

### RWB-P3-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05643 | RWB-P3-E1021-OPS | GAP-3077 | find it | Architect records the split: deviation triggers evaluated in S8 against the package in force from P7; manual and case-trigger paths stay in P3; one package, one version. |

### OTHER:TSD S8 T3.1 (deviation table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05645 | RWB-P3-E1021-OPS | GAP-3080 | 11 | Add rule_id and rule_version columns to deviation if an audit read of the transfer rule per deviation row is required; until then the DP-03 decision record is the transfer record and recovery_case.rule_version (DF-CAS-021) and assignment.transfer_reason_code (DF-WRK-040) stay with rwb-case. |

### RWB-P4-E1037-CON; OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05649 | RWB-P3-E1021-OPS | GAP-0990 | find it | Publish the authorise request and answer schema with its legalHold attribute, confirm the matrix version label, and tabulate the Queue and allocation letters. |

### OTHER:AsyncAPI 3.0 document of rwb.document.events.v1 (P5 contract baseline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05650 | RWB-P3-E1021-OPS | GAP-1036 | none | Publish the producer-side AsyncAPI 3.0 document with the registered JSON schemas of rwb.document.DocumentStored.v1 and rwb.document.DocumentFieldsExtracted.v1, their required fields and BACKWARD rule; hand DocumentStored schema to RWB-P3-E1021-CON. |

### RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05652 | RWB-P3-E1023-APP | DOR-RWB-P3-E1023-APP-21 | header | Build status is Not started; it must reach Done before this story is ready. |

### RWB-ITG-E1023-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05658 | RWB-P3-E1023-APP | GAP-0348 |  | Confirm the case-scoped deviation read with the S8 owner before AC18; treat rwb-deviation as SIT-available for the wave 1 run; keep the W1J01 synthetic fixture set. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05674 | RWB-P3-E1023-CON | DOR-RWB-P3-E1023-CON-7 | 11 | Give the BR Field ID for each of the five section 11 data rows (case, accounts, parties, timeline, timers); section 11 then cites it |

### OTHER:Business requirements document (section 8.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05675 | RWB-P3-E1023-CON | GAP-1456 | 8 | State the rule: business-epic wave kept; build wave per story confirmed at build sequencing by the delivery lead |

### RWB-P3-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05682 | RWB-P3-E1023-CON | GAP-1330 |  | State whether RWB-P3-E1073-CON publishes the case reads its consumers need, or move the RWB-P7-E1073-APP contract dependency to the P3 story that does. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05698 | RWB-P3-E1028-APP | DOR-RWB-P3-E1028-APP-10 | 15 | Add the Empty, Loading, Error and No access states for P3 SCR-03 and P3 SCR-09, which section 15 of RWB-P3-E1028-APP reads from this document (CG-ALL-3619, CG-ALL-3620). |

### OTHER:RWB-P2 story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05699 | RWB-P3-E1028-APP | DOR-RWB-P3-E1028-APP-9 | 14 | Use MSG-P4-001 with the standard meaning, as in RWB-P3-E1028-APP §14 (no session on a read) |

### OTHER:rwb-case contract and FSD P7 acceptance criteria A2.15 and A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05700 | RWB-P3-E1028-APP | GAP-1623 | n/a | Record that P3 reacts to ApprovalRequested to move the case state and raise the approval task, so rwb-case stays the only writer of case state; add to A2.15 and A2.16. |

### RWB-P3-E1028-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05701 | RWB-P3-E1028-APP | GAP-2202 | n/a | Add P1 rows for accountDates(List<UUID>) and holidays(LocalDate, LocalDate) with answer shape and data-as-of field; record the wave 1 pause operation in the P3 contract. |

### RWB-P3-E1028-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05703 | RWB-P3-E1028-APP | GAP-2203 | n/a | Add escalated_to_role (DF-WRK-043) and escalated_at (DF-WRK-044) and the TimerBreached payload fields; type, length and optionality Not specified in the source documents. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:EV-19) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05704 | RWB-P3-E1028-APP | GAP-0022 | n/a | The owner record lives in the event catalogue: PLT keeps retired EV-18 and P3 owns EV-19. The story names neither owner, so no story edit resolves it. |

### OTHER:TSD P4 T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05705 | RWB-P3-E1028-APP | GAP-0986 | none | Fix the authorise attribute set for a case read and a timer read, including escalatedToRole and escalatedAt; name the matrix version in force at 30 November 2026 in the policy pack; state the answer names the ESCALATED_TO_ROLE grant scope, no wider than the caller's role row. |

### OTHER:rwb-source-data, rwb-access and rwb-case API yaml files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05711 | RWB-P3-E1028-CON | DOR-RWB-P3-E1028-CON-8 | header | Publish GET /api/recovery/source-data/v1/accounts/{accountId}, GET /api/recovery/source-data/v1/calendar/holidays, POST /api/recovery/access/v1/authorise; align rwb-case.yaml timerType with LOV-TIMER; clear the 7 further detcheck findings. |

### RWB-P3-E2015-APP; RWB-P3-E1035-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05719 | RWB-P3-E1028-CON | DOR-RWB-P3-E1028-CON-10 | 15 | Define the empty, loading, error and no access states of SCR-03 and SCR-09 and their message text; section 15 records them as Not specified in the source documents (CG-ALL-3639, CG-ALL-3640). |

### OTHER:RWB-AD-015 story and the rwb-access service-level load contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05721 | RWB-P3-E1028-CON | GAP-2275 | 11 | Name the three access-side paths, the file columns, the effect fields, the parameter rows, the reference list codes and the SCR-42 panel split, as agreed at the wave 4 contract review. |

### OTHER:FSD P7 acceptance criteria AC-P7-015-01 (and A2.15; OTHER:A2.16) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05723 | RWB-P3-E1028-CON | GAP-1623 | 8 | Replace the case-status step with P3 moving the state on ApprovalRequested, the preferred option, and record the choice in the rwb-case contract. |

### RWB-P3-E2004-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05725 | RWB-P3-E1028-CON | GAP-0705 |  | Fix Timer properties treatmentId, timerType, startedAt, expiresAt, warnAt, paused and status as optional within major version 1; expiresAt as offset date-time |

### API:(service not named); OTHER:policy pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05730 | RWB-P3-E1028-CON | GAP-0986 |  | Fix authorise attributes for case and timer reads incl. escalatedToRole and escalatedAt; name the matrix version at 30 Nov 2026; answer names ESCALATED_TO_ROLE scope not wider than caller's role row |

### OTHER:rwb-case deployment values files and the DevOps runbook entry each alert links (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05731 | RWB-P3-E1028-CON | GAP-2204 |  | Set poll window, catch-up window, breach band and record-failure rate in the rwb-case values files, confirm at UAT, and record the agreed values in the linked runbook entry. Values not specified in the source documents (GAP-2204). |

### OTHER:Functional Specification P7 (A2.15; OTHER:A2.16) and the rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05741 | RWB-P3-E1028-OPS | GAP-1623 | 12.5 | Record the decision that P3 moves the case state and raises the approval task as a reaction to ApprovalRequested, and align AC-P7-015-01 with it. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:DF-WRK-044; OTHER:TimerBreached payload) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05745 | RWB-P3-E1028-OPS | GAP-2203 | 12.5 | Add escalated_to_role and escalated_at with type, length and optionality; fix the TimerBreached payload fields including caseNo, timerType and expiresAt; settle in the RWB-P3-E1028-CON baseline review. |

### API:(service not named); OTHER:TSD P4 T-A and the policy pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05747 | RWB-P3-E1028-OPS | GAP-0986 | none | Add the authorise request attributes for case and timer reads (case, queue, team, owner, object, timer type and status, escalation level, escalatedToRole, escalatedAt); name the matrix version in force at 30 November 2026; state that the escalation answer gives the grant scope with reason ESCALATED_TO_ROLE and no scope wider than the caller's role row. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:L371) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05748 | RWB-P3-E1030-APP | CG-ALL-3656 | 1, 13 | Rule a Java package segment that is not a Java reserved word for rwb-case and update the package column of the rwb-case row; the story copies the ruled package name. |

### OTHER:Contract fake library (owner not named in the sources) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05751 | RWB-P3-E1030-APP | DOR-RWB-P3-E1030-APP-22 | none | Publish the contract fake library and record its version. |

### OTHER:FSD P9 (FEAT-RPT-02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05755 | RWB-P3-E1030-APP | GAP-1652 | 8 | Remove queue depth, ageing and owner spread publication from FEAT-RPT-02 and its AC-P9-002-01, AC-ALT-P9-002-01 and AC-ALT-P9-002-02, or reference rwb-case as the publisher. |

### OTHER:rwb-case per-service Flyway sequence (DP-15; RWB-PLT-E1044-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05758 | RWB-P3-E1030-APP | CG-ALL-3657 | 13 | Issue the next free number of the rwb-case sequence and rename V1030_1__queue_measure.sql to V<that number>__queue_measure.sql; the story copies the name. |

### RWB-ITG-E1059-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05759 | RWB-P3-E1030-APP | GAP-0610 | find it | Keep legacy AC5 and TC-E1-059-05 with RWB-ITG-E1059-ITG; agree rwb-agent login and gateway route with owners; add RWB-P5-E1053-CON to contract dependencies once published. |

### OTHER:Build Notes v6 (RWB-TE-007) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05762 | RWB-P3-E1030-APP | GAP-3166 | find it | Read JOB-06 as a Temporal Schedule in the owning service; keep the retired RWB-TE-007 note for traceability only. |

### OTHER:Squad refinement / backlog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05765 | RWB-P3-E1030-CON | DOR-RWB-P3-E1030-CON-16 | Metadata | No size is specified in the source documents; the story records that sizing is pending and the squad sets it at refinement. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05769 | RWB-P3-E1030-CON | DOR-RWB-P3-E1030-CON-18 | 8 | DL25 remains open; its assumptions are not specified in the source documents. The decision is owned by the business decision log. |

### OTHER:Source data model / data dictionary (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05770 | RWB-P3-E1030-CON | DOR-RWB-P3-E1030-CON-7 | 11 | The BR field IDs are not specified in any source; the placeholder records the gap and the mapping belongs to the source data model. |

### OTHER:Integration pack review (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05772 | RWB-P3-E1030-CON | GAP-0354 | find it | Register JOB-06 as a Schedule in rwb-case and name its identifier, overlap policy and catch-up window; keep the P1 job catalogue as the run record and rerun facade; use rwb.reporting.ReportPublished.v1 as the publish marker. |

### OTHER:FSD P9 FEAT-RPT-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05773 | RWB-P3-E1030-CON | GAP-1652 | find it | Remove queue depth, ageing and owner spread computation from FEAT-RPT-02 and its acceptance criteria; P9 consumes the queue measures that P3 computes and publishes on the business date. |

### RWB-P3-E1030-APP; RWB-ITG-E1059-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05777 | RWB-P3-E1030-CON | GAP-0610 |  | Name the rwb-agent login (DP-02) with the ACE database team; name the gateway-bff route path in front of the admin reads in the API document; keep the legacy AC5 and TC-E1-059-05 only in RWB-ITG-E1059-ITG; add RWB-P5-E1053-CON to the contract dependency row when it is published; agree with the E1-059 evaluation story which story serves the sample and evaluation operations. |

### RWB-P3-E1030-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05779 | RWB-P3-E1030-CON | GAP-2207 | 12.6 | Set in the rwb-case values files per environment: the business time zone of the 06:30 firing, the catch-up window and overlap policy of the Schedule, the replica counts, resource limits and ingress host of the two deployments, the held-snapshot and missing-run alert threshold and window, the dead-letter rate and depth bands and the retry values of rebalance and takeQueueMeasures; confirm the zone and the catch-up window with the business owner and the platform team at the SIT dry run and record the agreed values in the runbook section each alert links. |

### OTHER:Build Notes v6 (RWB-TE-007 and RWB-E1-030) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05780 | RWB-P3-E1030-CON | GAP-3166 |  | Keep RWB-TE-007 Quartz schedule and job_catalog as retired traceability only; read JOB-06 and every Job as a Temporal Schedule in the owning service. |

### OTHER:Application and integration stories of key RWB-E1-059 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05792 | RWB-P3-E1030-OPS | GAP-0610 | find it | Keep AC5 and TC-E1-059-05 with RWB-ITG-E1059-ITG; name the rwb-agent login and the gateway-bff route path; add RWB-P5-E1053-CON to the contract dependencies in a later version. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05800 | RWB-P3-E1031-APP | DOR-RWB-P3-E1031-APP-22 | 14 | Publish a contract fake library version for RWB-P3-E1031-CON and record the version as published. |

### RWB-P3-E1031-CON; RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05806 | RWB-P3-E1031-APP | GAP-2208 | 3, 8, 15 | Publish team as an additive optional filter on GET /cases; name the rwb-access access-log operation with the AC-EXPT fields |

### OTHER:rwb-access contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05808 | RWB-P3-E1031-APP | GAP-2209 | 3 | Section 3 states the row, envelope and page-token names as Not specified in the source documents (GAP-2209); the contract names them; the 401 text is not in any source read here. |

### RWB-P3-E1031-CON; 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05812 | RWB-P3-E1031-CON | DOR-RWB-P3-E1031-CON-18 | 15 | Record an assumption against open decision DL31 (designer: SCR-02 route path, screen model and layout) so the P2 check passes; DL10, DL11 and DL26 already name ASM-2250, ASM-2357, ASM-2377, ASM-2863, ASM-0553, ASM-0703, ASM-1051, ASM-1104, ASM-0247, ASM-0264, ASM-0275 and ASM-0355. |

### OTHER:Technical specification P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05814 | RWB-P3-E1031-CON | GAP-2208 | 7 | Add optional team query parameter to API-P3-001 request list, as API-P3-017 has it; the rwb-access access-log operation is named in RWB-P4-E1039-CON. |

### 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20552 | RWB-P3-E1031-CON | R-15941 |  | Assumption against DL31 belongs to the DoR checklist DOR-RWB-P3-E1031-CON or its story. DL31 is not named here and no assumption text is sourced. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_case.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20559 | RWB-P3-E1030-APP | R-24912 |  | Next free rwb-case Flyway number is not in the sources (Service Template Specification v1). The sequence owner assigns it. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20669 | RWB-P3-E1030-CON | R-28558 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21890', 'R-28478', 'R-28528', 'R-28558', 'R-28573', 'R-28662'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0022 | TimerDue owner recorded as P3 and as PLT | Solution architect | Resolved (directive) |
| GAP-0346 | Route-decided transfer trigger has no wave 1 owner event | Tech lead | Resolved (directive) |
| GAP-0348 | RWB-E1-023 integration slice: the S8 deviation read path, the wave of rwb-deviation and the fixture composition are not fixed by the sources | TechX | Resolved (directive) |
| GAP-0353 | E1028 durable timers replace JOB-05 and the P1 account-date path leaves the slice | Solution architect | Resolved (directive) |
| GAP-0354 | Rebalancing trigger, measure delivery and rerun facade change in the target | Tech lead | Resolved (directive) |
| GAP-0355 | Export access entry, masking source and owner display name path are not named for the target | Tech lead | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0688 | Per-service database login name for rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0691 | Deployment topology of the transfer capability is not specified | Platform team | Resolved (directive) |
| GAP-0692 | The per-service database login name for rwb-case is not given | ACE DB owner | Resolved (directive) |
| GAP-0693 | The gateway-bff composite route specification for SCR-03 is not given | Solution architect | Resolved (directive) |
| GAP-0694 | The exact field masking contract shape is not given | P4 access owner | Resolved (directive) |
| GAP-0695 | The timeline paging and the interaction ledger read operation are not given | P1 source data owner | Resolved (directive) |
| GAP-0705 | No source fixes the plan-timer fields, types or required flags of the timers answer behind GET /cases/{caseId}/timers | Tech lead of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0986 | rwb-access timer and case read: the authorise request attribute set, the label of the matrix version in force and the scope that prevails under an escalation are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0989 | The authorise attribute set, the policy version labels and the full field-ID roster of the read-only case record view are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1036 | Producer-side AsyncAPI and JSON schema of rwb.document.events.v1 are not assigned to a contract story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1330 | RWB-P7-E1073-APP: the case read that feeds the dry run is attributed to RWB-P3-E1073-CON by the plan and to RWB-P3-E1023-CON by the P3 contract story, which serves no operation | Solution architect with the rwb-case contract owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1652 | Queue depth and ageing are computed in P3 and published in P9 | Solution architect with P3 | Resolved (directive) |
| GAP-2016 | Timer row and durable timer kept in step by one activity | Service owner P3 rwb-case with the platform team | Resolved (directive) |
| GAP-2202 | The account-date and holiday reads and the deviation pause have no published surface in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2203 | No source gives the field-level detail of the two escalation columns or of the TimerBreached payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2204 | No source gives the operational values for a durable timer: poll window, catch-up window, breach band and record-failure rate | DevOps lead | Resolved (directive) |
| GAP-2205 | The measure feed, the alert delivery path and the run record have no target artifact once the data lake and the job monitor are removed | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2206 | The published run record and the rerun operation of the legacy contract have no target shape | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2207 | No source gives the operating values for the rebalance Schedule or the deployment | DevOps lead | Resolved (directive) |
| GAP-2208 | Four target-side facts of the case list and its export are not fixed by any source, and the sources disagree on the team filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2209 | The row, envelope and page-token names of the case list and the 401 message text have no source | Solution architect | Resolved (directive) |
| GAP-2211 | No source fixes the v1.1 timeline item shape, the section state or its version against the RWB-P3-E1023-CON baseline | Solution architect | Resolved (directive) |
| GAP-2275 | Service-level load gate: the operations, the file columns, the effect list, the parameter rows and the SCR-42 panel split are not named for rwb-access | Solution architect, P4 and the P3 owner of the service-level and timer contract | Resolved (directive) |
| GAP-2277 | The contract document of the access-side service-level load has no declared source for its paths, schemas and error bodies | Tech lead, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3074 | The business epic places the story in wave 1 while the service sits in wave 2 | Programme planner with the S8 service owner | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3076 | No source publishes the operation names of the six rows this slice consumes | P1 rwb-source-data owner, P3 rwb-case owner, P4 rwb-access owner, P7 rwb-decision owner and the S8 service owner | Resolved (directive) |
| GAP-3077 | No source says which service hosts the TRANSFER package evaluation after the split | Solution architect with the S8 service owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-3079 | The event names of the P3 and P1 subscriptions are not published | P3 rwb-case owner, P1 rwb-source-data owner and the S8 service owner | Resolved (directive) |
| GAP-3080 | No source fixes where this slice records the rule ID and the package version of a transfer | S8 service owner with the data steward of module S8 and the P3 rwb-case owner | Resolved (directive) |
| GAP-3081 | RWB-S8-E1023-APP: the five read operations and the four consumed operation names of the case record view have no published baseline, and the freshness, scope and mask answers of the owners are unnamed | Solution architect | Resolved (directive) |
| GAP-3082 | RWB-S8-E1023-APP: a P3 Case and workflow module story is placed in rwb-deviation with an empty build row, and the plan gives the slice no platform dependency although seven pattern rows add one | Solution architect | Resolved (directive) |
| GAP-3083 | RWB-S8-E1023-APP: the plan assigns the slice no legacy acceptance criterion while it keeps thirteen legacy test cases, and the legacy criteria lose their owned ids | Solution architect | Resolved (directive) |
| GAP-3084 | RWB-S8-E1023-APP: the story wave is 1 by the business-epic map while the service wave is 2 in Arch v5, and the section timeout and the six lists have no published values for this page | Solution architect | Resolved (directive) |
| GAP-3166 | The Quartz note remains in the build notes although a Temporal Schedule replaces it | Platform lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E1023-APP | skipped AC ID | 105 | missing: AC4, AC11, AC12 |
| RWB-P3-E1031-APP | Not specified without item ID | 394 | The screen is SCR-02 and is served by the gateway-bff composite route, which calls rwb-case once and merges the answer into the case screen model, one hop (DP-1 |
