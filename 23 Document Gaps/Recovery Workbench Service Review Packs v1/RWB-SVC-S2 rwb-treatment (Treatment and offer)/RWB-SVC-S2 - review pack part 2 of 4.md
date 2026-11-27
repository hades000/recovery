# RWB-SVC-S2 rwb-treatment (Treatment and offer) - review pack, part 2 of 4 (RWB-S2-E2018-APP to RWB-S2-E3003-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 10 |
| Resolved in the stories | 225 |
| Cross-document (pending in another document) | 220 |
| Not applied (value not in the sources) | 24 |
| Open business decisions | 21 |
| Register gaps linked | 131 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S2-E2018-APP | 30 | 30 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2018 APP E-signature flow for customers and the bank v2.md |
| RWB-S2-E2025-APP | 31 | 33 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2025 APP Extraction for the stage 2 and 3 document types v2.md |
| RWB-S2-E2026-APP | 24 | 22 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2026 APP Document generation engine for contract, CA and mortgage templates v2.md |
| RWB-S2-E2027-APP | 24 | 39 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2027 APP Payment matching rules with the data team v2.md |
| RWB-S2-E2032-APP | 24 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2032 APP TDR offer-suggestion model through the model gateway [E3e] v2.md |
| RWB-S2-E3001-APP | 26 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3001 APP Create the treatment record v2.md |
| RWB-S2-E3001-CON | 12 | 17 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3001 CON Create the treatment record - contract v2.md |
| RWB-S2-E3002-APP | 17 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3002 APP Offer a settlement inside the range v2.md |
| RWB-S2-E3002-CON | 17 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3002 CON Offer a settlement inside the range - contract v2.md |
| RWB-S2-E3003-APP | 20 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3003 APP Approve a settlement below the floor v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S2-E2027-APP | R-02203 | CG-ALL-8423 | Script gap | Product owner | The story adds CURE_PERIOD_DAYS to the closed list LOV-TRT-OUTCOME | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-S1-E4009-APP, RWB-S1-E4009-CON, RWB-S2-E3003-APP, RWB-S2-E3003-CON, RWB-S7-E6018-APP, RWB-S7-E6018-CON | R-09221 | GAP-1464 | Register gap | Risk with the product heads | The approval limits by decision, product and amount are not set, so no approval requirement can be tested against its limit | Load the regulation's published levels as reference data in the version that applies at the release date, keep every limit and substitute as a versioned row with a valid-from date, and let each acceptance criterion run against the loaded version. No limit is written in this document, in a story or in code. |
| RWB-S1-E4006-APP, RWB-S1-E4006-CON, RWB-S2-E3002-APP, RWB-S2-E3002-CON, RWB-S2-E3003-APP, RWB-S2-E3003-CON | R-09237 | GAP-1465 | Register gap | Product head (Mortgage, HP, SSME) | The settlement range and the floor price basis per product are not specified | Hold the range and the floor as versioned reference rows per product and effective date, load a documented test version for SIT, and let the business owner approve the production version in the same way as the treatment policy. |
| RWB-S2-E2018-APP | R-12156 | CG-ALL-8376 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E2025-APP | R-12172 | CG-ALL-8401 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E2026-APP | R-12179 | CG-ALL-8418 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E2027-APP | R-12182 | CG-ALL-8428 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E2032-APP | R-12188 | CG-ALL-8442 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3001-APP | R-12194 | CG-ALL-8458 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3003-APP | R-12212 | CG-ALL-8497 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2025-ITG, RWB-P5-E2025-APP, RWB-P5-E2025-CON, RWB-P5-E2025-OPS, RWB-P7-E2025-APP, RWB-S2-E2025-APP, RWB-S4-E2025-APP | R-22604 | GAP-1285 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The extraction decision record's payload, value sets, read shape and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the extraction column set of decision_log_entry (new columns or jsonb members), the decision code of an extraction decision, the final-call value set, the threshold parameter names and version labels, the message ids and their texts, the document filter of the read and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2025-1 and its eight criteria stand on that shape |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-22619 | GAP-1287 | Register gap | Solution architect, P7 rwb-decision, with the data steward and the business owner | The generation record's payload, value sets, read shape, message set and screen id have no source | At design time of wave 2 the solution architect, the data steward and the business owner agree and approve, as reference data and as the OpenAPI of the service: the container of the template code, the template version, the treatment reference and the requesting role on decision_log_entry, the shape of the merge snapshot reference, the decision code D6.4 as a value of LOV-DECISION, the final-call list that holds GENERATED, the message ids and texts of a refused record and a duplicate append, the page-size parameter name, the search index and the panel id; until then the story holds the assumed shape of ASM-B-P7-03-E2026-1 to ASM-B-P7-03-E2026-5 and its nine criteria stand on that shape |
| RWB-ITG-E2028-ITG, RWB-ITG-E2029-ITG, RWB-ITG-E2030-ITG, RWB-ITG-E2031-ITG, RWB-ITG-E2032-ITG, RWB-P10-E2028-APP, RWB-P10-E2028-CON, RWB-P10-E2028-OPS, RWB-P10-E2029-APP, RWB-P10-E2029-CON, RWB-P10-E2030-APP, RWB-P10-E2030-CON, RWB-P10-E2031-APP, RWB-P10-E2031-CON, RWB-P10-E2031-OPS, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P4-E2031-APP, RWB-P5-E2030-APP, RWB-P7-E2028-APP, RWB-P7-E2029-APP, RWB-P7-E2032-APP, RWB-S2-E2032-APP, RWB-S8-E2029-APP | R-22645 | GAP-1527 | Register gap | Product owner | The Epic 2 legacy keys the FSD cites as the story of the feedback and legal pack criteria have no requirement row in the epic BRD | The PRD cites the three keys as the legacy story of the capability and traces the product requirement to the BRD requirement it serves, so the missing requirement row does not change what is built. The epic BRD is asked to add the three rows in its next version. |
| RWB-S2-E3003-APP, RWB-S2-E3003-CON, RWB-S2-E3012-APP, RWB-S2-E3012-CON | R-23367 | GAP-1706 | Register gap | Risk with the product heads | The approval limits the settlement and deed in lieu depend on are held by another service, are open as a decision, and are quoted differently in two places | Read every limit from the versioned delegation table of rwb-access at run time, record the level applied and the approver role on the treatment, and test with one documented test set until DL18 is answered; the two quoted sets are not reconciled here. |
| RWB-ITG-E2026-ITG, RWB-P4-E2026-APP, RWB-P5-E2026-APP, RWB-P5-E2026-CON, RWB-P6-E2026-APP, RWB-P7-E2026-APP, RWB-S2-E2026-APP | R-28820 | GAP-0940 | Register gap | Compliance and PDPA officer | The masking version label and the DF-PTY-007 rows on the generation path are not specified | Load the DF-PTY-007 masking rows with unmasked false for RW-RESTRUCT, RW-CASEOWN, RW-TEAMMGR and SY-CASEWF under the SIT masking version, name the version in the policy pack load record, and leave the format to the one masking library every screen uses. |
| RWB-ITG-E2032-ITG, RWB-P10-E2032-APP, RWB-P10-E2032-CON, RWB-P10-E2032-INF, RWB-P7-E2032-APP, RWB-S2-E2032-APP | R-28842 | GAP-1531 | Register gap | Product owner | The boundary of the TDR suggestion message is not defined between rwb-agent and the treatment screen | The PRD requires that a caller learns that no suggestion is available and why, in the terms of the outcome the service recorded, and leaves the screen, the wording and the message ownership to the treatment PRD and the message standard. |
| RWB-S2-E3001-APP, RWB-S2-E3001-CON, RWB-S2-E3018-APP, RWB-S2-E3018-CON | R-29105 | GAP-1714 | Register gap | Product Owner | No approval is recorded for the requirements this PRD states | Keep the document at status Draft, leave the approval table empty, and treat the missing approval as an assumption rather than an answer; the gate is cleared by the Product Owner and the FDA after this run. |
| RWB-S2-E3002-APP, RWB-S2-E3002-CON, RWB-S2-E3003-APP, RWB-S2-E3003-CON, RWB-S2-E3012-APP, RWB-S2-E3012-CON | R-29108 | GAP-1711 | Register gap | Compliance and PDPA officer | The classification and the retention of the treatment, the agreements and the plan timers are not set | Apply the working labels of this document (SENSITIVE_FINANCIAL for the terms and the agreements, CONFIDENTIAL for the references) and state the retention period as open; the class sets handling and the period is set under DL26. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S2-E2018-APP | R-02190 | CG-ALL-8359 | 13 | Index column treatment.signature_request_ref is not a field of treatment in LDM v9 | Index line for signature_request_ref is in section 13, outside this chunk, so no exact old text. LDM v9 DF-TRT-030 signature_status confirmed as the replacement; needs the section 13 chunk. |
| RWB-S2-E2018-APP | R-07626 | DOR-RWB-S2-E2018-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version is recorded in the story or sources. Version not specified in the source documents (DOR-RWB-S2-E2018-APP-22). |
| RWB-S2-E2018-APP | R-19178 | DOR-RWB-S2-E2018-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Section 8 rows R-UNI-40, R-RES-18, R-SET-11, CTL-12 have no BR ID in the chunk. BR10 and BR11 criteria and TC rows are in sections 7 and 16, outside this chunk. Adding IDs now would leave new rules uncovered. |
| RWB-S2-E2018-APP | R-22535 | GAP-2701 | 7, 8 | The legacy one module and one transaction for the signature request, the signed version and the treatment field become three owners, and the offer expiry that closed the request is now the treatment's own date | Reconciliation text must sit in sections 7 and 8 (lines 118-250), which this chunk omits; only the header was sent. Re-send those parts to apply. |
| RWB-S2-E2025-APP | R-19181 | DOR-RWB-S2-E2025-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | The field is named only in detcheck X10 citing section 12.3 payload and log lines, which are outside this chunk. No field value found; Not specified in the source documents (DOR-RWB-S2-E2025-APP-11). |
| RWB-S2-E2025-APP | R-19186 | DOR-RWB-S2-E2025-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR13-BR16 IDs added to rule rows R-UNI-38, CTL-08, CTL-11, CTL-12 in section 8. BR1-BR12 coverage by criteria and tests is in sections 7 and 16, outside this chunk. |
| RWB-S2-E2026-APP | R-07636 | DOR-RWB-S2-E2026-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources. Decision Log v12 line 81 (DT05) is a general rule, not a sign-off. Needs the record. |
| RWB-S2-E2026-APP | R-19190 | DOR-RWB-S2-E2026-APP-10 | find it | Definition of Ready item 10 Screens and states: Partial | SCR-14/SCR-15 state rows are in the section not supplied. The story file I found has different numbering, so no exact anchor was verified. |
| RWB-S2-E2026-APP | R-19191 | DOR-RWB-S2-E2026-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | The personal-data field and its guardrail row are in the section not supplied. No exact anchor was verified, so no edit was made. |
| RWB-S2-E2026-APP | R-26858 | CG-ALL-8419 | 12.5 | Criteria and tests keep legacy job and decision-log wording | AC8 and TC-E2-026-07/-16 lines are not in the supplied text. The L227 legacy list is not the cited line. No exact anchor, so no edit. |
| RWB-S2-E2027-APP | R-19201 | DOR-RWB-S2-E2027-APP-15 INVEST: Partial | 15 | Definition of Ready item 15 INVEST: Partial | Small row edit reverted: no two-week figure exists in the sources. Section 15 needs the next chunk for INVEST wording. |
| RWB-S2-E2032-APP | R-19217 | DOR-RWB-S2-E2032-APP-9 Messages: Partial | 14 | Definition of Ready item 9 Messages: Partial | No Error and Message Standard v4 file in the sources. MSG-P4-003 matched FSD P4 Access v3 VR-P4-011-1 at this step; it was later reworded under CG-ALL-8439. |
| RWB-S2-E2032-APP | R-26866 | CG-ALL-8443 | 12.5 | Criteria and tests keep legacy job and decision-log wording | TC-E2-032-06 and TC-E2-032-10 are in section 16, outside this chunk. Section 12.5 has no JOB-nn or decision-log wording. |
| RWB-S2-E2032-APP | R-28841 | GAP-1463 | 7 | RWB-E2-032 is conditional on a model existing and no decision row names who confirms it | Section 7 decision table is outside this chunk, so no DL row can be anchored. No date for the model answer is in the sources. |
| RWB-S2-E3001-APP | R-19219 | DOR-RWB-S2-E3001-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Personal-data fields flagged by detcheck (CG-ALL-8458) are not named in any source found; guardrail lines are not in the supplied text. Not specified in the source documents (DOR-RWB-S2-E3001-APP-11). |
| RWB-S2-E3001-CON | R-19231 | DOR-RWB-S2-E3001-CON-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Section 18 is not in this chunk, so DL10 cannot be closed. DL10 is a removed business decision; close it in section 18 once that text is provided. |
| RWB-S2-E3001-CON | R-19234 | DOR-RWB-S2-E3001-CON-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | AC and TC rows for BR1 to BR11 need sections 7 and 16, which are not in this chunk. Section 8 rows are present. Re-run with sections 7 and 16. |
| RWB-S2-E3001-CON | R-22398 | GAP-2691 | 12, 13 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Edit sits in sections 12 and 13, not in this chunk. The three operation and element names are in no source, so writing them would invent values. Re-run with sections 12 and 13. |
| RWB-S2-E3001-CON | R-22759 | GAP-2683 | 12 | The published shape of the release section, of the two release events, of the release vocabulary and of the view column contract has no source | Edit sits in section 12, not in this chunk. The release section, release events and release vocabulary have no source values. Re-run with section 12. |
| RWB-S2-E3001-CON | R-23363 | GAP-2685 | 12 | The published shape of the document-set section, of the set request and of the status vocabulary has no source | Edit sits in section 12, not in this chunk. The document-set section, set request and status vocabulary have no source values. Re-run with section 12. |
| RWB-S2-E3001-CON | R-32096 | NEWAC-RWB-S2-E3001-CON-AC8 | 7, 16 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so the AC8 scenario and its test row cannot be anchored. The proposed test has no value in the sources. Re-run with sections 7 and 16. |
| RWB-S2-E3002-APP | R-19240 | DOR-RWB-S2-E3002-APP-18 | 9 | Definition of Ready item 18 Open decisions: Partial | Section 9 text is not in this chunk, so there is no exact old text to edit. DL10 is open with no answer in Gap Register v1 (ASM-2863 is the assumption). |
| RWB-S2-E3003-APP | R-07676 | DOR-RWB-S2-E3003-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or 22/23 folders (grep). Sign-off would need an invented value. Needs the epic design record. |
| RWB-S2-E3003-APP | R-07679 | DOR-RWB-S2-E3003-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in 22 Microservice Realignment or 23 Document Gaps (grep). Citing one would invent it. |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (22)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16085 | RWB-S2-E2025-APP | CG-ALL-8382 | 2, 5, 11, 16 | Add field `party_names` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in the RWB-P5-E2025-APP type table. |
| CDC-16086 | RWB-S2-E2025-APP | CG-ALL-8383 | 2, 4, 11 | Add field `contract_amount` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in RWB-P5-E2025-APP. |
| CDC-16087 | RWB-S2-E2025-APP | CG-ALL-8384 | 2, 5 | Add field `approval_no` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in RWB-P5-E2025-APP. |
| CDC-16088 | RWB-S2-E2025-APP | CG-ALL-8385 | 2, 5 | Add field `approved_amount` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in RWB-P5-E2025-APP. |
| CDC-16089 | RWB-S2-E2025-APP | CG-ALL-8386 | 2, 5 | Add field `approval_date` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in RWB-P5-E2025-APP. |
| CDC-16090 | RWB-S2-E2025-APP | CG-ALL-8387 | 2, 4, 11 | Add field `mortgage_amount` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in the owning document. |
| CDC-16091 | RWB-S2-E2025-APP | CG-ALL-8388 | 2, 4, 11 | Add field `registration_date` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in the owning document. |
| CDC-16092 | RWB-S2-E2025-APP | CG-ALL-8389 | 2, 4, 11 | Add field `land_office` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in the owning document. |
| CDC-16093 | RWB-S2-E2025-APP | CG-ALL-8390 | 11 | Add field `source_document_id` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in the owning document. |
| CDC-16094 | RWB-S2-E2025-APP | CG-ALL-8391 | 11 | Add field `source_doc_version` to LDM v9 Fields or Data Classification v5 Fields, or record it as a named object in the owning document. |
| CDC-16097 | RWB-S2-E2025-APP | DOR-RWB-S2-E2025-APP-7 | 11 | Confirm DF-TRT-023 on treatment and add or confirm the names party_names, contract_amount, approval_no, approved_amount and seven more cited in section 11. |
| CDC-16115 | RWB-S2-E2026-APP | DOR-RWB-S2-E2026-APP-7 | 11 | Add treatment.contract_document_id (indexed) to the LDM v9 treatment entity; add decision_record as the local decision-record entity in LDM v9 and DC5. P3 legacy wording is open (text not supplied). |
| CDC-16117 | RWB-S2-E2026-APP | CG-ALL-8408 | 2, 4, 12.7 | Add decision_record as a dictionary field or entity, or record the decision record object in the owning document; the story names it at lines 62, 80 and 337. |
| CDC-16118 | RWB-S2-E2026-APP | CG-ALL-8409 | 11, 16 | Add transfer_price as a dictionary field or entity, or name the dictionary field used at line 260; the test row TC-E2-026-01 carries the legacy value. |
| CDC-16182 | RWB-S2-E2032-APP | DOR-RWB-S2-E2032-APP-7 | 11 | Add DF-ACC-009 to LDM v9; add decision_record as an entity or field in LDM v9 or Data Classification v5, or the story takes the LDM name |
| CDC-16238 | RWB-S2-E3002-APP | DOR-RWB-S2-E3002-APP-7 | 11 | Add decision_record as an entity of the library with fields DF-DEC-001 to DF-DEC-018; P3 wording is fixed under CG-ALL-8475. |
| CDC-16249 | RWB-S2-E3002-CON | DOR-RWB-S2-E3002-CON-7 | 11 | Register decision_record as an entity, or confirm it is out of model scope, so §11 cites a model element |
| CDC-16257 | RWB-S2-E3003-APP | CG-ALL-8485 | find it | Record price_below_floor as a reason-code value of P7 rwb-decision in the owning document, as it is not a field or entity. |
| CDC-16258 | RWB-S2-E3003-APP | CG-ALL-8486 | find it | Record below_floor_refused as a reason-code value of P7 rwb-decision in the owning document, as it is not a field or entity. |
| CDC-16259 | RWB-S2-E3003-APP | CG-ALL-8487 | 11 | Record decision_record in the owning document as the library object of RWB-PLT-E1027-CON in rwb_treatment, or use the dictionary name. |
| CDC-16260 | RWB-S2-E3003-APP | CG-ALL-8488 | 11 | Add approver_role as a treatment field in LDM v9 and Data Classification v5, or use the dictionary name. |
| CDC-16266 | RWB-S2-E3003-APP | DOR-RWB-S2-E3003-APP-7 | 11 | Add field or entity entries for treatment final_call, approver_role, decided_at, reason_code and decision_record, or list them as reference values; resolve the one further name in the detcheck. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16052 | RWB-S2-E2018-APP | CG-ALL-8371 | 12.5 | Add an Activities row for openSignatureWindow (type Activity, task queue rwb-treatment), or name a catalogued activity. |
| CDC-16053 | RWB-S2-E2018-APP | CG-ALL-8372 | 12.5 | Add an Activities row for recordSignatureResult on task queue rwb-treatment, or name a catalogued activity in section 12.5 of the story. |
| CDC-16054 | RWB-S2-E2018-APP | CG-ALL-8373 | 12.5 | Add an Activities row for closeSignatureWindow on task queue rwb-treatment, or name a catalogued activity in section 12.5 of the story. |
| CDC-16095 | RWB-S2-E2025-APP | CG-ALL-8398 | 12.5 | Add an Activities row for applyDocumentFacts on task queue rwb-treatment, with the input and output of RWB-S2-E2025-APP section 12.5. |
| CDC-16119 | RWB-S2-E2026-APP | CG-ALL-8414 | 12.5 | Add activity generateContractDocument on task queue rwb-treatment to the Activities sheet. |
| CDC-16120 | RWB-S2-E2026-APP | CG-ALL-8415 | 12.5 | Add activity recordAndApply on task queue rwb-treatment to the Activities sheet, with the RecordAndApply contract of the design. |
| CDC-16179 | RWB-S2-E2032-APP | CG-ALL-8437 | 12.5 | Add activity suggestTdrOffer to the Activities sheet on task queue rwb-treatment, with the input and output of section 12.5. |
| CDC-16180 | RWB-S2-E2032-APP | CG-ALL-8438 | 12.5 | Add activity recordSuggestion to the Activities sheet on task queue rwb-treatment, with its one-transaction contract of section 12.5. |
| CDC-16201 | RWB-S2-E3001-APP | CG-ALL-8455 | 12.5 | Add activity openTreatment on task queue rwb-treatment, with the TreatmentRequest in and the created Treatment and its ID out. |
| CDC-16202 | RWB-S2-E3001-APP | CG-ALL-8456 | 12.5 | Add activity recordAndApply on task queue rwb-treatment, writing the treatment row, local decision record, outbox rows and idempotency row in one transaction. |
| CDC-16227 | RWB-S2-E3002-APP | CG-ALL-8470 | 12.5 | Add a Workflows row for TreatmentWorkflow, settlement branch, task queue rwb-treatment, namespace rwb-recovery. |
| CDC-16233 | RWB-S2-E3002-APP | CG-ALL-8471 | 12.5 | Add activity buildSettlementOffer to the Activities sheet, or name a catalogued activity. |
| CDC-16234 | RWB-S2-E3002-APP | CG-ALL-8472 | 12.5 | Add activity checkFloor to the Activities sheet, or name a catalogued activity. |
| CDC-16235 | RWB-S2-E3002-APP | CG-ALL-8473 | 12.5 | Add activity recordAndApply to the Activities sheet, or name a catalogued activity. |
| CDC-16256 | RWB-S2-E3003-APP | DOR-RWB-S2-E3003-APP-8 | 12.5 | Add Activity checkFloor and the TreatmentWorkflow ID form and start rule, or align the story names. Task queue fixed under CG-ALL-8490. |
| CDC-16261 | RWB-S2-E3003-APP | CG-ALL-8492 | 12.5 | Add activity checkFloor on task queue rwb-treatment to the Activities sheet, or use a catalogued activity. |
| CDC-16262 | RWB-S2-E3003-APP | CG-ALL-8493 | 12.5 | Add activity requestSecondSignature on task queue rwb-treatment to the Activities sheet, or use a catalogued activity. |
| CDC-16263 | RWB-S2-E3003-APP | CG-ALL-8494 | 12.5 | Add activity recordAndApply on task queue rwb-treatment to the Activities sheet, or use a catalogued activity. |
| CDC-16264 | RWB-S2-E3003-APP | CG-ALL-8495 | 12.5 | Add activity publishApproved on task queue rwb-treatment to the Activities sheet, or use a catalogued activity. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16133 | RWB-S2-E2027-APP | CG-ALL-8425 | 12.1 | Add path GET /api/recovery/treatment/v1/treatments/{treatmentId} to the yaml, or the owner removes the operation. Story path is single-prefixed; no story edit. |
| CDC-16138 | RWB-S2-E2027-APP | DOR-RWB-S2-E2027-APP-8 | 12.1 | Add path GET /api/recovery/treatment/v1/treatments/{treatmentId} to the yaml, or the owner removes the operation. |
| CDC-16172 | RWB-S2-E2032-APP | CG-ALL-8432 | 12.1 | Publish the GET proposal read operation in rwb-treatment.yaml with its path, or remove it from section 12.1; the path is not specified in the source documents (GAP-1882). |
| CDC-16173 | RWB-S2-E2032-APP | CG-ALL-8433 | n/a | Remove the closed enum on proposedBy so LOV-PROPOSER values (AGENT, RULE, PERSON) are read as data with their version. |
| CDC-16174 | RWB-S2-E2032-APP | CG-ALL-8434 | n/a | Remove the closed enum on treatmentType so LOV-TREATMENT values are read as data with their version. |
| CDC-16177 | RWB-S2-E2032-APP | DOR-RWB-S2-E2032-APP-8 | n/a | Publish the proposal read operation and remove the closed enums on proposedBy and treatmentType, as CG-ALL-8432 to 8434 require. |
| CDC-16190 | RWB-S2-E3001-APP | CG-ALL-8449 | 3 | Remove the closed enum on approvalLevel so LOV-APPROVAL-LEVEL values are read as data without a code change. |
| CDC-16191 | RWB-S2-E3001-APP | CG-ALL-8450 | 3 | Remove the closed enum on proposedBy so LOV-PROPOSER values are read as data without a code change. |
| CDC-16192 | RWB-S2-E3001-APP | CG-ALL-8451 | 3 | Remove the closed enum on treatmentType so LOV-TREATMENT values are read as data without a code change. |
| CDC-16193 | RWB-S2-E3001-APP | CG-ALL-8452 | 3 | Remove the closed enum on outcome so LOV-TRT-OUTCOME values are read as data without a code change. |
| CDC-16194 | RWB-S2-E3001-APP | CG-ALL-8453 | 3 | Remove the closed enum on signatureStatus so LOV-TRT-SIGNATURE values are read as data without a code change. |
| CDC-16198 | RWB-S2-E3001-APP | DOR-RWB-S2-E3001-APP-8 | 12 | Hold approvalLevel, proposedBy, treatmentType and outcome as LOV references (LOV-APPROVAL-LEVEL, LOV-PROPOSER, LOV-TREATMENT, LOV-TRT-OUTCOME), not closed enums, and the four further fields flagged by detcheck (+4 more). |
| CDC-16226 | RWB-S2-E3002-APP | CG-ALL-8469 | 12.1 | Publish POST /treatments/{treatmentId}/offer in rwb-treatment.yaml, through RWB-S2-E3002-CON. |
| CDC-16242 | RWB-S2-E3002-CON | CG-ALL-8480 | 12.1 | Publish POST /api/recovery/treatment/v1/treatments/{treatmentId}/offer in rwb-treatment.yaml, as section 12.1 already states. |
| CDC-16243 | RWB-S2-E3002-CON | DOR-RWB-S2-E3002-CON-8 | 12.1 | Publish POST /api/recovery/treatment/v1/treatments/{treatmentId}/offer; PATCH stays without idempotency key per 12.1 and TSD S2 T-A.2 API-S2-003. |
| CDC-16255 | RWB-S2-E3003-APP | CG-ALL-8489 | 19 | Keep the outcome enum; LOV-TRT-OUTCOME is a closed list per Reference Data v5, so the yaml enum is correct. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16055 | RWB-S2-E2018-APP | CG-ALL-8374 | 16 | Add rows TC-S2-E2018-APP-01 to TC-S2-E2018-APP-04 to tab Story test cases, with Given, When and Then copied from AC1 to AC8. |
| CDC-16096 | RWB-S2-E2025-APP | CG-ALL-8399 | 16 | Add rows TC-S2-E2025-APP-01 to TC-S2-E2025-APP-04 to tab Story test cases, with Given, When and Then copied from AC1, AC4, AC5, AC6, AC7 and AC8. |
| CDC-16121 | RWB-S2-E2026-APP | CG-ALL-8416 | 16 | Add rows TC-S2-E2026-APP-01 to -04 with Given, When and Then copied from AC1, AC2 to AC3 and AC5, AC4 and AC6, and AC7 and AC8. |
| CDC-16123 | RWB-S2-E2026-APP | DOR-RWB-S2-E2026-APP-12 | 16 | Add rows TC-S2-E2026-APP-01 to TC-S2-E2026-APP-06 on tab Story test cases; align RTM v7 test lists with section 18. |
| CDC-16181 | RWB-S2-E2032-APP | CG-ALL-8440 | 16 | Add rows TC-S2-E2032-APP-01 to -04, and -05 and -06 added in section 16, with Given, When and Then copied from the criteria they cover. |
| CDC-16203 | RWB-S2-E3001-APP | CG-ALL-8457 | 16 | Add rows TC-E3-001-01 to TC-E3-001-06 to the Story test cases tab, with Given, When and Then copied from the criterion each one covers. |
| CDC-16213 | RWB-S2-E3001-CON | DOR-RWB-S2-E3001-CON-12 | 12.7, 16 | Register TC-S2-E3001-CON-01 to TC-S2-E3001-CON-05 and the new TC-S2-E3001-CON-06 and -07 |
| CDC-16222 | RWB-S2-E3001-CON | CG-ALL-8464 | 16 | Add rows TC-S2-E3001-CON-01 to TC-S2-E3001-CON-05 to Story test cases with Given, When and Then copied from the criteria they cover. |
| CDC-16236 | RWB-S2-E3002-APP | CG-ALL-8474 | 16 | Add rows TC-E3-002-01 to TC-E3-002-06 to tab Story test cases in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-16248 | RWB-S2-E3002-CON | DOR-RWB-S2-E3002-CON-12 | 16 | Add TC-S2-E3002-CON-01 to TC-S2-E3002-CON-06 with their section 16 covers and levels |
| CDC-16253 | RWB-S2-E3002-CON | CG-ALL-8481 | 16 | Add rows TC-S2-E3002-CON-01 to TC-S2-E3002-CON-05 with Given, When and Then copied from AC1 (01), AC2 (02), AC3 (03), AC4 and AC5 (04) and AC6 (05) of section 7. |
| CDC-16265 | RWB-S2-E3003-APP | CG-ALL-8496 | 16 | Add rows TC-E3-003-01 to TC-E3-003-06 with Given, When and Then copied from the criteria they cover. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16069 | RWB-S2-E2018-APP | GAP-2700 |  | Publish the record on the update operation of /api/recovery/treatment/v1, add the P6 to S2 cell, and note that a later Temporal move changes only the client. |
| CDC-16075 | RWB-S2-E2018-APP | GAP-1185 | find it | Publish no comms signature event; if a signature fact must travel, add it to rwb.treatment.events.v1 in a later catalogue revision, published by S2 rwb-treatment. |
| CDC-16102 | RWB-S2-E2025-APP | GAP-0068 | find it | Set rwb-litigation (S4) to wave 2 as in W-MAP. |
| CDC-16109 | RWB-S2-E2025-APP | GAP-1704 | 18 | Story keeps no document content in rwb_treatment; the architecture ownership change is not made in this story. |
| CDC-16143 | RWB-S2-E2027-APP | GAP-1626 | find it | Replace the slide 17 rwb-payment operations with the API Specification v4 pair GET /proceeds and POST /proceeds/{proceedsId}/match. |
| CDC-16187 | RWB-S2-E2032-APP | GAP-1883 | 4 | Add the suggestion operation of RWB-P10-E2032-CON to the rwb-agent inbound list on slide 16 at the architecture review before wave 2 closes. |
| CDC-16231 | RWB-S2-E3002-APP | GAP-1696 | 1 | Add S2 to the P1 REST cell of the connection matrix; confirm views are read only by rwb-source-data. |
| CDC-16244 | RWB-S2-E3002-CON | GAP-1696 |  | Add S2 to P1 REST cell; FSD S2 A2.6.3.1, A2.13.2, A2.10.2 and A2.17.2 obtain source facts via the rwb-source-data contract, not ACE views, ALS, CCMS, NLEADS. |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16050 | RWB-S2-E2018-APP | DOR-RWB-S2-E2018-APP-14 |  | Record the signed epic design sign-off for EP02. No signed epic design is in this story or the source documents; the sign-off is not specified in the source documents (DOR-RWB-S2-E2018-APP-14). |
| CDC-16081 | RWB-S2-E2025-APP | DOR-RWB-S2-E2025-APP-14 | n/a | Record the signed epic design sign-off against this story. |
| CDC-16135 | RWB-S2-E2027-APP | DOR-RWB-S2-E2027-APP-14 |  | Record the signed epic design sign-off for RWB-SVC-S2 in the epic design record. |
| CDC-16175 | RWB-S2-E2032-APP | DOR-RWB-S2-E2032-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S2 and confirm it against this story. |
| CDC-16195 | RWB-S2-E3001-APP | DOR-RWB-S2-E3001-APP-14 | header | Confirm the signed epic design sign-off for RWB-SVC-S2 is recorded there. |
| CDC-16209 | RWB-S2-E3001-CON | DOR-RWB-S2-E3001-CON-14 | find it | Record the signed epic design sign-off for EP03 and RWB-SVC-S2 in the epic design record |
| CDC-16228 | RWB-S2-E3002-APP | DOR-RWB-S2-E3002-APP-14 | 1 | Record the signed epic design sign-off for EP03 and link it to this story. |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16078 | RWB-S2-E2025-APP | CG-ALL-8393 | 12.2 | Declare the REST base /api/recovery/document/v1 for the document provider, as in the Document Index service table. |
| CDC-16079 | RWB-S2-E2025-APP | CG-ALL-8394 | 12.2 | Declare the REST base /api/recovery/case/v1 for the case provider, as in the Document Index service table. |
| CDC-16080 | RWB-S2-E2025-APP | CG-ALL-8395 | 12.2 | Declare the REST base /api/recovery/case/v1 for the reference-data read, as in the Document Index service table. |
| CDC-16126 | RWB-S2-E2026-APP | GAP-0938 | 12 | Add the authorise request and answer schema for POST /api/recovery/access/v1/authorise to the API specification and TSD P4 appendix T-A, publish with RWB-P4-E1037-CON, and stub the generation facts in RWB-P5-E2026-CON. |
| CDC-16132 | RWB-S2-E2026-APP | GAP-2394 | 13 | Allocate the next free API-P6-nnn ID at D1 and add POST /api/recovery/comms/v1/cases/{caseId}/generated-documents to the P6 API specification with the gateway-bff route. |

### RWB-P5-E2025-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16082 | RWB-S2-E2025-APP | DOR-RWB-S2-E2025-APP-21 | header | Header names RWB-P5-E2025-CON. Whether the contract is published is a P5 source fact, not a story edit. |
| CDC-16083 | RWB-S2-E2025-APP | DOR-RWB-S2-E2025-APP-22 | n/a | Publish the contract fake library version and record it as published. |
| CDC-16100 | RWB-S2-E2025-APP | GAP-1020 | find it | Publish the checked-fields read on /api/recovery/document/v1/cases/{caseId}/checked-fields with CheckedField and CheckedFieldSet shapes; apply DOCTYPE-2026.12 through the type table of RWB-P5-E1025-APP; keep EXTRACT_ACCURACY_PASS in document_hub_parameter. |
| CDC-16101 | RWB-S2-E2025-APP | GAP-1021 | find it | Declare one checked-fields read on the service base with its shape and status set; consume the three extraction operations from RWB-P5-E1053-CON without re-declaring them; keep the extraction event with new type codes in documentType. |
| CDC-16105 | RWB-S2-E2025-APP | GAP-1900 | Header | Publish one GET on the rwb-document base with case and document type parameters, CheckedField list answer, state filter and role masking; operation name and path Not specified in the source documents until baseline tag. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16098 | RWB-S2-E2025-APP | GAP-1713 | find it | Record the mapping of each prerequisite feature code to its owning service: approval to P7, case to P3, documents to P5, communications to P6, valuation to S1; FEAT-CHO-08 carried twice as written. |
| CDC-16150 | RWB-S2-E2027-APP | GAP-0260 |  | Mark the 13 field rows retired; set Owner to P3 rwb-case (retired table) and record the PAYMENT_MATCH rule package as P7 rwb-decision. |
| CDC-16165 | RWB-S2-E2027-APP | GAP-0218 |  | Record P7 rwb-decision as holder of the LOV-MATCH-TYPE codes and P8 rwb-payment as reader, carried as the match type column of PAYMENT_MATCH; the value rows are copied unchanged. |
| CDC-16205 | RWB-S2-E3001-APP | GAP-1698 | 11 | Add rows under rwb-treatment for contracts, settlement and deed-in-lieu agreements, and plan timers, alongside treatment. |
| CDC-16214 | RWB-S2-E3001-CON | GAP-1698 | find it | Add rows for the contracts, the settlement and deed-in-lieu agreements and the plan timers of rwb_treatment under S2, with key fields and no physical table name. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16111 | RWB-S2-E2026-APP | CG-ALL-8407 | 11 | Add field contract_document_id (document identifier, uuid) to treatment; installments_paid does not hold this meaning |
| CDC-16178 | RWB-S2-E2032-APP | CG-ALL-8431 | 12.7 | Record decision_record as the RWB-PLT-E1027-CON library table in rwb_treatment, or name the dictionary entity the story should use. |
| CDC-16199 | RWB-S2-E3001-APP | CG-ALL-8447 | 11 | Record decision_record as the local decision record table in schema rwb_treatment, defined by the RWB-PLT-E1027-CON DDL template (DP-03). |
| CDC-16200 | RWB-S2-E3001-APP | CG-ALL-8448 | 11 | Give DF-TRT-023 nleads_ref (varchar(30)) a row on the treatment entity, or confirm the correct ID; no story edit. |
| CDC-16204 | RWB-S2-E3001-APP | DOR-RWB-S2-E3001-APP-7 | 7, 11 | Add DF-TRT-023 to DF-TRT-026 as treatment fields (nleads_ref, credit_result, credit_result_reason, credit_result_at); add decision_record to LDM v9 and Data Classification v5. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16149 | RWB-S2-E2027-APP | GAP-2313 |  | Publish the rule-package and rule-version operations from RWB-P7-E2027-APP and RWB-P7-E2042-APP only; correct TSD P4 T-A.1 at the next version. |
| CDC-16152 | RWB-S2-E2027-APP | GAP-1290 |  | Carry legacy section 12 load and version-list shapes into the P7 API spec; add approve, rollback, dry-run detail and the governance decision code before the wave 2 contract freeze. |
| CDC-16153 | RWB-S2-E2027-APP | GAP-1293 |  | Use P7 rwb-decision with /admin/rule-packages and /admin/rule-package-versions on /api/recovery/decision/v1; keep /admin/rule-versions as legacy with no target story; correct the P4 attribution. |
| CDC-16223 | RWB-S2-E3001-CON | GAP-2690 | find it | Record the two treatment operations and the credit-result element set against rwb-treatment; level comparison against rwb-access; ledger ownership against rwb-decision; SCR-14 merge against the edge contract. |
| CDC-16254 | RWB-S2-E3002-CON | GAP-2690 | 8 | Record the two rwb-treatment operations and the credit-result element set against rwb-treatment; the level comparison and delegation version against rwb-access and the caller; one ledger entry per record and its sealing order against rwb-decision; the SCR-14 merge against the edge contract. Confirm the split when P2 and P3 publish. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16072 | RWB-S2-E2018-APP | CG-ALL-8375 | 18 | Align the REQ-OCC-009 test list in RTM v7 with section 18 of this story (TC-E2-018-01 to TC-E2-018-12, TC-S2-E2018-APP-01 to TC-S2-E2018-APP-07) at its next version. |
| CDC-16108 | RWB-S2-E2025-APP | CG-ALL-8400 | 18 | Align the test-case lists for REQ-DCM-006 and REQ-DCM-005 with section 18 of RWB-S2-E2025-APP in the next RTM version. |
| CDC-16131 | RWB-S2-E2026-APP | CG-ALL-8417 | 18 | In the next RTM version, align the REQ-DCM-012 and REQ-OCC-002 test lists with section 18 of RWB-S2-E2026-APP. |
| CDC-16189 | RWB-S2-E2032-APP | CG-ALL-8441 | 18 | Align the test lists for REQ-CHO-006 and REQ-DRI-001 with section 18 of RWB-S2-E2032-APP in the next RTM version. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16122 | RWB-S2-E2026-APP | DOR-RWB-S2-E2026-APP-1 | 1 | Add role RW-RESTRUCT with name restructuring officer (FCR), as used in the RW-RESTRUCT row of the story, so section 1 resolves to a listed role. |
| CDC-16211 | RWB-S2-E3001-CON | DOR-RWB-S2-E3001-CON-1 | 1 | Add role 'service contract owner' as a role code or role name |
| CDC-16237 | RWB-S2-E3002-APP | DOR-RWB-S2-E3002-APP-1 | 1 | Add or map role RW-RESTRUCT, restructuring officer (FCR), so the role name and code match section 5. |
| CDC-16247 | RWB-S2-E3002-CON | DOR-RWB-S2-E3002-CON-1 | 1 | Add a role for the contract owner of rwb-treatment, or name the existing role code, so the section 1 role resolves. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16048 | RWB-S2-E2018-APP | CG-ALL-8367 | 12.3 | Add event type rwb.treatment.SignatureRecorded.v1 to the Events sheet. |
| CDC-16049 | RWB-S2-E2018-APP | CG-ALL-8368 | 12.3 | Add event type rwb.treatment.SignatureWindowClosed.v1 to the Events sheet. |
| CDC-16113 | RWB-S2-E2026-APP | CG-ALL-8411 | 12.3 | Add event type rwb.treatment.ContractDocumentGenerated.v1 on rwb.treatment.events.v1 to the Events sheet |

### RWB-S4-E2025-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16106 | RWB-S2-E2025-APP | GAP-2835 | Header | Add source_document_id, source_doc_version, source_table_version and apply key to legal_action; map only same-name codes; record the twelve unmapped codes as the difference in the apply result. |
| CDC-16107 | RWB-S2-E2025-APP | GAP-2836 | Header | One hearing per legal action and hearing_date; hearing_type left empty pending litigation BA confirm; closed or withdrawn action answers 409 with baseline conflict message. |
| CDC-16110 | RWB-S2-E2025-APP | GAP-1904 | 15 | Wave 2 release kept. SCR-19 belongs to the S4 story, which holds the litigation workspace. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16134 | RWB-S2-E2027-APP | CG-ALL-8426 | 13 | Create story RWB-P7-E1073-CON (rules fake: version in force, NoPackageInForce) or name the existing story that carries that capability. |
| CDC-16136 | RWB-S2-E2027-APP | DOR-RWB-S2-E2027-APP-17 | header | Create story RWB-P7-E1073-CON or name the existing story that the dependency on the rules capability should point to. |
| CDC-16137 | RWB-S2-E2027-APP | DOR-RWB-S2-E2027-APP-21 | header | Create contract story RWB-S2-E2027-CON, or confirm RWB-S2-E3001-CON as this story's contract. |

### RWB-P8-E2027-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16147 | RWB-S2-E2027-APP | GAP-3180 | find it | Carry the confirmed match order EXACT, then PARTIAL, then WINDOW in the PAYMENT_MATCH scenario set so one order is tested. |
| CDC-16148 | RWB-S2-E2027-APP | GAP-2506 |  | Keep the slice as written; add C RWB-P7-E1073-CON to the C row in D1; publish row order as the target name, with priority as its legacy and TSD name; reconcile PMT-2026.12 to one version row. |
| CDC-16154 | RWB-S2-E2027-APP | GAP-1355 |  | Read AC6 through the rwb-decision contract mock, keep legacy steps verbatim, and add C RWB-P7-E1073-CON to the C row in D1. |

### RWB-P8-E2027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16155 | RWB-S2-E2027-APP | GAP-1359 |  | Publish the result as packageCode, versionInForce, ruleId, rowOrder and outputs; mark the two unnamed operation names as placeholders; rwb-decision confirms in RWB-P7-E1073-CON. |
| CDC-16156 | RWB-S2-E2027-APP | GAP-1360 |  | Publish the payload field lists of TreatmentBooked, PaymentMissed and ProceedsMatched in the AsyncAPI fragment as a marked working read; confirm with the named consumers. |
| CDC-16160 | RWB-S2-E2027-APP | GAP-2705 | 13 | Publish one read returning, for a case, a plan and a business date, the payment code, installment due date, match type, rule ID, package code and version and shortfall; name the payload members at major version 1. |

### RWB-P5-E2017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16057 | RWB-S2-E2018-APP | GAP-1182 | find it | Publish create, read-by-external-reference and update operations for signature_request before the wave 2 exit |
| CDC-16060 | RWB-S2-E2018-APP | GAP-1186 | find it | Publish whether the version add takes the signed PDF bytes or returns an upload link, so rwb-comms can stream the PDF without persisting it |

### RWB-P6-E2018-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16065 | RWB-S2-E2018-APP | GAP-1596 |  | Own the signature-request operation and flow: create the request through P5's contract, apply the signature basis rule, receive the result and call rwb-treatment. P5 stores request, status and signed copy. Confirm request-status read path with P5 before wave 2. |
| CDC-16071 | RWB-S2-E2018-APP | GAP-1196 |  | Add DP-03 and H RWB-PLT-E1027-CON to the slice pattern set, or confirm the platform release train delivers the decision-record library. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16076 | RWB-S2-E2018-APP | GAP-2355 | find it | Keep DocumentStored as the only event of this story; confirm with rwb-reporting whether a signature fact is needed and, if so, allocate a new DP-09 story with a CloudEvents payload of IDs and facts only. |
| CDC-16167 | RWB-S2-E2027-APP | GAP-1358 |  | Declare DecisionRecorded read only for the ledger acknowledgement of a local record, with no second writer; confirm the consumer list with the event catalogue owner. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16077 | RWB-S2-E2018-APP | GAP-2357 | find it | Add a rwb-document message for a closed signature request, with MSG-P3-005 kept until then; confirm Documents C, R and U as the operation-level rights of the five request operations. |
| CDC-16104 | RWB-S2-E2025-APP | GAP-1022 | find it | Ship operating values as environment placeholders; bind the model route endpoint and client credential as a secret reference; verify the OCR endpoint without replacing it; name the two alert identifiers. |

### OTHER:FSD P8 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16142 | RWB-S2-E2027-APP | GAP-1625 | find it | Confirm or replace the PRD-written criteria for AC-P8-003-01 to AC-P8-011-01 before wave 3 system test. |
| CDC-16144 | RWB-S2-E2027-APP | GAP-1631 | find it | Replace ATS, AMIS, LED and direct ALS/GL points with rwb-source-data reads and rwb-integration postings; keep auto-debit and LED routes outside the 19 services. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2027 APP  (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16169 | RWB-S2-E2027-APP | GAP-2311 | access profile section of the P4 story (not in this story) | Take matrix versions PM-2026.11 and PM-2026.12 and areas WRITE_OFF_AND_POSTING and RULES_AND_PARAMETERS from P4 FSD and TSD. Keep legacy letters CRUA, RA, C and A. Record SY-AGENT letters and database login name as open, to confirm with the security administrator before wave 2 test set sign-off. |
| CDC-16170 | RWB-S2-E2027-APP | GAP-2314 | 7 and 16 (in the P4 story) | Keep the acs list empty; accept the seven new access criteria (new, D-RCV-60) as the authority evidence of REQ-CHO-009; add no legacy access criterion; keep TC-E2-027-01 to TC-E2-027-13 run under the access profile. |

### RWB-P10-E2032-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16184 | RWB-S2-E2032-APP | GAP-0634 | find it | Fix the operation under /api/recovery/agent/v1 with three request members and eight answer members; map timeout, 4xx, 5xx and schema failure to TIMED_OUT, MODEL_ERROR and GUARDRAIL_FAILED; declare EV-28 payload from TSD P10 v2 T3.1; declare admin reads from RWB-P10-E1058-CON |
| CDC-16185 | RWB-S2-E2032-APP | GAP-0633 | find it | Fix operation path under /api/recovery/agent/v1; read account and payments via rwb-source-data and treatment via rwb-treatment on RWB-P3-E2004-CON; parameters and lists via rwb-case contracts; suggestion call 60 s, other hops 2 s; agent_version null |

### RWB-S2-E3001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16196 | RWB-S2-E3001-APP | DOR-RWB-S2-E3001-APP-21 | header | Set build status to Done once the contract is published. |
| CDC-16197 | RWB-S2-E3001-APP | DOR-RWB-S2-E3001-APP-22 | header | Publish the contract fake library and record its version. |

### OTHER:Functional Specification Document S2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16206 | RWB-S2-E3001-APP | GAP-1708 |  | Replace the placeholder criteria of A2.1.4.1 to A2.18.4.1 with criteria written from each step, rule and field; name alternate flows and background events. |
| CDC-16208 | RWB-S2-E3001-APP | GAP-1715 |  | Supply the change notes for versions 1 and 2 at the next FSD version; read the repeated FEAT-CHO-08 in A1.1 as one dependency. |

### RWB-PLT-E1027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16210 | RWB-S2-E3001-CON | CG-ALL-8463 | 12.7 | Record decision_record as the PLT library object applied in rwb_treatment, with its shape; no LDM v9 or Data Classification v5 field of that name |
| CDC-16232 | RWB-S2-E3002-APP | CG-ALL-8468 | 12.7 | Record decision_record as the library object of RWB-PLT-E1027-CON, or give it its LDM v9 or Data Classification v5 name. |

### OTHER:FSD S2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16216 | RWB-S2-E3001-CON | GAP-1712 | find it | Add field catalogs for the contract, agreement, plan timer and booking reference, with the physical field list left open to the data architect. |
| CDC-16217 | RWB-S2-E3001-CON | GAP-1702 | find it | Replace the completed ACE batch triggers with TreatmentWorkflow steps started by rwb-case and by owner-service events. Add no Schedule or batch trigger. |

### RWB-S2-E3002-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16229 | RWB-S2-E3002-APP | DOR-RWB-S2-E3002-APP-21 | 1 | Bring RWB-S2-E3002-CON to Done with the contract published. |
| CDC-16240 | RWB-S2-E3002-APP | GAP-1870 | 7 | Publish the working read of ASM-B-S2-01-E3002-1 and confirm it with the S1 owner of FEAT-VAL-06 at the wave 2 contract freeze. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16051 | RWB-S2-E2018-APP | DOR-RWB-S2-E2018-APP-8 | 13 | API yaml: signatureStatus enum must match LOV-TRT-SIGNATURE. Kafka Catalog v1: add rwb.treatment.SignatureRecorded.v1 and rwb.treatment.SignatureWindowClosed.v1. Temporal Catalog v1: align TreatmentWorkflow task queue and namespace. |

### OTHER:rwb-treatment service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16056 | RWB-S2-E2018-APP | GAP-1713 | find it | Map each prerequisite FEAT code to its owning service contract (P7 approval, P3 case, P5 documents, P6 communications, S1 valuation) and carry FEAT-CHO-08 twice as written |

### OTHER:work plan (rwb-treatment contract stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16058 | RWB-S2-E2018-APP | GAP-1183 | find it | Add an rwb-treatment contract story publishing the signature record operation and its field names on /api/recovery/treatment/v1 in wave 2 |

### RWB-P5-E1024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16059 | RWB-S2-E2018-APP | GAP-2356 | find it | Settle the container, WORM tier, object size limit, transfer path and refusal reporting for the signed PDF, carried as configuration rows of rwb.document.esign |

### OTHER:wave 2 e-signature harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16061 | RWB-S2-E2018-APP | GAP-0402 | find it | Specify the EasyApp test tenant and route via INT-34, the signed-PDF fixture, SIT hosts, seeding, evidence format and pass/fail gate with ACE and QA |

### OTHER:TSD P6 v2 integration inventory (T5.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16062 | RWB-S2-E2018-APP | GAP-1187 | find it | Add INT-34 with its request and result shape and endpoint, and certificate issuer, with endpoint and certificate as secret references under NFR-052 |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:P3 expiry story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16063 | RWB-S2-E2018-APP | GAP-1188 |  | Add the cancel as a fourth operation on /api/recovery/comms/v1 for P3, or a P3 event that P6 consumes, and name it in the P3 expiry story. |

### OTHER:FSD P5 Document hub v3; OTHER:PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16064 | RWB-S2-E2018-APP | GAP-1589 |  | Add the signature request as a document event and a metadata row, and carry the missing requirement text as OQ-P5-13. |

### OTHER:TSD P5 Document hub v2 Appendix T-A.1; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16066 | RWB-S2-E2018-APP | GAP-2352 |  | Add the five signature-request operations with API IDs and this story's paths; settle query names for the list and the external-reference read with rwb-comms. |

### OTHER:TSD P5 Document hub v2 T3.1; OTHER:rwb_document.sql; OTHER:TSD P6 Communications v2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16067 | RWB-S2-E2018-APP | GAP-2353 |  | Add signature_request with columns, constraints and indexes in P5 T3.1 and rwb_document.sql; remove it from P6 T3.1 at the next version. |

### OTHER:TSD S2 v2 T3.1; OTHER:FSD S2 A2.7 to A2.9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16068 | RWB-S2-E2018-APP | GAP-2699 |  | Specify the five nullable signature columns and two indexes, the update operation's additive properties, the two event names, the list codes and the window closure callback. |

### RWB-P5-E2018-APP; OTHER:rwb-document contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16070 | RWB-S2-E2018-APP | GAP-3182 |  | Move the V2_018 signature_request DDL to the rwb_document sequence and publish the request and result operations on the rwb-document contract. |

### OTHER:Functional Specification S2 (A2.18.2 and A2.15.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16073 | RWB-S2-E2018-APP | GAP-1704 | find it | Replace 'the Workbench document hub' with rwb-document reached through the P5 and P6 contracts; the treatment holds the document reference and rwb_treatment holds no document content. |

### OTHER:split_plan.json (RWB-E2-018 slices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16074 | RWB-S2-E2018-APP | GAP-1184 | find it | Record section 12.1 of RWB-S2-E2018-APP as the contract baseline for the three signature-request operations until RWB-P6-E2018-CON exists. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16084 | RWB-S2-E2025-APP | DOR-RWB-S2-E2025-APP-8 | 12.5 | P1 contract paths depend on CG-ALL-8393 to 8396; P2 workflow ID recorded as not specified (CG-ALL-8397). The +1 more is not in this chunk. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16099 | RWB-S2-E2025-APP | GAP-3194 | find it | Raise an ACE DB story for the source-column drop of rwb-treatment and cite it on row 121 before wave 2 starts. |

### OTHER:Extraction harness pack (QA; OTHER:P5 and P10 owners) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16103 | RWB-S2-E2025-APP | GAP-0407 | find it | Agree the classifier version, masked sample pack and extraction report with P5 and P10 owners; agree the wave 2 SIT seeding of DOCTYPE-2026.12 and the evidence format with QA. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16112 | RWB-S2-E2026-APP | CG-ALL-8410 | 12.2 | Publish POST /api/recovery/document/v1/cases/{caseId}/generated-documents (API-P5-016) with its operation identifier through RWB-P5-E2026-CON |

### RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16114 | RWB-S2-E2026-APP | DOR-RWB-S2-E2026-APP-22 | header | Record the published fake library version the story builds against |

### RWB-P5-E2026-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16116 | RWB-S2-E2026-APP | DOR-RWB-S2-E2026-APP-8 | 12.2 | Publish operation identifier for POST cases/{caseId}/generated-documents (API-P5-016); add event rwb.treatment.ContractDocumentGenerated.v1 to Kafka Catalog v1; align task queue rwb-treatment and namespace rwb-recovery with the catalog. |

### OTHER:TSD P5 v2 (T3.1 document table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16124 | RWB-S2-E2026-APP | GAP-1023 | header, 7, 13 | Add template_code varchar(30) and template_version integer beside template_id and treatment_id; build the partial unique index on (treatment_id, template_id) where state is DRAFT and is_active; record slide 16 path as losing (ASM-101). |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16125 | RWB-S2-E2026-APP | GAP-1580 | 18 | Add a generation section for REQ-DCM-012 with FR-P5-026 and AC-P5-019 in its next version. |

### RWB-ITG-E2026-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16127 | RWB-S2-E2026-APP | GAP-0408 | 16 | Agree the template fixtures, PDF/A-2b check and Thai font pack with the P6 and P5 owners; agree the wave 2 harness pack, seeding and evidence format with QA. |

### OTHER:PM-2026.12 policy pack load (TSD P4 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16128 | RWB-S2-E2026-APP | GAP-0937 | 9 | Add DOCUMENTS letters: C for RW-RESTRUCT, RW-CASEOWN and SY-CASEWF; R for RW-TEAMMGR; no row for RW-PHONECOL. Confirm at the policy pack review. |

### OTHER:PM-2026.12 policy pack and the reference data load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16129 | RWB-S2-E2026-APP | GAP-0939 | 9 | Add the SY-CASEWF role row with role_class NON_HUMAN_ACTOR, DOCUMENTS C and default_scope ALL; record it in the reference data load with its own approver. |

### RWB-P5-E2026-CON; OTHER:TSD P6 T-A; OTHER:rwb_comms V-baseline migration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16130 | RWB-S2-E2026-APP | GAP-2393 | 7 | Keep the request key and request lock in a rwb_comms table added by the V-baseline migration; record the rwb-document create operation in the P6 API specification when RWB-P5-E2026-CON is written. |

### OTHER:rwb-case route decision reason list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16139 | RWB-S2-E2027-APP | CG-ALL-8424 | find it | Record reason value broken_plan as a route-decision reason in its owning document; it is a reason code, not an LDM v9 or Data Classification v5 field. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16140 | RWB-S2-E2027-APP | DOR-RWB-S2-E2027-APP-11 | find it | Confirm the personal-data class of the P2 fields the detcheck flags; keep the no-personal-data statement for the decision record (DP-03) unless those fields are carried. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16141 | RWB-S2-E2027-APP | GAP-2395 | find it | Settle the rwb-comms package assignment with the rule registry owner before integration; no fourth package code invented. Not a change to this rwb-treatment story. |

### RWB-P7-E2027-APP; RWB-P3-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16145 | RWB-S2-E2027-APP | GAP-1292 | find it | Reconcile PM-2026.12 (2026-12-01) and PMT-2026.12 (2026-12-15) into one PAYMENT_MATCH label and valid-from date before SIT promotion. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16146 | RWB-S2-E2027-APP | GAP-1297 | find it | Raise one reconciliation with the RWB-E2-027 owner so that one PAYMENT_MATCH package code holds one version row before SIT. |

### OTHER:Test harness pack and rule-version load route (wave 2 harness pack) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16151 | RWB-S2-E2027-APP | GAP-0409 |  | Agree the ALS fixture, JOB-07 window control and rule-version load route with P8 and P7 owners; the harness pack, seeding and evidence format with QA. |

### OTHER:Operations values files (three values files) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16157 | RWB-S2-E2027-APP | GAP-1361 |  | Expose every numeric operations value as a chart value with a placeholder; close the values with the DL11 decisions before UAT. |

### OTHER:Contract baseline of rwb-decision, rwb-treatment and the shared event owners (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16158 | RWB-S2-E2027-APP | GAP-2507 | 13 | Publish RuleResult as packageCode, versionInForce, ruleId, rowOrder and outputs with NoPackageInForce; name the version-in-force read and the treatment installment-paid operation as placeholders; publish the three payload field lists; declare DecisionRecorded read-only on the shared topic with no second writer. |

### OTHER:Platform secret-store catalogue and the chart values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16159 | RWB-S2-E2027-APP | GAP-2508 | 13 | Record the names of the rwb-payment login, Kafka client credential, Temporal mTLS material, registry certificate and workload identity by role; expose numeric operations values as chart values; close DL11 before UAT. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16161 | RWB-S2-E2027-APP | GAP-1291 | 13 | Record H RWB-PLT-E1027-CON, H RWB-PLT-E1072-CON, C RWB-P7-E1073-CON, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1047-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON as non-blocking, built against fakes. |

### OTHER:FSD P8 v3 (Requirements served table) and TSD P8 v2 section T8 (Requirement traceability) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16162 | RWB-S2-E2027-APP | GAP-1624 |  | Fill the REQ ID data rows in both tables with the traced requirement IDs, or state that P8 has no requirement ID of its own. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16163 | RWB-S2-E2027-APP | GAP-1639 |  | Name the event-started workflows after their activities (matchPayments, confirmBookings), register them on task queue rwb-payment, and add a P8 row to the workflows sheet. |

### OTHER:rwb-decision version register (PAYMENT_MATCH package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16164 | RWB-S2-E2027-APP | GAP-1357 |  | Keep PM-2026.12 as the single version in force from 2026-12-01 and reconcile the PMT-2026.12 label to one version row before SIT. |

### OTHER:rwb-decision (rule_row catalogue and evaluation result) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16166 | RWB-S2-E2027-APP | GAP-1356 |  | Publish one name for the ordering column: row order as the target name, with priority recorded as its legacy and TSD name. |

### OTHER:Platform secret-store catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16168 | RWB-S2-E2027-APP | GAP-1362 |  | Record the names of the rwb-payment login, Kafka client credential, Temporal mTLS material, registry certificate and workload identity; reference them by role in the chart. |

### OTHER:Rule package registry in P7 rwb-decision (rule package load endpoints) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16171 | RWB-S2-E2027-APP | GAP-3188 |  | Move the load of rule packages to rwb-decision endpoints; keep the P4 reference load endpoint only for reference data that is not a rule package. |

### OTHER:Recovery Workbench story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16176 | RWB-S2-E2032-APP | DOR-RWB-S2-E2032-APP-21 | header | Create contract story RWB-S2-E2032-CON and link it as a contract dependency of RWB-S2-E2032-APP. |

### OTHER:Service contract of rwb-treatment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16183 | RWB-S2-E2032-APP | GAP-1713 | find it | Map each FEAT code to its owning service contract once: approval to P7, case to P3, documents to P5, communications to P6, valuation to S1; carry FEAT-CHO-08 as written |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-P10-E2032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16186 | RWB-S2-E2032-APP | GAP-0414 | find it | Agree one one-hop REST operation on the rwb-agent contract that starts a TDR suggestion run; add the S2 Treatment call to P10 on slide 13; QA lead fixes harness environment, stub controls, evidence format and gate at wave 2 entry |

### RWB-P10-E2032-CON; OTHER:T-A.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16188 | RWB-S2-E2032-APP | GAP-2403 | 12.1 | Agree the append request and answer, the two reads, LOV-DECISION value D5, final-call list with SUGGESTION_RECORDED, reference-data path, MSG-P7-009 text and rwb-decision login name. |

### OTHER:Message catalogue of the owning service and DL10 register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16207 | RWB-S2-E3001-APP | GAP-1710 |  | Serve MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 from their owners; hold MSG-S2-001 with Thai and English versions; Thai wording Not specified in the source documents. |

### OTHER:Screen specification of SCR-14 and SCR-15 (owning UI story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16212 | RWB-S2-E3001-CON | DOR-RWB-S2-E3001-CON-10 | find it | Add empty, loading, error and no access states to SCR-14 and SCR-15 |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16215 | RWB-S2-E3001-CON | GAP-1709 | find it | State the wave 2 slice (contract and treatment record with data date) and the E3 slice (offer, settlement, plan, deed in lieu). Header release is not changed. |

### RWB-S2-E3017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16218 | RWB-S2-E3001-CON | GAP-2682 | find it | Carry the release answer as an optional collateralRelease section of the treatment read; release facts as ACE read values; instruction as rwb.treatment.CollateralReleaseRequested.v1; confirmation via the same ACE read; parent CaseWorkflow moves the case. |

### RWB-S2-E3001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16219 | RWB-S2-E3001-CON | GAP-1869 | find it | Apply the camelCase Treatment and TreatmentRequest elements after DF-TRT-001 to DF-TRT-033, treatment as the only table, stage outcome to CaseWorkflow, decision code from the evaluated package; confirm at wave 2 freeze. |

### OTHER:FSD S2 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16220 | RWB-S2-E3001-CON | GAP-1708 | find it | The FSD owner replaces the placeholder acceptance criteria at the next FSD version, naming the alternate flows and background events of the module. |

### RWB-S2-E3014-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16221 | RWB-S2-E3001-CON | GAP-2677 | find it | Publish AssetUnlock with inspectionOutcome, unlockDecision, unlockDecidedAt, assetRef, ruleId and ruleVersion as a component of the treatment representation; no unlock or release event declared. |

### OTHER:rwb-treatment (S2) message catalogue; OTHER:catalogues of P1; OTHER:P4; OTHER:P7 and general (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16224 | RWB-S2-E3001-CON | GAP-1710 | 5 | Hold MSG-S2-001 with Thai and English versions; serve MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 from their owning catalogues; route both versions through DL10 before wave 3 release. |

### OTHER:FSD S2 (version 3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16225 | RWB-S2-E3001-CON | GAP-1715 | 1 | At the next FSD version, supply the change notes of versions 1 and 2 and read the repeated FEAT-CHO-08 in A1.1 as one dependency. |

### OTHER:contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16230 | RWB-S2-E3002-APP | DOR-RWB-S2-E3002-APP-22 | 1 | Publish a fake library version for RWB-S2-E3002-CON and record its version. |

### OTHER:rwb-decision rule package register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16239 | RWB-S2-E3002-APP | GAP-1707 | 7 | Name the package codes, labels and owners of RESTRUCTURE, PAYMENT_MATCH, BOOKING_MATCH and SETTLEMENT before wave 3 release. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16241 | RWB-S2-E3002-APP | GAP-1871 | 7 | Record POST /treatments/{treatmentId}/submit as superseded and confirm /offer with the solution architect at the wave 2 contract freeze. |

### OTHER:PO and solution architect (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16245 | RWB-S2-E3002-CON | GAP-1479 |  | Contract dependencies row reworded to Not specified in the source documents (GAP-1479); no valuation contract named |

### RWB-PLT-E1027-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16246 | RWB-S2-E3002-CON | CG-ALL-8479 |  | Record decision_record as the decision-record library object in the owning document, or use the dictionary name for it. |

### OTHER:rwb-decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16250 | RWB-S2-E3002-CON | GAP-1707 | none | Name the package codes, version labels and owners for RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH; record package and rule version on every treatment before wave 3 release |

### OTHER:S1 owner of FEAT-VAL-06 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16251 | RWB-S2-E3002-CON | GAP-1870 | 11 | Working read published in §11; rwb-case source removed; range and floor cited as AC2 context facts |

### RWB-S2-E3007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16252 | RWB-S2-E3002-CON | GAP-2659 | 11 | Publish the OfferRelease and EV-10 bodies as the working read of ASM-B2-S2-002-4; the release rides POST /treatments/{treatmentId}/offer |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16267 | RWB-S2-E3003-APP | GAP-1872 | 7; 8 | Target reading states the TreatmentApproved payload fields as the working read of ASM-3068; section 8 keeps the outcome-column gap open. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0068 | Wave conflict S4 / EP02 | Tech lead | Resolved (directive) |
| GAP-0218 | LOV-MATCH-TYPE is used by payment_match_rule, a table the target drops and the Ownership Map does not carry | Center of excellence | Resolved (directive) |
| GAP-0260 | payment_match_rule is in the inventory but not in the Ownership Map, and D-RCV-36 retires it as a table | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0402 | The e-signature harness pack and the EasyApp test route are not specified | Integration lead | Resolved (directive) |
| GAP-0407 | The extraction harness pack, the classifier version and the cross-service reader pack are not specified | Integration lead | Resolved (directive) |
| GAP-0408 | The generation harness pack, the template fixtures and the PDF/A conformance check are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0409 | The payment-matching harness pack, the ALS payment fixture and the rule-version load route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0414 | The TDR suggestion has no agreed start operation: the legacy treatment side calls rwb-agent in process, Architecture v5 gives no S2-to-P10 call, and no source gives the harness environment, the TDR model stub controls, the evidence format or the gate | Integration lead | Resolved (directive) |
| GAP-0633 | The TDR offer-suggestion slice in rwb-agent: the operation path below the base, the treatment and account read operations, the parameter keys, the screen route, the run version fields, the inputs reference and the two waits of the call are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-treatment, rwb-case and rwb-decision | Resolved (directive) |
| GAP-0634 | The TDR offer-suggestion contract slice: the operation path and request members, the record member types, the boundary answer and error mapping, the admin read route and the two-wait exception are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-decision, rwb-treatment, rwb-case and rwb-source-data | Resolved (directive) |
| GAP-0635 | The infrastructure slice of the TDR offer-suggestion key: the INT-23 host, port, certificate and Key Vault names, the partition and retention values, the sizing, the budget measurement points and the alarm thresholds are not specified by any source | SCB IT infrastructure with the ACE platform team and security | Resolved (directive) |
| GAP-0937 | The Documents letters per role are not in the P4 RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0938 | The authorise request and answer for a document generation request are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0939 | The role row, class and scope of the SY-CASEWF service identity are not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1020 | The checked-field reader, its operation and its field-level names are absent from every source, the five new types and the pass mark are an assumed load, and the case read of the scope check is in no C row | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1021 | The published Java reader becomes a REST contract no source names, the extraction operations belong to another baseline of the same service, and the plan lists no C row for the case read | Tech lead | Resolved (directive) |
| GAP-1022 | The deployment values of the extension are not specified: the model name and the provider product behind the agent route, the alert thresholds and identifiers, the evaluation cadence, the business-hours window and the reader thresholds | DevOps team | Resolved (directive) |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1024 | The generation contract baseline has no settled operation name, no published provider shapes and two consumed contracts outside the plan | Solution architect | Resolved (directive) |
| GAP-1181 | signature_request is defined in TSD P6 but is owned by P5 rwb-document | Solution architect | Resolved (directive) |
| GAP-1182 | The published P5 document names no operation to create, read by external reference or update a signature request | Solution architect | Resolved (directive) |
| GAP-1183 | No rwb-treatment contract story is in the plan, although the story reads the treatment and writes its signature record | Solution architect | Resolved (directive) |
| GAP-1184 | The plan holds no RWB-P6-E2018-CON, so the three signature-request operations have no published contract story | Solution architect | Resolved (directive) |
| GAP-1185 | The Architecture v5 event catalogue carries no comms signature event | Solution architect | Resolved (directive) |
| GAP-1186 | The signed PDF object and the byte transfer into the P5 write-once store are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1187 | The ACE common module e-signature path (INT-34) is not in the integration inventory and its shape, endpoint and certificate are unknown | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1188 | P3's cancel on offer expiry has no operation in the target catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1196 | DP-03 and its decision-record library are missing from the pattern set and the build list of the e-signature key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1289 | Where the generation record is written, and whether its failure stops the generation, is read two ways | Solution architect, with the platform team and the P7 rwb-decision owner | Resolved (directive) |
| GAP-1290 | PAYMENT_MATCH registry governance: shapes, decision-record payload, message set and promotion and rollback semantics are not specified | Solution architect, with the P7 business analyst and the rule owner RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1292 | PAYMENT_MATCH version label and valid-from date conflict between RWB-E2-027 and RWB-E2-042 | Rule owner RW-COE, with the P7 and P3 solution architects | Resolved (directive) |
| GAP-1293 | The rule-package operations: the legacy P4 attribution and the /admin/rule-versions paths against P7 and /admin/rule-package-versions | P7 solution architect, with the API specification owner | Resolved (directive) |
| GAP-1297 | PAYMENT_MATCH is labelled PMT-2026.12 from 2026-12-15 in this key and PM-2026.12 from 2026-12-01 in RWB-E2-027 | Business analyst | Resolved (directive) |
| GAP-1355 | The AC6 package load and the rule-evaluation contract have no C row in this key | Solution architect | Resolved (directive) |
| GAP-1356 | The ordering column is called row order in the story and priority in the TSD | Data steward | Resolved (directive) |
| GAP-1357 | The PAYMENT_MATCH version label differs between RWB-E2-027 and RWB-E2-042 | Center of excellence analyst | Resolved (directive) |
| GAP-1358 | DecisionRecorded is listed as consumed here but the catalogue names only two consumers | Integration architect | Resolved (directive) |
| GAP-1359 | The rule-evaluation result has no published schema and two of its field names are not given | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1360 | The three payment event payloads have no schema in any source | Integration architect | Resolved (directive) |
| GAP-1361 | No numeric operations value is specified for the matching service | DevOps engineer | Resolved (directive) |
| GAP-1362 | The secret names, the workload identity and the certificate of rwb-payment are not specified | Identity and access team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1463 | RWB-E2-032 is conditional on a model existing and no decision row names who confirms it | Restructure operations officer with the TDR team | Resolved (directive) |
| GAP-1479 | Epic 3 features depend on Epic 4 features that release a month later | Solution architect | Resolved (directive) |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1589 | Signatures are owned by P5 in Architecture v5 and the Ownership Map but have no requirement, feature or story | Solution architect with P6 and S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1596 | The signature request is defined as a Communications table while Architecture v5 gives signatures to the document hub | Solution architect | Resolved (directive) |
| GAP-1624 | FSD P8 issues no requirement ID, so the product requirement cannot be traced to an FSD requirement | Business analyst, P8 | Resolved (directive) |
| GAP-1625 | Eight of the eleven P8 features carry a placeholder acceptance criterion instead of a testable one | Business analyst, P8 | Resolved (directive) |
| GAP-1626 | The two operations named in Architecture v5 slide 17 are not the two operations in the API Specification and the Ownership Map | Solution architect | Resolved (directive) |
| GAP-1628 | The matching values have no table and no owner after payment_match_rule was retired | Solution architect | Resolved (directive) |
| GAP-1631 | The FSD names ALS, GL, ATS and AMIS as interface points, and v5 lets no service call a system of record | Solution architect | Resolved (directive) |
| GAP-1639 | The two event-started workflows have no name or identifier in any v5 source | Solution architect | Resolved (directive) |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1698 | The Ownership Map lists one table for rwb-treatment, although Architecture v5 gives it four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1702 | The FSD triggers on a completed ACE batch, and AceDataReady does not reach this service while no S2 job exists in the job map | Solution architect with the P1 owner | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1707 | Three Drools packages are named for this service with no code, version label or owner | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1708 | The FSD acceptance criteria are placeholders, so no criterion of this module is observable as written | Business analyst, S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1709 | The service is wave 2 and EP02 while every requirement of the module is an Epic 3 requirement | Solution architect | Resolved (directive) |
| GAP-1710 | Only one of the five messages this service shows is its own, and none has agreed wording | Business analyst, S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1712 | The field catalog covers eight fields and none of them describes a contract, an agreement, a plan timer or a booking | Data architect | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1715 | The history of FSD S2 versions 1 and 2 is not in the sources read, and the dependency sentence repeats a feature code | Business analyst, S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1716 | The treatment record exists twice: as this service's live record and as P1's dated copy | Data architect | Resolved (directive) |
| GAP-1869 | The treatment API shapes, the treatment table set, the case-state reporting and the decision code of a treatment event are not specified | Tech lead of rwb-treatment with the P3 owner of the case contract and the owner of the local decision-record library | Resolved (directive) |
| GAP-1870 | The settlement offer operation, its body and the range and floor facts are not specified for rwb-treatment | Tech lead of rwb-treatment with the S1 owner of the payoff and range calculation | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1871 | The offer operation is /treatments/{id}/offer in Architecture v5 and /treatments/{treatmentId}/submit in API Specification v4 and the TSD | Solution architect with the rwb-treatment tech lead | Resolved (directive) |
| GAP-1872 | The below-floor approval record, the delegation facts, the reason code and the TreatmentApproved payload are not specified for rwb-treatment | Tech lead of rwb-treatment with the rwb-access owner of the DoA table and the rwb-decision owner of the approval workflow | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1874 | The plan write path is /treatments/{id}/offer in Architecture v5 and /treatments/{treatmentId}/submit in API Specification v4 and the TSD, and the legacy endpoint table names neither | Solution architect with the rwb-treatment tech lead | Resolved (directive) |
| GAP-1876 | The checked-fields operation and payload on the treatment side, the treatment columns that carry the contract and mortgage facts, the masking of the treatment read and who stamps the type-table version are not specified | Solution architect with the rwb-treatment and rwb-document squads | Resolved (directive) |
| GAP-1877 | Architecture v5 puts the S2 call to P5 in the Temporal column while the legacy published interface and DP-11 make the checked-fields read one REST hop | Solution architect with the platform workflow team, rwb-document and rwb-treatment | Resolved (directive) |
| GAP-1878 | The treatment-side generation call, its two columns, the merge-field set and the generation event are not specified | Solution architect | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-1880 | The treatment-side matching read, the shortfall columns, the breach decision code and the plan-check cadence are not specified | Solution architect with the rwb-treatment and rwb-payment squads | Resolved (directive) |
| GAP-1881 | PAYMENT_MATCH is the rwb-payment matching package while this slice evaluates it for the plan breach on the treatment side | Solution architect with rwb-decision, rwb-payment and rwb-treatment | Resolved (directive) |
| GAP-1882 | The treatment-side use of the suggestion is unspecified: the agent-run operation and its payload on the caller side, the treatment columns that hold the proposal and the model, prompt and policy versions, the 60 s wait and its fallback contract, and the decision code of a suggestion record | Solution architect | Resolved (directive) |
| GAP-1883 | Architecture v5 slide 16 publishes no inbound suggestion operation on rwb-agent, while the legacy treatment flow calls one synchronously | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1899 | DP-09 and DP-10 are in the pattern list but this slice produces no event, consumes no event and registers no Schedule, and DocumentFieldsExtracted is consumed by rwb-case only | Solution architect | Resolved (directive) |
| GAP-1900 | The sources give only the Java interface of the field reader: no REST operation, path, transport or field-level name is named for the checked-fields read | Solution architect, with the rwb-document owner (P5) | Resolved (directive) |
| GAP-1901 | The mapping of an extracted field code onto an S4 column is not stated, and eleven codes, hearing_type and lawsuit_no have no counterpart of the same name | Business analyst and solution architect, with the rwb-document owner | Resolved (directive) |
| GAP-1902 | REQ-DCM-017 and REQ-DCM-018 are in the plan's requirement list for this story but in no row of the legacy traceability table, and legacy section 19 puts them out of scope | Business analyst | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1904 | SCR-19 Litigation workspace is listed with its first release in E5, while this story is a wave 2 story released on 31 December 2026 | Solution architect and the edge owner | Resolved (directive) |
| GAP-1905 | No approval of the realigned story or of the sources it consumes is recorded, so the story runs in Draft | Solution architect | Resolved (directive) |
| GAP-2311 | Values of the payment-matching access profile that the legacy story does not state | Business analyst, P4 | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2313 | The rule-package endpoints are P4 in the legacy contract and P7 in Arch v5 | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2314 | No legacy acceptance criterion of RWB-E2-027 belongs to the P4 slice | Business analyst, P4 | Resolved (directive) |
| GAP-2352 | The signature-request operations exist in no P5 source and carry no API ID, because the legacy key is a communications module story while the table is P5's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2353 | signature_request is defined in TSD P6 T3.1 inside the communications module and owned by P5 in the ownership ruling, so the table has no P5 data model | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2355 | No source names a signature event on the rwb-document topic, and the request state is readable only through the operations of the story | Solution architect | Resolved (directive) |
| GAP-2356 | The write-once container, the WORM tier, the size limit and the byte transfer behind the signed-version add are named by no source | SCB IT infrastructure | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2357 | No rwb-document message exists for a closed signature request and no source names the operation-level right of the five request operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2393 | rwb-comms generation request key and P5 document-create operation are not specified | Service owner, rwb-comms; service owner, rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2394 | Generated-documents endpoint is not in the P6 operation inventory | Architecture owner; service owner, rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2403 | No source gives the wire shape or the value sets this story needs: the append request and answer, the ledger read and its page, the reference-data operation, the text of MSG-P7-009 and the DP-02 login name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2506 | The rule-contract C row, the ordering column, the version label, the record consumer list and two consumed operation names are unsettled for the payment-matching slice, and the legacy AC6 load is not this story's | Solution architect, with the decision service owner, the data steward and the event catalogue owner | Resolved (directive) |
| GAP-2507 | The consumed rule-evaluation result, the treatment installment-paid call, the three event payloads and the shared record's consumer list have no published schema or operation name | Solution architect, with the owners of rwb-decision, rwb-treatment and the event catalogue | Resolved (directive) |
| GAP-2508 | No numeric operations value and no name of a secret, identity or certificate is specified for the matching deployment | DevOps engineer, with the platform administrator and the identity and access team | Resolved (directive) |
| GAP-2634 | The delegation-of-authority limit, its boundaries and the row that answers them are not published, and its owner is read two ways in this run | P4 rwb-access owner and P7 rwb-decision owner | Resolved (directive) |
| GAP-2659 | The release body, its required set, the release trigger path, the body of EV-10 and the release instant have no published shape | Solution architect with the rwb-treatment tech lead and the P6 and P8 owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2674 | The readiness check result, the title-set task, the trigger and the ACE status field are not specified for rwb-treatment | Tech lead of rwb-treatment with the P3 owner of the case contract, the P1 owner of the ACE read and the owner of the local decision-record library | Resolved (directive) |
| GAP-2675 | The published shape of the readiness section, of the title-set task request and of the view column contract has no source | Solution architect with the rwb-treatment tech lead, the P3 owner of the case contract and the P1 owner of the ACE read | Resolved (directive) |
| GAP-2677 | The field list, the value domain and the home of the unlock element, and the announcement of the release, have no published shape | Solution architect with the rwb-treatment tech lead and the P7 owner of the rule packages | Resolved (directive) |
| GAP-2682 | The release result, the release instruction, the confirmation read and the case outcome are not specified for rwb-treatment | Tech lead of rwb-treatment with the P3 owner of the case contract, the P8 owner of the payment contract, the P1 owner of the ACE read and the platform integration owner of the CCMS adapter | Resolved (directive) |
| GAP-2683 | The published shape of the release section, of the two release events, of the release vocabulary and of the view column contract has no source | Solution architect with the rwb-treatment tech lead, the P3 owner of the case contract, the P1 owner of the ACE read and the platform integration owner of the CCMS adapter | Resolved (directive) |
| GAP-2684 | The document-set result, the rendering hand-off, the party set and the case trigger are not specified for rwb-treatment | Tech lead of rwb-treatment with the P5 owner of the document contract, the P6 owner of the template catalogue and the P3 owner of the case contract | Resolved (directive) |
| GAP-2685 | The published shape of the document-set section, of the set request and of the status vocabulary has no source | Solution architect with the rwb-treatment tech lead, the P5 owner of the document contract and the P6 owner of the template catalogue | Resolved (directive) |
| GAP-2690 | The rwb-treatment share of the key is stated by no S2 source, and the caller contract, the level comparison, the case move and the record ownership are split across four stories | Solution architect with the rwb-integration, rwb-treatment, rwb-case and rwb-access tech leads and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2699 | The treatment-side signature columns, the operation a signature record arrives on, the event names, the two list codes and the closure are not specified for rwb-treatment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2700 | Architecture v5 gives S2 to P5 the Temporal cell and no cell from P6 or P5 into S2, while the legacy seam is one synchronous in-process call and the work package lists DP-11 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2701 | The legacy one module and one transaction for the signature request, the signed version and the treatment field become three owners, and the offer expiry that closed the request is now the treatment's own date | Solution architect | Resolved (directive) |
| GAP-2702 | The treatment-side checked-field read, the fact columns it fills, the type-table version stamp and the unmapped field codes are not specified | Tech lead of rwb-treatment with the P5 owner of the checked-field contract and the rwb-treatment data owner | Resolved (directive) |
| GAP-2703 | Architecture v5 puts the S2 read of rwb-document on Temporal while the legacy interface and DP-11 make it one REST hop | Solution architect with the P5 contract owner and the platform Temporal owner | Resolved (directive) |
| GAP-2705 | The match consequence that rwb-treatment consumes is not published, and no source names the plan states the treatment row holds after a match | Contract owner of rwb-treatment with the owner of rwb-payment and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2706 | No source names the rule set, the parameter codes or the signal that announce a plan state change, and none states who consumes the plan consequence once rwb-treatment owns it | Solution architect with the rule owner of rwb-decision and the parameters owner of rwb-case | Resolved (directive) |
| GAP-2835 | The litigation-side checked-field read, the fact columns it fills on legal_action and hearing, the source stamps and the unmapped field codes are not specified | Tech lead of rwb-litigation with the P5 owner of the checked-field contract and the rwb-litigation data owner | Resolved (directive) |
| GAP-2836 | No source says how an extracted hearing_date becomes a hearing row, which hearing_type that row carries, or what the apply does to an action in a closed status | Litigation business analyst with the rwb-litigation data owner and the S4 hearing story owner | Resolved (directive) |
| GAP-3179 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids | Solution architect with the decision and rules lead | Resolved (directive) |
| GAP-3180 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 | Decision and rules lead with the payment lead | Resolved (directive) |
| GAP-3182 | The signature_request table is created by P6 in the story and owned by P5 in the ownership map | Document hub lead with the communications lead | Resolved (directive) |
| GAP-3188 | The payment match rule load is a P4 reference load in the story and a P7 rule package in the target | Decision and rules lead with the access lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S2-E2025-APP | skipped AC ID | 134 | missing: AC10, AC11 |
| RWB-S2-E3002-APP | new AC without TC row | 377 | AC5 is new and no section 16 row covers it |
