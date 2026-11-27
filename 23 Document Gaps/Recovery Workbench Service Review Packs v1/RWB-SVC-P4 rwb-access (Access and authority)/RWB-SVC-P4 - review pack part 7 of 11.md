# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 7 of 11 (RWB-P4-E2004-APP to RWB-P4-E2015-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 119 |
| Cross-document (pending in another document) | 198 |
| Not applied (value not in the sources) | 22 |
| Open business decisions | 35 |
| Register gaps linked | 151 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-E2004-APP | 21 | 31 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2004 APP Treatment entity and plan timers data model v2.md |
| RWB-P4-E2007-APP | 24 | 35 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2007 APP Booking confirmation from the ALS load v2.md |
| RWB-P4-E2008-APP | 15 | 50 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2008 APP Payment matching with the missed payment event v2.md |
| RWB-P4-E2013-APP | 17 | 24 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2013 APP Approval routing with the delegation of authority table v2.md |
| RWB-P4-E2014-APP | 21 | 34 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2014 APP Approval screen for D7.1 demand and recall notices v2.md |
| RWB-P4-E2015-APP | 21 | 22 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E2015 APP Timers, escalation and the deviation flag on the case record view v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E2008-APP | R-10717 | CG-ALL-5197 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E2015-APP | R-10727 | CG-ALL-5233 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E1034-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22079 | GAP-1606 | Register gap | Product owner with Legal counsel | It is not stated whether the approval is taken on a template version or on a generated notice | Record the Legal approval on the template version as a decision record written through rwb-decision, and take the notice approval for the demand and recall types through the approval workflow on the generated notice; state both in the story's acceptance criteria. |
| RWB-ITG-E2001-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2036-ITG, RWB-ITG-E4046-ITG, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-P2-E2007-OPS, RWB-P2-E2033-APP, RWB-P2-E2033-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P2-E4046-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2007-APP, RWB-P3-E2033-APP, RWB-P3-E2036-APP, RWB-P4-E2002-APP, RWB-P4-E2007-APP, RWB-P4-E2033-APP, RWB-P4-E2036-APP, RWB-P7-E2001-APP, RWB-P7-E2002-APP, RWB-P7-E2007-APP, RWB-P7-E2036-APP, RWB-P8-E4046-APP, RWB-S2-E2007-APP, RWB-S8-E2033-APP, RWB-S8-E2036-APP | R-22302 | GAP-1541 | Register gap | Product owner | The FSD P2 requirement set does not cover the consumer-side composition slices assigned to rwb-integration in waves 2 to 4 | The PRD covers the P2-owning requirements and the one wave-2 orchestration step it traces to REQ-DRI-013. The consumer-side compositions stay with the owning module PRDs and are carried as open question Q-P2-06. |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E1038-APP, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22353 | GAP-0919 | Register gap | Business lead | Which delegation limit version is in force on the approval date of a treatment is a data state, not a document value | Decide the version in force per environment at the DoA load (RWB-P4-E1038-APP) and keep it out of code; the lookup always answers the version whose window covers the date asked, and the answer names it |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22357 | GAP-0704 | Register gap | Data product owner | The 01:30 treatment extract has no owner in the target and its DP04 read path and freshness element are not in the Ownership Map | Record the owner of the treatment extract as P9 rwb-reporting on JOB-15 with the DP04 copy in rwb_source_data, publish the case-facing read GET /api/recovery/source-data/v1/data-products/DP04/records with its freshness element in the Ownership Map and the P1 API file, and state in the event catalogue that the copy is built from the treatment events. |
| RWB-ITG-E2008-ITG, RWB-P1-E1015-APP, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22404 | GAP-0600 | Register gap | Solution architect with the P1 data product owner | FSD P1 A2.2 stamps a payment read on DP01 Account and arrears while the Work Package slice note names DP05, and no source states whether the read or the rwb-payment run answers a held business date | Hold both gates on DP01 Account and arrears and answer 409 with MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run, with no row of any kind; record DP05 as not the stamp of a payment read and correct the slice note in the Work Package and the data product map in the next version of FSD P1 A2.2; state in RWB-P8-E2008-CON that the run's own refusal for the business date is its own and that the read's 409 is the answer to a call made anyway. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22414 | GAP-1630 | Register gap | Finance and CFO delegate | The posting file has no layout, no schedule and no receiving ledger in any source | Fix one line per posting with case, account key, entry type, amount, value date, business date and posting reference, a manifest with count and checksum, and delivery through rwb-integration. Agree the layout with Finance and the ledger owner before wave 3. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22415 | GAP-1632 | Register gap | Business lead | A reversed payment has no product behaviour in the FSD although the routing rules require the case to reopen | Decide whether a reversal is in scope for this service. If it is, add a reversal source value, a reversal state on the proceeds record and an event that reopens the case through rwb-case. Until then the capability is out of scope and listed as an open question. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22416 | GAP-1633 | Register gap | Finance and CFO delegate | The fee tables that the fee feature reads are not defined anywhere | Name the fee table, its owner and its schedule, and hold the fee rate, the cap and the basis as versioned rows. Until then the fee calculation has no input and the feature cannot be tested. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22419 | GAP-1636 | Register gap | Finance and CFO delegate | The order in which a receipt is applied to the balance is named but not specified | Hold the application order as versioned rows with an owner and a valid-from date, record the version on each proceeds row, and let Finance set the sequence before wave 3. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22463 | GAP-1616 | Register gap | Risk and model risk officer with the rwb-access owner | The delegation of authority table is loaded and approved inside P7 while the ownership ruling gives the table to rwb-access | Keep in this service only the lookup at the moment of the decision and the recording of the row ID and version; move A2.24 with AC-P7-024-01 to AC-EXC-P7-024-05 to rwb-access, and confirm the lookup answer shape (level, row ID, version, NOT_COVERED, RELATED_PARTY reason) in the access contract. Until then this PRD reads the limits and records the version, and OQ-P7-05 stays open. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22470 | GAP-1253 | Register gap | Business lead with the Center of excellence | The escalation ceiling and the service level values of an approval are not specified | Fix three values as data owned by RW-COE: the service level per decision and per default, the escalation step in working days, and a maximum escalation count with its ceiling behaviour (hold, incident to RW-RISK, or committee). Carry them as rwb.approval.service-level.*, rwb.approval.escalation.step and rwb.approval.escalation.max-levels and close DL22. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22482 | GAP-0931 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masked rendering of the addressee postal address is not specified | Let the platform masking library own one rendering per field type, record it as data beside the masking row, and add the postal address rendering to the MASK-SIT-01 pack before the first SIT run of the approval screen |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22483 | GAP-1260 | Register gap | Business lead | The limit that applies on the approval screen conflicts with D7.1 carrying no amount limit | Show the approval level and the route role as the limit that applies for D7.1 (no amount, level none) and read the DoA table only where an amount-bearing decision uses the screen; confirm with Risk and Credit. |
| RWB-ITG-E2014-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22495 | GAP-1269 | Register gap | Compliance and PDPA officer | No source enumerates the mask flags of the screen fields | Declare a mask flag of NONE, PARTIAL or FULL with a policy key on every field of the two panels, PARTIAL for the postal address, and confirm the policy keys with the masking owner (P4). |
| RWB-ITG-E2015-ITG, RWB-ITG-E7006-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON | R-22499 | GAP-1827 | Register gap | Business lead | The deviation service level is 'set with DL22' and has no number, and the ten working day escalation comes only from the design | Carry the service level, the escalation period and the skip trace window as versioned reference data read at run time, assert no number, and take the values from DL22 when the business lead sets them. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22503 | GAP-0935 | Register gap | Business lead | Precedence between a role's default scope and an escalation grant is not specified | Rule that the wider of the two scopes is named, that the reason ESCALATED_TO_ROLE is carried while the escalation is open, and that the grant never exceeds Case record R on that one case. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22504 | GAP-0936 | Register gap | Compliance and PDPA officer | The masking version in force for SIT and the answer when two versions overlap are not specified | Record MASK-SIT-01 as the SIT version in the policy pack, and rule that the version with the latest valid_from on or before the business date is used, the answer naming the version it used. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22506 | GAP-3099 | Register gap | Solution architect, with the rwb-deviation owner, the rwb-case contract and reference-data owners, the product owner of the deviation service level, the rule-set owner of the Deviations package and the QA lead | RWB-S8-E2015-APP: the deviation section of the case record view has no read operation, no published view field names, no label for a code other than X3, no published value for the deviation service level and no escalation target | Publish the case deviation read as a service operation with a catalogue row, or amend the Ownership Map to carry GET /cases/{caseId}/deviations; freeze the deviation view field names in RWB-P3-E2015-CON; publish LOV-DEVIATION with a label per code and LOV-DEV-OUTCOME with a label per value; publish the deviation service level, its calendar and the row that holds it; publish the escalation target and the codes R-DEV-20 covers; record the six platform contracts as template dependencies of S8 beside the H row of the secondary slice; publish a level for each legacy test case. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-28740 | GAP-1638 | Register gap | Product owner | The only success measure of the module has no baseline and no measurement definition | Take the measure from the decision log as the FSD says, and have the product owner set the baseline, the target and the definition of 'the same day' before the wave-2 release note. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28769 | GAP-0933 | Register gap | Compliance and PDPA officer with the P4 build squad | The masking version in force in SIT is not recorded anywhere | Record the masking version in force per environment in the policy pack load record, with its approver and valid-from date, and assert it in the SIT entry check |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28770 | GAP-1261 | Register gap | Data steward and data product owner | The module specification keeps two daily data-lake interfaces that DP-17 removes | Retire INT-19, INT-20 and the daily copy from the P7 documents in the next module-specification version; no lake element appears in this key's stories, chart or run book. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |
| RWB-P4-E2004-APP | R-36708 | ASM-1641 | Register assumption |  | The delegation lookup answers against the limit version whose valid_from is not after the approval date and whose valid_to is empty or not before it, and names that version in the answer; DOA-2026.11 is the version loaded in SIT from 30 November 2026, and no code holds a version label. | Business lead and the DoA load owner at the RWB-P4-E1038-APP acceptance |
| RWB-P4-E2014-APP | R-36724 | ASM-1657 | Register assumption |  | The masked rendering of the addressee postal address is left to the one platform masking library and is not fixed by this story; the story asserts only that the field is marked masked, that the mask version is named, and that no value of the address appears in the answer or the access-log entry. | Compliance and PDPA officer, at the masking pack review |
| RWB-P4-E2014-APP | R-36725 | ASM-1658 | Register assumption |  | The masking version in force for SIT is MASK-SIT-01, as the two FSD examples name it; the story reads the version from the masking rows at run time and configures no version. | Compliance and PDPA officer with the P4 build squad, at the SIT entry check |
| RWB-P4-E2015-APP | R-36727 | ASM-1661 | Register assumption |  | When the caller's own scope and an escalation grant both admit the case, the answer names the wider scope and carries the reason ESCALATED_TO_ROLE while the escalation is open. | Business lead with the access policy owner |
| RWB-P4-E2015-APP | R-36728 | ASM-1662 | Register assumption |  | MASK-SIT-01 is the masking version in force for the SIT environment, and the version whose valid_from is the latest on or before the business date is the version an answer uses. | Compliance and PDPA officer at the policy pack load |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-E2004-APP | R-05774 | DOR-RWB-P4-E2004-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design reference is in the story parts or the sources searched. Writing one would invent a value. |
| RWB-P4-E2004-APP | R-05778 | DOR-RWB-P4-E2004-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version is in the story parts or the sources searched. Writing one would invent a value. |
| RWB-P4-E2004-APP | R-25450 | CG-ALL-5165 | 3, 3.1 | Flyway file V2004_1__treatment_access_decision.sql is not in the V0001..Vnnnn form | Migration name is at story line 397, outside the supplied parts. The next number of the rwb-access Flyway sequence is not in the sources; only the monolith V0001 is found. |
| RWB-P4-E2004-APP | R-30917 | NEWAC-RWB-P4-E2004-APP-AC17 | 7, 16 | AC17: replay of a write with the same idempotency key (no criterion covers a replay) | The idempotency key field, the replay outcome and the proposed test are Not specified in the source documents. A new AC would invent them. |
| RWB-P4-E2007-APP | R-16763 | DOR-RWB-P4-E2007-APP-10 | 9-10 | Definition of Ready item 10 Screens and states: Partial | Screen state text for SCR-01, SCR-14, SCR-29 is in sections 9-10, which are not in this chunk. No exact old text to edit. Re-issue with those sections. |
| RWB-P4-E2007-APP | R-25457 | CG-ALL-5181 | 3, 3.1 | Flyway file V2007_1__authorise_decision.sql is not in the V0001..Vnnnn form | Next Vnnnn of the rwb-access Flyway sequence is not in the sources (DP-15 says per-service only). Migration file name is not in this chunk either. Not specified in the source documents (CG-ALL-5181). |
| RWB-P4-E2008-APP | R-05788 | DOR-RWB-P4-E2008-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design sign-off in the story or the source documents; the epic design record was not found in the workspace. Not specified in the source documents (DOR-RWB-P4-E2008-APP-14). |
| RWB-P4-E2008-APP | R-16768 | DOR-RWB-P4-E2008-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | Screen-state text for SCR-04, SCR-14 and SCR-28 is not in the supplied story parts, so no exact old text can be copied. Needs the section holding those screens. |
| RWB-P4-E2008-APP | R-16769 | DOR-RWB-P4-E2008-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The personal-data field is named in neither detcheck nor the story text. Not specified in the source documents (DOR-RWB-P4-E2008-APP-11); the data owner must name it. |
| RWB-P4-E2008-APP | R-16771 | DOR-RWB-P4-E2008-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Criteria for BR3, BR7, BR8, BR10 belong in section 7 and test rows in section 16; neither section is in the chunk, so no anchor exists. Not edited. |
| RWB-P4-E2008-APP | R-25464 | CG-ALL-5198 | 3.1 | Flyway file V2008_1__access_payment_matching.sql is not in the V0001..Vnnnn form | Next free number of the rwb-access Flyway sequence is in no source found (Service Template Specification v1 §3.1 gives only the V0001 form). File name at line 338 is outside the chunk. Not renamed. |
| RWB-P4-E2008-APP | R-28738 | GAP-1353 |  | RWB-E2-008: no source fixes a numeric target for the outbox-lag, dead-letter or workflow-failure alerts of rwb-payment | No numeric target exists in any source. NFR and alert text is outside the chunk, so the no-default values file rule cannot be placed. No threshold written. |
| RWB-P4-E2008-APP | R-28744 | GAP-2498 | 7, 16 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept, and the legacy levels have no counterpart in the template | Covers column and System-to-Component and Access-to-Contract mapping sit in sections 7 and 16, which are not in the chunk. No edit made. |
| RWB-P4-E2013-APP | R-23045 | GAP-0971 | 7 | The rollback of a delegation version has no acceptance criterion, business rule or window semantics | Section 7 and 16 text is not in this chunk, so no exact anchor exists to add the rollback AC or its TC row. Rerun with those parts. |
| RWB-P4-E2014-APP | R-05801 | DOR-RWB-P4-E2014-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in the story or the sources searched. Sign-off must come from the epic design record, which is not in this chunk. |
| RWB-P4-E2014-APP | R-05804 | DOR-RWB-P4-E2014-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version is recorded as published in any source read. Writing one would invent a value. |
| RWB-P4-E2014-APP | R-05805 | DOR-RWB-P4-E2014-APP-23 | 3 | Definition of Ready item 23 Contract version fixed: Fail | No version for RWB-P7-E2014-CON or RWB-P4-E1037-CON in the story or sources (only the /v1 path). Value not specified. |
| RWB-P4-E2014-APP | R-25475 | CG-ALL-5219 | 3.1 | Flyway file V2014_1__access_authorise_indexes.sql is not in the V0001..Vnnnn form | Next rwb-access Flyway number is not in Service Template Specification v1 (V0001 to Vnnnn only) or the story. Migration row is outside this chunk. |
| RWB-P4-E2015-APP | R-05807 | DOR-RWB-P4-E2015-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design sign-off in the story or a repo-wide Grep of the .md sources. The record is outside the sources. Nothing invented. |
| RWB-P4-E2015-APP | R-05810 | DOR-RWB-P4-E2015-APP-22 | find it | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in repo .md sources (Grep). Cannot be recorded until the contract team publishes it. Nothing invented. |
| RWB-P4-E2015-APP | R-16787 | DOR-RWB-P4-E2015-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | The P2 field classed as personal data is not named in the story or the Detail, so it cannot be identified. No classification invented. |
| RWB-P4-E2015-APP | R-25482 | CG-ALL-5234 | 3, 3.1 | Flyway file V2015_1__access_decision_read_path.sql is not in the V0001..Vnnnn form | Next free V-number in the rwb_access Flyway sequence is not in the sources. Grep found only P1 engine V0001/V0002 names. Section 3.1 is outside this chunk. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08561 | RWB-P4-E2004-APP | CG-ALL-5159 | find it | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as data without a code change. |
| CDC-08564 | RWB-P4-E2004-APP | DOR-RWB-P4-E2004-APP-8 | 12.1 | Add paths POST /api/recovery/access/v1/authorise, GET /api/recovery/access/v1/doa-limits and GET /api/recovery/access/v1/me/permissions; hold defaultScope as LOV-SCOPE data, not a closed enum. |
| CDC-08589 | RWB-P4-E2007-APP | CG-ALL-5170 | 12.1 | Publish POST /api/recovery/access/v1/authorise through the owner's CON story, or remove the operation from section 12.1. |
| CDC-08590 | RWB-P4-E2007-APP | CG-ALL-5171 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions through the owner's CON story, or remove the operation from section 12.1. |
| CDC-08591 | RWB-P4-E2007-APP | CG-ALL-5172 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies through the owner's CON story, or remove the operation from section 12.1. |
| CDC-08593 | RWB-P4-E2007-APP | CG-ALL-5174 | 13 | Remove the closed enum on defaultScope; LOV-SCOPE is data read through the reference-data contract, as section 13 ReferenceCatalog already states. |
| CDC-08596 | RWB-P4-E2007-APP | DOR-RWB-P4-E2007-APP-8 | 12.1 | Add paths POST /authorise, GET /me/permissions and GET /masking-policies; hold defaultScope as LOV-SCOPE data, not as a closed enum. |
| CDC-08625 | RWB-P4-E2008-APP | CG-ALL-5190 | 2 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are accepted as data (the story reads them as data, per the ruling). |
| CDC-08626 | RWB-P4-E2008-APP | CG-ALL-5191 | 2 | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as data (the story reads them as data, per the ruling). |
| CDC-08698 | RWB-P4-E2014-APP | CG-ALL-5211 | 12.1 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the CON story for RWB-P4-E1037-CON |
| CDC-08699 | RWB-P4-E2014-APP | CG-ALL-5212 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions in rwb-access.yaml through the CON story for RWB-P4-E1037-CON |
| CDC-08700 | RWB-P4-E2014-APP | CG-ALL-5213 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through the CON story for RWB-P4-E1037-CON |
| CDC-08701 | RWB-P4-E2014-APP | CG-ALL-5214 | 2 | Remove the fixed enum on defaultScope so that LOV-SCOPE values are accepted as data |
| CDC-08702 | RWB-P4-E2014-APP | DOR-RWB-P4-E2014-APP-8 | 11 | Add POST /api/recovery/access/v1/authorise with Idempotency-Key, GET /api/recovery/access/v1/me/permissions and GET /api/recovery/access/v1/masking-policies; read LOV-SCOPE as data, not a closed defaultScope enum. |
| CDC-08732 | RWB-P4-E2015-APP | CG-ALL-5227 | 4 | Remove the closed enum on defaultScope so LOV-SCOPE values are read as data and a new list value passes schema validation. |
| CDC-08733 | RWB-P4-E2015-APP | DOR-RWB-P4-E2015-APP-8 | find it | Replace the closed enum on defaultScope with a reference to LOV-SCOPE, read as data. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08575 | RWB-P4-E2004-APP | GAP-0703 | 5 | Add rwb-case to the consumer list of rwb.treatment.TreatmentApproved.v1; confirm in wave 2 architecture review that treatment is S2's and rwb-case holds the timer in CaseWorkflow |
| CDC-08598 | RWB-P4-E2007-APP | CG-ALL-5175 | 12.3 | Specify the payload of rwb.access.AccessPolicyChanged.v1 (catalog row 'new', Events): currently Not specified in the source documents (GAP-0127; ASM-0204). Then align RWB-P4-E2007-APP section 12.3 to it. |
| CDC-08601 | RWB-P4-E2007-APP | GAP-3175 |  | List AceDataReady (EV-26) on rwb.source-data.events.v1 with LoadCompleted as its legacy alias. |
| CDC-08630 | RWB-P4-E2008-APP | CG-ALL-5192 | 12.3 | Specify the rwb.access.AccessPolicyChanged.v1 payload as roleCode, capabilityArea, matrixVersion and validFrom, IDs and facts only, as in RWB-P4-E2008-APP section 12.3. |
| CDC-08677 | RWB-P4-E2013-APP | DOR-RWB-P4-E2013-APP-8 | 12.3 | Specify the payload of rwb.access.AccessPolicyChanged.v1 (gap-0127, asm-0204). |
| CDC-08678 | RWB-P4-E2013-APP | CG-ALL-5203 |  | Specify the payload of rwb.access.AccessPolicyChanged.v1 as the changed policy reference: table, version, change kind, no personal data. |
| CDC-08689 | RWB-P4-E2013-APP | GAP-1221 |  | Add rwb-comms as consumer of rwb.decision.ApprovalRequested.v1 (escalation level raised, new due time) in the catalogue and in the rwb-decision AsyncAPI document; do not add ApprovalEscalated; keep TimerBreached as legacy reference. |
| CDC-08692 | RWB-P4-E2013-APP | GAP-1257 |  | Record the absence of ApprovalDecided in the baseline until the catalogue gains a row with number and consumers, or the topic list on Architecture v5 slide 14 drops it; DecisionRecorded stays the outcome event. |
| CDC-08705 | RWB-P4-E2014-APP | CG-ALL-5215 | 12.3 | Define the payload of rwb.access.AccessPolicyChanged.v1 in the Events row (new) as: policy kind, old and new version, validFrom, affected capability areas or fields, load reference. |
| CDC-08739 | RWB-P4-E2015-APP | CG-ALL-5228 | 12.3 | Specify the payload of rwb.access.AccessPolicyChanged.v1 (gap-0127; asm-0204), then align story section 12.3 to it. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08629 | RWB-P4-E2008-APP | CG-ALL-5187 | 13 | Record ck_permission_letters_known as a check on permission.letters under its dictionary name, or name the owning index or library object. |
| CDC-08666 | RWB-P4-E2008-APP | GAP-0927 | find it | Add capability area and right to the decision-record actions list in the next LDM version; carry filter and row count in that list. |
| CDC-08703 | RWB-P4-E2014-APP | CG-ALL-5209 | 1, 11 | Record value_token as the field of contact_point holding the postal address over v_ace_contact.contact_value, or record the object in LDM v9 and Data Classification v5. |
| CDC-08704 | RWB-P4-E2014-APP | CG-ALL-5210 | 1, 11, 12.7, 17 | Record contact_point as the P1-owned entity read through the DP-05 owner contract, or record the object in LDM v9 and Data Classification v5. |
| CDC-08706 | RWB-P4-E2014-APP | DOR-RWB-P4-E2014-APP-7 | 11 | Add DF-PTY-016 and DF-REF-039 to LDM v9 or give their current LDM IDs; add contact_point and its value_token field to LDM v9 or Data Classification v5. |
| CDC-08714 | RWB-P4-E2014-APP | GAP-2385 | find it | Add nullable decision_log_entry_id uuid to notice in rwb_comms with a unique index, written by approve and hold and null when no approval moved the notice; add the field to the rwb_comms logical data model before wave 2 build. |
| CDC-08742 | RWB-P4-E2015-APP | DOR-RWB-P4-E2015-APP-7 | 11 | Register DF-REF-039 in LDM v9; confirm id_no_token and value_token as LDM v9 or Data Classification v5 field names. |

### RWB-P2-E2007-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08603 | RWB-P4-E2007-APP | GAP-0597 | 12, 12.1 | Publish GET /batch-status with key pair sourceSystem and businessDate and six values status, isComplete, startedAt, completedAt, recordCount and feedVersion; answer 404 with MSG-P1-001 when no batch row exists; state that this gate read is distinct from the freshness reads of RWB-P1-E1015-APP; add the operation to the next API Specification version. |
| CDC-08604 | RWB-P4-E2007-APP | GAP-0594 | 11, 12 | Publish GET /booking-facts and GET /batch-status on base /api/recovery/source-data/v1 with BookingFact, BookingFactsAnswer, FieldState and BatchStatusAnswer and the section 11 property names of RWB-P1-E2007-APP; keep the freshness element as DataProductFreshness of RWB-P1-E1015-CON; add both operations to the next API Specification version. |
| CDC-08605 | RWB-P4-E2007-APP | GAP-0595 | 4 | Declare the case account set source: read the account set and product group from this service's case_list_row for the case and business date; if not accepted, add C dependency RWB-P3-E1018-CON and declare GET /api/recovery/case/v1/cases/{caseId}/accounts; rwb_case.case_account is not read. |
| CDC-08610 | RWB-P4-E2007-APP | GAP-0598 | 4, 12, 13 | Fix the account answer as account facts only, with no treatment term, outcome, difference, tolerance or package version; state that BookingMatchFacts is built by the calling slice; add a contract test that fails on any outcome-shaped field. |
| CDC-08611 | RWB-P4-E2007-APP | GAP-0658 | 13 | Baseline the contract with the result shape, task table, envelope statement, rerun operation, twelve consumed operations and seven fakes; record the JOB-08 ownership and the supersession of TSD P2 Integration v3 T5.2 in the gap register; confirm the seven message texts in the catalogue. |
| CDC-08613 | RWB-P4-E2007-APP | GAP-0730 | 3, 4, 15 | Publish the rwb-case per-service login; the gateway-bff composite route field list, hop list and masking detail; the rwb-treatment booked-terms field list; and the raiseTask result schema. |

### RWB-P8-E2008-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08636 | RWB-P4-E2008-APP | GAP-1346 | 12.2 | Operation names and payloads stated as Not specified in the source documents |
| CDC-08647 | RWB-P4-E2008-APP | GAP-1350 |  | Publish one OpenAPI 3.1 and one AsyncAPI document per service, problem+json on every non-2xx status, MatchRequest with proceeds identifier, case, treatment, account payment and reason code, next Flyway number, major version 1 with BACKWARD acceptance. |
| CDC-08657 | RWB-P4-E2008-APP | GAP-2494 |  | Fix one DecisionRecorded shape and consumer group, take decision codes from LOV-DECISION, carry inputs_ref as an opaque reference, keep the input age limit key as a placeholder read through DP-06, publish the page default with the read. |
| CDC-08658 | RWB-P4-E2008-APP | GAP-2504 |  | Publish v1 with the two operations, three event schemas, nine declarations, schema baseline and message map; mark unsettled elements with the placeholder and one review row; gate the tag on contract tests and schema lint. |
| CDC-08660 | RWB-P4-E2008-APP | GAP-2693 |  | Apply ProceedsMatched and PaymentMissed through the inbox of rwb-treatment, name activities applyProceedsMatched and holdMissedInstallment, and serve the plan position in the treatment read; confirm package and frequency at contract freeze. |
| CDC-08661 | RWB-P4-E2008-APP | GAP-1347 |  | Publish the three event schemas with the data fields named per event and the platform CloudEvents envelope; keep the decision-record element with its library owner; require a new schema version for any added business field. |

### RWB-P4-E1037-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08563 | RWB-P4-E2004-APP | DOR-RWB-P4-E2004-APP-21 | Contract dependencies row | Removed RWB-P4-E2004-CON from the Contract dependencies row |
| CDC-08644 | RWB-P4-E2008-APP | GAP-0925 |  | Extend the envelope with area, right, scope, resource, filter, rowCount and matrixVersion, and fix the three answer codes (allow, refuse by right, refuse by scope) at the wave 2 contract review. |
| CDC-08684 | RWB-P4-E2013-APP | GAP-1256 |  | Record the rule: warm read-through cache of the delegation version at start before readiness, refresh on DoaLimitChanged, effective date as the switch, alert when cached version is older than version in force. Mirror in RWB-P7-E2013-OPS. |
| CDC-08709 | RWB-P4-E2014-APP | GAP-0932 | find it | Publish the authorise, me-permissions and masking-policies request and response shapes; reconcile GET /me/session with GET /me/permissions; state whether the routed role or the holder is a request field. |
| CDC-08746 | RWB-P4-E2015-APP | GAP-0934 | none | Fix the authorise request with caseId, teamCode, ownerUserRef, escalatedToRole and escalatedAt as v1 with BACKWARD compatibility. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08583 | RWB-P4-E2004-APP | CG-ALL-5164 | 18 | Reconcile the four requirement test lists with section 18 of RWB-P4-E2004-APP in the next version; RTM lists include other story keys' test cases |
| CDC-08617 | RWB-P4-E2007-APP | CG-ALL-5180 | 18 | Align the REQ-CHO-008 test list with RWB-P4-E2007-APP section 18 (TC-E2-007-01 to TC-E2-007-12) in the next RTM version. |
| CDC-08632 | RWB-P4-E2008-APP | DOR-RWB-P4-E2008-APP-12 | 16, 18 | Reconcile the test case lists for REQ-CHO-007 and REQ-CHO-009 with section 18 of RWB-P4-E2008-APP. |
| CDC-08724 | RWB-P4-E2014-APP | CG-ALL-5218 | 18 | In the next RTM version align the REQ-APD-002 and REQ-APD-006 test lists with section 18 of RWB-P4-E2014-APP. |
| CDC-08750 | RWB-P4-E2015-APP | CG-ALL-5232 | 18 | Align the test lists of REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 and REQ-DRI-001 with RWB-P4-E2015-APP section 18 in the RTM's next version. |

### RWB-P7-E2014-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08716 | RWB-P4-E2014-APP | GAP-2387 |  | Baseline the notice answer fields: id, caseId, documentId, noticeType, state, templateCode, templateVersion, templateState, approvedAt, decisionLogEntryId; template state values DRAFT, APPROVED, WITHDRAWN. |
| CDC-08720 | RWB-P4-E2014-APP | GAP-1258 |  | Publish the field list and mask flags of the two approval panels as the working read, confirmed with route owner and consumer sign-offs. |
| CDC-08721 | RWB-P4-E2014-APP | GAP-1259 |  | Carry GET /api/recovery/approvals/{approvalId} as the working read and register it with the route owner at the first version freeze. |
| CDC-08722 | RWB-P4-E2014-APP | GAP-1267 |  | Keep READY, STALE_INPUT, DECIDED, GENERATED, APPROVED, HELD as panel states; treat loading, temporarily unavailable and session expired as route overlay states. |
| CDC-08728 | RWB-P4-E2014-APP | GAP-1266 |  | Publish field types of the approval screen model and queue paging defaults: page size default 20, maximum 100. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08597 | RWB-P4-E2007-APP | GAP-1696 | 12.2 | Obtain every source fact through the rwb-source-data contract; add S2 to the P1 REST cell of the connection matrix; S2 reads no ACE view or table. |
| CDC-08654 | RWB-P4-E2008-APP | GAP-1640 |  | Keep one matching run per business date in wave 2; record the payment-received same-day trigger as an open question; add an intraday run only when an interface carrying a payment in the day is named. |
| CDC-08708 | RWB-P4-E2014-APP | GAP-2093 | find it | Remove 'Decision: child: approval' from the P6 OUT list on slide 17; hold approval in P7 ApprovalWorkflow as child of NoticeDispatchWorkflow with the notice as source; S4 POST /notices/{noticeId}/approve stays the decision point; notice waits in Approved and is not written to the file. |
| CDC-08727 | RWB-P4-E2014-APP | GAP-1262 | find it | Retire ApprovalDecided from the rwb.decision.events.v1 line or add it to the catalogue with consumers; decided outcome stays on rwb.decision-record.v1 via DP-03. |

### RWB-P7-E2013-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08675 | RWB-P4-E2013-APP | DOR-RWB-P4-E2013-APP-21 |  | Publish the contract and confirm it as the contract dependency. |
| CDC-08680 | RWB-P4-E2013-APP | GAP-1623 | find it | Record that P3 moves the case state and raises the approval task on ApprovalRequested, and state that in A2.15 and A2.16. |
| CDC-08691 | RWB-P4-E2013-APP | GAP-1255 |  | Baseline the five approval resources and the case-status operation from TSD P7 T3.1 field names in camelCase with page and error conventions; fix the required properties of ApprovalAction; map case-status to an operation or event in the Ownership Map. |
| CDC-08693 | RWB-P4-E2013-APP | GAP-0732 |  | Fix at contract review with RWB-PLT-N001-CON: approval event fields consumed by case, task fields written (approval and preparer references), escalation representation, approval-to-case status mapping, composite route field list, rwb-case login name from ACE DB naming. |

### RWB-P4-E1037-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08558 | RWB-P4-E2004-APP | CG-ALL-5155 | 12.1 | Publish POST /api/recovery/access/v1/authorise in the paths of rwb-access.yaml. |
| CDC-08559 | RWB-P4-E2004-APP | CG-ALL-5156 | 12.1 | Publish GET /api/recovery/access/v1/doa-limits in the paths of rwb-access.yaml. |
| CDC-08560 | RWB-P4-E2004-APP | CG-ALL-5157 | 12.1 | Publish GET /api/recovery/access/v1/me/permissions in the paths of rwb-access.yaml. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08565 | RWB-P4-E2004-APP | GAP-2474 | 8 | Add a P7 row for GET /api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion= before the wave 2 baseline tag; state that the entry read is API-P7-007 of RWB-P7-E2005-APP. |
| CDC-08579 | RWB-P4-E2004-APP | GAP-1698 | 13 | Add rows for the treatment contracts, settlement and deed-in-lieu agreements and plan timers under rwb-treatment, owner S2, schema rwb_treatment |
| CDC-08748 | RWB-P4-E2015-APP | GAP-0714 | none | Add GET /cases/{caseId}/deviations to the S8 rows of Ownership Map v1 and to the S8 API file. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08566 | RWB-P4-E2004-APP | CG-ALL-5161 | 16 | Add rows TC-E2-004-15 (AC2) and TC-E2-004-16 (AC7) with Given, When and Then copied from AC2 and AC7 in the next version. |
| CDC-08599 | RWB-P4-E2007-APP | CG-ALL-5178 | 16 | Add row TC-E2-007-11 with Given, When and Then copied from criterion AC8. |
| CDC-08631 | RWB-P4-E2008-APP | CG-ALL-5194 | 16 | Add a row for TC-E2-008-10 with Given, When and Then copied from its criterion in the next version. |

### RWB-P8-E2008-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08569 | RWB-P4-E2004-APP | GAP-2503 | find it | Declare the nine consumed operations on per-service bases (one hop, 2 s timeout); name workflow matchPayments and its four activities; record in the RTM that legacy AC1, AC3, AC4 and AC5 are carried by no story. |
| CDC-08570 | RWB-P4-E2004-APP | GAP-1346 | find it | Name the seven consumed rows in section 12.2 with a placeholder until each owner publishes its operation; keep the plan H, C, I and X rows; confirm with the solution architect the scope of RWB-P3-E2004-CON, RWB-P3-E2042-CON and RWB-P7-E1073-CON. |
| CDC-08653 | RWB-P4-E2008-APP | GAP-1635 |  | Reconcile the daily money check to the ACE payment and account position and the posting file this service delivered; record any ledger return as an open question until the ledger owner publishes one. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08573 | RWB-P4-E2004-APP | GAP-0918 | 12.1 | Add API-P4-022 GET /doa-limits with the request and answer fields of section 12.1 and the outcome value set; RWB-P4-E2013-APP consumes it |
| CDC-08682 | RWB-P4-E2013-APP | GAP-0918 | find it | Add API-P4-022 GET /doa-limits with the request and answer fields of section 12.1 and the outcome value set. |
| CDC-08686 | RWB-P4-E2013-APP | GAP-0928 |  | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with the query and response fields this story uses, per Architecture v5 slides 14 and 41. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08576 | RWB-P4-E2004-APP | GAP-1341 | 12 | Record the legacy TimerScheduler, JOB-05 and TimerDue wording as superseded by Architecture v5 slides 42 and 44; the plan timer is a durable workflow timer |
| CDC-08587 | RWB-P4-E2004-APP | GAP-2476 | find it | Record how INSTALLMENT_DUE and CURE_PERIOD timers running at cut-over carry into the owning workflow; remove legacy steps 7 and 14 and AC2, AC12, AC14 timer assertions from the target tests |
| CDC-08608 | RWB-P4-E2007-APP | GAP-2485 | 13 | Record that this slice evaluates BOOKING_MATCH on the version it holds through the embedded kit and publishes the outcome; treatment state, task, route move and posting stay with their owners; restate the boundary of RWB-P7-E2042-APP once. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08600 | RWB-P4-E2007-APP | DOR-RWB-P4-E2007-APP-9 | 14 | Confirm the MSG-P2-011 wording against the standard and align the text in the standard or the owning rwb-integration slice; this story keeps its unchanged copy. |
| CDC-08668 | RWB-P4-E2008-APP | GAP-1637 | find it | Publish wording, Thai text, channel and blocking flag for MSG-P8-001 and MSG-P8-002. |
| CDC-08740 | RWB-P4-E2015-APP | CG-ALL-5230 | 14 | Add a new message ID for 'Two roles of the caller conflict' with text '{role} may not be held together with {role}.'; the story then cites it. |

### RWB-P6-E1052-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08710 | RWB-P4-E2014-APP | GAP-1264 | find it | Publish approve, regenerate and hold on the rwb-comms contract with states and error codes, or one decision operation with an outcome code; correct the Ownership Map rows. |
| CDC-08711 | RWB-P4-E2014-APP | GAP-1268 | find it | Add the rwb-document PDF reference to the notice answer with its route; amend AC2 and BR8 so the answer may carry the document reference while addressee and masked address come from rwb-source-data. |
| CDC-08713 | RWB-P4-E2014-APP | GAP-2384 | find it | Publish POST /api/recovery/comms/v1/notices/{noticeId}/approve, .../regenerate and .../hold with the request fields, notice answer and the 401, 403, 404, 409, 422, 503 set; add rows to the rwb-comms API file and the Ownership Map; keep as consumed in RWB-P7-E2014-CON. |

### RWB-P6-E1073-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08567 | RWB-P4-E2004-APP | GAP-2395 | find it | Settle the rwb-comms rule package assignment with the rule registry owner before integration; prove AC1 and AC5 on the three Epic 2 package codes read as fixtures, with no invented fourth code. |
| CDC-08634 | RWB-P4-E2008-APP | GAP-2395 | find it | Name the package codes and version labels of the three Epic 2 packages. Settle the rwb-comms package assignment with the rule registry owner before integration. Invent no fourth package code. |

### RWB-P3-E2004-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08571 | RWB-P4-E2004-APP | GAP-0705 | find it | After review with RWB-P3-E1028-CON, record treatmentId, timerType, startedAt, expiresAt (offset date-time), warnAt, paused and status as optional properties within major version 1. |
| CDC-08588 | RWB-P4-E2004-APP | GAP-2688 | 12.3 | Name the two consumed operations for CURE_PERIOD_DAYS, plan.warn-days and the seven lists; state member-level types of the TreatmentApproved payload; publish the fake set; state the one-running-plan guard on the treatment row as a partial unique index. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08581 | RWB-P4-E2004-APP | GAP-1712 |  | GAP-1712: require the eight catalog fields as written and hold the contract, agreement, plan timer and booking reference; leave the physical field list open until the data architect writes it with the DB story. |
| CDC-08712 | RWB-P4-E2014-APP | GAP-0398 |  | GAP-0398: record the wave 2 entry check, agreed by the integration lead and QA, as the resolution path. The route, fixtures, environment, evidence format, retention and gate stay Not specified in the source documents (GAP-0398). |

### OTHER:rwb-case values files (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08584 | RWB-P4-E2004-APP | GAP-0706 | find it | Set provisional defaults for the alert values (timer projection lag, subscription lag, dlt count, exception-queue count, DP04 freshness), confirm at UAT, and record agreed values in the linked runbook entries |
| CDC-08753 | RWB-P4-E2015-APP | GAP-0715 | find it | Set the timer projection lag, MSG-GEN-006 degradation rate and TimerBreached volume alert values, which are Not specified in the source documents (GAP-0715). |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (service story folder) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08592 | RWB-P4-E2007-APP | CG-ALL-5173 | 13 | Create story RWB-P7-E1073-CON, or name the existing story for the rule-package capability in the section 13 DP-04 row. |
| CDC-08595 | RWB-P4-E2007-APP | DOR-RWB-P4-E2007-APP-17 | 13 | Create story RWB-P7-E1073-CON, or re-point the section 13 DP-04 dependency to the existing story, per CG-ALL-5173. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08594 | RWB-P4-E2007-APP | DOR-RWB-P4-E2007-APP-14 | 13 | Confirm the signed epic design sign-off against the epic design record and record it there. |
| CDC-08674 | RWB-P4-E2013-APP | DOR-RWB-P4-E2013-APP-14 |  | Record the signed epic design sign-off. |

### OTHER:TSD P4 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08606 | RWB-P4-E2007-APP | GAP-0923 | 13 | Extend the T6.1 RBAC matrix with Case record and Treatment and offer columns; publish the full 14-area matrix version as data with RWB-P4-AD002-APP; confirm the RW-RESTRUCT and RW-CREDITAD letters (CASE_RECORD R and U, TREATMENT_AND_OFFER R) with the matrix owner. |
| CDC-08607 | RWB-P4-E2007-APP | GAP-0922 | 12.1, 13 | Add POST /authorise with its request and answer schema to TSD P4 appendix T-A and to the API specification of RWB-P4-E1037-CON; stub the path in that contract fake; fix the rwb-access login in the platform DB story; publish the composite route with gateway-bff (DP-19). |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08624 | RWB-P4-E2008-APP | CG-ALL-5189 | 13 | Create the story file RWB-P7-E1073-CON, or name the existing story that carries the rules capability, so the dependency resolves. |
| CDC-08627 | RWB-P4-E2008-APP | DOR-RWB-P4-E2008-APP-17 | 13 | Create the story file RWB-P7-E1073-CON, or name the existing story that carries the rules capability, so the dependency resolves. |

### RWB-P8-E2008-CON; API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08641 | RWB-P4-E2008-APP | GAP-0601 | 12 | Publish one row per payment_code ordered by paymentCode ascending, both reads unpaged with cap as configuration; name the fold rule and the over-cap answer; route duplicate codes to REC-05 if confirmed a break. |
| CDC-08642 | RWB-P4-E2008-APP | GAP-0599 | 12.1 | Publish the two read operations on /api/recovery/source-data/v1 with resource names, businessDate query parameter, element names and status set; confirm MSG-P2-007 with P1 owner. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08663 | RWB-P4-E2008-APP | GAP-1639 | none | Name the two event-started workflows after matchPayments and confirmBookings on task queue rwb-payment, or confirm the activity is the unit. |
| CDC-08752 | RWB-P4-E2015-APP | GAP-1830 | find it | Give SCR-06 and SCR-08 an owner and a gateway-bff composite route; confirm the queue read operation with the platform edge owner before the wave 2 screen test. |

### OTHER:(no target) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08672 | RWB-P4-E2008-APP | GAP-1349 | find it | Activity names and SCR field lists stated as Not specified; invented owner removed |
| CDC-08673 | RWB-P4-E2008-APP | GAP-2496 | find it | Pattern rows stated as Not specified; row IDs removed |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08681 | RWB-P4-E2013-APP | GAP-3177 | find it | Register the five-minute next-action Schedule in rwb-case and delete EV-18 from the Epic 2 contract tables. |
| CDC-08744 | RWB-P4-E2015-APP | GAP-3177 | none | Register the five-minute next-action Temporal Schedule in rwb-case; delete TimerDue (EV-18) from the Epic 2 contract tables. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08737 | RWB-P4-E2015-APP | CG-ALL-5225 | 11 | Add id_no_token to Fields, or record the object it names (index, library table or flag) in the owning document. |
| CDC-08738 | RWB-P4-E2015-APP | CG-ALL-5226 | 11 | Add value_token to Fields, or record the object it names (index, library table or flag) in the owning document. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08562 | RWB-P4-E2004-APP | DOR-RWB-P4-E2004-APP-12 | 12, 12.7, 16, 18 | Add rows TC-E2-004-15 to TC-E2-004-19 under the same IDs as section 16; align the section 18 test lists with RTM v7. |

### OTHER:FSD S2 module (A1.1 and A2.x prerequisites) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08568 | RWB-P4-E2004-APP | GAP-1713 | find it | Map each FEAT prerequisite to its owning service contract (approval P7, case P3, documents P5, communications P6, valuation S1) and record the mapping once in the service contract. |

### RWB-P4-E1037-CON; RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08572 | RWB-P4-E2004-APP | GAP-0917 | find it | Freeze the authorise and doa-limits request and answer fields at contract review; load the two capability areas into the policy pack as rows; name the rwb-access login with the DP-02 platform DB story. |

### OTHER:Wave 2 integration harness pack (QA and integration lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08574 | RWB-P4-E2004-APP | GAP-0389 | 16 | Agree the harness pack before the first SIT run: repository, SIT and UAT namespaces, seed files, business clock setting, per-run evidence report, retention and pass/fail gate |

### OTHER:rwb-decision contract (RWB-P7 decision service contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08577 | RWB-P4-E2004-APP | GAP-2473 | 14 | Publish the rule-catalogue answer element names and media type, decision record business date, treatment and timer spec fields, MSG-P7-009 text, ledger actor value and registry column names |

### RWB-S2-E2004-APP; RWB-P3-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08578 | RWB-P4-E2004-APP | GAP-2687 | 7 | Hold the treatment entity and plan facts on one table in rwb_treatment, publish them on rwb.treatment.TreatmentApproved.v1 and derive treatment state from case and payment signals. Keep no timer table, Quartz job, TimerDue topic or extract. The fourteen legacy criteria and sixteen test cases stay with RWB-P3-E2004-APP. This story already states that ownership in section 7, so no edit here. |

### OTHER:Recovery Workbench PRD of rwb-treatment (release slicing section) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08580 | RWB-P4-E2004-APP | GAP-1709 |  | Publish the contract and deliver the treatment record with its data date in wave 2. Release the offer, settlement, plan and deed in lieu capabilities with E3. No requirement changes; release dates are unchanged. |

### RWB-P7-E1073-CON; RWB-PLT-E1027-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; RWB-P7-E2005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08582 | RWB-P4-E2004-APP | GAP-1339 | 13 | Fix model and catalogue answer in OpenAPI; name envelope fields; add MSG-P7-009 and MSG-P7-012 to P7 message table; name SCR-38 and SCR-03 panels; state platform dependencies in build order |

### OTHER:gateway-bff route catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08585 | RWB-P4-E2004-APP | GAP-0920 | 15 | Publish the SCR-14 and SCR-03 composite routes with field lists and confirm no field on either is personal |

### OTHER:platform DB story of DP-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08586 | RWB-P4-E2004-APP | GAP-0921 | 3 | Fix the per-service login name of rwb-access, its grants and its schema owner in the platform DB story of DP-02 |

### RWB-P2-E2007-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08602 | RWB-P4-E2007-APP | GAP-0657 |  | Fix the six unsettled consumed paths and shapes with their owners; record the rwb-payment JOB-08 owner row as superseded and the TSD P2 v3 T5.2 read as superseded. |

### OTHER:Booking confirmation integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08609 | RWB-P4-E2007-APP | GAP-0395 | 13 | Agree with the platform edge story the composite booking and treatment route path and merge order; record the harness environment, ALS booking fixture format, seed pack, evidence format and retention, and pass or fail gate at the wave 2 entry check. |

### RWB-P2-E2007-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08612 | RWB-P4-E2007-APP | GAP-0659 | 13 | Fix the rwb-integration identity (Not specified in the source documents, GAP-0659), secret reference and probe checks; register the workflow on rwb-integration and record the JOB-08 owner conflict; set the four thresholds, series windows and backfill limit as environment values; write the JOB-08 catalogue row with its run book path; review the four runbook entries with the on-call rota. |

### OTHER:Contracts of rwb-integration, rwb-treatment and rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08614 | RWB-P4-E2007-APP | GAP-2486 | 3, 4 | Publish the operation set of the six legacy interfaces with paths and payloads on the DP-13 per-service base (one hop, 2 s timeout); take the decision code from LOV-DECISION; define inputs_ref and actions shapes, read filters, page size, ordering and MSG-GEN-006 text. |

### OTHER:P7 context pack event ownership rows (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08615 | RWB-P4-E2007-APP | GAP-2487 | 4 | Name rwb.decision.BookingDecisionMade.v1 on rwb.decision.events.v1, keyed by treatmentId, carrying outcome, row, package code and version, business date and difference terms; TreatmentBooked, CaseStateChanged and posting stay with their owners. |

### RWB-S2-E3001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08616 | RWB-P4-E2007-APP | GAP-2691 | 3, 15 | Add the approved-not-booked read, mark-booked write and booking-difference write with element names at the wave 2 freeze; add APPROVED and BOOKED to the state check constraint; define booking_difference as jsonb keyed by term name; enforce one confirmation per treatment and business date with a unique key. |

### OTHER:Parameters contract (DP-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08618 | RWB-P4-E2007-APP | GAP-0924 | find it | Register the cache lifetime as a parameter and agree its value at the wave 2 design review. Story AC7 and TC-E2-007-06 already test the version-keyed drop. |

### OTHER:Platform secret store (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08619 | RWB-P4-E2007-APP | GAP-2489 | find it | Allocate the rwb-decision login with schema rwb_decision and record it in the platform secret store. |

### OTHER:RWB-E2-007 legacy story and rwb-integration JOB-08 workflow specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08620 | RWB-P4-E2007-APP | GAP-2491 | find it | Record the Asia/Bangkok timezone, one run per business date with a second start refused MSG-P2-006, retry on the next AceDataReady, no fallback Schedule, and the flag off stopping the start. |

### OTHER:TSD P7 v2 and the rwb-reporting read-model owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08621 | RWB-P4-E2007-APP | GAP-2492 | find it | Create no reconciliation_result table in rwb_decision; serve counts from decision_log_entry and build the REC-03 break list from events in rwb-reporting. |

### OTHER:Parameters and reference-data registers; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:rwb-case contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08622 | RWB-P4-E2007-APP | GAP-2692 | find it | Add booking.missing.grace_loads and the treatment-type and outcome list codes; record TreatmentBooked ownership against rwb-payment; record the parent stage outcome contract. |

### RWB-P4-E2007-APP; OTHER:12.2; OTHER:12.8 and 13 (other chunks) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08623 | RWB-P4-E2007-APP | GAP-2488 | find it | Carry the seven H and four consumed contract rows named in the Work Package in the pattern table, fakes and dependency sections. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08628 | RWB-P4-E2008-APP | DOR-RWB-P4-E2008-APP-8 | 12.3 | Make roleClass and defaultScope reference LOV-ROLE-CLASS and LOV-SCOPE, not closed enums; set the DecisionRecorded event type to rwb.decision.DecisionRecorded.v1; align the AccessPolicyChanged.v1 payload with the catalog. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08633 | RWB-P4-E2008-APP | GAP-3175 |  | Name AceDataReady (EV-26, producer rwb-source-data) as the target event on rwb.source-data.events.v1, with LoadCompleted listed as its legacy alias. |

### RWB-P8-E2008-CON; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08635 | RWB-P4-E2008-APP | GAP-2503 | 12 | Declare the nine consumed operations on per-service bases with one hop and 2 s timeout; name workflow matchPayments and its four activities; record in the RTM that legacy AC1, AC3, AC4 and AC5 are carried by no story of this split. |

### OTHER:FSD S2 v3 (A2.10; OTHER:A2.11; OTHER:A2.17); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08637 | RWB-P4-E2008-APP | GAP-1703 |  | Record the booking reference from TreatmentBooked and the break from PaymentMissed; rwb-payment owns booking, matching and posting; the release request goes through rwb-integration. |

### OTHER:FSD P8 v3 (A2.3.4.1 to A2.11.4.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08638 | RWB-P4-E2008-APP | GAP-1625 |  | Replace placeholder AC-P8-003-01 to AC-P8-011-01 with testable main-flow criteria marked as new, for FSD owner confirmation before wave 3 system test. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08639 | RWB-P4-E2008-APP | GAP-1626 | 12 | Publish one operation pair for rwb-payment; take GET /proceeds and POST /proceeds/{proceedsId}/match from API Specification v4 as the contract and confirm before contract closure. |

### OTHER:FSD P8 v3 integration points of A2.1 and A2.3 to A2.11 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08640 | RWB-P4-E2008-APP | GAP-1631 |  | Read ALS position via rwb-source-data after each ACE batch; deliver ledger postings via rwb-integration; treat auto-debit and LED routes as outside the 19 services until an interface is named. |

### OTHER:TSD P4 T6.1 (Technical Specification P4; OTHER:RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08643 | RWB-P4-E2008-APP | GAP-0926 |  | Publish letters of all 14 LOV-CAPABILITY areas per role, with each role's default scope, as a new T6.1 version, and load them through RWB-P4-AD002-APP. |

### OTHER:Payment matching integration harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08645 | RWB-P4-E2008-APP | GAP-0393 |  | Record the composite proceeds and exception route path and merge order, harness environment, ALS payment fixture format, seed pack, evidence format, retention and pass or fail gate at the wave 2 entry check. |

### OTHER:RWB-E2-008 legacy story and TSD P8 v2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08646 | RWB-P4-E2008-APP | GAP-1348 |  | Keep the TSD P8 T3.1 proceeds field set; hold payment identity on account_payment_id; replace payment_missed_event_key with the DP-09 idempotency_key table; take the next number of the service Flyway sequence; data owner to confirm where payment code is held. |

### OTHER:Deployment specification for rwb-payment (TSD P8 v2 T6.2; OTHER:T7; OTHER:Appendix T-B) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08648 | RWB-P4-E2008-APP | GAP-1352 |  | Render the unit from the pinned chart with two api replicas and a worker tier with floor, ceiling and sizes; create three topics with platform defaults; gate every environment; canary or blue/green for PROD; down script per migration. |

### OTHER:Recovery Workbench split plan (WP B-P8-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08649 | RWB-P4-E2008-APP | GAP-1354 |  | Reallocate AC1, AC3, AC4 and AC5 to RWB-P8-E2008-APP in the next split plan revision, or add a coverage note to the epic overview. |

### OTHER:Reconciliation break list of rwb-source-data (P1); OTHER:FSD P8 v3 AC-EXC-P8-001-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08650 | RWB-P4-E2008-APP | GAP-1627 |  | Report the orphan payment as a break row with check name 'References' on the reconciliation break list; write no exception table in rwb_payment; data steward to confirm the check name. |

### OTHER:Epics 3 to 8 BRD (7.3; OTHER:DEP-005) and FSD P8 v3 A1.2 (FEAT-PAY-06) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08651 | RWB-P4-E2008-APP | GAP-1629 |  | Build settlement booking confirmation in wave 2 with EP03, the earlier release; proceeds features stay in wave 3. |

### OTHER:TSD P8 v2 T3.1 and T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08652 | RWB-P4-E2008-APP | GAP-1634 |  | Keep one business-key column varchar(255) holding the ACE payment_code with no foreign key; drop the uuid cross-reference account_payment_id from the field list. |

### OTHER:NFR Spec v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08655 | RWB-P4-E2008-APP | GAP-1643 |  | State the receipt volume per business date, sized from the observed receipt-to-installment ratio on ACE data for a busy month, in the next NFR version; use the ratio as an assumption until then. |

### OTHER:Work Package B2-P7-022 (RWB-E2-008 story line) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08656 | RWB-P4-E2008-APP | GAP-2493 |  | Keep the Work Package placement; rwb-payment writes the local record in its own transaction and publishes it; rwb-decision holds the package, rows and tests, collects records, appends to the central ledger and runs JOB-14. |

### OTHER:RWB-E2-008 deployment values in the rwb-payment chart and runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08659 | RWB-P4-E2008-APP | GAP-2505 |  | Take every threshold, count, retention, partition and limit as an environment value; review the five runbook entries with the on-call rota before promotion. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08662 | RWB-P4-E2008-APP | GAP-0604 | 3 | RWB-P3-E1043-CON added to Contract dependencies |

### RWB-P1-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08664 | RWB-P4-E2008-APP | GAP-0602 | none | Keep nextInstallmentDate on the installment-facts read and record GET /accounts/{id} as unowned and unpublished. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; RWB-P1-E2008-APP; RWB-P8-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08665 | RWB-P4-E2008-APP | GAP-0603 | none | Take the caller as the rwb-payment run with a workload identity token; settle the P8 to P1 step as one REST hop wrapped by the run's Temporal activity. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08667 | RWB-P4-E2008-APP | GAP-1351 | find it | Name DecisionRecorded as owned by rwb-decision (topic rwb.decision-record.v1 and central ledger) and align the producer and owner rows. |

### OTHER:Work Package plan generator and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08669 | RWB-P4-E2008-APP | GAP-2180 | find it | Keep one Work Package per story slice (drop B2-P1-014 or the RWB-E2-008 fanout entry in B-P1-08); add a plan-uniqueness check. |

### OTHER:P7 rule-package API contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08670 | RWB-P4-E2008-APP | GAP-2495 | find it | Publish the dry run as a read-only operation returning testResult, per-test-case expected and actual results and recorded dry-run counts. |

### OTHER:Program BRD v5 section 11 note (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08671 | RWB-P4-E2008-APP | GAP-1641 | find it | Add section 5.11 (REQ-S4-010) to the P8 requirements note in the next version. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08676 | RWB-P4-E2013-APP | DOR-RWB-P4-E2013-APP-22 |  | Publish a contract fake library version and record it. |

### OTHER:RWB-P7 decision story owning SCR-10 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08679 | RWB-P4-E2013-APP | DOR-RWB-P4-E2013-APP-10 |  | Add empty, loading, error and no-access states for SCR-10. |

### RWB-P4-E1037-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08683 | RWB-P4-E2013-APP | GAP-1252 | find it | Add GET /api/recovery/access/v1/doa-limits with P4 as owner, the query and answer fields, and list it in the operations of RWB-P4-E1037-CON. |

### OTHER:Approval-routing harness pack, agreed at the wave 2 entry check (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08685 | RWB-P4-E2013-APP | GAP-0397 | none | Agree the composite approval-queue route and merge order with the platform edge owner; agree harness environment, seeding, evidence format, retention and pass/fail gate with QA; hold as harness data, not in the story |

### OTHER:rwb-access DoA lookup and POST /authorise contract (contract review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08687 | RWB-P4-E2013-APP | GAP-0929 | 12 | Freeze the request and response field set of section 12 with outcomes COVERED, NO_HOLDER, NOT_COVERED, NO_AMOUNT_LIMIT, RELATED_PARTY and requiredLevel on refused decisions |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08688 | RWB-P4-E2013-APP | GAP-0930 |  | Add the rwb-decision service identity to the permission data with Approval check R and no other Recovery right; security administrator to confirm before the authorise contract is frozen. |

### OTHER:rwb-comms contract (TSD P6 v2 notice table; OTHER:API-P6-002 and API-P6-008) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08690 | RWB-P4-E2013-APP | GAP-1222 | 12.1 | Confirm GET /notices/{noticeId} and POST /cases/{caseId}/messages on /api/recovery/comms/v1 with the section 12.1 Notice and MessageRequest field sets before migration V2013_1 |

### OTHER:TSD P4 v3 (T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08694 | RWB-P4-E2013-APP | GAP-0979 | none | Name constraints per platform convention; PK on id; unique role_code; single FK permission.role_id; one index per read path with leading columns of section 13. |

### OTHER:TSD P7 v2 (T8 traceability table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08695 | RWB-P4-E2013-APP | GAP-1263 | none | Map REQ-APD-002 and REQ-APD-006: screen to FEAT-APD-08 with RWB-E2-014; routing to FEAT-APD-01 with RWB-E2-013. |

### OTHER:Edge and gateway design (platform edge owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08696 | RWB-P4-E2013-APP | GAP-1621 | none | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from service operations and record the four screen contracts there. |

### OTHER:TSD P7 v2; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08697 | RWB-P4-E2013-APP | GAP-1254 | none | Retire INT-19, INT-20, lake partition, manifest and watermark; rwb-reporting reads rwb.decision-record.v1; EV-08 unchanged; drop lake elements from contract and deployment. |

### OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08707 | RWB-P4-E2014-APP | GAP-1623 | find it | Record that the Waiting approval state move and the approval task are a P3 reaction to ApprovalRequested; this service writes rwb_decision only; amend FSD A2.15 and A2.16 to match. |

### OTHER:rwb-comms API file and TSD P6 notice rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08715 | RWB-P4-E2014-APP | GAP-2386 |  | State the rule that regeneration keeps the same notice row, moves document_id and template_id to the chosen Approved variant, increments the version, and keeps the superseded document readable per AC-ALT-P6-007-01. |

### OTHER:TSD P6 appendix T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08717 | RWB-P4-E2014-APP | GAP-2388 |  | Add the three notice decision operations to T-A.1 declared as Litigation right A with scope applied, enforced at gateway-bff via rwb-access, called by rwb-decision with service identity plus approver identifier. |

### OTHER:TSD P6 section 4 and decision-record library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08718 | RWB-P4-E2014-APP | GAP-2390 |  | Notice move writes one local decision record via the library with code D7.1, rule, IDs, template code and version, state from and to, reason code, approver and approval entry reference. |

### RWB-S4-E5001-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08719 | RWB-P4-E2014-APP | GAP-2743 |  | Record the two consumed rows as C dependencies; declare notice and template ownership for P6; name P6 operations in its contract story; add REQ-S4-001 to the trace; decide the D7.1 gate in the EP05 PRD. |

### OTHER:Context pack S4 and TSD S4 v2 (ownership rows and T5.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08723 | RWB-P4-E2014-APP | GAP-2742 | find it | Record notice and template rows as P6's or correct the S4 row; name the P6 generate-and-send operation and the rwb-case answer; add REQ-S4-001 to the key trace; decide D7.1 approval in EP05 PRD. |

### OTHER:Recovery Workbench TSD P7 v2 (T8 traceability table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08725 | RWB-P4-E2014-APP | GAP-1263 | find it | Correct REQ-APD-002 and REQ-APD-006 rows to FEAT-APD-08 with RWB-E2-014 for the screen and FEAT-APD-01 with RWB-E2-013 for routing. |

### OTHER:Edge and gateway design (gateway-bff composition) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08726 | RWB-P4-E2014-APP | GAP-1621 | find it | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from P7 operations and record the four screen contracts there. |

### OTHER:TSD P7 v2 (observability text) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08729 | RWB-P4-E2014-APP | GAP-1271 |  | Add dashboard and alert thresholds: any 5xx in five minutes; route p95 above registered budget; failed record write; empty D7.1 queue for 24 hours. |

### OTHER:rwb-case reference data (TSD P6 v2 T3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08730 | RWB-P4-E2014-APP | GAP-2391 |  | Add LOV-HOLD-REASON with REFUSED_BY_APPROVER and TEMPLATE_WITHDRAWN; keep switch key rwb.decision.notice-approval read by both services until renamed. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08731 | RWB-P4-E2014-APP | GAP-2389 |  | Keep H empty; add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON and the two rwb-case contracts of DP-06 and DP-07 to the C list. |

### OTHER:FSD S8 and rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08734 | RWB-P4-E2015-APP | GAP-1816 | n/a | Build S8 reads on rwb-source-data contract fields; boundary test fails the build on any view or ACE table read; confirm flags and freshness fields with P1 before wave 2 system test. |

### OTHER:S8 contract story; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08735 | RWB-P4-E2015-APP | GAP-1818 | n/a | Settle the raise, clear and case-record read deviation paths in the S8 contract story before the screen is built; carry the read as an open question with its owner. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:15; OTHER:25) and the S8 deviation story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08736 | RWB-P4-E2015-APP | GAP-1820 | none | Record the FSD approval as a step inside DeviationWorkflow taken by the role the code assigns; decision-record library writes entry and hash; leave P7 ApprovalWorkflow as an open question. |

### RWB-P3-E2015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08741 | RWB-P4-E2015-APP | DOR-RWB-P4-E2015-APP-10 | 4 | Add empty, loading, error and no-access states of SCR-03 and SCR-04 to the P3 screen spec. |

### OTHER:FSD S8 (A2.2.4.1 to A2.9.4.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08743 | RWB-P4-E2015-APP | GAP-1823 | none | Carry each FSD row as one criterion and add a step criterion per feature for pause, stop, routing, clear and two-deviation behaviour. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08745 | RWB-P4-E2015-APP | GAP-1832 | none | Add case, code, state, contact stop flag, return point and decision record reference to EV-06 and EV-07; no personal or financial value. |

### OTHER:Wave 2 harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08747 | RWB-P4-E2015-APP | GAP-0399 | none | Record the composite route path, merge order, timer and deviation fixtures, seeding, evidence format, retention and pass/fail gate at wave 2 entry. |

### OTHER:Functional Specification Document S8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08749 | RWB-P4-E2015-APP | GAP-1817 | find it | Replace the Workbench, Quartz scheduler integration point in A2.2.2, A2.3.2 and A2.6.2 with durable timers inside DeviationWorkflow through the workflow kit. |

### OTHER:Recovery Workbench FSD S8 (document control, inherited history table; OTHER:FSD owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08751 | RWB-P4-E2015-APP | GAP-1834 | inherited history | Add v1 and v2 rows to the inherited history as Not specified in the source documents (GAP-1834). Change log unchanged. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20680 | RWB-P4-E2013-APP | R-22469 |  | GET /notices/{noticeId} and POST /cases/{caseId}/messages are present. Section 12.1 field-set check is in a story outside this document (GAP-1222). |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20813 | RWB-P4-E2008-APP | R-22410 |  | Deployment values belong to the platform deployment spec, not this document. DL35 already lists deployment slots in Appendix T-B. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0389 | The harness repository, environments, seeding, business clock, evidence format and retention, pass/fail gate and the gateway-bff composite case-record route are not defined in the source documents | Integration lead | Resolved (directive) |
| GAP-0393 | Payment matching integration harness: composite proceeds and exception route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0395 | Booking confirmation integration harness: composite booking and treatment route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0397 | Approval-routing harness environment, composite queue route and evidence format are not specified | Integration lead | Resolved (directive) |
| GAP-0398 | Integration harness values for the D7.1 decision-screen journey are not specified | Integration lead | Resolved (directive) |
| GAP-0399 | Wave 2 case-record harness: composite route, timer and deviation fixtures, environment and evidence format undefined | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-0703 | The treatment entity moves to S2 while the legacy story holds it in P3, and the case side consumes TreatmentApproved which the event catalogue does not list for rwb-case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0705 | No source fixes the plan-timer fields, types or required flags of the timers answer behind GET /cases/{caseId}/timers | Tech lead of rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0706 | No source gives the alert values for the plan-timer projection, the subscription lag, the DP04 freshness or the exception-queue count | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0714 | Deviation read path is absent from the Ownership Map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0715 | No source gives the alert values for the timer projection, the degradation rate or the breach volume | DevOps lead | Resolved (directive) |
| GAP-0730 | rwb-case booking confirmation: login, composite route, treatment booking fields, match-result shape and route-rule evaluator owner are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
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
| GAP-0928 | GET /doa-limits is named in Architecture v5 and API v3 but absent from API Specification v4 | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0929 | The DoA lookup and authority-decision request and response shape is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0930 | The scope of the rwb-decision service identity inside rwb-access is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0932 | The request and response shape of the authorise operation is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0934 | The object attributes an authorise request carries are not specified | Solution architect | Resolved (directive) |
| GAP-0971 | The rollback of a delegation version has no acceptance criterion, business rule or window semantics | Business analyst, P4 | Accepted (directive); not applied: value not in the source documents |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0979 | The constraint names and the full index set of the five tables are not specified | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-1220 | The template code, channel, notice kind, state vocabulary, retry limit, template owner and MSG-GEN-006 text of the escalation notice are not specified in any source | Solution architect | Resolved (directive) |
| GAP-1221 | The event catalogue lists gateway-bff as the only consumer of ApprovalRequested and carries no ApprovalEscalated event, yet this story also consumes the event for the escalation notice | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1222 | No source names the notice and message operations or the notice fields that carry an approval reference, an escalation level, a recipient and a sent time | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1251 | The delegation of authority table is P4 rwb-access's while the routing rules and the approval resource are P7 rwb-decision | Solution architect | Resolved (directive) |
| GAP-1252 | The delegation limits operation has no row in the Ownership Map API catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1254 | The data lake copy of the decision record is removed under DP-17 while the legacy log path streams to it | Solution architect | Resolved (directive) |
| GAP-1255 | The request and answer field lists of the five approval operations and the case-status operation are not enumerated in any source | Tech lead of rwb-decision with the Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1256 | The delegation snapshot and its cache refresh have no named operation, store or interval | Solution architect | Resolved (directive) |
| GAP-1257 | ApprovalDecided is named on the service contract slide but has no event catalogue row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1258 | The field-level list and the mask flags of the D7.1 approval screen are published by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1259 | The composite-route name and path segment of the approval screen are not specified | Solution architect | Resolved (directive) |
| GAP-1262 | ApprovalDecided is named on the slide 14 contract line but has no event-catalogue row | Solution architect | Resolved (directive) |
| GAP-1263 | REQ-APD-002 and REQ-APD-006 are mapped to two different features and stories | Business analyst | Resolved (directive) |
| GAP-1264 | The three notice operations of the legacy NoticeApi have no owner path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1266 | The field types and order of the screen model and the queue paging defaults are not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1267 | The legacy screen states and the platform route states are two unreconciled vocabularies | Business analyst | Resolved (directive) |
| GAP-1268 | The notice summary excludes the PDF body and the addressee that the legacy screen shows | Data steward | Resolved (directive) |
| GAP-1270 | The timeout budget of a screen that composes three reads is not specified | Solution architect | Resolved (directive) |
| GAP-1271 | The dashboard names, the alert thresholds and the empty-queue window are not specified | DevOps engineer | Resolved (directive) |
| GAP-1339 | Values of the RESTRUCTURE catalogue and plan-timer ledger slice that no source fixes | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1341 | TimerDue and the five-minute JOB-05 check are retired in the target but kept by the legacy story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1698 | The Ownership Map lists one table for rwb-treatment, although Architecture v5 gives it four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1709 | The service is wave 2 and EP02 while every requirement of the module is an Epic 3 requirement | Solution architect | Resolved (directive) |
| GAP-1712 | The field catalog covers eight fields and none of them describes a contract, an agreement, a plan timer or a booking | Data architect | Resolved (directive) |
| GAP-1713 | The prerequisites of the module are feature codes of other modules that name no service | Solution architect | Resolved (directive) |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1817 | Three FSD integration points name the Quartz scheduler, which Architecture v5 and the Temporal design replace with durable timers in DeviationWorkflow | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1820 | The FSD records an approver on a deviation while the S8 row has no rwb-decision cell and no approval workflow is named for this service | Solution architect with the S8 business analyst | Resolved (directive) |
| GAP-1823 | The main success criterion of seven E2 features is the same case-record 'Timers shown' scenario on another story, and every alternate and exception row repeats three scenarios | Business analyst, S8 with the QA lead | Resolved (directive) |
| GAP-1830 | The two deviation screens have no owner cell in the Architecture screen matrix and no recorded route at the edge | Solution architect | Resolved (directive) |
| GAP-1831 | The wording, the Thai version and the approver of the eight messages the service shows are not in the FSD | Business analyst, S8 | Resolved (directive) |
| GAP-1832 | The two deviation events have a catalogue row and a topic but no field list, while the criteria expect an agent verdict and a decision log entry to travel with them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1834 | The change notes of FSD S8 versions 1 and 2 are not in the sources read | Business analyst, S8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2093 | The notice approval sits in P6, P7 and S4 at once | Service owners of P6 rwb-comms, P7 rwb-decision and S4 rwb-litigation | Resolved (directive) |
| GAP-2180 | Two Work Packages of the same stage write the same story file for RWB-P1-E2008-APP | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2216 | No source fixes the case-facts field list behind the D7.1 approval screen, the names of the two approval outcome events, the naming of the redress task, or the business date of the postal address input | Solution architect | Resolved (directive) |
| GAP-2384 | The three notice decision operations of the D7.1 approval have no REST row in the Ownership Map or in appendix T-A | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2385 | The notice table has no column for the decision entry reference that the approve and hold calls carry | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2386 | No source says whether a change of template variant replaces the notice row or creates a new version of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2387 | The notice answer has no field list, and the template state the approval panel must show is not part of it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2388 | The declared right of the three notice decision operations is not in the endpoint inventory or the RBAC matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2390 | No source says whether a notice move writes its own decision record or only references the approval entry of rwb-decision | Solution architect | Resolved (directive) |
| GAP-2391 | The hold reason vocabulary has no list of values, and the owner namespace of the feature switch is not settled for the comms half | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2473 | RWB-P7-E2004-APP: the wire shape of the rule-catalogue answer, the payload fields of the plan-timer decision record, the text of MSG-P7-009, the ledger writer identity and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2474 | RWB-P7-E2004-APP: the rule-catalogue read that two stories consume is attributed to no owner in the Ownership Map, while the entry read the same map attributes to this service is served by RWB-P7-E2005-APP | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2476 | RWB-P7-E2004-APP: the legacy plan timers run on the Quartz timer check and publish a timer-due event, both retired in the target, and no source says what happens to a plan timer already running at cut-over | Solution architect with the rwb-case service owner and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-2691 | The treatment-side booking write has no operation, no element names and no state value in the S2 sources, and the difference column has no shape | Solution architect, S2, with the rwb-treatment tech lead and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2692 | The rwb-treatment share of the key is stated by no S2 source, the P2 contract shapes it follows are unpublished, and the trigger, the task-raising and the event ownership are split across stories | Solution architect with the rwb-integration, rwb-treatment and rwb-case tech leads and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2693 | The delivery route of a match to rwb-treatment, the plan-position elements and the payment frequency of a plan are not specified for the S2 slice of RWB-E2-008 | Tech lead of rwb-treatment with the P8 rwb-payment owner, the P3 rwb-case owner and the P7 rwb-decision package owner at the wave 2 contract freeze | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
