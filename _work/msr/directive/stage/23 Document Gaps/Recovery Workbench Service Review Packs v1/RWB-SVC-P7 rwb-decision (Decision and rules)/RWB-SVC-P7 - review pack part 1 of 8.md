# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 1 of 8 (RWB-P7-E1001-APP to RWB-P7-E1017-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 113 |
| Cross-document (pending in another document) | 174 |
| Not applied (value not in the sources) | 31 |
| Open business decisions | 19 |
| Register gaps linked | 96 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-E1001-APP | 27 | 55 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1001 APP Recovery tables for the 14 data products v2.md |
| RWB-P7-E1008-APP | 20 | 28 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1008 APP Decision log store v1, append only and hash chained v2.md |
| RWB-P7-E1008-CON | 20 | 22 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1008 CON Decision log store v1, append only and hash chained - contract v2.md |
| RWB-P7-E1008-DB | 22 | 19 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1008 DB Decision log store v1, append only and hash chained - ACE DB v2.md |
| RWB-P7-E1008-OPS | 10 | 31 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1008 OPS Decision log store v1, append only and hash chained - deployment v2.md |
| RWB-P7-E1017-APP | 14 | 11 | 10 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1017 APP Retention and archive rule for the data store v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1008-ITG, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS | R-09175 | GAP-1225 | Register gap | Solution architect with the decision-center product owner | How nineteen local record chains become one central chain is not specified | Fix the rule as: the ledger recomputes entry_hash on the legacy canonical form (BR4) over the stored columns, orders by the ingest commit under the chain lock, and preserves the local chain sequence and hash on the row for reconciliation; then publish it in RWB-P7-E1008-CON. |
| RWB-P7-E1001-APP | R-11148 | CG-ALL-6816 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1008-APP | R-11157 | CG-ALL-6835 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1008-CON | R-11160 | CG-ALL-6847 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1008-DB | R-11164 | CG-ALL-6856 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1008-OPS | R-11170 | CG-ALL-6867 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1017-APP | R-11173 | CG-ALL-6875 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21843 | GAP-0001 | Register gap | Product Owner | Arch v5 waves have no release dates | Keep the dates unchanged and tentative, map waves 0-1 to Release 1 at the plan gate, and confirm the mapping in the verification loop |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21856 | GAP-0977 | Register gap | Data steward and data product owner (RW-DATASTEW) | The dictionary rows of the five rwb_access tables have no seeding owner after the split | Declare the 44 business rows as a build artefact of this story, hand the declaration to the one dictionary's seed in rwb_source_data, and let the seed carry the 35 standard-column rows under its own Field IDs. Cite the 44 business Field IDs only. |
| RWB-ITG-E1008-ITG, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS | R-21897 | GAP-0003 | Register gap | RW-RISK and Internal Audit | ADR-009 central log versus local record plus central ledger | Adopt RecordAndApply plus the central ledger and seal the change in ADR-022 after the Audit sign-off |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P7-E1017-APP | R-21967 | GAP-2070 | Register gap | Service owners P7 rwb-decision, P1 rwb-source-data and P4 rwb-access with Compliance | Where the retention period of the ledgers and the access log is held, and which job enforces it | Keep every period as written and mark the owner open: P7 enforces the ledger period, P1 the interaction ledger and P4 the access log, each as a row of its own retention data, until Compliance states where the periods are held. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21971 | GAP-1500 | Register gap | Compliance and PDPA officer | The retention rule table and the archive job move to the document service, while the FSD keeps both here | This service declares the retention class per data product and recovery table as versioned reference data, refuses a rule that names a read-only ACE view or the decision log, and archives nothing itself; the rule table and the monthly archive run belong to rwb-document. Confirm with Compliance that a class declared here and applied there is acceptable for the PDPA position. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1027-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-28460 | GAP-2067 | Register gap | Document owner of the audit and logging design | The source reads version 1 in its metadata table and v2 in its file name | Take the file name as the family version, so this document becomes version 3, and keep the source values in a 'Source version' row: 1, 28 October 2026. The change log carries both readings. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-28498 | GAP-1618 | Register gap | Compliance and PDPA officer | The decision log and the ledger carry no retention period, and the WORM seal period is unstated | Set the decision-log class period and the seal period under DL26 before the first release, keep the class per record class in reference data, and state in the retention rule that no archive runs inside this service. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-P7-E1008-APP | R-37362 | ASM-2189 | Register assumption |  | The central chain is built by recomputing entry_hash on the legacy canonical form (BR4) over the stored columns, appending under one advisory lock in ingest commit order, and keeping the local chain sequence and hash on the row for reconciliation. | The solution architect signs the rule off before the golden hash vectors of the ledger are frozen. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-E1001-APP | R-01755 | CG-ALL-6811 | 8 | rwb-decision.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data | Ruling: Reference Data v5 closed list governs, so the rwb-decision.yaml approvalLevel enum stays. The LOV-APPROVAL-LEVEL sentence sits outside this chunk, so it cannot be edited here. |
| RWB-P7-E1001-APP | R-01756 | CG-ALL-6812 | 8 | rwb-decision.yaml holds status as a closed enum while the story reads LOV-APPROVAL-STATUS as data | Ruling: Reference Data v5 closed list governs, so the rwb-decision.yaml status enum stays. The LOV-APPROVAL-STATUS sentence sits outside this chunk, so it cannot be edited here. |
| RWB-P7-E1001-APP | R-06620 | DOR-RWB-P7-E1001-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in the story or sources. Sign-off needs the epic design record, which is not provided: Not specified in the source documents (DOR-RWB-P7-E1001-APP-14). |
| RWB-P7-E1001-APP | R-06621 | DOR-RWB-P7-E1001-APP-16 | Header | Definition of Ready item 16 Size: Fail | Size is set by the squad at refinement and no value is in the sources, so the placeholder is used. |
| RWB-P7-E1001-APP | R-06625 | DOR-RWB-P7-E1001-APP-8 |  | Definition of Ready item 8 Contract: Fail | Depends on CG-ALL-6811 and CG-ALL-6812. Yaml enums stay under the closed-list ruling; the contract finding clears only after the LOV wording outside this chunk changes. |
| RWB-P7-E1001-APP | R-17856 | DOR-RWB-P7-E1001-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR3 already cites AC11. BR9 has no AC or TC row yet; sections 7 and 16 are outside this chunk, so no safe edit is possible. |
| RWB-P7-E1001-APP | R-28436 | GAP-2062 |  | No per-topic sizing exists for the 19 topics; one topic is sized in the architecture | Call-type and change-table sections are outside this chunk. Per-topic partition counts: Not specified in the source documents (GAP-2062). The change log says this story publishes no event. |
| RWB-P7-E1008-APP | R-06626 | DOR-RWB-P7-E1008-APP-14 | not located | Definition of Ready item 14 Epic design: Fail | No signed epic design record in 03 Requirements (searched for epic design record or sign-off) or in the story. Not specified in the source documents (DOR-RWB-P7-E1008-APP-14). |
| RWB-P7-E1008-APP | R-17859 | DOR-RWB-P7-E1008-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Screen Specifications v1.md SCR-38 (line 1402) lists only Loading, results, export. Empty, error and no-access states are not specified. Section 10 is not in this chunk. |
| RWB-P7-E1008-APP | R-17860 | DOR-RWB-P7-E1008-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | SCR-38 field table (Screen Specifications v1.md line 1404) marks all decision_log_entry fields Personal data No. The story field list is not in this chunk. Not specified in the source documents (DOR-RWB-P7-E1008-APP-11). |
| RWB-P7-E1008-APP | R-17864 | DOR-RWB-P7-E1008-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | New AC for BR7 to BR10 (section 7) and their TC rows (section 16) need those sections, which are not in this chunk, so the IDs cannot be anchored. |
| RWB-P7-E1008-APP | R-26179 | CG-ALL-6833 | 14 | MSG-GEN-006 text differs from the Error and Message Standard v4 | R-17867 found the English text identical to Error and Message Standard v4; the supplied replacement text is not in the sources. Business analyst to confirm. |
| RWB-P7-E1008-APP | R-26181 | CG-ALL-6836 | 12.5 | Criteria and tests keep legacy job and decision-log wording | The legacy JOB-nn, decision log and job record lines are AC8 and its test rows in sections 7 and 16, which are not in this chunk and cannot be matched exactly. |
| RWB-P7-E1008-APP | R-28461 | GAP-2075 | 3, 4 | The record that governs while the central ledger lags by up to five minutes | Audit search and strict-mode wait behaviour belong in sections 3 and 4, which are not in this chunk. Resubmit with those sections so the text can be anchored. |
| RWB-P7-E1008-CON | R-06632 | DOR-RWB-P7-E1008-CON-14 | find it | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off for RWB-P7-E1008 in the sources. Decision Log v11 DT05 is a process rule only. Left unchanged. |
| RWB-P7-E1008-DB | R-26192 | CG-ALL-6857 | 3 | Flyway file V_E1_008__declog_chain.sql is not in the V0001..Vnnnn form | The file name V_E1_008__declog_chain.sql is not in the supplied story parts, so no exact old text exists. The next free number of the rwb-decision sequence is not in the sources. Grep found no match in the project. |
| RWB-P7-E1008-DB | R-26193 | CG-ALL-6858 | 3 | Story cites document versions that are not the highest | The Physical Schema v6 citation is not in the supplied story parts, so no exact old text exists. Grep found no match for it in the project. Needs the full story text. |
| RWB-P7-E1008-DB | R-31416 | NEWAC-RWB-P7-E1008-DB-AC9 | 7 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in the supplied story parts, so the new AC9 and its TC row cannot be anchored. The proposed test is Not specified in the source documents. |
| RWB-P7-E1008-OPS | R-06641 | DOR-RWB-P7-E1008-OPS-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the source documents (03 Requirements and specifications, no sign-off text). A reference cannot be stated without inventing one; left open. |
| RWB-P7-E1008-OPS | R-17889 | DOR-RWB-P7-E1008-OPS-10 | 15 | Definition of Ready item 10 Screens and states: Partial | SCR-44 appears in the P1 FSD (Recovery data engine v3.md, line 1421) with no empty, loading, error or no-access states. Section 15 text is outside this chunk. |
| RWB-P7-E1008-OPS | R-21903 | GAP-1234 |  | No RPO, RTO or restore-verification standard exists for an append-only ledger | No RTO is stated in the sources; Gap Register v1 GAP-3246 records RPO and RTO per service as not stated. Section 12 is outside this chunk, so the RPO and gate text cannot be placed. |
| RWB-P7-E1017-APP | R-06647 | DOR-RWB-P7-E1017-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the project sources (search by record name and sign-off terms). Sign-off cannot be confirmed; no value invented. |
| RWB-P7-E1017-APP | R-06648 | DOR-RWB-P7-E1017-APP-16 | header | Definition of Ready item 16 Size: Fail | No size in any source; the row records the gap and asserts no process. |
| RWB-P7-E1017-APP | R-06650 | DOR-RWB-P7-E1017-APP-22 | header | Definition of Ready item 22 Fake published: Fail | Fake library version is in no source, the same gap as DOR-23; the gap is stated only. |
| RWB-P7-E1017-APP | R-06651 | DOR-RWB-P7-E1017-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Version is in no source, so the item is not resolved; the gap is stated only. |
| RWB-P7-E1017-APP | R-11171 | CG-ALL-6870 | 4, 12.1 | HTTP errors with no message ID: 401 no session; 404 no entry (id Not specified, GAP-2427 | Error and Message Standard v4 is not in the project sources, so no 401 or 404 message ID can be copied. Business analyst to confirm; placeholders stay. |
| RWB-P7-E1017-APP | R-26197 | CG-ALL-6873 | 16 | Test cases cover other criteria in Test Cases v8 | Story has no AC9 (skipped AC ID); the Covers change is reverted, not applied. |
| RWB-P7-E1017-APP | R-26199 | CG-ALL-6876 | 3, 3.1 | Flyway file V1017_1__decision_archive_records.sql is not in the V0001..Vnnnn form | The next number in the rwb-decision Flyway sequence is not in the sources. Not invented; the solution architect supplies it. |
| RWB-P7-E1017-APP | R-28499 | GAP-2427 | 14 | The text of MSG-P7-009 and the ids and texts of the not-found answer, the chain-break report and the collection gap alert are not written in any source | The texts of MSG-P7-009, the not-found answer, the chain-break report and the gap alert are in no source. Placeholders stay until the P7 business analyst writes them. |
| RWB-P7-E1017-APP | R-28500 | GAP-2428 | 3 | The JOB-14 timezone, page size, overlap and catch-up values, the property names and the behaviour of the feature flag when off are in no source | Invented values Asia/Bangkok, 5000 and one run at a time removed; the gap is stated only. |
| RWB-P7-E1017-APP | R-28502 | GAP-2431 |  | The story file at the Work Package path already existed as a partial artefact of the superseded Work Package B-P7-05, with no fragment, no register rows and citations that resolve to nothing | A full rewrite of the story file is a producing Work Package task outside this chunk. No B-P7-05 citation appears in the chunk text to remove. |

## 5. Cross-document changes (pending in the target document)


### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11541 | RWB-P7-E1001-APP | GAP-0100 | find it | List each operation under its owning service with its Architecture v5 base path; leave the final path and payload to API Specification v5. |
| CDC-11542 | RWB-P7-E1001-APP | GAP-0107 | find it | Derive the 48 cuts from sheet Tables, keeping a foreign key only when both tables share an owner; otherwise the column stays uuid; record the 48 rows in the README and the ERD. |
| CDC-11543 | RWB-P7-E1001-APP | GAP-0109 |  | Set the schema of outbox_event, outbox_delivery, processed_event and idempotency_key to each owning service schema (19 files); feature_flag and feature_flag_change to rwb_integration. |
| CDC-11544 | RWB-P7-E1001-APP | GAP-0206 |  | Add the data rows for the 48 table-to-table cuts with business-key columns; keep the 11 v_ace_* references as business keys; show all three cases per row. |
| CDC-11545 | RWB-P7-E1001-APP | GAP-0210 |  | Give the eleven ACE entity fields target schema rwb_source_data and owner P1 via rwb-source-data; add party_ext, contact_point_ext, account_ext and valuation_ext as Workbench targets. |
| CDC-11548 | RWB-P7-E1001-APP | GAP-0225 |  | Record S2 as owner of the live DP04 treatment record, with S3 (guarantee_claim) and P1 (dp_treatment, dp_guarantee_claim) named in the basis cell; split DP04 at next LDM revision if required. |
| CDC-11549 | RWB-P7-E1001-APP | GAP-0228 |  | Add the rwb_valuation tables (valuation, route decision, route agent output) owned by S1 and record S1 as owner of DP11 route economics. |
| CDC-11565 | RWB-P7-E1001-APP | GAP-0108 | none | Give rwb-valuation a local table assignment (S1) or keep valuation_ext in P1 and route economics in ACE; add rwb_valuation.sql (schema, platform library objects, note); read ACE through the rwb-source-data contract until a TSD adds a local table. |
| CDC-11570 | RWB-P7-E1001-APP | GAP-0202 |  | Give all 30 recovery.v_ace_* views owning service P1 and target schema 'recovery (ACE, read-only view)' per Architecture v5, and add a Views sheet to the map. |
| CDC-11574 | RWB-P7-E1001-APP | GAP-0226 |  | Record S5 as owner of the Workbench asset data set (asset_sale, listing); keep ACE collateral and valuation as a P1 read and valuation_ext as P1. |
| CDC-11575 | RWB-P7-E1001-APP | GAP-0227 |  | Record S4 as owner of the Workbench legal data set; keep ACE court records as a P1 read and notice and proof of delivery as P6. |
| CDC-11576 | RWB-P7-E1001-APP | GAP-0229 |  | Record P8 as owner of the proceeds and matching data set; write_off stays S7; ACE payment and gl_write_off records stay a P1 read. |
| CDC-11577 | RWB-P7-E1001-APP | GAP-0230 |  | Record P1 as owner of the interaction ledger and efs_ledger_outcome. Notice, template and merge_field stay P6. Case timeline stays a P3 read through the P1 contract. |
| CDC-11578 | RWB-P7-E1001-APP | GAP-0231 |  | Record P3 as owner of parameter_catalog, parameter_value, lov_value, reference_row and reference_version. Roles, permissions, masking_rule and delegation_limit stay P4. Templates and merge_field stay P6. |
| CDC-11584 | RWB-P7-E1001-APP | GAP-2132 |  | Let the Ownership Map sheet Tables govern ownership for all 93 tables. Keep the 92 and 4 of version 3 as printed. Counts reconcile in the per-service DB stories. |
| CDC-11643 | RWB-P7-E1008-DB | GAP-1224 |  | Confirm ingest of rwb.decision-record.v1 as the only writer of decision_log_entry, declare no append operation, and remove POST /decision-log from RWB-P7-E2028. Any write path needs the Ownership Map first. |
| CDC-11671 | RWB-P7-E1008-OPS | GAP-1224 | find it | Confirm the rwb.decision-record.v1 ingest as the only writer of decision_log_entry; remove POST /decision-log from E2028; add any service write path to the Ownership Map first. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11533 | RWB-P7-E1001-APP | CG-ALL-6807 | 5, 8, 9, 12.6, 13 | Record `tr_declog_append_only` as a trigger object on decision_log_entry, or use its dictionary name; the story keeps the trigger name. |
| CDC-11534 | RWB-P7-E1001-APP | CG-ALL-6808 | 5 | Record `insufficient_privilege` as the database refusal of the rwb_* logins, as the object AC7 and X5 name. |
| CDC-11535 | RWB-P7-E1001-APP | CG-ALL-6809 | 11 | Record `v_data_dictionary` as the dictionary view it names, or map it to data_contract if they are one object. |
| CDC-11552 | RWB-P7-E1001-APP | GAP-1280 | 12 | Correct rule_row to the 21 fields its fields sheet lists; remove rule_test_case.package_version_id; keep approval.case_id and approval.delegation_limit_id as values with no foreign key. |
| CDC-11555 | RWB-P7-E1001-APP | GAP-2401 | none | Correct rule_row to 21 fields per its fields sheet, remove rule_test_case.package_version_id, and keep approval.case_id and approval.delegation_limit_id as values with no foreign key. |
| CDC-11618 | RWB-P7-E1008-CON | CG-ALL-6839 | find it | Record ce_type as the CloudEvents binding attribute of the DecisionRecorded envelope, or name the dictionary field it maps to. |
| CDC-11619 | RWB-P7-E1008-CON | CG-ALL-6840 | find it | Record ce_id as the CloudEvents id binding attribute and its storage as idempotency_key, or name the dictionary field it maps to. |
| CDC-11659 | RWB-P7-E1008-OPS | CG-ALL-6859 | header | Record flyway_schema_history as a Flyway library table (object outside the dictionary) in the owning document. |
| CDC-11660 | RWB-P7-E1008-OPS | CG-ALL-6860 | header | Record ce_id as a named object in the owning document, or confirm the dictionary field name (nearest: case_id). |
| CDC-11661 | RWB-P7-E1008-OPS | CG-ALL-6861 | header | Record ce_type as a named object in the owning document, or confirm the dictionary field name (nearest: source_type). |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11532 | RWB-P7-E1001-APP | GAP-0012 | find it | Record creation of 19 schemas and 19 logins on the ACE PostgreSQL server in wave 0, with the per-login PgBouncer connection cap set with the ACE DBA. Cap value: Not specified in the source documents (GAP-0012). |
| CDC-11560 | RWB-P7-E1001-APP | GAP-2061 | none | Add a per-service availability table of 19 rows applying the same two targets, state one service shape repeated, and state a composed screen as the product of its called services within the one-hop budget. |
| CDC-11608 | RWB-P7-E1008-APP | GAP-1230 | n/a | Keep /decision-log as the published path; correct slide 14 (GET /decisions?caseId=) and slide 41 (first API path /decisions) in the next version. |
| CDC-11632 | RWB-P7-E1008-CON | GAP-1230 |  | Correct the rwb-decision read path to /decision-log in the next architecture version; /decision-log stays the published path. |
| CDC-11651 | RWB-P7-E1008-DB | GAP-1230 | find it | Correct the rwb-decision read path from /decisions to /decision-log in the next architecture version. |
| CDC-11669 | RWB-P7-E1008-OPS | GAP-2074 | find it | State that each service chains its records in chain_seq order, the ledger chains entries on ingest, the daily WORM fingerprint covers the ledger chain, and the ledger is the chain of record with the local chain for replay. |
| CDC-11672 | RWB-P7-E1008-OPS | GAP-1226 | find it | Withdraw FEAT-DRI-06 and its lake acceptance criteria; keep JOB-13 as continuous ingest and JOB-14 as the 02:00 chain check with WORM seal; record RWB-E1-014 retirement as delivered by the ledger. |
| CDC-11680 | RWB-P7-E1008-OPS | GAP-2075 | find it | Audit search reads the ledger only and shows an entry as not yet sealed until JOB-13 has collected it; strict mode waits for the ledger acknowledgement of its own record, reached through the owning service contract. |
| CDC-11681 | RWB-P7-E1008-OPS | GAP-1230 | find it | Correct slide 14 (GET /decisions?caseId=) and slide 41 (first API path /decisions) to /decision-log, the published path. |

### RWB-PLT-E1027-CON (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11594 | RWB-P7-E1008-APP | CG-ALL-6824 | 4, 9, 12.8 | Record ce_type as a CloudEvents attribute of the DecisionRecorded envelope, or add it to the dictionary. |
| CDC-11595 | RWB-P7-E1008-APP | CG-ALL-6825 | 4 | Record ce_specversion as a CloudEvents attribute of the DecisionRecorded envelope, or add it to the dictionary. |
| CDC-11596 | RWB-P7-E1008-APP | CG-ALL-6826 | 4, 5, 9, 11, 12.3, 12.8 | Record ce_id as a CloudEvents attribute of the DecisionRecorded envelope, or add it to the dictionary. |
| CDC-11598 | RWB-P7-E1008-APP | CG-ALL-6828 | 12.3, 12.4 | Record ce_source as a CloudEvents attribute of the DecisionRecorded envelope, or add it to the dictionary. |
| CDC-11610 | RWB-P7-E1008-APP | GAP-0984 | n/a | Publish decision_record column set, physical types and canonical-form rule; also add DECISION_LOG to TSD P4 RBAC matrix, fix per-service login names in platform DB story, and state local verifier behaviour in Temporal and Drools design. |
| CDC-11624 | RWB-P7-E1008-CON | GAP-2068 | 12.7 | Each service creates its local decision-record table in its own schema through the decision-record library, with the target field list; case reference and trace ID in inputsRef; name and DDL set in each DB story. |
| CDC-11634 | RWB-P7-E1008-CON | GAP-0984 |  | Publish the decision_record column set, physical types and canonical form there; add DECISION_LOG to the TSD P4 RBAC matrix; fix per-service login names in the platform DB story; state local verifier behaviour in Temporal and Drools design. |
| CDC-11654 | RWB-P7-E1008-DB | GAP-0984 | find it | Publish the decision_record column set, types and canonical-form rule; add DECISION_LOG to the TSD P4 RBAC matrix; fix per-service login names; state the Temporal and Drools verifier behaviour. |
| CDC-11684 | RWB-P7-E1008-OPS | GAP-0984 | find it | Publish the decision_record column set, physical types and canonical-form rule; add DECISION_LOG to the TSD P4 RBAC matrix; fix per-service login names in the platform DB story; state verifier behaviour in the Temporal and Drools design. |

### RWB-P7-E1008-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11589 | RWB-P7-E1008-APP | DOR-RWB-P7-E1008-APP-21 | n/a | Bring the build status to Done; it is currently Not started. |
| CDC-11590 | RWB-P7-E1008-APP | DOR-RWB-P7-E1008-APP-22 | n/a | Publish a contract fake library version and record it as published. |
| CDC-11638 | RWB-P7-E1008-DB | DOR-RWB-P7-E1008-DB-21 | n/a | Build and publish the contract story so its build status is Done. |
| CDC-11639 | RWB-P7-E1008-DB | DOR-RWB-P7-E1008-DB-22 | n/a | Publish a contract fake library version and record it as published. |
| CDC-11645 | RWB-P7-E1008-DB | GAP-1227 |  | Adopt GET /api/recovery/decision/v1/decision-log/{entryId} (200 once sealed) as the strict-mode confirmation, plus the sealed-entry announcement on rwb.decision-record.v1; publish both in the contract and the harness. |
| CDC-11656 | RWB-P7-E1008-OPS | DOR-RWB-P7-E1008-OPS-21 | header | Build status must reach Done before this story starts; it is currently Not started. Story now names it as the contract dependency. |
| CDC-11658 | RWB-P7-E1008-OPS | DOR-RWB-P7-E1008-OPS-23 | header | Publish the fixed contract version this story builds against; the source documents give only the /v1 path. |
| CDC-11673 | RWB-P7-E1008-OPS | GAP-1227 | find it | Adopt GET /api/recovery/decision/v1/decision-log/{entryId} returning 200 once sealed as the confirmation, plus the sealed-entry announcement on rwb.decision-record.v1; publish both in CON and the harness. |

### RWB-P7-E1008-DB (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11592 | RWB-P7-E1008-APP | CG-ALL-6822 | 2, 5, 8, 13 | Record trigger tr_declog_append_only and its owner in the DB story, or use the LDM dictionary name. |
| CDC-11593 | RWB-P7-E1008-APP | CG-ALL-6823 | 2 | Record function refuse_change and its owner in the DB story, or use the LDM dictionary name. |
| CDC-11597 | RWB-P7-E1008-APP | CG-ALL-6827 | 4 | Record decision_log_chain and its object in the DB story, or use the LDM dictionary name. |
| CDC-11600 | RWB-P7-E1008-APP | GAP-2068 | 11 | Each service creates its local decision-record table in its own schema through the library, with the target field list, and carries the case reference and trace ID in inputsRef. Name and DDL go in each DB story. |
| CDC-11662 | RWB-P7-E1008-OPS | CG-ALL-6862 | 4, 7 | Record trigger tr_declog_append_only and its object in the owning document, or use the dictionary name |
| CDC-11663 | RWB-P7-E1008-OPS | CG-ALL-6863 | 4, 7 | Record function refuse_change and its object in the owning document, or use the dictionary name |
| CDC-11685 | RWB-P7-E1008-OPS | GAP-1228 | 18 | DP-09 object creation noted against the DB story only. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11561 | RWB-P7-E1001-APP | CG-ALL-6815 | 18 | Align the REQ-RDF-001 and REQ-RDF-014 test lists in RTM v7 to the TC-E1-001-xx cases of RWB-P7-E1001-APP section 16; the story's section 18 already lists its own cases. |
| CDC-11606 | RWB-P7-E1008-APP | CG-ALL-6834 | 18 | Align the test trace of REQ-DRI-001 and the other requirements listed in the script gap with section 18 of RWB-P7-E1008-APP; REQ-DRI-001 lists TC-E1-008-03 in the story and TC-E1-008-01 and TC-E1-008-04 in the RTM. |
| CDC-11628 | RWB-P7-E1008-CON | CG-ALL-6846 | 18 | Align the traced test lists for the three differing requirements with RWB-P7-E1008-CON section 18 in the next version. |
| CDC-11648 | RWB-P7-E1008-DB | CG-ALL-6855 | 18 | Align the test lists for REQ-DRI-001 and the other two requirements with RWB-P7-E1008-DB section 18 in the next RTM version. |
| CDC-11676 | RWB-P7-E1008-OPS | CG-ALL-6866 | 18 | Align the REQ-DRI-001 test list and the other requirements' trace with section 18 of RWB-P7-E1008-OPS in the RTM next version. |
| CDC-11695 | RWB-P7-E1017-APP | CG-ALL-6874 | 18 | Align the REQ-RDF-013 test list with section 18 (TC-E1-017-01 to TC-E1-017-12) in the next RTM version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11587 | RWB-P7-E1008-APP | CG-ALL-6829 | 12.2 | Publish GET /api/recovery/case/v1/admin/lists/LOV-DECISION through the provider RWB-P3-E1043-CON, or the consumer uses a published operation. |
| CDC-11588 | RWB-P7-E1008-APP | CG-ALL-6830 | 12.2 | Publish GET /api/recovery/case/v1/admin/lists/LOV-APPROVAL-LEVEL through the provider RWB-P3-E1043-CON, or the consumer uses a published operation. |
| CDC-11591 | RWB-P7-E1008-APP | DOR-RWB-P7-E1008-APP-8 | 12.2 | Publish the two LOV paths (/admin/lists/LOV-DECISION and /admin/lists/LOV-APPROVAL-LEVEL); the topic is fixed in the story. |
| CDC-11615 | RWB-P7-E1008-CON | CG-ALL-6841 | 12.2 | Publish GET /api/recovery/case/v1/admin/lists/LOV-DECISION in rwb-case.yaml, or the consumer uses a published operation. |
| CDC-11616 | RWB-P7-E1008-CON | CG-ALL-6842 | 12.2 | Publish GET /api/recovery/case/v1/admin/lists/LOV-APPROVAL-LEVEL in rwb-case.yaml, or the consumer uses a published operation. |
| CDC-11617 | RWB-P7-E1008-CON | DOR-RWB-P7-E1008-CON-8 | 12.2 | Publish GET /api/recovery/case/v1/admin/lists/LOV-DECISION and GET /api/recovery/case/v1/admin/lists/LOV-APPROVAL-LEVEL (CG-ALL-6841, CG-ALL-6842). |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11536 | RWB-P7-E1001-APP | CG-ALL-6813 | 16 | Add a row for TC-E1-001-12 to Story test cases in the next version, with Given, When and Then copied from AC1, AC7 and BR1. |
| CDC-11627 | RWB-P7-E1008-CON | CG-ALL-6845 | 16 | Add rows for TC-P7-E1008-CON-01 to -06 with Given, When and Then copied from the criterion each covers. |
| CDC-11647 | RWB-P7-E1008-DB | CG-ALL-6854 |  | Add rows TC-P7-E1008-DB-01 to TC-P7-E1008-DB-07 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-11675 | RWB-P7-E1008-OPS | CG-ALL-6865 | 16 | Add rows TC-P7-E1008-OPS-01 to TC-P7-E1008-OPS-08 with Given, When and Then copied from the criterion each covers. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11599 | RWB-P7-E1008-APP | DOR-RWB-P7-E1008-APP-6 | 10 | Add role SY-DATALOAD, which section 10 of this story uses, to the role list. |
| CDC-11620 | RWB-P7-E1008-CON | DOR-RWB-P7-E1008-CON-1 | 1 | Add the role 'contract owner of rwb-decision' as a role code or role name, or name the existing role it maps to. |
| CDC-11640 | RWB-P7-E1008-DB | DOR-RWB-P7-E1008-DB-1 | n/a | Add the role 'ACE database engineer' as a role code or name, or map the story role to an existing role. |
| CDC-11664 | RWB-P7-E1008-OPS | DOR-RWB-P7-E1008-OPS-1 | 1 | Add role 'DevOps engineer of the platform' or record its role code so the §1 role resolves |

### parameter-catalog.csv (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11607 | RWB-P7-E1008-APP | GAP-1617 | 8 | Add three reference-data rows: ledger completeness target = 5 minutes; gap alert threshold = 5 minutes (Architecture v5 slide 28); strict-mode maximum wait = Not specified in the source documents (GAP-1617), to be confirmed with Risk and Internal Audit at the ADR-022 sign-off. |
| CDC-11630 | RWB-P7-E1008-CON | GAP-1617 | 4 | Completeness target and alert threshold marked Not specified; five-minute lag kept from GAP-2075 |
| CDC-11679 | RWB-P7-E1008-OPS | GAP-1617 | find it | Add the completeness target as 5 minutes and the gap alert threshold as 5 minutes; the strict-mode wait bound is Not specified in the source documents until ADR-022 sign-off with Risk and Internal Audit. |
| CDC-11682 | RWB-P7-E1008-OPS | GAP-1233 | 18 | Values not added; consumer group, alert threshold, verification job time and immutable-storage path marked Not specified. |

### RWB-P7-E2005-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11609 | RWB-P7-E1008-APP | GAP-1229 | n/a | Carry page 1, size 50, maximum 200 and the RFC 9457 problem body (type, title, status, detail, message identifier) into the decision-log read contract when filters are added. |
| CDC-11653 | RWB-P7-E1008-DB | GAP-1229 | find it | Publish page 1, size 50, maximum 200 and an RFC 9457 problem body with type, title, status, detail and message identifier when the filters are added. |
| CDC-11683 | RWB-P7-E1008-OPS | GAP-1229 | find it | Confirm page 1, size 50 and maximum 200, with an RFC 9457 body carrying type, title, status, detail and the message identifier, when the filters are added. |

### RWB-PLT-TE006-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11611 | RWB-P7-E1008-APP | GAP-1232 | n/a | Publish login naming rwb-<short>_app plus owner role, keep migration account separate from runtime login, and name the template version of the three library objects. |
| CDC-11636 | RWB-P7-E1008-CON | GAP-1232 |  | Publish the rwb-<short>_app login convention plus an owner role, keep the migration account separate from the runtime login, and name the template version of the three library objects. |
| CDC-11655 | RWB-P7-E1008-DB | GAP-1232 | 8 | Publish the login naming convention rwb-<short>_app plus an owner role; keep the migration account separate from the runtime login; name the template version of the three library objects. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11641 | RWB-P7-E1008-DB | DOR-RWB-P7-E1008-DB-9 | 14 | Text of MSG-P7-009 and MSG-P7-003 in section 14 to match the standard entries for these messages. |
| CDC-11689 | RWB-P7-E1017-APP | CG-ALL-6872 | 14 | Add a new message ID for the refused-record check (MSG-P7-009 text in section 14); the story then cites it. |
| CDC-11690 | RWB-P7-E1017-APP | DOR-RWB-P7-E1017-APP-9 | 14 | State the meaning of MSG-P7-009 as the standard gives it, or align this story's use of it to that meaning. MSG-GEN-001 row added in section 14 here. |

### 06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20538 | RWB-P7-E1001-APP | R-28433 |  | Ownership cells DP03, DP08, DP09, DP10, DP12, DP14 and split rows 7-8 need exact current text, which could not be read from the xlsx in this run. |
| CDC-20539 | RWB-P7-E1001-APP | R-21851 |  | Ownership has Owning service, Owning schema and Basis (D-RCV-60) in columns L-N; Ownership split has them in columns G-I. |
| CDC-20540 | RWB-P7-E1001-APP | R-28431 |  | Basis cell for the Ownership split row needs its exact current text to append the count basis; the cell could not be read in this run. |

### RWB-P1-E1001-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11539 | RWB-P7-E1001-APP | GAP-0557 | find it | Adopt the five wave-1 assumptions: keep the built baseline; create P1's 13 own tables from its split migration; name schema and login rwb_source_data; leave the four extension tables to RWB-P1-E1069-DB; keep the catalog, dictionary and v_data_dictionary in rwb_source_data. |
| CDC-11557 | RWB-P7-E1001-APP | GAP-2539 | none | Keep DP13 as one product with one row: money facts owned by ACE, the match owned by the Workbench; correct the catalog wording under a new catalog version. |

### 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11559 | RWB-P7-E1001-APP | GAP-0285 | none | Add one cut table mapping each built-schema table to its rwb_* schema, with its baseline migration and data move order; RWB-PLT-NF06-DB and each per-service DB story cite it. |
| CDC-11674 | RWB-P7-E1008-OPS | GAP-1231 | find it | Drop fk_decision_log_entry_case_id; keep case_id as a plain uuid verified through the P3 case contract; record the same ruling for every legacy cross-module key of the decision log. |

### OTHER:ERD v5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11568 | RWB-P7-E1001-APP | GAP-0115 |  | Draw the 108 v5 references unchanged and state the two metadata keys (sys_fields.object_name, sys_objects.data_product) separately in the reconciliation table. |
| CDC-11569 | RWB-P7-E1001-APP | GAP-0116 |  | Group the v5 objects by Ownership Map owner, add a cross-service reference table, and keep the v5 data-product table as section 3. |

### RWB-P7-E1008-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11604 | RWB-P7-E1008-APP | GAP-1234 | find it | Set RPO zero for committed entries via ACE database PITR plus seal files; RTO Not specified in the source documents (GAP-1234), to be agreed with the service owner; make chain re-verification and append-only check mandatory restore gates. |
| CDC-11626 | RWB-P7-E1008-CON | GAP-1234 | 4 | Set RPO zero for committed entries via ACE PITR plus seal files; RTO Not specified in the source documents (GAP-1234); make chain re-verification and append-only check mandatory restore gates. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11622 | RWB-P7-E1008-CON | DOR-RWB-P7-E1008-CON-12 | 12.7, 16, 18 | Register TC-P7-E1008-CON-01 to -08 in Test Cases v8; align the REQ-DRI test lists in RTM v7 with section 18. |
| CDC-11665 | RWB-P7-E1008-OPS | DOR-RWB-P7-E1008-OPS-12 | 16 | Add TC-P7-E1008-OPS-01 to -09 to Test Cases v8; align the §18 test lists of this story with RTM v7 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11623 | RWB-P7-E1008-CON | DOR-RWB-P7-E1008-CON-7 | 11 | Record ce_type and ce_id as CloudEvents transport attributes of RWB-PLT-E1027-CON, or confirm they are not data fields. |
| CDC-11666 | RWB-P7-E1008-OPS | DOR-RWB-P7-E1008-OPS-7 | 11 | Record flyway_schema_history, ce_id, ce_type, tr_declog_append_only and the further name, or use dictionary names |

### RWB-P7-E1008-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11635 | RWB-P7-E1008-CON | GAP-1228 |  | Record that the DP-09 library objects are created by RWB-P7-E1008-DB under the X row and that this consumer is built against the published template. |
| CDC-11650 | RWB-P7-E1008-DB | GAP-2075 | find it | Audit search reads the ledger only and shows entries not yet collected by JOB-13 as not yet sealed; strict mode waits for the ledger acknowledgement of its own record. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11687 | RWB-P7-E1017-APP | CG-ALL-6869 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation. |
| CDC-11688 | RWB-P7-E1017-APP | DOR-RWB-P7-E1017-APP-8 | find it | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml. Event type fixed in 12.4; error IDs stated in 12.1. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_source_data.sql (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20586 | RWB-P7-E1001-APP | R-28419 |  | rwb_source_data.sql already keeps lake_copy_watermark DDL with a retirement note (lines 361-363) citing GAP-0114. No change needed. |
| CDC-20588 | RWB-P7-E1001-APP | R-28419 |  | Same change as the other R-28419 row (GAP-0114). The DDL and retirement note already exist in rwb_source_data.sql. The P1 DB story edit is outside this file. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20684 | RWB-P7-E1001-APP | R-28443 |  | Section 'Epic 1 and the 19 services' already states P8 rwb-payment takes Epic 1 stories in wave 1 by the W-MAP rule (GAP-3171). |
| CDC-20685 | RWB-P7-E1017-APP | R-21973 |  | RWB-E1-017 already gives retention_rule and retention_action to P5 rwb_document (GAP-3158); no edit needed. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11537 | RWB-P7-E1001-APP | DOR-RWB-P7-E1001-APP-11 | 2 | Reconcile the P2 fields classed as personal data with section 2's statement that no personal value enters rwb_decision; name them or mark them not carried. |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11538 | RWB-P7-E1001-APP | GAP-0566 | find it | Publish the three read operations with their response fields and problem body in RWB-P1-E1069-CON, and record in the catalog the application, database and integration slices of RWB-E1-069 as proposed. |

### RWB-P4-E1001-APP; RWB-P4-E1037-APP; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11540 | RWB-P7-E1001-APP | GAP-0975 | find it | Confirm RWB-P4-E1001-APP owns the DDL, keys, indexes and migration of the five rwb_access tables; read sibling 'rwb_access baseline' as the version applied; RWB-P4-E1037-CON keeps the contract stub and creates no table. |

### OTHER:v4 Mapping workbook (Mapping and ACE gaps sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11546 | RWB-P7-E1001-APP | GAP-0211 |  | Add 'Target schema' and 'Owning service' columns after column N, one value per row from the Ownership Map Tables sheet; keep columns A to N unchanged. |

### OTHER:v3 data products workbook (Ownership and Ownership split sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11547 | RWB-P7-E1001-APP | GAP-0224 |  | Add 'Owning service (D-RCV-60)', 'Owning schema (D-RCV-60)' and 'Basis (D-RCV-60)' after column K, one owner per data product from the Ownership Map; keep A to K unchanged. |

### OTHER:RWB-E1-001 dictionary (section 13, sys_objects) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11550 | RWB-P7-E1001-APP | GAP-0333 |  | Record the 24 operational objects (OPS 13, AGT 8, RPT 3) as an open list with no rwb_* schema; per-service DB stories assign them; wave-1 run does not fail on them. |

### OTHER:TSD P4 v3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11551 | RWB-P7-E1001-APP | GAP-0976 | 12 | Fix rwb_access at exactly role, permission, role_conflict, masking_rule and delegation_limit; mark TSD P4 v3 declarations of lov_value, partner_user and the four rule tables as superseded by ownership rulings. |

### OTHER:Recovery Workbench Functional Specification (P1 field catalogues A2.1; OTHER:A2.2; OTHER:A2.15 to A2.18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11553 | RWB-P7-E1001-APP | GAP-1512 | none | Carry the field lists of data_contract, dp_treatment, dp_guarantee_claim and efs_ledger_outcome as placeholders until the technical specification review before wave 2. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11554 | RWB-P7-E1001-APP | GAP-2123 | none | Assign the rwb_valuation tables (valuations, D6 route decision, route agent output) to S1 in the Ownership Map and the Physical Schema folder. |

### OTHER:Technical Specification P8 T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11556 | RWB-P7-E1001-APP | GAP-2538 | none | Keep case_id, treatment_id and account_payment_id as uuid values with no foreign key; resolve references through the owners' contracts. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11558 | RWB-P7-E1001-APP | GAP-0150 | none | Record the split of the single 92-table recovery schema into one schema per service as new work (RWB-PLT-NF06-DB and the 19 per-service DB stories); keep FEAT-RDF-01 and FEAT-RDF-25 rows unchanged. |

### OTHER:Security and Access Design v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11562 | RWB-P7-E1001-APP | GAP-2035 | none | Rewrite section 7 per service: one login rwb_<short> per service with grants on its own schema only; rwb_source_data the only holder of the v_ace_* view grant; replace the recovery_svc isolation row with a service login isolation row; state the change in v5's realignment table. |

### OTHER:Functional Specification P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11563 | RWB-P7-E1001-APP | GAP-0980 | none | Field catalog: keep role.entra_group (DF-REF-039, varchar(120), technical spec T3.1) as a nullable empty column; read the Entra group mapping at run time from v_ace_iam_group through the rwb-source-data contract; copy no ACE fact. |

### OTHER:Technical Specification RWB-P4 v3 (T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11564 | RWB-P7-E1001-APP | GAP-0979 | none | Name constraints and indexes for role, role_conflict, masking_rule, delegation_limit and permission: platform naming convention; primary key on id; unique role_code; foreign key permission.role_id; one index per read path. |

### OTHER:Per-service Flyway sequence (DP-15; OTHER:ADR-021) in the service baseline; RWB-PLT-E1047-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11566 | RWB-P7-E1001-APP | GAP-0112 | none | Define one V0001 baseline per service schema; the view file follows the source V0002 and V0003 sections. |

### OTHER:rwb_source_data.sql and P1 DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11567 | RWB-P7-E1001-APP | GAP-0114 |  | Keep the lake_copy_watermark DDL in rwb_source_data.sql with a retirement note, and have the P1 DB story drop the table. |

### OTHER:'By source' sheet (source workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11571 | RWB-P7-E1001-APP | GAP-0212 |  | Read rwb_source_data.party_ext in the Aric via COLLINS cell; leave the 1/0/0/1 counts and the Total row unchanged. |

### OTHER:Mapping (v4 to v5; OTHER:Mapping rules) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11572 | RWB-P7-E1001-APP | GAP-0215 |  | State contact_point_ext, account_ext and valuation_ext under 'Extension fields' in the Mapping rules; leave the 133 field rows unchanged until LDM v10. |

### OTHER:Mapping (v5, column B) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11573 | RWB-P7-E1001-APP | GAP-0216 |  | Leave the data-product cell empty for the 81 blank field rows in v5; assign them at the next LDM revision. |

### OTHER:Ownership split (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11579 | RWB-P7-E1001-APP | GAP-0232 |  | Append the basis cell: 93 Ownership Map rows = 4 extension tables + 1 legacy table with no target (lake_copy_watermark) + 88 Tier 4 tables over 19 owners. Keep the count of 88. |

### OTHER:Recovery Workbench roles, change process and quality measures (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11580 | RWB-P7-E1001-APP | GAP-0233 |  | Add one role row (service data steward), one change-process step (owner service) and one quality measure (schema isolation). Keep the v3 rows unchanged. |

### OTHER:Ownership split and data product register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11581 | RWB-P7-E1001-APP | GAP-0234 |  | Append the owning service column. Change the two Workbench access cells to the owning service and its rwb_<name> schema. Replace the DL02 wording at the next revision. |

### OTHER:rwb-access story (key not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11582 | RWB-P7-E1001-APP | GAP-0978 |  | Write V<seq>__rwb_p4_e1001_access_schema.sql with the four-digit sequence taken at merge in the rwb-access pipeline; the test asserts it is later than every service-baseline version and never 0001 of the legacy line. |

### OTHER:Target Architecture v6 slide 11 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11583 | RWB-P7-E1001-APP | GAP-1984 |  | State 93 as the target count (87 Workbench tables plus 6 platform library tables) and record 92 as the version 6 monolith count that the physical schema work replaces. |

### OTHER:TSD P8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11585 | RWB-P7-E1001-APP | GAP-2534 |  | Publish the primary-key name, the two index names, the index column order and the Field IDs of is_active, state, version, created_at, created_by, updated_at and updated_by: Not specified in the source documents (GAP-2534). |

### OTHER:Recovery Workbench Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11586 | RWB-P7-E1001-APP | GAP-3171 | none | State the wave 1 delivery of rwb-payment in the service epic and the wave plan; the rwb-payment service wave governs its later stories. |

### OTHER:AsyncAPI document for rwb.decision-record.v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11601 | RWB-P7-E1008-APP | GAP-0332 | 11 | Publish the DecisionRecorded payload and ingest rule at the shared-topic contract review before first SIT: CloudEvents id as dedupe key in processed_event, order per case from producer, chain_seq and prev_hash assigned by rwb-decision under the chain lock, catch-up within five minutes. |

### OTHER:Functional Specification P7 v3 (FSD module) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11602 | RWB-P7-E1008-APP | GAP-1226 | find it | Withdraw FEAT-DRI-06 and its AC-P7-006-01 lake criteria in the next FSD version; keep JOB-13 as continuous ingest and JOB-14 as the 02:00 chain check with WORM seal; record RWB-E1-014 retirement as delivered by the ledger. |

### RWB-P7-E1008-DB; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11603 | RWB-P7-E1008-APP | GAP-1231 | find it | Drop fk_decision_log_entry_case_id; keep case_id as an identifier verified through P3's case contract; record the same ruling for other legacy cross-module keys of the decision log in Physical Schema v7. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11605 | RWB-P7-E1008-APP | GAP-2502 | find it | Replace rwb.decision-record.DecisionRecorded.v1 with rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 before the Kafka Topic and Event Catalog freeze; register only transfer acceptance and version in force. Ingest, chain and JOB-14 stay in RWB-P7-E1008-APP. |

### OTHER:Build sequence (delivery plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11612 | RWB-P7-E1008-APP | GAP-2437 | n/a | Record that a secondary slice builds against platform contracts and fakes of section 12.8 and reads same-service wave-1 tables in its own schema; no dependency row changes. |

### OTHER:Batch and Scheduling (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11613 | RWB-P7-E1008-APP | GAP-1240 | n/a | Mark JOB-13 as retired; keep the ingest continuous and JOB-14 as the only P7 Schedule. |

### RWB-P7-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11614 | RWB-P7-E1008-APP | GAP-2410 |  | Record in the build sequence that a secondary slice builds against the platform contracts and published fakes and reads the same service's wave-1 rows through its own schema, keeping lane depth within R5.7 rule 5. |

### RWB-P7-E2005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11621 | RWB-P7-E1008-CON | DOR-RWB-P7-E1008-CON-10 | 18 | Define the empty, loading, error and no-access states of SCR-38 in that story. |

### OTHER:FSD P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11625 | RWB-P7-E1008-CON | GAP-1226 | 4 | Withdraw FEAT-DRI-06 and its lake acceptance criteria; keep JOB-13 as continuous ingest and JOB-14 as 02:00 chain check with WORM seal; record RWB-E1-014 retirement as delivered by the ledger. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:TSD P7 v2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11629 | RWB-P7-E1008-CON | GAP-1622 | 4 | Add a contract version to the DecisionRecorded envelope and record it on decision_log_entry. The story now states the consumer rule for known and unknown versions. |

### OTHER:Temporal and Drools design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11631 | RWB-P7-E1008-CON | GAP-2075 | 12.1 | State that strict mode waits for the ledger acknowledgement of its own record only, not for pending entries of other services. |

### OTHER:Deployment configuration (DevOps lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11633 | RWB-P7-E1008-CON | GAP-1233 |  | Consumer group rwb-decision-ledger; lag alert at 5 minutes; dead-letter alert at the first dead letter; verification job at 01:00; per-environment WORM path agreed with the storage owner. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11637 | RWB-P7-E1008-DB | DOR-RWB-P7-E1008-DB-14 | n/a | Record the signed epic design sign-off for RWB-P7-E1008-DB. |

### OTHER:AsyncAPI contract for rwb.decision-record.v1 (shared-topic contract review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11642 | RWB-P7-E1008-DB | GAP-0332 |  | Publish the AsyncAPI document with the DecisionRecorded payload and the ingest rule: CloudEvents id as dedupe key in processed_event, per-case ordering from the producer, chain_seq and prev_hash assigned by rwb-decision under the chain lock, catch-up within five minutes. |

### OTHER:FSD P7 v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11644 | RWB-P7-E1008-DB | GAP-1226 |  | Withdraw FEAT-DRI-06 and its lake acceptance criteria; keep JOB-13 as continuous ingest and JOB-14 as the 02:00 chain check with WORM seal; record RWB-E1-014 retirement as delivered by the ledger. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11646 | RWB-P7-E1008-DB | GAP-3194 |  | Raise one ACE DB story per service without one (S2, S4, S5, S6, S7, P6, P8) for the DEF-05 column drop, or attach the drop to the creating APP story, and cite the chosen story on row 121 before wave 2. |

### RWB-PLT-TE006-CON; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11649 | RWB-P7-E1008-DB | GAP-1622 | 3 | Add a contract version to the DecisionRecorded event, let the consumer accept a known set of versions and send an unknown one to the dead-letter topic. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11652 | RWB-P7-E1008-DB | GAP-1233 | 3 | Consumer group name and dead-letter threshold set to Not specified in the source documents (GAP-1233); lag and verification-time alerts retained. |

### OTHER:rwb-source-data contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11657 | RWB-P7-E1008-OPS | DOR-RWB-P7-E1008-OPS-22 | 12.8 | Record the published library version of the P1 job view fake; not specified in the source documents (DOR-RWB-P7-E1008-OPS-22). |

### OTHER:Message catalogue owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11667 | RWB-P7-E1008-OPS | DOR-RWB-P7-E1008-OPS-9 | 14 | Row added with Not specified in the source documents placeholders |

### OTHER:DB story of each service writing a decision record (rwb-decision and the 19 services) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11668 | RWB-P7-E1008-OPS | GAP-2068 | find it | Name the local decision-record table and its DDL, created through the decision-record library, with the target field list and the case and trace ID held in inputsRef. |

### OTHER:AsyncAPI document for rwb.decision-record.v1 (shared-topic contract review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11670 | RWB-P7-E1008-OPS | GAP-0332 | find it | Publish the DecisionRecorded payload and the ingest rule: CloudEvents id as dedupe key in processed_event, per-case order, chain_seq and prev_hash assigned by rwb-decision under the chain lock, catch-up within five minutes. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11677 | RWB-P7-E1008-OPS | CG-ALL-6868 | 15 | Empty, loading, error and no-access states marked Not specified in the source documents |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11678 | RWB-P7-E1008-OPS | GAP-1622 | find it | Add a contract version to the DecisionRecorded event, record it on the decision_log_entry ledger entry, and have the consumer accept a known set of versions and send an unknown one to the dead-letter topic. |

### RWB-PLT-TE006-CON; OTHER:platform DB work (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11686 | RWB-P7-E1008-OPS | GAP-1232 | 7 | Publish the login convention rwb-<short>_app with a schema owner role and a separate migration account; name the template version and column set of the three PLT library objects. |

### OTHER:TSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11691 | RWB-P7-E1017-APP | GAP-0488 | 12.7 | Drop T3.6 retention_rule as a P1 table; P5 rwb-document owns retention_rule, retention_action, the load and the JOB-17 Schedule; P1 holds only the rule version, run date and rules in the request. |

### RWB-P1-E1017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11692 | RWB-P7-E1017-APP | GAP-0489 | 12.7 | Fix POST /retention-runs and GET /retention-runs/{runId} on /api/recovery/source-data/v1 with the rule version, run date and rules in the request, the counts per table, rule version, archive location and held cases in the answer, and the 202 and 409 responses. |

### OTHER:Build Notes v6 RWB-E1-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11693 | RWB-P7-E1017-APP | GAP-3158 | 12.7 | Move ownership of retention_rule and retention_action and the retention Schedule JOB-17 to P5 rwb_document; P1 keeps only a contract read. |

### RWB-PLT-TE012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11694 | RWB-P7-E1017-APP | GAP-0490 | 3 | Write-once archive container contract: account, credential scope, immutability policy, request shape and manifest schema. |

### OTHER:Platform secret store (ACE team allocation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11696 | RWB-P7-E1017-APP | GAP-2430 | 3 | Allocate the rwb-decision login with schema rwb_decision and record its name in the platform secret store. |

### OTHER:Recovery Workbench delivery sequence v6 (tracker) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11697 | RWB-P7-E1017-APP | GAP-3230 |  | Drop the rows of RWB-E1-014 and RWB-TE-007 at cut-over, or keep them struck through with 'retired, not pulled'; remove them from Depends on of RWB-E1-056 and RWB-E1-017. |

### 06 Data/Recovery Workbench Source to Target Mapping v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20537 | RWB-P7-E1001-APP | R-21850 |  | Mapping and ACE gaps sheets already have Target schema and Owning service columns (structure check). No edit made. |

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
| GAP-0342 | E1017 retention ownership and the P1 interaction path | Solution architect | Resolved (directive) |
| GAP-0488 | retention_rule ownership: TSD P1 v3 keeps it in P1, the Ownership Map and Arch v5 move retention to P5 | Solution architect | Resolved (directive) |
| GAP-0489 | The rwb-source-data retention-run contract shape is not specified | Solution architect | Resolved (directive) |
| GAP-0490 | The write-once archive contract (container, path and manifest) belongs to RWB-PLT-TE012-APP and is not specified | Solution architect | Resolved (directive) |
| GAP-0491 | The legal-hold query is a published interface with no REST path in the sources | Solution architect | Resolved (directive) |
| GAP-0557 | RWB-P1-E1001-APP: schema-split mechanics, login name, extension-table delivery boundary and Arch v5 against FSD and TSD P1 | Solution architect | Resolved (directive) |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0976 | The exact per-service table list of rwb_access is not stated in one place | Solution architect | Resolved (directive) |
| GAP-0978 | The file name and sequence number of the rwb_access baseline migration are not fixed | Tech lead | Resolved (directive) |
| GAP-0979 | The constraint names and the full index set of the five tables are not specified | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-0980 | role.entra_group is a column in the technical specification and not a Workbench column in the functional one | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0984 | rwb-access local decision-record store: the column set behind the five named columns, the canonical form, the genesis value, the verifier behaviour on write and read, the DECISION_LOG letters per role and the per-service login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1240 | JOB-13 is a 01:00 copy job in the specifications and a continuous ingest in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1246 | Approver index migration sits on a table created by another story | ACE team, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1280 | LDM v8 states 18 fields for rule_row and a rule_test_case.package_version_id that its fields sheet does not define, and both name cross-schema foreign keys that DP-01 forbids | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1512 | Four tables carry a name, an owner and a purpose but no field list in the read sources | Data architect | Resolved (directive) |
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
| GAP-2401 | The LDM states one field count for rule_row and a rule_test_case column its fields sheet does not define, and both TSD P7 and the LDM name cross-schema foreign keys that DP-01 forbids | Solution architect, P7 rwb-decision, with the data owners of rwb_case and rwb_access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2426 | The decision code, final call, action and outcome values and the payload placement of an archive or purge record are in no source | Solution architect | Resolved (directive) |
| GAP-2427 | The text of MSG-P7-009 and the ids and texts of the not-found answer, the chain-break report and the collection gap alert are not written in any source | Business analyst, P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2428 | The JOB-14 timezone, page size, overlap and catch-up values, the property names and the behaviour of the feature flag when off are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2430 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2431 | The story file at the Work Package path already existed as a partial artefact of the superseded Work Package B-P7-05, with no fragment, no register rows and citations that resolve to nothing | Delivery lead, with the traceability owner | Resolved (directive) |
| GAP-2432 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept | Traceability owner | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2502 | Decision-record event naming and the boundary with RWB-P7-E1008-APP and RWB-P7-E2027-APP | P7 solution architect, with the event platform owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2534 | The DDL of proceeds beyond its columns is not published: constraint names, index names, index columns and the Field IDs of the 7 standard columns | ACE team | Resolved (directive) |
| GAP-2535 | TSD P8 T3.1 carries payment_match_rule as a second table of the module, and the Ownership Map gives P8 one table only | Solution architect | Resolved (directive) |
| GAP-2536 | The read paths that proceeds has to serve, and the screens that read it, are stated in no source of the read set | Solution architect | Resolved (directive) |
| GAP-2537 | The handover of a service's field declaration to the one dictionary has no documented mechanism or operation | Solution architect | Resolved (directive) |
| GAP-2538 | TSD P8 T3.3 declares three many-to-one relationships of proceeds and the target keeps them as values | Solution architect | Resolved (directive) |
| GAP-2539 | DP13 Money and closure is catalogued with the system of record ACE only, while the match on the same row is a Workbench record | Business analyst, P8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2541 | EP01's wave map wave is 1 and rwb-payment's Architecture v5 wave is 2 for the same story | Portfolio lead | Resolved (directive) |
| GAP-3151 | Origin tag where one legacy criterion is carried by several new stories | TechX | Resolved (directive) |
| GAP-3158 | The retention tables are P1 tables in the story and P5 tables in the Ownership Map | P5 document owner | Resolved (directive) |
| GAP-3171 | Service P8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3230 | Two retired items still carry v6 windows and dependencies | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P7-E1017-APP | skipped AC ID | 131 | missing: AC9 |
