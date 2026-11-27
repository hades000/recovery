# RWB-PLT-TPL Service template and repositories - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 19 |
| Resolved in the stories | 177 |
| Cross-document (pending in another document) | 293 |
| Not applied (value not in the sources) | 29 |
| Open business decisions | 16 |
| Register gaps linked | 97 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-E1044-APP-2 | 6 | 18 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT E1044 APP-2 Database migrations versioned with parameterized schema names v2.md |
| RWB-PLT-E1044-APP | 7 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT E1044 APP Database migrations versioned with parameterized schema names v2.md |
| RWB-PLT-E1044-CON | 19 | 54 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT E1044 CON Database migrations versioned with parameterized schema names - contract v2.md |
| RWB-PLT-E1044-OPS | 8 | 20 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT E1044 OPS Database migrations versioned with parameterized schema names - deployment v2.md |
| RWB-PLT-N004-OPS | 5 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT N004 OPS Service pipeline template and Helm chart - deployment v2.md |
| RWB-PLT-NF01-OPS | 10 | 6 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT NF01 OPS Repository and pipeline baseline - deployment v2.md |
| RWB-PLT-NF03-OPS | 10 | 5 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT NF03 OPS Environment baseline - deployment v2.md |
| RWB-PLT-NF04-OPS | 8 | 4 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT NF04 OPS Secrets and configuration baseline - deployment v2.md |
| RWB-PLT-NF05-OPS | 8 | 5 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT NF05 OPS Quality gates baseline - deployment v2.md |
| RWB-PLT-TE001-APP-2 | 8 | 16 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE001 APP-2 Recovery module folder and boundary test v2.md |
| RWB-PLT-TE001-APP | 7 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE001 APP Recovery module folder and boundary test v2.md |
| RWB-PLT-TE002-APP | 9 | 12 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE002 APP Code owners for the recovery module v2.md |
| RWB-PLT-TE002-OPS | 6 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE002 OPS Code owners for the recovery module - deployment v2.md |
| RWB-PLT-TE003-APP-2 | 8 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE003 APP-2 Types and contract tests from the API specification v2.md |
| RWB-PLT-TE003-APP | 7 | 26 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE003 APP Types and contract tests from the API specification v2.md |
| RWB-PLT-TE004-APP | 10 | 12 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE004 APP Masked data in SIT and UAT v2.md |
| RWB-PLT-TE008-APP | 9 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE008 APP Decision log hash chain check v2.md |
| RWB-PLT-TE011-APP | 15 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE011 APP PDPA lint for code, tests and logs v2.md |
| RWB-PLT-TE012-APP | 17 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-TPL Service template and repositories/RWB PLT TE012 APP Document storage containers v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-PLT-NF03-OPS | R-09235 | GAP-2131 | Register gap | IT lead with Operational Risk | The restore pass mark has no target while the recovery objectives are open | Section 6.4 and NFT-PLT-08 run against the ACE objectives recorded under DL11 and are re-run when NFR-022 and NFR-023 are set; section 4 names the open IDs. |
| RWB-PLT-TE002-APP | R-11890 | CG-ALL-1550 | Script gap | Product owner | Open decision DL32 has no assumption | Owner rules DL32; until then build on the recommended option. |
| RWB-PLT-TE002-OPS | R-11898 | CG-ALL-1561 | Script gap | Product owner | Open decision DL32 has no assumption | Owner rules DL32; until then build on the recommended option. |
| RWB-PLT-TE008-APP | R-11979 | CG-ALL-1609 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-TE004-ITG, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP | R-22911 | GAP-1675 | Register gap | Compliance | The masking and scrubbing list for telemetry is not stated | Publish the masked and scrubbed field list per role, and apply it to the telemetry pipeline and the prompt path. |
| RWB-PLT-TE002-APP | R-33457 | ASM-ALL-1550 | Script assumption |  | Built on the recommended option of DL32: A. | CTO with SCB IT rules DL32 |
| RWB-PLT-TE002-OPS | R-33458 | ASM-ALL-1561 | Script assumption |  | Built on the recommended option of DL32: A. | CTO with SCB IT rules DL32 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1034-ITG, RWB-PLT-TE012-APP, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1041-APP, RWB-P6-AD017-APP, RWB-P6-E1034-APP | R-35419 | ASM-2709 | Register assumption |  | The values of the Non-Functional Specification v3 are the values this PRD is written against, with the status each one carries. A value marked Proposed is used as written until its owner confirms it under the decision named; a value marked Open is recorded as not set. | Solution architect with Risk at DL11 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-ITG-TE010-ITG, RWB-ITG-E1047-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P3-E1042-APP | R-35662 | ASM-3199 | Register assumption |  | The six open-point rows that named an individual (DL03, DL04, DL05, DL06, DL07, DL37) carry the Template and Rules R9 placeholder in the Owner column, with the organisation the same row already stated kept after it, and the five roles of section 9 are left as the only owner labels in the document. | Confirm the role that owns each of the six open points. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-E1044-APP-2 | R-07198 | DOR-RWB-PLT-E1044-APP-2-16 | Header | Definition of Ready item 16 Size: Fail | No size exists in the source documents; the row marks the gap rather than stating a process. |
| RWB-PLT-E1044-APP-2 | R-07201 | DOR-RWB-PLT-E1044-APP-2-23 |  | Definition of Ready item 23 Contract version fixed: Fail | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-23). Only the /v1 path is stated; a contract version would be invented. Header shows Contract dependencies None. |
| RWB-PLT-E1044-APP-2 | R-18596 | DOR-RWB-PLT-E1044-APP-2-10 |  | Definition of Ready item 10 Screens and states: Partial | Not specified in the source documents (DOR-RWB-PLT-E1044-APP-2-10). No source gives SCR-44 empty, loading, error or no-access states; a grep for SCR-44 found no screen spec for them. |
| RWB-PLT-E1044-APP-2 | R-31755 | NEWAC-RWB-PLT-E1044-APP-2-AC8 | 7, 16 | AC8: a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents (NEWAC-RWB-PLT-E1044-APP-2-AC8). Header shows Integration and Contract dependencies None, and no source gives failed-call behaviour; writing AC8 would invent it. |
| RWB-PLT-E1044-APP-2 | R-31756 | NEWAC-RWB-PLT-E1044-APP-2-AC9 | 7, 16 | AC9: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents (NEWAC-RWB-PLT-E1044-APP-2-AC9). The story defines no status model or allowed transitions, so a disallowed-transition criterion would invent rules. |
| RWB-PLT-E1044-APP | R-18594 | DOR-RWB-PLT-E1044-APP-4 | 7; 8 | Definition of Ready item 4 Business rules: Partial | Test case rows in section 16 not added: section 16 text is not in this chunk. |
| RWB-PLT-E1044-APP | R-31753 | NEWAC-RWB-PLT-E1044-APP-AC10 | 7; 16 | AC10: §8 BR6, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 16 test rows for AC10 and AC11 are missing because section 16 text is not in this chunk. |
| RWB-PLT-E1044-CON | R-18602 | DOR-RWB-PLT-E1044-CON-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-44 is in the P3 screen story, not this migration contract. Empty, loading, error and no-access states are screen design content not in the sources. No edit. |
| RWB-PLT-E1044-CON | R-22713 | GAP-2412 |  | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Element names, request and answer shapes, MSG-P7-009 text and the login name are in no readable source (checked the story and evidence). They cannot be invented here. No edit. |
| RWB-PLT-E1044-CON | R-28546 | GAP-1041 |  | The rwb-document login name and its grants are not specified | The rwb-document login name, secret reference and grants are not in any source. Allocating them needs a value the directive does not supply. No edit. |
| RWB-PLT-E1044-CON | R-28709 | GAP-0916 |  | The per-service database login name of rwb-access is not specified | No source gives the rwb_access login name (Template R5.5 DP-02, Architecture v5 slide 41, TSD P4 T1 and T3.1 checked). Naming it would invent a credential identifier. No edit. |
| RWB-PLT-E1044-CON | R-29038 | GAP-1420 |  | Per-service Flyway history table name and migration-run record fields are not specified | BR5 already states the default flyway_schema_history in the own schema. The migration-run record field list is in no source and cannot be stated without inventing it. No edit. |
| RWB-PLT-E1044-OPS | R-18608 | DOR-RWB-PLT-E1044-OPS-10 | 10 | Definition of Ready item 10 Screens and states: Partial | FSD P1 v3 line 1421 gives SCR-44 as purpose only (ACE batch status, jobs, reruns). No empty, loading, error or no-access states in any source, so none were added. |
| RWB-PLT-NF01-OPS | R-31818 | NEWAC-RWB-PLT-NF01-OPS-AC7 | 7, 16 | AC7: a status change the model does not allow is refused (no criterion covers a disallowed transition) | Story defines no status model or transition rules, and PRD PLT Platform v1.md has no match for status model, state machine or transition. An AC7 would need an invented model, so no edit. |
| RWB-PLT-TE001-APP-2 | R-02028 | CG-ALL-1530 | 7 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Architect's package segment for 'case' is not in the sources. Grepped PRD P3 rwb-case v1 (only the reserved-word package) and FSD P3 v5; no ruling found. Needs the Solution architect's ruling. |
| RWB-PLT-TE001-APP-2 | R-02029 | CG-ALL-1531 | 7 | Java package th.co.scb.ace.workbench.recovery.case.internal uses the reserved word 'case' | Architect's package segment for 'case.internal' is not in the sources. Same search as CG-ALL-1530 found no ruling. Needs the Solution architect's ruling. |
| RWB-PLT-TE002-APP | R-07408 | DOR-RWB-PLT-TE002-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in story or sources (folder 22 grep). Sign-off value cannot be written without inventing it. Not specified in the source documents (DOR-RWB-PLT-TE002-APP-14). |
| RWB-PLT-TE002-APP | R-07410 | DOR-RWB-PLT-TE002-APP-21 |  | Definition of Ready item 21 Contract published: Fail | No contract story for this legacy key in sources; CON dependencies not Done. Story text cannot resolve it. Not specified in the source documents (DOR-RWB-PLT-TE002-APP-21). |
| RWB-PLT-TE002-APP | R-07411 | DOR-RWB-PLT-TE002-APP-22 |  | Definition of Ready item 22 Fake published: Fail | Grep of folder 22 finds no published fake library version for RWB-P3-E1043-CON. Not specified in the source documents (DOR-RWB-PLT-TE002-APP-22). |
| RWB-PLT-TE002-APP | R-07412 | DOR-RWB-PLT-TE002-APP-23 |  | Definition of Ready item 23 Contract version fixed: Fail | Sources name only the /v1 path for RWB-P3-E1043-CON, with no contract version. Naming a version would be inferred. Not specified in the source documents (DOR-RWB-PLT-TE002-APP-23). |
| RWB-PLT-TE002-APP | R-18846 | DOR-RWB-PLT-TE002-APP-18 |  | Definition of Ready item 18 Open decisions: Partial | No assumption ID for open decision DL32 in sources; legacy story only cites DL32 for GitHub-format code owners. Not specified in the source documents (DOR-RWB-PLT-TE002-APP-18). |
| RWB-PLT-TE002-APP | R-29077 | GAP-1432 | 3 | The team handles, the ruleset name and the required-check list and its order are not specified | Required-check list and order are not specified in the sources; DevOps lead and solution architect still to close the point. |
| RWB-PLT-TE002-OPS | R-18853 | DOR-RWB-PLT-TE002-OPS-18 |  | Definition of Ready item 18 Open decisions: Partial | DL32 and its open-decision text are not in the supplied story text, so there is no anchor. Sources give no ASM ID for DL32; TE stories v8 L726 and L1041 mention it only as the GitHub host assumption. |
| RWB-PLT-TE002-OPS | R-18855 | DOR-RWB-PLT-TE002-OPS-4 |  | Definition of Ready item 4 Business rules: Partial | New criteria need a section 7 anchor and test rows need a section 16 anchor; neither part is in the supplied text. BR1 to BR8 are left uncovered. |
| RWB-PLT-TE002-OPS | R-31832 | NEWAC-RWB-PLT-TE002-OPS-AC6 |  | AC6: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC6 needs a section 7 anchor and a section 16 test row, neither in the supplied text. Proposed test is not specified in the source documents (NEWAC-RWB-PLT-TE002-OPS-AC6). |
| RWB-PLT-TE004-APP | R-07428 | DOR-RWB-PLT-TE004-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record for EP01-TE in the sources (searched folders 03 and 13, plus the Ways of Working v3 sign-off process). Sign-off cannot be confirmed from the documents; no edit. |
| RWB-PLT-TE004-APP | R-07430 | DOR-RWB-PLT-TE004-APP-21 | find it | Definition of Ready item 21 Contract published: Fail | No contract story of legacy key RWB-TE-004 in the sources. Done status of the CON dependencies sits in their own stories, not this one. No edit made. |
| RWB-PLT-TE004-APP | R-18872 | DOR-RWB-PLT-TE004-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | Error and Message Standard v4 is not in the sources (searched whole folder set). MSG-P2-006 wording cannot be aligned without it; section 14 unchanged. |
| RWB-PLT-TE004-APP | R-26709 | CG-ALL-1600 | 14 | MSG-P2-006 text differs from the Error and Message Standard v4 | Standard v4 is not in folders 03 or 13 (DOR-RWB-PLT-TE004-APP-9), so its text cannot be copied. The story keeps the RWB-TE-004 text. |

## 5. Cross-document changes (pending in the target document)


### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (84)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14110 | RWB-PLT-E1044-APP-2 | CG-ALL-1498 | Header | Renumber the duplicate FR-PLT-005 so each meaning has its own ID; the story's PRD reference row cites FR-PLT-005. |
| CDC-14111 | RWB-PLT-E1044-APP-2 | CG-ALL-1499 | header | Renumber the duplicate FR-PLT-006 row in the next PRD version. |
| CDC-14112 | RWB-PLT-E1044-APP-2 | CG-ALL-1500 | header | Renumber the duplicate FR-PLT-007 row in the next PRD version. |
| CDC-14127 | RWB-PLT-E1044-APP | CG-ALL-1488 | header | Renumber the duplicate FR-PLT-005 definition in the PRD's next version. This story keeps FR-PLT-005 for migration per service. |
| CDC-14128 | RWB-PLT-E1044-APP | CG-ALL-1489 | header | Renumber the duplicate FR-PLT-006 definition in the PRD's next version. |
| CDC-14129 | RWB-PLT-E1044-APP | CG-ALL-1490 | header | Renumber the duplicate FR-PLT-007 definition in the PRD's next version. |
| CDC-14130 | RWB-PLT-E1044-APP | DOR-RWB-PLT-E1044-APP-2 | 18 | Give FR-PLT-005, FR-PLT-006 and FR-PLT-007 one meaning each in the PRD. |
| CDC-14140 | RWB-PLT-E1044-CON | CG-ALL-1505 | header | Renumber one of the two FR-PLT-005 rows in the next PRD version. |
| CDC-14141 | RWB-PLT-E1044-CON | CG-ALL-1506 | header | Renumber one of the two FR-PLT-006 rows in the next PRD version. |
| CDC-14142 | RWB-PLT-E1044-CON | CG-ALL-1507 | header | Renumber one of the two FR-PLT-007 rows in the next PRD version. |
| CDC-14145 | RWB-PLT-E1044-CON | DOR-RWB-PLT-E1044-CON-2 | 18 | Give each of FR-PLT-005, FR-PLT-006 and FR-PLT-007 one meaning in the PRD so the traceability rows in section 18 link to a single requirement. |
| CDC-14197 | RWB-PLT-E1044-OPS | CG-ALL-1513 | header | Renumber the duplicate FR-PLT-005 in the PRD's next version. |
| CDC-14198 | RWB-PLT-E1044-OPS | CG-ALL-1514 | header | Renumber the duplicate FR-PLT-006 in the PRD's next version. |
| CDC-14199 | RWB-PLT-E1044-OPS | CG-ALL-1515 | header | Renumber the duplicate FR-PLT-007 in the PRD's next version. |
| CDC-14202 | RWB-PLT-E1044-OPS | DOR-RWB-PLT-E1044-OPS-2 | 18 | Give FR-PLT-005, FR-PLT-006 and FR-PLT-007 one meaning each in the PRD. |
| CDC-15191 | RWB-PLT-TE001-APP-2 | CG-ALL-1532 | header | Renumber the duplicate FR-PLT-001 row so that each ID has one meaning. |
| CDC-15192 | RWB-PLT-TE001-APP-2 | CG-ALL-1533 | header | Renumber the duplicate FR-PLT-002 row so that each ID has one meaning. |
| CDC-15193 | RWB-PLT-TE001-APP-2 | CG-ALL-1534 | header | Renumber the second FR-PLT-010 meaning (transactional outbox) in the PRD's next version |
| CDC-15194 | RWB-PLT-TE001-APP-2 | CG-ALL-1535 | header | Renumber the second FR-PLT-011 meaning (inbox dedupe, retry ladder) in the PRD's next version |
| CDC-15195 | RWB-PLT-TE001-APP-2 | CG-ALL-1536 | header | Renumber the second FR-PLT-012 meaning (idempotency key) in the PRD's next version |
| CDC-15196 | RWB-PLT-TE001-APP-2 | CG-ALL-1537 | header | Renumber the second FR-PLT-013 meaning (RFC 9457 problem envelope) in the PRD's next version |
| CDC-15197 | RWB-PLT-TE001-APP-2 | CG-ALL-1538 | header | Renumber the second FR-PLT-027 meaning (19 schemas, 19 logins) in the PRD's next version |
| CDC-15206 | RWB-PLT-TE001-APP | CG-ALL-1520 | header | Renumber the duplicate FR-PLT-001 in the PRD's next version. |
| CDC-15207 | RWB-PLT-TE001-APP | CG-ALL-1521 | header | Renumber the duplicate FR-PLT-002 in the PRD's next version. |
| CDC-15208 | RWB-PLT-TE001-APP | CG-ALL-1522 | header | Renumber the duplicate FR-PLT-010 in the PRD's next version. |
| CDC-15209 | RWB-PLT-TE001-APP | CG-ALL-1523 | header | Renumber the duplicate FR-PLT-011 in the PRD's next version. |
| CDC-15210 | RWB-PLT-TE001-APP | CG-ALL-1524 | header | Renumber the duplicate FR-PLT-012 in the PRD's next version. |
| CDC-15211 | RWB-PLT-TE001-APP | CG-ALL-1525 | Header | Renumber the duplicate FR-PLT-013 meaning in the PRD's next version. |
| CDC-15212 | RWB-PLT-TE001-APP | CG-ALL-1526 | Header | Renumber the duplicate FR-PLT-027 meaning in the PRD's next version. |
| CDC-15214 | RWB-PLT-TE001-APP | DOR-RWB-PLT-TE001-APP-2 | 18 | Give one meaning to each flagged FR ID (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011 and the 3 more) and supply the requirement text so each gets a row in section 18. |
| CDC-15220 | RWB-PLT-TE002-APP | CG-ALL-1542 | header | Renumber one of the two FR-PLT-001 rows (Service template completeness; the platform SHALL generate a new service from one template) in the next PRD version. |
| CDC-15221 | RWB-PLT-TE002-APP | CG-ALL-1543 | header | Renumber one of the two FR-PLT-002 rows (Module boundary test; the build SHALL fail a service reading an ACE table or view directly) in the next PRD version. |
| CDC-15222 | RWB-PLT-TE002-APP | CG-ALL-1544 | header | Renumber one of the two FR-PLT-010 rows (Transactional outbox; the library SHALL write a state change and its event in one transaction) in the next PRD version. |
| CDC-15223 | RWB-PLT-TE002-APP | CG-ALL-1545 | header | Renumber one of the two FR-PLT-011 rows (Inbox dedupe, retry ladder and dead-letter path) in the next PRD version. |
| CDC-15224 | RWB-PLT-TE002-APP | CG-ALL-1546 | header | Renumber one of the two FR-PLT-012 rows (Idempotency key; the library SHALL require an Idempotency-Key on every POST) in the next PRD version. |
| CDC-15225 | RWB-PLT-TE002-APP | CG-ALL-1547 | header | Renumber the duplicate FR-PLT-013 in the PRD's next version |
| CDC-15226 | RWB-PLT-TE002-APP | CG-ALL-1548 | header | Renumber the duplicate FR-PLT-027 in the PRD's next version |
| CDC-15234 | RWB-PLT-TE002-OPS | CG-ALL-1553 | header | Renumber the duplicate FR-PLT-001 (Service template completeness) in the PRD's next version. |
| CDC-15235 | RWB-PLT-TE002-OPS | CG-ALL-1554 | header | Renumber the duplicate FR-PLT-002 (Module boundary test) in the PRD's next version. |
| CDC-15236 | RWB-PLT-TE002-OPS | CG-ALL-1555 | header | Renumber the duplicate FR-PLT-010 (Transactional outbox) in the PRD's next version. |
| CDC-15237 | RWB-PLT-TE002-OPS | CG-ALL-1556 | header | Renumber the duplicate FR-PLT-011 (Inbox dedupe, retry ladder and dead-letter path) in the PRD's next version. |
| CDC-15238 | RWB-PLT-TE002-OPS | CG-ALL-1557 | header | Renumber the duplicate FR-PLT-012 (Idempotency key) in the PRD's next version. |
| CDC-15239 | RWB-PLT-TE002-OPS | CG-ALL-1558 | header | Renumber the duplicate FR-PLT-013 in the PRD's next version |
| CDC-15240 | RWB-PLT-TE002-OPS | CG-ALL-1559 | header | Renumber the duplicate FR-PLT-027 in the PRD's next version |
| CDC-15243 | RWB-PLT-TE002-OPS | DOR-RWB-PLT-TE002-OPS-2 | 18 | Renumber the duplicate FR-PLT IDs (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011 and others) in the next version |
| CDC-15251 | RWB-PLT-TE003-APP-2 | CG-ALL-1581 | header | Renumber the duplicate FR-PLT-001 in the next PRD PLT version so each ID has one meaning (owner Business analyst). |
| CDC-15252 | RWB-PLT-TE003-APP-2 | CG-ALL-1582 | header | Renumber the duplicate FR-PLT-009 in the next PRD PLT version so each ID has one meaning (owner Business analyst). |
| CDC-15253 | RWB-PLT-TE003-APP-2 | CG-ALL-1583 | header | Renumber the duplicate FR-PLT-010 in the next PRD PLT version so each ID has one meaning (owner Business analyst). |
| CDC-15254 | RWB-PLT-TE003-APP-2 | CG-ALL-1584 | header | Renumber the duplicate FR-PLT-011 in the next PRD PLT version so each ID has one meaning (owner Business analyst). |
| CDC-15255 | RWB-PLT-TE003-APP-2 | CG-ALL-1585 | find it | Renumber the duplicate FR-PLT-012 row in the PRD's next version so each ID has one meaning. |
| CDC-15256 | RWB-PLT-TE003-APP-2 | CG-ALL-1586 | find it | Renumber the duplicate FR-PLT-013 row in the PRD's next version so each ID has one meaning. |
| CDC-15257 | RWB-PLT-TE003-APP-2 | CG-ALL-1587 | find it | Renumber the duplicate FR-PLT-019 row in the PRD's next version so each ID has one meaning. |
| CDC-15258 | RWB-PLT-TE003-APP-2 | CG-ALL-1588 | find it | Renumber the duplicate FR-PLT-021 row in the PRD's next version so each ID has one meaning. |
| CDC-15259 | RWB-PLT-TE003-APP-2 | CG-ALL-1589 | find it | Renumber the duplicate FR-PLT-022 row in the PRD's next version so each ID has one meaning. |
| CDC-15260 | RWB-PLT-TE003-APP-2 | CG-ALL-1590 | find it | Renumber the duplicate FR-PLT-023 row in the PRD's next version so each ID has one meaning. |
| CDC-15261 | RWB-PLT-TE003-APP-2 | CG-ALL-1591 | find it | Renumber the duplicate FR-PLT-024 row in the PRD's next version so each ID has one meaning. |
| CDC-15262 | RWB-PLT-TE003-APP-2 | CG-ALL-1592 | find it | Renumber the duplicate FR-PLT-025 row in the PRD's next version so each ID has one meaning. |
| CDC-15263 | RWB-PLT-TE003-APP-2 | CG-ALL-1593 | find it | Renumber the duplicate FR-PLT-026 row in the PRD's next version so each ID has one meaning. |
| CDC-15264 | RWB-PLT-TE003-APP-2 | CG-ALL-1594 | find it | Renumber the duplicate FR-PLT-028 row in the PRD's next version so each ID has one meaning. |
| CDC-15265 | RWB-PLT-TE003-APP-2 | CG-ALL-1595 | find it | Renumber the duplicate FR-PLT-029 entry in the PRD's next version so each FR-PLT ID has one meaning. The story PRD reference is unchanged. |
| CDC-15274 | RWB-PLT-TE003-APP | CG-ALL-1563 | header | Renumber the duplicate FR-PLT-001 in the PRD's next version. |
| CDC-15275 | RWB-PLT-TE003-APP | CG-ALL-1564 | header | Renumber the duplicate FR-PLT-009 in the PRD's next version. |
| CDC-15276 | RWB-PLT-TE003-APP | CG-ALL-1565 | header | Renumber the duplicate FR-PLT-010 in the PRD's next version. |
| CDC-15277 | RWB-PLT-TE003-APP | CG-ALL-1566 | header | Renumber the duplicate FR-PLT-011 in the PRD's next version. |
| CDC-15278 | RWB-PLT-TE003-APP | CG-ALL-1567 | header | Renumber the duplicate FR-PLT-012 in the PRD's next version. |
| CDC-15279 | RWB-PLT-TE003-APP | CG-ALL-1568 | Header | Renumber the duplicate FR-PLT-013 meaning (the second definition, not RFC 9457 problem envelope) in the next PRD version. |
| CDC-15280 | RWB-PLT-TE003-APP | CG-ALL-1569 | Header | Renumber the duplicate FR-PLT-019 meaning (the second definition, not Authorisation guard, deny by default) in the next PRD version. |
| CDC-15281 | RWB-PLT-TE003-APP | CG-ALL-1570 | Header | Renumber the duplicate FR-PLT-021 meaning (the second definition, not Cluster, namespace, retention, search attributes) in the next PRD version. |
| CDC-15282 | RWB-PLT-TE003-APP | CG-ALL-1571 | Header | Renumber the duplicate FR-PLT-022 meaning (the second definition, not the versioned workflow kit) in the next PRD version. |
| CDC-15283 | RWB-PLT-TE003-APP | CG-ALL-1572 | Header | Renumber the duplicate FR-PLT-023 meaning (the second definition, not Schedules and durable timers replace Quartz) in the next PRD version. |
| CDC-15284 | RWB-PLT-TE003-APP | CG-ALL-1573 | Header | Renumber the duplicate FR-PLT-024 meaning (the second definition, not Retry policy, backup, failover, archive, replay gate) in the next PRD version. |
| CDC-15285 | RWB-PLT-TE003-APP | CG-ALL-1574 | Header | Renumber the duplicate FR-PLT-025 meaning (the second definition, not Stuck-workflow scan, smoke workflow, codec) in the next PRD version. |
| CDC-15286 | RWB-PLT-TE003-APP | CG-ALL-1575 | Header | Renumber the duplicate FR-PLT-026 meaning (the second definition, not Mutual TLS, admin audit, break-glass decode) in the next PRD version. |
| CDC-15287 | RWB-PLT-TE003-APP | CG-ALL-1576 | Header | Renumber the duplicate FR-PLT-028 meaning (the second definition, not topics, retry and dead-letter, ACLs, registry) in the next PRD version. |
| CDC-15288 | RWB-PLT-TE003-APP | CG-ALL-1577 | Header | Renumber the duplicate FR-PLT-029 meaning (the second definition, not Blob, key store and transfer resources) in the next PRD version. |
| CDC-15301 | RWB-PLT-TE004-APP | CG-ALL-1603 | Header | Renumber the duplicate FR-PLT-008 (Synthetic development, masked acceptance, personal-data scan) in the PRD's next version |
| CDC-15302 | RWB-PLT-TE004-APP | CG-ALL-1604 | Header | Renumber the duplicate FR-PLT-019 (Authorisation guard, deny by default) in the PRD's next version |
| CDC-15431 | RWB-PLT-TE008-APP | CG-ALL-1610 | Header | Renumber the duplicate FR-PLT-014 in the next PRD version. |
| CDC-15432 | RWB-PLT-TE008-APP | CG-ALL-1611 | Header | Renumber the duplicate FR-PLT-015 in the next PRD version. |
| CDC-15435 | RWB-PLT-TE008-APP | DOR-RWB-PLT-TE008-APP-2 | 18 | Give FR-PLT-014 and FR-PLT-015 one meaning each |
| CDC-15445 | RWB-PLT-TE011-APP | CG-ALL-1616 | find it | Renumber the duplicate FR-PLT-008 row in the functional table. |
| CDC-15446 | RWB-PLT-TE011-APP | CG-ALL-1617 | find it | Renumber the duplicate FR-PLT-019 row in the functional table. |
| CDC-15454 | RWB-PLT-TE012-APP | CG-ALL-1621 | header | Renumber the duplicate FR-PLT-028 in the next PRD PLT version. |
| CDC-15455 | RWB-PLT-TE012-APP | CG-ALL-1622 | header | Renumber the duplicate FR-PLT-029 in the next PRD PLT version. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14118 | RWB-PLT-E1044-APP-2 | CG-ALL-1497 | 18 | Align the REQ-RDF-001 and REQ-RDF-014 test lists in RTM v7 with the TC-PLT-E1044-APP2-01 to -06 IDs in section 18 of this story. |
| CDC-14176 | RWB-PLT-E1044-CON | CG-ALL-1504 | 18 | In its next version, align the REQ-RDF-001 and REQ-RDF-014 test lists with section 18 of RWB-PLT-E1044-CON. |
| CDC-14209 | RWB-PLT-E1044-OPS | CG-ALL-1512 | 18 | Align the REQ-RDF-001 and REQ-RDF-014 test lists in the next RTM version to the test cases of section 18 of this story. |
| CDC-15145 | RWB-PLT-NF04-OPS | DOR-RWB-PLT-NF04-OPS-12 | 16, 18 | Add a test-case list for NFR-052, NFR-054 and REQ-DRI-010 that matches story section 18 (TC-PLT-NF04-OPS-01 to -05); the REQ-DRI-010 row currently has only priority, epic and phase, and NFR-052 and NFR-054 have no row. |
| CDC-15146 | RWB-PLT-NF04-OPS | CG-ALL-1518 | 18 | Align the REQ-DRI-010 row with RWB-PLT-NF04-OPS section 18 (TC-PLT-NF04-OPS-03) in the next RTM version. The TC-E1 test list belongs to other stories, so section 18 is unchanged. |
| CDC-15200 | RWB-PLT-TE001-APP-2 | CG-ALL-1529 | 18 | Align the REQ-DRI-006 test list with section 18 of RWB-PLT-TE001-APP-2 (TC-PLT-TE001-APP2-05) in the next RTM version. |
| CDC-15213 | RWB-PLT-TE001-APP | DOR-RWB-PLT-TE001-APP-12 | 16, 18 | Align the REQ-DRI-006 trace with the story §18 list TC-TE-001-01 to TC-TE-001-08. |
| CDC-15215 | RWB-PLT-TE001-APP | CG-ALL-1519 | 18 | Align the REQ-DRI-006 trace with the story §18 list TC-TE-001-01 to TC-TE-001-08. |
| CDC-15227 | RWB-PLT-TE002-APP | DOR-RWB-PLT-TE002-APP-12 | 16, 18 | Align the RWB-PLT-TE002-APP test list with story section 16 (TC-TE-002-01 to TC-TE-002-11) |
| CDC-15228 | RWB-PLT-TE002-APP | CG-ALL-1541 | 18 | Align the REQ-DRI-006 test list with RWB-PLT-TE002-APP section 18 (TC-TE-002-01 to TC-TE-002-11) in the next version. |
| CDC-15245 | RWB-PLT-TE002-OPS | CG-ALL-1552 | 18 | Trace REQ-DRI-006 to TC-PLT-TE002-OPS-02 and TC-PLT-TE002-OPS-05, aligning it with §18 |
| CDC-15267 | RWB-PLT-TE003-APP-2 | CG-ALL-1580 | 18 | Align the REQ-DRI-007 test list and the one other differing requirement to section 18 of RWB-PLT-TE003-APP-2 (REQ-DRI-007: TC-PLT-TE003-APP2-02, TC-PLT-TE003-APP2-03). |
| CDC-15289 | RWB-PLT-TE003-APP | DOR-RWB-PLT-TE003-APP-12 | 16 | Trace REQ-DRI-007 to TC-TE-003-01 to TC-TE-003-07 and REQ-ACA-003 to TC-TE-003-08 and TC-TE-003-09, as in section 18 of RWB-PLT-TE003-APP. |
| CDC-15291 | RWB-PLT-TE003-APP | CG-ALL-1562 | 18 | Align the RTM trace of REQ-DRI-007 and REQ-ACA-003 to the section 18 test IDs of RWB-PLT-TE003-APP (TC-TE-003-01 to TC-TE-003-07; TC-TE-003-08 and TC-TE-003-09). |
| CDC-15307 | RWB-PLT-TE004-APP | CG-ALL-1602 | 18 | Align the REQ-RDF-010 test list with story section 18 (TC-TE-004-01 to TC-TE-004-07, TC-PLT-TE004-APP-09) in the next RTM version. |
| CDC-15438 | RWB-PLT-TE008-APP | CG-ALL-1608 | 18 | Align the REQ-DRI-003 test list with section 18 of this story |
| CDC-15447 | RWB-PLT-TE011-APP | DOR-RWB-PLT-TE011-APP-12 | 16, 18 | Align the test case lists for REQ-RDF-010, REQ-ACA-005 and the target elements with section 18 of this story. |
| CDC-15448 | RWB-PLT-TE011-APP | CG-ALL-1614 | 18 | Align the test lists for REQ-RDF-010 and REQ-ACA-005 with §18 of RWB-PLT-TE011-APP in the next RTM version. |
| CDC-15458 | RWB-PLT-TE012-APP | CG-ALL-1620 | 18 | Align the test lists of REQ-DCM-003 and REQ-DCM-002 with RWB-PLT-TE012-APP section 18 in the next RTM version |

### RWB-PLT-E1044-CON (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14104 | RWB-PLT-E1044-APP-2 | DOR-RWB-PLT-E1044-APP-2-21 | n/a | Reach build status Done; it is currently In build. |
| CDC-14105 | RWB-PLT-E1044-APP-2 | DOR-RWB-PLT-E1044-APP-2-22 | 12.8 | Publish a contract fake for rwb-source-data and record its library version, then name it in section 12.8. |
| CDC-14115 | RWB-PLT-E1044-APP-2 | GAP-1423 | 11 | Alert threshold and drift flag owner and values are now marked Not specified; the unsourced claims are removed. |
| CDC-14116 | RWB-PLT-E1044-APP-2 | GAP-2134 |  | No source names the mock product; the stub choice belongs to each provider's CON story, so this is not resolved here. |
| CDC-14120 | RWB-PLT-E1044-APP-2 | GAP-1420 |  | Fix the history table name as Flyway default flyway_schema_history in each service's own schema, and fix the migration-run record fields (service, schema, version, drift result, state). Keep flyway_schema_history_recovery only in RWB-PLT-E1044-APP. |
| CDC-14122 | RWB-PLT-E1044-APP | DOR-RWB-PLT-E1044-APP-21 | header | Complete the build of RWB-PLT-E1044-CON (currently In build) and publish the contract so its status is Done. |
| CDC-14123 | RWB-PLT-E1044-APP | DOR-RWB-PLT-E1044-APP-22 | header | Publish the contract fake library and record its published version in the contract story. |
| CDC-14124 | RWB-PLT-E1044-APP | DOR-RWB-PLT-E1044-APP-23 | header | Contract version row states v1 (from the /v1 path) and asks for confirmation against RWB-PLT-E1044-CON |
| CDC-14131 | RWB-PLT-E1044-APP | GAP-1421 | 12.9 | State that every service starts at V0001 in its own folder and that baselines have no cross-service order; publish the migration-run record fields with the service and schema keys. |
| CDC-14132 | RWB-PLT-E1044-APP | GAP-1422 | 12.9 | Publish the migration contract in the platform template repository next to the Flyway module; name the platform template as owner of the Flyway module; each service keeps only its migration folder and V0001 baseline. |
| CDC-14134 | RWB-PLT-E1044-APP | GAP-2134 | none | Stub server choice belongs to each provider's CON story per the directive; this story has no text on contract fakes to change. |
| CDC-14137 | RWB-PLT-E1044-APP | GAP-1420 | 8 | Fix the history table name as flyway_schema_history in the service's own schema and define the migration-run record fields. |
| CDC-14190 | RWB-PLT-E1044-CON | GAP-0548 | header | Keep wave 4 as the business epic EP08 tag; build Day 1; release the read path with the wave 1 rwb-source-data deploy; confirm release date at the wave entry check. |
| CDC-14193 | RWB-PLT-E1044-OPS | DOR-RWB-PLT-E1044-OPS-21 | header | Reach Done so the contract is published. Story now records the dependency and its In build status. |
| CDC-14204 | RWB-PLT-E1044-OPS | GAP-1421 | find it | State that each service starts at V0001 in its own folder, that baselines have no cross-service order, and publish the run-record fields with service and schema keys. |
| CDC-14205 | RWB-PLT-E1044-OPS | GAP-1422 | find it | Publish the contract document next to the Flyway module in the platform template repository; name the platform template as owner of the module; keep only the migration folder and V0001 baseline in each service. |
| CDC-14211 | RWB-PLT-E1044-OPS | GAP-1420 | none | Name the history table flyway_schema_history in each service's own schema and list the migration-run record fields; keep flyway_schema_history_recovery only in RWB-PLT-E1044-APP. |

### Epic design record (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14121 | RWB-PLT-E1044-APP | DOR-RWB-PLT-E1044-APP-14 | header | Confirm and record the signed sign-off of the epic design for RWB-PLT-TPL, then link it from this story. |
| CDC-14138 | RWB-PLT-E1044-CON | DOR-RWB-PLT-E1044-CON-14 | header | Record the signed epic design sign-off for RWB-PLT-TPL |
| CDC-15074 | RWB-PLT-N004-OPS | DOR-RWB-PLT-N004-OPS-14 | header | Record the signed epic design sign-off for RWB-PLT-TPL |
| CDC-15131 | RWB-PLT-NF01-OPS | DOR-RWB-PLT-NF01-OPS-14 | header | Record the signed sign-off of the epic design in the epic design record |
| CDC-15138 | RWB-PLT-NF03-OPS | DOR-RWB-PLT-NF03-OPS-14 | header | Record the signed epic design sign-off for RWB-PLT-TPL in the epic design record; no signed design is in the source set. |
| CDC-15143 | RWB-PLT-NF04-OPS | DOR-RWB-PLT-NF04-OPS-14 | header | Record the signed epic design sign-off in the epic design record so the story can cite it |
| CDC-15147 | RWB-PLT-NF05-OPS | DOR-RWB-PLT-NF05-OPS-14 | find it | Record the signed epic design sign-off for RWB-PLT-TPL |
| CDC-15188 | RWB-PLT-TE001-APP-2 | DOR-RWB-PLT-TE001-APP-2-14 | header | Record the signed epic design sign-off so that DoR item 14 can pass. |
| CDC-15204 | RWB-PLT-TE001-APP | DOR-RWB-PLT-TE001-APP-14 | header | Record the signed epic design sign-off for EP01-TE, then reference it from this story. |
| CDC-15232 | RWB-PLT-TE002-OPS | DOR-RWB-PLT-TE002-OPS-14 | header | Record the signed epic design sign-off for EP01-TE and RWB-PLT-TPL, since no signed epic design is in the story or source documents. |
| CDC-15247 | RWB-PLT-TE003-APP-2 | DOR-RWB-PLT-TE003-APP-2-14 | header | Record the signed epic design sign-off for RWB-PLT-TPL, then confirm it against this story. |
| CDC-15271 | RWB-PLT-TE003-APP | DOR-RWB-PLT-TE003-APP-14 | header | Record the signed epic design sign-off, then the story can cite it. |
| CDC-15426 | RWB-PLT-TE008-APP | DOR-RWB-PLT-TE008-APP-14 | Header | Record the signed sign-off for RWB-PLT-TE008-APP in the epic design record. |
| CDC-15440 | RWB-PLT-TE011-APP | DOR-RWB-PLT-TE011-APP-14 | find it | Record the signed epic design sign-off for EP01-TE. No sign-off appears in the story or source documents. |
| CDC-15450 | RWB-PLT-TE012-APP | DOR-RWB-PLT-TE012-APP-14 | header | Record the signed epic design sign-off for RWB-PLT-TPL. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14109 | RWB-PLT-E1044-APP-2 | CG-ALL-1496 | 16 | Add rows TC-PLT-E1044-APP2-01 to -06 under Story test cases, with Given, When and Then copied from AC1 to AC6. |
| CDC-14175 | RWB-PLT-E1044-CON | CG-ALL-1503 | 16 | Add rows for TC-PLT-E1044-CON-01 to -06 to the next Test Cases version with Given, When and Then copied from the criterion each covers. |
| CDC-14208 | RWB-PLT-E1044-OPS | CG-ALL-1511 | 16 | Add rows TC-PLT-E1044-OPS-01 to TC-PLT-E1044-OPS-06 with Given, When and Then copied from AC1 to AC6 of section 7 of this story. |
| CDC-15190 | RWB-PLT-TE001-APP-2 | CG-ALL-1528 | 16 | Add rows TC-PLT-TE001-APP2-01 to TC-PLT-TE001-APP2-05 with Given, When and Then copied from AC1 to AC5 in section 7. |
| CDC-15244 | RWB-PLT-TE002-OPS | CG-ALL-1551 | 16 | Add rows TC-PLT-TE002-OPS-01 to -05 with Given, When and Then copied from AC1 to AC5 |
| CDC-15250 | RWB-PLT-TE003-APP-2 | CG-ALL-1579 | 16 | Add rows TC-PLT-TE003-APP2-01 to -06 to Story test cases, with Given, When and Then copied from the criteria they cover (owner QA). |
| CDC-15266 | RWB-PLT-TE003-APP-2 | DOR-RWB-PLT-TE003-APP-2-12 | 16 | Add rows TC-PLT-TE003-APP2-01 to TC-PLT-TE003-APP2-06 with the Covers, Level and Data of section 16, and TC-PLT-TE003-APP2-07 (new, BR2). The section 18 list gap is under CG-ALL-1580. |
| CDC-15300 | RWB-PLT-TE004-APP | CG-ALL-1601 | 16 | Add the row TC-PLT-TE004-APP-09 with Given, When and Then copied from AC8 in the next Test Cases version. |
| CDC-15303 | RWB-PLT-TE004-APP | DOR-RWB-PLT-TE004-APP-12 | 12.7, 16, 18 | Add rows TC-PLT-TE004-APP-09 and TC-PLT-TE004-APP-10 under tab Story test cases |
| CDC-15430 | RWB-PLT-TE008-APP | CG-ALL-1607 | 16 | Add a row for TC-PLT-TE008-APP-10 with Given, When and Then copied from AC9. |
| CDC-15434 | RWB-PLT-TE008-APP | DOR-RWB-PLT-TE008-APP-12 | 16, 18 | Add TC-PLT-TE008-APP-10 and TC-PLT-TE008-APP-11 to tab Story test cases |
| CDC-15444 | RWB-PLT-TE011-APP | CG-ALL-1613 | 16 | Add a row for TC-PLT-TE011-APP-12 with Given, When and Then copied from AC11. |
| CDC-15453 | RWB-PLT-TE012-APP | CG-ALL-1619 | 16 | Add a row for TC-PLT-TE012-APP-14 with Given, When and Then copied from AC13. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14143 | RWB-PLT-E1044-CON | DOR-RWB-PLT-E1044-CON-1 | 1 | Add 'tech lead' as a role code or role name. |
| CDC-14200 | RWB-PLT-E1044-OPS | DOR-RWB-PLT-E1044-OPS-1 | 1 | Add role 'DevOps engineer of the platform' as a role code or name, or confirm the existing role it maps to. |
| CDC-15078 | RWB-PLT-N004-OPS | DOR-RWB-PLT-N004-OPS-1 | 1 | Add a role row for 'DevOps engineer' with its role code, or name the existing role code the story should use |
| CDC-15132 | RWB-PLT-NF01-OPS | DOR-RWB-PLT-NF01-OPS-1 | 1 | Add a role for DevOps engineer, or confirm the role code the story uses |
| CDC-15139 | RWB-PLT-NF03-OPS | DOR-RWB-PLT-NF03-OPS-1 | 1 | Add the DevOps engineer role with its role code, or confirm the existing role code and name for section 1. |
| CDC-15144 | RWB-PLT-NF04-OPS | DOR-RWB-PLT-NF04-OPS-1 | 1 | List the role 'platform engineer' as a role code or role name, or confirm the role code that section 1 should use |
| CDC-15241 | RWB-PLT-TE002-OPS | DOR-RWB-PLT-TE002-OPS-1 | 1 | Add a role code or role name 'DevOps engineer' for the DevOps role |
| CDC-15304 | RWB-PLT-TE004-APP | DOR-RWB-PLT-TE004-APP-6 | 10 | Add role SY-DATALOAD (data load identity, staging grant on the run's schemas, no live write outside the swap) |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14156 | RWB-PLT-E1044-CON | GAP-1206 | 13 | Update the dependency rows to six H rows and three C rows per the DP table; keep this story's metadata as the plan states until corrected. |
| CDC-14163 | RWB-PLT-E1044-CON | GAP-1343 | 13 | Publish the six DP-added dependencies (H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, C RWB-P4-E1037-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON) with this story as consumer. |
| CDC-14164 | RWB-PLT-E1044-CON | GAP-2501 | 13 | Record the DP-added H and C contracts as non-blocking platform and published contracts, built against their fakes. |
| CDC-14165 | RWB-PLT-E1044-CON | GAP-1223 | 3 | Read H as None plus the DP-named platform contracts; read C as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. |
| CDC-14166 | RWB-PLT-E1044-CON | GAP-2354 | 13 | Record the six platform CONs as wave-0 release train prerequisites; add RWB-P3-E1043-CON to contract rows of stories claiming DP-07. |
| CDC-14167 | RWB-PLT-E1044-CON | GAP-1291 | 13 | Record the DP-added H and C contracts as non-blocking platform and published contracts, built against their fakes. |
| CDC-14168 | RWB-PLT-E1044-CON | GAP-1295 | 3 | Read H as None plus the six DP-named platform contracts; read C as RWB-P10-E2028-CON plus C RWB-P3-E1043-CON and the published P3 case read and P4 authorise contracts. |
| CDC-14180 | RWB-PLT-E1044-CON | GAP-1337 | header | Carry the platform contracts and the rwb-case rule-package, parameters and reference-data contracts in the dependency map so sequencing is visible; metadata rows stay as the story object fixes them. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14106 | RWB-PLT-E1044-APP-2 | CG-ALL-1493 | 1, 8, 11, 12.7 | Record flyway_schema_history as a Flyway tool table outside the LDM and Data Classification, as the story already states. |
| CDC-14107 | RWB-PLT-E1044-APP-2 | CG-ALL-1494 | 2 | Record flyway_schema_history_recovery as the legacy Flyway tool table of RWB-E1-044 outside the LDM and Data Classification. |
| CDC-14108 | RWB-PLT-E1044-APP-2 | CG-ALL-1495 | 11 | Record information_schema as the database system catalog read by the drift gate, outside the LDM and Data Classification. |
| CDC-14139 | RWB-PLT-E1044-CON | CG-ALL-1502 | 1, 8, 12.7 | Record flyway_schema_history as a Flyway-managed table object in each service schema, not as a dictionary field. |
| CDC-14203 | RWB-PLT-E1044-OPS | DOR-RWB-PLT-E1044-OPS-7 | 11 | Register information_schema and flyway_schema_history as system catalog objects the deployment reads or writes. Section 11 data table added. |
| CDC-15429 | RWB-PLT-TE008-APP | CG-ALL-1606 | 2, 12.7, 19 | Add decision_record as a dictionary name, or record the per-service decision_record table as an object in the owning document. |
| CDC-15436 | RWB-PLT-TE008-APP | DOR-RWB-PLT-TE008-APP-7 | 11 | Add the decision_record entity (each service's rwb_<name> table) or name its mapped entity |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14125 | RWB-PLT-E1044-APP | CG-ALL-1486 | 11 | Record flyway_schema_history_recovery as a Flyway tool object outside the business model, or cite it in its owning document. |
| CDC-14126 | RWB-PLT-E1044-APP | CG-ALL-1487 | 11 | Record information_schema as a database system catalog object outside the business model, or cite it in its owning document. |
| CDC-14195 | RWB-PLT-E1044-OPS | CG-ALL-1509 | 11 | Record information_schema as a system catalogue object, or add the dictionary name the story uses. |
| CDC-14196 | RWB-PLT-E1044-OPS | CG-ALL-1510 | 12.7 | Record flyway_schema_history as a Flyway-managed table, or add the dictionary name the story uses. |
| CDC-15299 | RWB-PLT-TE004-APP | CG-ALL-1598 | 12.7 | Record tools.masked_copy_load (schema tools, outside the 19 service schemas) as a tool table with its fields, or name the object in the owning document. |
| CDC-15305 | RWB-PLT-TE004-APP | DOR-RWB-PLT-TE004-APP-7 | 11 | Add recovery_next and masked_copy_load as tool-only artefacts, or confirm them as outside the model; same check in Data Classification v5 |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14158 | RWB-PLT-E1044-CON | GAP-0568 | 13 | Publish login creation, credential policy, exact grant and revoke list with migration order; record RWB-PLT-E1044-CON as platform dependency of per-service database stories. |
| CDC-14171 | RWB-PLT-E1044-CON | GAP-1422 | none | Publish the migration contract document in the platform template repository beside the Flyway module; name the platform template as owner of the module; each service keeps only its migration folder and V0001 baseline. |
| CDC-15202 | RWB-PLT-TE001-APP-2 | GAP-1429 | find it | At the wave 0 template review, fix the module map path, the front-end module layout and the per-service package map; repositories inherit them. |
| CDC-15216 | RWB-PLT-TE001-APP | GAP-1430 | Not located | Name the per-service module map file, its directory and scope; RWB-PLT-N001-CON to publish the gateway-bff composite route list for the template to read. |
| CDC-15218 | RWB-PLT-TE001-APP | GAP-1429 | 12, 13 | Fix the module map path, the front-end module layout and the per-service package map before the first service repository is generated; every repository inherits them from the template. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14113 | RWB-PLT-E1044-APP-2 | DOR-RWB-PLT-E1044-APP-2-12 | 16, 18 | Register TC-PLT-E1044-APP2-01 to TC-PLT-E1044-APP2-06 in Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-14201 | RWB-PLT-E1044-OPS | DOR-RWB-PLT-E1044-OPS-12 | 16, 18 | Add TC-PLT-E1044-OPS-01 to -06 to Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-15199 | RWB-PLT-TE001-APP-2 | DOR-RWB-PLT-TE001-APP-2-12 | 16, 18 | Add TC-PLT-TE001-APP2-01 to -15 to Test Cases v8 tab Story test cases; align the section 18 test lists to RTM v7 |
| CDC-15242 | RWB-PLT-TE002-OPS | DOR-RWB-PLT-TE002-OPS-12 | 16, 18 | Add rows for TC-PLT-TE002-OPS-01 to -05 in Test Cases v8; align the §18 test lists in RTM v7 |

### OTHER:Environment and Deployment Design v5 (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15077 | RWB-PLT-N004-OPS | GAP-1668 | n/a | Record the four agreed environments (development, system integration, user acceptance, production) with one name pattern and one size table. |
| CDC-15080 | RWB-PLT-N004-OPS | GAP-1669 | 13 | Name the repository host, pipeline tool and artefact registry products and record them in the Environment and Deployment Design v5. No source names them (GAP-1669). |
| CDC-15135 | RWB-PLT-NF01-OPS | GAP-1669 | find it | Name the repository host, pipeline tool and artefact registry products; not specified in the source documents (GAP-1669). |
| CDC-15151 | RWB-PLT-NF05-OPS | GAP-1669 | find it | Name the repository host, pipeline tool and artefact registry products and record them |

### OTHER:Story set (next version) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14182 | RWB-PLT-E1044-CON | GAP-1277 | 13 | Carry the six platform H dependencies, one published C dependency and two service baselines in the dependency map as DP-added rows. Ready to start stays Day 1. |
| CDC-14183 | RWB-PLT-E1044-CON | GAP-1282 | 13 | Carry the six platform H dependencies and three published C dependencies in the dependency map as DP-added rows. Ready to start stays Day 1. |
| CDC-14184 | RWB-PLT-E1044-CON | GAP-1288 | 13 | Carry six platform H dependencies, two rwb-case C dependencies, the store baseline and the rwb-access authorise contract as DP-added rows. Ready to start stays Day 1. |

### OTHER:Story dependencies v5 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15203 | RWB-PLT-TE001-APP-2 | GAP-3234 | find it | On the Dependency classes sheet, record that platform technical-enabler work is team-type work: tracked, never blocking. Keep X on the ten rows. |
| CDC-15268 | RWB-PLT-TE003-APP-2 | GAP-3233 | find it | Keep the five Not carried rows visible, including RWB-TE-010 to RWB-TE-003 via RWB-ITG-TE010-ITG to RWB-PLT-TE003-APP-2. Add an X row only if the run books or harness wait for the named story. |
| CDC-15308 | RWB-PLT-TE004-APP | GAP-3233 | 18 | Keep the five version 4 dependencies visible as Not carried, including RWB-TE-009 to RWB-TE-004; add an X row only if the run books or the harness waits for the story. |

### RWB-PLT-TE003-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15273 | RWB-PLT-TE003-APP | DOR-RWB-PLT-TE003-APP-22 | header | Record the published contract fake library version for RWB-PLT-TE003-APP. |
| CDC-15295 | RWB-PLT-TE003-APP | GAP-1434 |  | Set the index folder, the gateway-bff x-module value and the aggregate report columns. Values not specified in the source documents (GAP-1434). |
| CDC-15296 | RWB-PLT-TE003-APP | DOR-RWB-PLT-TE003-APP-2 / GAP-3190 |  | The story does not divide the 79 operations across the 19 files. The split must be approved in the source documents first; no story edit. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14117 | RWB-PLT-E1044-APP-2 | GAP-3228 |  | Add a wave-0 window before 2 November 2026, or fold the 65 RWB-PLT wave-0 stories into Window 1 and extend that window. |
| CDC-15134 | RWB-PLT-NF01-OPS | GAP-3227 | find it | Set Release for RWB-PLT-N001 to RWB-PLT-N012, their CON variants and RWB-PLT-NF01 to RWB-PLT-NF08 to Window 1 (E1, 30 November 2026, tentative) or a stated wave-0 date. |

### OTHER:TSD P2 v3 (T3.1) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14119 | RWB-PLT-E1044-APP-2 | GAP-1992 |  | Remove outbox_event, outbox_delivery, processed_event, idempotency_key, feature_flag, feature_flag_change and efs_ledger_outcome from T3.1. Keep interface_config, job_catalog and outbound_item. Build the platform tables once in RWB-PLT-TE006-CON. |
| CDC-14136 | RWB-PLT-E1044-APP | GAP-1992 | none | Remove outbox_event, outbox_delivery, processed_event, idempotency_key, feature_flag and feature_flag_change; build them once in shared libraries (RWB-PLT-TE006-CON). Keep efs_ledger_outcome with P1. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14144 | RWB-PLT-E1044-CON | DOR-RWB-PLT-E1044-CON-12 | 16, 18 | Add TC-PLT-E1044-CON-01 to -06 as listed in story section 16 to Test Cases v8; align RTM v7 test lists with story section 18. |
| CDC-15456 | RWB-PLT-TE012-APP | DOR-RWB-PLT-TE012-APP-12 | 16 | Align RTM v7 test lists with section 18, and add the TC-PLT-TE012-APP-14 row to Test Cases v8. |

### RWB-PLT-N004-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15075 | RWB-PLT-N004-OPS | DOR-RWB-PLT-N004-OPS-22 | 12.8 | Record the contract fake library version it publishes, in its section 12.8 (Contract fakes). No source gives this version. |
| CDC-15076 | RWB-PLT-N004-OPS | DOR-RWB-PLT-N004-OPS-23 | header | State the contract version this story builds against. Only the /v1 REST path is in the sources, and it is not a contract version. |

### OTHER:Story dependencies v5 (Dependency classes sheet) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15229 | RWB-PLT-TE002-APP | GAP-3234 | header | Record that platform technical-enabler work is team-type work, tracked and never blocking; keep X on the ten rows. |
| CDC-15459 | RWB-PLT-TE012-APP | GAP-3234 | 18 | Record that platform technical-enabler work is team-type work: keep X on the ten rows, tracked, never blocking |

### RWB-PLT-TE002-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15230 | RWB-PLT-TE002-APP | GAP-1431 | header | Target repository layout and ruleset are derived in RWB-PLT-TE002-OPS; this story states them as not specified. |
| CDC-15231 | RWB-PLT-TE002-APP | GAP-3192 | 3 | Assumptions line no longer states one code owners file per repository as a target. |

### OTHER:(no target) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15233 | RWB-PLT-TE002-OPS | DOR-RWB-PLT-TE002-OPS-16 | section header | Size row set to the Not specified placeholder |
| CDC-15246 | RWB-PLT-TE002-OPS | GAP-1432 | section 8 | BR5 order reverted to the unordered check list; BR4 keeps the ruleset-name placeholder |

### OTHER:Contract fake library (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15249 | RWB-PLT-TE003-APP-2 | DOR-RWB-PLT-TE003-APP-2-22 | header | Publish the contract fake library version this story depends on, then record its version number. |
| CDC-15428 | RWB-PLT-TE008-APP | DOR-RWB-PLT-TE008-APP-22 | Header | Publish the contract fake library and record its version in this story's header. |

### OTHER:Template and Rules v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15269 | RWB-PLT-TE003-APP-2 | GAP-1433 | 11 | Specify the target file names and folder per service, the index format and the generated package names in the template. Keep the as-built names in the As built (monolith) appendix of RWB-PLT-TE003-APP. |
| CDC-15270 | RWB-PLT-TE003-APP-2 | GAP-1434 | 11 | Specify the index folder, the x-module value for gateway-bff operations and the aggregate report columns in the template. |

### RWB-PLT-E1043-CON; RWB-PLT-E1037-CON; RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15272 | RWB-PLT-TE003-APP | DOR-RWB-PLT-TE003-APP-21 | header | Publish the contract stories these depend on and move them to Done. |
| CDC-15441 | RWB-PLT-TE011-APP | DOR-RWB-PLT-TE011-APP-21 | find it | Publish the contracts and bring the contract stories to Done before this story starts. |

### OTHER:Story dependencies v5; OTHER:Dependency classes sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15294 | RWB-PLT-TE003-APP | GAP-3234 | Header | Keep X on the ten rows and record that platform technical-enabler work is team-type work: tracked, never blocks. |
| CDC-15449 | RWB-PLT-TE011-APP | GAP-3234 | 18 | On check row X, record that platform technical-enabler work is team-type work: tracked, never blocking. Keep X on the ten rows. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15297 | RWB-PLT-TE004-APP | CG-ALL-1599 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation. |
| CDC-15298 | RWB-PLT-TE004-APP | DOR-RWB-PLT-TE004-APP-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |

### RWB-P3-E1043-CON; RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15442 | RWB-PLT-TE011-APP | DOR-RWB-PLT-TE011-APP-22 | find it | Publish the contract fake library and record its published version. |
| CDC-15443 | RWB-PLT-TE011-APP | DOR-RWB-PLT-TE011-APP-23 | find it | Fix and state the contract version this story builds against; the story currently gives only the /v1 path. |

### RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-E1071-CON; RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15451 | RWB-PLT-TE012-APP | DOR-RWB-PLT-TE012-APP-21 | 12 | Publish the contract for this legacy key once the CON stories it depends on are Done. |
| CDC-15452 | RWB-PLT-TE012-APP | DOR-RWB-PLT-TE012-APP-22 | 12 | Record the published contract fake library version that this story uses. |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20886 | RWB-PLT-NF03-OPS | R-23300 |  | Document not read: no Bash tool here to run docview.py, and Read cannot open the .docx. Re-run with shell access. |
| CDC-20887 | RWB-PLT-NF05-OPS | R-23285 |  | Document not read: no Bash tool here to run docview.py, and Read cannot open the .docx. Re-run with shell access. |

### Epic design record; OTHER:RWB-PLT-TPL) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14103 | RWB-PLT-E1044-APP-2 | DOR-RWB-PLT-E1044-APP-2-14 | n/a | Record the signed epic design sign-off for RWB-PLT-E1044-APP-2. |

### OTHER:Feature and L3 process source (not in this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14114 | RWB-PLT-E1044-APP-2 | DOR-RWB-PLT-E1044-APP-2-2 | 18 | Feature and L3 process cells kept as Not specified placeholders |

### RWB-PLT-E1044-CON; RWB-PLT-E1044-OPS; OTHER:Template and Rules v1 (section R3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14133 | RWB-PLT-E1044-APP | GAP-1423 | 12 | Publish job-run record fields in CON; fix one alert per failed run per service in OPS; assign flag rwb.p3.migration-drift-gate to the platform library owner with legacy values unchanged (on in SIT, UAT, PROD; off in DEV). |

### OTHER:v6 By window (Window 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14135 | RWB-PLT-E1044-APP | GAP-3228 | none | Add a wave-0 review window before 2 November 2026 for the 65 wave-0 RWB-PLT platform stories. |

### OTHER:Data Migration Approach (v3) section 5 and plan/split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14146 | RWB-PLT-E1044-CON | GAP-0236 | find it | Record the owner-side load of each service as that service's own Flyway step under RWB-PLT-E1044-CON, run in the cutover step with its P1 extract story. No new story ID. |

### OTHER:Data Migration Approach and the rwb-payment proceeds schema for RWB-DM-013 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14147 | RWB-PLT-E1044-CON | GAP-2533 | find it | Publish the DM-013 handover file with count, checksum and per-row stamp, name a load command with run record, add a provenance column, and keep the legacy amount and received date with provenance. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14148 | RWB-PLT-E1044-CON | GAP-1946 | find it | Keep the H and C lists at None, record the nine platform and rwb-case CONs as wave-0 prerequisites, and read the ACE check as the DP06 data product under R3 precedence. |

### RWB-P6-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14149 | RWB-PLT-E1044-CON | GAP-1167 | find it | Keep H as an empty list and record the seven platform CONs as wave-0 build prerequisites in the dependency map, without changing lane depth. |

### RWB-P6-E1019-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14150 | RWB-PLT-E1044-CON | GAP-1174 | find it | Add the four platform contracts and the two P3 contracts to the RWB-P6-E1019-APP dependency rows, or record them in the platform release train. |

### RWB-S8-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14151 | RWB-PLT-E1044-CON | GAP-3075 | find it | Platform owner confirms which of the eight platform contracts publish before release. Assembler corrects the metadata rows if the plan is reissued. |

### OTHER:Work Package for the P5 story row (WP story line H; OTHER:C; OTHER:I; OTHER:X) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14152 | RWB-PLT-E1044-CON | GAP-2448 | find it | Keep the metadata rows as fixed, and record the DP-table dependencies in section 13 of that story, built against fakes on Day 1. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14153 | RWB-PLT-E1044-CON | GAP-1198 | 13 | Add platform contracts RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON and P3 contracts RWB-P3-E1042-CON, RWB-P3-E1043-CON to its dependency rows. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14154 | RWB-PLT-E1044-CON | GAP-2414 | 13 | Read the H list as None plus the eight platform contracts named in the DP table, and the C list as RWB-P3-E2041-CON plus the four named published contracts. |

### OTHER:FSD P7 v3 and TSD P7 v3 (template_use record; RWB-P6-E1046-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14155 | RWB-PLT-E1044-CON | GAP-2453 | 13 | Settle one template_use record side of the P6 key, publish the template and catalog reads in RWB-P6-E1046-CON, and fix the P7 table, columns and migration. |

### OTHER:FSD P4 and TSD P4 (REQ-ACA-006; OTHER:NFR-042); RWB-P10-E1063-CON; OTHER:rwb-access matrix load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14157 | RWB-PLT-E1044-CON | GAP-2333 | 13 | Keep both Reporting rights; replace the lake copy of the access rule with the served read's access entry; correct REQ-ACA-006 and NFR-042; add the listed H and C rows in the plan. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; RWB-P7-E1073-CON; OTHER:rwb_integration DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14159 | RWB-PLT-E1044-CON | GAP-0672 | 13 | Record eight DP H rows as wave-0 prerequisites; publish the model fetch in RWB-P7-E1073-CON; fix the local copy table and name the login before the baseline. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14160 | RWB-PLT-E1044-CON | GAP-1328 | 13 | Complete the metadata rows from the DP table, or state in R5.5 that platform H and self-referential C rows are held by platform and contract stories. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14161 | RWB-PLT-E1044-CON | GAP-2470 | 13 | Complete the metadata rows from the DP table, or state in R5.5 that platform H and self-referential C rows are held by platform and contract stories. |

### RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14162 | RWB-PLT-E1044-CON | GAP-2475 | 13 | Add the DP-added platform H rows, C rows and the workflow-kit dependency to the metadata, or state in R5.5 that they are held by the platform and contract stories. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:D1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14169 | RWB-PLT-E1044-CON | GAP-2317 | 13 | Add H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON and C RWB-P3-E1043-CON to the dependency map. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14170 | RWB-PLT-E1044-CON | GAP-2419 | 3 | Add an authorise operation row for the P4 platform guard; replace the agent contract fake with RWB-P10-TE013-CON when it lands. |

### RWB-PLT-E1044-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14172 | RWB-PLT-E1044-CON | GAP-1423 | 15 | Record fields, flag owner and alert threshold marked Not specified in section 15; the flag owner is not assigned. |

### OTHER:Delivery plan v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14173 | RWB-PLT-E1044-CON | GAP-3228 | none | Add a wave-0 review window before 2 November, or fold the 65 RWB-PLT platform stories into Window 1 and extend Window 1. |

### RWB-P1-E1069-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14174 | RWB-PLT-E1044-CON | GAP-0556 | none | Publish the customer and party answer schema with field names and not-found and stale shapes; record APP and DB as preconditions in the Dependency Map without an H edge; fix the read-path switch key and off behaviour in the Service Template Specification. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14177 | RWB-PLT-E1044-CON | GAP-2455 | 12.7 | Confirm that rwb-decision appends every DecisionRecorded fact of every service to decision_log_entry; the producer's local record is the working record and the ledger entry is the record of record; RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0 and wave-1 baseline outside H. |

### RWB-P6-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14178 | RWB-PLT-E1044-CON | GAP-1212 | header | Add the eight DP-added rows to the plan dependency lists, or record the five platform contracts and gateway route as wave-0 service template baseline and the two P3 reads as answered by contract fakes until published. |

### OTHER:Lane document (CG-W0 lane) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14179 | RWB-PLT-E1044-CON | GAP-1218 | header | State that the platform CONs of the DP table are wave-0 prerequisites carried outside H for every wave-1 APP story; Ready to start stays Day 1 under section R5.7 rule 1. |

### RWB-S8-E2012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14181 | RWB-PLT-E1044-CON | GAP-3091 | 13 | Track the eight platform H rows in section 13. Keep Depends on (build) None and Ready to start Day 1 as the split plan gives them. |

### OTHER:Wave 2 planning gate (story set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14185 | RWB-PLT-E1044-CON | GAP-2312 | 13 | Confirm at the wave 2 gate that no H chain is missing from the lane. Keep Depends on (build) None and the RWB-P8-E2027-CON contract as the WP fixes them. |

### OTHER:Build sequence (Work Package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14186 | RWB-PLT-E1044-CON | GAP-2410 | 13 | Record that a secondary slice builds against platform contracts and published fakes and reads same-service wave-1 rows through its own schema, within R5.7 rule 5 lane depth. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14187 | RWB-PLT-E1044-CON | GAP-1296 | 13 | Keep metadata as written. Carry the eight platform H and three C DP-added dependencies in section 13 as build-against rows. Ready to start stays Day 1. |

### RWB-P3-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14188 | RWB-PLT-E1044-CON | GAP-2398 | 13 | Keep the WP metadata rows as given. Carry the eleven added rows in the DP application of sections 13 and 18. Ready to start stays Day 1. |

### OTHER:TSD P2 v3 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14189 | RWB-PLT-E1044-CON | GAP-1992 | 13 | Remove outbox_event, outbox_delivery, processed_event, idempotency_key, feature_flag and feature_flag_change from T3.1 (built once in RWB-PLT-TE006-CON); move efs_ledger_outcome to P1 ownership. |

### OTHER:Template and Rules v1 R5.7 rule 8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14191 | RWB-PLT-E1044-CON | GAP-0555 | header | State that Ready to start is computed from the dependency graph only, so a wave 4 business-epic story with platform CON build edges may be picked up on Day 1; the wave tag stays a business-epic tag. |

### RWB-PLT-E1044-OPS; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14192 | RWB-PLT-E1044-OPS | DOR-RWB-PLT-E1044-OPS-14 | 14 | Record the signed epic design sign-off for EP01 in the epic design record and cite that record in this story. |

### OTHER:Contract fake library (rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14194 | RWB-PLT-E1044-OPS | DOR-RWB-PLT-E1044-OPS-22 | 12.8 | Publish the rwb-source-data contract fake and record its library version. |

### OTHER:Provider CON story of each service (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14206 | RWB-PLT-E1044-OPS | GAP-2134 | none | Name the stub server generated from the published contract that runs in the pipeline, as the CON story of each provider chooses it. |

### OTHER:Recovery Workbench v6 By window (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14207 | RWB-PLT-E1044-OPS | GAP-3228 | none | Add a wave-0 review window before 2 November 2026 for the 65 RWB-PLT wave-0 platform stories. |

### OTHER:TSD P2 v3; OTHER:T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14210 | RWB-PLT-E1044-OPS | GAP-1992 | none | Remove outbox_event, outbox_delivery, processed_event, idempotency_key, feature_flag and feature_flag_change; build them once in RWB-PLT-TE006-CON; keep efs_ledger_outcome with P1. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:identified by content, not confirmed by the register) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15079 | RWB-PLT-N004-OPS | GAP-1424 | none in this story | Publish the chart name, the chart repository, the container registry and image naming, the api and worker resource defaults with per-service overrides, the KEDA ceiling and backlog threshold per service, the CI toolchain and scanner set, the promotion gate and approver role for DEV, SIT, UAT and PROD, and the chart and template version scheme with pinning format; confirm with the platform administrator and DevOps lead before the chart is Published and before the canary runs. |

### OTHER:Recovery Workbench Technical Specifications by Module v6 (T0 Service section) or a PLT module file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15133 | RWB-PLT-NF01-OPS | GAP-1664 | header | Write the platform functional specification and map FR-PLT-001 to FR-PLT-034 to requirement IDs |

### OTHER:Template and Rules §R5.6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15136 | RWB-PLT-NF01-OPS | GAP-3199 | find it | State the epic-wave rule: epic wave = earliest wave among its stories, with the service wave shown beside it. |

### OTHER:Recovery Workbench capacity plan workbook v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15140 | RWB-PLT-NF03-OPS | GAP-0277 |  | Add a sheet Service volumes with one row per each of the 19 services: driver, 2027 volume by formula from existing sheets, unit, basis cell, topic, task queue and consumers. Totals on existing sheets unchanged. |

### OTHER:Environment pack agreed with platform administrator and solution architect (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15141 | RWB-PLT-NF03-OPS | GAP-1426 |  | Supply hosts, subscriptions, resource groups, regions, Temporal sizes, namespace key stores, ACE logins, pool caps and replica counts for DEV, SIT, UAT and PROD before first promotion. |

### OTHER:ACE team with SCB IT (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15142 | RWB-PLT-NF03-OPS | GAP-2127 |  | Provide pod sizes, connection cap per login and SIT test tool so section 2 can state them in place of the R9 placeholder. |

### RWB-PLT-NF05-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15148 | RWB-PLT-NF05-OPS | DOR-RWB-PLT-NF05-OPS-21 | find it | Contract dependency row now reads not specified, not the contract key. |

### OTHER:Contract fake library publication record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15149 | RWB-PLT-NF05-OPS | DOR-RWB-PLT-NF05-OPS-22 | find it | Record the published contract fake library version |

### OTHER:Contract version record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15150 | RWB-PLT-NF05-OPS | DOR-RWB-PLT-NF05-OPS-23 | find it | The story states the version is not specified; fixing the contract version belongs to the contract document. |

### RWB-PLT-E1043-CON; RWB-PLT-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15189 | RWB-PLT-TE001-APP-2 | DOR-RWB-PLT-TE001-APP-2-21 | section header | Contract dependencies row now names the two CON contracts that AC12 relies on; no CON dependency claim. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15198 | RWB-PLT-TE001-APP-2 | DOR-RWB-PLT-TE001-APP-2-10 | 15 | SCR-44 states written as Not specified placeholders citing CG-ALL-1539 |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15201 | RWB-PLT-TE001-APP-2 | GAP-1430 | find it | Name the per-service module map file in the template; RWB-PLT-N001-CON publishes the gateway-bff composite route list, which the template reads from the contract. |

### RWB-PLT-E1027-CON; RWB-PLT-E1043-CON; RWB-PLT-E1037-CON; RWB-PLT-TE006-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15205 | RWB-PLT-TE001-APP | DOR-RWB-PLT-TE001-APP-21 | Header | Publish the contract stories listed in Depends on (build) so that they reach Done. |

### OTHER:Repository governance record for the 20 repositories (DevOps) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15217 | RWB-PLT-TE001-APP | GAP-1432 | Not located | Set one team handle per owning team as @scb-ace/<team-handle>; one ruleset per repository on the protected branch; required checks: RWB-PLT-NF05-OPS quality gates, then the RWB-PLT-TE001-APP module boundary test. |

### OTHER:Story dependencies v5 (Dependency classes sheet, check row X) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15219 | RWB-PLT-TE001-APP | GAP-3234 | header | Keep X on the ten App development rows and record that platform technical-enabler work is team-type work: tracked, never blocks. |

### RWB-PLT-TE003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15248 | RWB-PLT-TE003-APP-2 | DOR-RWB-PLT-TE003-APP-2-21 | header | Create contract story RWB-PLT-TE003-CON and add it as a CON dependency in Contract dependencies of RWB-PLT-TE003-APP-2. |

### RWB-PLT-TE001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15290 | RWB-PLT-TE003-APP | DOR-RWB-PLT-TE003-APP-17 | Header | RWB-PLT-TE001-APP is named as the external dependency in the header. It stays pending until it is built, so no story edit. |

### OTHER:Story dependencies v5, legacy dependency trace sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15292 | RWB-PLT-TE003-APP | GAP-3233 | Header | Keep the RWB-TE-010 to RWB-TE-003 row (RWB-ITG-TE010-ITG) visible as Not carried; add an X row only if run books or the harness waits for RWB-TE-003. |

### OTHER:Performance mix in RWB-TE-009 (steps 5 to 8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15293 | RWB-PLT-TE003-APP | GAP-3191 | Header | Map each of the 7 operations to its owner service from the OperationCatalog of RWB-PLT-TE003-APP before the first gated run; keep the operations, weights and limits. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15306 | RWB-PLT-TE004-APP | GAP-0379 | 11 | Publish before the first SIT masked copy: table-to-schema map, verifier owner across 19 schemas, partial-failure rule, PII extract contract |

### RWB-PLT-E1027-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-E1071-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15427 | RWB-PLT-TE008-APP | DOR-RWB-PLT-TE008-APP-21 | Header | Bring the CON stories this story depends on to Done so the contract is published. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15433 | RWB-PLT-TE008-APP | DOR-RWB-PLT-TE008-APP-11 | 12 | Reclassify the P2 fields this story carries as personal data, or align the no-personal-data statement with the classification. |

### RWB-PLT-E1071-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15437 | RWB-PLT-TE008-APP | GAP-1437 | 11 | Schedule ID, catch-up and run-record retention are set by the E1071-CON catalog, which is not yet published. The story records the ingest state and ACE path only. |

### OTHER:Squad order, version 3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15439 | RWB-PLT-TE008-APP | GAP-3241 | find it | Keep items 19 and 21 with no story against them; repoint dependencies on RWB-TE-007 to RWB-PLT-E1071-CON |

### OTHER:Recovery Workbench document set: story RWB-E1-007 (secondary P5 slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15457 | RWB-PLT-TE012-APP | GAP-1027 | none | Treat the slice as new work with six new criteria and no legacy AC; take the manifest and claim-check names from RWB-P2-E1007-CON; read the type code and retention class from document_type, leaving the outbound type row to the type-table load placeholder; anchor document.case_id on the store request case ID and carry the 85 case IDs in the manifest; set CLAIM_CHECK_MINUTES = 15 from Arch v5 slide 11; build and test against the RWB-P5-E1024-APP store fake, the rwb-case contract fake and the RWB-PL fake. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0236 | The owner-side migration step has no story ID | TechX | Resolved (directive) |
| GAP-0277 | The forecast is written for one monolith and has no per-service volumes | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0379 | The per-schema table list of the masked copy, the owner of the verifier across the 19 schemas and the PII extract contract are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0380 | Chain-check scope across services, the ingest watermark and the Compliance route are not defined for the target | Tech lead | Resolved (directive) |
| GAP-0490 | The write-once archive contract (container, path and manifest) belongs to RWB-PLT-TE012-APP and is not specified | Solution architect | Resolved (directive) |
| GAP-0548 | A Day-1 story is tagged wave 4 while its service is wave 1 and the account read is needed by the wave 1 case screens | Tech lead | Resolved (directive) |
| GAP-0555 | A wave 4 story is marked Ready to start Day 1 on a platform Flyway contract, and the readiness rule does not name the case | Programme manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0556 | The read operation, its request and answer field names, and the feature switch of the read path are owned elsewhere or named by no source, while the story must still build and be switched | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0568 | rwb-source-data database slice: who creates the login and holds its credential, the exact grant names, the position of the three grant migrations on the sequence, and the platform sequence dependency of a Day-1 database story are not specified | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0916 | The per-service database login name of rwb-access is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1027 | The secondary P5 slice of RWB-E1-007 has no legacy AC and several document-hub values of the outbound path are not fixed in the sources | Solution architect (P5 document hub, with the rwb-integration contract owner) | Resolved (directive) |
| GAP-1031 | The storage account, the container names and the WORM policy of the platform storage product are not fixed in the sources | SCB IT infrastructure | Resolved (directive) |
| GAP-1041 | The rwb-document login name and its grants are not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1385 | The environments that receive the 19 schemas in wave 0 and the role that runs the script there are not specified | ACE DBA | Resolved (directive) |
| GAP-1391 | Where the grant check runs, what it publishes and how long the result is kept are not specified | DevOps lead | Resolved (directive) |
| GAP-1420 | Per-service Flyway history table name and migration-run record fields are not specified | Platform template owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1421 | Baseline order and sequence start across the 19 services are not specified | Solution architect | Resolved (directive) |
| GAP-1422 | Contract artefact location and owner of the Flyway configuration module are not specified | Platform template owner | Resolved (directive) |
| GAP-1423 | Job-run record fields, alert threshold and owner of the drift feature flag after the split are not specified | DevOps lead | Resolved (directive) |
| GAP-1424 | The chart name and registry, the resource sizes, the KEDA thresholds, the toolchain, the promotion gates and the chart version scheme are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1425 | The NF-01 legacy story text, the exact repository layout, the branch policy, the toolchain and the template version scheme are not in the source set | Solution architect | Resolved (directive) |
| GAP-1426 | The legacy NF-03 story text is absent from the source set, and the hosts, subscriptions, sizing, data refresh cadence and environment owners of the four environments are stated nowhere | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1427 | The NF-04 legacy story text is absent, and the key-store naming, rotation values, secret owners and configuration key names are not specified | Solution architect | Resolved (directive) |
| GAP-1428 | The NF-05 legacy story text is absent, and the gate thresholds, the tool products, the exception expiry and the reporting surface are not specified | Solution architect | Resolved (directive) |
| GAP-1429 | The target module-map location, the front-end module layout and the per-service package map are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1430 | The per-service module-map file name and the gateway-bff composite route list are not specified | Solution architect | Resolved (directive) |
| GAP-1431 | The target repository layout and the target branch ruleset of a service repository are not specified | Solution architect | Resolved (directive) |
| GAP-1432 | The team handles, the ruleset name and the required-check list and its order are not specified | DevOps lead | Resolved (directive) |
| GAP-1433 | Target API file layout, index format and per-service generated package names are not specified for the preserved contract-test story | Solution architect | Resolved (directive) |
| GAP-1434 | Index location, gateway-bff x-module value and the report format across the 19 pipelines are not specified for the delta story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1435 | The per-service staging schema, the per-service extract layout, the personal-data field registry operation and the tool schema are not defined for the 19-schema masked copy | Solution architect | Resolved (directive) |
| GAP-1436 | One rule set, one pinned dictionary version, its read path and the allow-list approver after the marks became reference data | Solution architect | Resolved (directive) |
| GAP-1437 | Owner, instance, run-record surface and reporting of the daily decision log hash-chain check after the split | Solution architect with RW-COMPLY | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1438 | One storage set or one per service, the container naming standard, the home of the retention period and the retention classes, the name of the retention Schedule and the readiness surface are not fixed once only rwb-document may reach the containers | Solution architect | Resolved (directive) |
| GAP-1664 | No FSD module exists for the platform, so no FSD requirement ID states a platform capability | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1668 | The environment set, its names and its sizing are not stated | Solution architect | Resolved (directive) |
| GAP-1669 | The repository and pipeline product is not named in any source | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1992 | TSD P2 names platform tables and one P1 table as its own | Solution architect | Resolved (directive) |
| GAP-2127 | No per-service size, connection cap or test tool for SIT | ACE team with SCB IT | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2134 | No source states which product hosts the contract fakes | TechX | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2533 | rwb-payment cutover load of RWB-DM-013: the handover file, the load command and its run record, a provenance column, the legacy payment_code column and the two schema-level H rows are fixed by no single source, and this slice owns no legacy criterion | Data steward and solution architect of rwb-payment, with the rwb-source-data owner, the schema baseline owner and the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3170 | The masked copy story writes the tables of three services from one platform story | Platform lead | Resolved (directive) |
| GAP-3190 | The 79 specified operations are not divided between the 19 API files | TechX | Resolved (directive) |
| GAP-3191 | The performance mix does not name the owning service of its 7 operations | QA team | Resolved (directive) |
| GAP-3192 | One code owners file or one per repository is not stated | DevOps team | Resolved (directive) |
| GAP-3199 | The epic wave is not defined for an epic whose stories span several business-epic waves | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3227 | The 23 new wave-0 platform stories have no release date | Delivery lead | Resolved (directive) |
| GAP-3228 | No review window covers the wave-0 platform block | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3234 | Ten class X rows point at a platform application story rather than at a DB, INF or OPS story | TechX (platform) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3241 | Two items that version 3 still orders are retired by D-RCV-60, and no source states what a squad does with a retired item in the order | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3251 | Non-feature tasks NF-01..NF-08 have no story master | Delivery lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-PLT-E1044-APP | new AC without TC row | 267 | AC10 is new and no section 16 row covers it |
| RWB-PLT-E1044-APP | new AC without TC row | 267 | AC11 is new and no section 16 row covers it |
