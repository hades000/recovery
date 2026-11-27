# RWB-ITG-W1 Wave 1 integration - review pack, part 1 of 5 (RWB-ITG-E1001-ITG to RWB-ITG-E1015-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 203 |
| Cross-document (pending in another document) | 240 |
| Not applied (value not in the sources) | 4 |
| Open business decisions | 23 |
| Register gaps linked | 200 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E1001-ITG | 26 | 56 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1001 ITG Recovery tables for the 14 data products - integration v2.md |
| RWB-ITG-E1002-ITG | 26 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1002 ITG Case list v1 with case ID, owner and queue - integration v2.md |
| RWB-ITG-E1007-ITG | 38 | 39 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1007 ITG Integration adapters for outbound files - integration v2.md |
| RWB-ITG-E1008-ITG | 20 | 27 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1008 ITG Decision log store v1, append only and hash chained - integration v2.md |
| RWB-ITG-E1011-ITG | 34 | 39 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1011 ITG Reconciliation and data quality report - integration v2.md |
| RWB-ITG-E1013-ITG | 28 | 34 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1013 ITG Baseline measures - integration v2.md |
| RWB-ITG-E1015-ITG | 31 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1015 ITG Freshness stamp per data product - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1008-ITG, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS | R-09175 | GAP-1225 | Register gap | Solution architect with the decision-center product owner | How nineteen local record chains become one central chain is not specified | Fix the rule as: the ledger recomputes entry_hash on the legacy canonical form (BR4) over the stored columns, orders by the ingest commit under the chain lock, and preserves the local chain sequence and hash on the row for reconciliation; then publish it in RWB-P7-E1008-CON. |
| RWB-ITG-E1002-ITG | R-09303 | CG-ALL-138 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1002-ITG | R-09305 | CG-ALL-143 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-ITG-E1007-ITG | R-09312 | CG-ALL-160 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1008-ITG | R-09317 | CG-ALL-175 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21843 | GAP-0001 | Register gap | Product Owner | Arch v5 waves have no release dates | Keep the dates unchanged and tentative, map waves 0-1 to Release 1 at the plan gate, and confirm the mapping in the verification loop |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21856 | GAP-0977 | Register gap | Data steward and data product owner (RW-DATASTEW) | The dictionary rows of the five rwb_access tables have no seeding owner after the split | Declare the 44 business rows as a build artefact of this story, hand the declaration to the one dictionary's seed in rwb_source_data, and let the seed carry the 35 standard-column rows under its own Field IDs. Cite the 44 business Field IDs only. |
| RWB-ITG-E1002-ITG, RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1002-OPS, RWB-P3-E1002-APP | R-21871 | GAP-1502 | Register gap | Product owner | The case list is split between this service and the case service, while the FSD gives screen and rows to one module | This service builds and publishes one row per case account per business date and holds the publication status; rwb-case serves the case list screen and its filters over those rows; the reconciliation and the hold stay here. Agree the split at the Epic 1 story review. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-21888 | GAP-1545 | Register gap | Compliance | The debt buyer tape is required to be masked before the data room, and to carry the personal data the sale terms allow | The tape carries only the fields the sale terms and the approved mask list allow, and the mask list is a reference-data row owned by Compliance under DL26; the PRD states the rule and leaves the field list open. |
| RWB-ITG-E1008-ITG, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS | R-21897 | GAP-0003 | Register gap | RW-RISK and Internal Audit | ADR-009 central log versus local record plus central ledger | Adopt RecordAndApply plus the central ledger and seal the change in ADR-022 after the Audit sign-off |
| RWB-ITG-E1011-ITG, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21922 | GAP-1651 | Register gap | Data steward and data product owner | The reconciliation and the data quality break are P1's, but FSD P9 specifies them as its own features | Read the reconciliation result and the break rows from P1's contract and hold the break view and the closure in P9 |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-28455 | GAP-1548 | Register gap | Compliance | No retention period is set for an outbound item, a delivery record or the transmission evidence of a file | The PRD states the retention of P2 transmission records as open under DL26 with the section R9 placeholder, and requires only that a resend and its audit record outlive the retention period of the case they belong to. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1027-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-28460 | GAP-2067 | Register gap | Document owner of the audit and logging design | The source reads version 1 in its metadata table and v2 in its file name | Take the file name as the family version, so this document becomes version 3, and keep the source values in a 'Source version' row: 1, 28 October 2026. The change log carries both readings. |
| RWB-ITG-E1013-ITG, RWB-ITG-E2009-ITG, RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E2009-APP, RWB-P9-E1013-APP, RWB-P9-E1013-CON, RWB-P9-E1013-OPS, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-P9-E8001-APP, RWB-P9-E8001-CON, RWB-P9-E8002-APP, RWB-P9-E8002-CON, RWB-S8-E2009-APP | R-28480 | GAP-1644 | Register gap | Business lead | The program BRD has no requirement section for P9 reporting | Keep the epic-level keys as the trace target and state the coverage basis in section 11.2 until a P9 requirement section exists |
| RWB-ITG-E1002-ITG | R-33379 | ASM-ALL-143 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E1001-ITG | R-03401 | DOR-RWB-ITG-E1001-ITG-14 | 2 | Definition of Ready item 14 Epic design: Fail | No signed EP01 epic design record found; grep of all .md for EP01 epic design sign-off returned nothing. Needs the sign-off record. |
| RWB-ITG-E1001-ITG | R-03402 | DOR-RWB-ITG-E1001-ITG-16 | 2 | Definition of Ready item 16 Size: Fail | No size for RWB-E1-001 in 04 User stories; the squad sets it at refinement. Recording a size now would invent a value. |
| RWB-ITG-E1001-ITG | R-03404 | DOR-RWB-ITG-E1001-ITG-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | Fakes are named in 12.8. No published fake library version in 05 Technical architecture (grep found none), so the placeholder stays. |
| RWB-ITG-E1013-ITG | R-21932 | GAP-2579 |  | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Benefit-model measure set, monthly day, month key, screen and requirement ID are an open business question (PRD P9 OQ-P9-02; BRD Epics 3 to 8 Q-020). No source gives the values. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00179 | RWB-ITG-E1001-ITG | CG-ALL-118 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} in rwb-source-data.yaml through the provider's CON story. |
| CDC-00236 | RWB-ITG-E1002-ITG | CG-ALL-130 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness (business-date freshness and ACE batch completeness) in rwb-source-data.yaml. |
| CDC-00254 | RWB-ITG-E1007-ITG | CG-ALL-145 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} through the rwb-source-data provider's CON story. |
| CDC-00255 | RWB-ITG-E1007-ITG | CG-ALL-146 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the rwb-source-data provider's CON story. |
| CDC-00256 | RWB-ITG-E1007-ITG | CG-ALL-147 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness through the rwb-source-data provider's CON story. |
| CDC-00293 | RWB-ITG-E1008-ITG | CG-ALL-167 | 12.2 | Publish operation GET /api/recovery/source-data/v1/accounts/{id} in paths through the rwb-source-data CON story |
| CDC-00294 | RWB-ITG-E1008-ITG | CG-ALL-168 | 12.2 | Publish operation GET /api/recovery/source-data/v1/customers/{id} in paths through the rwb-source-data CON story |
| CDC-00319 | RWB-ITG-E1011-ITG | CG-ALL-179 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness in rwb-source-data.yaml through the provider's CON story. |
| CDC-00358 | RWB-ITG-E1013-ITG | CG-ALL-193 | 12.2 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready in rwb-source-data.yaml through the provider CON story, or the story consumes a published operation. |
| CDC-00359 | RWB-ITG-E1013-ITG | CG-ALL-194 | 12.2 | Publish GET /api/recovery/source-data/v1/payments?accountId={accountId} in rwb-source-data.yaml through the provider CON story, or the story consumes a published operation. |
| CDC-00376 | RWB-ITG-E1013-ITG | GAP-0563 | 12.2 | Path and schema fixes belong to the P1 OpenAPI document. The story already calls these paths, so no story edit is needed. |
| CDC-00392 | RWB-ITG-E1015-ITG | CG-ALL-202 | 12.2 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready through the provider's CON story |
| CDC-00395 | RWB-ITG-E1015-ITG | DOR-RWB-ITG-E1015-ITG-8 | Header | Publish the readiness POST path (CG-ALL-202); catalogue JOB-04 in Temporal Catalog v1 (CG-ALL-203) |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00193 | RWB-ITG-E1001-ITG | GAP-0100 | find it | List each operation under its owning service with its Architecture v5 base path; leave final paths and payloads to API Specification v5. |
| CDC-00194 | RWB-ITG-E1001-ITG | GAP-0107 | find it | Derive the 48 cross-owner foreign key cuts from sheet Tables and record them in the FK cuts sheet, README and ERD. |
| CDC-00195 | RWB-ITG-E1001-ITG | GAP-0109 | find it | Emit outbox_event, outbox_delivery, processed_event and idempotency_key in all 19 service files; emit feature_flag and feature_flag_change once in rwb_integration.sql. |
| CDC-00214 | RWB-ITG-E1001-ITG | GAP-0108 | find it | Create rwb_valuation.sql with schema, platform library objects and a note; read ACE through rwb-source-data until a TSD adds a local table. |
| CDC-00219 | RWB-ITG-E1001-ITG | GAP-0202 |  | Assign owner P1 and target schema 'recovery (ACE, read-only view)' to the 30 recovery.v_ace_* views from Architecture v5; add a Views sheet. |
| CDC-00223 | RWB-ITG-E1001-ITG | GAP-0226 |  | Record S5 as owner of the Workbench asset data set; keep ACE collateral and valuation as a P1 read and valuation_ext as P1. |
| CDC-00232 | RWB-ITG-E1001-ITG | GAP-2535 |  | Remove payment_match_rule as a table: match rules are rows of the rwb-decision rule package, and no payment_match_rule table is created in rwb_payment (D-RCV-36 T10). |
| CDC-00287 | RWB-ITG-E1007-ITG | GAP-1538 | find it | Add rows for FileDelivered and FileFailed on rwb.integration.events.v1 with producer rwb-integration, keyed by case ID, owned by P2, with no numbered EV ID. |
| CDC-00306 | RWB-ITG-E1008-ITG | GAP-1224 | 11 | Align E2028 to drop POST /decision-log; no append operation is owned unless the Ownership Map adds one first. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00210 | RWB-ITG-E1001-ITG | CG-ALL-125 | 18 | RTM v7 REQ-RDF-001 lists only TC-E1-001-02, -03 and -07. Section 18 also names the TC-ITG-E1001 cases this story runs, so the RTM must add them. |
| CDC-00252 | RWB-ITG-E1002-ITG | CG-ALL-137 | 18 | Align the test lists of REQ-RDF-007, REQ-RDF-009 and the third differing requirement with RWB-ITG-E1002-ITG §18 in the next RTM version. |
| CDC-00269 | RWB-ITG-E1007-ITG | DOR-RWB-ITG-E1007-ITG-12 | 12, 16, 18 | Align the RWB-ITG-E1007-ITG test case lists with §18 of the story, including TC-ITG-E1007-05 to -09. |
| CDC-00284 | RWB-ITG-E1007-ITG | CG-ALL-159 | 18 | Align the test lists of REQ-DRI-006, REQ-DRI-007 and REQ-DRI-008 between RTM v7 and §18 in their next versions. |
| CDC-00310 | RWB-ITG-E1008-ITG | CG-ALL-174 | 18 | Align REQ-DRI-001 test list with RWB-ITG-E1008-ITG section 18 (TC-E1-008-03-ITG, TC-ITG-E1008-01, TC-ITG-E1008-02) in the next RTM version. |
| CDC-00348 | RWB-ITG-E1011-ITG | CG-ALL-189 | 18 | Align the test lists for REQ-RDF-007 and REQ-RDF-008 with section 18 of RWB-ITG-E1011-ITG in the next version |
| CDC-00382 | RWB-ITG-E1013-ITG | CG-ALL-197 | 18 | Align the REQ-RDF-012 test list in the next RTM version with RWB-ITG-E1013-ITG section 18 (TC-E1-013-01, -02, -05, -06), or the reverse, so both agree. |
| CDC-00403 | RWB-ITG-E1015-ITG | CG-ALL-207 | 18 | Align REQ-RDF-009 test trace with story section 18 range TC-E1-015-01-ITG to TC-E1-015-12-ITG in the next RTM version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00184 | RWB-ITG-E1001-ITG | CG-ALL-113 | 2, 4, 11 | Record v_data_dictionary as the rwb-source-data dictionary read model object in the owning document. |
| CDC-00185 | RWB-ITG-E1001-ITG | CG-ALL-114 | 13 | Record information_schema as the PostgreSQL system catalog object used by the estate and boundary tests. |
| CDC-00186 | RWB-ITG-E1001-ITG | CG-ALL-115 | 13 | Record pg_constraint as the PostgreSQL system catalog object used by the boundary test. |
| CDC-00187 | RWB-ITG-E1001-ITG | CG-ALL-116 | 13 | Record pg_views as the PostgreSQL system catalog object used by the view-definition check. |
| CDC-00241 | RWB-ITG-E1002-ITG | CG-ALL-127 | n/a | Record file_run as the rwb_integration object in the owning document, or use the dictionary name. |
| CDC-00304 | RWB-ITG-E1008-ITG | DOR-RWB-ITG-E1008-ITG-7 | 11 | Add decision_record as a per-service schema entity or map it to the existing decision entity; story keeps the name until then. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00188 | RWB-ITG-E1001-ITG | CG-ALL-123 | 16 | Add rows for TC-E1-001-12-ITG and TC-ITG-E1001-01 to TC-ITG-E1001-04 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-00244 | RWB-ITG-E1002-ITG | CG-ALL-135 | 16 | Add rows TC-ITG-E1002-01 to TC-ITG-E1002-04 with Given, When and Then copied from AC12 to AC15. |
| CDC-00267 | RWB-ITG-E1007-ITG | CG-ALL-157 | 16 | Add rows TC-ITG-E1007-01 to TC-ITG-E1007-09 with Given, When and Then copied from AC12 to AC19 of RWB-ITG-E1007-ITG. |
| CDC-00301 | RWB-ITG-E1008-ITG | CG-ALL-172 | 16 | Add rows TC-ITG-E1008-01 to TC-ITG-E1008-05 with Given, When and Then copied from the criteria they cover. |
| CDC-00326 | RWB-ITG-E1011-ITG | CG-ALL-187 | 16 | Add rows TC-E1-011-08-ITG, TC-E1-011-09-ITG and TC-ITG-E1011-01 to -04 with Given, When and Then copied from the criteria they cover; also add TC-ITG-E1011-05 to -09. |
| CDC-00397 | RWB-ITG-E1015-ITG | CG-ALL-205 | 16 | Add rows TC-E1-015-10-ITG, TC-E1-015-11-ITG, TC-E1-015-12-ITG to the next version, with Given, When and Then copied from AC9, AC10 and AC11 |

### parameter-catalog.csv (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00234 | RWB-ITG-E1002-ITG | CG-ALL-128 | find it | Publish the parameter catalog with key, owner, type, default and the story that reads each key, starting with case.entry.dpd. |
| CDC-00235 | RWB-ITG-E1002-ITG | CG-ALL-129 | find it | Record case.entry.dpd as the single key for this threshold, as this story reads it; align case.entry.dpd_threshold in the Assumptions Register and Test Cases v8 to it. |
| CDC-00238 | RWB-ITG-E1002-ITG | DOR-RWB-ITG-E1002-ITG-20 | find it | Publish the catalog rows and record case.entry.dpd as the one key for the DPD threshold. |
| CDC-00312 | RWB-ITG-E1008-ITG | GAP-1617 | find it | Add three reference-data keys: ledger completeness target 5 minutes; gap alert threshold 5 minutes; strict-mode maximum wait Not specified in the source documents (GAP-1617), pending ADR-022 sign-off. |
| CDC-00315 | RWB-ITG-E1008-ITG | GAP-1233 | find it | Add keys: consumer group rwb-decision-ledger; lag alert at 5 minutes; dead-letter alert at the first dead letter; verification job at 01:00 (one hour before the 02:00 chain check); WORM path Not specified in the source documents (GAP-1233), per environment. |
| CDC-00390 | RWB-ITG-E1013-ITG | GAP-2574 | 14 | Read every threshold, channel and owner from the catalogue row and values files. Name the held publish as the only caller of MSG-GEN-006 in the run book. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00247 | RWB-ITG-E1002-ITG | DOR-RWB-ITG-E1002-ITG-9 | 14 | Confirm the MSG-P1-001 wording in section 14 against standard v4 and align the flagged P3 text to it. |
| CDC-00251 | RWB-ITG-E1002-ITG | CG-ALL-134 | 14 | The standard v4 text is not in the read set, so the story keeps its existing MSG-P1-001 wording; the message text belongs to the standard. |
| CDC-00266 | RWB-ITG-E1007-ITG | CG-ALL-155 | 4, 14 | Add a new message ID for 'A call without a session' with text 'Your session has ended. Sign in again.'; then RWB-ITG-E1007-ITG MSG-P4-001 row cites that ID. |
| CDC-00270 | RWB-ITG-E1007-ITG | DOR-RWB-ITG-E1007-ITG-9 | 14 | MSG-P1-001 and MSG-P2-001 now carry the standard text. The MSG-P4-001 and MSG-P4-003 ID collisions remain and are noted in §14. |
| CDC-00283 | RWB-ITG-E1007-ITG | CG-ALL-156 | 14 | Add a new message ID for 'A resend names an unknown item', English 'This record was not found.'; the story then uses it in place of MSG-P4-003. |
| CDC-00387 | RWB-ITG-E1013-ITG | GAP-0565 | 14 | Set the second sentence of MSG-P1-001 to: Today's ACE batch has not arrived. Align the section 14 copy of this story to the same sentence. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00209 | RWB-ITG-E1001-ITG | GAP-2061 |  | Add a per-service availability table of 19 rows applying the same two targets; state a composed screen as the product of the services it calls, within the one-hop call budget. |
| CDC-00274 | RWB-ITG-E1007-ITG | GAP-0338 | find it | Update the P2 Integration row of the connection matrix (slide 13) with its read path to rwb-source-data and the FileFailed edge into rwb-case, or pass the figures in the manifest. |
| CDC-00314 | RWB-ITG-E1008-ITG | GAP-1230 | find it | Correct the read path to GET /decision-log (and GET /decision-log/{entryId}) in slide 14 and the first API path to /decision-log in slide 41. |
| CDC-00353 | RWB-ITG-E1011-ITG | GAP-0337 | find it | Add the three JOB-04 outbound reads to the rwb-source-data row; publish the case exclusion resource with path, fields and 2 s budget |
| CDC-00368 | RWB-ITG-E1013-ITG | GAP-1499 | 8 | Drop lake copy and INT-19 extract from the P1 features; assign measures and regulatory extract to rwb-reporting; confirm six measure definitions with the data steward before wave 2. |

### 06 Data/Recovery Workbench Source to Target Mapping v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20499 | RWB-ITG-E1007-ITG | R-28449 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |
| CDC-20500 | RWB-ITG-E1001-ITG | R-28423 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |
| CDC-20821 | RWB-ITG-E1001-ITG | R-21849 |  | Not applied: the v5 .xlsx cannot be read in this session (no shell tool; binary Read fails), so entity rows and columns cannot be verified. |
| CDC-20822 | RWB-ITG-E1001-ITG | R-21850 |  | Not applied: the v5 .xlsx cannot be read here, so header N and the Ownership Map values cannot be checked for an exact append. |
| CDC-20823 | RWB-ITG-E1001-ITG | R-28424 |  | Not applied: the current 'Extension fields' rule text in Mapping rules cannot be read here; xlsx_set needs it verbatim. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00204 | RWB-ITG-E1001-ITG | GAP-2401 |  | LDM rule_row entity states 21 fields matching its fields sheet; drop rule_test_case.package_version_id; approval.case_id and approval.delegation_limit_id become values with no foreign key; keep five foreign keys inside rwb_decision. |
| CDC-00246 | RWB-ITG-E1002-ITG | DOR-RWB-ITG-E1002-ITG-7 | 11 | Add file_run as an entity or field, or confirm the LDM entity used by DF-INT-001 to DF-INT-013 in section 11. |
| CDC-00299 | RWB-ITG-E1008-ITG | CG-ALL-165 | find it | Record decision_record as the DP-03 local library table in each wave-1 service schema. |
| CDC-00341 | RWB-ITG-E1011-ITG | GAP-1508 |  | Publish the break list as part of the reconciliation result and its read operation, not in an unowned table; fix the store at the data-model review before system test |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00237 | RWB-ITG-E1002-ITG | DOR-RWB-ITG-E1002-ITG-14 | find it | Record the signed epic design sign-off for service epic RWB-ITG-W1. |
| CDC-00259 | RWB-ITG-E1007-ITG | DOR-RWB-ITG-E1007-ITG-14 | none | Record the signed epic design sign-off in the epic design record and confirm it against this story. |
| CDC-00360 | RWB-ITG-E1013-ITG | DOR-RWB-ITG-E1013-ITG-14 | header | Record the signed epic design for RWB-ITG-W1: who signed it (by role) and the decision ID, so DoR item 14 can pass |
| CDC-00393 | RWB-ITG-E1015-ITG | DOR-RWB-ITG-E1015-ITG-14 | Header | Record the signed epic design sign-off for RWB-ITG-E1015-ITG |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00242 | RWB-ITG-E1002-ITG | CG-ALL-131 | 12.3 | Specify the FileDelivered.v1 payload fields (gap-0127), then align §12.3 to them. |
| CDC-00243 | RWB-ITG-E1002-ITG | CG-ALL-132 | 12.3 | Specify the FileFailed.v1 payload fields (gap-0127), then align §12.3 to them. |
| CDC-00263 | RWB-ITG-E1007-ITG | CG-ALL-150 | 12.3 | Define the payload of rwb.integration.FileDelivered.v1: fileId, interfaceId, businessDate, documentId, sha256, recordCount, requesting service. |
| CDC-00264 | RWB-ITG-E1007-ITG | CG-ALL-151 | 12.3 | Define the payload of rwb.integration.FileFailed.v1: fileId, interfaceId, businessDate, attemptCount, lastError code, caseIds, ownerRole. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00295 | RWB-ITG-E1008-ITG | CG-ALL-170 | 12.5 | Workflows sheet: add ChainCheckWorkflow (task queue rwb-decision, started by JOB-14); name it in the JOB-14 workflow column, now Not specified (GAP-0145; ASM-0226). |
| CDC-00300 | RWB-ITG-E1008-ITG | CG-ALL-171 | 12.5 | Add an Activities row ingestDecisionRecord on task queue rwb-decision, owned by RWB-P7-E1008-APP, per section 12.5. |
| CDC-00325 | RWB-ITG-E1011-ITG | CG-ALL-184 | 12.5 | Add an Activities row for Publish status step on rwb-source-data, or name a catalogued activity in section 12.5. |
| CDC-00364 | RWB-ITG-E1013-ITG | CG-ALL-195 | 12.5 | Add activity snapshot(page) to the Activities sheet, or the story uses a catalogued activity instead. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00323 | RWB-ITG-E1011-ITG | DOR-RWB-ITG-E1011-ITG-21 | header | Contract dependencies row names the provider contracts; no unknown story key |
| CDC-00324 | RWB-ITG-E1011-ITG | DOR-RWB-ITG-E1011-ITG-8 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness on rwb-source-data, GET /api/recovery/case/v1/exclusions on rwb-case, GET /api/recovery/comms/v1/cases/{caseId}/notices on rwb-comms, GET /api/recovery/reporting/v1/reports/{reportId} on rwb-reporting, and the two more paths not named in the item. |
| CDC-00344 | RWB-ITG-E1011-ITG | GAP-2234 | 4 | Publish the four section 12.1 operations with Platform administration R, Reporting R and Platform administration U, the 400, 401, 403, 404, 409, 503 problem set, and Idempotency-Key on rerun. |
| CDC-00354 | RWB-ITG-E1011-ITG | GAP-1172 | find it | Carry comms_quality_run, comms_quality_result, comms_quality_break, REC-09 checks ACK and POD, the Schedule after the POD read, and the two GET operations |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00178 | RWB-ITG-E1001-ITG | CG-ALL-117 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story; the story row is unchanged. |
| CDC-00258 | RWB-ITG-E1007-ITG | CG-ALL-149 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider's CON story. |
| CDC-00292 | RWB-ITG-E1008-ITG | CG-ALL-166 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise in paths through the rwb-access CON story |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00189 | RWB-ITG-E1001-ITG | DOR-RWB-ITG-E1001-ITG-12 | 16, 18 | Test Cases: add TC-E1-001-12-ITG and TC-ITG-E1001-01 to 04. RTM: add TC-ITG-E1001-01, -02, TC-E1-001-12-ITG to REQ-RDF-001; TC-ITG-E1001-01, TC-E1-001-03-ITG to REQ-RDF-014. |
| CDC-00245 | RWB-ITG-E1002-ITG | DOR-RWB-ITG-E1002-ITG-12 | 16 | Align TC-ITG-E1002-01 to -04 to Test Cases v8; align §18 lists to RTM v7; re-point rows for AC2, AC6 to AC9 and AC11 to owning stories. |
| CDC-00303 | RWB-ITG-E1008-ITG | DOR-RWB-ITG-E1008-ITG-12 | 16 | Add TC-ITG-E1008-01 to 05 to Test Cases v8; align section 18 test lists with RTM v7; confirm ownership of listed legacy criteria. |

### 06 Data/Recovery Workbench Physical Schema v7 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00208 | RWB-ITG-E1001-ITG | GAP-0285 |  | Add a cut table from each built schema table to its rwb_* schema, with its baseline migration and data move order; cite it from RWB-PLT-NF06-DB and each per-service DB story. |
| CDC-00215 | RWB-ITG-E1001-ITG | GAP-0112 | find it | Define one V0001 baseline per service schema; the view file follows source V0002 and V0003 sections. |
| CDC-00308 | RWB-ITG-E1008-ITG | GAP-1231 | 11 | Drop fk_decision_log_entry_case_id; record the same ruling for every legacy cross-module key of the decision log in v7. |

### RWB-P2-E1007-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00273 | RWB-ITG-E1007-ITG | GAP-0334 | find it | At the P2 contract review fix the deliverFile manifest schema, the claim-check handoff (document ID, SAS link lifetime, Blob upload path) and both Airflow window calls. Publish them in the activity contract and AsyncAPI before the first SIT run. |
| CDC-00280 | RWB-ITG-E1007-ITG | GAP-2229 | header | Confirm rwb.integration.FileFailed.v1 and FileDelivered.v1 element names, the resume-state carrier and the owner task code and due date rule; story to be renamed if they differ. |
| CDC-00281 | RWB-ITG-E1007-ITG | GAP-1396 | 4 | Fix the Airflow product, tenancy, service principal, timeout and retry values, DailyCaseRun wait mechanism and the three file-window operation paths and payloads at scheduling review; publish before first SIT run. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00302 | RWB-ITG-E1008-ITG | DOR-RWB-ITG-E1008-ITG-1 | 1 | Add role 'tech lead' to Users Roles and Permissions v5, or replace the section 1 role with one already listed there. |
| CDC-00365 | RWB-ITG-E1013-ITG | DOR-RWB-ITG-E1013-ITG-1 | 1 | Register role 'QA integration engineer' with its role code, or name the existing role code that sections 1 and 14 map to. |
| CDC-00398 | RWB-ITG-E1015-ITG | DOR-RWB-ITG-E1015-ITG-1 | 1 | Add a role code and name for 'QA integration engineer in the release squad', or map section 1 to an existing role code. |

### RWB-P9-E1013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00379 | RWB-ITG-E1013-ITG | GAP-2572 | 12.2 | Declare GET /measure-definitions with query onDate and a definition list answer as a target declaration pending P3 confirmation |
| CDC-00380 | RWB-ITG-E1013-ITG | GAP-2568 | 12 | Declare the reference-load element of table measure_definition on the rwb-reporting base; keep list values on the rwb-case reference-data contract |
| CDC-00389 | RWB-ITG-E1013-ITG | GAP-2571 | none | The uuid type for approved_by is declared in the CON. The data steward confirms the stored reference. No story edit. |

### RWB-P1-E1001-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00191 | RWB-ITG-E1001-ITG | GAP-0557 | find it | Adopt the five wave 1 assumptions: keep built baseline; split migration creates P1's 13 tables; schema and login rwb_source_data; extension tables to RWB-P1-E1069-DB; catalog and read model stay in rwb_source_data. |
| CDC-00207 | RWB-ITG-E1001-ITG | GAP-2539 |  | Correct the DP13 catalog row under a new catalog version: one product row with the money facts owned by ACE and the match owned by the Workbench. |

### OTHER:ERD v5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00217 | RWB-ITG-E1001-ITG | GAP-0115 | find it | Draw the 108 v5 references unchanged and state the two metadata keys (sys_fields.object_name, sys_objects.data_product) separately in the reconciliation table. |
| CDC-00218 | RWB-ITG-E1001-ITG | GAP-0116 | find it | Group v5 objects by Ownership Map owner, add a cross-service reference table, and keep the data-product table as section 3. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00257 | RWB-ITG-E1007-ITG | CG-ALL-148 | 12.2 | Publish POST /api/recovery/case/v1/cases/{caseId}/actions through the rwb-case provider's CON story. |
| CDC-00320 | RWB-ITG-E1011-ITG | CG-ALL-180 | 12.2 | Publish GET /api/recovery/case/v1/exclusions?businessDate={businessDate} in rwb-case.yaml through the P3 E1011 contract. |

### RWB-PLT-TE006-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00272 | RWB-ITG-E1007-ITG | GAP-1416 | find it | Fix one library artifact with a major version, the three interfaces and their exceptions, the four-table DDL with processed_event and idempotency_key columns, CloudEvents 1.0 attributes with caseId and ce_type, the inbox dedupe rule, retry ladder 1 min, 10 min, 1 h, dead-letter topic with one alert and replay tool. |
| CDC-00318 | RWB-ITG-E1008-ITG | GAP-1232 | find it | Publish rwb-<short>_app login convention and owner role, keep migration account separate from runtime login, and name the template version of the three library objects. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00290 | RWB-ITG-E1007-ITG | GAP-1547 | find it | State that partner and document channels keep their own contracts and P2 carries no requirement for them. Record the FSD sentence as superseded. |
| CDC-00396 | RWB-ITG-E1015-ITG | GAP-3154 | Header | Name the owner of DP01 to DP14 in the PRD; the stamp stays in P1 rwb-source-data for Epic 1 |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00311 | RWB-ITG-E1008-ITG | GAP-1622 | find it | Add a contract version to the DecisionRecorded event, record it on the decision_log_entry, and have the consumer accept a known set of versions and send an unknown one to the dead-letter topic. |
| CDC-00402 | RWB-ITG-E1015-ITG | GAP-1504 | 7 | Set EV-26 direction to produced by rwb-source-data on rwb.source-data.events.v1, with ACE ingestion outside the 19 services; correct at the next version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00321 | RWB-ITG-E1011-ITG | CG-ALL-181 | 12.2 | Add the GET operation to /api/recovery/comms/v1/cases/{caseId}/notices in rwb-comms.yaml; the path currently has POST only. |
| CDC-20649 | RWB-ITG-E1011-ITG | R-00063 |  | GET response schema for /cases/{caseId}/notices not specified in the source documents (CG-ALL-181). |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00327 | RWB-ITG-E1011-ITG | DOR-RWB-ITG-E1011-ITG-12 | 12, 16, 18 | Align section 18 test lists with RTM v7 for REQ-RDF-007, REQ-RDF-008 and REQ-CWC-004; add the section 12 contract test rows to Test Cases v8. |
| CDC-00399 | RWB-ITG-E1015-ITG | DOR-RWB-ITG-E1015-ITG-12 | 16, 18 | Add TC-E1-015-10-ITG, -11-ITG and -12-ITG to Test Cases v8; align RTM v7 test lists to section 18 of this story. |

### OTHER:v3 reconciliation register (Reconciliations sheet) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00349 | RWB-ITG-E1011-ITG | GAP-0271 | find it | Add a Per-service reconciliation sheet with one row per service (19): tables, check part, key, tolerance, cadence, break and result route, pattern, basis; R9 placeholder where unstated |
| CDC-00350 | RWB-ITG-E1011-ITG | GAP-0272 | find it | Add rows for P2, P4, P5, P10, S1, S3, S4, S6, S8, S9 with the tolerance cell carrying the Template and Rules R9 placeholder |

### OTHER:06 Data/Recovery Workbench Reporting and Analytics Data Model v3.xlsx (next version; OTHER:check v4) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00370 | RWB-ITG-E1013-ITG | GAP-0255 |  | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate; state that queue measures stay with P3 rwb_case. |
| CDC-00371 | RWB-ITG-E1013-ITG | GAP-0257 |  | dim_org and facts: key owner and team by ID from events; resolve display name from P3 queue_member and assignment behind the rwb-access masking policy; no personal data on events. |

### RWB-P9-E1013-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00373 | RWB-ITG-E1013-ITG | GAP-2567 | 12.2 | Keep plan metadata rows; declare the payments and freshness reads and two rwb-case rows as consumed in 12.2 with fakes; add the two rwb-source-data rows to the wave dependency map. |
| CDC-00391 | RWB-ITG-E1013-ITG | GAP-2575 | 13 | Carry measure_definition, measure_snapshot, measure_publish and the frozen-row trigger in V1013__measures.sql. The deployment story replays the same sequence. |

### 06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20525 | RWB-ITG-E1001-ITG | R-21851 |  | Ownership row 4 has columns L-N and Ownership split row 4 has G-I for D-RCV-60 owning service, schema and basis, per the v4 structure listing. Owner-per-product not verified. |
| CDC-20526 | RWB-ITG-E1001-ITG | R-21852 |  | Ownership row DP04 could not be read: no shell tool and Read cannot parse .xlsx. Exact current cells unknown, so no xlsx_set was written. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00180 | RWB-ITG-E1001-ITG | CG-ALL-119 | 12.2 | Publish GET /api/recovery/payment/v1/cases/{caseId}/payments in rwb-payment.yaml through the provider's CON story. |

### RWB-ITG-E1001-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00181 | RWB-ITG-E1001-ITG | DOR-RWB-ITG-E1001-ITG-21 | header | Contract dependencies cell marked Not specified (DOR-RWB-ITG-E1001-ITG-21) |

### OTHER:rwb-access, rwb-source-data and rwb-payment API yaml files; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00182 | RWB-ITG-E1001-ITG | DOR-RWB-ITG-E1001-ITG-8 | 4 | Publish POST /api/recovery/access/v1/authorise (rwb-access), GET /api/recovery/source-data/v1/accounts/{id} (rwb-source-data) and GET /api/recovery/payment/v1/cases/{caseId}/payments (rwb-payment). Confirm the event type name in Kafka Catalog v1 against rwb.decision.DecisionRecorded.v1. |

### OTHER:ACE database wave-0 setup (owner: ACE team and DBA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00183 | RWB-ITG-E1001-ITG | GAP-0012 |  | Create the 19 schemas and logins in wave 0 and set the PgBouncer pool and connection cap per login with the ACE DBA. |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00190 | RWB-ITG-E1001-ITG | GAP-0566 | find it | Publish the three read operations with response fields and problem body in RWB-P1-E1069-CON; record the application, database and wave 1 integration slice split in the Service Contract Catalog. Story side done in section 2. |

### RWB-P4-E1001-APP; RWB-P4-E1037-APP; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00192 | RWB-ITG-E1001-ITG | GAP-0975 | find it | Confirm RWB-P4-E1001-APP owns DDL of the five rwb_access tables; read sibling 'rwb_access baseline' references as the version applied; RWB-P4-E1037-CON keeps only the contract stub. |

### OTHER:Conceptual Data Model v6 (sheet Relationships); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00196 | RWB-ITG-E1001-ITG | GAP-0206 | 8 | Show per row: 48 cross-owner keys cut to business-key columns, 11 ACE view references kept, and the third case; fill the empty FK cuts sheet. |

### OTHER:Source to Target Mapping v4 (sheet Mapping), next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00197 | RWB-ITG-E1001-ITG | GAP-0210 | 11 | Keep the 11 ACE entity names; give their fields target schema rwb_source_data, owner P1, read via the rwb-source-data contract; add the four extension tables as Workbench targets. |

### OTHER:Source to Target Mapping v4 (sheets Mapping and ACE gaps), next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00198 | RWB-ITG-E1001-ITG | GAP-0211 | 11 | Add 'Target schema' and 'Owning service', one value per row from Ownership Map sheet Tables; keep columns A to N unchanged. |

### OTHER:Data Ownership and Stewardship v3 (sheets Ownership and Ownership split), next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00199 | RWB-ITG-E1001-ITG | GAP-0224 | 11 | Add 'Owning service (D-RCV-60)', 'Owning schema (D-RCV-60)', 'Basis (D-RCV-60)' at the end; one owner per data product from the Ownership Map; keep A to K unchanged. |

### OTHER:Data Ownership and Stewardship v3 (row DP04), next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00200 | RWB-ITG-E1001-ITG | GAP-0225 | 11 | Keep DP04 whole; record S2 as owner of the live record and name S3 and P1 in the basis cell. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:S1 rwb-valuation DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00201 | RWB-ITG-E1001-ITG | GAP-0228 | 11 | Record S1 as DP11 route economics owner; S1 DB story creates the rwb_valuation tables (valuation, route decision, route agent output); add the map rows. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:TSD P7 v2 T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00202 | RWB-ITG-E1001-ITG | GAP-1280 | 11 | Set rule_row to 21 fields; remove or define rule_test_case.package_version_id; remove the foreign keys on approval.case_id and approval.delegation_limit_id. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00203 | RWB-ITG-E1001-ITG | GAP-2123 |  | Assign the rwb_valuation tables (valuations, D6 route decision, route agent output) to S1 rwb-valuation in the Tables sheet and add them to the Physical Schema folder. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00205 | RWB-ITG-E1001-ITG | GAP-2537 |  | Record the hand-off of the service's 9 field rows as a build artefact to the one dictionary seed; add the handover to TSD P8 T3.1; prove the match by the conformance test. |

### OTHER:TSD P8 T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00206 | RWB-ITG-E1001-ITG | GAP-2538 |  | Proceeds relationships to recovery_case, treatment and account_payment become uuid values case_id, treatment_id and account_payment_id with no foreign key. |

### OTHER:Security and Access Design v4 (v5 realignment table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00211 | RWB-ITG-E1001-ITG | GAP-2035 | find it | Write section 7 per service: one login rwb_<short> per service, grants on own schema only, rwb_source_data sole holder of the v_ace_* view grant, recovery_svc row replaced by service login isolation. |

### OTHER:FSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00212 | RWB-ITG-E1001-ITG | GAP-0980 | find it | Reconcile to TSD P4 v3 T3.1: keep role.entra_group (DF-REF-039) nullable and empty; read the Entra mapping at run time via rwb-source-data from v_ace_iam_group, no copy. |

### OTHER:TSD P4 v3 T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00213 | RWB-ITG-E1001-ITG | GAP-0979 | find it | Add constraint names per platform convention, PK on id, unique role_code, single FK permission.role_id, and one index per read path with section 13 leading columns. |

### OTHER:rwb_source_data.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00216 | RWB-ITG-E1001-ITG | GAP-0114 | find it | Keep lake_copy_watermark DDL in rwb_source_data.sql with a retirement note so no source object is lost; P1 DB story drops it. |

### OTHER:Mapping v4 ('By source' sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00220 | RWB-ITG-E1001-ITG | GAP-0212 |  | In the Aric via COLLINS extension cell, read rwb_source_data.party_ext instead of 'recovery'; keep the 1/0/0/1 counts and Total unchanged. |

### OTHER:Mapping v4 (Mapping rules, 'Extension fields') (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00221 | RWB-ITG-E1001-ITG | GAP-0215 |  | Name contact_point_ext, account_ext and valuation_ext under 'Extension fields'; leave the 133 field rows unchanged until LDM v10. |

### OTHER:Mapping v4 (column B, data product) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00222 | RWB-ITG-E1001-ITG | GAP-0216 |  | Leave the 81 blank data-product cells empty in v5; assign them at the next LDM revision. |

### OTHER:v3 (DP07 system of record cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00224 | RWB-ITG-E1001-ITG | GAP-0227 |  | Record S4 as owner of the legal data set; keep ACE court records as a P1 read and notice and proof of delivery as P6. |

### OTHER:v3 (DP13 system of record cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00225 | RWB-ITG-E1001-ITG | GAP-0229 |  | Record P8 as owner of the proceeds and matching data set; keep write_off as S7 and ACE payment and GL records as a P1 read. |

### OTHER:v4 (DP05 ownership basis) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00226 | RWB-ITG-E1001-ITG | GAP-0230 |  | Record P1 as owner of the interaction ledger; keep notice content and delivery as P6 and the case timeline as a P3 read through the P1 contract. |

### OTHER:v4 (DP14 ownership basis) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00227 | RWB-ITG-E1001-ITG | GAP-0231 |  | Record P3 as owner of parameters and reference data; keep roles and DoA as P4 and templates and merge fields as P6. |

### OTHER:Ownership split v3 (basis cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00228 | RWB-ITG-E1001-ITG | GAP-0232 |  | Keep the count of 88 and append the reconciliation: 93 map rows, 4 extension tables, 1 legacy table with no target, 88 Tier 4 tables over 19 owners. |

### OTHER:Recovery Workbench Roles; OTHER:Change process and Quality measures (v4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00229 | RWB-ITG-E1001-ITG | GAP-0233 |  | Add a service data steward role row, an owner-service change-process step and a schema isolation quality measure; keep the v3 rows unchanged. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:DP08; OTHER:DP09; OTHER:DP10; OTHER:DP12; OTHER:DP14 and split rows 7; OTHER:8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00230 | RWB-ITG-E1001-ITG | GAP-0234 |  | Read Application owner (DL02) as the owning service in the appended column; set the two Workbench access cells to the owning service and its rwb_<name> schema; replace DL02 wording at next revision. |

### OTHER:TSD P8 T3.0 and T3.1 (DDL of proceeds) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00231 | RWB-ITG-E1001-ITG | GAP-2534 |  | Name the primary key, the two indexes and the Field IDs of the 7 standard columns at merge under the platform naming convention; the seed carries the standard-column Field IDs. |

### OTHER:TSD P8 index design (T-A.2 and T3) and FSD P8 screen stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00233 | RWB-ITG-E1001-ITG | GAP-2536 |  | Index the unmatched list on matched_to and received_date and the case read on case_id and received_date; leave screen field lists to the screen stories. |

### OTHER:rwb-source-data API yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00239 | RWB-ITG-E1002-ITG | DOR-RWB-ITG-E1002-ITG-8 | 12 | Publish GET /api/recovery/source-data/v1/freshness; register ReconciliationWorkflow (JOB-04) with its case list step. |

### OTHER:Functional Specification P3, section A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00240 | RWB-ITG-E1002-ITG | GAP-1549 | n/a | Restate the A1.5 read path as a read through the rwb-source-data contract; keep business-key link rules unchanged. |

### OTHER:frontend-context.md v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00248 | RWB-ITG-E1002-ITG | GAP-0017 | 13 | Record the screen-to-service map derived from the gateway-bff composite routes, with the 53 screens and design tokens. |

### RWB-P1-E1002-CON; RWB-P1-E1002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00249 | RWB-ITG-E1002-ITG | GAP-0486 |  | Define GET /case-list/dates/{businessDate}, GET /case-list/rows and the snapshot(page) input and output shapes as in the proposed fix. |

### OTHER:TSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00250 | RWB-ITG-E1002-ITG | GAP-1991 |  | Keep lake_copy_watermark as the watermark of the last published reporting projection and drop the lake extract INT-19 and INT-20 (DP-17). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00253 | RWB-ITG-E1007-ITG | CG-ALL-144 | 12.2 | Publish POST /api/recovery/document/v1/documents through the rwb-document provider's CON story. |

### OTHER:rwb-document and rwb-source-data API contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00260 | RWB-ITG-E1007-ITG | DOR-RWB-ITG-E1007-ITG-8 | 12.2 | Publish POST /api/recovery/document/v1/documents in rwb-document; publish GET /api/recovery/source-data/v1/customers/{id}, GET accounts/{id} and GET freshness in rwb-source-data; plus 5 more paths listed by detcheck. |

### OTHER:FSD P2 v3; OTHER:BRD Program v4 section 5.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00261 | RWB-ITG-E1007-ITG | GAP-1534 | 4 | Remove INT-19 and INT-20 lake outbound adapters; INT-19 becomes a rwb-reporting delivery request via the rwb-integration contract; INT-20 becomes continuous ingest in rwb-decision; correct BRD section 5.2. |

### OTHER:FSD P2 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00262 | RWB-ITG-E1007-ITG | GAP-1539 | 4 | Build INT-25 tape rows and account keys from the delivery request manifest raised by rwb-debtsale; read account facts via rwb-source-data contract; P2 reads neither debt_sale_account nor v_ace_account. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00265 | RWB-ITG-E1007-ITG | CG-ALL-152 | 12.5 | Add activity deliverFile(manifest), task queue rwb-integration, provided by P2. |

### OTHER:Recovery Workbench screen specification (P3 SCR-09; OTHER:SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00268 | RWB-ITG-E1007-ITG | DOR-RWB-ITG-E1007-ITG-10 | 7 | Add empty, loading, error and no-access states for SCR-09 and SCR-44. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00271 | RWB-ITG-E1007-ITG | GAP-0673 | find it | Mark the FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 INT-03 lines superseded for legacy key RWB-E4-046, with date and decision. Agree ALS interface id, transport, layout, result codes, attempts and intervals with the interface owner and load one versioned interface_config row per environment. |

### OTHER:Technical Solution Design P2 Integration v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00275 | RWB-ITG-E1007-ITG | GAP-0647 | find it | Supersede T1.1, T5.2 and T6.2 direct-view wording per Architecture v5 slide 9 and ADR-010. Build rwb-integration on /api/recovery/integration/v1 with own tables; read ACE facts via rwb-source-data (one hop, 2 s); take INT-25 tape rows from the deliverFile manifest; retire lake statements of INT-19, INT-20, JOB-13, JOB-15. |

### RWB-P2-E1007-CON; OTHER:rwb-comms contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00276 | RWB-ITG-E1007-ITG | GAP-0648 | find it | Fix the deliverFile manifest fields and return element and its three typed failures, re-confirmed with rwb-comms, rwb-payment, rwb-debtsale and rwb-reporting. Fix the notice-fact read in the rwb-comms contract. Publish one RFC 9457 problem body with the six TSD status codes. Fix the OpenAPI JSON names and the registry subject and compatibility level with the platform event owner. |

### OTHER:Operations story of rwb-integration (name not in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00277 | RWB-ITG-E1007-ITG | GAP-0650 | find it | Set chart values, replica counts, KEDA backlog threshold, lag and alert thresholds and build ID format as environment values. Confirm both windows with the bank Airflow owner as calls to the requesting services. Name the trigger contract and alert message IDs with the Airflow and observability owners. Keep the R9 placeholder until then. |

### RWB-P2-E1007-CON; OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00278 | RWB-ITG-E1007-ITG | GAP-0739 | find it | Read the two outcomes and the admin item from RWB-P2-E1007-CON. Read the route state to resume from the latest decision-record entry of the case and interface. Hold the task code and due date as rwb-case reference rows. Keep the legacy in-process interfaces internal to the listener. Drop the two lake extracts under DP-17; reporting reads rwb.case.events.v1 in rwb-reporting. |

### OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00279 | RWB-ITG-E1007-ITG | GAP-1162 | find it | Add one read returning the postal addressee only, by party_id, with a 2 s budget and a fake. Add that contract to this story's contract list in section 12. Keep the value out of rwb_comms, the event and every log. |

### RWB-P5-E1007-APP; RWB-P2-E1007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00282 | RWB-ITG-E1007-ITG | GAP-1027 | 4 | Take the deliverFile manifest and claim-check field names from RWB-P2-E1007-CON; read the outbound type code and retention class from document_type in force; carry the 85 case IDs in the manifest. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00285 | RWB-ITG-E1007-ITG | GAP-0981 | 4 | Register the access-review interface row (ID, OUTBOUND, file pattern, data product, owner and alert role); publish the extract layout and recipient; state the review-cycle date convention. |

### OTHER:Recovery Workbench mapping workbook (v4 Mapping column M) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00286 | RWB-ITG-E1007-ITG | GAP-0213 | find it | Keep the Interface cell text word for word in v5. Confirm the v4 interface numbers at the next interface review. |

### OTHER:FSD P2 v3 (A1.6 exclusion table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00288 | RWB-ITG-E1007-ITG | GAP-1542 | find it | List FEAT-DRI-09, FEAT-RDF-21 inbound half, FEAT-DRI-10, FileLoadAdapter, DQ-057, DQ-059, JOB-09, interface_run and interface_signoff in an exclusion table with later home ACE ingestion. Give them no FR, NFR or AC. |

### OTHER:FSD P2 v3 (A1.5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00289 | RWB-ITG-E1007-ITG | GAP-1546 | find it | State INT-17, INT-18 and INT-22 as reused ACE capabilities with no P2 build and no FR. Record that their behaviour is ACE's. |

### OTHER:Story dependencies v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00291 | RWB-ITG-E1007-ITG | GAP-3233 | find it | Keep the five version 4 dependency rows visible as Not carried in the trace. Add an X row later only if the run books or harness wait for the named story. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB-ITG-W1 Epic Overview v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00296 | RWB-ITG-E1008-ITG | DOR-RWB-ITG-E1008-ITG-14 | header | Record the epic design sign-off for RWB-ITG-W1 (approver role and date) in the Epic Overview copy |

### RWB-ITG-E1008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00297 | RWB-ITG-E1008-ITG | DOR-RWB-ITG-E1008-ITG-21 | header | Create the contract story that publishes CG-ALL-166 to CG-ALL-168, then add it to Contract dependencies |

### OTHER:rwb-access and rwb-source-data API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00298 | RWB-ITG-E1008-ITG | DOR-RWB-ITG-E1008-ITG-8 | find it | Publish POST /api/recovery/access/v1/authorise in rwb-access; publish GET /api/recovery/source-data/v1/accounts/{id} and customers/{id} in rwb-source-data. |

### OTHER:AsyncAPI contract of rwb.decision-record.v1 (shared-topic contract review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00305 | RWB-ITG-E1008-ITG | GAP-0332 | 11 | Publish the AsyncAPI document with the DecisionRecorded payload and the ingest rule before the first SIT run. |

### OTHER:FSD P7 v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00307 | RWB-ITG-E1008-ITG | GAP-1226 |  | Withdraw FEAT-DRI-06 and AC-P7-006-01; keep JOB-13 as continuous ingest and JOB-14 as 02:00 chain check; record RWB-E1-014 retirement. |

### OTHER:Deployment story of rwb_decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00309 | RWB-ITG-E1008-ITG | GAP-1234 |  | Set RPO zero for committed entries via ACE PITR plus seal files; RTO Not specified in the source documents (GAP-1234) pending service owner; make chain re-verification and append-only check mandatory restore gates. |

### OTHER:Functional Specification and the rwb-decision service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00313 | RWB-ITG-E1008-ITG | GAP-2075 | find it | State that audit search reads the ledger only and shows an entry as not yet sealed until JOB-13 has collected it; the local record is reached through the owning service's contract; strict mode waits for the ledger acknowledgement of its own record. |

### RWB-P7-E2005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00316 | RWB-ITG-E1008-ITG | GAP-1229 | find it | Confirm page 1, size 50 and maximum 200 with an RFC 9457 body (type, title, status, detail, message identifier) and carry the values when filters are added. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00317 | RWB-ITG-E1008-ITG | GAP-0984 | find it | Publish the decision_record column set, physical types and canonical-form rule; add DECISION_LOG to the TSD P4 RBAC matrix; fix per-service login names; state local verifier behaviour in Temporal and Drools design. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00322 | RWB-ITG-E1011-ITG | CG-ALL-182 | 12.2 | Publish GET /api/recovery/reporting/v1/reports/{reportId} in rwb-reporting.yaml through the provider's CON story. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00328 | RWB-ITG-E1011-ITG | GAP-0268 | find it | Add an owner from the Ownership Map to every reconciliation row; the owning service answers its Workbench side on its contract, one hop, 2 s timeout; rwb-source-data keeps the ACE side and the JOB-04 run. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations and Quality measures sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00329 | RWB-ITG-E1011-ITG | GAP-0269 | find it | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures, values from the Ownership Map sheet Tables. |

### OTHER:Recovery Workbench Functional Specification P1 v3 (A2.12; OTHER:A2.19; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00330 | RWB-ITG-E1011-ITG | GAP-1499 | find it | Remove the data lake and the INT-19 extract from A2.12, A2.19 and A2.20; publish measures and regulatory extracts from rwb-reporting; confirm output channel and six measure definitions with the data steward before wave 2. |

### OTHER:Business Requirements Document section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00331 | RWB-ITG-E1011-ITG | GAP-1456 | find it | State that Epic 1 stories keep their earlier wave per Template and Rules R5.6 while rwb-payment, rwb-asset and rwb-deviation start in wave 2 for their own epics. |

### OTHER:RWB-E1-055 story (section 4 step 11, section 8 BR5) and the reconciliation register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00332 | RWB-ITG-E1011-ITG | GAP-1169 | find it | Keep REC-05 for the business-key orphan check; give the notice barcode break its own code in both stories; correct one code so it has one meaning. |

### RWB-P6-E1011-APP; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00333 | RWB-ITG-E1011-ITG | GAP-1168 | find it | Add RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-source-data contract to the C list; name the reference-data read operation in RWB-P3-E1043-CON. |

### OTHER:Reconciliations workbook v3 (Reconciliations sheet; OTHER:REC-08 row B12:C12) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00334 | RWB-ITG-E1011-ITG | GAP-0270 |  | Compare the local decision record of each of the 19 services on rwb.decision-record.v1 with the central decision_log_entry of P7, on count and last hash, nightly, with the 02:00 hash-chain check (JOB-14) |

### OTHER:Reconciliations workbook v3 (Reconciliations sheet A9:G9 and A13:G13) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00335 | RWB-ITG-E1011-ITG | GAP-0273 |  | Add a REC numbering block mapping the notice-barcode check (A9) and business-key orphan check (A13) to the numbers RWB-E1-011 gives them; keep source IDs unchanged |

### OTHER:TSD P1 v3 and FSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00336 | RWB-ITG-E1011-ITG | GAP-0496 |  | Keep REC-01, REC-02 and REC-05 over P1 tables in RWB-P1-E1011-APP with no REC-03 or REC-04 row; move REC-03 to P3 and S5 slices, REC-04 to the P6 payment slice, and other services' REC-05 keys to their slices |

### RWB-P1-E1011-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00337 | RWB-ITG-E1011-ITG | GAP-0497 |  | Add GET /admin/reconciliation/results/{resultId}, the result and break-row element lists, ReconciliationWorkflow (recon-{businessDate}), activity reconciliation on rwb-source-data, and the ReconciliationQuery interface |

### RWB-P3-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00338 | RWB-ITG-E1011-ITG | GAP-0740 |  | Confirm check codes and state names; publish the four operation paths; decide account_id against account_key; align TSD P3 with FSD P3 v4; set Schedule cron; add the Platform administration right the proposed fix names |

### RWB-P6-E1011-APP; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00339 | RWB-ITG-E1011-ITG | GAP-1170 |  | Drop the two extracts and the INT-19 path from the P6 key; serve quality facts from GET /api/recovery/comms/v1/quality-results; agree with rwb-reporting how its report reads them |

### RWB-P6-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00340 | RWB-ITG-E1011-ITG | GAP-1171 |  | Serve quality facts from the service read model for wave 1 with no DP-09 event or push; settle in wave 2 whether rwb-reporting reads them or a quality event is added with DP-09 |

### RWB-P1-E1011-APP; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00342 | RWB-ITG-E1011-ITG | GAP-2232 | 4 | Record the rwb-case slice boundary: case-side facts of REC-01, REC-03 and REC-05 over rwb_case tables; no reconciliation_result row; no legacy acceptance criterion owned; platform CONs of the DP table not build dependencies of the APP story. |

### RWB-P1-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00343 | RWB-ITG-E1011-ITG | GAP-2233 | 4 | Add case_quality_run, case_quality_result and case_quality_break in schema rwb_case with reconciliation_result columns, unique on rec_code, quality_check, business_date and product_group; publish check names EXCL, PLAN and KEY. |

### OTHER:rwb-source-data service contract (/api/recovery/source-data/v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00345 | RWB-ITG-E1011-ITG | GAP-2235 | 4 | Publish a freshness read and one product-coded records read per data product, with business date, paging and element names; read the plan side of REC-03 by plan_ref. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00346 | RWB-ITG-E1011-ITG | GAP-1946 | 4 | Keep H and C at None; record the nine CONs as wave-0 prerequisites; read the ACE side via the DP06 contract; serve quality facts from GET /api/recovery/asset/v1/quality-results and quality-runs/{businessDate}; drop the extracts and INT-19 path as the fix states. |

### RWB-P6-E1011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00347 | RWB-ITG-E1011-ITG | GAP-1167 | 4 | Keep H at None; record the seven platform CONs as wave-0 build prerequisites in the dependency map, not as lane dependencies; L-P6-C depth unchanged. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:S1 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00351 | RWB-ITG-E1011-ITG | GAP-0274 | find it | Keep rwb-valuation as owner, state the capability from Architecture v5, carry the R9 placeholder until a table is listed |

### OTHER:v3 reconciliation register (Quality measures sheet; OTHER:B7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00352 | RWB-ITG-E1011-ITG | GAP-0276 | find it | Reword Timeliness: rwb-source-data reads the ACE batch and publishes AceDataReady; other services measure the freshness contract; owner rwb-source-data (P1) |

### OTHER:TSD P6 Communications v2 (rwb-comms RBAC matrix) and gateway-bff route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00355 | RWB-ITG-E1011-ITG | GAP-1173 | 7 | Add Platform administration area with right R for the two quality reads; keep Litigation R with scope for the case notice read as TSD P6 T-A API-P6-002 declares; add to Ownership Map at next version. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00356 | RWB-ITG-E1011-ITG | GAP-3172 | header | State wave 1 delivery of rwb-asset in the service epic and wave plan, raise the R5.6 conflict row per service and business epic, and let the rwb-asset service wave govern its later stories. |

### OTHER:BRD v4 section 3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00357 | RWB-ITG-E1011-ITG | GAP-1457 | 3 | In a later BRD version, renumber the section 3 headings by service epic while keeping every requirement key unchanged. |

### OTHER:Contract stories of the P1; OTHER:P3 and P9 services of RWB-E1-013 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00361 | RWB-ITG-E1013-ITG | DOR-RWB-ITG-E1013-ITG-21 | header | Contract dependencies reads Not specified in the source documents (DOR-RWB-ITG-E1013-ITG-21) |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00362 | RWB-ITG-E1013-ITG | DOR-RWB-ITG-E1013-ITG-8 | header | Publish the two rwb-source-data operations (CG-ALL-193, CG-ALL-194) and add activity snapshot(page) to Temporal Catalog v1 Activities (CG-ALL-195). |

### OTHER:FSD P9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00363 | RWB-ITG-E1013-ITG | GAP-1646 | 12.8 | Read the Power BI and data lake destinations in A2.1, A2.3, A2.4, A2.5, A2.7, A2.8 and AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01, AC-ALT-P9-004-01 as the reporting read model on the gateway-bff route, and lake delivery as a file delivered by rwb-integration. |

### OTHER:Screen specification for SCR-37 and SCR-44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00366 | RWB-ITG-E1013-ITG | DOR-RWB-ITG-E1013-ITG-10 | 10 | Add empty, loading, error and no access states for SCR-37 and SCR-44; this story owns no screen. |

### RWB-P3-E1013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00367 | RWB-ITG-E1013-ITG | DOR-RWB-ITG-E1013-ITG-7 | 11 | Replace legacy job and decision-log wording in its criteria with the v5 rwb-reporting and ReportPublished terms. |

### OTHER:Data model v3 (Facts sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00369 | RWB-ITG-E1013-ITG | GAP-0251 |  | Star schema stays as a read model in rwb_reporting served through gateway-bff; no lake is rebuilt. |

### OTHER:Recovery Workbench FSD P9 Reporting v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00372 | RWB-ITG-E1013-ITG | GAP-1649 |  | A2.1, A2.3, A2.8: publish the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE; carry the count of 7 as an open question. |

### RWB-P3-E1043-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00374 | RWB-ITG-E1013-ITG | GAP-2241 | 13 | Name the age-band list in the reference-data catalog with list code and table code; use that code in the age-band read and on the band list screen. |

### OTHER:Reporting workbook v3 (Facts F5-F13; OTHER:Dimensions B5/B6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00375 | RWB-ITG-E1013-ITG | GAP-0252 | 7 | Every ACE-fed fact and dimension takes rows from the rwb-source-data contract and snapshot(page); no recovery.v_ace_* grant for the read model; rwb-reporting never reads ACE views. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00377 | RWB-ITG-E1013-ITG | GAP-2239 | 12.2 | Add GET /api/recovery/case/v1/cases/facts with businessDate, page and size and the legacy facts fields, marked provisional |

### RWB-P9-E1013-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00378 | RWB-ITG-E1013-ITG | GAP-2240 | 12.2 | Publish the measure-catalog read as a GET on the rwb-reporting base with an onDate parameter and name it in the catalog |

### RWB-PLT-E1071-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00381 | RWB-ITG-E1013-ITG | GAP-0561 | 12.6 | Register the 05:30 Schedule, the rwb-source-data worker, task queue and topic with retry and .dlt topics as external or operations dependency |

### OTHER:project-context.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00383 | RWB-ITG-E1013-ITG | GAP-0016 | none | Retire the v2 Case volume and Staff rows and use the Architecture v5 Volume and Scale Forecast v3 figures. |

### OTHER:Version 3 of the facts, dimensions and measures register (name not given in the item) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00384 | RWB-ITG-E1013-ITG | GAP-0254 | none | Add Owner and Values from columns to Facts and Dimensions and an Owner column to Measures, with values from the Ownership Map (P9, rwb-reporting, schema rwb_reporting). |

### OTHER:FSD P1 and TSD P1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00385 | RWB-ITG-E1013-ITG | GAP-0559 | none | Mark the lake steps, the INT-19 row and lake_copy_watermark removed in the next versions; keep the case list and reconciliation publish status. |

### OTHER:TSD P1 list of values (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00386 | RWB-ITG-E1013-ITG | GAP-0564 | none | Add the gate pair COMPLETE and HOLD beside LOADED and STALE in the next P1 TSD version. |

### OTHER:rwb-case message catalogue and SCR-44 screen specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00388 | RWB-ITG-E1013-ITG | GAP-2242 | 14, 15 | Add one message for a held facts release to the rwb-case catalogue. Name the release-state columns and the two counts of SCR-44. |

### OTHER:rwb-source-data CON story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00394 | RWB-ITG-E1015-ITG | DOR-RWB-ITG-E1015-ITG-21 | Header | Create contract story RWB-ITG-E1015-CON and list it as the contract dependency |

### OTHER:RWB-E1-034 (legacy story) and the P6 rwb-comms contract in the API registry (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00400 | RWB-ITG-E1015-ITG | GAP-0357 | none | Read the five template operations from the P6 registry contract under /api/recovery/comms/v1/admin/templates, keep request, response, state and message unchanged, and route SCR-33 via gateway-bff. |

### OTHER:TSD P1 v3 T3.6 (rows DF-OPS-005 and DF-OPS-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00401 | RWB-ITG-E1015-ITG | GAP-0492 | 7 | Map source_extracted_at to started_at and loaded_at to completed_at as in FSD P1 v3 A2.14.2, and correct both rows in the next version. |

### OTHER:Data product catalog (data_product.expected_by values) and the Temporal Schedule register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00404 | RWB-ITG-E1015-ITG | GAP-0494 | find it | Add expected_by values for the remaining source-fed products once the data steward confirms them; register one Schedule per product named from the product code. |

### OTHER:Legacy dependency trace sheet and Story dependencies v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00405 | RWB-ITG-E1015-ITG | GAP-3233 | find it | Keep the five rows as Not carried; add an X row only if the run books or the harness really waits for the named story. |

### 06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20618 | RWB-ITG-E1001-ITG | R-21848 |  | Per-row cut values for v7 Relationships not readable: no docview access, and no v7 text extract. Fill-the-sheet part belongs in Ownership Map v1, not this document. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20809 | RWB-ITG-E1001-ITG | R-28438 |  | Primary key, index names and Field IDs need values not in the sources. Placeholder added after T3.0 (GAP-2534). |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20816 | RWB-ITG-E1007-ITG | R-28453 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09174', 'R-21873', 'R-28451', 'R-28452', 'R-28453'] |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20839 | RWB-ITG-E1008-ITG | R-21898 |  | AsyncAPI document with the DecisionRecorded message already exists (lines 45-57). Payload stays Not specified (GAP-0096; ASM-0160). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0012 | 19 schemas, logins and the connection budget are not created | ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0016 | Volumes differ between the v2 context and v5 | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0017 | No v5 screen inventory or screen-to-service map | Solution architect and UX lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0062 | Wave conflict P8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0063 | Wave conflict S5 / EP01 | Tech lead | Resolved (directive) |
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
| GAP-0251 | The nine fact tables are defined in a data lake; the target has no data lake | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0252 | The reporting layer reads recovery.v_ace_* views directly | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0254 | No fact, dimension or measure carries an owner or a schema | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0255 | The read-model control tables and the queue measures are absent | Data architecture team | Resolved (directive) |
| GAP-0257 | dim_org holds an owner while events carry no personal data | Data steward | Resolved (directive) |
| GAP-0268 | The nine reconciliations name one Workbench side, but that side sits in seven service schemas | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0269 | No reconciliation and no quality measure carries an owner | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0270 | REC-08 compares a decision-log copy that the target retires | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0271 | No per-service reconciliation rule, cadence or result route | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0272 | Ten services have no tolerance and no legacy reconciliation row | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0273 | REC-05 and REC-09 are numbered the other way round from RWB-E1-011 | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0274 | S1 rwb-valuation owns no table in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0275 | REC-03 and REC-04 have no per-service owner in the RWB-E1-011 slice set | TechX | Resolved (directive) |
| GAP-0276 | The Timeliness measure reads a Workbench read of the ACE batch that no service but P1 makes | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0285 | No source states how the built recovery schema, 92 tables and 14 data products, is cut across the 19 rwb_* schemas or how each V0001 baseline is produced | ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0332 | DecisionRecorded payload and the ingest rule into the central ledger are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0333 | The owning rwb_* schema of the 24 operational dictionary objects is not stated | ACE database administrator | Resolved (directive) |
| GAP-0334 | deliverFile manifest payload, claim-check handoff and the file-window trigger contract are not defined | Solution architect | Resolved (directive) |
| GAP-0335 | The target read operation that serves the case list and the path by which the daily extract reaches rwb-reporting once the data lake is removed are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0336 | Owner of REC-03 and REC-04 and the reporting delivery path of the two extracts are not named for the microservice target | Solution architect | Resolved (directive) |
| GAP-0337 | The connection matrix does not show the rwb-source-data outbound reads and the exclusion operation of the case contract is not named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0338 | Connection matrix gives rwb-integration only the document REST call and the outside file edge, while the file build reads source data and the failure reaches rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0339 | E1013 integration path after the data-lake removal | Solution architect | Resolved (directive) |
| GAP-0340 | E1015 integration slice crosses the wave 2 payment service and the removed lake | Solution architect | Resolved (directive) |
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0485 | The case list extract file, the outbound file adapter and the 07:30 Power BI data set have no target after the data lake is removed | Data architect | Resolved (directive) |
| GAP-0486 | The case-list read operations and their answer shapes are not specified in Arch v5 or in TSD P1 | Solution architect | Resolved (directive) |
| GAP-0487 | The case-list workflow name, the schedule name and the 07:15 fallback are not specified | Solution architect | Resolved (directive) |
| GAP-0492 | Freshness stamp: the source time and the load time of data_product_load are mapped differently by TSD P1 T3.6 and by FSD P1 A2.14 with legacy AC1 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0493 | AceDataReady and AceDataLate: the payload fields are fixed but the CloudEvents envelope attributes, the event key, the registry subject and the login on the security scheme are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0494 | Cut-off Schedules: the Schedule names, the per-product expected_by values beyond 08:00 and MON 08:00, the catch-up window and the deployment capacity are not specified | Platform administrator | Resolved (directive) |
| GAP-0495 | The two lake extracts and the Power BI data set have no successor in the target, while the legacy story still writes them and reads the report | Solution architect | Resolved (directive) |
| GAP-0496 | TSD P1 keeps REC-03, REC-04 and a cross-estate REC-05 inside P1 while the Change Register gives rwb-case, rwb-asset and rwb-comms their own slices of the same legacy key | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0497 | The reconciliation result path, the result and break-row shape, the ReconciliationQuery interface and the workflow and activity names are not specified in any source | Tech lead | Resolved (directive) |
| GAP-0557 | RWB-P1-E1001-APP: schema-split mechanics, login name, extension-table delivery boundary and Arch v5 against FSD and TSD P1 | Solution architect | Resolved (directive) |
| GAP-0558 | DP-17 removes the INT-19 lake extract and the Power BI feed that legacy AC3 and AC7 assert | Business analyst, P1 and P9 | Resolved (directive) |
| GAP-0559 | The P1 functional and technical specifications still describe the lake publish that DP-17 removes | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0560 | RWB-E1-013 is split across four stories and no single source assigns each legacy acceptance criterion | Business analyst, P1, P3 and P9 | Resolved (directive) |
| GAP-0561 | The 05:30 late check and the worker and queue registration have no story in the build dependencies of this slice | DevOps team and platform workflow owner | Resolved (directive) |
| GAP-0562 | No measure value, definition or snapshot is produced or read by the P1 slice of RWB-E1-013 | Business analyst, P1 and P9 | Resolved (directive) |
| GAP-0563 | The readiness and status operation shapes are fixed only in part by the architecture text | Solution architect and TechX contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0564 | The gate answers COMPLETE or HOLD while the freshness list of values holds LOADED and STALE | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0565 | MSG-P1-001 now names the ACE batch where the legacy story and the integration copy name a load | Business analyst, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0647 | rwb-integration outbound-file capability: ACE read path, INT-25 source table, data-lake retirement, JOB-10 and JOB-11 split, operation naming, alert event names, deliverFile manifest and job catalog rows not settled | Solution architect | Resolved (directive) |
| GAP-0648 | Outbound-file contract: deliverFile manifest and return, notice-fact read of rwb-comms, JSON field names and problem body, event schema subject and compatibility level not fixed by any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0649 | Outbound egress infrastructure: endpoint names, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period not specified in any source | SCB IT infrastructure | Resolved (directive) |
| GAP-0650 | Outbound-file deployment: chart values, replica counts, KEDA threshold, lag and alert thresholds, dashboard names, build ID format, Airflow trigger contract of the two file windows and the message identifiers of the lag and window alerts not specified in any source | DevOps team | Resolved (directive) |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0739 | The case side of an outbound file outcome leaves the delivery-event element names, the route state to resume, the task code and due date, the fate of the legacy in-process interfaces and the two lake extracts unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0740 | The rwb-case slice of RWB-E1-011 leaves the check codes, the four operation paths, the call type to rwb-source-data, the case key columns, the Schedule cron, the access right, the login and every report value that only the data lake held unspecified | Solution architect, with the P1 rwb-source-data owner, the P3 rwb-case owner and the data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0976 | The exact per-service table list of rwb_access is not stated in one place | Solution architect | Resolved (directive) |
| GAP-0978 | The file name and sequence number of the rwb_access baseline migration are not fixed | Tech lead | Resolved (directive) |
| GAP-0979 | The constraint names and the full index set of the five tables are not specified | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-0980 | role.entra_group is a column in the technical specification and not a Workbench column in the functional one | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0981 | rwb-access access-review extract (JOB-18): the interface ID, the file pattern, the extract layout, the recipient and the review-cycle date convention are not specified, the two requester activity names and the manifest are named by no source, and the delivery events are keyed by case ID while an access-review file has no case | Solution architect, P4 with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0984 | rwb-access local decision-record store: the column set behind the five named columns, the canonical form, the genesis value, the verifier behaviour on write and read, the DECISION_LOG letters per role and the per-service login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1027 | The secondary P5 slice of RWB-E1-007 has no legacy AC and several document-hub values of the outbound path are not fixed in the sources | Solution architect (P5 document hub, with the rwb-integration contract owner) | Resolved (directive) |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1162 | The addressee and contact value reach the INT-14 file through a contract that is not in the story's contract list, and no source names the operation or its elements | Solution architect, with the P1 and P6 owners | Resolved (directive) |
| GAP-1163 | DP-17 removes the INT-19 reporting extract and the INT-20 decision-log copy, so part of legacy RWB-E1-007 has no target and no replacement in this service | Business analyst and solution architect | Resolved (directive) |
| GAP-1164 | The INT-14 record layout, the file pattern and the claim-check store of the built file are named by no source, and the document contract is not in the story's contract list | Solution architect, with the P2 and P5 owners | Resolved (directive) |
| GAP-1165 | The retired inbound load leaves TC-E1-007-05, TC-E1-007-06 and the file checks DQ-057 and DQ-059 without a target in this service | Business analyst and QA lead | Resolved (directive) |
| GAP-1166 | No source defines a run record, a run operation or the right on the interface monitor for rwb-comms | Solution architect and the gateway-bff owner | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1168 | RWB-P6-E1011-APP: the parameters and reference-data contracts of rwb-case and the rwb-source-data contract the run reads are missing from the story's C list | Solution architect | Resolved (directive) |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1170 | RWB-P6-E1011-APP: the data lake is removed, so the reconciliation and data quality extracts and the report built on them have no target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1171 | RWB-P6-E1011-APP: no event is published because DP-09 is not in the pattern set, and no operation of rwb-reporting or rwb-source-data accepts the quality facts | Solution architect | Resolved (directive) |
| GAP-1172 | RWB-P6-E1011-APP: the quality tables, the check codes, the run cadence and the two quality read operations are not named in any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1173 | RWB-P6-E1011-APP: the right of the quality reads is Platform administration R in the legacy story, and the rwb-comms RBAC matrix has no Platform administration column | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1499 | The data lake and the dashboard connection are removed, so the reporting destinations of three FSD features have no home | Solution architect | Resolved (directive) |
| GAP-1503 | The baseline measure job has two owners, one in the FSD and one in the architecture | Center of excellence | Resolved (directive) |
| GAP-1504 | The data-ready and data-late events have two directions and two owners in the source set | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1507 | No freshness source is named for the period before the ACE batch record exists | Solution architect | Resolved (directive) |
| GAP-1508 | The per-account reconciliation break rows have no store after the quality-exception table leaves the schema | Data architect | Resolved (directive) |
| GAP-1512 | Four tables carry a name, an owner and a purpose but no field list in the read sources | Data architect | Resolved (directive) |
| GAP-1513 | The bank scheduler contract is a recommendation in the architecture, not an agreed interface | Solution architect with the bank platform team | Resolved (directive) |
| GAP-1514 | The job monitor and data-quality screens are first-in here and owned by reporting in the architecture | Solution architect | Resolved (directive) |
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
| GAP-1617 | The ledger completeness target, the gap alert threshold and the strict-mode wait bound have no value in the BRD or the FSD | Solution architect with the platform administrator | Resolved (directive) |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1646 | The data lake and the Power BI connection are removed but the whole reporting FSD is built on them | Solution architect | Resolved (directive) |
| GAP-1649 | The measure set is six definitions in one acceptance criterion and seven measures in another | Tribe lead with the Reporting and BI analyst | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1984 | The Workbench table count is 92 in version 6 and 93 in the Ownership Map | Data architect | Resolved (directive) |
| GAP-1991 | P1 keeps a lake copy after the data lake is removed | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2061 | The source is written for one recovery module and has no per-service target, size or deployment shape | Architecture with RWB-PLT-OBS and RWB-PLT-DB | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2062 | No per-topic sizing exists for the 19 topics; one topic is sized in the architecture | RWB-PLT-EVT with the owning services | Resolved (directive) |
| GAP-2068 | The local decision record has no table, no DDL and no case or trace column | Service owners of the 19 services with P7 rwb-decision | Resolved (directive) |
| GAP-2074 | One chain or 19 chains plus the ledger chain | Service owner P7 rwb-decision with the 19 service owners | Resolved (directive) |
| GAP-2075 | The record that governs while the central ledger lags by up to five minutes | Service owner P7 rwb-decision | Resolved (directive) |
| GAP-2123 | The Ownership Map assigns no table to rwb-valuation although Architecture v5 gives it a schema | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2132 | The recovery table count of the source and the table count of the Ownership Map do not agree | ACE | Resolved (directive) |
| GAP-2228 | The target form of the case list is not fixed by any source: the row shape, the account-data owner in the read path, the freshness stamp, the removal of the lake path and the ownership of the reconciliation | Solution architect | Resolved (directive) |
| GAP-2229 | Element names of the two delivery outcomes, the carrier of the route state to resume and the values of the owner task are not in the sources | TechX and the rwb-integration contract owner | Resolved (directive) |
| GAP-2230 | The legacy P3 interfaces and the case-action path have no operation in the target case contract | TechX | Resolved (directive) |
| GAP-2232 | The split of RWB-E1-011 across the services and the case-side scope are not ruled by any source | Solution architect | Resolved (directive) |
| GAP-2233 | The case-side result row has no table and no check codes in the target | Solution architect | Resolved (directive) |
| GAP-2234 | No source names the operations, rights or response shapes of the case-side quality run | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2235 | The data-product reads that replace the ACE views have no published path, element shape or product code in this story's sources | Solution architect | Resolved (directive) |
| GAP-2236 | The hand-off of the case-side hold to the case-list publish gate is not specified | Solution architect | Resolved (directive) |
| GAP-2237 | TSD P3 v3 declares the case links as uuid cross-references while the FSD re-base and the legacy data table use the ACE business keys | Solution architect | Resolved (directive) |
| GAP-2238 | The report, the Schedule cadence, the alert groups and the feature flag of the case-side run have no source | Solution architect | Resolved (directive) |
| GAP-2239 | The case-facts REST operation of rwb-case is not in the API Specification or the ownership map | TechX, with the API owner of P3 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2240 | The measure-catalog read of rwb-reporting has no path or shape in the sources | TechX, with the API owner of P9 reporting | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2241 | The list code and the table code of the age-band reference list are not named | TechX, with the data steward RW-DATASTEW | Resolved (directive) |
| GAP-2242 | No message is defined for a held facts release, and SCR-44 shows no release state | TechX, with the data steward RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2401 | The LDM states one field count for rule_row and a rule_test_case column its fields sheet does not define, and both TSD P7 and the LDM name cross-schema foreign keys that DP-01 forbids | Solution architect, P7 rwb-decision, with the data owners of rwb_case and rwb_access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2534 | The DDL of proceeds beyond its columns is not published: constraint names, index names, index columns and the Field IDs of the 7 standard columns | ACE team | Resolved (directive) |
| GAP-2535 | TSD P8 T3.1 carries payment_match_rule as a second table of the module, and the Ownership Map gives P8 one table only | Solution architect | Resolved (directive) |
| GAP-2536 | The read paths that proceeds has to serve, and the screens that read it, are stated in no source of the read set | Solution architect | Resolved (directive) |
| GAP-2537 | The handover of a service's field declaration to the one dictionary has no documented mechanism or operation | Solution architect | Resolved (directive) |
| GAP-2538 | TSD P8 T3.3 declares three many-to-one relationships of proceeds and the target keeps them as values | Solution architect | Resolved (directive) |
| GAP-2539 | DP13 Money and closure is catalogued with the system of record ACE only, while the match on the same row is a Workbench record | Business analyst, P8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2541 | EP01's wave map wave is 1 and rwb-payment's Architecture v5 wave is 2 for the same story | Portfolio lead | Resolved (directive) |
| GAP-2566 | RWB-E1-013: DP-17 removes the data lake while the two criteria this service owns assert the INT-19 extract, its trailer and the lake hold | Solution architect | Resolved (directive) |
| GAP-2567 | RWB-E1-013: the plan's C row names two rwb-case contracts and omits the two rwb-source-data rows the run consumes | Solution architect | Resolved (directive) |
| GAP-2568 | RWB-E1-013: the definition load of table measure_definition has no target operation, because the table is P9's while the reference-load framework is rwb-case's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2569 | RWB-E1-013: the Ownership Map gives rwb-reporting no event while the wave 1 harness names rwb.reporting.ReportPublished.v1 on the service topic | Solution architect | Resolved (directive) |
| GAP-2570 | RWB-E1-013: the Power BI refresh that AC3 asserts has no mechanism once the data lake is removed, and the measures read is assigned to Epic 2 by the legacy story | Solution architect | Resolved (directive) |
| GAP-2571 | RWB-E1-013: the approver of a definition is typed uuid by the TSD while the legacy criteria and the FSD name the reference TRB-0001 | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2572 | RWB-E1-013: no source gives the path or the shape of the definitions read that RWB-P3-E1013-APP consumes across the service boundary | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2573 | RWB-E1-013: JOB-15 has two candidate triggers, the Temporal Schedule of DP-10 and the Airflow chain that triggers report extracts | Solution architect | Resolved (directive) |
| GAP-2574 | RWB-E1-013: the alert thresholds, the channel names and the run-book identifiers of JOB-15 have no source, and MSG-GEN-006 loses its caller with the lake | DevOps team | Resolved (directive) |
| GAP-2575 | RWB-E1-013: the three measure tables' DDL sits with no DB story of this key, so the app story's migration carries it | ACE team | Resolved (directive) |
| GAP-2579 | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-2580 | Benefit realisation: the variance fields, the variance rule, the row ceiling, the event absence and the baseline date default are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-3151 | Origin tag where one legacy criterion is carried by several new stories | TechX | Resolved (directive) |
| GAP-3154 | No service owns each of the 14 data products, so the freshness stamp has no owner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3160 | The P2 outbound adapter writes a table owned by rwb-debtsale | Integration lead | Resolved (directive) |
| GAP-3169 | The reconciliation story writes 'the case exceptions' without naming a table | P1 data owner | Resolved (directive) |
| GAP-3171 | Service P8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3172 | Service S5 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3240 | One module per item in version 3 becomes several services per item in the split | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E1008-ITG | skipped AC ID | 99 | missing: AC6, AC7, AC8 |
| RWB-ITG-E1013-ITG | skipped AC ID | 104 | missing: AC1, AC3, AC4, AC5, AC7, AC8 |
