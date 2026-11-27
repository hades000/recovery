# RWB-SVC-S2 rwb-treatment (Treatment and offer) - review pack, part 1 of 4 (RWB-S2-E2004-APP to RWB-S2-E2017-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 113 |
| Cross-document (pending in another document) | 213 |
| Not applied (value not in the sources) | 12 |
| Open business decisions | 26 |
| Register gaps linked | 134 |
| Unconfirmed assumptions | 0 |
| Lint findings | 3 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S2-E2004-APP | 18 | 41 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2004 APP Treatment entity and plan timers data model v2.md |
| RWB-S2-E2006-APP | 17 | 25 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2006 APP Credit approval pack for NLEADS v2.md |
| RWB-S2-E2007-APP | 18 | 45 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2007 APP Booking confirmation from the ALS load v2.md |
| RWB-S2-E2008-APP | 29 | 58 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2008 APP Payment matching with the missed payment event v2.md |
| RWB-S2-E2010-APP | 14 | 21 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2010 APP Stage 2 data products contracts, plans and treatments v2.md |
| RWB-S2-E2017-APP | 17 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E2017 APP Contract, CA and mortgage document generation screens v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S2-E2006-APP | R-12117 | CG-ALL-8290 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E2007-APP | R-12126 | CG-ALL-8310 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E2008-APP | R-12135 | CG-ALL-8332 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E2017-APP | R-12144 | CG-ALL-8354 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E1038-APP, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22353 | GAP-0919 | Register gap | Business lead | Which delegation limit version is in force on the approval date of a treatment is a data state, not a document value | Decide the version in force per environment at the DoA load (RWB-P4-E1038-APP) and keep it out of code; the lookup always answers the version whose window covers the date asked, and the answer names it |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22357 | GAP-0704 | Register gap | Data product owner | The 01:30 treatment extract has no owner in the target and its DP04 read path and freshness element are not in the Ownership Map | Record the owner of the treatment extract as P9 rwb-reporting on JOB-15 with the DP04 copy in rwb_source_data, publish the case-facing read GET /api/recovery/source-data/v1/data-products/DP04/records with its freshness element in the Ownership Map and the P1 API file, and state in the event catalogue that the copy is built from the treatment events. |
| RWB-ITG-E2008-ITG, RWB-P1-E1015-APP, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22404 | GAP-0600 | Register gap | Solution architect with the P1 data product owner | FSD P1 A2.2 stamps a payment read on DP01 Account and arrears while the Work Package slice note names DP05, and no source states whether the read or the rwb-payment run answers a held business date | Hold both gates on DP01 Account and arrears and answer 409 with MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run, with no row of any kind; record DP05 as not the stamp of a payment read and correct the slice note in the Work Package and the data product map in the next version of FSD P1 A2.2; state in RWB-P8-E2008-CON that the run's own refusal for the business date is its own and that the read's 409 is the answer to a call made anyway. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22414 | GAP-1630 | Register gap | Finance and CFO delegate | The posting file has no layout, no schedule and no receiving ledger in any source | Fix one line per posting with case, account key, entry type, amount, value date, business date and posting reference, a manifest with count and checksum, and delivery through rwb-integration. Agree the layout with Finance and the ledger owner before wave 3. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22415 | GAP-1632 | Register gap | Business lead | A reversed payment has no product behaviour in the FSD although the routing rules require the case to reopen | Decide whether a reversal is in scope for this service. If it is, add a reversal source value, a reversal state on the proceeds record and an event that reopens the case through rwb-case. Until then the capability is out of scope and listed as an open question. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22416 | GAP-1633 | Register gap | Finance and CFO delegate | The fee tables that the fee feature reads are not defined anywhere | Name the fee table, its owner and its schedule, and hold the fee rate, the cap and the basis as versioned rows. Until then the fee calculation has no input and the feature cannot be tested. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22419 | GAP-1636 | Register gap | Finance and CFO delegate | The order in which a receipt is applied to the balance is named but not specified | Hold the application order as versioned rows with an owner and a valid-from date, record the version on each proceeds row, and let Finance set the sequence before wave 3. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22514 | GAP-0943 | Register gap | Compliance and PDPA officer | rwb-access document set: the masking version in force for SIT and the field IDs of the personal fields on the review view are not specified | Fix the mask version label per environment in the policy pack load, publish the field IDs of a generated contract and its parties with the LDM, and have the pack owner confirm the DF-PTY-007 and DF-PTY-016 rows before SIT. |
| RWB-ITG-E2017-ITG, RWB-P4-E2017-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E2017-APP, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22516 | GAP-1582 | Register gap | Legal counsel | E-discovery and court-ready evidence have no FSD feature, no operation and no response target | FR-P5-028, FR-P5-029 and AC-P5-021 carry the behaviour with the response target left open as OQ-P5-09. A discovery operation and its response target are needed before wave 2 acceptance. |
| RWB-ITG-E2017-ITG, RWB-PLT-TE012-APP, RWB-P3-E1018-CON, RWB-P3-E1043-CON, RWB-P4-E2017-APP, RWB-P5-E1024-APP, RWB-P5-E2017-APP, RWB-P5-E2017-CON, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2018-APP, RWB-P7-E1027-CON, RWB-P7-E2017-APP, RWB-S2-E2017-APP | R-22520 | GAP-1016 | Register gap | Solution architect, with the Legal counsel and product owner for the template set and the P6 and P5 service owners | The generation screens have no screen-read endpoint, the send path and the signature endpoint change owner, the lock flag and the three document states are in no list, and six consumed contracts sit outside the contract-dependency list | Declare the set read and the merge-value read on base /api/recovery/document/v1 as this key's screen operations (ASM-102); keep the legacy section 13 name for the send, rebased as POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send, and consume P6's API-P6-009 instead of providing the legacy signature endpoint (ASM-101); read the locked flag as a property of the P6 catalog answer and treat a field with no flag as locked (ASM-103); write DRAFT, REVIEWED and SENT as the three values of document.state and leave every transition to this story (ASM-104); keep the template set, the three legal types and the type mapping as data rows confirmed by Legal and the product owner (ASM-105); promote a reviewed document through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP without naming a new operation (ASM-106); consume the P6 catalog, S2 treatment, P3 case, P7 ledger and P6 signature operations with fakes while the C list keeps the reference-data contract only (ASM-107); build the three signature-request operations that rwb-comms calls and mark their names as not specified (ASM-108); read GEN_IDEMPOTENCY_HOURS from document_hub_parameter, which is this service's own table (ASM-109); carry the D6.4 record as the only published element and declare no rwb.document event (ASM-110); rename the two flags (ASM-111); and carry the login name, the two message texts and the tentative release as placeholders (ASM-112). |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-28740 | GAP-1638 | Register gap | Product owner | The only success measure of the module has no baseline and no measurement definition | Take the measure from the decision log as the FSD says, and have the product owner set the baseline, the target and the definition of 'the same day' before the wave-2 release note. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S2-E2004-APP | R-22349 | GAP-1346 | 12.2 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Section 12.2 text is not in this chunk, so the seven operation rows cannot be anchored. Plan confirmation needs the solution architect, not a story edit. |
| RWB-S2-E2006-APP | R-07595 | DOR-RWB-S2-E2006-APP-21 | find it | Definition of Ready item 21 Contract published: Fail | RWB-S2-E2006-CON and any CON dependency are absent from all sources. Adding one needs a new story key, which is not allowed. Story unchanged. |
| RWB-S2-E2006-APP | R-19132 | DOR-RWB-S2-E2006-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | The field detcheck classes as personal data is not named in any source. No field can be corrected. Story no-personal-data statement unchanged. |
| RWB-S2-E2006-APP | R-19135 | DOR-RWB-S2-E2006-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Current text of sections 7 and 16 is not in this chunk, so no safe anchor exists. Add the BR4 criterion and test case once that text is supplied. |
| RWB-S2-E2007-APP | R-07599 | DOR-RWB-S2-E2007-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record is named in the story or sources (Decision Log v11/v12 searched; only DT05 names a design sign-off process). Cannot confirm without inventing a record. |
| RWB-S2-E2007-APP | R-19139 | DOR-RWB-S2-E2007-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Item and sources do not name the P2 field classed as personal data; identifying it would invent a value. |
| RWB-S2-E2007-APP | R-26823 | CG-ALL-8307 | 14 | MSG-P2-006 text differs from the Error and Message Standard v4 | Standard v4 §4 MSG-P2-006 text found, but story use is outside its Raised when. The fix needs a new message ID from the BA, a business decision that cannot be invented here. |
| RWB-S2-E2007-APP | R-26825 | CG-ALL-8312 | 12.5 | Criteria and tests keep legacy job and decision-log wording | The JOB-nn, decision-log and job-record lines are in §7 and §16, which are not in this chunk. §12.5 has no such wording. Apply in the chunk holding them. |
| RWB-S2-E2007-APP | R-28731 | GAP-2488 | 3 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Header already matches the WP (Depends on (build) None; contract RWB-P2-E2007-CON only). The pattern table (section 3) and 12.8 fakes text are not in this chunk; resubmit with those parts. |
| RWB-S2-E2010-APP | R-07617 | DOR-RWB-S2-E2010-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version found in PRD S2 or FSD S2 (only REST base /api/recovery/treatment/v1). Placeholder already in header Contract version row; no value invented. |
| RWB-S2-E2010-APP | R-12140 | CG-ALL-8343 | 12.8 | Criteria and test data read ACE views directly | Flagged ACE-view read is in AC6 of section 7, which is not in this chunk. Section 12.8 has no ACE read to change. Needs section 7 text. |
| RWB-S2-E2010-APP | R-19160 | DOR-RWB-S2-E2010-APP-7 | 11 | Definition of Ready item 7 Data: Partial | Placeholders already in BR Field ID of the updated_at and LOV reference-data rows. No DF ID for these fields in PRD S2 or FSD S2 (LOV-TRT-OUTCOME not found there). |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15835 | RWB-S2-E2004-APP | CG-ALL-8265 |  | Remove the fixed enum on approvalLevel so LOV-APPROVAL-LEVEL values are accepted as data without a code change. |
| CDC-15836 | RWB-S2-E2004-APP | CG-ALL-8266 |  | Remove the fixed enum on proposedBy so LOV-PROPOSER values are accepted as data without a code change. |
| CDC-15837 | RWB-S2-E2004-APP | CG-ALL-8267 |  | Remove the fixed enum on treatmentType so LOV-TREATMENT values are accepted as data without a code change. |
| CDC-15838 | RWB-S2-E2004-APP | CG-ALL-8268 |  | Remove the fixed enum on outcome so LOV-TRT-OUTCOME values are accepted as data without a code change. |
| CDC-15839 | RWB-S2-E2004-APP | CG-ALL-8269 |  | Remove the fixed enum on signatureStatus so LOV-TRT-SIGNATURE values are accepted as data without a code change. |
| CDC-15844 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-8 | find it | Replace the closed enums with LOV references: approvalLevel to LOV-APPROVAL-LEVEL, proposedBy to LOV-PROPOSER, treatmentType to LOV-TREATMENT, outcome to LOV-TRT-OUTCOME, and the four further fields in detcheck. |
| CDC-15901 | RWB-S2-E2007-APP | CG-ALL-8297 | 12.1 | Publish the GET approved-not-booked list path under /api/recovery/treatment/v1 through RWB-S2-E2007-CON; operation name Not specified (GAP-2691; ASM-4444). |
| CDC-15902 | RWB-S2-E2007-APP | CG-ALL-8298 | 12.1 | Publish the POST mark-booked write under /api/recovery/treatment/v1 through RWB-S2-E2007-CON; operation name Not specified (GAP-2691; ASM-4444). |
| CDC-15903 | RWB-S2-E2007-APP | CG-ALL-8299 | 12.1 | Publish the POST booking-difference write under /api/recovery/treatment/v1 through RWB-S2-E2007-CON; operation name Not specified (GAP-2691; ASM-4444). |
| CDC-15909 | RWB-S2-E2007-APP | DOR-RWB-S2-E2007-APP-8 | 13 | Add the approved-not-booked GET, the mark-booked POST and the booking-difference POST with the fields listed in the item; operation names are Not specified in the source documents (GAP-2691; ASM-4444). |
| CDC-15946 | RWB-S2-E2008-APP | CG-ALL-8318 | 12.1 | Publish GET /api/recovery/treatment/v1/treatments/{treatmentId} (API-S2-002) through RWB-S2-E3001-CON, or remove the operation from the story. |
| CDC-15947 | RWB-S2-E2008-APP | CG-ALL-8319 | 12.1 | Publish PATCH /api/recovery/treatment/v1/treatments/{treatmentId} (API-S2-003) through RWB-S2-E3001-CON, or remove the operation from the story. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15846 | RWB-S2-E2004-APP | CG-ALL-8264 | find it | Record decision_record as the platform library table of DP-03 in schema rwb_treatment, or add it as a dictionary name. |
| CDC-15852 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-7 | 11 | Add DF-TRT-023 as a BR Field ID in LDM v9. Confirm decision_record as an entity in LDM v9 or Data Classification v5. |
| CDC-15876 | RWB-S2-E2006-APP | CG-ALL-8280 | find it | Add or confirm field credit_result_at for DF-TRT-026 on treatment, or supply the dictionary name the story should use. |
| CDC-15877 | RWB-S2-E2006-APP | CG-ALL-8281 | find it | Record decision_record as the PLT library table in rwb_treatment for DF-DEC-001 to DF-DEC-018, or supply the dictionary name. |
| CDC-15911 | RWB-S2-E2007-APP | CG-ALL-8293 | 3 | Record principal_outstanding as a v_ace_account column owned by rwb-source-data, or add it to the dictionary under its dictionary name. |
| CDC-15912 | RWB-S2-E2007-APP | CG-ALL-8294 | 3 | Record settlement_booked_date as a v_ace_account column owned by rwb-source-data, or add it to the dictionary under its dictionary name. |
| CDC-15913 | RWB-S2-E2007-APP | CG-ALL-8295 | 3 | Record settlement_booked_amount as a v_ace_account column owned by rwb-source-data, or add it to the dictionary under its dictionary name. |
| CDC-15914 | RWB-S2-E2007-APP | CG-ALL-8296 | 12.7, 13 | Record decision_record as the PLT library object applied in rwb_treatment (DP-03), or add it to the dictionary under its dictionary name. |
| CDC-15951 | RWB-S2-E2008-APP | CG-ALL-8317 | 12.7 | Add decision_record as a field or entity in LDM v9 or Data Classification v5, or use the existing dictionary name. |
| CDC-15960 | RWB-S2-E2008-APP | DOR-RWB-S2-E2008-APP-7 | 11 | Add decision_record as a rwb_treatment entity (local PLT decision record, DF-DEC-001 to DF-DEC-018) or name the LDM entity it maps to. |
| CDC-16036 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-7 | 11 | Add decision_record as the PLT library entity in rwb_treatment (DP-03) with its fields to LDM v9 and Data Classification v5. |

### RWB-P8-E2008-APP (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15957 | RWB-S2-E2008-APP | DOR-RWB-S2-E2008-APP-10 | 15 | Add Empty, Loading, Error and No access state rows for SCR-28 Proceeds matching and SCR-44 run summary, which rwb-payment owns. SCR-14 rows already exist in section 15. |
| CDC-15973 | RWB-S2-E2008-APP | GAP-1348 | not in chunk | Align the proceeds field set with TSD P8 T3.1, replace payment_missed_event_key with the DP-09 idempotency_key table, and use the service's own next Flyway number. |
| CDC-15975 | RWB-S2-E2008-APP | GAP-1352 |  | Worker floor and ceiling, resource requests and limits, cluster and environment names, partition count, topic retention, PROD rollout strategy, release gate approvers, rollback window. Not specified in the source documents (GAP-1352) |
| CDC-15976 | RWB-S2-E2008-APP | GAP-1354 | not in chunk | Reallocate legacy AC1, AC3, AC4 and AC5 to RWB-P8-E2008-APP, or add a coverage note. |
| CDC-15980 | RWB-S2-E2008-APP | GAP-1635 |  | Reconcile FEAT-PAY-11 to the ACE payment and account position and the posting file; record a ledger return as an open question until the ledger owner publishes one. |
| CDC-15981 | RWB-S2-E2008-APP | GAP-1640 |  | Keep one matching run per business date in wave 2; record the same-day payment-received trigger as an open question; add an intraday run only when a daytime payment interface is named. |
| CDC-15983 | RWB-S2-E2008-APP | GAP-2493 |  | Split the record: rwb-payment writes and publishes the local record in its own transaction; rwb-decision collects, appends to the hash-chained ledger and runs JOB-14, evaluating no payment. |
| CDC-15986 | RWB-S2-E2008-APP | GAP-2505 |  | Ship one chart with api and worker deployments, migration job, topics, consumer groups, five alerts with runbook links, four dashboard series, flag, backfill and rollback; take thresholds as environment values. |
| CDC-15990 | RWB-S2-E2008-APP | CG-ALL-8335 | 15 | Carry the SCR-28 states (empty, loading, error, no access) in its section 15; empty, error and no access are Not specified in the source documents (CG-ALL-8335). |
| CDC-15991 | RWB-S2-E2008-APP | CG-ALL-8336 | 15 | Carry the SCR-44 states (empty, loading, error, no access) in its section 15; empty, error and no access are Not specified in the source documents (CG-ALL-8336). |
| CDC-15998 | RWB-S2-E2008-APP | GAP-1353 |  | Hold outbox-lag, dead-letter, workflow-failure, API error-rate and latency thresholds as data in the service values file with no default. Not specified in the source documents (GAP-1353) |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15878 | RWB-S2-E2006-APP | CG-ALL-8282 | 11 | Add treatment entity rows for DF-TRT-023 to DF-TRT-026 (nleads_ref, credit_result, credit_result_reason, credit_result_at), as in Physical Schema v4 (06 Data). |
| CDC-15879 | RWB-S2-E2006-APP | CG-ALL-8283 | 11 | Add the treatment field row for DF-TRT-024 (credit_result), which LDM v9 lacks, so the story's section 11 mapping resolves; the story keeps its ID |
| CDC-15880 | RWB-S2-E2006-APP | CG-ALL-8284 | 11 | Add the treatment field row for DF-TRT-025 (credit_result_reason), which LDM v9 lacks, so the story's section 11 mapping resolves |
| CDC-15881 | RWB-S2-E2006-APP | CG-ALL-8285 | 11 | Add the treatment field row for DF-TRT-026 (credit_result_at), which LDM v9 lacks, so the story's section 11 mapping resolves |
| CDC-15884 | RWB-S2-E2006-APP | DOR-RWB-S2-E2006-APP-7 | 11 | Add or correct treatment rows DF-TRT-023 to DF-TRT-026, and register credit_result_at and decision_record in LDM v9 and Data Classification v5 |
| CDC-15918 | RWB-S2-E2007-APP | DOR-RWB-S2-E2007-APP-7 | 11 | Add DF-ACC-009, DF-ACC-030, DF-ACC-031 and fields principal_outstanding, settlement_booked_date, settlement_booked_amount and decision_record, with the two further names from the detcheck, or align the story IDs. |
| CDC-15958 | RWB-S2-E2008-APP | DOR-RWB-S2-E2008-APP-11 | n/a (field not named) | Reclassify the personal-data flags on the rwb_treatment fields P2 names so they match AC7, which states no personal field is carried. |
| CDC-15996 | RWB-S2-E2008-APP | GAP-0927 | Header | Carry the filter and row count in the actions list of the decision-record entry; add capability area and right to that list in the next LDM version. |
| CDC-16030 | RWB-S2-E2017-APP | CG-ALL-8347 | 3, 12.7, 13 | Record decision_record as the PLT library object of rwb_treatment that DP-03 provides, read by reference DF-TRT-003 and never written. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15858 | RWB-S2-E2004-APP | GAP-3177 |  | Register the five-minute next-action Temporal Schedule in rwb-case. Remove EV-18 TimerDue from the Epic 2 contract tables in the story set. |
| CDC-15905 | RWB-S2-E2007-APP | CG-ALL-8302 | 12.5 | Add a Workflows row for `TreatmentWorkflow` (booking branch): stage child of CaseWorkflow, namespace rwb-recovery, task queue rwb-treatment, as named in RWB-S2-E2007-APP section 12.5. |
| CDC-15915 | RWB-S2-E2007-APP | CG-ALL-8303 | 12.5 | Add activity evaluateBookingMatch on task queue rwb-treatment to the Activities sheet. |
| CDC-15916 | RWB-S2-E2007-APP | CG-ALL-8304 | 12.5 | Add activity recordAndApply on task queue rwb-treatment to the Activities sheet. |
| CDC-15953 | RWB-S2-E2008-APP | CG-ALL-8327 | 12.5 | Add activity applyProceedsMatched to the catalog or use a catalogued activity. |
| CDC-15954 | RWB-S2-E2008-APP | CG-ALL-8328 | 12.5 | Add activity holdMissedInstallment to the catalog or use a catalogued activity. |
| CDC-15955 | RWB-S2-E2008-APP | CG-ALL-8329 | 12.5 | Add activity RecordAndApply to the catalog or use a catalogued activity. |
| CDC-15987 | RWB-S2-E2008-APP | GAP-2693 | 9, 12.4, 12.5 | Activity names in 12.4 and the plan-position row now read Not specified (GAP-2693; ASM-4452) |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15870 | RWB-S2-E2004-APP | CG-ALL-8276 | 18 | Align the test lists of the four requirements in section 18 with the RTM at its next version. |
| CDC-15896 | RWB-S2-E2006-APP | CG-ALL-8289 | 18 | Align the test lists for REQ-CHO-008, REQ-CHO-006 and the third requirement with section 18 of this story in the next RTM version. |
| CDC-15940 | RWB-S2-E2007-APP | CG-ALL-8309 | 18 | Align the REQ-CHO-008 test list to RWB-S2-E2007-APP section 18 (TC-E2-007-01, TC-E2-007-03, TC-E2-007-11, TC-S2-E2007-APP-01 to -10). |
| CDC-15959 | RWB-S2-E2008-APP | DOR-RWB-S2-E2008-APP-12 | 7, 12.7, 16, 18 | Align the §18 test lists of REQ-CHO-007 and REQ-CHO-009 with §16, which now carries TC-S2-E2008-APP-06 to -09. |
| CDC-15989 | RWB-S2-E2008-APP | CG-ALL-8331 | 18 | Align the test lists of REQ-CHO-007 and REQ-CHO-009 with RWB-S2-E2008-APP section 18 in the next RTM version. |
| CDC-16024 | RWB-S2-E2010-APP | CG-ALL-8342 | 18 | Align the REQ-RDF-014 and REQ-RDF-010 test lists in RTM v7 with section 18 of this story in its next version. |
| CDC-16044 | RWB-S2-E2017-APP | CG-ALL-8353 | 18 | Align the test lists of REQ-DCM-012, REQ-OCC-002 and REQ-OCC-009 with section 18 of RWB-S2-E2017-APP, which now lists TC-S2-E2017-APP-01 to -08 |

### RWB-P8-E2008-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15963 | RWB-S2-E2008-APP | GAP-2503 | find it | Declare the nine consumed operations on per-service bases with one hop and a 2 s timeout, and name the workflow matchPayments and its four activities. Record in the RTM that AC1, AC3, AC4 and AC5 of the legacy key are carried by no story of this split. |
| CDC-15968 | RWB-S2-E2008-APP | GAP-0601 | find it | Publish one row per payment_code ordered by paymentCode ascending, with unpaged reads and the row cap as configuration. Name the fold rule in the OpenAPI fragment. Route a confirmed duplicate payment_code to REC-05 of RWB-P1-E1011-APP. |
| CDC-15974 | RWB-S2-E2008-APP | GAP-1350 | not in chunk | Publish one OpenAPI 3.1 and one AsyncAPI document, problem+json on non-2xx, MatchRequest properties, next Flyway number, major version 1 with BACKWARD. |
| CDC-15984 | RWB-S2-E2008-APP | GAP-2494 |  | Fix one DecisionRecorded shape and consumer group, take decision codes from LOV-DECISION, carry inputs_ref as an opaque reference, keep the input age limit key as a DP-06 placeholder, publish the page default. |
| CDC-15985 | RWB-S2-E2008-APP | GAP-2504 |  | Publish v1 with the two operations, three event schemas, nine declarations, schema baseline and message map; mark unsettled elements with the placeholder and one review row. |
| CDC-15988 | RWB-S2-E2008-APP | GAP-1347 |  | Publish three event schemas with the data fields the legacy story names per event and the platform CloudEvents envelope; require a new schema version for any added business field. |
| CDC-15997 | RWB-S2-E2008-APP | GAP-1351 |  | Declare DecisionRecorded on rwb.decision-record.v1 as a produced event whose schema is rwb-decision's; rwb-decision owns the topic and ledger; publish only through RWB-PLT-E1027-CON (DP-03) |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15848 | RWB-S2-E2004-APP | CG-ALL-8273 | 4, 14 | Business analyst adds a new message ID for the no-package-in-force refusal, because the story use differs from the standard Raised when. |
| CDC-15919 | RWB-S2-E2007-APP | DOR-RWB-S2-E2007-APP-9 | 14 | Supply the text of MSG-P7-009 and align the texts of MSG-P2-011, MSG-P3-027 and MSG-P2-006 to the standard |
| CDC-15999 | RWB-S2-E2008-APP | GAP-1637 |  | Publish wording, Thai text, channel and blocking status for MSG-P8-001 and MSG-P8-002. Story keeps both IDs unchanged. |
| CDC-16007 | RWB-S2-E2010-APP | CG-ALL-8338 | 14 | Add a new message ID for 'A page or a size is out of range' with text '{field} is outside the accepted range {range}.'; then the story cites it. |
| CDC-16008 | RWB-S2-E2010-APP | CG-ALL-8339 | 14 | Add a new message ID for 'The caller is not signed in' with text 'Sign in to continue.'; then the story cites it. |
| CDC-16013 | RWB-S2-E2010-APP | DOR-RWB-S2-E2010-APP-9 | 14 | Restate the meanings of MSG-GEN-003 and MSG-P4-001 and the text of MSG-P4-003 as the standard v4 defines them |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15849 | RWB-S2-E2004-APP | CG-ALL-8275 | 16 | Add rows TC-S2-E2004-APP-01 to TC-S2-E2004-APP-10 with Given, When and Then copied from the criteria they cover. |
| CDC-15882 | RWB-S2-E2006-APP | CG-ALL-8287 | 16 | Add rows for TC-S2-E2006-APP-01 to TC-S2-E2006-APP-09 to tab Story test cases, with Given, When and Then copied from the criteria they cover |
| CDC-15917 | RWB-S2-E2007-APP | CG-ALL-8308 | 16 | Add Story test cases rows for TC-E2-007-11 and TC-S2-E2007-APP-01 to TC-S2-E2007-APP-10 in the next version, with Given, When and Then copied from the criteria they cover. |
| CDC-15956 | RWB-S2-E2008-APP | CG-ALL-8330 | 16 | Add rows for TC-S2-E2008-APP-01 to -05 with Given, When and Then copied from AC3 to AC7 of this story. |
| CDC-16009 | RWB-S2-E2010-APP | CG-ALL-8341 | 16 | Add rows TC-S2-E2010-APP-01 to TC-S2-E2010-APP-07 with Given, When and Then copied from the criterion each covers. |
| CDC-16031 | RWB-S2-E2017-APP | CG-ALL-8351 | 16 | Add rows for TC-S2-E2017-APP-01 to TC-S2-E2017-APP-04 with Given, When and Then copied from the criteria they cover. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15847 | RWB-S2-E2004-APP | CG-ALL-8272 | 12.4 | Add rwb-treatment as a consumer of rwb.case.CaseStateChanged.v1 (EV-05) and add its ACL entry. |
| CDC-15863 | RWB-S2-E2004-APP | GAP-0703 |  | Add rwb-case as a consumer of rwb.treatment.TreatmentApproved.v1 so the subscription is contractual. Confirm treatment state stays in rwb_treatment and not in rwb_case. |
| CDC-15899 | RWB-S2-E2006-APP | GAP-2483 | 7 | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision.events.v1 and the shared ledger topic, keyed by case id, and map it to the free identifier among EV-08, EV-09 and EV-30. |
| CDC-15938 | RWB-S2-E2007-APP | GAP-2487 |  | Name rwb.decision.BookingDecisionMade.v1 on rwb.decision.events.v1, keyed by treatmentId, carrying outcome, row, package code and version, business date and difference terms; leave TreatmentBooked, CaseStateChanged and posting with their owners. |
| CDC-15952 | RWB-S2-E2008-APP | CG-ALL-8322 | 12.4 | Add rwb-treatment as a consumer of rwb.payment.ProceedsMatched.v1 and add its ACL. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15840 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-14 |  | Record the signed epic design sign-off for RWB-S2-E2004-APP; none exists in the story or source documents. |
| CDC-15948 | RWB-S2-E2008-APP | DOR-RWB-S2-E2008-APP-14 | find it | Confirm the signed sign-off of the epic design and record it there, so the story can cite it. |
| CDC-16004 | RWB-S2-E2010-APP | DOR-RWB-S2-E2010-APP-14 | header | Confirm the signed epic design sign-off and record it in the epic design record. |
| CDC-16026 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-14 | header | Confirm the epic design sign-off and record it in the epic design record; no sign-off exists in the story or sources. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15845 | RWB-S2-E2004-APP | GAP-2474 | find it | Add GET /rule-catalog/{ruleId}?packageVersion= as a P7 row, and name the entry read as API-P7-007 of RWB-P7-E2005-APP. |
| CDC-15866 | RWB-S2-E2004-APP | GAP-1698 |  | Add rows for the contracts, settlement and deed-in-lieu agreements and plan timers of rwb_treatment, owner S2, as the four entity groups in Arch v5 slides 18 and 41. |
| CDC-15891 | RWB-S2-E2006-APP | GAP-2478 |  | Rule delegation_limit to rwb-access, publish the level read with its fake, and correct the DP-07 pattern row to name rwb-access. |
| CDC-15993 | RWB-S2-E2008-APP | GAP-1639 | Header | Name the two event-started workflows matchPayments and confirmBookings, register them on task queue rwb-payment, or confirm the activity alone is the unit. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15861 | RWB-S2-E2004-APP | GAP-0918 |  | Add API-P4-022 GET /doa-limits with the request and answer fields of the delegation lookup. Keep the outcome value set on the contract page. RWB-P4-E2013-APP consumes the same operation. |
| CDC-15892 | RWB-S2-E2006-APP | GAP-2479 |  | Add GET /api/recovery/access/v1/doa-limits with decisionCode, regulationItem, productGroup, amount, asOfDate; publish texts of MSG-P7-010, MSG-GEN-006 and MSG-P4-003. |
| CDC-15969 | RWB-S2-E2008-APP | GAP-0599 | not in chunk | Publish the two reads on /api/recovery/source-data/v1 with resource names, businessDate parameter, element names and the status set of legacy section 12.1. |
| CDC-15979 | RWB-S2-E2008-APP | GAP-1634 |  | Drop the uuid CROSS_REF account_payment_id and keep one varchar(255) business-key column for the ACE payment_code with no foreign key. |

### RWB-P2-E2007-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15908 | RWB-S2-E2007-APP | DOR-RWB-S2-E2007-APP-22 | header | Publish a contract fake library version for RWB-P2-E2007-CON and record it as published. |
| CDC-15933 | RWB-S2-E2007-APP | GAP-0598 | 4 | Answer the account read as account facts only, with no treatment term, outcome, difference, tolerance or package version; state that BookingMatchFacts is built by the calling slice; add a contract test failing on any outcome-shaped field. |
| CDC-15936 | RWB-S2-E2007-APP | GAP-0730 |  | Fix the rwb-case login in the platform DB story; publish the composite route, treatment booking fields and raiseTask result schema with RWB-P2-E2007-CON and the S2 contract. |
| CDC-15937 | RWB-S2-E2007-APP | GAP-2486 |  | Publish the operation set from the six legacy interfaces on the per-service base (DP-13) with one hop and 2 s timeout; take decision code and outcome values from LOV-DECISION; fix read filters, page size, ordering and MSG-GEN-006 text before SIT. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15851 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-12 | 12.7, 16, 18 | Test Cases v8 has no TC-S2-E2004-APP rows: add TC-S2-E2004-APP-01 to TC-S2-E2004-APP-15 as in section 16. RTM v7 rows REQ-CHO-006 and REQ-CHO-007 list only legacy TC-E2 IDs: add the section 18 S2 IDs. |
| CDC-16011 | RWB-S2-E2010-APP | DOR-RWB-S2-E2010-APP-12 | 12.7, 16, 18 | Add TC-S2-E2010-APP-01 to -09 to Test Cases v8; align the §18 test lists, including TC-08, with RTM v7 |
| CDC-16035 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-12 | 12.7, 16, 18 | Add TC-S2-E2017-APP-01 to -05 to tab Story test cases; align RTM v7 test lists with section 18 of this story. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15894 | RWB-S2-E2006-APP | GAP-2689 | 7 | Add the credit-result variant of the treatment PATCH with element names, If-Match and once-only rule at wave 2 freeze; add state check and four columns on Flyway. |
| CDC-15897 | RWB-S2-E2006-APP | GAP-2690 | 18 | Record the treatment operations and credit-result element set against rwb-treatment, and the level comparison against rwb-access, once P2 and P3 publish. |
| CDC-15898 | RWB-S2-E2006-APP | GAP-2482 | 7 | D5 identification and the approve/refuse mapping marked Not specified in the source documents (GAP-2482) |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15904 | RWB-S2-E2007-APP | CG-ALL-8300 | 13 | Create RWB-P7-E1073-CON or name the existing story that carries the rwb-decision rule-package contract for DP-04. |
| CDC-15906 | RWB-S2-E2007-APP | DOR-RWB-S2-E2007-APP-17 | header | Create or name the existing story for the RWB-P7-E1073-CON dependency (CG-ALL-8300). |
| CDC-15907 | RWB-S2-E2007-APP | DOR-RWB-S2-E2007-APP-21 | header | Create contract story RWB-S2-E2007-CON for the rwb-treatment operations of section 12.1, or confirm none is needed. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15910 | RWB-S2-E2007-APP | GAP-1696 | 11 | Rewrite FSD S2 A2.6.3.1, A2.13.2, A2.10.2 and A2.17.2 to read source facts through rwb-source-data; add S2 to the P1 REST cell of the Architecture v5 connection matrix. |
| CDC-15966 | RWB-S2-E2008-APP | GAP-1626 | find it | Restate the rwb-payment contract as GET /proceeds and POST /proceeds/{proceedsId}/match, the API Specification v4 pair. Confirm before the contract story closes. |
| CDC-15994 | RWB-S2-E2008-APP | GAP-0602 | 7 | Record GET /accounts/{id} of Architecture v5 slide 15 as unowned and unpublished; nextInstallmentDate stays on the installment-facts read. |

### RWB-P1-E2010-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16016 | RWB-S2-E2010-APP | GAP-0509 | none | Add the guarantee claim read and the case-existence answer as C dependencies, each with a fake |
| CDC-16017 | RWB-S2-E2010-APP | GAP-2695 | none | Name the changed-window and active-count reads as GET /treatments and GET /treatments/active-count on /api/recovery/treatment/v1; remove the P3 case-contract paths |
| CDC-16022 | RWB-S2-E2010-APP | GAP-2739 | Header | Keep the DP04 copy with rwb-source-data in rwb_source_data and the live claim with rwb-guarantee in rwb_guarantee; build against the fake of the claim read; record the wave difference as a dependency in the DP04 release note. |

### RWB-P5-E2017-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16028 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-22 | 12.8 | Record the published contract fake library version for RWB-P5-E2017-CON. |
| CDC-16042 | RWB-S2-E2017-APP | GAP-1278 | 7 | Publish the rwb.decision-record.v1 payload field set, the correction final call, the document set and value pair reference shapes, the two parameter names and the MSG-P4-003 message id. |
| CDC-16046 | RWB-S2-E2017-APP | GAP-1017 | find it | Declare the seven operations on /api/recovery/document/v1, the send path of section 13 with API-P6-009 consumed, and the request and answer field names as the proposed fix of GAP-1017 states |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15864 | RWB-S2-E2004-APP | GAP-1341 |  | Record the legacy TimerScheduler and JOB-05 wording as superseded by Architecture v5 slides 42 and 44. Plan timers stay durable timers; no Schedule or TimerDue topic. |
| CDC-15931 | RWB-S2-E2007-APP | GAP-2485 | 4 | Record that BOOKING_MATCH is evaluated on the version held, through the embedded kit (DP-04), and restate the RWB-P7-E2042-APP boundary once. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15929 | RWB-S2-E2007-APP | GAP-0923 |  | Extend T6.1 with Case record and Treatment and offer columns: CASE_RECORD R and U, TREATMENT_AND_OFFER R for RW-RESTRUCT and RW-CREDITAD, confirmed with the matrix owner. |
| CDC-15970 | RWB-S2-E2008-APP | GAP-0926 | not in chunk | Publish the permission letters of all 14 LOV-CAPABILITY areas per role, with each role's default scope. |

### RWB-S2-E2010-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16005 | RWB-S2-E2010-APP | DOR-RWB-S2-E2010-APP-21 | header | Status changed from Resolved to Cross-document. |
| CDC-16019 | RWB-S2-E2010-APP | GAP-0512 | 4 | Publish the DP04 record and guarantee claim read property names from the legacy RWB-E2-010 data rows and API Specification v4; leave required flags and lengths to baseline review; fake the guarantee claim read. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16025 | RWB-S2-E2017-APP | CG-ALL-8348 | 12.2 | Publish GET /api/recovery/document/v1/cases/{caseId}/generated-documents?treatmentId={treatmentId} through RWB-P5-E2017-CON, or agree a published operation to consume. |
| CDC-16029 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-8 | 12.2, 12.5 | Publish the GET generated-documents?treatmentId operation through RWB-P5-E2017-CON (P1 path item). |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16043 | RWB-S2-E2017-APP | GAP-0401 | 7 | Publish the gateway-bff composite route path for SCR-14 and SCR-30 and the merge order; agree with QA the wave 2 harness repository, environment, seeding, evidence format and pass/fail gate. |
| CDC-16047 | RWB-S2-E2017-APP | GAP-0944 | find it | Publish the composite route field list for SCR-14 and SCR-30 with the gateway-bff contract, and add the allowed-action decision code to the decision-code list before the audit query is built |

### RWB-S2-E2004-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15841 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-21 |  | Create contract story RWB-S2-E2004-CON, then add it as a contract dependency in this story's header. |

### OTHER:Contract fake library (published fakes register) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15842 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-22 | 12.8 | Record the rwb-case contract fake (case-signal fake) and its library version as published. |

### RWB-P3-E2004-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15843 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-23 | header | Placeholder row Contract version added to the header |

### OTHER:Screen specifications (SCR-03; OTHER:SCR-09; OTHER:SCR-14) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15850 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-10 | 15 | Empty, loading, error and no-access states marked Not specified in section 15; no state written |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; OTHER:BA for MSG-P3-027 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15853 | RWB-S2-E2004-APP | DOR-RWB-S2-E2004-APP-9 | 14 | MSG-P4-003 aligned to v4 text; MSG-P3-027 reverted |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15854 | RWB-S2-E2004-APP | GAP-2404 | find it | Read H as None plus the five platform contracts; read C as RWB-P10-E2032-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and the P4 authorise contract. Platform contracts stay Day 1 prerequisites. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15855 | RWB-S2-E2004-APP | GAP-2395 | find it | Use the three Epic 2 package codes and version labels as the fixture set. Attach no rwb-comms notice to a package by assumption. Settle rwb-comms package assignment with the rule registry owner before integration. |

### OTHER:FSD S2 and the rwb-treatment service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15856 | RWB-S2-E2004-APP | GAP-1713 | find it | Record once in the service contract the owning contract for each feature-code prerequisite. Carry the duplicate FEAT-CHO-08 as written. |

### OTHER:RWB-E2-008 application slice (rwb-payment story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15857 | RWB-S2-E2004-APP | GAP-2503 | find it | Declare the nine consumed operations with one hop and 2 s timeout. Name workflow matchPayments with its four activities. Record in the RTM that legacy AC1, AC3, AC4 and AC5 are carried by no story. |

### OTHER:rwb-case OpenAPI file for GET /cases/{caseId}/timers (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15859 | RWB-S2-E2004-APP | GAP-0705 |  | Fix the plan-timer properties treatmentId, timerType, startedAt, expiresAt, warnAt, paused and status, all optional in major version 1, with expiresAt as an offset date-time. |

### RWB-P4-E1037-CON; RWB-P4-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15860 | RWB-S2-E2004-APP | GAP-0917 |  | Freeze the POST /authorise request and answer at contract review. Load the two capability areas into the policy pack as RWB-P4-AD002-APP rows. Name the rwb-access login with DP-02. |

### OTHER:Wave 2 integration harness pack (QA and integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15862 | RWB-S2-E2004-APP | GAP-0389 |  | Agree the harness repository, environments, seed files, business clock, evidence report, pass/fail gate and gateway-bff composite route before the first SIT run. |

### RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15865 | RWB-S2-E2004-APP | GAP-2473 |  | Publish the catalogue answer element names and media type, the decision record fields, the text of MSG-P7-009, the system actor value and the four registry table columns. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15867 | RWB-S2-E2004-APP | GAP-1709 |  | State in the release slicing that the contract and treatment record with its data date ship in wave 2 and the offer, settlement, plan and deed in lieu capabilities ship with E3. |

### OTHER:Data architect (physical field list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15868 | RWB-S2-E2004-APP | GAP-1712 | 1 | Invented storage sentence removed from section 1 |

### RWB-P7-E1073-CON; RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15869 | RWB-S2-E2004-APP | GAP-1339 |  | Fix the model and catalogue answer shape and the DecisionRecorded envelope field names; add MSG-P7-009 and MSG-P7-012 to the P7 message table from the Error and Message Standard. |

### OTHER:rwb-case deployment values files (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15871 | RWB-S2-E2004-APP | GAP-0706 | None | Add provisional default values for the plan-timer projection lag, subscription lag, .dlt count, exception-queue count and DP04 freshness; confirm at UAT with the service owner and platform observability owner. |

### OTHER:gateway-bff route catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15872 | RWB-S2-E2004-APP | GAP-0920 | None | Publish the SCR-14 treatment record and SCR-03 timer panel composite routes with their field lists and confirm no personal field is on either. |

### OTHER:Platform DB story of DP-02 (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15873 | RWB-S2-E2004-APP | GAP-0921 | None | Fix the login name, grants and schema owner for rwb-access and each service schema in the platform DB story; P4 stories reference it. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md; RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15874 | RWB-S2-E2004-APP | GAP-2476 | None | Record how a running INSTALLMENT_DUE or CURE_PERIOD timer is carried into the workflow owning the wait at cut-over; remove legacy steps 7 and 14 and AC2, AC12, AC14 from the target test set. |

### OTHER:rwb-treatment service contract document (major version 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15875 | RWB-S2-E2004-APP | GAP-2688 | None | Name the parameters and reference-data operations consumed, the member-level types and lengths of the TreatmentApproved payload, and the fake set. |

### OTHER:Screen specification for SCR-14 (document not named in the source) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15883 | RWB-S2-E2006-APP | DOR-RWB-S2-E2006-APP-10 | 11 | Add the empty, loading, error and no-access states of SCR-14 |

### OTHER:Service contract of rwb-treatment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15885 | RWB-S2-E2006-APP | GAP-1713 |  | Record once the mapping of the feature-code prerequisites to owning service contracts: approval to P7, case to P3, documents to P5, communications to P6, valuation to S1; keep duplicate FEAT-CHO-08. |

### RWB-ITG-E2006-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15886 | RWB-S2-E2006-APP | GAP-1344 |  | Correct attribution of delegation_limit to P4 rwb-access in the ITG story; add DoA limit read to Ownership Map API catalogue with P4 owner and P7, P3, P2 consumers. |

### OTHER:Credit approval pack integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15887 | RWB-S2-E2006-APP | GAP-0394 |  | Record composite credit-pack route and merge order, harness environment and repository, seed data, evidence format and retention, and pass/fail gate at wave 2 entry check. |

### RWB-P2-E2006-APP; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15888 | RWB-S2-E2006-APP | GAP-0663 |  | Settle rwb-integration login, contract field names, NLEADS read operations, ownership split, resource placement and approval-level values against doa.txt item 2.1.1 in wave 2 contract review. |

### RWB-P3-E2006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15889 | RWB-S2-E2006-APP | GAP-0729 |  | Agree rwb-case login, SCR-14 composite route, NLEADS credit-decision read, treatment result fields and AC2/AC7 approval levels against doa.txt item 2.1.1 before wave 2 build. |

### RWB-P7-E2006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15890 | RWB-S2-E2006-APP | GAP-1342 |  | Settle rwb-decision login, decide path, ApprovalAction and DecisionLogEntry fields, delegation read shape, single level-comparison owner and actions key names in the wave 2 contract review. |

### OTHER:Decision-record schema document (TSD P7 T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15893 | RWB-S2-E2006-APP | GAP-2480 |  | Fix D5 actions keys requiredLevel, delegationLimitId, limitVersion, nleadsRef, resultDate; take inputs_ref from the pack read reference; confirm NLEADS reference pattern with SCB IT. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15895 | RWB-S2-E2006-APP | GAP-1343 | header | Publish the six DP-added dependencies with this story as consumer; confirm RWB-P4-E1037-CON as contract dependency at wave 2 contract review. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15900 | RWB-S2-E2006-APP | GAP-2484 | find it | Give GET /cases/{caseId}/recommendation to the P7 story serving the decision screen; treat the four platform contracts as published before Day 1. Story metadata rows unchanged. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15920 | RWB-S2-E2007-APP | GAP-3175 | find it | List AceDataReady (EV-26) as the target event name on rwb.source-data.events.v1, with LoadCompleted as its legacy alias |

### RWB-P6-E1073-APP; OTHER:RWB-E2-042 section 2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15921 | RWB-S2-E2007-APP | GAP-2395 | find it | Settle the rwb-comms rule package with the rule registry owner and read the three Epic 2 package codes as the fixture set; invent no fourth code |

### OTHER:Functional Specification S2 (A1.1 and A2 prerequisites) and the service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15922 | RWB-S2-E2007-APP | GAP-1713 | find it | Map each prerequisite feature code to the contract of its owning service once, carrying the duplicate FEAT-CHO-08 as written |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:41; OTHER:44) and FSD S2 A2.10; OTHER:A2.11; OTHER:A2.17 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15923 | RWB-S2-E2007-APP | GAP-1703 | find it | Let rwb-payment own booking, matching and posting, with TreatmentBooked and PaymentMissed as inputs; the release request leaves through the integration contract |

### RWB-P2-E2007-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:TSD P2 Integration v3; OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15924 | RWB-S2-E2007-APP | GAP-0657 | find it | Apply the app-slice fixes as the proposed fix states, with the six consumed paths and the rwb-integration login in their owner documents |

### RWB-P2-E2007-CON; OTHER:TSD P1 v3 and Section B notes (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15925 | RWB-S2-E2007-APP | GAP-0596 | 3 | Publish fieldState AVAILABLE or NOT_AVAILABLE per field with no value on NOT_AVAILABLE, and name the flag rwb.dataengine.booking-facts |

### RWB-P2-E2007-CON; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15926 | RWB-S2-E2007-APP | GAP-0597 | 12, 12.1 | Publish GET /batch-status with key pair sourceSystem and businessDate and six values; answer 404 with MSG-P1-001 when no batch row exists |

### RWB-P2-E2007-CON; RWB-P1-E2007-APP; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15927 | RWB-S2-E2007-APP | GAP-0594 | 11, 12 | Publish GET /booking-facts and GET /batch-status on /api/recovery/source-data/v1 with BookingFact, BookingFactsAnswer, FieldState and BatchStatusAnswer |

### RWB-P2-E2007-CON; RWB-P3-E1018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15928 | RWB-S2-E2007-APP | GAP-0595 | 4 | Declare the case account set source in RWB-P2-E2007-CON: the case list row, or the case accounts operation if RWB-P3-E1018-CON is added |

### OTHER:TSD P4 appendix T-A; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15930 | RWB-S2-E2007-APP | GAP-0922 |  | Add POST /authorise with request and answer schema; stub it in the contract fake; fix the rwb-access login in the platform DB story; publish the composite route with gateway-bff (DP-19). |

### OTHER:Booking confirmation harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15932 | RWB-S2-E2007-APP | GAP-0395 |  | Record the composite route path and merge order (agreed with the platform edge story), harness environment, ALS booking fixture format, seed pack, evidence format, retention and pass/fail gate at the wave 2 entry check. |

### RWB-P2-E2007-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15934 | RWB-S2-E2007-APP | GAP-0658 |  | Baseline result shape, task table, envelope, rerun operation, twelve consumed operations and seven fakes; record JOB-08 ownership and the TSD P2 v3 T5.2 supersession; confirm seven message texts. |

### RWB-P2-E2007-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15935 | RWB-S2-E2007-APP | GAP-0659 |  | Fix rwb-integration login, secret reference and probe checks; register JOB-08 on rwb-integration and record the owner conflict; take thresholds, series windows and backfill limit as environment values; write the JOB-08 catalogue row with run book path; review four runbook entries with the on-call rota. |

### RWB-S2-E3001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15939 | RWB-S2-E2007-APP | GAP-2691 | 12.5 | Add the approved-not-booked read, the mark-booked write and the booking-difference write with their element names at the wave 2 contract freeze; add APPROVED and BOOKED to the state check constraint. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15941 | RWB-S2-E2007-APP | GAP-0924 | 7, 16 | Add a cache-lifetime parameter key with its value agreed at the wave 2 design review (key name: Not specified in the source documents (GAP-0924)). |

### OTHER:ACE platform secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15942 | RWB-S2-E2007-APP | GAP-2489 | 9 | Allocate the rwb-decision login for schema rwb_decision and record it in the platform secret store. |

### RWB-P2-E2007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15943 | RWB-S2-E2007-APP | GAP-2491 | 4 | State the JOB-08 run as: event-started BookingConfirmationWorkflow on queue rwb-decision at Asia/Bangkok, one run per business date, second start refused with MSG-P2-006, failed gate retried on next AceDataReady for the date, no fallback Schedule, flag off stops the start while written records stay readable. |

### OTHER:TSD P7 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15944 | RWB-S2-E2007-APP | GAP-2492 | 16 | Create no reconciliation_result table in rwb_decision; publish each decision and its outcome; serve counts from decision_log_entry on the read of 12.1; rwb-reporting builds the REC-03 break list from events with field IDs carried as values. |

### parameter-catalog.csv; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15945 | RWB-S2-E2007-APP | GAP-2692 | 16 | Add booking.missing.grace_loads and the treatment-type and outcome list codes to the parameter and reference-data registers; record TreatmentBooked ownership against rwb-payment in the event catalogue; record the parent stage outcome contract in the rwb-case baseline. |

### OTHER:Contract story for RWB-S2-E2008 (not yet in the set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15949 | RWB-S2-E2008-APP | DOR-RWB-S2-E2008-APP-21 | header | Removed the unknown key RWB-S2-E2008-CON from Contract dependencies |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15950 | RWB-S2-E2008-APP | DOR-RWB-S2-E2008-APP-8 | 12.4 | Add GET and PATCH /treatments/{treatmentId} (API-S2-002, API-S2-003) to rwb-treatment.yaml; confirm topic of rwb.payment.ProceedsMatched.v1; add rwb-treatment as consumer. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15961 | RWB-S2-E2008-APP | GAP-3175 | find it | List LoadCompleted as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1, keeping AceDataReady as the target name. |

### OTHER:FSD P6 v3; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15962 | RWB-S2-E2008-APP | GAP-2395 | find it | Name the rule package of rwb-comms and the package codes it reads once the rule registry owner settles the assignment. No fourth code is invented. |

### OTHER:FSD S2 v3 (A2.10; OTHER:A2.11; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15964 | RWB-S2-E2008-APP | GAP-1703 | find it | Remove booking, payment matching and posting from the A2.10, A2.11 and A2.17 writes. Record the booking reference from TreatmentBooked and the break from PaymentMissed. Route the release request through the integration contract. |

### OTHER:FSD P8 v3 (A2.3.4.1 to A2.11.4.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15965 | RWB-S2-E2008-APP | GAP-1625 | find it | Replace the placeholder AC-P8-003-01 to AC-P8-011-01 with testable main-flow criteria drawn from the feature statement, rules and field list, and mark them as new. |

### OTHER:FSD P8 v3 and TSD P8 v2 T5.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15967 | RWB-S2-E2008-APP | GAP-1631 | find it | Read ALS through rwb-source-data, deliver ledger postings through rwb-integration, and mark the ATS, AMIS and LED routes as outside the 19 services until an interface is named. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15971 | RWB-S2-E2008-APP | GAP-0925 | not in chunk | Extend the authorise envelope with area, right, scope, resource, filter, rowCount and matrixVersion, and fix the three answer codes. |

### RWB-ITG-E2008-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15972 | RWB-S2-E2008-APP | GAP-0393 |  | Record the composite proceeds and exception route path, merge order, harness environment, ALS payment fixture format, seed pack, evidence format and retention, and pass or fail gate at the wave 2 entry check. Not specified in the source documents (GAP-0393) |

### RWB-P8-E2008-APP; OTHER:AC-EXC-P8-002-02) and rwb-source-data break list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15977 | RWB-S2-E2008-APP | GAP-1627 | not in chunk | Record the orphan as a break row with check name References; write no quality exception table in rwb_payment. Data steward confirms the check name. |

### OTHER:FSD P8 v3 feature overview (FEAT-PAY-06) and Epics 3 to 8 BRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15978 | RWB-S2-E2008-APP | GAP-1629 | not in chunk | Move booking confirmation to wave 2 with EP03, and keep the proceeds features in wave 3. |

### OTHER:NFR Specification v3 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15982 | RWB-S2-E2008-APP | GAP-1643 |  | State a receipts-per-business-date figure derived from the observed receipt-to-installment ratio on ACE data for a busy month; use the ratio as an assumption until then. |

### OTHER:FSD P8 v3 (Requirements served) and TSD P8 v2 (T8 Requirement traceability) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15992 | RWB-S2-E2008-APP | GAP-1624 | 18 | Fill both tables with the REQ IDs served, or state that P8 has no requirement ID of its own, with FEAT and AC IDs traced per product requirement. |

### RWB-P8-E2008-APP; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15995 | RWB-S2-E2008-APP | GAP-0603 | Header | Record the payment-matching run as caller with a workload identity token and settle the P8 to P1 step as one REST hop; correct the activity description in the catalog. |

### OTHER:Work Package plan generator (B-P1-08; OTHER:B2-P1-014) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16000 | RWB-S2-E2008-APP | GAP-2180 |  | Keep one Work Package per story slice; drop B2-P1-014 or drop RWB-E2-008 from B-P1-08 fanout; add a plan-uniqueness check for 'Write only' blocks. |

### OTHER:FSD P7 v3 (dry-run operation of rule-package version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16001 | RWB-S2-E2008-APP | GAP-2495 |  | Publish the dry run as a read-only operation returning testResult (total, passed, failed, failing IDs), per-case expected and actual, and recorded dry-run counts. |

### OTHER:Program BRD v5 section 11 note (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16002 | RWB-S2-E2008-APP | GAP-1641 |  | Add section 5.11 (REQ-S4-010) to the P8 requirements note in the next version. Story cites REQ-S4-010 once its section text is in scope. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16003 | RWB-S2-E2008-APP | GAP-1349 |  | Publish a home for GET /cases/{id}/payments or answer it through GET /proceeds with case scope; leave SCR-28 field lists with RWB-PLT-N001-CON. |

### OTHER:contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16006 | RWB-S2-E2010-APP | DOR-RWB-S2-E2010-APP-22 | 12.8 | Publish the contract fake for rwb-case, name it in section 12.8, and record its published library version. |

### OTHER:gateway-bff story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16010 | RWB-S2-E2010-APP | DOR-RWB-S2-E2010-APP-10 | header | Add empty, loading, error and no-access states for SCR-03, SCR-14 and SCR-45, as these screens are composed by gateway-bff. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16012 | RWB-S2-E2010-APP | DOR-RWB-S2-E2010-APP-18 | 8, 18 | Status changed from Resolved to Cross-document. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16014 | RWB-S2-E2010-APP | GAP-3176 | none | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points |

### OTHER:Register gap log, row 121 (GAP-3194) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16015 | RWB-S2-E2010-APP | GAP-3194 | 12.7 | Raise an ACE DB story for the S2 rwb-treatment column drop, or attach it to the creating APP story, and cite the chosen story on row 121 before wave 2 |

### OTHER:DP04 harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16018 | RWB-S2-E2010-APP | GAP-0392 | 4 | Agree the composite DP04 route path and merge order with the platform edge story, and the harness environment, seed pack, evidence format, retention and pass or fail gate, at the wave 2 entry check; record the result before the first real-service run. |

### OTHER:Parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16020 | RWB-S2-E2010-APP | GAP-2696 | 4 | Hold the active treatment states as a parameter row of the parameters contract; the two operations and the reference-data read path are now in section 4 steps 1, 2, 6 and 8. |

### RWB-P1-E2010-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16021 | RWB-S2-E2010-APP | GAP-2738 | 4 | Publish GET /api/recovery/guarantee/v1/guarantee-claims?changedFrom=&changedTo=&page=&size= with items, window, page, size and scope-filtered total, ordered by updated_at and id, a declared maximum size, 400 on empty or inverted window, and a fake answering an empty list and an error. |

### RWB-S3-E2010-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16023 | RWB-S2-E2010-APP | GAP-2740 | 4 | Answer every claim in the window with its case_id and resolve nothing in the claim read; References check, break list and retry stay with RWB-P1-E2010-APP; add a case-existence consumed contract only if the data steward asks. |

### OTHER:Recovery Workbench work package list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16027 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-21 | header | Record RWB-P5-E2017-CON as the published contract for this story; create RWB-S2-E2017-CON only if the work package list adds it. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16032 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-1 | 1 | Add restructuring officer (FCR) as the role name of role code RW-RESTRUCT, the code section 10 already uses. |

### RWB-S2-E2017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16033 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-10 | 1 | Add empty, loading, error and no access states to SCR-30 in its owning document. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16034 | RWB-S2-E2017-APP | DOR-RWB-S2-E2017-APP-11 | 11 | Confirm the section 11 identifier fields (case_id, treatment id, decision code) carry no personal data, or correct the classification to match the No personal data statement. |

### OTHER:TSD P4 T6.1 RBAC matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16037 | RWB-S2-E2017-APP | GAP-0942 | 16 | Add a Documents column: CRU for RW-RESTRUCT and RW-CASEOWN, R for RW-TEAMMGR, CRUA for RW-LEGAL; confirm with matrix owner; publish in PM-2026.12 pack via RWB-P4-AD002-APP. |

### OTHER:rwb-treatment service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16038 | RWB-S2-E2017-APP | GAP-1713 | 5 | Record once the mapping of each FEAT prerequisite to its owning service contract (P7 approval, P3 case, P5 documents, P6 communications, S1 valuation); carry duplicate FEAT-CHO-08 as written. |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16039 | RWB-S2-E2017-APP | GAP-1580 | header | Add a generation section for REQ-DCM-012 stating the behaviour of POST /cases/{caseId}/generated-documents and POST /documents/{documentId}/regenerate, with FR-P5-026 and AC-P5-019. |

### OTHER:TSD P6 v2 (T-A.2; RWB-P6-E1046-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16040 | RWB-S2-E2017-APP | GAP-2392 | 7 | Add treatment-type and product-group filters to API-P6-003; add application/json to API-P6-005; add locked attribute to merge_field; publish set rows as rwb-case reference data under RWB-P3-E1043-CON; copy five message texts when issued. |

### OTHER:TSD P4 appendix T-A and T6.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16041 | RWB-S2-E2017-APP | GAP-0941 | 7 | Publish the authorise path with request and answer schema in the API specification and appendix T-A; carry it on RWB-P4-E1037-CON and stub it; fix the rwb-access login; state the service identity scope rule in T6.2. |

### OTHER:Functional Specification Document S2 (A2.18.2; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16045 | RWB-S2-E2017-APP | GAP-1704 | find it | Replace 'the Workbench document hub' with the P5 and P6 contract operations for generation, review and signature, and hold the document reference on the treatment |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0066 | Wave conflict S3 / EP02 | Tech lead | Resolved (directive) |
| GAP-0389 | The harness repository, environments, seeding, business clock, evidence format and retention, pass/fail gate and the gateway-bff composite case-record route are not defined in the source documents | Integration lead | Resolved (directive) |
| GAP-0392 | DP04 integration harness: composite record route, environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0393 | Payment matching integration harness: composite proceeds and exception route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0394 | Credit approval pack integration harness: composite credit-pack route, harness environment, seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0395 | Booking confirmation integration harness: composite booking and treatment route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0509 | The guarantee claim read of rwb-guarantee and the case-existence answer are not in the Work Package's contract list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0510 | The workflow and activity names of the stage 2 build are a target design choice | Solution architect | Resolved (directive) |
| GAP-0511 | The expected-by time of DP04 is assumed from the decision log and stated by no source | Data steward | Resolved (directive) |
| GAP-0512 | The field-level DP04 record schema and the shape of the guarantee claim read are not specified | Tech lead | Resolved (directive) |
| GAP-0513 | No deployment value, threshold, probe timing or fixture owner exists for the stage 2 build | DevOps lead | Resolved (directive) |
| GAP-0594 | The shapes and property names of the two booking-fact reads are in no source document | Tech lead | Resolved (directive) |
| GAP-0595 | The case's account set and its product group have no P1 read in the target | Solution architect | Resolved (directive) |
| GAP-0596 | How the read answers the three Section B columns, and which flag holds it back, is stated nowhere | Data architect | Resolved (directive) |
| GAP-0597 | The batch-status answer has two values in the legacy interface and nine fields in the view, and no source fixes which of them it returns | Tech lead | Resolved (directive) |
| GAP-0598 | No source says where the account read ends and the built match facts begin | Solution architect | Resolved (directive) |
| GAP-0599 | The two read operations, their resource and element names and their error status set are stated by no source, because the legacy read was an in-process Java interface with no path, no query parameter and no status code | Solution architect with the P8 contract owner | Resolved (directive) |
| GAP-0601 | The order of the payment answer, the fold of a repeated payment_code, the row cap of one call and the number of ALS payments per business date are stated by no source | Tech lead with the P8 contract owner | Resolved (directive) |
| GAP-0602 | Architecture v5 slide 15 names a GET /accounts/{id} of rwb-source-data that TSD P1 T-A.1 does not carry and no Work Package owns, while this story answers nextInstallmentDate | Solution architect with the P1 tech lead | Resolved (directive) |
| GAP-0603 | The caller of both reads has no actor of record after the data-load actor was retired, and the architecture names the P8 to P1 call as a Temporal activity while the Work Package fixes one REST hop | Solution architect with the P8 tech lead and the P4 owner | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0658 | rwb-integration booking confirmation (contract slice): the JOB-08 ownership and consumer lists, the ACE read boundary, the rerun placement and the twelve consumed shapes are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0659 | rwb-integration booking confirmation (deployment slice): the login and secret reference, the JOB-08 ownership, the alert thresholds, the runbook ownership and the backfill limit are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner; business on-call owner for the package alerts | Resolved (directive) |
| GAP-0663 | rwb-integration credit approval pack: login, contract field names, NLEADS read, the ownership split, the integration-base resource placement and the approval-level values are not settled by any one source | Solution architect | Resolved (directive) |
| GAP-0703 | The treatment entity moves to S2 while the legacy story holds it in P3, and the case side consumes TreatmentApproved which the event catalogue does not list for rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0705 | No source fixes the plan-timer fields, types or required flags of the timers answer behind GET /cases/{caseId}/timers | Tech lead of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0706 | No source gives the alert values for the plan-timer projection, the subscription lag, the DP04 freshness or the exception-queue count | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0729 | rwb-case credit approval: login, edge route and the NLEADS and treatment contract shapes are not specified | TechX | Resolved (directive) |
| GAP-0730 | rwb-case booking confirmation: login, composite route, treatment booking fields, match-result shape and route-rule evaluator owner are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0917 | rwb-access treatment and plan-timer slice: the authorise request and answer, the Treatment and offer and Case record letters and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0918 | The delegation lookup GET /doa-limits and its request and answer fields exist only on Architecture v5 slide 14, not in the TSD P4 appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0920 | The composite route field list for SCR-14 Treatment record and the SCR-03 timer panel is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0921 | The per-service login of rwb-access is named by DP-02 and by no document | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0922 | rwb-access booking confirmation: the authorise request and answer shapes, the contract entry of the authorise path and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0923 | rwb-access booking confirmation: the TSD RBAC matrix has no Case record column, so the CASE_RECORD R and U letters the booking tasks need are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0924 | rwb-access booking confirmation: the lifetime of a cached authorise decision is not specified | Solution architect | Resolved (directive) |
| GAP-0925 | POST /authorise request and response shape is not specified for the payment-matching reads | Solution architect | Resolved (directive) |
| GAP-0926 | Permission letters for WRITE_OFF_AND_POSTING and TREATMENT_AND_OFFER and the scope of the Credit Administration role are absent from the RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0927 | The field that carries the filter and the row count in an AC-READ or AC-DENY entry is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0941 | rwb-access document set: the authorise request and answer shape for the document screens, and the scope a service identity is asked for, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0944 | rwb-access document set: the composite route field list of SCR-14 and SCR-30, and the decision code of an allowed screen action entry, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1017 | The generation-screens baseline fixes six operations and four shapes that no source names, two conflicting legacy paths, the field names of the request and answer objects, and a status mapping the legacy section 12 states only in prose | Tech lead of rwb-document, with the solution architect and the rwb-comms owner | Resolved (directive) |
| GAP-1278 | The record payload, the reference shapes and the correction final call of the RWB-E2-017 decision slice have no source | Solution architect | Resolved (directive) |
| GAP-1339 | Values of the RESTRUCTURE catalogue and plan-timer ledger slice that no source fixes | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1341 | TimerDue and the five-minute JOB-05 check are retired in the target but kept by the legacy story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1342 | rwb-decision credit approval slice: the decide path, the delegation answer shape, the actions keys, the comparison site, the message texts, the decision sub-code, the per-service login and the screen identity are not fixed by any one source | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1344 | The delegation of authority table is ruled to rwb-access by the Ownership Map while the integration story of this key attributes the required level to rwb-decision | Solution architect | Resolved (directive) |
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1347 | RWB-E2-008: the three event payloads and the decision-record element are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1348 | RWB-E2-008: the proceeds field set and its idempotency tables disagree between the legacy story and TSD P8 T3.1 | Solution architect | Resolved (directive) |
| GAP-1349 | RWB-E2-008: the case payment read, the SCR-28 and run-view field lists and the activity names of JOB-07 are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1350 | RWB-E2-008: the contract artefact names, the problem+json body, the MatchRequest shape and the registry mode of rwb-payment are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1351 | RWB-E2-008: the producer and the owner of DecisionRecorded disagree between the event catalogue and the messaging design | Solution architect | Resolved (directive) |
| GAP-1352 | RWB-E2-008: the deployment targets, the tier sizes, the rollout strategy and the rollback procedure of rwb-payment have no source | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1353 | RWB-E2-008: no source fixes a numeric target for the outbox-lag, dead-letter or workflow-failure alerts of rwb-payment | Platform administrator | Resolved (directive) |
| GAP-1354 | Legacy AC1, AC3, AC4 and AC5 of RWB-E2-008 are owned by no story in this split | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1580 | Document generation REQ-DCM-012 has no FSD P5 feature section | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1624 | FSD P8 issues no requirement ID, so the product requirement cannot be traced to an FSD requirement | Business analyst, P8 | Resolved (directive) |
| GAP-1625 | Eight of the eleven P8 features carry a placeholder acceptance criterion instead of a testable one | Business analyst, P8 | Resolved (directive) |
| GAP-1626 | The two operations named in Architecture v5 slide 17 are not the two operations in the API Specification and the Ownership Map | Solution architect | Resolved (directive) |
| GAP-1627 | The data quality exception list that holds an unmatched payment has no home in v5 | Data architect | Resolved (directive) |
| GAP-1629 | Settlement booking confirmation is Epic 3 work in the BRD and Epic 4 work in the FSD | Solution architect | Resolved (directive) |
| GAP-1631 | The FSD names ALS, GL, ATS and AMIS as interface points, and v5 lets no service call a system of record | Solution architect | Resolved (directive) |
| GAP-1634 | The proceeds record names the ACE payment twice, once as a uuid cross-reference and once as a business key | Data architect | Resolved (directive) |
| GAP-1635 | The daily money reconciliation compares to a ledger position the Workbench does not receive | Reconciliation officer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1637 | The two run messages of this module have no wording in the message standard | Business analyst, P8 | Resolved (directive) |
| GAP-1639 | The two event-started workflows have no name or identifier in any v5 source | Solution architect | Resolved (directive) |
| GAP-1640 | Payment received is a named same-day trigger under DL06 and the matching run is once per business date | Solution architect | Resolved (directive) |
| GAP-1641 | The program BRD note on P8 requirements leaves out the enforcement proceeds requirement it also cites | Business analyst, P8 | Resolved (directive) |
| GAP-1643 | No receipt volume is stated for the volume test of this service | Solution architect | Resolved (directive) |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1698 | The Ownership Map lists one table for rwb-treatment, although Architecture v5 gives it four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1709 | The service is wave 2 and EP02 while every requirement of the module is an Epic 3 requirement | Solution architect | Resolved (directive) |
| GAP-1712 | The field catalog covers eight fields and none of them describes a contract, an agreement, a plan timer or a booking | Data architect | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1716 | The treatment record exists twice: as this service's live record and as P1's dated copy | Data architect | Resolved (directive) |
| GAP-2180 | Two Work Packages of the same stage write the same story file for RWB-P1-E2008-APP | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2392 | The catalog answer, the locked attribute, the set rows and five message texts are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2473 | RWB-P7-E2004-APP: the wire shape of the rule-catalogue answer, the payload fields of the plan-timer decision record, the text of MSG-P7-009, the ledger writer identity and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2474 | RWB-P7-E2004-APP: the rule-catalogue read that two stories consume is attributed to no owner in the Ownership Map, while the entry read the same map attributes to this service is served by RWB-P7-E2005-APP | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2476 | RWB-P7-E2004-APP: the legacy plan timers run on the Quartz timer check and publish a timer-due event, both retired in the target, and no source says what happens to a plan timer already running at cut-over | Solution architect with the rwb-case service owner and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2478 | delegation_limit has no owner in the P7 rows, and three sources name three different homes for the level | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2479 | The delegation read of rwb-access has no named path, request, answer or message text | P4 and P7 contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2480 | The field set of a D5 credit entry and the format of the NLEADS reference are not specified | P7 solution architect and the ledger owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2481 | The legacy story requires the Treatment and offer right while the endpoint of this service declares the Decision log right | P4 access owner and the P7 solution architect | Resolved (directive) |
| GAP-2482 | How a D5 credit approval is identified, and whether a result is an approve or a dedicated credit-result action, is not stated | P7 solution architect and the routing story owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2483 | The event name that carries the D5 record on the service topic is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2485 | The booking-confirmation decision is placed in rwb-decision while DP-04 and the registry story keep the evaluation in the owning service and state that rwb-decision never evaluates | Solution architect, with the decision service owner | Resolved (directive) |
| GAP-2486 | The operation set, paths and payloads of the batch, account, treatment, task, parameter and list contracts, the decision code, the record's snapshot and actions shape and several read and message details are in no source | Solution architect, with the owners of rwb-integration, rwb-treatment and rwb-case | Resolved (directive) |
| GAP-2487 | No source names the event that carries a booking decision out of rwb-decision, because the legacy TreatmentBooked is rwb-payment's and is raised after the treatment is booked | Solution architect, with the event platform owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2489 | The name of the rwb-decision database login is in no source | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2490 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its eleven legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2491 | The timezone, overlap, retry and fallback of the JOB-08 run and the behaviour of the legacy feature flag when off are in no source | Solution architect, with the workflow platform owner | Resolved (directive) |
| GAP-2492 | The legacy run writes the REC-03 result to reconciliation_result, and no table or owner of that name exists in the target and no source assigns the break list | Solution architect, with the reporting owner | Resolved (directive) |
| GAP-2493 | The Work Package places the payment-matching decision and its record in rwb-decision, while DP-03 keeps the record write in the owning service's transaction and DP-04 keeps the evaluation there, so no source fixes where a match record becomes central | Solution architect, with the decision service owner and the payment service owner | Resolved (directive) |
| GAP-2494 | No source names the target operations, the DecisionRecorded payload, the decision code of a missed payment, the inputs reference, the parameter key of the input age limit or the read page | Solution architect, with the owners of rwb-payment, rwb-access and rwb-case | Resolved (directive) |
| GAP-2495 | The dry-run answer of a rule-package version beyond testResult and dryRunCounts, and whether a caller may supply boundary cases, is in no source | Solution architect, with the rule registry owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2497 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2498 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2504 | rwb-payment payment matching (contract slice): the element names of the nine consumed operations, the extra event payload fields, the operation the architecture lists and the ownership map does not, and the schema baseline of proceeds are fixed by no single source | Contract owner of rwb-payment, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the event platform | Resolved (directive) |
| GAP-2505 | rwb-payment payment matching (deployment slice): the login and secret reference, the replica and threshold values, the partition and retention values, the build ID policy, the backfill limit and the runbook ownership are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2687 | The legacy treatment entity, its plan timers and its DP04 extract are split across three services, and no source states what the plan-timer data model holds on the S2 side once the clock moves to rwb-case | Solution architect with the data owner of rwb-treatment and the owners of rwb-case and rwb-source-data | Resolved (directive) |
| GAP-2688 | The parameters and reference-data operation names, the contract fake set, the field-level type of the event payload and the guard that limits a case to one running plan are not published for rwb-treatment | Contract owner of rwb-treatment with the parameters and reference-data owner of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2689 | The treatment-side credit-result record has no operation, no element names, no state values and no column rule in the S2 sources | Solution architect, S2, with the rwb-treatment tech lead and the rwb-integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2690 | The rwb-treatment share of the key is stated by no S2 source, and the caller contract, the level comparison, the case move and the record ownership are split across four stories | Solution architect with the rwb-integration, rwb-treatment, rwb-case and rwb-access tech leads and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2692 | The rwb-treatment share of the key is stated by no S2 source, the P2 contract shapes it follows are unpublished, and the trigger, the task-raising and the event ownership are split across stories | Solution architect with the rwb-integration, rwb-treatment and rwb-case tech leads and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2693 | The delivery route of a match to rwb-treatment, the plan-position elements and the payment frequency of a plan are not specified for the S2 slice of RWB-E2-008 | Tech lead of rwb-treatment with the P8 rwb-payment owner, the P3 rwb-case owner and the P7 rwb-decision package owner at the wave 2 contract freeze | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2695 | The owner of the treatment changed-window and active-count reads conflicts between the DP04 story and the service ownership | Solution architect | Resolved (directive) |
| GAP-2696 | The two operation shapes, the active-state rule and the reference-data read path are fixed by no source document | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2697 | The treatment-side panel section, its properties and action vocabulary, the treatment-type document set row and the one-hop set read are not specified | Solution architect | Resolved (directive) |
| GAP-2698 | The legacy files the whole generation capability under the document module, while the target gives the treatment screen leg to rwb-treatment and the set to rwb-document | Solution architect | Resolved (directive) |
| GAP-2738 | No source publishes a claim-side changed-window read for the DP04 build: the operation, its path, its page parameters, its maximum size, its error mapping and a count read all have no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2739 | The owner and the timing of the dated DP04 copy of a guarantee claim conflict: the legacy story writes dp_guarantee_claim itself and puts the claim interface in Epic 4, the target gives the copy to rwb-source-data in wave 2 and the claim record to rwb-guarantee in wave 3 | Solution architect | Resolved (directive) |
| GAP-2740 | No source says which side resolves a claim whose case does not exist, or whether the claim read answers such a claim at all | Data steward | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S2-E2004-APP | unknown story key | 23 | RWB-P7-E1073-CON is not a story of the set: \| Dependencies added by patterns \| Read as added by DP03, DP04, DP06, DP07, DP09, DP10, DP14, DP15 and DP19, not by the plan: platform H row |
| RWB-S2-E2006-APP | skipped AC ID | 115 | missing: AC10, AC11 |
| RWB-S2-E2010-APP | unknown story key | 26 | RWB-S2-E2010-CON is not a story of the set: \| Contract dependencies \| RWB-P1-E2010-CON, RWB-S2-E2010-CON \| |
