# RWB-ITG-W1 Wave 1 integration - review pack, part 5 of 5 (RWB-ITG-E1066-ITG to RWB-ITG-W1J02-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 183 |
| Cross-document (pending in another document) | 218 |
| Not applied (value not in the sources) | 21 |
| Open business decisions | 15 |
| Register gaps linked | 136 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E1066-ITG | 23 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1066 ITG Interaction ledger store and writer - integration v2.md |
| RWB-ITG-E1067-ITG | 16 | 11 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1067 ITG Every Workbench action into the interaction ledger - integration v2.md |
| RWB-ITG-E1069-ITG | 8 | 37 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1069 ITG Read-only ACE source views, grants and boundary rule - integration v2.md |
| RWB-ITG-E1070-ITG | 11 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1070 ITG Temporal platform on the ACE AKS clusters - integration v2.md |
| RWB-ITG-E1073-ITG | 22 | 41 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1073 ITG Rule authoring, validation, test scenarios, approval and rollback in Drools - integration v2.md |
| RWB-ITG-TE004-ITG | 10 | 14 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG TE004 ITG Masked data in SIT and UAT - integration v2.md |
| RWB-ITG-TE006-ITG | 12 | 27 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG TE006 ITG Outbox and retry for outbound work - integration v2.md |
| RWB-ITG-TE008-ITG | 17 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG TE008 ITG Decision log hash chain check - integration v2.md |
| RWB-ITG-TE013-ITG | 30 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG TE013 ITG Agent runtime client with fallback - integration v2.md |
| RWB-ITG-W1J01-ITG | 13 | 12 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J01 ITG Contract-test harness and synthetic test data - integration v2.md |
| RWB-ITG-W1J02-ITG | 21 | 9 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J02 ITG Wave 1 v5 journey end to end - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1067-ITG | R-09406 | CG-ALL-432 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1073-ITG | R-09418 | CG-ALL-465 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-TE008-ITG | R-09557 | CG-ALL-500 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1066-ITG, RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1066-OPS, RWB-P3-E1066-APP | R-22263 | GAP-2253 | Register gap | rwb-case reference data owner and Compliance | LOV-LEDGER-EVENT carries 14 values in the TSD and 12 in the legacy story | Load the fourteen values of TSD P3 v3 T5.1 as the reference rows of LOV-LEDGER-EVENT, with PARTNER_RESULT and OFFER included and the Thai labels of DL10, and let RWB-P1-E1066-CON validate against the same list; the two extra values add no rule and remove none. |
| RWB-ITG-E1069-ITG, RWB-P1-E1069-APP, RWB-P1-E1069-DB, RWB-P4-E1069-APP | R-22278 | GAP-0901 | Register gap | Compliance and PDPA officer | rwb-access ACE masking pack: no source names which ACE view fields the masking rows must cover or at which field IDs | Publish the masking field map as part of the pack design: one row per personal field ID of the 30 views with the role that may see it, agreed by the Compliance and PDPA officer, and load it with the pack instead of leaving the set to the story. |
| RWB-ITG-TE004-ITG, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP | R-22911 | GAP-1675 | Register gap | Compliance | The masking and scrubbing list for telemetry is not stated | Publish the masked and scrubbed field list per role, and apply it to the telemetry pipeline and the prompt path. |
| RWB-ITG-TE006-ITG, RWB-PLT-N009-APP, RWB-PLT-N009-CON, RWB-PLT-TE006-APP, RWB-PLT-TE006-CON | R-22913 | GAP-1674 | Register gap | Compliance | The retention of the platform rows, of the stored idempotent answer and of the telemetry is not stated | Set the retention per platform object under DL26 and record it in the Logical Data Model next version. |
| RWB-ITG-E1073-ITG, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28681 | GAP-0006 | Register gap | RW-COE and RW-RISK | Rule format XLS decision tables or DMN 1.6 | Keep XLS tables for the Phase 1 packages and convert one table at a time, with both formats on the same runtime |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28693 | GAP-2047 | Register gap | Solution architect with Risk and Internal Audit | The decision log is now written locally by each service and sealed centrally | Version 4 measures the local decision record of each service and the central ledger of P7 rwb-decision as two instances of the same two alerts, with the chain check read per service and once for the ledger. |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28694 | GAP-2051 | Register gap | P7 rwb-decision with Compliance and Internal Audit | The hash chain check now spans 19 local chains and one central ledger | Version 4 raises the alert on the local chain of each service and once on the central ledger, and attributes a break to the service whose chain fails; the run book of RWB-E1-073 and RWB-E2-037 names the check. |
| RWB-ITG-TE013-ITG, RWB-P10-TE013-APP, RWB-P10-TE013-CON, RWB-P10-TE013-OPS, RWB-P7-TE013-APP | R-28926 | GAP-1320 | Register gap | P10 agent runtime business analyst with the model risk officer | No source fixes the model version of agent INTAKE, which the entry must carry | The model version of agent INTAKE is fixed with the approved policy of the agent in RWB-P10-TE013-CON and RWB-P10-TE013-APP and arrives inside the record; the fixtures of this story carry a synthetic model version and the criteria assert presence, not a value |
| RWB-ITG-E1073-ITG | R-33383 | ASM-ALL-465 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E1067-ITG | R-03645 | DOR-RWB-ITG-E1067-ITG-14 | 3 | Definition of Ready item 14 Epic design: Fail | Needs a signed epic design record for RWB-ITG-W1. None found in folders 0*, 22 or the Template and Rules v1. Sign-off is an approval; it cannot be invented. |
| RWB-ITG-E1067-ITG | R-03646 | DOR-RWB-ITG-E1067-ITG-16 | Header | Definition of Ready item 16 Size: Fail | Size row added as Not specified in the source documents; no size value exists, so the item stays open until the squad sizes the story. |
| RWB-ITG-E1067-ITG | R-03649 | DOR-RWB-ITG-E1067-ITG-23 | Header | Definition of Ready item 23 Contract version fixed: Fail | Contract version row gives the /v1 path only; the full version is not specified in the source documents, so the item stays open. |
| RWB-ITG-E1067-ITG | R-14147 | DOR-RWB-ITG-E1067-ITG-17 | Header | Definition of Ready item 17 Dependencies: Partial | Depends on (build) stays None, matching section 3 (no build dependency, ready on Day 1). The three APP stories are already named under Integration dependencies. |
| RWB-ITG-E1069-ITG | R-03651 | DOR-RWB-ITG-E1069-ITG-16 | header | Definition of Ready item 16 Size: Fail | The source documents give no size. The Size row carries the not-specified marker, and the item stays open until the story is sized. |
| RWB-ITG-E1069-ITG | R-14153 | DOR-RWB-ITG-E1069-ITG-17 | header | Definition of Ready item 17 Dependencies: Partial | Build status: clears only once RWB-P1-E1069-APP and RWB-P4-E1069-APP are built. Story text cannot supply it; the header already lists both as integration dependencies. |
| RWB-ITG-E1069-ITG | R-29872 | NEWAC-RWB-ITG-E1069-ITG-AC8 | 7, 16 | AC8: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Section 9 has no case status and no business row; its states define no disallowed transition. An AC8 and its TC would need an invented transition and test. |
| RWB-ITG-E1070-ITG | R-03661 | DOR-RWB-ITG-E1070-ITG-23 | header | Definition of Ready item 23 Contract version fixed: Fail | The story uses published activity contract jars, but no version is in the story or the source documents. The header row records the gap and invents no version. |
| RWB-ITG-E1073-ITG | R-03664 | DOR-RWB-ITG-E1073-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size exists in the sources. The header carries a Not specified placeholder only. |
| RWB-ITG-E1073-ITG | R-03666 | DOR-RWB-ITG-E1073-ITG-21 | header | Definition of Ready item 21 Contract published: Fail | This integration story provides no operation of its own, so it has no contract to publish. The Contract dependencies row lists the contracts it consumes. |
| RWB-ITG-E1073-ITG | R-03667 | DOR-RWB-ITG-E1073-ITG-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | At integration level the real services replace the contract fakes (section 12.8), so no fake is needed for this story. |
| RWB-ITG-TE004-ITG | R-04147 | DOR-RWB-ITG-TE004-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or the source excerpts; searched for this epic's sign-off and found none, so it cannot be confirmed. |
| RWB-ITG-TE004-ITG | R-04148 | DOR-RWB-ITG-TE004-ITG-16 |  | Definition of Ready item 16 Size: Fail | No size in the story or the source excerpts; the size is the squad's refinement estimate, so no value can be recorded without inventing one. |
| RWB-ITG-TE004-ITG | R-04149 | DOR-RWB-ITG-TE004-ITG-21 | header | Definition of Ready item 21 Contract published: Fail | No contract story for this key is in the source set; the header Contract dependencies reads Not specified in the source documents. |
| RWB-ITG-TE006-ITG | R-04154 | DOR-RWB-ITG-TE006-ITG-16 | header | Definition of Ready item 16 Size: Fail | Size row added, but the size itself is set by the squad at refinement; no size is available in the source documents, so DoR item 16 remains open. |
| RWB-ITG-TE006-ITG | R-30086 | NEWAC-RWB-ITG-TE006-ITG-AC12 | 7, 16 | AC12: a status change the model does not allow is refused (no criterion covers a disallowed transition) | AC6 already covers a disallowed transition: resending a DELIVERED delivery is refused (MSG-P2-022). A further criterion would duplicate it, so none was added. |
| RWB-ITG-W1J01-ITG | R-04182 | DOR-RWB-ITG-W1J01-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | Source excerpts hold no line for a signed epic design (DoR item 14; decision log DT05; ways of working; stakeholder map); recording a sign-off would invent an approval. |
| RWB-ITG-W1J01-ITG | R-04183 | DOR-RWB-ITG-W1J01-ITG-16 | header | Definition of Ready item 16 Size: Fail | Size row added as Not specified; the item stays open until the squad sizes the story at refinement. |
| RWB-ITG-W1J01-ITG | R-04185 | DOR-RWB-ITG-W1J01-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | Source excerpts hold no published contract fake library version; Catalog v2 7.2 (staged) gives only the name and version rule, and 12.8 leaves the stub location unspecified (GAP-0384). |
| RWB-ITG-W1J01-ITG | R-14706 | DOR-RWB-ITG-W1J01-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | Small cannot be confirmed until the squad sizes the story at refinement. |
| RWB-ITG-W1J02-ITG | R-14713 | DOR-RWB-ITG-W1J02-ITG-15 |  | Definition of Ready item 15 INVEST: Partial | No size is stated in the sources, so a two-week fit cannot be asserted; the squad sets the size at refinement. |

## 5. Cross-document changes (pending in the target document)


### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00931 | RWB-ITG-E1066-ITG | DOR-RWB-ITG-E1066-ITG-1 | 1 | Add role 'QA integration engineer' or map it to an existing role code and name |
| CDC-00942 | RWB-ITG-E1067-ITG | DOR-RWB-ITG-E1067-ITG-1 | 1 | Add a role name and code for QA integration engineer so the §1 role resolves. |
| CDC-00964 | RWB-ITG-E1069-ITG | DOR-RWB-ITG-E1069-ITG-1 | 1 | Add a role code or name for 'tech lead', or confirm the role code used in section 1. |
| CDC-01000 | RWB-ITG-E1070-ITG | DOR-RWB-ITG-E1070-ITG-1 | 1 | Register QA integration engineer as a role name, or map the story role to an existing role code. |
| CDC-01003 | RWB-ITG-E1070-ITG | GAP-2038 | find it | Set SY-CASEWF to the identity of P3 rwb-case only, reached through the CaseWorkflow signal; read SY-RULES as one role held by each service identity inside its runtime. |
| CDC-01017 | RWB-ITG-E1073-ITG | DOR-RWB-ITG-E1073-ITG-1 | 1 | No role code for 'tech lead' exists in the sources. The story keeps its persona unchanged. |
| CDC-02202 | RWB-ITG-TE004-ITG | DOR-RWB-ITG-TE004-ITG-1 | 1 | Add the role 'QA integration engineer' with its role code, which is Not specified in the source documents (DOR-RWB-ITG-TE004-ITG-1). |
| CDC-02204 | RWB-ITG-TE004-ITG | DOR-RWB-ITG-TE004-ITG-6 | 10 | Add role SY-DATALOAD (data load identity) to Users Roles and Permissions v5. |
| CDC-02225 | RWB-ITG-TE006-ITG | DOR-RWB-ITG-TE006-ITG-1 | 1 | Add the role code or name 'tech lead' that section 1 uses, so the role resolves to a listed entry. |
| CDC-02245 | RWB-ITG-TE008-ITG | DOR-RWB-ITG-TE008-ITG-1 | 1 | Add tech lead as a role name, or name the role code section 1 should use |
| CDC-02297 | RWB-ITG-W1J01-ITG | DOR-RWB-ITG-W1J01-ITG-1 | 1 | Add a role code or role name for the QA team member that section 1 can cite, replacing the unlisted 'member of the QA team'. |
| CDC-02307 | RWB-ITG-W1J02-ITG | DOR-RWB-ITG-W1J02-ITG-1 | 1 | Add a role code for member of the QA team, or confirm an existing role code, so section 1 names a role that is in the document. |
| CDC-02308 | RWB-ITG-W1J02-ITG | DOR-RWB-ITG-W1J02-ITG-6 | 10 | Add role RW-OFF (recovery officer) to the role list so that section 10 of the story has a matching role. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00930 | RWB-ITG-E1066-ITG | CG-ALL-426 | 16 | Add rows TC-ITG-E1066-01 (AC9, BR8, BR9) and TC-ITG-E1066-02 (AC10, BR8, BR10) with Given, When and Then copied from AC9 and AC10 |
| CDC-00932 | RWB-ITG-E1066-ITG | DOR-RWB-ITG-E1066-ITG-12 | 16 | Add the test cases TC-ITG-E1066-01 and TC-ITG-E1066-02 with their Given, When and Then (AC9, AC10); also TC-ITG-E1066-03 and TC-ITG-E1066-04 added here. |
| CDC-00941 | RWB-ITG-E1067-ITG | CG-ALL-430 | 16 | Add rows TC-ITG-E1067-01 to TC-ITG-E1067-04 with Given, When and Then copied from ACs 6 to 9 of this story. |
| CDC-00963 | RWB-ITG-E1069-ITG | CG-ALL-441 | section 16 | TC-ITG-E1069-01 to 06 are missing from Test Cases v8. The new TC-ITG-E1069-07 also needs a row in the next workbook version. |
| CDC-01016 | RWB-ITG-E1073-ITG | CG-ALL-460 |  | Add rows TC-ITG-E1073-01 to TC-ITG-E1073-05 to Story test cases in the next version, with Given, When and Then copied from AC1 to AC5. |
| CDC-01018 | RWB-ITG-E1073-ITG | DOR-RWB-ITG-E1073-ITG-12 | 12, 16, 18 | Add rows TC-ITG-E1073-01 to TC-ITG-E1073-05 to tab Story test cases; check section 18 lists against RTM v7. |
| CDC-02201 | RWB-ITG-TE004-ITG | CG-ALL-471 | 16 | Add rows for TC-ITG-TE004-01 to TC-ITG-TE004-05 with Given, When and Then copied from the criteria AC1 to AC5 they cover. |
| CDC-02224 | RWB-ITG-TE006-ITG | CG-ALL-486 | 16 | Add rows TC-ITG-TE006-01 to TC-ITG-TE006-06 to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-02244 | RWB-ITG-TE008-ITG | CG-ALL-497 | 16 | Add rows TC-ITG-TE008-01 to TC-ITG-TE008-05 to the next version, with Given, When and Then copied from the criteria they cover |
| CDC-02277 | RWB-ITG-TE013-ITG | CG-ALL-508 | 16 | Add rows TC-ITG-TE013-01 to TC-ITG-TE013-05 to Story test cases with Given, When and Then copied from AC1 to AC5 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00961 | RWB-ITG-E1069-ITG | CG-ALL-436 | 12.7 | Record ace_view_owner (owner role of the 30 recovery.v_ace_* views) as an object in the owning document, or use its dictionary name. |
| CDC-00962 | RWB-ITG-E1069-ITG | CG-ALL-437 | 12.7 | Record v_data_dictionary (dictionary view read on the rwb_source_data login) as an object in the owning document, or use its dictionary name. |
| CDC-00966 | RWB-ITG-E1069-ITG | DOR-RWB-ITG-E1069-ITG-7 | 11 | Register ace_view_owner and v_data_dictionary as database objects, or record the harness's direct view reads as an accepted test-only exception. |
| CDC-00998 | RWB-ITG-E1070-ITG | CG-ALL-444 |  | Record temporal_visibility as the Temporal visibility database owned by temporal_svc, or give it its dictionary name. |
| CDC-00999 | RWB-ITG-E1070-ITG | CG-ALL-445 |  | Record temporal_svc as the login owning the temporal and temporal_visibility databases, or give it its dictionary name. |
| CDC-01001 | RWB-ITG-E1070-ITG | DOR-RWB-ITG-E1070-ITG-7 | 11 | Register temporal_svc and temporal_visibility as entities or fields in LDM v9 and Data Classification v5. |
| CDC-02200 | RWB-ITG-TE004-ITG | CG-ALL-466 | 11 | No dictionary name fits; the name tool_run stays in the story until the owning document records the object. Only the row's first cell changed, under DOR-7. |
| CDC-02205 | RWB-ITG-TE004-ITG | DOR-RWB-ITG-TE004-ITG-7 | 11 | Add `tool_run` (schema tools) as an entity or field. The §11 row now carries a Not specified placeholder for its BR Field ID. |
| CDC-02227 | RWB-ITG-TE006-ITG | DOR-RWB-ITG-TE006-ITG-7 | 11 | Confirm or register ce_id, ce_source, ce_type, ce_schemaurl and the four further ce_ names flagged by detcheck as LDM fields. |
| CDC-02246 | RWB-ITG-TE008-ITG | DOR-RWB-ITG-TE008-ITG-7 | 11 | Missing field IDs in section 11 are marked Not specified. Entity decision_record still needs to be recorded in LDM v9 and Data Classification v5. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00953 | RWB-ITG-E1069-ITG | CG-ALL-440 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-01011 | RWB-ITG-E1073-ITG | CG-ALL-454 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-02196 | RWB-ITG-TE004-ITG | CG-ALL-467 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or agree a published operation to consume. |
| CDC-02210 | RWB-ITG-TE006-ITG | CG-ALL-482 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-02237 | RWB-ITG-TE008-ITG | CG-ALL-493 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-02273 | RWB-ITG-TE013-ITG | CG-ALL-504 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise in rwb-access.yaml via the provider's CON story; story unchanged. |
| CDC-02291 | RWB-ITG-W1J01-ITG | CG-ALL-514 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or the consumer takes a published operation. |
| CDC-02302 | RWB-ITG-W1J02-ITG | CG-ALL-519 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access CON story, or the story must consume a published operation instead. |
| CDC-02306 | RWB-ITG-W1J02-ITG | DOR-RWB-ITG-W1J02-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise (CG-ALL-519). The CG-ALL-518 and CG-ALL-520 story-side rows are resolved in this chunk. |

### Epic design record (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00928 | RWB-ITG-E1066-ITG | DOR-RWB-ITG-E1066-ITG-14 | n/a | Record the signed epic design sign-off for RWB-ITG-W1 and EP01 |
| CDC-00954 | RWB-ITG-E1069-ITG | DOR-RWB-ITG-E1069-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-W1, which is not in the story or source documents. |
| CDC-00990 | RWB-ITG-E1070-ITG | DOR-RWB-ITG-E1070-ITG-14 | header | Record the signed epic design sign-off for the epic that this story belongs to. |
| CDC-01012 | RWB-ITG-E1073-ITG | DOR-RWB-ITG-E1073-ITG-14 | header | Confirm the signed epic design sign-off and record it in the epic design record. |
| CDC-02212 | RWB-ITG-TE006-ITG | DOR-RWB-ITG-TE006-ITG-14 |  | Confirm the signed epic design for RWB-ITG-W1 and record the sign-off reference. |
| CDC-02239 | RWB-ITG-TE008-ITG | DOR-RWB-ITG-TE008-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-W1 in the epic design record. |
| CDC-02274 | RWB-ITG-TE013-ITG | DOR-RWB-ITG-TE013-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-TE013-ITG. |
| CDC-02303 | RWB-ITG-W1J02-ITG | DOR-RWB-ITG-W1J02-ITG-14 |  | Record the signed epic design of RWB-ITG-W1 and its sign-off date so DoR item 14 can be marked met for RWB-ITG-W1J02-ITG. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00947 | RWB-ITG-E1067-ITG | CG-ALL-431 | 18 | Align the test case lists for REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007 to section 18 of RWB-ITG-E1067-ITG, which matches its section 16 IDs. |
| CDC-00979 | RWB-ITG-E1069-ITG | CG-ALL-442 | 18 | Align REQ-RDF-002 and REQ-DRI-006 test lists between section 18 of RWB-ITG-E1069-ITG and the RTM in their next versions. |
| CDC-01034 | RWB-ITG-E1073-ITG | CG-ALL-462 | 18 | Align the test lists for the four requirements in the next RTM version with section 18 of RWB-ITG-E1073-ITG. |
| CDC-02208 | RWB-ITG-TE004-ITG | CG-ALL-473 | 18 | In the next RTM version, align the test lists for REQ-RDF-010 and the second differing requirement with section 18 of RWB-ITG-TE004-ITG. |
| CDC-02233 | RWB-ITG-TE006-ITG | CG-ALL-488 | 18 | Align the REQ-DRI-007 test list with RWB-ITG-TE006-ITG section 18 (TC-TE-006-01-ITG to -13-ITG, TC-ITG-TE006-01 to -07) in the next version. |
| CDC-02248 | RWB-ITG-TE008-ITG | CG-ALL-499 | 18 | Align REQ-DRI-003 test cases to TC-ITG-TE008-01 to TC-ITG-TE008-10 in the next RTM version. |
| CDC-02283 | RWB-ITG-TE013-ITG | CG-ALL-510 | 18 | Align the test lists of REQ-DRI-001 and the other differing requirements with RWB-ITG-TE013-ITG section 18 in the next RTM version. |
| CDC-02310 | RWB-ITG-W1J02-ITG | CG-ALL-522 | 18 | Trace the 12 requirements listed in the evidence to the same test cases as section 18 of RWB-ITG-W1J02-ITG. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01031 | RWB-ITG-E1073-ITG | GAP-2457 | find it | Give physical columns, types and nullability for rule_package, rule_package_version, rule_row and rule_test_case on the DF-REF-274 to DF-REF-299 field names; confirm artifact columns with RWB-PLT-E1072-CON. |
| CDC-02217 | RWB-ITG-TE006-ITG | CG-ALL-475 | 4 | Record ce_id as a CloudEvents 1.0 transport attribute object in LDM v9 Fields, or name the dictionary field it maps to. |
| CDC-02218 | RWB-ITG-TE006-ITG | CG-ALL-476 | 4 | Record ce_source as a CloudEvents 1.0 transport attribute object in LDM v9 Fields, or name the dictionary field it maps to. |
| CDC-02219 | RWB-ITG-TE006-ITG | CG-ALL-477 | 4 | Record ce_type as a CloudEvents 1.0 transport attribute object in LDM v9 Fields, or name the dictionary field it maps to. |
| CDC-02220 | RWB-ITG-TE006-ITG | CG-ALL-478 | 4 | Record ce_schemaurl as a CloudEvents 1.0 transport attribute object in LDM v9 Fields, or name the dictionary field it maps to. |
| CDC-02221 | RWB-ITG-TE006-ITG | CG-ALL-479 | 4 | Record ce_time as a CloudEvents 1.0 transport attribute object in LDM v9 Fields, or name the dictionary field it maps to. |
| CDC-02222 | RWB-ITG-TE006-ITG | CG-ALL-480 | 4 | Record ce_idempotencykey as a CloudEvents 1.0 transport attribute object in LDM v9 Fields, or name the dictionary field it maps to. |
| CDC-02223 | RWB-ITG-TE006-ITG | CG-ALL-481 | 11 | Record decision_record as the entity carried on rwb.decision-record.v1 in LDM v9 Fields, or name the dictionary field it maps to. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00937 | RWB-ITG-E1066-ITG | GAP-0267 | 1 | Set the Owner column to P1 rwb-source-data on the 29 interaction fields, and show P3 rwb-case as the reader for the case timeline. |
| CDC-00968 | RWB-ITG-E1069-ITG | GAP-0014 | find it | Add the v5 tables for S1 and P8 and populate the FK cuts sheet with ID references. |
| CDC-00969 | RWB-ITG-E1069-ITG | GAP-0110 | find it | Record the 30 recovery.v_ace_* views as read-only in schema recovery in recovery_views.sql, and v_data_dictionary in rwb_source_data. |
| CDC-00970 | RWB-ITG-E1069-ITG | GAP-0259 | find it | Set Owner to P1 rwb-source-data (recovery view) on all 304 view fields, and grant no other service login any view. |
| CDC-01015 | RWB-ITG-E1073-ITG | GAP-1329 |  | Use the /admin/rule-versions family for the registry in both documents, and either publish GET /rule-catalog as an owned operation or remove it from the consumed set. |
| CDC-01023 | RWB-ITG-E1073-ITG | GAP-0700 |  | Add rows for the seven operations (load, version list, approve, rollback, dry run, model read, catalog read) under P7 with rights, answers and error codes. |
| CDC-02206 | RWB-ITG-TE004-ITG | GAP-0379 | 10 | Publish before the first SIT masked copy: the table-to-schema map, verifier owner, partial-failure rule and PII extract contract (manifest fields, file format, delivery window). Story §10 names the Solution architect as owner. |

### API:(service not named) (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00936 | RWB-ITG-E1066-ITG | GAP-2072 | 1 | Correct the x-module of GET and POST /cases/{caseId}/interactions from P3 to P1, and correct TSD T3.1 interaction to P1 rwb-source-data. |
| CDC-00948 | RWB-ITG-E1067-ITG | GAP-2072 | 8 | Move the interaction table and GET and POST /cases/{caseId}/interactions to P1 rwb-source-data (x-module P1); rwb-case reads through the P1 contract. |
| CDC-00950 | RWB-ITG-E1067-ITG | GAP-1058 | header | Add the JSON Schema registry subject name of the DocumentStored message under x-topic schema-registry |
| CDC-01013 | RWB-ITG-E1073-ITG | DOR-RWB-ITG-E1073-ITG-23 | header | Contract version row added as Not specified in the source documents. |
| CDC-01014 | RWB-ITG-E1073-ITG | DOR-RWB-ITG-E1073-ITG-8 |  | Publish GET and POST /api/recovery/decision/v1/admin/rule-versions, POST .../{versionId}/approve and POST .../{versionId}/rollback, and the two further paths named in the detcheck. |
| CDC-01028 | RWB-ITG-E1073-ITG | GAP-2458 |  | Add a paged open-case fact read filtered by status, returning product group, queue, region, exposure band and deviation flag; the dry run uses it with the 2 s one-hop timeout. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01006 | RWB-ITG-E1073-ITG | CG-ALL-449 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-versions through the provider's CON story. |
| CDC-01007 | RWB-ITG-E1073-ITG | CG-ALL-450 | 12.2 | Publish POST /api/recovery/decision/v1/admin/rule-versions through the provider's CON story. |
| CDC-01008 | RWB-ITG-E1073-ITG | CG-ALL-451 | 12.2 | Publish POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve through the provider's CON story. |
| CDC-01009 | RWB-ITG-E1073-ITG | CG-ALL-452 | 12.2 | Publish POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/rollback through the provider's CON story. |
| CDC-01010 | RWB-ITG-E1073-ITG | CG-ALL-453 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{n}/{v} through the provider's CON story. |
| CDC-02294 | RWB-ITG-W1J01-ITG | CG-ALL-517 | 12.2 | Provider to confirm the full path under base /api/recovery/decision/v1; yaml lists /admin/rule-packages/{packageCode}/versions with GET and POST. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00951 | RWB-ITG-E1069-ITG | CG-ALL-438 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the provider's CON story. |
| CDC-00952 | RWB-ITG-E1069-ITG | CG-ALL-439 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} through the provider's CON story. |
| CDC-02197 | RWB-ITG-TE004-ITG | CG-ALL-468 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} in rwb-source-data.yaml through the provider's CON story, or agree a published operation to consume. |
| CDC-02198 | RWB-ITG-TE004-ITG | CG-ALL-469 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} in rwb-source-data.yaml through the provider's CON story, or agree a published operation to consume. |
| CDC-02290 | RWB-ITG-W1J01-ITG | CG-ALL-513 | 12.2 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready through the provider's CON story, or the consumer takes a published operation. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01004 | RWB-ITG-E1070-ITG | GAP-2017 | find it | Write rwb-platform as the platform team queue outside the 19 service queues, with its smoke and health workflows and owner. |
| CDC-02238 | RWB-ITG-TE008-ITG | CG-ALL-495 | 12.5 | Workflows sheet: add ChainCheckWorkflow (task queue rwb-decision, started by JOB-14) and name it in the JOB-14 workflow column, now Not specified (GAP-0145; ASM-0226). |
| CDC-02243 | RWB-ITG-TE008-ITG | CG-ALL-496 | 12.5 | Add Activities row for ingestDecisionRecord on task queue rwb-decision, or name a catalogued activity in 12.5 |
| CDC-02275 | RWB-ITG-TE013-ITG | DOR-RWB-ITG-TE013-ITG-8 | 12.4 | Add activity Decision-record ingest of rwb-decision to the Temporal Catalog v1. |
| CDC-02276 | RWB-ITG-TE013-ITG | CG-ALL-507 | 12.5 | Add an Activity row for Decision-record ingest of rwb-decision on task queue rwb-decision, owned by RWB-P7-TE013-APP, or name a catalogued activity |

### RWB-PLT-TE006-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02214 | RWB-ITG-TE006-ITG | DOR-RWB-ITG-TE006-ITG-22 | 12.8 | No contract fake is named for rwb-access; fake library version is Not specified in the source documents. Publishing the fake belongs to the platform contract. |
| CDC-02228 | RWB-ITG-TE006-ITG | GAP-1416 |  | Publish one versioned library artifact with three interfaces and exceptions, DDL for four tables incl. processed_event and idempotency_key, CloudEvents attributes with caseId and ce_type, inbox dedupe rule, retry ladder 1 min/10 min/1 h with dead-letter topic, one alert and replay tool, and ownership of case events, task and decision record. |
| CDC-02230 | RWB-ITG-TE006-ITG | GAP-1666 |  | Publish one retry table: three retries per outbound item to the exception queue (P2), retry topics 1/10/60 min then .dlt with alert for events, and 10 Temporal activity attempts with a non-retryable list. |
| CDC-02231 | RWB-ITG-TE006-ITG | GAP-0382 | 11 | Section 11 names the DEV retries and three consumers; case-event mapping and final dead-letter values remain with the platform contract. |
| CDC-02232 | RWB-ITG-TE006-ITG | GAP-1415 | 18 | Traceability row uses the Kafka retry ladder and a continuous relay worker; ownership of the exception path remains in the platform library contract. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00944 | RWB-ITG-E1067-ITG | DOR-RWB-ITG-E1067-ITG-12 | 16 | Story test rows in section 16 are complete; TC-ITG-E1067-01 to -07 must be added to Test Cases v8 and RTM v7 aligned to section 18. |
| CDC-00965 | RWB-ITG-E1069-ITG | DOR-RWB-ITG-E1069-ITG-12 | 16 | Test Cases v8: add TC-ITG-E1069-01 to -06 rows. RTM v7: align its test lists for REQ-RDF-002 and REQ-DRI-006 with section 18. |
| CDC-02226 | RWB-ITG-TE006-ITG | DOR-RWB-ITG-TE006-ITG-12 | 12, 16, 18 | Register TC-ITG-TE006-01 to TC-ITG-TE006-07 in Test Cases v8 and align the RTM v7 test lists with section 18. |
| CDC-02278 | RWB-ITG-TE013-ITG | DOR-RWB-ITG-TE013-ITG-12 | 16 | Test Cases v8: add TC-ITG-TE013-01 to -05 rows. RTM v7: align the section 18 test lists to the story |

### RWB-P6-E1073-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01030 | RWB-ITG-E1073-ITG | GAP-1214 |  | The local copy table, parameter read path, check names and run record remain unspecified; the story builds against fakes meanwhile. |
| CDC-01045 | RWB-ITG-E1073-ITG | GAP-1215 | header | At the next rules-of-record pass, correct either the DP-04 row (H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON) or the plan line for RWB-P6-E1073-APP (Contract dependencies RWB-P3-E1073-CON) so they agree. Keep the plan line as written until then. |
| CDC-01046 | RWB-ITG-E1073-ITG | GAP-1218 | header | Add RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON to Depends on (build). Keep Ready to start Day 1. |

### RWB-P1-E1066-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00929 | RWB-ITG-E1066-ITG | DOR-RWB-ITG-E1066-ITG-21 | header | Story side: Contract dependencies now names RWB-P1-E1066-CON. Publication of the contract must be confirmed in that contract story. |
| CDC-00935 | RWB-ITG-E1066-ITG | GAP-2256 | 12 | The missing rwb-case counterparts of API-P3-015 and API-P3-014 belong to the API specification; no story edit made for this item. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00955 | RWB-ITG-E1069-ITG | DOR-RWB-ITG-E1069-ITG-21 | header | Contract dependencies row reads the not-specified marker |
| CDC-00957 | RWB-ITG-E1069-ITG | DOR-RWB-ITG-E1069-ITG-8 | header | Publish GET source-data accounts/{id}, GET source-data customers/{id} and POST access/v1/authorise. |

### RWB-P1-E1069-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00976 | RWB-ITG-E1069-ITG | GAP-1509 | find it | Record the 365-day stale rule as data and assign one writer for valuation_ext.stale_flag and valuation_ext.age_days, until then this service writes both. |
| CDC-00986 | RWB-ITG-E1069-ITG | GAP-2040 | 16 | Hold the Read-only ACE grant view conformance test in the P1 slice as sole grant holder with the ACE DBA; P4 keeps role and masking checks; v5 names RWB-E1-069 as the view test and the per-service boundary test as the cross-schema check. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00989 | RWB-ITG-E1070-ITG | CG-ALL-447 | 12.5 | Add a Workflows row for PlatformSmokeWorkflow with workflow ID platform-smoke-20261116 from the platform workflow kit, or confirm the catalogued workflow name. |
| CDC-00992 | RWB-ITG-E1070-ITG | DOR-RWB-ITG-E1070-ITG-8 | 12.5 | Add the PlatformSmokeWorkflow row for workflow ID platform-smoke-20261116 from the platform workflow kit, as in CG-ALL-447. |

### RWB-P3-E1073-INF (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01024 | RWB-ITG-E1073-ITG | GAP-0701 |  | Load test holding 20 cached package versions while evaluating; record heap request, heap limit and cache bound per environment as reviewed values; keep the evaluated copy in memory only; platform owner confirms before wave 1 release. |
| CDC-01038 | RWB-ITG-E1073-ITG | GAP-0702 |  | Record readiness gate, probe timings, ports, certificate subject and image-scan window as reviewed values per environment; confirm with platform and security owners at SIT; keep them out of code and chart constants. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01029 | RWB-ITG-E1073-ITG | GAP-2459 | find it | Map the free identifiers of EV-08, EV-09 and EV-30 to rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1, keyed by package code, with package code, version label, in-force time and SHA-256. |
| CDC-02288 | RWB-ITG-TE013-ITG | GAP-2425 | 5 | Publish DecisionRecorded as rwb.decision-record.DecisionRecorded.v1 and tie it to the P7 event row (EV-08, EV-09 or EV-30) when the catalog is indexed. Topic and payload unchanged. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02213 | RWB-ITG-TE006-ITG | DOR-RWB-ITG-TE006-ITG-21 | 12.2 | Publish POST /authorise in rwb-access.yaml and POST /cases/{caseId}/actions in rwb-case.yaml. No CON story RWB-ITG-TE006-CON is cited: the harness provides no contract. |
| CDC-02215 | RWB-ITG-TE006-ITG | DOR-RWB-ITG-TE006-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml and POST /api/recovery/case/v1/cases/{caseId}/actions in rwb-case.yaml. |

### RWB-P10-TE013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02279 | RWB-ITG-TE013-ITG | GAP-1005 | none | Name provider, model, model version and field-extraction route; keep the route as property rwb.document.extract.model-route with no model name in code |
| CDC-02281 | RWB-ITG-TE013-ITG | GAP-0620 | 12 | Keep the declared agent-steps and decision-record operations and refusals; reconcile REST POST /agent-steps with ITG BR7 and AC1 (no REST call inside a step); confirm the run-read route. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02293 | RWB-ITG-W1J01-ITG | CG-ALL-516 | 12.2 | Provider to confirm the full path under base /api/recovery/comms/v1; yaml lists /admin/templates with GET and POST. |
| CDC-20653 | RWB-ITG-W1J01-ITG | R-00307 |  | GET and POST on /admin/templates already present; full published path is confirmed by provider CON story (CG-ALL-516). |

### RWB-ITG-W1J02-ITG; 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02304 | RWB-ITG-W1J02-ITG | DOR-RWB-ITG-W1J02-ITG-21 |  | Mark DoR item 21 met or waived: this story declares Contract dependencies None and runs from Day 1 against the stub set of §12.8 (§R5.7 rules 1 and 6). |
| CDC-02305 | RWB-ITG-W1J02-ITG | DOR-RWB-ITG-W1J02-ITG-22 |  | Mark DoR item 22 met or waived: §12.8 generates one WireMock stub per published contract and pins each version in the run report. |

### 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20548 | RWB-ITG-W1J02-ITG | R-04190 |  | Mark-met-or-waived entry for item 21 belongs to the DoR checklist of RWB-ITG-W1J02-ITG. This definition keeps item 21 as the generic contract gate. |
| CDC-20549 | RWB-ITG-W1J02-ITG | R-04191 |  | WireMock stub and run-report pin belong to the DoR checklist of RWB-ITG-W1J02-ITG. No published fake version is sourced, so none is written here. |

### OTHER:P7 functional specification (FSD P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00933 | RWB-ITG-E1066-ITG | GAP-1612 | n/a | Ledger stays with P1 here. BR6 cites FEAT-ILG-02, which the re-issue removes; story not edited for that. |

### OTHER:P3 case module specification and integration module specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00934 | RWB-ITG-E1066-ITG | GAP-1511 | n/a | This service (P1 rwb-source-data) owns the ledger tables and write path, as this story already states. |

### RWB-P1-E1066-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00938 | RWB-ITG-E1066-ITG | GAP-0506 | 9 | Carry every deployment value, alert threshold, probe timing, window and incident route as a named chart value set per environment; fail the release when the append-only trigger is missing. |

### RWB-P1-E1066-APP; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00939 | RWB-ITG-E1066-ITG | GAP-2254 | 9 | Record the legacy migration required flags for the five values a ledger entry cannot do without, as stated in RWB-P1-E1066-APP. |

### RWB-P1-E1067-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00940 | RWB-ITG-E1067-ITG | DOR-RWB-ITG-E1067-ITG-21 | 3 | Section 3 names the contract story and the condition. That story is still Draft; it must reach Done and its contract be listed with its version. |

### RWB-P3-E1067-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00943 | RWB-ITG-E1067-ITG | DOR-RWB-ITG-E1067-ITG-10 | Not in chunk | Add empty, loading, error and no access states for SCR-03 and SCR-09 in that story's screen section. |

### OTHER:FSD P7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00945 | RWB-ITG-E1067-ITG | GAP-1612 | 8 | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; rwb-source-data owns the one ledger, rwb-case serves the timeline over its contract |

### OTHER:rwb-case API and event specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00946 | RWB-ITG-E1067-ITG | GAP-2257 | 8 | In BR3 and BR11 the key and actor attributes and the registry subject are now held in configuration and marked Not specified. The values belong in the rwb-case spec. |

### OTHER:contract/ledger-intake-map-v1.yaml (new) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00949 | RWB-ITG-E1067-ITG | GAP-0508 | 12 | Publish one row per consumed event type with a version label field and the six rows of section 12.4 of the contract. |

### OTHER:Contract fake library of rwb-source-data and rwb-access (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00956 | RWB-ITG-E1069-ITG | DOR-RWB-ITG-E1069-ITG-22 | section 12.8 | Section 12.8 names the two fakes. Their publication and the library version belong to the providers and are not specified in the source documents. |

### OTHER:RWB-ACE-001 (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00958 | RWB-ITG-E1069-ITG | GAP-1505 | 12.8 | Accept scope and dates for RWB-ACE-001 and confirm the fallback freshness source CG-9 before system test. |

### OTHER:RWB-PLT-DB; OTHER:Environment and Deployment Design (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00959 | RWB-ITG-E1069-ITG | GAP-3155 | 13 | Name one login per service for the 19 services in the ACE DB stories and state them in the Environment and Deployment Design. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00960 | RWB-ITG-E1069-ITG | GAP-3156 | 13 | Split the V0002 and V0003 grant block into one grant per service login; keep ace_view_owner and the 30 views with P1. |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00967 | RWB-ITG-E1069-ITG | GAP-0566 | find it | Publish the three read operations with response fields and problem body in RWB-P1-E1069-CON. Record the split: application slice, database slice and wave 1 integration slice. |

### OTHER:Handling tab (v4 workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00971 | RWB-ITG-E1069-ITG | GAP-0263 | find it | Replace the recovery identity SELECT on recovery.v_ace_* with rwb_source_data only. Route other services through the P1 REST contract or a Temporal activity, with audit via ACE Common PII logging. |

### OTHER:Environment and Deployment Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00972 | RWB-ITG-E1069-ITG | GAP-0377 | find it | Name the 19 rwb_* logins and their grant matrix on the 30 views, public and their own schemas, once the document is issued. |

### OTHER:TSD P1 v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00973 | RWB-ITG-E1069-ITG | GAP-0567 | find it | Carry the REST contract wording of T2 and T5.2 as a change note: base /api/recovery/source-data/v1, 2 s client budget, and AceSourceReadRepository kept as internal. |

### OTHER:TSD P1 v3 and FSD P1 v3 (next versions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00974 | RWB-ITG-E1069-ITG | GAP-0569 | find it | Rename the service role to rwb_source_data, state the per-service schema and USAGE on schema recovery in the Service Template Specification, and record the rename in the Change Register against DP-02. |

### OTHER:rwb-access ACE masking pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00975 | RWB-ITG-E1069-ITG | GAP-0903 | find it | Publish per personal field ID the roles that see it unmasked as masking_rule rows, approved by the Compliance and PDPA officer and the security administrator. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00977 | RWB-ITG-E1069-ITG | GAP-0568 | find it | Publish login creation and credential policy, exact grant and revoke list, and the order of the three migrations; record RWB-PLT-E1044-CON as platform dependency of per-service database stories. |

### OTHER:Recovery Workbench v6 source grants block (lines 6824-6845) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00978 | RWB-ITG-E1069-ITG | GAP-0111 | find it | Carry the grants block as a commented template pointing to RWB-PLT-NF06 and RWB-PLT-N011; do not invent role names. |

### OTHER:RWB-E1-069 realigned story, section 18 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00980 | RWB-ITG-E1069-ITG | GAP-3213 | find it | The E1 owner adds REQ-RDF-004 to its section 18 row, or the E3 integration trace is accepted as the citation. |

### OTHER:FSD P1 A1.3 and TSD P1 T6.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00981 | RWB-ITG-E1069-ITG | GAP-0570 | find it | ACE team lead publishes the Tier 1 table list (21 names or the 22nd table) and the legacy grant block stays the enumeration until then. |

### OTHER:TSD P4 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00982 | RWB-ITG-E1069-ITG | GAP-0902 | find it | Fix the masking version naming rule with the pack owner, year and month as in PM-2026.12, and record it in T3.1. |

### RWB-P4-E1069-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00983 | RWB-ITG-E1069-ITG | GAP-0904 | 7 | Replace 'the rwb-access login (DP-02)' placeholder and its not-specified text with login `rwb_access`; carry the same name in the platform DB story and Environment and Deployment Design. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00984 | RWB-ITG-E1069-ITG | GAP-0905 | 8 | Record that masking_rule.field_id is a dictionary field ID held as a value with no cross-schema key; the dictionary stays with P1's data-dictionary API and is not duplicated. |

### OTHER:Per-service module map and service template (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00985 | RWB-ITG-E1069-ITG | GAP-0906 | 7 | Publish the per-service module map with an explicitly empty source-object list for the 18 services that read no view, including rwb-access; set the BND-6 failure wording once in the service template. |

### OTHER:Legacy dependency trace sheet and Story dependencies v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00987 | RWB-ITG-E1069-ITG | GAP-3233 | n/a | Keep the five version 4 dependency rows visible as Not carried; add an X row only if the run books or the harness waits for the named story. |

### OTHER:Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00988 | RWB-ITG-E1070-ITG | CG-ALL-446 | 13 | Create story RWB-P7-E1073-CON, or name the existing contract story for the rwb-decision rule-package dependency, which DP-04 currently references. |

### RWB-P4-E1022-APP; RWB-PLT-E1070-APP; OTHER:Gap Register v2 CG-ALL-446 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00991 | RWB-ITG-E1070-ITG | DOR-RWB-ITG-E1070-ITG-17 | header | Bring RWB-P4-E1022-APP and RWB-PLT-E1070-APP to Done; create or correct the RWB-P7-E1073-CON reference under CG-ALL-446 |

### RWB-PLT-E1070-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00993 | RWB-ITG-E1070-ITG | GAP-0007 | 13 | Upgrade Temporal to 1.30 or later in wave 0 before any worker is built. The Platform team sets the owner and date. |

### OTHER:Wave 0 Service Catalog; OTHER:Environment and Deployment Design v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00994 | RWB-ITG-E1070-ITG | GAP-1440 |  | Record the platform login, platform task queue, platform admin base and the SCB IT approved Temporal server and Java SDK release. |

### OTHER:Wave 0 Service Catalog; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00995 | RWB-ITG-E1070-ITG | GAP-1442 |  | Name the platform login, platform task queue, platform admin base and codec key names; register the platform row in the naming table. |

### OTHER:Service Catalog v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00996 | RWB-ITG-E1070-ITG | GAP-1672 |  | Name one accountable team for the shared Temporal cluster and one for the Recovery business-event topics. |

### OTHER:Non Functional Specification v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00997 | RWB-ITG-E1070-ITG | GAP-1670 |  | Set recovery point and time, namespace quotas and rate limits, key rotation period and retention targets under DL11 and DL26 before wave-1 release. |

### OTHER:ADR-011 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01002 | RWB-ITG-E1070-ITG | GAP-0002 | find it | Update ADR-011 to the parent CaseWorkflow with a child workflow per stage, Continue-As-New and ABANDON close policy before Epic 3. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01005 | RWB-ITG-E1070-ITG | GAP-3163 | find it | Read Module P3 for RWB-E1-070 to RWB-E1-072 as consumed by P3 rather than owned by P3; keep the build order. |

### OTHER:Technical Specification P7 (rwb-decision); OTHER:Technical Specifications P3 and P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01019 | RWB-ITG-E1073-ITG | GAP-1615 | find it | Re-issue TSD P7 with rule tables and rule-version/rule-package operations; remove them from TSD P3 and P4; set x-module of nine rule paths to P7. |

### RWB-P3-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01020 | RWB-ITG-E1073-ITG | GAP-1330 |  | State whether it publishes the open-case reads its consumers need, or move the case-read dependency to the P3 story that does (RWB-P3-E1023-CON). |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:41; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01021 | RWB-ITG-E1073-ITG | GAP-0383 |  | Assign one package code and version label each to rwb-comms and rwb-integration; add GET /rule-models/{packageCode}/{versionLabel} under P7 rwb-decision with the checksum; publish the refused-load message in the rwb-decision catalogue keeping MSG-P3-027. |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01022 | RWB-ITG-E1073-ITG | GAP-0699 |  | Correct the ownership labels of rule_package, rule_package_version, rule_row and rule_test_case to P7 (rwb-decision). |

### OTHER:Rule programme package-to-service map (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01025 | RWB-ITG-E1073-ITG | GAP-1216 |  | Publish one row per package with its owning service, version labels and target queues, including the package assigned to rwb-comms. |

### OTHER:rwb-decision API document and wave-1 contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01026 | RWB-ITG-E1073-ITG | GAP-1217 |  | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} with the DRL, SHA-256 checksum, version state and valid-from date; 404 for unknown label, 409 for not loadable, 2 s budget, one hop. |

### OTHER:rwb-decision contract (registry resources, model answer, dry-run report, workbook object, version-list panel, service lo (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01027 | RWB-ITG-E1073-ITG | GAP-1327 |  | Publish the registry resources with physical columns, the model answer, dry-run counts, workbook container and object name, panel identifier, service login and the two parameter codes. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01032 | RWB-ITG-E1073-ITG | GAP-0672 |  | The story keeps the plan H and C lists. The assigned package, model-fetch surface, local copy table, consumers and login sit in other documents. |

### OTHER:Template and Rules v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01033 | RWB-ITG-E1073-ITG | GAP-1328 |  | The story reads DP rows as pattern-added dependencies, as section 13 states, and the header now lists them. R5.5 wording is the change needed. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01035 | RWB-ITG-E1073-ITG | GAP-1620 | find it | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats, that a version names its format, and that conversion is a version change with its own test evidence. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01036 | RWB-ITG-E1073-ITG | GAP-0118 |  | State amended T1 and T2: the workflow runs on the task queue of the owning service; each scheduled job becomes a Temporal Schedule or event-started workflow in the owning service; JOB-05 stays behind the TimerScheduler port until Epic 3. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01037 | RWB-ITG-E1073-ITG | GAP-0205 |  | Record 'Rule' as rule_row in the ownership basis (owner P7). Add rule_package and rule_package_version as P7 entities in the next LDM version; do not rename any v6 row. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01039 | RWB-ITG-E1073-ITG | GAP-1219 |  | Add rwb-comms to the consumers of RulePackageInForce, or publish the package-to-service map. Until then rwb-comms consumes the event on the slide 20 rule and the difference is carried here. |

### OTHER:Temporal and Drools design v? slide 15 (version states) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01040 | RWB-ITG-E1073-ITG | GAP-1331 |  | State that REFUSED is a state of a stored version that failed its promotion checks; a load refused at a check leaves no version row and is proved by its decision log entry. |

### OTHER:Rules Engine Design v3, section 4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01041 | RWB-ITG-E1073-ITG | GAP-2031 |  | Keep the name RulePackageEffectiveDateJob as the step; state that it runs as JOB-20, a Temporal Schedule in rwb-decision (P7), which publishes RulePackageInForce (EV-30). |

### OTHER:Rules Engine Design v3, sections 2 and 4 (version 4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01042 | RWB-ITG-E1073-ITG | GAP-2049 |  | Keep MSG-P3-027 character for character; raise the alert in the service that loads the package; name P7 rwb-decision as registry owner; keep RWB-E1-073 as run book owner. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01043 | RWB-ITG-E1073-ITG | GAP-2460 | 8 | BR10 marks the catalogue that holds rules.testcases.min as Not specified (GAP-2460) |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01044 | RWB-ITG-E1073-ITG | GAP-2461 |  | Record that the five rule-package operations and their authority checks move from the access module (recovery.accessadmin.rulepackages) to rwb-decision (P7) per the Ownership Map; the rights stay rows of the rwb-access role model. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02199 | RWB-ITG-TE004-ITG | DOR-RWB-ITG-TE004-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml, and GET /api/recovery/source-data/v1/customers/{id} and GET /api/recovery/source-data/v1/accounts/{id} in rwb-source-data.yaml. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02203 | RWB-ITG-TE004-ITG | DOR-RWB-ITG-TE004-ITG-12 | 16, 18 | Add rows for TC-ITG-TE004-01 to -05 to Test Cases v8; align the §18 test lists with RTM v7. |

### OTHER:Split plan (legacy RWB-TE-004) and Build Notes v6 RWB-TE-004 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02207 | RWB-ITG-TE004-ITG | GAP-3170 | 4 | Assign the masking tool to RWB-PLT-TE004-APP and have each owning service load its own masked rows in its own story; remove the three-service table writes from RWB-ITG-TE004-ITG. |

### OTHER:Story dependencies v5 and legacy dependency trace sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02209 | RWB-ITG-TE004-ITG | GAP-3233 |  | The five gaps sit in the dependency trace, not this story; the Depends on row was filled under DOR-RWB-ITG-TE004-ITG-17, not for this item. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02211 | RWB-ITG-TE006-ITG | CG-ALL-483 | 12.2 | Publish POST /api/recovery/case/v1/cases/{caseId}/actions in rwb-case.yaml through the provider's CON story. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:39; OTHER:47) with the ACE platform team (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02216 | RWB-ITG-TE006-ITG | GAP-0011 | header | Confirm Kafka hosting; reserve dedicated topics and ACLs in wave 0; keep outbox and Event Hubs Premium fallback; agree capacity, topic naming, ACL model, schema registry and environments. |

### OTHER:RWB-E1-067 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02229 | RWB-ITG-TE006-ITG | GAP-0376 |  | P1 runs one consumer group across the three topics, accepts current and previous schema versions, dedupes on CloudEvents id, assigns case_seq under the case lock, orders the ledger read by occurredAt then case_seq, and reports cross-topic inversions; keep the legacy event-to-code map. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02234 | RWB-ITG-TE006-ITG | GAP-1622 | find it | Add a contract version to DecisionRecorded, record it on decision_log_entry, and send unknown versions to the dead-letter topic; add the version fields to TSD P7 T3.1. |

### OTHER:Information Flow v5 deck (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02235 | RWB-ITG-TE006-ITG | GAP-2107 | find it | Add slides on both Kafka roles: ACE PII topics for logging (unchanged), and the 19 business-event topics plus rwb.decision-record.v1 with their own ACLs, retention and no personal data. |

### OTHER:TSD P2 v3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02236 | RWB-ITG-TE006-ITG | GAP-1992 | find it | Remove the six platform tables and efs_ledger_outcome from T3.1; build platform tables once in the shared libraries (RWB-PLT-TE006-CON) and keep efs_ledger_outcome with P1. |

### RWB-ITG-TE008-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02240 | RWB-ITG-TE008-ITG | DOR-RWB-ITG-TE008-ITG-21 | header; 16 | No contract story is in the set. The header and TC-ITG-TE008-07 record it as Not specified; it must be created and published before this story is ready. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02241 | RWB-ITG-TE008-ITG | DOR-RWB-ITG-TE008-ITG-8 | 12.2; 12.4; 12.5 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml. Add workflow ChainCheckWorkflow (JOB-14) and activity ingestDecisionRecord, both on rwb-decision, to Temporal Catalog. |

### RWB-P7-E1008-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02242 | RWB-ITG-TE008-ITG | CG-ALL-492 | 3, 4, 10, 11, 18, 19 | Record decision_record as a per-service schema table object with chain_seq, prev_hash and entry_hash in the schema design. |

### RWB-PLT-E1071-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02247 | RWB-ITG-TE008-ITG | GAP-1437 | 8 | Publish schedule ID and display name, catch-up and backfill rule, run-record retention, rwb-decision ingest completeness publication, and the Compliance channel for JOB-14; record the ACE choice in the legacy JOB-14 run book. |

### OTHER:Version 3 order (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02249 | RWB-ITG-TE008-ITG | GAP-3241 | header | Keep items 19 and 21 in place as retired with no story; repoint any dependency on RWB-TE-007 to RWB-PLT-E1071-CON. |

### RWB-P10-TE013-CON; OTHER:ADR-020; RWB-P10-E1058-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02280 | RWB-ITG-TE013-ITG | GAP-2187 | none | Publish the run-submit and run-to-record link operations with their members; record the 60 s budget as the single DP-11 exception in ADR-020; name rwb-agent login; settle guardrail check codes |

### RWB-P7-TE013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02282 | RWB-ITG-TE013-ITG | GAP-1315 | 12 | Approve in the OpenAPI and physical schema the actions keys agentRunId, mode, fallback, fallbackReason, the agent-step LOV-DECISION code and the field set of the two ledger reads. |

### RWB-ITG-E1059-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02284 | RWB-ITG-TE013-ITG | GAP-0610 | find it | Keep AC5 and TC-E1-059-05 with RWB-ITG-E1059-ITG; name the rwb-agent login and the gateway route path with their owners; add RWB-P5-E1053-CON to the contract dependencies once published. |

### OTHER:Decision-log store slice (JOB-14) and service template with platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02285 | RWB-ITG-TE013-ITG | GAP-2420 | 13 | Give the nightly chain-check time, timezone and overlap policy for JOB-14, and the rwb-decision login, consumer group, Flyway user and property names from the service template and platform DB story. |

### OTHER:rwb-agent contract (agent policy) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02286 | RWB-ITG-TE013-ITG | GAP-2421 | 12 | Publish the model version of each live agent, including INTAKE, with the agent policy. Story already asserts equality with the run fixture. |

### OTHER:rwb-reporting reporting contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02287 | RWB-ITG-TE013-ITG | GAP-2424 | 2 | Define the operation name, period grain and rounding of the agent fallback rate, and publish the count by agent version and month readable from the ledger. Threshold stays below 10 percent per month. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02289 | RWB-ITG-TE013-ITG | GAP-1318 | Header | The login name is in no source and is allocated by RWB-PLT-NF06-DB; the story keeps the phrase the rwb-decision login (DP-02) and needs no edit. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02292 | RWB-ITG-W1J01-ITG | CG-ALL-515 | 12.2 | Provider to confirm the full path under base /api/recovery/document/v1; yaml lists /cases/{caseId}/documents with GET and POST. |

### RWB-ITG-W1J01-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02295 | RWB-ITG-W1J01-ITG | DOR-RWB-ITG-W1J01-ITG-21 | header | Contract dependencies name RWB-ITG-W1J01-CON; the contract still has to be published by that deliverable. |

### OTHER:rwb-source-data, rwb-access, rwb-document and rwb-comms OpenAPI documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02296 | RWB-ITG-W1J01-ITG | DOR-RWB-ITG-W1J01-ITG-8 | 11 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready, POST /api/recovery/access/v1/authorise, POST and GET /api/recovery/document/v1/cases/{caseId}/documents, GET and POST /api/recovery/comms/v1/admin/templates, and the one further unpublished path in the detcheck. |

### RWB-ITG-E1018-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02298 | RWB-ITG-W1J01-ITG | GAP-0343 | 7 | Assert the Kafka CaseCreated event on rwb.case.events.v1 and the P7 DecisionRecorded ledger entry, use the P7 admin rollback for AC15, and seed the batch through the W1J01 harness. |

### RWB-ITG-E1023-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02299 | RWB-ITG-W1J01-ITG | GAP-0348 | 7 | Confirm the case-scoped deviation read with the S8 service owner before AC18 is built, and treat rwb-deviation as available in SIT for the wave 1 run. |

### RWB-ITG-W1J02-ITG; RWB-ITG-W2J01-ITG; RWB-ITG-W3J01-ITG; RWB-ITG-W4J01-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02300 | RWB-ITG-W1J01-ITG | GAP-2122 |  | Write the step-by-step journey and the test case IDs of each wave in its journey story, so a wave gate can be signed against a named list. |

### OTHER:Test strategy version 3 (window order of Epic 1; OTHER:Epic 2 and Epic 3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02301 | RWB-ITG-W1J01-ITG | GAP-3244 |  | Add a Day-1 window before window 1 listing the wave 0 platform stories N001 to N012 and the harness and journey stories W1J01 to W4J01, since wave 0 is not a release and they unblock every later window. |

### RWB-PLT-N001-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02309 | RWB-ITG-W1J02-ITG | GAP-0385 |  | Publish the gateway-bff composite route path and its merge order with RWB-PLT-N001-CON, and name the P10 agent-run start operation with the rwb-agent owner; the QA lead agrees the harness pack, the seeded identifiers beyond RW-2026-000123, the evidence format and retention and the all-green gate at the wave entry check. |

### 04 User stories/Recovery Workbench Technical Enabler Stories v8.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20608 | RWB-ITG-TE004-ITG | R-22909 |  | Tool is already on RWB-PLT-TE004-APP (lines 2468, 2790, 2812) and ITG story has no three-service writes. Split reassignment belongs in split plan and Build Notes v6. |

### 12 Project communication/Recovery Workbench Change Briefing Temporal Drools and Microservices v2.pptx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20621 | RWB-ITG-E1073-ITG | R-28686 |  | Version-state rule belongs in the Temporal and Drools design deck (slide 15), not this briefing. This briefing is a .pptx with no supported fix op. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20635 | RWB-ITG-E1070-ITG | R-28679 |  | RWB-E1-070 'What moves' says P3 consumes the platform and contributes no platform story; build order unchanged (GAP-3163). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20639 | RWB-ITG-TE013-ITG | R-28930 |  | Model version of each live agent is a story-side assertion that reads model_version from the run. No literal is needed in this document (GAP-2421). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0002 | ADR-011 still describes one long case workflow | Recovery tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0007 | Temporal version 1.30+, 1.28.1 and 1.29.7 | Platform team | Resolved (directive) |
| GAP-0011 | Kafka hosting not confirmed | Enterprise Architecture and ACE platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0014 | Table inventory does not cover the v5 schema-per-service model and the FK cuts are empty | Solution architect and ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0080 | The agent platform of DL33 is never named as a service | TechX | Resolved (directive) |
| GAP-0083 | The tool gateway's target systems are not named | TechX | Resolved (directive) |
| GAP-0110 | The map does not say which schema holds the 30 ACE views | ACE team | Resolved (directive) |
| GAP-0111 | The source grants use placeholder roles and do not create the 19 logins | ACE team | Resolved (directive) |
| GAP-0118 | The amendment of D-RCV-36 T1 and T2 has no wording in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0205 | The entity called Rule is rule_row, and the model holds neither rule_package nor rule_package_version | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0259 | The 30 ACE source views have no owner in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0263 | One recovery identity reads the ACE views; the target has one login and one schema per service | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0267 | The interaction ledger is defined by the case module but the Ownership Map gives it to P1 | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0348 | RWB-E1-023 integration slice: the S8 deviation read path, the wave of rwb-deviation and the fixture composition are not fixed by the sources | TechX | Resolved (directive) |
| GAP-0375 | The cross-service ledger-write contract and its failure mapping are not defined | Solution architect | Resolved (directive) |
| GAP-0376 | The event-to-ledger map, the cross-topic ordering rule and the duplicate key after the split into per-service topics are not defined | Solution architect | Resolved (directive) |
| GAP-0377 | The 19 login names, the grant matrix on the 30 ACE views and the two-part boundary rule after the schema split are not stated | ACE database administrator | Resolved (directive) |
| GAP-0378 | The worker registration, task-queue and namespace contract between the 19 services and the Temporal platform is not defined | Solution architect | Resolved (directive) |
| GAP-0379 | The per-schema table list of the masked copy, the owner of the verifier across the 19 schemas and the PII extract contract are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0380 | Chain-check scope across services, the ingest watermark and the Compliance route are not defined for the target | Tech lead | Resolved (directive) |
| GAP-0381 | The call type between the client and rwb-agent, the run result after the 60 second budget and the guardrail check codes are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0382 | TE006 outbox slice: the case-event mapping, the retry and dead-letter values, and the consumer list per event type | Solution architect | Resolved (directive) |
| GAP-0383 | The rule package of rwb-comms and of rwb-integration, the rule-model fetch path and its owner, and the message family of the refusal are not stated in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0384 | The wave 1 contract-test harness, its pipeline wiring and the synthetic test data set are not specified | QA lead | Resolved (directive) |
| GAP-0385 | The wave 1 journey harness environment, seeded data, evidence format and release gate are not specified | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0504 | The append path, its authorisation handling and its 404 semantics are a target choice, not a legacy value | Solution architect | Resolved (directive) |
| GAP-0505 | The exact ledger resource path, the login wording and the field-level required flags are not specified | Tech lead | Resolved (directive) |
| GAP-0506 | No deployment value, alert threshold, probe timing or incident route exists for the ledger writer | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0507 | The mapping of the document fact and the timer fact onto the target event types is not specified | Solution architect | Resolved (directive) |
| GAP-0508 | The format and version label of the ledger intake map are not specified | Tech lead | Resolved (directive) |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0567 | The ACE read is a REST contract of rwb-source-data in Architecture v5 and an in-process Java interface in TSD P1 and legacy RWB-E1-069 | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0568 | rwb-source-data database slice: who creates the login and holds its credential, the exact grant names, the position of the three grant migrations on the sequence, and the platform sequence dependency of a Day-1 database story are not specified | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0569 | The service role is recovery_svc on one recovery schema in TSD P1 and legacy RWB-E1-069, and a per-service login rwb_source_data with its own schema under Architecture v5 | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0570 | The number of Tier 1 ACE tables is 21 in legacy RWB-E1-069 and 22 in FSD P1 and TSD P1, and the grant list is enumerated only in the legacy story | ACE team lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0619 | The app slice of the agent runtime client: the two operations the legacy Java interface spans, the call type and the budget of a step, the login, the record write and its link, the guardrail check-code list and the route in front of the run read are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-decision, rwb-case and rwb-access | Resolved (directive) |
| GAP-0620 | The client contract: the operation paths and the member types beyond the legacy Java records, the refusal set, the 409 of an in-flight repeat, the record reference and the route in front of the run read are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0621 | The deployment slice of the agent runtime client: the chart values, the login secret, the topic rights of the shared decision-record topic, the worker concurrency, the alert thresholds, the route path and the capacity figures are not specified by any source | SCB IT infrastructure and the DevOps team with the ACE platform team and security | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0699 | The rule package registry and the workbook object are declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0700 | The five authoring operations and the two rule reads have no Ownership Map row and no field-level shape | P7 rwb-decision owner with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0701 | The KieBase cache sizing, the JVM heap and the storage of a local model artefact are not specified | SCB IT infrastructure with the rwb-case owner team | Resolved (directive) |
| GAP-0702 | No source gives the readiness gate, the probe timings, the ports, the certificate subject or the image-scan window | SCB IT infrastructure with the platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0902 | rwb-access ACE masking pack: no source names the masking version label | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0903 | rwb-access ACE masking pack: no source holds the roster of roles that see a personal field unmasked | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0904 | rwb-access: the per-service database login name is named by no source | ACE team lead and ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0905 | rwb-access: unclear whether this service may hold masking rows that key on the P1 field catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0906 | rwb-access: the boundary rule has no allowed-object list and no build-log wording for this service | Tech lead, rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1005 | The extractor provider, model name and model version behind extraction_method MODEL are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1055 | The exact idempotency-key format of rwb.document.DocumentStored.v1 is not stated for the target topic | Tech lead | Resolved (directive) |
| GAP-1056 | The CloudEvents attribute names that carry the actor and the occurred time on rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
| GAP-1057 | The retry limit applied to the JOB-11 outbox relay of rwb-document is not stated | Platform administrator | Resolved (directive) |
| GAP-1058 | The JSON Schema registry subject name and the AsyncAPI document location for rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
| GAP-1214 | RWB-P6-E1073-APP: the local copy table and its columns, the parameter read path, the two added check names and the local run record are not specified in the source documents | Solution architect | Resolved (directive) |
| GAP-1215 | RWB-P6-E1073-APP: the DP-04 row of the pattern table names H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON while the plan gives no H and C RWB-P3-E1073-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1216 | RWB-P6-E1073-APP: no source names the rule package rwb-comms is assigned, its version labels or its target queues | Solution architect | Resolved (directive) |
| GAP-1217 | RWB-P6-E1073-APP: the model fetch operation, its path segments, its request fields and its response fields are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1219 | RWB-P6-E1073-APP: Arch v5 slide 43 lists four consumers of RulePackageInForce while slide 20 says every service refreshes its cache on it, and the ITG story makes rwb-comms an evaluator | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1315 | The key set of the decision entry of an agent step, the sub-decision code beside the route code, and the field set of the two ledger reads have no source | Solution architect, P7 rwb-decision, with the P10 agent runtime business analyst and the data steward | Resolved (directive) |
| GAP-1316 | The operation and parameter names of the agent fallback-rate measure have no source | Data steward with the P9 reporting analyst and the P10 agent runtime business analyst | Resolved (directive) |
| GAP-1317 | The text of MSG-P7-009 and the shape of an append that is refused are not written out in any source | Solution architect, P7 rwb-decision, with the platform event team | Resolved (directive) |
| GAP-1318 | The name of the per-service database login is not fixed by any source | ACE DB team with the platform team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1327 | RWB-P7-E1073-APP: the model answer, the dry-run report, the refusal of the model read, the workbook object, the version-list panel, the service login, the parameter codes and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1329 | RWB-P7-E1073-APP: the same rule registry is named as /admin/rule-versions by API Specification v4 and the integration story and as /admin/rule-package* by the legacy story and the Ownership Map, and a third read /rule-catalog is consumed but unowned | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1330 | RWB-P7-E1073-APP: the case read that feeds the dry run is attributed to RWB-P3-E1073-CON by the plan and to RWB-P3-E1023-CON by the P3 contract story, which serves no operation | Solution architect with the rwb-case contract owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1331 | RWB-P7-E1073-APP: REFUSED is one of the six version states while a load refused at a check writes no rule_package_version row, so no stored version ever reaches it | Solution architect with the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1415 | The retry schedule, the JOB-11 sender and the ownership of the exception path are unresolved for the outbox library | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1435 | The per-service staging schema, the per-service extract layout, the personal-data field registry operation and the tool schema are not defined for the 19-schema masked copy | Solution architect | Resolved (directive) |
| GAP-1437 | Owner, instance, run-record surface and reporting of the daily decision log hash-chain check after the split | Solution architect with RW-COMPLY | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1440 | The platform identity and the SCB IT approved Temporal server and SDK release are not stated in any read source | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1442 | The platform worker has no platform login, no task-queue row and no admin base in any read source, and no source gives the build-ID format or the codec key name | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1505 | The Section B views and every Tier 2 feature depend on ACE additions that the ACE team has not accepted | ACE team lead | Resolved (directive) |
| GAP-1509 | Which function writes the appraisal stale flag and age is not set | Business analyst, P1 and S1 | Resolved (directive) |
| GAP-1511 | Two module specifications define the ledger tables and the ownership map leaves both here | Solution architect | Resolved (directive) |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1666 | The retry limit of an event and of a call is stated differently in the BRD and in Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1670 | Several platform targets are unset: recovery point and time, the per-namespace quotas, the key rotation period and the retention periods | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1672 | The owner of record for the shared Temporal cluster and for the Kafka hosting is not named | Enterprise Architecture | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1992 | TSD P2 names platform tables and one P1 table as its own | Solution architect | Resolved (directive) |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-2017 | rwb-platform task queue is not in the 19 services or in the R4 naming rule | Platform team (RWB-PLT-WF) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2030 | Delivery ownership of E1-072 and E1-073 differs between the story set and the Ownership Map | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2031 | The effective-date job is a Quartz job owned by RW-COE in version 3 and a Temporal Schedule in rwb-decision in Architecture v5 | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2038 | The mapping of a service workload identity to the SY- roles is not specified | Platform with P3 rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2040 | The view conformance test of RWB-E1-069 is split across two services | P1 rwb-source-data with the ACE DBA | Resolved (directive) |
| GAP-2049 | The rule package compile alert names P3 while the registry is P7 and the load happens in every owning service | P7 rwb-decision with the centre of excellence | Resolved (directive) |
| GAP-2072 | The interaction ledger is claimed by rwb-case and by rwb-source-data | Service owner P1 rwb-source-data with P3 rwb-case | Resolved (directive) |
| GAP-2107 | Kafka has two roles in the deck and only one of them is named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2122 | The journey steps and test cases of each wave are not stated | QA team | Resolved (directive) |
| GAP-2148 | Integration stories and class I dependencies are not covered by either definition | QA lead | Resolved (directive) |
| GAP-2154 | The seed, business date, volumes and identifiers of the synthetic fixture set are not stated | QA lead | Resolved (directive) |
| GAP-2155 | The pack, the evidence format and the retention of a journey and harness run are not stated | QA lead | Resolved (directive) |
| GAP-2158 | No source states who signs a wave gate | Delivery lead | Resolved (directive) |
| GAP-2159 | The harness is described as serving all four waves and scoped to the wave 1 services | QA lead | Resolved (directive) |
| GAP-2187 | The agent runtime client has no published operation, no call type and no target-side home for the record write | Solution architect | Resolved (directive) |
| GAP-2188 | The client contract has no source member types, refusal detail or record reference shape | Solution architect | Resolved (directive) |
| GAP-2189 | The release has no source topology, sizing, login name, alert threshold, runbook text or route path | DevOps lead | Resolved (directive) |
| GAP-2254 | The ledger columns are required in the legacy migration and optional in the TSD | rwb-source-data contract owner (TechX) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2255 | The case-side link table, its states, its key and the write order are not in the sources | TechX | Resolved (directive) |
| GAP-2256 | API-P3-015 and API-P3-014 of the TSD have no rwb-case counterpart after the split | rwb-source-data contract owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2257 | The CloudEvents key and actor attributes, the idempotency-key format, the relay publish limit and the registry subject of the case topic are not in the sources | rwb-case contract owner and the platform event library owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2417 | The decision code of an agent step and the placement and key set of the agent run, the mode, the fallback and its reason are in no source | Solution architect | Resolved (directive) |
| GAP-2418 | The text of MSG-P7-009 and the identifiers and texts of the not-found answer and the chain-break report are not written in any source | Business analyst, P7 | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2420 | The per-service login name, the environment and property names and the time of the chain check are in no source | Solution architect | Resolved (directive) |
| GAP-2421 | The model version of agent INTAKE is named in no source | Solution architect | Resolved (directive) |
| GAP-2422 | The legacy story says the client publishes no event while DP-03 requires the record on the shared decision-record topic | Solution architect | Resolved (directive) |
| GAP-2423 | The fixed story path already held an artefact of the superseded Work Package B-P7-05 whose citations resolve to no register row | Documentation lead | Resolved (directive) |
| GAP-2424 | The fallback-rate measure, its operation name and its threshold ownership are in no source | Business analyst, P7 | Resolved (directive) |
| GAP-2425 | The EV number of the DecisionRecorded event is left open by the Ownership Map among three P7 events | Solution architect | Resolved (directive) |
| GAP-2457 | The physical columns of rule_package, rule_package_version, rule_row and rule_test_case are not in any source | TechX and the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2458 | No provided operation of the case service returns the open case facts a dry run needs | P3 and P7 contract owners | Resolved (directive) |
| GAP-2459 | Which owned event announces a rule package version in force is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2460 | The value of rules.testcases.min is assumed and no parameter catalogue holds it | P3 parameter owner and the P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2461 | The legacy endpoints and their controller sit in the access module, while the Ownership Map gives them to P7 | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3155 | The per-service login names are not fixed in any source | ACE DB lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3156 | The V0002 and V0003 grant block gives one monolith login, not one login per service | ACE DB lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3157 | The rule tables are described as recovery-schema tables but are owned by rwb-decision | P7 rule owner | Resolved (directive) |
| GAP-3163 | The Temporal platform and the Drools runtime sit in a P3 module in the story and in platform epics in the split plan | Platform lead | Resolved (directive) |
| GAP-3170 | The masked copy story writes the tables of three services from one platform story | Platform lead | Resolved (directive) |
| GAP-3193 | The owner of the outbox admin endpoints after the split is not stated | TechX | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3241 | Two items that version 3 still orders are retired by D-RCV-60, and no source states what a squad does with a retired item in the order | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3244 | The new platform stories N001 to N012 and the harness stories W1J01 to W4J01 sit in no window of version 3 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
