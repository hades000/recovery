# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 2 of 8 (RWB-P7-E1018-APP to RWB-P7-E1046-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 10 |
| Resolved in the stories | 204 |
| Cross-document (pending in another document) | 212 |
| Not applied (value not in the sources) | 36 |
| Open business decisions | 33 |
| Register gaps linked | 162 |
| Unconfirmed assumptions | 0 |
| Lint findings | 5 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-E1018-APP | 20 | 29 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1018 APP Case ID issuance and case record v1 v2.md |
| RWB-P7-E1020-APP | 21 | 29 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1020 APP Allocation and assignment engine v1 v2.md |
| RWB-P7-E1021-APP | 19 | 17 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1021 APP Transfer rules and engine v1 v2.md |
| RWB-P7-E1027-APP | 26 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1027 APP Decision log writer v1 v2.md |
| RWB-P7-E1027-CON | 15 | 17 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1027 CON Decision log writer v1 - contract v2.md |
| RWB-P7-E1028-APP | 21 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1028 APP Service levels, timers, escalation and prescription dates v2.md |
| RWB-P7-E1030-APP | 15 | 12 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1030 APP Daily rebalancing and queue measures v2.md |
| RWB-P7-E1032-APP | 30 | 35 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1032 APP Automatic attach from the OCR intake v2.md |
| RWB-P7-E1039-APP | 20 | 22 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1039 APP Access log into the decision log and break-glass admin v2.md |
| RWB-P7-E1046-APP | 17 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E1046 APP Template and merge field catalog as data v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P7-E1046-APP | R-01786 | CG-ALL-6976 | Script gap | Product owner | The story adds COURT_FILING to the closed list LOV-NOTICE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P7-E1046-APP | R-01787 | CG-ALL-6977 | Script gap | Product owner | The story adds COURT_FILING to the closed list LOV-PRODUCT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P7-E1018-APP | R-11178 | CG-ALL-6886 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1020-APP | R-11185 | CG-ALL-6902 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1027-APP | R-11191 | CG-ALL-6921 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1027-CON | R-11194 | CG-ALL-6929 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1028-APP | R-11198 | CG-ALL-6937 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1030-APP | R-11199 | CG-ALL-6945 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1032-APP | R-11205 | CG-ALL-6960 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E1039-APP | R-11207 | CG-ALL-6971 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-22002 | GAP-0685 | Register gap | Business owner; reference data administrator | The source of the caseload cap is not fixed: parameter row or reference data | Keep the cap as versioned reference data on queue.capacity_cap and queue_member.capacity, as the legacy data model does, and add a parameter key only if a product-level override is wanted; state the ruling in the Reference Data and Parameters design. |
| RWB-ITG-E1021-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-22012 | GAP-3078 | Register gap | P7 rwb-decision owner with the business owner of module S8 | The TRANSFER rows that fire on the deviation triggers and the text of R-DEV-04 to R-DEV-06 are not published | The rule owner publishes the DEV transfer rows and the text of R-DEV-04 to R-DEV-06 with the package version; the story then reads them unchanged and no code changes. |
| RWB-ITG-E1027-ITG, RWB-ITG-E1037-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-22037 | GAP-2073 | Register gap | Service owner P7 rwb-decision with P4 rwb-access and Compliance | The approver identifier is personal data under a rule that forbids personal data in records | Store the identifier, never a name; mask it in every export under the masking rows of rwb-access (P4) and record the read in the PII log. The protection of the column itself is a decision for Compliance and Information Security. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22078 | GAP-1595 | Register gap | Product owner | The document module is said to own the letter templates and their fields, while Architecture v5 gives templates and merge fields to rwb-comms | Hold the template record, its versions and the Legal approval in rwb-comms, hold the merge-field catalog in rwb-comms, and keep the template body file in rwb-document as a document with a reference on the template row; record DL28 as superseded by D-RCV-60 and close it with the product owner. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-22113 | GAP-1570 | Register gap | Compliance with the solution architect | The access log has no stated retention, no stated searchable period, no stated storage object and no stated cross-service read right, although it is the evidence for every access question | Answer DL26 for the access log in one row: the retention period, whether it equals the decision log period, which object answers the query (the local record, the central ledger, or a projection of both), which fields are searchable and for how far back, and which roles in other services may read it. Until then this PRD keeps the classification at PII and marks the retention as not set. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22125 | GAP-2089 | Register gap | Product owner; service owners of P6 rwb-comms and P5 rwb-document | The Decision Log gives the letter templates to the document module, while Architecture v5 and the Ownership Map give them to rwb-comms | Follow Architecture v5 and the Ownership Map: templates and merge fields are P6 rwb_comms. Record the DL28 answer as a gap and ask the product owner to reaffirm or amend DL28 before the template story is Done. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E1008-ITG, RWB-ITG-E1027-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-28460 | GAP-2067 | Register gap | Document owner of the audit and logging design | The source reads version 1 in its metadata table and v2 in its file name | Take the file name as the family version, so this document becomes version 3, and keep the source values in a 'Source version' row: 1, 28 October 2026. The change log carries both readings. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-28522 | GAP-0686 | Register gap | Business owner, Shared operations; platform team, Temporal | The exact cadence of the rebalancing trigger is not defined for rwb-case | Run JOB-06 as its own Temporal Schedule at 06:30 Asia/Bangkok, after DailyCaseRun has finished, with overlap policy SKIP and a catch-up window; confirm the order with the operations owner and record it in the Temporal Workflow and Activity Catalog. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28588 | GAP-1576 | Register gap | Compliance with the solution architect | REQ-ACA-006 still requires an access entry for every read of the data lake copy, which Architecture v5 removes | Re-issue REQ-ACA-006 and NFR-042 in the next business requirement version as 'every read of the case store, the document store and a data product', so the requirement, the functional specification and this PRD use one list of objects; nothing else in the requirement changes. |
| RWB-ITG-E1039-ITG, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28591 | GAP-1591 | Register gap | Compliance and PDPA officer | NFR-042 still requires logging the data lake copy of the document store although the data lake is removed | The PRD requires every read of a document and of its extracted fields to be logged and carries no lake clause. NFR-042 needs the same correction in its next version. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-28596 | GAP-2098 | Register gap | Service owner of P6 rwb-comms; Compliance and Legal roles | The Compliance approval of customer wording has no artefact in the target template | Record the Compliance approval as a second approval of P7 with the template as its source, and keep approved_by_legal on the template row for the Legal approval that the endpoint records. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-E1018-APP | R-11174 | CG-ALL-6878 | 4, 12.1 | HTTP errors with no message ID: 401 no session; 404 no case-creation entry for the case | No 401 or 404 message ID found in the 03 folder sources (Error and Message Standard v4 not holding them). Business analyst to supply; none invented. |
| RWB-P7-E1018-APP | R-17903 | DOR-RWB-P7-E1018-APP-11 | 9 | Definition of Ready item 11 Guardrails: Partial | Which fields are personal data is a classification the sources do not make; no field named, so no edit. |
| RWB-P7-E1018-APP | R-26201 | CG-ALL-6884 | 16 | Test cases cover other criteria in Test Cases v8 | Rows TC-E1-018-02 to -10 aligned to Test Cases v8 AC2 to AC10. v8 ACs for TC-01 and one other row are not in the sources; those rows unchanged. |
| RWB-P7-E1018-APP | R-26203 | CG-ALL-6887 | 3.1 | Flyway file V1018_2__case_creation_profile.sql is not in the V0001..Vnnnn form | Next Flyway number is not in the sources, so V1018_2 cannot be renumbered. The name sits in §3.1 and line 325, outside this chunk. |
| RWB-P7-E1020-APP | R-17911 | DOR-RWB-P7-E1020-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-38 empty, loading, error and no-access states are not in the story chunk or the sources searched; cannot be placed without invention. |
| RWB-P7-E1020-APP | R-17913 | DOR-RWB-P7-E1020-APP-18 |  | Definition of Ready item 18 Open decisions: Partial | DL22 and DL23 are open business decisions; the story text listing them is outside this chunk, so the assumptions cannot be placed here. |
| RWB-P7-E1020-APP | R-17915 | DOR-RWB-P7-E1020-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR4 and BR9 added to TC-22 Covers; BR8 already in TC-16. ALLOC-014 has no source in the documents, so it is unchanged; section 7 is outside this chunk. |
| RWB-P7-E1020-APP | R-26209 | CG-ALL-6903 | 3 | Flyway file V1020_1__allocation_record.sql is not in the V0001..Vnnnn form | Next number in the rwb_decision Flyway sequence is not in the sources; migration name V1020_1 left unchanged. |
| RWB-P7-E1020-APP | R-31425 | NEWAC-RWB-P7-E1020-APP-AC14 | 7 | AC14: §5 X4: The ledger store is unavailable (covered by 'TC-E1-020-15' only) | Section 7 is outside this chunk, so AC14 cannot be anchored; the proposed test is not specified in the sources. |
| RWB-P7-E1021-APP | R-06675 | DOR-RWB-P7-E1021-APP-23 | 9 | Definition of Ready item 23 Contract version fixed: Fail | No contract version for RWB-P3-E1021-CON in the story files (04 User stories); header keeps the Not specified placeholder. Needs the contract owner. |
| RWB-P7-E1021-APP | R-26212 | CG-ALL-6911 | 16 | Test cases cover other criteria in Test Cases v8 | Test Cases v8 cache lists AC numbers for TC-E1-021-11 to -21 only in truncated form; nine visible mappings alone not applied. Section 16 unchanged. |
| RWB-P7-E1021-APP | R-26214 | CG-ALL-6914 | 3 | Flyway file V1021_1__transfer_record.sql is not in the V0001..Vnnnn form | Supplied text has no V1021_1 migration line (L331 is a package fixture row). The next Vnnnn of the service sequence is not in the sources. |
| RWB-P7-E1027-APP | R-06677 | DOR-RWB-P7-E1027-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or the 22 folder sources; sign-off cannot be confirmed from any value found. Left unchanged. |
| RWB-P7-E1027-APP | R-26218 | CG-ALL-6922 | 11 | Flyway file V_E1027__declog_idempotency.sql is not in the V0001..Vnnnn form | Next V number of the rwb_decision Flyway sequence is not in the sources (searched 22 folder for V0001 and V_E1027). Section 11 is outside this chunk. |
| RWB-P7-E1027-CON | R-06683 | DOR-RWB-P7-E1027-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off reference in the story or sources. A sign-off cannot be stated without inventing one. Not specified in the source documents (DOR-RWB-P7-E1027-CON-14). |
| RWB-P7-E1027-CON | R-17932 | DOR-RWB-P7-E1027-CON-11 |  | Definition of Ready item 11 Guardrails: Partial | The source list of personal-data fields was not found, so no field can be corrected. Not specified in the source documents (DOR-RWB-P7-E1027-CON-11). |
| RWB-P7-E1027-CON | R-17934 | DOR-RWB-P7-E1027-CON-18 |  | Definition of Ready item 18 Open decisions: Partial | DL10 and ASM-2250, ASM-2357, ASM-2377, ASM-2863 were not found in the story text or sources searched. Not specified in the source documents (DOR-RWB-P7-E1027-CON-18). |
| RWB-P7-E1027-CON | R-22043 | GAP-1237 | 16 | The canonical form of the entry hash is not specified | Canonical form rules are not in the sources. TC-P7-E1027-CON-03 records them as Not specified (GAP-1237) and adds no rules. |
| RWB-P7-E1027-CON | R-22045 | GAP-1403 |  | Local decision-record contract: record schema, table shape, shared-topic envelope and message catalogue | Column types, widths, constraints, DDL and hash algorithm are not in the sources. Publishing them needs invented values. Not specified in the source documents (GAP-1403). |
| RWB-P7-E1027-CON | R-22507 | GAP-2210 |  | No source gives the case status history, the transfer from-queue or the decision-record read behind the timeline | Section 12 text is not in this chunk, so the query-path edit cannot be made. The decision-record query filter and field list are not in the sources. Not specified in the source documents (GAP-2210). |
| RWB-P7-E1028-APP | R-06687 | DOR-RWB-P7-E1028-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source docs. Searched 03 Requirements and story sets; placeholder kept in header table. |
| RWB-P7-E1028-APP | R-06690 | DOR-RWB-P7-E1028-APP-22 | header | Definition of Ready item 22 Fake published: Fail | RWB-P3-E1028-CON names four fakes but no fake library version is recorded as published. Searched story sets; placeholder kept in header table. |
| RWB-P7-E1030-APP | R-17946 | DOR-RWB-P7-E1030-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-38 state rows sit in a section outside this chunk; no current story text here to anchor the empty, loading, error and no-access states. |
| RWB-P7-E1030-APP | R-17947 | DOR-RWB-P7-E1030-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Guardrails section is outside this chunk; the personal-data classing cannot be corrected from the text supplied. |
| RWB-P7-E1030-APP | R-17949 | DOR-RWB-P7-E1030-APP-18 | 8 | Definition of Ready item 18 Open decisions: Partial | No source confirms DL23 or DL25. The directive is not evidence of confirmation, so the open decisions remain open. |
| RWB-P7-E1030-APP | R-26230 | CG-ALL-6946 | 3, 3.1 | Flyway file V1030_1__rebalance_ledger.sql is not in the V0001..Vnnnn form | Migration line is outside this chunk. Service Template Spec v1 3.1 gives no next free rwb-decision number; the story sequence is not in the sources. Not invented. |
| RWB-P7-E1032-APP | R-06704 | DOR-RWB-P7-E1032-APP-22 | header | Definition of Ready item 22 Fake published: Fail | Searched the probe cache and PRDs for RWB-P7-E1032-CON fake versions; none recorded as published. Recording one would invent it. Header unchanged. |
| RWB-P7-E1032-APP | R-06705 | DOR-RWB-P7-E1032-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Only the /v1 path of base /api/recovery/decision/v1 (section 12.1) is in the sources; no contract release version found. Header placeholder kept. |
| RWB-P7-E1032-APP | R-11201 | CG-ALL-6952 | 4, 12.1 | HTTP errors with no message ID: 401 no session; 404 the entry is absent | Error and Message Standard v4 has no message for 401 no session or 404 entry absent; MSG-GEN-006 does not fit. No ID invented; placeholders kept. |
| RWB-P7-E1032-APP | R-17954 | DOR-RWB-P7-E1032-APP-11 | 7, 11 | Definition of Ready item 11 Guardrails: Partial | The guardrail text naming the P2 personal-data fields is in sections 7 or 11, which are not in this chunk. No anchor for an edit. |
| RWB-P7-E1032-APP | R-17957 | DOR-RWB-P7-E1032-APP-4 | 7, 8, 16 | Definition of Ready item 4 Business rules: Partial | Criteria for BR2, BR5, BR7, BR9, BR10, BR12 sit in section 7, not in this chunk. Cannot add criteria or TC rows without that text. |
| RWB-P7-E1032-APP | R-17958 | DOR-RWB-P7-E1032-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | Standard texts cannot be copied while CG-ALL-6955 and CG-ALL-6956 require a new ID first. |
| RWB-P7-E1032-APP | R-26235 | CG-ALL-6961 | 3 | Flyway file V1032_1__decision_intake_attach_entry.sql is not in the V0001..Vnnnn form | Migration name is not in the story text given. Next number of the rwb-decision Flyway sequence is not in the sources searched (22 Microservice Realignment, _work/msr/directive/stage). Not specified in the source documents (CG-ALL-6961). |
| RWB-P7-E1039-APP | R-06712 | DOR-RWB-P7-E1039-APP-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | No rwb-case contract fake name or published fake version in sources. Searched Service Contract Catalog v1 (05 Technical architecture): rows say only 'its fake'. Naming one would invent it. |
| RWB-P7-E1039-APP | R-17962 | DOR-RWB-P7-E1039-APP-15 | find it | Definition of Ready item 15 INVEST: Partial | No source gives a two-week fit for INVEST Small. Size is set by the squad at refinement (Size row, DOR-RWB-P7-E1039-APP-16). No value added. |
| RWB-P7-E1039-APP | R-26242 | CG-ALL-6972 | 3, 3.1 | Flyway file V1039_1__access_ledger.sql is not in the V0001..Vnnnn form | Next free number of the rwb-decision Flyway sequence is not in the sources. The migration sentence is outside the supplied story parts. V1039_1 kept. Owner: Solution architect. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11727 | RWB-P7-E1020-APP | CG-ALL-6892 | 12.1 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} in the owner's yaml through the contract story; section 12.1 keeps the operation. |
| CDC-11733 | RWB-P7-E1020-APP | DOR-RWB-P7-E1020-APP-8 | find it | Add path GET /rule-models/{packageCode}/{version}. |
| CDC-11756 | RWB-P7-E1021-APP | CG-ALL-6906 | 12.1 | Publish GET /api/recovery/decision/v1/rule-models/{packageCode}/{version} through the owner's contract story, or remove the operation from section 12.1. |
| CDC-11773 | RWB-P7-E1027-APP | CG-ALL-6918 |  | Remove the closed enum on approvalLevel so that LOV-APPROVAL-LEVEL values are data accepted without a code change. |
| CDC-11776 | RWB-P7-E1027-APP | DOR-RWB-P7-E1027-APP-8 |  | Remove the closed enum on approvalLevel so LOV-APPROVAL-LEVEL values are data. Event type part resolved in section 12.3. |
| CDC-11803 | RWB-P7-E1028-APP | CG-ALL-6931 | 13 | Remove the closed enum on approvalLevel so LOV-APPROVAL-LEVEL values are accepted as data. |
| CDC-11804 | RWB-P7-E1028-APP | DOR-RWB-P7-E1028-APP-8 | 13 | Remove the closed enum on approvalLevel so LOV-APPROVAL-LEVEL values are accepted as data. |
| CDC-11818 | RWB-P7-E1030-APP | CG-ALL-6941 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log in rwb-decision.yaml through the CON story, owner Solution architect. |
| CDC-11819 | RWB-P7-E1030-APP | CG-ALL-6942 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} in rwb-decision.yaml through the CON story, owner Solution architect. |
| CDC-11821 | RWB-P7-E1030-APP | DOR-RWB-P7-E1030-APP-8 | 12.1 | Publish both GET /api/recovery/decision/v1/decision-log and GET /api/recovery/decision/v1/decision-log/{entryId} in rwb-decision.yaml through the CON story. |
| CDC-11865 | RWB-P7-E1039-APP | CG-ALL-6967 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log in rwb-decision.yaml through the owning contract story, or remove the operation from 12.1 |
| CDC-11866 | RWB-P7-E1039-APP | CG-ALL-6968 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} in rwb-decision.yaml through the owning contract story, or remove the operation from 12.1 |
| CDC-11867 | RWB-P7-E1039-APP | DOR-RWB-P7-E1039-APP-8 | 12.1 | Publish both decision-log GET paths (list and {entryId}) in rwb-decision.yaml through the owning contract story, or remove them from 12.1 |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11699 | RWB-P7-E1018-APP | DOR-RWB-P7-E1018-APP-8 | 4, 12.1 | Event type corrected in 12.4 under CG-ALL-6880. |
| CDC-11701 | RWB-P7-E1018-APP | CG-ALL-6881 | 4, 14 | Add a new message ID for a rule reference that is half given, a version label the registry does not hold, or a decision code outside LOV-DECISION (ruleId, ruleVersion, decisionCode). The story then cites that ID in section 14 in place of MSG-P7-009 for this use. |
| CDC-11702 | RWB-P7-E1018-APP | CG-ALL-6882 | 4, 14 | Add a new message ID for an answered entry that does not match the chain (chainSeq named). The story then cites that ID in section 14 in place of MSG-P7-012 for this use. |
| CDC-11705 | RWB-P7-E1018-APP | DOR-RWB-P7-E1018-APP-9 | 14 | MSG-P7-009 use waits on the standard's ID (CG-ALL-6881); MSG-P7-012 use also waits (CG-ALL-6882). BR4 unheld-label message is unassigned. |
| CDC-11734 | RWB-P7-E1020-APP | CG-ALL-6897 | 4, 14 | Add a new message ID for a record refused for a missing or invalid field, text naming the field; the story then cites it in sections 5 and 14 in place of MSG-P7-009. |
| CDC-11735 | RWB-P7-E1020-APP | CG-ALL-6898 | 4, 14 | Add a new message ID for the owning-service no-version-in-force refusal (package code and version label only), since the story's use differs from the MSG-P3-027 Raised-when text. |
| CDC-11763 | RWB-P7-E1021-APP | CG-ALL-6909 | 4, 14 | Add a new message ID for the ledger schema refusal (ruleVersion, decisionCode, versions, state or checksum); the story cites it once it exists |
| CDC-11764 | RWB-P7-E1021-APP | CG-ALL-6910 | 4, 14 | Add a new message ID for the decision log chain break on the page; the story cites it once it exists |
| CDC-11766 | RWB-P7-E1021-APP | DOR-RWB-P7-E1021-APP-9 | 14 | Add new message IDs for the ledger schema refusal and the chain break; story cites them once they exist |
| CDC-11835 | RWB-P7-E1032-APP | CG-ALL-6955 | 14 | MSG-P7-009 row reverted |
| CDC-11836 | RWB-P7-E1032-APP | CG-ALL-6956 | 14 | MSG-GEN-006 row reverted |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11718 | RWB-P7-E1018-APP | CG-ALL-6885 | 18 | Align the test lists of the other five requirements in section 18 with the story (or the reverse) |
| CDC-11747 | RWB-P7-E1020-APP | CG-ALL-6901 | 18 | Align the test-case lists of the four requirements in RTM v7 with section 18 of RWB-P7-E1020-APP in the next RTM version. |
| CDC-11768 | RWB-P7-E1021-APP | CG-ALL-6913 | 18 | Align the test lists for REQ-CWC-010, REQ-CWC-016, REQ-WKM-003 and REQ-CWC-005 with RWB-P7-E1021-APP section 18 in its next version. |
| CDC-11781 | RWB-P7-E1027-APP | CG-ALL-6920 | 18 | Align the REQ-DRI-004 and REQ-DRI-005 test lists with section 18 of RWB-P7-E1027-APP in the next RTM version. |
| CDC-11797 | RWB-P7-E1027-CON | Test cases not in Test Cases v8 | 16, 18 | Sections 16 and 18 were edited: TC-P7-E1027-CON-08 to 11 were added and the section 18 mapping row now lists TC-08. |
| CDC-11812 | RWB-P7-E1028-APP | CG-ALL-6936 | 18 | Align the trace lists of REQ-CWC-011, REQ-CWC-012 and the third listed requirement with section 18 of RWB-P7-E1028-APP |
| CDC-11825 | RWB-P7-E1030-APP | CG-ALL-6944 | 18 | Align the REQ-CWC-015 and REQ-RDF-012 test lists in RTM v7 with RWB-P7-E1030-APP section 18 in the next RTM version. |
| CDC-11853 | RWB-P7-E1032-APP | GAP-3144 | 7 | Record the primary and secondary AC split so the fifteen legacy criteria are counted once, against RWB-P5-E1032-APP. |
| CDC-11855 | RWB-P7-E1032-APP | CG-ALL-6959 | 18 | Align the test lists for REQ-DCM-007, REQ-DCM-005 and REQ-DRI-004 to the test cases of RWB-P7-E1032-APP section 18 (TC-E1-032-01 to TC-E1-032-15; TC-E1-032-02 to TC-E1-032-07 and TC-E1-032-11; TC-E1-032-16 and TC-E1-032-17), removing the other-story IDs from those rows. |
| CDC-11881 | RWB-P7-E1039-APP | CG-ALL-6970 | 18 | Align REQ-ACA-006 and REQ-ACA-008 test lists with story section 18 at the next RTM version; section 18 kept as is in this pass. |
| CDC-11903 | RWB-P7-E1046-APP | CG-ALL-6982 | 18 | Align REQ-OCC-001 and REQ-OCC-002 test lists with section 18 of this story in the next RTM version. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11740 | RWB-P7-E1020-APP | GAP-2443 | find it | Add the package-artifact operation to the P7 row and the API Specification at the next version, with the same base, model-owner identity and checksum in the answer. |
| CDC-11778 | RWB-P7-E1027-APP | GAP-1235 | 3 | Record the decision-record append as a local in-process operation on task queue rwb-decision under DP-03; add no REST write path unless an out-of-process caller is named. |
| CDC-11792 | RWB-P7-E1027-CON | GAP-1235 | 7 | Add a local operation: the decision-record append, in process on task queue rwb-decision under DP-03; no REST row. |
| CDC-11814 | RWB-P7-E1028-APP | GAP-0022 | 4 | Record PLT as owner of EV-18 TimerDue (retired); EV-19 TimerBreached stays with P3 |
| CDC-11824 | RWB-P7-E1030-APP | GAP-2205 | 12.6, 14 | Name the reporting feed and its fields in the P9 contract before wave 1 closes; name the delivery service for MSG-P3-028, MSG-P3-011 and MSG-P3-029; state whether the run record and rerun surface are a workflow read plus Schedule trigger or a published operation; add the agreed rows. |
| CDC-11871 | RWB-P7-E1039-APP | GAP-0661 | none | Baseline the two read-only operations on /api/recovery/integration/v1 and the eight consumed operations as the Proposed fix states. |
| CDC-11882 | RWB-P7-E1039-APP | GAP-2039 |  | Add access_log row to the Tables sheet: rwb_access, owner P4 rwb-access, append-only, with its DB story in RWB-SVC-P4 at next revision. |
| CDC-11885 | RWB-P7-E1039-APP | GAP-0165 |  | Add access log table row in rwb_access (P4), append-only, created by RWB-P4-E1039-DB, with columns and retention defined there. |
| CDC-11886 | RWB-P7-E1039-APP | GAP-2069 |  | Add access_log as an append-only table in rwb_access (P4) behind GET /admin/access-log, created by the P4 DB story. |
| CDC-11893 | RWB-P7-E1046-APP | GAP-1023 | 11 | Use /cases/{caseId}/generated-documents on /api/recovery/document/v1 (ASM-101); add template_code varchar(30) and template_version integer beside template_id and treatment_id, and a partial unique index on (treatment_id, template_id) where state is DRAFT and is_active (ASM-103). |

### RWB-P6-E1046-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11888 | RWB-P7-E1046-APP | DOR-RWB-P7-E1046-APP-22 |  | Record the published contract fake library version that this story builds against. |
| CDC-11896 | RWB-P7-E1046-APP | GAP-1063 | find it | Map legacy POST /admin/reference-loads to POST /admin/templates upload plus approve; keep SHA-256 hash rule as upload idempotency; TC-E1-046-09 asserts refusal on mapped operation. |
| CDC-11897 | RWB-P7-E1046-APP | GAP-1065 | find it | Fix one resolution rule for body_ref (P5 rwb-document contract or service container) before RWB-P6-E1052 build; story keeps body_ref opaque. |
| CDC-11898 | RWB-P7-E1046-APP | GAP-1066 | 3 | Section 3 approver bullet keeps the conversion as Not specified in the source documents. |
| CDC-11899 | RWB-P7-E1046-APP | GAP-1067 | find it | Baseline property lists for TemplatePage, Template, TemplateApproval and TemplateWithdrawal in camelCase; add current-version filter (code, language, onDate) to API-P6-003. |
| CDC-11901 | RWB-P7-E1046-APP | GAP-2345 | find it | Add additive current-version read (for example GET /admin/templates/current with code, language, onDate) within major version 1 before wave-1 contract tests. |
| CDC-11902 | RWB-P7-E1046-APP | GAP-2453 | 3 | Section 3 read-path bullet reverted to Not specified in the source documents. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11698 | RWB-P7-E1018-APP | DOR-RWB-P7-E1018-APP-14 | find it | Confirm and record the signed epic design sign-off for EP01; none is recorded in the source documents. |
| CDC-11729 | RWB-P7-E1020-APP | DOR-RWB-P7-E1020-APP-14 | header | Record the signed epic design sign-off covering this story; the source documents hold none. |
| CDC-11759 | RWB-P7-E1021-APP | DOR-RWB-P7-E1021-APP-14 | header | Record the signed epic design sign-off for this story and replace the placeholder in the header table. |
| CDC-11820 | RWB-P7-E1030-APP | DOR-RWB-P7-E1030-APP-14 | not located | Confirm the signed epic design sign-off against the epic design record and record it there. |
| CDC-11831 | RWB-P7-E1032-APP | DOR-RWB-P7-E1032-APP-14 | Metadata | Record the signed epic design sign-off for RWB-SVC-P7 so DoR item 14 can pass |
| CDC-11887 | RWB-P7-E1046-APP | DOR-RWB-P7-E1046-APP-14 |  | Record the signed sign-off of the epic design. No signed epic design is in the story or the source documents. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11736 | RWB-P7-E1020-APP | DOR-RWB-P7-E1020-APP-11 | 11 | Set the personal-data classification of decision_log_entry fields to match the story's statement that it carries identifiers and facts only. |
| CDC-11745 | RWB-P7-E1020-APP | GAP-2439 | 11 | Publish the rule_package_version columns (state, valid-from, approver, DRL, checksum) and confirm the artifact payload with RWB-PLT-E1072-CON. |
| CDC-11786 | RWB-P7-E1027-CON | CG-ALL-6924 | find it | Record ce_type as the CloudEvents type attribute of the envelope (Kafka Topic and Event Catalog v1, Envelope sheet), or add the name to Fields. |
| CDC-11787 | RWB-P7-E1027-CON | CG-ALL-6925 | find it | Record ce_subject as the CloudEvents subject attribute of the envelope (Kafka Topic and Event Catalog v1, Envelope sheet), or add the name to Fields. |
| CDC-11868 | RWB-P7-E1039-APP | CG-ALL-6966 | 12.7 | Record break_glass_grant as an object owned by RWB-P4-E1039-APP in LDM v9, or give its dictionary name |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11790 | RWB-P7-E1027-CON | DOR-RWB-P7-E1027-CON-7 | 11 | Confirm ce_type and ce_subject as CloudEvents envelope attributes, or register them as fields. |
| CDC-11870 | RWB-P7-E1039-APP | DOR-RWB-P7-E1039-APP-7 | none | Add break_glass_grant as an entity, or name the P4 table as the LDM names it; this story holds no grant on it. |
| CDC-11889 | RWB-P7-E1046-APP | CG-ALL-6978 |  | Add template_use as a dictionary entity or record it as a new object in the owning document. Nearest names: template_code, template, template_id. |
| CDC-11890 | RWB-P7-E1046-APP | CG-ALL-6979 |  | Confirm the dictionary name for the entry-id field of decision_log_entry, or record the object in the owning document. Nearest names: identity_ref, entry_date, external_ref. |
| CDC-11892 | RWB-P7-E1046-APP | DOR-RWB-P7-E1046-APP-7 | 11 | Add entity template_use (rwb_decision) and field entry_ref to LDM v9 and Data Classification v5. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11703 | RWB-P7-E1018-APP | CG-ALL-6883 | 16 | Add rows TC-E1-018-15 and TC-E1-018-16 to tab Story test cases, with Given, When and Then copied from their criteria in section 16 of the story. |
| CDC-11796 | RWB-P7-E1027-CON | CG-ALL-6927 | 16 | Add rows for TC-P7-E1027-CON-01 to TC-P7-E1027-CON-07 with Given, When and Then copied from the criteria they cover in the next version. |
| CDC-11806 | RWB-P7-E1028-APP | CG-ALL-6934 | 16 | Add TC-E1-028-14 to tab Story test cases, with Given, When and Then copied from AC4 and BR6 in section 7. |
| CDC-11880 | RWB-P7-E1039-APP | CG-ALL-6969 | 16 | TC-02 to TC-10 covers restored to the story's own scenario numbers |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11704 | RWB-P7-E1018-APP | DOR-RWB-P7-E1018-APP-12 | 12.7, 16, 18 | TC-E1-018-17 added to section 16 for section 12.7. |
| CDC-11758 | RWB-P7-E1021-APP | DOR-RWB-P7-E1021-APP-12 | 12.7, 16, 18 | Add full tests for TC-E1-021-17 (AC6) and TC-E1-021-18 (AC5, AC6, table boundary) and align the section 18 test lists with RTM v7. |
| CDC-11789 | RWB-P7-E1027-CON | DOR-RWB-P7-E1027-CON-12 | 12.7, 16, 18 | Register TC-P7-E1027-CON-01 to -08 in Test Cases v8; align section 18 test lists of this story with its RTM v7 row. |

### RWB-P3-E1018-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11711 | RWB-P7-E1018-APP | GAP-0676 |  | Agree and record the field-level OpenAPI schema: required flags, GET /cases page and sort parameters, caseNo pattern, error codes per operation. |
| CDC-11723 | RWB-P7-E1018-APP | GAP-0572 |  | One operation for the business date, paged by page and size; default and maximum page size fixed in the published contract; per-account read refused under DP-11. |
| CDC-11725 | RWB-P7-E1018-APP | GAP-1038 |  | Name the rwb_document login and grants under DP-02; publish case-read request and response field names and the not-found message ID in RWB-P3-E1018-CON. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11712 | RWB-P7-E1018-APP | GAP-2433 |  | Write MSG-P7-009 (names the field and case reference) and MSG-P7-012 (names the chain position) as sentences; add both rows to the API specification. |
| CDC-11716 | RWB-P7-E1018-APP | GAP-2434 |  | Add finalCall to the query parameters of API-P7-006; fix the creation-filter answer as a page of entries with the thirteen fields this story names. |
| CDC-11738 | RWB-P7-E1020-APP | GAP-0345 | find it | Publish JOB-03 step state on the rwb-case run result; keep the catalogue read and rerun on the P1 job catalogue; fix the rerun facade for a workflow step in the P1 contract before wave 1 exit. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11721 | RWB-P7-E1018-APP | GAP-0982 |  | Add the case-authority request and answer schema for POST /authorise, publish with RWB-P4-E1037-CON, record caller teams and regions in T3.1, list masking field IDs with version. |
| CDC-11858 | RWB-P7-E1032-APP | GAP-0744 | find it | Add a case-side document reconcile job run daily with overlap policy SKIP and a catch-up window; time of day Not specified in the source documents (GAP-0744). |
| CDC-11861 | RWB-P7-E1032-APP | GAP-0994 | find it | Register the JOB-12 Schedule for the business-hours window with overlap policy SKIP and a catch-up of one run; hold thresholds as environment values; lag alert identifier is a placeholder until the Error and Message Standard names it. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11728 | RWB-P7-E1020-APP | CG-ALL-6893 | 13 | Create story RWB-P7-E1073-CON for the rule-package contract named in DP-04, or name the existing story that holds it. |
| CDC-11730 | RWB-P7-E1020-APP | DOR-RWB-P7-E1020-APP-17 | header, 13 | Create RWB-P7-E1073-CON (see CG-ALL-6893) or name the existing dependency; the named dependency must then exist. |
| CDC-11731 | RWB-P7-E1020-APP | DOR-RWB-P7-E1020-APP-21 | header | Publish contract story RWB-P7-E1020-CON for the rwb-decision REST contract and name it as a contract dependency of this story. |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11744 | RWB-P7-E1020-APP | GAP-2441 | 3 | Fix business date as a record attribute and queue and owner identifiers as named actions payload members at contract review. |
| CDC-11777 | RWB-P7-E1027-APP | GAP-1238 | 3 | Story now states rwb.decision.DecisionRecorded.v1 per EV-08 and cites GAP-1238 for the platform contract's differing type; the mismatch stays open in that contract. |
| CDC-11791 | RWB-P7-E1027-CON | Two ce_type values are published for DecisionRecorded | 7, 12.3 | AC6 and the §12.3 type now both use rwb.decision.DecisionRecorded.v1 as in the Kafka catalog, the same type the platform library writes. |

### RWB-P7-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11774 | RWB-P7-E1027-APP | DOR-RWB-P7-E1027-APP-21 |  | Build status moved from Not started to Done. |
| CDC-11775 | RWB-P7-E1027-APP | DOR-RWB-P7-E1027-APP-22 |  | Publish the contract fake library and record its version. |
| CDC-11780 | RWB-P7-E1027-APP | GAP-1237 | 3 | Freeze the canonical form (ordered field list, UTF-8, no whitespace, null as empty string, 64 lowercase hex) and publish one cross-language fixture for all writers and the verifier. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11783 | RWB-P7-E1027-APP | GAP-1617 | 8 | Add reference-data rows: completeness target and gap alert threshold at 5 minutes (Architecture v5); strict-mode wait bound Not specified in the source documents (GAP-1617), to confirm at ADR-022 sign-off. |
| CDC-11859 | RWB-P7-E1032-APP | GAP-0745 | find it | Add a rwb-case parameter for the case-side switch, default on, owner RW-COE; key Not specified in the source documents (GAP-0745); off means the case side writes nothing from an event. |
| CDC-11862 | RWB-P7-E1032-APP | GAP-1200 | header | Record that the communications module declares no business-owned notice parameter, so DP-06 applies to it as a path without a value. |

### RWB-P4-E1039-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11874 | RWB-P7-E1039-APP | GAP-0359 | 12 | Name POST /admin/break-glass-grants as the grant operation and the local-record fault point and evidence location at the integration pack review before the SIT run. |
| CDC-11875 | RWB-P7-E1039-APP | GAP-0780 | 12 | Confirm the DP-03 library table name in rwb_access with the DP-03 owner, keep the legacy path as an alias of POST /admin/break-glass-grants, and fix the actions keys in the contract. |
| CDC-11877 | RWB-P7-E1039-APP | GAP-0782 | 11 | Confirm the break_glass_grant table, its unique partial constraint and the access-log retention and partition parameters, with DL26 set by Compliance. |

### RWB-P4-E1039-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11876 | RWB-P7-E1039-APP | GAP-0781 | 12 | Add the grant end and read paths under the DP-13 base, the expired-session message id to the message catalogue, and the full grant answer and grant state field. |
| CDC-11879 | RWB-P7-E1039-APP | GAP-2339 | 12 | Define how grant ID and incident reference reach a consuming service (claim or call), their lifetime and reuse bound, and add the mechanism to the session contract. |
| CDC-11883 | RWB-P7-E1039-APP | GAP-2076 |  | State that the access entry carries the version the owning service applied at event time; rwb-decision registry stays the source of version and effective date. |

### OTHER:RWB-PLT-DB (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11726 | RWB-P7-E1018-APP | GAP-2438 | header | Name the rwb-decision database login and its secret-store entry, with the migration role and the application role kept apart |
| CDC-11742 | RWB-P7-E1020-APP | GAP-3207 | 3 | Publish the per-service database login name of rwb-case in RWB-PLT-DB and the rwb-case DB story. |

### RWB-P3-E1020-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11732 | RWB-P7-E1020-APP | DOR-RWB-P7-E1020-APP-22 | 13 | Publish the contract fake and record its library version as published; the story then names that version. |
| CDC-11741 | RWB-P7-E1020-APP | GAP-3072 | find it | Publish case element and stage outcome field names, queue-and-members element, handler choice rule (fewest open deviations, no cap), DEV-HANDLER parameter row, and confirm the four handler role codes against TSD S8 T6.1. |

### OTHER:Build Notes v6 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11754 | RWB-P7-E1020-APP | GAP-3173 | 1 | State wave 1 delivery of rwb-deviation in the service epic and wave plan; rwb-deviation service wave governs later stories |
| CDC-11864 | RWB-P7-E1032-APP | GAP-3174 | header | State wave 1 delivery of rwb-partner in the service epic and the wave plan, and let the rwb-partner service wave govern its later stories. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11757 | RWB-P7-E1021-APP | CG-ALL-6907 | 13 | Create RWB-P7-E1073-CON, or name the existing story that carries the same capability as the DP-04 contract dependency. |
| CDC-11760 | RWB-P7-E1021-APP | DOR-RWB-P7-E1021-APP-17 | 13 | Create RWB-P7-E1073-CON, or name the existing story that carries the same capability as the DP-04 contract dependency. |

### RWB-P3-E1021-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11761 | RWB-P7-E1021-APP | DOR-RWB-P7-E1021-APP-22 | header | Record the published contract fake library version and replace the placeholder in the header table. |
| CDC-11771 | RWB-P7-E1021-APP | GAP-1036 | 7 | Publish the AsyncAPI 3.0 document and registered JSON schemas for rwb.document.DocumentStored.v1 and DocumentFieldsExtracted.v1 with required fields and BACKWARD rule; hand DocumentStored schema to RWB-P3-E1021-CON as trigger fixture. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11762 | RWB-P7-E1021-APP | DOR-RWB-P7-E1021-APP-8 | 12.1 | Reconcile the payload of rwb.decision.RulePackageInForce.v1 with the rwb-decision contract so both sources match. Also publish the 12.1 model path per CG-ALL-6906. |
| CDC-11813 | RWB-P7-E1028-APP | GAP-2203 | 4 | Add escalated_to_role and escalated_at (DF-WRK-043, DF-WRK-044) with type, length and optionality, and the TimerBreached payload field list to the event catalogue |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11769 | RWB-P7-E1021-APP | GAP-0990 | 7 | Publish the authorise request and answer schema with its legalHold attribute, confirm the matrix version label in force at the release date with the matrix owner, and tabulate the Queue and allocation letters in TSD P4 T6.1. |
| CDC-11873 | RWB-P7-E1039-APP | GAP-0966 | 12 | Add the rule-package actions, request and answer fields and the change decision code to POST /authorise, and stub them in the contract fake. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11782 | RWB-P7-E1027-APP | GAP-1622 | 8 | Add a contract version to the DecisionRecorded event, record it on the ledger entry, and have the consumer accept known versions and dead-letter unknown ones. |
| CDC-11798 | RWB-P7-E1027-CON | GAP-1622 | 16 | Add a contract version to the DecisionRecorded event, record it on the ledger entry, and route an unknown version to the dead-letter topic. |

### RWB-P6-E1046-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11894 | RWB-P7-E1046-APP | GAP-1064 | n/a | Add the rwb-source-data data-dictionary contract (GET /api/recovery/source-data/v1/admin/data-dictionary/fields) to C, or confirm coverage; until then build against it as a fake with one hop and a 2 s timeout (DP-11). |
| CDC-11895 | RWB-P7-E1046-APP | GAP-1068 | n/a | Refuse a request whose declared right is absent with 403 MSG-P4-002 from the service's operation configuration; add DP-08 with RWB-P4-E1037-CON if a service-side authorise call is required. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20686 | RWB-P7-E1020-APP | R-28528 |  | Section 'Epic 1 and the 19 services' already states S8 rwb-deviation takes Epic 1 stories in wave 1 (GAP-3173). |
| CDC-20687 | RWB-P7-E1032-APP | R-28573 |  | Section 'Epic 1 and the 19 services' already states S9 rwb-partner takes Epic 1 stories in wave 1 (GAP-3174). |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20869 | RWB-P7-E1030-APP | R-28557 |  | Operating values per environment belong in rwb-case deployment values and runbooks; section 3.2 already gives the 2 API pods. |
| CDC-20870 | RWB-P7-E1032-APP | R-22060 |  | Per-environment values need SIT measurement and scan throughput; they belong in the SCB IT infrastructure environment files. |

### OTHER:Recovery Workbench FSD P3, section A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11700 | RWB-P7-E1018-APP | GAP-1549 | find it | Restate the A1.5 ACE read path as a read through the rwb-source-data contract (ADR-010); keep the business-key link rules unchanged. |

### OTHER:rwb-source-data service API document (entry-candidates read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11706 | RWB-P7-E1018-APP | GAP-0571 | find it | Publish GET /api/recovery/source-data/v1/entry-candidates with businessDate and threshold required, page and size optional, EntryCandidatePage response, statuses 400, 401, 403, 409, 422, 503, and its OpenAPI 3.1 fragment. |

### RWB-P1-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11707 | RWB-P7-E1018-APP | GAP-0575 | find it | Return REC-05 breaks in the candidates response with keyType, businessKey, viewName and businessDate; the durable list stays in RWB-P1-E1011-APP. |

### OTHER:RWB-SVC-P3 database story and the service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11708 | RWB-P7-E1018-APP | GAP-0675 | find it | Allocate the rwb-case login name with its grants (schema rwb_case only) and secret reference, and record it in the service catalogue. |

### OTHER:P1 extension-table API document (account_ext and party_ext PUT operations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11709 | RWB-P7-E1018-APP | GAP-0573 | find it | P1 writes account_ext.dispute_open and the party_ext flags through two PUT operations by business key; the body carries all four party flags and P1 validates the caller's token. |

### OTHER:rwb-case reference-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11710 | RWB-P7-E1018-APP | GAP-0576 |  | Return product_group as the unvalidated product_category value; any LOV-PRODUCT mapping and out-of-list handling sit in the consumer's reference-data contract. |

### OTHER:TSD P7 v2 T3.1 and T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11713 | RWB-P7-E1018-APP | GAP-2435 | 11 | Restate DF-DEC-002 as an indexed business key with no foreign key; drop the recovery_case row of T3.3; state that the ALS business date is carried inside inputs_ref. |

### OTHER:Rule-row catalogue of package ENTRY (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11714 | RWB-P7-E1018-APP | GAP-2436 |  | Name the admitting ENTER rule ID of package ENTRY, then copy that identifier into the registry fixture of RWB-P7-E1018-APP. |

### RWB-P1-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11715 | RWB-P7-E1018-APP | GAP-3162 |  | Write party_ext and account_ext rows in the P1 story and read them back by contract; the case tables stay in P3. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11717 | RWB-P7-E1018-APP | GAP-0674 |  | Publish the gateway-bff composite route for SCR-02 and SCR-03: path, parallel calls, merge order, masking rules and the 2 s budget. |

### OTHER:Recovery Workbench User Story Worked Example v6 and WP C-WEX work package index (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11719 | RWB-P7-E1018-APP | GAP-3206 |  | Read the (E1-018) heading as a scheduling label; RWB-E1-020 stays the subject; correct the heading in the work package index of the next run. |

### OTHER:Recovery Workbench Gap Register v1 (GAP-3213 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11720 | RWB-P7-E1018-APP | GAP-3213 | 18 | Record that the E3 integration trace (RWB-ITG-E3013-ITG, RWB-ITG-E3017-ITG, RWB-ITG-E3026-ITG) is accepted; list legacy slices RWB-E1-069, RWB-E1-018, RWB-E2-006 |

### RWB-P7-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11722 | RWB-P7-E1018-APP | GAP-2437 |  | Record that the secondary slice builds against platform contracts and the section 12.8 fakes and reads the same service's wave-1 tables in its own schema. No dependency row moves. |

### OTHER:Platform deployment topology and rwb-case environment values (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11724 | RWB-P7-E1018-APP | GAP-0677 |  | Publish rwb-case cluster names, node pools, replicas, resources, zone spread, ingress class and probe paths as environment values files, not chart defaults. |

### OTHER:Business requirements document, section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11737 | RWB-P7-E1020-APP | GAP-1456 | find it | State the rule in section 8.2: stories keep the business-epic wave, the owning service starts in its Architecture v5 wave, and the delivery lead confirms the wave per story at build sequencing. |

### OTHER:Service Catalog and RWB-PLT-DB stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11739 | RWB-P7-E1020-APP | GAP-0684 | find it | Allocate the rwb-case service login with schema rwb_case in the 19-schema list, derived from the schema name, stored in Key Vault; record it before first deployment. Name Not specified in the source documents (GAP-0684). |

### RWB-P3-E1020-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11743 | RWB-P7-E1020-APP | GAP-3208 | 3 | Fix the Temporal cron expression of the DailyCaseRun schedule where the deployment is described. |

### RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11746 | RWB-P7-E1020-APP | GAP-1336 | 12 | Fix the model answer, inputs snapshot and announcement payload in the registry contract; name plan-status section with gateway-bff route owner; publish per-service login. |

### OTHER:WP C-WEX work package index (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11748 | RWB-P7-E1020-APP | GAP-3206 | 1 | Correct the heading E1-018 to RWB-E1-020 at the next run; the story keeps RWB-E1-020 as its subject. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11749 | RWB-P7-E1020-APP | GAP-3209 | 7 | Add a criterion-ownership column to the Legacy map sheet listing the single owning new story for each of the thirteen legacy criteria |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11750 | RWB-P7-E1020-APP | GAP-0687 | 1 | Expose replicas, autoscaling bounds, node pool, connection pool size and history archive as chart values with documented defaults; record SIT findings there |

### OTHER:Functional Specification P4 and Technical Specification P4 (rwb-access) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11751 | RWB-P7-E1020-APP | GAP-0987 | 9 | Record the authorise attribute set, matrix version PM-2026.11 in force with PM-2026.12 from 2026-12-01, and the Queue and allocation role roster |

### OTHER:P7 message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11752 | RWB-P7-E1020-APP | GAP-2442 | 5 | Approve wording for MSG-P7-009 and the chain-break warning; ID, named field and same-day Compliance report stay fixed |

### RWB-S8-E1020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11753 | RWB-P7-E1020-APP | GAP-3073 | 1 | Take event names and consumers from TSD S8 T0.2 and T5.2.1; build behind service baseline with no own element; DP platform rows are wave 0 preconditions; keep wave 1 |

### OTHER:Template and Rules (section 1 worked example) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11755 | RWB-P7-E1020-APP | GAP-2150 | 1 | Confirm the RWB-P3-E1042-CON example and decide whether a microservice worked example replaces RWB-E1-020 or stands beside it |

### RWB-P3-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11765 | RWB-P7-E1021-APP | DOR-RWB-P7-E1021-APP-10 | n/a | Define empty, loading, error and no-access states for screen SCR-03 |

### OTHER:BRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11767 | RWB-P7-E1021-APP | GAP-1456 | header | State in section 8.2 that the business-epic wave is kept and the service starts in its own wave; delivery lead confirms wave per story at build sequencing |

### OTHER:Platform team chart values for rwb-decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11770 | RWB-P7-E1021-APP | GAP-0691 | 5 | Publish cluster, node pool, replica counts, ingress host, resource limits and disruption budget as chart values; no environment default shipped. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11772 | RWB-P7-E1021-APP | GAP-1037 | 5 | Allocate the rwb-document login name, its grants (schema rwb_document only) and its secret reference, and record them in the service catalogue. |

### RWB-P7-E1027-CON; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11779 | RWB-P7-E1027-APP | GAP-1236 | 11 | Fix the physical column list, the data-date column and the inputs digest in rwb_decision.sql and the contract baseline; publish the MSG-P7-009 and MSG-P7-003 entry format with the platform message catalogue. |

### OTHER:Batch and Scheduling (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11784 | RWB-P7-E1027-APP | GAP-1240 | 8 | In the next version, mark JOB-13 as retired; keep JOB-14 (02:00 chain check) as the only P7 Schedule; ingest stays continuous in RWB-P7-E1008-APP. |

### OTHER:P7 module specification (FSD) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11785 | RWB-P7-E1027-APP | GAP-1239 | 8 | Delete A2.6 and its acceptance criteria (AC-P7-006-01 to AC-EXC-P7-006-04) in the next version; move the reporting need to the rwb-reporting projection from events. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11788 | RWB-P7-E1027-CON | DOR-RWB-P7-E1027-CON-1 | 1 | Add the role contract owner of rwb-decision, or the role code it maps to, to the roles list. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11793 | RWB-P7-E1027-CON | GAP-1236 | 16 | Fix the physical column list, the data-date column and the inputs digest in rwb_decision.sql and the contract baseline; publish the MSG-P7-009 and MSG-P7-003 catalogue entry format. |

### OTHER:Platform decision-record library baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11794 | RWB-P7-E1027-CON | GAP-1402 | 16 | Publish the group, artefact name and publication channel of the decision-record library; confirm the no-case entry-id key and the incident route in the verification loop. |

### OTHER:Technical Specification Document P5 (T3.1; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11795 | RWB-P7-E1027-CON | GAP-1023 | 18 | Record POST /documents/generate from Architecture v5 slide 16 as the loser; add template_code varchar(30) and template_version integer beside template_id and treatment_id; build the partial unique index on (treatment_id, template_id) where state is DRAFT and is_active; read templates only through RWB-P6-E1046-CON. |

### OTHER:Business Requirements Document (NFR-033 to NFR-035); OTHER:FSD and platform reference data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11799 | RWB-P7-E1027-CON | GAP-1617 | 16 | Set the completeness target and the gap alert threshold at five minutes each as reference-data rows; the maximum strict-mode wait has no source value and needs confirming with Risk and Internal Audit at ADR-022 sign-off. |

### OTHER:Batch and Scheduling document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11800 | RWB-P7-E1027-CON | GAP-1240 | 7, 8 | Mark JOB-13 as retired; ingest continuous in RWB-P7-E1008-APP; JOB-14 is the only P7 Schedule |

### OTHER:FSD P7 module specification; OTHER:A2.6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11801 | RWB-P7-E1027-CON | GAP-1239 | 7 | Delete A2.6 and AC-P7-006-01 to AC-EXC-P7-006-04 next version; move reporting need to rwb-reporting projection from events |

### OTHER:generation contract baseline (P5 document generation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11802 | RWB-P7-E1027-CON | GAP-1024 |  | Declare POST /cases/{caseId}/generated-documents per Ownership Map and TSD P5 API-P5-016; fix three resources as schema constraints; publish four provider interfaces and decision record as typed contracts; declare one event with five fields; record S2, P1, P7 reads as consumed and faked |

### OTHER:TSD P7 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11805 | RWB-P7-E1028-APP | CG-ALL-6930 | 3, 5, 13, 16 | Record tr_declog_append_only as the append-only trigger object of decision_log_entry; it is not an LDM v9 or Data Classification v5 field. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11807 | RWB-P7-E1028-APP | DOR-RWB-P7-E1028-APP-11 | 11 | Confirm the personal-data class of each decision_log_entry field, including the user ID fields DF-DEC-030, DF-DEC-011 and DF-DEC-007, and align section 11 of RWB-P7-E1028-APP to it. |

### RWB-P4-E1028-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11808 | RWB-P7-E1028-APP | DOR-RWB-P7-E1028-APP-6 | 10 | Add the authorise check path the guard calls for the decision-log read; this story names the cached permission decision and no endpoint because DP-08 is not in the slice. |

### RWB-P3-E1028-CON; OTHER:A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11809 | RWB-P7-E1028-APP | GAP-1623 |  | State that P3 moves the case state and raises the approval task on ApprovalRequested; this service calls no case operation. |

### RWB-P3-E1028-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11810 | RWB-P7-E1028-APP | GAP-2016 |  | Declare the durable timer authoritative with the timer row as audit copy written by ApplyStateActivity in the same transaction and read back on reopen; retire JOB-05 in TC-E1-028-07 once settled. |

### RWB-P3-E1028-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11811 | RWB-P7-E1028-APP | GAP-2202 | 12.2 | Add P1 rows for RecoveryDataQuery.accountDates(List<UUID>) and holidays(LocalDate, LocalDate) with answer shape; record the wave 1 deviation pause operation in the P3 contract |

### API:(service not named); OTHER:TSD P4 T-A and policy pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11815 | RWB-P7-E1028-APP | GAP-0986 | 16 | Fix the authorise attributes for case and timer reads, including escalatedToRole and escalatedAt; name the matrix version at 30 November 2026; scope answer carries reason ESCALATED_TO_ROLE |

### OTHER:rwb-case values files and the runbook entry each alert links (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11816 | RWB-P7-E1028-APP | GAP-2204 |  | Set the poll window, catch-up window, breach band and record-failure rate in the rwb-case values files; confirm at UAT; record the agreed values in the runbook entry. |

### OTHER:TSD P7 T3.1 and the source for ASM-2337 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11817 | RWB-P7-E1028-APP | GAP-1324 | 8 | Placeholder GAP-1324 kept in section 8 BR9 and AC2; no value in sources |

### RWB-P3-E1030-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11822 | RWB-P7-E1030-APP | GAP-0354 | 10, 16 | Register JOB-06 as a Schedule in rwb-case, name its identifier, overlap policy and catch-up window at integration pack review; keep the P1 job catalogue as the operations facade for the run record and rerun; fix rwb.reporting.ReportPublished.v1 as the publish marker and the five-minute ledger target as the collection measure. |

### OTHER:FSD P9 (FEAT-RPT-02; OTHER:AC-P9-002-01; OTHER:AC-ALT-P9-002-01; OTHER:AC-ALT-P9-002-02) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11823 | RWB-P7-E1030-APP | GAP-1652 | 12.7 | P3 computes the queue measures on the business date and P9 publishes them, reading the case list count for the reconciliation; remove P9 computation of queue depth and ageing. |

### RWB-ITG-E1059-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11826 | RWB-P7-E1030-APP | GAP-0610 | 3, 5 | Keep legacy AC5 and TC-E1-059-05 with RWB-ITG-E1059-ITG; name the rwb-agent login and gateway route with their owners; add RWB-P5-E1053-CON to the contract row of a later version. |

### RWB-P3-E1030-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11827 | RWB-P7-E1030-APP | GAP-2206 | 3 | Decide whether a business date's run is a readable document resource; if so add the operation and ownership row and publish the run record schema in version 1 before reporting builds. |

### OTHER:rwb-case deployment values files and runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11828 | RWB-P7-E1030-APP | GAP-2207 | 3 | Set the replica, limit, ingress, alert, dead-letter and retry values per environment; confirm the zone and catch-up window at the SIT dry run. |

### OTHER:Build Notes v6 (RWB-TE-007) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11829 | RWB-P7-E1030-APP | GAP-3166 | 3 | Retire the Quartz schedule and job_catalog to traceability only; read JOB-06 and every other Job as a Temporal Schedule in the owning service. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11830 | RWB-P7-E1032-APP | CG-ALL-6951 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's contract story RWB-P4-E1037-CON |

### RWB-P7-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11832 | RWB-P7-E1032-APP | DOR-RWB-P7-E1032-APP-21 | Metadata | Create contract story RWB-P7-E1032-CON for the decision-log REST operations of section 12.1 |

### OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11833 | RWB-P7-E1032-APP | DOR-RWB-P7-E1032-APP-8 | 12.1 | Publish POST /api/recovery/access/v1/authorise. Story errors placeholder written; event type rename is in text outside the given parts. |

### RWB-S9-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11834 | RWB-P7-E1032-APP | GAP-1843 | header | Keep wave 1 as a contract-only slice; panel, allocation and fees land in wave 4. |

### RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11837 | RWB-P7-E1032-APP | GAP-0992 | 13 | Add C RWB-P3-E1042-CON and C RWB-P3-E1043-CON to the C list; fix the four intake shapes as the smallest superset of the legacy list, keep unnamed elements behind the placeholder, and declare the four consumed rows with their fakes. |

### RWB-P3-E1032-APP; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11838 | RWB-P7-E1032-APP | GAP-0742 | 13 | Add rwb_case.case_document_link with case_id, document_id, checklist_state, extracted_field_count, linked_at and source_event_id, unique key on (case_id, document_id), no cross-service foreign key; data steward to supply field IDs. |

### RWB-P5-E1032-APP; OTHER:TSD P5 v2; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11839 | RWB-P7-E1032-APP | GAP-0991 | 13 | Publish /resolve as the attach operation with right C and a 201 Document answer; declare rwb.document.DocumentAttached.v1 on rwb.document.events.v1; catalogue owner adds the name or confirms DocumentStored before wave 1. |

### OTHER:Environment files (owner: SCB IT infrastructure) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11840 | RWB-P7-E1032-APP | GAP-0993 |  | Record the agreed per-environment values: worker replica count, request and limit, KEDA ceiling, document_text growth and index budget, rwb-quarantine clearing age, hold container capacity, scan rate per hour. |

### RWB-P5-E1032-CON; OTHER:RWB-P6 contract (notice parameters, event payload, screen ID) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11841 | RWB-P7-E1032-APP | GAP-1197 |  | Publish the request and answer of POST /cases/{caseId}/generated-documents with the intake item created; name the document type and source for a notice letter copy; register notice parameter names; extend the NoticeGenerated.v1 catalogue row to its payload; allocate the notice screen ID. |

### RWB-P5-E1032-CON; OTHER:RWB-P6 contract; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11842 | RWB-P7-E1032-APP | GAP-1199 |  | State whether the hub creates an intake item from a generated document and which request fields it needs, so the handoff is specified once. |

### OTHER:Test case register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11843 | RWB-P7-E1032-APP | GAP-1201 | 16 | Record that attach proof of TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP and that the P6 copy proves the service side; note TC-E1-032-16 as the notice-read refusal. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-ITG-E1032-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11844 | RWB-P7-E1032-APP | GAP-1202 |  | Decide once whether rwb-document consumes rwb.comms.NoticeGenerated.v1 or is called by rwb-comms; align event catalogue row, P5 story and integration suite. |

### OTHER:TSD P7 v2 T3.1 decision_log_entry; OTHER:migration V1032_1 in rwb_decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11845 | RWB-P7-E1032-APP | GAP-2444 | 11 | Carry document reference, intake item and match method in actions; classifier version in model_version; confidence and type candidates in recommendation; message id in outcome; final_call ATTACHED; add columns by migration V1032_1. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:rwb-case reference-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11846 | RWB-P7-E1032-APP | GAP-2445 |  | Add LOV-DECISION with DOCATT as a value at the version in force; read it through the rwb-case reference-data contract; unknown code refused with MSG-P7-009. |

### OTHER:TSD P7 v2 T5.3 (DecisionRecorded schema); RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11847 | RWB-P7-E1032-APP | GAP-2447 |  | Define the DecisionRecorded fact keyed by caseId with decisionCode, caseId, documentId, intakeItemId, matchMethod, classifierVersion, confidence, approverUserId, finalCall, messageId and inputsRef; no OCR text, file or account number; refuse a fact without document reference. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11848 | RWB-P7-E1032-APP | GAP-3137 | Header | Partner frame header row removed |

### OTHER:S9 contract baseline (rwb-partner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11849 | RWB-P7-E1032-APP | GAP-3138 |  | Publish the partner file channel: submission row in rwb_partner, PartnerDocumentSubmitted fact, attach event consumed, and item read used to copy match state. |

### RWB-S9-E1032-CON; RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11850 | RWB-P7-E1032-APP | GAP-3141 | 3 | Publish POST and GET /partner/instructions/{instructionId}/documents, the document-hub intake creation, the rwb.partner.PartnerDocumentSubmitted.v1 payload, and the 404 and 409 bodies in RFC 9457 shape. |

### OTHER:RWB-S9 reference data set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11851 | RWB-P7-E1032-APP | GAP-3142 | 3 | Publish the intake bound parameter row, the acceptance decision code with its version, and LOV-DOC-TYPE alongside LOV-INSTR-STATUS. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11852 | RWB-P7-E1032-APP | GAP-3143 | 4 | Add partner_intake with its field IDs to the LDM and physical schema before the wave 1 entry check. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11854 | RWB-P7-E1032-APP | GAP-1198 | 3 | Add the seven platform contracts and the two P3 contracts to the dependency rows, or record in the platform release train that wave 1 services compile against them. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11856 | RWB-P7-E1032-APP | GAP-0746 | find it | Hold the case review task code, element type and task status values as reference data in the rwb-case reference tables, loaded before the review queue story starts. |

### OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11857 | RWB-P7-E1032-APP | GAP-0743 | find it | Use GET /api/recovery/source-data/v1/accounts/{id} with the ACE account number as the identifier; agree the query form with rwb-source-data before integration. |

### OTHER:platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11860 | RWB-P7-E1032-APP | GAP-0748 | find it | Name one login each for rwb-case and rwb-document in the platform DB story; login names Not specified in the source documents (GAP-0748) until agreed. |

### OTHER:FSD P7 rwb-partner; OTHER:S9 Screens table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11863 | RWB-P7-E1032-APP | GAP-3145 | header | Name the screen that carries the document submission of an instruction (PRT-02 Instruction is the candidate); this story keeps the service answer unchanged. |

### OTHER:Recovery Workbench P3 story set (screens SCR-38 and SCR-43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11869 | RWB-P7-E1039-APP | DOR-RWB-P7-E1039-APP-10 | none | Add empty, loading, error and no-access states to SCR-38 and SCR-43 in the P3 story; this story shows no screens. |

### RWB-P3-E1039-CON; RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11872 | RWB-P7-E1039-APP | GAP-0660 | 12 | Fix the ageing read, the reference-data read and the access-log operation in the P3 and P4 contract stories on the composed read paths; keep the composed read and export on the integration base as read-only. |

### OTHER:Platform deployment values files and platform secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11878 | RWB-P7-E1039-APP | GAP-0783 | 13 | Agree alert routes and thresholds with the security administrator and platform on-call, set the Kafka ACL set and retry cadence, and record secret names and topology values. |

### OTHER:P5 contract (TSD P5 v2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11884 | RWB-P7-E1039-APP | GAP-2341 |  | Add rule stating which P5 reads write an access entry, their decision codes and the owner of each entry. |

### OTHER:P3 rwb-case screen specification (SCR-33; OTHER:SCR-40) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11891 | RWB-P7-E1046-APP | DOR-RWB-P7-E1046-APP-10 | n/a | Add empty, loading, error and no-access states to SCR-33 and SCR-40. |

### RWB-P6-E1046-CON; OTHER:RWB-PLT-DB and TSD P5 Document hub v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11900 | RWB-P7-E1046-APP | GAP-2343 | find it | Name version identifier property in catalog answer; fix rwb-document login name; document template_id as soft reference with reconciliation check, not a foreign key. |

### OTHER:Work Package; RWB-P5-E2026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11904 | RWB-P7-E1046-APP | GAP-2344 | find it | Add the DP-07 rwb-case reference-data contract and the DP-15 and DP-19 platform contract stories to this slice's dependency rows. RWB-P5-E2026-CON to name the GenerateRequest and RegenerateRequest fields, the regenerate reason field, the refused-document error body, index ix_document_template and the Flyway step. |

### OTHER:Work Package (split plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11905 | RWB-P7-E1046-APP | GAP-2346 | find it | Record one owning story per legacy criterion and mark RWB-P5-E1046-APP as test-case-bearing but criterion-free for the nine legacy test cases. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0022 | TimerDue owner recorded as P3 and as PLT | Solution architect | Resolved (directive) |
| GAP-0064 | Wave conflict S8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0065 | Wave conflict S9 / EP01 | Tech lead | Resolved (directive) |
| GAP-0165 | The access log is named by Architecture v5 but is not itemised in the Ownership Map | ACE team | Resolved (directive) |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0345 | JOB-03 run surface and exact rerun facade are not specified for an ITG suite | Service owner of rwb-case with the service owner of rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0346 | Route-decided transfer trigger has no wave 1 owner event | Tech lead | Resolved (directive) |
| GAP-0352 | E1027 decision codes and reference data move to P3 while the writer and the ledger are PLT and P7 | Solution architect | Resolved (directive) |
| GAP-0353 | E1028 durable timers replace JOB-05 and the P1 account-date path leaves the slice | Solution architect | Resolved (directive) |
| GAP-0354 | Rebalancing trigger, measure delivery and rerun facade change in the target | Tech lead | Resolved (directive) |
| GAP-0356 | Intake trigger, attach operation and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0359 | Break-glass grant operation, central ledger fault point and SIT evidence are not named for the 19-service target | Tech lead | Resolved (directive) |
| GAP-0360 | Reference-load owner, field-ID check and template body storage move in the target | Solution architect | Resolved (directive) |
| GAP-0571 | The entry-candidate contract: the resource and parameter names, the response entity, its field names, the paging, the error status set and the access rule are not fixed by any source, and this legacy key has no contract story of its own | Tech lead of rwb-source-data with the solution architect and the P3 owner of the case contract | Resolved (directive) |
| GAP-0572 | Whether the entry read is one operation for a business date or one operation per account, and how a page of about 28,100 candidates is cut, are not specified | Tech lead of rwb-source-data with the owner of the rwb-case case creation job | Resolved (directive) |
| GAP-0573 | Which service writes account_ext.dispute_open and the party_ext flags, which right the confirmation needs, and where party_ext.vulnerable comes from on the first write are not settled | Solution architect with the P1 service owner, the P3 owner of the exclusion screen and the P4 owner of the role model | Resolved (directive) |
| GAP-0574 | The ALS batch gate before RWB-ACE-001 lands: v_ace_batch_status is a Section B view, and the behaviour of an entry read for a date whose batch record does not exist yet is not specified | Recovery tech lead with the ACE team lead and the platform team that owns the RWB-ACE-001 sequence | Resolved (directive) |
| GAP-0575 | The shape and the home of the REC-05 break list are not specified, and the table that held it leaves the schema | Data architect with the data steward and the P1 owner of the reconciliation job | Resolved (directive) |
| GAP-0576 | The product group of a candidate row: whether the ACE product_category value is passed through or mapped to the LOV-PRODUCT codes, and what happens to a value outside the list, is not specified | Business analyst, P1 with the center of excellence and the owner of the rwb-case reference data | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0675 | Per-service login name for rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0676 | Field-level OpenAPI schema of the case resource is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0677 | Deployment topology detail for rwb-case is not specified | DevOps engineer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0684 | The rwb-case service login name is not given in any source | ACE team, DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0687 | The deployment topology of the rwb-case allocation worker is not specified | Platform team; DevOps | Resolved (directive) |
| GAP-0688 | Per-service database login name for rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0691 | Deployment topology of the transfer capability is not specified | Platform team | Resolved (directive) |
| GAP-0742 | No case-side document link table or field IDs in the sources | RW-DATASTEW | Resolved (directive) |
| GAP-0743 | No named rwb-source-data operation for the ACE account number | RW-COE | Resolved (directive) |
| GAP-0744 | Cadence and time of the daily reconcile Schedule not specified | RW-COE | Resolved (directive) |
| GAP-0745 | The rwb-case feature switch key is not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0747 | Decision code and final call for the case document link are not specified | RW-COE | Resolved (directive) |
| GAP-0748 | Per-service login names for rwb-case and rwb-document are not specified | RW-SECADM | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0780 | Local decision-record table, legacy break-glass path and the composition of the entry actions are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0781 | The grant end and read paths, the 401 business message id and the full grant answer are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0782 | No source names the grant table, its two-person constraint, the retention period or the partition granularity of the access log | ACE database engineer | Resolved (directive) |
| GAP-0783 | Alert routes, thresholds, Kafka ACL set, retry cadence and secret names are not fixed by the sources | DevOps engineer | Resolved (directive) |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0986 | rwb-access timer and case read: the authorise request attribute set, the label of the matrix version in force and the scope that prevails under an escalation are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0987 | Authority attributes, matrix version label and role roster for an allocation and queue read | Solution architect of rwb-access | Resolved (directive) |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0991 | The attach operation, its right and the attach event name differ between the legacy story, the TSD and the Arch v5 event catalogue | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0992 | The intake-match contract baseline fixes shapes and paths the sources do not name at field level, and the plan's C list omits the two rwb-case reads | Tech lead | Resolved (directive) |
| GAP-0993 | The compute, storage, hold-container and scanning capacity values of the intake-match path are not specified | SCB IT infrastructure | Resolved (directive) |
| GAP-0994 | The Schedule window, the catch-up policy, the alert thresholds and the lag-alert identifier of the intake path are not specified | DevOps team | Resolved (directive) |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1024 | The generation contract baseline has no settled operation name, no published provider shapes and two consumed contracts outside the plan | Solution architect | Resolved (directive) |
| GAP-1036 | Producer-side AsyncAPI and JSON schema of rwb.document.events.v1 are not assigned to a contract story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1038 | The rwb-document login name, the not-found message ID of the case read and the case-read field names are not specified | Solution architect with the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1063 | The legacy template and catalog load path is replaced by the TSD admin template operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1064 | The data-dictionary read has no contract dependency in the plan | Solution architect | Resolved (directive) |
| GAP-1065 | No source says where the template body object lives | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1066 | The approver identity type of a template version is not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1067 | The request and answer field names of the five admin operations are not in T-A.2 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1068 | The service-side guard on the admin operations is not specified and DP-08 is not declared | Solution architect | Resolved (directive) |
| GAP-1197 | The request and answer shape of the letter-copy handoff, the document type and source the hub assigns, the notice parameters, the P1 recipient field IDs, the payload field names of the event and the notice screen identifier are all unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1199 | No source describes the letter copy becoming an intake item at the document hub, and FSD P6 keeps a generated document as a stored document on the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1200 | The P6 module declares no notice parameter, so DP-06 has no named value to read | Business analyst | Resolved (directive) |
| GAP-1201 | The legacy access case and the legacy attach cases have no subject in rwb-comms, so the carried test cases prove the notice read instead | Test lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1202 | The event catalogue names rwb-decision as the only consumer of NoticeGenerated, while the document hub is expected to turn the copy into an intake item | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1203 | The base documents of the story are in review, not approved | Business analyst | Resolved (directive) |
| GAP-1235 | The decision-record write operation is absent from the Ownership Map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1236 | The full record shape, the data-date column, the inputs digest and the message catalogue entry format are not specified | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1237 | The canonical form of the entry hash is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1238 | Two ce_type values are published for DecisionRecorded | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1239 | The decision-log stream to the data lake is retired but still specified | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1240 | JOB-13 is a 01:00 copy job in the specifications and a continuous ingest in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1323 | Gap cited in RWB P7 E1021 APP Transfer rules and engine v1 v1 | Tech lead | Resolved (directive) |
| GAP-1324 | Gap cited in RWB P7 E1028 APP Service levels, timers, escalation and prescription dates v1 | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1325 | Gap cited in RWB-P7-E1028-APP | Tech lead | Resolved (directive) |
| GAP-1326 | Gap cited in RWB P7 E1030 APP Daily rebalancing and queue measures v1 | Tech lead | Resolved (directive) |
| GAP-1336 | Shape of the model answer, of the inputs snapshot and of the announcement, with the carrier names of the plan-status move | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1402 | Local decision-record library: artefact coordinates, no-case publish path, chain scope and incident routing | Solution architect | Resolved (directive) |
| GAP-1403 | Local decision-record contract: record schema, table shape, shared-topic envelope and message catalogue | Solution architect | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1571 | The break-glass duration, the minimum reason length and the review window appear only inside acceptance criteria and are open in the decision log | SCB IT security with the security administrator | Resolved (directive) |
| GAP-1617 | The ledger completeness target, the gap alert threshold and the strict-mode wait bound have no value in the BRD or the FSD | Solution architect with the platform administrator | Resolved (directive) |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1652 | Queue depth and ageing are computed in P3 and published in P9 | Solution architect with P3 | Resolved (directive) |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-2016 | Timer row and durable timer kept in step by one activity | Service owner P3 rwb-case with the platform team | Resolved (directive) |
| GAP-2039 | The access log is named as an rwb_access object but has no row in the Ownership Map | P4 rwb-access with the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2068 | The local decision record has no table, no DDL and no case or trace column | Service owners of the 19 services with P7 rwb-decision | Resolved (directive) |
| GAP-2069 | The access log has an API and an owner but no table in the Ownership Map | Service owner P4 rwb-access | Resolved (directive) |
| GAP-2074 | One chain or 19 chains plus the ledger chain | Service owner P7 rwb-decision with the 19 service owners | Resolved (directive) |
| GAP-2075 | The record that governs while the central ledger lags by up to five minutes | Service owner P7 rwb-decision | Resolved (directive) |
| GAP-2076 | The versions in force in the access log come from two services | Service owners P4 rwb-access and P7 rwb-decision | Resolved (directive) |
| GAP-2150 | The worked example is a monolith story key with no service and no realignment equivalent | Document owner; analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2202 | The account-date and holiday reads and the deviation pause have no published surface in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2203 | No source gives the field-level detail of the two escalation columns or of the TimerBreached payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2204 | No source gives the operational values for a durable timer: poll window, catch-up window, breach band and record-failure rate | DevOps lead | Resolved (directive) |
| GAP-2205 | The measure feed, the alert delivery path and the run record have no target artifact once the data lake and the job monitor are removed | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2206 | The published run record and the rerun operation of the legacy contract have no target shape | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2207 | No source gives the operating values for the rebalance Schedule or the deployment | DevOps lead | Resolved (directive) |
| GAP-2210 | No source gives the case status history, the transfer from-queue or the decision-record read behind the timeline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2339 | How the active break-glass grant and its incident reach rwb-document on a document content read is not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2340 | The capability-area code, the result code and the field list of a document content read in an access entry are not specified | Data steward | Resolved (directive) |
| GAP-2341 | Which reads of the document hub other than the content read write an access entry in the target is not fixed | Solution architect | Resolved (directive) |
| GAP-2342 | The incident queue name and the session-answer reuse bound of the content read are not specified | DevOps team | Resolved (directive) |
| GAP-2343 | The catalog version answer read by rwb-document, its field names and the rwb-document login name are not specified, and the legacy document-to-template key becomes a soft cross-service reference | Solution architect, with the P5 TechX squad and the P6 rwb-comms squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2344 | The dependency rows of this slice name one contract only, and the request field names, the reason field, the index name and the migration step name are not specified | Solution architect, with the P5 TechX squad | Resolved (directive) |
| GAP-2345 | The rwb-comms catalog baseline declares no operation that answers the current Approved version for a template code, language and date | Tech lead of rwb-comms, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2346 | This slice owns no legacy acceptance criterion while the Work Package lists all nine legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2433 | The message text of MSG-P7-009 and of the chain warning MSG-P7-012 is named in the sources but never written | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2435 | TSD P7 still models decision_log_entry.case_id as a uuid with a relationship to recovery_case and gives the row no business-date column | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2436 | The literal rule ID of the ENTER rule of package ENTRY is named in no source | Business analyst, Epic 1 | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2438 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2439 | The physical columns of rule_package_version and the payload a compiled package is served in are not in the sources | TechX and the P7 solution architect | Resolved (directive) |
| GAP-2440 | The rule ID of the same allocation row is ALLOC-014 in the legacy story and ALLOC-MTG-BKK-01 in the FSD | P7 business analyst and the reference data administrator | Resolved (directive) |
| GAP-2441 | How the business date, the queue identifier and the owner identifier travel in the decision record is not in the sources | P7 and P3 contract owners | Resolved (directive) |
| GAP-2442 | The text of MSG-P7-009, the text of the chain-break warning and the field name of the per-entry chain result are not in the sources | P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2443 | No provided operation of the Ownership Map serves a compiled rule package version to the owning service | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2444 | DOCATT attach entry has no defined field set for the document reference, the intake item, the match method, the confidence, the final call and the message id | Solution architect, P7 | Resolved (directive) |
| GAP-2445 | The decision code list in force does not enumerate DOCATT in any source readable here | Reference data administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2446 | Whether an item held for a person leaves a decision record is not stated | Business analyst, P7 | Resolved (directive) |
| GAP-2447 | The DecisionRecorded payload of an attach has no defined field set | Solution architect, integration | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2449 | Login name, parameter names and message texts are not written in any source readable here | Tech lead, P7 | Resolved (directive) |
| GAP-2450 | The trigger of the ledger completeness check is not stated | Solution architect, P7 | Resolved (directive) |
| GAP-2452 | No source gives the ledger's access shape: the element names inside the actions payload beyond the legacy list, the grant, incident and review-due elements of the decision-log read, the use of the access code AC-VERS, and the catalogue entry format of MSG-P7-009 | Business analyst P7 | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2465 | The five-minute ledger completeness target has no named alert, owner or threshold | Platform observability owner with the P7 solution architect | Resolved (directive) |
| GAP-3072 | RWB-S8-E1020-APP: the allocation-to-deviation boundary, the handler roster, the assignment method and any handler cap have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3073 | RWB-S8-E1020-APP: the key has no contract story of its own, the event names are taken from the TSD, and the business wave is earlier than the service wave | Programme lead and solution architect | Resolved (directive) |
| GAP-3074 | The business epic places the story in wave 1 while the service sits in wave 2 | Programme planner with the S8 service owner | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3076 | No source publishes the operation names of the six rows this slice consumes | P1 rwb-source-data owner, P3 rwb-case owner, P4 rwb-access owner, P7 rwb-decision owner and the S8 service owner | Resolved (directive) |
| GAP-3077 | No source says which service hosts the TRANSFER package evaluation after the split | Solution architect with the S8 service owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-3079 | The event names of the P3 and P1 subscriptions are not published | P3 rwb-case owner, P1 rwb-source-data owner and the S8 service owner | Resolved (directive) |
| GAP-3080 | No source fixes where this slice records the rule ID and the package version of a transfer | S8 service owner with the data steward of module S8 and the P3 rwb-case owner | Resolved (directive) |
| GAP-3137 | The partner slice of RWB-E1-032 and its target service frame are not stated in any source | Solution architect | Resolved (directive) |
| GAP-3138 | The partner-origin channel of an intake item and its attach state are a boundary no source states | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3139 | Wave conflict: EP01 puts this story in wave 1 while rwb-partner is wave 4 in Arch v5 | Tech lead | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3141 | The two partner submission operations, the intake creation path and the PartnerDocumentSubmitted event are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3142 | The intake bound, the decision code and version, and the two lists in force are not named | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3143 | No data model carries a partner-side submission row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3144 | No source states how the legacy criteria split between the document-hub and partner slices | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3145 | The partner portal screen that submits a file is not fixed | Business analyst | Resolved (directive) |
| GAP-3162 | The case story writes the P1 extension tables | P3 case owner | Resolved (directive) |
| GAP-3166 | The Quartz note remains in the build notes although a Temporal Schedule replaces it | Platform lead | Resolved (directive) |
| GAP-3173 | Service S8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3174 | Service S9 takes Epic 1 stories in wave 1 although its Arch v5 wave is 4 | Delivery lead | Resolved (directive) |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3207 | No source names the rwb-case database login or where the caseload cap is stored | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3208 | The schedule expression of the DailyCaseRun (legacy JOB-03) is not stated by any source | Solution architect | Resolved (directive) |
| GAP-3209 | No single source divides the thirteen legacy criteria of RWB-E1-020 across its seven stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P7-E1020-APP | skipped AC ID | 111 | missing: AC9, AC10, AC11, AC12, AC13, AC14 |
| RWB-P7-E1021-APP | skipped AC ID | 115 | missing: AC8 |
| RWB-P7-E1028-APP | new AC without TC row | 429 | AC8 is new and no section 16 row covers it |
| RWB-P7-E1032-APP | skipped AC ID | 132 | missing: AC10, AC11, AC12, AC13 |
| RWB-P7-E1032-APP | unknown story key | 27 | RWB-P7-E1032-CON is not a story of the set: \| Contract published \| RWB-P7-E1032-CON, version Not specified in the source documents (DOR-RWB-P7-E1032-APP-23) \| |
