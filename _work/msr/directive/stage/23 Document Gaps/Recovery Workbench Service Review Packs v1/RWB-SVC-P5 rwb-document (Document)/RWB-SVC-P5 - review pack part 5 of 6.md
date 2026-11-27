# RWB-SVC-P5 rwb-document (Document) - review pack, part 5 of 6 (RWB-P5-E1057-INF to RWB-P5-E2018-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 163 |
| Cross-document (pending in another document) | 188 |
| Not applied (value not in the sources) | 16 |
| Open business decisions | 40 |
| Register gaps linked | 105 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P5-E1057-INF | 14 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1057 INF Intake from branches, mailroom, partner SFTP and email - infrastructure v2.md |
| RWB-P5-E1057-OPS | 17 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1057 OPS Intake from branches, mailroom, partner SFTP and email - deployment v2.md |
| RWB-P5-E1062-APP | 14 | 28 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1062 APP Deviation screening agent in shadow [E2b] v2.md |
| RWB-P5-E1065-APP | 20 | 32 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1065 APP Sandbox database with synthetic recovery data v2.md |
| RWB-P5-E1067-APP | 18 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1067 APP Every Workbench action into the interaction ledger v2.md |
| RWB-P5-E2016-APP | 17 | 9 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2016 APP Full case record view with the history timeline v2.md |
| RWB-P5-E2017-APP | 22 | 25 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2017 APP Contract, CA and mortgage document generation screens v2.md |
| RWB-P5-E2017-CON | 14 | 28 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2017 CON Contract, CA and mortgage document generation screens - contract v2.md |
| RWB-P5-E2018-APP | 27 | 25 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E2018 APP E-signature flow for customers and the bank v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P5-E1062-APP | R-01566 | CG-ALL-6093 | Script gap | Product owner | The story adds DEATH_CERTIFICATE to the closed list LOV-DOC-SOURCE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01568 | CG-ALL-6104 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-CUSTODY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01569 | CG-ALL-6105 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-CUSTODY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01570 | CG-ALL-6106 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-DOC-SOURCE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01571 | CG-ALL-6107 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-DOC-SOURCE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01572 | CG-ALL-6108 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-EXTRACT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01573 | CG-ALL-6109 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-EXTRACT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01574 | CG-ALL-6110 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-INTAKE-MATCH | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01575 | CG-ALL-6111 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-INTAKE-MATCH | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01576 | CG-ALL-6112 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-INTAKE-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01577 | CG-ALL-6113 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-INTAKE-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01578 | CG-ALL-6114 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-OCR-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01579 | CG-ALL-6115 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-OCR-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01580 | CG-ALL-6116 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01581 | CG-ALL-6117 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-REVIEW | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01582 | CG-ALL-6118 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-SCAN-RESULT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01583 | CG-ALL-6119 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-SCAN-RESULT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01584 | CG-ALL-6120 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-STAGE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1065-APP | R-01585 | CG-ALL-6121 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-STAGE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E2018-APP | R-01607 | CG-ALL-6180 | Script gap | Product owner | The story adds GET to the closed list LOV-SIGN-METHOD | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E2018-APP | R-01608 | CG-ALL-6181 | Script gap | Product owner | The story adds GET to the closed list LOV-SIGN-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1062-APP | R-10928 | CG-ALL-6100 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1067-APP | R-10932 | CG-ALL-6133 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2017-APP | R-10933 | CG-ALL-6157 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2017-CON | R-10937 | CG-ALL-6176 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E2018-APP | R-10941 | CG-ALL-6192 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1057-ITG, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-P5-E1057-APP, RWB-P5-E1057-CON, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-S9-E1057-APP | R-22197 | GAP-3146 | Register gap | Business lead; solution architect; rwb-partner tech lead; rwb-access owner; programme lead | RWB-S9-E1057-APP: the split plan gives this secondary slice no legacy criterion and no build row while the P5 slice of the same key hands the partner criteria to it, no source publishes a partner-by-code read or the code filter of GET /partners, the two refusal reasons and the not-found behaviour are not published, the constraint on partner_code and the panel transition table are not specified, the DP-07 rows cannot be carried in an empty H row, and EP01 wave 1 is earlier than the service wave 4 | Serve the partner panel read as the code filter of the published GET /partners under base /api/recovery/partner/v1 with right R and the scope applied, answer the six published properties from partner in rwb_partner, answer an empty list for an unknown code and the stored panel status for a partner that is not ACTIVE, leave BR4 and the two reasons with the caller, read LOV-PANEL and LOV-PARTNER-TYPE through DP-07, write nothing and publish nothing, keep wave 1 and record the DP-07 rows, the constraint on the partner code, the panel transition table and the criteria assignment of the two slices as open items. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1039-APP, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22216 | GAP-2330 | Register gap | Internal audit role and the solution architect, P4 | The access entry of an agent read has no source row, element list or decision-code vocabulary of its own | Fix the entry members of a non-human read in the access-entry writer of RWB-P4-E1039-APP and publish them once for every service identity, so an audit query by agent code and policy version answers from the same chain as the screen entries. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22221 | GAP-2328 | Register gap | Compliance and PDPA officer and the security administrator role | Which of the run's fields are personal for a non-human actor, and the mask format served to an agent, are not specified | Fix the personal field list of the four agent reads and the mask format served to a non-human caller with the masking owner, load it as a masking version rather than as code, and prove it with a synthetic value that must appear in no answer, no log and no span. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22514 | GAP-0943 | Register gap | Compliance and PDPA officer | rwb-access document set: the masking version in force for SIT and the field IDs of the personal fields on the review view are not specified | Fix the mask version label per environment in the policy pack load, publish the field IDs of a generated contract and its parties with the LDM, and have the pack owner confirm the DF-PTY-007 and DF-PTY-016 rows before SIT. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22516 | GAP-1582 | Register gap | Legal counsel | E-discovery and court-ready evidence have no FSD feature, no operation and no response target | FR-P5-028, FR-P5-029 and AC-P5-021 carry the behaviour with the response target left open as OQ-P5-09. A discovery operation and its response target are needed before wave 2 acceptance. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E1023-ITG, RWB-ITG-E2016-ITG, RWB-P3-E1023-APP, RWB-P3-E1023-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P4-E1023-APP, RWB-P5-E2016-APP, RWB-S8-E1023-APP | R-28538 | GAP-1577 | Register gap | Business analyst with the P3 product owner | The case record view and its history timeline are listed as P4 features while the screen and its endpoints belong to rwb-case | Move FEAT-ACA-11 and FEAT-ACA-12 with their acceptance criteria to FSD P3 in the next version, and leave in FSD P4 only the authorise, scope and masking behaviour the screen consumes, so each feature has one owner and one acceptance set. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E2016-ITG, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P5-E2016-APP | R-28783 | GAP-1062 | Register gap | Data steward and data product owner | Which table supplies the document type label a timeline item shows | Display the label from document_type at the version in force, label_en by default and label_th by locale, and compare the list with LOV-DOC-TYPE through the reference-data contract of rwb-case rather than copying it; fall back to the type code when the row of that version is absent. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-P5-E2016-APP | R-37066 | ASM-2010 | Register assumption |  | The document type label shown on an item is read from document_type in rwb_document at the version in force, label_en by default and label_th by locale, the list is compared with LOV-DOC-TYPE through the reference-data contract of rwb-case and never copied, and a type code with no row in that version shows as its code. | Data steward and data product owner with the P5 business analyst |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P5-E1062-APP | R-17379 | DOR-RWB-P5-E1062-APP-8 | 12.1 | Definition of Ready item 8 Contract: Partial | 401/404 placeholders set in §12.1 (CG-ALL-6095). Payload differs from Kafka Catalog v1, under CG-ALL-6097, outside this chunk; contract stays partial. |
| RWB-P5-E1062-APP | R-25868 | CG-ALL-6101 | 3.1 | Flyway file V1062_1__agent_input_read.sql is not in the V0001..Vnnnn form | Next V-number for rwb-document is not in the sources (CG-ALL-6101). Service Template §3.1 gives only the V0001 to Vnnnn rule. Solution architect to supply. |
| RWB-P5-E1062-APP | R-31191 | NEWAC-RWB-P5-E1062-APP-AC10 | 8 | AC10: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so AC10 and its test row cannot be placed. Proposed test is Not specified (NEWAC-RWB-P5-E1062-APP-AC10). |
| RWB-P5-E1065-APP | R-25873 | CG-ALL-6127 | 3 | Flyway file V1065_1__document_estate_seed.sql is not in the V0001..Vnnnn form | Migration name V1065_1__document_estate_seed.sql is not in the story text given; next rwb-document Flyway number not in sources (Not specified in the source documents (CG-ALL-6127)). |
| RWB-P5-E2016-APP | R-22508 | GAP-0400 |  | Gateway-bff composite timeline route, harness environment and evidence gate are not specified | Route path, merge order, fixture seeding, SIT environment, evidence format, retention and gate method are in no source (searched stage Technical Specifications and Template Spec). Owner: integration lead. |
| RWB-P5-E2016-APP | R-25885 | CG-ALL-6142 | 3 | Flyway file V2016_1__document_timeline_index.sql is not in the V0001..Vnnnn form | Next Flyway number for rwb-document is not in the sources (searched Template Spec v2 §3.1, ADR-021, TSD P5 v4). Migration name not in the supplied story text; no invented number. |
| RWB-P5-E2017-APP | R-28785 | GAP-1017 | 12 | The generation-screens baseline fixes six operations and four shapes that no source names, two conflicting legacy paths, the field names of the request and answer objects, and a status mapping the legacy section 12 states only in prose | Section 12 operations, fields, envelope and the legacy field list are not in the chunk, and the working copy was not found. Fix also cites ASM-113 to ASM-116, which I cannot create here. |
| RWB-P5-E2017-CON | R-17415 | DOR-RWB-P5-E2017-CON-10 | 13 | Definition of Ready item 10 Screens and states: Partial | Section 13 text is not in the chunk, so SCR-14 and SCR-30 state text cannot be anchored. Empty, loading, error and no-access values are in no source; none written. |
| RWB-P5-E2017-CON | R-17419 | DOR-RWB-P5-E2017-CON-4 | 7; 16 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 text is not in the chunk, so no anchor exists for BR1 to BR12 AC and TC rows. The next free AC number is unverified; none invented. |
| RWB-P5-E2017-CON | R-22515 | GAP-1278 | 12.3 | The record payload, the reference shapes and the correction final call of the RWB-E2-017 decision slice have no source | Section 12.3 text is not in the chunk, so the placeholder cannot be anchored. Final call, reference shapes and parameter names need the P5 contract and reference data. |
| RWB-P5-E2017-CON | R-22517 | GAP-2697 | 7; 12 | The treatment-side panel section, its properties and action vocabulary, the treatment-type document set row and the one-hop set read are not specified | Sections 7 and 12 text is not in the chunk, so no anchor exists for the panel section, set read or action vocabulary. Names stay provisional until the contract is frozen. |
| RWB-P5-E2017-CON | R-22518 | GAP-2698 | 13 | The legacy files the whole generation capability under the document module, while the target gives the treatment screen leg to rwb-treatment and the set to rwb-document | Section 13 text is not in the chunk, so the placement and no-decision-record statement cannot be anchored. Nothing written. |
| RWB-P5-E2017-CON | R-22525 | GAP-1186 | 12; 12.8 | The signed PDF object and the byte transfer into the P5 write-once store are not specified | Sections 12 and 12.8 text is not in the chunk, so the transport statement and fake cannot be anchored. No source fixes the transport choice; none invented. |
| RWB-P5-E2018-APP | R-22526 | GAP-0402 |  | The e-signature harness pack and the EasyApp test route are not specified | EasyApp test tenant, route, harness, seeding and evidence values are in no source read (story text, architecture extract, ownership.json). Needs agreement with the ACE team and QA. No edit. |
| RWB-P5-E2018-APP | R-25901 | CG-ALL-6193 |  | Flyway file V2018_1__signature_request.sql is not in the V0001..Vnnnn form | Next number of the service Flyway sequence is in no source. The file name sits in section 13, outside this chunk. Cited L374 is the DP-05 row, not the migration name. |
| RWB-P5-E2018-APP | R-25902 | CG-ALL-6194 |  | Flyway file V2_018__signature_request.sql is not in the V0001..Vnnnn form | Same as CG-ALL-6193: next Flyway number is in no source. File name is in section 13, outside this chunk. Cited L374 is the DP-05 row. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (29)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10167 | RWB-P5-E1057-INF | CG-ALL-6082 | 12.1 | Remove any path attributed to RWB-P5-E1057-INF, or publish the admin operations through RWB-P5-E1057-CON, which owns them. |
| CDC-10171 | RWB-P5-E1057-INF | DOR-RWB-P5-E1057-INF-8 | 12.1 | Remove any path attributed to RWB-P5-E1057-INF, or publish the admin operations through RWB-P5-E1057-CON, which owns them. |
| CDC-10181 | RWB-P5-E1057-OPS | CG-ALL-6086 | 12.1 | Publish the three admin operations (GET and POST under /api/recovery/document/v1/admin/jobs) through RWB-P5-E1057-CON, or remove them from 12.1. |
| CDC-10273 | RWB-P5-E2017-APP | CG-ALL-6146 | 12.1 | Publish GET /api/recovery/document/v1/cases/{caseId}/generated-documents in rwb-document.yaml through RWB-P5-E2017-CON. Story unchanged. |
| CDC-10274 | RWB-P5-E2017-APP | CG-ALL-6147 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId}/merge-values in rwb-document.yaml through RWB-P5-E2017-CON. Story unchanged. |
| CDC-10275 | RWB-P5-E2017-APP | CG-ALL-6148 | 12.1 | Publish POST /api/recovery/document/v1/documents/{documentId}/regenerate in rwb-document.yaml through RWB-P5-E2017-CON. Story unchanged. |
| CDC-10276 | RWB-P5-E2017-APP | CG-ALL-6149 | 12.1 | Publish POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send in rwb-document.yaml through RWB-P5-E2017-CON. Story unchanged. |
| CDC-10277 | RWB-P5-E2017-APP | CG-ALL-6150 | 12.1 | Publish POST /api/recovery/document/v1/treatments/{treatmentId}/signature-requests in rwb-document.yaml through RWB-P5-E2017-CON. Story unchanged. |
| CDC-10278 | RWB-P5-E2017-APP | CG-ALL-6151 | 12.1 | Publish GET /api/recovery/document/v1/signature-requests in rwb-document.yaml through RWB-P5-E2017-CON. Story unchanged. |
| CDC-10279 | RWB-P5-E2017-APP | CG-ALL-6152 | 12.1 | Publish PATCH /api/recovery/document/v1/signature-requests/{requestId} in rwb-document.yaml through RWB-P5-E2017-CON. Story unchanged. |
| CDC-10280 | RWB-P5-E2017-APP | CG-ALL-6153 | 12.2 | Publish POST /api/recovery/document/v1/documents/{documentId}/store in rwb-document.yaml through the provider's CON story. Story unchanged. |
| CDC-10281 | RWB-P5-E2017-APP | CG-ALL-6154 | 12.1 | Remove the fixed enum on reviewStatus; the value set is data from Reference Data v5 LOV-REVIEW. Story unchanged. |
| CDC-10286 | RWB-P5-E2017-APP | DOR-RWB-P5-E2017-APP-8 | 12.1 | Add the Idempotency-Key header to the four listed operations and add the listed P1 paths missing from the yaml. |
| CDC-10298 | RWB-P5-E2017-CON | CG-ALL-6163 | 12.1 | Publish GET /api/recovery/document/v1/cases/{caseId}/generated-documents as an operation on the path, alongside POST. |
| CDC-10299 | RWB-P5-E2017-CON | CG-ALL-6164 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId}/merge-values in rwb-document.yaml. |
| CDC-10300 | RWB-P5-E2017-CON | CG-ALL-6165 | 12.1 | Publish POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send in rwb-document.yaml. |
| CDC-10301 | RWB-P5-E2017-CON | CG-ALL-6166 | 12.1 | Publish POST /api/recovery/document/v1/treatments/{treatmentId}/signature-requests in rwb-document.yaml. |
| CDC-10302 | RWB-P5-E2017-CON | CG-ALL-6167 | 12.1 | Publish GET /api/recovery/document/v1/signature-requests in rwb-document.yaml. |
| CDC-10303 | RWB-P5-E2017-CON | CG-ALL-6168 | 12.1 | Publish PATCH /api/recovery/document/v1/signature-requests/{requestId} in rwb-document.yaml. |
| CDC-10304 | RWB-P5-E2017-CON | CG-ALL-6169 | 12.2 | Publish POST /api/recovery/document/v1/documents/{documentId}/store in rwb-document.yaml, as the provider of the consumed row. |
| CDC-10305 | RWB-P5-E2017-CON | CG-ALL-6170 | 8 | Remove the closed enum on reviewStatus so LOV-REVIEW values are data; the story keeps LOV-REVIEW as data. |
| CDC-10308 | RWB-P5-E2017-CON | DOR-RWB-P5-E2017-CON-8 | find it | Add GET /cases/{caseId}/generated-documents, GET /documents/{documentId}/merge-values, POST /cases/{caseId}/generated-documents/send, POST /treatments/{treatmentId}/signature-requests and the five more listed |
| CDC-10326 | RWB-P5-E2018-APP | CG-ALL-6184 | 12.1 | Publish POST /api/recovery/document/v1/cases/{caseId}/signature-requests in the yaml, as 12.1 describes it. |
| CDC-10327 | RWB-P5-E2018-APP | CG-ALL-6185 | 12.1 | Publish GET /api/recovery/document/v1/cases/{caseId}/signature-requests in the yaml, as 12.1 describes it. |
| CDC-10328 | RWB-P5-E2018-APP | CG-ALL-6186 | 12.1 | Publish GET /api/recovery/document/v1/signature-requests/{requestId} in the yaml, as 12.1 describes it. |
| CDC-10329 | RWB-P5-E2018-APP | CG-ALL-6187 | 12.1 | Publish GET /api/recovery/document/v1/signature-requests in the yaml, as 12.1 describes it. |
| CDC-10330 | RWB-P5-E2018-APP | CG-ALL-6188 | 12.1 | Publish PATCH /api/recovery/document/v1/signature-requests/{requestId} in the yaml, as 12.1 describes it. |
| CDC-10332 | RWB-P5-E2018-APP | DOR-RWB-P5-E2018-APP-21 | header | Publish the signature-request operations (CG-ALL-6184 to CG-ALL-6188) so a contract exists for this story. |
| CDC-10333 | RWB-P5-E2018-APP | DOR-RWB-P5-E2018-APP-8 | 12.1 | Add paths POST /cases/{caseId}/signature-requests, GET /cases/{caseId}/signature-requests, GET /signature-requests/{requestId}, GET /signature-requests and the two further paths in the detcheck. |

### Epic design record (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10168 | RWB-P5-E1057-INF | DOR-RWB-P5-E1057-INF-14 | find it | Record the signed epic design sign-off, or confirm where it is held. |
| CDC-10182 | RWB-P5-E1057-OPS | DOR-RWB-P5-E1057-OPS-14 | not in the supplied story parts | Record the signed epic design sign-off for EP01 in the epic design record; the story does not record a sign-off. |
| CDC-10194 | RWB-P5-E1062-APP | DOR-RWB-P5-E1062-APP-14 | none | Record the signed epic design sign-off in the epic design record. |
| CDC-10222 | RWB-P5-E1065-APP | DOR-RWB-P5-E1065-APP-14 | none | Record the signed epic design sign-off for this story's epic |
| CDC-10253 | RWB-P5-E1067-APP | DOR-RWB-P5-E1067-APP-14 |  | Record the signed epic design sign-off for EP01 in the epic design record |
| CDC-10264 | RWB-P5-E2016-APP | DOR-RWB-P5-E2016-APP-14 | header | Record the signed epic design sign-off for RWB-P5-E2016-APP. |
| CDC-10307 | RWB-P5-E2017-CON | DOR-RWB-P5-E2017-CON-14 | find it | Record the signed sign-off of the epic design for EP02 and link it to this story |
| CDC-10331 | RWB-P5-E2018-APP | DOR-RWB-P5-E2018-APP-14 | header | Record the signed epic design sign-off for this story in the epic design record. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10179 | RWB-P5-E1057-INF | CG-ALL-6084 | 18 | Align the REQ-DCM-009 and REQ-DCM-010 test cases to section 18 of RWB-P5-E1057-INF. |
| CDC-10192 | RWB-P5-E1057-OPS | CG-ALL-6090 | 18 | Align the REQ-DCM-009 and REQ-DCM-010 test lists between section 18 and RTM v7 in their next versions. |
| CDC-10214 | RWB-P5-E1062-APP | CG-ALL-6099 | 18 | Align the RTM test lists for REQ-DVH-001, REQ-DVH-003 and REQ-DVH-007 with section 18 of this story in the next RTM version. |
| CDC-10243 | RWB-P5-E1065-APP | CG-ALL-6126 | 18 | Align the REQ-RDF-001 and REQ-RDF-010 test lists with section 18 of RWB-P5-E1065-APP in the next version. |
| CDC-10269 | RWB-P5-E2016-APP | CG-ALL-6141 |  | Align trace lists for REQ-WKM-008, REQ-OCC-008 and REQ-CWC-016 with section 18 of RWB-P5-E2016-APP in the next RTM version. |
| CDC-10295 | RWB-P5-E2017-APP | CG-ALL-6156 | 18 | Align the test-case lists of the three differing requirements (REQ-DCM-012, REQ-OCC-002 and the third) with section 18 of RWB-P5-E2017-APP. |
| CDC-10306 | RWB-P5-E2017-CON | DOR-RWB-P5-E2017-CON-12 | 12.7, 16, 18 | AC8 and boundary rows added in sections 12.7 and 16; section 18 left for the RTM check |
| CDC-10323 | RWB-P5-E2017-CON | CG-ALL-6175 | 18 | Align the REQ-DCM-012 and REQ-OCC-002 test lists with section 18 of RWB-P5-E2017-CON in the next RTM version. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10178 | RWB-P5-E1057-INF | CG-ALL-6083 | 16 | Add rows TC-P5-E1057-INF-01 to TC-P5-E1057-INF-06 with Given, When and Then copied from the criteria they cover. |
| CDC-10191 | RWB-P5-E1057-OPS | CG-ALL-6089 | 16 | Add rows for TC-P5-E1057-OPS-01 to TC-P5-E1057-OPS-06 with Given, When and Then copied from the criterion each covers. |
| CDC-10227 | RWB-P5-E1065-APP | CG-ALL-6124 | 16 | Add row TC-P5-E1065-01 with Given, When and Then copied from the criterion it covers (AC8) |
| CDC-10228 | RWB-P5-E1065-APP | DOR-RWB-P5-E1065-APP-12 | 16 | Add TC-P5-E1065-01, TC-P5-E1065-02 and TC-P5-E1065-03 under tab Story test cases |
| CDC-10242 | RWB-P5-E1065-APP | CG-ALL-6125 | 16 | Covers restored to the story's internal mapping: TC-E1-065-02 AC6, TC-E1-065-07 AC3, TC-E1-065-09 AC5. |
| CDC-10322 | RWB-P5-E2017-CON | CG-ALL-6173 | 16 | Status changed from Resolved to Cross-document; TC-11 and TC-12 covers need checking. |
| CDC-10348 | RWB-P5-E2018-APP | CG-ALL-6190 | 16 | Covers column reverted to the story's own AC numbering for TC-01, 02, 05, 06, 08, 09, 10 and 11 |

### RWB-P5-E2017-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10283 | RWB-P5-E2017-APP | DOR-RWB-P5-E2017-APP-21 | header | Set build status to Done and publish the contract baseline. |
| CDC-10285 | RWB-P5-E2017-APP | DOR-RWB-P5-E2017-APP-23 | header | Contract version row states /v1 base; version number Not specified |
| CDC-10289 | RWB-P5-E2017-APP | GAP-1713 | header | Record once, in the service contract, the owning service of each prerequisite code (approval P7, case P3, documents P5, communications P6, valuation S1); carry the duplicate FEAT-CHO-08 as written. |
| CDC-10293 | RWB-P5-E2017-APP | GAP-1278 |  | Publish the rwb.decision-record.v1 payload field set, the correction final call, the document set and value pair reference shapes, and the two parameter names. |
| CDC-10336 | RWB-P5-E2018-APP | GAP-1713 | find it | Record once the mapping of each FEAT dependency code to the owning service contract (P7 approval, P3 case, P5 documents, P6 communications, S1 valuation). |
| CDC-10337 | RWB-P5-E2018-APP | GAP-1182 | 12 | Publish create, read-by-external-reference and update operations for signature_request before the wave 2 exit. |
| CDC-10339 | RWB-P5-E2018-APP | GAP-1186 | 12 | Publish whether the signature version add takes the signed PDF bytes in the body or returns an upload link first. |

### RWB-P5-E1057-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10169 | RWB-P5-E1057-INF | DOR-RWB-P5-E1057-INF-21 | header | Contract dependency declared in header; the Fail stands until the CON build is Done |
| CDC-10170 | RWB-P5-E1057-INF | DOR-RWB-P5-E1057-INF-22 | find it | Publish a contract fake library version and record it as published. |
| CDC-10176 | RWB-P5-E1057-INF | GAP-1012 | find it | Publish the three admin operations, the run record and the fields of the run answer; the partner read goes through the rwb-partner contract with a fake and no C row. |
| CDC-10177 | RWB-P5-E1057-INF | GAP-1013 | find it | Fix the three admin operations and run resources as the smallest superset of the legacy job record; declare the channel code as a token and lists as lists; publish six fakes and the drift test. |
| CDC-10180 | RWB-P5-E1057-INF | NEWAC-RWB-P5-E1057-INF-AC8 | 7, 16 | AC8 and TC-P5-E1057-INF-09 reduced to a no-operation statement; the 401, 403 and 404 answers belong to CON |
| CDC-10190 | RWB-P5-E1057-OPS | GAP-1013 | 12 | Fix the three admin operations and the three run resources as the smallest superset of the legacy job record; declare channel code as a token and list values as lists; publish six fakes and the drift test; keep unnamed elements as placeholders; add the partner read to the plan C list. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10174 | RWB-P5-E1057-INF | DOR-RWB-P5-E1057-INF-1 | 1 | Add a role for infrastructure engineer, or confirm the role code the story should use. |
| CDC-10220 | RWB-P5-E1062-APP | GAP-2329 |  | Set the service identity of the agent platform to scope ALL, and state the default scope rule for every non-human actor role in the access and administration documentation. |
| CDC-10287 | RWB-P5-E2017-APP | DOR-RWB-P5-E2017-APP-1 | 1 | Add or confirm a role code and name for restructuring officer (FCR). |
| CDC-10311 | RWB-P5-E2017-CON | DOR-RWB-P5-E2017-CON-1 | 1 | Add 'tech lead' as a role code or name, or the story names a listed role |
| CDC-10350 | RWB-P5-E2018-APP | GAP-2357 | 7 | Confirm Documents C, R and U as operation-level rights of the five signature-request operations; add a rwb-document closed-request message at the next message standard version |

### RWB-P10-E1062-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10197 | RWB-P5-E1062-APP | DOR-RWB-P5-E1062-APP-22 | none | Publish a fake library version of RWB-P10-E1062-CON and record it as published. |
| CDC-10209 | RWB-P5-E1062-APP | GAP-0615 | n/a | Fix one run-start and one run-read operation on /api/recovery/agent/v1, declare the three event payloads with case ID key and .dlt route, and mark the unnamed consumed paths with the placeholder. |
| CDC-10213 | RWB-P5-E1062-APP | GAP-0614 | find it | Fix the run-start operation on /api/recovery/agent/v1, the read paths through rwb-case, rwb-deviation, rwb-source-data and rwb-document, and the run and proposal events with registry entries. |
| CDC-10217 | RWB-P5-E1062-APP | GAP-1047 | find it | State that the agent case read maps to API-P5-002, the document read to API-P5-003 and the field filter to API-P5-009; publish the tool call field names in the rwb-document AsyncAPI and OpenAPI. |
| CDC-10218 | RWB-P5-E1062-APP | GAP-1048 | find it | Fix the DocumentStored payload as documentId, caseId, documentType, source and storedAt, and the outbox event ID as the idempotency key, in the rwb.document.events.v1 AsyncAPI and this contract. |

### OTHER:FSD S8 (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10204 | RWB-P5-E1062-APP | GAP-1823 | n/a | Rewrite the seven E2 main, alternate and exception criteria with the S8 business analyst and QA lead, adding step criteria for pause, stop, routing and clear. |
| CDC-10205 | RWB-P5-E1062-APP | GAP-1826 | n/a | Carry the twelve named R-DEV rules as the requirement set and add the rule IDs R-DEV-19 to R-DEV-21 from the design; package authoring stays in rwb-decision. |
| CDC-10215 | RWB-P5-E1062-APP | GAP-1834 | find it | Add v1 and v2 rows to the inherited history table as Not specified in the source documents until the FSD S8 folder is completed. |
| CDC-10216 | RWB-P5-E1062-APP | GAP-1833 | find it | State the platform figures and the two evaluation samples, assert no module volume, and measure the real deviation rate in shadow before the wave 2 volume sizing. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10206 | RWB-P5-E1062-APP | GAP-1819 | n/a | Add the missing rwb_deviation entity rows for screening runs, scores, contact stops, agent feedback and breach record for S8 in the same change that writes the S8 DB story. |
| CDC-10268 | RWB-P5-E2016-APP | GAP-0716 |  | Publish one case-scoped interaction-ledger read on rwb-source-data base with the query and masked summary shape of API-P3-014; record which interaction operation rwb-case keeps. |
| CDC-10271 | RWB-P5-E2016-APP | GAP-0717 | find it | Add GET /cases/{caseId}/notices under P6 with its query and response shape, and align the P6 contract baseline to it. |
| CDC-10315 | RWB-P5-E2017-CON | GAP-1713 | find it | Map each listed prerequisite code to its owning contract: approval P7, case P3, documents P5, communications P6, valuation S1; carry duplicate FEAT-CHO-08 as written. |

### RWB-P1-E1065-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10225 | RWB-P5-E1065-APP | DOR-RWB-P5-E1065-APP-22 | none | Record the published contract fake library version |
| CDC-10237 | RWB-P5-E1065-APP | GAP-0502 | 12 | Publish the stage interface and its input and output profile (five elements), the four fixtures (full seed, empty seed, refused seed, timeout) and drift detection as a build failure. |
| CDC-10238 | RWB-P5-E1065-APP | GAP-2249 | 3 | Seed one open task and one active timer per active case; set remaining timer offsets as timer-table rows at load review. |
| CDC-10239 | RWB-P5-E1065-APP | GAP-2250 | 3 | Distribute the 2,812 cases by product group to queue rows of the seed file; cap every member at 40 open cases. |

### RWB-PLT-N001-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10294 | RWB-P5-E2017-APP | GAP-0401 |  | Publish the gateway-bff composite route path, merge order, harness repository, environment, data seeding, evidence format and wave 2 pass/fail gate, agreed with QA. |
| CDC-10296 | RWB-P5-E2017-APP | GAP-0944 | 5 | Publish the composite route field list for SCR-14 and SCR-30 with gateway-bff contract; add the allowed-action decision code AC-READ to the decision-code list of the ledger. Story side: section 5 X11 note now states AC-READ and AC-DENY use. |
| CDC-10319 | RWB-P5-E2017-CON | GAP-0401 | 12 | Publish the gateway-bff composite route for the SCR-14 and SCR-30 document set, its merge order over rwb-treatment, rwb-document, rwb-comms and rwb-access, and agree the wave 2 harness pack, seeding and evidence format with QA. |
| CDC-10325 | RWB-P5-E2017-CON | GAP-0944 |  | Publish the composite route field list for SCR-14 Treatment record and SCR-30 Case documents, and add the allowed-action decision code to the ledger's decision-code list before the audit query is built. |

### OTHER:Recovery Workbench Service Story Files v1 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10193 | RWB-P5-E1062-APP | CG-ALL-6096 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story that holds this capability in the section 13 DP-04 dependency. |
| CDC-10195 | RWB-P5-E1062-APP | DOR-RWB-P5-E1062-APP-17 | 13 | Create story file RWB-P7-E1073-CON or name the existing story that the section 13 dependency refers to. |
| CDC-10196 | RWB-P5-E1062-APP | DOR-RWB-P5-E1062-APP-21 | none | Create the contract story RWB-P5-E1062-CON for the published contract of this service, or record that the contract is published. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10202 | RWB-P5-E1062-APP | DOR-RWB-P5-E1062-APP-7 | 11, 13 | Register v_document_field_search as a migration view of rwb_document, or confirm it is not an entity (CG-ALL-6094). |
| CDC-10309 | RWB-P5-E2017-CON | CG-ALL-6162 | find it | Confirm the dictionary name of the P6 template catalog merge key transfer_price, or record the object that holds it (index, library table or flag) |
| CDC-10335 | RWB-P5-E2018-APP | DOR-RWB-P5-E2018-APP-7 | 11 | Confirm DF-DOC-103 as signature_request.external_ref, and register the party key field (story uses person_key, DF-DOC-100) in LDM v9 and Data Classification v5. |

### OTHER:Recovery Workbench Service Story Files v1 (04 User stories) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10221 | RWB-P5-E1065-APP | CG-ALL-6123 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story for the rule-package capability in the DP-04 row |
| CDC-10223 | RWB-P5-E1065-APP | DOR-RWB-P5-E1065-APP-17 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story for the rule-package capability in the DP-04 row |
| CDC-10224 | RWB-P5-E1065-APP | DOR-RWB-P5-E1065-APP-21 | none | Add contract story RWB-P5-E1065-CON, or confirm RWB-P1-E1065-CON as this story's contract |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10175 | RWB-P5-E1057-INF | DOR-RWB-P5-E1057-INF-12 | 12.7, 16, 18 | Add TC-P5-E1057-INF-01 to TC-P5-E1057-INF-07 to Test Cases v8 and align the test lists of section 18 in RTM v7 to section 16. |
| CDC-10187 | RWB-P5-E1057-OPS | DOR-RWB-P5-E1057-OPS-12 | 12, 12.7, 16, 18 | Register TC-P5-E1057-OPS-01 to -09 in Test Cases v8; align the section 18 test lists with RTM v7 |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10183 | RWB-P5-E1057-OPS | DOR-RWB-P5-E1057-OPS-8 | 12.5 | Add activity pickup on task queue rwb-document (owner RWB-P5-E1057-APP), or remove it from 12.5. |
| CDC-10186 | RWB-P5-E1057-OPS | CG-ALL-6088 | 12.5 | Add an activity row for pickup on task queue rwb-document, or replace pickup with a catalogued activity |

### OTHER:FSD P5 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10185 | RWB-P5-E1057-OPS | GAP-1587 | header | Replace branch scanner, SFTP and mailbox reading in AC-P5-013-01, AC-ALT-P5-013-01 and AC-ALT-P5-013-02 with intake items from rwb-integration; P5 keeps source, channel, capture time, hash and duplicate rule. |
| CDC-10316 | RWB-P5-E2017-CON | GAP-1580 | find it | Add a generation section covering REQ-DCM-012 with a functional statement, linked to FR-P5-026 and AC-P5-019. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10198 | RWB-P5-E1062-APP | GAP-1816 | none | Show rwb-source-data as the S8 read path to ACE data on the slide 13 connection matrix and in the contract for the screening stories. |
| CDC-10346 | RWB-P5-E2018-APP | GAP-2700 | header | Publish the signature record on the update operation of /api/recovery/treatment/v1 with a fake, so both sides build on the same day. |

### OTHER:TSD P4 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10207 | RWB-P5-E1062-APP | GAP-2326 | n/a | Add the POST /authorise operation row with its request and answer shape to the API specification index at its next revision, confirmed at the wave 1 contract review. |
| CDC-10211 | RWB-P5-E1062-APP | GAP-2327 | n/a | Fix CALLER_KIND, RIGHT_NOT_HELD and SCOPE_NOT_ALL as the refusal reasons of the authorise operation, publish them with status codes in the API specification, and confirm them with each caller service. |

### OTHER:(no target) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10230 | RWB-P5-E1065-APP | GAP-0384 wave 1 contract-test harness and test data set | 19 | Owner roles removed; the out-of-scope line now reads Not specified in the source documents (GAP-0384). |
| CDC-10236 | RWB-P5-E1065-APP | GAP-0501 sandbox scope per service and generator placement |  | Package line now states that the scope per service and the generator placement are Not specified in the source documents (GAP-0501). |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10250 | RWB-P5-E1065-APP | GAP-1052 | 4 | Fix the synthetic file naming pattern next to sandbox file properties. |
| CDC-10252 | RWB-P5-E1065-APP | GAP-1053 | 7 | Record DEV storage account and container names, the rwb-document login and the DEV read-only role; publish the SCR-30 and SCR-31 composite route with field-level masking under RWB-PLT-N001-CON. |

### RWB-P1-E1067-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10255 | RWB-P5-E1067-APP | DOR-RWB-P5-E1067-APP-22 |  | Publish the contract fake library version and record it as published |
| CDC-10259 | RWB-P5-E1067-APP | GAP-0507 |  | Fix rows 16 and 19 of Architecture v5 slide 15 in the intake map: EV-16 DocumentStored to rwb.document.DocumentStored.v1 and EV-19 TimerBreached to rwb.case.TimerBreached.v1, consumed by rwb-source-data; each producer signs its row. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10256 | RWB-P5-E1067-APP | DOR-RWB-P5-E1067-APP-11 |  | Reclassify the P2 fields that detcheck flags as personal data, or confirm none is carried in the DocumentStored payload |
| CDC-10334 | RWB-P5-E2018-APP | CG-ALL-6183 | 11 | Give signature_request.external_ref a row with its field ID, or confirm the ID; DF-DOC-103 has no row in LDM v9. |

### RWB-P1-E1067-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10258 | RWB-P5-E1067-APP | GAP-0376 |  | One consumer group across the three topics; accept current and previous schema version; dedupe on CloudEvents id in rwb_source_data.processed_event; assign case_seq under the case lock; ordered read by occurredAt then case_seq; report cross-topic inversions; keep the legacy event-to-code map. |
| CDC-10263 | RWB-P5-E1067-APP | GAP-0508 | n/a | Publish the intake map with one row per consumed event type, a version label field, and the six rows of contract section 12.4. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10288 | RWB-P5-E2017-APP | GAP-0942 | 10 | Add a Documents column: CRU for RW-RESTRUCT and RW-CASEOWN, R for RW-TEAMMGR, CRUA for RW-LEGAL; confirm with the matrix owner and publish before the pack is in force. |
| CDC-10314 | RWB-P5-E2017-CON | GAP-0942 | 10 | Add Documents column: CRU for RW-RESTRUCT and RW-CASEOWN, R for RW-TEAMMGR, CRUA for RW-LEGAL, once the matrix owner confirms. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10292 | RWB-P5-E2017-APP | GAP-0941 |  | Publish the authorise path with its request and answer schema, carry it on RWB-P4-E1037-CON and stub it in that contract fake, and state the service identity scope rule in TSD P4 T6.2. |
| CDC-10343 | RWB-P5-E2018-APP | GAP-2352 | 7 | Add the five signature-request operations with API IDs and the paths used by this story; settle the list query names and the external-reference read with rwb-comms. |

### RWB-S9-E1057-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10172 | RWB-P5-E1057-INF | GAP-1843 | find it | Keep wave 1 as a contract-only slice: partner identity and partner document path published; panel, allocation and fees land in wave 4. |

### OTHER:FSD P5 v3 intake sections (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10173 | RWB-P5-E1057-INF | GAP-1587 | 1 | Remove P5 file-system intake; rwb-integration takes the file from the channel and hands it to P5 as an intake item. P5 keeps source, channel, capture time, hash and duplicate rule. |

### RWB-S9-E1032-APP; RWB-S9-E1057-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10184 | RWB-P5-E1057-OPS | GAP-1843 | header | Keep wave 1 as a contract-only slice (partner identity and partner document path); move panel, allocation and fees to wave 4. |

### RWB-P5-E1057-CON; RWB-P5-E1057-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10188 | RWB-P5-E1057-OPS | GAP-1012 | section 10 (Schedule row) | Schedule row: business-hours window and its confirmation owner stated as Not specified (GAP-1012). |

### RWB-P5-E1057-INF; RWB-P5-E1041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10189 | RWB-P5-E1057-OPS | GAP-1014 | section 10 | Section 10 adds the DMZ position and scan-rate confirmation, with its owner Not specified (GAP-1014). |

### OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10199 | RWB-P5-E1062-APP | GAP-1822 | none | Add the call-note read as a field of the rwb-source-data contract; confirm the document read with rwb-document before the shadow screening test. |

### OTHER:P3 screen SCR-30 specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10200 | RWB-P5-E1062-APP | DOR-RWB-P5-E1062-APP-10 | n/a | Add empty, loading, error and no-access states to SCR-30; this story renders no screen and serves the agent through API-P5-002, API-P5-003 and API-P5-009. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10201 | RWB-P5-E1062-APP | DOR-RWB-P5-E1062-APP-12 | 16 | Add the contract and boundary test cases TC-E1-062-11 and TC-E1-062-12 to tab Story test cases; reconcile the other P3 test cases and align section 18 test lists to RTM v7. |

### OTHER:BRD Epic 1 v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10203 | RWB-P5-E1062-APP | GAP-1456 | n/a | State in section 8.2 that the business-epic wave is kept and that stories of rwb-payment, rwb-asset and rwb-deviation are built in wave 1 per Template and Rules R5.6, confirmed per story by the delivery lead. |

### RWB-P10-E1062-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10208 | RWB-P5-E1062-APP | GAP-0371 | n/a | Evaluate the code owner role from the P7 rule package via the embedded Drools kit, read interactions through the P1 ledger contract, and prove deviation absence via the P3 case read and absence of rwb.deviation.DeviationRaised.v1. |

### OTHER:FSD P10 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10210 | RWB-P5-E1062-APP | GAP-1532 | n/a | Read the mode from the policy row so one code path serves both the shadow run of Epic 1 and the L1 run of Epic 2, and correct the A2.8 heading and intent to match. |

### RWB-S8-E1062-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10212 | RWB-P5-E1062-APP | GAP-3085 | find it | Publish the rwb-deviation estate read, the agent-policy read operation name, the R-DEV-05 and R-DEV-06 codes and owner roles, the answer limit value and the test level split. |

### OTHER:rwb-access masking contract (masking policy owned by rwb-access) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10219 | RWB-P5-E1062-APP | GAP-1049 | 8 | Publish the mask format and the per-role list of personal document fields, and state that SY-AGENT holds Documents R with every personal field masked and no clear value in the answer, the log or the trace. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:Lists (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10226 | RWB-P5-E1065-APP | CG-ALL-6122 | 16 | Add list LOV-RISK-TIER, or name a Reference Data v5 list in the TC-E1-065-03 row |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10229 | RWB-P5-E1065-APP | DOR-RWB-P5-E1065-APP-20 | 16 | Add list LOV-RISK-TIER |

### RWB-P4-E1022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10231 | RWB-P5-E1065-APP | GAP-0896 | find it | State that the sign-in path resolves the DEV synthetic test identity to role.entra_group rows only. Platform administrator owns the DEV identity list; Service Template Specification fixes the key format; retirement rule recorded with DL39. |

### RWB-S8-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10232 | RWB-P5-E1065-APP | GAP-3086 | find it | Publish the deviation seed profile with case references and routed states, the deviation count per case and per code, the stage contract read operations and fields, the codes and owner roles of R-DEV-05 and R-DEV-06, and the test level of the legacy cases; keep the H row empty. |

### OTHER:TSD P4 (T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10233 | RWB-P5-E1065-APP | GAP-0900 | find it | Extend the RBAC matrix from three capability areas to the 14 areas of LOV-CAPABILITY and publish the full matrix version with the pack load story RWB-P4-AD002-APP. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10234 | RWB-P5-E1065-APP | GAP-0895 | find it | Fix the access seed file's repository path, format, version label and row count, and state whether the DEV seed carries the SIT matrix version or a DEV-only label. |

### OTHER:TSD P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10235 | RWB-P5-E1065-APP | GAP-0898 | find it | Add POST /authorise and GET /me/permissions with their request and answer schemas, stub them in the contract fake, and publish the SCR-43 composite route with gateway-bff (DP-19). |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10240 | RWB-P5-E1065-APP | GAP-2252 | 3 | Confirm the seeded creation code (RWB-P3-E1018-APP) and the seeded exclusion code (RWB-P3-E1019-APP or exclusion rule) at the decision-record contract review. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10241 | RWB-P5-E1065-APP | GAP-2251 rwb-case login name and read-only role field identifiers | 3 | Login name is set by the platform schema story, not by this story. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10244 | RWB-P5-E1065-APP | GAP-1051 | 3 | Publish the per-case document count and version depth as seed parameters shared with RWB-P5-E1025-APP. |

### OTHER:Story map; RWB-P5-E1055-APP; RWB-P5-E1041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10245 | RWB-P5-E1065-APP | GAP-2351 | 3 | Record RWB-P5-E1017-APP as sole owner of JOB-17; RWB-P5-E1052-APP as notice generation slice with no Schedule; correct other files. |

### OTHER:Work Package plan (B-P1-02 and B2-P1-001) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10246 | RWB-P5-E1065-APP | GAP-2161 | none | Keep one Work Package per RWB-E1-064 slice; remove duplicate fanout or retire B2-P1-001; add plan-uniqueness check. |

### RWB-P1-E1065-CON; RWB-P5-E1049-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10247 | RWB-P5-E1065-APP | GAP-1054 | 3 | Fix held item count per shape and page count per item as seed parameters; name DEV review reasons in RWB-P5-E1049-APP. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10248 | RWB-P5-E1065-APP | GAP-0897 | 3 | Fix rwb-access login; publish DEV-only rwb_sandbox_read grant list (SELECT on role and permission only); record DP-15 retirement of single-schema grant. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10249 | RWB-P5-E1065-APP | GAP-0899 | none | Publish the 54-role list with administration and non-human roles marked; reconcile with 42 rows in T6.1; fix DEV seed role count. |

### RWB-P1-E1065-CON; OTHER:Build Notes v6 RWB-E1-065 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10251 | RWB-P5-E1065-APP | GAP-3168 | none | Build sandbox from the 19 Flyway sequences plus the two view migrations; state seeding order per schema. |

### OTHER:Recovery Workbench Work Package (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10254 | RWB-P5-E1067-APP | DOR-RWB-P5-E1067-APP-21 |  | Create contract story RWB-P5-E1067-CON and record it as a contract dependency, or confirm RWB-P1-E1067-CON as the only contract |

### OTHER:FSD P7 functional specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10257 | RWB-P5-E1067-APP | GAP-1612 |  | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; rwb-source-data owns the one ledger. |

### OTHER:section 12.3 AsyncAPI fragment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10260 | RWB-P5-E1067-APP | GAP-1056 | 10 | Attribute names for actor and occurred time marked Not specified in section 10 |

### OTHER:rwb-case API and event specification; OTHER:platform event library registry (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10261 | RWB-P5-E1067-APP | GAP-2257 | 10 | Attribute names and registry values marked Not specified in section 10 |

### OTHER:TSD P3 v3; API:(service not named); OTHER:ownership.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10262 | RWB-P5-E1067-APP | GAP-2072 | n/a | Correct the interaction table and the two interaction endpoints to rwb-source-data P1, with rwb-case reading through the P1 contract, as the plan ruling states. |

### RWB-P5-E2016-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10265 | RWB-P5-E2016-APP | DOR-RWB-P5-E2016-APP-21 | header | Header dependency not added: RWB-P5-E2016-CON is not in the story set yet. The contract story must be created and published in the story set. |

### OTHER:Contract fake library (API-P5-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10266 | RWB-P5-E2016-APP | DOR-RWB-P5-E2016-APP-22 | 12 | Publish a contract fake library version for API-P5-002 and record its version number. |

### RWB-P7-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10267 | RWB-P5-E2016-APP | GAP-2210 |  | Publish the rwb-decision decision-record query path, filter and field list; state-change and creation items read from decision records; transfer from queue and owner from the closed previous assignment row; rule version from the transfer decision record; no history table in rwb_case. |

### RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10270 | RWB-P5-E2016-APP | GAP-2211 | find it | Publish the timeline addition as v1.1, an additive minor version inside major version 1, with the item detail fields, the TimelineSection state on 200 and the page total; keep type order, section timeout and page size as rwb-case parameters. |

### RWB-P3-E2016-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10272 | RWB-P5-E2016-APP | GAP-1060 | find it | Add doc_version to the document TimelineItem so the count shows without a second call; full history stays on API-P5-003 when the item is opened. |

### RWB-P5-E2017-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10282 | RWB-P5-E2017-APP | DOR-RWB-P5-E2017-APP-14 | header | Record the signed epic design sign-off for RWB-P5-E2017-APP; no signed design is in the story or sources. |

### OTHER:Published fake library version (fake publication) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10284 | RWB-P5-E2017-APP | DOR-RWB-P5-E2017-APP-22 | 12.8 | Central ledger fake named in 12.8; published fake version left Not specified |

### OTHER:FSD P5 v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10290 | RWB-P5-E2017-APP | GAP-1580 | header | Add a generation section for REQ-DCM-012 with its acceptance criteria. Until then FR-P5-026 and AC-P5-019 carry the behaviour; the story PRD reference now names both. |

### OTHER:TSD P6 v2 (API-P6-003; RWB-P6-E1046-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10291 | RWB-P5-E2017-APP | GAP-2392 | 8 | Add treatment-type and product-group filters to API-P6-003; add application/json to API-P6-005; add the locked attribute to merge_field; publish the set rows under RWB-P3-E1043-CON; copy the five message texts when the catalog is issued. |

### OTHER:Story dependencies v5 (Dependency classes sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10297 | RWB-P5-E2017-APP | GAP-3234 | header | Record that platform technical-enabler work is team-type work, tracked and never blocking; keep X on the ten rows. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10310 | RWB-P5-E2017-CON | CG-ALL-6172 | 14 | Add a new message ID for No authenticated caller (401) for this story; the story then cites it. The standard keeps MSG-P4-001 for sign-in with no role. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10312 | RWB-P5-E2017-CON | DOR-RWB-P5-E2017-CON-11 | find it | Reconcile the personal-data class of the flagged fields with the story's no-personal-data statement (AC7); the detcheck does not name the fields |

### OTHER:Platform message catalog (MSG-P4 set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10313 | RWB-P5-E2017-CON | DOR-RWB-P5-E2017-CON-9 | 14 | Confirm the standard meaning of MSG-P4-001 and align the section 14 row to it if the meaning differs from No authenticated caller. |

### OTHER:TSD P6 v2; RWB-P6-E1046-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10317 | RWB-P5-E2017-CON | GAP-2392 | 11 | Add treatment-type and product-group filters to API-P6-003; add JSON form of API-P6-005; add locked attribute to merge_field; publish set rows as reference data; copy five message texts when issued. |

### OTHER:TSD P4 appendix T-A and T6.2; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10318 | RWB-P5-E2017-CON | GAP-0941 | 10 | Publish the POST /authorise path with request and answer schema, stub it in the contract fake, and state the service identity scope rule in T6.2. |

### OTHER:Recovery Workbench plan (rwb-treatment contract stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10320 | RWB-P5-E2017-CON | GAP-1183 | 12.8 | Add the rwb-treatment contract story that publishes the treatment read and the signature record operation with its field names for wave 2; the base is /api/recovery/treatment/v1. |

### OTHER:Technical Solution Design P6 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10321 | RWB-P5-E2017-CON | GAP-1181 | 12 | Remove the signature_request table from T3.1 (DF-DOC-096 to DF-DOC-107) so the P6 Flyway sequence creates no signature table; P5 rwb-document owns it per the Ownership Map. |

### OTHER:Functional Specification Document; OTHER:S2 A2.18.2; OTHER:A2.15.2 and A2.8.3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10324 | RWB-P5-E2017-CON | GAP-1704 |  | Replace 'the Workbench document hub' with the P5 and P6 contracts for generation, review and signature; hold only the document reference on the treatment, with no document content in schema rwb_treatment. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10338 | RWB-P5-E2018-APP | GAP-2356 | 12 | Add rwb.document.esign keys for the container, WORM tier, maximum object size and transfer path, with values Not specified in the source documents (GAP-2356) until settled. |

### OTHER:Integration inventory (TSD P6 v2 T5.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10340 | RWB-P5-E2018-APP | GAP-1187 | find it | Add INT-34 with its request and result shape, endpoint and certificate issuer, published by the ACE common module owner. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10341 | RWB-P5-E2018-APP | GAP-1188 | 7 | Contract gap sits in Architecture v5 and the rwb-comms API. AC4 kept as written. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10342 | RWB-P5-E2018-APP | GAP-1589 | header | Record the signature request as a document event and a metadata row on the document; add OQ-P5-13 carrying the missing requirement text. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10344 | RWB-P5-E2018-APP | GAP-2353 | header | Keep signature_request in rwb_document; add the table with its constraints and indexes; remove it from the rwb-comms data model in the next TSD P6 version. |

### OTHER:TSD S2 rwb-treatment v2 (T3.1; OTHER:T-A.1) and FSD S2 A2.7 to A2.9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10345 | RWB-P5-E2018-APP | GAP-2699 | header | Add five nullable signature columns and two indexes; declare additive properties on the update operation; name two outcome events; read method and status lists via reference-data contract; add one closure callback. |

### RWB-P6-E2018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10347 | RWB-P5-E2018-APP | GAP-1196 | header | Add DP-03 and H RWB-PLT-E1027-CON to the slice, or confirm the platform release train delivers the decision-record library. |

### OTHER:Functional Specification Document S2 (A2.18.2; RWB-P6-E2018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-10349 | RWB-P5-E2018-APP | GAP-1704 | 3 | Name POST /cases/{caseId}/generated-documents and POST /documents/{documentId}/review as the P5 contracts; replace 'Workbench document hub' with rwb-document; keep no document content in rwb_treatment. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20630 | RWB-P5-E1067-APP | R-22269 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22269'] |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20668 | RWB-P5-E1065-APP | R-28662 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21890', 'R-28478', 'R-28528', 'R-28558', 'R-28573', 'R-28662'] |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20756 | RWB-P5-E1067-APP | R-28664 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: '**interaction** (EXTEND ACE activity log). One entry in the intera |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20779 | RWB-P5-E2017-CON | R-17422 |  | The standard text for MSG-P4-001 is not in the story set, so the meaning cannot be checked or aligned here. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0367 | Partner eligibility, channel configuration and job monitoring move in the target | Tech lead | Resolved (directive) |
| GAP-0371 | Rule-row owner lookup, interaction ledger read and deviation-absence evidence are not named for the target | P10 agent owner, P7 decision owner, P1 source data owner, S8 deviation owner and P4 access owner | Resolved (directive) |
| GAP-0374 | The per-schema seed volumes, the seeding order across the 19 baselines and the cutover from the one recovery schema are not stated | Solution architect | Resolved (directive) |
| GAP-0376 | The event-to-ledger map, the cross-topic ordering rule and the duplicate key after the split into per-service topics are not defined | Solution architect | Resolved (directive) |
| GAP-0384 | The wave 1 contract-test harness, its pipeline wiring and the synthetic test data set are not specified | QA lead | Resolved (directive) |
| GAP-0400 | Gateway-bff composite timeline route, harness environment and evidence gate are not specified | Integration lead | Resolved (directive) |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0402 | The e-signature harness pack and the EasyApp test route are not specified | Integration lead | Resolved (directive) |
| GAP-0501 | The sandbox scope per service and the placement of the generator module are not specified | Solution architect | Resolved (directive) |
| GAP-0502 | The contract of a build tool is not described by any source document | Tech lead | Resolved (directive) |
| GAP-0503 | The sandbox database scope and its read-only role name are not specified | ACE data architect | Resolved (directive) |
| GAP-0507 | The mapping of the document fact and the timer fact onto the target event types is not specified | Solution architect | Resolved (directive) |
| GAP-0508 | The format and version label of the ledger intake map are not specified | Tech lead | Resolved (directive) |
| GAP-0614 | The screening slice in rwb-agent: the run-start path, the parameter and ledger operation paths, the two added events, the screening feature flag, the boundary status of a failed tool call and the route in front of the reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-deviation, rwb-case, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0615 | The screening contract slice: the run-start path and request members, the member types of the proposal payload, the two added event names and payloads, the consumed paths no source names and the route name are not specified by any source | Tech lead of rwb-agent with the solution architect and the owners of rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0716 | Case interaction-ledger read has no agreed owner-side contract path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0717 | Case-scoped notice list has no Ownership Map row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0895 | rwb-access sandbox seed: the access seed file's location, format, version label and row count are not specified, and whether the DEV matrix version must equal the SIT version is not stated | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0896 | rwb-access sandbox seed: the owner, the key format and the retirement rule of the DEV synthetic test identity per role are not specified | Platform administrator | Resolved (directive) |
| GAP-0897 | rwb-access sandbox seed: the per-service login name and the DEV-only read-only role over rwb_access are not fixed for the target schema | Platform DB owner | Resolved (directive) |
| GAP-0898 | rwb-access sandbox seed: the authorise and me/permissions request and answer shapes, and the screen route that shows the seeded rows, are absent from the TSD appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0899 | rwb-access sandbox seed: the legacy seed loads 54 roles, while the TSD P4 RBAC matrix tabulates 42 role rows, and the difference is not enumerated | Business analyst, P4 | Resolved (directive) |
| GAP-0900 | rwb-access sandbox seed: the matrix letters for 11 of the 14 capability areas are not tabulated, so the seed content has no source table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0941 | rwb-access document set: the authorise request and answer shape for the document screens, and the scope a service identity is asked for, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0944 | rwb-access document set: the composite route field list of SCR-14 and SCR-30, and the decision code of an allowed screen action entry, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1012 | The channel pickup has no target shape of its own: the run record, the rerun operation, the channel property layout, the single-run rule and the cross-service partner read are named by the legacy story only | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1013 | The channel-intake contract baseline fixes operation names, shapes and enumerations the sources do not name, and the plan's C list omits the partner read | Tech lead | Resolved (directive) |
| GAP-1014 | The four pickup channels, their credentials, their folder lifecycle, the partner DMZ position and the scan capacity are environment facts no source states | SCB IT infrastructure | Resolved (directive) |
| GAP-1015 | The deployment of the channel pickup has no source for its values, its chart key names, its Schedule ID, its catch-up window, its alert thresholds and its runbook entries | DevOps engineer | Resolved (directive) |
| GAP-1017 | The generation-screens baseline fixes six operations and four shapes that no source names, two conflicting legacy paths, the field names of the request and answer objects, and a status mapping the legacy section 12 states only in prose | Tech lead of rwb-document, with the solution architect and the rwb-comms owner | Resolved (directive) |
| GAP-1047 | The agent's document-read tool contract is not defined in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1048 | The idempotency-key format of DocumentStored and the event field names the agent reads are not defined | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1049 | The mask format and the per-role list of personal fields for SY-AGENT are not defined | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1050 | The read behaviour for a stored document whose type has left the version in force is not defined | Business analyst, P5 | Resolved (directive) |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1052 | The file-name pattern of the synthetic documents is not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1054 | The count of held intake items per exception shape and the pages each held item carries are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1055 | The exact idempotency-key format of rwb.document.DocumentStored.v1 is not stated for the target topic | Tech lead | Resolved (directive) |
| GAP-1056 | The CloudEvents attribute names that carry the actor and the occurred time on rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
| GAP-1057 | The retry limit applied to the JOB-11 outbox relay of rwb-document is not stated | Platform administrator | Resolved (directive) |
| GAP-1058 | The JSON Schema registry subject name and the AsyncAPI document location for rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
| GAP-1059 | The contract shape rwb-case and rwb-document share for the case timeline is not specified | Solution architect | Resolved (directive) |
| GAP-1060 | Whether the version count of a document travels on the timeline item or only on the document detail | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1061 | The summary wording of a document timeline item is not specified | Business analyst, P5 | Resolved (directive) |
| GAP-1181 | signature_request is defined in TSD P6 but is owned by P5 rwb-document | Solution architect | Resolved (directive) |
| GAP-1182 | The published P5 document names no operation to create, read by external reference or update a signature request | Solution architect | Resolved (directive) |
| GAP-1183 | No rwb-treatment contract story is in the plan, although the story reads the treatment and writes its signature record | Solution architect | Resolved (directive) |
| GAP-1184 | The plan holds no RWB-P6-E2018-CON, so the three signature-request operations have no published contract story | Solution architect | Resolved (directive) |
| GAP-1185 | The Architecture v5 event catalogue carries no comms signature event | Solution architect | Resolved (directive) |
| GAP-1186 | The signed PDF object and the byte transfer into the P5 write-once store are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1187 | The ACE common module e-signature path (INT-34) is not in the integration inventory and its shape, endpoint and certificate are unknown | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1188 | P3's cancel on offer expiry has no operation in the target catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1196 | DP-03 and its decision-record library are missing from the pattern set and the build list of the e-signature key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1278 | The record payload, the reference shapes and the correction final call of the RWB-E2-017 decision slice have no source | Solution architect | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1532 | The screening feature is titled at L1 and its main criterion stores a shadow run that creates no deviation | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1587 | FSD P5 takes branch, mailroom, SFTP and mailbox files inside P5 while Architecture v5 gives P5 no file interface | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1589 | Signatures are owned by P5 in Architecture v5 and the Ownership Map but have no requirement, feature or story | Solution architect with P6 and S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1596 | The signature request is defined as a Communications table while Architecture v5 gives signatures to the document hub | Solution architect | Resolved (directive) |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1822 | The screening agent reads call notes and documents, while the S8 row has no rwb-document cell and no call-note data product is named anywhere | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1826 | The FSD names 12 of the 22 R-DEV rules and the deviation rule package is Phase 2 with no owner for S8 | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1833 | No deviation, screening or queue volume is stated for this module | Solution architect | Resolved (directive) |
| GAP-1834 | The change notes of FSD S8 versions 1 and 2 are not in the sources read | Business analyst, S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-2072 | The interaction ledger is claimed by rwb-case and by rwb-source-data | Service owner P1 rwb-source-data with P3 rwb-case | Resolved (directive) |
| GAP-2137 | Which service seeds which rows of the shared case set is not specified | QA | Resolved (directive) |
| GAP-2154 | The seed, business date, volumes and identifiers of the synthetic fixture set are not stated | QA lead | Resolved (directive) |
| GAP-2161 | Two Work Packages write the same three story files and three fragments for legacy RWB-E1-064 on rwb-source-data | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2210 | No source gives the case status history, the transfer from-queue or the decision-record read behind the timeline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2211 | No source fixes the v1.1 timeline item shape, the section state or its version against the RWB-P3-E1023-CON baseline | Solution architect | Resolved (directive) |
| GAP-2249 | Task and timer counts per seeded case, and the timer offsets beyond the FSD P3 AC-ALT-P3-011 offsets, are not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2250 | The distribution of the 2,812 seeded cases across the 12 queues and 48 members is not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2251 | The rwb-case login name, the DEV read-only role name and the field identifiers of six seeded tables are not in the sources | TechX and the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2252 | The decision code and the payload of the decision records the seed writes are not in the sources | TechX and the rwb-decision contract owner | Resolved (directive) |
| GAP-2257 | The CloudEvents key and actor attributes, the idempotency-key format, the relay publish limit and the registry subject of the case topic are not in the sources | rwb-case contract owner and the platform event library owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2326 | The agent-authority part of POST /authorise has no operation row, request shape or answer shape in any source | Solution architect, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2327 | The reason-code vocabulary of a refusal and the status of each code are not specified | Solution architect, P4 and the security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2329 | The default scope of the agent service identity is not specified for this legacy key | Security administrator role | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2352 | The signature-request operations exist in no P5 source and carry no API ID, because the legacy key is a communications module story while the table is P5's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2353 | signature_request is defined in TSD P6 T3.1 inside the communications module and owned by P5 in the ownership ruling, so the table has no P5 data model | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2355 | No source names a signature event on the rwb-document topic, and the request state is readable only through the operations of the story | Solution architect | Resolved (directive) |
| GAP-2356 | The write-once container, the WORM tier, the size limit and the byte transfer behind the signed-version add are named by no source | SCB IT infrastructure | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2357 | No rwb-document message exists for a closed signature request and no source names the operation-level right of the five request operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2697 | The treatment-side panel section, its properties and action vocabulary, the treatment-type document set row and the one-hop set read are not specified | Solution architect | Resolved (directive) |
| GAP-2698 | The legacy files the whole generation capability under the document module, while the target gives the treatment screen leg to rwb-treatment and the set to rwb-document | Solution architect | Resolved (directive) |
| GAP-2699 | The treatment-side signature columns, the operation a signature record arrives on, the event names, the two list codes and the closure are not specified for rwb-treatment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2700 | Architecture v5 gives S2 to P5 the Temporal cell and no cell from P6 or P5 into S2, while the legacy seam is one synchronous in-process call and the work package lists DP-11 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2701 | The legacy one module and one transaction for the signature request, the signed version and the treatment field become three owners, and the offer expiry that closed the request is now the treatment's own date | Solution architect | Resolved (directive) |
| GAP-3085 | RWB-S8-E1062-APP: the deviation estate the shadow screening run reads has no read operation, no published agent-policy read, no owner role for R-DEV-05 and R-DEV-06, no value for the answer limit and no test level | Solution architect, with the rwb-deviation owner, the rule-set owner of the Deviations package, the rwb-agent contract owner, the rwb-case parameter and reference-data owners, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3086 | RWB-S8-E1065-APP: the deviation slice of the sandbox has no published case-reference source, no deviation count per case or per code, no operation or field names for the stage contract read, no codes or owner roles for R-DEV-05 and R-DEV-06, no test level for the ten legacy cases and an empty H row for eight patterns | Solution architect, with the rwb-deviation owner, the rwb-case and rwb-document owners, the rwb-source-data sandbox owner, the rule-set owner of the Deviations package, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3168 | The sandbox story applies three migrations where 19 schemas now need their own sequence | ACE DB lead | Resolved (directive) |
| GAP-3182 | The signature_request table is created by P6 in the story and owned by P5 in the ownership map | Document hub lead with the communications lead | Resolved (directive) |
| GAP-3234 | Ten class X rows point at a platform application story rather than at a DB, INF or OPS story | TechX (platform) | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
