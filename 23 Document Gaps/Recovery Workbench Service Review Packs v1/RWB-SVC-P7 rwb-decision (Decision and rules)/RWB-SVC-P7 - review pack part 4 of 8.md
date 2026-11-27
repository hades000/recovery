# RWB-SVC-P7 rwb-decision (Decision and rules) - review pack, part 4 of 8 (RWB-P7-E2005-CON to RWB-P7-E2013-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 161 |
| Cross-document (pending in another document) | 206 |
| Not applied (value not in the sources) | 24 |
| Open business decisions | 33 |
| Register gaps linked | 139 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P7-E2005-CON | 25 | 9 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2005 CON Decision log query API for audit - contract v2.md |
| RWB-P7-E2006-APP | 21 | 31 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2006 APP Credit approval pack for NLEADS v2.md |
| RWB-P7-E2007-APP | 24 | 42 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2007 APP Booking confirmation from the ALS load v2.md |
| RWB-P7-E2008-APP | 23 | 49 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2008 APP Payment matching with the missed payment event v2.md |
| RWB-P7-E2012-APP | 29 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2012 APP Manual transfer and reassignment screen with reason v2.md |
| RWB-P7-E2013-APP | 22 | 32 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2013 APP Approval routing with the delegation of authority table v2.md |
| RWB-P7-E2013-CON | 17 | 24 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P7 rwb-decision (Decision and rules)/RWB P7 E2013 CON Approval routing with the delegation of authority table - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P7-E2013-APP | R-01828 | CG-ALL-7152 | Script gap | Product owner | The story adds ESCALATED to the closed list LOV-APPROVAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P7-E2005-CON | R-11244 | CG-ALL-7075 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2006-APP | R-11252 | CG-ALL-7091 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2007-APP | R-11258 | CG-ALL-7111 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2008-APP | R-11265 | CG-ALL-7126 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P7-E2012-APP | R-11272 | CG-ALL-7143 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2005-ITG, RWB-P4-E1037-CON, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-22366 | GAP-1243 | Register gap | Compliance and PDPA officer, with the P4 access owner | Whether the audit role may see unmasked person keys in an entry or an export | The audit read and the export carry the masked value under the policy of rwb-access in force, with no unmasking operation on either read; Compliance either confirms that reading or publishes an audit-specific policy row before the wave 2 exit. |
| RWB-ITG-E2005-ITG, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-22368 | GAP-1241 | Register gap | Compliance and PDPA officer, with the P7 business lead | Decision log retention period is not set | Compliance fixes the retention period and the archive rule for decision_log_entry as reference data before the wave 2 exit; until then the store keeps every entry, the query purges nothing and archives nothing, and the value is read as a parameter when it arrives. |
| RWB-ITG-E2008-ITG, RWB-P1-E1015-APP, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22404 | GAP-0600 | Register gap | Solution architect with the P1 data product owner | FSD P1 A2.2 stamps a payment read on DP01 Account and arrears while the Work Package slice note names DP05, and no source states whether the read or the rwb-payment run answers a held business date | Hold both gates on DP01 Account and arrears and answer 409 with MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run, with no row of any kind; record DP05 as not the stamp of a payment read and correct the slice note in the Work Package and the data product map in the next version of FSD P1 A2.2; state in RWB-P8-E2008-CON that the run's own refusal for the business date is its own and that the read's 409 is the answer to a call made anyway. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22414 | GAP-1630 | Register gap | Finance and CFO delegate | The posting file has no layout, no schedule and no receiving ledger in any source | Fix one line per posting with case, account key, entry type, amount, value date, business date and posting reference, a manifest with count and checksum, and delivery through rwb-integration. Agree the layout with Finance and the ledger owner before wave 3. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22415 | GAP-1632 | Register gap | Business lead | A reversed payment has no product behaviour in the FSD although the routing rules require the case to reopen | Decide whether a reversal is in scope for this service. If it is, add a reversal source value, a reversal state on the proceeds record and an event that reopens the case through rwb-case. Until then the capability is out of scope and listed as an open question. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22416 | GAP-1633 | Register gap | Finance and CFO delegate | The fee tables that the fee feature reads are not defined anywhere | Name the fee table, its owner and its schedule, and hold the fee rate, the cap and the basis as versioned rows. Until then the fee calculation has no input and the feature cannot be tested. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22419 | GAP-1636 | Register gap | Finance and CFO delegate | The order in which a receipt is applied to the balance is named but not specified | Hold the application order as versioned rows with an owner and a valid-from date, record the version on each proceeds row, and let Finance set the sequence before wave 3. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22463 | GAP-1616 | Register gap | Risk and model risk officer with the rwb-access owner | The delegation of authority table is loaded and approved inside P7 while the ownership ruling gives the table to rwb-access | Keep in this service only the lookup at the moment of the decision and the recording of the row ID and version; move A2.24 with AC-P7-024-01 to AC-EXC-P7-024-05 to rwb-access, and confirm the lookup answer shape (level, row ID, version, NOT_COVERED, RELATED_PARTY reason) in the access contract. Until then this PRD reads the limits and records the version, and OQ-P7-05 stays open. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22470 | GAP-1253 | Register gap | Business lead with the Center of excellence | The escalation ceiling and the service level values of an approval are not specified | Fix three values as data owned by RW-COE: the service level per decision and per default, the escalation step in working days, and a maximum escalation count with its ceiling behaviour (hold, incident to RW-RISK, or committee). Carry them as rwb.approval.service-level.*, rwb.approval.escalation.step and rwb.approval.escalation.max-levels and close DL22. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E2005-ITG, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-28719 | GAP-1244 | Register gap | Business analyst, P7, with Compliance | REQ-ACA-006 and NFR-042 still name a data-lake copy that DP-17 removes | Read REQ-ACA-006 and NFR-042 as covering the case store, the document store and the reporting read model; drop the lake wording at the next BRD and NFR version, retire the lake analysis with no target path and no dependency, and write the AC-READ/AC-EXPT record for the query path only. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-28740 | GAP-1638 | Register gap | Product owner | The only success measure of the module has no baseline and no measurement definition | Take the measure from the decision log as the FSD says, and have the product owner set the baseline, the target and the definition of 'the same day' before the wave-2 release note. |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28761 | GAP-3094 | Register gap | Business lead | The handler rows R-DEV-04 to R-DEV-06 and the SCR-05 deviation fragment layout are not in the sources | Read the four rows from the Business Rules and Routing Logic workbook at build time, render the fragment as a table of code, handler, paused state, contact stop and rule ID, and confirm the layout with the screen owner. |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28763 | GAP-3097 | Register gap | Business lead | The transfer reason codes R01 to R06 are an assumed set pending DL23 | Read the list at its version on the rwb-case reference-data contract, render whatever is in force, and hold the six codes as the default set until DL23 closes. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P7-E2005-CON | R-00663 | CG-ALL-3425 |  | Status 'Active' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-3425 is not in this chunk and no text for it was supplied. Needs a chunk that includes it. |
| RWB-P7-E2005-CON | R-18023 | DOR-RWB-P7-E2005-CON-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 text is not in this chunk, so no exact old text exists to add the SCR-38 empty, loading, error and no-access states. Needs section 15. |
| RWB-P7-E2005-CON | R-18024 | DOR-RWB-P7-E2005-CON-11 | 12.2 | Definition of Ready item 11 Guardrails: Partial | Section 12.2 field list is not in this chunk, so personal-data classing cannot be set or anchored. Needs section 12.2. |
| RWB-P7-E2005-CON | R-28718 | GAP-1246 | 13 | Approver index migration sits on a table created by another story | Section 13 migration text is not in this chunk, so the V2005_1 index-only migration note cannot be anchored. Needs section 13. |
| RWB-P7-E2006-APP | R-18034 | DOR-RWB-P7-E2006-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Section 18 text (L470-477) is not in this chunk, so no anchored edit can be made. DL12, DL18, DL19 rows are absent there. Needs section 18 text to apply. |
| RWB-P7-E2007-APP | R-06780 | DOR-RWB-P7-E2007-APP-17 | 3 | Definition of Ready item 17 Dependencies: Fail | Section 3 text not in chunk. The v1 story file names RWB-P7-E1073-CON at line 70, but that wording differs from the chunk, so no exact old text. No edit made. |
| RWB-P7-E2007-APP | R-18042 | DOR-RWB-P7-E2007-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Section 11 not in chunk; the field classed as personal data cannot be identified from the chunk or the v1 file. No edit made. |
| RWB-P7-E2007-APP | R-28731 | GAP-2488 | 3, 12.2, 12.8, 13 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Fix edits sections 3, 12.2, 12.8 and 13, none in the chunk. No staged copy matches the chunk text, so no exact old text. No edit made. |
| RWB-P7-E2008-APP | R-06786 | DOR-RWB-P7-E2008-APP-14 | Not in chunk | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources. Probe cache checked; Decision Log v11 mentions epic design sign-offs only in general. Needs the epic design record. |
| RWB-P7-E2008-APP | R-06790 | DOR-RWB-P7-E2008-APP-22 | Not in chunk | Definition of Ready item 22 Fake published: Fail | Not specified in the source documents (DOR-RWB-P7-E2008-APP-22). Users Roles and Permissions v5 A7 row has no fake library version. |
| RWB-P7-E2008-APP | R-18051 | DOR-RWB-P7-E2008-APP-11 | Not in chunk | Definition of Ready item 11 Guardrails: Partial | Guardrails section not in this chunk. The P2 personal-data fields are not named in the item and are not recoverable from the sources. |
| RWB-P7-E2008-APP | R-18052 | DOR-RWB-P7-E2008-APP-18 | Not in chunk | Definition of Ready item 18 Open decisions: Partial | Open-decisions section not in this chunk. DL25 is recorded as decided (A, 2026-11-06) in Decision Log v11, so no open decision remains to list. |
| RWB-P7-E2008-APP | R-22349 | GAP-1346 | 12.2 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Section 12.2 text is not in this chunk, so the seven consumed rows cannot be named by an exact edit. Resend section 12.2. |
| RWB-P7-E2008-APP | R-22423 | GAP-2494 | 11-13 | No source names the target operations, the DecisionRecorded payload, the decision code of a missed payment, the inputs reference, the parameter key of the input age limit or the read page | Sections 11 to 13 are not in this chunk, so the DecisionRecorded, consumer group and page default edits cannot be made. Resend those sections. |
| RWB-P7-E2008-APP | R-26302 | CG-ALL-7127 | 13 | Flyway file V2_008__payment_matching.sql is not in the V0001..Vnnnn form | The migration name is in section 13, which is not in this chunk. The next rwb_decision Flyway number is not in the supplied sources, so none is invented. |
| RWB-P7-E2008-APP | R-28746 | GAP-1349 | 5, 13 | RWB-E2-008: the case payment read, the SCR-28 and run-view field lists and the activity names of JOB-07 are not fixed by any source | Sections 5 and 13 are not in this chunk. The four matchPayments step activity names are not in any source, so they are not named. |
| RWB-P7-E2012-APP | R-18058 | DOR-RWB-P7-E2012-APP-11 | 3 | Definition of Ready item 11 Guardrails: Partial | Field classed as personal data is not named in the sources and the guardrail text is outside this chunk. Naming a field would invent a value; no edit made. |
| RWB-P7-E2012-APP | R-26310 | CG-ALL-7144 | 3, 3.1 | Flyway file V2027_3__decision_transfer_ledger.sql is not in the V0001..Vnnnn form | Line 391 in the chunk is the DP-14 row, not the V2027_3 migration name. Next Vnnnn is not in sources (D-RCV-28, merge order). No edit made. |
| RWB-P7-E2012-APP | R-28765 | GAP-3091 | 13 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Section 13 text is not in this chunk; the invented gate rule is removed. Depends on (build) None and Ready to start Day 1 kept. |
| RWB-P7-E2013-APP | R-06801 | DOR-RWB-P7-E2013-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed design record for this epic in the story or sources (grep of Definition of Ready, ways of working, DT05). The sign-off is not invented; the epic design record must be checked. |
| RWB-P7-E2013-APP | R-26316 | CG-ALL-7164 | 3 | Flyway file V2013_1__approval.sql is not in the V0001..Vnnnn form | No next V-number for the rwb_decision Flyway sequence in the sources; only platform V0001 is found. Not invented; the solution architect supplies the number. |
| RWB-P7-E2013-APP | R-26317 | CG-ALL-7165 | 12.5 | Criteria and tests keep legacy job and decision-log wording | The AC2, AC14 and test lines with JOB-nn or decision-log wording are outside the supplied story parts. Section 12.5 has no such wording. No edit made. |
| RWB-P7-E2013-CON | R-22471 | GAP-1255 | 12 | The request and answer field lists of the five approval operations and the case-status operation are not enumerated in any source | Section 12 text is not in this chunk, so no exact old text can be edited. Field lists must come from TSD P7 T3.1. Needs a chunk with section 12. |
| RWB-P7-E2013-CON | R-23122 | GAP-1889 | 12.1 | The approval contract publishes no operation that raises an approval item, so the petition's take-to-the-approver shape has no owner | No source gives the raise path, operation ID, error set or body schema; 12.1 lists no raise (CG-B-P7-01-E2013-5). Placeholder stays; no edit made. |

## 5. Cross-document changes (pending in the target document)


### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12118 | RWB-P7-E2006-APP | CG-ALL-7083 | 12.1 | 401 errors marked Not specified in the source documents (CG-ALL-7083) |
| CDC-12153 | RWB-P7-E2007-APP | CG-ALL-7108 | 14 | Add a new message ID with text for a consumed contract unavailable or answering beyond 2 s; the story then cites that ID in section 14 in place of MSG-GEN-006. |
| CDC-12184 | RWB-P7-E2008-APP | DOR-RWB-P7-E2008-APP-8 | 4, 12.1 | Add message IDs for 401 no session and for 404 an unknown package, version or entry (CG-ALL-7116). P1 is already fixed in section 4 step 4. |
| CDC-12186 | RWB-P7-E2008-APP | CG-ALL-7116 | 4, 12.1 | Add message IDs for 401 no session and for 404 an unknown package, version or entry, for the business analyst to write; story placeholders stay until then. |
| CDC-12187 | RWB-P7-E2008-APP | CG-ALL-7120 | 14 | Business analyst adds a new message ID for the append or chain-check failure. MSG-GEN-006 text is not copied, because story use differs from standard use (System of record unavailable). |
| CDC-12189 | RWB-P7-E2008-APP | DOR-RWB-P7-E2008-APP-9 | 14 | Business analyst adds a message ID for MSG-GEN-006 use (append or chain-check failure). MSG-P3-027 and MSG-GEN-001 already match standard v4. |
| CDC-12224 | RWB-P7-E2008-APP | GAP-1637 | find it | Publish wording, Thai text and channel for MSG-P8-001 and MSG-P8-002, and state whether MSG-P8-001 blocks. |
| CDC-12233 | RWB-P7-E2012-APP | CG-ALL-7137 | 4, 14 | Add a new message ID for refusal of a ledger record with a missing or invalid field; the story then cites it instead of MSG-P7-009. |
| CDC-12234 | RWB-P7-E2012-APP | CG-ALL-7138 | 4, 14 | Add a new message ID for no TRANSFER version in force on a business date, since the story's use differs from the standard's load-failure use of MSG-P3-027. |
| CDC-12236 | RWB-P7-E2012-APP | DOR-RWB-P7-E2012-APP-9 Messages: Partial | 14 | MSG-P7-009 and MSG-P3-027 text kept as the story's own wording; the new IDs and text route to the standard. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12136 | RWB-P7-E2006-APP | GAP-2483 |  | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision.events.v1 as well as the shared ledger topic, keyed by case id, and map it to a free identifier of EV-08, EV-09 or EV-30. |
| CDC-12145 | RWB-P7-E2007-APP | CG-ALL-7101 | 12.3 | Add rwb.decision.BookingDecisionMade.v1 to the Events sheet on topic rwb.decision.events.v1, owner P7. |
| CDC-12151 | RWB-P7-E2007-APP | CG-ALL-7103 | 12.4 | Add rwb-decision as a consumer of rwb.source-data.AceDataReady.v1, with its ACL. |
| CDC-12152 | RWB-P7-E2007-APP | CG-ALL-7104 | 12.4 | Add rwb-decision as a consumer of rwb.treatment.TreatmentApproved.v1, with its ACL. |
| CDC-12190 | RWB-P7-E2008-APP | GAP-3175 | find it | List AceDataReady (EV-26) as the target name on rwb.source-data.events.v1, with LoadCompleted as its legacy alias. |
| CDC-12280 | RWB-P7-E2013-CON | DOR-RWB-P7-E2013-CON-8 | 7, 12.4 | Add rwb-decision as a consumer of rwb.access.DoaLimitChanged.v1, including its ACL (P2). Story idempotency gap closed in section 7 AC1 (POST lines 110-112); P1 closed by CG-ALL-7170. |
| CDC-12282 | RWB-P7-E2013-CON | CG-ALL-7171 | 12.4 | Add rwb-decision as a consumer of rwb.access.DoaLimitChanged.v1 in the Events consumers list, with its ACL. |
| CDC-12291 | RWB-P7-E2013-CON | GAP-1221 | find it | Keep rwb.decision.ApprovalRequested.v1 as the published escalation event; add rwb-comms as a consumer of that event. Do not add ApprovalEscalated; TimerBreached stays a legacy reference. |
| CDC-12302 | RWB-P7-E2013-CON | GAP-1254 | find it | Mark INT-19, INT-20, lake partition, manifest and watermark as retired; state rwb-reporting reads rwb.decision-record.v1. Keep EV-08 unchanged. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12104 | RWB-P7-E2005-CON | CG-ALL-7074 | 18 | Align the RTM v7 test lists for REQ-DRI-012, REQ-DRI-003, REQ-ACA-006 and the fourth requirement to section 18 of RWB-P7-E2005-CON. |
| CDC-12156 | RWB-P7-E2007-APP | DOR-RWB-P7-E2007-APP-12 | 12.7, 16, 18 | Align the REQ-CHO-008 test list with section 18 of RWB-P7-E2007-APP (TC-E2-007-01 to -09, -11, -12). |
| CDC-12174 | RWB-P7-E2007-APP | CG-ALL-7110 | 18 | Align the REQ-CHO-008 test list with section 18 of RWB-P7-E2007-APP in the next RTM version. |
| CDC-12192 | RWB-P7-E2008-APP | GAP-2503 | find it | Record that legacy AC1, AC3, AC4 and AC5 of RWB-E2-008 are carried by no story of this split. |
| CDC-12216 | RWB-P7-E2008-APP | CG-ALL-7125 | 18 | Align the REQ-CHO-007 and REQ-CHO-009 test lists with section 18 of RWB-P7-E2008-APP in the next RTM version. |
| CDC-12241 | RWB-P7-E2012-APP | CG-ALL-7142 | 18 | Align the REQ-WKM-003 and REQ-WKM-007 test lists in its next version with story section 18. |
| CDC-12276 | RWB-P7-E2013-APP | CG-ALL-7163 | 18 | Align the test case lists of the nine requirements with the section 18 list of RWB-P7-E2013-APP in the next RTM version. |
| CDC-12299 | RWB-P7-E2013-CON | CG-ALL-7173 | 18 | Align the test lists of REQ-APD-001, REQ-APD-003, REQ-APD-009 and the fourth differing requirement with RWB-P7-E2013-CON section 18. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12122 | RWB-P7-E2006-APP | GAP-1713 | 5 | Record once in the service contract the owning contract of each feature-code prerequisite: approval to P7, case to P3, documents to P5, communications to P6, valuation to S1; carry FEAT-CHO-08 twice as written. |
| CDC-12127 | RWB-P7-E2006-APP | GAP-1342 | 12 | Settle in the wave 2 contract review: the rwb-decision login; the decision path on the approval resource with ApprovalAction and DecisionLogEntry field names; the delegation read shape and catalogue row; one owner for the level comparison; the NLEADS, level and result-date keys. |
| CDC-12128 | RWB-P7-E2006-APP | GAP-2478 | 4 | Rule delegation_limit to rwb-access, publish the level read there with its fake, and correct the DP-07 row of the pattern table; the level, row id and version stay on the approval row and the D5 entry. |
| CDC-12159 | RWB-P7-E2007-APP | GAP-2395 | find it | Settle with the rule registry owner which rule package rwb-comms reads, before integration; add no package code by assumption. |
| CDC-12160 | RWB-P7-E2007-APP | GAP-1713 | find it | Map each feature-code prerequisite to the contract of its owning service and record the mapping once in the service contract. |
| CDC-12191 | RWB-P7-E2008-APP | GAP-2395 | find it | Name the rule package code and version label that rwb-comms reads, settled with the rule registry owner. |
| CDC-12218 | RWB-P7-E2008-APP | GAP-1639 | find it | Name the event-started workflows for JOB-07 and JOB-08 (matchPayments, confirmBookings) on task queue rwb-payment, or confirm the activity is the unit. |
| CDC-12287 | RWB-P7-E2013-CON | GAP-1252 | 8, 11 | Add GET /api/recovery/access/v1/doa-limits with owner P4 to the API catalogue and to the operation list of RWB-P4-E1037-CON |

### RWB-P2-E2007-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12147 | RWB-P7-E2007-APP | DOR-RWB-P7-E2007-APP-21 | Header | Header keeps the contract dependency; no status change recorded in the story. |
| CDC-12148 | RWB-P7-E2007-APP | DOR-RWB-P7-E2007-APP-22 | Header | Record the contract fake library version as published. |
| CDC-12163 | RWB-P7-E2007-APP | GAP-0596 | 3 | Publish fieldState AVAILABLE or NOT_AVAILABLE per field with no value on NOT_AVAILABLE, and name flag rwb.dataengine.booking-facts, off until the Section B migration is applied. |
| CDC-12164 | RWB-P7-E2007-APP | GAP-0597 | 12, 12.1 | Publish GET /batch-status with sourceSystem and businessDate, the six values, and 404 with MSG-P1-001 when no batch row exists for the source and date. |
| CDC-12165 | RWB-P7-E2007-APP | GAP-0594 | 11, 12 | Publish GET /booking-facts and GET /batch-status on base /api/recovery/source-data/v1 with BookingFact, BookingFactsAnswer, FieldState and BatchStatusAnswer. |
| CDC-12169 | RWB-P7-E2007-APP | GAP-0658 | find it | Baseline result shape, task table, envelope, rerun operation, twelve consumed operations and seven fakes; record JOB-08 owner conflict and TSD P2 v3 T5.2 supersession in the gap register. |
| CDC-12171 | RWB-P7-E2007-APP | GAP-0730 | find it | Publish the composite route, treatment booking fields and raiseTask result schema for the rwb-case slice; fix the rwb-case login in the platform DB story. |
| CDC-12172 | RWB-P7-E2007-APP | GAP-2486 | find it | Publish the operation set, paths and payloads from the six legacy interfaces on the DP-13 base; take decision code and outcome values from LOV-DECISION; fix read filters, page size, ordering and MSG-GEN-006 text before SIT. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12103 | RWB-P7-E2005-CON | CG-ALL-7073 | 16 | Add rows for TC-P7-E2005-CON-01 to TC-P7-E2005-CON-08 with Given, When and Then copied from the criterion each covers. |
| CDC-12154 | RWB-P7-E2007-APP | CG-ALL-7109 | 16 | Add rows for TC-E2-007-11 with Given, When and Then copied from AC8 (BR9) of RWB-P7-E2007-APP. |
| CDC-12188 | RWB-P7-E2008-APP | CG-ALL-7122 | 16 | Add a row for TC-E2-008-10: Given a role without Decision log R, When it calls GET /decision-log, Then 403 with MSG-P4-002 and no entry is read (AC9). |
| CDC-12229 | RWB-P7-E2012-APP | DOR-RWB-P7-E2012-APP-12 | 16 | Add TC-E2-012-15 and TC-E2-012-16 to TC-E2-012-20 under the story test cases tab, and align the section 18 test lists with RTM v7. |
| CDC-12235 | RWB-P7-E2012-APP | CG-ALL-7139 | 16 | Add row TC-E2-012-15 to tab Story test cases with Given, When and Then copied from AC6 of RWB-P7-E2012-APP. |
| CDC-12246 | RWB-P7-E2012-APP | GAP-3098 | 16 | Keep one row per legacy TC ID in the assembled master, record both slices against it; End to end level from RWB-P3-E2012-APP, Component level from this story |
| CDC-12298 | RWB-P7-E2013-CON | CG-ALL-7172 | 16 | Add rows for TC-P7-E2013-CON-01 to TC-P7-E2013-CON-08, with Given, When and Then copied from the criterion each covers. |

### RWB-P8-E2008-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12197 | RWB-P7-E2008-APP | GAP-0601 | 12 | Publish one row per payment_code ordered by paymentCode ascending, unpaged reads with the cap as configuration, the fold rule in the OpenAPI fragment, and the over-cap answer in the next API Specification; route a confirmed duplicate to REC-05 of RWB-P1-E1011-APP. |
| CDC-12198 | RWB-P7-E2008-APP | GAP-0599 | 12 | Publish the two operations on /api/recovery/source-data/v1 with resource names, the businessDate query parameter, element names and the status set in the OpenAPI fragment; take consumed rows at the wave 2 freeze. |
| CDC-12203 | RWB-P7-E2008-APP | GAP-1350 | 12 | Publish one OpenAPI 3.1 and one AsyncAPI document per service, problem+json on every non-2xx status, MatchRequest properties, the next Flyway number, and major version 1 with BACKWARD acceptance. |
| CDC-12212 | RWB-P7-E2008-APP | GAP-2504 | find it | Publish v1 with the two operations, three event schemas, nine declarations, schema baseline and message map. Mark each unsettled element with the placeholder and one review row. |
| CDC-12215 | RWB-P7-E2008-APP | GAP-1347 | 3 | Publish the schemas of TreatmentBooked, PaymentMissed and ProceedsMatched on rwb.payment.events.v1 with PaymentMissed (treatmentId, dueDate, amountDue) and ProceedsMatched (proceedsId, caseId, amount); TreatmentBooked fields Not specified in the source documents; require a new version for added business fields. |
| CDC-12219 | RWB-P7-E2008-APP | GAP-0602 | find it | Record the account resource of Architecture v5 slide 15 as unowned and unpublished; if commissioned, give it a P1 owner and move nextInstallmentDate in one contract change. |

### RWB-P7-E2006-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12107 | RWB-P7-E2006-APP | CG-ALL-7078 | 12.1 | Publish POST /api/recovery/decision/v1/approvals/{approvalId}/approve in rwb-decision.yaml. |
| CDC-12108 | RWB-P7-E2006-APP | CG-ALL-7079 | 12.1 | Publish POST /api/recovery/decision/v1/approvals/{approvalId}/refuse in rwb-decision.yaml. |
| CDC-12109 | RWB-P7-E2006-APP | CG-ALL-7080 | 12.1 | Publish GET /api/recovery/decision/v1/approvals/{approvalId} in rwb-decision.yaml. |
| CDC-12110 | RWB-P7-E2006-APP | CG-ALL-7081 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log in rwb-decision.yaml. |
| CDC-12111 | RWB-P7-E2006-APP | CG-ALL-7082 | 12.1 | Publish GET /api/recovery/decision/v1/decision-log/{entryId} in rwb-decision.yaml. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12116 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-8 | 12.1 | Add the approve, refuse, approval read and decision-log paths named by detcheck, plus the five more listed. |
| CDC-12138 | RWB-P7-E2007-APP | CG-ALL-7093 | 12.1 | Publish POST /api/recovery/decision/v1/admin/jobs/{jobId}/rerun in rwb-decision.yaml, or remove it from section 12.1. |
| CDC-12139 | RWB-P7-E2007-APP | CG-ALL-7094 | 12.1 | Publish GET /api/recovery/decision/v1/booking-decisions in rwb-decision.yaml, or remove it from section 12.1. |
| CDC-12149 | RWB-P7-E2007-APP | DOR-RWB-P7-E2007-APP-8 | Header | Publish POST /admin/jobs/{jobId}/rerun and GET /booking-decisions in rwb-decision.yaml, and the listed rwb-integration batch and case account paths, with the 7 further detcheck paths. |
| CDC-12250 | RWB-P7-E2013-APP | DOR-RWB-P7-E2013-APP-8 | 12.1 | Hold approvalLevel and status as LOV-APPROVAL-LEVEL and LOV-APPROVAL-STATUS references, not closed enums; align event type to rwb.decision.DecisionRecorded.v1 per Kafka Catalog v1 (+5 more not listed). 401 mapping done in CG-ALL-7154. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12098 | RWB-P7-E2005-CON | DOR-RWB-P7-E2005-CON-14 | find it | Record the signed epic design sign-off for this story's epic; the story and source documents carry none. |
| CDC-12112 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-14 | header | Confirm and record the signed epic design sign-off, then cite it in the story. |
| CDC-12146 | RWB-P7-E2007-APP | DOR-RWB-P7-E2007-APP-14 | Header | Record the signed epic design sign-off that covers RWB-P7-E2007-APP. |
| CDC-12230 | RWB-P7-E2012-APP | DOR-RWB-P7-E2012-APP-14 | Header | Record the signed epic design sign-off for RWB-SVC-P7 and cite its reference in this story. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12117 | RWB-P7-E2006-APP | CG-ALL-7077 | 11 | Record credit_result_at as a field of the treatment owner (DF-TRT-026), or name the owning object. |
| CDC-12157 | RWB-P7-E2007-APP | DOR-RWB-P7-E2007-APP-7 | 11 | Add DF-ACC-009, DF-ACC-030 and DF-ACC-031 as v_ace_account legacy field IDs, or record them as legacy-only IDs of the account answer. |
| CDC-12185 | RWB-P7-E2008-APP | CG-ALL-7115 | 3, 5 | Record tr_declog_append_only as the append-only trigger object of rwb_decision.decision_log_entry, or use its dictionary name. |
| CDC-12221 | RWB-P7-E2008-APP | GAP-0927 | find it | Carry filter and row count in the actions list of the decision-record entry; add capability area and right to the same list. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12125 | RWB-P7-E2006-APP | GAP-0663 | 12 | Settle in the wave 2 contract review: rwb-integration login with the ACE DB owner; resource placement; operation names and field sets of the rwb-source-data, rwb-treatment, rwb-case, rwb-document and rwb-access reads; AC2 and AC7 approval levels against doa.txt item 2.1.1. |
| CDC-12126 | RWB-P7-E2006-APP | GAP-0729 | 12 | Agree the rwb-case login with the ACE DB story, the SCR-14 composite route with the edge story, the NLEADS credit-decision read and treatment result fields with the P1 and S2 contract stories; settle AC2 and AC7 levels against doa.txt item 2.1.1. |
| CDC-12134 | RWB-P7-E2006-APP | GAP-2690 | 1 | Record the two treatment operations and the credit-result element set against rwb-treatment, the level comparison against rwb-access, the ledger entry against rwb-decision and the SCR-14 merge against the edge contract. |
| CDC-12135 | RWB-P7-E2006-APP | GAP-2482 | 6 | Set source_type to CREDIT_APPROVAL and source_ref to the treatment id for a D5 row; state that a credit result is recorded through approve or refuse on that row. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12129 | RWB-P7-E2006-APP | GAP-2479 | 12 | Add GET /api/recovery/access/v1/doa-limits with decisionCode, regulationItem, productGroup, amount and asOfDate, answering level, delegationLimitId, limitVersion or NOT_COVERED; publish MSG-P7-010, MSG-GEN-006 and MSG-P4-003 texts. |
| CDC-12240 | RWB-P7-E2012-APP | GAP-3093 | none | Publish GET /cases/{caseId}/deviations on /api/recovery/deviation/v1 as the answer the move and the SCR-05 panel use; keep DeviationRaised and DeviationCleared for the event-fed flag; fix the read schema. |
| CDC-12267 | RWB-P7-E2013-APP | GAP-0928 |  | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with the query and response fields this story uses; correct the v4 omission per Architecture v5. |
| CDC-12289 | RWB-P7-E2013-CON | GAP-0928 | find it | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with the query and response fields this story uses; correct the v4 omission per R-PREC in favour of Architecture v5. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12253 | RWB-P7-E2013-APP | CG-ALL-7159 | 12.5 | Add activity readDelegation in rwb-decision on task queue rwb-decision, or use a catalogued activity. |
| CDC-12254 | RWB-P7-E2013-APP | CG-ALL-7160 | 12.5 | Add activity routeApproval in rwb-decision on task queue rwb-decision, or use a catalogued activity. |
| CDC-12255 | RWB-P7-E2013-APP | CG-ALL-7161 | 12.5 | Add activity recordOutcome in rwb-decision through the library on task queue rwb-decision, or use a catalogued activity. |
| CDC-12256 | RWB-P7-E2013-APP | CG-ALL-7162 | 12.5 | Add activity escalateApproval in rwb-decision on task queue rwb-decision, or use a catalogued activity. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12100 | RWB-P7-E2005-CON | DOR-RWB-P7-E2005-CON-12 | 12.7, 16, 18 | Add rows TC-P7-E2005-CON-01 to TC-P7-E2005-CON-09 to Test Cases v8, and align the section 18 test lists with RTM v7. |
| CDC-12181 | RWB-P7-E2008-APP | DOR-RWB-P7-E2008-APP-12 | 16, 18 | Add TC-E2-008-10, TC-E2-008-11 and TC-E2-008-12 with Given/When/Then; align RTM v7 test lists with §18. |
| CDC-12284 | RWB-P7-E2013-CON | DOR-RWB-P7-E2013-CON-12 | 12.7, 16, 18 | Add Story test cases rows TC-P7-E2013-CON-01 to -09 to the tab; align the section 18 test lists with RTM v7. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12105 | RWB-P7-E2005-CON | GAP-2468 |  | Carry the six platform CON rows (DP-03, DP-06, DP-07, DP-09, DP-10, DP-19) and RWB-P7-E2005-CON in the dependency map; keep lane at Day 1. |
| CDC-12132 | RWB-P7-E2006-APP | GAP-1343 |  | Publish the six DP-added dependencies with this story as consumer: RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON and RWB-P4-E1037-CON. |
| CDC-12297 | RWB-P7-E2013-CON | GAP-1885 | 12.2 | Consumed rows belong in the Dependency Map, not in this story. No header row is added for them. |

### RWB-P7-E2006-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12113 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-21 | header | Create the contract story publishing the five section 12.1 operations in rwb-decision.yaml. |
| CDC-12114 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-22 | Header | Publish a contract fake library version and record it as published. |
| CDC-12115 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-23 | header | Placeholder in Contract dependencies row |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12150 | RWB-P7-E2007-APP | GAP-1696 | Not located in supplied parts | Add S2 to the P1 REST cell of the connection matrix (slide 13). Reroute FSD S2 A2.6.3.1, A2.13.2, A2.10.2 and A2.17.2 reads through the rwb-source-data contract. |
| CDC-12195 | RWB-P7-E2008-APP | GAP-1626 | find it | Align slide 17 rwb-payment operations to GET /proceeds and POST /proceeds/{proceedsId}/match as in API Specification v4. |
| CDC-12293 | RWB-P7-E2013-CON | GAP-1257 | find it | Delete ApprovalDecided from the rwb.decision.events.v1 list on slide 14 and rely on DecisionRecorded as the outcome event, unless a catalogue row with a number and consumers is added. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12180 | RWB-P7-E2008-APP | CG-ALL-7117 | 13 | Create story RWB-P7-E1073-CON or name the existing story that holds the same rule-package contract capability. |
| CDC-12182 | RWB-P7-E2008-APP | DOR-RWB-P7-E2008-APP-17 | 13 | Create story RWB-P7-E1073-CON or name the existing story holding the same rule-package contract capability. |
| CDC-12183 | RWB-P7-E2008-APP | DOR-RWB-P7-E2008-APP-21 | none | Publish RWB-P8-E2008-CON (already named in Contract dependencies) or create RWB-P7-E2008-CON for the paths this story exposes. |

### RWB-P3-E2012-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12242 | RWB-P7-E2012-APP | CG-ALL-7145 SCR-05 states | 15 | No SCR-05 state rows added to this story. |
| CDC-12243 | RWB-P7-E2012-APP | CG-ALL-7146 SCR-07 states | 15 | No SCR-07 state rows added to this story. |
| CDC-12244 | RWB-P7-E2012-APP | CG-ALL-7147 SCR-09 states | 15 | No SCR-09 state rows added to this story. |

### RWB-P7-E2013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12247 | RWB-P7-E2013-APP | DOR-RWB-P7-E2013-APP-21 | header | Publish the contract and set its build status from Not started to Done. |
| CDC-12248 | RWB-P7-E2013-APP | DOR-RWB-P7-E2013-APP-22 | header | Publish a contract fake library version and record it as published. |
| CDC-12272 | RWB-P7-E2013-APP | GAP-1255 | 12 | Baseline the five approval resources from TSD P7 T3.1 camelCase fields with page and error conventions, fix required ApprovalAction properties, and add the case-status operation to the Ownership Map. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12249 | RWB-P7-E2013-APP | DOR-RWB-P7-E2013-APP-5 | 9 | Confirm In progress and Waiting approval (section 9 From/To values) are listed in LOV-CASE-STATUS; add them if not. ESCALATED is already kept out of LOV-APPROVAL-STATUS in section 9. |
| CDC-12258 | RWB-P7-E2013-APP | DOR-RWB-P7-E2013-APP-20 |  | Add the LOV-OVERRIDE-REASON list. |
| CDC-12285 | RWB-P7-E2013-CON | DOR-RWB-P7-E2013-CON-20 | find it | Add LOV-OVERRIDE-REASON as a P2 List value so that BR9 reference data is complete |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12099 | RWB-P7-E2005-CON | DOR-RWB-P7-E2005-CON-1 | 1 | Add a role code or role name for the tech lead of rwb-decision, the role named in section 1 of RWB-P7-E2005-CON. |
| CDC-12283 | RWB-P7-E2013-CON | DOR-RWB-P7-E2013-CON-1 | 1 | Add the role 'tech lead of rwb-decision' with a role code and name, so the section 1 role resolves. |

### RWB-P2-E2006-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12120 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-11 | find it | Reconcile the personal-data classification of its fields with this story, which states that no personal data is carried. |
| CDC-12121 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-9 | 14 | Use the standard meaning of MSG-P7-010, MSG-GEN-006 and MSG-P4-003 as in Error and Message Standard v4 §4. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12140 | RWB-P7-E2007-APP | CG-ALL-7095 | 12.2 | Publish GET /api/recovery/integration/v1/batches/{source}/{businessDate} in rwb-integration.yaml through RWB-P2-E2007-CON. |
| CDC-12141 | RWB-P7-E2007-APP | CG-ALL-7096 | 12.2 | Publish GET /api/recovery/integration/v1/cases/{caseId}/accounts?businessDate= in rwb-integration.yaml through RWB-P2-E2007-CON. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12142 | RWB-P7-E2007-APP | CG-ALL-7097 | 12.2 | Publish GET /api/recovery/treatment/v1/treatments?type=&state=APPROVED&booked=false in rwb-treatment.yaml through the provider's CON story. |
| CDC-12143 | RWB-P7-E2007-APP | CG-ALL-7098 | 12.2 | Publish POST /api/recovery/treatment/v1/treatments/{treatmentId}/booking in rwb-treatment.yaml through the provider's CON story. |

### RWB-P4-AD002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12166 | RWB-P7-E2007-APP | GAP-0923 | find it | Extend TSD P4 T6.1 RBAC matrix with Case record and Treatment and offer columns, publish the 14-area matrix as data, and confirm RW-RESTRUCT and RW-CREDITAD letters with the matrix owner. |
| CDC-12199 | RWB-P7-E2008-APP | GAP-0926 | 10 | Publish a new T6.1 version with letters for all 14 LOV-CAPABILITY areas per role, including Write-off and posting and Treatment and offer, and the default scope of each role. |

### RWB-P4-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12200 | RWB-P7-E2008-APP | GAP-0925 | 10 | Extend the envelope with area, right, scope, resource, filter, rowCount and matrixVersion, and fix the three answer codes at the wave 2 contract review. |
| CDC-12268 | RWB-P7-E2013-APP | GAP-0929 | 3 | Field set deferred to the contract review |

### RWB-P8-E2008-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12202 | RWB-P7-E2008-APP | GAP-1348 | 13 | Keep the TSD P8 T3.1 proceeds field set with account_payment_id; replace payment_missed_event_key with the DP-09 idempotency_key table; take the next number of the service Flyway sequence; data owner confirms where the payment code is held. |
| CDC-12214 | RWB-P7-E2008-APP | GAP-2693 | 4 | Specify the match route to rwb-treatment: applyProceedsMatched and holdMissedInstallment via the inbox of ProceedsMatched.v1 and PaymentMissed.v1; serve the plan position as elements of the API-S2-002 treatment read; confirm package and frequency at contract freeze. |

### RWB-P8-E2008-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12204 | RWB-P7-E2008-APP | GAP-1352 | 13 | Render the rwb-payment deployment unit from the pinned chart with the worker floor, ceiling, tier sizes, topic partitions and retention, the PROD canary or blue/green step, release gates and a down script per migration. |
| CDC-12213 | RWB-P7-E2008-APP | GAP-2505 | find it | Ship one chart with api and worker deployments, migration job, topic and two consumer groups, five alerts with runbook links, four dashboard series, flag, backfill and rollback. Take thresholds as environment values. |

### RWB-P3-E2012-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12238 | RWB-P7-E2012-APP | GAP-0710 | none | Fix one selection element in the rwb-case contract: an ordered array with caseId, the assignment or messageId of the refusal, and the done and total counts; order is the caller's; the summary is derived from the array. |
| CDC-12239 | RWB-P7-E2012-APP | GAP-0711 | none | Fix a refusal element with a reason code, the owner list with an open-case count and cap each, and the current and target state; read the cap and hold inside the operation before the first write. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12245 | RWB-P7-E2012-APP | GAP-3095 | 7 | Declare the S8 consumer group for the case status and legal-hold events against a placeholder; bind the published event names when the rwb-case event catalogue fixes them |
| CDC-12273 | RWB-P7-E2013-APP | GAP-1257 | find it | Delete ApprovalDecided from the slide 14 EVT line, or add a catalogue row with number and consumers; no P7 story publishes it. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12261 | RWB-P7-E2013-APP | GAP-3177 |  | Register the five-minute next-action Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables. |
| CDC-12286 | RWB-P7-E2013-CON | GAP-3177 | find it | Register the five-minute next-action Schedule in rwb-case; delete EV-18 from the Epic 2 contract tables |

### OTHER:RWB-E2-031 app slice of the agent monitoring dashboard v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12101 | RWB-P7-E2005-CON | GAP-0629 | find it | Apply the nine resolutions of the proposed fix there; the additive agent-version filter and three elements on rwb-decision need the elements named first |

### OTHER:Agent monitoring dashboard v2 contract slice (rwb-agent), from RWB-E2-031 section 12 and TSD P10 v2 T-A.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12102 | RWB-P7-E2005-CON | GAP-0630 |  | Fix the seven added member names with four-decimal rule and major-version-1 additive rule; name drift inputs after watch_measures members; declare agent-version filter and three decision-record elements as additive change of rwb-decision contract; name notice path by owner; register route under RWB-PLT-N001-CON. |

### OTHER:RWB-E2-031 version 2 contract slice (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12106 | RWB-P7-E2005-CON | GAP-2199 | 7 | Right name recorded in AC5; filter, override element, notice and paging remain open |

### RWB-P3-E2006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12119 | RWB-P7-E2006-APP | DOR-RWB-P7-E2006-APP-10 | find it | Add empty, loading, error and no-access states for screen SCR-14. |

### RWB-ITG-E2006-ITG; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12123 | RWB-P7-E2006-APP | GAP-1344 | 4 | Confirm delegation_limit stays with P4 rwb-access; add the DoA limit read to the Ownership Map API catalogue with P4 as owner and P7, P3, P2 as consumers; correct the attribution in the ITG story. |

### OTHER:Credit approval pack harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12124 | RWB-P7-E2006-APP | GAP-0394 | 13 | Agree the composite credit-pack route and merge order with the platform edge story, and record the harness environment, repository, seed data, evidence format, retention and pass/fail gate before the first real-service run. |

### OTHER:Decision-record schema document (TSD P7 T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12130 | RWB-P7-E2006-APP | GAP-2480 | 12 | Fix the D5 key set of actions as requiredLevel, delegationLimitId, limitVersion, nleadsRef and resultDate; take inputs_ref from the pack read reference; confirm the NLEADS reference pattern with SCB IT before the wave 2 test cycle. |

### OTHER:TSD S2 v2 (rwb-treatment contract baselines T3.0 to T3.2 and T-A.1) and FSD S2 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12131 | RWB-P7-E2006-APP | GAP-2689 | 12 | Add the credit-result variant of the treatment PATCH with its element names, If-Match header and once-only rule at the wave 2 freeze; add SUBMITTED, APPROVED and REFUSED to the state check; add the four credit columns on the service Flyway sequence. |

### RWB-ITG-E3013-ITG; RWB-ITG-E3017-ITG; RWB-ITG-E3026-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12133 | RWB-P7-E2006-APP | GAP-3213 | 18 | Accept the E3 integration trace of REQ-RDF-004 as the citation for the legacy keys and record it in the v7 row. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12137 | RWB-P7-E2006-APP | GAP-2484 |  | Give GET /cases/{caseId}/recommendation to the P7 story that serves the decision screen; keep the metadata rows as given and treat the four platform contracts as published before Day 1. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12144 | RWB-P7-E2007-APP | CG-ALL-7099 | 12.2 | Publish POST /api/recovery/case/v1/cases/{caseId}/tasks in rwb-case.yaml through the provider's CON story. |

### OTHER:Owner stories for SCR-01; OTHER:SCR-14 and SCR-29 (treatment, case and payment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12155 | RWB-P7-E2007-APP | DOR-RWB-P7-E2007-APP-10 | 15 | Add empty, loading, error and no-access states for SCR-01, SCR-14 and SCR-29. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12158 | RWB-P7-E2007-APP | GAP-3175 | find it | Name AceDataReady (EV-26, producer rwb-source-data) as the target event and list LoadCompleted as its legacy alias. |

### OTHER:FSD S2 (A2.10; OTHER:A2.11; OTHER:A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12161 | RWB-P7-E2007-APP | GAP-1703 | find it | Replace direct NLEADS, ALS and GL booking writes with consumption of TreatmentBooked and PaymentMissed from rwb-payment and a release request via the integration contract. |

### RWB-P2-E2007-APP; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12162 | RWB-P7-E2007-APP | GAP-0657 | find it | Keep JOB-08 with rwb-integration; record the slide 44 rwb-payment owner row as superseded for JOB-08; serve the JOB-08 rerun on the integration base. |

### OTHER:TSD P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12167 | RWB-P7-E2007-APP | GAP-0922 | find it | Add the POST /authorise path with request and answer schemas to the API specification and TSD P4 appendix T-A, publish with RWB-P4-E1037-CON and stub it in the contract fake; fix the rwb-access login and gateway-bff composite route. |

### OTHER:Booking confirmation integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12168 | RWB-P7-E2007-APP | GAP-0395 | find it | Agree at the wave 2 entry check the composite booking and treatment route path and merge order, harness environment, ALS booking fixture format, seed pack, evidence format, retention and pass or fail gate. |

### RWB-P2-E2007-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12170 | RWB-P7-E2007-APP | GAP-0659 | find it | Fix identity, secret reference and probe checks; register JOB-08 on rwb-integration and record the owner conflict; write the JOB-08 catalogue row with run book path; review four runbook entries with the on-call rota. |

### RWB-S2-E3001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12173 | RWB-P7-E2007-APP | GAP-2691 | 4 | Add the approved-not-booked read, the mark-booked write and the booking-difference write with element names at wave 2 freeze; CHECK on state with APPROVED and BOOKED; booking_difference jsonb keyed by term; unique key per treatment and business date. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12175 | RWB-P7-E2007-APP | GAP-0924 |  | Add a key for the lifetime of the cached rwb-access authorise decision, with its value agreed at the wave 2 design review. |

### OTHER:Platform secret store (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12176 | RWB-P7-E2007-APP | GAP-2489 |  | Allocate the rwb-decision login with schema rwb_decision and record it in the platform secret store. |

### OTHER:Source for JOB-08 run timing and legacy flag behaviour (none in the sources) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12177 | RWB-P7-E2007-APP | GAP-2491 | 8 | BR13 keeps the start trigger; timezone, overlap, retry, fallback and flag-off behaviour are Not specified in the source documents. |

### OTHER:Source that assigns the REC-03 break list (none in the sources) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12178 | RWB-P7-E2007-APP | GAP-2492 | 8 | BR14 drops the rwb-reporting assignment and DF-OPS values; the break-list owner is Not specified in the source documents. |

### parameter-catalog.csv; OTHER:reference-data register; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12179 | RWB-P7-E2007-APP | GAP-2692 | 1 | Add booking.missing.grace_loads and the treatment-type and outcome list codes; record TreatmentBooked ownership against rwb-payment; record the parent stage outcome contract. |

### OTHER:FSD S2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12193 | RWB-P7-E2008-APP | GAP-1703 | find it | Remove the NLEADS, ALS and payment-schedule writes of A2.10, the missed-payment count of A2.11 and the CCMS release of A2.17; rwb-payment owns them and this service records the events. |

### OTHER:FSD P8 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12194 | RWB-P7-E2008-APP | GAP-1625 | find it | Replace placeholder rows AC-P8-003-01 to AC-P8-011-01 with testable main-flow criteria. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:A2.3 to A2.11) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12196 | RWB-P7-E2008-APP | GAP-1631 | 11 | Name the ALS read through rwb-source-data and ledger postings through rwb-integration; list no ATS, AMIS or LED interface; treat auto-debit and LED routes as outside the 19 services. |

### OTHER:Payment matching integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12201 | RWB-P7-E2008-APP | GAP-0393 | 13 | Record the composite proceeds and exception route path and merge order, harness environment, ALS payment fixture format, seed pack, evidence format, retention and pass or fail gate at the wave 2 entry check. |

### OTHER:WP B-P8-01 split plan (next revision) or epic overview coverage note (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12205 | RWB-P7-E2008-APP | GAP-1354 | 7 | Reallocate AC1, AC3, AC4 and AC5 to RWB-P8-E2008-APP in the next split plan revision, or add a coverage note to the epic overview. |

### OTHER:FSD P8 v3 (AC-EXC-P8-001-02; OTHER:AC-EXC-P8-002-02) and rwb-source-data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12206 | RWB-P7-E2008-APP | GAP-1627 | find it | Report the orphan payment as a break row on the reconciliation break list, check name 'References'. Write no exception table in rwb_payment. Data steward confirms the check name. |

### OTHER:FSD P8 v3 (A1.2 FEAT-PAY-06) and Epics 3 to 8 BRD (7.3; OTHER:DEP-005) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12207 | RWB-P7-E2008-APP | GAP-1629 | find it | Move the first release of FEAT-PAY-06 from E4 to E3 (wave 2, EP03). The proceeds features stay in E4 (wave 3). |

### OTHER:TSD P8 v2 (T3.1 DF-FIN-004; OTHER:T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12208 | RWB-P7-E2008-APP | GAP-1634 | find it | Replace the account_payment_id uuid CROSS_REF with one business-key column, varchar(255), holding the ACE payment_code, with no foreign key. |

### OTHER:FSD P8 v3 (A2.11.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12209 | RWB-P7-E2008-APP | GAP-1635 | find it | Reconcile to the ACE payment and account position and to the posting file. Record a ledger return as an open question until the ledger owner publishes one. |

### OTHER:FSD P8 v3 (AC-BG-P8-001-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12210 | RWB-P7-E2008-APP | GAP-1640 | find it | Keep one matching run per business date in wave 2. Record the payment-received same-day trigger as an open question. Add an intraday run only when an interface carrying payments intraday is named. |

### OTHER:NFR Spec v3 (NFR-001 and new volume row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12211 | RWB-P7-E2008-APP | GAP-1643 | find it | State receipts per business date, sized from the receipt-to-installment ratio on ACE data for a busy month. Until then the volume test uses the ratio as an assumption. Figure: Not specified in the source documents (GAP-1643). |

### OTHER:FSD P8 v3 (Requirements served) and TSD P8 v2 (T8 Requirement traceability) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12217 | RWB-P7-E2008-APP | GAP-1624 | find it | Fill the requirements table with REQ IDs for P8, or state that P8 has no requirement ID of its own. |

### RWB-P8-E2008-APP; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12220 | RWB-P7-E2008-APP | GAP-0603 | find it | Record the payment-matching run's workload identity as caller in the authority table; correct the P8 to P1 activity to one REST hop wrapped by the run's activity. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:Contract; OTHER:TSD P8 T5.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12222 | RWB-P7-E2008-APP | GAP-1351 | 16 | DP-03 ownership line in section 16 stays as written; sources still disagree |

### RWB-P8-E2008-OPS; OTHER:DL11) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12223 | RWB-P7-E2008-APP | GAP-1353 | find it | Hold outbox-lag, dead-letter and workflow-failure thresholds as service values data with no default; raise alerts on their own measurement before PROD. |

### OTHER:Work Package plan (B-P1-08; OTHER:B2-P1-014) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12225 | RWB-P7-E2008-APP | GAP-2180 | find it | Keep one Work Package per story slice; drop the duplicate write of RWB-P1-E2008-APP and add a plan-uniqueness check. |

### OTHER:Recovery Workbench FSD P7 v3 (dry run of a rule-package version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12226 | RWB-P7-E2008-APP | GAP-2495 |  | Publish the dry run as a read-only operation returning testResult (total, passed, failed, failing case IDs), per-test-case expected and actual result, and recorded dry-run counts. Boundary cases stay in the version's rule_test_case set. |

### OTHER:Platform secret store (ACE team allocation for schema rwb_decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12227 | RWB-P7-E2008-APP | GAP-2497 |  | Allocate the rwb-decision login for schema rwb_decision and record it in the platform secret store. |

### OTHER:Program BRD v5 section 11 note (for BRD owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12228 | RWB-P7-E2008-APP | GAP-1641 | header | Story cites REQ-S4-010 in the PRD reference; the BRD note itself is outside this story. |

### OTHER:Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12231 | RWB-P7-E2012-APP | DOR-RWB-P7-E2012-APP-21 | Header | Create contract story RWB-P7-E2012-CON, or record that this story owns no contract. |

### RWB-P3-E2012-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12232 | RWB-P7-E2012-APP | DOR-RWB-P7-E2012-APP-22 | Header | Record the published fake library version of RWB-P3-E2012-CON. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12237 | RWB-P7-E2012-APP | GAP-2502 | 11 | Publish rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 in place of rwb.decision-record.DecisionRecorded.v1 for the same record; the boundary is set in section 11 of this story. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:Lists (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12251 | RWB-P7-E2013-APP | CG-ALL-7153 | find it | Add list LOV-OVERRIDE-REASON with the values the story uses (Not specified in the source documents (CG-ALL-7153)); the list is not in the shown story text. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:Events row rwb.access.DoaLimitChanged.v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12252 | RWB-P7-E2013-APP | CG-ALL-7158 | 12.4 | Add rwb-decision as a consumer, and its ACL, for rwb.access.DoaLimitChanged.v1; the story's cache-refresh handler depends on it. |

### OTHER:RWB-P3 story (SCR-10 and SCR-11) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12257 | RWB-P7-E2013-APP | DOR-RWB-P7-E2013-APP-10 |  | Add empty, loading, error and no-access states to SCR-10 and SCR-11. |

### OTHER:RWB-P3 story (Criteria and tests) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12259 | RWB-P7-E2013-APP | DOR-RWB-P7-E2013-APP-7 |  | Replace legacy job and decision-log wording with the durable timer and the decision-record library. |

### OTHER:FSD P7 (A2.15; OTHER:A2.16) and rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12260 | RWB-P7-E2013-APP | GAP-1623 |  | Record that P3 moves the case state and raises the task on ApprovalRequested (preferred option) in the contract and FSD criteria. |

### RWB-P4-E1038-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12262 | RWB-P7-E2013-APP | GAP-0842 |  | Serve GET /doa-limits once from rwb-access; RWB-P4-AD016-APP owns the answer; drop the routing story claim to the path. |

### RWB-P4-E1037-CON; RWB-P7-E2013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12263 | RWB-P7-E2013-APP | GAP-1251 |  | State that the level lookup is a P4 read with a 2 s budget and that the approval stores delegation_limit_id, approval_level and limit_version only, with no join, view or foreign key into rwb_access. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12264 | RWB-P7-E2013-APP | GAP-1252 |  | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with its query (decision, regulation item, product, amounts, on-date) and answer fields. |

### RWB-P4-E1037-CON; RWB-P7-E2013-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12265 | RWB-P7-E2013-APP | GAP-1256 |  | Record the cache rule: version held in a local read-through cache, warmed before readiness, refreshed on DoaLimitChanged, effective date as switch, alert when cached version is older than in force. |

### OTHER:harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12266 | RWB-P7-E2013-APP | GAP-0397 | 3 | Route, harness and evidence held as harness-pack data |

### OTHER:TSD P4 v3 (T6.1 permission data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12269 | RWB-P7-E2013-APP | GAP-0930 |  | Add the rwb-decision service identity with Approval check R and no other Recovery right; confirm with the security administrator before the authorise contract is frozen. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-decision AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12270 | RWB-P7-E2013-APP | GAP-1221 |  | Add rwb-comms as a consumer of rwb.decision.ApprovalRequested.v1, which carries the raised escalation level and new due time; do not add an ApprovalEscalated event. |

### OTHER:rwb-comms contract review (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12271 | RWB-P7-E2013-APP | GAP-1222 | 3 | Notice and message operations, base path and field sets marked Not specified (GAP-1222) |

### RWB-P7-E2013-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12274 | RWB-P7-E2013-APP | GAP-0732 | find it | Record the approval event fields rwb-case reads, the task fields it writes, the escalation form, the status mapping, the composite field list and the rwb-case login. |

### RWB-P7-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12275 | RWB-P7-E2013-APP | GAP-1223 | find it | H = None plus the platform contracts of the DP table; C = RWB-P7-E2013-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON. |

### OTHER:TSD P7 v2 traceability table (T8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12277 | RWB-P7-E2013-APP | GAP-1263 | find it | Map the screen part of REQ-APD-002 and REQ-APD-006 to FEAT-APD-08 with RWB-E2-014; keep FEAT-APD-01 with RWB-E2-013 for routing. |

### OTHER:Edge and gateway design (gateway-bff) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12278 | RWB-P7-E2013-APP | GAP-1621 | 1 | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations, and record the four screen contracts there, not in the P7 PRD. |

### RWB-P7-E2013-CON; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12279 | RWB-P7-E2013-CON | DOR-RWB-P7-E2013-CON-14 | none | Record the signed epic design sign-off in the epic design record |

### OTHER:Recovery Workbench Reference Data and Lists of Values v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12281 | RWB-P7-E2013-CON | CG-ALL-7169 | 12 | Add list LOV-OVERRIDE-REASON to Lists; values not specified in the source documents (CG-ALL-7169) |

### OTHER:Platform edge and QA wave 2 entry record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12288 | RWB-P7-E2013-CON | GAP-0397 | find it | Route, environment, seeding, evidence and gate are agreed at wave 2 entry, not in this story. |

### OTHER:TSD P4 v3 T6.1 (permission data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12290 | RWB-P7-E2013-CON | GAP-0930 | find it | Add the rwb-decision service identity with Approval check R and no other Recovery right; security administrator to confirm before the authorise contract is frozen. |

### OTHER:rwb-comms contract (TSD P6 v2 notice and message operations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12292 | RWB-P7-E2013-CON | GAP-1222 | 12.1 | Confirm GET /notices/{noticeId} and POST /cases/{caseId}/messages on /api/recovery/comms/v1 with the Notice and MessageRequest field sets at rwb-comms contract review |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12294 | RWB-P7-E2013-CON | GAP-0732 | none | Fix the case-side approval and task fields, the approval-to-case status mapping, the escalation representation, the composite route and the rwb-case login at the RWB-P7-E2013-CON and RWB-PLT-N001-CON reviews |

### OTHER:TSD P6 v2 rwb-comms template catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12295 | RWB-P7-E2013-CON | GAP-1220 | find it | Load template row MSG-P7-011 with placeholders {decision} and {caseNo}, channel from LOV-CHANNEL (value Not specified in the source documents (GAP-1220)), status Approved, retry from RWB-PLT-TE006-CON outbox policy. |

### OTHER:Wave 3 contract freeze: rwb-document, rwb-comms, rwb-case and rwb-decision API contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12296 | RWB-P7-E2013-CON | GAP-2765 | 12.2 | Publish the pack and defect-list read, the notice and template-status read, the case read with route fact and task raise, the D7 approval raise, and the reference-data read of RWB-P3-E1043-CON, each one hop with 2 s budget, breaker and fake. |

### OTHER:TSD P7 v2, traceability table T8 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12300 | RWB-P7-E2013-CON | GAP-1263 | 18 | Map REQ-APD-002 and REQ-APD-006 to FEAT-APD-08 with RWB-E2-014 for the screen, and to FEAT-APD-01 with RWB-E2-013 for the routing, as the FSD keeps them. |

### OTHER:Edge and gateway design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12301 | RWB-P7-E2013-CON | GAP-1621 | find it | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations and which screen states this service owns; record the four screen contracts there. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20767 | RWB-P7-E2005-CON | R-22673 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-00541', 'R-00542', 'R-00544', 'R-00545', 'R-00546', 'R-00547', 'R-04736', 'R-04742', 'R-04751', 'R-22673', 'R-2 |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0387 | Harness repository, environments, seeding, evidence, gate and gateway route for the decision-log audit query harness | Integration lead | Resolved (directive) |
| GAP-0393 | Payment matching integration harness: composite proceeds and exception route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0394 | Credit approval pack integration harness: composite credit-pack route, harness environment, seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0395 | Booking confirmation integration harness: composite booking and treatment route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0396 | Gateway-bff composite transfer route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0397 | Approval-routing harness environment, composite queue route and evidence format are not specified | Integration lead | Resolved (directive) |
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
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0630 | The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source | Tech lead of rwb-agent | Resolved (directive) |
| GAP-0657 | rwb-integration booking confirmation (app slice): JOB-08 ownership and event consumer lists, the ACE read boundary, the consumed paths and shapes, the login, the package values and the MSG-P1-001 wording are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision; ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0658 | rwb-integration booking confirmation (contract slice): the JOB-08 ownership and consumer lists, the ACE read boundary, the rerun placement and the twelve consumed shapes are not settled by one source | Solution architect; contract owners of rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0659 | rwb-integration booking confirmation (deployment slice): the login and secret reference, the JOB-08 ownership, the alert thresholds, the runbook ownership and the backfill limit are not fixed by a source | DevOps engineer; platform administrator; platform workflow kit owner; business on-call owner for the package alerts | Resolved (directive) |
| GAP-0663 | rwb-integration credit approval pack: login, contract field names, NLEADS read, the ownership split, the integration-base resource placement and the approval-level values are not settled by any one source | Solution architect | Resolved (directive) |
| GAP-0710 | The partial-success shape of a selection and its summary message are not typed | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0711 | The at-cap and legal-hold pre-check answers have no typed shape | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0712 | Who may add or retire a transfer reason code is not specified | Centre of excellence; data steward | Resolved (directive) |
| GAP-0713 | The activity timeouts and the alert thresholds of the manual move are not specified | DevOps lead; service owner of rwb-case | Resolved (directive) |
| GAP-0729 | rwb-case credit approval: login, edge route and the NLEADS and treatment contract shapes are not specified | TechX | Resolved (directive) |
| GAP-0730 | rwb-case booking confirmation: login, composite route, treatment booking fields, match-result shape and route-rule evaluator owner are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
| GAP-0922 | rwb-access booking confirmation: the authorise request and answer shapes, the contract entry of the authorise path and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0923 | rwb-access booking confirmation: the TSD RBAC matrix has no Case record column, so the CASE_RECORD R and U letters the booking tasks need are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0924 | rwb-access booking confirmation: the lifetime of a cached authorise decision is not specified | Solution architect | Resolved (directive) |
| GAP-0925 | POST /authorise request and response shape is not specified for the payment-matching reads | Solution architect | Resolved (directive) |
| GAP-0926 | Permission letters for WRITE_OFF_AND_POSTING and TREATMENT_AND_OFFER and the scope of the Credit Administration role are absent from the RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0927 | The field that carries the filter and the row count in an AC-READ or AC-DENY entry is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0928 | GET /doa-limits is named in Architecture v5 and API v3 but absent from API Specification v4 | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0929 | The DoA lookup and authority-decision request and response shape is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0930 | The scope of the rwb-decision service identity inside rwb-access is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1220 | The template code, channel, notice kind, state vocabulary, retry limit, template owner and MSG-GEN-006 text of the escalation notice are not specified in any source | Solution architect | Resolved (directive) |
| GAP-1221 | The event catalogue lists gateway-bff as the only consumer of ApprovalRequested and carries no ApprovalEscalated event, yet this story also consumes the event for the escalation notice | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1222 | No source names the notice and message operations or the notice fields that carry an approval reference, an escalation level, a recipient and a sent time | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1229 | The paging defaults, the maximum page size and the full error body of the decision-log reads are unpublished | Contract owner of rwb-decision | Resolved (directive) |
| GAP-1242 | Audit export: a synchronous full-result CSV against a 2 s one-hop budget | Solution architect, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1246 | Approver index migration sits on a table created by another story | ACE team, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1247 | First-page performance target over 10,000 entries is assumed and not fixed | Solution architect, with the QA lead | Resolved (directive) |
| GAP-1248 | Element list of the audit answer beyond the legacy names, and the element that carries the warning | Solution architect, with the TechX lead of rwb-decision | Resolved (directive) |
| GAP-1249 | Message identifier of the 401 answer is not given by any source | Solution architect, with the platform library owner | Resolved (directive) |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1251 | The delegation of authority table is P4 rwb-access's while the routing rules and the approval resource are P7 rwb-decision | Solution architect | Resolved (directive) |
| GAP-1252 | The delegation limits operation has no row in the Ownership Map API catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1254 | The data lake copy of the decision record is removed under DP-17 while the legacy log path streams to it | Solution architect | Resolved (directive) |
| GAP-1255 | The request and answer field lists of the five approval operations and the case-status operation are not enumerated in any source | Tech lead of rwb-decision with the Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1256 | The delegation snapshot and its cache refresh have no named operation, store or interval | Solution architect | Resolved (directive) |
| GAP-1257 | ApprovalDecided is named on the service contract slide but has no event catalogue row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1263 | REQ-APD-002 and REQ-APD-006 are mapped to two different features and stories | Business analyst | Resolved (directive) |
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
| GAP-1621 | Four screens are attributed to P7 while the edge ruling composes every screen in gateway-bff | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
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
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1889 | The approval contract publishes no operation that raises an approval item, so the petition's take-to-the-approver shape has no owner | Solution architect, P7 rwb-decision, with the S4 rwb-litigation architect and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2180 | Two Work Packages of the same stage write the same story file for RWB-P1-E2008-APP | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2199 | RWB-E2-031 version 2 contract slice: the decision-log filter and override element, the notice operation, the name of the read right, the paging and member types, the route path, the login and the Schedule step names are not fixed by the sources | Tech lead of rwb-agent with the owners of rwb-decision, rwb-comms and rwb-access | Resolved (directive) |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2462 | The inner shape of the actions and outcome columns of a hand-over decision entry is not in any source | Solution architect with the data steward | Resolved (directive) |
| GAP-2464 | No source fixes the query parameters and paging of GET /decision-log | P7 contract owner | Resolved (directive) |
| GAP-2468 | The story line carries one C row and no H row while the pattern table adds six platform H rows and the guard | Coordinator of the realignment with the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-2500 | Transfer decision record and ledger read: the decision code, the MSG-P7-009 text, the answer element, the no-version answer and the DP-02 login name are not specified | P7 business analyst and solution architect, with the API specification owner | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2502 | Decision-record event naming and the boundary with RWB-P7-E1008-APP and RWB-P7-E2027-APP | P7 solution architect, with the event platform owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2504 | rwb-payment payment matching (contract slice): the element names of the nine consumed operations, the extra event payload fields, the operation the architecture lists and the ownership map does not, and the schema baseline of proceeds are fixed by no single source | Contract owner of rwb-payment, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the event platform | Resolved (directive) |
| GAP-2505 | rwb-payment payment matching (deployment slice): the login and secret reference, the replica and threshold values, the partition and retention values, the build ID policy, the backfill limit and the runbook ownership are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2689 | The treatment-side credit-result record has no operation, no element names, no state values and no column rule in the S2 sources | Solution architect, S2, with the rwb-treatment tech lead and the rwb-integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2690 | The rwb-treatment share of the key is stated by no S2 source, and the caller contract, the level comparison, the case move and the record ownership are split across four stories | Solution architect with the rwb-integration, rwb-treatment, rwb-case and rwb-access tech leads and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2692 | The rwb-treatment share of the key is stated by no S2 source, the P2 contract shapes it follows are unpublished, and the trigger, the task-raising and the event ownership are split across stories | Solution architect with the rwb-integration, rwb-treatment and rwb-case tech leads and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2693 | The delivery route of a match to rwb-treatment, the plan-position elements and the payment frequency of a plan are not specified for the S2 slice of RWB-E2-008 | Tech lead of rwb-treatment with the P8 rwb-payment owner, the P3 rwb-case owner and the P7 rwb-decision package owner at the wave 2 contract freeze | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2765 | No source publishes the four consumed surfaces the pack step needs: the pack and defect-list read of rwb-document, the notice and template-status read of rwb-comms, the case read with its task raise and route fact of rwb-case, and the D7 approval item of rwb-decision | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2771 | The legacy endpoint block gives the contract the notice approval operation, which the TSD places first in Epic 2 and which the ownership rows still list under rwb-litigation | Solution architect | Resolved (directive) |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3092 | The operation names and shapes of the consumed contracts other than RWB-P3-E2012-CON are not published | Solution architect | Resolved (directive) |
| GAP-3093 | The open-deviation read the P3 slice names is not a row of the Ownership Map, and the S8 event subscription already carries the same fact | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3095 | The event names of the case status and legal-hold changes this service consumes are not published | Solution architect | Resolved (directive) |
| GAP-3096 | deviation has no transfer reason, rule ID or rule-version column, and the legacy write set is on the rwb-case tables | Solution architect | Resolved (directive) |
| GAP-3098 | The fifteen legacy test case IDs of RWB-E2-012 are carried by both slices | QA lead | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P7-E2006-APP | unknown story key | 24 | RWB-P7-E2006-CON is not a story of the set: \| Contract dependencies \| RWB-P7-E2006-CON (not yet created; contract version: Not specified in the source documents (DOR-RWB-P7-E2006-APP-2 |
| RWB-P7-E2008-APP | new AC without TC row | 428 | AC10 is new and no section 16 row covers it |
