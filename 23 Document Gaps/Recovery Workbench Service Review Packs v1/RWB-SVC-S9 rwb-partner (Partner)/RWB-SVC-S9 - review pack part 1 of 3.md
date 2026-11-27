# RWB-SVC-S9 rwb-partner (Partner) - review pack, part 1 of 3 (RWB-S9-AD022-APP to RWB-S9-E6033-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 15 |
| Resolved in the stories | 304 |
| Cross-document (pending in another document) | 232 |
| Not applied (value not in the sources) | 21 |
| Open business decisions | 12 |
| Register gaps linked | 105 |
| Unconfirmed assumptions | 0 |
| Lint findings | 11 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S9-AD022-APP | 24 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 AD022 APP Partner firms and partner users v2.md |
| RWB-S9-AD022-CON | 13 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 AD022 CON Partner firms and partner users - contract v2.md |
| RWB-S9-E1032-APP | 32 | 44 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E1032 APP Automatic attach from the OCR intake v2.md |
| RWB-S9-E1057-APP | 13 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E1057 APP Intake from branches, mailroom, partner SFTP and email v2.md |
| RWB-S9-E2019-APP | 12 | 23 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E2019 APP Partner identities through the external gateway v2.md |
| RWB-S9-E2034-APP | 22 | 27 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E2034 APP Interaction ledger on the case and from every channel v2.md |
| RWB-S9-E6029-APP | 29 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6029 APP Onboard a partner and set terms v2.md |
| RWB-S9-E6029-CON | 13 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6029 CON Onboard a partner and set terms - contract v2.md |
| RWB-S9-E6030-APP | 19 | 10 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6030 APP Hold the partner panel and fee schedule as data v2.md |
| RWB-S9-E6030-CON | 21 | 3 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6030 CON Hold the partner panel and fee schedule as data - contract v2.md |
| RWB-S9-E6031-APP | 24 | 11 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6031 APP Allocate work by measured return v2.md |
| RWB-S9-E6031-CON | 15 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6031 CON Allocate work by measured return - contract v2.md |
| RWB-S9-E6032-APP | 28 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6032 APP Override an allocation with a reason v2.md |
| RWB-S9-E6032-CON | 15 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6032 CON Override an allocation with a reason - contract v2.md |
| RWB-S9-E6033-APP | 24 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6033 APP Receive a partner result into the case v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S9-AD022-APP | R-13506 | CG-ALL-11714 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S9-E6029-APP | R-13529 | CG-ALL-11786 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E1057-ITG, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-P5-E1057-APP, RWB-P5-E1057-CON, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-S9-E1057-APP | R-22197 | GAP-3146 | Register gap | Business lead; solution architect; rwb-partner tech lead; rwb-access owner; programme lead | RWB-S9-E1057-APP: the split plan gives this secondary slice no legacy criterion and no build row while the P5 slice of the same key hands the partner criteria to it, no source publishes a partner-by-code read or the code filter of GET /partners, the two refusal reasons and the not-found behaviour are not published, the constraint on partner_code and the panel transition table are not specified, the DP-07 rows cannot be carried in an empty H row, and EP01 wave 1 is earlier than the service wave 4 | Serve the partner panel read as the code filter of the published GET /partners under base /api/recovery/partner/v1 with right R and the scope applied, answer the six published properties from partner in rwb_partner, answer an empty list for an unknown code and the stored panel status for a partner that is not ACTIVE, leave BR4 and the two reasons with the caller, read LOV-PANEL and LOV-PARTNER-TYPE through DP-07, write nothing and publish nothing, keep wave 1 and record the DP-07 rows, the constraint on the partner code, the panel transition table and the criteria assignment of the two slices as open items. |
| RWB-ITG-E6032-ITG, RWB-S9-E6032-APP, RWB-S9-E6032-CON | R-22854 | GAP-3112 | Register gap | Business lead; solution architect; rwb-decision rule owner; rwb-access owner | RWB-S9-E6032-APP: no source publishes an override operation, an override element or a reason property, no rule row or decision code names the placement override, the instruction status list has no published transition table, the two screens give the override no state and name no action, the legacy permission table gives right U while the operation declares C and its 21 and 5 further holders are not enumerated, and no requirement row traces to FEAT-PRM-04 | Serve the override as the branch of the published API-S9-002 with one additive optional overrideReason property, record the reason and the rule version in the local decision record before the change, end the replaced partner_instruction at RECALLED and create the replacement at SENT, take right C over the operation matrix and record the wider legacy U as a difference, place the action on SCR-35 in its list state behind the composite route, keep the case, the clock and the officer assignment with rwb-case, and hold the rule ID, the decision code, the transition table and the requirement row as open items. |
| RWB-ITG-E6032-ITG, RWB-S9-E6032-APP, RWB-S9-E6032-CON | R-22855 | GAP-3113 | Register gap | Solution architect; rwb-partner tech lead; business lead; rwb-decision rule owner; rwb-access owner | RWB-S9-E6032-CON: InstructionRequest publishes no override property and no source gives the override an element, the required flags of the request are not published, no rule row or decision code names the placement, TSD S9 T5.3 and the Event and Messaging Design disagree on the direction of EV-21 while the pattern set carries no DP-09, the legacy permission table gives U while the operation declares C, and no requirement row traces to FEAT-PRM-04 | Publish the override branch inside API-S9-002 with the published InstructionRequest plus one additive optional overrideReason, the PartnerInstruction answer with its nine properties, six required flags and four lists, the rule row as a class C consumed row with a fake and no rule row, no override element, no event, no second topic and no Schedule, the partner-portal right C with the seven holders of T6.1 and the legacy U recorded as a difference, and hold the request's required flags, the rule ID, the decision code, the transition table and the requirement row as open items. |
| RWB-S9-E6029-APP, RWB-S9-E7018-APP | R-29236 | GAP-1855 | Register gap | Business analyst, S9 with Legal counsel and Compliance | The module has no message of its own, and no Thai wording is stated for any of its messages | Take the wording from the Error and Message Standard for the reused messages and author the module's own messages with the story, in Thai and English, before the wave-4 release. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S9-AD022-APP | R-08962 | DOR-RWB-S9-AD022-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources; project-wide search found no epic design record or sign-off. No sign-off invented; needs the epic design record. |
| RWB-S9-AD022-CON | R-08968 | DOR-RWB-S9-AD022-CON-14 | none | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (grep 'epic design' found only scratch files). Sign-off would be invented; not recorded here. |
| RWB-S9-E1032-APP | R-27895 | CG-ALL-11745 | 7 | Criteria and tests keep legacy job and decision-log wording | Section 7 criterion line (working copy line 227) says 'the JOB-12 cadence'. That line is not in the supplied text, so not edited. Use the reconcile Schedule of 12.6 and the workflow name. |
| RWB-S9-E1032-APP | R-28572 | GAP-3145 | 3 | The partner portal screen that submits a file is not fixed | PRT-02 is not confirmed here. The screen number stays Not specified in the source documents (GAP-3145). |
| RWB-S9-E2019-APP | R-08985 | DOR-RWB-S9-E2019-APP-16 Size: Fail | header | Definition of Ready item 16 Size: Fail | No size value or sizing process exists in the sources; the row is a placeholder only. |
| RWB-S9-E2019-APP | R-13517 | CG-ALL-11758 | 4, 12.1 | HTTP errors with no message ID: 422 a load field that fails its rule, with the field named | Error and Message Standard v4 (MSG-GEN-001 to -007) has no message for a field failing its rule. -001 is empty, -002 range, -003 date order, -007 list. No fit, so no ID was invented. |
| RWB-S9-E2019-APP | R-22540 | GAP-0403 | find it | The external partner gateway test route and the partner harness pack are not specified | Test route, directory tenant, harness seeding and evidence values appear in no source. Needs agreement with platform edge team and QA, outside the documents. |
| RWB-S9-E2034-APP | R-08990 | DOR-RWB-S9-E2034-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in story or sources; a sign-off value would be invented. Searched all .md sources: only role descriptions. Needs the epic design record. |
| RWB-S9-E2034-APP | R-27908 | CG-ALL-11775 |  | Flyway file V2034_1__partner_ledger_fact.sql is not in the V0001..Vnnnn form | Current story text has no V2034_1 migration line (directive out file line 332 blank). No next free Flyway number in sources. Not specified in the source documents (CG-ALL-11775). |
| RWB-S9-E6029-APP | R-08996 | DOR-RWB-S9-E6029-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-S9-E6029 found. Grep of 03 Requirements and 22 Microservice Realignment for 'epic design' and sign-off shows no such record. Sign-off cannot be confirmed. |
| RWB-S9-E6030-APP | R-03168 | CG-ALL-11800 | outside chunk | rwb-partner.yaml holds panelStatus as a closed enum while the story reads LOV-PANEL as data | Ruling is closed list (Reference Data v5, LOV-PANEL). The passage calling LOV-PANEL data is not in this chunk, so it cannot be edited here. yaml enum kept. |
| RWB-S9-E6030-APP | R-03169 | CG-ALL-11801 | outside chunk | rwb-partner.yaml holds partnerType as a closed enum while the story reads LOV-PARTNER-TYPE as data | Ruling is closed list (Reference Data v5, LOV-PARTNER-TYPE). The passage calling LOV-PARTNER-TYPE data is not in this chunk, so it cannot be edited here. yaml enum kept. |
| RWB-S9-E6030-APP | R-09011 | DOR-RWB-S9-E6030-APP-8 | outside chunk | Definition of Ready item 8 Contract: Fail | Depends on the closed-list story edits for CG-ALL-11800 and CG-ALL-11801. Those passages are outside this chunk, so the contract check stays Fail. |
| RWB-S9-E6030-CON | R-09013 | DOR-RWB-S9-E6030-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design for EP06 in sources. Searched 22 Microservice Realignment: only DT05 (decision log v10 csv) sets the process, not a sign-off. Left unchanged. |
| RWB-S9-E6031-APP | R-09023 | DOR-RWB-S9-E6031-APP-8 | 9 | Definition of Ready item 8 Contract: Fail | Story §12.3 and §12.5 text is not in this chunk, so no exact old text. Topic and queue already match the catalog. Payload (EV-20: instructionId, partnerId, type, dueOn) and InstructionWorkflow ID form are not resolved. |
| RWB-S9-E6031-APP | R-22852 | GAP-3111 | 8 | Placement contract of S9: request body, element property names, status vocabulary and four consumed operation names are not published | No source value for the request body, property names, status vocabulary, operation names or error set. Searched the APIs sheet, context pack, legacy story, Kafka and Temporal catalogs. Needs Tech lead decision. |
| RWB-S9-E6031-CON | R-09024 | DOR-RWB-S9-E6031-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed EP06 epic design record in the sources. Grep of the project folders found none; only the ways-of-working sign-off rule. Sign-off value not invented; no edit. |
| RWB-S9-E6032-APP | R-09028 | DOR-RWB-S9-E6032-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design sign-off in the story or source docs; the epic design record is not in the sources. Citing one would invent it. Needs the record. |
| RWB-S9-E6032-APP | R-21427 | DOR-RWB-S9-E6032-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Section 10 text for SCR-34 and SCR-35 is not in the supplied story parts, so the states cannot be added against the current text. Needs section 10 supplied. |
| RWB-S9-E6033-APP | R-21445 | DOR-RWB-S9-E6033-APP-4 | 7 | Definition of Ready item 4 Business rules: Partial | AC3 unchanged in the diff; BR8 still has no criterion line. |
| RWB-S9-E6033-APP | R-33257 | NEWAC-RWB-S9-E6033-APP-AC10 | 7, 8, 16 | AC10: §8 BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC10 is now used for X7, so the no-new-AC10 note was wrong. BR8 criterion still missing. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml (29)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19825 | RWB-S9-AD022-APP | CG-ALL-11707 | 12.1 | Publish GET /api/recovery/partner/v1/partners (API-S9-001) through RWB-S9-AD022-CON, or remove it from 12.1 |
| CDC-19826 | RWB-S9-AD022-APP | CG-ALL-11708 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions (API-S9-003) through RWB-S9-AD022-CON, or remove it from 12.1 |
| CDC-19837 | RWB-S9-AD022-CON | CG-ALL-11717 | 12.1 | Publish path /api/recovery/partner/v1/partners (operation API-S9-001) with its GET operation. |
| CDC-19838 | RWB-S9-AD022-CON | CG-ALL-11718 | 12.1 | Publish path /api/recovery/partner/v1/partner/instructions (operation API-S9-003) with its GET operation. |
| CDC-19839 | RWB-S9-AD022-CON | CG-ALL-11719 | 12.1 | Publish path /api/recovery/partner/v1/cases/{caseId}/instructions (operation API-S9-002) with its POST operation. |
| CDC-19840 | RWB-S9-AD022-CON | CG-ALL-11720 | 12.1 | Publish path /api/recovery/partner/v1/partner/instructions/{instructionId}/accept (operation API-S9-004) with its POST operation. |
| CDC-19841 | RWB-S9-AD022-CON | CG-ALL-11721 | 12.1 | Publish path /api/recovery/partner/v1/partner/instructions/{instructionId}/results (operation API-S9-005) with its POST operation. |
| CDC-19842 | RWB-S9-AD022-CON | CG-ALL-11722 | 12.1 | Publish path /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices (operation API-S9-006) with its POST operation. |
| CDC-19844 | RWB-S9-AD022-CON | DOR-RWB-S9-AD022-CON-8 | 1 | Add under /api/recovery/partner/v1 the operations API-S9-001 to API-S9-004 (GET /partners, GET /partner/instructions, POST /cases/{caseId}/instructions, POST /partner/instructions/{instructionId}/accept) and the five further operations the detcheck names. |
| CDC-19849 | RWB-S9-E1032-APP | CG-ALL-11734 | 12.1 | Publish POST /api/recovery/partner/v1/partner/instructions/{instructionId}/documents as described in RWB-S9-E1032-APP 12.1. |
| CDC-19850 | RWB-S9-E1032-APP | CG-ALL-11735 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions/{instructionId}/documents as described in RWB-S9-E1032-APP 12.1. |
| CDC-19893 | RWB-S9-E1057-APP | CG-ALL-11749 | 12.1 | Contract dependency cell now names the GET /partners contract, not a story key |
| CDC-19897 | RWB-S9-E1057-APP | DOR-RWB-S9-E1057-APP-8 | find it | Add path GET /api/recovery/partner/v1/partners with the optional code filter (API-S9-001), published through RWB-S9-E1057-CON. |
| CDC-19910 | RWB-S9-E2019-APP | CG-ALL-11755 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions in rwb-partner.yaml through RWB-S9-E2019-CON. Story 12.1 already carries the path correctly. |
| CDC-19911 | RWB-S9-E2019-APP | CG-ALL-11756 | 12.1 | Publish GET /api/recovery/partner/v1/partners in rwb-partner.yaml through RWB-S9-E2019-CON. Story 12.1 already carries the path correctly. |
| CDC-19912 | RWB-S9-E2019-APP | CG-ALL-11757 | 12.1 | Publish POST /api/recovery/partner/v1/admin/reference-loads (stated default) in rwb-partner.yaml through RWB-S9-E2019-CON. |
| CDC-19916 | RWB-S9-E2019-APP | DOR-RWB-S9-E2019-APP-8 | 12.1 | Publish the three paths of 12.1 (partner/instructions, partners, admin/reference-loads) per CG-ALL-11755 to CG-ALL-11757. The 422 messageId is Not specified in the source documents. |
| CDC-19960 | RWB-S9-E6029-APP | CG-ALL-11781 | 12.1 | Publish the POST or PATCH /partners operation (method and path Not specified in the source documents (GAP-3106; ASM-5340)) through RWB-S9-E6029-CON, or remove it from 12.1. |
| CDC-19976 | RWB-S9-E6029-CON | CG-ALL-11791 | 12.1 | Publish the POST or PATCH /api/recovery/partner/v1/partners operation; method Not specified in the source documents (GAP-3107; ASM-5340) |
| CDC-19978 | RWB-S9-E6029-CON | DOR-RWB-S9-E6029-CON-8 | 12.1 | Publish the POST or PATCH /partners operation (GAP-3107; ASM-5340) in rwb-partner.yaml. |
| CDC-20022 | RWB-S9-E6032-APP | CG-ALL-11835 | 12.1 | Publish POST /api/recovery/partner/v1/cases/{caseId}/instructions (API-S9-002) in rwb-partner.yaml through RWB-S9-E6032-CON. |
| CDC-20024 | RWB-S9-E6032-APP | CG-ALL-11838 | 12 | Remove the closed enum on status; accept LOV-INSTR-STATUS values as data. |
| CDC-20025 | RWB-S9-E6032-APP | CG-ALL-11839 | 12 | Remove the closed enum on instructionType; accept LOV-INSTRUCTION values as data. |
| CDC-20026 | RWB-S9-E6032-APP | CG-ALL-11840 | 12 | Remove the closed enum on panelStatus; accept LOV-PANEL values as data. |
| CDC-20027 | RWB-S9-E6032-APP | CG-ALL-11841 | 12 | Remove the closed enum on partnerType; accept LOV-PARTNER-TYPE values as data. |
| CDC-20029 | RWB-S9-E6032-APP | DOR-RWB-S9-E6032-APP-8 | Header | Add path POST /cases/{caseId}/instructions (API-S9-002) under base /api/recovery/partner/v1; read status and instructionType as LOV-INSTR-STATUS and LOV-INSTRUCTION data, not closed enums. |
| CDC-20035 | RWB-S9-E6032-CON | CG-ALL-11851 | 12.1 | Story sentence states that the yaml does not declare POST /cases/{caseId}/instructions yet; publication location marked Not specified in the source documents. |
| CDC-20043 | RWB-S9-E6033-APP | CG-ALL-11862 | 12.1 | Publish POST /partner/instructions/{instructionId}/results (API-S9-005) in rwb-partner.yaml through RWB-S9-E6033-CON, or remove it from section 12.1. |
| CDC-20044 | RWB-S9-E6033-APP | CG-ALL-11863 | 12.1 | Publish GET /partner/instructions (API-S9-003) in rwb-partner.yaml through RWB-S9-E6033-CON, or remove it from section 12.1. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19833 | RWB-S9-AD022-APP | CG-ALL-11713 | 16 | Add rows TC-S9-AD022-APP-01 to -10 to Story test cases, with Given, When and Then copied from section 7 and the section 16 rows. |
| CDC-19846 | RWB-S9-AD022-CON | DOR-RWB-S9-AD022-CON-12 | 12.7, 16 | Add rows TC-S9-AD022-CON-01 to TC-S9-AD022-CON-06 under the same IDs as section 16. |
| CDC-19848 | RWB-S9-AD022-CON | CG-ALL-11726 | 16 | Add rows TC-S9-AD022-CON-01 to TC-S9-AD022-CON-05 with Given, When and Then copied from the criterion each covers (AC1 to AC6 as listed in section 16). |
| CDC-19860 | RWB-S9-E1032-APP | CG-ALL-11742 | 16 | Add rows TC-S9-E1032-APP-01 to TC-S9-E1032-APP-08 with Given, When and Then copied from the criteria each covers (AC1 to AC7). |
| CDC-19900 | RWB-S9-E1057-APP | CG-ALL-11750 | 16 | Add rows TC-S9-E1057-01 to TC-S9-E1057-08 with Given, When and Then copied from the criteria they cover. |
| CDC-19966 | RWB-S9-E6029-APP | CG-ALL-11785 | 16 | Add rows TC-E6-029-01 to TC-E6-029-04 with Given, When and Then copied from the criteria they cover. |
| CDC-19983 | RWB-S9-E6029-CON | DOR-RWB-S9-E6029-CON-12 | 12.7, 16 | Register TC-E6-029-01 to TC-E6-029-04 and TC-S9-E6029-CON-01 to TC-S9-E6029-CON-07 |
| CDC-19987 | RWB-S9-E6029-CON | CG-ALL-11795 | 16 | Add the nine rows to Story test cases, with Given, When and Then copied from the criterion each covers (TC-E6-029-01 to -04 and TC-S9-E6029-CON-01 to -05). |
| CDC-19992 | RWB-S9-E6030-APP | CG-ALL-11802 | 16 | Add rows TC-E6-030-01 to TC-E6-030-04 with Given, When and Then copied from the criterion each row covers; add TC-E6-030-05 to TC-E6-030-10 added by this story. |
| CDC-20000 | RWB-S9-E6030-CON | CG-ALL-11810 | 16 | Add rows for TC-E6-030-01 to TC-E6-030-04, TC-S9-E6030-CON-01 to TC-S9-E6030-CON-05, with Given, When and Then copied from the criterion each covers. |
| CDC-20001 | RWB-S9-E6031-APP | DOR-RWB-S9-E6031-APP-12 | 12, 12.7, 16 | Add tab Story test cases rows for TC-E6-031-01 to -04, TC-S9-E6031-01 and -02, and new TC-S9-E6031-03 to -05. |
| CDC-20006 | RWB-S9-E6031-APP | CG-ALL-11820 | 16 | Add rows TC-E6-031-01 to TC-E6-031-04 and TC-S9-E6031-01 and TC-S9-E6031-02, with Given, When and Then copied from the criteria they cover. |
| CDC-20015 | RWB-S9-E6031-CON | DOR-RWB-S9-E6031-CON-12 | 12.7, 16 | Add rows on the Story test cases tab for TC-E6-031-01 to TC-E6-031-04 and TC-S9-E6031-CON-01 to TC-S9-E6031-CON-07. |
| CDC-20021 | RWB-S9-E6031-CON | CG-ALL-11831 | 16 | Add rows for TC-E6-031-01 to TC-E6-031-04 and TC-S9-E6031-CON-01 to TC-S9-E6031-CON-05, with Given, When and Then copied from the criterion each covers. |
| CDC-20032 | RWB-S9-E6032-APP | CG-ALL-11845 | 16 | Add rows TC-E6-032-01, TC-E6-032-02, TC-E6-032-03 and TC-E6-032-04 with Given, When and Then copied from the criteria they cover in section 7. |
| CDC-20033 | RWB-S9-E6032-APP | DOR-RWB-S9-E6032-APP-12 | 12, 12.7, 16 | Tab Story test cases: add TC-E6-032-01 to TC-E6-032-11 with the Given, When and Then of section 16. |
| CDC-20042 | RWB-S9-E6032-CON | CG-ALL-11857 | 16 | Add rows for TC-E6-032-01 to -04 and TC-S9-E6032-CON-01 to -06, with Given, When and Then copied from the criterion each covers. |
| CDC-20051 | RWB-S9-E6033-APP | CG-ALL-11868 | 16 | Add rows TC-E6-033-02, TC-E6-033-04, TC-S9-E6033-APP-01 to -09 with Given, When, Then copied from the criteria they cover |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19831 | RWB-S9-AD022-APP | CG-ALL-11710 | 12.5 | Add an Activities row for sweepContractEnd: task queue rwb-partner, the business date in, the firms with their users and contract end out. |
| CDC-19832 | RWB-S9-AD022-APP | CG-ALL-11711 | 12.5 | Add an Activities row for endAccountValidity: task queue rwb-partner, the firm, users and end date in, record reference and count out, record first. |
| CDC-19853 | RWB-S9-E1032-APP | CG-ALL-11738 | 12.5 | Add PartnerInstructionWorkflow, namespace rwb-recovery, task queue rwb-partner, owned by the S9 instruction stories. |
| CDC-19854 | RWB-S9-E1032-APP | CG-ALL-11741 | 12.5 | Add PartnerIntakeReconcileWorkflow, task queue rwb-partner, started by the Schedule of 12.6. |
| CDC-19858 | RWB-S9-E1032-APP | CG-ALL-11739 | 12.5 | Add activity recordPartnerDocument on task queue rwb-partner, using the contract element already given in section 12.5. |
| CDC-19859 | RWB-S9-E1032-APP | CG-ALL-11740 | 12.5 | Add activity reconcilePartnerIntake on task queue rwb-partner, using the contract element already given in section 12.5. |
| CDC-19940 | RWB-S9-E2034-APP | CG-ALL-11772 | 12.5 | Add activity writeLedgerFact to the Activities sheet for task queue rwb-partner: builds the fact and writes the outbox row inside the change transaction (BR7). |
| CDC-19981 | RWB-S9-E6029-CON | CG-ALL-11794 | 12.5 | Add an activity for rwb-partner onboarding or confirm that none is declared. |
| CDC-20031 | RWB-S9-E6032-APP | CG-ALL-11844 | 12.5 | Add activity recordPlacementOverride on task queue rwb-partner with its contract element, or name a catalogued activity. |
| CDC-20039 | RWB-S9-E6032-CON | CG-ALL-11856 | 12.5 | Add an Activities row for recordPlacementOverride on task queue rwb-partner, matching the contract element in section 12.5 of RWB-S9-E6032-CON. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19830 | RWB-S9-AD022-APP | CG-ALL-11706 | 11 | Record decision_record as a PLT library object in rwb_partner in the owning document, or use the dictionary name |
| CDC-19857 | RWB-S9-E1032-APP | CG-ALL-11731 | 12.7 | Record decision_record as the PLT library table written through DecisionRecordWriter.record, or use the dictionary name; story line 324 unchanged. |
| CDC-19866 | RWB-S9-E1032-APP | GAP-0742 |  | Add table rwb_case.case_document_link with case_id, document_id, checklist_state, extracted_field_count, linked_at and source_event_id, a unique key on (case_id, document_id), and no cross-service foreign key. Field IDs to come from the next data dictionary version (owner RW-DATASTEW). |
| CDC-19938 | RWB-S9-E2034-APP | CG-ALL-11763 | 12.7 | Record v_partner_ledger_fact as a read-only view in rwb_partner, created by migration V2034_1 (design choice, ASM-5538), not as an entity. |
| CDC-19939 | RWB-S9-E2034-APP | CG-ALL-11764 | 12.7 | Record decision_record as a PLT library table applied in rwb_partner (DP-03), or use its dictionary name. |
| CDC-19943 | RWB-S9-E2034-APP | DOR-RWB-S9-E2034-APP-7 | 11 | Confirm DF-INT-036 as a field of entity interaction or confirm the interaction field set is DF-INT-001 to DF-INT-029. |
| CDC-19965 | RWB-S9-E6029-APP | CG-ALL-11780 | 12.7 | Record decision_record as a DP-03 library object of rwb_partner, or give it the dictionary name; the story names it in 12.7 as a PLT library object. |
| CDC-19991 | RWB-S9-E6030-APP | CG-ALL-11799 | 11, 12.4 | Record library table decision_record in rwb_partner in the owning document, or use the dictionary name instead. |

### RWB-P2-E2034-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19934 | RWB-S9-E2034-APP | DOR-RWB-S9-E2034-APP-21 |  | Publish contract story RWB-S9-E2034-CON, or confirm RWB-P2-E2034-CON as the contract this story depends on. |
| CDC-19935 | RWB-S9-E2034-APP | DOR-RWB-S9-E2034-APP-22 |  | Publish a contract fake library version and record it as published. |
| CDC-19949 | RWB-S9-E2034-APP | GAP-2186 | 12 | Publish the contact-fact read on the P1 base with path, contact-key parameter and masked members; confirm GET /efs-history of RWB-P1-E2001-APP answers the outcome list; realign the two consumed rows. |
| CDC-19951 | RWB-S9-E2034-APP | GAP-0664 | 12 | Approve the five assumptions at contract review: login, append and fact element names, admin bodies and mapping, retry intervals of 1 min, 10 min, 1 hour with three attempts, and the ownership split. |
| CDC-19952 | RWB-S9-E2034-APP | GAP-0665 | 12 | Approve the two assumptions before baseline tag: wire shapes of append, two P1 reads, five fact answers and two admin operations; dedupe key, state moves, append-before-inbox order, repeated key as success. |
| CDC-19955 | RWB-S9-E2034-APP | GAP-2225 | 12 | Confirm element names, paths and field shapes of the interaction item, append command and intake result at contract review; rename in this story if they differ, changing no value or rule. |
| CDC-19956 | RWB-S9-E2034-APP | GAP-3149 | 12 | Agree EV-20 and EV-21 payload element names and the seam with RWB-P2-E2034-CON at its contract review; the seven ledger attributes stay declared as placeholders here. |
| CDC-20054 | RWB-S9-E6033-APP | GAP-3149 | 11 | Section 11 declares no ledger row, retention class or timeline read. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19845 | RWB-S9-AD022-CON | DOR-RWB-S9-AD022-CON-1 | 1 | Confirm 'tech lead' of rwb-partner as a role code or role name, or name the existing role that the story should use. |
| CDC-19862 | RWB-S9-E1032-APP | DOR-RWB-S9-E1032-APP-6 | 10 | Add role SY-PARTNER (service identity, login rwb_partner) with its schema-only write authority. |
| CDC-19942 | RWB-S9-E2034-APP | DOR-RWB-S9-E2034-APP-6 | 10 | Add role SY-PARTNER (service identity, login rwb_partner); no story change. |
| CDC-19982 | RWB-S9-E6029-CON | DOR-RWB-S9-E6029-CON-1 | 1 | Publish a role code or name for 'tech lead' (rwb-partner tech lead) so section 1 matches a listed role |
| CDC-20013 | RWB-S9-E6031-CON | DOR-RWB-S9-E6031-CON-1 | 1 | Add the role 'tech lead' (or its role code) for rwb-partner so that the section 1 role resolves; no story edit. |
| CDC-20040 | RWB-S9-E6032-CON | DOR-RWB-S9-E6032-CON-1 | 1 | Add a role code or role name for the rwb-partner tech lead, or name the existing v5 role it maps to, so the section 1 role can be traced. |
| CDC-20052 | RWB-S9-E6033-APP | DOR-RWB-S9-E6033-APP-6 | 10 | Add SY-PARTNER, service identity (login rwb_partner), with its grant in schema rwb_partner, as a role row. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19861 | RWB-S9-E1032-APP | DOR-RWB-S9-E1032-APP-12 | 16 | Align its test lists with section 16 of RWB-S9-E1032-APP (TC-S9-E1032-APP-01 to -10) for REQ-DCM-007, REQ-DCM-005 and REQ-DRI-004. |
| CDC-19881 | RWB-S9-E1032-APP | GAP-3144 | 1 | Record that AC1 to AC15 and TC-E1-032-01 to TC-E1-032-17 count once against RWB-P5-E1032-APP; the split is stated in section 1. |
| CDC-19883 | RWB-S9-E1032-APP | CG-ALL-11743 | 18 | Align the traced test lists for REQ-DCM-007 and REQ-DCM-005 with section 18 of RWB-S9-E1032-APP in the next RTM version; section 18 gets the same alignment in its next version. |
| CDC-19908 | RWB-S9-E1057-APP | CG-ALL-11752 | 18 | Align REQ-DCM-009 and REQ-DCM-010 test lists in the RTM with section 18 of RWB-S9-E1057-APP in the next RTM version. |
| CDC-19930 | RWB-S9-E2019-APP | CG-ALL-11760 | 18 | Align REQ-ACA-012 test list to section 18 (TC-E2-019-01 to TC-E2-019-21) in the next version, replacing the three IDs listed there. |
| CDC-19957 | RWB-S9-E2034-APP | CG-ALL-11774 | 18 | Align the test lists of the nine requirements in the next RTM version to section 18 of RWB-S9-E2034-APP, or align section 18 to the RTM where the RTM IDs are this story's. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19863 | RWB-S9-E1032-APP | DOR-RWB-S9-E1032-APP-7 | 11 | Add the entity partner_intake (rwb_partner) and the fields instruction_id, decision_record, intake_item_id and the two further names flagged by detcheck, with their classification. |
| CDC-19968 | RWB-S9-E6029-APP | DOR-RWB-S9-E6029-APP-7 | 11 | Register decision_record as a PLT library entity in rwb_partner. Criteria and tests wording in sections 7 and 16 is outside this chunk. |
| CDC-19993 | RWB-S9-E6030-APP | DOR-RWB-S9-E6030-APP-7 | 11 | Add entity or table decision_record (platform library table in rwb_partner, DP-03) to LDM v9 and classify it in Data Classification v5. |
| CDC-20007 | RWB-S9-E6031-APP | DOR-RWB-S9-E6031-APP-7 | 11 | Register decision_record as an entity or field of rwb_partner, or record it as a PLT library object outside the LDM, with its field list and classification. |
| CDC-20049 | RWB-S9-E6033-APP | CG-ALL-11861 | 12.7 | Add decision_record as a local rwb_partner table written through DecisionRecordWriter.record, or name its dictionary field; owner Data |
| CDC-20053 | RWB-S9-E6033-APP | DOR-RWB-S9-E6033-APP-7 | 11 | Section 11 edited for GAP-2103 and GAP-3149; decision_record not in LDM v9 or Data Classification v5. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19894 | RWB-S9-E1057-APP | DOR-RWB-S9-E1057-APP-14 | find it | Confirm and record the signed epic design sign-off for RWB-S9-E1057-APP. |
| CDC-19913 | RWB-S9-E2019-APP | DOR-RWB-S9-E2019-APP-14 | header | Record the signed epic design sign-off for EP02 in the epic design record; no signed design is in the sources. |
| CDC-19977 | RWB-S9-E6029-CON | DOR-RWB-S9-E6029-CON-14 | none | Confirm and record the signed epic design sign-off for RWB-S9-E6029-CON |
| CDC-19988 | RWB-S9-E6030-APP | DOR-RWB-S9-E6030-APP-14 | not in chunk | Record a signed epic design sign-off; none exists in the story or source documents. |
| CDC-20002 | RWB-S9-E6031-APP | DOR-RWB-S9-E6031-APP-14 | header | Record the signed epic design sign-off. |
| CDC-20037 | RWB-S9-E6032-CON | DOR-RWB-S9-E6032-CON-14 | 14 | Record the signed epic design sign-off for RWB-SVC-S9 with approver role and date. Not specified in the source documents (DOR-RWB-S9-E6032-CON-14) |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19827 | RWB-S9-AD022-APP | CG-ALL-11709 | 12.2 | Declare REST base /api/recovery/access/v1 for P4 rwb-access, taken from the Document Index service table |
| CDC-19843 | RWB-S9-AD022-CON | CG-ALL-11723 | 12.2 | Declare REST base /api/recovery/access/v1 for the rwb-access service, as in PRD P4 rwb-access v1 line 34 and FSD P4 Access and administration v4 line 47. |
| CDC-19902 | RWB-S9-E1057-APP | DOR-RWB-S9-E1057-APP-6 | 10 | Publish the authorise check that API-S9-001 calls for partner-portal right R. |
| CDC-20023 | RWB-S9-E6032-APP | CG-ALL-11836 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rwb-decision provider, taken from the Document Index service table. |
| CDC-20036 | RWB-S9-E6032-CON | CG-ALL-11852 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule row, from the provider's REST base in the Document Index service table. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19917 | RWB-S9-E2019-APP | CG-ALL-11759 | 4, 14 | Add a new message ID for 'The parameters, the lists or the authorise answer cannot be read' with its text; keep MSG-GEN-006 for system of record unavailable (R-UNI-33). |
| CDC-19919 | RWB-S9-E2019-APP | DOR-RWB-S9-E2019-APP-9 | 14 | Add a new message ID for 'The parameters, the lists or the authorise answer cannot be read' with its text; keep MSG-GEN-006 for system of record unavailable (R-UNI-33). |
| CDC-20005 | RWB-S9-E6031-APP | CG-ALL-11819 | 4, 14 | Add a new message ID for an X4 data product behind its business date, with its text; §14 then cites that ID in place of MSG-P1-001. |
| CDC-20017 | RWB-S9-E6031-CON | DOR-RWB-S9-E6031-CON-9 | 14 | Confirm that MSG-P1-001 carries the data-freshness meaning and text used in section 14; the wave 4 text is open under GAP-3110. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19920 | RWB-S9-E2019-APP | GAP-0067 |  | Story keeps wave 2 per W-MAP as ruled. |
| CDC-19990 | RWB-S9-E6030-APP | GAP-1835 | not in chunk | Add S9 Partner cells for rwb-source-data freshness and rwb-case reads, or confirm each freshness rule is answered by a contract response. |
| CDC-20030 | RWB-S9-E6032-APP | GAP-1835 | Header | Add S9 Partner cells for rwb-source-data freshness reads, or confirm the five freshness rules are answered by a contract response; the FSD reads ACE views only via rwb-source-data. |
| CDC-20048 | RWB-S9-E6033-APP | GAP-1835 | none | Read case, party and queue facts through the rwb-case contract and data-product freshness through the rwb-source-data contract; add the missing S9 cells or confirm the five freshness rules are answered by contract responses. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19836 | RWB-S9-AD022-APP | GAP-3103 | find it | Publish partner_user fields in the TSD S9 T3.1 catalogue and the PRD; name the contract-end Schedule and its clock; decide whether a recall is announced by an event; confirm the feature REQ-S9-001 to REQ-S9-009 serve. |
| CDC-19847 | RWB-S9-AD022-CON | GAP-3103 | 8 | Publish partner_user fields identity_ref, partner_id, role_code, valid_from, valid_to in the TSD S9 T3.1 catalogue; name the contract-end Schedule and its clock; decide whether a recall is announced by an event; confirm the feature the REQ rows serve. |
| CDC-19944 | RWB-S9-E2034-APP | GAP-1612 | find it | Re-issue FSD P7 without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012. |

### RWB-S9-E6033-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20045 | RWB-S9-E6033-APP | DOR-RWB-S9-E6033-APP-21 | header | Complete the contract build and publish it, moving its build status from Not started to Done. |
| CDC-20046 | RWB-S9-E6033-APP | DOR-RWB-S9-E6033-APP-22 | header | Publish the contract fake library and record its version. |
| CDC-20056 | RWB-S9-E6033-APP | GAP-3115 | 4 | Publish the multipart part names, the PartnerInstruction and InstructionPage element names and the error bodies at contract freeze; take the gateway profile from the platform edge story. |

### RWB-S9-AD022-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19828 | RWB-S9-AD022-APP | DOR-RWB-S9-AD022-APP-21 | header | Move the build status from Not started to Done and publish the contract |
| CDC-19835 | RWB-S9-AD022-APP | GAP-0442 | find it | Fix the portal route, the firm-scope field name and the refusal-or-ignore rule; pin the partner session and MFA assertion shape; publish any partner-user read; fix the cross-firm answer and its message. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19851 | RWB-S9-E1032-APP | CG-ALL-11736 | 12.3 | Add rwb.partner.PartnerDocumentSubmitted.v1 on rwb.partner.events.v1, key caseId, publisher rwb-partner. |
| CDC-19852 | RWB-S9-E1032-APP | CG-ALL-11737 | 12.4 | Add rwb.document.DocumentAttached.v1 on rwb.document.events.v1, publisher P5 rwb-document (RWB-P5-E1032-APP 12.3). |

### RWB-S9-E1032-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19855 | RWB-S9-E1032-APP | DOR-RWB-S9-E1032-APP-21 | header | Create contract story RWB-S9-E1032-CON for the rwb-partner operations, events and fakes of this story. |
| CDC-19877 | RWB-S9-E1032-APP | GAP-3138 | 1 | Publish the partner file channel: submission row, PartnerDocumentSubmitted fact, attach event consumed and item read used to copy match state. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19874 | RWB-S9-E1032-APP | GAP-2445 | find it | Add DOCATT as a value of LOV-DECISION in force, read through the rwb-case reference-data contract at the version in force; unknown codes refused with MSG-P7-009. |
| CDC-19879 | RWB-S9-E1032-APP | GAP-3142 | n/a | Publish the intake bound parameter row, the acceptance decision code with its version, and LOV-DOC-TYPE; keep values out of code. |

### RWB-P3-E1043-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19886 | RWB-S9-E1032-APP | GAP-0746 |  | Hold the case review task code, element type and status values as reference data in the rwb-case reference tables and load them before the review queue story starts. |
| CDC-19996 | RWB-S9-E6030-APP | GAP-3108 | 8 | Raise to P3 and P4 for next contract revision: panel maintenance operation, version column on partner, partner_user catalogue. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19887 | RWB-S9-E1032-APP | GAP-0745 | not in chunk | Add the case-side switch parameter, key Not specified in the source documents (GAP-0745), default on, owner RW-COE; off means the case side writes nothing from an event. |
| CDC-19889 | RWB-S9-E1032-APP | GAP-1200 | not in chunk | Name the business-owned communications values with defaults in a parameter catalog row, or state that the module has none and DP-06 applies as a path without a value. |

### RWB-P5-E1057-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19895 | RWB-S9-E1057-APP | DOR-RWB-S9-E1057-APP-21 |  | Contract publication is recorded as a dependency, not resolved in this story |
| CDC-19906 | RWB-S9-E1057-APP | GAP-1013 | 18 | Publish the three admin operations, the IntakeRun, IntakeRunChannel and IntakeRunPage fields and the six fakes with a drift test; add the partner read to the plan C list. |

### RWB-P5-E1057-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19899 | RWB-S9-E1057-APP | GAP-1587 | find it | rwb-integration takes files from the channel and hands them to P5 as intake items; P5 keeps source, channel, capture time, hash and duplicate rule, with no file-system path. |
| CDC-19907 | RWB-S9-E1057-APP | GAP-1015 | 12 | Register the Schedule ID, overlap policy SKIP with a one-run catch-up window, four channel blocks, four alerts with identifiers or placeholders, and one runbook entry each; confirm window, thresholds and two identifiers before wave 1. |

### RWB-S9-E2019-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19914 | RWB-S9-E2019-APP | DOR-RWB-S9-E2019-APP-21 |  | Contract dependencies row names RWB-S9-E2019-CON. |
| CDC-19915 | RWB-S9-E2019-APP | DOR-RWB-S9-E2019-APP-22 | 12.8 | Record a published library version for the rwb-partner contract fake named in 12.8. Item named rwb-case; the story is rwb-partner. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19933 | RWB-S9-E2034-APP | CG-ALL-11767 | 12.2 | Publish POST /api/recovery/access/v1/authorise in paths, through the rwb-access provider CON story. |
| CDC-19936 | RWB-S9-E2034-APP | DOR-RWB-S9-E2034-APP-8 | 12.2, 12.3, 12.5 | Publish POST /api/recovery/access/v1/authorise, and clear the two detcheck findings not listed in the item. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19948 | RWB-S9-E2034-APP | GAP-2321 |  | Record the recommended resolution: the owners settle the masking label, covered field IDs, AC-READ granularity and parameter rows at wave 2 or build, and confirm the authorise element at contract review. No story value or refusal changes. |
| CDC-20011 | RWB-S9-E6031-APP | GAP-3110 | find it | Close GAP-3110 with: partner_instruction DF-PRT-008 to DF-PRT-016 and partner_user DF-REF-212 to DF-REF-217 (Data Classification v5); EV-20 and EV-21 names (Kafka catalog v1); MSG-P1-001 text (Error and Message Standard v4). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19972 | RWB-S9-E6029-APP | GAP-1848 | find it | Add screen rows with owner and route for SCR-34, SCR-35, SCR-36 and PRT-01 to PRT-04; serve the partner screens through the partner gateway. |
| CDC-19984 | RWB-S9-E6029-CON | GAP-3107 | 11 | Publish the onboarding write method, path and request element; the partner_user field list in T3.1; the reference-data operation with RWB-P3-E1043-CON on the C row; the 409 message ID; the EV-20 and EV-21 names |

### RWB-S9-E6030-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19989 | RWB-S9-E6030-APP | DOR-RWB-S9-E6030-APP-21 | header | Build status must be Done before this story starts; it is currently Not started. |
| CDC-19994 | RWB-S9-E6030-APP | GAP-3109 | 12 | Publish tagged addendum with the two reads, Partner element, two lists, version stamp, reference-data row and decision element; publish no write operation; bind each status to a section 14 message. |

### RWB-S9-E6031-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20003 | RWB-S9-E6031-APP | DOR-RWB-S9-E6031-APP-21 | header | Move build status from Not started to Done. |
| CDC-20004 | RWB-S9-E6031-APP | DOR-RWB-S9-E6031-APP-22 | header | Record the published contract fake library version. |

### RWB-ITG-E6031-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20010 | RWB-S9-E6031-APP | GAP-0461 | find it | Record the agreed harness values at the wave 4 entry check: SIT, base hosts, PRT-SYN-0031-A, PRT-SYN-0031-B, PRT-SYN-0031-C, RW-2027-000831, RW-2027-000832, scorecard version, measured-return values, freshness cut-off and a gate where a stub pass is never a real pass. |
| CDC-20019 | RWB-S9-E6031-CON | GAP-0461 | find it | Set the harness environment, fixture, synthetic keys, scorecard version, measured-return values, freshness cut-off and pass or fail gate at the wave 4 entry check, as proposed. |

### RWB-ITG-E6032-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20034 | RWB-S9-E6032-APP | GAP-0462 | 16 | At the wave 4 entry check agree SIT and hosts, fixtures, keys, reason code, evidence and gate; publish InstructionRequest and PartnerInstruction with RWB-S9-E6032-CON. |
| CDC-20041 | RWB-S9-E6032-CON | GAP-0462 | 11 | At the wave 4 entry check, agree SIT and base hosts, fixture layout, synthetic partners, keys, reason code, evidence format and retention, and the pass or fail gate; until then drive the override through the one published placement and assert published status codes only. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19829 | RWB-S9-AD022-APP | DOR-RWB-S9-AD022-APP-8 | 12.1 | Publish the three P1 paths and add activity sweepContractEnd to Temporal Catalog v1; the two further findings are not in this chunk |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19834 | RWB-S9-AD022-APP | GAP-3104 | find it | Publish a PartnerUser element or confirm the table-only reading; publish the rwb-access operation names for RWB-P4-E1022-CON; map EV-20 and EV-21 to their names. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19856 | RWB-S9-E1032-APP | DOR-RWB-S9-E1032-APP-8 | 12 | Add paths POST and GET /partner/instructions/{instructionId}/documents to rwb-partner.yaml; add event types rwb.partner.PartnerDocumentSubmitted.v1 and rwb.document.DocumentAttached.v1 to Kafka Catalog v1, plus the 4 further detcheck items. |

### RWB-S9-E6033-CON; RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19864 | RWB-S9-E1032-APP | GAP-0992 | 1 | Fix the four shapes as the smallest superset of the legacy list; declare the two rwb-case case reads as C dependencies with their fakes; keep unnamed elements behind the placeholder until owner documents confirm. |

### RWB-P5-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19865 | RWB-S9-E1032-APP | GAP-0356 | 4, 5, 7, 12, 13 | Start the intake from DocumentStored with KEDA workers in place of the 15-minute JOB-12. Keep GET /review-items. Attach as POST /intake-items/{intakeItemId}/resolve with the item version. Keep CASE_NO_PATTERN, ACCOUNT_NO_PATTERN and CLASSIFY_THRESHOLD as document_hub_parameter rows read as data, sent via DP-06 to the P3 rwb-case parameters contract. Prove the P6 letter copy and S9 partner result on the same match path. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19867 | RWB-S9-E1032-APP | GAP-0991 | find it | Declare rwb.document.DocumentAttached.v1 on rwb.document.events.v1, or confirm DocumentStored as the attach event name, before wave 1 release. Story-side /resolve wording needs the section text, not in this chunk. |

### OTHER:Environment files (SCB IT infrastructure) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19868 | RWB-S9-E1032-APP | GAP-0993 | find it | Record per environment the replica count, request and limit set, KEDA ceiling, document_text growth and index budget, rwb-quarantine clearing age, hold container capacity and scan rate per hour, from SIT measurement and scan product throughput. |

### OTHER:TSD P5 v2; OTHER:TSD P6 Communications v2; OTHER:FSD P6 v2; parameter-catalog.csv; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19869 | RWB-S9-E1032-APP | GAP-1197 | find it | Publish the generated-document request and answer with the intake item created; name the letter-copy document type and source; register notice parameter names; extend the NoticeGenerated payload; allocate the notice screen ID. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19870 | RWB-S9-E1032-APP | GAP-1199 | find it | State whether the hub creates an intake item from a generated document and which request fields it needs, so the handoff is specified once. |

### OTHER:Test case register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19871 | RWB-S9-E1032-APP | GAP-1201 | find it | Record that attach proof of TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP; note TC-E1-032-01 as the notice-read refusal in this service. |

### RWB-ITG-E1032-ITG; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19872 | RWB-S9-E1032-APP | GAP-1202 | find it | Align the NoticeGenerated.v1 consumers row to the chosen reading (call edge from rwb-comms to rwb-document; rwb-decision the only event consumer), and align the P5 story and integration suite. |

### OTHER:Recovery Workbench TSD P7 v2 T3.1 (decision_log_entry) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19873 | RWB-S9-E1032-APP | GAP-2444 | 11 | Map the DOCATT attach entry: document reference, intake item and match method in actions; classifier version in model_version; confidence and type candidates in recommendation; refusal message id in outcome; final_call ATTACHED. Add the columns by migration V1032_1 in rwb_decision. |

### RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19875 | RWB-S9-E1032-APP | GAP-2447 | n/a | Define the DecisionRecorded payload field set (caseId, documentId, decisionCode, matchMethod, classifierVersion, confidence and the rest) and refuse a fact without a document reference. |

### RWB-S9-E1032-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19876 | RWB-S9-E1032-APP | GAP-3137 | Header | Confirm the secondary partner slice in the Change Register and publish the rwb-partner frame for RWB-S9-E1032-APP; story cites GAP-3137 in the contract version row. |

### RWB-S9-E1032-CON; RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19878 | RWB-S9-E1032-APP | GAP-3141 | n/a | Publish POST and GET /partner/instructions/{instructionId}/documents, the document-hub intake creation, the PartnerDocumentSubmitted payload, and the 404 and 409 bodies in RFC 9457 shape. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19880 | RWB-S9-E1032-APP | GAP-3143 | n/a | Add partner_intake with its field IDs to the LDM before the wave 1 entry check; the story migration is the only definition until then. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19882 | RWB-S9-E1032-APP | GAP-1198 | n/a | Add the seven platform contracts and two P3 contracts from the DP table to the dependency rows, or record in the platform release train that wave 1 services compile against them. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19884 | RWB-S9-E1032-APP | CG-ALL-11747 | 15 | Add empty, error and no access states to section SCR-31, or record them as Not specified in the source documents (CG-ALL-11747). |

### OTHER:BRD v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19885 | RWB-S9-E1032-APP | GAP-1457 |  | Renumber the section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### OTHER:platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19888 | RWB-S9-E1032-APP | GAP-0748 | not in chunk | Name one database login per service for rwb-case and rwb-document, reference them here once agreed. Login strings are not in the sources. |

### OTHER:FSD P6 Communications v3 and TSD P6 Communications v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19890 | RWB-S9-E1032-APP | GAP-1203 | not in chunk | Approve both documents, or record that wave 1 builds on the reviewed versions and any approved-text change is a change request. |

### OTHER:TSD P7 v2 and FSD P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19891 | RWB-S9-E1032-APP | GAP-2449 |  | Use the phrase 'the rwb-decision login (DP-02)'; keep placeholders 'Not specified in the source documents (GAP-2449)' for the parameter names and for the texts of MSG-P7-009 and MSG-GEN-006; read parameters through the rwb-case parameters contract. |

### OTHER:FSD P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19892 | RWB-S9-E1032-APP | GAP-2450 |  | Run the ledger completeness check on the ledger ingest window of DP-06 with no Temporal Schedule and no cron entry of this service. |

### RWB-S9-E1057-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19896 | RWB-S9-E1057-APP | DOR-RWB-S9-E1057-APP-22 | find it | Publish the contract fake for GET /partners (API-S9-001) and record its library version. |

### OTHER:split plan (split_plan.json) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19898 | RWB-S9-E1057-APP | GAP-1843 | find it | Restate the wave 1 slice of RWB-E1-057 as contract-only (partner identity and document path); panel, allocation and fees move to wave 4. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19901 | RWB-S9-E1057-APP | DOR-RWB-S9-E1057-APP-12 | 16 | Added TC-S9-E1057-09 to -13 |

### RWB-P5-E1057-CON; RWB-P5-E1057-OPS; RWB-P5-E1057-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19903 | RWB-S9-E1057-APP | GAP-1012 | 12 | CON: publish the three admin operations and run record fields. OPS and INF: carry channel property layout. Schedule owner confirms window, overlap and catch-up before wave 1. |

### RWB-P5-E1057-INF; RWB-P5-E1041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19904 | RWB-S9-E1057-APP | GAP-1014 | 12 | Record channel inventory as environment configuration; keep key material and mailbox credential as key store secret references; provision scan capacity; network and security owners confirm DMZ and scan rate. |

### OTHER:RWB-P1 admin job contract (rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19905 | RWB-S9-E1057-APP | GAP-0367 | 8 | Publish the JOB-12 run read and rerun operation of the P1 admin job view. Story bullet records the move to P1 and P5. |

### OTHER:BRD v4 section 3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19909 | RWB-S9-E1057-APP | GAP-1457 | 3 | Renumber section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### OTHER:P3 screen specification (SCR-34) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19918 | RWB-S9-E2019-APP | DOR-RWB-S9-E2019-APP-10 | 12.1, 14 | Add the empty, loading, error and no-access states of SCR-34. |

### RWB-P4-E2019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19921 | RWB-S9-E2019-APP | GAP-0785 | 4 | Register POST /partner-identities/resolve and its two schemas; agree the refusal-to-status table with the gateway owner and message catalogue; state that the capability publishes and consumes no event. |

### OTHER:rwb-decision contract baseline (TSD P7 v2 appendix T-A.1 and T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19922 | RWB-S9-E2019-APP | GAP-1272 |  | Fix the rwb-access record path to rwb-decision, the partnerId and date-range query parameters, the entry composition, the allowed/refused result vocabulary, the page-size bound parameter and both index names. |

### OTHER:Backlog (P4 epic; OTHER:Epic 2 joiner, mover and leaver story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19923 | RWB-S9-E2019-APP | GAP-1573 |  | Create the Epic 2 story for REQ-ACA-011 with the group-change scenario, session re-resolution, reallocation hand-off to rwb-case and leaver response time; answer DL38 and DL40. |

### OTHER:TSD S9 (T-A.1; OTHER:T-A.2; OTHER:T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19924 | RWB-S9-E2019-APP | GAP-3148 |  | Add the reference-load operation POST /api/recovery/partner/v1/admin/reference-loads with table code partner_user and Idempotency-Key, map refusals to legacy message ids, add the partner_user field catalogue from DF-REF-212 to DF-REF-217. |

### OTHER:RWB-E2-019 build notes (P4 story; OTHER:migration V_E2_019__partner_user.sql) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19925 | RWB-S9-E2019-APP | GAP-3181 | 12.1 | Remove the partner_user DDL and the reference load handler from the P4 build notes; keep session, role and scope checks in rwb-access. |

### API:(service not named); OTHER:TSD P4 v3 appendix T-A and T3.2, external gateway contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19926 | RWB-S9-E2019-APP | GAP-0784 |  | Register the partner identity resolution operation with its claim set, answer schema and PLACED scope type; state the lifetime of a resolved answer against the partner edge token lifetime. |

### OTHER:Security design decision; OTHER:Service Catalog and partner gateway runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19927 | RWB-S9-E2019-APP | GAP-1395 |  | Fix DMZ zone design, gateway product and version, client authentication method, token lifetimes, identity provider, certificate lifecycle, rate limits, WAF rule set and DR objectives. |

### OTHER:FSD S9 (A2.1 and related capability-area rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19928 | RWB-S9-E2019-APP | GAP-1850 |  | Name capability area PARTNER_PORTAL and the LOV-INSTRUCTION and LOV-INSTR-STATUS lists as the Logical Data Model holds them, and add them to the exception criteria. |

### OTHER:Owner of the route for PRT-01 and SCR-34 (not named in any source; OTHER:GAP-1848) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19929 | RWB-S9-E2019-APP | GAP-1848 | 15 | Screen owners for PRT-01 and SCR-34 recorded; route owner still Not specified. |

### OTHER:Recovery Workbench TSD P4 technical specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19931 | RWB-S9-E2019-APP | GAP-1567 |  | Drop lov_value and partner_user from T3.1 (with the T3.3 relationship); keep lists of values in TSD P3 and partner identity in TSD S9; state in the rwb-access contract which list versions and identity attributes it reads and its refresh rate. |

### RWB-PLT-N007-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19932 | RWB-S9-E2019-APP | GAP-0786 |  | Extend the certificate profile and rotation window to the rwb-access hop; record the per-client limit and burst for the resolution route in the gateway configuration baseline; publish rwb-access namespace, service and port. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19937 | RWB-S9-E2034-APP | GAP-1844 |  | Keep the RWB-E2-019 and RWB-E2-034 partner slices in wave 2 as EP02 partner identity slices, with the partner_user binding and FAPI 2.0 route published before panel work; correct the wave 4 service create ordering. |

### OTHER:Functional Specification Document S9 (Screens) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19941 | RWB-S9-E2034-APP | DOR-RWB-S9-E2034-APP-10 |  | Add empty, loading, error and no access states for SCR-04, SCR-34 and SCR-35 in the owning screen specification. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19945 | RWB-S9-E2034-APP | GAP-3175 | find it | Keep AceDataReady (EV-26) as target name on rwb.source-data.events.v1 and list LoadCompleted as its legacy alias. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19946 | RWB-S9-E2034-APP | GAP-3176 | find it | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### RWB-P2-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19947 | RWB-S9-E2034-APP | GAP-0590 | find it | Fix key EFS:<efs_record_key>; the view row fold count is this service's; the ledger writer counts repeat appends; the run reports both counts. |

### RWB-ITG-E2034-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19950 | RWB-S9-E2034-APP | GAP-0416 | 16 | Agree composite route and merge order with platform edge story; SIT environment, seeding, evidence format, retention and gate with QA at wave 2 entry; hold as harness pack data. |

### RWB-P2-E2034-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19953 | RWB-S9-E2034-APP | GAP-0666 | 13 | Approve in release readiness review: two consumer groups with offset policy and commit point, scan and retry intervals, lag and alert thresholds, build ID format, fixture ownership; carried as environment values. |

### OTHER:Recovery Workbench Data Dictionary Reference Data (DP-07) and Business Requirements Epic 2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19954 | RWB-S9-E2034-APP | GAP-2184 | 18 | Publish retention class list with periods and version; add PARTNER_RESULT and OFFER to LOV-LEDGER-EVENT; confirm uuid link types in LDM; name feature IDs for the four requirements. |

### OTHER:Recovery Workbench plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19958 | RWB-S9-E2034-APP | GAP-3187 | n/a | Keep RWB-E2-033 to RWB-E2-036 primary P2 with code in rwb-case as the ruling records; record the P2-or-P3 decision once in the plan at assembly. |

### RWB-P1-E1066-CON; RWB-P1-E1066-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19959 | RWB-S9-E2034-APP | GAP-2185 | n/a | Settle one ledger path family and realign the append row and its fake to POST /cases/{caseId}/interactions; this story publishes that form and adds no third path. |

### RWB-S9-E6029-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19961 | RWB-S9-E6029-APP | DOR-RWB-S9-E6029-APP-21 | n/a | Move build status from Not started to Done so the contract is published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19962 | RWB-S9-E6029-APP | DOR-RWB-S9-E6029-APP-8 | section 8 POST or PATCH /partners row | Add the POST or PATCH /partners operation with the DF-PRT-001 to DF-PRT-007 request and Partner response; method and path Not specified in the source documents (GAP-3106; ASM-5340). |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19963 | RWB-S9-E6029-APP | GAP-1835 | n/a | Add S9 Partner read cells for rwb-case and rwb-source-data, or confirm the five freshness rules are answered by a contract response. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19964 | RWB-S9-E6029-APP | GAP-1840 | n/a | Author a partner rule set from FSD A2.3, A2.4 and A2.8 to A2.15, governed in rwb-decision and evaluated by this service's embedded Drools kit. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19967 | RWB-S9-E6029-APP | DOR-RWB-S9-E6029-APP-11 | 8 | Confirm which fields of this story are classed as personal data; BR10 states none is carried, which the classification contradicts. |

### RWB-S9-E6029-CON; OTHER:T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19969 | RWB-S9-E6029-APP | GAP-3107 | find it | Publish the onboarding write method, path and request element, the partner_user field list, the reference-data operation with RWB-P3-E1043-CON, and the message ID bound to the 409. |

### OTHER:Recovery Workbench plan and TSD S9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19970 | RWB-S9-E6029-APP | GAP-3106 | find it | Add plan rows RWB-P3-E1043-CON and RWB-PLT-TE006-CON, and publish the onboarding write and partner_user field list in the rwb-partner contract. |

### RWB-ITG-E6029-ITG; RWB-S9-E6029-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19971 | RWB-S9-E6029-APP | GAP-0459 | find it | Record the SIT hosts, fixture layout, key scheme, terms fixture, business date, evidence format and gate, and publish the InstructionRequest shape and onboarding right. |

### OTHER:Recovery Workbench Gap Register v1 (23 Document Gaps) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19973 | RWB-S9-E6029-APP | GAP-1851 |  | Close GAP-1851 with the proposed fix: one owner role per partner type as a versioned panel row read at run time; refuse an allocation where the type has no owner role. Owner role: Business analyst, S9 with the partner and agency manager. |

### RWB-S9-E7011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19974 | RWB-S9-E6029-APP | GAP-1856 | find it | Hold the scorecard measures, weights, thresholds and capacity rule as versioned data rows, agreed with the scorecard story. |

### OTHER:FSD S9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19975 | RWB-S9-E6029-APP | GAP-1842 | 7 | Replace the fifteen identical generic main success rows and the 'None' alternate and background tables in A2.1.4.1 to A2.15.4.4 with step-specific criteria; carry AC-EXC-S9-001-01 to AC-EXC-S9-015-02 as they stand. |

### OTHER:BRD Epics 3 to 8 v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19979 | RWB-S9-E6029-CON | GAP-1757 | none | Answer Q-019 on the owner of the partner instruction capability; align the RWB-S5-E4023 wave 3 build to the published rwb-partner contract and its fake. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19980 | RWB-S9-E6029-CON | GAP-1845 | none | Publish InstructionWorkflow, EV-20 and EV-21 as a contract before wave 4 so rwb-litigation and rwb-asset build against the fake in wave 3. |

### OTHER:TSD S9; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19985 | RWB-S9-E6029-CON | GAP-3106 | 11 | Publish the onboarding write in the rwb-partner contract; add the partner_user field list; add plan rows RWB-P3-E1043-CON and RWB-PLT-TE006-CON; record whether a partner-to-version link is needed |

### RWB-ITG-E6029-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19986 | RWB-S9-E6029-CON | GAP-0459 | 10 | §10 states right C; the onboarding request element is the seven-property partner shape in §11, with the method and path Not specified. |

### RWB-ITG-E6030-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19995 | RWB-S9-E6030-APP | GAP-0460 | 16 | Agree at wave 4 entry check: harness environment, fixture layout, synthetic keys, panel and fee schedule versions, service levels, business dates, evidence format and gate. Publish panel-version load or read-only version path and valid-from rule. |

### OTHER:Functional Specification Document S9 (A2.1.1 to A2.15.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19997 | RWB-S9-E6030-APP | GAP-1856 | none | Hold scorecard measures, weights, thresholds and capacity rule as versioned data rows; agree initial set with the scorecard story. |

### OTHER:Recovery Workbench Program v5 section 10.2 and the rwb-partner service contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19998 | RWB-S9-E6030-CON | GAP-1845 | 1 | Publish InstructionWorkflow, EV-20 and EV-21 as a contract ahead of wave 4 so rwb-litigation and rwb-asset build against the fake in wave 3. |

### RWB-S9-E6030-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19999 | RWB-S9-E6030-CON | DOR-RWB-S9-E6030-CON-10 | 1 | Add empty, loading, error and no-access states for SCR-34 and SCR-35. |

### OTHER:Platform message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20008 | RWB-S9-E6031-APP | DOR-RWB-S9-E6031-APP-9 | 14 | Confirm the meaning of MSG-P1-001 for the data-freshness answer, or give the freshness answer a message ID that the standard does not already use. |

### OTHER:Epics 3 to 8 Specification v3 (APIs sheet and features sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20009 | RWB-S9-E6031-APP | GAP-1482 | find it | Keep /cases/{caseId}/instructions and /partner/instructions tagged E4; tag FEAT-PRM-03 and FEAT-PRM-05 as E6 consumers of those endpoints. |

### OTHER:Program v5 section 10.2 and 10.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20012 | RWB-S9-E6031-CON | GAP-1845 | 12.3, 12.5 | Plan publication of InstructionWorkflow, EV-20 and EV-21 as a contract ahead of wave 4, so the S4 and S5 wave 3 builds use the fake. |

### RWB-S9-E6031-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20014 | RWB-S9-E6031-CON | DOR-RWB-S9-E6031-CON-10 | find it | State empty, loading, error and no-access states for SCR-34 and SCR-35. |

### OTHER:rwb-access (DP-08) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20016 | RWB-S9-E6031-CON | DOR-RWB-S9-E6031-CON-6 | 10 | Name the authorise check that the three REST operations call. |

### OTHER:user story master and APIs sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20018 | RWB-S9-E6031-CON | GAP-1482 | find it | Keep the partner instruction endpoints in E4 and tag FEAT-PRM-03 and FEAT-PRM-05 in E6 as consumers of the same contract. |

### OTHER:S9 FSD and TSD (extract set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20020 | RWB-S9-E6031-CON | GAP-3110 | find it | Publish the partner_instruction and partner_user columns, the seventh partner field, the EV-20 and EV-21 names, the service levels, the MSG-P1-001 text and the status vocabulary beyond SENT. |

### RWB-S9-E6032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20028 | RWB-S9-E6032-APP | DOR-RWB-S9-E6032-APP-21 | Header | Set build status to Done with the contract published; it is currently Not started. |

### OTHER:Program v5 section 10.2 and BRD E38 section 7.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20038 | RWB-S9-E6032-CON | GAP-1845 | find it | Either move rwb-partner to wave 3, or publish InstructionWorkflow, EV-20 and EV-21 as a contract before wave 4 with the S4 and S5 owners. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20047 | RWB-S9-E6033-APP | DOR-RWB-S9-E6033-APP-8 | 12.5 | Items 1-3 carried as cross-document or resolved; workflow ID form and start rule recorded as not specified. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20050 | RWB-S9-E6033-APP | CG-ALL-11866 | 12.5 | Add activity recordPartnerResult on task queue rwb-partner: one rwb_partner transaction (instruction columns, decision record, outbox row) |

### RWB-ITG-E6033-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20055 | RWB-S9-E6033-APP | GAP-0463 | 3, 12.8, 13, 15 | Agree at the wave 4 entry check and record in the harness README: SIT base hosts, fixture layout, synthetic keys, result reference and answer shape, same-day cut-off, evidence format and retention, pass or fail gate. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0065 | Wave conflict S9 / EP01 | Tech lead | Resolved (directive) |
| GAP-0067 | Wave conflict S9 / EP02 | Tech lead | Resolved (directive) |
| GAP-0356 | Intake trigger, attach operation and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0367 | Partner eligibility, channel configuration and job monitoring move in the target | Tech lead | Resolved (directive) |
| GAP-0403 | The external partner gateway test route and the partner harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0416 | Ledger harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0442 | Partner portal route, firm-scope resolution and partner session are not specified by any source read | Solution architect | Resolved (directive) |
| GAP-0459 | Partner-onboarding integration harness: environment, fixture keys, terms fixture, business date, evidence and gate are not specified, the Ownership Map publishes no partner create or panel-change operation, and neither the InstructionRequest shape nor the right required to onboard is published | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0460 | Partner panel and fee-schedule harness: environment, fixture versions, evidence and gate are not specified, and no panel-version or fee-schedule load operation is published | Integration lead | Resolved (directive) |
| GAP-0461 | Measured-return placement harness: environment, fixture and keys, scorecard version, measured-return values, freshness cut-off and gate are not specified, the map publishes no allocation or scorecard read, the InstructionRequest shape is not published, and the legacy endpoint table names R and U where the placement declares C | Integration lead | Resolved (directive) |
| GAP-0462 | Partner allocation override harness: environment, fixture keys, reason code, evidence and gate are not specified; the map publishes no override operation and no reason field name or outside-panel refusal message | Integration lead | Resolved (directive) |
| GAP-0463 | Partner-result integration harness: environment, fixture keys, answer shapes, same-day cut-off, evidence and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0664 | The rwb-integration login, the entry and fact JSON field names, the admin bodies, the mapping detail, the retry intervals and the ownership split of the ledger intake are not fixed in the source documents | Solution architect | Resolved (directive) |
| GAP-0665 | The append, EFS and contact wire shapes, the admin operation bodies, the dedupe key of each type and the ordering of the append and the inbox are not stated for the intake contract | Solution architect | Resolved (directive) |
| GAP-0666 | The consumer group names, the offset policy, the retry scan interval, the lag and alert thresholds, the build ID format and the fixture owner of the intake deployment are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0742 | No case-side document link table or field IDs in the sources | RW-DATASTEW | Resolved (directive) |
| GAP-0743 | No named rwb-source-data operation for the ACE account number | RW-COE | Resolved (directive) |
| GAP-0744 | Cadence and time of the daily reconcile Schedule not specified | RW-COE | Resolved (directive) |
| GAP-0745 | The rwb-case feature switch key is not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0747 | Decision code and final call for the case document link are not specified | RW-COE | Resolved (directive) |
| GAP-0748 | Per-service login names for rwb-case and rwb-document are not specified | RW-SECADM | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0784 | The partner identity resolution operation, its claim set, its answer schema, the scope type PLACED and the lifetime of an answer are specified by no source | Solution architect, P4 rwb-access with the external gateway owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0785 | The contract of the partner identity resolution names no path, no claim or answer field, no refusal-to-status mapping and no statement of its absent events in any source | Tech lead of rwb-access with the external gateway owner and the rwb-partner service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0786 | The certificate profile, the rotation and revocation of the rwb-access hop, the numeric rate limit and the namespace and service names of the DMZ hop are specified by no source | SCB IT infrastructure with the security design authority | Resolved (directive) |
| GAP-0991 | The attach operation, its right and the attach event name differ between the legacy story, the TSD and the Arch v5 event catalogue | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0992 | The intake-match contract baseline fixes shapes and paths the sources do not name at field level, and the plan's C list omits the two rwb-case reads | Tech lead | Resolved (directive) |
| GAP-0993 | The compute, storage, hold-container and scanning capacity values of the intake-match path are not specified | SCB IT infrastructure | Resolved (directive) |
| GAP-0994 | The Schedule window, the catch-up policy, the alert thresholds and the lag-alert identifier of the intake path are not specified | DevOps team | Resolved (directive) |
| GAP-1012 | The channel pickup has no target shape of its own: the run record, the rerun operation, the channel property layout, the single-run rule and the cross-service partner read are named by the legacy story only | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1013 | The channel-intake contract baseline fixes operation names, shapes and enumerations the sources do not name, and the plan's C list omits the partner read | Tech lead | Resolved (directive) |
| GAP-1014 | The four pickup channels, their credentials, their folder lifecycle, the partner DMZ position and the scan capacity are environment facts no source states | SCB IT infrastructure | Resolved (directive) |
| GAP-1015 | The deployment of the channel pickup has no source for its values, its chart key names, its Schedule ID, its catch-up window, its alert thresholds and its runbook entries | DevOps engineer | Resolved (directive) |
| GAP-1197 | The request and answer shape of the letter-copy handoff, the document type and source the hub assigns, the notice parameters, the P1 recipient field IDs, the payload field names of the event and the notice screen identifier are all unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1199 | No source describes the letter copy becoming an intake item at the document hub, and FSD P6 keeps a generated document as a stored document on the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1200 | The P6 module declares no notice parameter, so DP-06 has no named value to read | Business analyst | Resolved (directive) |
| GAP-1201 | The legacy access case and the legacy attach cases have no subject in rwb-comms, so the carried test cases prove the notice read instead | Test lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1202 | The event catalogue names rwb-decision as the only consumer of NoticeGenerated, while the document hub is expected to turn the copy into an intake item | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1203 | The base documents of the story are in review, not approved | Business analyst | Resolved (directive) |
| GAP-1272 | The partner access decision record has no operation, no field composition and no result vocabulary in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1273 | The append path of a partner access record is read synchronously while Arch v5 names it as a consumed event | Solution architect and integration lead | Resolved (directive) |
| GAP-1395 | DMZ network design, gateway product, FAPI 2.0 settings, external identity provider, certificate lifecycle, rate limits, WAF rule set and DR target of the partner gateway are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1482 | Partner instruction is an Epic 4 endpoint in the specification and an Epic 6 feature in the same specification | Partner and agency manager | Resolved (directive) |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1573 | The joiner, mover and leaver capability has a Must requirement in Epic 2, a feature code in Epic 1 and no legacy story, and its response times are open under DL38 | Business analyst with the security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1587 | FSD P5 takes branch, mailroom, SFTP and mailbox files inside P5 while Architecture v5 gives P5 no file interface | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1757 | The E4 vendor allocation depends on a partner capability delivered one wave later | Solution architect | Resolved (directive) |
| GAP-1835 | The FSD reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them and gives S9 no cell to P1 | Solution architect with the P1 owner | Resolved (directive) |
| GAP-1838 | partner_instruction.case_id is a cross-schema foreign key to recovery_case, while ADR-014 requires a business key and no foreign key out of the schema | Data architect with the platform DB owner | Resolved (directive) |
| GAP-1840 | No rule row covers allocation by measured return, scoring, review, fee approval, conduct sampling or the field app | Center of excellence analyst with P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1842 | Every FSD acceptance criterion in this module is the same generic statement, and no feature has an alternate flow or a background event | Business analyst, S9 | Resolved (directive) |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1845 | Epic 4 and Epic 5 need partner instructions in wave 3, while rwb-partner is created in wave 4 | Solution architect with the S4 and S5 owners | Resolved (directive) |
| GAP-1848 | The three staff screens and the four partner portal screens have no owner, and their first appearance precedes the service wave | Solution architect with the platform edge owner | Resolved (directive) |
| GAP-1849 | The partner portal base is /partner/v1/* in the FSD and in Architecture v5, while the naming rule is /api/recovery/<short>/v1 | Solution architect with the platform edge owner | Resolved (directive) |
| GAP-1850 | The FSD names no capability area and two of the four lists the module needs | Security administrator with the business analyst, S9 | Resolved (directive) |
| GAP-1851 | REQ-S9-002 (one named owner per partner type) is served by no feature, and no field holds the owner | Business analyst, S9 with the partner and agency manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1852 | Partner identity is a table in rwb_partner while the requirement that governs it is delivered by rwb-access | Security administrator with the P4 and S9 owners | Resolved (directive) |
| GAP-1856 | The scorecard measures, weights and thresholds are not in the sources, which repeat one metric for all fifteen features | Partner and agency manager with the center of excellence analyst | Resolved (directive) |
| GAP-2103 | The deck does not say whether a partner result is a partner record or a dated data product | Solution architect | Resolved (directive) |
| GAP-2184 | The retention class list, the added event codes, the link column types and the feature IDs of four requirements are in no source | Data architect | Resolved (directive) |
| GAP-2185 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2186 | The EFS outcome read and the contact-fact read that the channel consumer calls are named by interface only, with no path, parameter or owning story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2225 | Element names of the interaction item, the append command and the intake result are not in the sources | TechX and rwb-source-data contract owner | Resolved (directive) |
| GAP-2226 | Legacy occurred-time order and the case timeline page order differ | TechX | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2444 | DOCATT attach entry has no defined field set for the document reference, the intake item, the match method, the confidence, the final call and the message id | Solution architect, P7 | Resolved (directive) |
| GAP-2445 | The decision code list in force does not enumerate DOCATT in any source readable here | Reference data administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2446 | Whether an item held for a person leaves a decision record is not stated | Business analyst, P7 | Resolved (directive) |
| GAP-2447 | The DecisionRecorded payload of an attach has no defined field set | Solution architect, integration | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2449 | Login name, parameter names and message texts are not written in any source readable here | Tech lead, P7 | Resolved (directive) |
| GAP-2450 | The trigger of the ledger completeness check is not stated | Solution architect, P7 | Resolved (directive) |
| GAP-3103 | RWB-S9-AD022-APP: the partner user catalogue, the date trigger, the recall event and the legacy predecessor are unstated | Business analyst, S9; solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3104 | RWB-S9-AD022-CON: no element for the partner user, no operation name for the rwb-access read, and no ID mapping for the two events | Solution architect; tech lead of rwb-partner | Resolved (directive) |
| GAP-3106 | RWB-S9-E6029-APP: the onboarding write has no published operation, partner_user has no field list, the terms have no linking column, and the reference-data read has no plan row | Solution architect with the rwb-partner tech lead, the rwb-case reference-data owner and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3107 | RWB-S9-E6029-CON: the onboarding operation, the partner_user shape, the terms link, the consumed operation name and the conflict message have no published baseline | Solution architect with the rwb-partner tech lead and the rwb-case reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3108 | RWB-S9-E6030-APP: the panel slice owns no fee-schedule, service-level or version storage, publishes no write operation, and its feature has no requirement row | Solution architect | Resolved (directive) |
| GAP-3109 | RWB-S9-E6030-CON: the panel baseline has no published write operation, no path for the reference-data read, no status-to-message mapping and no level on the legacy cases | Solution architect | Resolved (directive) |
| GAP-3110 | Placement slice of S9: instruction columns, event names, service levels and the freshness message text are not published | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3111 | Placement contract of S9: request body, element property names, status vocabulary and four consumed operation names are not published | Tech lead | Resolved (directive) |
| GAP-3114 | The result-intake elements of rwb-partner are not fixed by any source: the 409 and 404 problem texts, the multipart bound, the decision code and version the local record names, the activity and signal names, and the retention of the request | Solution architect with the partner service owner | Resolved (directive) |
| GAP-3115 | The published shapes of the partner result contract are not fixed by any source: the multipart schema, the PartnerInstruction and InstructionPage element names, the event payload beyond three fields, the partner gateway profile and the error bodies | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3137 | The partner slice of RWB-E1-032 and its target service frame are not stated in any source | Solution architect | Resolved (directive) |
| GAP-3138 | The partner-origin channel of an intake item and its attach state are a boundary no source states | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3139 | Wave conflict: EP01 puts this story in wave 1 while rwb-partner is wave 4 in Arch v5 | Tech lead | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3141 | The two partner submission operations, the intake creation path and the PartnerDocumentSubmitted event are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3142 | The intake bound, the decision code and version, and the two lists in force are not named | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3143 | No data model carries a partner-side submission row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3144 | No source states how the legacy criteria split between the document-hub and partner slices | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3145 | The partner portal screen that submits a file is not fixed | Business analyst | Resolved (directive) |
| GAP-3147 | EP02 wave 2 for rwb-partner while the service's Architecture v5 wave is 4 | Solution architect | Resolved (directive) |
| GAP-3148 | The rwb-partner slice of the key has no published load path, no message per condition and no partner_user catalogue | Solution architect with the reference data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3149 | rwb-partner interaction-ledger slice: no ledger column or operation in S9, no published payload for EV-20 or EV-21, the seam with RWB-P2-E2034-CON undefined, the list members, the retry bound and the holder-reference form unpublished, and an empty H row against ten platform contracts | Solution architect; rwb-integration contract owner (RWB-P2-E2034-CON); rwb-source-data ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3174 | Service S9 takes Epic 1 stories in wave 1 although its Arch v5 wave is 4 | Delivery lead | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3181 | The partner_user table is created by P4 in the story and owned by S9 in the ownership map | Access lead with the partner lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S9-AD022-APP | skipped AC ID | 111 | missing: AC1, AC8 |
| RWB-S9-E1032-APP | unknown story key | 27 | RWB-S9-E1032-CON is not a story of the set: \| Contract dependencies \| RWB-P5-E1032-CON; RWB-S9-E1032-CON \| |
| RWB-S9-E1032-APP | unknown story key | 28 | RWB-S9-E1032-CON is not a story of the set: \| Contract version \| v1 of RWB-S9-E1032-CON, path /api/recovery/partner/v1; frame per GAP-3137 \| |
| RWB-S9-E1032-APP | unknown story key | 393 | RWB-S9-E1032-CON is not a story of the set: \| DP table record (GAP-2448) \| Dependency rows of DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19; the metadata rows stay as the work pac |
| RWB-S9-E2019-APP | unknown story key | 28 | RWB-S9-E2019-CON is not a story of the set: \| Contract dependencies \| RWB-P4-E2019-CON, RWB-S9-E2019-CON \| |
| RWB-S9-E2019-APP | unknown story key | 351 | RWB-S9-E2019-CON is not a story of the set: \| rwb-partner contract fake (RWB-S9-E2019-CON) \| The rwb-partner operations of 12.1 \| Not specified in the source documents (DOR-RWB-S9-E201 |
| RWB-S9-E2034-APP | skipped AC ID | 108 | missing: AC9, AC10, AC11 |
| RWB-S9-E2034-APP | duplicate TC ID | 457 | TC-E2-034-13 |
| RWB-S9-E2034-APP | duplicate TC ID | 458 | TC-E2-034-14 |
| RWB-S9-E2034-APP | Not specified without item ID | 429 | No screen is built here. The partner entry appears on SCR-04 Case timeline, whose states — Loading, Filtered and Empty with MSG-P3-024, Error (Not specified in |
| RWB-S9-E6030-APP | skipped AC ID | 118 | missing: AC1, AC4 |
