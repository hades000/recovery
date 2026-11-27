# RWB-ITG-W2 Wave 2 integration - review pack, part 4 of 5 (RWB-ITG-E2027-ITG to RWB-ITG-E2038-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 166 |
| Cross-document (pending in another document) | 191 |
| Not applied (value not in the sources) | 27 |
| Open business decisions | 28 |
| Register gaps linked | 148 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E2027-ITG | 38 | 22 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2027 ITG Payment matching rules with the data team - integration v2.md |
| RWB-ITG-E2028-ITG | 14 | 11 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2028 ITG Case intake agent live at L1 [E3a] - integration v2.md |
| RWB-ITG-E2029-ITG | 14 | 19 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2029 ITG Deviation screening agent evaluation and L1 on one segment [E3b] - integration v2.md |
| RWB-ITG-E2030-ITG | 12 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2030 ITG Legal document agent in shadow on Epic 1 data [E3c] - integration v2.md |
| RWB-ITG-E2031-ITG | 17 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2031 ITG Agent monitoring dashboard v2 [E3d] - integration v2.md |
| RWB-ITG-E2032-ITG | 13 | 13 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2032 ITG TDR offer-suggestion model through the model gateway [E3e] - integration v2.md |
| RWB-ITG-E2033-ITG | 10 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2033 ITG Case and queue list with status, owner and ageing - integration v2.md |
| RWB-ITG-E2034-ITG | 11 | 24 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2034 ITG Interaction ledger on the case and from every channel - integration v2.md |
| RWB-ITG-E2035-ITG | 14 | 29 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2035 ITG Next action on the case - integration v2.md |
| RWB-ITG-E2036-ITG | 10 | 18 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2036 ITG Queue write interface for models and agents - integration v2.md |
| RWB-ITG-E2038-ITG | 13 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2038 ITG Temporal security, codec server and admin audit - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E2033-ITG | R-00177 | CG-ALL-750 | Script gap | Product owner | The story adds CAR to the closed list LOV-CASE-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E2033-ITG | R-00178 | CG-ALL-751 | Script gap | Product owner | The story adds CAR to the closed list LOV-PRODUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E2033-ITG | R-00179 | CG-ALL-752 | Script gap | Product owner | The story adds CAR to the closed list LOV-STAGE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E2033-ITG | R-00180 | CG-ALL-753 | Script gap | Product owner | The story adds CAR to the closed list LOV-TIMER-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E2029-ITG | R-09454 | CG-ALL-734 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2033-ITG | R-09457 | CG-ALL-758 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-ITG-E2034-ITG | R-09460 | CG-ALL-766 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-ITG-E2035-ITG | R-09463 | CG-ALL-777 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-ITG-E2029-ITG, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P7-E2029-APP, RWB-S8-E2029-APP | R-22656 | GAP-1828 | Register gap | Risk and model risk officer | The confidence threshold for the low-confidence review and the evidence required to run the agent at L1 are not stated | Read the threshold and the autonomy policy from versioned reference data held by rwb-agent and rwb-decision, assert no number, and leave the evidence pack and the approval of a level change to Q-014 and BR-084. |
| RWB-ITG-E1063-ITG, RWB-ITG-E2031-ITG, RWB-P10-E1063-APP, RWB-P10-E1063-CON, RWB-P10-E1063-OPS, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P4-E1063-APP, RWB-P4-E2031-APP, RWB-P6-E1063-APP | R-28648 | GAP-1529 | Register gap | Business lead | The agent monitor screen is named with no screen specification in the source set | The PRD states what the screen shows and that every measure is filtered by agent, policy version, prompt version and business date, and leaves the layout to the design system and the story set. |
| RWB-ITG-E2032-ITG, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P7-E2032-APP, RWB-S2-E2032-APP | R-28842 | GAP-1531 | Register gap | Product owner | The boundary of the TDR suggestion message is not defined between rwb-agent and the treatment screen | The PRD requires that a caller learns that no suggestion is available and why, in the terms of the outcome the service recorded, and leaves the screen, the wording and the message ownership to the treatment PRD and the message standard. |
| RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28853 | GAP-1560 | Register gap | AI product owner | The queue write interface for models and agents has no approved consumer and no flag removal date | Name the first approved consumer and the flag removal date before the wave 2 release. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-ITG-E2033-ITG | R-33387 | ASM-ALL-758 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-ITG-E2034-ITG | R-33388 | ASM-ALL-766 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E2035-ITG | R-33389 | ASM-ALL-777 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E2027-ITG | R-03815 | DOR-RWB-ITG-E2027-ITG-14 | header | Definition of Ready item 14 Epic design: Fail | Needs a signed epic design record for RWB-ITG-W2, which is not in the story files (dorcheck.py RECORD_ITEMS line 41). No RWB-ITG-W2 design doc found by Glob. |
| RWB-ITG-E2027-ITG | R-03816 | DOR-RWB-ITG-E2027-ITG-16 | header | Definition of Ready item 16 Size: Fail | Size is a refinement record outside the story (dorcheck.py line 41). No size value in the item or story; adding one would invent it. |
| RWB-ITG-E2027-ITG | R-03817 | DOR-RWB-ITG-E2027-ITG-17 | header | Definition of Ready item 17 Dependencies: Fail | Not-done deps are delivery state. Nonexistent RWB-P7-E1073-CON is at lines 219/392, which were not supplied; no RWB-P7-E1073-CON file exists to replace it. |
| RWB-ITG-E2027-ITG | R-03818 | DOR-RWB-ITG-E2027-ITG-21 | header | Definition of Ready item 21 Contract published: Fail | Header now names contract dependency RWB-P8-E2027-CON. Its publication is delivery state; no RWB-ITG-E2027-CON story exists and none is invented. |
| RWB-ITG-E2027-ITG | R-03819 | DOR-RWB-ITG-E2027-ITG-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | A published fake library version is a release record (dorcheck.py line 426, always Fail). No version is in the item or the sources. |
| RWB-ITG-E2027-ITG | R-22630 | GAP-0409 | 4 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | Fixture, JOB-07 control, SIT seeding, evidence format absent from story and *Test*.md; story L61/L371/L418 mark them Not specified (GAP-0409). Load route at L74. |
| RWB-ITG-E2028-ITG | R-03823 | DOR-RWB-ITG-E2028-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size found in the Wave 2 integration story files or the DoR review. A header Size row is added that reads Not specified in the source documents. |
| RWB-ITG-E2028-ITG | R-03825 | DOR-RWB-ITG-E2028-ITG-22 | header | Definition of Ready item 22 Fake published: Fail | No published fake library version in the story, the RWB-P10-E2028-CON or RWB-P3-E1043-CON stories, or the DoR review. Row stays Not specified. |
| RWB-ITG-E2028-ITG | R-03826 | DOR-RWB-ITG-E2028-ITG-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version found in the rwb-agent story files or the DoR review. The header Contract version row reads Not specified in the source documents. |
| RWB-ITG-E2028-ITG | R-14348 | DOR-RWB-ITG-E2028-ITG-10 | header | Definition of Ready item 10 Screens and states: Partial | Screen Specifications v1 has no empty, loading, error or no-access states for SCR-03 or SCR-46, so they cannot be added without inventing them. |
| RWB-ITG-E2029-ITG | R-03829 | DOR-RWB-ITG-E2029-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the story or sources; the Size row reads Not specified. |
| RWB-ITG-E2029-ITG | R-22653 | GAP-0411 | 15 | SIT harness environment, SCREEN-S2 fixture pack, Enterprise AI test profile, evidence format and gate for the deviation-screening journey are not specified in any source read | No source gives the harness, fixture pack, profile, evidence format or gate. The story marks them Not specified (GAP-0411; ASM-0586). |
| RWB-ITG-E2029-ITG | R-28642 | GAP-1833 | 13 | No deviation, screening or queue volume is stated for this module | No module volume is in the sources. Unsupported figures and the shadow-run claim were removed. |
| RWB-ITG-E2030-ITG | R-03834 | DOR-RWB-ITG-E2030-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed EP03 epic design record found in Decision Log v11, DoR/DoD v3 or a grep of all .md files for EP03 sign-off or approval. The sign-off cannot be invented. |
| RWB-ITG-E2032-ITG | R-03846 | DOR-RWB-ITG-E2032-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record. Decision log v10 DT05 gives only the sign-off cadence. RWB-ITG-W2 is in no file outside folder 23. A sign-off needs the record. |
| RWB-ITG-E2032-ITG | R-03847 | DOR-RWB-ITG-E2032-ITG-16 | Header table | Definition of Ready item 16 Size: Fail | No size is given in the item or story. The Size row records it as not specified. |
| RWB-ITG-E2032-ITG | R-03849 | DOR-RWB-ITG-E2032-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published fake library version in folder 22, the DoR/DoD v3 export or the decision logs. Header already says Not specified (DOR-RWB-ITG-E2032-ITG-22). |
| RWB-ITG-E2032-ITG | R-03850 | DOR-RWB-ITG-E2032-ITG-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No OpenAPI version is given in the item or story text. The header records the /v1 path and marks the version as not specified. |
| RWB-ITG-E2033-ITG | R-03852 | DOR-RWB-ITG-E2033-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | Epic design sign-off for RWB-ITG-W2 is a governance event; no record found in PRD, story or realignment .md files. Recording one would invent an approval. |
| RWB-ITG-E2033-ITG | R-03855 | DOR-RWB-ITG-E2033-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published fake library version found; PRD PLT line 469 and stories only plan publication. A version would be invented. |
| RWB-ITG-E2034-ITG | R-03859 | DOR-RWB-ITG-E2034-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size figure exists in the sources. The header Size row reads Not specified, so DoR item 16 stays open. |
| RWB-ITG-E2034-ITG | R-14385 | DOR-RWB-ITG-E2034-ITG-15 | 6 | Definition of Ready item 15 INVEST: Partial | Decision Log v12 DT04 says delivery is Kanban, so two weeks is not a sprint boundary. No source says it fits two weeks. Section 6 text not supplied. |
| RWB-ITG-E2034-ITG | R-22570 | GAP-2321 | 3 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | No story edit made. The values are not in the sources and are to be settled at wave-2 policy load, access-log review and build. |
| RWB-ITG-E2036-ITG | R-03872 | DOR-RWB-ITG-E2036-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size value exists in the sources. The Size row records it as Not specified; DoR 16 stays unmet. |
| RWB-ITG-E2036-ITG | R-14400 | DOR-RWB-ITG-E2036-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | No source states the two-week fit. The Size row records it as Not specified; the INVEST gap stays open. |
| RWB-ITG-E2036-ITG | R-24011 | CG-ALL-782 | 15 | SCR-02 has no empty, loading, error, no access state in the story | Rows added as placeholders. The Screen Specifications v1 text for the SCR-02 Empty and Loading states is not yet in the story, so the gap stays open. |
| RWB-ITG-E2036-ITG | R-24012 | CG-ALL-783 | 15 | SCR-07 has no empty, loading, error, no access state in the story | Rows added as placeholders. The Screen Specifications v1 text for the SCR-07 Loading state is not yet in the story, so the gap stays open. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01557 | RWB-ITG-E2027-ITG | CG-ALL-723 | 18 | Align the REQ-CHO-009 test list with section 18 of RWB-ITG-E2027-ITG in the next RTM version. |
| CDC-01575 | RWB-ITG-E2028-ITG | CG-ALL-729 | 18 | Align the test lists of REQ-DRI-001 and REQ-ACA-005 with section 18 of RWB-ITG-E2028-ITG in the next RTM version |
| CDC-01582 | RWB-ITG-E2029-ITG | DOR-RWB-ITG-E2029-ITG-12 | 18 | Align the REQ-DVH-001 and REQ-DVH-006 test case lists to section 18 of this story, which covers TC-E2-029-01 to TC-E2-029-12-ITG. |
| CDC-01594 | RWB-ITG-E2029-ITG | CG-ALL-733 | 18 | Align the REQ-DVH-001 and REQ-DVH-006 test lists with RWB-ITG-E2029-ITG section 18 in the next RTM version. |
| CDC-01596 | RWB-ITG-E2030-ITG | DOR-RWB-ITG-E2030-ITG-12 | 16, 18 | Sections 16 and 18 now list the same thirteen cases; the RTM v7 list is in another document. |
| CDC-01606 | RWB-ITG-E2030-ITG | CG-ALL-738 | 18 | Section 18 is the source for this story; the RTM rows for this story's test cases need to change in the next RTM version. |
| CDC-01616 | RWB-ITG-E2031-ITG | CG-ALL-743 | - | Align the test lists for REQ-DRI-009 and REQ-APD-005 between RTM v7 and section 18 of this story in their next versions. |
| CDC-01624 | RWB-ITG-E2032-ITG | DOR-RWB-ITG-E2032-ITG-12 | 18 | Align the REQ-CHO-006 and REQ-DRI-001 test lists to the section 18 lists of RWB-ITG-E2032-ITG (TC-E2-032-01 to -10 ITG); the story side is unchanged. |
| CDC-01634 | RWB-ITG-E2032-ITG | CG-ALL-748 | 18 | Align the REQ-CHO-006 and REQ-DRI-001 test lists in RTM v7 to section 18 of RWB-ITG-E2032-ITG in the next RTM version. |
| CDC-01639 | RWB-ITG-E2033-ITG | DOR-RWB-ITG-E2033-ITG-12 | 18 | Section 16 now has 14 test cases, including TC-13 and TC-14. RTM v7 is not in this chunk, so tracing them belongs to the RTM. |
| CDC-01647 | RWB-ITG-E2033-ITG | CG-ALL-755 | 18 | Align the test lists for REQ-WKM-002, REQ-DVH-006 and REQ-ACA-006 with section 18 of RWB-ITG-E2033-ITG in the next version. |
| CDC-01656 | RWB-ITG-E2034-ITG | DOR-RWB-ITG-E2034-ITG-12 | 16, 18 | Align the test case lists in section 18 with RTM v7. TC-E2-034-08-ITG stays a copy only, with AC8 owned by RWB-P2-E2034-APP. |
| CDC-01670 | RWB-ITG-E2034-ITG | CG-ALL-763 | 18 | Align the test lists of the nine requirements that differ with section 18 of RWB-ITG-E2034-ITG in the next RTM version. |
| CDC-01681 | RWB-ITG-E2035-ITG | DOR-RWB-ITG-E2035-ITG-12 | 16, 18 | Align the test case lists of REQ-WKM-012 to REQ-WKM-016 with RWB-ITG-E2035-ITG §18. |
| CDC-01694 | RWB-ITG-E2035-ITG | CG-ALL-772 | 18 | Align the test-case lists of the five differing requirements with section 18 of RWB-ITG-E2035-ITG in the next RTM version. |
| CDC-01709 | RWB-ITG-E2036-ITG | DOR-RWB-ITG-E2036-ITG-12 | 16, 18 | Align the test lists of REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020 and REQ-ACA-010 to the section 18 lists of this story, which cover TC-E2-036-01 to 14-ITG. |
| CDC-01718 | RWB-ITG-E2036-ITG | CG-ALL-781 | 18 | Align the test case lists of the five differing requirements (including REQ-CWC-017 and REQ-CWC-018) with section 18 of RWB-ITG-E2036-ITG in the next RTM version. |
| CDC-01726 | RWB-ITG-E2038-ITG | DOR-RWB-ITG-E2038-ITG-12 | 16, 18 | Story §16 now has 13 test cases (TC-10 to TC-13 added for AC5 to AC8). §18 test lists need RTM v7 alignment. |
| CDC-01727 | RWB-ITG-E2038-ITG | CG-ALL-787 | 18 | Align the REQ-DRI-001 and REQ-DRI-005 test lists in RTM v7 with RWB-ITG-E2038-ITG section 18 in its next version. |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01566 | RWB-ITG-E2028-ITG | DOR-RWB-ITG-E2028-ITG-14 | header | Record the signed epic design sign-off covering RWB-ITG-E2028-ITG |
| CDC-01576 | RWB-ITG-E2029-ITG | DOR-RWB-ITG-E2029-ITG-14 | find it | Record the signed epic design sign-off and link it to RWB-ITG-E2029-ITG. |
| CDC-01608 | RWB-ITG-E2031-ITG | DOR-RWB-ITG-E2031-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-E2031-ITG; no sign-off is in the story or source documents. |
| CDC-01649 | RWB-ITG-E2034-ITG | DOR-RWB-ITG-E2034-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-W2 that covers RWB-ITG-E2034-ITG |
| CDC-01675 | RWB-ITG-E2035-ITG | DOR-RWB-ITG-E2035-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-W2 that covers RWB-ITG-E2035-ITG |
| CDC-01704 | RWB-ITG-E2036-ITG | DOR-RWB-ITG-E2036-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-W2 that covers RWB-ITG-E2036-ITG |
| CDC-01720 | RWB-ITG-E2038-ITG | DOR-RWB-ITG-E2038-ITG-14 | find it | Record the signed epic design sign-off for this story. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01549 | RWB-ITG-E2027-ITG | GAP-0260 | 13 | Add a row for payment_match_rule: keep the 13 field rows marked retired as a table, Owner P3 rwb-case (retired table); PAYMENT_MATCH rule package owned by P7 rwb-decision. |
| CDC-01559 | RWB-ITG-E2027-ITG | GAP-1639 |  | Add the workflows matchPayments and confirmBookings on task queue rwb-payment to the workflows sheet, or confirm the activities are the unit. |
| CDC-01586 | RWB-ITG-E2029-ITG | GAP-1819 |  | Add S8 rows under schema rwb_deviation for the screening run, score per code, contact stop, agent feedback and breach record, with key fields only. |
| CDC-01648 | RWB-ITG-E2033-ITG | GAP-3187 |  | The plan keeps rwb-integration primary for RWB-E2-033 to RWB-E2-036. The tension is recorded for assembly; no story text change. |
| CDC-01683 | RWB-ITG-E2035-ITG | GAP-2395 | none | This story does not mention rwb-comms; the package assignment gap sits in the P6 documents. |
| CDC-01729 | RWB-ITG-E2038-ITG | GAP-2042 |  | Codec server and per-namespace codec keys are platform components of RWB-PLT-E2038, one key per namespace with the old key kept for decode. Rotation is run by Platform (RWB-PLT-WF) under the key policy of SCB IT security. Add codec server and key rows to the ownership map. |

### RWB-P10-E2032-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01623 | RWB-ITG-E2032-ITG | DOR-RWB-ITG-E2032-ITG-21 | header | Publication of the contract is a contract-side fact. The header names the contract dependencies but cannot show them as published. |
| CDC-01627 | RWB-ITG-E2032-ITG | GAP-0634 | section 12 | Contract-level slice; the contract carries the values. |
| CDC-01628 | RWB-ITG-E2032-ITG | GAP-0633 | none | The values sit in the contract. The section 11 read path stays the P3 case operation (DP-05). |
| CDC-01629 | RWB-ITG-E2032-ITG | GAP-0414 | 5 | Publish one one-hop REST operation on the rwb-agent contract that starts a TDR suggestion run, agreed by rwb-treatment and rwb-agent owners; harness environment, stub controls, evidence format and gate Not specified in the source documents (GAP-0414), fixed by QA lead at wave 2 entry check. |
| CDC-01631 | RWB-ITG-E2032-ITG | GAP-1882 | find it | Name the caller-side agent-run operation, its request members and the treatment proposal columns at the wave 2 contract review; record override and fallback decision codes with rwb-decision. |
| CDC-01633 | RWB-ITG-E2032-ITG | GAP-2403 | find it | Agree at wave 2 review the append and two read shapes, LOV-DECISION value D5, the SUGGESTION_RECORDED final-call list, the reference-data path, MSG-P7-009 text and the rwb-decision login name. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01613 | RWB-ITG-E2031-ITG | GAP-2318 | - | Keep both gates; record at the wave 2 access-review run which roles hold Platform administration R and Rules and parameters R. A single-right decision is one permission row per role. |
| CDC-01654 | RWB-ITG-E2034-ITG | DOR-RWB-ITG-E2034-ITG-1 | 1 | Add a role for the integration and QA team, or name the existing role code this story should use. No role code is invented in the story. |
| CDC-01680 | RWB-ITG-E2035-ITG | DOR-RWB-ITG-E2035-ITG-1 | 1 | Add a role code and name for the integration and QA team harness user, or confirm the existing code; §1 then cites that code. |
| CDC-01708 | RWB-ITG-E2036-ITG | DOR-RWB-ITG-E2036-ITG-1 | 1 | Provide a role code or name for the integration and QA team used in RWB-ITG-E2036-ITG section 1 |
| CDC-01724 | RWB-ITG-E2038-ITG | DOR-RWB-ITG-E2038-ITG-1 | 1 | Confirm a role code or name for the integration and QA team, so that the section 1 role matches a row in the document. |

### RWB-P2-E2034-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01650 | RWB-ITG-E2034-ITG | DOR-RWB-ITG-E2034-ITG-21 | header | RWB-P2-E2034-CON is added as a contract dependency. It is still Draft, so publication must happen in that story. |
| CDC-01651 | RWB-ITG-E2034-ITG | DOR-RWB-ITG-E2034-ITG-22 | 12.8 | Publish the contract fake library for RWB-P2-E2034-CON v1 and record its published version |
| CDC-01665 | RWB-ITG-E2034-ITG | GAP-0665 | 12 | Approve the wire shapes of the append, P1 reads, fact answers and admin operations, the dedupe key, state moves and append-before-inbox order with repeated-key as success, before baseline tag. |
| CDC-01668 | RWB-ITG-E2034-ITG | GAP-2225 | 12 | Confirm element names, paths and field shapes of the interaction item, append command and intake result at contract review; rename here if they differ. |
| CDC-01669 | RWB-ITG-E2034-ITG | GAP-3149 | 9 | Agree the property list, schema subject and envelope element names of EV-20 InstructionIssued and EV-21 PartnerResultSubmitted and the seam with this story at contract review; this story claims no ledger row, retention class or timeline read. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01565 | RWB-ITG-E2028-ITG | CG-ALL-727 | 12.2 | Publish GET /api/recovery/agent/v1/agent-runs (status, autonomy mode, agent and agent version, data as of, fallback flag) through the provider's CON story |
| CDC-01567 | RWB-ITG-E2028-ITG | DOR-RWB-ITG-E2028-ITG-8 | 12.2 | Publish GET /api/recovery/agent/v1/agent-runs (see CG-ALL-727); the event type is fixed in 12.4 |
| CDC-20637 | RWB-ITG-E2028-ITG | R-00172 |  | GET /agent-runs is not in rwb-agent.yaml. Its parameters and response schema are not specified in the source documents (CG-ALL-727). |
| CDC-20638 | RWB-ITG-E2028-ITG | R-03827 |  | Agent-runs publication is missing from rwb-agent.yaml; schema not specified in the source documents. Event type belongs to story 12.4 (DOR-RWB-ITG-E2028-ITG-8). |

### RWB-P7-E1073-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01551 | RWB-ITG-E2027-ITG | GAP-1359 | 12.2 | rwb-decision confirms the result (packageCode, versionInForce, ruleId, rowOrder, outputs) and publishes the version-in-force read operation name. |
| CDC-01674 | RWB-ITG-E2035-ITG | CG-ALL-768 | 13 | Create story RWB-P7-E1073-CON, or the solution architect names the existing story that carries the Drools rule-package capability |
| CDC-01676 | RWB-ITG-E2035-ITG | DOR-RWB-ITG-E2035-ITG-17 | header | The named dependency RWB-P7-E1073-CON must exist (see CG-ALL-768); the open build dependencies are a build state, not a story edit |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01556 | RWB-ITG-E2027-ITG | GAP-1291 | 13 | Record H RWB-PLT-E1027-CON, H RWB-PLT-E1072-CON, C RWB-P7-E1073-CON, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1047-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON as non-blocking, built against fakes. |
| CDC-01564 | RWB-ITG-E2027-ITG | GAP-2312 | section Header | DP-added platform dependencies are not in the metadata rows; the Dependency Map must list them as non-blocking, as under GAP-1291. |
| CDC-01615 | RWB-ITG-E2031-ITG | GAP-2317 | - | Add H RWB-PLT-E1027-CON (DP-03), H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON (DP-07), H RWB-PLT-E1044-CON (DP-15) and H RWB-PLT-N001-CON (DP-19); leave the Work Package metadata unchanged. |

### RWB-P10-E2028-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01570 | RWB-ITG-E2028-ITG | GAP-2191 | - | Fix two operations on /api/recovery/agent/v1 with legacy members; name answer and request members; event rwb.agent.AgentFeedbackRecorded.v1; DecisionRecorded on rwb.decision-record.v1; gateway-bff route of one hop and 2 s. |
| CDC-01573 | RWB-ITG-E2028-ITG | GAP-0623 | - | Fix two operations on /api/recovery/agent/v1; declare record event rwb.decision-record.DecisionRecorded.v1 on rwb.decision-record.v1 keyed by case ID; settle 409 and 422 refusals with MSG-GEN-004. |
| CDC-01574 | RWB-ITG-E2028-ITG | GAP-1294 | - | Agree append operation on POST /api/recovery/decision/v1/decision-log, two read shapes, LOV-DECISION value D6, verdict list of three values, reason-code list, MSG-P7-009 text and rwb-decision login. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01625 | RWB-ITG-E2032-ITG | DOR-RWB-ITG-E2032-ITG-7 | 11 | Register field ID DF-ACC-009 as principal_outstanding of v_ace_account so every BR Field ID in section 11 resolves. |
| CDC-01653 | RWB-ITG-E2034-ITG | CG-ALL-759 | 11 | Add a Fields row for DF-INT-036 (collections_history.contact_result); v9 has it only in the ACE mapping, to v_ace_efs_action.contact_result. |
| CDC-01657 | RWB-ITG-E2034-ITG | DOR-RWB-ITG-E2034-ITG-7 | 11 | Add DF-INT-036 contact_result as a field of v_ace_efs_action, or correct the field ID. Section 11 has 35 data rows, which matches the count. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01635 | RWB-ITG-E2032-ITG | GAP-1463 | none | No source names who confirms the model exists. The decision row belongs in the decision log, not in the story. |
| CDC-01682 | RWB-ITG-E2035-ITG | DOR-RWB-ITG-E2035-ITG-18 | none | DL24 has no assumption in the source documents, and DL22 and DL24 are not in the story text. |
| CDC-01700 | RWB-ITG-E2035-ITG | GAP-2411 | 12 | Name the per-service login for rwb-decision in RWB-PLT-DB and the secret store, with the migration role and the application role kept apart, before deployment. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01673 | RWB-ITG-E2035-ITG | CG-ALL-767 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-versions in rwb-decision.yaml through the rwb-decision CON story |
| CDC-01678 | RWB-ITG-E2035-ITG | DOR-RWB-ITG-E2035-ITG-8 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-versions (CG-ALL-767); the event type part is resolved in the story under CG-ALL-769 |
| CDC-01702 | RWB-ITG-E2036-ITG | CG-ALL-778 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-versions in rwb-decision.yaml through the provider's CON story |

### RWB-P2-E2035-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01685 | RWB-ITG-E2035-ITG | GAP-0667 | 12 | Record GET /cases/{caseId}/next-action served by rwb-integration under /api/recovery/integration/v1; fix consumed names, operations, Schedule values and messages; correct Ownership Map row. |
| CDC-01686 | RWB-ITG-E2035-ITG | GAP-0668 | 12 | Baseline the three operation names, nine consumed shapes, split note, workflow and Schedule contract and error mapping; rwb-case, rwb-access and rwb-decision owners confirm element names. |
| CDC-01696 | RWB-ITG-E2035-ITG | GAP-2409 | none | Mark packageVersion as a required query parameter on GET /api/recovery/decision/v1/rule-catalog/{ruleId} and keep the MSG-GEN-001 refusal. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01544 | RWB-ITG-E2027-ITG | CG-ALL-721 | 16 | Add rows TC-E2-027-12-ITG and TC-E2-027-13-ITG to Story test cases, with Given, When and Then copied from their section 16 descriptions in this story. |
| CDC-01679 | RWB-ITG-E2035-ITG | CG-ALL-771 | 16 | Add a row for TC-E2-035-14-ITG with Given, When and Then copied from ITG AC4 (no RESTRUCTURE version in force on 2027-01-04). |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01547 | RWB-ITG-E2027-ITG | GAP-1626 | find it | Replace the rwb-payment operations with GET /proceeds and POST /proceeds/{proceedsId}/match, as in API Specification v4. |
| CDC-01632 | RWB-ITG-E2032-ITG | GAP-1883 | find it | Add the suggestion operation of RWB-P10-E2032-CON to the rwb-agent inbound list through the architecture review before wave 2 closes. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01550 | RWB-ITG-E2027-ITG | GAP-1290 | 12 | Registry shapes, record payload, message set and promotion and rollback semantics belong to the catalogue; the story uses the published operations only. |
| CDC-01604 | RWB-ITG-E2030-ITG | GAP-2360 | 12 | Fix the DocumentChecklist schema with per-item fields, the document list per item, and the completeness reference. |

### RWB-P8-E2027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01552 | RWB-ITG-E2027-ITG | GAP-1880 | 9 | Add the matching read to section 12.1: case, plan and business date in; payment code, due date, match type, rule ID, package code and version, shortfall out. |
| CDC-01553 | RWB-ITG-E2027-ITG | GAP-2705 | 9, 12.2 | Publish one match-consequence read (case, plan, business date) returning payment code, due date, match type, rule ID, package code and version, shortfall; name members at v1. |

### RWB-P10-E2028-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01569 | RWB-ITG-E2028-ITG | GAP-2190 | - | Name rwb-agent login (DP-02) with grants on rwb_agent only; D6 as LOV-DECISION value; freshness date from rwb-source-data read; event rwb.agent.AgentFeedbackRecorded.v1; seven lists and case-decision path as proposed. |
| CDC-01572 | RWB-ITG-E2028-ITG | GAP-0622 | - | Service identity as DP-02 with grants on rwb_agent only; D6 through local decision-record library; DecisionRecorded as rwb.decision-record.DecisionRecorded.v1; SUMMARY item key; 422 for verdict outside LOV-FEEDBACK. |

### RWB-P10-E2029-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01588 | RWB-ITG-E2029-ITG | GAP-0625 | 12 | Name the rwb-agent login at wave 2 build start; create the two rwb_agent indexes in the P10 DB story if earlier migrations do not hold them. S8 raise path, P3 keys and route go in their own contracts. |
| CDC-01590 | RWB-ITG-E2029-ITG | GAP-2193 | 12 | Name the rwb-agent login in the ACE DB story, fix the three rwb-case parameter keys, fix the route in the gateway-bff contract and record the rwb_agent Flyway position. |

### RWB-P10-E2029-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01591 | RWB-ITG-E2029-ITG | GAP-2194 | 12 | Publish the raise and entry-read shapes, register the completion payload subject, fix the route in gateway-bff, and confirm the five score-row members with the data steward. |
| CDC-01592 | RWB-ITG-E2029-ITG | GAP-2402 | 12 | At contract review agree the append path and DecisionRecord answer, evaluation and run reads, case-less approval variant, LOV-DECISION promotion code, MSG-P7-009 text, EV-30 name, rwb-decision login and nine DP dependency rows. |

### RWB-P10-E2031-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01610 | RWB-ITG-E2031-ITG | GAP-0629 | - | Apply the proposed fix: drift step in the v1 Schedule workflow, segment read from the run row, decision-contract additions, notice path by owner, policy values in watch_measures, migration V10_007, route under RWB-PLT-N001-CON. |
| CDC-01617 | RWB-ITG-E2031-ITG | GAP-2198 | none | Apply the accepted defaults: drift step agentDrift joins the baseline Schedule; segment read from the run row; override and decision-quality figures from the rwb-decision decision-log read; notice via rwb-comms; drift values as approved policy rows; migration adds indexes only; element change additive within major version 1; screen states read from policy mode; login and route path fixed with the deployment and edge stories; range limits as configuration values; windows of 7 calendar days. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01620 | RWB-ITG-E2031-ITG | GAP-2319 | none | At D1, confirm the eight legacy test case ids are held by both slices, no measure is implemented twice, and exception X6 is the one access criterion the legacy story carries; no change to the legacy master. |
| CDC-01721 | RWB-ITG-E2038-ITG | DOR-RWB-ITG-E2038-ITG-21 | header | No RWB-ITG-E2038-CON exists. The contract is published by the PLT contract story that the Service Story Catalog splits from RWB-E2-038. Its key is not in this story or the item, so the fix sits there. |

### OTHER:rwb-integration contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01636 | RWB-ITG-E2033-ITG | DOR-RWB-ITG-E2033-ITG-21 | header | No contract story key for rwb-integration is in the story set; the header states Not specified. Publication belongs to the contract. |
| CDC-01637 | RWB-ITG-E2033-ITG | DOR-RWB-ITG-E2033-ITG-23 | header | Contract version row states Not specified |

### OTHER:TSD P4 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01690 | RWB-ITG-E2035-ITG | GAP-2324 | 7 | Extend T6.1 with a Case record column for every role; publish the 14-area matrix through RWB-P4-AD002-APP; fix specialist default scope with the security administrator before PM-2026.12. |
| CDC-01691 | RWB-ITG-E2035-ITG | GAP-2322 | 12 | Add GET /api/recovery/access/v1/role-catalogue/{roleCode} with its answer schema to the API spec and appendix T-A; publish with RWB-P4-E1037-CON; fix authorise request and answer; fix rwb-access login; add unknown-role message. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01693 | RWB-ITG-E2035-ITG | GAP-2323 | 8 | Add CUSTOMER_PARTY as a fourth LOV-ROLE-CLASS value in the load that carries the roles, and align the field catalogs to list it. |
| CDC-01698 | RWB-ITG-E2035-ITG | GAP-2407 | none | Publish LOV-DECISION in the reference-data load with the state-change codes marked, and let the latestStateChange filter read that mark. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01697 | RWB-ITG-E2035-ITG | GAP-2325 | 8 | State that role rows are versioned by the matrix version they load with, or add a role_version label; add the cache lifetime as a DP-06 parameter with its value agreed at the wave 2 design review. |
| CDC-01714 | RWB-ITG-E2036-ITG | GAP-0735 | 7 | Add key rwb.casewf.placement.approved-callers (empty at go-live); matrix version change for SY-AGENT Queue and allocation C by RW-SECADM; overflow 201 field list and caller mapping in RWB-P2-E2036-CON; login name in platform DB story. |

### RWB-P2-E2036-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01705 | RWB-ITG-E2036-ITG | DOR-RWB-ITG-E2036-ITG-21 | header | CON dependency added to this story. DoR 21 'Done and catalogued' stays unmet until that contract story leaves Draft and is catalogued. |
| CDC-01717 | RWB-ITG-E2036-ITG | GAP-2412 | 13 | Publish placement fact element names on rwb.decision-record.v1 and the P3 case-read and P4 authorise shapes; add the reference-data operation; add the MSG-P7-009 text to the message standard; fix the login name in the platform DB story. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01543 | RWB-ITG-E2027-ITG | CG-ALL-718 | 13 | Create story RWB-P7-E1073-CON, or name the existing story for the same capability; then correct the C dependency in DP-04 of section 13 to match. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01545 | RWB-ITG-E2027-ITG | GAP-2395 | find it | Bind the rwb-comms notice to the three Epic 2 package codes read through the contract, prove AC1 and AC5 on them, and settle assignment with the rule registry owner. |

### OTHER:FSD P8 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01546 | RWB-ITG-E2027-ITG | GAP-1625 | find it | Replace placeholder rows A2.3.4.1, A2.4.4.1, A2.5.4.1, A2.6.4.1, A2.7.4.1, A2.8.4.1, A2.9.4.1, A2.10.4.1 and A2.11.4.1 with testable main-flow criteria. |

### OTHER:TSD P4 T-A.1 (Technical Specification P4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01548 | RWB-ITG-E2027-ITG | GAP-2313 | section 12 | Story side applied in section 12.2: the operations belong to P7 and the P4 attribution is not used. The TSD P4 text remains to be changed. |

### OTHER:Temporal and Drools Design; OTHER:parameters contract of rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01554 | RWB-ITG-E2027-ITG | GAP-2706 |  | Name the package code of the RES rule set held by rwb-decision, evaluated by rwb-treatment, and the parameter keys CURE_PERIOD_DAYS and restructure.max_breaks at contract freeze; publish no plan event in wave 2. |

### OTHER:Temporal and Drools Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01555 | RWB-ITG-E2027-ITG | GAP-1881 |  | Keep PAYMENT_MATCH with rwb-decision and its match rows with rwb-payment; evaluate RESTRUCTURE breach rows R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 in rwb-treatment; publish rwb.treatment.TreatmentClosed.v1 once per breached plan. |

### OTHER:FSD P8 v3 and TSD P8 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01558 | RWB-ITG-E2027-ITG | GAP-1624 | 18 | Fill the Requirements served table in FSD P8 v3 and the T8 Requirement traceability table in TSD P8 v2 with REQ IDs, or state that P8 has no requirement ID of its own. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01560 | RWB-ITG-E2027-ITG | GAP-0218 | Header | Record P7 rwb-decision as holder of the three LOV-MATCH-TYPE codes and P8 rwb-payment as reader, carried as the match type column of PAYMENT_MATCH; record package version in decision log. |

### OTHER:rwb-decision rule_row catalogue and evaluation result (TSD P8 T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01561 | RWB-ITG-E2027-ITG | GAP-1356 | 7 | Publish one column name, row order, in the rule_row catalogue and evaluation result; record priority (DF-REF-270) as the legacy and TSD name. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01562 | RWB-ITG-E2027-ITG | GAP-1358 | 12.4 | Story 12.4 states DecisionRecorded is read only; the consumer list itself belongs to the event catalogue. |

### OTHER:Platform secret-store catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01563 | RWB-ITG-E2027-ITG | GAP-1362 | 9 | Record names of the rwb-payment per-service login, Kafka client credential, Temporal mTLS material, registry certificate and workload identity, referenced by role in the chart. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01568 | RWB-ITG-E2028-ITG | DOR-RWB-ITG-E2028-ITG-12 | section 16, 18 | RTM v7 lists only legacy TC-E2-028 IDs. Story side: TC-E2-028-12, -13 and -14-ITG added, and -14-ITG added to REQ-ACA-005. |

### OTHER:Wave 2 SIT harness pack and Enterprise AI test tenant (integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01571 | RWB-ITG-E2028-ITG | GAP-0410 | - | Agree Enterprise AI test tenant and guardrail profile with P10 owner and platform team; agree harness pack, seeding and evidence format with QA. |

### OTHER:Contract story for this journey (not in the story set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01577 | RWB-ITG-E2029-ITG | DOR-RWB-ITG-E2029-ITG-21 | header | No published contract is identified in the sources; the Contract dependencies row reads Not specified. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01578 | RWB-ITG-E2029-ITG | DOR-RWB-ITG-E2029-ITG-22 | find it | No published fake library version exists in the sources. |

### OTHER:rwb-source-data contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01579 | RWB-ITG-E2029-ITG | GAP-1816 | header | Return the FSD source field names (party flag, deceased marker, freshness) on the contract; confirm with P1 before the wave 2 system test. |

### OTHER:rwb-document contract (P5) and rwb-source-data contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01580 | RWB-ITG-E2029-ITG | GAP-1822 | header | Confirm the document read with P5 and the call-note field with P1 before the shadow screening test. |

### OTHER:S8 contract story (rwb-deviation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01581 | RWB-ITG-E2029-ITG | GAP-1818 | header | Settle the raise, clear and case-record read paths, and record a GET path if one is kept, before the screen is built. |

### OTHER:Message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01583 | RWB-ITG-E2029-ITG | DOR-RWB-ITG-E2029-ITG-9 | 14 | A MSG-P7-002 row is in section 14 with placeholders; its wording and trigger are not in the source documents. |

### OTHER:FSD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01584 | RWB-ITG-E2029-ITG | GAP-1823 | 7 | AC2 is unchanged on this point; the rewrite of the FSD 'Timers shown' rows is left to the BA and QA lead. |

### OTHER:FSD S8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01585 | RWB-ITG-E2029-ITG | GAP-1826 |  | Add R-DEV-19, R-DEV-20 and R-DEV-21 to the named deviation rule set; package authoring and promotion stay in rwb-decision. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01587 | RWB-ITG-E2029-ITG | GAP-1832 | 7 | AC2 reverted; no field list asserted. |

### OTHER:Owning contracts of the screening evaluation and S8 raise path (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01589 | RWB-ITG-E2029-ITG | GAP-0626 | 12 | Contract values are fixed by their owners at the wave 2 contract freeze, not in this story. |

### RWB-S8-E2029-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01593 | RWB-ITG-E2029-ITG | GAP-3100 | 12 | Publish the raise request with the three added fields, name the agent-policy read, add the one-open-code unique index, publish the decision-record envelope type, and assign levels to legacy cases in the Test Cases workbook. |

### OTHER:Contract fake library of the contracts named in the Contract dependencies row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01595 | RWB-ITG-E2030-ITG | DOR-RWB-ITG-E2030-ITG-22 | 13 | Publish the fake library version for those contracts and record it in the story. |

### RWB-P5-E2025-CON; RWB-P10-E1062-CON; OTHER:rwb-litigation read contract; OTHER:rwb-case parameter contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01597 | RWB-ITG-E2030-ITG | GAP-0627 | 12 | Publish the per-case legal-action REST operation with member names, the checklist and OCR-text operations, the POST /agent-runs start operation, and the parameter keys for the minimum sample and promotion list. |

### RWB-P5-E2025-CON; RWB-P10-E2030-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01598 | RWB-ITG-E2030-ITG | GAP-0628 | 12 | Declare the OCR-text and checklist reads, the legal-action read path, the run operations, the five pack members with three statuses, and EV-28 as the only event. |

### RWB-P5-E2025-CON; OTHER:rwb-litigation read contract; OTHER:rwb-case parameter contract; OTHER:gateway-bff route contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01599 | RWB-ITG-E2030-ITG | GAP-2196 | 12 | Publish paths below /api/recovery/document/v1, the legal-action read path and members, parameter and list codes, the gateway-bff route path, the pack and run answer member types, and the service login. |

### OTHER:Harness README for the wave 2 integration harness (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01600 | RWB-ITG-E2030-ITG | GAP-0412 | 16 | Record the SIT wave 2 environment and seed, the LEGAL-S1 50-pack fixture, the MORTGAGE_CIVIL 9-item fixture, the model stub behaviours, the P5-down control, the evidence format and the pass and fail gate. |

### API:(service not named); OTHER:RWB-PLT platform story for the route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01601 | RWB-ITG-E2030-ITG | GAP-2197 | 12 | Add POST /api/recovery/agent/v1/agent-runs with its idempotency rule, the six AgentConfigVersion members beyond the baseline, the pack and score row member types, and the boundary read paths. |

### RWB-P10-E2030-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01602 | RWB-ITG-E2030-ITG | GAP-2358 | 12 | Publish the pack tool call as one operation per case with named per-item fields and a stated mapping of HTTP 503 to TOOL_UNAVAILABLE with fallback true. |

### OTHER:FSD P5 section A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01603 | RWB-ITG-E2030-ITG | GAP-2359 | 12 | State the case type to stage and route mapping, or add case type as a checklist key, and load the MORTGAGE_CIVIL checklist of 9 items at a named version. |

### OTHER:TSD P5 T3.1 (case_document_check) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01605 | RWB-ITG-E2030-ITG | GAP-2361 | section 7 | The defect status of a checklist item and its hub-side evidence belong in TSD P5 T3.1. The story is not changed until the TSD records them. |

### OTHER:Business Requirements Epic 1 (next version after v5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01607 | RWB-ITG-E2030-ITG | GAP-2362 | 19 | Name the BRD section and the L3 process of REQ-DCM-011 so the traceability row in section 19 can be completed. |

### RWB-P10-E2031-CON; RWB-P7-E2005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01609 | RWB-ITG-E2031-ITG | DOR-RWB-ITG-E2031-ITG-22 | header | Header Contract fake library version row reads Not specified (DOR-RWB-ITG-E2031-ITG-22) |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01611 | RWB-ITG-E2031-ITG | GAP-2316 | - | Add to the next contract version: object-type code of the agent monitor, record code of a read, access-entry field list, page bounds of the log read; name the read index in rwb_access; record the Flyway step. |

### OTHER:SIT harness profile (QA lead, wave 2 entry check) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01612 | RWB-ITG-E2031-ITG | GAP-0413 | - | Agree the harness profile, seed pack, fixed clock at 2026-12-14, evidence format and pass/fail gate; confirm the drift Schedule runs in rwb-agent. |

### RWB-P10-E1063-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01614 | RWB-ITG-E2031-ITG | GAP-0630 | - | Fix the seven added member names and four-decimal rule; name drift inputs after watch_measures members; add agent-version filter and three decision-record elements to the rwb-decision contract; name notice path; register route under RWB-PLT-N001-CON. |

### OTHER:Deployment slice of RWB-E2-031 v2 on rwb-agent (story key not given in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01618 | RWB-ITG-E2031-ITG | GAP-2200 | none | Apply the accepted defaults: route path fixed with the edge story; login referenced by a secret reference named with the platform administrator; topology and budget as values files reviewed at release; notice reached through its contract; Schedule created or updated idempotently by the release; single egress is the model gateway private endpoint declared once for the run path. |

### OTHER:checks/run_all.py and the plan generator (B-P10-02 fanout list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01619 | RWB-ITG-E2031-ITG | GAP-2201 | none | Remove RWB-E2-031 from the B-P10-02 fanout or retire B-P10-02 for this key; number the defaults once as ASM-B2-P10-005-1 to -24; mark the B-P10-02-E2031 gap and assumption rows superseded; add checks that fail on duplicate output paths and on ASM ids cited by a story that do not resolve in the assumptions folder. |

### RWB-P7-E2005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01621 | RWB-ITG-E2031-ITG | GAP-2199 | none | Add the agent-version filter and the override-reason element as additive members of GET /decision-log and GET /decision-log/{entryId}; use one page size with a cursor and four-decimal rate and amount members; route path and login fixed with the edge and deployment stories; Schedule keeps the baseline name and four steps. |

### OTHER:Deployment slice of RWB-E2-031 v2 on rwb-agent; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01622 | RWB-ITG-E2031-ITG | GAP-0631 | none | Reference the login as a secret reference named 'the rwb-agent login (DP-02)'; register the route under RWB-PLT-N001-CON with its path left to the edge story; expose every threshold and topology value as a named chart value, not hard-coded; update the Schedule in place and verify the two steps on one workflow identity; verify the consume right of rwb-reporting without creating its consumer group. |

### OTHER:FSD S2 and the S2 service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01626 | RWB-ITG-E2032-ITG | GAP-1713 | none | Map each FEAT prerequisite to its owning service contract (approval P7, case P3, documents P5, communications P6, valuation S1) once; carry the duplicate FEAT-CHO-08 as written. |

### OTHER:SCB IT infrastructure environment register (INT-23; OTHER:Key Vault, rwb-agent login, rwb.agent.events.v1, budgets, alarms) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01630 | RWB-ITG-E2032-ITG | GAP-0635 | find it | Record each INT-23 host, port, certificate, Key Vault, login, topic, sizing, budget and alarm value as a reviewed value per environment; provision per the proposed fix. |

### OTHER:Lists of values workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01638 | RWB-ITG-E2033-ITG | DOR-RWB-ITG-E2033-ITG-5 | 9 | Section 9 states no state transition |

### OTHER:23 Document Gaps/Recovery Workbench Assumptions Register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01640 | RWB-ITG-E2033-ITG | DOR-RWB-ITG-E2033-ITG-18 | 15 | Add an assumption for DL31 on RWB-ITG-E2033-ITG: TechX designer under the product owner, using ACE components, on gateway-bff composite routes. |

### OTHER:rwb-integration contract, /api/recovery/integration/v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01641 | RWB-ITG-E2033-ITG | GAP-0661 | find it | Contract baseline belongs to the integration contract and P3/P4 contract stories; no story text change needed. |

### OTHER:rwb-integration contract and P3/P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01642 | RWB-ITG-E2033-ITG | GAP-0660 | find it | Ownership and path decisions sit in the contract and P3/P4 stories, not in this story. |

### RWB-P2-E2033-CON; RWB-P3-E2011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01643 | RWB-ITG-E2033-ITG | GAP-2224 | find it | Fix v1 row and envelope names, confirm page bounds and export limit as parameter rows, add ageInStateDays beside ageDays, drop duplicate timer index, name login and flag owner. |

### RWB-P2-E2033-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01644 | RWB-ITG-E2033-ITG | GAP-3101 | find it | Declare read-only GET /api/recovery/deviation/v1/deviation-flags for S8 with a gap; add it to the consumed set at next revision; page bound as an rwb-case parameter row. |

### RWB-P2-E2033-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01645 | RWB-ITG-E2033-ITG | GAP-2320 | find it | Fix session element list, authorise branch and batch bound, extract record fields; record P2 attribution as a build-against dependency of the access slice. |

### OTHER:Wave 2 release record (harness appendix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01646 | RWB-ITG-E2033-ITG | GAP-0415 | find it | Ratify harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence and gate format as one appendix before Done. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01652 | RWB-ITG-E2034-ITG | GAP-1844 | Header | Keep the S9 partner identity slice in wave 2 as the partner identity and portal contract slice; publish partner_user binding and FAPI 2.0 route before panel work starts. |

### RWB-P3-E2034-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01655 | RWB-ITG-E2034-ITG | DOR-RWB-ITG-E2034-ITG-10 | 15 | The harness builds no screen. The §15 state rows added under CG-ALL-764/765 are marked Not specified where the specs are missing; the state text belongs to the owning app stories. |

### OTHER:Functional Specification P7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01658 | RWB-ITG-E2034-ITG | GAP-1612 | find it | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35. Keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012 under rwb-source-data. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01659 | RWB-ITG-E2034-ITG | GAP-3175 | find it | Keep AceDataReady (EV-26) as the target event name on rwb.source-data.events.v1 and list LoadCompleted as its legacy alias. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01660 | RWB-ITG-E2034-ITG | GAP-3176 | 12.5 | Confirm that no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### RWB-P2-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01661 | RWB-ITG-E2034-ITG | GAP-0590 | 5 | X1 marks key format and counting owner as Not specified (GAP-0590) |

### RWB-P1-E2001-APP; RWB-P2-E2034-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01662 | RWB-ITG-E2034-ITG | GAP-2186 | 12.2 | Publish the contact-fact read with path, contact-key parameter and masked members; confirm the EFS outcome read as GET /efs-history or name its operation; realign the two consumed rows of 12.2 to them. |

### OTHER:Ledger harness pack (wave 2 entry check) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01663 | RWB-ITG-E2034-ITG | GAP-0416 | 16 | Agree the composite route and merge order, SIT environment, seeding, evidence format, retention and pass/fail gate; hold the values as data in the harness pack. |

### RWB-P2-E2034-APP; RWB-P2-E2034-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01664 | RWB-ITG-E2034-ITG | GAP-0664 | 12 | Approve the five assumptions in contract review: login, append and fact element names, admin bodies, per-type mapping, retry intervals and default ruling. |

### RWB-P2-E2034-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01666 | RWB-ITG-E2034-ITG | GAP-0666 | 12.9 | Approve the two consumer groups, offset policy, commit point, scan and retry intervals, lag and alert thresholds, build ID format and fixture ownership as environment values in release readiness review. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01667 | RWB-ITG-E2034-ITG | GAP-2184 | 3 | Publish the retention class list and periods, add PARTNER_RESULT and OFFER to LOV-LEDGER-EVENT, confirm uuid link columns, and name the four feature IDs. |

### OTHER:Recovery Workbench plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01671 | RWB-ITG-E2034-ITG | GAP-3187 | header | Keep rwb-integration as primary for RWB-E2-033 to RWB-E2-036 and record the P3 tension for the assembly step. |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01672 | RWB-ITG-E2034-ITG | GAP-2185 | 12 | Settle one ledger path family in the case-scoped form, POST and GET /cases/{caseId}/interactions, and realign the append row of RWB-P1-E1066-APP and its fake to it. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON; RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01677 | RWB-ITG-E2035-ITG | DOR-RWB-ITG-E2035-ITG-22 | 12.8 | Publish the contract fake library for each contract dependency and record its published version |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01684 | RWB-ITG-E2035-ITG | GAP-3177 | 13 | Register the five-minute next-action Schedule in rwb-case; delete EV-18 from the Epic 2 contract tables. |

### RWB-P2-E2035-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01687 | RWB-ITG-E2035-ITG | GAP-0669 | 13 | Fix identity, secret reference and probe checks; add next-action-check job row with run book path; review three runbook entries with the on-call rota. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01688 | RWB-ITG-E2035-ITG | GAP-2406 | 7 | Sources disagree: registry stories give 2026-12-15 and the legacy key gives before 11 December 2026. The owning story must settle it, so no story edit is made. |

### RWB-P3-E2042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01689 | RWB-ITG-E2035-ITG | GAP-2405 | 7 | Fix the rule-catalog row answer and the latest-state-change answer schemas; add 404 and 422 entries of MSG-P3-027 and MSG-GEN-001 for both reads. |

### OTHER:Gateway-bff platform edge story and the wave 2 integration entry check record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01692 | RWB-ITG-E2035-ITG | GAP-0418 | 12 | Record the composite route path, merge order, call list, slow-source answer, harness repo, SIT env, seeded data, evidence format, retention and pass/fail gate |

### OTHER:Recovery Workbench delivery plan (primary-service rows of RWB-E2-033 to RWB-E2-036) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01695 | RWB-ITG-E2035-ITG | GAP-3187 | header | Keep rwb-integration as primary for the four keys and record the case-and-workflow tension for the assembly step. |

### OTHER:rwb-case reference data (list of values for rule_row.timer_spec) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01699 | RWB-ITG-E2035-ITG | GAP-2408 | 8 | Publish the timer spec shapes as a list of values with their parsing rule, extended with 'payment due 30 days' and 'deadline driven', so the caller parses the data and the registry returns a string. |

### RWB-P7-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01701 | RWB-ITG-E2035-ITG | GAP-2410 | header | Record that a secondary slice builds against the platform contracts and published fakes and reads the same service's wave-1 rows through its own schema, keeping lane depth within R5.7 rule 5. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01703 | RWB-ITG-E2036-ITG | CG-ALL-779 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P2 rwb-integration (Integration)/RWB P2 E2036 CON Queu (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01706 | RWB-ITG-E2036-ITG | DOR-RWB-ITG-E2036-ITG-22 |  | Record the published version of the contract fake library defined in section 12.8 |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01707 | RWB-ITG-E2036-ITG | DOR-RWB-ITG-E2036-ITG-8 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-versions and POST /api/recovery/access/v1/authorise (see CG-ALL-778 and CG-ALL-779) |

### RWB-P2-E2036-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01710 | RWB-ITG-E2036-ITG | GAP-0670 | 4, 12, 13 | Keep POST /api/recovery/case/v1/queues/{queueId}/placements with rwb-case; rwb-integration serves POST /api/recovery/integration/v1/queues/{queueId}/placements forwarding to it; read the approved callers list through rwb-case under rwb.casewf.placement.approved-callers. |

### RWB-P2-E2036-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01711 | RWB-ITG-E2036-ITG | GAP-0671 | 12 | Declare the integration-base placement as provided with the four legacy body fields, a required Idempotency-Key and the legacy 201 shape; declare the case-base placement as consumed and owned by P3; mark unpublished consumed element names as placeholders. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01712 | RWB-ITG-E2036-ITG | GAP-0957 | 12 | Carry the section 12.1 element names of the authorise and me/permissions request and answer in the service contract; reconfirm with RWB-P2-E2036-CON 12.2 at contract review; keep caller type as a carried value of the approved callers list. |

### OTHER:Wave 2 queue-placement harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01713 | RWB-ITG-E2036-ITG | GAP-0419 | 13 | Agree the composite placement route path and merge order, harness repository, SIT environment, seeded callers, queues, caps and overflow queues, evidence format, retention and pass/fail gate, and hold them as data in the harness pack. |

### OTHER:Service contract document for rwb-access queue-write authority (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01715 | RWB-ITG-E2036-ITG | GAP-0958 | 14 | Fix five reason codes with one status each: 403 for RIGHT_NOT_HELD, CALLER_KIND and SCOPE_NOT_ALL; 422 and 503 keep MSG-GEN-001, MSG-GEN-002 and MSG-P7-003. MSG-P4-002 is the message of every 403. |

### RWB-S8-E2036-APP; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01716 | RWB-ITG-E2036-ITG | GAP-3102 | 13 | Publish the hold element (case reference, deviation reference, code, open count, handler, return point, contact-stop flag, rule version) and have the rwb-case owner declare the event-driven set and clear of recovery_case.deviation_open. |

### OTHER:Build plan (the plan that gives RWB-E2-033 to RWB-E2-036 primary P2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01719 | RWB-ITG-E2036-ITG | GAP-3187 |  | Directive accepts keeping the plan primary. The change is in the plan, not this story, so no story edit is made. |

### OTHER:Contract fake library (section 12.8 fakes) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01722 | RWB-ITG-E2038-ITG | DOR-RWB-ITG-E2038-ITG-22 | 12.8 | Publish the contract fake library and record its published version in the story. |

### OTHER:Wave 0 Service Catalog (platform login, task queue, admin base); OTHER:key management runbook (codec key rotation and version retention) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01723 | RWB-ITG-E2038-ITG | GAP-1441 | find it | Fix the platform login, task queue and admin base in the Wave 0 Service Catalog, and the codec key rotation period and version retention in the key management runbook. |

### OTHER:Screen specifications for SCR-38 and SCR-43 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01725 | RWB-ITG-E2038-ITG | DOR-RWB-ITG-E2038-ITG-10 | find it | Add empty, loading, error and no access states for SCR-38 and SCR-43. |

### OTHER:Version 4 of the Temporal security design (section 4.1 and section 7.1 rows, per GAP-2038 evidence) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01728 | RWB-ITG-E2038-ITG | GAP-2038 |  | The story names SY-RULES only as a refused caller and maps no workload identity to SY- roles; the mapping change belongs to the Temporal security design. |

### 08 AI and agents/Recovery Workbench AI and Agent Architecture v2.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20620 | RWB-ITG-E2038-ITG | R-28677 |  | Workload-to-SY role mapping belongs to the Temporal security design, not this document. Document not searched: docview tool unavailable. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20811 | RWB-ITG-E2027-ITG | R-28825 |  | Row order belongs to the rule_row catalogue. DF-REF-270 priority is already the TSD name in T3.1. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0218 | LOV-MATCH-TYPE is used by payment_match_rule, a table the target drops and the Ownership Map does not carry | Center of excellence | Resolved (directive) |
| GAP-0260 | payment_match_rule is in the inventory but not in the Ownership Map, and D-RCV-36 retires it as a table | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0409 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0410 | The agent-intake harness pack, the Enterprise AI test endpoint and the policy fixtures are not specified | Integration lead | Resolved (directive) |
| GAP-0411 | SIT harness environment, SCREEN-S2 fixture pack, Enterprise AI test profile, evidence format and gate for the deviation-screening journey are not specified in any source read | Integration lead | Resolved (directive) |
| GAP-0412 | Harness environment, seed fixtures, model stub, evidence format and pass gate for the legal document agent shadow journey are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0413 | SIT harness environment, two-week and November seed, fixed clock, cost reconciliation fixture, evidence and gate for the agent-monitor journey | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0414 | The TDR suggestion has no agreed start operation: the legacy treatment side calls rwb-agent in process, Architecture v5 gives no S2-to-P10 call, and no source gives the harness environment, the TDR model stub controls, the evidence format or the gate | Integration lead | Resolved (directive) |
| GAP-0415 | The SIT harness environment, seed pack, OpenXML comparison method, access-log assertion and evidence format for the case-list journey are not specified in any source read | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0416 | Ledger harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0417 | Workflow security harness environment, seeding, evidence format, retention and test certificate details are not specified | Integration lead | Resolved (directive) |
| GAP-0418 | Gateway-bff composite next-action route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0419 | Wave 2 queue-placement harness: composite route, environment, seeding, evidence format and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0590 | The repeat of an EFS history entry is counted in this service or in the ledger writer, and the key format is unnamed | Solution architect, P1 | Resolved (directive) |
| GAP-0622 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the item key set, the invalid-verdict refusal, the migration order and the segment rule are not specified | Solution architect with the P10 service owner and the owners of rwb-case and rwb-decision | Resolved (directive) |
| GAP-0623 | Case intake agent at L1 contract in rwb-agent: the member types of the answer and of the request, the record event type name, the route path, the 409 rule and the invalid-verdict refusal are not specified | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision and rwb-case | Resolved (directive) |
| GAP-0624 | Case intake agent at L1 deployment in rwb-agent: the login, the migration order, the topic partitions and retry names, the alert window and thresholds, the worker and probe values and the route path are not specified | Platform administrator with the DevOps team and the ACE database team | Resolved (directive) |
| GAP-0625 | The app slice of the deviation screening evaluation and L1 on one segment: the service login, the S8 raise contract story, the parameter keys of the floor and the promotion condition, the sealed decision-entry read, the gateway-bff route path and the migration numbering are not fixed by any source | TechX with the rwb-deviation (S8) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0626 | The contract slice of the deviation screening evaluation and L1 on one segment: the S8 raise path and members, the parameter keys, the member types of a consumed answer, the sealed decision-entry read, the service login and the route path are not specified by any source | TechX with the rwb-deviation (S8) owner, the rwb-decision (P7) owner, the rwb-case (P3) owner and the platform team | Resolved (directive) |
| GAP-0627 | The app slice of the legal document agent in shadow: the document, OCR-text and checklist operations and members, the legal-action read, the run-start path, the parameter keys, the service login, the route, the BRD section of REQ-DCM-011 and the pack member types are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0628 | The contract baseline of the legal document agent: the OCR-text and checklist operations and member names, the legal-action read, the run-start path, the route, the paging and member types, and the event family beyond EV-28 are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-document, rwb-litigation and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0630 | The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source | Tech lead of rwb-agent | Resolved (directive) |
| GAP-0631 | The deployment slice of the agent monitoring dashboard v2: the topology, alert thresholds, login, route path, the Schedule update path and the consumer group ownership are not specified | Platform administrator | Resolved (directive) |
| GAP-0633 | The TDR offer-suggestion slice in rwb-agent: the operation path below the base, the treatment and account read operations, the parameter keys, the screen route, the run version fields, the inputs reference and the two waits of the call are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-treatment, rwb-case and rwb-decision | Resolved (directive) |
| GAP-0634 | The TDR offer-suggestion contract slice: the operation path and request members, the record member types, the boundary answer and error mapping, the admin read route and the two-wait exception are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision, rwb-treatment, rwb-case and rwb-source-data | Resolved (directive) |
| GAP-0635 | The infrastructure slice of the TDR offer-suggestion key: the INT-23 host, port, certificate and Key Vault names, the partition and retention values, the sizing, the budget measurement points and the alarm thresholds are not specified by any source | SCB IT infrastructure with the ACE platform team and security | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0664 | The rwb-integration login, the entry and fact JSON field names, the admin bodies, the mapping detail, the retry intervals and the ownership split of the ledger intake are not fixed in the source documents | Solution architect | Resolved (directive) |
| GAP-0665 | The append, EFS and contact wire shapes, the admin operation bodies, the dedupe key of each type and the ordering of the append and the inbox are not stated for the intake contract | Solution architect | Resolved (directive) |
| GAP-0666 | The consumer group names, the offset policy, the retry scan interval, the lag and alert thresholds, the build ID format and the fixture owner of the intake deployment are not fixed in the source documents | DevOps lead | Resolved (directive) |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0669 | rwb-integration next action deployment: the login and secret reference, the next-action-check run values, the alert thresholds and the runbook ownership are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner | Resolved (directive) |
| GAP-0670 | rwb-integration queue-write adapter: the operation owner, the login, the consumed contract field names and the replay window are not fixed by one source | Solution architect | Resolved (directive) |
| GAP-0671 | rwb-integration queue-write adapter contract: the ownership of the placement path, the consumed contract shapes and the library table columns are not fixed by one source | Tech lead | Resolved (directive) |
| GAP-0734 | The next-action slice leaves the legacy AC allocation, the daily check Schedule, the DL22 durations and the role-class field unspecified | Tech lead | Resolved (directive) |
| GAP-0735 | The placement slice leaves the legacy AC allocation, the approved callers list, the production matrix grant, the overflow shape, the caller mapping and the login name unspecified | Tech lead | Resolved (directive) |
| GAP-0957 | rwb-access queue-write authority: the request and answer element set of the placement admission part of POST /authorise and of the non-human part of GET /me/permissions is named by no source | Solution architect | Resolved (directive) |
| GAP-0958 | rwb-access queue-write authority: the refusal reason code vocabulary and the status each code answers with are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0959 | rwb-access queue-write authority: no source binds a role to a list of teams or regions, so a scope narrower than ALL cannot be resolved for a non-human caller | Security administrator | Resolved (directive) |
| GAP-0960 | rwb-access queue-write authority: how a caller code is bound to a Workbench role, and whether a caller code is itself a role, is fixed by no source | Security administrator | Resolved (directive) |
| GAP-1290 | PAYMENT_MATCH registry governance: shapes, decision-record payload, message set and promotion and rollback semantics are not specified | Solution architect, with the P7 business analyst and the rule owner RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1293 | The rule-package operations: the legacy P4 attribution and the /admin/rule-versions paths against P7 and /admin/rule-package-versions | P7 solution architect, with the API specification owner | Resolved (directive) |
| GAP-1294 | No source gives the value set or the wire shape this story needs: the append request and answer, the ledger read and its page, the reason codes, the run read field set, the text of MSG-P7-009 and the DP-02 login name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1355 | The AC6 package load and the rule-evaluation contract have no C row in this key | Solution architect | Resolved (directive) |
| GAP-1356 | The ordering column is called row order in the story and priority in the TSD | Data steward | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1358 | DecisionRecorded is listed as consumed here but the catalogue names only two consumers | Integration architect | Resolved (directive) |
| GAP-1359 | The rule-evaluation result has no published schema and two of its field names are not given | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1360 | The three payment event payloads have no schema in any source | Integration architect | Resolved (directive) |
| GAP-1361 | No numeric operations value is specified for the matching service | DevOps engineer | Resolved (directive) |
| GAP-1362 | The secret names, the workload identity and the certificate of rwb-payment are not specified | Identity and access team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1441 | Platform identity and Temporal security values are not fixed in the read sources | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1463 | RWB-E2-032 is conditional on a model existing and no decision row names who confirms it | Restructure operations officer with the TDR team | Resolved (directive) |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1624 | FSD P8 issues no requirement ID, so the product requirement cannot be traced to an FSD requirement | Business analyst, P8 | Resolved (directive) |
| GAP-1625 | Eight of the eleven P8 features carry a placeholder acceptance criterion instead of a testable one | Business analyst, P8 | Resolved (directive) |
| GAP-1626 | The two operations named in Architecture v5 slide 17 are not the two operations in the API Specification and the Ownership Map | Solution architect | Resolved (directive) |
| GAP-1628 | The matching values have no table and no owner after payment_match_rule was retired | Solution architect | Resolved (directive) |
| GAP-1631 | The FSD names ALS, GL, ATS and AMIS as interface points, and v5 lets no service call a system of record | Solution architect | Resolved (directive) |
| GAP-1639 | The two event-started workflows have no name or identifier in any v5 source | Solution architect | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1832 | The two deviation events have a catalogue row and a topic but no field list, while the criteria expect an agent verdict and a decision log entry to travel with them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1880 | The treatment-side matching read, the shortfall columns, the breach decision code and the plan-check cadence are not specified | Solution architect with the rwb-treatment and rwb-payment squads | Resolved (directive) |
| GAP-1881 | PAYMENT_MATCH is the rwb-payment matching package while this slice evaluates it for the plan breach on the treatment side | Solution architect with rwb-decision, rwb-payment and rwb-treatment | Resolved (directive) |
| GAP-1882 | The treatment-side use of the suggestion is unspecified: the agent-run operation and its payload on the caller side, the treatment columns that hold the proposal and the model, prompt and policy versions, the 60 s wait and its fallback contract, and the decision code of a suggestion record | Solution architect | Resolved (directive) |
| GAP-1883 | Architecture v5 slide 16 publishes no inbound suggestion operation on rwb-agent, while the legacy treatment flow calls one synchronously | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2038 | The mapping of a service workload identity to the SY- roles is not specified | Platform with P3 rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2042 | The codec server and the per-namespace codec keys have no owner and no rotation rule | Platform (RWB-PLT-WF) with SCB IT security | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2184 | The retention class list, the added event codes, the link column types and the feature IDs of four requirements are in no source | Data architect | Resolved (directive) |
| GAP-2185 | The interaction ledger is published on two different operation paths | Solution architect | Resolved (directive) |
| GAP-2186 | The EFS outcome read and the contact-fact read that the channel consumer calls are named by interface only, with no path, parameter or owning story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2190 | Case intake agent live at L1 in rwb-agent: the service login, the decision code, the business date of the stale check, the acceptance event name, the list codes, the case-decision proposal path, the route path, the feature flag home, the topic and migration values and the policy values the gate reads are not specified | Solution architect with the P10 service owner and the owners of rwb-case, rwb-decision and rwb-source-data | Resolved (directive) |
| GAP-2191 | Case intake agent at L1 contract in rwb-agent: the member types of the answer and of the request, the acceptance event name, the case-decision proposal path, the route path, the 409 rule, the item key set, the invalid-verdict refusal and the policy values are not specified | Tech lead of rwb-agent with the solution architect and the owners of rwb-case and rwb-decision | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2192 | Case intake agent at L1 deployment in rwb-agent: the login, the route path, the topic partitions, retry and retention, the migration order, the alert window and thresholds, the worker and probe values and the consumer groups are not specified | Platform administrator with the DevOps team and the ACE database team | Resolved (directive) |
| GAP-2193 | RWB-P10-E2029-APP: values the sources leave open for the screening L1 app slice | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2194 | RWB-P10-E2029-CON: contract detail the sources leave open for the screening key | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2196 | Legal document agent in shadow in rwb-agent (app slice): the consumed operation paths below the rwb-document base, the legal-action read path, the parameter codes and the list codes, the gateway-bff route path, the member types of the pack and of the run answer, and the service login are not specified | Solution architect with the owners of rwb-document, rwb-litigation and rwb-case, and the platform library owner for the route | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2197 | Legal document agent in shadow in rwb-agent (contract slice): the run-start path below the agent base, the consumed boundary paths and field names, the six policy members beyond the baseline, the member types of the pack and the score row, and the gateway-bff route path are not specified | Solution architect with the owners of rwb-document, rwb-litigation and rwb-case, and the platform library owner for the route | Resolved (directive) |
| GAP-2198 | RWB-E2-031 version 2 app slice: the drift step and its Schedule, the segment source, the decision-log read, the notice, the policy values, the migration scope, the element change, the screen states, the login, the route path, the range limits and the two windows are not named by the sources | Tech lead of rwb-agent with the solution architect | Resolved (directive) |
| GAP-2199 | RWB-E2-031 version 2 contract slice: the decision-log filter and override element, the notice operation, the name of the read right, the paging and member types, the route path, the login and the Schedule step names are not fixed by the sources | Tech lead of rwb-agent with the owners of rwb-decision, rwb-comms and rwb-access | Resolved (directive) |
| GAP-2200 | RWB-E2-031 version 2 deployment slice: the route path, the login secret, the topology and budget, the notice operation, the Schedule registration detail and the model gateway egress are not fixed by the sources | DevOps engineer with the platform administrator and the security administrator | Resolved (directive) |
| GAP-2201 | Two Work Packages write the same three story files, the same three fragments and two overlapping assumption sets for legacy RWB-E2-031 on rwb-agent | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2224 | The case list is served twice in the target, and the row names, the bounds, the login and the flag mechanism of the owner's list have no source | Solution architect | Resolved (directive) |
| GAP-2225 | Element names of the interaction item, the append command and the intake result are not in the sources | TechX and rwb-source-data contract owner | Resolved (directive) |
| GAP-2226 | Legacy occurred-time order and the case timeline page order differ | TechX | Resolved (directive) |
| GAP-2311 | Values of the payment-matching access profile that the legacy story does not state | Business analyst, P4 | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2313 | The rule-package endpoints are P4 in the legacy contract and P7 in Arch v5 | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2314 | No legacy acceptance criterion of RWB-E2-027 belongs to the P4 slice | Business analyst, P4 | Resolved (directive) |
| GAP-2316 | The agent-monitor object of the access log, the record code of a read, the field list of an entry and the migration step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2318 | The legacy story and the rwb-agent contract name different rights for the same read of the agent monitor | Security administrator | Resolved (directive) |
| GAP-2319 | The secondary slice carries no legacy acceptance criterion of its own, and the legacy data, endpoint, job and screen blocks belong to other services and other slices | Business analyst with the solution architect | Resolved (directive) |
| GAP-2320 | rwb-access answer behind the case and queue list: element names, the P2 attribution of the contract dependency, the authorise branch, the extract record, the login and the parameter and reference paths are not settled by any source read | Solution architect | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2322 | rwb-access next action: the role-catalogue operation, the authorise request and answer of a next-action read, the rwb-access login and the message for an unknown role code are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2323 | rwb-access next action: the role class list has no customer-party value, while the legacy waiting text is produced for a customer party or a partner user | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2324 | rwb-access next action: the RBAC matrix tabulates three capability areas and gives no Case record letter, so the R rights and the scopes the next-action read needs are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2325 | rwb-access next action: a role row carries no version label of its own and the lifetime of a cached access or role answer is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2358 | The rwb-agent tool call, per-item field names and unavailable-read mapping behind RWB-P10-E2030-CON | Solution architect | Resolved (directive) |
| GAP-2359 | The checklist is keyed by stage and route while the legacy asks for the checklist of a case type | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2360 | The per-item fields of the document checklist answer the pack reader needs | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2361 | The defect status of a checklist item and the evidence it needs on the hub side | Business analyst, P5 | Resolved (directive) |
| GAP-2362 | The BRD section and L3 process of REQ-DCM-011 | Business analyst, programme | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2400 | The route-set criterion of the legacy story belongs to RWB-E2-035 and no source states that a notice of rwb-comms reads the route set | Business analyst | Resolved (directive) |
| GAP-2402 | No source gives the wire shapes, the value sets or the dependency rows this story needs: the append request and answer, the evaluation and run reads, the case-less approval row, the promotion decision code, the text of MSG-P7-009, the name behind EV-30 and the DP-02 login name | Solution architect, P7 rwb-decision, with the P10 rwb-agent owner, the rwb-case owner, the data steward and the delivery lead | Resolved (directive) |
| GAP-2403 | No source gives the wire shape or the value sets this story needs: the append request and answer, the ledger read and its page, the reference-data operation, the text of MSG-P7-009 and the DP-02 login name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2405 | rwb-decision next action: the answer shape of the rule-catalog and latest-state-change reads, and their not-found and malformed-parameter messages, are not specified | Solution architect | Resolved (directive) |
| GAP-2406 | The valid-from date of package version RES-2026.12 is 2026-12-15 in the registry stories and before 11 December 2026 in the legacy key every test of this story reads | Business analyst, P7 | Resolved (directive) |
| GAP-2407 | rwb-decision next action: no source enumerates the decision codes or final calls that count as a state change for the latestStateChange filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2408 | rwb-decision next action: rule_row.timer_spec has no list of values, and two legacy specs are outside the four shapes the legacy rule enumerates | Business analyst, Epic 2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2409 | The published catalogue path shows packageVersion as an optional query parameter and no source says what an absent value answers | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2411 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-2507 | The consumed rule-evaluation result, the treatment installment-paid call, the three event payloads and the shared record's consumer list have no published schema or operation name | Solution architect, with the owners of rwb-decision, rwb-treatment and the event catalogue | Resolved (directive) |
| GAP-2508 | No numeric operations value and no name of a secret, identity or certificate is specified for the matching deployment | DevOps engineer, with the platform administrator and the identity and access team | Resolved (directive) |
| GAP-2705 | The match consequence that rwb-treatment consumes is not published, and no source names the plan states the treatment row holds after a match | Contract owner of rwb-treatment with the owner of rwb-payment and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2706 | No source names the rule set, the parameter codes or the signal that announce a plan state change, and none states who consumes the plan consequence once rwb-treatment owns it | Solution architect with the rule owner of rwb-decision and the parameters owner of rwb-case | Resolved (directive) |
| GAP-3100 | RWB-S8-E2029-APP: the confirmed-proposal raise has no published request shape beyond the legacy Java signature, no operation name for the agent-policy read, no published constraint for one open code, no envelope type for the decision-record entry and no test level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3101 | rwb-deviation case and queue list slice: no read in the Ownership Map, no seam with the composed page, no path, field names or page bound, the flag derived twice and the pause projection without the rule package | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3102 | RWB-S8-E2036-APP: the deviation hold that the queue-write interface obeys has no published element names, no case-event names, no case-side setter for deviation_open and no placement-half criteria, and the pattern set adds dependencies the metadata rows do not carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3149 | rwb-partner interaction-ledger slice: no ledger column or operation in S9, no published payload for EV-20 or EV-21, the seam with RWB-P2-E2034-CON undefined, the list members, the retry bound and the holder-reference form unpublished, and an empty H row against ten platform contracts | Solution architect; rwb-integration contract owner (RWB-P2-E2034-CON); rwb-source-data ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3187 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while their code and tables are in rwb-case | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3188 | The payment match rule load is a P4 reference load in the story and a P7 rule package in the target | Decision and rules lead with the access lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E2027-ITG | skipped AC ID | 110 | missing: AC6, AC7, AC10 |
