# RWB-SVC-S5 rwb-asset (Asset) - review pack, part 1 of 4 (RWB-S5-E1011-APP to RWB-S5-E3024-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 13 |
| Resolved in the stories | 278 |
| Cross-document (pending in another document) | 262 |
| Not applied (value not in the sources) | 20 |
| Open business decisions | 31 |
| Register gaps linked | 72 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S5-E1011-APP | 28 | 48 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E1011 APP Reconciliation and data quality report v2.md |
| RWB-S5-E3019-APP | 25 | 23 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3019 APP Take a repossessed vehicle onto the books v2.md |
| RWB-S5-E3019-CON | 21 | 19 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3019 CON Take a repossessed vehicle onto the books - contract v2.md |
| RWB-S5-E3020-APP | 29 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3020 APP Take a property onto the books after a deed in lieu v2.md |
| RWB-S5-E3020-CON | 18 | 14 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3020 CON Take a property onto the books after a deed in lieu - contract v2.md |
| RWB-S5-E3021-APP | 29 | 20 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3021 APP Take a property onto the books after an LED auction v2.md |
| RWB-S5-E3021-CON | 19 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3021 CON Take a property onto the books after an LED auction - contract v2.md |
| RWB-S5-E3022-APP | 25 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3022 APP Serve the statutory notice and prove delivery v2.md |
| RWB-S5-E3022-CON | 18 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3022 CON Serve the statutory notice and prove delivery - contract v2.md |
| RWB-S5-E3023-APP | 19 | 23 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3023 APP Track holding age against the provision steps v2.md |
| RWB-S5-E3023-CON | 15 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3023 CON Track holding age against the provision steps - contract v2.md |
| RWB-S5-E3024-APP | 20 | 22 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3024 APP Record and track the asset stock balance v2.md |
| RWB-S5-E3024-CON | 12 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3024 CON Record and track the asset stock balance - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S5-E3020-APP | R-02434 | CG-ALL-9629 | Script gap | Product owner | The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3020-APP | R-02435 | CG-ALL-9630 | Script gap | Product owner | The story adds ASSET_ON_BOOKS to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3021-APP | R-02439 | CG-ALL-9656 | Script gap | Product owner | The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3021-APP | R-02440 | CG-ALL-9657 | Script gap | Product owner | The story adds ASSET_ON_BOOKS to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3021-APP | R-02441 | CG-ALL-9658 | Script gap | Product owner | The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-TRANSFER-IN | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3021-APP | R-02442 | CG-ALL-9659 | Script gap | Product owner | The story adds ASSET_ON_BOOKS to the closed list LOV-TRANSFER-IN | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3024-APP | R-02468 | CG-ALL-9757 | Script gap | Product owner | The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3024-APP | R-02469 | CG-ALL-9758 | Script gap | Product owner | The story adds ASSET_ON_BOOKS to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3024-APP | R-02470 | CG-ALL-9759 | Script gap | Product owner | The story adds ASSET_PENDING_TAKE_ON to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3024-APP | R-02471 | CG-ALL-9760 | Script gap | Product owner | The story adds ASSET_ON_BOOKS to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3020-APP | R-12744 | CG-ALL-9640 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3021-APP | R-12758 | CG-ALL-9674 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3022-APP | R-12770 | CG-ALL-9707 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3023-APP | R-12784 | CG-ALL-9740 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3024-APP | R-12797 | CG-ALL-9773 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1011-ITG, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21922 | GAP-1651 | Register gap | Data steward and data product owner | The reconciliation and the data quality break are P1's, but FSD P9 specifies them as its own features | Read the reconciliation result and the break rows from P1's contract and hold the break view and the closure in P9 |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-S5-E3019-APP, RWB-S5-E3019-CON, RWB-S5-E4034-APP, RWB-S5-E4034-CON | R-23474 | GAP-1769 | Register gap | Solution architect with the data product owner | The asset population, the auction round volume and the holding cost volume are in no source | Size on the case volume and the NPA book stated in NFR-001 until the asset and round volumes are given, and record the volume as an open question that blocks the performance test only. |
| RWB-S5-E3023-APP, RWB-S5-E3023-CON | R-23484 | GAP-2855 | Register gap | S5 rwb-asset service owner with the data steward, the NPA business owner and the rwb-decision rule owner | The holding-age and provision-step facts have no column and no list value, no source in the extract set gives their field names, and no source prints the thresholds, the step percentages or the cost-of-carry rate | Agree the home of the holding age, the next provision step date, the cost to date and the holding status with the DB story of S5, keep the provision thresholds, the step percentages and the rate in the DISPOSAL package as versioned values, and let the verification loop replace the placeholders when the FSD S5 and TSD S5 are placed in the extract set. |
| RWB-S5-E3023-APP, RWB-S5-E3023-CON | R-23485 | GAP-2856 | Register gap | S5 rwb-asset service owner with the P1, P3, P8 owners and the owner of the Finance provision feed | The trigger, the four consumed owner contracts and the Finance provision feed route have no single source, and the plan records no contract, integration or external dependency for either slice | Let step D1 decide whether the four consumed surfaces become class C dependencies of this key and a Temporal row for rwb-payment, publish the operation and activity names from their owners, and let the Finance feed owner publish the route and the element; until then the stories build on fakes and carry the placeholder. |
| RWB-S5-E3024-APP, RWB-S5-E3024-CON | R-23488 | GAP-1472 | Register gap | Head of NPA | The non performing asset stock balance has no named owner | Name the NPA and asset manager as the role that owns the stock position per case, with the head of NPA as the recipient of the monthly report, and confirm both in the operating model. |
| RWB-S5-E3024-APP, RWB-S5-E3024-CON | R-23489 | GAP-1762 | Register gap | Head of NPA | The non performing asset stock balance must have one named owner and no source names the role | Hold the owner as a role in versioned reference data, refuse to publish the monthly balance where no owner role is in force, and leave the answer to Q-009. |
| RWB-S2-E3012-CON, RWB-S5-E3020-APP, RWB-S5-E3020-CON | R-29113 | GAP-2846 | Register gap | Business lead | The Land Office registration has no service owner in the target | Model the registration only as the registered transfer fact of RWB-S2-E3012-CON and keep the registration itself as an officer and legal step outside every service. |
| RWB-S5-E3019-APP, RWB-S5-E3019-CON, RWB-S5-E4034-APP, RWB-S5-E4034-CON | R-29152 | GAP-1764 | Register gap | Compliance and PDPA officer | The classification and the retention of the asset, listing and sale records are not set | Carry the classification stated in section 8 of this PRD, hold the periods as open, and record the classification on every record so a retention load can be applied without a rebuild. |
| RWB-S5-E3021-APP, RWB-S5-E3021-CON | R-29156 | GAP-2851 | Register gap | Solution architect and the business owner of S5 | RWB-S5-E3021: the FSD S5 and the TSD S5 that both slices read are In review with an empty sign-off table and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs before any status changes |
| RWB-S5-E3023-APP, RWB-S5-E3023-CON | R-29158 | GAP-2858 | Register gap | Solution architect and the business owner of S5 | The legacy story, the feature extract and the upstream documents the two slices read are not approved and the realigned stories have no sign-off | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs and place the FSD S5 and TSD S5 in the extract set before any status changes. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-S5-E3020-APP, RWB-S5-E3020-CON | R-38350 | ASM-4711 | Register assumption |  | The Land Office registration is kept outside every service and is read as the registered transfer fact of RWB-S2-E3012-CON and as an officer step. | Business lead |
| RWB-S5-E3023-APP, RWB-S5-E3023-CON | R-38365 | ASM-4726 | Register assumption |  | The holding age is derived from the asset dates the dictionary gives (stock_date, DF-COL-040, and transfer_in_date, DF-COL-036) and held as a durable timer of AssetDisposalWorkflow; the next provision step date is a reference value read at its version and held as the timer's end; no column is added for the age, the next step date or the cost to date beyond the columns the DB story of S5 publishes. | The S5 owner, the data steward and the DB story owner confirm the home of the age, the next provision step date and the cost to date, and that no new column is intended. |
| RWB-S5-E3023-APP, RWB-S5-E3023-CON | R-38369 | ASM-4730 | Register assumption |  | The rwb-source-data data-product read, the rwb-case state read and the rwb-case case-move answer are treated as class C dependencies even though the contract-dependency row of both slices is None: both stories build against the published documents of their owners and their fakes on Day 1, and the metadata rows keep the values the plan gives them. | Step D1 decides whether the three rows become C dependencies of this key or a rwb-source-data and rwb-case baseline is raised for them. |
| RWB-S5-E3023-APP, RWB-S5-E3023-CON | R-38373 | ASM-4734 | Register assumption |  | Both stories carry Status Draft (realignment v1) and the missing approval of the realigned stories, of the legacy master and of the FSD S5 and TSD S5 files (which are absent from the extract set) is treated as an assumption of this run rather than as a blocker; no behaviour and no value of either story depends on a signature, and no status of a source document is changed. | The verification loop collects the sign-offs and places the FSD S5 and TSD S5 in the extract set, and only then changes the status of the stories. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S5-E1011-APP | R-08131 | DOR-RWB-S5-E1011-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources; the only sign-off reference is Decision Log v11 DT05 (timing). Sign-off cannot be asserted (DOR-RWB-S5-E1011-APP-14). |
| RWB-S5-E1011-APP | R-08134 | DOR-RWB-S5-E1011-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version is recorded as published in the source set (probe cache searched). A version would be invented (DOR-RWB-S5-E1011-APP-22). |
| RWB-S5-E1011-APP | R-20090 | DOR-RWB-S5-E1011-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | Section 8 text for SCR-44 and SCR-45 is not in this chunk, so no anchor exists to add the empty, loading, error and no access states (DOR-RWB-S5-E1011-APP-10). |
| RWB-S5-E1011-APP | R-27266 | CG-ALL-9600 | 3 | Flyway file V1011_1__asset_quality.sql is not in the V0001..Vnnnn form | The next Vnnnn of the rwb-asset Flyway sequence is not in the sources. Searched the story set for db/migration and V0001 and found only the platform baseline. Migration name line L259 is outside this chunk. |
| RWB-S5-E3019-APP | R-27271 | CG-ALL-9613 | 7 | Criteria and tests keep legacy job and decision-log wording | AC1, AC4 and the §7 note already read decision record. The third JOB-nn/job record line is in §16, outside this chunk, and its text was not supplied, so it was not edited. |
| RWB-S5-E3019-APP | R-29153 | GAP-1768 | 14 | Four of the six messages this module shows belong to other services and the two of its own have no approved wording | Cite MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-S5-001 and MSG-S5-002 by ID. §14 text is not in this chunk, so no edit was made and the wording is not invented. |
| RWB-S5-E3019-CON | R-08144 | DOR-RWB-S5-E3019-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design record or signed sign-off found. Glob for epic design .md files returned none; grep for 'epic design' in the folder shows no sign-off. Needs the record. |
| RWB-S5-E3019-CON | R-20110 | DOR-RWB-S5-E3019-CON-15 INVEST | header | Definition of Ready item 15 INVEST: Partial | The Small and two-week sizing is not in the sources. |
| RWB-S5-E3019-CON | R-23469 | GAP-2838 |  | RWB-S5-E3019-CON: the consumed operation names, the case boundary name, the event consumer list and the error set have no published baseline | Section 12 text is not in the chunk and the story file was not found in the folder, so no old text can be matched. Tag date is not in sources. Owner confirmation is external. Placeholders already in header. |
| RWB-S5-E3019-CON | R-23476 | GAP-2853 |  | This legacy key owns no REST operation although the legacy story lists two, and the five consumed rows are class C in fact while the plan's C row is None | Sections 12.1 and 12.2 (lines 248-293) were not supplied and the story file was not found in the folder, so old text cannot be matched. Re-run with those lines. |
| RWB-S5-E3019-CON | R-27275 | CG-ALL-9624 | 14 | MSG-P1-001 text differs from the Error and Message Standard v4 | R-20115 says the English already equals the standard, so no edit is made here. |
| RWB-S5-E3020-APP | R-20116 | DOR-RWB-S5-E3020-APP-10 | 9-10 | Definition of Ready item 10 Screens and states: Partial | SCR-21 has loading and list states and SCR-22 has take-on, held, listed and sold states (pipeline story file, line 391). Empty, error and no-access states are absent. The sections holding them are outside this chunk, and no source gives their text. |
| RWB-S5-E3020-APP | R-20117 | DOR-RWB-S5-E3020-APP-11 | 9 | Definition of Ready item 11 Guardrails: Partial | Flagged field not named in the item or chunk; Not specified in the source documents (DOR-RWB-S5-E3020-APP-11). Section 9 and BR10 state no personal data; no flagged field found in the story or sources. |
| RWB-S5-E3020-CON | R-08155 | DOR-RWB-S5-E3020-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off in the project sources (grep for 'epic design' found nothing). Value cannot be stated without inventing it; needs the epic design record. |
| RWB-S5-E3020-CON | R-29151 | GAP-2839 | 7 | Legacy AC3 of a deed in lieu story tests the vehicle repossession rule R-DIS-01 | AC3 and its R-DIS rule table are in section 7, which is not in this chunk, so the old text cannot be copied. Re-run with section 7 included. |
| RWB-S5-E3020-CON | R-32582 | NEWAC-RWB-S5-E3020-CON-AC8 | 7 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | New AC8 belongs in section 7 and its test row in section 16, neither in this chunk. Proposed test is Not specified in the source documents (NEWAC-RWB-S5-E3020-CON-AC8). |
| RWB-S5-E3021-APP | R-27291 | CG-ALL-9676 | 7 | Criteria and tests keep legacy job and decision-log wording | Current AC5 and TC rows are not in this chunk, so no exact old text. L206 quotes legacy wording it says must stand word for word. Needs current sections 7 and 16. |
| RWB-S5-E3023-APP | R-08181 | DOR-RWB-S5-E3023-APP-16 | header | Definition of Ready item 16 Size: Fail | Squad sizing is not in the item or any source, so no value was written. |
| RWB-S5-E3023-APP | R-20172 | DOR-RWB-S5-E3023-APP-10 | 13 | Definition of Ready item 10 Screens and states: Partial | SCR-21/22 empty, loading, error and no-access states are in no source I checked; needs a source (CG-ALL-9742, CG-ALL-9743). |
| RWB-S5-E3024-APP | R-20189 | DOR-RWB-S5-E3024-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Section 10 text is not in this chunk, so no exact old text can be copied. FSD S5 v5 gives SCR-21/SCR-22 purpose only, so states need a Not specified placeholder. Rerun with section 10. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (26)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17544 | RWB-S5-E1011-APP | CG-ALL-9589 | 12.2 | The unpublished DP06/records path is kept as the consumed path and marked not published; the consumed path is Not specified in the source documents. |
| CDC-17663 | RWB-S5-E3021-APP | CG-ALL-9665 | 12.2 | Declare REST base /api/recovery/source-data/v1 for rwb-source-data, taken from the Document Index service table. |
| CDC-17664 | RWB-S5-E3021-APP | CG-ALL-9666 | 12.2 | Declare REST base /api/recovery/case/v1 for rwb-case, taken from the Document Index service table. |
| CDC-17683 | RWB-S5-E3021-CON | CG-ALL-9684 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the P1 rwb-source-data read. |
| CDC-17684 | RWB-S5-E3021-CON | CG-ALL-9685 | 12.2 | Declare REST base /api/recovery/case/v1 for the P3 rwb-case read. |
| CDC-17686 | RWB-S5-E3021-CON | DOR-RWB-S5-E3021-CON-8 | 12.2 | Declare REST bases /api/recovery/source-data/v1 and /api/recovery/case/v1; close the remaining P1 contract rows listed in the detcheck. |
| CDC-17698 | RWB-S5-E3022-APP | CG-ALL-9697 | 12.2 | Declare REST base /api/recovery/comms/v1 for POST /CASES/{CASEID}/NOTICES (API-P6-001), using the provider REST base in the Document Index service table. |
| CDC-17699 | RWB-S5-E3022-APP | CG-ALL-9698 | 12.2 | Declare REST base /api/recovery/comms/v1 for GET /NOTICES/{NOTICEID} (API-P6-002), using the provider REST base in the Document Index service table. |
| CDC-17700 | RWB-S5-E3022-APP | CG-ALL-9699 | 12.2 | Declare REST base /api/recovery/source-data/v1 for GET /PROOF-OF-DELIVERY, using the provider REST base in the Document Index service table. |
| CDC-17701 | RWB-S5-E3022-APP | CG-ALL-9700 | 12.2 | Declare REST base /api/recovery/case/v1 for GET /CASES/{CASEID} family (READ), using the provider REST base in the Document Index service table. |
| CDC-17714 | RWB-S5-E3022-CON | CG-ALL-9714 | 12.2 | Declare REST base /api/recovery/comms/v1 for POST /cases/{caseId}/notices (API-P6-001) using the Document Index service table |
| CDC-17715 | RWB-S5-E3022-CON | CG-ALL-9715 | 12.2 | Declare REST base /api/recovery/comms/v1 for GET /notices/{noticeId} (API-P6-002) using the Document Index service table |
| CDC-17716 | RWB-S5-E3022-CON | CG-ALL-9716 | 12.2 | Declare REST base /api/recovery/source-data/v1 for GET /proof-of-delivery using the Document Index service table |
| CDC-17717 | RWB-S5-E3022-CON | CG-ALL-9717 | 12.2 | Declare REST base /api/recovery/case/v1 for GET /cases/{caseId} family using the Document Index service table |
| CDC-17719 | RWB-S5-E3022-CON | DOR-RWB-S5-E3022-CON-8 | 12.2 | Declare REST bases /api/recovery/comms/v1, /api/recovery/source-data/v1 and /api/recovery/case/v1 for the consumed paths of section 12.2 |
| CDC-17728 | RWB-S5-E3023-APP | CG-ALL-9732 | 12.2 | Declare REST base /api/recovery/source-data/v1 for rwb-source-data, using the provider base from the Document Index service table. |
| CDC-17729 | RWB-S5-E3023-APP | CG-ALL-9733 | 12.2 | Declare REST base /api/recovery/case/v1 for rwb-case, using the provider base from the Document Index service table. |
| CDC-17733 | RWB-S5-E3023-APP | DOR-RWB-S5-E3023-APP-8 | header | Add the base paths /api/recovery/source-data/v1 and /api/recovery/case/v1 (servers currently lists only /api/recovery/v1). |
| CDC-17751 | RWB-S5-E3023-CON | CG-ALL-9746 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for rwb-source-data, taken from the Document Index service table. |
| CDC-17752 | RWB-S5-E3023-CON | CG-ALL-9747 | 12.2 | Declare the REST base /api/recovery/case/v1 for rwb-case, taken from the Document Index service table. |
| CDC-17754 | RWB-S5-E3023-CON | DOR-RWB-S5-E3023-CON-8 | 12.2, 12.5 | Declare REST bases /api/recovery/source-data/v1 and /api/recovery/case/v1 (CG-ALL-9746, CG-ALL-9747). Story-side P1 and P2 workflow items fixed in 12.5. |
| CDC-17767 | RWB-S5-E3024-APP | CG-ALL-9766 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for rwb-source-data in the yaml REST bases, using the provider base from the Document Index service table. |
| CDC-17768 | RWB-S5-E3024-APP | CG-ALL-9767 | 12.2 | Declare the REST base /api/recovery/case/v1 for rwb-case in the yaml REST bases, using the provider base from the Document Index service table. |
| CDC-17785 | RWB-S5-E3024-APP | GAP-2860 | 5, 7, 8, 10, 11, 12, 13, 16, 18 | Declare AssetStockBalance as computed with no table in TSD S5 T3.1; publish the reserved POST on /api/recovery/asset/v1 with the next API Specification version |
| CDC-17789 | RWB-S5-E3024-CON | CG-ALL-9781 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the provider, taken from the Document Index service table. |
| CDC-17790 | RWB-S5-E3024-CON | CG-ALL-9782 | 12.2 | Declare the REST base /api/recovery/case/v1 for the provider, taken from the Document Index service table. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (26)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17554 | RWB-S5-E1011-APP | DOR-RWB-S5-E1011-APP-7 | 11 | Add field IDs DF-COL-028, DF-COL-029, DF-COL-031, DF-COL-032, DF-COL-033, DF-COL-034, DF-COL-036, DF-COL-037 and DF-COL-041 to the asset entity; register asset_quality_run, asset_quality_result and asset_quality_break |
| CDC-17597 | RWB-S5-E3019-APP | CG-ALL-9606 | 11, 12.7, 13 | Record holding_cost_to_date as a field in LDM v9 Fields and Data Classification v5 Fields, or name the dictionary field used in its place. |
| CDC-17598 | RWB-S5-E3019-APP | CG-ALL-9607 | 11, 12.7 | Record decision_record as an entity or field in LDM v9 Fields and Data Classification v5 Fields, or name the dictionary object used in its place. |
| CDC-17601 | RWB-S5-E3019-APP | DOR-RWB-S5-E3019-APP-7 | 11 | Add or confirm fields collateral_id, holding_status, holding_cost_to_date and decision_record and the one further P2 name |
| CDC-17615 | RWB-S5-E3019-CON | CG-ALL-9617 | 7, 9, 11 | Add field collateral_id to the asset entity (uuid, foreign key to collateral.id), as in 06 Data Physical Schema v4.sql, the asset table (FK at line 2578). |
| CDC-17616 | RWB-S5-E3019-CON | CG-ALL-9618 | 7, 9, 11 | Add field holding_status to the asset entity (varchar(15), not null, default HELD), as in 06 Data Physical Schema v4.sql line 378. |
| CDC-17617 | RWB-S5-E3019-CON | CG-ALL-9619 | 7, 9, 11 | Add field holding_cost_to_date to the asset entity (numeric(18,2)), as in 06 Data Physical Schema v4.sql line 379. |
| CDC-17621 | RWB-S5-E3019-CON | DOR-RWB-S5-E3019-CON-7 | 11 | Add or map collateral_id, holding_status, holding_cost_to_date and the decision_record library table (see CG-ALL-9620). |
| CDC-17651 | RWB-S5-E3020-CON | CG-ALL-9645 | 10 | Record holding_cost_to_date as a field of the asset entity with its dictionary name, or record the owning object (index, library table or flag) in the owning document. Owner role: Data. |
| CDC-17652 | RWB-S5-E3020-CON | CG-ALL-9646 | 10 | Record holding_status as a field of the asset entity with its dictionary name, or record the owning object (index, library table or flag) in the owning document. Owner role: Data. |
| CDC-17657 | RWB-S5-E3020-CON | DOR-RWB-S5-E3020-CON-7 | 11 | Add holding_cost_to_date and holding_status as fields or entities, or map them to the existing names |
| CDC-17670 | RWB-S5-E3021-APP | CG-ALL-9660 | 2, 4, 5, 8, 11, 12.4 | Record the object behind handed_over (index, library table or flag) or add it to the dictionary under its name. |
| CDC-17671 | RWB-S5-E3021-APP | CG-ALL-9661 | 4 | Record the object behind holding_status (index, library table or flag) or confirm the dictionary name, such as lit_status, plan_status or ocr_status. |
| CDC-17672 | RWB-S5-E3021-APP | CG-ALL-9662 | 4 | Record the object behind collateral_id (index, library table or flag) or confirm the dictionary name, such as collateral or collateral_no. |
| CDC-17673 | RWB-S5-E3021-APP | CG-ALL-9663 | 11 | Record the object behind decision_record (index, library table or flag) or confirm the dictionary name, such as decision_log_id. |
| CDC-17674 | RWB-S5-E3021-APP | CG-ALL-9664 | 11 | Record the object behind inbox_event (index, library table or flag) or confirm the dictionary name, such as outbox_event. |
| CDC-17678 | RWB-S5-E3021-APP | DOR-RWB-S5-E3021-APP-7 | 11 | Add BR Field IDs DF-COL-028 to DF-COL-039 and the names handed_over, holding_status, collateral_id and decision_record |
| CDC-17695 | RWB-S5-E3021-CON | DOR-RWB-S5-E3021-CON-7 | 11 | Add or confirm collateral_id, holding_status, holding_cost_to_date and handed_over as fields or entities. |
| CDC-17711 | RWB-S5-E3022-APP | DOR-RWB-S5-E3022-APP-7 | 11 | Add decision_record as the platform library entity created in rwb_asset, or confirm it is outside both documents. |
| CDC-17724 | RWB-S5-E3022-CON | DOR-RWB-S5-E3022-CON-7 | 11 | Add decision_record as the rwb_asset library entity in LDM v9 and Data Classification v5, or confirm the library object name. |
| CDC-17745 | RWB-S5-E3023-APP | DOR-RWB-S5-E3023-APP-7 | 11 | Add DF-COL-031 to DF-COL-040 as asset fields; confirm or rename collateral_id, decision_record and under_transfer. |
| CDC-17761 | RWB-S5-E3023-CON | DOR-RWB-S5-E3023-CON-7 | 11 | Confirm under_transfer as an existing field or entity, or as a value of the title status field used in L288. |
| CDC-17774 | RWB-S5-E3024-APP | CG-ALL-9761 | 1, 4, 8, 19 | Add holding_cost_to_date as a field of asset (S5, rwb_asset), or record the object in the owning document. No story edit. |
| CDC-17775 | RWB-S5-E3024-APP | CG-ALL-9762 | 1, 4, 8, 12.1, 13 | Add holding_status as a field of asset (S5, rwb_asset) against LOV-HOLDING, or record the object in the owning document. No story edit. |
| CDC-17776 | RWB-S5-E3024-APP | CG-ALL-9763 | 8 | Add collateral_id as a field of asset (S5, rwb_asset), or record the object in the owning document. No story edit. |
| CDC-17777 | RWB-S5-E3024-APP | CG-ALL-9764 | 11 | Record decision_record as a platform library object created in rwb_asset, or add it to the owning document. No story edit. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (20)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17552 | RWB-S5-E1011-APP | CG-ALL-9598 | 16 | Add rows TC-E1-011-08 (AC7, BR5, BR9, BR13) and TC-E1-011-09 (AC4, BR6, BR12) with Given, When and Then copied from those criteria. |
| CDC-17600 | RWB-S5-E3019-APP | CG-ALL-9612 | 16 | Add rows TC-E3-019-01 to TC-E3-019-06 to the Story test cases tab, with Given, When and Then copied from the criteria they cover (AC1 to AC4). |
| CDC-17620 | RWB-S5-E3019-CON | DOR-RWB-S5-E3019-CON-12 | 12.7, 16 | Add tab Story test cases rows for TC-E3-019-01 to -06 and TC-S5-E3019-CON-01 to -06. |
| CDC-17630 | RWB-S5-E3019-CON | CG-ALL-9625 | 16 | Add rows TC-E3-019-01 to -06 and TC-S5-E3019-CON-01 to -03 with Given, When and Then copied from the criteria they cover. |
| CDC-17640 | RWB-S5-E3020-APP | CG-ALL-9639 | 16 | Add rows for TC-E3-020-01 to TC-E3-020-06 to Story test cases in the next version, with Given, When and Then copied from the criteria they cover. |
| CDC-17656 | RWB-S5-E3020-CON | DOR-RWB-S5-E3020-CON-12 | 12.7, 16 | Add rows TC-E3-020-01 to -06 and TC-S5-E3020-CON-01 to -05 under the same IDs |
| CDC-17662 | RWB-S5-E3020-CON | CG-ALL-9652 | 16 | Add rows TC-E3-020-01 to TC-E3-020-06 and TC-S5-E3020-CON-01 to TC-S5-E3020-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-17676 | RWB-S5-E3021-APP | CG-ALL-9673 | 16 | Add rows for TC-E3-021-01 to TC-E3-021-06 and TC-S5-E3021-APP-01 with Given, When and Then copied from the criteria they cover |
| CDC-17694 | RWB-S5-E3021-CON | DOR-RWB-S5-E3021-CON-12 | 12.7, 16 | Add the story test rows TC-S5-E3021-CON-01 to -06 and TC-E3-021-01 to -06 (legacy cases carried as contract half) with their Given, When and Then. |
| CDC-17697 | RWB-S5-E3021-CON | CG-ALL-9692 | 16 | Add rows for TC-E3-021-01 to -06 and TC-S5-E3021-CON-01 to -04 in the next version, with Given, When and Then copied from the covered criteria. |
| CDC-17708 | RWB-S5-E3022-APP | CG-ALL-9705 | 16 | Add rows TC-E3-022-01 to TC-E3-022-06 in the next version, with Given, When and Then copied from the criteria they cover. |
| CDC-17726 | RWB-S5-E3022-CON | CG-ALL-9722 | 16 | Add rows for TC-E3-022-01 to -06 and TC-S5-E3022-CON-01 to -04, with Given, When and Then copied from the criterion each covers. |
| CDC-17742 | RWB-S5-E3023-APP | CG-ALL-9739 | 16 | Add rows TC-E3-023-01 to TC-E3-023-05 with Given, When and Then copied from the criteria each row covers in section 16. |
| CDC-17743 | RWB-S5-E3023-APP | DOR-RWB-S5-E3023-APP-12 | 16 | Add rows TC-E3-023-01 to TC-E3-023-08 on tab Story test cases; story now has contract TC-06 and boundary TC-07. |
| CDC-17760 | RWB-S5-E3023-CON | DOR-RWB-S5-E3023-CON-12 | 12.7, 16 | Add rows TC-E3-023-01 to -05 and TC-S5-E3023-CON-01 to -04 on tab Story test cases, plus TC-S5-E3023-CON-05 for the §12.7 boundary. |
| CDC-17765 | RWB-S5-E3023-CON | CG-ALL-9753 | 16 | Add tab Story test cases rows for TC-E3-023-01 to -05 and TC-S5-E3023-CON-01 to -04 with Given, When and Then copied from the criteria they cover. |
| CDC-17779 | RWB-S5-E3024-APP | CG-ALL-9772 | 16 | Add rows TC-E3-024-01 to TC-E3-024-06 with Given, When and Then copied from the criteria they cover. |
| CDC-17781 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-12 | 16 | Add Given/When/Then rows for TC-E3-024-01 to TC-E3-024-09 under tab Story test cases |
| CDC-17797 | RWB-S5-E3024-CON | DOR-RWB-S5-E3024-CON-12 | 16 | Add rows for TC-E3-024-01 to -06 and TC-S5-E3024-CON-01 to -09 on tab Story test cases; TC-S5-E3024-CON-05 added as the table boundary test. |
| CDC-17802 | RWB-S5-E3024-CON | CG-ALL-9787 | 16 | Add rows for TC-E3-024-01 to -06 and TC-S5-E3024-CON-01 to -04 with Given, When and Then copied from the criterion each covers. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17546 | RWB-S5-E1011-APP | CG-ALL-9591 | 12.5 | Add a rwb-asset Workflow row named AssetQualityWorkflow (task queue rwb-asset, namespace rwb-recovery), so that section 12.5 names a catalogued workflow. |
| CDC-17593 | RWB-S5-E3019-APP | DOR-RWB-S5-E3019-APP-8 | header | Add activity takeOnAsset under AssetDisposalWorkflow. The rwb.asset topic part is resolved by CG-ALL-9608. |
| CDC-17599 | RWB-S5-E3019-APP | CG-ALL-9610 | 12.5 | Add a row for activity takeOnAsset on queue rwb-asset to the Activities sheet, with the input and output given in section 12.5. |
| CDC-17613 | RWB-S5-E3019-CON | DOR-RWB-S5-E3019-CON-8 | 12.5 | Add activity takeOnAsset to the catalog. |
| CDC-17618 | RWB-S5-E3019-CON | CG-ALL-9623 | 12.5 | Add an Activities row for takeOnAsset: queue rwb-asset; case and repossession fact in; rule ID with package version, asset reference, event and stage outcome out. |
| CDC-17639 | RWB-S5-E3020-APP | CG-ALL-9637 | 12.5 | Add activity takeOnAsset to the Activities sheet with task queue rwb-asset, or replace it with a catalogued activity. |
| CDC-17649 | RWB-S5-E3020-CON | DOR-RWB-S5-E3020-CON-8 | 12.5 | Register activity takeOnAsset on task queue rwb-asset in the Activities list. |
| CDC-17675 | RWB-S5-E3021-APP | CG-ALL-9671 | 12.5 | Add activity takeOnLedAuctionAsset on task queue rwb-asset, or name a catalogued activity in RWB-S5-E3021-APP section 12.5. |
| CDC-17692 | RWB-S5-E3021-CON | CG-ALL-9690 | 12.5 | Add the Activities row takeOnLedAuctionAsset (task queue rwb-asset) for the take-on step, or catalogue an existing activity in its place. |
| CDC-17738 | RWB-S5-E3023-APP | CG-ALL-9735 | 12.5 | Start rule stated in header; workflow ID form still Not specified in the source documents (CG-ALL-9735). |
| CDC-17739 | RWB-S5-E3023-APP | CG-ALL-9736 | 12.5 | Add an Activities row for applyHoldingStep on queue rwb-asset with the contract element used in section 12.5. |
| CDC-17740 | RWB-S5-E3023-APP | CG-ALL-9737 | 12.5 | Add an Activities row for applyProvisionStep on queue rwb-asset with the contract element used in section 12.5. |
| CDC-17741 | RWB-S5-E3023-APP | CG-ALL-9738 | 12.5 | Add an Activities row for requestCostOfCarry on queue rwb-payment with the contract element used in section 12.5. |
| CDC-17756 | RWB-S5-E3023-CON | CG-ALL-9750 | 12.5 | Add activity applyHoldingStep to the Activities sheet, or name a catalogued activity in §12.5. |
| CDC-17757 | RWB-S5-E3023-CON | CG-ALL-9751 | 12.5 | Add activity applyProvisionStep to the Activities sheet, or name a catalogued activity in §12.5. |
| CDC-17758 | RWB-S5-E3023-CON | CG-ALL-9752 | 12.5 | Add activity requestCostOfCarry on task queue rwb-payment to the Activities sheet, or name a catalogued activity in §12.5. |
| CDC-17795 | RWB-S5-E3024-CON | CG-ALL-9785 | 12.5 | Add activity confirmStockBalance to the Activities sheet: inputs scope, as-at date, officer reference; outputs AssetStockBalance, record reference, rule version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17595 | RWB-S5-E3019-APP | CG-ALL-9604 | 4, 7, 9 | Name the dictionary field for collateral_id or record the object (index, library table, flag) in LDM v9. Data to confirm; nearest collateral, collateral_no, collateral_detail not chosen. |
| CDC-17596 | RWB-S5-E3019-APP | CG-ALL-9605 | 4, 9 | Name the dictionary field for holding_status or record the object in LDM v9. Data to supply; nearest lit_status, plan_status, ocr_status not chosen. |
| CDC-17637 | RWB-S5-E3020-APP | CG-ALL-9631 |  | Record collateral_id as a field of asset, or give the dictionary field name used for the ACE collateral reference. |
| CDC-17638 | RWB-S5-E3020-APP | CG-ALL-9632 | 4, 9, 11 | Add holding_status as a field of the asset entity (LOV-HOLDING, value HELD), or give the dictionary name the story should use. |
| CDC-17642 | RWB-S5-E3020-APP | DOR-RWB-S5-E3020-APP-7 | 11 | Add DF-COL-028 to DF-COL-039 or confirm owner; add names collateral_id, holding_status and decision_record or confirm they are owned elsewhere. |
| CDC-17689 | RWB-S5-E3021-CON | CG-ALL-9681 | 7, 11 | Add field collateral_id, or confirm the existing field it maps to (collateral, collateral_no or collateral_detail), for the Asset element link. |
| CDC-17690 | RWB-S5-E3021-CON | CG-ALL-9682 | 11 | Add field holding_status with the LOV-HOLDING values HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED. |
| CDC-17691 | RWB-S5-E3021-CON | CG-ALL-9683 | 11 | Add field holding_cost_to_date to the Asset element columns (DF-COL-028 to DF-COL-042). |
| CDC-17706 | RWB-S5-E3022-APP | CG-ALL-9696 | 12.7 | Record decision_record as the platform library table created in rwb_asset, or use its dictionary name. |
| CDC-17720 | RWB-S5-E3022-CON | CG-ALL-9713 | header | Record decision_record as a PLT library table created in rwb_asset (DP-03); it is not an LDM v9 field |
| CDC-17735 | RWB-S5-E3023-APP | CG-ALL-9729 | 8 | Confirm the dictionary name for collateral_id or record it as the other service's identifier object; nearest dictionary names are collateral, collateral_no, collateral_detail. |
| CDC-17736 | RWB-S5-E3023-APP | CG-ALL-9730 | 11 | Record decision_record as a PLT library object created in rwb_asset under DP-03, outside the LDM v9 field set. |
| CDC-17755 | RWB-S5-E3023-CON | CG-ALL-9745 | 12.8 | Record under_transfer as a title status value of the owning rwb-case object, or use the dictionary name for it. |
| CDC-17784 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-7 | 11 | Register field IDs DF-COL-028, DF-COL-029, DF-COL-031 to DF-COL-037, DF-COL-039 to DF-COL-041 and names holding_cost_to_date, holding_status, collateral_id, decision_record |
| CDC-17793 | RWB-S5-E3024-CON | CG-ALL-9778 | 4, 8, 11 | Record holding_status as a dictionary field, or record the object (index, library table or flag) in the owning document; no dictionary name matches. |
| CDC-17794 | RWB-S5-E3024-CON | CG-ALL-9779 | 11, 19 | Record holding_cost_to_date as a dictionary field, or record the object (index, library table or flag) in the owning document; last_tdr_date does not match. |
| CDC-17798 | RWB-S5-E3024-CON | DOR-RWB-S5-E3024-CON-7 | 11 | Add holding_status and holding_cost_to_date to the asset entity, or classify them in Data Classification v5. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17603 | RWB-S5-E3019-APP | GAP-2837 | header, 7, 2 | Add asset row (S5, rwb_asset) from Architecture v5 slides 19 and 41 and TSD S5 T3.1 |
| CDC-17606 | RWB-S5-E3019-APP | GAP-1907 | 2 | Add an asset table row owned by S5, from Architecture v5 slides 19 and 41 and TSD S5 T3.1. The ACE fact is already read through the rwb-source-data DP06 contract. |
| CDC-17610 | RWB-S5-E3019-APP | GAP-1751 | 2 | Add an asset row owned by S5 in schema rwb_asset, alongside listing and asset_sale. |
| CDC-17625 | RWB-S5-E3019-CON | GAP-1907 | none | Add the S5 asset row from Architecture v5 slides 19 and 41 and TSD S5 T3.1. |
| CDC-17627 | RWB-S5-E3019-CON | GAP-1751 | 4 | Add an asset table row owned by S5 in schema rwb_asset, in the same change as the story statement of holding-record ownership. |
| CDC-17647 | RWB-S5-E3020-APP | GAP-1751 | 4 | Add a table row: asset, owned by S5, schema rwb_asset, keyed by the ACE asset key with no foreign key. |
| CDC-17648 | RWB-S5-E3020-APP | GAP-2841 | 4 | Add the missing row: asset, owned by S5, in rwb_asset; keep the asset_sale and listing rows as given. |
| CDC-17661 | RWB-S5-E3020-CON | GAP-2841 | 4 | Add a Tables row: asset owned by S5 in schema rwb_asset, with the take-on columns DF-COL-028 to DF-COL-042. Keep asset_sale and listing as they are. |
| CDC-17680 | RWB-S5-E3021-APP | GAP-1751 | 11 | Add an asset row owned by S5 in schema rwb_asset, keyed by the ACE asset key with no foreign key |
| CDC-17696 | RWB-S5-E3021-CON | GAP-1751 | 11 | Add an asset table row owned by rwb-asset in schema rwb_asset, keyed by asset_ref, with the ACE asset read-only through rwb-source-data. |
| CDC-17749 | RWB-S5-E3023-APP | GAP-1752 |  | Add entity-group rows for auction round, bid, award, holding-cost movement and work order; physical names left to the DB story; add before the S5 DB story starts. |
| CDC-17764 | RWB-S5-E3023-CON | GAP-1752 |  | Add rows for auction round, bid, award, holding cost movement and work order as entity groups of this service; leave physical names to the S5 DB story; complete before it starts. |
| CDC-17786 | RWB-S5-E3024-APP | GAP-1751 | 8 | Add an asset table row: schema rwb_asset, owner S5 (rwb-asset); no foreign key to the ACE asset; the ACE asset stays read-only through the source-data contract. |
| CDC-17801 | RWB-S5-E3024-CON | GAP-1751 | 8 | Add an asset table row owned by S5 in schema rwb_asset; restate TSD S5 T3.1 asset as this service's own record, not an extension of ACE Asset. Story BR1 now states the keyed record. |

### Epic design record (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17590 | RWB-S5-E3019-APP | DOR-RWB-S5-E3019-APP-14 | find it | Record the signed epic design sign-off for RWB-SVC-S5 so DoR item 14 can pass. No signed design is in the sources. |
| CDC-17632 | RWB-S5-E3020-APP | DOR-RWB-S5-E3020-APP-14 |  | Record the signed sign-off of the epic design for RWB-SVC-S5 (Wave 2) in the epic design record. |
| CDC-17665 | RWB-S5-E3021-APP | DOR-RWB-S5-E3021-APP-14 | Definition of Ready | Record the signed epic design sign-off for RWB-S5-E3021-APP in the epic design record. |
| CDC-17685 | RWB-S5-E3021-CON | DOR-RWB-S5-E3021-CON-14 | header | Confirm and record the signed epic design sign-off for service epic RWB-SVC-S5. |
| CDC-17702 | RWB-S5-E3022-APP | DOR-RWB-S5-E3022-APP-14 | 19 | Record the signed epic design sign-off for this story in the epic design record. |
| CDC-17718 | RWB-S5-E3022-CON | DOR-RWB-S5-E3022-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-S5 so the story can cite it |
| CDC-17730 | RWB-S5-E3023-APP | DOR-RWB-S5-E3023-APP-14 | header | Record the signed epic design sign-off for this story. |
| CDC-17753 | RWB-S5-E3023-CON | DOR-RWB-S5-E3023-CON-14 | none | Record the signed epic design sign-off for RWB-S5-E3023-CON. Not specified in the source documents (DOR-RWB-S5-E3023-CON-14) |
| CDC-17769 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-14 | find it | Record the signed epic design sign-off in the epic design record, then cite it in the story. |
| CDC-17791 | RWB-S5-E3024-CON | DOR-RWB-S5-E3024-CON-14 | header | Record the signed epic design sign-off for service epic RWB-SVC-S5 in the epic design record. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17584 | RWB-S5-E1011-APP | GAP-0337 |  | Add the three outbound reads of JOB-04 to the rwb-source-data row of the connection matrix. Publish the case-contract exclusion resource with its path, fields and 2 s budget. |
| CDC-17594 | RWB-S5-E3019-APP | GAP-1750 | find it | Rename v_ace_* field-catalog sources to rwb-source-data contract fields; add the S5 to P1 cell to the connection matrix. |
| CDC-17611 | RWB-S5-E3019-APP | GAP-1767 | 4 | Add S5 cells to P5 (rwb-document) and P6 (rwb-comms) so the notice request and evidence upload have drawn paths. |
| CDC-17614 | RWB-S5-E3019-CON | GAP-1750 | 12 | Add S5 to the P1 cell of the connection matrix. |
| CDC-17628 | RWB-S5-E3019-CON | GAP-1767 |  | Add the S5 cells to P6 (notices via rwb-comms) and P5 (documents via rwb-document) in the connection matrix. |
| CDC-17687 | RWB-S5-E3021-CON | GAP-1750 | 12.2 | Add S5 to the P1 cell so rwb-source-data is the only reader of the ACE asset, collateral and score views. |
| CDC-17712 | RWB-S5-E3022-APP | GAP-1767 | 13 | Draw the S5 cells to P6 (notice request, proof of delivery) and to P5 (photographs, inspection and transfer documents on rwb-document). |
| CDC-17725 | RWB-S5-E3022-CON | GAP-1767 | 4 | Add the S5 to P6 cell for the notice request and proof-of-delivery read, and the S5 to P5 cell for photograph, inspection and transfer document storage through rwb-document. |
| CDC-17734 | RWB-S5-E3023-APP | GAP-1750 | 12.2 | Add the missing S5 to the P1 cell; confirm the contract fields, business key and freshness response with P1 before wave 2 system test. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17641 | RWB-S5-E3020-APP | DOR-RWB-S5-E3020-APP-6 | 10 | Add role SY-DATALOAD, which §10 of RWB-S5-E3020-APP uses. |
| CDC-17654 | RWB-S5-E3020-CON | DOR-RWB-S5-E3020-CON-1 | 1 | Add 'tech lead' as a role, or replace it in section 1 with a role code or name that exists in v5 |
| CDC-17677 | RWB-S5-E3021-APP | DOR-RWB-S5-E3021-APP-6 | 10 | Add role SY-DATALOAD to the roster, or the story replaces it with a role the document holds |
| CDC-17710 | RWB-S5-E3022-APP | DOR-RWB-S5-E3022-APP-6 | 10 | Add role SY-DATALOAD, the service identity named in §10, to the roles document, or confirm its removal from §10. |
| CDC-17722 | RWB-S5-E3022-CON | DOR-RWB-S5-E3022-CON-1 | 1 | Add tech lead as a role name in Users Roles and Permissions v5, or re-point section 1 to a role listed there. |
| CDC-17744 | RWB-S5-E3023-APP | DOR-RWB-S5-E3023-APP-6 | 10 | Add role SY-DATALOAD with Asset and disposal R, or remove it from section 10 of the story. |
| CDC-17759 | RWB-S5-E3023-CON | DOR-RWB-S5-E3023-CON-1 | 1 | Add a role code or role name for the tech lead of rwb-asset, used in §1 and §10, or name the existing role it maps to. |
| CDC-17783 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-6 | 10 | Add role SY-DATALOAD with Asset and disposal R or C per TSD S5 T6.1 |
| CDC-17796 | RWB-S5-E3024-CON | DOR-RWB-S5-E3024-CON-1 | 1 | Add a role for 'tech lead' with its role code, or confirm the existing role code to use in the section 1 role of this story. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17542 | RWB-S5-E1011-APP | CG-ALL-9587 | 12.1 | Publish GET /api/recovery/asset/v1/quality-runs/{businessDate} in rwb-asset.yaml through the RWB-S5-E1011-CON story |
| CDC-17543 | RWB-S5-E1011-APP | CG-ALL-9588 | 12.1 | Publish GET /api/recovery/asset/v1/quality-results in rwb-asset.yaml through the RWB-S5-E1011-CON story |
| CDC-17545 | RWB-S5-E1011-APP | CG-ALL-9590 | 12.2 | Remove the fixed enum on saleChannel so LOV-SALE-CHANNEL values are accepted as data without a code change |
| CDC-17547 | RWB-S5-E1011-APP | DOR-RWB-S5-E1011-APP-8 | find it | Add GET /quality-runs/{businessDate} and GET /quality-results to rwb-asset.yaml; publish DP06 records path in rwb-source-data; make saleChannel an LOV-read field, not a closed enum. |
| CDC-17766 | RWB-S5-E3024-APP | CG-ALL-9765 | 12.1 | Publish the POST operation for the confirmation of the balance (path Not specified in the source documents (GAP-2860; ASM-4738)) with StockBalanceConfirmation in and AssetStockBalance out, through RWB-S5-E3024-CON; otherwise remove the row from §12.1. |
| CDC-17788 | RWB-S5-E3024-CON | CG-ALL-9780 | 12.1 | Publish the POST operation with the StockBalanceConfirmation request and AssetStockBalance response, or remove it; the story keeps the placeholder until then. |
| CDC-17792 | RWB-S5-E3024-CON | DOR-RWB-S5-E3024-CON-8 | 12.1, 12.2, 12.5 | Publish the POST operation in rwb-asset.yaml and declare the REST bases of source-data and case; the task queue is already fixed in the story. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17548 | RWB-S5-E1011-APP | CG-ALL-9592 | 12.5 | Add an Activities row for loadTolerance (calls rwb-case P3, task queue rwb-asset) or name a catalogued activity. |
| CDC-17549 | RWB-S5-E1011-APP | CG-ALL-9593 | 12.5 | Add an Activities row for readAssetFacts (calls rwb-source-data P1, task queue rwb-asset) or name a catalogued activity. |
| CDC-17550 | RWB-S5-E1011-APP | CG-ALL-9594 | 12.5 | Add an Activities row for reconcileAssets (reads rwb_asset only, task queue rwb-asset) or name a catalogued activity. |
| CDC-17551 | RWB-S5-E1011-APP | CG-ALL-9595 | 12.5 | Add an Activities row for writeQualityFacts (writes rwb_asset only, task queue rwb-asset) or name a catalogued activity. |
| CDC-17707 | RWB-S5-E3022-APP | CG-ALL-9703 | 12.5 | Add an Activities row serveStatutoryNotice on task queue rwb-asset, or name a catalogued activity in §12.5. |

### OTHER:Recovery Workbench Gap Register v1 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17560 | RWB-S5-E1011-APP | GAP-0495 |  | Record GAP-0495 as resolved: the reconciliation and data-quality lake extracts and the 07:30 Power BI refresh are removed. Results are read through GET /admin/reconciliation/results and GET /admin/reconciliation/results/{resultId} on API-P1-003. Keep the legacy lake text as history. |
| CDC-17564 | RWB-S5-E1011-APP | GAP-0275 |  | Record that S2 (rwb-treatment) owns the Workbench side of REC-03 and P8 (rwb-payment) owns the Workbench side of REC-04, each answered on its contract; add a slice for each at Step D1. |
| CDC-17565 | RWB-S5-E1011-APP | GAP-0336 |  | Name the owner of REC-03 and REC-04 when wave 2 enters; keep NOT_RUN with the legacy BR10 reason until then; route both extracts as a deliverFile manifest from rwb-source-data to rwb-reporting through rwb-integration. |

### RWB-P6-E1011-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17561 | RWB-S5-E1011-APP | GAP-1168 |  | Add RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-source-data data-product contract to the C list; name the reference-data read operation in RWB-P3-E1043-CON. |
| CDC-17569 | RWB-S5-E1011-APP | GAP-1170 | 19 | Drop the reconciliation and data-quality extracts and the INT-19 path; serve quality facts from GET /api/recovery/comms/v1/quality-results; settle the report reads with rwb-reporting; record the decision in the Change Register against RWB-E1-014 and INT-19. |
| CDC-17570 | RWB-S5-E1011-APP | GAP-1171 | 19 | Serve the quality facts from the service's own read model for wave 1; decide in wave 2 whether rwb-reporting reads them or a quality event is added with DP-09 and a platform event library story. |

### RWB-P1-E1011-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17567 | RWB-S5-E1011-APP | GAP-0497 | 19 | Publish GET /admin/reconciliation/results and GET /admin/reconciliation/results/{resultId} on /api/recovery/source-data/v1, with the result and break-row element lists, workflow ReconciliationWorkflow (recon-{businessDate}, activity reconciliation, queue rwb-source-data) and the ReconciliationQuery interface. |
| CDC-17571 | RWB-S5-E1011-APP | GAP-1508 | 19 | Publish the per-account break list as part of the reconciliation result and its read operation, not in an unowned table; fix the store at the data-model review before system test. |
| CDC-17575 | RWB-S5-E1011-APP | GAP-2235 | 19 | Publish a freshness read and one product-coded records read per data product on /api/recovery/source-data/v1, with the product code, business date, paging and element names; plan rows keyed by plan_ref. |

### RWB-P3-E1011-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17568 | RWB-S5-E1011-APP | GAP-0740 | 19 | Confirm REC-01 EXCL, REC-05 KEY and REC-05 REF and the four run states; publish the four rwb-case operation paths; settle the rwb-source-data call type; set the Schedule cron; add the Platform administration right; align account_id with FSD P3 v4. |
| CDC-17574 | RWB-S5-E1011-APP | GAP-2234 | 19 | Publish the four section 12.1 operations under the rwb-case contract with Platform administration R, Reporting R and Platform administration U, the 400, 401, 403, 404, 409 and 503 problem set, and an Idempotency-Key on the rerun. |
| CDC-17576 | RWB-S5-E1011-APP | GAP-2236 | 19 | Expose GET /reconciliation/status on rwb-case returning RELEASED, HELD or NOT_RUN for the business date, with the unexplained exclusion count per product group; the rwb-source-data case-list gate reads it before release. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17579 | RWB-S5-E1011-APP | CG-ALL-9599 | 18 | Align the REQ-RDF-007 and REQ-RDF-008 test lists with §18 of this story in the next RTM version. |
| CDC-17713 | RWB-S5-E3022-APP | CG-ALL-9706 | 18 | Align the REQ-OCC-006 test list with section 18 of this story (TC-E3-022-01, TC-E3-022-02); the TC-E2 IDs it lists belong to another story. |
| CDC-17727 | RWB-S5-E3022-CON | CG-ALL-9723 | 18 | Align the REQ-OCC-006 row with section 18, which names TC-E3-022-01 only. |

### RWB-S5-E3019-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17591 | RWB-S5-E3019-APP | DOR-RWB-S5-E3019-APP-21 | header | Set build status from Not started to Done once the contract is published. |
| CDC-17592 | RWB-S5-E3019-APP | DOR-RWB-S5-E3019-APP-22 | header | Publish a contract fake library version and record its version number against this story. |
| CDC-17608 | RWB-S5-E3019-APP | GAP-2838 | Header, 14 | Record the tag date; confirm the DP06 operation name with rwb-source-data and the case move element with rwb-case before the tag; publish the AssetTakenOn consumer list. |

### RWB-S5-E3024-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17604 | RWB-S5-E3019-APP | GAP-2860 | find it | Apply the proposed fix there: figure definition, confirm write path, owner RW-NPAMGR, R-DIS-01 and R-DIS-02 build split |
| CDC-17624 | RWB-S5-E3019-CON | GAP-2860 | none in story | Apply the item's fix: stock balance = count of rwb_asset asset rows with totals of book_value and holding_cost_to_date per holding_status for LOV-SEGMENT scope and an as-at date, stored in no table; serve on GET /assets as AssetStockBalance; confirm with one POST on the asset base (path reserved for the next API Specification version); owner role RW-NPAMGR with scope from the rwb-access matrix; record R-DIS-01 and R-DIS-02 built by RWB-S5-E3019-APP and RWB-S5-E3020-APP. |
| CDC-17644 | RWB-S5-E3020-APP | GAP-2860 | 8 | Define the stock balance figure, scope and as-at date, its write operation, TSD object and requirement id; record that R-DIS-01 and R-DIS-02 are built by RWB-S5-E3019-APP and RWB-S5-E3020-APP. |

### RWB-S5-E3020-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17631 | RWB-S5-E3019-CON | GAP-2839 | find it | Keep AC3 verbatim with its origin tag; table R-DIS-02 as this step's rule; name R-DIS-01 and R-DIS-03 as owned by RWB-S5-E3019-APP and RWB-S5-E3021-APP. No edit in this story. |
| CDC-17633 | RWB-S5-E3020-APP | DOR-RWB-S5-E3020-APP-21 | header | Set build status to Done once the contract is published. |
| CDC-17634 | RWB-S5-E3020-APP | DOR-RWB-S5-E3020-APP-22 |  | Publish a contract fake library version and record it as published. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17643 | RWB-S5-E3020-APP | DOR-RWB-S5-E3020-APP-9 | 14 | Confirm MSG-P1-001 text against the standard and align the text in §14 of RWB-S5-E3020-APP. |
| CDC-17658 | RWB-S5-E3020-CON | DOR-RWB-S5-E3020-CON-9 | 14 | Align the MSG-P1-001 text with the standard entry, or record the standard text as the story's wording |
| CDC-17799 | RWB-S5-E3024-CON | DOR-RWB-S5-E3024-CON-9 | 14 | Confirm the MSG-P1-001 text the standard gives; the story then copies that text in place of the FSD wording. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17653 | RWB-S5-E3020-CON | CG-ALL-9650 | 12.5 | Add activity takeOnAsset to the Activities sheet, or map the step to an existing catalogued activity |
| CDC-17721 | RWB-S5-E3022-CON | CG-ALL-9720 | 12.5 | Add the rwb-asset activity serveStatutoryNotice, or name a catalogued activity in section 12.5. |
| CDC-17778 | RWB-S5-E3024-APP | CG-ALL-9770 | 12.5 | Add confirmStockBalance (rwb-asset, the one confirmation step) to the Activities sheet, or name a catalogued activity in this story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17553 | RWB-S5-E1011-APP | DOR-RWB-S5-E1011-APP-12 | 16, 18 | Add TC-E1-011-08 and TC-E1-011-09 rows to tab Story test cases; align the section 18 test lists of RWB-S5-E1011-APP to RTM v7 |
| CDC-17723 | RWB-S5-E3022-CON | DOR-RWB-S5-E3022-CON-12 | 16, 18 | Add TC-E3-022-01 to -06 and TC-S5-E3022-CON-01 to -05 under their IDs in Test Cases v8; align the RTM v7 test lists with section 18. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17572 | RWB-S5-E1011-APP | GAP-2232 | 19 | Record the boundary: rwb-case owns the case-side facts of REC-01, REC-03 and REC-05 over its own tables; it writes no reconciliation_result row and owns no legacy AC; platform DP CONs are not build dependencies of the APP story. |
| CDC-17577 | RWB-S5-E1011-APP | GAP-2237 |  | Keep the link columns as ACE business keys account_key and person_key, varchar(255), no foreign key (D-RCV-35 re-base); record the TSD P3 v3 uuid form as a pre-re-base artefact in the Change Register. |

### RWB-S5-E3019-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17622 | RWB-S5-E3019-CON | GAP-2837 | header | Add the S5 asset row from Architecture v5 slides 19 and 41 and TSD S5 T3.1; state that only RWB-S5-E3023-APP runs the R-DIS-06 clocks. |
| CDC-17747 | RWB-S5-E3023-APP | GAP-2837 | 7 | Add C rows for rwb-source-data and rwb-case; add RWB-PLT-TE006-CON to H; add asset row to Ownership Map; adopt REQ-S5-001. |

### OTHER:plan revision (build plan) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17645 | RWB-S5-E3020-APP | GAP-2843 | 13 | Add RWB-PLT-TE006-CON as a platform dependency of the AssetTakenOn event in the next plan revision. |
| CDC-17646 | RWB-S5-E3020-APP | GAP-2840 | header | Add RWB-S2-E3012-CON as class C contract dependency of RWB-S5-E3020-APP in the next plan revision. |

### RWB-S5-E3020-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17655 | RWB-S5-E3020-CON | DOR-RWB-S5-E3020-CON-10 | find it | Add empty, loading, error and no-access states to SCR-21 and SCR-22 |
| CDC-17682 | RWB-S5-E3021-APP | GAP-2839 | find it | Keep legacy AC3 word for word with its origin tag and table R-DIS-02 as the rule of that step; name R-DIS-01 and R-DIS-03 as sibling-route rules owned by RWB-S5-E3019-APP and RWB-S5-E3021-APP. |

### RWB-S5-E3022-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17703 | RWB-S5-E3022-APP | DOR-RWB-S5-E3022-APP-21 | 19 | Set build status to Done so the contract is published. |
| CDC-17704 | RWB-S5-E3022-APP | DOR-RWB-S5-E3022-APP-22 | 19 | Publish the contract fake library and record its published version. |

### RWB-S5-E3023-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17731 | RWB-S5-E3023-APP | DOR-RWB-S5-E3023-APP-21 | header | Move the build status from Not started to Done before this story starts. |
| CDC-17732 | RWB-S5-E3023-APP | DOR-RWB-S5-E3023-APP-22 | header | Publish the contract fake and record its library version. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17737 | RWB-S5-E3023-APP | CG-ALL-9731 | 12.8 | Record under_transfer as a value of the title_status list, since it is used as a value and not as a field or entity name. |
| CDC-17780 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-11 | 11 | Reconcile the personal-data class of the fields this story reads with its statement that no personal data is carried. |

### OTHER:split_plan.json (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17762 | RWB-S5-E3023-CON | GAP-2837 |  | Keep H, C, I, X rows; add C rows for rwb-source-data and rwb-case; add RWB-PLT-TE006-CON as wave 0 library; add asset row to Ownership Map; adopt REQ-S5-001; state in both APP stories that only RWB-S5-E3023-APP runs R-DIS-06 clocks. |
| CDC-17763 | RWB-S5-E3023-CON | GAP-1906 |  | Keep H, C, I, X rows; add rwb-source-data, rwb-case and DP-09 library rows as dependencies; declare AssetTakenOn from the outbox; read the case move as the workflow stage outcome; note that the plan has no requirement id for REQ-S5-001. |

### RWB-S5-E3024-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17771 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-21 | find it | Set the build status of RWB-S5-E3024-CON to Done. |
| CDC-17772 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-22 | find it | Publish the contract fake library and record its version as published. |

### OTHER:Recovery Workbench v3 workbook, sheet Reconciliations (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17555 | RWB-S5-E1011-APP | GAP-0268 | find it | Add an owner service per row from the Ownership Map; REC-05 is owned by rwb-asset reading its own tables and the rwb-source-data contract; rwb-source-data keeps the ACE side and the JOB-04 run |

### OTHER:Recovery Workbench v3 workbook, sheets Reconciliations and Quality measures (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17556 | RWB-S5-E1011-APP | GAP-0269 | find it | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures, values taken from the Ownership Map Tables sheet |

### OTHER:FSD P1 (A2.12; OTHER:A2.19; OTHER:A2.20); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:41 and 44 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17557 | RWB-S5-E1011-APP | GAP-1499 | find it | Remove the data lake and INT-19 integration points; route freshness, reconciliation and the six measures through rwb-reporting; confirm measure definitions with the data steward before wave 2 |

### OTHER:Business requirements document, section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17558 | RWB-S5-E1011-APP | GAP-1456 |  | State the rule that Epic 1 requirement stories keep the business-epic wave 1 while rwb-payment, rwb-asset and rwb-deviation start in wave 2; delivery lead confirms the wave per story at build sequencing. |

### OTHER:RWB-E1-055 legacy story and Recovery Workbench Gap Register v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17559 | RWB-S5-E1011-APP | GAP-1169 |  | Give the notice barcode break its own check code and keep REC-05 for the business-key orphan check; no code is named in the sources. |

### OTHER:Reconciliations sheet of the v3 reconciliation workbook, row REC-08 (cells B12 and C12) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17562 | RWB-S5-E1011-APP | GAP-0270 |  | REC-08 compares the local decision record of each of the 19 services on rwb.decision-record.v1 with the central decision_log_entry of P7, on count and last hash, nightly, with the 02:00 hash-chain check. |

### OTHER:Recovery Workbench Reconciliations v3 workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17563 | RWB-S5-E1011-APP | GAP-0273 |  | Add the REC numbering block that maps each check to the number this document and RWB-E1-011 give it; keep source IDs unchanged. |

### OTHER:TSD P1 v3 and FSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17566 | RWB-S5-E1011-APP | GAP-0496 |  | Keep REC-01, REC-02 and REC-05 over P1 own tables; move REC-03 and REC-04 and the other services REC-05 keys to their own slices. |

### RWB-P3-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17573 | RWB-S5-E1011-APP | GAP-2233 | 19 | Create case_quality_run, case_quality_result and case_quality_break in schema rwb_case with the reconciliation_result column names and a unique key on rec_code, quality_check, business_date and product_group; publish the three check names; add the tables to the baseline migration. |

### RWB-P6-E1011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17578 | RWB-S5-E1011-APP | GAP-1167 | 3 | Record the seven platform CONs as wave-0 platform prerequisites, not lane dependencies; keep H at None; L-P6-C depth unchanged. |

### OTHER:Reconciliation workbook v3 (new Per-service reconciliation sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17580 | RWB-S5-E1011-APP | GAP-0271 | 4, 12 | Add a Per-service reconciliation sheet, one row per service with tables, check part, key, tolerance, cadence, break and result route, pattern and basis; Template and Rules R9 placeholder where unstated. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:P4; OTHER:P5; OTHER:P10; OTHER:S1; OTHER:S3; OTHER:S4; OTHER:S6; OTHER:S8; OTHER:S9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17581 | RWB-S5-E1011-APP | GAP-0272 |  | Tolerance cell of each of the ten rows carries the Template and Rules R9 placeholder. No value is set; the tolerance is a business decision for Step D1. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Services row S1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17582 | RWB-S5-E1011-APP | GAP-0274 |  | S1 row keeps rwb-valuation as owner, states the capability Arch v5 gives it (valuations, D6 route decision, route agent output, RouteDecisionWorkflow) and carries the Template and Rules R9 placeholder until a table is listed. |

### OTHER:v3 Quality measures!B7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17583 | RWB-S5-E1011-APP | GAP-0276 |  | Timeliness reads: the ACE batch for the business date is complete when rwb-source-data reads it and publishes AceDataReady. Other services measure the freshness contract. Owner is P1 rwb-source-data. |

### API:(service not named); OTHER:TSD P6 Communications v2 and FSD P6 Communications v3 (quality model) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17585 | RWB-S5-E1011-APP | GAP-1172 |  | Carry the rwb-comms quality model into the API Specification, schema folder and batch design: comms_quality_run, comms_quality_result, comms_quality_break; REC-09 checks ACK and POD; one Schedule after the pod read; GET /quality-runs/{businessDate} and GET /quality-results. |

### OTHER:TSD P6 Communications v2 (T6.1 RBAC matrix) and gateway-bff route definition (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17586 | RWB-S5-E1011-APP | GAP-1173 |  | Add a Platform administration area with right R to the rwb-comms RBAC matrix and declare the two quality reads there; add the area to the gateway-bff route. Case notice read stays Litigation R with scope. |

### OTHER:FSD P1 Screens table (SCR-44 Interface and job monitor; OTHER:SCR-45 Data quality) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17587 | RWB-S5-E1011-APP | GAP-1514 |  | Assign the screen shell and route: this service serves the job, freshness, reconciliation and dictionary operations; the composite route is the edge's; the steering dashboard shell is reporting's. Fix before Epic 2 acceptance. |

### OTHER:Recovery Workbench Build Notes Epic 1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17588 | RWB-S5-E1011-APP | GAP-3169 |  | In the View note of RWB-E1-011, name reconciliation_result in place of 'the case exceptions' for the reconciliation breaks, not the P3 case_entry_exclusion. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx; OTHER:service epic RWB-SVC-S5 wave plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17589 | RWB-S5-E1011-APP | GAP-3172 | header | State the wave 1 delivery of rwb-asset in the service epic and wave plan, and let the rwb-asset service wave govern its later stories. Build notes must record the R5.6 conflict row. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17602 | RWB-S5-E3019-APP | GAP-1946 | find it | Apply the proposed fix there: keep H and C at None, record nine CONs as wave-0 prerequisites, serve quality facts from the GET quality paths |

### OTHER:Split plan DP-09 row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17605 | RWB-S5-E3019-APP | GAP-1908 | header, 8 | Event declared from outbox in BR7; no DP-09 wave 0 text is in the story. |

### OTHER:rwb-case published operation for case state read and stage move (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17607 | RWB-S5-E3019-APP | GAP-1909 | Header | Placeholder declared in the story; the rwb-case operation is still unpublished and its name unconfirmed. |

### RWB-S5-E3021-APP; OTHER:FEAT-AST-03) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17609 | RWB-S5-E3019-APP | GAP-2848 | 7 | Add one criterion for R-DIS-03 (ASSET_PENDING_TAKE_ON, LED_HANDOVER_RECEIVED, led_result = handed_over, to ASSET_ON_BOOKS) and one test case row, and build one shared take-on component. |

### RWB-S5-E3020-APP; RWB-S5-E3020-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17612 | RWB-S5-E3019-APP | GAP-2839 | 8 | BR10 row added here tagging R-DIS-01 |

### RWB-S5-E3019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17619 | RWB-S5-E3019-CON | DOR-RWB-S5-E3019-CON-10 |  | Add empty, loading, error and no-access states for SCR-21 and SCR-22. |

### RWB-S5-E3021-APP; RWB-S5-E3021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17623 | RWB-S5-E3019-CON | GAP-2847 | none | Keep H, C, I and X as the plan states; declare the AuctionResult event and three REST rows as facts with Day 1 fakes; record RWB-PLT-TE006-CON as wave 0 library. |

### OTHER:RWB-S5-E3021 story (APP) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17626 | RWB-S5-E3019-CON | GAP-2848 |  | Copy the four legacy criteria verbatim, build one shared take-on component, and cover R-DIS-03 with one new criterion and one new test case there. |

### OTHER:RWB-S5-E3021 story (APP) and TSD S5 T3.1; OTHER:T3.2; OTHER:T5.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17629 | RWB-S5-E3019-CON | GAP-2849 |  | Publish the LED result, round and ladder facts, the AuctionResult consumed event properties and producer key, and the handover price mapping to DF-COL-038. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17635 | RWB-S5-E3020-APP | DOR-RWB-S5-E3020-APP-8 | 12.5 | Align rwb.asset.AssetTakenOn.v1 payload with one source; add activity takeOnAsset on rwb-asset to Temporal Catalog v1. |

### OTHER:Connection matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17636 | RWB-S5-E3020-APP | GAP-1750 |  | Add S5 to the P1 cell so rwb-asset reads ACE facts only through rwb-source-data. |

### OTHER:Connection matrix (P1 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17650 | RWB-S5-E3020-CON | GAP-1750 | header | Add S5 to the P1 cell; confirm rwb-source-data contract fields, business key and freshness with P1 before wave 2 system test. |

### RWB-S5-E3024-APP; OTHER:FSD S5; OTHER:TSD S5; OTHER:rwb-access matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17659 | RWB-S5-E3020-CON | GAP-2860 | find it | Apply the proposed fix in the register row: define the stock-balance figure, the POST confirmation path, the RW-NPAMGR owner and the R-DIS-01 and R-DIS-02 build record |

### OTHER:RWB-S5-E3021 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17660 | RWB-S5-E3020-CON | GAP-2848 |  | Copy the four legacy criteria verbatim; build one shared take-on component; add one R-DIS-03 criterion (new, D-RCV-60) and its test case. Not in this story's text. |

### RWB-S5-E3021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17666 | RWB-S5-E3021-APP | DOR-RWB-S5-E3021-APP-21 | Definition of Ready | Set the build status of RWB-S5-E3021-CON to Done. |

### OTHER:contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17667 | RWB-S5-E3021-APP | DOR-RWB-S5-E3021-APP-22 | Definition of Ready | Publish the contract fake library and record the published version. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17668 | RWB-S5-E3021-APP | DOR-RWB-S5-E3021-APP-8 | 12.2 | Add base paths /api/recovery/source-data/v1 and /api/recovery/case/v1 to the yaml; reconcile the topic of rwb.litigation.AuctionResult.v1 with the catalog (rwb.litigation.events.v1). |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:FSD S5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17669 | RWB-S5-E3021-APP | GAP-1750 | 12.2 | Add the S5 to P1 cell to the connection matrix; carry FSD ACE field names as rwb-source-data contract fields; confirm contract fields, business key and freshness with P1 before wave 2 system test. |

### OTHER:Plan H; OTHER:C; OTHER:I and X rows (outside this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17679 | RWB-S5-E3021-APP | GAP-2847 | 12.5 | DP09 added to the story pattern set header |

### OTHER:rwb-litigation AuctionResult event contract; OTHER:TSD S5 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17681 | RWB-S5-E3021-APP | GAP-2849 | 12.4 | Publish AuctionResult property names, consumer group and the LED producer story key; add the LED result, round and ladder |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17688 | RWB-S5-E3021-CON | CG-ALL-9680 | 8, 12.8 | Record `handed_over` as a named result value of the R-DIS-01/02/03/06 rule outcomes, so the name resolves outside this story. |

### RWB-S5-E3021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17693 | RWB-S5-E3021-CON | DOR-RWB-S5-E3021-CON-10 | find it | Add empty, loading, error and no access states for SCR-21 and SCR-22. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17705 | RWB-S5-E3022-APP | DOR-RWB-S5-E3022-APP-8 | 12 | Add the bases /api/recovery/comms/v1, /api/recovery/source-data/v1 and /api/recovery/case/v1 to an API Specification v5 yaml; align the AssetDisposalWorkflow task queue rwb-asset and namespace rwb-recovery with the catalog. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17709 | RWB-S5-E3022-APP | DOR-RWB-S5-E3022-APP-12 | 16, 18 | Align the §18 test lists with TC-E3-022-01 to TC-E3-022-08 in RTM v7; add the new contract and boundary rows to Test Cases v8. |

### OTHER:DISPOSAL package parameter values (owned by NPA and asset manager) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17746 | RWB-S5-E3023-APP | GAP-1468 | 13 | Thresholds, step percentages and re-appraisal interval named as versioned parameters; no values stated. |

### RWB-S5-E3019-APP; RWB-S5-E3019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17748 | RWB-S5-E3023-APP | GAP-1906 |  | Keep H, C, I, X rows; add rwb-source-data, rwb-case and DP-09 outbox/inbox library as build dependencies; declare AssetTakenOn from the outbox on rwb.asset.events.v1; read case move as stage outcome; carry REQ-S5-001 with a note that the plan has no requirement id. |

### OTHER:Plan requirements for both slices (split_plan.json, step D1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17750 | RWB-S5-E3023-APP | GAP-2857 | header | Requirement row REQ-S5-003 added to the story master. |

### OTHER:Epic or squad refinement record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17770 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-16 | header | Size row reads Not specified only; the squad-sizing wording is removed |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17773 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-8 | 12.5 | rwb-asset.yaml: add the balance confirmation POST (GAP-2860; ASM-4738). Source-data and case yaml: add the missing base paths. Catalog: align AssetDisposalWorkflow queue and namespace. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17782 | RWB-S5-E3024-APP | DOR-RWB-S5-E3024-APP-20 | 13 | Register keys for LOV-HOLDING, LOV-SEGMENT, LOV-ASSET-TYPE and LOV-TRANSFER-IN and name the reference-data contract (DP-06, DP-07) |

### OTHER:Contract dependency register and split plan; API:(service not named); OTHER:TSD S5 (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17787 | RWB-S5-E3024-APP | GAP-2861 | Header; 11 | Set the RWB-S5-E3024-CON contract dependency row to the three consumed rows; publish the confirmation POST with StockBalanceConfirmation and AssetStockBalance shapes and required flags; declare owner as an rwb-access role code; map FEAT-AST-06 to a requirement ID. |

### OTHER:rwb-access role matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17800 | RWB-S5-E3024-CON | GAP-2860 | 4 | Owner role code and its scope recorded as Not specified in the source documents (GAP-2860) in section 4 step 2 |

### API:(service not named); OTHER:TSD S5 (next version); OTHER:contract dependency register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17803 | RWB-S5-E3024-CON | GAP-2861 | 1, 12.1 | Story header now lists three consumed rows; POST path stays Not specified in section 12.1. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0063 | Wave conflict S5 / EP01 | Tech lead | Resolved (directive) |
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
| GAP-0495 | The two lake extracts and the Power BI data set have no successor in the target, while the legacy story still writes them and reads the report | Solution architect | Resolved (directive) |
| GAP-0496 | TSD P1 keeps REC-03, REC-04 and a cross-estate REC-05 inside P1 while the Change Register gives rwb-case, rwb-asset and rwb-comms their own slices of the same legacy key | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0497 | The reconciliation result path, the result and break-row shape, the ReconciliationQuery interface and the workflow and activity names are not specified in any source | Tech lead | Resolved (directive) |
| GAP-0740 | The rwb-case slice of RWB-E1-011 leaves the check codes, the four operation paths, the call type to rwb-source-data, the case key columns, the Schedule cron, the access right, the login and every report value that only the data lake held unspecified | Solution architect, with the P1 rwb-source-data owner, the P3 rwb-case owner and the data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1168 | RWB-P6-E1011-APP: the parameters and reference-data contracts of rwb-case and the rwb-source-data contract the run reads are missing from the story's C list | Solution architect | Resolved (directive) |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1170 | RWB-P6-E1011-APP: the data lake is removed, so the reconciliation and data quality extracts and the report built on them have no target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1171 | RWB-P6-E1011-APP: no event is published because DP-09 is not in the pattern set, and no operation of rwb-reporting or rwb-source-data accepts the quality facts | Solution architect | Resolved (directive) |
| GAP-1172 | RWB-P6-E1011-APP: the quality tables, the check codes, the run cadence and the two quality read operations are not named in any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1173 | RWB-P6-E1011-APP: the right of the quality reads is Platform administration R in the legacy story, and the rwb-comms RBAC matrix has no Platform administration column | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1468 | The provision step thresholds and the held-asset re-appraisal interval are not specified | NPA and asset manager | Resolved (directive) |
| GAP-1499 | The data lake and the dashboard connection are removed, so the reporting destinations of three FSD features have no home | Solution architect | Resolved (directive) |
| GAP-1508 | The per-account reconciliation break rows have no store after the quality-exception table leaves the schema | Data architect | Resolved (directive) |
| GAP-1514 | The job monitor and data-quality screens are first-in here and owned by reporting in the architecture | Solution architect | Resolved (directive) |
| GAP-1750 | FSD S5 reads the ACE asset, collateral and score views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1751 | The asset record is modelled as an extension of the ACE asset, while Architecture v5 gives rwb-asset the assets taken on | Data architect | Resolved (directive) |
| GAP-1752 | The Ownership Map lists no table for auction rounds, bids or holding costs, although Architecture v5 and the rules need them | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1759 | Proceeds, cost of carry and fees are posted to ALS and the ledger by this service, while Architecture v5 gives posting to rwb-payment | Solution architect | Resolved (directive) |
| GAP-1761 | The disposal rule set has 72 rules over 40 states, the FSD names about 40 of them, and the package is Phase 2 with no code | Center of excellence analyst | Resolved (directive) |
| GAP-1767 | The statutory notice and the document evidence have no cell in the connection matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1768 | Four of the six messages this module shows belong to other services and the two of its own have no approved wording | Business analyst, S5 | Resolved (directive) |
| GAP-1906 | RWB-S5-E3019: the take-on slice has no source for its dependency rows, its event, its case move, its requirement id and the duplicated R-DIS-06 criterion | Solution architect | Resolved (directive) |
| GAP-1907 | RWB-S5-E3019: the asset table has no Ownership Map row and rwb-asset holds no ACE view grant while the legacy story reads v_ace_npa_asset | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1908 | RWB-S5-E3019: the published asset event has no DP-09 row in the plan | Solution architect | Resolved (directive) |
| GAP-1909 | RWB-S5-E3019: the case state read and the case-move answer have no published operation | Solution architect | Resolved (directive) |
| GAP-1910 | RWB-S5-E3019: the module declares no external dependency although the legacy step names RPS, the Field App and AMIS | Solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2232 | The split of RWB-E1-011 across the services and the case-side scope are not ruled by any source | Solution architect | Resolved (directive) |
| GAP-2233 | The case-side result row has no table and no check codes in the target | Solution architect | Resolved (directive) |
| GAP-2234 | No source names the operations, rights or response shapes of the case-side quality run | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2235 | The data-product reads that replace the ACE views have no published path, element shape or product code in this story's sources | Solution architect | Resolved (directive) |
| GAP-2236 | The hand-off of the case-side hold to the case-list publish gate is not specified | Solution architect | Resolved (directive) |
| GAP-2237 | TSD P3 v3 declares the case links as uuid cross-references while the FSD re-base and the legacy data table use the ACE business keys | Solution architect | Resolved (directive) |
| GAP-2238 | The report, the Schedule cadence, the alert groups and the feature flag of the case-side run have no source | Solution architect | Resolved (directive) |
| GAP-2837 | RWB-S5-E3019-APP: the take-on slice has no plan row for its cross-service reads, its outbox library, its requirement id or the duplicated R-DIS-06 criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2838 | RWB-S5-E3019-CON: the consumed operation names, the case boundary name, the event consumer list and the error set have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2839 | Legacy AC3 of a deed in lieu story tests the vehicle repossession rule R-DIS-01 | Business analyst, S5 | Resolved (directive) |
| GAP-2840 | The registered deed in lieu transfer contract RWB-S2-E3012-CON is absent from the contract-dependency row | Solution architect | Resolved (directive) |
| GAP-2841 | The asset table is absent from the Ownership Map although TSD S5 T3.1 and Architecture v5 give the asset record to S5 | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2842 | The rwb-source-data data-product read that carries the ACE NPA asset and collateral facts has no published operation name | Solution architect | Resolved (directive) |
| GAP-2843 | Event 22 AssetTakenOn needs the outbox library of DP-09, which the pattern set and the build row of this key do not carry | Platform library owner | Resolved (directive) |
| GAP-2844 | The case-move answer of rwb-case has no published operation | Solution architect | Resolved (directive) |
| GAP-2845 | No requirement id is allocated to legacy key RWB-E3-020 in the split plan | Business analyst, S5 | Resolved (directive) |
| GAP-2847 | RWB-S5-E3021: the take-on step consumes and publishes an event and reads four owner contracts, while the plan carries no C or I row and its pattern set omits DP-09 | Solution architect | Resolved (directive) |
| GAP-2848 | RWB-S5-E3021: two of the four legacy criteria are the rules of the other take-on routes and the LED rule of the feature has no legacy criterion | Business analyst with the S5 service owner | Resolved (directive) |
| GAP-2849 | RWB-S5-E3021: the LED result, its event properties, its column and the rwb-litigation contract have no published shape | Solution architect and the business analyst of S5 | Resolved (directive) |
| GAP-2850 | RWB-S5-E3021: the legacy key and both slices carry no requirement id and TSD S5 T8 names none for FEAT-AST-03 | S5 rwb-asset service owner with the business analyst | Resolved (directive) |
| GAP-2852 | The notice, its confirmed address, its delivery proof and the failed notice task have no rwb-asset column, no rwb-asset list and no rwb-asset row, and the feature's screens carry no notice state | S5 rwb-asset service owner with the P6 rwb-comms owner, the P1 rwb-source-data owner and the P3 rwb-case owner | Resolved (directive) |
| GAP-2853 | This legacy key owns no REST operation although the legacy story lists two, and the five consumed rows are class C in fact while the plan's C row is None | S5 rwb-asset service owner with the solution architect and the S1 rwb-valuation owner | Resolved (directive) |
| GAP-2854 | The trigger, the notice-serving operation, the confirmed-address field, the task-creation operation and the WIN integration point have no single source, and the feature carries no requirement id | S5 rwb-asset service owner with the solution architect, the P6 rwb-comms owner and the P3 rwb-case owner | Resolved (directive) |
| GAP-2857 | The legacy key carries no requirement id in the story master and the plan carries no requirement for either slice | S5 rwb-asset service owner with the business analyst | Resolved (directive) |
| GAP-2860 | RWB-S5-E3024-APP: the stock balance has no figure definition, no write operation for its confirmation, no object in the TSD, no requirement id, and its two take-on rules are owned by sibling stories | Business analyst S5 with the solution architect and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2861 | RWB-S5-E3024-CON: the balance element, the confirmation operation and the owner field have no published shape, path or source, and the split plan sets the contract dependency row to None | Solution architect with the tech lead of rwb-asset and the rwb-access contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2874 | No source names an operation, an event or a representation for the disposal-route recommendation, so the element and its property are design names of the baseline | S5 rwb-asset service owner with the solution architect and the API contract owner | Resolved (directive) |
| GAP-2940 | Legacy AC3 of RWB-E4-029 owns R-DIS-02, the deed in lieu take-on that RWB-S5-E3020-APP already builds for the same rule | Business analyst of the Asset module with the solution architect of S5 | Resolved (directive) |
| GAP-3169 | The reconciliation story writes 'the case exceptions' without naming a table | P1 data owner | Resolved (directive) |
| GAP-3172 | Service S5 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
