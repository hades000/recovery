# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 5 of 8 (RWB-P7-E2013-OPS to RWB-P7-E2019-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 99 |
| Cross-document (pending in another document) | 158 |
| Not applied (value not in the sources) | 25 |
| Open business decisions | 24 |
| Register gaps linked | 71 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-E2013-OPS | 12 | 28 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2013 OPS Approval routing with the delegation of authority table - deployment v2.md |
| RWB-P7-E2014-APP | 31 | 30 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2014 APP Approval screen for D7.1 demand and recall notices v2.md |
| RWB-P7-E2014-CON | 11 | 23 | 11 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2014 CON Approval screen for D7.1 demand and recall notices - contract v2.md |
| RWB-P7-E2014-OPS | 11 | 35 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2014 OPS Approval screen for D7.1 demand and recall notices - deployment v2.md |
| RWB-P7-E2017-APP | 15 | 25 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2017 APP Contract, CA and mortgage document generation screens v2.md |
| RWB-P7-E2019-APP | 19 | 17 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2019 APP Partner identities through the external gateway v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P7-E2014-APP | R-11289 | CG-ALL-7194 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2017-APP | R-11296 | CG-ALL-7225 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2019-APP | R-11299 | CG-ALL-7239 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E1034-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22079 | GAP-1606 | Register gap | Product owner with Legal counsel | It is not stated whether the approval is taken on a template version or on a generated notice | Record the Legal approval on the template version as a decision record written through rwb-decision, and take the notice approval for the demand and recall types through the approval workflow on the generated notice; state both in the story's acceptance criteria. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22463 | GAP-1616 | Register gap | Risk and model risk officer with the rwb-access owner | The delegation of authority table is loaded and approved inside P7 while the ownership ruling gives the table to rwb-access | Keep in this service only the lookup at the moment of the decision and the recording of the row ID and version; move A2.24 with AC-P7-024-01 to AC-EXC-P7-024-05 to rwb-access, and confirm the lookup answer shape (level, row ID, version, NOT_COVERED, RELATED_PARTY reason) in the access contract. Until then this PRD reads the limits and records the version, and OQ-P7-05 stays open. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22470 | GAP-1253 | Register gap | Business lead with the Center of excellence | The escalation ceiling and the service level values of an approval are not specified | Fix three values as data owned by RW-COE: the service level per decision and per default, the escalation step in working days, and a maximum escalation count with its ceiling behaviour (hold, incident to RW-RISK, or committee). Carry them as rwb.approval.service-level.*, rwb.approval.escalation.step and rwb.approval.escalation.max-levels and close DL22. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22482 | GAP-0931 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masked rendering of the addressee postal address is not specified | Let the platform masking library own one rendering per field type, record it as data beside the masking row, and add the postal address rendering to the MASK-SIT-01 pack before the first SIT run of the approval screen |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22483 | GAP-1260 | Register gap | Business lead | The limit that applies on the approval screen conflicts with D7.1 carrying no amount limit | Show the approval level and the route role as the limit that applies for D7.1 (no amount, level none) and read the DoA table only where an amount-bearing decision uses the screen; confirm with Risk and Credit. |
| RWB-ITG-E2014-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22495 | GAP-1269 | Register gap | Compliance and PDPA officer | No source enumerates the mask flags of the screen fields | Declare a mask flag of NONE, PARTIAL or FULL with a policy key on every field of the two panels, PARTIAL for the postal address, and confirm the policy keys with the masking owner (P4). |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22514 | GAP-0943 | Register gap | Compliance and PDPA officer | rwb-access document set: the masking version in force for SIT and the field IDs of the personal fields on the review view are not specified | Fix the mask version label per environment in the policy pack load, publish the field IDs of a generated contract and its parties with the LDM, and have the pack owner confirm the DF-PTY-007 and DF-PTY-016 rows before SIT. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22516 | GAP-1582 | Register gap | Legal counsel | E-discovery and court-ready evidence have no FSD feature, no operation and no response target | FR-P5-028, FR-P5-029 and AC-P5-021 carry the behaviour with the response target left open as OQ-P5-09. A discovery operation and its response target are needed before wave 2 acceptance. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28769 | GAP-0933 | Register gap | Compliance and PDPA officer with the P4 build squad | The masking version in force in SIT is not recorded anywhere | Record the masking version in force per environment in the policy pack load record, with its approver and valid-from date, and assert it in the SIT entry check |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28770 | GAP-1261 | Register gap | Data steward and data product owner | The module specification keeps two daily data-lake interfaces that DP-17 removes | Retire INT-19, INT-20 and the daily copy from the P7 documents in the next module-specification version; no lake element appears in this key's stories, chart or run book. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P7-E2014-APP | R-37494 | ASM-2224 | Register assumption |  | For D7.1 the limit that applies on the screen is read as no amount limit at approval level none, shown as the approval level and the route role, and the DoA table is not consulted for this decision; the DoA table stays P4 rwb-access' and is read by the routing story where an amount-bearing decision uses it. | Business lead with Risk and Credit |
| RWB-P7-E2014-APP, RWB-P7-E2014-OPS | R-37500 | ASM-2225 | Register assumption |  | No data-lake element exists in this key: INT-19, INT-20 and the daily decision-log copy are retired, the record is published on rwb.decision-record.v1 and reporting reads events, and JOB-13 is continuous Kafka ingest in the owning service. | Data steward and data product owner in the next module-specification version |
| RWB-P7-E2014-CON | R-37504 | ASM-2233 | Register assumption |  | Every field of the two panels declares a mask flag of NONE, PARTIAL or FULL with a policy key; the postal address is PARTIAL, identifiers and codes are NONE, and the mask itself is applied by the route with the policy of rwb-access. | Compliance and PDPA officer with the masking owner |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-E2013-OPS | R-22466 | GAP-0929 |  | The DoA lookup and authority-decision request and response shape is not specified | The request and response field sets are in the story DoA sections, outside this chunk, so there is no anchor for the freeze note. Re-run with those sections. |
| RWB-P7-E2013-OPS | R-22469 | GAP-1222 | 12.1 | No source names the notice and message operations or the notice fields that carry an approval reference, an escalation level, a recipient and a sent time | Section 12.1 Notice and MessageRequest text is outside this chunk, so there is no anchor. Re-run with section 12.1 to confirm the paths and field sets. |
| RWB-P7-E2014-APP | R-06817 | DOR-RWB-P7-E2014-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (project-wide search for 'epic design'). Sign-off needs its owner's record; no value written. |
| RWB-P7-E2014-APP | R-11286 | CG-ALL-7188 | 4, 12.1 | HTTP errors with no message ID: 401 no session | Error and Message Standard v4 has no 401 no-session row. MSG-GEN-006 (system unavailable) does not fit. No ID invented; BA to confirm. |
| RWB-P7-E2014-CON | R-18094 | DOR-RWB-P7-E2014-CON-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Rows SCR-10, SCR-11 and SCR-18 are in section 10, which is not in this chunk. Empty, loading, error and no-access states are not in any source read. |
| RWB-P7-E2014-CON | R-18097 | DOR-RWB-P7-E2014-CON-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | New AC and TC rows for BR1 to BR13 need sections 7 and 16 and their next free numbers, which are not in this chunk. |
| RWB-P7-E2014-CON | R-22481 | GAP-0398 | find it | Integration harness values for the D7.1 decision-screen journey are not specified | The touched story text is not in this chunk. The route, fixtures, environment and gate values are in no source read; they are agreed at the wave 2 entry check. |
| RWB-P7-E2014-CON | R-22489 | GAP-2390 | not in chunk | No source says whether a notice move writes its own decision record or only references the approval entry of rwb-decision | Notice move write text is not in this chunk, so no old text can be copied. Re-send that section to add the D7.1 local record. |
| RWB-P7-E2014-CON | R-22490 | GAP-2743 | not in chunk | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Dependency Map, Ownership Map and trace text are not in this chunk. The placeholders and the D7.1 gate decision are not in the sources. Re-send those sections. |
| RWB-P7-E2014-CON | R-22492 | GAP-1258 | not in chunk | The field-level list and the mask flags of the D7.1 approval screen are published by no source | Screen field list and mask flag text are not in this chunk, so no old text can be copied. Re-send that section to publish the field list. |
| RWB-P7-E2014-CON | R-22493 | GAP-1259 | 12 | The composite-route name and path segment of the approval screen are not specified | Section 12 route table is not in this chunk, so no old text can be copied. Re-send section 12 to add GET /api/recovery/approvals/{approvalId}. |
| RWB-P7-E2014-CON | R-22494 | GAP-1267 | 15 | The legacy screen states and the platform route states are two unreconciled vocabularies | Section 15 screen state text is not in this chunk, so no old text can be copied. Re-send section 15 to add the panel states and overlay rule. |
| RWB-P7-E2014-CON | R-28772 | GAP-1266 | 9 | The field types and order of the screen model and the queue paging defaults are not specified | Section 9 text is not in this chunk, so no old text can be copied. Re-send section 9 to add the 20/100 paging defaults and field types. |
| RWB-P7-E2014-CON | R-28773 | GAP-1271 | not in chunk | The dashboard names, the alert thresholds and the empty-queue window are not specified | Observability and threshold text is not in this chunk, so no old text can be copied. Re-send that section to add the four alert rules. |
| RWB-P7-E2014-CON | R-31505 | NEWAC-RWB-P7-E2014-CON-AC9 | 7; 16 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so AC9 and its test row cannot be written. The proposed test is not specified in the sources. |
| RWB-P7-E2014-OPS | R-18100 | DOR-RWB-P7-E2014-OPS-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 text is not in this chunk, so its exact old text cannot be copied. Apply in the chunk that holds section 9. |
| RWB-P7-E2014-OPS | R-18102 | DOR-RWB-P7-E2014-OPS-18 |  | Definition of Ready item 18 Open decisions: Partial | The open-decisions section is not in this chunk, so DL34, DL35 and their ASM IDs cannot be recorded. Apply in the chunk that holds it. |
| RWB-P7-E2014-OPS | R-18104 | DOR-RWB-P7-E2014-OPS-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in this chunk, so the next free AC and TC IDs cannot be assigned without inventing numbers. Apply with those sections. |
| RWB-P7-E2017-APP | R-06833 | DOR-RWB-P7-E2017-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in the story or the sources (searched the story and the Logical Data Model and Error Standard caches). Recording a sign-off would invent an approval. Needs the epic design record. |
| RWB-P7-E2017-APP | R-26349 | CG-ALL-7226 | 3 | Flyway file V2026_2__decision_log_documentscreens_index.sql is not in the V0001..Vnnnn form | Migration name is in section 13 (not in the supplied text). Next free rwb_decision number is not in the sources; Service Template Spec v1 gives only V0001 as baseline. Solution architect to assign. |
| RWB-P7-E2019-APP | R-06839 | DOR-RWB-P7-E2019-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or the sources (searched the folder for epic design sign-off). Sign-off cannot be confirmed; left as is. |
| RWB-P7-E2019-APP | R-18116 | DOR-RWB-P7-E2019-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The field rows that carry the personal-data class are not in the chunk, so they cannot be anchored or edited. Needs the section 12 field rows. |
| RWB-P7-E2019-APP | R-18120 | DOR-RWB-P7-E2019-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Adding the AC in section 7 and the TC rows in section 16 needs those sections, which are not in the chunk. No anchor text available. |
| RWB-P7-E2019-APP | R-26355 | CG-ALL-7240 Flyway file name V2026_2__decision_log_partner_access_index.sql is not in the V0001..Vnnnn form | 3.1 | Flyway file V2026_2__decision_log_partner_access_index.sql is not in the V0001..Vnnnn form | The migration name line is outside the chunk, and the next free Vnnnn of the rwb_decision sequence is not in the text. Setting it would invent a number. Not specified in the source documents (CG-ALL-7240). |
| RWB-P7-E2019-APP | R-31509 | NEWAC-RWB-P7-E2019-APP-AC11 | 8 | AC11: §8 BR8, BR11, BR14, BR15 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 and 16 are not in the chunk, so the AC and its test row cannot be anchored. Proposed test is not specified in the sources. |

## 5. Cross-document changes (pending in the target document)


### RWB-P7-E2014-CON (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12332 | RWB-P7-E2014-APP | DOR-RWB-P7-E2014-APP-21 | header | Build status is Not started; it must reach Done before this story is ready to start. |
| CDC-12333 | RWB-P7-E2014-APP | DOR-RWB-P7-E2014-APP-22 | header | Publish the contract fake library and record its published version. |
| CDC-12334 | RWB-P7-E2014-APP | DOR-RWB-P7-E2014-APP-23 | header | Contract version built against row added, stating the version is Not specified in the source documents |
| CDC-12350 | RWB-P7-E2014-APP | GAP-2387 |  | Baseline the notice answer as id, caseId, documentId, noticeType, state, templateCode, templateVersion, templateState, approvedAt and decisionLogEntryId, with template states DRAFT, APPROVED and WITHDRAWN and no personal field. |
| CDC-12354 | RWB-P7-E2014-APP | GAP-1258 |  | Publish the field list and mask flags of the D7.1 approval panels as the working read, confirmed with the route owner and three consumer sign-offs; mask flags not specified in the source documents (GAP-1258). |
| CDC-12358 | RWB-P7-E2014-APP | GAP-1266 | 7 | Set the queue page size default to 20 and the maximum to 100; publish the field types of the screen model and of the ApprovalPage query parameters decision, product, page and size. |
| CDC-12385 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS-21 |  | Move build status of RWB-P7-E2014-CON from Not started to Done. |
| CDC-12386 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS-22 |  | Publish a contract fake library version and record it as published. |
| CDC-12403 | RWB-P7-E2014-OPS | GAP-2387 |  | Baseline notice answer as id, caseId, documentId, noticeType, state, templateCode, templateVersion, templateState, approvedAt, decisionLogEntryId; template states DRAFT, APPROVED, WITHDRAWN. |
| CDC-12408 | RWB-P7-E2014-OPS | GAP-1258 |  | Publish the field list and mask flags of the approval panels as the working read, confirm with the route owner and consumer sign-offs, and correct by a new contract version. |
| CDC-12415 | RWB-P7-E2014-OPS | GAP-1266 |  | Fix the page size default at 20, the maximum at 100, and publish the field types of the screen model |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12306 | RWB-P7-E2013-OPS | CG-ALL-7178 | 11 | Record information_schema as a database system catalog object (object list of rwb_decision) in the owning document, or use its dictionary name. |
| CDC-12307 | RWB-P7-E2013-OPS | CG-ALL-7179 | 12.7 | Record flyway_schema_history as the Flyway system history table inside rwb_decision in the owning document, or use its dictionary name. |
| CDC-12311 | RWB-P7-E2013-OPS | DOR-RWB-P7-E2013-OPS-7 | 11 | Job-run record field list added from the prose of section 11 |
| CDC-12348 | RWB-P7-E2014-APP | GAP-2385 |  | Add nullable decision_log_entry_id uuid to notice with a unique index, written by approve and hold and null where no approval moved the notice; add the field to the rwb_comms LDM before wave 2 build. |
| CDC-12371 | RWB-P7-E2014-CON | GAP-2385 | find it | Add nullable column decision_log_entry_id uuid to notice in rwb_comms with a unique index, written by approve and hold and null when no approval moved the notice; Flyway step V2014_1__notice_decision_reference.sql; add to LDM before wave 2 build. |
| CDC-12401 | RWB-P7-E2014-OPS | GAP-2385 |  | Add nullable decision_log_entry_id uuid to notice with a unique index, via Flyway step V2014_1__notice_decision_reference.sql, before the wave 2 build. |
| CDC-12423 | RWB-P7-E2017-APP | DOR-RWB-P7-E2017-APP-7 | 11 | Add trigger tr_declog_append_only and merge field transfer_price (locked) to LDM v9, or confirm both as non-LDM objects; rerun detcheck. decided_at is DF-DEC-016 in LDM v9 (line 450). |
| CDC-12426 | RWB-P7-E2017-APP | CG-ALL-7217 | 3, 7, 12.8 | Record transfer_price as a dictionary field or as the merge field key of the P6 merge field catalog; nearest names are not the same field. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12327 | RWB-P7-E2013-OPS | CG-ALL-7182 | 18 | Align the test IDs of REQ-APD-001, REQ-APD-007 and REQ-APD-010 with section 18 of RWB-P7-E2013-OPS in the next RTM version. |
| CDC-12356 | RWB-P7-E2014-APP | CG-ALL-7193 | 18 | Align the REQ-APD-002 and REQ-APD-006 test lists in RTM v7 with section 18 of RWB-P7-E2014-APP in the next RTM version. |
| CDC-12378 | RWB-P7-E2014-CON | CG-ALL-7203 | 18 | Align the REQ-APD-002 and REQ-APD-006 test lists with section 18 of RWB-P7-E2014-CON in the next RTM version. |
| CDC-12411 | RWB-P7-E2014-OPS | CG-ALL-7210 | 18 | Align the REQ-APD-006 and REQ-APD-002 test lists in RTM v7 with the TC-P7-E2014-OPS IDs in section 18 in the next RTM version. |
| CDC-12430 | RWB-P7-E2017-APP | DOR-RWB-P7-E2017-APP-12 | 12.7, 16 | TC-E2-017-16 added in section 16 as a Contract test for ASM-3438; section 18 unchanged. |
| CDC-12440 | RWB-P7-E2017-APP | CG-ALL-7224 | 18 | Align RTM v7 trace lists for REQ-DCM-012, REQ-OCC-002 and REQ-OCC-009 with section 18 of this story in its next version. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12316 | RWB-P7-E2013-OPS | GAP-1252 | 8 | Add GET /api/recovery/access/v1/doa-limits with owner P4 and list it in RWB-P4-E1037-CON |
| CDC-12369 | RWB-P7-E2014-CON | GAP-1264 | find it | Publish approve, regenerate and hold on the rwb-comms contract with their states and error codes, or one decision operation with an outcome code; correct the Ownership Map rows. |
| CDC-12370 | RWB-P7-E2014-CON | GAP-2384 | find it | Add POST /api/recovery/comms/v1/notices/{noticeId}/approve, .../regenerate and .../hold with request fields and the 401, 403, 404, 409, 422 and 503 set; add the rows to the rwb-comms API file and the Ownership Map. |
| CDC-12376 | RWB-P7-E2014-CON | GAP-2742 | 18 | Record notice and template rows as P6's or correct the S4 row; name the P6 notice operation and the rwb-case answer; add REQ-S4-001 to the key's trace; decide the D7.1 approval conflict in the EP05 PRD. |
| CDC-12400 | RWB-P7-E2014-OPS | GAP-2384 |  | Publish POST /api/recovery/comms/v1/notices/{noticeId}/approve, /regenerate and /hold with the listed request fields, answer and error set; add the three rows at next revision. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12419 | RWB-P7-E2017-APP | CG-ALL-7218 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log through the owning CON story, or remove it from 12.1. |
| CDC-12420 | RWB-P7-E2017-APP | CG-ALL-7219 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} through the owning CON story, or remove it from 12.1. |
| CDC-12424 | RWB-P7-E2017-APP | DOR-RWB-P7-E2017-APP-8 | 12.1 | Add GET /api/recovery/decision/v1/decision-log and GET /api/recovery/decision/v1/decision-log/{entryId}; rwb-access to publish POST /api/recovery/access/v1/authorise. |
| CDC-12444 | RWB-P7-E2019-APP | CG-ALL-7233 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log in paths through the owning contract story, as TSD P7 v2 T-A.1 API-P7-006 requires. |
| CDC-12445 | RWB-P7-E2019-APP | CG-ALL-7234 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} in paths through the owning contract story, as TSD P7 v2 T-A.1 API-P7-007 requires. |

### RWB-P7-E2013-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12304 | RWB-P7-E2013-OPS | DOR-RWB-P7-E2013-OPS-22 | 12.8 | Publish the rwb-source-data contract fake and record its contract fake library version as published. |
| CDC-12305 | RWB-P7-E2013-OPS | DOR-RWB-P7-E2013-OPS-23 | header | Fix and publish the contract version this story builds against, then state it in the story. |
| CDC-12322 | RWB-P7-E2013-OPS | GAP-1255 |  | Baseline the five approval resources from TSD P7 T3.1 field names in camelCase, fix the required property of ApprovalAction, and add the case-status operation to the Ownership Map. |
| CDC-12324 | RWB-P7-E2013-OPS | GAP-0732 |  | Fix at contract review: approval event fields consumed by the case, task fields written (approval reference, preparer reference), escalation representation, status mapping, composite route fields and the rwb-case login name. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12308 | RWB-P7-E2013-OPS | DOR-RWB-P7-E2013-OPS-1 | 1 | Add the role DevOps engineer of the rwb-decision service as a role code or role name, or the story must use an existing role. |
| CDC-12363 | RWB-P7-E2014-CON | DOR-RWB-P7-E2014-CON-1 | 1 | Add a role code and role name for the 'tech lead' role used in section 1 of RWB-P7-E2014-CON; v5 lists only RW-* codes and none is a tech lead role. |
| CDC-12389 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS-1 | 1 | Add a role code for 'DevOps engineer of the service', or name an existing role to replace it in story section 1. |
| CDC-12428 | RWB-P7-E2017-APP | DOR-RWB-P7-E2017-APP-1 | 1 | Add or confirm role codes for restructuring officer (FCR) as RW-RESTRUCT as used in section 4, case owner and internal audit reader. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12317 | RWB-P7-E2013-OPS | GAP-1256 |  | Record the delegation snapshot rule: warm read-through cache at start before readiness, refresh on DoaLimitChanged keyed on effective date, and an alert when the cached version is older than the version in force. |
| CDC-12345 | RWB-P7-E2014-APP | GAP-0932 | 8 | Publish the authorise, me-permissions and masking-policies shapes and state whether the routed role or the holder is a request field |
| CDC-12368 | RWB-P7-E2014-CON | GAP-0932 | find it | Publish the authorise, me-permissions and masking-policies shapes and state whether the routed role or the holder is a request field; reconcile GET /me/session with GET /me/permissions. |
| CDC-12396 | RWB-P7-E2014-OPS | GAP-0932 |  | Publish the authorise, me-permissions and masking-policies shapes and state whether the routed role or the holder is a request field. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12326 | RWB-P7-E2013-OPS | CG-ALL-7181 | 16 | Add rows TC-P7-E2013-OPS-01 to TC-P7-E2013-OPS-08 with Given, When and Then copied from the criteria they cover. |
| CDC-12377 | RWB-P7-E2014-CON | CG-ALL-7202 | 16 | Add rows for TC-P7-E2014-CON-01 to TC-P7-E2014-CON-08 with Given, When and Then copied from the criterion each covers. |
| CDC-12390 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS-12 | 16, 18 | Add rows TC-P7-E2014-OPS-01 to -07 for AC1 to AC7. Reconcile the section 18 test lists to RTM v7. |
| CDC-12410 | RWB-P7-E2014-OPS | CG-ALL-7209 | 16 | Add rows TC-P7-E2014-OPS-01 to TC-P7-E2014-OPS-07 with Given, When and Then copied from the criterion each covers. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12336 | RWB-P7-E2014-APP | CG-ALL-7187 | find it | Add list LOV-OVERRIDE-REASON to Lists, or name an existing Reference Data v5 list in the story. |
| CDC-12340 | RWB-P7-E2014-APP | DOR-RWB-P7-E2014-APP-20 | 8 | Add the list LOV-OVERRIDE-REASON to Reference Data v5, which BR6 and BR11 read |
| CDC-12388 | RWB-P7-E2014-OPS | CG-ALL-7208 |  | Add list LOV-OVERRIDE-REASON to Lists, or point RWB-P7-E2014-OPS at an existing Reference Data v5 list. No list values are given in the source documents. |
| CDC-12391 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS-20 |  | Add the list LOV-OVERRIDE-REASON, which the P2 detcheck finds missing. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12303 | RWB-P7-E2013-OPS | DOR-RWB-P7-E2013-OPS-14 | header | Record the signed epic design sign-off for EP02 in the epic design record; the story cites no sign-off. |
| CDC-12362 | RWB-P7-E2014-CON | DOR-RWB-P7-E2014-CON-14 | find it | Confirm and record the signed epic design sign-off for RWB-P7-E2014-CON. |
| CDC-12384 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS-14 |  | Record the signed epic design sign-off for RWB-P7-E2014-OPS in the epic design record. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12331 | RWB-P7-E2014-APP | CG-ALL-7190 | 12.5 | Add a Workflows row for ApprovalWorkflow (workflow kit template) on task queue rwb-decision, or confirm its catalogued name. The story names no catalogued alternative. |
| CDC-12337 | RWB-P7-E2014-APP | CG-ALL-7191 | 12.5 | Add activity recordDecision to the Activities sheet, task queue rwb-decision, or confirm a catalogued activity to use. |
| CDC-12338 | RWB-P7-E2014-APP | CG-ALL-7192 | 12.5 | Add activity applyNoticeOutcome to the Activities sheet, task queue rwb-decision, or confirm a catalogued activity to use. |

### RWB-P6-E2014-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12360 | RWB-P7-E2014-APP | GAP-2389 |  | Keep H empty; add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON to the C list. |
| CDC-12383 | RWB-P7-E2014-CON | GAP-2389 |  | Add to the C list: RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON. Keep H empty. |
| CDC-12418 | RWB-P7-E2014-OPS | GAP-2389 |  | Keep H empty; add six platform contracts and two rwb-case contracts to the C list at the next plan revision |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12421 | RWB-P7-E2017-APP | CG-ALL-7220 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-12446 | RWB-P7-E2019-APP | CG-ALL-7235 | 12.2 | Publish POST /api/recovery/access/v1/authorise in paths through the provider's contract story RWB-P4-E2019-CON. |
| CDC-12450 | RWB-P7-E2019-APP | GAP-0785 | 8 | Register POST /partner-identities/resolve on /api/recovery/access/v1 and its two schemas; agree the refusal-to-status table with the gateway owner and message catalogue; state that the capability publishes and consumes no event. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12310 | RWB-P7-E2013-OPS | DOR-RWB-P7-E2013-OPS-12 | 12, 16, 18 | Add TC-P7-E2013-OPS-01 to TC-P7-E2013-OPS-09 to Test Cases v8; align the RTM v7 test lists with the section 18 rows |
| CDC-12364 | RWB-P7-E2014-CON | DOR-RWB-P7-E2014-CON-12 | 16, 18 | Add TC-P7-E2014-CON-01 to TC-P7-E2014-CON-08 to Test Cases v8; align the section 18 test lists of RWB-P7-E2014-CON to RTM v7. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12319 | RWB-P7-E2013-OPS | GAP-0928 |  | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with the query and response fields this story uses, correcting the omission per Architecture v5. |
| CDC-12454 | RWB-P7-E2019-APP | GAP-3148 | header | Fix the partner_user load on POST /api/recovery/partner/v1/admin/reference-loads with table code partner_user and Idempotency-Key; map each refusal to its legacy message id; take partner_user fields from DF-REF-212 to DF-REF-217; keep the five-minute refresh as an assumed parameter. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12321 | RWB-P7-E2013-OPS | GAP-1221 |  | Add rwb-comms as a consumer of rwb.decision.ApprovalRequested.v1 and mirror it in the rwb-decision AsyncAPI document; no ApprovalEscalated event is created. |
| CDC-12330 | RWB-P7-E2013-OPS | GAP-1254 | 13 | State INT-19, INT-20, lake partition, manifest and watermark as retired; rwb-reporting reads from rwb.decision-record.v1; keep EV-08 unchanged. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12323 | RWB-P7-E2013-OPS | GAP-1257 |  | Remove ApprovalDecided from the rwb.decision.events.v1 list, since no catalogue row, number or consumer exists and the outcome is carried by DecisionRecorded. |
| CDC-12366 | RWB-P7-E2014-CON | GAP-2093 | find it | Remove Decision: child: approval from the rwb-comms OUT list; keep ApprovalWorkflow in P7 as a child of NoticeDispatchWorkflow with the notice as source; the notice waits in Approved. |

### OTHER:TSD P7 v2 (T8 traceability table) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12328 | RWB-P7-E2013-OPS | GAP-1263 | 18 | Map REQ-APD-002 and REQ-APD-006 to FEAT-APD-01 with RWB-E2-013 for routing, keeping FEAT-APD-08 with RWB-E2-014 for the screen, in the next version. |
| CDC-12412 | RWB-P7-E2014-OPS | GAP-1263 |  | Map REQ-APD-002 and REQ-APD-006 to FEAT-APD-08 with RWB-E2-014 for the screen and to FEAT-APD-01 with RWB-E2-013 for routing |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12343 | RWB-P7-E2014-APP | GAP-2093 | 7 | Hold the approval in P7 ApprovalWorkflow as child of NoticeDispatchWorkflow with the notice as source; keep S4 POST /notices/{noticeId}/approve as the litigation officer decision point; remove 'Decision: child: approval' from rwb-comms OUT |
| CDC-12394 | RWB-P7-E2014-OPS | GAP-2093 |  | Hold the approval in P7 ApprovalWorkflow as a child of NoticeDispatchWorkflow, with S4 POST /notices/{noticeId}/approve as the decision point; the notice waits in Approved. |

### RWB-P7-E2014-CON; RWB-P3-E1043-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12344 | RWB-P7-E2014-APP | GAP-2216 | 7 | Fix the case-facts projection with inputAsOf on API-P3-002, the refusal and return events on rwb.decision.events.v1, the task code with its reference row, and the dated contact read on rwb-source-data |
| CDC-12395 | RWB-P7-E2014-OPS | GAP-2216 |  | Fix the case-facts projection with inputAsOf, the refusal and return events, the redress task and reference row, and the dated contact read. |

### RWB-P6-E1052-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12346 | RWB-P7-E2014-APP | GAP-1264 | 7 | Publish approve, regenerate and hold on the rwb-comms contract with states and error codes; correct the Ownership Map rows |
| CDC-12398 | RWB-P7-E2014-OPS | GAP-1268 |  | Serve the notice PDF as the document reference through rwb-document, and take the addressee role and masked address from the rwb-source-data fields. |

### OTHER:rwb-comms API file (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12349 | RWB-P7-E2014-APP | GAP-2386 |  | State that a template variant change regenerates on the same notice row: document_id and template_id move to the chosen Approved variant, the version column increments, and the previous document stays readable per AC-ALT-P6-007-01. |
| CDC-12402 | RWB-P7-E2014-OPS | GAP-2386 |  | State that regenerate keeps the same notice row, moves document_id and template_id to the chosen Approved variant, increments the version, and keeps the previous document per AC-ALT-P6-007-01. |

### RWB-S4-E5001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12352 | RWB-P7-E2014-APP | GAP-2743 | none | Record the two consumed notice and template rows as C dependencies with placeholders in the Dependency Map; declare notice and template ownership for P6 in the Ownership Map and name the P6 operations (rwb-comms generate and send, case-move answer) in the P6 contract story; add REQ-S4-001 to the trace. Keep template status on the notice contract, as this story already reads it (DF-LEG-031). The D7.1 gate is a business decision and is not decided here. |
| CDC-12406 | RWB-P7-E2014-OPS | GAP-2743 |  | Record the two consumed rows as C dependencies, declare notice and template ownership in the P6 Ownership Map, add REQ-S4-001 to the trace, and decide the D7.1 gate in the EP05 PRD. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12375 | RWB-P7-E2014-CON | GAP-1270 | 18 | Register the approval-screen route with 2 s per downstream and the same 1.2 s composition budget as the case screen; record measured p95 on the dashboard. |
| CDC-12439 | RWB-P7-E2017-APP | GAP-0401 | 15 | Publish the gateway-bff composite route for the SCR-14 and SCR-30 document set, its merge order, harness repository, environment, data seeding, evidence format and wave 2 pass/fail gate, agreed with QA. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12387 | RWB-P7-E2014-OPS | CG-ALL-7207 |  | Record flyway_schema_history as the Flyway schema history object in rwb_decision, owner Data. |
| CDC-12392 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS-7 | 11 | Add flyway_schema_history as a field or entity in LDM v9 and Data Classification v5. |

### RWB-P7-E2017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12422 | RWB-P7-E2017-APP | DOR-RWB-P7-E2017-APP-21 | header | Contract dependencies row says the P7 contract story is not yet created; no story key is named. |
| CDC-12433 | RWB-P7-E2017-APP | GAP-1713 | header | Record once the owning-service contract for each prerequisite code (FEAT-APD-01 to FEAT-VAL-06); carry the duplicate FEAT-CHO-08 as written. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12427 | RWB-P7-E2017-APP | CG-ALL-7223 | 4, 14 | Add a new message ID for 'The case or the entry is outside the caller's scope' for this story's use; the story then cites it. |
| CDC-12431 | RWB-P7-E2017-APP | DOR-RWB-P7-E2017-APP-9 | 14 | Add a new message ID for 'The case or the entry is outside the caller's scope' for this story's use; the story then cites it. |

### OTHER:P3 screen catalogue (SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12309 | RWB-P7-E2013-OPS | DOR-RWB-P7-E2013-OPS-10 | not located in given text | Record empty, loading, error and no access states for SCR-44 in the P3 screen catalogue. |

### RWB-P7-E2013-CON; OTHER:FSD P7 A2.15 and A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12312 | RWB-P7-E2013-OPS | GAP-1623 | none | Record that the Waiting approval move and the approval task are a P3 reaction to ApprovalRequested; this service writes only rwb_decision |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Epic 2 contract tables (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12313 | RWB-P7-E2013-OPS | GAP-3177 | none | Register the five-minute next-action Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables |

### RWB-P4-E1038-APP; RWB-P4-E2013-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12314 | RWB-P7-E2013-OPS | GAP-0842 | none | Serve GET /doa-limits once from rwb-access; RWB-P4-AD016-APP owns the answer and RWB-P4-E2013-APP owns the routing with no second path |

### RWB-P7-E2013-CON; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12315 | RWB-P7-E2013-OPS | GAP-1251 | none | State that the level lookup is a 2 s read on rwb-access and that the approval stores delegation_limit_id, approval_level and limit_version only |

### OTHER:Approval-routing harness pack (named in the GAP-0397 fix; OTHER:no document of that name in the sources) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12318 | RWB-P7-E2013-OPS | GAP-0397 |  | Hold as data: the composite approval-queue route and merge order (platform edge owner), and the harness environment, delegation-version seeding, holders, service-level clocks, evidence format, retention and pass/fail gate (QA), agreed at the wave 2 entry check. |

### OTHER:TSD P4 v3 T6.1 (permission data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12320 | RWB-P7-E2013-OPS | GAP-0930 |  | Add the rwb-decision service identity with Approval check R and no other Recovery right; confirm with the security administrator before the authorise contract is frozen. |

### OTHER:rwb-comms template catalogue (TSD P6 v2 template and merge_field) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12325 | RWB-P7-E2013-OPS | GAP-1220 | 13 | Load one row: message ID MSG-P7-011, placeholders {decision} and {caseNo}, channel from LOV-CHANNEL, Approved version; retry from the RWB-PLT-TE006-CON outbox policy; template code agreed at wave 2 design review. |

### OTHER:Edge and gateway design (gateway-bff) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12329 | RWB-P7-E2013-OPS | GAP-1621 | 15 | Fix which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations; record the four screen contracts there, not in this PRD. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12335 | RWB-P7-E2014-APP | DOR-RWB-P7-E2014-APP-8 | 12.1 | Kafka Catalog v1: align event type to rwb.decision.DecisionRecorded.v1. Temporal Catalog v1: add ApprovalWorkflow and recordDecision (see CG-ALL-7191). 401 placeholder added in 12.1. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12339 | RWB-P7-E2014-APP | DOR-RWB-P7-E2014-APP-12 | 16, 18 | Added TC-E2-014-28 (contract) and TC-E2-014-29 (boundary) to section 16; section 18 trace row now covers TC-E2-014-01 to TC-E2-014-29. |

### OTHER:P3 Criteria and tests (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12341 | RWB-P7-E2014-APP | DOR-RWB-P7-E2014-APP-7 | 11 | Replace the legacy job and decision-log wording with the current terms; the replacement wording is not in the sources. Section 11 of RWB-P7-E2014-APP (19 data rows) is unchanged. |

### OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12342 | RWB-P7-E2014-APP | GAP-1623 | 7 | Record that the Waiting approval state and the approval task are a P3 reaction to ApprovalRequested; align FSD A2.15 and A2.16 to that choice |

### RWB-P7-E2014-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12347 | RWB-P7-E2014-APP | GAP-2384 |  | Publish POST /api/recovery/comms/v1/notices/{noticeId}/approve, /regenerate and /hold with decisionLogEntryId, reasonCode and templateCode as in the legacy operations, the notice answer and the 401/403/404/409/422/503 set; add the rows. |

### OTHER:TSD P6 v2 T-A.1 and T6.1 (RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12351 | RWB-P7-E2014-APP | GAP-2388 |  | Add rows for the three notice decision operations declared as Litigation right A with scope applied, enforced at gateway-bff via rwb-access, called by rwb-decision with service identity plus approver user identifier and decision entry reference. |

### OTHER:rwb-source-data and rwb-case C rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12353 | RWB-P7-E2014-APP | GAP-1265 | header | Contract dependencies row names the two consumed contracts; their C row IDs are Not specified in the source documents (GAP-1265) |

### OTHER:TSD S4 v2; OTHER:Context pack S4; OTHER:P6 rwb-comms contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12355 | RWB-P7-E2014-APP | GAP-2742 | 18 | Record notice and template rows as P6 in the Ownership Map or correct the S4 row; name the P6 notice operation and case answer in their contract stories; decide the D7.1 approval conflict in the EP05 PRD. Story side: REQ-S4-001 added to trace. |

### OTHER:Edge and gateway design (solution architect with the platform edge owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12357 | RWB-P7-E2014-APP | GAP-1621 | 8 | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from rwb-decision operations and which this service owns; record the four screen contracts there. |

### OTHER:rwb-case reference data; parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12359 | RWB-P7-E2014-APP | GAP-2391 | 8 | Add LOV-HOLD-REASON with REFUSED_BY_APPROVER and TEMPLATE_WITHDRAWN to rwb-case reference data; keep the key rwb.decision.notice-approval read by rwb-decision and rwb-comms until the platform feature-flag owner renames it. |

### OTHER:Gateway-bff composite route document (platform, owner PLT) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12361 | RWB-P7-E2014-CON | CG-ALL-7200 | 12.1 | Publish GET /api/recovery/approvals/{approvalId} as the gateway-bff public route for the D7.1 approval screen; rwb-decision.yaml does not carry this path. |

### OTHER:rwb-case contract (case contract owner) and FSD P7 acceptance criteria A2.15 and A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12365 | RWB-P7-E2014-CON | GAP-1623 | find it | Record the P3 reaction to ApprovalRequested as the writer of the Waiting approval state and the approval task, and align AC-P7-015-01 to it. |

### OTHER:Baseline reviews for the D7.1 approval shapes (case-facts projection, outcome event names, redress task naming, postal a (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12367 | RWB-P7-E2014-CON | GAP-2216 | 11 | Section 11 carries these as assumptions ASM-B2-P3-006-1 to -4 until the baseline reviews publish them |

### OTHER:rwb-comms API file and TSD P6 v2 (T3.1 notice table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12372 | RWB-P7-E2014-CON | GAP-2386 | find it | Regenerate on the same notice row: document_id and template_id move to the chosen Approved variant, the version column increments, the previous document stays in rwb-document with its template version, and the approval keeps one source_ref. |

### OTHER:rwb-comms API file and TSD P6 v2 (T-A.2 API-P6-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12373 | RWB-P7-E2014-CON | GAP-2387 | find it | Baseline the notice answer as id, caseId, documentId, noticeType, state, templateCode, templateVersion, templateState, approvedAt and decisionLogEntryId, mapped from notice and template with no personal field; template states DRAFT, APPROVED, WITHDRAWN. |

### OTHER:TSD P6 v2 (T-A.1 endpoint inventory and T6.1 rights matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12374 | RWB-P7-E2014-CON | GAP-2388 | find it | Add three rows for the notice decision operations declared as Litigation right A with scope applied, enforced at gateway-bff through rwb-access; rwb-decision calls them with its service identity, approver user identifier and decision entry reference. |

### OTHER:TSD P7 v2, traceability table T8 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12379 | RWB-P7-E2014-CON | GAP-1263 | 18 | Keep REQ-APD-002 and REQ-APD-006 on FEAT-APD-08 with RWB-E2-014 for the screen and FEAT-APD-01 with RWB-E2-013 for routing; correct the T8 rows. |

### OTHER:Edge and gateway design (gateway-bff screen contracts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12380 | RWB-P7-E2014-CON | GAP-1621 | 15 | Fix which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations and record the four screen contracts there. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12381 | RWB-P7-E2014-CON | GAP-1262 | 12.3 | Publish the decided outcome on rwb.decision-record.v1 through the local library (DP-03); retire ApprovalDecided from the slide 14 line or add it to the catalogue with its consumers. |

### OTHER:TSD P6 v2 T3.2 (rwb-case reference data) or rwb-comms contract value set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12382 | RWB-P7-E2014-CON | GAP-2391 |  | Add LOV-HOLD-REASON with REFUSED_BY_APPROVER and TEMPLATE_WITHDRAWN to rwb-case reference data, or publish the same two values as the rwb-comms value set. Keep rwb.decision.notice-approval read by both services until the platform feature-flag owner renames it. |

### OTHER:rwb-case contract and FSD P7 acceptance criteria A2.15 and A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12393 | RWB-P7-E2014-OPS | GAP-1623 |  | Record the preferred option: P3 moves the case state and raises the task on ApprovalRequested, with one writer of the case state. |

### RWB-P6-E1052-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12397 | RWB-P7-E2014-OPS | GAP-1264 |  | Publish the notice decision operations (approve, regenerate, hold) with their states and error codes, and correct the Ownership Map rows. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12399 | RWB-P7-E2014-OPS | GAP-0398 |  | Record the recommended resolution: the integration lead agrees the composite decision-screen route and merge order with the platform edge owner, and the fixture set, SIT environment, evidence format, retention and 16:00 pass/fail gate with QA at the wave 2 entry check. Owner role: Integration lead. |

### OTHER:Recovery Workbench TSD P6 v2 (T-A.1 and T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12404 | RWB-P7-E2014-OPS | GAP-2388 |  | Add the three notice operations as Litigation right A with scope applied, enforced at gateway-bff via rwb-access; rwb-decision calls with its service identity plus approver user identifier. |

### OTHER:Recovery Workbench TSD P6 v2 T4 and FSD P6 v3 A2.1.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12405 | RWB-P7-E2014-OPS | GAP-2390 |  | A notice move writes one local decision record via the library with code D7.1, rule, IDs, template code and version, states, reason, approver and approval entry reference. |

### RWB-P7-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12407 | RWB-P7-E2014-OPS | GAP-1265 |  | Add RWB-P1-E1015-CON and RWB-P3-E1018-CON as C rows, or record both reads as route-level composites of RWB-PLT-N001-CON. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:PRD of EP05 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12409 | RWB-P7-E2014-OPS | GAP-2742 | 3 | Carry the P6 notice generate and send and the rwb-case answer as non-blocking C rows; record notice and template row ownership; name the P6 and case operations; add REQ-S4-001 to the key trace; decide the D7.1 approval conflict in the EP05 PRD. |

### OTHER:Edge and gateway-bff design (solution architect and platform edge owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12413 | RWB-P7-E2014-OPS | GAP-1621 |  | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service and record the four screen contracts there |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:slides 41 to 43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12414 | RWB-P7-E2014-OPS | GAP-1262 |  | Publish the decided outcome on rwb.decision-record.v1 via DP-03 and retire ApprovalDecided from the slide 14 line or add it to the catalogue |

### OTHER:Platform observability owner (ASM-2235) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12416 | RWB-P7-E2014-OPS | DOR-RWB-P7-E2014-OPS / GAP-1271 | 7 | Restored 'Not specified in the source documents (GAP-1271; ASM-2235)' for the alert thresholds and the empty-queue window in AC6. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:platform feature-flag owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12417 | RWB-P7-E2014-OPS | GAP-2391 |  | Add LOV-HOLD-REASON with REFUSED_BY_APPROVER and TEMPLATE_WITHDRAWN; keep flag rwb.decision.notice-approval read by both services until renamed |

### OTHER:TSD P7 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12425 | RWB-P7-E2017-APP | CG-ALL-7216 | 3, 5, 7, 13 | Record tr_declog_append_only in T3.1 as the append-only trigger of decision_log_entry, a database object, not an LDM field. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12429 | RWB-P7-E2017-APP | DOR-RWB-P7-E2017-APP-11 | 9, 10 | Confirm the personal-data class of the entry fields the story carries, including the reason and identifiers; align the guardrail statement. |

### OTHER:TSD P4 (T6.1 RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12432 | RWB-P7-E2017-APP | GAP-0942 | 13 | Add Documents column: RW-RESTRUCT CRU, RW-CASEOWN CRU, RW-TEAMMGR R, RW-LEGAL CRUA; confirm with matrix owner; publish in PM-2026.12 pack via RWB-P4-AD002-APP. |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12434 | RWB-P7-E2017-APP | GAP-1580 | header | Add a generation section stating REQ-DCM-012 with FR-P5-026 and AC-P5-019 covering generation from approved templates with no re-keying. |

### OTHER:TSD P6 v2 (T-A.2; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12435 | RWB-P7-E2017-APP | GAP-2392 | 13 | Add treatment-type and product-group filters to API-P6-003; add application/json to API-P6-005; add locked attribute to merge_field; publish set rows in RWB-P3-E1043-CON; copy five message texts when issued. |

### OTHER:TSD P4 appendix T-A and T6.2; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12436 | RWB-P7-E2017-APP | GAP-0941 | 13 | Publish POST /authorise with request and answer schema, carry it on RWB-P4-E1037-CON with a stub, fix the rwb-access login, and state the service identity scope rule. |

### RWB-P5-E2017-CON; OTHER:rwb-case parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12437 | RWB-P7-E2017-APP | GAP-1278 | 13 | Publish the DecisionRecorded payload field set on rwb.decision-record.v1 and the parameter names of the page-size bound and completeness target; the story already reads the final call from the list. |

### OTHER:TSD S2 v2 (T3.1; RWB-S2-E2026-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12438 | RWB-P7-E2017-APP | GAP-2697 | 15 | Publish the treatment-read panel section as an optional additive property with its property names and action vocabulary; take the set read from RWB-P5-E2017-CON with a 2 s budget and a fake; keep names provisional until frozen. |

### RWB-S2-E2026-APP; RWB-P5-E2017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12441 | RWB-P7-E2017-APP | GAP-1704 | 3 | Request generation, review and signature through the P5 and P6 contracts, hold the document reference on the treatment, and keep no document content in schema rwb_treatment. |

### RWB-P5-E2017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12442 | RWB-P7-E2017-APP | GAP-1017 | 3 | Declare the seven generation-screen operations on /api/recovery/document/v1, map regenerate to API-P5-017, fix the send and signature paths and field names, and map failures to one envelope. |

### RWB-PLT-N001-CON; OTHER:ledger decision-code list (document not named in source) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12443 | RWB-P7-E2017-APP | GAP-0944 | 9 | Publish the composite route field list for SCR-14 Treatment record and SCR-30 Case documents, and add the allowed-action decision code (for a correction or a send) to the ledger decision-code list. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12447 | RWB-P7-E2019-APP | DOR-RWB-P7-E2019-APP-8 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log and GET /api/recovery/decision/v1/decision-log/{entryId} in rwb-decision.yaml; publish POST /api/recovery/access/v1/authorise in rwb-access.yaml. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12448 | RWB-P7-E2019-APP | GAP-1844 | header | Place the creation of service RWB-SVC-P7 (rwb-decision) in wave 2 with RWB-S9-E2019-APP so this story's wave 2 slice has its service. |

### OTHER:Wave 2 partner harness pack and partner gateway test route (platform edge team and QA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12449 | RWB-P7-E2019-APP | GAP-0403 | header | Record the partner gateway test route and its FAPI 2.0 profile, the partner directory test tenant, how a token with the amr claim is obtained, the harness seeding of three firms and four partner identities, the evidence format and retention, and the pass/fail gate. Values not specified in source documents (GAP-0403). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; OTHER:TSD P7 v2 appendix T-A.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12451 | RWB-P7-E2019-APP | GAP-1272 | 8 | Fix the record path, the partnerId and date-range query parameters, the entry composition, the result vocabulary, the page-size bound parameter and the two index names. Values not specified in source documents (GAP-1272). |

### OTHER:Backlog split plan (P4 epic; OTHER:Epic 2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12452 | RWB-P7-E2019-APP | GAP-1573 | header | Create the Epic 2 story for REQ-ACA-011 with the group-change scenario, session re-resolution, reallocation hand-off to rwb-case and leaver response time; answer DL38 and DL40. Values not specified in source documents. |

### OTHER:Split plan (partner identity allocation) and FSD S9 Existing capability check (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12453 | RWB-P7-E2019-APP | GAP-1852 | header | Record that P4 keeps the internal role model, the gateway enforces the external identity, and S9 holds the partner_user binding scoping a partner user to one firm and one partner role. |

### RWB-P4-E2019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12455 | RWB-P7-E2019-APP | GAP-3181 | 3 | Move the partner_user DDL, its migration and the reference load handler to the S9 rwb_partner sequence; keep session, role and scope checks in rwb-access |

### RWB-P4-E2019-CON; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12456 | RWB-P7-E2019-APP | GAP-0784 | 3 | Register the partner identity resolution operation with its path, claim names, answer field names and PLACED scope type; state the lifetime of a resolved answer against the partner edge token lifetime |

### OTHER:Partner gateway security design decision; OTHER:Service Catalog and gateway runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12457 | RWB-P7-E2019-APP | GAP-1395 |  | Fix DMZ zone design, gateway product and version, client authentication method, token lifetimes, external IdP, certificate lifecycle, rate limits, WAF rule set and DR objectives in the security design authority review |

### RWB-P7-E2019-APP; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12458 | RWB-P7-E2019-APP | CG-ALL-7238 | 18 | Align the REQ-ACA-012 test list in RTM v7 with section 18 in its next version; section 18 reads TC-E2-019-01 to TC-E2-019-12 |

### RWB-P4-E2019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12459 | RWB-P7-E2019-APP | GAP-1567 | 3 | Drop lov_value and partner_user from T3.1; keep lists of values in TSD P3 and partner identity in TSD S9; state the rwb-access read path, versions and refresh rate |

### RWB-PLT-N007-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12460 | RWB-P7-E2019-APP | GAP-0786 |  | Extend the certificate profile and rotation window to the rwb-access hop; record the per-client limit, burst and window for the resolution route; publish the rwb-access namespace, service and port |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0067 | Wave conflict S9 / EP02 | Tech lead | Resolved (directive) |
| GAP-0397 | Approval-routing harness environment, composite queue route and evidence format are not specified | Integration lead | Resolved (directive) |
| GAP-0398 | Integration harness values for the D7.1 decision-screen journey are not specified | Integration lead | Resolved (directive) |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0403 | The external partner gateway test route and the partner harness pack are not specified | Integration lead | Resolved (directive) |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0784 | The partner identity resolution operation, its claim set, its answer schema, the scope type PLACED and the lifetime of an answer are specified by no source | Solution architect, P4 rwb-access with the external gateway owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0785 | The contract of the partner identity resolution names no path, no claim or answer field, no refusal-to-status mapping and no statement of its absent events in any source | Tech lead of rwb-access with the external gateway owner and the rwb-partner service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0786 | The certificate profile, the rotation and revocation of the rwb-access hop, the numeric rate limit and the namespace and service names of the DMZ hop are specified by no source | SCB IT infrastructure with the security design authority | Resolved (directive) |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
| GAP-0928 | GET /doa-limits is named in Architecture v5 and API v3 but absent from API Specification v4 | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0929 | The DoA lookup and authority-decision request and response shape is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0930 | The scope of the rwb-decision service identity inside rwb-access is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0932 | The request and response shape of the authorise operation is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0941 | rwb-access document set: the authorise request and answer shape for the document screens, and the scope a service identity is asked for, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0944 | rwb-access document set: the composite route field list of SCR-14 and SCR-30, and the decision code of an allowed screen action entry, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1017 | The generation-screens baseline fixes six operations and four shapes that no source names, two conflicting legacy paths, the field names of the request and answer objects, and a status mapping the legacy section 12 states only in prose | Tech lead of rwb-document, with the solution architect and the rwb-comms owner | Resolved (directive) |
| GAP-1220 | The template code, channel, notice kind, state vocabulary, retry limit, template owner and MSG-GEN-006 text of the escalation notice are not specified in any source | Solution architect | Resolved (directive) |
| GAP-1221 | The event catalogue lists gateway-bff as the only consumer of ApprovalRequested and carries no ApprovalEscalated event, yet this story also consumes the event for the escalation notice | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1222 | No source names the notice and message operations or the notice fields that carry an approval reference, an escalation level, a recipient and a sent time | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1251 | The delegation of authority table is P4 rwb-access's while the routing rules and the approval resource are P7 rwb-decision | Solution architect | Resolved (directive) |
| GAP-1252 | The delegation limits operation has no row in the Ownership Map API catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1254 | The data lake copy of the decision record is removed under DP-17 while the legacy log path streams to it | Solution architect | Resolved (directive) |
| GAP-1255 | The request and answer field lists of the five approval operations and the case-status operation are not enumerated in any source | Tech lead of rwb-decision with the Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1256 | The delegation snapshot and its cache refresh have no named operation, store or interval | Solution architect | Resolved (directive) |
| GAP-1257 | ApprovalDecided is named on the service contract slide but has no event catalogue row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1258 | The field-level list and the mask flags of the D7.1 approval screen are published by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1259 | The composite-route name and path segment of the approval screen are not specified | Solution architect | Resolved (directive) |
| GAP-1262 | ApprovalDecided is named on the slide 14 contract line but has no event-catalogue row | Solution architect | Resolved (directive) |
| GAP-1263 | REQ-APD-002 and REQ-APD-006 are mapped to two different features and stories | Business analyst | Resolved (directive) |
| GAP-1264 | The three notice operations of the legacy NoticeApi have no owner path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1266 | The field types and order of the screen model and the queue paging defaults are not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1267 | The legacy screen states and the platform route states are two unreconciled vocabularies | Business analyst | Resolved (directive) |
| GAP-1268 | The notice summary excludes the PDF body and the addressee that the legacy screen shows | Data steward | Resolved (directive) |
| GAP-1270 | The timeout budget of a screen that composes three reads is not specified | Solution architect | Resolved (directive) |
| GAP-1271 | The dashboard names, the alert thresholds and the empty-queue window are not specified | DevOps engineer | Resolved (directive) |
| GAP-1272 | The partner access decision record has no operation, no field composition and no result vocabulary in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1273 | The append path of a partner access record is read synchronously while Arch v5 names it as a consumed event | Solution architect and integration lead | Resolved (directive) |
| GAP-1278 | The record payload, the reference shapes and the correction final call of the RWB-E2-017 decision slice have no source | Solution architect | Resolved (directive) |
| GAP-1395 | DMZ network design, gateway product, FAPI 2.0 settings, external identity provider, certificate lifecycle, rate limits, WAF rule set and DR target of the partner gateway are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1573 | The joiner, mover and leaver capability has a Must requirement in Epic 2, a feature code in Epic 1 and no legacy story, and its response times are open under DL38 | Business analyst with the security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1621 | Four screens are attributed to P7 while the edge ruling composes every screen in gateway-bff | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1844 | Two S9 stories sit in wave 2 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1852 | Partner identity is a table in rwb_partner while the requirement that governs it is delivered by rwb-access | Security administrator with the P4 and S9 owners | Resolved (directive) |
| GAP-2093 | The notice approval sits in P6, P7 and S4 at once | Service owners of P6 rwb-comms, P7 rwb-decision and S4 rwb-litigation | Resolved (directive) |
| GAP-2216 | No source fixes the case-facts field list behind the D7.1 approval screen, the names of the two approval outcome events, the naming of the redress task, or the business date of the postal address input | Solution architect | Resolved (directive) |
| GAP-2384 | The three notice decision operations of the D7.1 approval have no REST row in the Ownership Map or in appendix T-A | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2385 | The notice table has no column for the decision entry reference that the approve and hold calls carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2386 | No source says whether a change of template variant replaces the notice row or creates a new version of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2387 | The notice answer has no field list, and the template state the approval panel must show is not part of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2388 | The declared right of the three notice decision operations is not in the endpoint inventory or the RBAC matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2390 | No source says whether a notice move writes its own decision record or only references the approval entry of rwb-decision | Solution architect | Resolved (directive) |
| GAP-2391 | The hold reason vocabulary has no list of values, and the owner namespace of the feature switch is not settled for the comms half | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2697 | The treatment-side panel section, its properties and action vocabulary, the treatment-type document set row and the one-hop set read are not specified | Solution architect | Resolved (directive) |
| GAP-2698 | The legacy files the whole generation capability under the document module, while the target gives the treatment screen leg to rwb-treatment and the set to rwb-document | Solution architect | Resolved (directive) |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3147 | EP02 wave 2 for rwb-partner while the service's Architecture v5 wave is 4 | Solution architect | Resolved (directive) |
| GAP-3148 | The rwb-partner slice of the key has no published load path, no message per condition and no partner_user catalogue | Solution architect with the reference data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3181 | The partner_user table is created by P4 in the story and owned by S9 in the ownership map | Access lead with the partner lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
