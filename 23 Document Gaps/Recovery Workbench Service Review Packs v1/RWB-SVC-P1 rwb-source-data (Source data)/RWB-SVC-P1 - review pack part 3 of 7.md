# RWB-SVC-P1 rwb-source-data (Source data) - review pack, part 3 of 7 (RWB-P1-E1011-OPS to RWB-P1-E1017-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 180 |
| Cross-document (pending in another document) | 231 |
| Not applied (value not in the sources) | 6 |
| Open business decisions | 21 |
| Register gaps linked | 115 |
| Unconfirmed assumptions | 0 |
| Lint findings | 4 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P1-E1011-OPS | 17 | 45 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1011 OPS Reconciliation and data quality report - deployment v2.md |
| RWB-P1-E1013-APP | 28 | 38 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1013 APP Baseline measures v2.md |
| RWB-P1-E1015-APP | 36 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1015 APP Freshness stamp per data product v2.md |
| RWB-P1-E1015-CON | 17 | 22 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1015 CON Freshness stamp per data product - contract v2.md |
| RWB-P1-E1015-OPS | 15 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1015 OPS Freshness stamp per data product - deployment v2.md |
| RWB-P1-E1016-APP | 17 | 22 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1016 APP Access control per data product and catalog entries v2.md |
| RWB-P1-E1016-CON | 15 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1016 CON Access control per data product and catalog entries - contract v2.md |
| RWB-P1-E1016-DB | 13 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1016 DB Access control per data product and catalog entries - ACE DB v2.md |
| RWB-P1-E1017-APP | 22 | 25 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1017 APP Retention and archive rule for the data store v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P1-E1011-OPS | R-09679 | CG-ALL-2083 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1013-APP | R-09685 | CG-ALL-2098 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1015-APP | R-09695 | CG-ALL-2118 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1016-APP | R-09704 | CG-ALL-2156 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1011-ITG, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21922 | GAP-1651 | Register gap | Data steward and data product owner | The reconciliation and the data quality break are P1's, but FSD P9 specifies them as its own features | Read the reconciliation result and the break rows from P1's contract and hold the break view and the closure in P9 |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-21966 | GAP-1501 | Register gap | Compliance and PDPA officer | Field-level masking rules belong to the access service, while the FSD loads them here | This service keeps data_product_access (role, product, read right) and applies the masking policy of rwb-access, cached per the platform pattern; the masking rows themselves are rwb-access's. Confirm the split with Compliance and Security before the first masking test. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P7-E1017-APP | R-21967 | GAP-2070 | Register gap | Service owners P7 rwb-decision, P1 rwb-source-data and P4 rwb-access with Compliance | Where the retention period of the ledgers and the access log is held, and which job enforces it | Keep every period as written and mark the owner open: P7 enforces the ledger period, P1 the interaction ledger and P4 the access log, each as a row of its own retention data, until Compliance states where the periods are held. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21971 | GAP-1500 | Register gap | Compliance and PDPA officer | The retention rule table and the archive job move to the document service, while the FSD keeps both here | This service declares the retention class per data product and recovery table as versioned reference data, refuses a rule that names a read-only ACE view or the decision log, and archives nothing itself; the rule table and the monthly archive run belong to rwb-document. Confirm with Compliance that a class declared here and applied there is acceptable for the PDPA position. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E2008-ITG, RWB-P1-E1015-APP, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22404 | GAP-0600 | Register gap | Solution architect with the P1 data product owner | FSD P1 A2.2 stamps a payment read on DP01 Account and arrears while the Work Package slice note names DP05, and no source states whether the read or the rwb-payment run answers a held business date | Hold both gates on DP01 Account and arrears and answer 409 with MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run, with no row of any kind; record DP05 as not the stamp of a payment read and correct the slice note in the Work Package and the data product map in the next version of FSD P1 A2.2; state in RWB-P8-E2008-CON that the run's own refusal for the business date is its own and that the read's 409 is the answer to a call made anyway. |
| RWB-ITG-E1013-ITG, RWB-ITG-E2009-ITG, RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E2009-APP, RWB-P9-E1013-APP, RWB-P9-E1013-CON, RWB-P9-E1013-OPS, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-P9-E8001-APP, RWB-P9-E8001-CON, RWB-P9-E8002-APP, RWB-P9-E8002-CON, RWB-S8-E2009-APP | R-28480 | GAP-1644 | Register gap | Business lead | The program BRD has no requirement section for P9 reporting | Keep the epic-level keys as the trace target and state the coverage basis in section 11.2 until a P9 requirement section exists |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-28495 | GAP-1510 | Register gap | Compliance with Security | The classification scheme per data product and the retention periods are open, so the PRD labels are a reading of the field markers | Apply the four-label scheme from the field markers now: personal fields and the party and contact extension rows as personal data, balances and amounts as sensitive financial data, case, legal, collateral and metadata as confidential, and no data product as public. Replace with the approved scheme when DL26 closes. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-28498 | GAP-1618 | Register gap | Compliance and PDPA officer | The decision log and the ledger carry no retention period, and the WORM seal period is unstated | Set the decision-log class period and the seal period under DL26 before the first release, keep the class per record class in reference data, and state in the retention rule that no archive runs inside this service. |
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
| RWB-P1-E1015-CON | R-04364 | DOR-RWB-P1-E1015-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the source documents (Decision Log v12 and project .md files checked; only scratch files match). Sign-off cannot be asserted. Section 14 text not in chunk. |
| RWB-P1-E1016-APP | R-04374 | DOR-RWB-P1-E1016-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed EP01 epic design record in the story or sources. Searched the story file and the DoR rule, DT05 and sign-off meeting rows. Needs the record itself, not a text edit. |
| RWB-P1-E1016-APP | R-04375 | DOR-RWB-P1-E1016-APP-16 | Header | Definition of Ready item 16 Size: Fail | Added a Size row reading Not specified; the squad sizes the story at refinement. No size value is invented, so the item stays open. |
| RWB-P1-E1016-CON | R-04380 | DOR-RWB-P1-E1016-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed EP01 epic design is in the sources (Decision Log v11/v12 has only DT05; DoR v3 item 14). Confirming sign-off needs an invented record reference. Story unchanged. |
| RWB-P1-E1017-APP | R-04389 | DOR-RWB-P1-E1017-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources (prior search of folders 02-05, 11, 13 found only the sign-off meeting and process). Sign-off cannot be asserted; needs the epic design record. |
| RWB-P1-E1017-APP | R-04390 | DOR-RWB-P1-E1017-APP-16 | header | Definition of Ready item 16 Size: Fail | The size is not yet set. The header records that the squad sizes the story at refinement. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (23)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02785 | RWB-P1-E1011-OPS | CG-ALL-2074 | Header | Remove the fixed enum on result so LOV-REC-RESULT values are accepted as data, per Reference Data v5 Lists and this story. |
| CDC-02830 | RWB-P1-E1013-APP | CG-ALL-2085 | 12.1 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready in rwb-source-data.yaml through the CON story. |
| CDC-02831 | RWB-P1-E1013-APP | CG-ALL-2086 | 12.1 | Publish GET /api/recovery/source-data/v1/business-days/{date}/status in rwb-source-data.yaml through the CON story. |
| CDC-02832 | RWB-P1-E1013-APP | CG-ALL-2087 | 12.1 | Publish GET /api/recovery/source-data/v1/payments?accountId={accountId} in rwb-source-data.yaml through the CON story. |
| CDC-02833 | RWB-P1-E1013-APP | CG-ALL-2089 | 3 | Remove the closed enum on result so LOV-REC-RESULT values load as reference data without a code change. |
| CDC-02837 | RWB-P1-E1013-APP | DOR-RWB-P1-E1013-APP-8 | 12.1 | Add paths POST /business-days/{date}/ready, GET /business-days/{date}/status and GET /payments?accountId={accountId} as defined in 12.1; the error message IDs are in CG-ALL-2088. |
| CDC-02868 | RWB-P1-E1015-APP | CG-ALL-2104 | 12.1 | Add GET /api/recovery/source-data/v1/freshness to rwb-source-data.yaml through RWB-P1-E1015-CON, or remove the operation from 12.1. |
| CDC-02869 | RWB-P1-E1015-APP | CG-ALL-2105 | 12.1 | Add POST /api/recovery/source-data/v1/business-days/{date}/ready to rwb-source-data.yaml through RWB-P1-E1015-CON, or remove it from 12.1. |
| CDC-02891 | RWB-P1-E1015-CON | CG-ALL-2122 | 12.1 | Publish GET /api/recovery/source-data/v1/freshness in rwb-source-data.yaml, or remove it from the contract |
| CDC-02892 | RWB-P1-E1015-CON | CG-ALL-2123 | 12.1 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready in rwb-source-data.yaml, or remove it from the contract |
| CDC-02895 | RWB-P1-E1015-CON | DOR-RWB-P1-E1015-CON-8 | 12.1 | Declare the Idempotency-Key header on POST /business-days/{date}/ready in rwb-source-data.yaml |
| CDC-02932 | RWB-P1-E1016-APP | CG-ALL-2146 | 12.1 | Publish GET /api/recovery/source-data/v1/customers/{id} through the owner's CON story |
| CDC-02933 | RWB-P1-E1016-APP | CG-ALL-2147 | 12.1 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the owner's CON story |
| CDC-02934 | RWB-P1-E1016-APP | CG-ALL-2148 | 12.1 | Publish GET /api/recovery/source-data/v1/collateral/{id} through the owner's CON story |
| CDC-02935 | RWB-P1-E1016-APP | CG-ALL-2149 | 12.1 | Publish GET /api/recovery/source-data/v1/payments?accountId= through the owner's CON story |
| CDC-02938 | RWB-P1-E1016-APP | DOR-RWB-P1-E1016-APP-8 | 12 | Add paths GET /customers/{id}, GET /accounts/{id}, GET /collateral/{id} and GET /payments?accountId=, and the one further path the detcheck counts. |
| CDC-02954 | RWB-P1-E1016-CON | CG-ALL-2161 | 12.1 | Publish GET /api/recovery/source-data/v1/customers/{id} in rwb-source-data.yaml, through the CON story |
| CDC-02955 | RWB-P1-E1016-CON | CG-ALL-2162 | 12.1 | Publish GET /api/recovery/source-data/v1/accounts/{id} in rwb-source-data.yaml, through the CON story |
| CDC-02956 | RWB-P1-E1016-CON | CG-ALL-2163 | 12.1 | Publish GET /api/recovery/source-data/v1/collateral/{id} in rwb-source-data.yaml, through the CON story |
| CDC-02957 | RWB-P1-E1016-CON | CG-ALL-2164 | 12.1 | Publish GET /api/recovery/source-data/v1/payments?accountId= in rwb-source-data.yaml, through the CON story |
| CDC-02990 | RWB-P1-E1017-APP | CG-ALL-2181 | 12.1 | Publish POST /api/recovery/source-data/v1/retention-runs with the request body and 202 answer fixed by RWB-P1-E1017-CON |
| CDC-02991 | RWB-P1-E1017-APP | CG-ALL-2182 | 12.1 | Publish GET /api/recovery/source-data/v1/retention-runs/{runId} with the answer schema fixed by RWB-P1-E1017-CON |
| CDC-02995 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-23 | header | Add the POST /retention-runs path (used by JOB-17 per the story change log). The file is version 5.0.0 (line 9) but has no retention-runs path (grep confirmed). Story text not edited: citing 5.0.0 would be unsupported until the path exists. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02791 | RWB-P1-E1011-OPS | CG-ALL-2077 | 12.5 | Add Activity row reconciliation on task queue rwb-source-data to the Activities sheet. |
| CDC-02834 | RWB-P1-E1013-APP | CG-ALL-2093 | 12.5 | The workflow reconciliation (JOB-04) is kept as the story names it. The Temporal Catalog v1 needs the row. |
| CDC-02839 | RWB-P1-E1013-APP | CG-ALL-2094 | 12.5 | Add an Activities row for snapshot(page) on task queue rwb-source-data, input business date and page cursor, output one page of the date's facts with the next cursor. |
| CDC-02870 | RWB-P1-E1015-APP | CG-ALL-2108 | 12.5 | Add a Workflows row for AceIngestCheckWorkflow on task queue rwb-source-data. No catalogued replacement is named in the sources. |
| CDC-02874 | RWB-P1-E1015-APP | CG-ALL-2109 | 12.5 | Add an Activities row for stampProducts, or the story must use a catalogued activity. |
| CDC-02875 | RWB-P1-E1015-APP | CG-ALL-2110 | 12.5 | Add an Activities row for markStale, or the story must use a catalogued activity. |
| CDC-02876 | RWB-P1-E1015-APP | CG-ALL-2111 | 12.5 | Add Activities rows for publishAceDataReady and publishAceDataLate, or the story must use catalogued activities. |
| CDC-02877 | RWB-P1-E1015-APP | CG-ALL-2112 | 12.5 | Add an Activities row for checkDailyCompleteness, or the story must use a catalogued activity. |
| CDC-02894 | RWB-P1-E1015-CON | CG-ALL-2125 | 12.5 | Add an AceIngestCheckWorkflow row to the Workflows sheet |
| CDC-02897 | RWB-P1-E1015-CON | CG-ALL-2126 | 12.5 | Add a checkDailyCompleteness row to the Activities sheet |
| CDC-02920 | RWB-P1-E1015-OPS | CG-ALL-2136 | 12.5 | Add activity checkDailyCompleteness with task queue rwb-source-data, registered by the worker. |
| CDC-02930 | RWB-P1-E1015-OPS | GAP-0494 | 11 | The Schedule name, the per-product expected_by values beyond 08:00 and MON 08:00, the catch-up window and the deployment capacity are Not specified in the source documents (GAP-0494); the catalog extension is cross-document. |
| CDC-02992 | RWB-P1-E1017-APP | CG-ALL-2183 | 12.5 | Catalog v1 is .xlsx only and was not read; no export found. RetentionWorkflow (P5 E1041 APP §12.5) is rwb-document's JOB-17 run, not this one. |
| CDC-02998 | RWB-P1-E1017-APP | CG-ALL-2185 | 12.5 | Add activity selectRows(page) with task queue rwb-source-data and the contract element of 12.5 |
| CDC-02999 | RWB-P1-E1017-APP | CG-ALL-2186 | 12.5 | Add activity archiveTable with task queue rwb-source-data and the contract element of 12.5 |
| CDC-03000 | RWB-P1-E1017-APP | CG-ALL-2187 | 12.5 | Add activity verifyManifest with task queue rwb-source-data and the contract element of 12.5 |
| CDC-03001 | RWB-P1-E1017-APP | CG-ALL-2188 | 12.5 | Add activity deleteArchivedRows with task queue rwb-source-data and the contract element of 12.5 |
| CDC-03002 | RWB-P1-E1017-APP | CG-ALL-2189 | 12.5 | Add activity recordRun with task queue rwb-source-data and the contract element of 12.5 |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02878 | RWB-P1-E1015-APP | CG-ALL-2114 | 4, 14 | Section 14 uses MSG-P4-001 for a no-role case that the standard's meaning does not carry. The business analyst must add any new meaning to the standard first. |
| CDC-02881 | RWB-P1-E1015-APP | DOR-RWB-P1-E1015-APP-9 | 14 | MSG-P1-001 English text aligned to the standard; MSG-P4-001 text changed to a no-role meaning. |
| CDC-02898 | RWB-P1-E1015-CON | CG-ALL-2127 | 14 | Add a new message ID for 'No session on a read' with text 'Sign in to continue.'; MSG-P4-001 keeps 'Sign-in with no Workbench role'. |
| CDC-02901 | RWB-P1-E1015-CON | DOR-RWB-P1-E1015-CON-9 | 14 | Add a new message ID for 'No session on a read' with text 'Sign in to continue.'; MSG-P4-001 keeps 'Sign-in with no Workbench role' (as CG-ALL-2127). |
| CDC-02923 | RWB-P1-E1015-OPS | DOR-RWB-P1-E1015-OPS-9 | find it | Confirm the v4 wording of MSG-P1-001 so section 14 can match it |
| CDC-02942 | RWB-P1-E1016-APP | CG-ALL-2152 | 4, 14 | Add a new message ID for 'No valid session' with the text 'Your session has ended. Sign in again.'. MSG-P4-001 keeps its standard meaning. |
| CDC-02946 | RWB-P1-E1016-APP | DOR-RWB-P1-E1016-APP-9 | 14 | In §4 add two new message IDs: (1) catalog load marks a v_ace_* view with a system of record other than ACE (AC11), English as in story §14 row MSG-P1-003; (2) no valid session, 'Your session has ended. Sign in again.'; Thai for both. Then repoint the story. |
| CDC-02949 | RWB-P1-E1016-APP | CG-ALL-2151 | 14 | Add a new P1 message ID, raised when a catalog load marks a v_ace_* view with a system of record other than ACE (AC11), English as in story §14 row MSG-P1-003, plus Thai; then replace MSG-P1-003 in the story with it. |
| CDC-02959 | RWB-P1-E1016-CON | CG-ALL-2166 | 4, 14 | Add a new message ID for the 'No valid session' text; the story then cites that ID in §14 in place of MSG-P4-001 |
| CDC-02964 | RWB-P1-E1016-CON | DOR-RWB-P1-E1016-CON-9 | 14 | Align the MSG-P1-003 row with the §14 text, which BR4 copies unchanged from the legacy story |
| CDC-02967 | RWB-P1-E1016-CON | CG-ALL-2167 | 14 | BA adds a new P1 message ID with the English text and When of RWB-P1-E1016-CON §14 row MSG-P1-003, plus Thai text; the story then cites that ID. MSG-P1-003 in the standard stays. |
| CDC-03003 | RWB-P1-E1017-APP | CG-ALL-2191 | 4, 14 | Business analyst adds a new message ID for a start whose body fails validation, text 'The request is not valid: {detail}.'; story then cites it |
| CDC-03007 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-9 | 14 | Align the MSG-P2-006 text with the standard and confirm the meaning of MSG-GEN-001 used for X9 and for a start whose body fails validation. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02816 | RWB-P1-E1011-OPS | CG-ALL-2080 | 16 | Add rows TC-E1-011-08 (covers AC7) and TC-E1-011-09 (covers AC6), with Given, When and Then copied from those criteria. |
| CDC-02879 | RWB-P1-E1015-APP | CG-ALL-2115 | 16 | Add rows TC-E1-015-10, TC-E1-015-11 and TC-E1-015-12 to tab Story test cases, with Given, When and Then copied from AC9, AC10 and AC11. |
| CDC-02880 | RWB-P1-E1015-APP | DOR-RWB-P1-E1015-APP-12 | 16 | Story adds TC-13 and TC-14 (section 12 contract and 12.7 boundary), TC-15 to TC-17 (BR9 to BR11) and TC-18 to TC-29 (AC15 to AC26). Workbook and RTM v7 rows are pending. |
| CDC-02900 | RWB-P1-E1015-CON | DOR-RWB-P1-E1015-CON-12 | 12.7, 16, 18 | Add TC-E1-015-10, TC-E1-015-11 and TC-E1-015-12 to tab Story test cases; align the section 18 test lists with RTM v7. |
| CDC-02910 | RWB-P1-E1015-CON | CG-ALL-2129 | 16 | Add rows TC-E1-015-10, TC-E1-015-11 and TC-E1-015-12 with Given, When and Then copied from the criteria they cover (AC2 and AC4; AC2; AC3 and AC4). |
| CDC-02928 | RWB-P1-E1015-OPS | CG-ALL-2138 | 16 | Add rows TC-E1-015-10, TC-E1-015-11, TC-E1-015-12 with Given, When and Then from the criteria they cover |
| CDC-02943 | RWB-P1-E1016-APP | CG-ALL-2153 | 16 | Add rows for TC-E1-016-10, TC-E1-016-11 and TC-E1-016-12 to the next version, with Given, When and Then copied from AC9, AC10 and AC11. |
| CDC-02968 | RWB-P1-E1016-CON | CG-ALL-2168 | 16 | Add rows TC-E1-016-10, TC-E1-016-11 and TC-E1-016-12 to tab Story test cases, with Given, When and Then copied from AC1 and AC7, AC2 and AC7, and AC3 and AC6. |
| CDC-02969 | RWB-P1-E1016-CON | CG-ALL-2169 | 16 | TC-E1-016-05 to -07 covers rows changed. TC-E1-016-08 stays on AC3 because this story's AC8 is about rule tracing; QA to reconcile the v8 row. |
| CDC-02979 | RWB-P1-E1016-DB | DOR-RWB-P1-E1016-DB-12 | 12.7,16,18 | Add story rows TC-E1-016-10, TC-E1-016-11 and TC-E1-016-12 to tab Story test cases; align RTM v7 with section 18. |
| CDC-02985 | RWB-P1-E1016-DB | CG-ALL-2176 | 16 | Add rows TC-E1-016-10, TC-E1-016-11 and TC-E1-016-12 with Given, When and Then copied from the criteria they cover. |
| CDC-02986 | RWB-P1-E1016-DB | CG-ALL-2177 | 16 | The Covers column keeps this story's own criteria. The numbers AC5, AC6 and AC8 match legacy RWB-E1-016 criteria, so the workbook's Covers values need correcting. No story edit. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02817 | RWB-P1-E1011-OPS | CG-ALL-2082 | 18 | Align the REQ-RDF-007, REQ-RDF-008 and REQ-CWC-004 test lists with RWB-P1-E1011-OPS section 18 in the next RTM version. |
| CDC-02859 | RWB-P1-E1013-APP | CG-ALL-2097 | 18 | The RTM test list is the document to change. Section 18 only has its range extended to cover the added test rows, up to TC-E1-013-22. |
| CDC-02888 | RWB-P1-E1015-APP | CG-ALL-2117 | 18 | Align the REQ-RDF-009 test list with RWB-P1-E1015-APP §18 (TC-E1-015-03, TC-E1-015-08 and the §16 rows) in the next RTM version; TC-E1-023-02, TC-E1-023-04 and TC-E1-069-03 belong to other stories. |
| CDC-02911 | RWB-P1-E1015-CON | CG-ALL-2131 | 18 | Align the REQ-RDF-009 test list in RTM v7 with section 18 of this story (TC-E1-015-01, -03, -10, -11) and reconcile the other TC rows in the next version. |
| CDC-02929 | RWB-P1-E1015-OPS | CG-ALL-2140 | 18 | Status set to Cross-document; story side not changed further |
| CDC-02950 | RWB-P1-E1016-APP | CG-ALL-2155 | 18 | Align REQ-RDF-010 test list with section 18 of RWB-P1-E1016-APP (TC-E1-016-01, TC-E1-016-03 to 10), or the reverse, in the next RTM version. |
| CDC-02970 | RWB-P1-E1016-CON | CG-ALL-2170 | 18 | Align the test lists of the three differing requirements with RWB-P1-E1016-CON section 18 in the next RTM version. |
| CDC-02987 | RWB-P1-E1016-DB | CG-ALL-2178 | 18 | Align the REQ-RDF-010 and REQ-RDF-011 test lists with section 18 of RWB-P1-E1016-DB, including TC-E1-016-10 and the test cases the RTM lists for this story. |
| CDC-03009 | RWB-P1-E1017-APP | CG-ALL-2192 | 18 | Section 18 lists the same test cases as section 16. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02792 | RWB-P1-E1011-OPS | DOR-RWB-P1-E1011-OPS-1 | 1 | Add 'platform engineer' as a role code or role name, or the story names a role that already exists there. |
| CDC-02899 | RWB-P1-E1015-CON | DOR-RWB-P1-E1015-CON-1 | 1 | Register 'tech lead' as a role code or role name, or confirm the role name the story should use. |
| CDC-02921 | RWB-P1-E1015-OPS | DOR-RWB-P1-E1015-OPS-1 | 1 | Register 'platform engineer' as a role code or name, or confirm the role section 1 uses |
| CDC-02960 | RWB-P1-E1016-CON | DOR-RWB-P1-E1016-CON-1 | 1 | Add 'tech lead' as a role name or code, or list the §1 persona's role in UR&P v5 |
| CDC-02977 | RWB-P1-E1016-DB | DOR-RWB-P1-E1016-DB-1 | 1 | Add the role 'ACE database engineer' with its role code, or name the role that exists. |
| CDC-03006 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-6 | 10 | Add role SY-DATALOAD. Story side: rwb-access authorise step for POST /retention-runs and GET /retention-runs/{runId} added to section 10; check name Not specified in the source documents. |

### RWB-P9-E1013-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02836 | RWB-P1-E1013-APP | DOR-RWB-P1-E1013-APP-22 | 14 | No fake library version is recorded in the source documents. The contract story must record the published version. |
| CDC-02847 | RWB-P1-E1013-APP | GAP-2570 |  | Declare the GET /reports/measures read shape in the wave 1 contract for the harness and the catalog consumer; the dashboard and SCR-37 stay in RWB-P9-E2009-APP. |
| CDC-02853 | RWB-P1-E1013-APP | GAP-2240 | find it | Publish the measure-catalog read as GET on the rwb-reporting base with an onDate parameter and name it in the Service Contract Catalog. |
| CDC-02855 | RWB-P1-E1013-APP | GAP-2572 | find it | Declare GET /measure-definitions with query onDate and a definition list answer, marked as a target pending P3 confirmation of path and fields. |
| CDC-02857 | RWB-P1-E1013-APP | GAP-2568 | find it | Declare the reference-load element of table measure_definition on the rwb-reporting base, keep list values on the rwb-case reference contract, and get rwb-case confirmation of ownership. |
| CDC-02866 | RWB-P1-E1013-APP | GAP-2571 | 16 | Declare measure_definition.approved_by as uuid and approved_at as timestamptz per TSD P9 T3.1, carry TRB-0001 as a comment on the element; the story fixture of TC-E1-013-01 already holds TRB-0001 |

### RWB-P6-E1011-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02798 | RWB-P1-E1011-OPS | GAP-1168 | n/a | Add RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-source-data data-product contract to the C list; name the reference-data read operation in RWB-P3-E1043-CON; keep the build unblocked by the 12.8 fakes until published. |
| CDC-02806 | RWB-P1-E1011-OPS | GAP-1170 | 4 | Drop the reconciliation and data quality extracts and the INT-19 path; serve quality facts from GET /api/recovery/comms/v1/quality-results; record the decision in the Change Register against RWB-E1-014 and INT-19. |
| CDC-02807 | RWB-P1-E1011-OPS | GAP-1171 | 12 | Serve the quality facts from the read model of this service for wave 1; settle in wave 2 whether rwb-reporting reads them or a quality event is added with DP-09 and a platform event library story. |
| CDC-02815 | RWB-P1-E1011-OPS | GAP-1167 | find it | Keep H at None; record the seven platform CONs as wave-0 build prerequisites arriving with the platform release train; add them to the dependency map as platform prerequisites, not lane dependencies, so L-P6-C depth is unchanged. |

### RWB-P9-E1013-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02854 | RWB-P1-E1013-APP | GAP-2566 | find it | Keep legacy AC3 and AC7 word for word. Prove publish, freshness stamp, hold and resend on measure_publish in rwb_reporting. Declare no lake path or extract element. |
| CDC-02856 | RWB-P1-E1013-APP | GAP-2573 | find it | Register one Schedule at 01:30 Asia/Bangkok for the measures run and leave the Airflow call of a report extract unwired. |
| CDC-02858 | RWB-P1-E1013-APP | GAP-2569 | find it | Declare no event in 12.3 and 12.4. Keep the topic provisioned by the platform. Raise any freshness event as its own story with the outbox library row. |
| CDC-02867 | RWB-P1-E1013-APP | GAP-2575 | 8 | The three measure tables belong to rwb-reporting, so their DDL belongs in that service's migration. BR13 keeps this service from reading or writing them. |

### RWB-P1-E1015-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02871 | RWB-P1-E1015-APP | DOR-RWB-P1-E1015-APP-21 | header | Set build status to Done once the contract story is built; it is currently Not started. |
| CDC-02872 | RWB-P1-E1015-APP | DOR-RWB-P1-E1015-APP-22 | header | Publish the contract fake library and record its published version. |
| CDC-02916 | RWB-P1-E1015-OPS | DOR-RWB-P1-E1015-OPS-21 | find it | Set build status to Done with the contract published. |
| CDC-02917 | RWB-P1-E1015-OPS | DOR-RWB-P1-E1015-OPS-22 | find it | Publish a contract fake library version and record it as published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02893 | RWB-P1-E1015-CON | CG-ALL-2124 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml |
| CDC-02913 | RWB-P1-E1015-OPS | CG-ALL-2134 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider CON story, or the consumer switches to a published operation. |
| CDC-02936 | RWB-P1-E1016-APP | CG-ALL-2150 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story |
| CDC-02958 | RWB-P1-E1016-CON | CG-ALL-2165 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml, through the provider's CON story |

### RWB-P1-E1011-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02787 | RWB-P1-E1011-OPS | DOR-RWB-P1-E1011-OPS-21 | Header | Publish the contract and set its build status to Done before this story starts. |
| CDC-02804 | RWB-P1-E1011-OPS | GAP-0497 | 12.1 | Publish GET /admin/reconciliation/results and GET /admin/reconciliation/results/{resultId} with the result and break-row element lists, the workflow ID recon-{businessDate}, the activity reconciliation and the ReconciliationQuery interface. |
| CDC-02811 | RWB-P1-E1011-OPS | GAP-2235 | 11 | Publish the freshness read and one product-coded records read per data product on /api/recovery/source-data/v1 with the business date, paging, element names and plan_ref keys. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02820 | RWB-P1-E1011-OPS | GAP-0274 |  | S1 row keeps rwb-valuation as owner, states the Arch v5 capability, and carries the Template and Rules R9 placeholder until a table is listed for it. |
| CDC-02824 | RWB-P1-E1011-OPS | GAP-1173 |  | Declare the two quality reads in Platform administration with right R; add that area to the RBAC matrix and gateway-bff route; keep case notice read at Litigation R with scope. |
| CDC-02919 | RWB-P1-E1015-OPS | GAP-3154 | find it | Add data product rows DP01 to DP14 with the owning service of each, or name the owners in the PRDs. Stamp stays in rwb-source-data for Epic 1. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02822 | RWB-P1-E1011-OPS | GAP-0337 |  | Add the three JOB-04 outbound reads to the rwb-source-data row; publish the case exclusion resource with path, fields and 2 s budget. |
| CDC-02884 | RWB-P1-E1015-APP | GAP-0493 | 1 | Name the registry subject and compatibility level for rwb.source-data.events.v1; fix types and nullability of the seven T5.3 payload fields. |
| CDC-02941 | RWB-P1-E1016-APP | CG-ALL-2145 | 7 | Record recovery_svc as the rwb_source_data login of the recovery service in the owning document, as DP-02 already states. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02835 | RWB-P1-E1013-APP | DOR-RWB-P1-E1013-APP-14 | 14 | Record the signed epic design sign-off, then cite it in this story. |
| CDC-02915 | RWB-P1-E1015-OPS | DOR-RWB-P1-E1015-OPS-14 | Header | Record the signed epic design (sign-off) for EP01 and mark Definition of Ready item 14 Pass for RWB-P1-E1015-OPS. |
| CDC-02973 | RWB-P1-E1016-DB | DOR-RWB-P1-E1016-DB-14 | header | Record the signed epic design sign-off for EP01 in the epic design record. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02945 | RWB-P1-E1016-APP | DOR-RWB-P1-E1016-APP-7 | 11 | Add v_data_product_catalog, v_data_dictionary and recovery_svc as named read model and login entries, or confirm they sit outside the LDM as read-model and login names. |
| CDC-02963 | RWB-P1-E1016-CON | DOR-RWB-P1-E1016-CON-7 | 11 | No entity added; v_data_product_catalog stays a read-model view recorded in RWB-P1-E1016-DB, as §12.7 states |
| CDC-02976 | RWB-P1-E1016-DB | CG-ALL-2175 | 1 | Record v_data_dictionary as a read-model object of RWB-P1-E1001-APP, or name its dictionary entity. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02793 | RWB-P1-E1011-OPS | DOR-RWB-P1-E1011-OPS-12 | 12, 12.7, 16, 18 | Add TC-E1-011-08 and TC-E1-011-09 to Story test cases; align Covers with this story's criteria; align section 18 test lists with RTM v7. |
| CDC-02962 | RWB-P1-E1016-CON | DOR-RWB-P1-E1016-CON-12 | 12.7, 16, 18 | Add TC-E1-016-10 to -12 under this story in Test Cases v8; align RTM v7 test lists to §18 of this story |

### OTHER:Reconciliation register v3 (REC ownership) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02801 | RWB-P1-E1011-OPS | GAP-0275 | n/a | Record that S2 (rwb-treatment) owns the Workbench side of REC-03 and P8 (rwb-payment) owns REC-04, each answered on its contract. Slices to be added at Step D1; no story created here. |
| CDC-02802 | RWB-P1-E1011-OPS | GAP-0336 | Header | Integration dependencies row now names the deliverFile manifest and states no extract job or lake path; REC-03 and REC-04 owner is not named in the story. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02808 | RWB-P1-E1011-OPS | GAP-2232 | 3 | Rule that rwb-case owns the case-side facts of REC-01, REC-03 and REC-05 over its own tables, writes no reconciliation_result row and owns no legacy criterion; record the boundary. |
| CDC-02813 | RWB-P1-E1011-OPS | GAP-2237 | find it | Align TSD P3 DF-CAS-026 link columns to account_key and person_key varchar business keys per FSD re-base D-RCV-35; record the uuid form as the pre-re-base artefact in the Change Register. |

### OTHER:rwb-case service contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02810 | RWB-P1-E1011-OPS | GAP-2234 | 12.1 | Publish the four operations of the legacy run with Platform administration R, Reporting R, Platform administration U, the 400, 401, 403, 404, 409 and 503 problem set and an Idempotency-Key on the rerun. |
| CDC-02812 | RWB-P1-E1011-OPS | GAP-2236 | 12.1 | Expose GET /reconciliation/status on rwb-case returning RELEASED, HELD or NOT_RUN for the business date and the unexplained exclusion count per product group. |

### OTHER:FSD P9 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02838 | RWB-P1-E1013-APP | GAP-1646 | 4 | Read Power BI and data lake destinations of A2.1, A2.3, A2.4, A2.5, A2.7 and A2.8 as the reporting read model on the gateway-bff route, and lake deliveries as files delivered by rwb-integration; rewrite AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01 and AC-ALT-P9-004-01. |
| CDC-02846 | RWB-P1-E1013-APP | GAP-1649 | find it | Publish the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE in AC-P9-001-01; align AC-P9-003-01, AC-P9-008-01, AC-ALT-P9-003-01 and AC-ALT-P9-003-02; carry the count as an open question. |

### OTHER:Functional Specification P1 and Technical Specification P1 (rwb-source-data) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02862 | RWB-P1-E1013-APP | GAP-0559 | none | Mark the lake steps, the INT-19 row and lake_copy_watermark removed in the next versions; keep the publish status of the case list and the reconciliation result. |
| CDC-02864 | RWB-P1-E1013-APP | GAP-0565 | 14, 15 | Story sections 14 and 15 use the Error and Message Standard v4 text of MSG-P1-001. The FSD and TSD P1 wording names the ACE batch and differs. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02873 | RWB-P1-E1015-APP | GAP-3154 | header | Name the owning service for DP01 to DP14. The freshness stamp stays in P1 for Epic 1, so no story change is needed. |
| CDC-02896 | RWB-P1-E1015-CON | GAP-3154 | none | Name the owner of DP01 to DP14 in the PRD; keep the freshness stamp in rwb-source-data for Epic 1. Ownership Map v1 also needs the product rows. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02885 | RWB-P1-E1015-APP | GAP-1504 | 1 | Set EV-26 and EV-27 direction to Produced by rwb-source-data on rwb.source-data.events.v1; ACE ingestion is not a producer on a Recovery topic. |
| CDC-02927 | RWB-P1-E1015-OPS | GAP-1504 | 18 | EV-26 and EV-27 direction Produced by rwb-source-data on rwb.source-data.events.v1; ACE ingestion removed as owning module |

### RWB-P2-E2007-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02886 | RWB-P1-E1015-APP | GAP-0597 | 12.1 | Publish GET /batch-status with key pair sourceSystem and businessDate, values status, isComplete, startedAt, completedAt, recordCount, feedVersion; 404 with MSG-P1-001 when no batch row; state it is the gate read distinct from the freshness reads. |
| CDC-02908 | RWB-P1-E1015-CON | GAP-0594 |  | Publish GET /booking-facts and GET /batch-status on /api/recovery/source-data/v1 with BookingFact, BookingFactsAnswer, FieldState and BatchStatusAnswer; freshness element as DataProductFreshness. |

### OTHER:Legacy dependency trace sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02890 | RWB-P1-E1015-APP | GAP-3233 | none | Keep the five version 4 dependencies as Not carried rows; add an X row later only if the run books or the harness wait for the named story. |
| CDC-02931 | RWB-P1-E1015-OPS | GAP-3233 | 5 | Keep the five Not carried rows visible in the trace; add an X row only if the run books or the harness waits for the named story |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02903 | RWB-P1-E1015-CON | GAP-2228 | find it | Publish CaseListRow per open case with account keys and legacy account columns; rwb-case reads the freshness answer of RWB-P1-E1015-CON in one hop with a 2 s budget; drop case_list_row, extract, lake path and DP-17 data set; REC-01 and REC-05 stay with RWB-P1-E1011. |
| CDC-02904 | RWB-P1-E1015-CON | GAP-0357 |  | Publish the base and route of the five template operations under /api/recovery/comms/v1/admin/templates, the composite route of SCR-33, and the data product whose freshness stamp the catalog shows. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02922 | RWB-P1-E1015-OPS | DOR-RWB-P1-E1015-OPS-12 | 16 | Add TC-E1-015-10, -11, -12 to Test Cases v8 with Given, When, Then; align section 18 test lists to RTM v7 |
| CDC-02944 | RWB-P1-E1016-APP | DOR-RWB-P1-E1016-APP-12 | 16, 18 | Contract and boundary tests were added to section 16 (TC-E1-016-13, -14). The workbook and matrix rows belong to those documents. |

### RWB-P1-E1016-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02937 | RWB-P1-E1016-APP | DOR-RWB-P1-E1016-APP-21 | Header | Complete the build so its status is Done with the contract published |
| CDC-02974 | RWB-P1-E1016-DB | DOR-RWB-P1-E1016-DB-21 | header | Move build status from Not started to Done before this story is ready. |

### RWB-P1-E1016-DB (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02939 | RWB-P1-E1016-APP | CG-ALL-2143 | 2, 3, 4, 7, 12.7, 12.8, 13 | Record v_data_product_catalog as the catalog read-model object that RWB-P1-E1016-DB creates. Use the same name in the owning document; LDM v9 needs no new field. |
| CDC-02951 | RWB-P1-E1016-APP | GAP-0484 | 13 | Deliver the three indexes, read model v_data_product_catalog, DPA-2026.11 seed, 122/1,366 dictionary conformance check and schema checks; create no table already created by RWB-P1-E1001-APP or RWB-P1-E1069-DB; own no masking row; repeat run changes nothing. |

### RWB-P1-E1001-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02940 | RWB-P1-E1016-APP | CG-ALL-2144 | 2, 18 | Record v_data_dictionary as the read-model object that RWB-P1-E1001-APP delivers in schema rwb_source_data. |
| CDC-02947 | RWB-P1-E1016-APP | GAP-0557 | find it | Adopt the five assumptions: keep V0001 as built; create P1's 13 own tables in rwb_source_data from its split migration; name schema and login rwb_source_data; leave the four extension tables to RWB-P1-E1069-DB; keep the catalog read model with no REST operation added. |

### RWB-P5-E1016-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02953 | RWB-P1-E1016-APP | GAP-1028 | 12 | Apply the proposed fix: record the split and origin of the six criteria; publish the two retention-class operations with the RetentionClass shape; consume published P4, P3 and P1 contracts with fakes; add the four C entries; inherit guard library and gateway route; name the login as the source states. |
| CDC-02989 | RWB-P1-E1016-DB | GAP-1028 | 7 | Accept the six new criteria as the P5 deliverable and record the split; publish GET /api/recovery/document/v1/retention-classes and .../retention-classes/{classCode} with the RetentionClass shape of RWB-P5-AD021-CON; consume the P4, P3 and P1 operations as contracts with fakes and add the four missing C entries; inherit the guard library and gateway route from the service template with no H dependency. |

### RWB-P1-E1017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02993 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-21 | find it | Build status from Not started to Done |
| CDC-02994 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-22 | find it | Publish a contract fake library version and record it as published |

### RWB-P7-E1017-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03010 | RWB-P1-E1017-APP | GAP-2427 | 14 | S14 MSG-P7-009 text: 'The decision record was refused: {field} is missing or not valid.' (RWB-PLT-E1027-CON s14). Other three texts and ids: none found; keep placeholders. |
| CDC-03011 | RWB-P1-E1017-APP | GAP-2428 | none | Record JOB-14 at 02:00 Asia/Bangkok on queue rwb-decision, page size 5000, one run at a time, property names and flag-off behaviour in the service template. |

### RWB-P1-E1011-OPS; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02786 | RWB-P1-E1011-OPS | DOR-RWB-P1-E1011-OPS-14 | Header | Record the signed epic design sign-off for RWB-P1-E1011-OPS. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02788 | RWB-P1-E1011-OPS | DOR-RWB-P1-E1011-OPS-22 | 12.8 | rwb-case fakes are named in 12.8 and the published fake library version is marked Not specified. Publishing the fake library version belongs to the contract stories. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02789 | RWB-P1-E1011-OPS | DOR-RWB-P1-E1011-OPS-8 | Header | Resolve CG-ALL-2074, CG-ALL-2075, CG-ALL-2076 and CG-ALL-2077 in those catalogs and the yaml. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02790 | RWB-P1-E1011-OPS | CG-ALL-2075 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1 (EV-26), with its ACL. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02794 | RWB-P1-E1011-OPS | GAP-0268 | find it | Give each reconciliation row an owner from the Ownership Map; the owning service answers the Workbench side on its contract (one hop, 2 s timeout); rwb-source-data keeps the ACE side and the JOB-04 run. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations and Quality measures sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02795 | RWB-P1-E1011-OPS | GAP-0269 | find it | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures, values from the Ownership Map Tables sheet. |

### OTHER:FSD P1 (features A2.12; OTHER:A2.19; OTHER:A2.20) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02796 | RWB-P1-E1011-OPS | GAP-1499 | find it | Remove the Data lake and INT-19 extract integration points; the reporting outputs move to rwb-reporting per Architecture v5 slides 41 and 44. |

### OTHER:RWB-E1-055 story file and the reconciliation check register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02797 | RWB-P1-E1011-OPS | GAP-1169 | n/a | Give the notice barcode break its own check code, distinct from REC-05 (business-key orphan check) and REC-09, so one code has one meaning. Keep REC-05 for the business-key orphan check as the data steward settled. |

### OTHER:Reconciliation register v3 (Reconciliations sheet; OTHER:REC-08 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02799 | RWB-P1-E1011-OPS | GAP-0270 | n/a | Restate REC-08 as the local decision record of each of the 19 services on rwb.decision-record.v1 compared with P7 decision_log_entry, on count and last hash nightly, with the JOB-14 02:00 hash-chain check. |

### OTHER:Reconciliation register v3 (to v4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02800 | RWB-P1-E1011-OPS | GAP-0273 | n/a | Add a REC numbering block mapping each check to its number in this document and to the number RWB-E1-011 and the story set give it. Source IDs are not renumbered. |

### RWB-P1-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02803 | RWB-P1-E1011-OPS | GAP-0496 | n/a | Keep REC-01, REC-02 and REC-05 over P1 tables in RWB-P1-E1011-APP. Remove REC-03 and REC-04 from P1 and leave them to S2, S5 and P6/payment slices. Proven end to end in RWB-ITG-E1011-ITG. |

### OTHER:rwb-case service contract and the rwb-case slice story of RWB-E1-011 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02805 | RWB-P1-E1011-OPS | GAP-0740 | 12 | Publish the four rwb-case operation paths, the three check codes and four run states, the case key columns, the access rights and the schedule per the item's proposed fix. |

### OTHER:RWB-P3 rwb-case slice of RWB-E1-011 and the rwb-case service baseline migration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02809 | RWB-P1-E1011-OPS | GAP-2233 | 11 | Create case_quality_run, case_quality_result and case_quality_break in schema rwb_case with the legacy reconciliation_result columns and a unique key on rec_code, quality_check, business_date and product_group. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02814 | RWB-P1-E1011-OPS | GAP-1946 | find it | Keep H and C at None; record the nine platform and rwb-case CONs as wave-0 prerequisites; read the ACE-side check as the DP06 data product; drop the two extracts and the INT-19 path; serve quality facts from the asset quality API. |

### OTHER:Recovery Workbench reconciliation register v3 (new Per-service reconciliation sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02818 | RWB-P1-E1011-OPS | GAP-0271 | find it | Add a sheet with one row per service for the 19 services giving tables, check part, key, tolerance, cadence, break and result route, pattern and basis; use the Template and Rules R9 placeholder where the source states no cadence or route. |

### OTHER:Recovery Workbench reconciliation register v3 (Reconciliations sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02819 | RWB-P1-E1011-OPS | GAP-0272 | find it | Add rows for P2, P4, P5, P10, S1, S3, S4, S6, S8 and S9; set the tolerance cell to the Template and Rules R9 placeholder, not a value. |

### OTHER:Recovery Workbench Quality measures v3 (Quality measures B7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02821 | RWB-P1-E1011-OPS | GAP-0276 |  | Timeliness reads: ACE batch complete when rwb-source-data reads it and publishes AceDataReady; other services measure the freshness contract; owner is P1 rwb-source-data. |

### RWB-P6-E1011-APP; OTHER:TSD P6 Communications v2; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02823 | RWB-P1-E1011-OPS | GAP-1172 |  | Carry the rwb-comms quality model (three tables, checks ACK and POD, one Schedule, two read operations) into the API Specification and schema folder at the next version. |

### OTHER:Functional Specification P1 (Screens table SCR-44; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02825 | RWB-P1-E1011-OPS | GAP-1514 |  | Serve job, freshness, reconciliation and dictionary operations from this service; composite route is edge's; dashboard shell is rwb-reporting's. |

### RWB-P3-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02826 | RWB-P1-E1011-OPS | GAP-2238 | 12.6 | Case-side reads, Schedule with SKIP and catch-up, cron set at deployment, three alert groups, flag rwb.p3.case-quality-run: already in its BR15; keep. |

### OTHER:04 User stories/Recovery Workbench Build Notes Epic 1 v6.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02827 | RWB-P1-E1011-OPS | GAP-3169 | 11 | In the RWB-E1-011 View note, replace 'the case exceptions' with the reconciliation breaks in reconciliation_result. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02828 | RWB-P1-E1011-OPS | GAP-3172 |  | State wave 1 delivery of rwb-asset in the service epic and wave plan; let the rwb-asset Arch v5 wave 2 govern its later stories. |

### OTHER:Business Requirements Document v4 section 3 headings (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02829 | RWB-P1-E1011-OPS | GAP-1457 |  | In a later BRD version, renumber section 3 headings by service epic, keeping every requirement key unchanged. |

### OTHER:P3 screen story for SCR-37 and SCR-44 (name Not specified in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02840 | RWB-P1-E1013-APP | DOR-RWB-P1-E1013-APP-10 | none | Add empty, loading, error and no-access states for SCR-37 and SCR-44. |

### OTHER:FSD P1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02841 | RWB-P1-E1013-APP | GAP-1499 | find it | Remove the lake write from A2.12 and A2.20 and the INT-19 extract and lake statement from A2.19; state reconciliation results and freshness as output served to rwb-reporting. Story BR9 already removes the lake. |

### RWB-P9-E6037-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02842 | RWB-P1-E1013-APP | GAP-2579 | none | Mark ASM-4251 to ASM-4254 confirmed: measure set, monthly step in first JOB-15 run after month close, month-end business_date key, SCR-37. Requirement ID still to be traced. |

### OTHER:Star schema workbook v3 (Facts; OTHER:Dimensions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02843 | RWB-P1-E1013-APP | GAP-0251 | find it | Redefine the nine fact tables as the rwb_reporting read model fed from service topics; serve GET /dashboards/{id} and GET /reports/{id} via gateway-bff; rebuild no lake or Power BI connection. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02844 | RWB-P1-E1013-APP | GAP-0255 | find it | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate; state queue measures stay with P3 rwb_case. |

### OTHER:Star schema workbook v3 (Dimensions; OTHER:Facts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02845 | RWB-P1-E1013-APP | GAP-0257 | find it | Key owner and team by ID on events and resolve display names from P3 queue_member and assignment behind the rwb-access masking policy; no personal data on any event. |

### RWB-P9-E1013-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02848 | RWB-P1-E1013-APP | GAP-2567 | none | Add the two rwb-source-data rows (payments read, freshness answer) to the wave dependency map. Keep the P9 metadata rows; its 12.2 declares the consumed reads with fakes. |

### RWB-P3-E1043-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02849 | RWB-P1-E1013-APP | GAP-2241 |  | Name the age-band list in the reference-data catalog with a list code and a table code, then use that code on the band read and the band list screen. Codes: Not specified in the source documents (GAP-2241). |

### OTHER:06 Data/Recovery Workbench Reporting and Analytics Data Model v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02850 | RWB-P1-E1013-APP | GAP-0252 | none | Facts refresh cells and Dimensions holiday and product rows: feed from the rwb-source-data contract and snapshot(page); no recovery.v_ace_* grant or direct read by P9. |

### OTHER:P1 OpenAPI document of the RWB-SVC-P1 contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02851 | RWB-P1-E1013-APP | GAP-0563 |  | Fix the readiness, status and payments paths, the freshness path, the 202 answer and the three status values; field names follow the P1 logical data model field IDs. Paths: Not specified in the source documents (GAP-0563). |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02852 | RWB-P1-E1013-APP | GAP-2239 | 12 | Publish GET /api/recovery/case/v1/cases/facts with businessDate, page and size, and confirm the operation at the next revision. Mark the path and field names provisional until then. |

### OTHER:project-context.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02860 | RWB-P1-E1013-APP | GAP-0016 | none | Replace the v2 Case volume and Staff rows with the v5 Volume and Scale Forecast v3 figures and retire the v2 rows. |

### OTHER:Version 3 facts, dimensions and measures workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02861 | RWB-P1-E1013-APP | GAP-0254 | none | Add Owner and Values from columns to Facts and Dimensions and an Owner column to Measures, each taken from the Ownership Map; read model in schema rwb_reporting. |

### OTHER:Technical Specification P1 (rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02863 | RWB-P1-E1013-APP | GAP-0564 | none | Add the gate pair COMPLETE and HOLD to the list of values in the next version; keep LOADED and STALE for the freshness stamp. |

### OTHER:rwb-case message catalogue; OTHER:Screen Specifications v1 (SCR-44) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02865 | RWB-P1-E1013-APP | GAP-2242 | 15 | Add one message for a held facts release to the rwb-case catalogue and define the SCR-44 release columns and the two counts. |

### OTHER:RWB-E1-034 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02882 | RWB-P1-E1015-APP | GAP-0357 | find it | Read the five template operations from the P6 contract in the registry; keep requests, responses, states and messages unchanged; leave the generation hold to the P6 notice workflow and RWB-E1-052. |

### OTHER:TSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02883 | RWB-P1-E1015-APP | GAP-0492 | 4 | Correct T3.6: DF-OPS-005 source_extracted_at from started_at; DF-OPS-006 loaded_at from completed_at. Story already reads this way. |

### RWB-P8-E2008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02887 | RWB-P1-E1015-APP | GAP-0599 | 12.1 | Publish the two reads on /api/recovery/source-data/v1 with resource names, businessDate query parameter, element names and status set; consume them from the OpenAPI fragment at contract freeze. |

### RWB-P1-E1015-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02889 | RWB-P1-E1015-APP | GAP-0494 | 7 | Carry the Schedule name pattern, the catch-up window and the deployment capacity as values; extend the catalog with the remaining products' expected_by values once the data steward confirms them. |

### OTHER:TSD T-A.2 (Job resource and run element) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02902 | RWB-P1-E1015-CON | GAP-2163 | find it | Fix a closed run status of PENDING, RUNNING, COMPLETE, FAILED, WAITING with one date per meaning and one row per attempt; state the freshness answer as owned by RWB-P1-E1015-CON with no field restated. |

### OTHER:RWB-E1-015 integration slice and RWB-ITG-W2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02905 | RWB-P1-E1015-CON | GAP-0340 |  | Assert JOB-02 and JOB-04 in wave 1; verify JOB-07 and JOB-08 start in RWB-ITG-W2; read the released case list from P1 case_list_row, not a lake copy. |

### OTHER:Technical Service Design P1 v3 (T3.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02906 | RWB-P1-E1015-CON | GAP-0492 |  | At its next version map source_extracted_at to started_at and loaded_at to completed_at for DF-OPS-005 and DF-OPS-006, matching FSD P1 A2.14 and the legacy values. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:EV-27) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02907 | RWB-P1-E1015-CON | GAP-1504 |  | Set both events to produced by rwb-source-data on rwb.source-data.events.v1; ACE ingestion is not a producer on a Recovery topic. |

### RWB-P7-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02909 | RWB-P1-E1015-CON | GAP-1265 |  | Add RWB-P1-E1015-CON and RWB-P3-E1018-CON as C rows, or record the two reads as route-level composites of RWB-PLT-N001-CON. |

### OTHER:Story dependencies v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02912 | RWB-P1-E1015-CON | GAP-3233 | none | Keep the five version 4 dependencies as rows with Status Not carried; add an X row only if the run books or the harness waits for the named story. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02914 | RWB-P1-E1015-OPS | CG-ALL-2135 | 12.5 | Add a Workflows row for AceIngestCheckWorkflow, task queue rwb-source-data, worker deployment of the release, as named in RWB-P1-E1015-OPS §12.5. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02918 | RWB-P1-E1015-OPS | DOR-RWB-P1-E1015-OPS-8 | find it | Publish the authorise path in rwb-access.yaml. Add AceIngestCheckWorkflow and checkDailyCompleteness to Temporal Catalog v1. |

### OTHER:RWB-ITG-W2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02924 | RWB-P1-E1015-OPS | GAP-0340 | find it | Verify JOB-07 and JOB-08 start (rwb-payment, P8) in the wave 2 integration tests |

### OTHER:Technical Solution Design P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02925 | RWB-P1-E1015-OPS | GAP-0492 | 11 | T3.6 rows DF-OPS-005 and DF-OPS-006: source_extracted_at from started_at; loaded_at from completed_at |

### OTHER:AsyncAPI document / platform owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02926 | RWB-P1-E1015-OPS | GAP-0493 | 11 | Envelope attributes, event key, registry subject and security scheme login are Not specified in the source documents (GAP-0493); AsyncAPI and the platform owner must supply them. |

### OTHER:rwb-source-data service API document (OpenAPI 3.1 fragment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02948 | RWB-P1-E1016-APP | GAP-0571 | find it | Publish GET /api/recovery/source-data/v1/entry-candidates with required businessDate and threshold, optional page and size, response EntryCandidatePage, and statuses 400, 401, 403, 409, 422 and 503. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02952 | RWB-P1-E1016-APP | GAP-0983 | 12 | Publish request and answer schemas of GET /admin/roles, GET /masking-policies and POST /authorise, with marker values, maskingExceptions part, both version fields and the access resolution the request carries. |

### OTHER:P3 screen specification (SCR-03 and SCR-47) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02961 | RWB-P1-E1016-CON | DOR-RWB-P1-E1016-CON-10 | none | Add empty, error and no-access states to SCR-03; add empty, loading, error and no-access states to SCR-47 |

### OTHER:Technical Specification P1 v3 (T3.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02965 | RWB-P1-E1016-CON | GAP-0481 | 12.7 | Remove the masking table from P1's schema; masking, role and permission tables stay with rwb-access per Ownership Map v1 |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02966 | RWB-P1-E1016-CON | GAP-2181 | 4 | DP02 row marked Not specified in the story text for members, vocabulary and consent rule. |

### OTHER:TSD P4 appendix T-A; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02971 | RWB-P1-E1016-CON | GAP-0983 |  | Publish request and answer schemas of GET /admin/roles, GET /masking-policies and POST /authorise, with marker values, maskingExceptions part, both version fields and access resolution. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; RWB-P5-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02972 | RWB-P1-E1016-CON | GAP-1028 | 7, 16 | Publish retention-classes GET operations with the shared RetentionClass shape of RWB-P5-AD021-CON; consume the P4, P3 and P1 operations with fakes; inherit guard library and gateway route from template. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02975 | RWB-P1-E1016-DB | DOR-RWB-P1-E1016-DB-22 | header | Publish the contract fake and record its library version for RWB-P1-E1016-CON. |

### OTHER:P3 screen SCR-44 (owning story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02978 | RWB-P1-E1016-DB | DOR-RWB-P1-E1016-DB-10 | 9 | Add empty, loading, error and no-access states to SCR-44. |

### OTHER:rwb-source-data service API document (OpenAPI 3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02980 | RWB-P1-E1016-DB | GAP-0571 | none | Publish GET /api/recovery/source-data/v1/entry-candidates with businessDate and threshold required, page and size optional; response EntryCandidatePage with businessDate, threshold, asOf, page, size, total, candidates[] and breaks[]; candidate elements named after the field they read; statuses 400, 401, 403, 409, 422, 503; access by the rwb-case service identity. |

### OTHER:Technical Specification P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02981 | RWB-P1-E1016-DB | GAP-0481 | 8 | Remove masking_rule from the P1 schema and V0001 (T3.6). P1 holds data_product_access only and takes the masking answer from POST /api/recovery/access/v1/authorise and FieldMasker of RWB-P4-E1037-CON, one hop, 2 s timeout. |

### OTHER:rwb-source-data service API document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02982 | RWB-P1-E1016-DB | GAP-0341 | 7 | Specify one catalog contract: the P1 catalog API composes P1 product, field and access rows; owner roles and masking resolved through P4 (rwb-access); retention class through the P5 contract; no service copies another service's table. |

### OTHER:rwb-case reference-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02983 | RWB-P1-E1016-DB | GAP-0483 | none | Add reference-data table code data_product_access as a load through the rwb-case contract, with a handler in rwb-source-data replacing DataProductAccessLoader; rwb-source-data exposes no load endpoint of its own. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02984 | RWB-P1-E1016-DB | GAP-3194 | 1 | Raise one ACE DB story per owning service without one (S2, S4, S5, S6, S7, P6, P8) for the DEF-05 column drop, or attach the drop to the APP story that creates the table; cite the chosen story on row 121 before wave 2 starts. |

### OTHER:TSD P4 appendix T-A and the OpenAPI file of rwb-access (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02988 | RWB-P1-E1016-DB | GAP-0983 | 7 | Publish request and answer schemas for GET /admin/roles, GET /masking-policies and POST /authorise, with marker values, the maskingExceptions part, both version fields and the access resolution the request carries. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02996 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-8 | find it | Rolls up 2181, 2182, 2183 and 2184. The +5 more detcheck items are not listed in the sources. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02997 | RWB-P1-E1017-APP | CG-ALL-2184 | 12.5 | Add activity validateRules with task queue rwb-source-data |

### OTHER:P3 story that owns SCR-47 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03004 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-10 | Not specified in the source documents (DOR-RWB-P1-E1017-APP-10) | Add empty, loading, error and no-access states for SCR-47 in the story that owns the screen |

### RWB-P1-E1001-APP; RWB-P1-E1017-OPS; RWB-P1-E1064-APP; RWB-PLT-TE012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03005 | RWB-P1-E1017-APP | DOR-RWB-P1-E1017-APP-17 | Header | Complete the four build dependencies that are not done yet |

### RWB-PLT-TE012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03008 | RWB-P1-E1017-APP | GAP-0490 | 8 | Publish the write-once container contract: account, credential scope, immutability policy, request shape and manifest schema. Story side: BR4 now states own credential and manifest read-back. |

### OTHER:ACE team, platform secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03012 | RWB-P1-E1017-APP | GAP-2430 | none | Allocate the rwb-decision database login for schema rwb_decision and record it in the platform secret store; the story keeps the phrase until then. |

### OTHER:v6 Sequence tracker (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03013 | RWB-P1-E1017-APP | GAP-3230 | none | Drop rows for RWB-E1-014 and RWB-TE-007 (Sequence items 19 and 21) at cutover, or keep them struck through as retired, not pulled. |

### OTHER:Story dependencies v5 (Dependency classes sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03014 | RWB-P1-E1017-APP | GAP-3234 | Header | Record on the check row X that platform technical-enabler work is team-type work, tracked and never blocking; keep X on the ten rows. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20812 | RWB-P1-E1013-APP | R-28487 |  | Held facts release message belongs to the rwb-case message catalogue; SCR-44 release columns belong to Screen Specifications v1. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0016 | Volumes differ between the v2 context and v5 | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0063 | Wave conflict S5 / EP01 | Tech lead | Resolved (directive) |
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
| GAP-0336 | Owner of REC-03 and REC-04 and the reporting delivery path of the two extracts are not named for the microservice target | Solution architect | Resolved (directive) |
| GAP-0337 | The connection matrix does not show the rwb-source-data outbound reads and the exclusion operation of the case contract is not named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0339 | E1013 integration path after the data-lake removal | Solution architect | Resolved (directive) |
| GAP-0340 | E1015 integration slice crosses the wave 2 payment service and the removed lake | Solution architect | Resolved (directive) |
| GAP-0341 | E1016 catalog composition across rwb-source-data, rwb-access and rwb-document | Solution architect | Resolved (directive) |
| GAP-0342 | E1017 retention ownership and the P1 interaction path | Solution architect | Resolved (directive) |
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0482 | The data_product_access seed of the version in force is only partly specified | Data steward | Resolved (directive) |
| GAP-0483 | The monolith reference-load endpoint has no target owner for an access load | Tech lead | Resolved (directive) |
| GAP-0484 | The DB slice of this legacy key cannot deliver the table DDL, because two other stories already create the tables | ACE database lead | Resolved (directive) |
| GAP-0488 | retention_rule ownership: TSD P1 v3 keeps it in P1, the Ownership Map and Arch v5 move retention to P5 | Solution architect | Resolved (directive) |
| GAP-0489 | The rwb-source-data retention-run contract shape is not specified | Solution architect | Resolved (directive) |
| GAP-0490 | The write-once archive contract (container, path and manifest) belongs to RWB-PLT-TE012-APP and is not specified | Solution architect | Resolved (directive) |
| GAP-0491 | The legal-hold query is a published interface with no REST path in the sources | Solution architect | Resolved (directive) |
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
| GAP-0571 | The entry-candidate contract: the resource and parameter names, the response entity, its field names, the paging, the error status set and the access rule are not fixed by any source, and this legacy key has no contract story of its own | Tech lead of rwb-source-data with the solution architect and the P3 owner of the case contract | Resolved (directive) |
| GAP-0594 | The shapes and property names of the two booking-fact reads are in no source document | Tech lead | Resolved (directive) |
| GAP-0597 | The batch-status answer has two values in the legacy interface and nine fields in the view, and no source fixes which of them it returns | Tech lead | Resolved (directive) |
| GAP-0599 | The two read operations, their resource and element names and their error status set are stated by no source, because the legacy read was an in-process Java interface with no path, no query parameter and no status code | Solution architect with the P8 contract owner | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0740 | The rwb-case slice of RWB-E1-011 leaves the check codes, the four operation paths, the call type to rwb-source-data, the case key columns, the Schedule cron, the access right, the login and every report value that only the data lake held unspecified | Solution architect, with the P1 rwb-source-data owner, the P3 rwb-case owner and the data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0983 | rwb-access policy and catalogue answers: no source names the request and answer field set of the role catalogue, the masking policy read or the data-product authorise answer, nor the marker vocabulary or the masking-exceptions part | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1028 | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1080 | The field names behind the rwb-source-data data-product contract are not specified | Solution architect | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1168 | RWB-P6-E1011-APP: the parameters and reference-data contracts of rwb-case and the rwb-source-data contract the run reads are missing from the story's C list | Solution architect | Resolved (directive) |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1170 | RWB-P6-E1011-APP: the data lake is removed, so the reconciliation and data quality extracts and the report built on them have no target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1171 | RWB-P6-E1011-APP: no event is published because DP-09 is not in the pattern set, and no operation of rwb-reporting or rwb-source-data accepts the quality facts | Solution architect | Resolved (directive) |
| GAP-1172 | RWB-P6-E1011-APP: the quality tables, the check codes, the run cadence and the two quality read operations are not named in any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1173 | RWB-P6-E1011-APP: the right of the quality reads is Platform administration R in the legacy story, and the rwb-comms RBAC matrix has no Platform administration column | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1499 | The data lake and the dashboard connection are removed, so the reporting destinations of three FSD features have no home | Solution architect | Resolved (directive) |
| GAP-1503 | The baseline measure job has two owners, one in the FSD and one in the architecture | Center of excellence | Resolved (directive) |
| GAP-1504 | The data-ready and data-late events have two directions and two owners in the source set | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1507 | No freshness source is named for the period before the ACE batch record exists | Solution architect | Resolved (directive) |
| GAP-1508 | The per-account reconciliation break rows have no store after the quality-exception table leaves the schema | Data architect | Resolved (directive) |
| GAP-1513 | The bank scheduler contract is a recommendation in the architecture, not an agreed interface | Solution architect with the bank platform team | Resolved (directive) |
| GAP-1514 | The job monitor and data-quality screens are first-in here and owned by reporting in the architecture | Solution architect | Resolved (directive) |
| GAP-1646 | The data lake and the Power BI connection are removed but the whole reporting FSD is built on them | Solution architect | Resolved (directive) |
| GAP-1649 | The measure set is six definitions in one acceptance criterion and seven measures in another | Tribe lead with the Reporting and BI analyst | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2163 | RWB-AD-018: the contract baseline has no field-level detail for the run element and its boundary with the freshness resource is not written down | P1 tech lead with the solution architect | Resolved (directive) |
| GAP-2181 | The DP02 contact-and-consent row, the consent vocabulary, the members of the letter append and the unserved status are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2228 | The target form of the case list is not fixed by any source: the row shape, the account-data owner in the read path, the freshness stamp, the removal of the lake path and the ownership of the reconciliation | Solution architect | Resolved (directive) |
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
| GAP-2426 | The decision code, final call, action and outcome values and the payload placement of an archive or purge record are in no source | Solution architect | Resolved (directive) |
| GAP-2427 | The text of MSG-P7-009 and the ids and texts of the not-found answer, the chain-break report and the collection gap alert are not written in any source | Business analyst, P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2428 | The JOB-14 timezone, page size, overlap and catch-up values, the property names and the behaviour of the feature flag when off are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2430 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2431 | The story file at the Work Package path already existed as a partial artefact of the superseded Work Package B-P7-05, with no fragment, no register rows and citations that resolve to nothing | Delivery lead, with the traceability owner | Resolved (directive) |
| GAP-2432 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept | Traceability owner | Resolved (directive) |
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
| GAP-3154 | No service owns each of the 14 data products, so the freshness stamp has no owner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3158 | The retention tables are P1 tables in the story and P5 tables in the Ownership Map | P5 document owner | Resolved (directive) |
| GAP-3169 | The reconciliation story writes 'the case exceptions' without naming a table | P1 data owner | Resolved (directive) |
| GAP-3172 | Service S5 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3230 | Two retired items still carry v6 windows and dependencies | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3234 | Ten class X rows point at a platform application story rather than at a DB, INF or OPS story | TechX (platform) | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P1-E1013-APP | skipped AC ID | 99 | missing: AC8 |
| RWB-P1-E1015-APP | skipped AC ID | 115 | missing: AC1, AC2, AC4, AC5, AC6, AC7, AC9, AC10, AC11 |
| RWB-P1-E1015-CON | skipped AC ID | 92 | missing: AC7, AC8 |
| RWB-P1-E1015-OPS | skipped AC ID | 96 | missing: AC7, AC8 |
