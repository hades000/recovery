# RWB-SVC-P5 rwb-document (Document) - review pack, part 1 of 6 (RWB-P5-AD021-APP to RWB-P5-E1024-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 175 |
| Cross-document (pending in another document) | 158 |
| Not applied (value not in the sources) | 12 |
| Open business decisions | 36 |
| Register gaps linked | 109 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P5-AD021-APP | 17 | 10 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 AD021 APP Retention classes and legal hold v2.md |
| RWB-P5-AD021-CON | 18 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 AD021 CON Retention classes and legal hold - contract v2.md |
| RWB-P5-E1007-APP | 30 | 33 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1007 APP Integration adapters for outbound files v2.md |
| RWB-P5-E1016-APP | 19 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1016 APP Access control per data product and catalog entries v2.md |
| RWB-P5-E1017-APP | 23 | 19 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1017 APP Retention and archive rule for the data store v2.md |
| RWB-P5-E1018-APP | 20 | 25 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1018 APP Case ID issuance and case record v1 v2.md |
| RWB-P5-E1021-APP | 23 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1021 APP Transfer rules and engine v1 v2.md |
| RWB-P5-E1024-APP | 25 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P5 rwb-document (Document)/RWB P5 E1024 APP Document store and index v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P5-AD021-CON | R-01464 | CG-ALL-5715 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-RETENTION-ACTION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-AD021-CON | R-01465 | CG-ALL-5716 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-RETENTION-ACTION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-AD021-CON | R-01466 | CG-ALL-5717 | Script gap | Product owner | The story adds LEGAL10Y to the closed list LOV-RETENTION-END | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-AD021-CON | R-01467 | CG-ALL-5718 | Script gap | Product owner | The story adds GENERAL05Y to the closed list LOV-RETENTION-END | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1017-APP | R-01480 | CG-ALL-5764 | Script gap | Product owner | The story adds DOCRET to the closed list LOV-RETENTION-ACTION | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-E1018-APP | R-01483 | CG-ALL-5774 | Script gap | Product owner | The story adds WAITING_COURT to the closed list LOV-CASE-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1041-APP, RWB-P5-E1041-CON | R-09222 | GAP-1581 | Register gap | Solution architect with Legal counsel | Legal hold REQ-DCM-016 has no FSD feature, the hold API belongs to P3, and the delivery story sits in Epic 8 | The PRD states the hold as a P5 product behaviour driven by the hold P3 records (FR-P5-025), slices it to wave 4 with RWB-AD-021, and keeps the retention class and the scan in wave 1. The BRD and the story set need one position on the wave. |
| RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1041-APP, RWB-P5-E1041-CON | R-09223 | GAP-1584 | Register gap | Compliance and PDPA officer | Retention periods are not set while the acceptance criteria assert named retention classes | The PRD requires a class on every document and a period from the retention table, treats the class names in the criteria as examples of a reference-table version, and carries the periods as OQ-P5-10. The retention rule field list and the approved periods are needed before wave 1 acceptance. |
| RWB-P5-AD021-APP | R-10819 | CG-ALL-5711 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1007-APP | R-10829 | CG-ALL-5747 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1016-APP | R-10832 | CG-ALL-5759 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1017-APP | R-10834 | CG-ALL-5770 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P5-E1024-APP | R-10844 | CG-ALL-5799 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-21888 | GAP-1545 | Register gap | Compliance | The debt buyer tape is required to be masked before the data room, and to carry the personal data the sale terms allow | The tape carries only the fields the sale terms and the approved mask list allow, and the mask list is a reference-data row owned by Compliance under DL26; the PRD states the rule and leaves the field list open. |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-21966 | GAP-1501 | Register gap | Compliance and PDPA officer | Field-level masking rules belong to the access service, while the FSD loads them here | This service keeps data_product_access (role, product, read right) and applies the masking policy of rwb-access, cached per the platform pattern; the masking rows themselves are rwb-access's. Confirm the split with Compliance and Security before the first masking test. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P7-E1017-APP | R-21967 | GAP-2070 | Register gap | Service owners P7 rwb-decision, P1 rwb-source-data and P4 rwb-access with Compliance | Where the retention period of the ledgers and the access log is held, and which job enforces it | Keep every period as written and mark the owner open: P7 enforces the ledger period, P1 the interaction ledger and P4 the access log, each as a row of its own retention data, until Compliance states where the periods are held. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21971 | GAP-1500 | Register gap | Compliance and PDPA officer | The retention rule table and the archive job move to the document service, while the FSD keeps both here | This service declares the retention class per data product and recovery table as versioned reference data, refuses a rule that names a read-only ACE view or the decision log, and archives nothing itself; the rule table and the monthly archive run belong to rwb-document. Confirm with Compliance that a class declared here and applied there is acceptable for the PDPA position. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E1021-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-22012 | GAP-3078 | Register gap | P7 rwb-decision owner with the business owner of module S8 | The TRANSFER rows that fire on the deviation triggers and the text of R-DEV-04 to R-DEV-06 are not published | The rule owner publishes the DEV transfer rows and the text of R-DEV-04 to R-DEV-06 with the package version; the story then reads them unchanged and no code changes. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P5-E1041-APP | R-23065 | GAP-1025 | Register gap | Solution architect, with the Compliance and PDPA officer role owner and the P3 and P5 service owners | The retention-class and legal-hold read surface of rwb-document has no operation, no shape and no document-level hold in any source, and the case and reference contracts it consumes are not in the story's contract list | Read recovery_case.legal_hold through the P3 case contract on every read and project it onto the document as legalHold and legalHoldRef, with no hold table and no hold write in rwb_document; keep the plan's C list as None, build against the three P3 fakes and record the missing rows for step D1; fix the four read paths, their queries and their answers in the RWB-P5-AD021-CON baseline and treat them as not specified in the sources; keep every period, age basis and end action as a class-load data row of RWB-P5-E1041-APP and let a missing class fail as 422 rather than default; read the retention_action rows and the DOCRET reference the run wrote and start, stop or re-run nothing, since JOB-17 belongs to RWB-P5-E1017-APP. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-28455 | GAP-1548 | Register gap | Compliance | No retention period is set for an outbound item, a delivery record or the transmission evidence of a file | The PRD states the retention of P2 transmission records as open under DL26 with the section R9 placeholder, and requires only that a resend and its audit record outlive the retention period of the case they belong to. |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-28495 | GAP-1510 | Register gap | Compliance with Security | The classification scheme per data product and the retention periods are open, so the PRD labels are a reading of the field markers | Apply the four-label scheme from the field markers now: personal fields and the party and contact extension rows as personal data, balances and amounts as sensitive financial data, case, legal, collateral and metadata as confidential, and no data product as public. Replace with the approved scheme when DL26 closes. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-28498 | GAP-1618 | Register gap | Compliance and PDPA officer | The decision log and the ledger carry no retention period, and the WORM seal period is unstated | Set the decision-log class period and the seal period under DL26 before the first release, keep the class per record class in reference data, and state in the retention rule that no archive runs inside this service. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1034-ITG, RWB-PLT-TE012-APP, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1041-APP, RWB-P6-AD017-APP, RWB-P6-E1034-APP | R-35419 | ASM-2709 | Register assumption |  | The values of the Non-Functional Specification v3 are the values this PRD is written against, with the status each one carries. A value marked Proposed is used as written until its owner confirms it under the decision named; a value marked Open is recorded as not set. | Solution architect with Risk at DL11 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P5-AD021-APP | R-17063 | DOR-RWB-P5-AD021-APP-10 | 12.9; 15 | Definition of Ready item 10 Screens and states: Partial | Empty, loading, error and no-access states for SCR-31 and SCR-32 sit in sections 12.9 and 15, outside this chunk. Cannot be written without that text. |
| RWB-P5-AD021-APP | R-17064 | DOR-RWB-P5-AD021-APP-11 | 13 | Definition of Ready item 11 Guardrails: Partial | Per-field personal-data classes sit in section 13 text outside this chunk. Cannot correct the P2 field classes without that field text. |
| RWB-P5-E1007-APP | R-06075 | DOR-RWB-P5-E1007-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record ID in the story or sources searched. Sign-off needs an invented reference, so the story is unchanged. |
| RWB-P5-E1007-APP | R-06078 | DOR-RWB-P5-E1007-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version in the story or sources searched. A published version would be invented, so the story is unchanged. |
| RWB-P5-E1007-APP | R-06079 | DOR-RWB-P5-E1007-APP-23 |  | Definition of Ready item 23 Contract version fixed: Fail | Story names only the /v1 REST path. No contract version is in the sources, and naming one would be invented, so the story is unchanged. |
| RWB-P5-E1007-APP | R-10827 | CG-ALL-5740 | 12.3 | Payload of rwb.document.DocumentStored.v1 differs from Kafka Catalog v1 | Field names of the payload could not be verified against Kafka Catalog v1; the earlier payload is kept and the mismatch stays open. |
| RWB-P5-E1016-APP | R-06082 | DOR-RWB-P5-E1016-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or project sources; project grep found only scratch files under _work/msr. Sign-off not invented. |
| RWB-P5-E1016-APP | R-28496 | GAP-1028 |  | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Sections 7, 12 and 16 are not in this chunk, so no exact old text exists for the six criteria, C entries or login wording. Needs those section texts. |
| RWB-P5-E1017-APP | R-25717 | CG-ALL-5771 | 3, 3.1 | Flyway file V1017_1__document_retention.sql is not in the V0001..Vnnnn form | Next Vnnnn of the rwb-document sequence is not in sources; grep of db/migration found none. L420 is blank in the supplied text, so no anchor. Needs the service sequence. |
| RWB-P5-E1017-APP | R-28503 | GAP-2432 | 7, 16 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept | Covers and Level text of sections 7 and 16 is not in this chunk, so there is no exact anchor. Apply the Detail mapping in the chunk that carries those sections. |
| RWB-P5-E1021-APP | R-25726 | CG-ALL-5790 | 16 | Test cases cover other criteria in Test Cases v8 | Test Cases v8 AC1-AC14 are legacy RWB-E1-021 criteria with different meaning from story ACs. Renumbering would be a number swap; a QA re-map is needed. No mapping found in sources. |
| RWB-P5-E1024-APP | R-25731 | CG-ALL-5800 | 3 | Flyway file V1024_1__document_store.sql is not in the V0001..Vnnnn form | Line 413 (section 12.5) is outside this chunk and its exact text was not supplied. Service Template Spec v1 §3.1 gives V0001 as baseline with no next number, so the value cannot be set. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09466 | RWB-P5-AD021-CON | CG-ALL-5720 | 12.1 | Publish GET /api/recovery/document/v1/retention-classes as in 12.1, single base prefix |
| CDC-09467 | RWB-P5-AD021-CON | CG-ALL-5721 | 12.1 | Publish GET /api/recovery/document/v1/retention-classes/{classCode} as in 12.1, single base prefix |
| CDC-09468 | RWB-P5-AD021-CON | CG-ALL-5722 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId}/retention as in 12.1, single base prefix |
| CDC-09469 | RWB-P5-AD021-CON | CG-ALL-5723 | 12.1 | Publish GET /api/recovery/document/v1/documents/{documentId}/retention-actions as in 12.1, single base prefix |
| CDC-09470 | RWB-P5-AD021-CON | CG-ALL-5724 | 12.1 | Publish POST /api/recovery/document/v1/admin/retention-loads under owner story RWB-P5-E1041-CON, as 12.1 names it |
| CDC-09471 | RWB-P5-AD021-CON | CG-ALL-5725 | 12.1 | Not claimed by this baseline; remove from this story's yaml scope or publish only under the owner stories named in 12.1 |
| CDC-09472 | RWB-P5-AD021-CON | CG-ALL-5726 | 12.1 | Publish GET /api/recovery/document/v1/admin/retention-runs under owner story RWB-P5-E1017-APP, as 12.1 names it |
| CDC-09473 | RWB-P5-AD021-CON | CG-ALL-5727 | 12.1 | Not claimed by this baseline; remove from this story's yaml scope or publish only under owner story RWB-P5-E1017-APP |
| CDC-09476 | RWB-P5-AD021-CON | DOR-RWB-P5-AD021-CON-8 | 12.1 | Add the paths listed in the detcheck that are absent; declare Idempotency-Key on the three POST operations, or state their keys in the owning stories' contracts (RWB-P5-E1041-CON, RWB-P5-E1017-APP). |
| CDC-09486 | RWB-P5-E1007-APP | CG-ALL-5738 | 12.1 | Publish POST /documents in rwb-document.yaml through the RWB-P2-E1007-CON contract story, as the owner's yaml; the story's 12.1 row stays. |
| CDC-09519 | RWB-P5-E1016-APP | CG-ALL-5752 | 12.1 | Publish GET /api/recovery/document/v1/retention-classes in rwb-document.yaml through the owning CON story, or remove the operation from 12.1. |
| CDC-09520 | RWB-P5-E1016-APP | CG-ALL-5753 | 12.1 | Publish GET /api/recovery/document/v1/retention-classes/{classCode} in rwb-document.yaml through the owning CON story, or remove the operation from 12.1. |
| CDC-09521 | RWB-P5-E1016-APP | CG-ALL-5754 | not located in chunk | Remove the closed enum on action so its values are read as data from LOV-RETENTION-ACTION, consistent with Reference Data v5 Lists. |
| CDC-09524 | RWB-P5-E1016-APP | DOR-RWB-P5-E1016-APP-8 | n/a | Publish the two GET retention-classes paths and remove the closed action enum, per CG-ALL-5752, CG-ALL-5753 and CG-ALL-5754. |
| CDC-09534 | RWB-P5-E1017-APP | CG-ALL-5766 | 13 | Remove the closed enum on action so LOV-RETENTION-ACTION values are accepted as data; the Reference Data v5 list is the higher-precedence source. |
| CDC-09539 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-8 | 13 | Remove the closed enum on action so LOV-RETENTION-ACTION values load as data without a schema failure. |
| CDC-09592 | RWB-P5-E1024-APP | CG-ALL-5796 |  | Remove the fixed reviewStatus enum so the LOV-REVIEW values from Reference Data v5 Lists are accepted as data. |
| CDC-09595 | RWB-P5-E1024-APP | DOR-RWB-P5-E1024-APP-8 | 12.3 | Replace the closed enum for reviewStatus with the LOV-REVIEW reference that the story reads as data (P1). |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09464 | RWB-P5-AD021-APP | CG-ALL-5710 | 18 | Trace REQ-DCM-016 to TC-AD-021-02 in place of TC-E1-041-03, TC-E1-041-04 and TC-E1-041-10, as section 18 states |
| CDC-09474 | RWB-P5-AD021-CON | DOR-RWB-P5-AD021-CON-12 | 16 | Added AC6 and AC7 test rows (TC-AD-021-04, -05) and 12.7 boundary row TC-AD-021-06 in section 16; the boundary row's covers and data are Not specified. |
| CDC-09483 | RWB-P5-AD021-CON | CG-ALL-5733 | 18 | Align the REQ-DCM-016 test list with RWB-P5-AD021-CON §18 (TC-AD-021-02) in the next RTM version. |
| CDC-09510 | RWB-P5-E1007-APP | CG-ALL-5746 | 18 | Align the REQ-DRI-006 and REQ-DRI-007 test lists with section 18 of this story in the next RTM version. |
| CDC-09531 | RWB-P5-E1016-APP | CG-ALL-5758 |  | Align the test case lists of REQ-RDF-010 and the other listed requirement with section 18 of RWB-P5-E1016-APP in the next RTM version. |
| CDC-09546 | RWB-P5-E1017-APP | CG-ALL-5769 | 18 | Story section 18 lists TC-E1-017-01 to 19; the RTM v7 row must match in its next version. |
| CDC-09571 | RWB-P5-E1018-APP | CG-ALL-5778 | 18 | Trace the seven listed requirements to the test lists of RWB-P5-E1018-APP section 18, which is kept unchanged. |
| CDC-09587 | RWB-P5-E1021-APP | CG-ALL-5791 | 18 | Align the REQ-CWC-010 and REQ-CWC-016 test lists in RTM v7 to this story's section 18 (TC-E1-021-01, -04, -10, -11, -14 and -09, -16). |
| CDC-09608 | RWB-P5-E1024-APP | CG-ALL-5798 | 18 | Align the test lists of the five requirements (REQ-DCM-001 and four others) to RWB-P5-E1024-APP section 18 in the next RTM version. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09456 | RWB-P5-AD021-APP | DOR-RWB-P5-AD021-APP-14 | find it | Confirm and record the signed sign-off of the epic design in the epic design record |
| CDC-09475 | RWB-P5-AD021-CON | DOR-RWB-P5-AD021-CON-14 |  | Record the signed epic design sign-off for RWB-P5-AD021-CON |
| CDC-09535 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-14 | header | Record the signed epic design sign-off reference for RWB-SVC-P5. |
| CDC-09553 | RWB-P5-E1018-APP | DOR-RWB-P5-E1018-APP-14 | find it | Record the signed epic design sign-off for RWB-P5-E1018-APP; no sign-off appears in the story or the source documents. |
| CDC-09578 | RWB-P5-E1021-APP | DOR-RWB-P5-E1021-APP-14 | n/a | Record the signed epic design sign-off for RWB-SVC-P5 / EP01 and confirm it. No sign-off is in the story or source set. |
| CDC-09593 | RWB-P5-E1024-APP | DOR-RWB-P5-E1024-APP-14 |  | Record the signed epic design sign-off for RWB-P5-E1024-APP. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09460 | RWB-P5-AD021-APP | CG-ALL-5709 | 14 | Add a new message ID for the run summary alert naming cases kept on legal hold; the story then cites it |
| CDC-09477 | RWB-P5-AD021-CON | CG-ALL-5728 | 14 | Add a new message ID for 'A value is outside its range, or a class is not in the rule version in force', with its text and 422 status. Then RWB-P5-AD021-CON section 14 cites that ID in place of MSG-GEN-002. |
| CDC-09478 | RWB-P5-AD021-CON | CG-ALL-5729 | 14 | Add a new message ID for 'The run summary alert of the month names the cases kept on legal hold', with its text. Then RWB-P5-AD021-CON section 14 cites that ID in place of MSG-P1-020. |
| CDC-09479 | RWB-P5-AD021-CON | CG-ALL-5730 | 14 | Add a new message ID for 'A read meets a run in progress on the same document', with its text and 409 status. Then RWB-P5-AD021-CON section 14 cites that ID in place of MSG-P2-006. |
| CDC-09527 | RWB-P5-E1016-APP | DOR-RWB-P5-E1016-APP-9 | 14 | Confirm the MSG-P1-003 wording in the standard against section 14; the text is P1's and is named here, not produced here. |
| CDC-09543 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-9 | 14 | Make the MSG-P2-006 text match section 14 of this story, which copies RWB-E1-017. |

### RWB-P5-AD021-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09457 | RWB-P5-AD021-APP | DOR-RWB-P5-AD021-APP-21 | header | Build the contract story to Done and publish the contract |
| CDC-09458 | RWB-P5-AD021-APP | DOR-RWB-P5-AD021-APP-22 | find it | Publish a contract fake library version and record it as published |
| CDC-09465 | RWB-P5-AD021-APP | GAP-1026 | 12 | Publish the four reads and four resources with paths, field sets, status mapping and P3 rows as consumed; name the admin operations of RWB-P5-E1041-CON and RWB-P5-E1017-APP; mark unsourced texts Not specified. |
| CDC-09481 | RWB-P5-AD021-CON | DOR-RWB-P5-AD021-CON-9 | 14 | Confirm the meaning of MSG-GEN-002, MSG-P1-020 and MSG-P2-006 against the standard and align their use in section 14. |
| CDC-09485 | RWB-P5-AD021-CON | GAP-1026 | 12 | Set C to the three P3 rows (GET case, POST legal-hold, GET lists) with owner P3, 2 s budget and fakes; name RWB-P5-E1041-CON and RWB-P5-E1017-APP as admin owners; record the missing C entries for step D1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09459 | RWB-P5-AD021-APP | CG-ALL-5708 | 11; 13 | Add party_id as a dictionary field (ACE customer business key of document), or record the object it names in the owning document. Data owner to confirm the name. |
| CDC-09462 | RWB-P5-AD021-APP | DOR-RWB-P5-AD021-APP-7 | 11 | Add party_id as a field of document (the ACE customer business key, DF-DOC-003) in the data model and its classification |
| CDC-09490 | RWB-P5-E1007-APP | Name recovery_svc is not a field or entity in LDM v9 or Data Classification v5 | 11 | Section 11 states recovery_svc is not in LDM v9 or Data Classification v5 |
| CDC-09582 | RWB-P5-E1021-APP | CG-ALL-5787 | 12.3 | Record ce_id as the CloudEvents 1.0 binary-mode header of the event envelope, a transport object, not a dictionary field. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09461 | RWB-P5-AD021-APP | DOR-RWB-P5-AD021-APP-6 | 10 | Add roles SY-DOCUMENT (rwb-document service identity) and SY-P7 (decision record writer) as used in section 10 |
| CDC-09480 | RWB-P5-AD021-CON | DOR-RWB-P5-AD021-CON-1 | 1 | Add tech lead as a role name, or confirm the role code the story should use. |
| CDC-09542 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-6 | 10 | Add role SY-DATALOAD for the rwb-document service identity. |
| CDC-09599 | RWB-P5-E1024-APP | DOR-RWB-P5-E1024-APP-6 | 10 | Add role SY-DOCUMENT (rwb-document service identity) to the roles list. |

### RWB-P3-E1018-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09554 | RWB-P5-E1018-APP | DOR-RWB-P5-E1018-APP-22 | find it | Record the published contract fake library version that RWB-P5-E1018-APP builds against. |
| CDC-09560 | RWB-P5-E1018-APP | GAP-0343 | find it | Assert Kafka rwb.case.events.v1 CaseCreated and P7 DecisionRecorded on rwb.decision-record.v1 instead of the local caseCreated and P3 decision log; seed the ALS batch through the W1J01 harness. |
| CDC-09564 | RWB-P5-E1018-APP | GAP-0676 |  | Agree the field-level OpenAPI schema at baseline review: required flags per operation, GET /cases page and sort parameters, caseNo pattern and error codes per operation. Record it in the rwb-case API file. |
| CDC-09576 | RWB-P5-E1018-APP | GAP-1038 | find it | Publish the not-found message ID and the GET /cases/{caseId} request and response field names; the rwb_document login belongs in its DB story |

### RWB-P2-E1007-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09496 | RWB-P5-E1007-APP | GAP-0334 | 13 | Fix the deliverFile manifest schema, the claim-check handoff between rwb-integration and rwb-document, and the two Airflow window calls at the P2 contract review, and publish them in the activity contract jar and AsyncAPI before the first SIT run. |
| CDC-09499 | RWB-P5-E1007-APP | GAP-0648 | - | Fix deliverFile manifest and return, the three typed failures, the rwb-comms notice-fact read, the RFC 9457 body, JSON names and registry subject as the item states. |
| CDC-09506 | RWB-P5-E1007-APP | GAP-2229 | n/a | Confirm FileFailed.v1 and FileDelivered.v1 payload elements, the resume-state carrier and the task code and due date values at contract review; rename in this story only where they differ. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09497 | RWB-P5-E1007-APP | GAP-0338 | 11 | Update the P2 Integration row of the connection matrix (slide 13) to show its read path to rwb-source-data and the FileFailed edge into rwb-case, or have the requester pass the figures in the manifest. |
| CDC-09548 | RWB-P5-E1017-APP | GAP-2428 | find it | Set JOB-14 to daily 02:00 Asia/Bangkok on queue rwb-decision, page size 5000, one run at a time; record property names and flag-off behaviour as configuration in the service template. |
| CDC-09573 | RWB-P5-E1018-APP | GAP-0982 | find it | Add the case-authority request and answer schema for POST /api/recovery/access/v1/authorise, record the caller teams and regions in TSD P4 T3.1, and list the case-record personal field IDs with version for the masking pack. |

### RWB-P7-E1018-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09565 | RWB-P5-E1018-APP | GAP-2433 |  | Write one sentence for MSG-P7-009 naming the field and case reference, and one warning for MSG-P7-012 naming the chain position, before wave 1. Add both rows to the API specification. |
| CDC-09567 | RWB-P5-E1018-APP | GAP-2436 |  | Name the admitting rule ID of package ENTRY in the rule-row catalogue and copy that identifier into the registry fixture of the P7 story. |
| CDC-09569 | RWB-P5-E1018-APP | GAP-2434 |  | Add finalCall to the query parameters of API-P7-006. Fix the creation filter answer as a page of entries with the thirteen named fields. |

### RWB-P2-E1007-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09501 | RWB-P5-E1007-APP | GAP-0739 | 2, 13 | Keep the seam: outcomes and admin item from RWB-P2-E1007-CON; route state from the latest decision-record entry; task code and due date as rwb-case reference rows. |
| CDC-09507 | RWB-P5-E1007-APP | GAP-3160 | n/a | Keep interface_config, outbound_item, outbox_event, outbox_delivery and processed_event in P2; drop writes of debt_sale_account (S6) and recovery_case (P3); S6 owns debt_sale_account via contract call or P2 event. |

### RWB-P2-E1007-APP; 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09513 | RWB-P5-E1007-APP | GAP-1540 |  | State the attempt spacing as the FSD acceptance criterion and the interface configuration values as configuration in force; fix neither as a product rule. |
| CDC-09514 | RWB-P5-E1007-APP | GAP-1542 |  | Move removed IDs to an exclusion table with later home (ACE ingestion); add no FR, NFR or AC; state that no inbound adapter, folder, run or sign-off exists. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09515 | RWB-P5-E1007-APP | GAP-1546 | n/a | State INT-17, INT-18 and INT-22 as reused ACE capabilities with no P2 build and no FR; record their behaviour as ACE's. |
| CDC-09516 | RWB-P5-E1007-APP | GAP-1547 | n/a | Record the FSD sentence on the partner and document transport as superseded; state that those channels keep their own contracts with no P2 requirement. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09525 | RWB-P5-E1016-APP | CG-ALL-5756 | 16 | Add rows TC-E1-016-10, TC-E1-016-11 and TC-E1-016-12 with Given, When and Then copied from the criteria they cover. |
| CDC-09557 | RWB-P5-E1018-APP | CG-ALL-5776 | 16 | Add rows TC-E1-018-15 and TC-E1-018-16, with Given, When and Then copied from the criteria they cover. |

### RWB-P5-E1017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09536 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-21 | header | Create the contract story for /api/recovery/document/v1, publish it and link it as the contract dependency. |
| CDC-09537 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-22 | header | Publish the contract fake library version and record it as published. |

### RWB-P1-E1018-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09562 | RWB-P5-E1018-APP | GAP-0573 |  | P1 writes party_ext and account_ext by two PUT operations by business key, with all four party flags in the body. The screen keeps the confirmation and its audit. P1 enforces no role model (ASM-B-P1-07-E1018-3, AC3). |
| CDC-09563 | RWB-P5-E1018-APP | GAP-0576 |  | Return product_group as the product_category value the view returned, unvalidated and unmapped. A value outside LOV-PRODUCT is returned as read, never coerced, dropped or defaulted (ASM-B-P1-07-E1018-6, AC1). |

### RWB-P3-E1021-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09579 | RWB-P5-E1021-APP | DOR-RWB-P5-E1021-APP-21 | n/a | Confirm RWB-P3-E1021-CON is published. The story already names it as the contract dependency; no RWB-P5-E1021-CON is needed. |
| CDC-09580 | RWB-P5-E1021-APP | DOR-RWB-P5-E1021-APP-22 | n/a | Record the published fake library version. No version is given in the source documents. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09581 | RWB-P5-E1021-APP | CG-ALL-5785 | 13 | Record the unique partial index uk_document_case_type_hash as an index object. Lines 197 and 301 lie outside this chunk. |
| CDC-09597 | RWB-P5-E1024-APP | CG-ALL-5795 | 13 | Record uk_document_case_type_hash as the unique partial index on rwb_document.document (case_id, document_type, content_sha256) WHERE is_active, or use its dictionary name. |

### OTHER:Message catalogue (MSG standard) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09463 | RWB-P5-AD021-APP | DOR-RWB-P5-AD021-APP-9 | 14 | Confirm the meaning of MSG-P1-020 as the run summary naming legal-hold cases, or assign the standard's own ID to it |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; RWB-P6-E4042-CON; RWB-P6-E4042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09482 | RWB-P5-AD021-CON | GAP-1141 | find it | Add the rwb-document retention-class read as a C row of RWB-P6-E4042-APP once P5 publishes it; fix its path and answer in RWB-P6-E4042-CON; record in the Service Contract Catalog that rwb-comms reads a class and never sets one. |

### RWB-P5-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09484 | RWB-P5-AD021-CON | GAP-1028 | 18 | Record the split of RWB-E1-016 with this story as its secondary P5 slice; add C entries for the four P4, P3 and P1 operations with fakes and the four missing C entries; no H dependency. |

### OTHER:Story backlog (no contract story key in the sources) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09487 | RWB-P5-E1007-APP | Definition of Ready item 21 Contract published: Fail |  | Contract story for rwb-document does not exist; the story's only contract dependency is RWB-P2-E1007-CON. Created outside this story. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09488 | RWB-P5-E1007-APP | DOR-RWB-P5-E1007-APP-8 | 12.1 | Align DocumentStored.v1 payload with the catalog v1 entry; publish POST /documents in rwb-document.yaml (CG-ALL-5738). |

### OTHER:FSD P2 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09489 | RWB-P5-E1007-APP | GAP-1539 | none | Build the INT-25 tape from the tape rows and account keys in the delivery request manifest raised by rwb-debtsale; read account facts through the rwb-source-data contract; P2 reads neither debt_sale_account nor v_ace_account. |

### OTHER:P3 screen specification (SCR-09; OTHER:SCR-30) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09491 | RWB-P5-E1007-APP | DOR-RWB-P5-E1007-APP-10 | none | Add empty, loading, error and no-access states to SCR-09 and SCR-30. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09492 | RWB-P5-E1007-APP | DOR-RWB-P5-E1007-APP-11 | none | Reclassify the P2 fields that this story does not carry as not personal data. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09493 | RWB-P5-E1007-APP | DOR-RWB-P5-E1007-APP-12 | 12, 12.7, 16 | Align the P3 test cases for this story's criteria and the RTM v7 test lists to section 16, including the added TC-E1-007-11 and TC-E1-007-12. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09494 | RWB-P5-E1007-APP | GAP-0673 | 11 | Mark FSD P2 Integration v3 A1.5 and TSD P2 Integration v3 T1 and T5.1 INT-03 lines superseded for legacy key RWB-E4-046 with date and decision. Agree ALS interface id, transport, layout, result codes, retry limits and intervals with the interface owner and load one versioned interface_config row per environment in rwb-integration. |

### RWB-PLT-TE006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09495 | RWB-P5-E1007-APP | GAP-1416 | 13 | Fix one published artifact with major version, the three interfaces and exceptions, DDL of the four tables with processed_event and idempotency_key columns, CloudEvents 1.0 attributes with caseId and ce_type, inbox dedupe rule, retry ladder 1 min 10 min 1 h, dead-letter topic with one alert and replay tool, and case-step events staying with owning service. |

### OTHER:TSD P2 Integration v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09498 | RWB-P5-E1007-APP | GAP-0647 | Header | Replace T1.1, T5.2 and T6.2 direct-view wording with Architecture v5 and ADR-010: every ACE fact via rwb-source-data, one hop, 2 s. |

### OTHER:Operations story for outbound-file deployment, owned by the DevOps team (no story key in the sources) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09500 | RWB-P5-E1007-APP | GAP-0650 | 9 | Set chart values, replica counts, KEDA backlog threshold, lag and alert thresholds and build ID format as environment values. Confirm both windows with the bank Airflow owner as calls on the requesting services' APIs; register no Schedule or timer. Fix the trigger contract and alert message identifiers with the Airflow owner and platform observability owner. |

### OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09502 | RWB-P5-E1007-APP | GAP-1162 | Header | Add one read returning the postal addressee by party_id, with a 2 s budget and a fake; keep the value out of rwb_comms, events and logs. |

### OTHER:rwb-comms outbound-run story and gateway-bff screen route (owners: Solution architect and gateway-bff owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09503 | RWB-P5-E1007-APP | GAP-1166 | none | Answer run state from notice dispatch fields, workflow run and P2 status, with no run table. Provide one read and one rerun on the service base. Enforce the right at gateway-bff for the screen path. Edge owner confirms whether a local guard is needed. |

### OTHER:Recovery Workbench PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09504 | RWB-P5-E1007-APP | GAP-1537 | - | State that the bank scheduler owns the window, its opening time and re-run; the service owns the attempt ladder, exception state and owner task; DL11 owns the single retry count. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09505 | RWB-P5-E1007-APP | GAP-1544 | n/a | Inherit the programme NFR targets; state outbound file size, file count, daily tape volume, 16:00 window and 01:30 extract targets as open under DL11 with placeholder R9. |

### OTHER:Key-rotation runbook (rotation period) and per-environment values of the INT-14 and INT-25 endpoints, set by the bank MF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09508 | RWB-P5-E1007-APP | GAP-0649 | n/a | Provision endpoints, receivers, PGP keys, staging, size, timeout and concurrency values per environment; record rotation period in the key-rotation runbook. |

### OTHER:Owner CON stories of rwb-source-data, rwb-integration and rwb-reporting (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09509 | RWB-P5-E1007-APP | GAP-1396 | n/a | Fix Airflow product, tenancy, service principal, timeout and retry values, DailyCaseRun wait mechanism and file-window operation paths at scheduling design review; publish before first SIT chain run. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09511 | RWB-P5-E1007-APP | GAP-0981 |  | Register one OUTBOUND interface row for the access-review file with interface ID, file pattern, data product, owner role and alert role; publish layout and recipient; state review-cycle date convention. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09512 | RWB-P5-E1007-APP | GAP-1538 |  | Add rows for FileDelivered and FileFailed, producer rwb-integration, topic rwb.integration.events.v1, keyed by case ID, with no numbered EV ID. |

### OTHER:RWB-P3 story owning the file-outcome listener (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09517 | RWB-P5-E1007-APP | GAP-2230 | n/a | Record ASM-B2-P3-013-4: the case-action and task-raise interfaces stay internal to the listener; no path is added to the rwb-case contract. |

### OTHER:Legacy dependency trace sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09518 | RWB-P5-E1007-APP | GAP-3233 | n/a | Keep the five rows as Not carried; add an X row only if the run books or the harness wait for the named story. |

### RWB-P1-E1016-CON; RWB-P3-E1018-CON; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09522 | RWB-P5-E1016-APP | DOR-RWB-P5-E1016-APP-21 | header | No story edit; publication status is held by the CON stories. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09523 | RWB-P5-E1016-APP | DOR-RWB-P5-E1016-APP-22 | n/a | Record the published fake library version for the rwb-access authorise and permissions fakes and the rwb-source-data data-dictionary fake. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09526 | RWB-P5-E1016-APP | DOR-RWB-P5-E1016-APP-12 | 16, 12.7, 18 | Add TC-E1-016-10, -11 and -12 to Test Cases v8 (tab Story test cases); align the section 18 test lists to RTM v7. |

### OTHER:rwb-source-data service API document (P1 contract; OTHER:tech lead of rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09528 | RWB-P5-E1016-APP | GAP-0571 | none | Publish GET /api/recovery/source-data/v1/entry-candidates with required businessDate and threshold, optional page and size, answering EntryCandidatePage; statuses 400, 401, 403, 409, 422, 503; OpenAPI 3.1 fragment. |

### OTHER:Technical Specification P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09529 | RWB-P5-E1016-APP | GAP-0481 |  | Remove masking_rule and its role and permission rows from the P1 schema (T3.6); P1 holds data_product_access only and takes masking from POST /api/recovery/access/v1/authorise and FieldMasker of RWB-P4-E1037-CON. |

### RWB-P1-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09530 | RWB-P5-E1016-APP | GAP-0482 |  | Seed only the six rows the sources give under DPA-2026.11; no other role or product row by default; later loads go through the rwb-case reference-data contract; data steward closes the gap before use outside SIT. |

### RWB-P1-E1016-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09532 | RWB-P5-E1016-APP | GAP-0484 | header | E1016-DB delivers the three indexes, the read model v_data_product_catalog, the DPA-2026.11 seed, the 122/1,366 dictionary conformance check and the schema checks; it creates no table that RWB-P1-E1001-APP or RWB-P1-E1069-DB already creates, owns no masking row, and a repeated run changes nothing. |

### OTHER:TSD P4 appendix T-A and the OpenAPI file of the rwb-access service (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09533 | RWB-P5-E1016-APP | GAP-0983 | 8 | Publish the request and answer schemas of GET /admin/roles, GET /masking-policies and POST /authorise in TSD P4 appendix T-A and in the OpenAPI file of the service, with the marker values, the maskingExceptions part, the two version fields and the access resolution the request carries. |

### OTHER:Recovery Workbench Reference Data and Lists of Values v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09538 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-5 | 9 | Add DOCRET to the closed list LOV-RETENTION-ACTION (current values ARCHIVED, LISTED, HELD, EXCEPTION); the story keeps its six transitions in section 9. |

### OTHER:Recovery Workbench P3 screen SCR-47 specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09540 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-10 |  | Add empty, loading, error and no access states to SCR-47. |

### OTHER:Recovery Workbench P2 field classification (data dictionary) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09541 | RWB-P5-E1017-APP | DOR-RWB-P5-E1017-APP-11 |  | Remove the personal-data class from P2 fields that this story states carry no personal data. |

### OTHER:TSD P1 v3 (T3.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09544 | RWB-P5-E1017-APP | GAP-0488 | 12.7 | Remove retention_rule as a P1-owned table; P5 rwb-document owns it per Ownership Map ruling ASM-A6-tables-10. |

### RWB-P1-E1017-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09545 | RWB-P5-E1017-APP | GAP-0489 | 4 | Fix POST /retention-runs and GET /retention-runs/{runId} on /api/recovery/source-data/v1 with the rule version, run date and rules in the request, and counts per table, rule version, archive location and held cases in the answer, field-level detail settled there. |

### RWB-P7-E1017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09547 | RWB-P5-E1017-APP | GAP-2427 | find it | Write the texts of MSG-P7-009, the not-found answer, the chain-break report and the collection gap alert once with the P7 business analyst; keep the legacy AC8 check name inside MSG-P7-009. |

### OTHER:Platform secret store (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09549 | RWB-P5-E1017-APP | GAP-2430 | find it | Allocate the login for schema rwb_decision and record it in the platform secret store; the story keeps the phrase 'the rwb-decision login (DP-02)' until then. |

### OTHER:Sequence tracker v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09550 | RWB-P5-E1017-APP | GAP-3230 | find it | Drop rows 19 and 21 (RWB-E1-014, RWB-TE-007) at cutover, or keep them struck through as 'retired, not pulled'; clear their names from Depends on in RWB-E1-056 and RWB-E1-017. |

### OTHER:Story map (sequence tracker); RWB-P5-E1055-APP; RWB-P5-E1065-APP; RWB-P5-E1041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09551 | RWB-P5-E1017-APP | GAP-2351 | find it | Record RWB-P5-E1017-APP as sole owner of JOB-17; record RWB-P5-E1052-APP as notice generation slice of the document hub with no Schedule; correct the other files at next version. |

### RWB-P5-AD021-CON; RWB-P5-AD021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09552 | RWB-P5-E1017-APP | GAP-1026 | find it | Publish the four reads and four resources on /api/recovery/document/v1 with the class-in-force rule, projected hold, LOV-RETENTION-ACTION values and DOCRET reference; declare RetentionLoad, RetentionLoadResult, RetentionRun and RetentionRunPage; carry the three P3 rows as consumed. |

### OTHER:Functional Specification P3 (FSD P3 A1.5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09555 | RWB-P5-E1018-APP | GAP-1549 | find it | Restate the A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### OTHER:RWB-P1 story holding the ALS batch gate (reads v_ace_batch_status) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09556 | RWB-P5-E1018-APP | GAP-0574 | find it | While v_ace_batch_status does not exist, answer 409 with MSG-P1-001, create no case and never stamp DP01 LOADED; read the gate from the view only, with no fallback. |

### RWB-P5-E1026-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09558 | RWB-P5-E1018-APP | DOR-RWB-P5-E1018-APP-10 | 9-10 | Define the empty, loading, error and no-access states of SCR-30 Case documents and SCR-03 Case record; this story only reads them (story line 444 assigns screens and states to RWB-P5-E1026-APP). |

### OTHER:rwb-source-data service API document (tech lead of rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09559 | RWB-P5-E1018-APP | GAP-0571 | find it | Publish GET /api/recovery/source-data/v1/entry-candidates with required businessDate and threshold, optional page and size; EntryCandidatePage with businessDate, threshold, asOf, page, size, total, candidates[], breaks[]; statuses 400, 401, 403, 409, 422, 503; OpenAPI 3.1 fragment of the three operations. |

### OTHER:RWB-SVC-P3 database story and service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09561 | RWB-P5-E1018-APP | GAP-0675 |  | Allocate the rwb-case login name with grants on schema rwb_case only, no privilege on another schema, and record it in the service catalogue. |

### OTHER:TSD P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09566 | RWB-P5-E1018-APP | GAP-2435 |  | Restate DF-DEC-002 as an indexed business key with no foreign key and drop the recovery_case row of T3.3. State in T3.1 that the ALS business date is carried inside inputs_ref. |

### RWB-P3-E1018-APP; RWB-P1-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09568 | RWB-P5-E1018-APP | GAP-3162 |  | Keep the case tables in P3. Write party_ext and account_ext rows in RWB-P1-E1018-APP and read them back by contract. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09570 | RWB-P5-E1018-APP | GAP-0674 |  | Publish the gateway-bff composite route for SCR-02 and SCR-03 with its path, the parallel calls to rwb-case and rwb-source-data, the merge order, the masking rules and the 2 s budget. |

### OTHER:Work package C-WEX (WP index) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09572 | RWB-P5-E1018-APP | GAP-3206 | find it | Read '(E1-018)' in the heading as a scheduling label; keep RWB-E1-020 as subject; note in the run edit log and correct the heading in the next WP index. |

### OTHER:rwb-source-data slice of RWB-E1-018 and assumption register ASM-B-P1-07-E1018-2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09574 | RWB-P5-E1018-APP | GAP-0572 | find it | Fix one operation per business date, paged by page and size; default and maximum page size: Not specified in the source documents (GAP-0572); record in ASM-B-P1-07-E1018-2. |

### OTHER:Deployment topology and environment values for rwb-case (platform template; OTHER:not in the sources read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09575 | RWB-P5-E1018-APP | GAP-0677 | find it | Publish the rwb-case cluster, node pool, replica, resource, zone spread, ingress class and probe values as values files, not chart defaults |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09577 | RWB-P5-E1018-APP | GAP-2438 | find it | Fix the rwb-decision login name in the secret store, with migration and application roles kept apart |

### OTHER:Business Requirements Document, section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09583 | RWB-P5-E1021-APP | GAP-1456 | 8 | State in section 8.2 that a story keeps the business-epic wave (wave 1 here) and that the delivery lead confirms wave per story at build sequencing. |

### OTHER:API yaml of rwb-case, rwb-access, rwb-source-data and rwb-decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09584 | RWB-P5-E1021-APP | GAP-3076 | 12 | Publish the operation names for the six consumed rows: transfer request, queue and capacity read, LOV-TRANSFER-REASON read, package read, authorise call and case-facts read. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09585 | RWB-P5-E1021-APP | GAP-3079 | 16 | Publish the Kafka event names of the case triggers and the S8 subscriptions on these topics. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09586 | RWB-P5-E1021-APP | GAP-0688 | 12 | Name the rwb-case database login and its grant set, referenced by vault secret. |

### RWB-P4-E1037-CON; OTHER:matrix owner; OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09588 | RWB-P5-E1021-APP | GAP-0990 | find it | Publish the authorise request and answer schema with its legalHold attribute; confirm the matrix version label in force at 30 November 2026 with the matrix owner; tabulate the Queue and allocation letters in TSD P4 T6.1. |

### OTHER:Platform team chart values for rwb-case (deployment chart) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09589 | RWB-P5-E1021-APP | GAP-0691 | find it | Publish cluster, node pool, replica counts per environment, ingress host, resource limits and pod disruption budget as chart values; no environment default shipped. |

### OTHER:P5 contract baseline story or rwb-document deployment story; RWB-P3-E1021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09590 | RWB-P5-E1021-APP | GAP-1036 | find it | Publish the AsyncAPI 3.0 document of rwb.document.events.v1 with the registered JSON schemas for DocumentStored.v1 and DocumentFieldsExtracted.v1, required fields and BACKWARD rule; hand the DocumentStored schema to RWB-P3-E1021-CON as the trigger fixture. |

### RWB-PLT-NF06-DB; OTHER:service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09591 | RWB-P5-E1021-APP | GAP-1037 | find it | Allocate the rwb-document login name, its grants (schema rwb_document only, no privilege on another schema) and its secret reference; record them in the service catalogue. |

### OTHER:rwb-document contract CON stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09594 | RWB-P5-E1024-APP | Definition of Ready item 21 Contract published: Fail | 3 | Contract publication belongs to the rwb-document contract stories; this APP story only states that it does not publish the contract. |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09596 | RWB-P5-E1024-APP | GAP-1583 |  | Add FR-P5-030 and FR-P5-031 with AC-P5-022 and AC-P5-023 as wave 1 release gates; keep the backup schedule and restore evidence open as OQ-P5-05. |

### RWB-P5-E1025-APP; RWB-PLT-TE012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09598 | RWB-P5-E1024-APP | DOR-RWB-P5-E1024-APP-17 | header | Complete both builds; this story is gated by them (Ready to start already names RWB-P5-E1025-APP). |

### OTHER:Work Package B-P5-03 (line 58) and the RWB-E1-007 secondary slice record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09600 | RWB-P5-E1024-APP | GAP-1027 | Header | Record the secondary P5 slice of RWB-E1-007 as new work under D-RCV-60 with six new criteria and no legacy AC; the slice is not this story's legacy key RWB-E1-024. |

### OTHER:TSD P5 Document hub v2 (T3.1 and T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09601 | RWB-P5-E1024-APP | GAP-1588 | Header | Drop the EXTEND of the ACE Attachment object and the document party_id relationship to the ACE party; state the Workbench document hub as the system of record with the file in Blob with WORM and metadata in rwb_document. |

### OTHER:TSD P5 Document hub v2 (DF-DOC-003 and T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09602 | RWB-P5-E1024-APP | GAP-1594 | Header | Replace party_id uuid with the business key person_key varchar(255), no foreign key, per the FSD v3 change note. |

### OTHER:P5 case documents contract story (new) and the DB story of rwb-document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09603 | RWB-P5-E1024-APP | GAP-1033 | Header | Publish one P5 contract story for the SCR-30 operations (Document, DocumentPage, DocumentChecklist field names) before the SIT run; name the rwb_document login in the DB story. |

### RWB-P5-E1054-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09604 | RWB-P5-E1024-APP | GAP-1010 | Header | Publish the by-number case read on RWB-P3-E1035-CON; take role, team and scope from the cached permission decision until a P4 CON row is added; fix the field names and three message texts in RWB-P5-E1054-CON before the wave 1 entry check. |

### OTHER:rwb-document OpenAPI and AsyncAPI documents (contract baseline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09605 | RWB-P5-E1024-APP | GAP-1011 | Header | Freeze the seven operations, nine resources, five value sets, one IntakeResolution envelope, the If-Match lock with idempotent repeat, and the event schema. |

### OTHER:TSD P5 Document hub v2 (T-A.2 API-P5-005 entry) and the infrastructure story of rwb-document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09606 | RWB-P5-E1024-APP | GAP-2356 | Header | Settle the container, WORM tier, maximum object size and signed-PDF transfer path, and carry them as configuration rows of rwb.document.esign. |

### RWB-P5-E1057-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09607 | RWB-P5-E1024-APP | GAP-1018 Field capture: store capture block, intake submit path, parameter and list names, service login name and approval status not settled by the sources | 4 | Capture field names are Not specified in the source documents (GAP-1018); intake submit path and approval status sit in other stories. |

### OTHER:Story dependencies v5 (Dependency classes sheet, check row X) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-09609 | RWB-P5-E1024-APP | GAP-3234 | header | Record that platform technical-enabler work is team-type work: keep X on the ten rows, tracked, never blocking. |

### 05 Technical architecture/Recovery Workbench API Specification v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20627 | RWB-P5-E1021-APP | R-22010 |  | Already in yaml: postCasesCaseidTransfer, getQueues, getAdminListsListcode, getAdminRulePackages, postApprovalsApprovalidApprove. No case-facts operation; name not specified (R-22010). |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20817 | RWB-P5-E1007-APP | R-09174 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09174', 'R-21873', 'R-28451', 'R-28452', 'R-28453'] |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20826 | RWB-P5-E1018-APP | R-09171 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09171', 'R-16120', 'R-22565'] |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20867 | RWB-P5-E1021-APP | R-28532 |  | Cluster, node pool, replicas, ingress, limits and PDB are platform chart values, not content of this document. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0213 | Five rows still cite 'number in Interface Specifications v3' after v4 of that document was issued | Integration architecture team | Resolved (directive) |
| GAP-0334 | deliverFile manifest payload, claim-check handoff and the file-window trigger contract are not defined | Solution architect | Resolved (directive) |
| GAP-0338 | Connection matrix gives rwb-integration only the document REST call and the outside file edge, while the file build reads source data and the failure reaches rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0341 | E1016 catalog composition across rwb-source-data, rwb-access and rwb-document | Solution architect | Resolved (directive) |
| GAP-0342 | E1017 retention ownership and the P1 interaction path | Solution architect | Resolved (directive) |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0346 | Route-decided transfer trigger has no wave 1 owner event | Tech lead | Resolved (directive) |
| GAP-0349 | E1024 document store split across rwb-document, rwb-case and the shared decision-record topic | Solution architect | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0482 | The data_product_access seed of the version in force is only partly specified | Data steward | Resolved (directive) |
| GAP-0483 | The monolith reference-load endpoint has no target owner for an access load | Tech lead | Resolved (directive) |
| GAP-0484 | The DB slice of this legacy key cannot deliver the table DDL, because two other stories already create the tables | ACE database lead | Resolved (directive) |
| GAP-0488 | retention_rule ownership: TSD P1 v3 keeps it in P1, the Ownership Map and Arch v5 move retention to P5 | Solution architect | Resolved (directive) |
| GAP-0489 | The rwb-source-data retention-run contract shape is not specified | Solution architect | Resolved (directive) |
| GAP-0490 | The write-once archive contract (container, path and manifest) belongs to RWB-PLT-TE012-APP and is not specified | Solution architect | Resolved (directive) |
| GAP-0491 | The legal-hold query is a published interface with no REST path in the sources | Solution architect | Resolved (directive) |
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
| GAP-0688 | Per-service database login name for rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0691 | Deployment topology of the transfer capability is not specified | Platform team | Resolved (directive) |
| GAP-0739 | The case side of an outbound file outcome leaves the delivery-event element names, the route state to resume, the task code and due date, the fate of the legacy in-process interfaces and the two lake extracts unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0981 | rwb-access access-review extract (JOB-18): the interface ID, the file pattern, the extract layout, the recipient and the review-cycle date convention are not specified, the two requester activity names and the manifest are named by no source, and the delivery events are keyed by case ID while an access-review file has no case | Solution architect, P4 with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0983 | rwb-access policy and catalogue answers: no source names the request and answer field set of the role catalogue, the masking policy read or the data-product authorise answer, nor the marker vocabulary or the masking-exceptions part | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1010 | The review parameter route, the by-number case path, the access decision and the field-level names of the review queue are not settled by the sources | Solution architect with the TechX tech lead of rwb-document and the P3 and P4 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1011 | No source fixes the field-level names of the nine review resources, the one resolve answer, the field-patch idempotency, the document read position or the three platform message texts | Tech lead of rwb-document with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1018 | Field capture: the store capture block, the intake submit path, the parameter and list names, the service login name and the approval status are not settled by the sources | Tech lead of rwb-document | Resolved (directive) |
| GAP-1026 | The contract baseline of the retention-class and legal-hold surface fixes paths, shapes, statuses and a hold projection that no source names, and it consumes three P3 rows the plan does not carry | Tech lead of rwb-document, with the solution architect and the P3 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1027 | The secondary P5 slice of RWB-E1-007 has no legacy AC and several document-hub values of the outbound path are not fixed in the sources | Solution architect (P5 document hub, with the rwb-integration contract owner) | Resolved (directive) |
| GAP-1028 | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1030 | The per-service database login name for rwb-document is not specified | ACE DB team | Resolved (directive) |
| GAP-1031 | The storage account, the container names and the WORM policy of the platform storage product are not fixed in the sources | SCB IT infrastructure | Resolved (directive) |
| GAP-1032 | The request and response field names of the store operations and the not-found message are not specified | Solution architect | Resolved (directive) |
| GAP-1033 | Request and response field names of the three SCR-30 operations, the per-service login name and the text of MSG-GEN-006 are not fixed in the sources | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1036 | Producer-side AsyncAPI and JSON schema of rwb.document.events.v1 are not assigned to a contract story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1038 | The rwb-document login name, the not-found message ID of the case read and the case-read field names are not specified | Solution architect with the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1141 | Retention is module P6 in the story and P5 rwb-document in the ownership map, and no C row declares the retention contract | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1162 | The addressee and contact value reach the INT-14 file through a contract that is not in the story's contract list, and no source names the operation or its elements | Solution architect, with the P1 and P6 owners | Resolved (directive) |
| GAP-1163 | DP-17 removes the INT-19 reporting extract and the INT-20 decision-log copy, so part of legacy RWB-E1-007 has no target and no replacement in this service | Business analyst and solution architect | Resolved (directive) |
| GAP-1164 | The INT-14 record layout, the file pattern and the claim-check store of the built file are named by no source, and the document contract is not in the story's contract list | Solution architect, with the P2 and P5 owners | Resolved (directive) |
| GAP-1165 | The retired inbound load leaves TC-E1-007-05, TC-E1-007-06 and the file checks DQ-057 and DQ-059 without a target in this service | Business analyst and QA lead | Resolved (directive) |
| GAP-1166 | No source defines a run record, a run operation or the right on the interface monitor for rwb-comms | Solution architect and the gateway-bff owner | Resolved (directive) |
| GAP-1396 | Airflow product, tenancy, DAG names, identity method, timeout and retry values, the DailyCaseRun wait contract and the file-window operation are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
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
| GAP-1583 | Sizing, backup and the records management position have no FSD feature and no owned artifact | IT lead with the document hub owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1588 | The TSD extends the ACE Attachment object while the requirement makes the hub the system of record in Blob with WORM | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1594 | The FSD identifies the customer on a document by the ACE person key and the TSD by party id | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2229 | Element names of the two delivery outcomes, the carrier of the route state to resume and the values of the owner task are not in the sources | TechX and the rwb-integration contract owner | Resolved (directive) |
| GAP-2230 | The legacy P3 interfaces and the case-action path have no operation in the target case contract | TechX | Resolved (directive) |
| GAP-2335 | The two DP-11 contract reads of the legacy in-process calls are absent from the Work Package dependency rows and DP-08 is not among the patterns | Solution architect | Resolved (directive) |
| GAP-2351 | The monthly retention job JOB-17 is attributed to RWB-P5-E1052-APP by two service story files and to RWB-P5-E1017-APP and RWB-P5-E1041-APP by others, while this Work Package gives RWB-P5-E1052-APP the notice generation slice | Solution architect, with the delivery lead and the traceability owner | Resolved (directive) |
| GAP-2356 | The write-once container, the WORM tier, the size limit and the byte transfer behind the signed-version add are named by no source | SCB IT infrastructure | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2426 | The decision code, final call, action and outcome values and the payload placement of an archive or purge record are in no source | Solution architect | Resolved (directive) |
| GAP-2427 | The text of MSG-P7-009 and the ids and texts of the not-found answer, the chain-break report and the collection gap alert are not written in any source | Business analyst, P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2428 | The JOB-14 timezone, page size, overlap and catch-up values, the property names and the behaviour of the feature flag when off are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2430 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2431 | The story file at the Work Package path already existed as a partial artefact of the superseded Work Package B-P7-05, with no fragment, no register rows and citations that resolve to nothing | Delivery lead, with the traceability owner | Resolved (directive) |
| GAP-2432 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept | Traceability owner | Resolved (directive) |
| GAP-2433 | The message text of MSG-P7-009 and of the chain warning MSG-P7-012 is named in the sources but never written | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2435 | TSD P7 still models decision_log_entry.case_id as a uuid with a relationship to recovery_case and gives the row no business-date column | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2436 | The literal rule ID of the ENTER rule of package ENTRY is named in no source | Business analyst, Epic 1 | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2438 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3074 | The business epic places the story in wave 1 while the service sits in wave 2 | Programme planner with the S8 service owner | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3076 | No source publishes the operation names of the six rows this slice consumes | P1 rwb-source-data owner, P3 rwb-case owner, P4 rwb-access owner, P7 rwb-decision owner and the S8 service owner | Resolved (directive) |
| GAP-3077 | No source says which service hosts the TRANSFER package evaluation after the split | Solution architect with the S8 service owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-3079 | The event names of the P3 and P1 subscriptions are not published | P3 rwb-case owner, P1 rwb-source-data owner and the S8 service owner | Resolved (directive) |
| GAP-3080 | No source fixes where this slice records the rule ID and the package version of a transfer | S8 service owner with the data steward of module S8 and the P3 rwb-case owner | Resolved (directive) |
| GAP-3158 | The retention tables are P1 tables in the story and P5 tables in the Ownership Map | P5 document owner | Resolved (directive) |
| GAP-3160 | The P2 outbound adapter writes a table owned by rwb-debtsale | Integration lead | Resolved (directive) |
| GAP-3162 | The case story writes the P1 extension tables | P3 case owner | Resolved (directive) |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3230 | Two retired items still carry v6 windows and dependencies | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3234 | Ten class X rows point at a platform application story rather than at a DB, INF or OPS story | TechX (platform) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3240 | One module per item in version 3 becomes several services per item in the split | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P5-E1017-APP | skipped AC ID | 143 | missing: AC13 |
| RWB-P5-E1018-APP | skipped AC ID | 110 | missing: AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15 |
