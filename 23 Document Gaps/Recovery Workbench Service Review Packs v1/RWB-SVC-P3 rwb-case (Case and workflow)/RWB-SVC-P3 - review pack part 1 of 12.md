# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 1 of 12 (RWB-P3-AD019-APP to RWB-P3-E1018-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 184 |
| Cross-document (pending in another document) | 248 |
| Not applied (value not in the sources) | 7 |
| Open business decisions | 20 |
| Register gaps linked | 149 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-AD019-APP | 28 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 AD019 APP Data quality and reconciliation console v2.md |
| RWB-P3-E1002-APP | 11 | 21 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1002 APP Case list v1 with case ID, owner and queue v2.md |
| RWB-P3-E1007-APP | 32 | 36 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1007 APP Integration adapters for outbound files v2.md |
| RWB-P3-E1011-APP | 30 | 50 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1011 APP Reconciliation and data quality report v2.md |
| RWB-P3-E1013-APP | 24 | 35 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1013 APP Baseline measures v2.md |
| RWB-P3-E1018-APP | 40 | 36 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1018 APP Case ID issuance and case record v1 v2.md |
| RWB-P3-E1018-CON | 19 | 44 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1018 CON Case ID issuance and case record v1 - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E1018-APP | R-00664 | CG-ALL-3426 | Script gap | Product owner | The story adds WAITING_COURT to the closed list LOV-CASE-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-AD019-APP | R-10173 | CG-ALL-3352 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1002-APP | R-10182 | CG-ALL-3374 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-P3-E1002-APP | R-10183 | CG-ALL-3375 | Script gap | Product owner | Open decision DL31 has no assumption | Owner rules DL31; until then build on the recommended option. |
| RWB-P3-E1018-APP | R-10204 | CG-ALL-3447 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1018-APP | R-10206 | CG-ALL-3456 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-ITG-E1002-ITG, RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1002-OPS, RWB-P3-E1002-APP | R-21871 | GAP-1502 | Register gap | Product owner | The case list is split between this service and the case service, while the FSD gives screen and rows to one module | This service builds and publishes one row per case account per business date and holds the publication status; rwb-case serves the case list screen and its filters over those rows; the reconciliation and the hold stay here. Agree the split at the Epic 1 story review. |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-21888 | GAP-1545 | Register gap | Compliance | The debt buyer tape is required to be masked before the data room, and to carry the personal data the sale terms allow | The tape carries only the fields the sale terms and the approved mask list allow, and the mask list is a reference-data row owned by Compliance under DL26; the PRD states the rule and leaves the field list open. |
| RWB-ITG-E1011-ITG, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21922 | GAP-1651 | Register gap | Data steward and data product owner | The reconciliation and the data quality break are P1's, but FSD P9 specifies them as its own features | Read the reconciliation result and the break rows from P1's contract and hold the break view and the closure in P9 |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E1007-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-P3-E1007-APP, RWB-P4-E1007-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP | R-28455 | GAP-1548 | Register gap | Compliance | No retention period is set for an outbound item, a delivery record or the transmission evidence of a file | The PRD states the retention of P2 transmission records as open under DL26 with the section R9 placeholder, and requires only that a resend and its audit record outlive the retention period of the case they belong to. |
| RWB-ITG-E1013-ITG, RWB-ITG-E2009-ITG, RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E2009-APP, RWB-P9-E1013-APP, RWB-P9-E1013-CON, RWB-P9-E1013-OPS, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-P9-E8001-APP, RWB-P9-E8001-CON, RWB-P9-E8002-APP, RWB-P9-E8002-CON, RWB-S8-E2009-APP | R-28480 | GAP-1644 | Register gap | Business lead | The program BRD has no requirement section for P9 reporting | Keep the epic-level keys as the trace target and state the coverage basis in section 11.2 until a P9 requirement section exists |
| RWB-P3-E1002-APP | R-33401 | ASM-ALL-3374 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-P3-E1002-APP | R-33402 | ASM-ALL-3375 | Script assumption |  | Built on the recommended option of DL31: A, using the ACE components. | Product owner rules DL31 |
| RWB-P3-E1018-APP | R-33404 | ASM-ALL-3456 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E1002-APP | R-00642 | CG-ALL-3369 | 1 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | Package segment for the service needs a Solution architect naming ruling; none in sources (Service Template v2, catalogs, TSD/FSD). No name invented. Evidence line 35. |
| RWB-P3-E1002-APP | R-00643 | CG-ALL-3370 | 12.8 | Java package th.co.scb.ace.workbench.recovery.case.caselist uses the reserved word 'case' | No ruled segment for ...recovery.case.caselist in sources; Solution architect naming ruling needed. No name invented. Evidence line 340. |
| RWB-P3-E1002-APP | R-04910 | DOR-RWB-P3-E1002-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or in folders 03, 04, 05 or the directive set. Sign-off cannot be confirmed without an invented record. |
| RWB-P3-E1002-APP | R-04911 | DOR-RWB-P3-E1002-APP-16 | section header | Definition of Ready item 16 Size: Fail | No size is given in the item or the story text, so DoR item 16 stays open. No number invented. |
| RWB-P3-E1007-APP | R-04916 | DOR-RWB-P3-E1007-APP-12 | 12.7, 16, 18 | Definition of Ready item 12 Test cases: Fail | Test rows have level and data, but boundary test (ASM-3438) and RTM v7 mismatch are not applied; sources not provided. |
| RWB-P3-E1007-APP | R-21891 | GAP-1161 | 13 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Fakes named for DP-07, DP-09, DP-10 and DP-19; DP-03 fake and its build-list row are not added, though a story edit was possible. |
| RWB-P3-E1018-APP | R-15785 | DOR-RWB-P3-E1018-APP-18 | 7 | Definition of Ready item 18 Open decisions: Partial | DL17 is answered in sources (decision log, answer A; BRD Epic 1). Adding its assumption needs a new ASM number, which only D1 may assign. Searched story, BRD and decision logs. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05187 | RWB-P3-AD019-APP | CG-ALL-3343 | 12.1 | Publish GET /api/recovery/case/v1/data-quality/reconciliation-breaks through the rwb-case CON story, or remove the operation from section 12.1. |
| CDC-05188 | RWB-P3-AD019-APP | CG-ALL-3344 | 12.1 | Publish GET /api/recovery/case/v1/data-quality/referential-completeness through the rwb-case CON story, or remove the operation from section 12.1. |
| CDC-05189 | RWB-P3-AD019-APP | CG-ALL-3345 | 12.1 | Publish GET /api/recovery/case/v1/data-quality/stale-products through the rwb-case CON story, or remove the operation from section 12.1. |
| CDC-05262 | RWB-P3-E1011-APP | CG-ALL-3395 | 12.1 | Publish GET /api/recovery/case/v1/quality-runs/{businessDate} in rwb-case.yaml through the CON story |
| CDC-05263 | RWB-P3-E1011-APP | CG-ALL-3396 | 12.1 | Publish GET /api/recovery/case/v1/quality-results in rwb-case.yaml through the CON story |
| CDC-05264 | RWB-P3-E1011-APP | CG-ALL-3397 | 12.1 | Publish GET /api/recovery/case/v1/reconciliation-facts/{businessDate} in rwb-case.yaml through the CON story |
| CDC-05265 | RWB-P3-E1011-APP | CG-ALL-3398 | 12.1 | Publish GET /api/recovery/case/v1/reconciliation-facts/keys in rwb-case.yaml through the CON story |
| CDC-05266 | RWB-P3-E1011-APP | CG-ALL-3399 | 1 | Remove the fixed reasonCode enum so LOV-EXCLUSION-REASON values are accepted as data, as Reference Data v5 Lists defines them |
| CDC-05273 | RWB-P3-E1011-APP | DOR-RWB-P3-E1011-APP-8 | 9, 10 | Add GET /quality-runs/{businessDate}, GET /quality-results, GET /reconciliation-facts/{businessDate}, GET /reconciliation-facts/keys and the six further paths listed by detcheck. |
| CDC-05297 | RWB-P3-E1011-APP | GAP-2234 | 12.1 | Publish the four operations of 12.1 with Platform administration R, Reporting R and Platform administration U, the 400, 401, 403, 404, 409 and 503 problem set, and an Idempotency-Key on the rerun. |
| CDC-05299 | RWB-P3-E1011-APP | GAP-2236 | 4 | Add GET /reconciliation/status returning RELEASED, HELD or NOT_RUN for the business date with the unexplained exclusion count per product group; the rwb-source-data case-list gate reads it. |
| CDC-05312 | RWB-P3-E1013-APP | CG-ALL-3415 | 12.1 | Publish GET /api/recovery/case/v1/cases/facts in rwb-case.yaml through the CON story, or remove it from section 12.1. |
| CDC-05313 | RWB-P3-E1013-APP | CG-ALL-3416 | 12.1 | Publish GET /api/recovery/case/v1/admin/lists/{listCode} in rwb-case.yaml through the CON story, or remove it from section 12.1. |
| CDC-05317 | RWB-P3-E1013-APP | DOR-RWB-P3-E1013-APP-8 | 12.1 | Publish both GET /api/recovery/case/v1/cases/facts and GET /api/recovery/case/v1/admin/lists/{listCode} in rwb-case.yaml. |
| CDC-05353 | RWB-P3-E1018-APP | CG-ALL-3436 | 9 | Remove the fixed status enum so LOV-CASE-STATUS values are accepted as data, as section 9 states. |
| CDC-05368 | RWB-P3-E1018-APP | GAP-0676 | 12.1 | Add the field-level schema of the case resource agreed in the baseline review of RWB-P3-E1018-CON: required flags, GET /cases page and sort parameters, caseNo pattern and error codes per operation. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05195 | RWB-P3-AD019-APP | CG-ALL-3347 | 12.1 | Add message IDs for 401 no session and for 503 rwb-source-data down on a read-only screen; RWB-P3-AD019-APP §12.1 then cites them. |
| CDC-05212 | RWB-P3-E1002-APP | CG-ALL-3364 | 4, 14 | Business analyst adds a new message ID for 'No valid session'; the story cites it once it exists. |
| CDC-05213 | RWB-P3-E1002-APP | CG-ALL-3365 | section 4, 14 | The item reports a different meaning in the standard. The story keeps the ID until a new one exists; its text now follows the v4 template under DOR-RWB-P3-E1002-APP-9. |
| CDC-05214 | RWB-P3-E1002-APP | CG-ALL-3366 | section 4, 14 | The item reports a different meaning in the standard. The story keeps the ID until a new one exists; its text now follows the v4 template under DOR-RWB-P3-E1002-APP-9. |
| CDC-05215 | RWB-P3-E1002-APP | CG-ALL-3367 | 4, 14 | Business analyst adds a new message ID for 'source-data contract does not answer'; the story cites it once it exists. |
| CDC-05218 | RWB-P3-E1002-APP | DOR-RWB-P3-E1002-APP-9 | section 14 | GEN-002 and GEN-007 texts taken from Standard v4; GEN-006 text left as not specified. |
| CDC-05234 | RWB-P3-E1007-APP | CG-ALL-3383 | 14 | The standard text is not in the source documents; no story alignment is possible here (see R-15766). |
| CDC-05235 | RWB-P3-E1007-APP | DOR-RWB-P3-E1007-APP-9 | 14 | State the v4 text of MSG-P2-001 and align it with the MSG-P2-001 row of section 14 of RWB-P3-E1007-APP, which reads the item text as written until then. |
| CDC-05342 | RWB-P3-E1013-APP | GAP-0565 |  | Set MSG-P1-001 to '{product} is from {date}. Today's ACE batch has not arrived.' as in FSD P1 VR-P1-001-1 and TSD P1 T3.7 |
| CDC-05369 | RWB-P3-E1018-APP | GAP-2433 | 14 | Write MSG-P7-009 (naming the field and case reference) and MSG-P7-012 (chain position warning) in the message catalogue and add both rows to the rwb-decision API specification. |
| CDC-05394 | RWB-P3-E1018-CON | CG-ALL-3466 | 4, 14 | Add a new message ID for 'A request body or query fails schema validation' (text: The request could not be read: {detail}.) for the story to cite in place of MSG-P3-030. |
| CDC-05395 | RWB-P3-E1018-CON | CG-ALL-3467 | 4, 14 | Add a new message ID for 'A required header is missing on a POST' (text: The request is missing {header}.) for the story to cite in place of MSG-P3-031. |
| CDC-05396 | RWB-P3-E1018-CON | CG-ALL-3468 | 4, 14 | Add a new message ID for 'An Idempotency-Key is replayed with a different body' (text: This request was already sent with different content.) for the story to cite in place of MSG-P3-032. |
| CDC-05397 | RWB-P3-E1018-CON | CG-ALL-3469 | 4, 14 | Add a new message ID for 'An unsupported major version is requested' with text 'This version of the service is not available.'; then §14 cites it in place of MSG-P3-033. |
| CDC-05417 | RWB-P3-E1018-CON | CG-ALL-3470 | 14 | MSG-P1-001 text copied from the standard; the When column is left for the business analyst. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05191 | RWB-P3-AD019-APP | CG-ALL-3353 | 13 | Solution architect rules a P3 package segment that is not a Java reserved word, replacing th.co.scb.ace.workbench.recovery.case; RWB-P3-AD019-APP §13 then copies it. |
| CDC-05192 | RWB-P3-AD019-APP | CG-ALL-3354 | 13 | With the ruled P3 segment, replace th.co.scb.ace.workbench.recovery.case.dataquality; RWB-P3-AD019-APP §13 then copies it. |
| CDC-05226 | RWB-P3-E1007-APP | CG-ALL-3387 | 1, 13 | P3 row (line 371): replace the reserved-word segment `case` in the Java package th.co.scb.ace.workbench.recovery.case with the non-reserved segment the Service Template Specification v1 naming rule fixes for rwb-case; RWB-P3-E1007-APP then copies it in sections 1 and 13. |
| CDC-05227 | RWB-P3-E1007-APP | CG-ALL-3388 | 13 | Same P3 row (line 371): the base segment ruled there is the one the module package th.co.scb.ace.workbench.recovery.case.fileoutcome inherits; once ruled, the story copies the corrected sub-package in section 13. |
| CDC-05268 | RWB-P3-E1011-APP | CG-ALL-3409 | 13 | Rule the package segment that replaces the Java reserved word `case` for rwb-case and update the P3 package in the row; the story copies the ruled package. |
| CDC-05269 | RWB-P3-E1011-APP | CG-ALL-3410 | 13 | The ruled segment applies to the module package th.co.scb.ace.workbench.recovery.case.quality as well; update the P3 package in the row and the story copies it. |
| CDC-05354 | RWB-P3-E1018-APP | CG-ALL-3448 | 13 | Rule the Java package segment for rwb-case in place of the reserved word 'case' and publish it in the rwb-case row (L371, now th.co.scb.ace.workbench.recovery.case); 13 copies the ruled package. |
| CDC-05355 | RWB-P3-E1018-APP | CG-ALL-3449 | 13 | Rule the module Java package for casecreation under the ruled service segment (row L371 names only the base package ...recovery.case); 13 copies the ruled package. |
| CDC-05389 | RWB-P3-E1018-CON | CG-ALL-3474 | 2 | Rule the last Java package segment for rwb-case, because `case` is a Java reserved word, and publish it; the story then copies the ruled segment in place of th.co.scb.ace.workbench.recovery.case. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05216 | RWB-P3-E1002-APP | DOR-RWB-P3-E1002-APP-12 | 12.7, 16, 18 | Align the test lists for this story with section 18, which still differs from RTM v7. |
| CDC-05224 | RWB-P3-E1002-APP | CG-ALL-3368 | 18 | Align the REQ-RDF-007 and REQ-RDF-009 test lists with section 18 (TC-E1-002-01, -02, -10; -03, -05) and the third listed requirement in the RTM's next version. |
| CDC-05253 | RWB-P3-E1007-APP | CG-ALL-3386 | 18 | Align REQ-DRI-006, REQ-DRI-007 and the third requirement's test list with section 18 of this story in the next RTM version. |
| CDC-05282 | RWB-P3-E1011-APP | DOR-RWB-P3-E1011-APP-12 | 16 | Align the test case lists of the REQ rows with section 16 and section 18 of RWB-P3-E1011-APP, including TC-E1-011-10 to TC-E1-011-13. |
| CDC-05302 | RWB-P3-E1011-APP | CG-ALL-3408 | 18 | Align the test lists of REQ-RDF-007, REQ-RDF-008 and the third differing requirement between §18 and RTM v7 in their next versions. |
| CDC-05336 | RWB-P3-E1013-APP | CG-ALL-3418 | 18 | Trace REQ-RDF-012 to TC-E1-013-01 to TC-E1-013-12 as RWB-P3-E1013-APP section 18 does; remove TC-E1-030-01, TC-E1-030-02 and TC-E1-030-09 from that row. |
| CDC-05373 | RWB-P3-E1018-APP | CG-ALL-3446 | 18 | Align the test lists for the six requirements with section 18 of RWB-P3-E1018-APP in the next RTM version. |
| CDC-05419 | RWB-P3-E1018-CON | CG-ALL-3473 | 18 | Align the test lists of the seven requirements with section 18 of RWB-P3-E1018-CON in the next RTM version. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05298 | RWB-P3-E1011-APP | GAP-2235 | 4 | Publish the freshness read and one product-coded records read per data product with business date, paging and element names; expose plan rows keyed by plan_ref for REC-03. |
| CDC-05348 | RWB-P3-E1018-APP | CG-ALL-3429 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the provider's CON story. |
| CDC-05349 | RWB-P3-E1018-APP | CG-ALL-3430 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} through the provider's CON story. |
| CDC-05350 | RWB-P3-E1018-APP | CG-ALL-3431 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness through the provider's CON story. |
| CDC-05363 | RWB-P3-E1018-APP | GAP-0571 | 12.2 | Publish GET /api/recovery/source-data/v1/entry-candidates with businessDate and threshold as required query parameters, page and size optional, response EntryCandidatePage, and statuses 400, 401, 403, 409, 422 and 503, through the provider's CON story. |
| CDC-05383 | RWB-P3-E1018-CON | CG-ALL-3457 | 12.2 | Publish GET /api/recovery/source-data/v1/accounts/{id} through the provider's CON story, or consume a published operation. |
| CDC-05384 | RWB-P3-E1018-CON | CG-ALL-3458 | 12.2 | Publish GET /api/recovery/source-data/v1/customers/{id} through the provider's CON story, or consume a published operation. |
| CDC-05385 | RWB-P3-E1018-CON | CG-ALL-3459 | 12.2 | Publish GET /api/recovery/source-data/v1/freshness through the provider's CON story, or consume a published operation. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05196 | RWB-P3-AD019-APP | CG-ALL-3349 | 12.5 | Add activity refreshStaleSet: type Activity, task queue rwb-case, one freshness read per data product with 2 s budget and one GET retry, returns stale rows, writes no table. |
| CDC-05205 | RWB-P3-E1002-APP | CG-ALL-3360 | 12.5 | Add rwb-case workflow CaseListDayOpen with activities readFreshness and raiseStaleListAlert, started by Schedule rwb-case-caselist-daily, as story 12.5 and 12.6 describe. |
| CDC-05208 | RWB-P3-E1002-APP | DOR-RWB-P3-E1002-APP-8 | 12.5 | Add workflow CaseListDayOpen and activities readFreshness and raiseStaleListAlert for rwb-case, queue rwb-case, as in story 12.5. |
| CDC-05277 | RWB-P3-E1011-APP | CG-ALL-3401 | 12.5 | Add activity loadTolerance to the Activities sheet. |
| CDC-05278 | RWB-P3-E1011-APP | CG-ALL-3402 | 12.5 | Add activity readAceFacts to the Activities sheet. |
| CDC-05279 | RWB-P3-E1011-APP | CG-ALL-3403 | 12.5 | Add activity reconcileCaseFacts to the Activities sheet. |
| CDC-05280 | RWB-P3-E1011-APP | CG-ALL-3404 | 12.5 | Add activity writeQualityFacts to the Activities sheet: type Activity, task queue rwb-case, as named in section 12.5 of RWB-P3-E1011-APP. |

### RWB-P2-E1007-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05229 | RWB-P3-E1007-APP | DOR-RWB-P3-E1007-APP-21 | Header | Contract publication is outside this story; the header already cites RWB-P2-E1007-CON. |
| CDC-05238 | RWB-P3-E1007-APP | GAP-0334 | n/a | Fix deliverFile manifest schema, claim-check handoff, SAS lifetime and the two window trigger calls before the first SIT run. |
| CDC-05240 | RWB-P3-E1007-APP | GAP-0647 | n/a | Build outbound-file capability in rwb-integration; read ACE facts via rwb-source-data; supersede TSD P2 v3 direct-view wording; retire INT-19, INT-20, JOB-13, JOB-15. |
| CDC-05241 | RWB-P3-E1007-APP | GAP-0648 | n/a | Fix deliverFile manifest and return, notice-fact read, RFC 9457 problem body, OpenAPI JSON names and event subject and compatibility level. |
| CDC-05243 | RWB-P3-E1007-APP | GAP-0739 | n/a | Fix FileDelivered and FileFailed element names and the admin item in the P2 contract; keep the seam as the ruling states. |
| CDC-05248 | RWB-P3-E1007-APP | GAP-2229 | n/a | Confirm the element names of rwb.integration.FileFailed.v1 and FileDelivered.v1, the resume-state carrier and the task code and due date rule; rename here at contract review without changing a value. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20565 | RWB-P3-E1007-APP | R-09172 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20566 | RWB-P3-E1007-APP | R-09174 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20569 | RWB-P3-E1007-APP | R-09173 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20570 | RWB-P3-E1007-APP | R-28453 |  | write failed: WRITE FAILED (nothing was written): X002-F1: old text found 0 time(s), expected 1: 'An outbound file reads ACE through the `recovery.v_ace_*` views on |
| CDC-20818 | RWB-P3-E1007-APP | R-28452 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09174', 'R-21873', 'R-28451', 'R-28452', 'R-28453'] |
| CDC-20819 | RWB-P3-E1007-APP | R-28451 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-09174', 'R-21873', 'R-28451', 'R-28452', 'R-28453'] |

### RWB-P9-E1013-APP (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05321 | RWB-P3-E1013-APP | GAP-0255 | 12.7 | Add a Read-model controls section naming measure_definition, measure_snapshot and measure_publish under P9 with the publish gate, and stating that queue_measure stays with P3 rwb_case (RWB-P3-E1030-APP). |
| CDC-05323 | RWB-P3-E1013-APP | GAP-1649 | 7 | Publish the six baseline measures plus CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE and AGENT_OVERRIDE, and carry the measure count as an open question. |
| CDC-05328 | RWB-P3-E1013-APP | GAP-0558 | 7, 16 | Read legacy AC3 and AC7 as superseded by DP-17: the publish, the hold and the alert move to the P9 publication and its ReportPublished event, rwb-source-data supplies the gate and the freshness the publication reads, and the lake extract, the trailer, the Power BI data set and the resend are recorded as removed with no replacement in wave 1. |
| CDC-05333 | RWB-P3-E1013-APP | GAP-2566 | 7, 16 | Keep legacy AC3 and AC7 word for word, prove the publish, the freshness stamp, the hold and the resend on measure_publish inside rwb_reporting, declare no lake path and no extract element in the contract, and let a later decision register decide whether a reporting extract to any destination is rebuilt. |
| CDC-05346 | RWB-P3-E1013-APP | GAP-2575 |  | Carry measure_definition, measure_snapshot, measure_publish and the frozen-row trigger in V1013__measures.sql in the per-service sequence; deployment story replays it |

### RWB-P9-E1013-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05324 | RWB-P3-E1013-APP | GAP-2570 | 12.2 | Declare the measures read in the wave 1 contract for the harness and the catalog consumer, keep the dashboard and its data set in RWB-P9-E2009-APP, and leave the connection of any reporting client to the read as an open decision for the PRD step. |
| CDC-05332 | RWB-P3-E1013-APP | GAP-2240 | 12.2 | Publish the measure-catalog read as GET on the rwb-reporting base with an onDate parameter, and name it in the Service Contract Catalog. |
| CDC-05334 | RWB-P3-E1013-APP | GAP-2572 | 12.2 | Declare GET /measure-definitions with query parameter onDate and a definition list answer as a target declaration pending P3 confirmation. |
| CDC-05335 | RWB-P3-E1013-APP | GAP-2568 | 12.2 | Declare the reference-load element of table measure_definition on the rwb-reporting base; keep list values on the rwb-case reference-data contract; rwb-case owner to confirm the load owner. |
| CDC-05344 | RWB-P3-E1013-APP | GAP-2571 |  | Declare measure_definition.approved_by as uuid and approved_at as timestamptz; carry TRB-0001 as element comment and test fixture |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05371 | RWB-P3-E1018-APP | GAP-2434 | 4 | Add finalCall to the query parameters of API-P7-006 and fix the creation-filter answer as a page of entries with the thirteen fields named by RWB-P3-E1018-APP. |
| CDC-05406 | RWB-P3-E1018-CON | GAP-2433 | 14 | Author MSG-P7-009 as one sentence naming the field and the case reference and MSG-P7-012 as one warning naming the chain position, and map both rows in the rwb-case API error responses |
| CDC-05410 | RWB-P3-E1018-CON | GAP-2434 | find it | Add finalCall to the query parameters of API-P7-006 and fix the creation-filter answer as a page of entries with an agreed field set shared with RWB-P7-E2005-APP. |
| CDC-05421 | RWB-P3-E1018-CON | GAP-0982 | none | Add the case-authority request and answer schema for POST /api/recovery/access/v1/authorise; record where caller teams and regions are held in TSD P4 T3.1; list case-record personal field IDs with version. |
| CDC-05425 | RWB-P3-E1018-CON | GAP-1038 | 11 | Publish the GET /cases/{caseId} request and response field names and the not-found message ID in the rwb-case API specification; name the rwb_document login with its grants and pool size in the DB story under DP-02 |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05193 | RWB-P3-AD019-APP | DOR-RWB-P3-AD019-APP-14 | header | Record the signed epic design sign-off so Definition of Ready item 14 passes. |
| CDC-05228 | RWB-P3-E1007-APP | DOR-RWB-P3-E1007-APP-14 | header | Record the signed epic design sign-off for RWB-P3-E1007-APP and confirm it against this story. |
| CDC-05270 | RWB-P3-E1011-APP | DOR-RWB-P3-E1011-APP-14 |  | Record the signed epic design of RWB-SVC-P3, the epic of RWB-P3-E1011-APP, so Definition of Ready item 14 passes. |
| CDC-05390 | RWB-P3-E1018-CON | DOR-RWB-P3-E1018-CON-14 |  | Record the signed epic design sign-off for RWB-SVC-P3 that DoR item 14 asks for. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05206 | RWB-P3-E1002-APP | DOR-RWB-P3-E1002-APP-21 | 14 | Record contract story RWB-P3-E1002-CON for rwb-case, or confirm none exists, so the story's Contract dependencies row can be set. Not found in the catalog today. |
| CDC-05207 | RWB-P3-E1002-APP | DOR-RWB-P3-E1002-APP-22 | 14 | Record the published contract fake library version for the rwb-case contract, or state that none is published. |
| CDC-05236 | RWB-P3-E1007-APP | GAP-0673 | none | Mark FSD P2 Integration v3 A1.5 and the TSD P2 Integration v3 T1 and T5.1 line on INT-03 superseded for legacy key RWB-E4-046, with date and decision; load the ALS interface as one versioned interface_config row per environment, agreed with the interface owner. |
| CDC-05331 | RWB-P3-E1013-APP | GAP-2239 | 12.1 | Publish GET /api/recovery/case/v1/cases/facts with businessDate, page and size, and confirm the path and fields at the next revision. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05221 | RWB-P3-E1002-APP | GAP-0335 | find it | Agree the rwb-integration deliverFile manifest and the FileDelivered and FileFailed events for the reporting leg at wave-1 review; this story keeps the read on GET /api/recovery/case/v1/cases and names no file path. |
| CDC-05239 | RWB-P3-E1007-APP | GAP-0338 | n/a | Add the P2 Integration read path to rwb-source-data and the FileFailed edge into rwb-case to the connection matrix. |
| CDC-05251 | RWB-P3-E1007-APP | GAP-1396 | n/a | Fix Airflow product, tenancy, service principal, timeouts, retries, DailyCaseRun wait mechanism and file-window operations at the scheduling design review. |
| CDC-05376 | RWB-P3-E1018-APP | GAP-0982 |  | Add the request and answer schema of POST /api/recovery/access/v1/authorise, record where caller teams and regions are held in TSD P4 T3.1, and list case-record personal field IDs with version for the masking pack. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05249 | RWB-P3-E1007-APP | GAP-3160 | n/a | Remove debt_sale_account from the P2 adapter write list; S6 rwb_debtsale owns it, reached by a contract call or an event from P2. |
| CDC-05256 | RWB-P3-E1007-APP | GAP-1538 | find it | Add rows for FileDelivered and FileFailed: producer rwb-integration, topic rwb.integration.events.v1, consumer requesting service, keyed by case ID; no numbered EV ID. |
| CDC-05305 | RWB-P3-E1011-APP | GAP-0274 | find it | The S1 row keeps rwb-valuation as owner, states the capability Arch v5 gives it (valuations, D6 route decision, route agent output) and carries the Template and Rules R9 placeholder until a table is listed. |
| CDC-05412 | RWB-P3-E1018-CON | GAP-1085 | 12.1 | Record the rwb-case task-raise operation (caseId, taskCode, ownerRole, reasonCode) in the Ownership Map next to GET /me/tasks and PATCH /tasks/{taskId} and publish it in the service API file |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05274 | RWB-P3-E1011-APP | CG-ALL-3392 | 7, 11, 12.7, 13 | Record case_quality_run as a service-owned rwb_case table with no field ID, as GAP-0740 and ASM-1351 state, or add it as a dictionary name. |
| CDC-05275 | RWB-P3-E1011-APP | CG-ALL-3393 | 7, 11, 12.7, 13 | Record case_quality_result as a service-owned rwb_case table with no field ID, as GAP-0740 and ASM-1351 state, or add it as a dictionary name. |
| CDC-05276 | RWB-P3-E1011-APP | CG-ALL-3394 | 7, 11, 12.7, 13 | Record case_quality_break as a service-owned rwb_case table with no field ID, as GAP-0740 and ASM-1351 state, or add it as a dictionary name. |
| CDC-05283 | RWB-P3-E1011-APP | DOR-RWB-P3-E1011-APP-7 | 11 | Add case_quality_run, case_quality_result and case_quality_break as rwb_case tables owned by rwb-case, per section 12.7 of RWB-P3-E1011-APP. |

### RWB-P6-E1011-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05288 | RWB-P3-E1011-APP | GAP-1168 |  | Add RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-source-data data-product contract to its C list. |
| CDC-05294 | RWB-P3-E1011-APP | GAP-1170 | 1 | Drop the two extracts and the INT-19 path; serve the quality facts from GET /api/recovery/comms/v1/quality-results; settle with rwb-reporting how its report reads them; record the decision in the Change Register against RWB-E1-014 and INT-19. |
| CDC-05295 | RWB-P3-E1011-APP | GAP-1171 | 1 | Hand the quality facts over through the P6 read model for wave 1; settle in wave 2 whether rwb-reporting reads them or a quality event is added with DP-09 and a platform event library story. |
| CDC-05308 | RWB-P3-E1011-APP | GAP-1172 | find it | Carry comms_quality_run, comms_quality_result and comms_quality_break, REC-09 with checks ACK and POD, one Schedule after the pod read, and GET /quality-runs/{businessDate} and GET /quality-results into the API Specification, schema folder and batch design at the next version. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05281 | RWB-P3-E1011-APP | CG-ALL-3407 | 16 | Add rows TC-E1-011-08 and TC-E1-011-09 with Given, When and Then copied from AC7, AC9 and AC4 of section 7. |
| CDC-05361 | RWB-P3-E1018-APP | CG-ALL-3444 | 16 | Add story test cases TC-E1-018-15 and TC-E1-018-16 to tab Story test cases, with Given, When and Then from AC13 and AC15. |
| CDC-05418 | RWB-P3-E1018-CON | CG-ALL-3472 | 16 | Add rows for TC-P3-E1018-CON-01 to TC-P3-E1018-CON-06 with Given, When and Then copied from the criteria they cover. |

### RWB-P3-E1018-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05358 | RWB-P3-E1018-APP | DOR-RWB-P3-E1018-APP-21 | 3 | Record Build status Done for RWB-P3-E1018-CON when the case contract is published. |
| CDC-05378 | RWB-P3-E1018-APP | GAP-0572 |  | Publish one business-date entry operation, paged by page and size, with default and maximum page size fixed in the contract; refuse per-account reads under DP-11. |
| CDC-05380 | RWB-P3-E1018-APP | GAP-1038 |  | Publish GET /cases/{caseId} request and response field names and the not-found message ID; name the rwb_document login and grants under DP-02. |

### RWB-P1-E1018-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05366 | RWB-P3-E1018-APP | GAP-0573 | 3 | P1 writes account_ext and party_ext as two PUT operations by business key called by the exclusion screen through gateway-bff; the body carries all four party flags so vulnerable is always written by the caller, a repeat leaves one row and a changed body replaces the flags on the same key with a version increment; P1 validates the caller token and enforces no role model (ASM-B-P1-07-E1018-3). |
| CDC-05367 | RWB-P3-E1018-APP | GAP-0576 | 11 | Return product_group as the v_ace_account.product_category value read, unvalidated and unmapped; a value outside LOV-PRODUCT is returned as read and never coerced, dropped or defaulted; any mapping or label is the consumer's through the rwb-case reference-data contract (ASM-B-P1-07-E1018-6). |
| CDC-05409 | RWB-P3-E1018-CON | GAP-3162 | 12.7 | Write the party_ext and account_ext rows through the two PUT operations by business key in P1's own transaction; rwb-case keeps only recovery_case, case_account, case_party and case_entry_exclusion |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05204 | RWB-P3-AD019-APP | GAP-3232 | - | Use the 2,534 catalog rows as the source of the v5 graph and state the template baseline once on Dependency classes; story files keep their rows and no story is re-cut. |
| CDC-05382 | RWB-P3-E1018-APP | GAP-3209 |  | Add a criterion-ownership column listing the single new story that owns each of the thirteen RWB-E1-020 criteria, and the test case split. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05210 | RWB-P3-E1002-APP | CG-ALL-3361 | 12.5 | Add the activity readFreshness to the Activities sheet, or name a catalogued activity. |
| CDC-05211 | RWB-P3-E1002-APP | CG-ALL-3362 | 12.5 | Add the activity raiseStaleListAlert to the Activities sheet, or name a catalogued activity. |

### OTHER:FSD P2 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05231 | RWB-P3-E1007-APP | GAP-1535 | none | Outbound file ACE reads go through the rwb-source-data contract (one hop, 2 s budget). No grant of rwb_integration on the recovery schema. Restate A1.5 and AC-ALT-P2-001-03 accordingly. |
| CDC-05232 | RWB-P3-E1007-APP | GAP-1539 | none | Tape rows and account keys travel in the delivery request manifest raised by rwb-debtsale; account facts come through the rwb-source-data contract. P2 reads neither debt_sale_account nor v_ace_account. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05233 | RWB-P3-E1007-APP | CG-ALL-3381 | change log; DP-02 row | Record recovery_svc as the rwb-case service login name (DP-02) or the dictionary name is used. The change log text cannot be edited here. |
| CDC-05322 | RWB-P3-E1013-APP | GAP-0257 | 11 | State that the read model keys owner and team by ID from the events and resolves the display name from the P3 queue_member and assignment rows behind the rwb-access masking policy; no personal data travels on an event. |

### RWB-P3-E1011-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05271 | RWB-P3-E1011-APP | DOR-RWB-P3-E1011-APP-21 | Header | The header Contract dependencies row names the rwb-case contract v1 and the contract story that publishes it and its fake library version; the story key is not restated as a dependency entry (DOR-RWB-P3-E1011-APP-21). |
| CDC-05272 | RWB-P3-E1011-APP | DOR-RWB-P3-E1011-APP-22 | Header | Contract dependencies row names the rwb-case contract story for the contract and its fake library version |

### RWB-P1-E1011-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05291 | RWB-P3-E1011-APP | GAP-0496 | 18 | Keep REC-01, REC-02 and REC-05 over P1's own tables; remove REC-03, REC-04 and other services' REC-05 keys; read AC5 and AC6 as five checks over three product groups; keep the twelve legacy table names as history. |
| CDC-05296 | RWB-P3-E1011-APP | GAP-1508 | 11 | Publish the enterprise break list inside the reconciliation result and its read operation, and fix its store at the data-model review before system test. |

### OTHER:Reconciliations v3 workbook (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05303 | RWB-P3-E1011-APP | GAP-0271 | find it | Add a Per-service reconciliation sheet with one row per service (19 services) giving its tables, check part, key, tolerance, cadence, break and result route, pattern and basis; cells the source does not state carry the Template and Rules R9 placeholder. |
| CDC-05304 | RWB-P3-E1011-APP | GAP-0272 | find it | Add rows for the ten services P2, P4, P5, P10, S1, S3, S4, S6, S8 and S9; the tolerance cell of each carries the Template and Rules R9 placeholder. No value is set here. |

### RWB-P1-E1013-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05330 | RWB-P3-E1013-APP | GAP-1503 | 4, 12.6 | Restate A2.19 as serving the measure snapshot for a business date whose ACE batches are complete; rwb-reporting publishes the baseline and freezes it, and the frozen baseline is not written back to rwb-source-data; align AC-P1-019-01, AC-ALT-P1-019-01 to -02 and AC-EXC-P1-019-02. |
| CDC-05340 | RWB-P3-E1013-APP | GAP-0562 | find it | Read the P1 slice as facts and gate only (listEligibleAccounts, snapshot(page), payments since entry, freshness stamp, reconciliation); assert no measure figure there; leave measure figures to RWB-P9-E1013-APP and RWB-ITG-E1013-ITG. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05347 | RWB-P3-E1018-APP | CG-ALL-3428 | 13 | Record case.entry.dpd as the single parameter key; align case.entry.dpd_threshold in Recovery Workbench Assumptions Register v1 and Recovery Workbench Test Cases v8 to it. |
| CDC-05357 | RWB-P3-E1018-APP | DOR-RWB-P3-E1018-APP-20 | 9 | Record case.entry.dpd as the single parameter key; align case.entry.dpd_threshold in Recovery Workbench Assumptions Register v1 and Recovery Workbench Test Cases v8 to it. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05351 | RWB-P3-E1018-APP | CG-ALL-3432 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{n}/{v} through the provider's CON story. |
| CDC-05386 | RWB-P3-E1018-CON | CG-ALL-3460 | 12.2 | Publish GET /api/recovery/decision/v1/rule-models/{n}/{v} through the provider's CON story, or consume a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05352 | RWB-P3-E1018-APP | CG-ALL-3433 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-05387 | RWB-P3-E1018-CON | CG-ALL-3461 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or consume a published operation. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05362 | RWB-P3-E1018-APP | DOR-RWB-P3-E1018-APP-1 | 1 | Add or confirm the role name 'product owner' used in section 1 of RWB-P3-E1018-APP. |
| CDC-05398 | RWB-P3-E1018-CON | DOR-RWB-P3-E1018-CON-1 | 1 | Add 'tech lead' as a role code or role name in Users Roles and Permissions v5, or confirm the existing role code that §1 should use. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05372 | RWB-P3-E1018-APP | GAP-0674 | 15 | Publish the gateway-bff composite route for SCR-02 and SCR-03 with path, parallel calls, merge order, masking rules and 2 s budget. |
| CDC-05411 | RWB-P3-E1018-CON | GAP-0674 | find it | Publish the gateway-bff composite route for SCR-02 and SCR-03 with path, parallel calls, merge order, customer-field masking rules and the 2 s budget. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05388 | RWB-P3-E1018-CON | CG-ALL-3462 | 13 | Create story file RWB-P7-E1073-CON, the dependency named in the DP-04 row of section 13. |
| CDC-05391 | RWB-P3-E1018-CON | DOR-RWB-P3-E1018-CON-17 | 13 | RWB-P7-E1073-CON is named in section 13 but has no story file (CG-ALL-3462); the dependency can only be fixed in the story folder, not in this story. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows and Activities sheets (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05190 | RWB-P3-AD019-APP | CG-ALL-3348 | 12.5 | Add workflow DataQualityFreshnessCheck (P3, rwb-case, queue rwb-case, Schedule every 15 minutes) and activity refreshStaleSet, as in RWB-P3-AD019-APP §12.5. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05194 | RWB-P3-AD019-APP | DOR-RWB-P3-AD019-APP-8 | 12.1 | rwb-case.yaml: add GET /data-quality/reconciliation-breaks, /data-quality/referential-completeness and /data-quality/stale-products. rwb-source-data: publish GET /api/recovery/source-data/v1/freshness. Add the three further detcheck paths. |

### OTHER:rwb-source-data contract (P1) and gateway-bff contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05197 | RWB-P3-AD019-APP | GAP-0441 |  | Publish reconciliation, key-resolution and freshness reads with paths, paging and field shapes; publish SCR-45 composite route with merge rules and per-call timeout; add a problem code and text for an unreachable P1 read. |

### OTHER:TSD P1 v3 (API-P1-003 contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05198 | RWB-P3-AD019-APP | GAP-0519 |  | Publish response fields, paging and REC-05 break-list row shape, answered from reconciliation_result DF-OPS-118 to DF-OPS-129 and REC-05 orphan rows. |

### RWB-P1-AD019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05199 | RWB-P3-AD019-APP | GAP-0520 |  | Start JOB-04 from AceDataReady on the workflow kit; run no Temporal Schedule of its own for the console. |

### OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05200 | RWB-P3-AD019-APP | GAP-0728 |  | Add reconciliation, key-resolution and freshness reads as GET operations with business date as query parameter and paged answer; name the rwb-case login with ACE DB owners; fix SCR-45 composite route via RWB-PLT-N001-CON. |

### OTHER:Reconciliations sheet (v3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05201 | RWB-P3-AD019-APP | GAP-0268 |  | Add an owner column to each reconciliation row from the Ownership Map; the owning service answers its Workbench side on its contract, one hop with 2 s timeout; rwb-source-data keeps the ACE side and JOB-04. |

### OTHER:Reconciliations and quality measures register v3 (sheets Reconciliations; OTHER:Quality measures) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05202 | RWB-P3-AD019-APP | GAP-0269 | - | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures, with values from the Ownership Map Tables sheet per service and schema. |

### OTHER:Reconciliations register v3 (new sheet Per-service reconciliation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05203 | RWB-P3-AD019-APP | GAP-0271 | - | Add sheet Per-service reconciliation with one row per service of the 19: tables, check part, key, tolerance, cadence, break and result route, pattern and basis; unsourced cells carry the Template and Rules R9 placeholder. |

### OTHER:FSD P3 (Functional Specification Document P3), section A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05209 | RWB-P3-E1002-APP | GAP-1549 | find it | Restate the A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### OTHER:Open decision register of the P2 story holding DL17 and DL31 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05217 | RWB-P3-E1002-APP | DOR-RWB-P3-E1002-APP-18 | none in this story | Record an assumption for DL17 and an assumption for DL31; neither has one. |

### RWB-P1-E1011-APP; RWB-P1-E1002-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05219 | RWB-P3-E1002-APP | GAP-0485 | find it | Publish GET /case-list/dates/{businessDate} and GET /case-list/rows plus the snapshot(page) activity as proposed; keep the publish_status gate as the release point; retire the lake file and data set (DP-17). |

### OTHER:frontend-context.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05220 | RWB-P3-E1002-APP | GAP-0017 | find it | Record the screen-to-service map derived from the gateway-bff composite routes, including SCR-02 through gateway-bff (DP-19), in the next context run. |

### RWB-P1-E1002-CON; RWB-P1-E1002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05222 | RWB-P3-E1002-APP | GAP-0486 | find it | Add GET /case-list/dates/{businessDate} answering businessDate, publishStatus, rowCount and refreshedAt; GET /case-list/rows in the 19-column order; and the snapshot(page) activity with its input and output shape. |

### OTHER:TSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05223 | RWB-P3-E1002-APP | GAP-1991 | find it | Keep lake_copy_watermark as the watermark of the last published reporting projection and drop the lake extract INT-19 and INT-20 (DP-17). |

### RWB-P1-E1002-APP; RWB-P1-E1002-CON; RWB-P1-E1002-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05225 | RWB-P3-E1002-APP | GAP-0487 | 3 | Name CaseListBuildWorkflow (workflow ID = business date) started by rwb.source-data.AceDataReady.v1 and the DailyCaseList Schedule at 07:15 Asia/Bangkok, overlap SKIP, one-business-date catch-up; 07:15 read from caselist.allocation.wait.until. |

### OTHER:FSD P2 v3 (and BRD Program v4 section 5.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05230 | RWB-P3-E1007-APP | GAP-1534 | none | Remove INT-19 and INT-20 as outbound adapters. INT-19 becomes a rwb-reporting delivery request via the rwb-integration delivery contract; INT-20 becomes continuous ingest in rwb-decision. No lake target. |

### RWB-PLT-TE006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05237 | RWB-P3-E1007-APP | GAP-1416 | n/a | Fix the library contract: artifact and major version, three interfaces with exceptions, DDL of four tables with processed_event and idempotency_key columns, CloudEvents attributes, inbox dedupe, retry ladder and dead-letter topic. |

### OTHER:Operations story and bank Airflow owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05242 | RWB-P3-E1007-APP | GAP-0650 | n/a | Set chart values, replica counts, KEDA threshold, alert thresholds and build ID format; fix the two window trigger contracts and alert identifiers. |

### OTHER:rwb-source-data contract (P1) and rwb-document contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05244 | RWB-P3-E1007-APP | GAP-1162 | header | Add a postal addressee read by party_id with a 2 s budget and a fake; keep the value out of rwb_comms, events and logs. |

### OTHER:rwb-document contract and WIN interface owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05245 | RWB-P3-E1007-APP | GAP-1164 | header | Fix the INT-14 record layout and file pattern with the WIN owner; store the built file behind a claim-check reference; pass only the reference in the manifest. |

### OTHER:TSD P6 Communications v2 (T-A and T6.1) and the gateway-bff owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05246 | RWB-P3-E1007-APP | GAP-1166 | 8 | Confirm the run state is answered from dispatch fields, workflow run and P2 status with no run table; add one read and one rerun on the service base; enforce the right at gateway-bff; confirm edge guard with the owner. |

### OTHER:PRD for RWB-E1-007 outbound interfaces (DL11; OTHER:Template and Rules R9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05247 | RWB-P3-E1007-APP | GAP-1544 | n/a | State the interface-level file size, throughput, window length and daily volume targets as open under DL11, inheriting the programme targets. |

### OTHER:Outbound egress infrastructure values (SCB IT infrastructure; OTHER:MFT team, key store) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05250 | RWB-P3-E1007-APP | GAP-0649 | n/a | Provision the two endpoints, receivers, keys, DNS, allow-list, staging and the size, timeout and rotation values per environment with the MFT team, network and security. |

### OTHER:RWB-P5 document-hub story for WP B-P5-03 (secondary slice of RWB-E1-007) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05252 | RWB-P3-E1007-APP | GAP-1027 | n/a | Treat the P5 slice as new work with six criteria and no legacy AC; take manifest and claim-check fields from RWB-P2-E1007-CON; set CLAIM_CHECK_MINUTES = 15. |

### OTHER:Interface configuration version in force; RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05254 | RWB-P3-E1007-APP | GAP-0981 | find it | Register one OUTBOUND interface row for the access-review file with interface ID, file pattern, data product, owner role and alert role; publish the extract layout, recipient and review-cycle date convention in RWB-P4-AD008-APP. |

### OTHER:Interface Specifications v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05255 | RWB-P3-E1007-APP | GAP-0213 | find it | Story rows still cite v3; interface numbers to be confirmed at the next interface review. |

### OTHER:FSD P2 v3 and interface configuration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05257 | RWB-P3-E1007-APP | GAP-1540 | find it | Interval conflict is between FSD and interface configuration; story text is unchanged. |

### OTHER:FSD P2 v3 (A1.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05258 | RWB-P3-E1007-APP | GAP-1542 | find it | Move removed IDs to an exclusion table with later home; add no FR, NFR or AC; state no inbound adapter, folder, run or sign-off exists. |

### OTHER:FSD P2 v3 (A1.5) and the PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05259 | RWB-P3-E1007-APP | GAP-1546 | find it | State INT-17, INT-18 and INT-22 as reused ACE capabilities with no P2 build and no FR; record that their behaviour is ACE's. |

### OTHER:PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05260 | RWB-P3-E1007-APP | GAP-1547 |  | State that the partner and document channels keep their own contracts, that P2 carries no requirement for them, and record the FSD sentence as superseded. |

### OTHER:Legacy dependency trace sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05261 | RWB-P3-E1007-APP | GAP-3233 |  | Keep the five Not carried rows visible for RWB-E1-056 to RWB-E1-007, RWB-E1-056 to RWB-E1-015, RWB-E1-056 to RWB-E1-069, RWB-TE-009 to RWB-TE-004 and RWB-TE-010 to RWB-TE-003; add an X row only if the run books or harness wait. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05267 | RWB-P3-E1011-APP | CG-ALL-3400 | 12.5 | Add a row for the workflow CaseQualityWorkflow of rwb-case: task queue rwb-case, namespace rwb-recovery, one run per business date, started by the case quality Schedule. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05284 | RWB-P3-E1011-APP | GAP-0268 |  | Give each of the nine reconciliation rows an owner service and a per-service split, taken from the Ownership Map Tables sheet. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations and Quality measures sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05285 | RWB-P3-E1011-APP | GAP-0269 |  | Append Owner and Per-service reconciliation columns to Reconciliations, and an Owner service column to Quality measures, from the Ownership Map Tables sheet. |

### OTHER:Business requirements document, section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05286 | RWB-P3-E1011-APP | GAP-1456 |  | State the rule that Epic 1 stories keep wave 1 where a receiving service epic starts in wave 2. |

### OTHER:RWB-E1-055 legacy story (notice barcode check) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05287 | RWB-P3-E1011-APP | GAP-1169 |  | Give the notice barcode check its own code instead of REC-05. REC-05 stays the business-key orphan check. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations row REC-08) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05289 | RWB-P3-E1011-APP | GAP-0270 |  | Compare each of the 19 services' local decision records on rwb.decision-record.v1 with P7 decision_log_entry, nightly, with the 02:00 hash-chain check. |

### OTHER:Recovery Workbench reconciliation workbook v4 (REC numbering block) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05290 | RWB-P3-E1011-APP | GAP-0273 |  | Add a REC numbering block that maps each check to its number here and in RWB-E1-011, keeping source IDs. |

### RWB-P1-E1011-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05292 | RWB-P3-E1011-APP | GAP-0497 | 19 | Publish GET /admin/reconciliation/results and GET /admin/reconciliation/results/{resultId} on /api/recovery/source-data/v1, the result and break-row element lists, workflow ReconciliationWorkflow with ID recon-{businessDate}, activity reconciliation on rwb-source-data, and interface ReconciliationQuery. |

### OTHER:TSD P3 v3; OTHER:FSD P3 v4 and the rwb-case service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05293 | RWB-P3-E1011-APP | GAP-0740 | 5 | Confirm the three check codes and four state names; publish the four operation paths before the wave-1 contract test; agree REST or Temporal reads with the P1 owner; decide account_id against account_key; set the Schedule cron; add Platform administration R for the quality reads. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05300 | RWB-P3-E1011-APP | GAP-1946 |  | Keep H and C at None; record nine CONs as wave-0 prerequisites; read the ACE side via the DP06 rwb-source-data product; serve asset facts from /api/recovery/asset/v1 quality endpoints. |

### RWB-P6-E1011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05301 | RWB-P3-E1011-APP | GAP-1167 | 3 | Keep H at None; record the seven platform CONs as wave-0 build prerequisites in the dependency map, not as lane dependencies; L-P6-C depth unchanged. |

### OTHER:Reconciliations v3 workbook (Quality measures sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05306 | RWB-P3-E1011-APP | GAP-0276 | find it | Rewrite Timeliness: the ACE batch is complete when rwb-source-data reads it and publishes AceDataReady; other services measure the freshness contract; the measure owner is P1 rwb-source-data. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05307 | RWB-P3-E1011-APP | GAP-0337 | find it | Add the three outbound reads of JOB-04 to the rwb-source-data row of the connection matrix; publish the exclusion resource on the rwb-case contract with its path, fields and 2 s budget (path and fields Not specified in the source documents). |

### OTHER:TSD P6 Communications v2 (T6.1) and the gateway-bff route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05309 | RWB-P3-E1011-APP | GAP-1173 | find it | Declare the two quality reads in the Platform administration area with right R and add that area to the rwb-comms RBAC matrix and the gateway-bff route; the case notice read keeps Litigation R with scope per T-A API-P6-002. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05310 | RWB-P3-E1011-APP | GAP-3172 |  | State the wave 1 delivery of rwb-asset in the service epic and the wave plan, and that the rwb-asset service wave governs its later stories (R5.6 conflict row). |

### OTHER:BRD v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05311 | RWB-P3-E1011-APP | GAP-1457 |  | Renumber section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### RWB-P3-E1013-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05314 | RWB-P3-E1013-APP | DOR-RWB-P3-E1013-APP-14 | header | Record the signed epic design sign-off in the epic design record, then link it from the story. |

### RWB-P3-E1013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05315 | RWB-P3-E1013-APP | DOR-RWB-P3-E1013-APP-21 | header | Create and publish the contract story RWB-P3-E1013-CON, then add it as a contract dependency of this story. |

### RWB-P3-E1013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05316 | RWB-P3-E1013-APP | DOR-RWB-P3-E1013-APP-22 | header | Publish the contract fake library and record its published version in the story. |

### OTHER:FSD P9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05318 | RWB-P3-E1013-APP | GAP-1646 |  | Read Power BI and data lake destinations of A2.1, A2.3, A2.4, A2.5, A2.7 and A2.8 as the rwb-reporting read model on gateway-bff; lake deliveries as files delivered by rwb-integration; restate AC-ALT-P9-001-02, AC-EXC-P9-001-03, AC-P9-004-01 and AC-ALT-P9-004-01. |

### OTHER:FSD P1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05319 | RWB-P3-E1013-APP | GAP-1499 |  | Drop the lake copy and INT-19 extract from A2.12, A2.19 and A2.20; serve reconciliation results and freshness to rwb-reporting through snapshot activity and read model; move the six quality measures to rwb-reporting. |

### OTHER:Version 3 (Facts tab) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05320 | RWB-P3-E1013-APP | GAP-0251 |  | Replace the data-lake star schema with the rwb_reporting read model fed from service topics, served through GET /dashboards/{id} and GET /reports/{id} behind gateway-bff; drop the Power BI lake load. |

### RWB-P3-E1043-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05325 | RWB-P3-E1013-APP | GAP-2241 | 3, 12.1 | Name the age-band reference list with its list code and the table code of its reference version in the reference-data catalog, and use those codes in the read on /admin/lists/{listCode} and on the band list screen. |

### OTHER:Reporting-layer facts and dimensions specification (v3 Facts and Dimensions) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05326 | RWB-P3-E1013-APP | GAP-0252 | 11 | Every ACE-fed fact and dimension row takes its rows from the rwb-source-data contract and its snapshot(page) activity; the read model holds no recovery.v_ace_* grant and P9 never reads the ACE views directly. |

### RWB-ITG-E1013-ITG; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05327 | RWB-P3-E1013-APP | GAP-0339 | 12, 13 | Prove the v5 path: rwb-reporting projects from events and the P1 snapshot activity, publishes on rwb.reporting.events.v1 and rwb-integration delivers the regulatory extract; keep the lake assertion out of the wave 1 suite; add the measure_definition load path and the numbered ReportPublished catalogue entry to the Ownership Map. |

### OTHER:P1 OpenAPI document of the epic's contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05329 | RWB-P3-E1013-APP | GAP-0563 | 12.2 | Fix the readiness, status and payments paths, the 202 answer and the three status values; reuse the path names called by RWB-ITG-E1013-ITG; field names follow the P1 logical data model field IDs. |

### OTHER:project-context.md v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05337 | RWB-P3-E1013-APP | GAP-0016 | find it | Retire the Case volume and Staff rows and use the Volume and Scale Forecast v3 figures from Architecture v5 slides 33 and 48. |

### OTHER:Star schema Facts; OTHER:Dimensions and Measures tables, version 3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05338 | RWB-P3-E1013-APP | GAP-0254 | find it | Add Owner and Values from columns to Facts and Dimensions and an Owner column to Measures, each value taken from Recovery Workbench Microservice Ownership Map v1 (P9 rwb-reporting, schema rwb_reporting). |

### OTHER:P1 functional and technical specifications (FSD and TSD) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05339 | RWB-P3-E1013-APP | GAP-0559 | find it | Mark the lake publish steps, the INT-19 row and lake_copy_watermark removed in the next FSD and TSD versions; keep the publish status of the case list and the reconciliation result. |

### OTHER:P1 TSD; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05341 | RWB-P3-E1013-APP | GAP-0564 | find it | Add the gate pair COMPLETE and HOLD to the list of values in the next P1 TSD version; keep LOADED or STALE per product. |

### OTHER:rwb-case message catalogue and SCR-44 screen specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05343 | RWB-P3-E1013-APP | GAP-2242 | 5 | Add one message for a held facts release to the catalogue; name the release state and the facts and case list count columns of SCR-44 |

### OTHER:DevOps catalogue, values files and run book of JOB-15 (OPS story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05345 | RWB-P3-E1013-APP | GAP-2574 |  | Hold thresholds, channels and run-book paths as catalogue and values-file entries; use the 15-minute failed-run target from NFR-068; name the caller of MSG-GEN-006 in the run book |

### RWB-P3-E1018-OPS; RWB-P3-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05356 | RWB-P3-E1018-APP | DOR-RWB-P3-E1018-APP-17 | 13 | Record Build status Done for both build dependencies once their work is complete, so this story's dependency item passes. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05359 | RWB-P3-E1018-APP | DOR-RWB-P3-E1018-APP-8 | 12.2 | Publish the operations named in the detcheck list through the providers' CON stories (source-data accounts, customers, freshness; decision rule-models; access authorise). |

### OTHER:FSD P3 (section A1.5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05360 | RWB-P3-E1018-APP | GAP-1549 | A1.5 | Restate the ACE read path as a read through the rwb-source-data contract, per Arch v5 slide 45 and ADR-010; keep business-key link rules. |

### OTHER:FSD P1 v3 (section A2.11) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05364 | RWB-P3-E1018-APP | GAP-0575 | 13 | Decide OQ-P1-06: where the per-account REC-05 break list is kept, and the break row fields, with RWB-P1-E1011-APP as owner. |

### OTHER:The database story of RWB-SVC-P3 and the service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05365 | RWB-P3-E1018-APP | GAP-0675 | 3, 10 | Allocate the rwb-case login name and grant it schema rwb_case only, with no privilege on another schema; record the login, its grants and its secret reference in the service catalogue. |

### OTHER:TSD P7 (T3.1 DF-DEC-002; OTHER:T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05370 | RWB-P3-E1018-APP | GAP-2435 | 13 | Restate DF-DEC-002 as an indexed business key with no foreign key, drop the decision_log_entry to recovery_case row of T3.3, and state in T3.1 that the ALS business date is carried inside inputs_ref. |

### OTHER:Recovery Workbench work package index (WP C-WEX) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05374 | RWB-P3-E1018-APP | GAP-3206 |  | Correct the heading '(E1-018)' to a scheduling label; the subject of the worked example remains RWB-E1-020. Record the reading in the run edit log. |

### OTHER:Requirements traceability register v7; OTHER:REQ-RDF-004 row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05375 | RWB-P3-E1018-APP | GAP-3213 | 18 | List the legacy slices RWB-E1-069, RWB-E1-018 and RWB-E2-006 and the citing stories RWB-ITG-E3013-ITG, RWB-ITG-E3017-ITG and RWB-ITG-E3026-ITG; the E3 integration trace is accepted, so no section 18 row is added here. |

### OTHER:Recovery Workbench work package index (build sequence) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05377 | RWB-P3-E1018-APP | GAP-2437 |  | Record that RWB-P7-E1018-APP builds against platform contracts and fakes of section 12.8 and reads wave-1 tables in its own schema, with no dependency row change. |

### OTHER:rwb-case deployment topology and environment values (platform Helm chart values) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05379 | RWB-P3-E1018-APP | GAP-0677 |  | Publish cluster names, node pools, replicas, resources, zone spread, ingress class and probe settings as values files for rwb-case. |

### OTHER:RWB-PLT-DB (platform DB story) and secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05381 | RWB-P3-E1018-APP | GAP-2438 |  | Fix the rwb-decision login name with migration and application roles kept apart, and reference it from every P7 story. |

### OTHER:rwb-source-data and rwb-decision OpenAPI yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05392 | RWB-P3-E1018-CON | DOR-RWB-P3-E1018-CON-8 | 12 | Publish the GET paths named in the detcheck: source-data accounts/{id}, customers/{id}, freshness; decision rule-models/{n}/{v}; and the four more listed. |

### OTHER:Recovery Workbench FSD P3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05393 | RWB-P3-E1018-CON | GAP-1549 | find it | Restate the A1.5 ACE read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### RWB-P3-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05399 | RWB-P3-E1018-CON | DOR-RWB-P3-E1018-CON-10 | find it | Add an error and no-access state to SCR-02, and empty, error and no-access states to SCR-03 in the app story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05400 | RWB-P3-E1018-CON | DOR-RWB-P3-E1018-CON-12 | 12.7, 16, 18 | Add TC-P3-E1018-CON-01 to -15 to Test Cases v8. Align the §18 test lists with RTM v7. |

### OTHER:The standard message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05401 | RWB-P3-E1018-CON | DOR-RWB-P3-E1018-CON-9 | 14 | Issue contract-level message IDs that do not clash with the standard: MSG-P3-030, MSG-P3-031, MSG-P3-032 and MSG-P3-033 are used in §14 with meanings other than the standard's, and two further §14 IDs clash as well; §14 then copies the agreed IDs. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:RWB-E1-013 C row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05402 | RWB-P3-E1018-CON | GAP-2567 | find it | Add the two rwb-source-data rows (payments since entry, daily completeness gate) to the wave dependency map. Keep the metadata rows as the plan states them. |

### OTHER:Recovery Workbench API inventory and service API document (rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05403 | RWB-P3-E1018-CON | GAP-0571 | find it | Publish GET /api/recovery/source-data/v1/entry-candidates with required businessDate and threshold, optional page and size, response EntryCandidatePage, statuses 400, 401, 403, 409, 422, 503. |

### OTHER:RWB-SVC-P3 database story and service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05404 | RWB-P3-E1018-CON | GAP-0675 |  | Allocate the rwb-case login name, its grants (schema rwb_case only, no privilege on another schema) and its secret reference, and record them in the service catalogue. |

### OTHER:openapi/rwb-case-v1.yaml (the rwb-case API file) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05405 | RWB-P3-E1018-CON | GAP-0676 | 11, 12.1, 19 | Record the field-level schema agreed in the baseline review of RWB-P3-E1018-CON: required flags per operation, the page and sort parameter set of GET /cases, the caseNo pattern and the exact error codes per operation. |

### OTHER:TSD P7 v3 (T3.1; OTHER:T3.3; OTHER:DF-DEC-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05407 | RWB-P3-E1018-CON | GAP-2435 |  | Restate DF-DEC-002 as an indexed business key with no foreign key, drop the recovery_case row of T3.3, and state in T3.1 that the ALS business date is carried inside inputs_ref. |

### OTHER:Package ENTRY rule-row catalogue (Business analyst; OTHER:Epic 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05408 | RWB-P3-E1018-CON | GAP-2436 |  | Name the rule ID that admits a case in the rule-row catalogue, then copy that identifier into this story's registry fixture. |

### RWB-P2-E2007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05413 | RWB-P3-E1018-CON | GAP-0595 | 4 | Take the account set and product group from case_list_row for the case and business date; otherwise declare GET /api/recovery/case/v1/cases/{caseId}/accounts in RWB-P2-E2007-CON and add C RWB-P3-E1018-CON. |

### RWB-P7-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05414 | RWB-P3-E1018-CON | GAP-1265 | find it | Add C rows for RWB-P1-E1015-CON and RWB-P3-E1018-CON, or record both reads as route-level composites of RWB-PLT-N001-CON. |

### API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:rwb-case administration stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05415 | RWB-P3-E1018-CON | GAP-2223 | 11 | Record the authorise request and response shape in the rwb-access API specification, name the checklist contract story in the Ownership Map and the C dependency set, and load the task code, owner role, discretion, due-date parameter and decision code as data rows before wave 2 |

### OTHER:Work Package dependency rows (D1) of the consuming case-search story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05416 | RWB-P3-E1018-CON | GAP-2335 | find it | Add C RWB-P3-E1018-CON and C RWB-P4-E1037-CON to the dependency map at D1 and state the search is buildable from Day 1 against the two fakes. |

### OTHER:WP C-WEX (work package index) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05420 | RWB-P3-E1018-CON | GAP-3206 | none | Correct the heading label of the work package and record the reading that E1-018 is a scheduling label in the next run's index. |

### RWB-P7-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05422 | RWB-P3-E1018-CON | GAP-2437 | none | Record that the secondary slice builds against platform contracts and section 12.8 fakes and reads wave-1 tables in its own schema; no dependency row moves. |

### OTHER:ASM-B-P1-07-E1018-2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05423 | RWB-P3-E1018-CON | GAP-0572 | none | Record one business-date entry-read operation, paged by page and size; default and maximum page size: Not specified in the source documents (GAP-0572); a per-account read is refused under DP-11. |

### OTHER:Platform deployment template and rwb-case environment values file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05424 | RWB-P3-E1018-CON | GAP-0677 | none | Publish the rwb-case deployment topology (cluster names, node pools, replicas, resources, zone spread, ingress class, probe paths and timings) as environment values files. |

### OTHER:RWB-PLT-DB and the secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-05426 | RWB-P3-E1018-CON | GAP-2438 | none | Fix the rwb-decision database login name, keep migration and application roles separate, and reference it from every P7 story. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20713 | RWB-P3-E1011-APP | R-21918 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21918', 'R-22054', 'R-22286', 'R-22289', 'R-22316', 'R-28613'] |

### 05 Technical architecture/Recovery Workbench Interface Specifications v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20892 | RWB-P3-E1007-APP | R-28449 |  | The story rows that cite v3 are in the story file. Interface numbers are to be confirmed at the interface review. No change in this workbook (GAP-0213). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0016 | Volumes differ between the v2 context and v5 | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0017 | No v5 screen inventory or screen-to-service map | Solution architect and UX lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0063 | Wave conflict S5 / EP01 | Tech lead | Resolved (directive) |
| GAP-0213 | Five rows still cite 'number in Interface Specifications v3' after v4 of that document was issued | Integration architecture team | Resolved (directive) |
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
| GAP-0334 | deliverFile manifest payload, claim-check handoff and the file-window trigger contract are not defined | Solution architect | Resolved (directive) |
| GAP-0335 | The target read operation that serves the case list and the path by which the daily extract reaches rwb-reporting once the data lake is removed are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0336 | Owner of REC-03 and REC-04 and the reporting delivery path of the two extracts are not named for the microservice target | Solution architect | Resolved (directive) |
| GAP-0337 | The connection matrix does not show the rwb-source-data outbound reads and the exclusion operation of the case contract is not named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0338 | Connection matrix gives rwb-integration only the document REST call and the outside file edge, while the file build reads source data and the failure reaches rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0339 | E1013 integration path after the data-lake removal | Solution architect | Resolved (directive) |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0441 | The data quality console read shapes, the gateway-bff route specification, the refresh cadence and the unreachable-read message are not stated in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0447 | The cutover reconciliation harness pack for legal events and cases is not specified | Integration lead | Resolved (directive) |
| GAP-0485 | The case list extract file, the outbound file adapter and the 07:30 Power BI data set have no target after the data lake is removed | Data architect | Resolved (directive) |
| GAP-0486 | The case-list read operations and their answer shapes are not specified in Arch v5 or in TSD P1 | Solution architect | Resolved (directive) |
| GAP-0487 | The case-list workflow name, the schedule name and the 07:15 fallback are not specified | Solution architect | Resolved (directive) |
| GAP-0495 | The two lake extracts and the Power BI data set have no successor in the target, while the legacy story still writes them and reads the report | Solution architect | Resolved (directive) |
| GAP-0496 | TSD P1 keeps REC-03, REC-04 and a cross-estate REC-05 inside P1 while the Change Register gives rwb-case, rwb-asset and rwb-comms their own slices of the same legacy key | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0497 | The reconciliation result path, the result and break-row shape, the ReconciliationQuery interface and the workflow and activity names are not specified in any source | Tech lead | Resolved (directive) |
| GAP-0519 | The shape of the reconciliation read and of the REC-05 break list is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0520 | DP-10 is listed on the P1 slice while JOB-04 is an event-started workflow and the freshness Schedule is rwb-case's | Solution architect | Resolved (directive) |
| GAP-0558 | DP-17 removes the INT-19 lake extract and the Power BI feed that legacy AC3 and AC7 assert | Business analyst, P1 and P9 | Resolved (directive) |
| GAP-0559 | The P1 functional and technical specifications still describe the lake publish that DP-17 removes | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0560 | RWB-E1-013 is split across four stories and no single source assigns each legacy acceptance criterion | Business analyst, P1, P3 and P9 | Resolved (directive) |
| GAP-0561 | The 05:30 late check and the worker and queue registration have no story in the build dependencies of this slice | DevOps team and platform workflow owner | Resolved (directive) |
| GAP-0562 | No measure value, definition or snapshot is produced or read by the P1 slice of RWB-E1-013 | Business analyst, P1 and P9 | Resolved (directive) |
| GAP-0563 | The readiness and status operation shapes are fixed only in part by the architecture text | Solution architect and TechX contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0564 | The gate answers COMPLETE or HOLD while the freshness list of values holds LOADED and STALE | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0565 | MSG-P1-001 now names the ACE batch where the legacy story and the integration copy name a load | Business analyst, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0571 | The entry-candidate contract: the resource and parameter names, the response entity, its field names, the paging, the error status set and the access rule are not fixed by any source, and this legacy key has no contract story of its own | Tech lead of rwb-source-data with the solution architect and the P3 owner of the case contract | Resolved (directive) |
| GAP-0572 | Whether the entry read is one operation for a business date or one operation per account, and how a page of about 28,100 candidates is cut, are not specified | Tech lead of rwb-source-data with the owner of the rwb-case case creation job | Resolved (directive) |
| GAP-0573 | Which service writes account_ext.dispute_open and the party_ext flags, which right the confirmation needs, and where party_ext.vulnerable comes from on the first write are not settled | Solution architect with the P1 service owner, the P3 owner of the exclusion screen and the P4 owner of the role model | Resolved (directive) |
| GAP-0574 | The ALS batch gate before RWB-ACE-001 lands: v_ace_batch_status is a Section B view, and the behaviour of an entry read for a date whose batch record does not exist yet is not specified | Recovery tech lead with the ACE team lead and the platform team that owns the RWB-ACE-001 sequence | Resolved (directive) |
| GAP-0575 | The shape and the home of the REC-05 break list are not specified, and the table that held it leaves the schema | Data architect with the data steward and the P1 owner of the reconciliation job | Resolved (directive) |
| GAP-0576 | The product group of a candidate row: whether the ACE product_category value is passed through or mapped to the LOV-PRODUCT codes, and what happens to a value outside the list, is not specified | Business analyst, P1 with the center of excellence and the owner of the rwb-case reference data | Resolved (directive) |
| GAP-0595 | The case's account set and its product group have no P1 read in the target | Solution architect | Resolved (directive) |
| GAP-0647 | rwb-integration outbound-file capability: ACE read path, INT-25 source table, data-lake retirement, JOB-10 and JOB-11 split, operation naming, alert event names, deliverFile manifest and job catalog rows not settled | Solution architect | Resolved (directive) |
| GAP-0648 | Outbound-file contract: deliverFile manifest and return, notice-fact read of rwb-comms, JSON field names and problem body, event schema subject and compatibility level not fixed by any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0649 | Outbound egress infrastructure: endpoint names, accounts, folders, receiver ranges, PGP key identifiers, staging names, file-size limit, transfer timeout and rotation period not specified in any source | SCB IT infrastructure | Resolved (directive) |
| GAP-0650 | Outbound-file deployment: chart values, replica counts, KEDA threshold, lag and alert thresholds, dashboard names, build ID format, Airflow trigger contract of the two file windows and the message identifiers of the lag and window alerts not specified in any source | DevOps team | Resolved (directive) |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0675 | Per-service login name for rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0676 | Field-level OpenAPI schema of the case resource is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0677 | Deployment topology detail for rwb-case is not specified | DevOps engineer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0728 | RWB-AD-019 in rwb-case: login name, edge composite route, source-data read shape and contract placement not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0739 | The case side of an outbound file outcome leaves the delivery-event element names, the route state to resume, the task code and due date, the fate of the legacy in-process interfaces and the two lake extracts unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0740 | The rwb-case slice of RWB-E1-011 leaves the check codes, the four operation paths, the call type to rwb-source-data, the case key columns, the Schedule cron, the access right, the login and every report value that only the data lake held unspecified | Solution architect, with the P1 rwb-source-data owner, the P3 rwb-case owner and the data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0981 | rwb-access access-review extract (JOB-18): the interface ID, the file pattern, the extract layout, the recipient and the review-cycle date convention are not specified, the two requester activity names and the manifest are named by no source, and the delivery events are keyed by case ID while an access-review file has no case | Solution architect, P4 with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1027 | The secondary P5 slice of RWB-E1-007 has no legacy AC and several document-hub values of the outbound path are not fixed in the sources | Solution architect (P5 document hub, with the rwb-integration contract owner) | Resolved (directive) |
| GAP-1038 | The rwb-document login name, the not-found message ID of the case read and the case-read field names are not specified | Solution architect with the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1085 | No operation in the ownership map raises a task on rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1396 | Airflow product, tenancy, DAG names, identity method, timeout and retry values, the DailyCaseRun wait contract and the file-window operation are not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1499 | The data lake and the dashboard connection are removed, so the reporting destinations of three FSD features have no home | Solution architect | Resolved (directive) |
| GAP-1503 | The baseline measure job has two owners, one in the FSD and one in the architecture | Center of excellence | Resolved (directive) |
| GAP-1508 | The per-account reconciliation break rows have no store after the quality-exception table leaves the schema | Data architect | Resolved (directive) |
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
| GAP-1646 | The data lake and the Power BI connection are removed but the whole reporting FSD is built on them | Solution architect | Resolved (directive) |
| GAP-1649 | The measure set is six definitions in one acceptance criterion and seven measures in another | Tribe lead with the Reporting and BI analyst | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1991 | P1 keeps a lake copy after the data lake is removed | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2223 | The case-side slice of the field-capture path rests on answers no source specifies: the stage and route fields of the case resource, the authorise call shape, the contract story of the checklist read, and the task data | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-2252 | The decision code and the payload of the decision records the seed writes are not in the sources | TechX and the rwb-decision contract owner | Resolved (directive) |
| GAP-2335 | The two DP-11 contract reads of the legacy in-process calls are absent from the Work Package dependency rows and DP-08 is not among the patterns | Solution architect | Resolved (directive) |
| GAP-2433 | The message text of MSG-P7-009 and of the chain warning MSG-P7-012 is named in the sources but never written | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2435 | TSD P7 still models decision_log_entry.case_id as a uuid with a relationship to recovery_case and gives the row no business-date column | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2436 | The literal rule ID of the ENTER rule of package ENTRY is named in no source | Business analyst, Epic 1 | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2438 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-3160 | The P2 outbound adapter writes a table owned by rwb-debtsale | Integration lead | Resolved (directive) |
| GAP-3162 | The case story writes the P1 extension tables | P3 case owner | Resolved (directive) |
| GAP-3169 | The reconciliation story writes 'the case exceptions' without naming a table | P1 data owner | Resolved (directive) |
| GAP-3172 | Service S5 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3209 | No single source divides the thirteen legacy criteria of RWB-E1-020 across its seven stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3232 | The story catalog carries 2,534 dependency rows while the story files carry 2,609 for the same 1,034 stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3233 | Five of the 325 story dependencies of version 4 are carried by no row of the realigned graph | TechX with the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3240 | One module per item in version 3 becomes several services per item in the split | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E1018-APP | skipped AC ID | 109 | missing: AC1, AC9, AC13, AC15 |
