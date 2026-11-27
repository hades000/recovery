# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 3 of 11 (RWB-P4-AD016-APP to RWB-P4-E1019-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 183 |
| Cross-document (pending in another document) | 248 |
| Not applied (value not in the sources) | 11 |
| Open business decisions | 24 |
| Register gaps linked | 174 |
| Unconfirmed assumptions | 0 |
| Lint findings | 3 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-AD016-APP | 30 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD016 APP Load the delegation of authority table v2.md |
| RWB-P4-AD016-CON | 20 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD016 CON Load the delegation of authority table - contract v2.md |
| RWB-P4-E1001-APP | 24 | 55 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1001 APP Recovery tables for the 14 data products v2.md |
| RWB-P4-E1007-APP | 25 | 38 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1007 APP Integration adapters for outbound files v2.md |
| RWB-P4-E1008-APP | 19 | 30 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1008 APP Decision log store v1, append only and hash chained v2.md |
| RWB-P4-E1016-APP | 15 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1016 APP Access control per data product and catalog entries v2.md |
| RWB-P4-E1018-APP | 22 | 29 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1018 APP Case ID issuance and case record v1 v2.md |
| RWB-P4-E1019-APP | 28 | 24 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1019 APP Roles, teams and queues as data v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E1019-APP | R-01192 | CG-ALL-4901 | Script gap | Product owner | The story adds AUDIT_VIEW to the closed list LOV-CAPABILITY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-ITG-E1008-ITG, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS | R-09175 | GAP-1225 | Register gap | Solution architect with the decision-center product owner | How nineteen local record chains become one central chain is not specified | Fix the rule as: the ledger recomputes entry_hash on the legacy canonical form (BR4) over the stored columns, orders by the ingest commit under the chain lock, and preserves the local chain sequence and hash on the row for reconciliation; then publish it in RWB-P7-E1008-CON. |
| RWB-P4-E1001-APP | R-10609 | CG-ALL-4843 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E1008-APP | R-10622 | CG-ALL-4870 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E1016-APP | R-10626 | CG-ALL-4884 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21843 | GAP-0001 | Register gap | Product Owner | Arch v5 waves have no release dates | Keep the dates unchanged and tentative, map waves 0-1 to Release 1 at the plan gate, and confirm the mapping in the verification loop |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21856 | GAP-0977 | Register gap | Data steward and data product owner (RW-DATASTEW) | The dictionary rows of the five rwb_access tables have no seeding owner after the split | Declare the 44 business rows as a build artefact of this story, hand the declaration to the one dictionary's seed in rwb_source_data, and let the seed carry the 35 standard-column rows under its own Field IDs. Cite the 44 business Field IDs only. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-21888 | GAP-1545 | Register gap | Compliance | The debt buyer tape is required to be masked before the data room, and to carry the personal data the sale terms allow | The tape carries only the fields the sale terms and the approved mask list allow, and the mask list is a reference-data row owned by Compliance under DL26; the PRD states the rule and leaves the field list open. |
| RWB-ITG-E1008-ITG, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS | R-21897 | GAP-0003 | Register gap | RW-RISK and Internal Audit | ADR-009 central log versus local record plus central ledger | Adopt RecordAndApply plus the central ledger and seal the change in ADR-022 after the Audit sign-off |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-21966 | GAP-1501 | Register gap | Compliance and PDPA officer | Field-level masking rules belong to the access service, while the FSD loads them here | This service keeps data_product_access (role, product, read right) and applies the masking policy of rwb-access, cached per the platform pattern; the masking rows themselves are rwb-access's. Confirm the split with Compliance and Security before the first masking test. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-28455 | GAP-1548 | Register gap | Compliance | No retention period is set for an outbound item, a delivery record or the transmission evidence of a file | The PRD states the retention of P2 transmission records as open under DL26 with the section R9 placeholder, and requires only that a resend and its audit record outlive the retention period of the case they belong to. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1027-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-28460 | GAP-2067 | Register gap | Document owner of the audit and logging design | The source reads version 1 in its metadata table and v2 in its file name | Take the file name as the family version, so this document becomes version 3, and keep the source values in a 'Source version' row: 1, 28 October 2026. The change log carries both readings. |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-28495 | GAP-1510 | Register gap | Compliance with Security | The classification scheme per data product and the retention periods are open, so the PRD labels are a reading of the field markers | Apply the four-label scheme from the field markers now: personal fields and the party and contact extension rows as personal data, balances and amounts as sensitive financial data, case, legal, collateral and metadata as confidential, and no data product as public. Replace with the approved scheme when DL26 closes. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-P4-E1001-APP | R-36596 | ASM-1711 | Register assumption |  | Each of the five tables carries the 7 standard columns of the service template (is_active, state, version, created_at, created_by, updated_at, updated_by), and the 44 business Field IDs of section 11 are the ones this story declares and cites; the Field IDs of the 35 standard columns are the one dictionary's and are not cited here. | Data steward and data product owner (RW-DATASTEW), with the one dictionary's seed |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-AD016-CON | R-05583 | DOR-RWB-P4-AD016-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or project *.md sources (earlier grep). No value to write; left unchanged. |
| RWB-P4-AD016-CON | R-30830 | NEWAC-RWB-P4-AD016-CON-AC7 | 7 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Adding AC7 needs section 7 and section 16 text, which is not in this chunk, and the proposed test is not in the sources. No partial AC added. |
| RWB-P4-E1001-APP | R-05589 | DOR-RWB-P4-E1001-APP-21 | header | Definition of Ready item 21 Contract published: Fail | The story names contracts (AC8, Background), so not applicable is wrong; the row is Not specified. |
| RWB-P4-E1001-APP | R-30831 | NEWAC-RWB-P4-E1001-APP-AC12 | 7 | AC12: §8 BR3, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7/16 absent from chunk. Draft in _work/msr/directive/mp/out already has AC12 (BR3, TC-E1-001-13) and AC13 (BR11). Unanchored; no edit made. |
| RWB-P4-E1007-APP | R-10615 | CG-ALL-4854 | 14 | MSG-P2-001 text differs from the Error and Message Standard v4 | Edit reverted. R-16585 records the §14 text as matching the standard word for word, so no change is needed. |
| RWB-P4-E1007-APP | R-10617 | CG-ALL-4858 | 12.8 | Criteria and test data read ACE views directly | rwb-source-data fake is not in 12.8 or any source checked; the 30 ace views are BND-6 negative fixtures (AC7, TC-E1-007-02) and a fake cannot carry them without inventing a contract. QA ruling needed. |
| RWB-P4-E1008-APP | R-25328 | CG-ALL-4871 | 3 | Flyway file V1008_1__decision_record.sql is not in the V0001..Vnnnn form | Next free number of the rwb-access Flyway sequence is not in the sources (only V0001 baseline; sister stories use V4001_1 etc.). Line 367 is outside the chunk. Owner: Solution architect. |
| RWB-P4-E1008-APP | R-30836 | NEWAC-RWB-P4-E1008-APP-AC9 | 7, 16 | AC9: §8 BR7, BR8, BR10, BR11, BR12, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC9 text and its section 16 test row are not in the chunk; placeholder keeps AC numbering continuous. |
| RWB-P4-E1016-APP | R-05607 | DOR-RWB-P4-E1016-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in the source documents; Grep of source folders finds none. Writing the sign-off would invent it. Needs the epic design record. |
| RWB-P4-E1016-APP | R-10627 | CG-ALL-4885 | 4, 12.8 | Criteria and test data read ACE views directly | Section 12.8 has no rwb-source-data contract fake, so rewriting AC7 and TC-E1-016-10 needs an invented fake. Owner role QA to supply the fake. |
| RWB-P4-E1019-APP | R-25344 | CG-ALL-4911 | 3, 3.1 | Flyway file V1019_1__role_matrix.sql is not in the V0001..Vnnnn form | Next Flyway number for rwb-access is not in the sources; grep for V0001 and db/migration found only other services' sequences. Name kept until confirmed. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (30)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07813 | RWB-P4-AD016-APP | CG-ALL-4815 | 12.1 | Publish POST /api/recovery/access/v1/admin/doa-loads in rwb-access.yaml through the provider's CON story. |
| CDC-07814 | RWB-P4-AD016-APP | CG-ALL-4816 | 12.1 | Publish POST /api/recovery/access/v1/admin/doa-loads/{loadId}/approve in rwb-access.yaml through the provider's CON story. |
| CDC-07815 | RWB-P4-AD016-APP | CG-ALL-4817 | 12.1 | Publish GET /api/recovery/access/v1/admin/doa-loads/{loadId} in rwb-access.yaml through the provider's CON story. |
| CDC-07816 | RWB-P4-AD016-APP | CG-ALL-4818 | 12.1 | Publish GET /api/recovery/access/v1/doa-limits in rwb-access.yaml through the provider's CON story. |
| CDC-07817 | RWB-P4-AD016-APP | CG-ALL-4819 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-E1037-CON, the provider contract story. |
| CDC-07819 | RWB-P4-AD016-APP | DOR-RWB-P4-AD016-APP-8 | 12.2 | Add the paths POST /admin/doa-loads, POST /admin/doa-loads/{loadId}/approve, GET /admin/doa-loads/{loadId} and GET /doa-limits, plus the two further paths the detcheck lists |
| CDC-07829 | RWB-P4-AD016-CON | CG-ALL-4827 | 12.1 | Publish POST /api/recovery/access/v1/admin/doa-loads with the multipart file, query table, validFrom and version label, the DoaLoad answer and the Idempotency-Key header. |
| CDC-07830 | RWB-P4-AD016-CON | CG-ALL-4828 | 12.1 | Publish POST /api/recovery/access/v1/admin/doa-loads/{loadId}/approve with no request body, the DoaVersion answer and the Idempotency-Key header. |
| CDC-07831 | RWB-P4-AD016-CON | CG-ALL-4829 | 12.1 | Publish GET /api/recovery/access/v1/admin/doa-loads/{loadId} with the DoaLoadAnswer response. |
| CDC-07832 | RWB-P4-AD016-CON | CG-ALL-4830 | 12.1 | Publish GET /api/recovery/access/v1/doa-limits with its query parameters and the DoaLimitAnswer response. |
| CDC-07833 | RWB-P4-AD016-CON | CG-ALL-4831 | 12.2 | Publish POST /api/recovery/access/v1/authorise, provided by rwb-access itself, with the MSG-P4-002 refusal shape. Recommended option taken per directive. |
| CDC-07834 | RWB-P4-AD016-CON | DOR-RWB-P4-AD016-CON-8 | 12.1 | Publish the four operations of CG-ALL-4827 to CG-ALL-4830 and the POST /authorise of CG-ALL-4831, and declare the Idempotency-Key header on POST /admin/doa-loads and POST /admin/doa-loads/{loadId}/approve. |
| CDC-07844 | RWB-P4-AD016-CON | GAP-0840 | 16 | TC-AD-016-CON-01 states the field formats as Not specified in the source documents (GAP-0840). |
| CDC-07846 | RWB-P4-E1001-APP | CG-ALL-4838 | 8 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are accepted as data without a code change. |
| CDC-07847 | RWB-P4-E1001-APP | CG-ALL-4839 | 8 | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as data without a code change. |
| CDC-07849 | RWB-P4-E1001-APP | DOR-RWB-P4-E1001-APP-8 | 8 | Remove the closed enums on roleClass and defaultScope so LOV-ROLE-CLASS and LOV-SCOPE are read as data. |
| CDC-07902 | RWB-P4-E1007-APP | CG-ALL-4849 | n/a | Remove the closed enum on defaultScope so LOV-SCOPE values load as data, as Reference Data v5 Lists defines them. |
| CDC-07939 | RWB-P4-E1008-APP | CG-ALL-4863 | 12.1 | Publish GET /api/recovery/access/v1/admin/access-log in rwb-access.yaml through the CON story, as the solution architect owns. |
| CDC-07940 | RWB-P4-E1008-APP | CG-ALL-4864 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the CON story, as the solution architect owns. |
| CDC-07945 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-8 | 12.1, 12.3 | Publish the two missing operations in rwb-access.yaml through the CON story; the event type is fixed in the story. |
| CDC-07969 | RWB-P4-E1016-APP | CG-ALL-4876 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through the CON story. |
| CDC-07970 | RWB-P4-E1016-APP | CG-ALL-4877 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the CON story. |
| CDC-07971 | RWB-P4-E1016-APP | CG-ALL-3426 | 1 | Remove the closed roleClass enum so LOV-ROLE-CLASS values are accepted as data. |
| CDC-07972 | RWB-P4-E1016-APP | CG-ALL-4880 | 1 | Remove the closed defaultScope enum so LOV-SCOPE values are accepted as data. |
| CDC-07986 | RWB-P4-E1018-APP | CG-ALL-4889 | 12.1 | Publish POST /api/recovery/access/v1/authorise through the owner's contract story RWB-P4-E1037-CON. |
| CDC-07987 | RWB-P4-E1018-APP | CG-ALL-4890 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions through the owner's contract story RWB-P4-E1037-CON. |
| CDC-07988 | RWB-P4-E1018-APP | CG-ALL-4892 | 13 | Remove the closed enum on defaultScope; LOV-SCOPE values are read as data per DP-07 and the story text. |
| CDC-08015 | RWB-P4-E1019-APP | CG-ALL-4902 | 12.1 | Publish GET /admin/roles under base /api/recovery/access/v1 as stated in 12.1, without the doubled prefix in the item |
| CDC-08016 | RWB-P4-E1019-APP | CG-ALL-4903 | 12.1 | Publish GET /me/session under base /api/recovery/access/v1 as stated in 12.1, without the doubled prefix in the item |
| CDC-08019 | RWB-P4-E1019-APP | DOR-RWB-P4-E1019-APP-8 | find it | Add GET /api/recovery/access/v1/admin/roles and GET /api/recovery/access/v1/me/session; declare roleClass as a read value of LOV-ROLE-CLASS, not a closed enum. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07857 | RWB-P4-E1001-APP | GAP-0100 | 9 | Endpoints sheet: list each of the 156 operations under its owning service with its Architecture v5 base path. Leave the final operation path and payload to API Specification v5. |
| CDC-07858 | RWB-P4-E1001-APP | GAP-0107 | 9 | FK cuts sheet: add the 48 cross-owner foreign keys derived from sheet Tables (keep if same owner, else column stays uuid). Record the 48 rows in the README and the ERD. |
| CDC-07859 | RWB-P4-E1001-APP | GAP-0109 | 9 | Tables sheet: set outbox_event, outbox_delivery, processed_event and idempotency_key to each of the 19 service schemas with no business foreign key. Set feature_flag and feature_flag_change once in rwb_integration. |
| CDC-07864 | RWB-P4-E1001-APP | GAP-0225 | 9 | Record S2 as owner of the live treatment record, with S3 and P1 named in the basis cell. Keep DP04 whole unless the LDM is split at its next revision. |
| CDC-07865 | RWB-P4-E1001-APP | GAP-0228 |  | Add rows for the rwb_valuation tables (valuation, D6 route decision, route agent output) owned by S1 rwb-valuation. |
| CDC-07866 | RWB-P4-E1001-APP | GAP-0333 |  | State the owning rwb_* schema and login for each of the 24 operational sys_objects (13 OPS, 8 AGT, 3 RPT). |
| CDC-07882 | RWB-P4-E1001-APP | GAP-0108 |  | Write rwb_valuation.sql with the schema, the platform library objects and a note; assign owner S1 to the valuation tables or read ACE through the rwb-source-data contract until a TSD adds a local table. |
| CDC-07884 | RWB-P4-E1001-APP | GAP-0114 |  | Remove the P1 and rwb_source_data assignment of lake_copy_watermark. Keep its DDL in rwb_source_data.sql with a retirement note; the P1 DB story drops it. |
| CDC-07887 | RWB-P4-E1001-APP | GAP-0202 |  | Give all 30 recovery.v_ace_* views owner P1 and target schema 'recovery (ACE, read-only view)', taken from Architecture v5. Add a Views sheet. |
| CDC-07888 | RWB-P4-E1001-APP | GAP-0212 |  | In the Aric via COLLINS row, read the ACE table as rwb_source_data.party_ext. Leave the 1/0/0/1 counts and Total row unchanged. |

### 06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20527 | RWB-P4-E1001-APP | R-28427 |  | ITG story: DP07 system of record cell could not be read (.xlsx unreadable here). Exact old value unknown; S4 legal data set change not written. |
| CDC-20528 | RWB-P4-E1001-APP | R-28428 |  | ITG story: DP13 system of record cell could not be read (.xlsx unreadable here). Exact old value unknown; P8 proceeds change not written. |
| CDC-20529 | RWB-P4-E1001-APP | R-28429 |  | ITG story: DP05 ownership basis could not be read (.xlsx unreadable here). Exact old value unknown; P1 interaction ledger change not written. |
| CDC-20530 | RWB-P4-E1001-APP | R-28430 |  | ITG story: DP14 ownership basis could not be read (.xlsx unreadable here). Exact old value unknown; P3 parameters change not written. |
| CDC-20531 | RWB-P4-E1001-APP | R-28431 |  | ITG story: Ownership split basis cell (row 8, count 88) could not be read here. Exact old text unknown; reconciliation not written. |
| CDC-20532 | RWB-P4-E1001-APP | R-28427 |  | APP story (RWB-P4-E1001-APP): legal data set owner row (legal_action, hearing S4; notice P6) could not be read. Exact old value unknown; not written. |
| CDC-20533 | RWB-P4-E1001-APP | R-28428 |  | APP story (RWB-P4-E1001-APP): proceeds row (P8; write_off S7) could not be read. Exact old value unknown; not written. |
| CDC-20534 | RWB-P4-E1001-APP | R-28429 |  | APP story (RWB-P4-E1001-APP): interaction/efs_ledger_outcome row (P1) could not be read. Exact old value unknown; not written. |
| CDC-20535 | RWB-P4-E1001-APP | R-28430 |  | APP story (RWB-P4-E1001-APP): lov_value, reference_row, parameter_catalog rows (P3) could not be read. Exact old value unknown; not written. |
| CDC-20536 | RWB-P4-E1001-APP | R-28431 |  | APP story (RWB-P4-E1001-APP): Ownership split basis cell could not be read here. Exact old text unknown; 93-row reconciliation not written. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07824 | RWB-P4-AD016-APP | DOR-RWB-P4-AD016-APP-7 | 11 | Register DF-REF-039, the last field of the role row in section 11 (entra_group), in LDM v9 or confirm its ID there. |
| CDC-07854 | RWB-P4-E1001-APP | DOR-RWB-P4-E1001-APP-7 | 11 | Confirm DF-REF-039 (role.entra_group, per TSD P4 v3 T3.1) is in LDM v9 or re-cite it. The v_data_dictionary wording is fixed in the story. |
| CDC-07868 | RWB-P4-E1001-APP | GAP-1280 |  | Correct rule_row to 21 fields, remove rule_test_case.package_version_id, and drop the cross-schema foreign keys on approval.case_id and approval.delegation_limit_id. |
| CDC-07871 | RWB-P4-E1001-APP | GAP-2401 |  | Correct the rule_row field count to 21, remove rule_test_case.package_version_id, and keep approval foreign keys as values only. |
| CDC-07913 | RWB-P4-E1007-APP | DOR-RWB-P4-E1007-APP-7 | 11 | Confirm DF-REF-039 exists for the role entity; if it does not, the story row DF-REF-034 to DF-REF-039 follows the LDM ID set. |
| CDC-07946 | RWB-P4-E1008-APP | CG-ALL-4861 | 13 | Section 13 names decision_record as a local object not held in LDM v9 |
| CDC-07947 | RWB-P4-E1008-APP | CG-ALL-4862 | 13 | Section 13 names tr_declog_append_only as a local object not held in LDM v9 |
| CDC-07977 | RWB-P4-E1016-APP | DOR-RWB-P4-E1016-APP-7 | 11 | Add or confirm field ID DF-REF-039 (role.entra_group) in v9, or correct the story row to the v9 ID. |
| CDC-08023 | RWB-P4-E1019-APP | DOR-RWB-P4-E1019-APP-7 | 11 | Add field ID DF-REF-039 (role.entra_group) to the LDM or confirm the ID; the §11 row count of 20 already matches. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07823 | RWB-P4-AD016-APP | DOR-RWB-P4-AD016-APP-12 | 12.7, 16, 18 | Align its test lists with section 18 of the story, which now includes TC-AD-016-10; the missing Test Cases v8 rows are a separate item |
| CDC-07826 | RWB-P4-AD016-APP | CG-ALL-4823 | 18 | Align the test lists of the four requirements that differ with section 18 of RWB-P4-AD016-APP in the next RTM version. |
| CDC-07843 | RWB-P4-AD016-CON | CG-ALL-4834 | 18 | Align REQ-ACA-004 and REQ-DRI-010 test lists to section 18 of this story (TC-AD-016-CON-01, -02, -05, -07 and -02, -04, -06). |
| CDC-07879 | RWB-P4-E1001-APP | CG-ALL-4842 | 18 | Align the REQ-RDF-001 and REQ-RDF-014 test lists to the §18 lists of RWB-P4-E1001-APP in the next RTM version. |
| CDC-07931 | RWB-P4-E1007-APP | CG-ALL-4857 | n/a | In the next RTM version, align the test lists of REQ-DRI-006, REQ-DRI-007 and the third requirement to section 18 of this story. |
| CDC-07960 | RWB-P4-E1008-APP | CG-ALL-4869 |  | Reconcile the REQ-DRI-001 test list with §18 of RWB-P4-E1008-APP (TC-E1-008-03) in the next RTM version; RTM also lists TC-E1-008-01 and TC-E1-008-04. |
| CDC-07982 | RWB-P4-E1016-APP | CG-ALL-4883 | 18 | Align the test lists of the three requirements with RWB-P4-E1016-APP section 18 in the next RTM version; section 18 of this story is aligned in the same cycle. |
| CDC-08032 | RWB-P4-E1019-APP | CG-ALL-4910 | 18 | Align REQ-CWC-006 and REQ-ACA-002 test lists with section 18 in the next RTM version; the REQ-ACA-002 RTM list is truncated in the evidence. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07822 | RWB-P4-AD016-APP | CG-ALL-4822 | 16 | Add rows TC-AD-016-05 to TC-AD-016-09 to tab Story test cases, with Given, When and Then copied from the criteria they cover (AC4, AC7 and AC8, AC10, AC11, AC3) |
| CDC-07837 | RWB-P4-AD016-CON | DOR-RWB-P4-AD016-CON-12 | 12.7, 16, 18 | Register TC-AD-016-CON-01 to -07 with their AC links; align RTM v7 with the section 18 test lists. |
| CDC-07842 | RWB-P4-AD016-CON | CG-ALL-4833 | 16 | Add rows TC-AD-016-CON-01 to TC-AD-016-CON-06 to Story test cases, with Given, When and Then copied from the criterion each covers in section 7. |
| CDC-07851 | RWB-P4-E1001-APP | CG-ALL-4840 | 16 | Add the Story test cases rows for TC-E1-001-12 (Given, When, Then copied from AC1, AC7, BR1, BR7) and for TC-E1-001-13 to -15. |
| CDC-07878 | RWB-P4-E1001-APP | CG-ALL-4841 | 16 | Restored the original AC cites in section 16 |
| CDC-07975 | RWB-P4-E1016-APP | CG-ALL-4881 | 16 | Add rows TC-E1-016-10, TC-E1-016-11 and TC-E1-016-12 with Given, When and Then copied from the criteria they cover (AC7 and BR10; BR2; BR2). |
| CDC-07995 | RWB-P4-E1018-APP | CG-ALL-4893 | 16 | Add rows TC-E1-018-15 and TC-E1-018-16 with Given, When and Then copied from AC2, AC3 and AC6. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07850 | RWB-P4-E1001-APP | GAP-0012 | 9 | Record the per-login PgBouncer connection cap; create the 19 schemas and logins in wave 0 with the ACE DBA. Cap value: Not specified in the source documents (GAP-0012). |
| CDC-07877 | RWB-P4-E1001-APP | GAP-2061 |  | Add a 19-row per-service availability table applying the same targets, write one service shape once, and state the composed screen as the product of its called services within the one-hop budget. |
| CDC-07917 | RWB-P4-E1007-APP | GAP-0338 |  | Update the P2 Integration row to show the read path to rwb-source-data and the FileFailed edge into rwb-case. |
| CDC-07929 | RWB-P4-E1007-APP | GAP-0649 | n/a | Fix endpoints, accounts, folders, receivers, PGP key identifiers, staging, file-size limit, timeout and rotation period with the MFT, network and security teams. |
| CDC-07930 | RWB-P4-E1007-APP | GAP-1396 | n/a | Fix the Airflow product, tenancy, principal, timeout and retry values, the DailyCaseRun wait mechanism and the owner operation paths at the scheduling design review. |
| CDC-07963 | RWB-P4-E1008-APP | GAP-1230 |  | Change slide 14 GET /decisions?caseId= and slide 41 first path /decisions to /decision-log, matching the Ownership Map and API Specification. |

### OTHER:06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07892 | RWB-P4-E1001-APP | GAP-0227 |  | In v4, record S4 (rwb_litigation) as owner of the legal data set (legal actions, hearings, judgments, enforcement). ACE court records stay a P1 read; notice and proof of delivery stay P6. |
| CDC-07893 | RWB-P4-E1001-APP | GAP-0229 |  | In v4, record P8 (rwb_payment) as owner of the proceeds and matching data set. write_off stays S7 (rwb_writeoff); ACE payment and gl_write_off records stay a P1 read. |
| CDC-07894 | RWB-P4-E1001-APP | GAP-0230 |  | In v4, record P1 (rwb_source_data) as owner of the interaction and EFS ledger. Notice content and delivery stay P6; the case timeline stays a P3 read through the P1 contract. |
| CDC-07895 | RWB-P4-E1001-APP | GAP-0231 |  | In v4, record P3 (rwb_case) as owner of parameters, lists of values and reference versions, per the R-PREC default ruling. Roles, permissions, masking rules and DoA stay P4; templates and merge fields stay P6. |
| CDC-07896 | RWB-P4-E1001-APP | GAP-0232 |  | Keep the count of 88 and add this to the basis cell: 93 Ownership Map rows, minus 4 Tier 3 extension tables (party_ext, contact_point_ext, account_ext, valuation_ext), minus 1 legacy P1 table with no target (lake_copy_watermark), gives 88 Tier 4 tables over 19 owners. |
| CDC-07897 | RWB-P4-E1001-APP | GAP-0233 |  | In v4, add one role row (service data steward), one change-process step (owner service) and one quality measure (schema isolation). Keep the v3 Roles rows 6-8, change step 4 and quality rows 5, 8, 10 unchanged. |

### RWB-P2-E1007-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07905 | RWB-P4-E1007-APP | DOR-RWB-P4-E1007-APP-22 | header | Publish the deliverFile fake and record its library version as published. |
| CDC-07906 | RWB-P4-E1007-APP | DOR-RWB-P4-E1007-APP-23 | header | State the contract version this story builds against, then record it in the story header. |
| CDC-07916 | RWB-P4-E1007-APP | GAP-0334 | 8 | Fix the deliverFile manifest schema, the claim-check handoff and the two Airflow window calls, and publish them in the activity contract and AsyncAPI before the first SIT run. |
| CDC-07919 | RWB-P4-E1007-APP | GAP-0648 |  | Fix the deliverFile manifest fields (interface ID, business date, case IDs, idempotency key, claim-check link, requesting service), the return element and the three typed failures; fix the notice-fact read in the rwb-comms contract. |
| CDC-07921 | RWB-P4-E1007-APP | GAP-0739 |  | Fix the delivery-event element names, the route state to resume from the latest decision-record entry, the task code and due date as rwb-case reference rows, and the in-process interfaces as internal listener services. |
| CDC-07927 | RWB-P4-E1007-APP | GAP-2229 | n/a | Confirm the FileFailed and FileDelivered element names, the resume-state carrier and the owner task code and due-date values at contract review. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07821 | RWB-P4-AD016-APP | CG-ALL-4821 | 4, 14 | Add a message ID for the reference-data read, parameter read or store unavailable case, text 'The service is busy. Try again in a few minutes.'; the story then cites it in place of MSG-GEN-006 |
| CDC-07825 | RWB-P4-AD016-APP | DOR-RWB-P4-AD016-APP-9 Messages: Partial | 14 | Reverted the MSG-GEN-006 row to its prior text |
| CDC-07835 | RWB-P4-AD016-CON | CG-ALL-4832 | 14 | Add a new message ID for the reference-data read, parameter read or store unavailable case, with the text 'The service is busy. Try again in a few minutes.'; the story then cites that ID in 12.1 and 14. |
| CDC-07948 | RWB-P4-E1008-APP | CG-ALL-4866 | 14 | Add a new message ID for 'The caller has no session' with text 'Your session has ended. Sign in again to continue.' for this story to cite. ID: Not specified in the source documents (CG-ALL-4866). |
| CDC-08020 | RWB-P4-E1019-APP | CG-ALL-4907 | 4, 14 | Add a new message ID for 'The caller holds both roles of a conflicting pair' with its text; the story then cites it. MSG-P4-006 keeps the standard's meaning. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07848 | RWB-P4-E1001-APP | DOR-RWB-P4-E1001-APP-14 | header | Record the signed epic design sign-off for RWB-P4-E1001-APP; the story now carries a placeholder row for it. |
| CDC-07904 | RWB-P4-E1007-APP | DOR-RWB-P4-E1007-APP-14 | header | Record the signed epic design sign-off in the epic design record and cite it in the story. |
| CDC-07942 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-14 | n/a | Record the signed sign-off of the epic design in the epic design record. |
| CDC-07990 | RWB-P4-E1018-APP | DOR-RWB-P4-E1018-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-P4 in the epic design record and cite it here. |
| CDC-08017 | RWB-P4-E1019-APP | DOR-RWB-P4-E1019-APP-14 | not located | Record the signed epic design sign-off for RWB-P4-E1019-APP |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07903 | RWB-P4-E1007-APP | CG-ALL-4853 | 12.5 | Register the JOB-18 workflow owned by RWB-P4-AD008-APP on queue rwb-access, or name the catalogued workflow in §12.5. |
| CDC-07907 | RWB-P4-E1007-APP | DOR-RWB-P4-E1007-APP-8 | 12.5 | Register buildAccessReviewFile(reviewDate) and requestFileDelivery(manifest) on queue rwb-access, and clear the two further detcheck entries. |
| CDC-07909 | RWB-P4-E1007-APP | CG-ALL-4850 | 12.5 | Add Activities row buildAccessReviewFile(reviewDate) on task queue rwb-access, provided by RWB-P4-E1007-APP. |
| CDC-07910 | RWB-P4-E1007-APP | CG-ALL-4851 | 12.5 | Add Activities row requestFileDelivery(manifest) on task queue rwb-access, provided by RWB-P4-E1007-APP. |
| CDC-07911 | RWB-P4-E1007-APP | CG-ALL-4852 | 12.5 | Add Activities row deliverFile(manifest) on task queue rwb-integration, provided by RWB-P2-E1007-CON and called from requestFileDelivery. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20561 | RWB-P4-E1019-APP | R-16608 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20563 | RWB-P4-E1007-APP | R-21885 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20564 | RWB-P4-E1007-APP | R-28451 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20567 | RWB-P4-E1007-APP | R-28452 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20568 | RWB-P4-E1007-APP | R-21886 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |

### 06 Data/Recovery Workbench Physical Schema v7 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07860 | RWB-P4-E1001-APP | GAP-0206 | 9 | Relationships sheet: cut the 48 table-to-table foreign keys to business-key columns, keep the 11 v_ace_* references as they are, and show all three cases per row. |
| CDC-07876 | RWB-P4-E1001-APP | GAP-0285 | 18 | RWB-PLT-NF06-DB row marks the cut of built tables as Not specified (GAP-0285) |
| CDC-07883 | RWB-P4-E1001-APP | GAP-0112 |  | Define one V0001 baseline per service schema, with the view file following the source V0002 and V0003 sections (DP-15, ADR-021). |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08002 | RWB-P4-E1018-APP | GAP-2433 | find it | Write MSG-P7-009 as one sentence naming the field and the case reference, and MSG-P7-012 as one warning naming the chain position; add both rows to the API specification before wave 1. |
| CDC-08005 | RWB-P4-E1018-APP | GAP-2434 |  | Add finalCall to the query parameters of API-P7-006 and fix the creation-filter answer as a page of entries with a stated field set. |
| CDC-08009 | RWB-P4-E1018-APP | GAP-0982 |  | Add the case-authority request and answer schema for POST /authorise, publish with RWB-P4-E1037-CON, record where caller teams and regions are held, and list case-record personal field IDs with version |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20771 | RWB-P4-E1008-APP | R-16592 |  | A new ID for the no-role message is not in the sources. VR-P4-001-1 keeps MSG-P4-001. The no-session row belongs to RWB-P4-E1008-APP section 14. |
| CDC-20774 | RWB-P4-AD016-APP | R-28981 |  | MSG-P1-002 and MSG-P7-010 shared catalogue entries belong to the P4 message list, not this FSD. |
| CDC-20775 | RWB-P4-E1008-APP | R-16592 |  | Duplicate of the R-16592 row above, kept as its own disposition for this item. Section 14 no-session MSG-P4-001 is in RWB-P4-E1008-APP. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07836 | RWB-P4-AD016-CON | DOR-RWB-P4-AD016-CON-1 | 1 | Add 'tech lead' as a role code or role name, or record it there as a non-system persona; section 1 keeps 'tech lead' unchanged. |
| CDC-08022 | RWB-P4-E1019-APP | DOR-RWB-P4-E1019-APP-6 | 10 | Add role SY-DATALOAD. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07852 | RWB-P4-E1001-APP | DOR-RWB-P4-E1001-APP-11 |  | Set the personal-data class to none for the P2 fields of the five rwb_access tables, consistent with story BR8 (no personal data in the schema). |
| CDC-07951 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-11 | - | Classify the P2 fields of decision_record, including actor_user_id and the case reference, as personal data or not. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07853 | RWB-P4-E1001-APP | DOR-RWB-P4-E1001-APP-12 | 12.7, 16, 18 | Add TC-E1-001-13 to Test Cases v8 and to RTM v7 REQ-RDF-001; align the other section 18 test lists with RTM v7. |
| CDC-07989 | RWB-P4-E1018-APP | DOR-RWB-P4-E1018-APP-12 | 16 | Add TC-E1-018-15 and TC-E1-018-16 to the workbook tab; align section 18 test lists with RTM v7. |

### RWB-P1-E1001-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07856 | RWB-P4-E1001-APP | GAP-0557 | 12.7 | Adopt the wave 1 assumptions: keep the built baseline as built; create P1's 13 own tables from its split migration; name schema and login rwb_source_data; leave the four extension tables to RWB-P1-E1069-DB; keep catalog, dictionary and v_data_dictionary in rwb_source_data with no REST operation added. |
| CDC-07874 | RWB-P4-E1001-APP | GAP-2539 |  | Correct the DP13 system-of-record wording to name ACE for the money facts and the Workbench for the match. |

### OTHER:Mapping v4 (field mapping workbook) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07861 | RWB-P4-E1001-APP | GAP-0210 | 9 | Keep the 11 ACE entity names word for word. Set target schema rwb_source_data and owner P1 for their fields, read through the rwb-source-data contract. Add the four extension tables as Workbench targets at the next revision. |
| CDC-07862 | RWB-P4-E1001-APP | GAP-0211 | 9 | Add 'Target schema' and 'Owning service' to the Mapping and ACE gaps sheets, one value per row from the Ownership Map Tables sheet. Keep columns A to N unchanged. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07872 | RWB-P4-E1001-APP | GAP-2537 |  | Record the handover of the 9 field rows as a build artefact of this story to the one dictionary seed, proven by the conformance test. |
| CDC-07875 | RWB-P4-E1001-APP | GAP-0150 |  | Record the split of the single recovery schema into one rwb_* schema per service as new work (RWB-PLT-NF06-DB and per-service DB stories); keep the 92-table and 30-view counts. |

### OTHER:ERD v5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07885 | RWB-P4-E1001-APP | GAP-0115 |  | Draw the v5 references unchanged. State sys_fields.object_name and sys_objects.data_product separately in the reconciliation table. |
| CDC-07886 | RWB-P4-E1001-APP | GAP-0116 |  | Group v5 objects by Ownership Map owner, add a cross-service reference table, and keep the v5 data-product table as section 3. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07914 | RWB-P4-E1007-APP | GAP-0673 |  | Mark the FSD P2 Integration v3 A1.5 and TSD T1/T5.1 INT-03 lines superseded for the ALS legacy key, with date and decision; load the ALS interface_config row per environment. |
| CDC-08028 | RWB-P4-E1019-APP | GAP-1176 | 4 | State that queue, team code, role code and version are read from P3 and role, rights and scope from P4; publish or withdraw a membership operation on RWB-P3-E1019-CON. |

### RWB-PLT-TE006-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07915 | RWB-P4-E1007-APP | GAP-1416 |  | Fix one versioned artifact, the three interfaces with exceptions, the four-table DDL with processed_event and idempotency_key columns, the CloudEvents attribute set, the retry ladder and the dead-letter topic. |
| CDC-07968 | RWB-P4-E1008-APP | GAP-1232 | 7 | Publish the rwb-<short>_app login convention and an owner role; keep the migration account separate from the runtime login; name the template version of the three library objects. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07936 | RWB-P4-E1007-APP | GAP-1546 |  | State the INT-17, INT-18 and INT-22 paths as reused ACE capabilities with no P2 build and no FR. Record that their behaviour is ACE's. |
| CDC-07937 | RWB-P4-E1007-APP | GAP-1547 |  | Record the FSD transport sentence as superseded. State that the partner and document channels keep their own contracts (rwb-partner, rwb-document) and that P2 carries no requirement for them. |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07991 | RWB-P4-E1018-APP | DOR-RWB-P4-E1018-APP-22 | 13 | Publish a fake version of the authorise and permission operations and record its number in section 13 configuration. |
| CDC-08018 | RWB-P4-E1019-APP | DOR-RWB-P4-E1019-APP-22 | not located | Publish the contract fake library version this story consumes; no version number is in the source documents |

### OTHER:rwb-source-data entry-candidates contract (RWB-P1) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07997 | RWB-P4-E1018-APP | GAP-0575 | find it | Return breaks[] in the same response: one row per key and view with no matching row, with keyType ACCOUNT or PERSON, businessKey, viewName and businessDate; no dq_ table; the durable list stays with RWB-P1-E1011-APP. |
| CDC-08000 | RWB-P4-E1018-APP | GAP-0576 | find it | Return product_group as the product_category value the view returned, unvalidated and unmapped; a value outside LOV-PRODUCT is returned as read and never coerced, dropped or defaulted. |

### RWB-P3-E1018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08001 | RWB-P4-E1018-APP | GAP-0676 | find it | Agree the field-level schema with the consuming teams: required flags per operation, page and sort parameters of GET /cases, caseNo pattern, and error codes per operation. |
| CDC-08013 | RWB-P4-E1018-APP | GAP-1038 |  | Name the rwb_document login and grants under DP-02; publish the case-read field names and not-found message ID in RWB-P3-E1018-CON |

### RWB-P3-E1019-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08026 | RWB-P4-E1019-APP | GAP-0681 | 4 | Publish the Queues template as an xlsx workbook with one header row per sheet (QUEUE, QUEUE_MEMBER), one column per field and one check per required column. |
| CDC-08031 | RWB-P4-E1019-APP | GAP-3159 | 3 | Stop loading role in P3; read roles from rwb-access by contract; keep queue, queue_member and reference tables in P3. |

### OTHER:Recovery Workbench TSD P4 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08034 | RWB-P4-E1019-APP | GAP-1574 | 3 | Publish the approved role conflict list with its version label and effective dates; add the matrix effective-date column to T3.1 or state where it lives; confirm role and permission row counts. |
| CDC-08035 | RWB-P4-E1019-APP | GAP-1567 | 3 | Drop lov_value and partner_user from T3.1; keep lists of values in TSD P3 and partner identity in TSD S9; state in the rwb-access contract the list versions and partner attributes read and the refresh rate. |

### 06 Data/Recovery Workbench Source to Target Mapping v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20516 | RWB-P4-E1001-APP | R-21849 |  | Mapping v4 ACE entity rows could not be read with the permitted tools. No exact old text, so no fix written. Needs a fix in a later run. |
| CDC-20517 | RWB-P4-E1001-APP | R-21850 |  | Mapping and ACE gaps sheet headers could not be read with the permitted tools. No fix written. Needs a fix in a later run. |

### RWB-P4-AD016-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07818 | RWB-P4-AD016-APP | DOR-RWB-P4-AD016-APP-21 | header | Move build status from Not started to Done so the contract is published. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07820 | RWB-P4-AD016-APP | CG-ALL-4820 | 12.3 | State the payload of rwb.access.DoaLimitChanged.v1: limitVersion, table delegation_limit, change kind approved, validFrom, validTo, rowCount, and no personal data, as in RWB-P4-AD016-APP section 12.3. |

### OTHER:P4 message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07827 | RWB-P4-AD016-APP | GAP-0837 | find it | Add MSG-P1-002 and MSG-P7-010 word for word to the P4 catalogue as shared entries, keeping one message id each. |

### OTHER:wp/B-P4-04.md and wp/B2-P4-010.md (plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07828 | RWB-P4-AD016-APP | GAP-2278 | find it | Keep one Work Package for RWB-AD-016: remove it from the B-P4-04 fanout, number CG and ASM rows once, add a plan-uniqueness check to checks/run_all.py. |

### OTHER:Message catalogue standard (P2 MSG-GEN-006 entry) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07838 | RWB-P4-AD016-CON | DOR-RWB-P4-AD016-CON-9 | 14 | Confirm the standard's meaning of MSG-GEN-006 and align the availability use or its ID; section 14 keeps MSG-GEN-006 meanwhile. |

### OTHER:RWB-P3 reference-data contract review (rwb-case contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07839 | RWB-P4-AD016-CON | GAP-1564 | 1 | Confirm load, approve, verify and rollback stay with rwb-case and rwb-access publishes the lookup answers; otherwise restore API-P4-005, 006, 009 and 010 to P4. |

### OTHER:Reference data administrator at the data review (file layout not in the sources) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07840 | RWB-P4-AD016-CON | GAP-0834 | 11 | Section 11 keeps the row shape by reference to RWB-P4-E1038-APP; no file layout is specified in the story. |

### OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07841 | RWB-P4-AD016-CON | GAP-0836 | 12.1 | Correct appendix T-A API-P4-006 to right A in Rules and parameters for the DoA approval, recorded in the change register. |

### OTHER:wp/B-P4-04.md, wp/B2-P4-010.md and split_plan.json (Work Package set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07845 | RWB-P4-AD016-CON | GAP-2278 |  | Remove RWB-AD-016 from the B-P4-04 fanout so B2-P4-010 alone owns it; number CG and ASM IDs once; add a plan-uniqueness check to checks/run_all.py. |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07855 | RWB-P4-E1001-APP | GAP-0566 | 12.8 | Publish the three read operations with response fields and problem body in RWB-P1-E1069-CON; record the view SQL, helper functions and conformance test as rwb-source-data's application slice, the login, grants, view owner and four extension tables as its database slice, and the 19-login proof as the wave 1 integration slice. |

### OTHER:Data product workbook v3 (Ownership and Ownership split sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07863 | RWB-P4-E1001-APP | GAP-0224 | 9 | Add 'Owning service (D-RCV-60)', 'Owning schema (D-RCV-60)' and 'Basis (D-RCV-60)' at the end of both sheets, one owner per data product from the Ownership Map. Keep columns A to K unchanged. |

### OTHER:TSD P4 v3, table T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07867 | RWB-P4-E1001-APP | GAP-0976 |  | Mark lov_value, partner_user and the four rule tables as the monolith module view, superseded by the ownership rulings and Architecture v5 slide 41. |

### OTHER:Functional specification P1 field catalogues (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07869 | RWB-P4-E1001-APP | GAP-1512 |  | Add placeholder field lists for data_contract, dp_treatment, dp_guarantee_claim and efs_ledger_outcome, to be fixed at the TSD review before wave 2. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07870 | RWB-P4-E1001-APP | GAP-2123 |  | Assign the rwb_valuation tables to S1 rwb-valuation so component and integration tests have a schema to seed. |

### OTHER:TSD P8 v? table T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07873 | RWB-P4-E1001-APP | GAP-2538 |  | Record case_id, treatment_id and account_payment_id on proceeds as uuid values with no foreign key. |

### OTHER:Recovery Workbench Security and Access Design v4 (to v5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07880 | RWB-P4-E1001-APP | GAP-2035 |  | Rewrite section 7 per service: one login rwb_<short> per service, grants on the own schema only, rwb_source_data sole holder of the view grant, recovery_svc row replaced by a service login isolation row. |

### OTHER:FSD P4 v3 (field catalog) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07881 | RWB-P4-E1001-APP | GAP-0980 |  | Keep role.entra_group as the TSD DF-REF-039 column, nullable and empty; read the group mapping at run time through the rwb-source-data contract; state it is not a copied ACE fact. |

### OTHER:v4 Mapping (Mapping rules) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07889 | RWB-P4-E1001-APP | GAP-0215 |  | Add contact_point_ext, account_ext and valuation_ext to the Extension fields rule. Leave the 133 field rows unchanged until LDM v10. |

### OTHER:v4 Mapping (column B) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07890 | RWB-P4-E1001-APP | GAP-0216 |  | Leave the data product cell empty for the 81 blank rows. Do not guess a DP code; assign at the next LDM revision. |

### OTHER:v4 Mapping (DP06 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07891 | RWB-P4-E1001-APP | GAP-0226 |  | Record S5 as owner of the Workbench asset data set. ACE collateral and valuation stay a P1 read, and valuation_ext stays P1, as the basis cell states. |

### OTHER:Recovery Workbench Data Ownership and Stewardship register (next revision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07898 | RWB-P4-E1001-APP | GAP-0234 |  | Replace 'Application owner (DL02)' in Ownership rows DP03, DP08, DP09, DP10, DP12, DP14 with the owning service named in the appended column; change 'Read and write by the recovery module' in Ownership split rows 7 and 8 to the owning service and its rwb_<name> schema. |

### OTHER:Recovery Workbench Target Architecture v6 (slide 11) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07899 | RWB-P4-E1001-APP | GAP-1984 |  | Record 92 as the version 6 monolith count that the physical schema work replaces, and state the target as 93 (87 Workbench tables plus 6 platform library tables) once, as in Ownership Map v1 sheet Tables. |

### OTHER:Recovery Workbench Target Architecture v6 (call-type and change tables) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07900 | RWB-P4-E1001-APP | GAP-2062 |  | State the retry and dead-letter policy (1 min, 10 min, 1 h, then .dlt and alert) as the target for every topic; use 12 partitions, RF 3, 7 days for rwb.payment.events.v1 as default until RWB-PLT-EVT sets each service; record the open point in the change table. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07901 | RWB-P4-E1007-APP | CG-ALL-4848 | 12.2 | Publish POST /api/recovery/document/v1/documents in rwb-document.yaml through the provider (P5) CON story; no story edit. |

### OTHER:BRD Program v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07908 | RWB-P4-E1007-APP | GAP-1534 | 4 | Correct section 5.2: remove INT-19 and INT-20 as outbound lake adapters; INT-19 is a delivery request from rwb-reporting via rwb-integration; INT-20 is continuous ingest in rwb-decision (JOB-13). |

### OTHER:Phase 3 screen specification (SCR-43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07912 | RWB-P4-E1007-APP | DOR-RWB-P4-E1007-APP-10 |  | Define empty, loading, error and no-access states for SCR-43 in the P3 screen specification. |

### OTHER:TSD P2 Integration v3 and the rwb-integration story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07918 | RWB-P4-E1007-APP | GAP-0647 |  | Record that TSD P2 v3 T1.1, T5.2 and T6.2 direct-view wording is superseded by Architecture v5 and ADR-010; build the outbound capability on /api/recovery/integration/v1; retire the lake statements of INT-19, INT-20, JOB-13 and JOB-15. |

### OTHER:Operations story for the outbound-file deployment and the bank Airflow owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07920 | RWB-P4-E1007-APP | GAP-0650 |  | Set chart values, replica counts, KEDA threshold, lag and alert thresholds and build ID format as environment values; record that no Schedule or timer is registered for either file window. |

### OTHER:rwb-comms outbound-file story for INT-14 and its contract list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07922 | RWB-P4-E1007-APP | GAP-1162 |  | Add the rwb-source-data read that returns the postal addressee by party_id (2 s budget, fake) to the INT-14 story's contract list; keep the value out of rwb_comms, events and logs. |

### OTHER:rwb-comms interface-monitor story and the gateway-bff owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07923 | RWB-P4-E1007-APP | GAP-1166 |  | Answer run state from dispatch fields, workflow run and P2 status; provide one read and one rerun on the service base; enforce the monitor right at gateway-bff; confirm any local guard with the edge owner. |

### OTHER:FSD P2 v3, section A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07924 | RWB-P4-E1007-APP | GAP-1536 |  | Remove JOB-10, JOB-13 and JOB-15 as P2 triggers; the Ownership Map owner stands; rwb-integration registers no Temporal Schedule and provides delivery only. |

### OTHER:FSD P2 v3 section A2.2 and AC-EXC-P2-001-01 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07925 | RWB-P4-E1007-APP | GAP-1537 |  | State that the bank scheduler owns the window, its opening time and re-runs; the service owns the attempt ladder, the exception state and the owner task; DL11 holds the single retry-count owner. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07926 | RWB-P4-E1007-APP | GAP-1544 | n/a | Inherit the programme targets for every service; state interface-level volume and window targets as open under DL11 with placeholder R9. |

### OTHER:Build Notes v6 (RWB-E1-007 View note) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07928 | RWB-P4-E1007-APP | GAP-3160 | n/a | Stop the P2 adapter writing debt_sale_account and recovery_case; S6 owns debt_sale_account through a contract call or event from P2. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07932 | RWB-P4-E1007-APP | GAP-0981 |  | Register one OUTBOUND interface row for the access-review file (interface ID, file pattern, data product, owner role, alert role). Publish extract layout and recipient in RWB-P4-AD008-APP and state the review-cycle date convention. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Events sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07933 | RWB-P4-E1007-APP | GAP-1538 |  | Add rows for FileDelivered and FileFailed: producer rwb-integration, topic rwb.integration.events.v1, consumers requesting service, keyed by case ID. No numbered EV ID is given in the sources. |

### OTHER:Interface configuration retry rows and FSD P2 v3 AC-EXC-P2-001-01 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07934 | RWB-P4-E1007-APP | GAP-1540 |  | Keep retry values as interface configuration rows. State the FSD attempt intervals as the acceptance criterion and the row values as configuration in force. Fix neither as a product rule. |

### OTHER:FSD P2 v3 (A1.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07935 | RWB-P4-E1007-APP | GAP-1542 |  | Move FEAT-DRI-09, the inbound half of FEAT-RDF-21, FEAT-DRI-10, FileLoadAdapter, DQ-057, DQ-059, JOB-09, interface_run and interface_signoff to an explicit exclusion table with later home. Add no FR, NFR or AC. State that no inbound adapter, folder, run or sign-off exists. |

### OTHER:Legacy dependency trace sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07938 | RWB-P4-E1007-APP | GAP-3233 | find it | Keep the five Not carried rows visible in the trace; add an X row only if the run books or the harness waits for the named story |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; OTHER:test data owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07941 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-12 | 7, 16, 18 | TC-E1-008-11 to -14 added; data for TC-11 to -14 Not specified. |

### OTHER:Squad sizing at refinement (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07943 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-16 | header | Size row states Not specified in the source documents. |

### OTHER:Story backlog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07944 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-21 | header | RWB-P4-E1008-CON not listed; header keeps RWB-P7-E1008-CON only. |

### OTHER:rwb-source-data contract fake (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07949 | RWB-P4-E1008-APP | CG-ALL-4872 | 12.8 | Publish a rwb-source-data contract fake for the AC8 customer data, so the Given lines can be written against it. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07950 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-10 | 15 | SCR-38 and SCR-43 state rows added to section 15 |

### OTHER:03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07952 | RWB-P4-E1008-APP | DOR-RWB-P4-E1008-APP-9 | 14 | VR-P4-001-1 gives MSG-P4-001 a no-role meaning. Give the no-role message its own ID; MSG-P4-001 stays the no-session message in RWB-P4-E1008-APP section 14. |

### RWB-P4-E1037-APP; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07953 | RWB-P4-E1008-APP | GAP-0975 | find it | Read every 'rwb_access baseline' reference as the version applied by RWB-P4-E1001-APP; RWB-P4-E1037-CON keeps the contract stub and creates no table. |

### OTHER:AsyncAPI document for rwb.decision-record.v1 (shared-topic contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07954 | RWB-P4-E1008-APP | GAP-0332 | find it | Publish the DecisionRecorded payload and ingest rule: CloudEvents id as dedupe key in processed_event, per-case order from producer, chain_seq and prev_hash assigned by rwb-decision under the chain lock, catch-up within five minutes, before the first SIT run. |

### OTHER:sibling P7 story E2028 (declares POST /decision-log) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07955 | RWB-P4-E1008-APP | GAP-1224 | 11 | Remove the POST /decision-log declaration; the Ownership Map does not own it and the ledger is written only by the ingest of rwb.decision-record.v1. |

### OTHER:FSD module P7 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07956 | RWB-P4-E1008-APP | GAP-1226 | find it | Withdraw FEAT-DRI-06 and its lake acceptance criteria; keep JOB-13 as continuous ingest and JOB-14 as the 02:00 chain check with the WORM seal; record RWB-E1-014 retired by the ledger. |

### RWB-P7-E1008-CON; OTHER:integration harness of wave 1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07957 | RWB-P4-E1008-APP | GAP-1227 | 11 | Strict-mode confirmation read set to Not specified in the source documents. |

### RWB-P7-E1008-DB; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07958 | RWB-P4-E1008-APP | GAP-1231 | find it | Drop fk_decision_log_entry_case_id; keep case_id as a plain uuid verified through P3's case contract; record the same ruling for every legacy cross-module key of the decision log. |

### OTHER:RPO and RTO standard for the append-only ledger (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07959 | RWB-P4-E1008-APP | GAP-1234 | 3 | Restore gate sentence removed from section 3; RPO and RTO stay Not specified |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:Technical Specification P7 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07961 | RWB-P4-E1008-APP | GAP-1622 |  | Add a contract version to DecisionRecorded and a schema version field to decision_log_entry (DF-DEC-001 to DF-DEC-031). |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07962 | RWB-P4-E1008-APP | GAP-1617 |  | Add reference-data rows: completeness target 5 minutes, gap alert threshold 5 minutes, and strict-mode wait bound Not specified (confirm at ADR-022 sign-off). |

### OTHER:rwb-decision deployment configuration (DevOps lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07964 | RWB-P4-E1008-APP | GAP-1233 | none | Adopt consumer group rwb-decision-ledger; alert at 5 minutes of lag and at the first dead letter; run the append-only verification job one hour before the 02:00 chain check; agree a per-environment WORM path with the storage owner. |

### RWB-P7-E2005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07965 | RWB-P4-E1008-APP | GAP-1229 | 7 | Publish page 1, size 50, maximum 200, and an RFC 9457 problem body with type, title, status, detail and message identifier for the decision-log reads. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07966 | RWB-P4-E1008-APP | GAP-0984 | 7 | Publish the decision_record column set, physical types and canonical-form rule; add DECISION_LOG to the TSD P4 RBAC matrix; fix per-service login names in the platform DB story; state the local verifier behaviour in the Temporal and Drools design. |

### RWB-P7-E1008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07967 | RWB-P4-E1008-APP | GAP-1228 | header | State that the DP-09 library objects are created by RWB-P7-E1008-DB and the consumer is built against the published template, or add DP09 and RWB-PLT-TE006-CON to the H row. |

### RWB-P4-E1016-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07973 | RWB-P4-E1016-APP | DOR-RWB-P4-E1016-APP-21 | header | Create contract story RWB-P4-E1016-CON that publishes the 12.1 operations, then record it as a contract dependency. |

### OTHER:rwb-access contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07974 | RWB-P4-E1016-APP | DOR-RWB-P4-E1016-APP-22 | header | Publish the contract fake library version for rwb-access and record it against this story. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07976 | RWB-P4-E1016-APP | DOR-RWB-P4-E1016-APP-12 | 12.7, 16, 18 | Add the rows for TC-E1-016-01 to TC-E1-016-15 that Test Cases v8 lacks (the P2 part is under CG-ALL-4881). Align the §18 test lists of this story with RTM v7. |

### OTHER:rwb-source-data contract (entry-candidate read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07978 | RWB-P4-E1016-APP | GAP-0571 | 12.1 | Publish GET /api/recovery/source-data/v1/entry-candidates with businessDate and threshold required, page and size optional, the EntryCandidatePage response, status set 400, 401, 403, 409, 422 and 503, and its access rule. |

### OTHER:Technical Specification P1 v3 (TSD P1 v3); OTHER:T3.6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07979 | RWB-P4-E1016-APP | GAP-0481 | 2 | Remove masking_rule from the P1 schema and from P1's masking application; P1 holds data_product_access only and takes the masking answer from POST /api/recovery/access/v1/authorise and the FieldMasker interface of RWB-P4-E1037-CON, one hop with a 2 s timeout; no masking, role or permission table in any query. |

### OTHER:data_product_access seed DPA-2026.11 (rwb-source-data reference data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07980 | RWB-P4-E1016-APP | GAP-0482 | find it | Seed only the six rows the sources give: RW-CASEOWN and RW-AUDIT on DP02; RW-PHONECOL on DP01, DP02, DP03 and DP05. Leave other roles and products to a later approved load; data steward closes the gap before use outside SIT. |

### RWB-P1-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07981 | RWB-P4-E1016-APP | GAP-0483 | 16 | Approved load arrives as reference data for table code data_product_access through the rwb-case reference-data contract; a handler in rwb-source-data replaces DataProductAccessLoader; the service exposes no load endpoint of its own. |

### RWB-P1-E1016-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07983 | RWB-P4-E1016-APP | GAP-0484 | 16 | Deliver the three indexes, read model v_data_product_catalog, DPA-2026.11 seed, 122/1,366 dictionary conformance check and schema checks; create no table already created by RWB-P1-E1001-APP or RWB-P1-E1069-DB; a repeated run changes nothing. |

### OTHER:TSD P4 appendix T-A and the rwb-access OpenAPI file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07984 | RWB-P4-E1016-APP | GAP-0983 | 15 | Publish request and answer schemas of GET /admin/roles, GET /masking-policies and POST /authorise, with marker values, the maskingExceptions part, matrix_version and masking_version fields, and the access resolution in the request. |

### RWB-P5-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07985 | RWB-P4-E1016-APP | GAP-1028 | find it | Accept six new criteria as P5 deliverable and record the split; publish GET /api/recovery/document/v1/retention-classes and .../{classCode} with RetentionClass shape of RWB-P5-AD021-CON; consume P4, P3, P1 operations as published contracts with fakes; inherit guard library and gateway route; no H dependency; login per proposed fix |

### RWB-P4-E1037-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07992 | RWB-P4-E1018-APP | DOR-RWB-P4-E1018-APP-8 | 13 | Add POST /authorise and GET /me/permissions under /api/recovery/access/v1; replace the closed defaultScope enum with a reference to LOV-SCOPE as data. |

### OTHER:FSD P3, section A1.5 (What P3 needs table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07993 | RWB-P4-E1018-APP | GAP-1549 | 8 | Restate the A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### RWB-ITG-E1018-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07994 | RWB-P4-E1018-APP | GAP-0574 | 16 | While v_ace_batch_status is absent, the entry read answers 409 with MSG-P1-001, no candidate, no break row, DP01 never stamped LOADED; gate read from the view only, never inferred. |

### OTHER:rwb-source-data service API document (RWB-P1) and the rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07996 | RWB-P4-E1018-APP | GAP-0571 | find it | Publish GET /api/recovery/source-data/v1/entry-candidates with required query parameters businessDate and threshold, optional page and size; response EntryCandidatePage with businessDate, threshold, asOf, page, size, total, candidates[] and breaks[]; statuses 400, 401, 403, 409, 422, 503; OpenAPI 3.1 fragment of the three operations. |

### OTHER:RWB-SVC-P3 database story and the service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07998 | RWB-P4-E1018-APP | GAP-0675 | find it | Allocate the rwb-case login name Not specified in the source documents (GAP-0675), with grants on schema rwb_case only and no privilege on another schema; record it in the service catalogue. |

### OTHER:RWB-P1 rwb-source-data API file and the rwb-case exclusion-screen story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07999 | RWB-P4-E1018-APP | GAP-0573 | find it | P1 writes account_ext.dispute_open and party_ext through two PUT operations by business key, called through gateway-bff; the body carries all four party flags; a repeated body leaves one row; a changed body replaces the flags with a version increment. |

### OTHER:TSD P7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08003 | RWB-P4-E1018-APP | GAP-2435 | 11 | Restate DF-DEC-002 as an indexed business key with no foreign key, drop the recovery_case row of T3.3, and state in T3.1 that the ALS business date is carried inside inputs_ref. |

### OTHER:Package ENTRY rule workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08004 | RWB-P4-E1018-APP | GAP-2436 |  | Name the admitting rule ID in the rule-row catalogue of package ENTRY so the registry fixture of this story can copy it. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08006 | RWB-P4-E1018-APP | GAP-0674 | 15 | Publish the gateway-bff composite route for SCR-02 and SCR-03 with its path, parallel calls, merge order, masking rules and 2 s budget. |

### OTHER:Work package C-WEX index (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08007 | RWB-P4-E1018-APP | GAP-3206 |  | Read the (E1-018) heading as a scheduling label, keep RWB-E1-020 as the subject, and correct the heading in the WP index on the next run. |

### OTHER:RWB-E1-069; OTHER:RWB-E1-018 and RWB-E2-006 slices (section 18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08008 | RWB-P4-E1018-APP | GAP-3213 |  | Add REQ-RDF-004 to the section 18 trace of each legacy slice, or accept the E3 integration trace; list the citing stories in the v7 row |

### RWB-P7-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08010 | RWB-P4-E1018-APP | GAP-2437 |  | Record that the slice builds against platform contracts and section 12.8 fakes and reads same-service wave-1 tables in its own schema; no dependency row changes |

### OTHER:ASM-B-P1-07-E1018-2 and the rwb-source-data entry-read contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08011 | RWB-P4-E1018-APP | GAP-0572 |  | Fix one business-date operation paged by page and size with published default and maximum page size; refuse a per-account read as fan-out under DP-11 |

### OTHER:rwb-case deployment topology and environment values (platform template) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08012 | RWB-P4-E1018-APP | GAP-0677 |  | Publish cluster, node pools, replicas, resources, zone spread, ingress class and probe settings as values files, not chart defaults |

### OTHER:RWB-PLT-DB and the secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08014 | RWB-P4-E1018-APP | GAP-2438 |  | Fix the rwb-decision login name in RWB-PLT-DB and the secret store, with migration and application roles kept apart, and reference it from every P7 story |

### OTHER:Screen specification of SCR-43 (owner not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08021 | RWB-P4-E1019-APP | DOR-RWB-P4-E1019-APP-10 | 13 | Supply the empty, loading, error and no-access states of SCR-43 |

### OTHER:Message catalogue of P2 (MSG-P4-006 entry) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08024 | RWB-P4-E1019-APP | DOR-RWB-P4-E1019-APP-9 | 14 | Align the meaning of MSG-P4-006 with the standard or rename the conflicting-pair message in P2. |

### OTHER:rwb-access OpenAPI document (GET /me/session) and rwb-comms OpenAPI document (notice response) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08025 | RWB-P4-E1019-APP | GAP-0344 | 4 | Publish the team scope field for GET /me/session and the queue and team code fields of the notice response, or record them in the Service Contract Catalog. |

### OTHER:Later rwb-case contract story (rollback and verify operations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08027 | RWB-P4-E1019-APP | GAP-0682 | 5 | Publish POST /admin/reference-loads/{loadId}/rollback and .../verify in a later rwb-case contract story, owned by rwb-case per the ownership map. |

### RWB-P6-E1019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08029 | RWB-P4-E1019-APP | GAP-1178 | 16 | Carry TC-E1-019-13 in RWB-P6-E1019-APP as the guard test of the routing read, and record in the register that the load-path proof is owned by RWB-P3-E1019-APP. |

### OTHER:TSD P6 Communications v2 (P6 API file) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08030 | RWB-P4-E1019-APP | GAP-1179 | 12.1 | Add the routing read operation with an allocated API identifier at the next module API revision; this story keeps the section 12.1 shape fixed until then. |

### RWB-P4-E1001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08033 | RWB-P4-E1019-APP | GAP-0979 | 4 | Primary key on id; unique role_code; foreign key permission.role_id; one index per read path with the leading columns of section 13; constraint names Not specified in the source documents (GAP-0979) |

### OTHER:rwb-access grant data (access owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08036 | RWB-P4-E1019-APP | GAP-0683 | 3, 10 | Confirm RW-TEAMMGR holds Reference data A for TEAM, QUEUE and QUEUE_MEMBER and record the grant as rwb-access data; 403 MSG-P4-002 stays the refusal. |

### OTHER:Service template (reference reader caching rule) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08037 | RWB-P4-E1019-APP | GAP-1177 | none in story | State that a reader may cache for the life of one call only; a longer-lived cache is an owner contract with a version and an invalidation event. |

### OTHER:Control register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08038 | RWB-P4-E1019-APP | GAP-1180 | none in story | Register CTL-08 with its text, owner and evidence; cite the register row from the stories that apply it. |

### 05 Technical architecture/Recovery Workbench Availability Performance and Recovery Design v3.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20629 | RWB-P4-E1008-APP | R-21903 |  | Bash is unavailable so docview.py could not run, and Read cannot parse the .docx. The exact restore-gate and RPO/RTO text is unknown, so no exact old text exists to replace. Rerun with Bash. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20672 | RWB-P4-E1007-APP | R-21890 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21890', 'R-28478', 'R-28528', 'R-28558', 'R-28573', 'R-28662'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0012 | 19 schemas, logins and the connection budget are not created | ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0062 | Wave conflict P8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0100 | Ownership Map endpoints are the monolith operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0107 | The Ownership Map 'FK cuts' sheet has no rows while 48 cross-owner foreign keys exist | Architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0108 | rwb-valuation owns no table in the Ownership Map | Architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0109 | The map does not say which schema holds the six PLT library tables | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0112 | The per-service Flyway sequence is not specified | ACE team | Resolved (directive) |
| GAP-0113 | The four extension tables have no table comment | Data steward | Resolved (directive) |
| GAP-0114 | lake_copy_watermark has an owner but no target | Architecture team | Resolved (directive) |
| GAP-0115 | ERD v5 draws 90 foreign keys and Physical Schema v6 has 92 | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0116 | ERD v5 has no owner or service grouping | Architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0150 | FEAT-RDF-01 still creates one recovery schema of 92 tables while D-RCV-60 gives each service its own schema | ACE database team lead and the platform DB solution architect | Resolved (directive) |
| GAP-0202 | The 30 recovery.v_ace_* views have no row in the Ownership Map, so the model gives them no owner | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0206 | The 104 relationships are single-schema references and the Ownership Map's FK cut sheet is empty | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0210 | Eleven 'Workbench entity' names in v4 are ACE entities with no row in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0211 | v4 has no owner column and no target schema, so ownership is carried only by the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0212 | The 'By source' sheet counts the extension field against ACE table 'recovery' | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0213 | Five rows still cite 'number in Interface Specifications v3' after v4 of that document was issued | Integration architecture team | Resolved (directive) |
| GAP-0215 | Only party_ext appears in the mapping; the other three extension tables are absent | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0216 | 81 of the 133 field rows carry no data product | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0224 | v3 states no owning service and no owning schema for any of the 14 data products | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0225 | DP04 Treatment and offers has three owners after the realignment | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0226 | DP06 Collateral and assets mixes ACE data, S5 asset records and a P1 extension table | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0227 | DP07 Legal events and cases mixes ACE court records, S4 legal actions and P6 notices | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0228 | DP11 Scores and route economics has no table row in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0229 | DP13 Money and closure mixes P8 proceeds, S7 write-off and ACE payment and GL data | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0230 | DP05 Contact and promises splits into a P1 ledger, P6 letters and a P3 case timeline | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0231 | DP14 Reference data splits into P3 parameters and lists, P4 roles and DoA, and P6 templates | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0232 | The 88 Workbench tables of Tier 4 cannot be reconciled with the 93 rows of the Ownership Map from v3 alone | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0233 | Roles, Change process and Quality measures still describe one Workbench owner, one backlog and one check set | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0234 | Six Ownership rows name 'Application owner (DL02)' and two Ownership split rows name 'the recovery module' | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0285 | No source states how the built recovery schema, 92 tables and 14 data products, is cut across the 19 rwb_* schemas or how each V0001 baseline is produced | ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0332 | DecisionRecorded payload and the ingest rule into the central ledger are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0333 | The owning rwb_* schema of the 24 operational dictionary objects is not stated | ACE database administrator | Resolved (directive) |
| GAP-0334 | deliverFile manifest payload, claim-check handoff and the file-window trigger contract are not defined | Solution architect | Resolved (directive) |
| GAP-0338 | Connection matrix gives rwb-integration only the document REST call and the outside file edge, while the file build reads source data and the failure reaches rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0341 | E1016 catalog composition across rwb-source-data, rwb-access and rwb-document | Solution architect | Resolved (directive) |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0344 | Field names of the P4 session team scope and the P6 notice queue code are not fixed by any source | Service owner of rwb-access and service owner of rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0482 | The data_product_access seed of the version in force is only partly specified | Data steward | Resolved (directive) |
| GAP-0483 | The monolith reference-load endpoint has no target owner for an access load | Tech lead | Resolved (directive) |
| GAP-0484 | The DB slice of this legacy key cannot deliver the table DDL, because two other stories already create the tables | ACE database lead | Resolved (directive) |
| GAP-0557 | RWB-P1-E1001-APP: schema-split mechanics, login name, extension-table delivery boundary and Arch v5 against FSD and TSD P1 | Solution architect | Resolved (directive) |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0571 | The entry-candidate contract: the resource and parameter names, the response entity, its field names, the paging, the error status set and the access rule are not fixed by any source, and this legacy key has no contract story of its own | Tech lead of rwb-source-data with the solution architect and the P3 owner of the case contract | Resolved (directive) |
| GAP-0572 | Whether the entry read is one operation for a business date or one operation per account, and how a page of about 28,100 candidates is cut, are not specified | Tech lead of rwb-source-data with the owner of the rwb-case case creation job | Resolved (directive) |
| GAP-0573 | Which service writes account_ext.dispute_open and the party_ext flags, which right the confirmation needs, and where party_ext.vulnerable comes from on the first write are not settled | Solution architect with the P1 service owner, the P3 owner of the exclusion screen and the P4 owner of the role model | Resolved (directive) |
| GAP-0574 | The ALS batch gate before RWB-ACE-001 lands: v_ace_batch_status is a Section B view, and the behaviour of an entry read for a date whose batch record does not exist yet is not specified | Recovery tech lead with the ACE team lead and the platform team that owns the RWB-ACE-001 sequence | Resolved (directive) |
| GAP-0575 | The shape and the home of the REC-05 break list are not specified, and the table that held it leaves the schema | Data architect with the data steward and the P1 owner of the reconciliation job | Resolved (directive) |
| GAP-0576 | The product group of a candidate row: whether the ACE product_category value is passed through or mapped to the LOV-PRODUCT codes, and what happens to a value outside the list, is not specified | Business analyst, P1 with the center of excellence and the owner of the rwb-case reference data | Resolved (directive) |
| GAP-0647 | rwb-integration outbound-file capability: ACE read path, INT-25 source table, data-lake retirement, JOB-10 and JOB-11 split, operation naming, alert event names, deliverFile manifest and job catalog rows not settled | Solution architect | Resolved (directive) |
| GAP-0648 | Outbound-file contract: deliverFile manifest and return, notice-fact read of rwb-comms, JSON field names and problem body, event schema subject and compatibility level not fixed by any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0649 | Outbound egress infrastructure: endpoint names, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period not specified in any source | SCB IT infrastructure | Resolved (directive) |
| GAP-0650 | Outbound-file deployment: chart values, replica counts, KEDA threshold, lag and alert thresholds, dashboard names, build ID format, Airflow trigger contract of the two file windows and the message identifiers of the lag and window alerts not specified in any source | DevOps team | Resolved (directive) |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0675 | Per-service login name for rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0676 | Field-level OpenAPI schema of the case resource is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0677 | Deployment topology detail for rwb-case is not specified | DevOps engineer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0678 | The per-service database login name of rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0679 | The column-level split of the legacy role and permission tables between rwb-case and rwb-access is not defined | Solution architect | Resolved (directive) |
| GAP-0680 | The column-level definition of queue measures and of the remaining list-of-values columns is not specified | Technical lead, rwb-case | Resolved (directive) |
| GAP-0681 | The queues reference-load template format is not specified | Reference data owner (Shared operations) | Resolved (directive) |
| GAP-0682 | The rollback and verify operations of reference loads sit outside the rwb-case operation set given for this legacy key | Solution architect | Resolved (directive) |
| GAP-0683 | The approver authority for a queues load is assumed, not confirmed | Access owner, rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0739 | The case side of an outbound file outcome leaves the delivery-event element names, the route state to resume, the task code and due date, the fate of the legacy in-process interfaces and the two lake extracts unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0833 | The DoA load and approval paths are not in an approved source, and two P4 stories declare them | Solution architect | Resolved (directive) |
| GAP-0834 | The delegation of authority file format is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0835 | The regulation item list is not enumerated in any source | Business analyst, P4 | Resolved (directive) |
| GAP-0836 | The right that gates the approval is stated as Reference data A in one source and as Rules and parameters A in another, and as a parameter in a third | Security administrator | Resolved (directive) |
| GAP-0837 | MSG-P1-002 and MSG-P7-010 are messages of other catalogues and the P4 message list does not carry them | Business analyst, P4 | Resolved (directive) |
| GAP-0838 | Who raises the incident behind a NOT_COVERED answer is not specified | Solution architect | Resolved (directive) |
| GAP-0839 | The RELATED_PARTY answer does not say whether the reason is a code on the answer or a row condition | Business analyst, P4 | Resolved (directive) |
| GAP-0840 | The field-level schema of the load, approval and lookup answers is not specified | Solution architect | Resolved (directive) |
| GAP-0841 | The DoaLimitChanged event key and payload are not specified | Solution architect | Resolved (directive) |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
| GAP-0843 | The HTTP status of a NOT_COVERED answer is not specified | Solution architect | Resolved (directive) |
| GAP-0857 | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Business analyst, P4 | Resolved (directive) |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0976 | The exact per-service table list of rwb_access is not stated in one place | Solution architect | Resolved (directive) |
| GAP-0978 | The file name and sequence number of the rwb_access baseline migration are not fixed | Tech lead | Resolved (directive) |
| GAP-0979 | The constraint names and the full index set of the five tables are not specified | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-0980 | role.entra_group is a column in the technical specification and not a Workbench column in the functional one | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0981 | rwb-access access-review extract (JOB-18): the interface ID, the file pattern, the extract layout, the recipient and the review-cycle date convention are not specified, the two requester activity names and the manifest are named by no source, and the delivery events are keyed by case ID while an access-review file has no case | Solution architect, P4 with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0983 | rwb-access policy and catalogue answers: no source names the request and answer field set of the role catalogue, the masking policy read or the data-product authorise answer, nor the marker vocabulary or the masking-exceptions part | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0984 | rwb-access local decision-record store: the column set behind the five named columns, the canonical form, the genesis value, the verifier behaviour on write and read, the DECISION_LOG letters per role and the per-service login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0985 | Role version: roster, row counts, role-file layout, matrix effective date, conflict list and MSG-P4-006 text not specified | Security administrator (RW-SECADM), with the reference data administrator (RW-REFADM) | Resolved (directive) |
| GAP-1027 | The secondary P5 slice of RWB-E1-007 has no legacy AC and several document-hub values of the outbound path are not fixed in the sources | Solution architect (P5 document hub, with the rwb-integration contract owner) | Resolved (directive) |
| GAP-1028 | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1038 | The rwb-document login name, the not-found message ID of the case read and the case-read field names are not specified | Solution architect with the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1162 | The addressee and contact value reach the INT-14 file through a contract that is not in the story's contract list, and no source names the operation or its elements | Solution architect, with the P1 and P6 owners | Resolved (directive) |
| GAP-1163 | DP-17 removes the INT-19 reporting extract and the INT-20 decision-log copy, so part of legacy RWB-E1-007 has no target and no replacement in this service | Business analyst and solution architect | Resolved (directive) |
| GAP-1164 | The INT-14 record layout, the file pattern and the claim-check store of the built file are named by no source, and the document contract is not in the story's contract list | Solution architect, with the P2 and P5 owners | Resolved (directive) |
| GAP-1165 | The retired inbound load leaves TC-E1-007-05, TC-E1-007-06 and the file checks DQ-057 and DQ-059 without a target in this service | Business analyst and QA lead | Resolved (directive) |
| GAP-1166 | No source defines a run record, a run operation or the right on the interface monitor for rwb-comms | Solution architect and the gateway-bff owner | Resolved (directive) |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1175 | DP-08 is claimed while the authorise contract and the guard library are in no dependency list | Solution architect | Resolved (directive) |
| GAP-1176 | The split of the legacy role, queue and membership data between rwb-case and rwb-access is not stated, and the membership read has no published operation | Solution architect | Resolved (directive) |
| GAP-1177 | No source decides whether a reader keeps a local cache of the role and queue data | Solution architect | Resolved (directive) |
| GAP-1178 | The legacy reference-load path has no rwb-comms target, so the legacy access case has no endpoint in this service | Test lead | Resolved (directive) |
| GAP-1179 | The P6 API specification has no operation that exposes the approver role and the approver queue of a notice | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1180 | Control CTL-08 is cited by the legacy story and the case story but is absent from the rules register | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1224 | The append path into the central decision ledger is not a published operation | Solution architect with the rwb-decision service owner | Resolved (directive) |
| GAP-1226 | JOB-13 and FEAT-DRI-06 still describe a data-lake copy that the architecture removes | Business analyst P7 with the enterprise architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1227 | The strict-mode confirmation a call waits on is not specified | Solution architect with the integration lead | Resolved (directive) |
| GAP-1228 | The ledger consumes the shared topic and dedupes in an inbox while its patterns and H row carry no DP-09 | Platform event owner with the rwb-decision tech lead | Resolved (directive) |
| GAP-1229 | The paging defaults, the maximum page size and the full error body of the decision-log reads are unpublished | Contract owner of rwb-decision | Resolved (directive) |
| GAP-1230 | The ledger read is /decisions on the architecture slide and /decision-log in the Ownership Map | Solution architect with the contract owner of rwb-decision | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1231 | decision_log_entry.case_id loses the foreign key that the legacy schema and the TSD declare | ACE data architect for rwb_decision | Resolved (directive) |
| GAP-1232 | The rwb-decision login, the schema owner separation and the library-object column set are unspecified | ACE database administrator with the platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1233 | The consumer group, the alert thresholds, the verification job time and the seal target of the ledger are unset | DevOps lead with the platform observability owner | Resolved (directive) |
| GAP-1234 | No RPO, RTO or restore-verification standard exists for an append-only ledger | DevOps lead with the resilience owner | Resolved (directive) |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1280 | LDM v8 states 18 fields for rule_row and a rule_test_case.package_version_id that its fields sheet does not define, and both name cross-schema foreign keys that DP-01 forbids | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1396 | Airflow product, tenancy, DAG names, identity method, timeout and retry values, the DailyCaseRun wait contract and the file-window operation are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1512 | Four tables carry a name, an owner and a purpose but no field list in the read sources | Data architect | Resolved (directive) |
| GAP-1534 | Data lake extracts INT-19 and INT-20 still listed as outbound adapters in FSD P2 v3, removed by Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1535 | FSD P2 v3 has the outbound file read the recovery.v_ace_* views directly; Architecture v5 and ADR-010 reserve the views to rwb-source-data | Solution architect | Resolved (directive) |
| GAP-1536 | Job ownership of JOB-10, JOB-13 and JOB-15 differs between FSD P2 v3 and the Ownership Map | Platform administrator | Resolved (directive) |
| GAP-1537 | Who retries a failed transfer is stated three ways: Airflow, the service retry ladder, or the outbox sender | Solution architect | Resolved (directive) |
| GAP-1538 | FileDelivered and FileFailed have no row in the 31-row Ownership Map event register | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1539 | FSD P2 v3 builds the debt buyer tape from debt_sale_account, a table the Ownership Map gives to S6 rwb-debtsale | Solution architect | Resolved (directive) |
| GAP-1540 | Retry interval values differ between the FSD criterion and the interface configuration used by the service stories | Platform administrator | Resolved (directive) |
| GAP-1542 | FSD P2 v3 keeps removed function and check IDs with no target behaviour | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1544 | No non-functional target is stated for an outbound file itself: size, throughput, window length or volume per day | Solution architect | Resolved (directive) |
| GAP-1546 | The notification and logging rows of the FSD interface register state no Workbench behaviour | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1547 | FSD P2 v3 claims the transport of the partner portal and the document hub; Architecture v5 gives each its own service | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1617 | The ledger completeness target, the gap alert threshold and the strict-mode wait bound have no value in the BRD or the FSD | Solution architect with the platform administrator | Resolved (directive) |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1984 | The Workbench table count is 92 in version 6 and 93 in the Ownership Map | Data architect | Resolved (directive) |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2061 | The source is written for one recovery module and has no per-service target, size or deployment shape | Architecture with RWB-PLT-OBS and RWB-PLT-DB | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2062 | No per-topic sizing exists for the 19 topics; one topic is sized in the architecture | RWB-PLT-EVT with the owning services | Resolved (directive) |
| GAP-2068 | The local decision record has no table, no DDL and no case or trace column | Service owners of the 19 services with P7 rwb-decision | Resolved (directive) |
| GAP-2074 | One chain or 19 chains plus the ledger chain | Service owner P7 rwb-decision with the 19 service owners | Resolved (directive) |
| GAP-2075 | The record that governs while the central ledger lags by up to five minutes | Service owner P7 rwb-decision | Resolved (directive) |
| GAP-2123 | The Ownership Map assigns no table to rwb-valuation although Architecture v5 gives it a schema | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2132 | The recovery table count of the source and the table count of the Ownership Map do not agree | ACE | Resolved (directive) |
| GAP-2229 | Element names of the two delivery outcomes, the carrier of the route state to resume and the values of the owner task are not in the sources | TechX and the rwb-integration contract owner | Resolved (directive) |
| GAP-2230 | The legacy P3 interfaces and the case-action path have no operation in the target case contract | TechX | Resolved (directive) |
| GAP-2276 | The right letters of the service-level load and approval differ between the legacy story and TSD P4 v3 | Solution architect, security administrator role, P4 | Resolved (directive) |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2401 | The LDM states one field count for rule_row and a rule_test_case column its fields sheet does not define, and both TSD P7 and the LDM name cross-schema foreign keys that DP-01 forbids | Solution architect, P7 rwb-decision, with the data owners of rwb_case and rwb_access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2433 | The message text of MSG-P7-009 and of the chain warning MSG-P7-012 is named in the sources but never written | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2435 | TSD P7 still models decision_log_entry.case_id as a uuid with a relationship to recovery_case and gives the row no business-date column | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2436 | The literal rule ID of the ENTER rule of package ENTRY is named in no source | Business analyst, Epic 1 | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2438 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2534 | The DDL of proceeds beyond its columns is not published: constraint names, index names, index columns and the Field IDs of the 7 standard columns | ACE team | Resolved (directive) |
| GAP-2535 | TSD P8 T3.1 carries payment_match_rule as a second table of the module, and the Ownership Map gives P8 one table only | Solution architect | Resolved (directive) |
| GAP-2536 | The read paths that proceeds has to serve, and the screens that read it, are stated in no source of the read set | Solution architect | Resolved (directive) |
| GAP-2537 | The handover of a service's field declaration to the one dictionary has no documented mechanism or operation | Solution architect | Resolved (directive) |
| GAP-2538 | TSD P8 T3.3 declares three many-to-one relationships of proceeds and the target keeps them as values | Solution architect | Resolved (directive) |
| GAP-2539 | DP13 Money and closure is catalogued with the system of record ACE only, while the match on the same row is a Workbench record | Business analyst, P8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2541 | EP01's wave map wave is 1 and rwb-payment's Architecture v5 wave is 2 for the same story | Portfolio lead | Resolved (directive) |
| GAP-3151 | Origin tag where one legacy criterion is carried by several new stories | TechX | Resolved (directive) |
| GAP-3159 | The role table is loaded by P3 in the story and owned by P4 in the Ownership Map | P4 access owner | Resolved (directive) |
| GAP-3160 | The P2 outbound adapter writes a table owned by rwb-debtsale | Integration lead | Resolved (directive) |
| GAP-3162 | The case story writes the P1 extension tables | P3 case owner | Resolved (directive) |
| GAP-3171 | Service P8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3240 | One module per item in version 3 becomes several services per item in the split | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P4-E1001-APP | Not specified without item ID | 326 | The 19 service schemas of the estate are never read by `rwb-access`, and `rwb-access` writes nothing outside `rwb_access`. The database login is the service's o |
| RWB-P4-E1008-APP | new AC without TC row | 463 | AC9 is new and no section 16 row covers it |
| RWB-P4-E1018-APP | skipped AC ID | 116 | missing: AC9, AC10, AC11, AC12, AC13, AC14, AC15 |
