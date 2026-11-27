# RWB-ITG-W2 Wave 2 integration - review pack, part 2 of 5 (RWB-ITG-E2008-ITG to RWB-ITG-E2016-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 179 |
| Cross-document (pending in another document) | 175 |
| Not applied (value not in the sources) | 21 |
| Open business decisions | 44 |
| Register gaps linked | 161 |
| Unconfirmed assumptions | 0 |
| Lint findings | 4 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E2008-ITG | 41 | 38 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2008 ITG Payment matching with the missed payment event - integration v2.md |
| RWB-ITG-E2009-ITG | 20 | 24 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2009 ITG Steering dashboard v1 data set - integration v2.md |
| RWB-ITG-E2010-ITG | 24 | 14 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2010 ITG Stage 2 data products contracts, plans and treatments - integration v2.md |
| RWB-ITG-E2012-ITG | 17 | 17 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2012 ITG Manual transfer and reassignment screen with reason - integration v2.md |
| RWB-ITG-E2013-ITG | 25 | 22 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2013 ITG Approval routing with the delegation of authority table - integration v2.md |
| RWB-ITG-E2014-ITG | 26 | 31 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2014 ITG Approval screen for D7.1 demand and recall notices - integration v2.md |
| RWB-ITG-E2015-ITG | 14 | 16 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2015 ITG Timers, escalation and the deviation flag on the case record view - integration v2.md |
| RWB-ITG-E2016-ITG | 12 | 13 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W2 Wave 2 integration/RWB ITG E2016 ITG Full case record view with the history timeline - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E1034-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22079 | GAP-1606 | Register gap | Product owner with Legal counsel | It is not stated whether the approval is taken on a template version or on a generated notice | Record the Legal approval on the template version as a decision record written through rwb-decision, and take the notice approval for the demand and recall types through the approval workflow on the generated notice; state both in the story's acceptance criteria. |
| RWB-ITG-E2008-ITG, RWB-P1-E1015-APP, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22404 | GAP-0600 | Register gap | Solution architect with the P1 data product owner | FSD P1 A2.2 stamps a payment read on DP01 Account and arrears while the Work Package slice note names DP05, and no source states whether the read or the rwb-payment run answers a held business date | Hold both gates on DP01 Account and arrears and answer 409 with MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run, with no row of any kind; record DP05 as not the stamp of a payment read and correct the slice note in the Work Package and the data product map in the next version of FSD P1 A2.2; state in RWB-P8-E2008-CON that the run's own refusal for the business date is its own and that the read's 409 is the answer to a call made anyway. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22414 | GAP-1630 | Register gap | Finance and CFO delegate | The posting file has no layout, no schedule and no receiving ledger in any source | Fix one line per posting with case, account key, entry type, amount, value date, business date and posting reference, a manifest with count and checksum, and delivery through rwb-integration. Agree the layout with Finance and the ledger owner before wave 3. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22415 | GAP-1632 | Register gap | Business lead | A reversed payment has no product behaviour in the FSD although the routing rules require the case to reopen | Decide whether a reversal is in scope for this service. If it is, add a reversal source value, a reversal state on the proceeds record and an event that reopens the case through rwb-case. Until then the capability is out of scope and listed as an open question. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22416 | GAP-1633 | Register gap | Finance and CFO delegate | The fee tables that the fee feature reads are not defined anywhere | Name the fee table, its owner and its schedule, and hold the fee rate, the cap and the basis as versioned rows. Until then the fee calculation has no input and the feature cannot be tested. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22419 | GAP-1636 | Register gap | Finance and CFO delegate | The order in which a receipt is applied to the balance is named but not specified | Hold the application order as versioned rows with an owner and a valid-from date, record the version on each proceeds row, and let Finance set the sequence before wave 3. |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22435 | GAP-1663 | Register gap | Solution architect with the AI product owner | No event source is named for the agent acceptance and override measures | Count the two rates from the decision record, which carries the agent and prompt version, the recommendation, the approval and the outcome |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-22439 | GAP-3178 | Register gap | Reporting and BI lead with the data product owner | RWB-E2-009 writes an INT-19 extract for a data lake that the target removes | Name the read model or event topic the Power BI data set subscribes to after the data lake removal, and update the acceptance criteria of RWB-E2-009 once. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22463 | GAP-1616 | Register gap | Risk and model risk officer with the rwb-access owner | The delegation of authority table is loaded and approved inside P7 while the ownership ruling gives the table to rwb-access | Keep in this service only the lookup at the moment of the decision and the recording of the row ID and version; move A2.24 with AC-P7-024-01 to AC-EXC-P7-024-05 to rwb-access, and confirm the lookup answer shape (level, row ID, version, NOT_COVERED, RELATED_PARTY reason) in the access contract. Until then this PRD reads the limits and records the version, and OQ-P7-05 stays open. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22470 | GAP-1253 | Register gap | Business lead with the Center of excellence | The escalation ceiling and the service level values of an approval are not specified | Fix three values as data owned by RW-COE: the service level per decision and per default, the escalation step in working days, and a maximum escalation count with its ceiling behaviour (hold, incident to RW-RISK, or committee). Carry them as rwb.approval.service-level.*, rwb.approval.escalation.step and rwb.approval.escalation.max-levels and close DL22. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22482 | GAP-0931 | Register gap | Compliance and PDPA officer with the P4 solution architect | The masked rendering of the addressee postal address is not specified | Let the platform masking library own one rendering per field type, record it as data beside the masking row, and add the postal address rendering to the MASK-SIT-01 pack before the first SIT run of the approval screen |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22483 | GAP-1260 | Register gap | Business lead | The limit that applies on the approval screen conflicts with D7.1 carrying no amount limit | Show the approval level and the route role as the limit that applies for D7.1 (no amount, level none) and read the DoA table only where an amount-bearing decision uses the screen; confirm with Risk and Credit. |
| RWB-ITG-E2014-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22495 | GAP-1269 | Register gap | Compliance and PDPA officer | No source enumerates the mask flags of the screen fields | Declare a mask flag of NONE, PARTIAL or FULL with a policy key on every field of the two panels, PARTIAL for the postal address, and confirm the policy keys with the masking owner (P4). |
| RWB-ITG-E2015-ITG, RWB-ITG-E7006-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON | R-22499 | GAP-1827 | Register gap | Business lead | The deviation service level is 'set with DL22' and has no number, and the ten working day escalation comes only from the design | Carry the service level, the escalation period and the skip trace window as versioned reference data read at run time, assert no number, and take the values from DL22 when the business lead sets them. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22503 | GAP-0935 | Register gap | Business lead | Precedence between a role's default scope and an escalation grant is not specified | Rule that the wider of the two scopes is named, that the reason ESCALATED_TO_ROLE is carried while the escalation is open, and that the grant never exceeds Case record R on that one case. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22504 | GAP-0936 | Register gap | Compliance and PDPA officer | The masking version in force for SIT and the answer when two versions overlap are not specified | Record MASK-SIT-01 as the SIT version in the policy pack, and rule that the version with the latest valid_from on or before the business date is used, the answer naming the version it used. |
| RWB-ITG-E2015-ITG, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E2015-APP, RWB-S8-E2015-APP | R-22506 | GAP-3099 | Register gap | Solution architect, with the rwb-deviation owner, the rwb-case contract and reference-data owners, the product owner of the deviation service level, the rule-set owner of the Deviations package and the QA lead | RWB-S8-E2015-APP: the deviation section of the case record view has no read operation, no published view field names, no label for a code other than X3, no published value for the deviation service level and no escalation target | Publish the case deviation read as a service operation with a catalogue row, or amend the Ownership Map to carry GET /cases/{caseId}/deviations; freeze the deviation view field names in RWB-P3-E2015-CON; publish LOV-DEVIATION with a label per code and LOV-DEV-OUTCOME with a label per value; publish the deviation service level, its calendar and the row that holds it; publish the escalation target and the codes R-DEV-20 covers; record the six platform contracts as template dependencies of S8 beside the H row of the secondary slice; publish a level for each legacy test case. |
| RWB-ITG-E1013-ITG, RWB-ITG-E2009-ITG, RWB-P1-E1013-APP, RWB-P3-E1013-APP, RWB-P3-E2009-APP, RWB-P9-E1013-APP, RWB-P9-E1013-CON, RWB-P9-E1013-OPS, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-P9-E8001-APP, RWB-P9-E8001-CON, RWB-P9-E8002-APP, RWB-P9-E8002-CON, RWB-S8-E2009-APP | R-28480 | GAP-1644 | Register gap | Business lead | The program BRD has no requirement section for P9 reporting | Keep the epic-level keys as the trace target and state the coverage basis in section 11.2 until a P9 requirement section exists |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1023-ITG, RWB-ITG-E2016-ITG, RWB-P3-E1023-APP, RWB-P3-E1023-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P4-E1023-APP, RWB-P5-E2016-APP, RWB-S8-E1023-APP | R-28538 | GAP-1577 | Register gap | Business analyst with the P3 product owner | The case record view and its history timeline are listed as P4 features while the screen and its endpoints belong to rwb-case | Move FEAT-ACA-11 and FEAT-ACA-12 with their acceptance criteria to FSD P3 in the next version, and leave in FSD P4 only the authorise, scope and masking behaviour the screen consumes, so each feature has one owner and one acceptance set. |
| RWB-ITG-E1062-ITG, RWB-ITG-E2015-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P3-E2015-APP, RWB-P3-E2015-CON, RWB-P3-E2015-OPS, RWB-P4-E1062-APP, RWB-P4-E2015-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP, RWB-S8-E2015-APP | R-28640 | GAP-1829 | Register gap | Compliance and PDPA officer | The retention period and the classification scheme of the deviation record are not set | State the record class and a working classification per entity, state no period, and take the periods and the scheme from DL26 and Q-012 before the first release. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-28740 | GAP-1638 | Register gap | Product owner | The only success measure of the module has no baseline and no measurement definition | Take the measure from the decision log as the FSD says, and have the product owner set the baseline, the target and the definition of 'the same day' before the wave-2 release note. |
| RWB-ITG-E2009-ITG, RWB-P3-E2009-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S8-E2009-APP | R-28752 | GAP-1659 | Register gap | Risk and model risk officer | No target is set for agent acceptance and override | Publish the two rates per agent and version and set no threshold until one is agreed |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28761 | GAP-3094 | Register gap | Business lead | The handler rows R-DEV-04 to R-DEV-06 and the SCR-05 deviation fragment layout are not in the sources | Read the four rows from the Business Rules and Routing Logic workbook at build time, render the fragment as a table of code, handler, paused state, contact stop and rule ID, and confirm the layout with the screen owner. |
| RWB-ITG-E2012-ITG, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P7-E2012-APP, RWB-S8-E2012-APP | R-28763 | GAP-3097 | Register gap | Business lead | The transfer reason codes R01 to R06 are an assumed set pending DL23 | Read the list at its version on the rwb-case reference-data contract, render whatever is in force, and hold the six codes as the default set until DL23 closes. |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28769 | GAP-0933 | Register gap | Compliance and PDPA officer with the P4 build squad | The masking version in force in SIT is not recorded anywhere | Record the masking version in force per environment in the policy pack load record, with its approver and valid-from date, and assert it in the SIT entry check |
| RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-28770 | GAP-1261 | Register gap | Data steward and data product owner | The module specification keeps two daily data-lake interfaces that DP-17 removes | Retire INT-19, INT-20 and the daily copy from the P7 documents in the next module-specification version; no lake element appears in this key's stories, chart or run book. |
| RWB-ITG-E2016-ITG, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P5-E2016-APP | R-28783 | GAP-1062 | Register gap | Data steward and data product owner | Which table supplies the document type label a timeline item shows | Display the label from document_type at the version in force, label_en by default and label_th by locale, and compare the list with LOV-DOC-TYPE through the reference-data contract of rwb-case rather than copying it; fall back to the type code when the row of that version is absent. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
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
| RWB-ITG-E2008-ITG | R-03717 | DOR-RWB-ITG-E2008-ITG-17 | header | Definition of Ready item 17 Dependencies: Fail | The fail comes from build status: the 8 Integration dependencies are not delivered yet, and story text cannot change that. Missing story RWB-P7-E1073-CON is tracked by CG-ALL-598. |
| RWB-ITG-E2010-ITG | R-03728 | DOR-RWB-ITG-E2010-ITG-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design for RWB-ITG-W2 in the W2 story folder or 22 Microservice Realignment. A sign-off is a governance record and can't be invented, so the placeholder stays. |
| RWB-ITG-E2010-ITG | R-03731 | DOR-RWB-ITG-E2010-ITG-22 | header | Definition of Ready item 22 Fake published: Fail | No published fake library version in the RWB-P1-E2010-CON chunks or 22 Microservice Realignment. The CON story only says to publish fakes. Placeholder stays. |
| RWB-ITG-E2010-ITG | R-03732 | DOR-RWB-ITG-E2010-ITG-23 | header | Definition of Ready item 23 Contract version fixed: Fail | The RWB-P1-E2010-CON chunks raise the same item 23 Fail and give no fixed contract version or tag, only /v1. The header keeps /v1 and the placeholder. |
| RWB-ITG-E2010-ITG | R-14251 | DOR-RWB-ITG-E2010-ITG-15 | section 1 | Definition of Ready item 15 INVEST: Partial | No size is given for this story. §1 and the Size row leave sizing to the squad at refinement, so Small and the two-week fit are not asserted. |
| RWB-ITG-E2012-ITG | R-03735 | DOR-RWB-ITG-E2012-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size for this story in 04 User Stories Epic 2 v8, Build Notes Epic 2 v4 or the C4-SBO build order. The squad sizes it at refinement; adding a number would invent one. |
| RWB-ITG-E2012-ITG | R-03736 | DOR-RWB-ITG-E2012-ITG-17 | header | Definition of Ready item 17 Dependencies: Fail | The 3 dependencies not being done is build status. RWB-P7-E1073-CON is only in the _work/msr/dor review, not in the story. CG-ALL-625 is still open. |
| RWB-ITG-E2012-ITG | R-03737 | DOR-RWB-ITG-E2012-ITG-21 |  | Definition of Ready item 21 Contract published: Fail | An ITG story needs no CON story of its own. The publication state of the named contracts is not in the sources, so there is no story edit. |
| RWB-ITG-E2012-ITG | R-14261 | DOR-RWB-ITG-E2012-ITG-15 | 1 | Definition of Ready item 15 INVEST: Partial | No size is given in the story or sources (see DOR-16), so the story cannot state that it fits within two weeks. |
| RWB-ITG-E2012-ITG | R-22457 | GAP-3096 |  | deviation has no transfer reason, rule ID or rule-version column, and the legacy write set is on the rwb-case tables | AC2 already keeps rule and version on the decision record. The deviation row needs nothing more, so there is no story edit. |
| RWB-ITG-E2013-ITG | R-03741 | DOR-RWB-ITG-E2013-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record exists; Ways of Working v3 and decision DT05 give only the sign-off rule and cadence. Recording one would invent an approval. |
| RWB-ITG-E2013-ITG | R-03744 | DOR-RWB-ITG-E2013-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published fake library version for RWB-ITG-E2013-CON in project .md files (grep for fake/stub library or pack versions). A version would be invented. |
| RWB-ITG-E2013-ITG | R-14268 | DOR-RWB-ITG-E2013-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | No source gives a size or sprint fit. The Size row reads Not specified; INVEST is checked at refinement. |
| RWB-ITG-E2014-ITG | R-03749 | DOR-RWB-ITG-E2014-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size value is in the sources; the Size row leaves it to the squad at refinement, within two weeks. |
| RWB-ITG-E2014-ITG | R-03751 | DOR-RWB-ITG-E2014-ITG-22 | header | Definition of Ready item 22 Fake published: Fail | No fake library version in the sources (searched E2014 story files, ITG E2014 files, contract fake lines). The header row keeps the Not specified placeholder. |
| RWB-ITG-E2015-ITG | R-03755 | DOR-RWB-ITG-E2015-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design sign-off found in 01 Decisions and governance or 05 Technical architecture .md files. Recording one would invent a sign-off. |
| RWB-ITG-E2015-ITG | R-03756 | DOR-RWB-ITG-E2015-ITG-16 |  | Definition of Ready item 16 Size: Fail | No size found for this story or RWB-P3-E2015-CON in 04 User stories .md. The squad sets size at refinement, so no value can be written now. |
| RWB-ITG-E2015-ITG | R-03758 | DOR-RWB-ITG-E2015-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | RWB-P3-E2015-CON is Not started and Service Contract Catalog v1 has no E2015 entry. No published fake version exists to record. |
| RWB-ITG-E2016-ITG | R-03762 | DOR-RWB-ITG-E2016-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the source documents. The Size row records this and that the squad sizes the story at refinement. |
| RWB-ITG-E2016-ITG | R-03763 | DOR-RWB-ITG-E2016-ITG-21 |  | Definition of Ready item 21 Contract published: Fail | RWB-ITG-E2016-CON is not a story of the set, so it is not named as a contract dependency. No publication of the contract is claimed. |
| RWB-ITG-E2016-ITG | R-14292 | DOR-RWB-ITG-E2016-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | Whether the story fits within two weeks cannot be stated without a squad estimate. The Size row is left for refinement. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01212 | RWB-ITG-E2008-ITG | CG-ALL-597 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or consume a published operation |
| CDC-01250 | RWB-ITG-E2009-ITG | CG-ALL-609 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story; story path unchanged. |
| CDC-01275 | RWB-ITG-E2010-ITG | CG-ALL-616 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story. |
| CDC-01287 | RWB-ITG-E2012-ITG | CG-ALL-624 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story |
| CDC-01290 | RWB-ITG-E2012-ITG | DOR-RWB-ITG-E2012-ITG-8 | 12.2, 12.4 | Publish POST /api/recovery/access/v1/authorise (CG-ALL-624). Event-type part resolved in story (CG-ALL-626) |
| CDC-01304 | RWB-ITG-E2013-ITG | CG-ALL-641 | 12.2 | Publish POST /api/recovery/access/v1/authorise in paths, through the provider's CON story, or the story must consume a published operation. |
| CDC-01306 | RWB-ITG-E2013-ITG | DOR-RWB-ITG-E2013-ITG-8 | 12.2, 12.4, 13 | Event name rwb.decision.DecisionRecorded.v1 applied in 12.4 and 13. |
| CDC-01326 | RWB-ITG-E2014-ITG | CG-ALL-655 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or have consumers switch to an already published operation. |
| CDC-01357 | RWB-ITG-E2015-ITG | CG-ALL-662 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-01359 | RWB-ITG-E2015-ITG | DOR-RWB-ITG-E2015-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-01373 | RWB-ITG-E2016-ITG | CG-ALL-667 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider CON story, or consume a published operation |
| CDC-01376 | RWB-ITG-E2016-ITG | DOR-RWB-ITG-E2016-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider CON story |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01219 | RWB-ITG-E2008-ITG | DOR-RWB-ITG-E2008-ITG-1 | 1 | Confirm a role code or role name for 'member of the integration and QA team' so §1 can cite it. |
| CDC-01254 | RWB-ITG-E2009-ITG | DOR-RWB-ITG-E2009-ITG-1 | 1 | Add the role 'member of the integration and QA team' or name its role code in Users Roles and Permissions v5 |
| CDC-01277 | RWB-ITG-E2010-ITG | DOR-RWB-ITG-E2010-ITG-1 | 1 | Add a role for the integration and QA team, or confirm an existing role code that covers it, so §1 names a valid role. |
| CDC-01278 | RWB-ITG-E2010-ITG | DOR-RWB-ITG-E2010-ITG-6 | 10 | Confirm RW-DATASTEW, RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE, RW-AUDIT, RW-PHONECOL and the integration and QA team exist as roles; RW-2026-000512 is a case ID, not a role. |
| CDC-01292 | RWB-ITG-E2012-ITG | DOR-RWB-ITG-E2012-ITG-1 | 1 | Add the role 'member of the integration and QA team' with its role code, or name an existing role; role code Not specified in the source documents (DOR-RWB-ITG-E2012-ITG-1). |
| CDC-01307 | RWB-ITG-E2013-ITG | DOR-RWB-ITG-E2013-ITG-1 | 1 | Add a role code for 'member of the integration and QA team', or name an existing role in section 1. |
| CDC-01315 | RWB-ITG-E2013-ITG | GAP-0930 | header | Add the rwb-decision service identity with Approval check R and no other Recovery right; security administrator confirms before the authorise contract is frozen. |
| CDC-01360 | RWB-ITG-E2015-ITG | DOR-RWB-ITG-E2015-ITG-1 | 1 | Add a role for the member of the integration and QA team, or name the existing role code the harness user holds, so section 1 uses a role code or name from the list. |
| CDC-01377 | RWB-ITG-E2016-ITG | DOR-RWB-ITG-E2016-ITG-1 | 1 | Add a technical role name and code for the integration and QA team member in §1; code Not specified in the source documents (DOR-RWB-ITG-E2016-ITG-1) |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01224 | RWB-ITG-E2008-ITG | GAP-2503 | 4, 12.2 | Story-side operations and workflow name are carried in §12.2 (GAP-1346) and §4 (GAP-1639). The remaining app-slice names belong to the RTM and app story. |
| CDC-01238 | RWB-ITG-E2008-ITG | CG-ALL-603 | 18 | §18 now includes the RTM v7 cases (DOR-12). Remaining differences are for the RTM to take up. |
| CDC-01286 | RWB-ITG-E2010-ITG | CG-ALL-620 | 18 | Align the test lists of REQ-RDF-014 and REQ-RDF-010 with RWB-ITG-E2010-ITG section 18 in the next RTM version. |
| CDC-01293 | RWB-ITG-E2012-ITG | DOR-RWB-ITG-E2012-ITG-12 | 16, 18 | Align the test case lists for REQ-WKM-003, REQ-WKM-007, REQ-WKM-008, REQ-CWC-010 and REQ-CWC-016 with section 18 of RWB-ITG-E2012-ITG. |
| CDC-01300 | RWB-ITG-E2012-ITG | CG-ALL-630 | 18 | Align the REQ-WKM-003 and REQ-WKM-007 test lists in RTM v7 with section 18 of this story in their next versions. |
| CDC-01361 | RWB-ITG-E2015-ITG | DOR-RWB-ITG-E2015-ITG-12 | 16, 18 | Section 16 maps test cases to AC1 to AC7; the RTM v7 list difference sits outside this story. |
| CDC-01368 | RWB-ITG-E2015-ITG | CG-ALL-664 | 18 | Align the test lists of REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 and the fourth requirement with section 18 in the next RTM version. |
| CDC-01378 | RWB-ITG-E2016-ITG | DOR-RWB-ITG-E2016-ITG-12 | 16, 18 | Align its test case lists for the requirements in section 18 of this story, including TC-E2-016-13-ITG on REQ-WKM-008. |
| CDC-01382 | RWB-ITG-E2016-ITG | CG-ALL-669 | 18 | Trace the same test cases as RWB-ITG-E2016-ITG section 18 for REQ-WKM-008, REQ-OCC-008, REQ-CWC-016 and REQ-DRI-002 in the next RTM version. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01214 | RWB-ITG-E2008-ITG | DOR-RWB-ITG-E2008-ITG-14 | header | Record the signed epic design for service epic RWB-ITG-W2 (sign-off role and date) so the story can cite it |
| CDC-01251 | RWB-ITG-E2009-ITG | DOR-RWB-ITG-E2009-ITG-14 |  | Record the signed epic design for RWB-ITG-W2 (who signed it, by role, and the date), so DoR item 14 can cite it |
| CDC-01289 | RWB-ITG-E2012-ITG | DOR-RWB-ITG-E2012-ITG-14 |  | No sign-off exists in the story or the sources. The sign-off must be confirmed in the epic design record. |
| CDC-01327 | RWB-ITG-E2014-ITG | DOR-RWB-ITG-E2014-ITG-14 | none | Record the signed epic design sign-off in the epic design record; the story cannot evidence it from its own text. |
| CDC-01374 | RWB-ITG-E2016-ITG | DOR-RWB-ITG-E2016-ITG-14 | header | Record the signed epic design for RWB-ITG-W2, with its sign-off role and date, so DoR item 14 can cite it |

### RWB-P6-E1052-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01336 | RWB-ITG-E2014-ITG | GAP-1264 | 12 | Publish approve, regenerate and hold on the rwb-comms contract with their states and error codes, or one outcome-coded operation; correct the Ownership Map api rows. |
| CDC-01337 | RWB-ITG-E2014-ITG | GAP-1268 | 7 | Serve the notice PDF as a document reference through rwb-document, and carry the addressee role and masked address from rwb-source-data decision-panel fields in the notice answer. |
| CDC-01338 | RWB-ITG-E2014-ITG | GAP-2384 | 12 | Publish POST .../notices/{noticeId}/approve, .../regenerate and .../hold with the listed request fields and 401/403/404/409/422/503 set; add rows to the rwb-comms API file and Ownership Map; list as consumed in RWB-P7-E2014-CON. |
| CDC-01340 | RWB-ITG-E2014-ITG | GAP-2386 | 7 | State in the rwb-comms API file that a template change regenerates on the same notice row: document_id and template_id move to the chosen Approved variant, version increments, and the previous document stays readable. |
| CDC-01341 | RWB-ITG-E2014-ITG | GAP-2387 | 12 | Baseline the notice answer fields id, caseId, documentId, noticeType, state, templateCode, templateVersion, templateState, approvedAt and decisionLogEntryId, with template states DRAFT, APPROVED and WITHDRAWN. |

### RWB-S8-E2009-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01266 | RWB-ITG-E2009-ITG | GAP-3088 | none (other document) | The gap concerns the S8 slice's INT-19 extract and data set in its service; its owner and replacement path belong to that story. |
| CDC-01267 | RWB-ITG-E2009-ITG | GAP-3089 | none (other document) | The legacy criterion and test case assignment belongs to the S8 slice story. No text for it is carried in this harness story. |
| CDC-01268 | RWB-ITG-E2009-ITG | GAP-3087 | none (other document) | The placement of the S8 slice, the seven owner reads, the matrix edge and the platform prerequisites belong to that story and the contract owners. |
| CDC-01272 | RWB-ITG-E2009-ITG | GAP-3090 |  | Publish the schedule id, calendar, catch-up policy and rerun input (workflow kit owner); the two Measure fields and dimension format (reporting owner); the alert channel and two recipients (rwb-comms); read the three filter lists as rwb-case reference data. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01302 | RWB-ITG-E2012-ITG | GAP-3095 |  | No story edit: sections 12.4 and 13 list no case status or legal-hold event for this story. The names belong in the rwb-case event catalogue. |
| CDC-01316 | RWB-ITG-E2013-ITG | GAP-1221 | header | Add rwb-comms as consumer of rwb.decision.ApprovalRequested.v1 for the escalation re-publish, also in the rwb-decision AsyncAPI document; do not add ApprovalEscalated. |
| CDC-01319 | RWB-ITG-E2013-ITG | GAP-1257 | header | The header records that ApprovalDecided, consumed in 12.4, has no catalogue row. Adding the row is for the event catalogue. |
| CDC-01325 | RWB-ITG-E2013-ITG | GAP-1254 | 7 | Mark INT-19, INT-20, lake partition, manifest and watermark retired; rwb-reporting builds from rwb.decision-record.v1; keep EV-08; drop lake from contract and deployment. |

### RWB-P7-E2014-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01346 | RWB-ITG-E2014-ITG | GAP-1258 | 4 | Publish the field list and mask flags of the SCR-11 and SCR-18 panels as the working read; confirm with route owner and three consumer sign-offs; correct by new contract version. |
| CDC-01347 | RWB-ITG-E2014-ITG | GAP-1259 | 4 | Carry GET /api/recovery/approvals/{approvalId} as the working read and register it with the route owner at the first version freeze. |
| CDC-01348 | RWB-ITG-E2014-ITG | GAP-1270 | n/a | Register GET /api/recovery/approvals/{approvalId} with a 2 s budget per downstream and the 1.2 s composition budget of the case screen; record measured p95 on the dashboard. |
| CDC-01353 | RWB-ITG-E2014-ITG | GAP-1266 | 7 | Set the queue page size default to 20 and the maximum to 100; publish field types for the screen model and the ApprovalPage response; confirm with front end and route owner. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01211 | RWB-ITG-E2008-ITG | CG-ALL-596 | 12.2 | Publish GET /api/recovery/source-data/v1/admin/data-quality/exceptions through the provider's CON story, or consume a published operation |
| CDC-01273 | RWB-ITG-E2010-ITG | CG-ALL-614 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP04/records through the provider CON story. |
| CDC-01274 | RWB-ITG-E2010-ITG | CG-ALL-615 | 12.2 | Publish GET /api/recovery/source-data/v1/admin/data-quality/exceptions through the provider CON story. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01213 | RWB-ITG-E2008-ITG | CG-ALL-598 | 13 | Create story RWB-P7-E1073-CON, or name the existing story key for the DP-04 dependency |
| CDC-01215 | RWB-ITG-E2008-ITG | DOR-RWB-ITG-E2008-ITG-21 | header | No contract story of this story's own exists. The listed reference-data contract RWB-P3-E1043-CON (GAP-0604) is not yet published. |
| CDC-01288 | RWB-ITG-E2012-ITG | CG-ALL-625 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that carries the DP-04 C dependency |

### RWB-P4-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01229 | RWB-ITG-E2008-ITG | GAP-0925 | - | Extend the envelope with area, right, scope, resource, filter, rowCount and matrixVersion, and fix the three answer codes at the wave 2 contract review. |
| CDC-01335 | RWB-ITG-E2014-ITG | GAP-0932 | 7 | Publish the authorise, me-permissions and masking-policies shapes and state whether the routed role or the holder is a request field. |
| CDC-01364 | RWB-ITG-E2015-ITG | GAP-0934 |  | Fix the authorise request with caseId, teamCode, ownerUserRef, escalatedToRole and escalatedAt; version it v1 with backward compatibility. |

### RWB-P8-E2008-OPS (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01230 | RWB-ITG-E2008-ITG | GAP-1352 | 19 | Pinned chart; two api replicas; worker floor, ceiling and sizes as values; three topics with platform defaults; gate every environment; canary or blue/green for PROD; down script per migration. |
| CDC-01235 | RWB-ITG-E2008-ITG | GAP-2505 | 13 | Carry the deployment slice; thresholds, counts and limits as environment values; review five runbook entries with the on-call rota before promotion. |
| CDC-01243 | RWB-ITG-E2008-ITG | GAP-1353 | 13 | Hold outbox-lag, dead-letter and workflow-failure thresholds as data with no target-like default; Platform administrator closes before PROD. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01245 | RWB-ITG-E2008-ITG | GAP-2495 |  | Publish the dry run as a read-only operation returning testResult with total, passed, failed, failing case IDs, per-case results and recorded dry-run counts. |
| CDC-01297 | RWB-ITG-E2012-ITG | GAP-2500 | 7 | AC2 requires a decision code on the record; the code itself is Not specified (GAP-2500) |
| CDC-01314 | RWB-ITG-E2013-ITG | GAP-0928 | header | Add GET /api/recovery/access/v1/doa-limits as a P4 operation with the query and response fields this story uses, correcting the v4 omission per R-PREC. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01248 | RWB-ITG-E2008-ITG | GAP-1349 | find it | Remove GET /cases/{id}/payments from the rwb-payment IN list or add a matching Ownership Map row. Story side to answer the case payment list via GET /proceeds with case scope, once its section text is supplied. |
| CDC-01333 | RWB-ITG-E2014-ITG | GAP-2093 | 7 | Assign the approval to P7 ApprovalWorkflow as child of NoticeDispatchWorkflow, with POST /notices/{noticeId}/approve as the litigation decision point; remove P6 'Decision: child: approval' from the OUT list. |
| CDC-01370 | RWB-ITG-E2015-ITG | GAP-1830 |  | Assign owners to SCR-06 and SCR-08 as gateway-bff composite routes over the S8 read and command contract; confirm with the edge owner. |

### RWB-P9-E1013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01260 | RWB-ITG-E2009-ITG | GAP-2570 | 11 | Declare the GET /reports/measures read shape for the harness and P3 catalog consumer; keep dashboard and data set in RWB-P9-E2009-APP. |
| CDC-01261 | RWB-ITG-E2009-ITG | GAP-2576 | 11 | Declare the three consumed operations and two owner-queue activities with names, payloads, errors and the INT-19 hand-off to rwb-integration. |
| CDC-01262 | RWB-ITG-E2009-ITG | GAP-2577 | 11 | Publish v1 increment: baselineValue delta, dimension fixing, declarations, activity contracts, subscriptions, JOB-15 registration, message map and fakes; placeholders with one review row. |

### RWB-P1-E2010-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01283 | RWB-ITG-E2010-ITG | GAP-0512 | find it | Property names and the guarantee claim read belong to the contract story RWB-P1-E2010-CON, not to this story. |
| CDC-01284 | RWB-ITG-E2010-ITG | GAP-2696 | find it | Active states go to a parameter row in the parameters contract; the operations belong to the contract story RWB-P1-E2010-CON. |
| CDC-01285 | RWB-ITG-E2010-ITG | GAP-2738 | find it | Declare GET /api/recovery/guarantee/v1/guarantee-claims with page, size, window and max size, 400 on empty or inverted window, in guarantee OpenAPI and this contract, with a fake. |

### RWB-P7-E2013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01305 | RWB-ITG-E2013-ITG | DOR-RWB-ITG-E2013-ITG-21 | header | Contract dependency RWB-P7-E2013-CON added |
| CDC-01318 | RWB-ITG-E2013-ITG | GAP-1255 | header | Baseline the five approval resources from TSD P7 T3.1 field names in camelCase, fix the required property of each ApprovalAction call, and add the case-status operation or its event subscription to the Ownership Map. |
| CDC-01320 | RWB-ITG-E2013-ITG | GAP-0732 | header | Fix the approval event fields consumed, the task fields written including approval and preparer references, the escalation representation, the status mapping, the composite route field list, and the rwb-case login name from the ACE DB naming decision. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01330 | RWB-ITG-E2014-ITG | CG-ALL-654 | Header | Add list LOV-OVERRIDE-REASON, or point the story to an existing Reference Data v5 list. |
| CDC-01331 | RWB-ITG-E2014-ITG | DOR-RWB-ITG-E2014-ITG-20 | 8 | Add LOV-OVERRIDE-REASON as a list of values; it is used by BR6 and is missing from v5. |
| CDC-01355 | RWB-ITG-E2014-ITG | GAP-2391 | 8 | Add LOV-HOLD-REASON with REFUSED_BY_APPROVER and TEMPLATE_WITHDRAWN; keep switch key rwb.decision.notice-approval read by rwb-comms and rwb-decision until the platform feature-flag owner renames it. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01218 | RWB-ITG-E2008-ITG | CG-ALL-601 | 16 | Add TC-E2-008-10-ITG with Given: RW-CASEOWN calls GET /proceeds; When: the call is made; Then: refused with MSG-P4-002; copied from the §16 row. |
| CDC-01291 | RWB-ITG-E2012-ITG | CG-ALL-628 | 16 | Add rows for TC-E2-012-15-ITG in the next Test Cases version, with Given, When and Then copied from legacy criterion AC13 (BR12) of RWB-E2-012. |

### RWB-P8-E2008-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01231 | RWB-ITG-E2008-ITG | GAP-1354 | - | Add AC1, AC3, AC4 and AC5 to the acs list of RWB-P8-E2008-APP in the next split plan revision. |
| CDC-01240 | RWB-ITG-E2008-ITG | GAP-0603 |  | Record the payment-matching run's operator in the authority table; keep the P8 to P1 step as one REST hop under the run's Temporal activity; correct the activity description in the Temporal Workflow and Activity Catalog. |

### OTHER:FSD P8 v3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01232 | RWB-ITG-E2008-ITG | GAP-1629 |  | Feature overview FEAT-PAY-06: build the settlement booking confirmation in wave 2 with EP03 (first in E3); proceeds features stay in wave 3. Align Epics 3 to 8 BRD DEP-005. |
| CDC-01233 | RWB-ITG-E2008-ITG | GAP-1635 |  | FEAT-PAY-11: reconcile to ACE payment and account position and to the delivered posting file confirmed by rwb-integration; ledger return only if published, else open question. |

### RWB-P8-E2008-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01234 | RWB-ITG-E2008-ITG | GAP-2504 | 12 | Publish v1 with placeholders and review rows; gate the tag on contract tests and schema lint; name correction is a patch, shape change a new version. |
| CDC-01237 | RWB-ITG-E2008-ITG | GAP-1347 | 7 | Publish schemas for TreatmentBooked, PaymentMissed and ProceedsMatched on rwb.payment.events.v1 with PaymentMissed fields treatmentId, dueDate, amountDue and ProceedsMatched fields proceedsId, caseId, amount; TreatmentBooked fields Not specified in the source documents (GAP-1347); CloudEvents envelope; new version for added fields. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01241 | RWB-ITG-E2008-ITG | GAP-0927 |  | Carry the filter and row count in the actions list of the decision-record entry; add the capability area and the right to the same list in the next LDM version. |
| CDC-01339 | RWB-ITG-E2014-ITG | GAP-2385 | 12 | Add nullable decision_log_entry_id uuid to notice with a unique index, in Flyway step V2014_1__notice_decision_reference.sql, set by approve and hold, and add it to the logical data model before wave 2 build. |

### RWB-P9-E2009-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01255 | RWB-ITG-E2009-ITG | DOR-RWB-ITG-E2009-ITG-10 | none (other document) | SCR-37 is owned by RWB-P9-E2009-APP and this story builds no screen, so the states belong in that story. |
| CDC-01265 | RWB-ITG-E2009-ITG | GAP-2578 | 11 | Ship deployment values for logins, replicas, consumer offsets, retention, alert thresholds, run message ID and runbook entries per the deployment slice fix. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01258 | RWB-ITG-E2009-ITG | GAP-0255 | none (other document) | The control tables and the queue measure ownership belong to the data model and the ownership map, not this story. |
| CDC-01259 | RWB-ITG-E2009-ITG | GAP-0257 | 11 | Key owner and team by ID on events; resolve display name from P3 queue_member and assignment behind rwb-access masking; state the rule in v3 Dimensions. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01263 | RWB-ITG-E2009-ITG | GAP-0731 | 11 | Record the case-fact read schema, cut-off rule and fact transport agreed with the rwb-reporting owner. |
| CDC-01375 | RWB-ITG-E2016-ITG | DOR-RWB-ITG-E2016-ITG-22 | 12.8 | Record the published fake library version for each provider contract used in §12.8 (rwb-case, rwb-document, rwb-decision, rwb-comms) |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01280 | RWB-ITG-E2010-ITG | GAP-3194 | find it | Raise an ACE DB story for each of S2, S4, S5, S6, S7, P6 and P8, or attach the column drop to their creating APP story; cite the chosen story on register row 121 before wave 2. |
| CDC-01358 | RWB-ITG-E2015-ITG | DOR-RWB-ITG-E2015-ITG-21 | header | Add dependency row: RWB-ITG-E2015-ITG depends on RWB-P3-E2015-CON, class C. |

### RWB-P1-E2010-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01281 | RWB-ITG-E2010-ITG | GAP-0509 | find it | Add the rwb-guarantee guarantee claim read as a C dependency with a fake returning no claim, and the rwb-case case-existence answer from RWB-P3-E2004-CON with a fake. |
| CDC-01282 | RWB-ITG-E2010-ITG | GAP-2695 | find it | Name GET /treatments and GET /treatments/active-count on /api/recovery/treatment/v1 (S2) in section 12.2 in place of the case contract RWB-P3-E2004-CON reads. |

### RWB-P3-E2012-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01295 | RWB-ITG-E2012-ITG | GAP-0710 |  | Fix one selection element: an ordered array with caseId, the assignment or refusal messageId, and done and total counts; the order is the caller's; the summary is derived from the array, never a second call. |
| CDC-01296 | RWB-ITG-E2012-ITG | GAP-0711 |  | Fix a refusal element with a reason code, the owner list with open-case count and cap each, and the current and target state; cap and hold are read inside the operation before the first write. |

### RWB-S8-E2012-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01298 | RWB-ITG-E2012-ITG | GAP-3093 |  | Publish GET /cases/{caseId}/deviations on /api/recovery/deviation/v1 as the read for the move and the SCR-05 panel; keep DeviationRaised and DeviationCleared for the event-fed flag; fix the read schema in the service CON story. |
| CDC-01303 | RWB-ITG-E2012-ITG | GAP-3091 | Header | The plan build list belongs to the split plan. Header Contract dependencies stays None, consistent with GAP-2501. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01366 | RWB-ITG-E2015-ITG | GAP-0714 |  | Add GET /cases/{caseId}/deviations to the S8 rows and the S8 API file. |
| CDC-01380 | RWB-ITG-E2016-ITG | GAP-0716 |  | Contract and ownership record sit outside this story; story text not changed. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01216 | RWB-ITG-E2008-ITG | DOR-RWB-ITG-E2008-ITG-22 | 12.8 | Publish the contract fake library for RWB-P3-E1043-CON and record its version so §12.8 of this story can cite it |

### OTHER:rwb-source-data OpenAPI; OTHER:rwb-access OpenAPI; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01217 | RWB-ITG-E2008-ITG | DOR-RWB-ITG-E2008-ITG-8 | 12.8 | Two paths are missing from the OpenAPI files. The story-side event name is aligned to the catalog under CG-ALL-599. |

### OTHER:07 Screens and experience/Recovery Workbench Screen Specifications v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01220 | RWB-ITG-E2008-ITG | DOR-RWB-ITG-E2008-ITG-10 | 13 | Define empty, loading and error behaviour for SCR-14 and SCR-44, and empty and error behaviour for SCR-28. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01221 | RWB-ITG-E2008-ITG | DOR-RWB-ITG-E2008-ITG-12 | 16, 18 | Add TC-E2-008-10-ITG and TC-E2-008-11-ITG to Test Cases; align RTM test lists for REQ-CHO-007 and REQ-CHO-009 with story section 18. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01222 | RWB-ITG-E2008-ITG | GAP-3175 | find it | Name AceDataReady (EV-26) as the target event on rwb.source-data.events.v1 and list LoadCompleted as its legacy alias. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01223 | RWB-ITG-E2008-ITG | GAP-2395 | find it | Read the three Epic 2 package codes and version labels as the fixture set; settle rwb-comms package assignment with the rule registry owner before integration. |

### OTHER:Functional Specification Document S2 (A2.10; OTHER:A2.11; OTHER:A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01225 | RWB-ITG-E2008-ITG | GAP-1703 | find it | Record the booking reference from TreatmentBooked and the break from PaymentMissed; rwb-payment owns booking, matching and posting; release request goes through the integration contract. |

### OTHER:Functional Specification Document P8 v3 (A2.3.4.1 to A2.11.4.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01226 | RWB-ITG-E2008-ITG | GAP-1625 | find it | Replace the eight placeholder criteria with testable criteria from the feature statement, rules and fields, marked as new; FSD owner confirms before wave 3 system test. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01227 | RWB-ITG-E2008-ITG | GAP-1626 | find it | Align the P8 operations to the API Specification v4 pair GET /proceeds and POST /proceeds/{proceedsId}/match; confirm before the contract story closes. |

### RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01228 | RWB-ITG-E2008-ITG | GAP-0926 | - | Publish letters of all 14 capability areas per role with each role's default scope as a new T6.1 version, then load through RWB-P4-AD002-APP. |

### RWB-S2-E2008-APP; RWB-P8-E2008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01236 | RWB-ITG-E2008-ITG | GAP-2693 | 7 | Route the match and the miss through ProceedsMatched and PaymentMissed via inbox, name activities applyProceedsMatched and holdMissedInstallment, serve plan position as elements of API-S2-002, confirm package and frequency at contract freeze. |

### OTHER:FSD P8 v3 and TSD P8 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01239 | RWB-ITG-E2008-ITG | GAP-1624 | 18 | Fill the Requirements served table in FSD P8 v3 and the Requirement traceability table in TSD P8 v2 with the REQ IDs served, or state that P8 has no requirement ID of its own. |

### OTHER:rwb-payment service AsyncAPI document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01242 | RWB-ITG-E2008-ITG | GAP-1351 |  | Name DecisionRecorded as a produced event whose schema is owned by rwb-decision; publish it only through the local library of DP-03. |

### OTHER:Work Package plan generator (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01244 | RWB-ITG-E2008-ITG | GAP-2180 |  | Keep one Work Package per story slice: drop B2-P1-014 or drop RWB-E2-008 from B-P1-08 fanout; add a plan-uniqueness check to checks/run_all.py. |

### RWB-P7-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01246 | RWB-ITG-E2008-ITG | GAP-2498 | 16 | Keep the ten legacy TC IDs, map System to Component and Access to Contract, leave legacy criteria with their owning slices and the ITG story. |

### OTHER:Recovery Workbench Business Requirements Program v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01247 | RWB-ITG-E2008-ITG | GAP-1641 | 18 | Add section 5.11 (REQ-S4-010) to the section 11 note on where P8 requirements are carried. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01249 | RWB-ITG-E2009-ITG | CG-ALL-608 | 12.2 | Publish GET /api/recovery/deviation/v1/deviations through the provider CON story; story path unchanged. |

### RWB-P9-E2009-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01252 | RWB-ITG-E2009-ITG | DOR-RWB-ITG-E2009-ITG-22 |  | Record the published contract fake library version for the v1 baseline |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01253 | RWB-ITG-E2009-ITG | DOR-RWB-ITG-E2009-ITG-8 | 12.2 | Publish GET /api/recovery/deviation/v1/deviations and POST /api/recovery/access/v1/authorise through provider CON stories. Event type fixed in this story (CG-ALL-610). |

### RWB-P9-E6037-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01256 | RWB-ITG-E2009-ITG | GAP-2579 |  | Record as confirmed its assumed defaults for the benefit-model measure set, monthly timing, month key, screen and requirement ID (ASM-4251, ASM-4252 and related rows). |

### OTHER:Data model workbook v3; OTHER:Facts sheet (Facts!A2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01257 | RWB-ITG-E2009-ITG | GAP-0251 | none (other document) | Story AC1 already reads the rwb-reporting model with no data lake; the fact-table definition change belongs to the data model workbook. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01264 | RWB-ITG-E2009-ITG | GAP-1563 | 11 | Name the P3 exception visibility on the case and the P8 matching rule in both PRDs; correct the REQ-CHO-009 row assignment. |

### OTHER:v3 fact workbook; OTHER:Facts sheet (F6; OTHER:F10; OTHER:F12; OTHER:F13) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01269 | RWB-ITG-E2009-ITG | GAP-0253 | none (other document) | The refresh schedule belongs to the fact workbook. This harness story defines no refresh. |

### OTHER:v3 fact workbook; OTHER:Read model sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01270 | RWB-ITG-E2009-ITG | GAP-0256 | none (other document) | The late-arrival, freeze and replay rules belong to the read model definition. The harness only asserts the results. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:FSD P3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01271 | RWB-ITG-E2009-ITG | GAP-0258 | none (other document) | The Power BI publishing text sits in the LDM and the FSD. Those documents must remove it. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01276 | RWB-ITG-E2010-ITG | DOR-RWB-ITG-E2010-ITG-8 | Header | Publish the three unpublished operations (CG-ALL-614, CG-ALL-615, CG-ALL-616) through provider CON stories. |

### OTHER:Batch and Scheduling (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01279 | RWB-ITG-E2010-ITG | GAP-3176 | find it | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### RWB-P7-E2027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01294 | RWB-ITG-E2012-ITG | GAP-2502 | 1 | Section 1 states the boundary with RWB-P7-E1008-APP |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01299 | RWB-ITG-E2012-ITG | GAP-2501 |  | Record as non-blocking platform and published contracts, built against their fakes: RWB-PLT-E1027-CON (DP-03), RWB-PLT-E1072-CON and RWB-P7-E1073-CON (DP-04), RWB-PLT-E1043-CON and RWB-P3-E1043-CON (DP-07), RWB-PLT-TE006-CON (DP-09), RWB-PLT-E1043-CON and RWB-PLT-E1071-CON (DP-10), RWB-PLT-E1047-CON (DP-14), RWB-PLT-E1044-CON (DP-15), RWB-PLT-N001-CON (DP-19); metadata rows unchanged. |

### OTHER:CON stories of rwb-case, rwb-decision, rwb-access and rwb-source-data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01301 | RWB-ITG-E2012-ITG | GAP-3092 | 15 | Publish the operation names, paths and schemas of the LOV-TRANSFER-REASON reference read, rwb-decision package read, rwb-access authorise call and rwb-source-data case-facts read. |

### OTHER:rwb-case contract and FSD P7 (A2.15; OTHER:A2.16) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01308 | RWB-ITG-E2013-ITG | GAP-1623 | 7 | Record the choice in the case contract (P3 reaction to ApprovalRequested, preferred) and in FSD acceptance criteria A2.15 and A2.16 |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Epic 2 contract tables (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01309 | RWB-ITG-E2013-ITG | GAP-3177 | 7 | Register the five-minute next-action Schedule in the catalog and delete EV-18 from the Epic 2 contract tables |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P4-E1038-APP; RWB-P4-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01310 | RWB-ITG-E2013-ITG | GAP-0842 | 7 | Serve GET /doa-limits once on the ownership map path; RWB-P4-AD016-APP owns the answer; RWB-P4-E2013-APP owns routing only |

### RWB-P4-E1037-CON; RWB-P7-E2013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01311 | RWB-ITG-E2013-ITG | GAP-1251 | 7 | State the level lookup as a read with 2 s budget; approval stores delegation_limit_id, approval_level and limit_version only, with no join, view or foreign key |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01312 | RWB-ITG-E2013-ITG | GAP-1252 | 7 | Add GET /api/recovery/access/v1/doa-limits owned by P4, with its query and answer, to the catalogue and operation list |

### RWB-P4-E1037-CON; RWB-P7-E2013-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01313 | RWB-ITG-E2013-ITG | GAP-1256 | 7 | Record the warm-start local read-through cache rule, refreshed on DoaLimitChanged, with an alert on a stale version |

### OTHER:TSD P6 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01317 | RWB-ITG-E2013-ITG | GAP-1222 | header | Confirm or extend the notice table with approval reference, escalation level, recipient role, recipient user reference and send time; confirm GET /notices/{noticeId} and POST /cases/{caseId}/messages on /api/recovery/comms/v1. |

### RWB-ITG-E2013-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01321 | RWB-ITG-E2013-ITG | GAP-1223 | header | Set H list to None plus the DP platform contracts, and C list to RWB-P7-E2013-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON; story stays Day 1. |

### RWB-PLT-TE006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01322 | RWB-ITG-E2013-ITG | GAP-1220 | 7 | Add escalation template row: message ID MSG-P7-011, placeholders {decision} and {caseNo}, channel from LOV-CHANNEL, Approved version; retry from outbox policy; template code and channel agreed at wave 2 design review. |

### OTHER:TSD P7 v2 (T8 traceability table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01323 | RWB-ITG-E2013-ITG | GAP-1263 | 18 | Map REQ-APD-002 and REQ-APD-006 to FEAT-APD-08 with RWB-E2-014 (screen) and to FEAT-APD-01 with RWB-E2-013 (routing). |

### OTHER:Edge and gateway design (gateway-bff) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01324 | RWB-ITG-E2013-ITG | GAP-1621 | 15 | Record which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations and which states it owns, with the four screen contracts. |

### OTHER:Contract story for RWB-ITG-E2014 (not in the story set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01328 | RWB-ITG-E2014-ITG | DOR-RWB-ITG-E2014-ITG-21 | Header | RWB-ITG-E2014-CON is not a story of the set; header shows Not specified until the contract is published. |

### OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01329 | RWB-ITG-E2014-ITG | DOR-RWB-ITG-E2014-ITG-8 | Header | Path is missing from rwb-access. The event type rename is made in the story under CG-ALL-656. |

### OTHER:rwb-case contract (case state and task ownership) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01332 | RWB-ITG-E2014-ITG | GAP-1623 | 7 | Decide whether the Waiting approval move and the approval task are a P3 reaction to ApprovalRequested (preferred) or a P3 call; record in the contract and in FSD A2.15 and A2.16. |

### RWB-P7-E2014-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01334 | RWB-ITG-E2014-ITG | GAP-2216 | 7 | Publish the case-facts projection with inputAsOf, the refusal and return events, the task code and reference row, and the dated contact read in the baseline reviews. |

### OTHER:TSD P6 v2 (T-A.1 and T6.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01342 | RWB-ITG-E2014-ITG | GAP-2388 | 12 | Add rows for the three notice operations as Litigation right A with scope applied, enforced at gateway-bff via rwb-access; rwb-decision calls them with service identity, approver user identifier and decision entry reference. |

### OTHER:FSD P6 v3 (A2.1.2) and TSD P6 v2 (T4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01343 | RWB-ITG-E2014-ITG | GAP-2390 | 12 | Let the notice move write one local decision record through the library with code D7.1, rule, notice and case IDs, template code and version, state from and to, reason code, approver and approval entry reference. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:P6 contract story; RWB-S4-E5001-CON; OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01344 | RWB-ITG-E2014-ITG | GAP-2743 |  | Add two consumed rows as C dependencies with placeholders; declare notice and template ownership (P6); name P6 operations; keep template status on notice contract; trace REQ-S4-001; decide D7.1 gate. |

### RWB-ITG-E2014-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01345 | RWB-ITG-E2014-ITG | GAP-1265 | header | Add C rows for RWB-P1-E1015-CON and RWB-P3-E1018-CON to this key, or record both reads as route-level composites of RWB-PLT-N001-CON. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:S4 rwb-litigation; OTHER:P3 rwb-case) and EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01349 | RWB-ITG-E2014-ITG | GAP-2742 | n/a | Add non-blocking C rows for the P6 notice generate and send and the rwb-case stage answer; record notice and template rows as P6's or correct the S4 row; name the P6 operation and case answer; add REQ-S4-001 to the key trace; decide the D7.1 approval path once in the EP05 PRD. |

### OTHER:TSD P7 v2 (traceability table T8) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01350 | RWB-ITG-E2014-ITG | GAP-1263 | 8 | Correct the REQ-APD-002 row to FEAT-APD-08 with RWB-E2-014 (screen) and the REQ-APD-006 row to FEAT-APD-01 with RWB-E2-013 (routing). |

### OTHER:Edge and gateway design (gateway-bff composition) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01351 | RWB-ITG-E2014-ITG | GAP-1621 | 7 | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service and which this service owns; record the four screen contracts there, not in this PRD. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:41; OTHER:42; OTHER:43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01352 | RWB-ITG-E2014-ITG | GAP-1262 | 7 | The story consumes rwb.decision.ApprovalDecided.v1 in section 12; the missing event-catalogue row is for the source documents to settle. |

### OTHER:Platform observability configuration for the approval screen (ADR-023) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01354 | RWB-ITG-E2014-ITG | GAP-1271 |  | Alert on any 5xx in five minutes, on route p95 above the registered budget, on a failed record write and on an empty D7.1 queue for 24 hours; review thresholds with the platform observability owner. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01356 | RWB-ITG-E2014-ITG | GAP-2389 |  | Keep H empty; add to C list: RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01362 | RWB-ITG-E2015-ITG | GAP-3177 | none | Register the five-minute next-action Schedule in rwb-case, and delete EV-18 from the Epic 2 contract tables. |

### OTHER:Contract story for rwb.deviation.events.v1 (EV-06; OTHER:EV-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01363 | RWB-ITG-E2015-ITG | GAP-1832 | 7 | Define the envelope of DeviationRaised and DeviationCleared: case key, deviation code, state, contact stop flag, return point and decision record reference, with no personal or financial value. |

### OTHER:Wave 2 case-record harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01365 | RWB-ITG-E2015-ITG | GAP-0399 | 7, 15 | Record the route path, merge order, fixtures, seeding, evidence format, retention and pass/fail gate agreed at the wave 2 entry check. |

### OTHER:FSD S8 (A2.2.2; OTHER:A2.3.2; OTHER:A2.6.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01367 | RWB-ITG-E2015-ITG | GAP-1817 |  | State the pause, prescription clock and resume as durable timers inside DeviationWorkflow and drop the Quartz integration point. |

### OTHER:FSD S8 Document control (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01369 | RWB-ITG-E2015-ITG | GAP-1834 |  | Add the v1 and v2 change notes, dates and contents when the S8 folder is completed. |

### OTHER:rwb-case values files and alert runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01371 | RWB-ITG-E2015-ITG | GAP-0715 |  | No threshold appears in the sources. The values are set in the values files and runbook, not in this story. |

### OTHER:DL10 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01372 | RWB-ITG-E2015-ITG | GAP-1831 |  | The story keeps all eight message IDs and serves them from the catalogue in Thai and English. The Thai wording and the approver sit in DL10 per NFR-059. |

### RWB-P7-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01379 | RWB-ITG-E2016-ITG | GAP-2210 | 8 | Publish the decision-record query path, filter and field list for the case's decision records used by the timeline. |

### OTHER:TSD P5 (T-A.2; OTHER:API-P5-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01381 | RWB-ITG-E2016-ITG | GAP-1059 | 8 | Add an inclusive from and to date window and the items at, type, summary, by, reference and doc_version; fix field names at the RWB-P3-E2016-CON baseline review. |

### RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01383 | RWB-ITG-E2016-ITG | GAP-2211 | 9 | Publish the timeline addition as v1.1, an additive minor version inside major version 1, with reasonCode, fromQueueCode, toQueueCode, ruleId, the TimelineSection state on a 200 response and the page total; type order, section timeout and page size stay parameters of rwb-case. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:P6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01384 | RWB-ITG-E2016-ITG | GAP-0717 | 9 | Add GET /cases/{caseId}/notices under P6 with its query and response shape, and align the P6 contract baseline to it. |

### RWB-P3-E2016-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01385 | RWB-ITG-E2016-ITG | GAP-1060 | 9 | Add doc_version to the TimelineItem for document items; API-P5-003 returns the full version history when the item is opened. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0066 | Wave conflict S3 / EP02 | Tech lead | Resolved (directive) |
| GAP-0251 | The nine fact tables are defined in a data lake; the target has no data lake | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0253 | The refresh wording has no schedule in the target | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0255 | The read-model control tables and the queue measures are absent | Data architecture team | Resolved (directive) |
| GAP-0256 | No late-arrival, freeze or replay rule on any fact table | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0257 | dim_org holds an owner while events carry no personal data | Data steward | Resolved (directive) |
| GAP-0258 | The LDM and the FSD still publish to Power BI, which is removed | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0391 | Gateway-bff composite steering route, harness environment, measure-day seeding, evidence format and pass/fail gate not specified | Integration lead | Resolved (directive) |
| GAP-0392 | DP04 integration harness: composite record route, environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0393 | Payment matching integration harness: composite proceeds and exception route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0396 | Gateway-bff composite transfer route, harness environment, seeding, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0397 | Approval-routing harness environment, composite queue route and evidence format are not specified | Integration lead | Resolved (directive) |
| GAP-0398 | Integration harness values for the D7.1 decision-screen journey are not specified | Integration lead | Resolved (directive) |
| GAP-0399 | Wave 2 case-record harness: composite route, timer and deviation fixtures, environment and evidence format undefined | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0400 | Gateway-bff composite timeline route, harness environment and evidence gate are not specified | Integration lead | Resolved (directive) |
| GAP-0509 | The guarantee claim read of rwb-guarantee and the case-existence answer are not in the Work Package's contract list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0510 | The workflow and activity names of the stage 2 build are a target design choice | Solution architect | Resolved (directive) |
| GAP-0511 | The expected-by time of DP04 is assumed from the decision log and stated by no source | Data steward | Resolved (directive) |
| GAP-0512 | The field-level DP04 record schema and the shape of the guarantee claim read are not specified | Tech lead | Resolved (directive) |
| GAP-0513 | No deployment value, threshold, probe timing or fixture owner exists for the stage 2 build | DevOps lead | Resolved (directive) |
| GAP-0599 | The two read operations, their resource and element names and their error status set are stated by no source, because the legacy read was an in-process Java interface with no path, no query parameter and no status code | Solution architect with the P8 contract owner | Resolved (directive) |
| GAP-0601 | The order of the payment answer, the fold of a repeated payment_code, the row cap of one call and the number of ALS payments per business date are stated by no source | Tech lead with the P8 contract owner | Resolved (directive) |
| GAP-0602 | Architecture v5 slide 15 names a GET /accounts/{id} of rwb-source-data that TSD P1 T-A.1 does not carry and no Work Package owns, while this story answers nextInstallmentDate | Solution architect with the P1 tech lead | Resolved (directive) |
| GAP-0603 | The caller of both reads has no actor of record after the data-load actor was retired, and the architecture names the P8 to P1 call as a Temporal activity while the Work Package fixes one REST hop | Solution architect with the P8 tech lead and the P4 owner | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0710 | The partial-success shape of a selection and its summary message are not typed | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0711 | The at-cap and legal-hold pre-check answers have no typed shape | Solution architect, P3; tech lead of rwb-case | Resolved (directive) |
| GAP-0712 | Who may add or retire a transfer reason code is not specified | Centre of excellence; data steward | Resolved (directive) |
| GAP-0713 | The activity timeouts and the alert thresholds of the manual move are not specified | DevOps lead; service owner of rwb-case | Resolved (directive) |
| GAP-0714 | Deviation read path is absent from the Ownership Map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0715 | No source gives the alert values for the timer projection, the degradation rate or the breach volume | DevOps lead | Resolved (directive) |
| GAP-0716 | Case interaction-ledger read has no agreed owner-side contract path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0717 | Case-scoped notice list has no Ownership Map row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0731 | Case-fact read shape, cut-off rule and the reporting hand-off are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
| GAP-0925 | POST /authorise request and response shape is not specified for the payment-matching reads | Solution architect | Resolved (directive) |
| GAP-0926 | Permission letters for WRITE_OFF_AND_POSTING and TREATMENT_AND_OFFER and the scope of the Credit Administration role are absent from the RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0927 | The field that carries the filter and the row count in an AC-READ or AC-DENY entry is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0928 | GET /doa-limits is named in Architecture v5 and API v3 but absent from API Specification v4 | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0929 | The DoA lookup and authority-decision request and response shape is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0930 | The scope of the rwb-decision service identity inside rwb-access is not specified | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0932 | The request and response shape of the authorise operation is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0934 | The object attributes an authorise request carries are not specified | Solution architect | Resolved (directive) |
| GAP-1059 | The contract shape rwb-case and rwb-document share for the case timeline is not specified | Solution architect | Resolved (directive) |
| GAP-1060 | Whether the version count of a document travels on the timeline item or only on the document detail | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1061 | The summary wording of a document timeline item is not specified | Business analyst, P5 | Resolved (directive) |
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
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1347 | RWB-E2-008: the three event payloads and the decision-record element are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1348 | RWB-E2-008: the proceeds field set and its idempotency tables disagree between the legacy story and TSD P8 T3.1 | Solution architect | Resolved (directive) |
| GAP-1349 | RWB-E2-008: the case payment read, the SCR-28 and run-view field lists and the activity names of JOB-07 are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1350 | RWB-E2-008: the contract artefact names, the problem+json body, the MatchRequest shape and the registry mode of rwb-payment are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1351 | RWB-E2-008: the producer and the owner of DecisionRecorded disagree between the event catalogue and the messaging design | Solution architect | Resolved (directive) |
| GAP-1352 | RWB-E2-008: the deployment targets, the tier sizes, the rollout strategy and the rollback procedure of rwb-payment have no source | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1353 | RWB-E2-008: no source fixes a numeric target for the outbox-lag, dead-letter or workflow-failure alerts of rwb-payment | Platform administrator | Resolved (directive) |
| GAP-1354 | Legacy AC1, AC3, AC4 and AC5 of RWB-E2-008 are owned by no story in this split | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1563 | The BRD assigns payment matching to rwb-case while Architecture v5 gives it to rwb-payment | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-1646 | The data lake and the Power BI connection are removed but the whole reporting FSD is built on them | Solution architect | Resolved (directive) |
| GAP-1649 | The measure set is six definitions in one acceptance criterion and seven measures in another | Tribe lead with the Reporting and BI analyst | Resolved (directive) |
| GAP-1658 | SCR-37 has no owner and no serving path | Solution architect | Resolved (directive) |
| GAP-1662 | RWB-E2-009 promises a Power BI data set, which ADR-018 removes | Solution architect | Resolved (directive) |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1716 | The treatment record exists twice: as this service's live record and as P1's dated copy | Data architect | Resolved (directive) |
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
| GAP-2210 | No source gives the case status history, the transfer from-queue or the decision-record read behind the timeline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2211 | No source fixes the v1.1 timeline item shape, the section state or its version against the RWB-P3-E1023-CON baseline | Solution architect | Resolved (directive) |
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
| GAP-2570 | RWB-E1-013: the Power BI refresh that AC3 asserts has no mechanism once the data lake is removed, and the measures read is assigned to Epic 2 by the legacy story | Solution architect | Resolved (directive) |
| GAP-2576 | rwb-reporting steering dashboard (application slice): the consumed operation names, the workflow and activity names, the read-model design, the INT-19 replacement and the agent fact source are fixed by no single source | Solution architect, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the reporting service | Resolved (directive) |
| GAP-2577 | rwb-reporting steering dashboard (contract slice): the element names of the consumed declarations, the event envelope naming, the Measure delta, the schema increments and the file shape of the extract are fixed by no single source | Contract owner of rwb-reporting, with the owners of rwb-case, rwb-agent, rwb-source-data, rwb-integration and the event platform | Resolved (directive) |
| GAP-2578 | rwb-reporting steering dashboard (deployment slice): the login and secret reference, the replica and threshold values, the consumer offset and retention policy, the catch-up window, the backfill limit and the message ID of the run alert are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2579 | Benefit realisation: measure set, monthly timing, month key, screen and requirement ID are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-2693 | The delivery route of a match to rwb-treatment, the plan-position elements and the payment frequency of a plan are not specified for the S2 slice of RWB-E2-008 | Tech lead of rwb-treatment with the P8 rwb-payment owner, the P3 rwb-case owner and the P7 rwb-decision package owner at the wave 2 contract freeze | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2695 | The owner of the treatment changed-window and active-count reads conflicts between the DP04 story and the service ownership | Solution architect | Resolved (directive) |
| GAP-2696 | The two operation shapes, the active-state rule and the reference-data read path are fixed by no source document | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2738 | No source publishes a claim-side changed-window read for the DP04 build: the operation, its path, its page parameters, its maximum size, its error mapping and a count read all have no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2739 | The owner and the timing of the dated DP04 copy of a guarantee claim conflict: the legacy story writes dp_guarantee_claim itself and puts the claim interface in Epic 4, the target gives the copy to rwb-source-data in wave 2 and the claim record to rwb-guarantee in wave 3 | Solution architect | Resolved (directive) |
| GAP-2740 | No source says which side resolves a claim whose case does not exist, or whether the claim read answers such a claim at all | Data steward | Resolved (directive) |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3087 | RWB-S8-E2009-APP: a P9 Reporting story is placed in rwb-deviation with one C row and an empty build row, and the seven owner reads, the matrix edge and the platform prerequisites are unpublished | Solution architect | Resolved (directive) |
| GAP-3088 | RWB-S8-E2009-APP: DP-17 removes the data lake, so the INT-19 extract and the Power BI data set of the story have no target owner and no replacement path in this service | Solution architect | Resolved (directive) |
| GAP-3089 | RWB-S8-E2009-APP: the plan assigns the slice no legacy acceptance criterion while it keeps ten legacy test cases, and the legacy criteria lose their owned ids | Solution architect | Resolved (directive) |
| GAP-3090 | RWB-S8-E2009-APP: the schedule time, the dimension format, the two added Measure fields and the alert recipients have no published values for the deviation serving | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3092 | The operation names and shapes of the consumed contracts other than RWB-P3-E2012-CON are not published | Solution architect | Resolved (directive) |
| GAP-3093 | The open-deviation read the P3 slice names is not a row of the Ownership Map, and the S8 event subscription already carries the same fact | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3095 | The event names of the case status and legal-hold changes this service consumes are not published | Solution architect | Resolved (directive) |
| GAP-3096 | deviation has no transfer reason, rule ID or rule-version column, and the legacy write set is on the rwb-case tables | Solution architect | Resolved (directive) |
| GAP-3098 | The fifteen legacy test case IDs of RWB-E2-012 are carried by both slices | QA lead | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3177 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them | Solution architect with the case and workflow lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E2008-ITG | skipped AC ID | 98 | missing: AC2, AC6, AC7, AC8, AC9 |
| RWB-ITG-E2009-ITG | skipped AC ID | 103 | missing: AC5, AC6, AC7, AC8, AC9 |
| RWB-ITG-E2010-ITG | skipped AC ID | 110 | missing: AC5, AC6, AC7, AC8 |
| RWB-ITG-E2013-ITG | skipped AC ID | 96 | missing: AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14 |
