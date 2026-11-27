# RWB-PLT-LIB Shared libraries - review pack, part 3 of 4 (RWB-PLT-E1043-CON to RWB-PLT-TE006-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 154 |
| Cross-document (pending in another document) | 231 |
| Not applied (value not in the sources) | 17 |
| Open business decisions | 18 |
| Register gaps linked | 142 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-E1043-CON | 32 | 67 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1043 CON Reference data service with versioned tables - contract v2.md |
| RWB-PLT-E1047-APP | 14 | 8 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1047 APP Feature flags for module release with a removal date v2.md |
| RWB-PLT-E1047-CON | 23 | 26 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1047 CON Feature flags for module release with a removal date - contract v2.md |
| RWB-PLT-E1072-APP | 11 | 29 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1072 APP Drools runtime and rule package store v2.md |
| RWB-PLT-E1072-CON | 20 | 66 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1072 CON Drools runtime and rule package store - contract v2.md |
| RWB-PLT-N009-APP | 11 | 5 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT N009 APP RFC 9457 problem and Idempotency-Key helpers v2.md |
| RWB-PLT-N009-CON | 9 | 3 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT N009 CON RFC 9457 problem and Idempotency-Key helpers - interface and fake - contract v2.md |
| RWB-PLT-NF02-APP | 11 | 1 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT NF02 APP Shared library baseline v2.md |
| RWB-PLT-TE006-APP | 23 | 26 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT TE006 APP Outbox and retry for outbound work v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-PLT-E1047-CON | R-11657 | CG-ALL-1386 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-PLT-N009-APP | R-11856 | CG-ALL-1413 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-PLT-N009-CON | R-11857 | CG-ALL-1414 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-PLT-TE006-APP | R-11941 | CG-ALL-1422 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E1057-ITG, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-P5-E1057-APP, RWB-P5-E1057-CON, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-S9-E1057-APP | R-22197 | GAP-3146 | Register gap | Business lead; solution architect; rwb-partner tech lead; rwb-access owner; programme lead | RWB-S9-E1057-APP: the split plan gives this secondary slice no legacy criterion and no build row while the P5 slice of the same key hands the partner criteria to it, no source publishes a partner-by-code read or the code filter of GET /partners, the two refusal reasons and the not-found behaviour are not published, the constraint on partner_code and the panel transition table are not specified, the DP-07 rows cannot be carried in an empty H row, and EP01 wave 1 is earlier than the service wave 4 | Serve the partner panel read as the code filter of the published GET /partners under base /api/recovery/partner/v1 with right R and the scope applied, answer the six published properties from partner in rwb_partner, answer an empty list for an unknown code and the stored panel status for a partner that is not ACTIVE, leave BR4 and the two reasons with the caller, read LOV-PANEL and LOV-PARTNER-TYPE through DP-07, write nothing and publish nothing, keep wave 1 and record the DP-07 rows, the constraint on the partner code, the panel transition table and the criteria assignment of the two slices as open items. |
| RWB-ITG-TE006-ITG, RWB-PLT-N009-APP, RWB-PLT-N009-CON, RWB-PLT-TE006-APP, RWB-PLT-TE006-CON | R-22913 | GAP-1674 | Register gap | Compliance | The retention of the platform rows, of the stored idempotent answer and of the telemetry is not stated | Set the retention per platform object under DL26 and record it in the Logical Data Model next version. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23236 | GAP-3031 | Register gap | Solution architect; business lead | RWB-S7-E6020-APP: the review date has no property, field ID, column or list, the legacy timer table is not S7's, R-WO-17's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes four contracts, DP-04, DP-09 and DP-10 are absent, and no source publishes a rule, a message or a state for a date in the past or a second decision at DEFERRED | Keep the plan's H, C, I and X rows as they stand; carry the review date as an additive request property recorded in the decision record and the case move, with no column and no field ID until the business lead and rwb-case confirm them; set the review timer as a durable workflow timer and let rwb-case own the timer row; map R-WO-17's owner to the roles that hold right A for the act and to the write-off team for the return; declare the four consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-09 and DP-10 rows; leave a second decision at DEFERRED and a past review date unpublished and tracked |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S7-E6019-APP, RWB-S7-E6019-CON | R-23240 | GAP-3029 | Register gap | Solution architect; business lead | RWB-S7-E6019-APP: the reject reason and the decision code have no field, column or list, R-WO-16's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes three contracts, DP-04 and DP-09 are absent, and no published row moves a case out of RETURNED_TO_PURSUE | Keep the plan's H, C, I and X rows as they stand; record the reason and the decision code as request and record inputs with a placeholder until the business lead confirms them; map R-WO-16's owner to the four roles that hold right A in TSD S7 T6.1; declare the three consumed rows in sections 12.2 and 12.8 and record the absent DP-04 and DP-09 rows; leave the onward path of RETURNED_TO_PURSUE to the case owner and raise it in the next planning cut; keep committee_date and every other write_off column out of the reject slice |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S9-E6034-APP, RWB-S9-E6034-CON | R-23241 | GAP-3117 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S9-E6034-APP: the legacy story names two read endpoints and no operation that places the account, partner_instruction carries no rule-version or decision column, S9 owns no route set so the placement rule is only expressible as the D9 rows R-WO-29 to R-WO-32, the legacy permission table gives the Partner portal right R while the issue needs C and the FSD also-uses role has no matrix row, both screens are list states with no placement form, the plan C row is empty while the case and the rule package are consumed, DP-04 and DP-09 are absent, the EV-20 consumer set and payload are not published, and no requirement row traces to FEAT-PRM-06 | Keep the plan H, C, I and X rows as they stand; issue the placement through API-S9-002 and never through a new path; record the rule version and the picked agency on the local decision record and add no column to partner_instruction; read the placement rows from rwb-decision as data and record the absent DP-04 rows; read the case on the rwb-case contract and record the absent C rows; authorise the issue on the Partner portal right C the matrix gives and record the legacy right R and the missing also-uses row as conflicts; serve the placement from the list state of SCR-35 through the composite route and carry the form as a placeholder; publish EV-20 with IDs only and record the absent DP-09 row; let the trace rest on the legacy key and the feature row until the E6 BRD and the PRD publish a requirement |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-S6-E6005-APP, RWB-S6-E6012-APP | R-23244 | GAP-3015 | Register gap | Solution architect with the owners of rwb-case (P3), rwb-decision (P7), rwb-access (P4) and rwb-source-data (P1), and the business owner of the debt sale cap | RWB-S6-E6012-APP: the cap slice has no plan row for the five consumed contracts, no cap parameter row, no cap route rule, no published trigger, no headroom column and no service contract baseline | Publish the five consumed operations with their fake; add C rows for rwb-case, rwb-decision, rwb-access and rwb-source-data; add the DP-04, DP-06, DP-07, DP-08 and DP-09 rows the tables need; name the cap row, its version, its basis and its owner; publish one route rule for the cap or confirm that R-DS-19 and R-DS-23 are its only test and which story owns them; publish the trigger or confirm the call from the lot build and award steps; add the cap-position and headroom fields or confirm the decision record as their only home; create the service contract baseline for this legacy key; and carry REQ-S6-001 and BR-050 in the plan |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-PLT-E1037-CON, RWB-PLT-E1072-CON, RWB-P4-E1037-CON, RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-29029 | GAP-2809 | Register gap | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P4 rwb-access and platform library architects and the business owner of S4 | The D7.4 limit, the approval row and the rule-package read carry no value and no dependency row | Declare the approval as the P7 child workflow consumed on queue rwb-decision, the D7.4 limit and the approver's delegation as consumed on the rwb-access authorise contract, and the LITIGATION package with R-LIT-30 and R-LIT-41 to R-LIT-43 as consumed from rwb-decision, each with the placeholder on its operation name and ceiling; fix no limit value in code or in the document, and leave the metadata rows as the plan gives them. |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-29032 | GAP-2807 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case reference-data owner and the business owner of S4 | The fee schedule has no field list, no owner row and no version in any source | Read the fee schedule, the fee types and the court levels as versioned reference data of rwb-case on its contract, name the read on the contract rows of both stories with the operation name left as the placeholder, carry the schedule version on every decision record, and leave the metadata rows as the plan gives them. |
| RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1043-APP, RWB-P3-E1043-CON | R-29035 | GAP-0222 | Register gap | Data steward and data product owner | The Owner column is a stewardship role, not a service, and it is kept unchanged | Read column D as the stewardship owner that approves a value, and the appended 'Owning service (D-RCV-60)' as the service that loads and serves it; the Key sheet gains the two terms that say so. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-ITG-TE010-ITG, RWB-ITG-E1047-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P3-E1042-APP | R-35662 | ASM-3199 | Register assumption |  | The six open-point rows that named an individual (DL03, DL04, DL05, DL06, DL07, DL37) carry the Template and Rules R9 placeholder in the Owner column, with the organisation the same row already stated kept after it, and the five roles of section 9 are left as the only owner labels in the document. | Confirm the role that owns each of the six open points. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-E1043-CON | R-11628 | CG-ALL-1370 | 12.8 | Criteria and test data read ACE views directly | AC5 and TC-PLT-E1043-CON-04 are outside this chunk. The rwb-source-data contract fake key is not in the sources, so no 12.8 row can be named. |
| RWB-PLT-E1043-CON | R-18588 | DOR-RWB-PLT-E1043-CON-9 | 14 | Definition of Ready item 9 Messages: Partial | The Error and Message Standard v4 text for MSG-P3-027 is not in the sources. Rewriting the section 14 message would invent it, so it is left unchanged. |
| RWB-PLT-E1043-CON | R-28444 | GAP-1279 | find it | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Cites the rwb-decision login, migration, constraints and DP-table rows of other stories. The named sections are not in this chunk and no value was found in the chunk. |
| RWB-PLT-E1043-CON | R-28505 | GAP-2429 | find it | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Cites a story line with Depends on empty and RWB-P1-E1017-CON. This story reads None with RWB-P3 contract dependencies. Sections 3, 12.2, 12.8 and 13 are not in this chunk. |
| RWB-PLT-E1043-CON | R-28574 | GAP-3140 | find it | The DP table names platform H rows that the plan's H list does not carry | The H list and wave-0 baseline text belong to slice RWB-S9-E1032-APP, which is not in this chunk. This story's DP-added line lists different platform rows, so no baseline can be recorded here. |
| RWB-PLT-E1043-CON | R-28651 | GAP-1212 | find it | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | Concerns the dependency lists of RWB-P6-E1063-APP, not this story. The dependency and baseline sections are not in this chunk. |
| RWB-PLT-E1043-CON | R-28695 | GAP-1218 | find it | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Concerns the H list and lane wording of RWB-P6-E1073-APP, not this story. The pattern table and lane text are not in this chunk. |
| RWB-PLT-E1047-APP | R-07210 | DOR-RWB-PLT-E1047-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No epic design sign-off in the story, the DOR review or the 03 Requirements folder. The sign-off needs the epic design record, which is not in the sources. |
| RWB-PLT-E1047-APP | R-18614 | DOR-RWB-PLT-E1047-APP-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Empty, loading, error and no-access states for SCR-02 are not in the 03 Requirements folder or the story. They need the SCR-02 screen state spec, which the sources do not hold. |
| RWB-PLT-E1047-APP | R-18616 | DOR-RWB-PLT-E1047-APP-18 | not in chunk | Definition of Ready item 18 Open decisions: Partial | Directive decisions are recorded but the story text containing open decisions is not in this chunk, so the item cannot be resolved here. |
| RWB-PLT-E1072-APP | R-07243 | DOR-RWB-PLT-E1072-APP-16 | header | Definition of Ready item 16 Size: Fail | Size is not in the sources; the squad-refinement statement was removed and the placeholder kept. |
| RWB-PLT-E1072-APP | R-29049 | GAP-3167 |  | The number of Epic 1 rule packages is not reconciled with the phase 1 package list | No source names the five Epic 1 package codes; Build Notes v6 and the Temporal and Drools design give only the eight phase 1 names. Needs a P7 rule owner ruling; seed sits in RWB-P7-E1073-CON. |
| RWB-PLT-E1072-CON | R-29049 | GAP-3167 |  | The number of Epic 1 rule packages is not reconciled with the phase 1 package list | No source names which five of the eight Phase 1 packages are Epic 1 (checked Build Notes Epic 1 v6 and PRD PLT v1). Choosing them needs the P7 rule owner. No edit. |
| RWB-PLT-N009-APP | R-23293 | GAP-1401 | 11 | The published problem-detail schema, the error-map table source, the expiry window and the stored-response scope are not specified for the contract | Column-set clause (c) is not addressed by the story, so the item stays open. |
| RWB-PLT-NF02-APP | R-18806 | DOR-RWB-PLT-NF02-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Fix needs new AC rows in section 7 and TC rows in section 16, plus their next free numbers. Neither section is in this chunk, so no edit was made. |
| RWB-PLT-TE006-APP | R-11941 |  |  | Fields classed as personal data where the story says none is carried | No item ID or story text in this chunk, so no anchor exists for an edit. Needs the item and its current story text. |
| RWB-PLT-TE006-APP | R-26712 | CG-ALL-1421 | 14 | MSG-P2-001 text differs from the Error and Message Standard v4 | Error and Message Standard v4 wording of MSG-P2-001 was not found in folder search (see DOR item 9); the text cannot be aligned without invented wording. |

## 5. Cross-document changes (pending in the target document)


### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (41)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14039 | RWB-PLT-E1043-CON | CG-ALL-1371 | n/a | Renumber the duplicate FR-PLT-016 row in the next PRD version so each ID has one meaning. |
| CDC-14040 | RWB-PLT-E1043-CON | CG-ALL-1372 | n/a | Renumber the duplicate FR-PLT-017 row in the next PRD version so each ID has one meaning. |
| CDC-14041 | RWB-PLT-E1043-CON | CG-ALL-1373 | n/a | Renumber the duplicate FR-PLT-018 row in the next PRD version so each ID has one meaning. |
| CDC-14042 | RWB-PLT-E1043-CON | CG-ALL-1374 | header, 18 | Renumber the duplicate FR-PLT-020 in the PRD's next version so the identifier has one meaning. |
| CDC-14045 | RWB-PLT-E1043-CON | DOR-RWB-PLT-E1043-CON-2 | 18 | Renumber the duplicate meanings of FR-PLT-016, FR-PLT-017, FR-PLT-018 and FR-PLT-020 so each identifier has one meaning. |
| CDC-14214 | RWB-PLT-E1047-APP | CG-ALL-1379 | header | Renumber the duplicate FR-PLT-016 in the PRD's next version so each ID has one meaning. |
| CDC-14215 | RWB-PLT-E1047-APP | CG-ALL-1380 | header | Renumber the duplicate FR-PLT-017 in the PRD's next version so each ID has one meaning. |
| CDC-14216 | RWB-PLT-E1047-APP | CG-ALL-1381 | header | Renumber the duplicate FR-PLT-018 in the PRD's next version so each ID has one meaning. |
| CDC-14218 | RWB-PLT-E1047-APP | DOR-RWB-PLT-E1047-APP-2 | 18 | Give FR-PLT-016, FR-PLT-017 and FR-PLT-018 one meaning each in the PRD. |
| CDC-14220 | RWB-PLT-E1047-CON | CG-ALL-1387 | header | Renumber the duplicate FR-PLT-016 (feature flags with a removal date vs. versioned feature flag row) in the next PRD version |
| CDC-14221 | RWB-PLT-E1047-CON | CG-ALL-1388 | header | Renumber the duplicate FR-PLT-017 (parameter and configuration client) in the next PRD version |
| CDC-14222 | RWB-PLT-E1047-CON | CG-ALL-1389 | header | Renumber the duplicate FR-PLT-018 (reference-data client) in the next PRD version |
| CDC-14225 | RWB-PLT-E1047-CON | DOR-RWB-PLT-E1047-CON-2 | 18 | Give FR-PLT-016, FR-PLT-017 and FR-PLT-018 one meaning each so the §18 links resolve. |
| CDC-14466 | RWB-PLT-E1072-APP | CG-ALL-1396 |  | Renumber the duplicate definition of FR-PLT-014 in the PRD's next version so each ID has one meaning |
| CDC-14467 | RWB-PLT-E1072-APP | CG-ALL-1397 |  | Renumber the duplicate definition of FR-PLT-015 in the PRD's next version so each ID has one meaning |
| CDC-14468 | RWB-PLT-E1072-APP | CG-ALL-1398 |  | Renumber the duplicate definition of FR-PLT-016 in the PRD's next version so each ID has one meaning |
| CDC-14469 | RWB-PLT-E1072-APP | CG-ALL-1399 |  | Renumber the duplicate definition of FR-PLT-017 in the PRD's next version so each ID has one meaning |
| CDC-14470 | RWB-PLT-E1072-APP | CG-ALL-1400 |  | Renumber the duplicate definition of FR-PLT-018 in the PRD's next version so each ID has one meaning |
| CDC-14471 | RWB-PLT-E1072-APP | CG-ALL-1401 |  | Renumber the duplicate definition of FR-PLT-020 in the PRD's next version so each ID has one meaning |
| CDC-14489 | RWB-PLT-E1072-CON | CG-ALL-1407 | n/a | Renumber the duplicate FR-PLT-014 row in the next PRD version |
| CDC-14490 | RWB-PLT-E1072-CON | CG-ALL-1408 | n/a | Renumber the duplicate FR-PLT-015 row in the next PRD version |
| CDC-14491 | RWB-PLT-E1072-CON | CG-ALL-1409 | n/a | Renumber the duplicate FR-PLT-016 row in the next PRD version |
| CDC-14492 | RWB-PLT-E1072-CON | CG-ALL-1410 | n/a | Renumber the duplicate FR-PLT-017 row in the next PRD version |
| CDC-14493 | RWB-PLT-E1072-CON | CG-ALL-1411 | header | Renumber the duplicate FR-PLT-018 in the PRD's next version so each ID has one meaning |
| CDC-14494 | RWB-PLT-E1072-CON | CG-ALL-1412 | header | Renumber the duplicate FR-PLT-020 in the PRD's next version so each ID has one meaning |
| CDC-14497 | RWB-PLT-E1072-CON | DOR-RWB-PLT-E1072-CON-2 | 18 | Renumber duplicate FR-PLT-014, 015, 016, 017 and the other two duplicates in the PRD's next version |
| CDC-15313 | RWB-PLT-TE006-APP | CG-ALL-1423 | header | Renumber the duplicate FR-PLT-001 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15314 | RWB-PLT-TE006-APP | CG-ALL-1424 | header | Renumber the duplicate FR-PLT-009 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15315 | RWB-PLT-TE006-APP | CG-ALL-1425 | header | Renumber the duplicate FR-PLT-010 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15316 | RWB-PLT-TE006-APP | CG-ALL-1426 | header | Renumber the duplicate FR-PLT-011 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15317 | RWB-PLT-TE006-APP | CG-ALL-1427 | header | Renumber the duplicate FR-PLT-012 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15318 | RWB-PLT-TE006-APP | CG-ALL-1428 | header | Renumber the duplicate FR-PLT-013 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15319 | RWB-PLT-TE006-APP | CG-ALL-1429 | header | Renumber the duplicate FR-PLT-021 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15320 | RWB-PLT-TE006-APP | CG-ALL-1430 | header | Renumber the duplicate FR-PLT-022 (one of its two meanings) in the next PRD version. Owner: Business analyst. |
| CDC-15321 | RWB-PLT-TE006-APP | CG-ALL-1431 | header | Renumber the duplicate FR-PLT-023 definition in the next PRD version so the ID has one meaning. |
| CDC-15322 | RWB-PLT-TE006-APP | CG-ALL-1432 | header | Renumber the duplicate FR-PLT-024 definition in the next PRD version so the ID has one meaning. |
| CDC-15323 | RWB-PLT-TE006-APP | CG-ALL-1433 | header | Renumber the duplicate FR-PLT-025 definition in the next PRD version so the ID has one meaning. |
| CDC-15324 | RWB-PLT-TE006-APP | CG-ALL-1434 | header | Renumber the duplicate FR-PLT-026 definition in the next PRD version so the ID has one meaning. |
| CDC-15325 | RWB-PLT-TE006-APP | CG-ALL-1435 | header | Renumber the duplicate FR-PLT-028 definition in the next PRD version so the ID has one meaning. |
| CDC-15326 | RWB-PLT-TE006-APP | CG-ALL-1436 | header | Renumber the duplicate FR-PLT-029 definition in the next PRD version so the ID has one meaning. |
| CDC-15328 | RWB-PLT-TE006-APP | DOR-RWB-PLT-TE006-APP-2 | 18 | Give FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011 and 10 more listed FR IDs one meaning each; name the feature for REQ-DRI-007. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14058 | RWB-PLT-E1043-CON | GAP-1206 | Header | Update plan and dependency map to six H rows and three C rows from the DP table; keep metadata as the plan states until corrected. |
| CDC-14075 | RWB-PLT-E1043-CON | GAP-2317 | header | Add H RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON and C RWB-P3-E1043-CON for the RWB-P4-E2031-APP prerequisites. Leave the Work Package metadata unchanged. |
| CDC-14085 | RWB-PLT-E1043-CON | GAP-1885 | 18 | Carry the five consumed items as non-blocking rows: P7 approval contract as C of wave 2; case and partner contracts on fakes; RWB-P3-E1043-CON as C; declared rights as DP-08 edge and guard rules. |
| CDC-14086 | RWB-PLT-E1043-CON | GAP-2751 | 18 | Carry API-P5-002, API-P5-008 and API-P3-002 as non-blocking consumed rows on fakes; RWB-P3-E1043-CON as C; declared rights as DP-08 edge and guard rules. |
| CDC-14087 | RWB-PLT-E1043-CON | GAP-2801 | 18 | Carry the four appeal consumed surfaces as non-blocking rows: approval contract as C of its wave; case and partner contracts on fakes; RWB-P3-E1043-CON as C; DP-08 edge and guard rules. |
| CDC-14091 | RWB-PLT-E1043-CON | GAP-1335 | 13 | Carry RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON as sequencing rows; keep this story's metadata rows unchanged. |
| CDC-14092 | RWB-PLT-E1043-CON | GAP-1337 | 13 | Carry the platform contracts and the rwb-case rule-package, parameters and reference-data contracts (C RWB-P7-E1073-CON, C RWB-P3-E1042-CON, C RWB-P3-E1043-CON) as sequencing rows; keep metadata rows unchanged. |
| CDC-14508 | RWB-PLT-E1072-CON | GAP-2501 | 13 | Record the DP-added H and C contracts as non-blocking platform and published contracts in the Dependency Map, built against their fakes; keep the metadata rows as given. |
| CDC-14509 | RWB-PLT-E1072-CON | GAP-1291 | 13 | Record the DP-added H and C contracts as non-blocking platform and published contracts in the Dependency Map, built against their fakes; keep the metadata rows as given. |
| CDC-14516 | RWB-PLT-E1072-CON | GAP-2419 | 13 | Treat RWB-PLT-E1072-CON as a wave 0 platform contract with its fake; replace the agent contract fake with RWB-P10-TE013-CON when it lands. |
| CDC-14528 | RWB-PLT-E1072-CON | GAP-2797 |  | Declare the LITIGATION package as a non-blocking consumed contract from rwb-decision with its fake at the version in force; declare no rule row, package or rule version there. |
| CDC-14537 | RWB-PLT-E1072-CON | GAP-1337 |  | Carry the platform contracts and the rwb-case rule-package, parameter and reference-data contracts in the dependency map. Keep the metadata rows as set. |
| CDC-14538 | RWB-PLT-E1072-CON | GAP-1340 |  | Read the twelve DP-added dependencies from section 13 at assembly. Leave the metadata rows as the WP fixes them. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14056 | RWB-PLT-E1043-CON | GAP-0779 | n/a | Settle the load-path owner, publish /api/recovery/access/v1/masking-policies with Reference data R, and publish AccessPolicyChanged with change kind, version and effective date. |
| CDC-14078 | RWB-PLT-E1043-CON | GAP-2419 | header | Keep H and C as the Work Package fixes them; treat the seven platform contracts and RWB-P3-E1043-CON as wave 0 contract fakes; replace the agent contract fake with RWB-P10-TE013-CON when it lands. |
| CDC-14100 | RWB-PLT-E1043-CON | GAP-0221 | 7 | Keep every list row and Source cell; add Owning service (D-RCV-60) and Owning schema (D-RCV-60) columns: rule_row rwb_decision P7, document_type and retention_rule rwb_document P5, role rwb_access P4; state the serving contract in the route column. |
| CDC-14219 | RWB-PLT-E1047-APP | GAP-1667 | 8 | Add a platform row for the platform store and library component to the Services sheet. |
| CDC-14232 | RWB-PLT-E1047-CON | GAP-1667 |  | Name the platform store and the component that serves the four feature-flag paths, and add a platform row to the Services sheet if the store is a deployable. |
| CDC-14480 | RWB-PLT-E1072-APP | GAP-1413 | find it | Add a row for GET /rule-models/{n}/{v} owned by rwb-decision and list every model-holding service as RulePackageInForce subscriber. Story §11 now records shape and phase-1 format. |
| CDC-14517 | RWB-PLT-E1072-CON | GAP-0004 | 13 | Nominate one package per route set, owned by the service in the Ownership Map and delivered in the epic that starts that service. |
| CDC-14518 | RWB-PLT-E1072-CON | GAP-1413 | 1, 3, 12 | Add a GET /rule-models/{n}/{v} row to the Endpoints sheet with owner rwb-decision; the story names rwb-decision as owner and states the phase-1 format. |
| CDC-14545 | RWB-PLT-E1072-CON | GAP-1319 | 13 | Add the rwb-access authorise answer consumed by the two reads to the Ownership Map API table. |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14037 | RWB-PLT-E1043-CON | DOR-RWB-PLT-E1043-CON-14 | n/a | Record the signed epic design sign-off, then cite it in the story. |
| CDC-14459 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-14 | none | Record the signed epic design sign-off |
| CDC-14488 | RWB-PLT-E1072-CON | DOR-RWB-PLT-E1072-CON-14 | n/a | Record the signed epic design sign-off for this story |
| CDC-15103 | RWB-PLT-N009-APP | DOR-RWB-PLT-N009-APP-14 | header | Record the signed epic design sign-off; the story cannot record it from the source documents. |
| CDC-15108 | RWB-PLT-N009-CON | DOR-RWB-PLT-N009-CON-14 | - | Confirm and record the signed epic design sign-off for RWB-PLT-LIB; no signed design is in the story or source documents. |
| CDC-15137 | RWB-PLT-NF02-APP | DOR-RWB-PLT-NF02-APP-14 | none | Record the signed epic design sign-off for RWB-PLT-LIB |
| CDC-15309 | RWB-PLT-TE006-APP | DOR-RWB-PLT-TE006-APP-14 | Header | Record the signed epic design sign-off for service epic RWB-PLT-LIB. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14090 | RWB-PLT-E1043-CON | CG-ALL-1369 | 18 | Align the three requirement rows in RTM v7 with section 18 of RWB-PLT-E1043-CON, including REQ-DRI-011. |
| CDC-14217 | RWB-PLT-E1047-APP | DOR-RWB-PLT-E1047-APP-12 | 16, 18 | Align the REQ-DRI-010 test list with story section 18 (TC-E1-047-01 to TC-E1-047-10), which covers the ten tests in section 16. |
| CDC-14242 | RWB-PLT-E1047-CON | CG-ALL-1385 | 18 | Trace REQ-DRI-010 to TC-PLT-E1047-CON-01 to TC-PLT-E1047-CON-05 in the next RTM version, aligned with section 18. |
| CDC-14473 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-12 | 16, 18 | Add the section 18 test lists for TC-E1-072-08 and TC-E1-072-09 as RTM v7 states them |
| CDC-14474 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-2 | 18 | Feature and L3 process columns carry placeholders only |
| CDC-14483 | RWB-PLT-E1072-APP | CG-ALL-1395 | 18 | Align the test case lists of the six requirements that differ (including REQ-CWC-016) with section 18 of RWB-PLT-E1072-APP in the next RTM version. |
| CDC-14532 | RWB-PLT-E1072-CON | CG-ALL-1406 | 18 | Align the test lists of the six requirements in section 18 and in the RTM in their next versions. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14043 | RWB-PLT-E1043-CON | DOR-RWB-PLT-E1043-CON-1 | 1 | Add a role code or role name for 'platform contract owner' so that the role in section 1 resolves. |
| CDC-14223 | RWB-PLT-E1047-CON | DOR-RWB-PLT-E1047-CON-1 | 1 | Add a role code and name for 'consumer of the platform shared libraries', or confirm the existing role code section 1 should cite; code not specified in the source documents (DOR-RWB-PLT-E1047-CON-1) |
| CDC-14472 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-1 | 1 | Add the service-team role code, or confirm the role name to use in section 1 of RWB-PLT-E1072-APP |
| CDC-14495 | RWB-PLT-E1072-CON | DOR-RWB-PLT-E1072-CON-1 | 1 | Add or name a role code for the consumer of the embedded rules kit so section 1 cites a role present in the table |
| CDC-15109 | RWB-PLT-N009-CON | DOR-RWB-PLT-N009-CON-1 | 1 | Register tech lead as a role code and role name, or the story names a role already listed there. |
| CDC-15327 | RWB-PLT-TE006-APP | DOR-RWB-PLT-TE006-APP-1 | 1 | Add 'platform library engineer' as a role name, or confirm the existing role code it maps to, so the section 1 role resolves. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14089 | RWB-PLT-E1043-CON | CG-ALL-1368 | 16 | Add rows for TC-PLT-E1043-CON-01 to TC-PLT-E1043-CON-05 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-14241 | RWB-PLT-E1047-CON | CG-ALL-1384 | 16 | Add rows for TC-PLT-E1047-CON-01 to TC-PLT-E1047-CON-05 with Given, When and Then copied from AC1 to AC6. |
| CDC-14496 | RWB-PLT-E1072-CON | DOR-RWB-PLT-E1072-CON-12 | 16, 18 | Add TC-PLT-E1072-CON-01 to -06 to Test Cases v8; align section 18 test lists to RTM v7 |
| CDC-14531 | RWB-PLT-E1072-CON | CG-ALL-1405 | 16 | Add rows for TC-PLT-E1072-CON-01 to TC-PLT-E1072-CON-05 with Given, When and Then copied from the criterion each one covers. |

### RWB-PLT-TE006-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14235 | RWB-PLT-E1047-CON | GAP-2262 |  | Fix the event envelope and retry settings for rwb.case.events.v1, limiting the CaseCreated payload to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate and dpdAtEntry. |
| CDC-15310 | RWB-PLT-TE006-APP | DOR-RWB-PLT-TE006-APP-21 | Header | Move build status from Not started to Done. |
| CDC-15329 | RWB-PLT-TE006-APP | GAP-1416 | 18 | Publish one artifact with a major version; the three interfaces with exceptions; DDL template of four tables incl. processed_event and idempotency_key columns; CloudEvents 1.0 attributes incl. caseId and ce_type shape; inbox dedupe rule; retry ladder 1 min, 10 min, 1 h, dead-letter topic with one alert and replay tool; case-step events, task and decision record stay with owning service. |
| CDC-15331 | RWB-PLT-TE006-APP | GAP-1415 | 7 | State which part of the exception path the library owns and which part the owning case-step service owns; the relay is a continuous per-service worker, not a Temporal Schedule; one alert to the platform administrator on the dead-letter path. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14036 | RWB-PLT-E1043-CON | CG-ALL-1366 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story key that serves the rwb-decision registry dependency in section 13 DP-04. |
| CDC-14458 | RWB-PLT-E1072-APP | CG-ALL-1392 | 13 | Create story file RWB-P7-E1073-CON, or name the existing governance-contract story the dependency refers to |
| CDC-14460 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-17 | 13 | Create story file RWB-P7-E1073-CON, or name the existing governance-contract story the dependency refers to |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14038 | RWB-PLT-E1043-CON | CG-ALL-1367 | 14 | The v4 text is not in the source documents, so the story keeps the legacy text. The standard must supply the wording. |
| CDC-14465 | RWB-PLT-E1072-APP | CG-ALL-1394 | 14 | MSG-P3-027 text kept unchanged |
| CDC-14476 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-9 | 14 | Confirm the MSG-P3-027 text against the standard or restore the legacy text. Story keeps the text unchanged, per GAP-1414. |

### RWB-P7-E1073-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14061 | RWB-PLT-E1043-CON | GAP-1328 | n/a | Complete the APP metadata rows from the DP table: eight H rows and the C rows of DP-06 and DP-07, and add DP-09 to the pattern list. |
| CDC-14234 | RWB-PLT-E1047-CON | GAP-1328 |  | Complete the metadata rows from the DP table or state in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories. |
| CDC-14505 | RWB-PLT-E1072-CON | GAP-1328 |  | Complete the H and C metadata from the DP table or state in Template and Rules R5.5 that platform H and self-referential C rows are held by the platform and contract stories. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14079 | RWB-PLT-E1043-CON | GAP-1558 | find it | Realign the x-module of GET /admin/lists/{listCode}, POST /admin/reference-loads and the three sibling list and reference-load paths to P3 rwb-case. |
| CDC-14482 | RWB-PLT-E1072-APP | GAP-2029 | find it | Add GET /rule-models/{n}/{v} under /api/recovery/decision/v1, owned by rwb-decision, and confirm the operation name and payload. |
| CDC-14519 | RWB-PLT-E1072-CON | GAP-2029 | 3 | Add the GET /rule-models/{n}/{v} operation served by rwb-decision under /api/recovery/decision/v1, confirming its operation name and payload. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14093 | RWB-PLT-E1043-CON | GAP-2484 | 13 | Assign GET /cases/{caseId}/recommendation to the P7 story that serves the decision screen; treat RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON as published before Day 1. |
| CDC-15107 | RWB-PLT-N009-APP | GAP-3232 | header | Use the Dependencies sheet as the source of the v5 graph and state the template baseline once on the Dependency classes sheet; story files keep their rows. |
| CDC-15110 | RWB-PLT-N009-CON | GAP-3232 | find it | Use the catalog as the source of the v5 dependency graph and state the template baseline once on the Dependency classes sheet. Story files keep their rows; no story is re-cut. |

### RWB-PLT-E1072-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14461 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-21 | none | Set build status to Done once the contract is published |
| CDC-14462 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-22 | find it | Record the published version of the contract fake library for RWB-PLT-E1072-CON |
| CDC-14463 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-23 | header | Contract version row set to a placeholder; the path-derived v1 was removed. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14475 | RWB-PLT-E1072-APP | DOR-RWB-PLT-E1072-APP-7 | 11 | Confirm whether metric name drools_kiebase_builds_total is a field or entity, or record it as a platform metric outside the data model. Story §11 now states nine rows have no BR Field ID. |
| CDC-14478 | RWB-PLT-E1072-APP | GAP-2457 | find it | Provide physical columns, types, nullability, state and artifact columns for rule_package, rule_package_version, rule_row and rule_test_case, for TSD P7 T3.1. |
| CDC-14502 | RWB-PLT-E1072-CON | GAP-2457 |  | Add physical columns, types and nullability for rule_package, rule_package_version, rule_row and rule_test_case; confirm artifact columns with the embedded Drools kit of this story. |

### OTHER:Rules Engine Design v3 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14546 | RWB-PLT-E1072-CON | GAP-2025 | n/a | Mark the sections 1 and 6 wording (Drools embedded in the recovery module; one Spring service inside the module) as superseded by Architecture v5: embedded Drools per service, registry in rwb-decision. |
| CDC-14547 | RWB-PLT-E1072-CON | GAP-2027 | n/a | Section 6: RuleCatalog and RulePackageRepository are served by rwb-decision (P7) over rule_package, rule_package_version, rule_row and rule_test_case; owning services ask the registry and keep no rule_row copy. |
| CDC-14548 | RWB-PLT-E1072-CON | GAP-2028 | n/a | Section 3: the Import line names the owning service's fact class. Exact class names: Not specified in the source documents (GAP-2028), settled when the packages are authored. |

### RWB-S5-E1011-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14046 | RWB-PLT-E1043-CON | GAP-1946 |  | Record the nine platform and rwb-case CONs as wave-0 prerequisites and fakes; read the ACE check as the DP06 data product; drop the extracts and INT-19 path; serve facts from the asset quality GET endpoints. |
| CDC-14226 | RWB-PLT-E1047-CON | GAP-1946 |  | Apply the proposed fix: keep H and C at None, record the nine CONs as wave-0 prerequisites, serve quality facts from the quality endpoints. |

### RWB-P6-E1011-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14047 | RWB-PLT-E1043-CON | GAP-1167 |  | Keep plan H at None; record the seven platform CONs as wave-0 build prerequisites from the platform release train; add them to the dependency map as platform prerequisites. |
| CDC-14227 | RWB-PLT-E1047-CON | GAP-1167 |  | Keep H at None and record the seven platform CONs as wave-0 build prerequisites, added to the dependency map as platform prerequisites. |

### RWB-P6-E1019-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14049 | RWB-PLT-E1043-CON | GAP-1174 |  | Add RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON to its dependency rows, or record them in the platform release train. |
| CDC-14228 | RWB-PLT-E1047-CON | GAP-1174 |  | Add RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON and RWB-PLT-E1044-CON to its dependency rows, or record them in the release train. |

### RWB-S8-E1021-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14050 | RWB-PLT-E1043-CON | GAP-3075 |  | Platform owner confirms which of the eight platform contracts publish before release; reissue metadata rows if the plan is reissued; keep build list empty and C as RWB-P3-E1021-CON. |
| CDC-14498 | RWB-PLT-E1072-CON | GAP-3075 |  | Record the DP-table H and C rows in the metadata rows; keep H empty and C RWB-P3-E1021-CON as the plan states. |

### RWB-PLT-E1043-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14054 | RWB-PLT-E1043-CON | GAP-1147 | Header | At next plan revision add H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON for DP07 to the dependency rows. Header already lists DP07 and C RWB-P3-E1043-CON. |
| CDC-14055 | RWB-PLT-E1043-CON | GAP-2414 | Header | Carry the H and C rows that the DP table adds into the plan metadata; header keeps Depends on (build) None and the contract list as delivered. |

### RWB-P7-E2002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14064 | RWB-PLT-E1043-CON | GAP-2470 |  | Complete the metadata rows from the DP table, or keep the plan rows and state in R5.5 that platform H and self-referential C rows are held by their platform and contract stories. |
| CDC-14506 | RWB-PLT-E1072-CON | GAP-2470 |  | Complete the H and C metadata from the DP table, or state in Template and Rules R5.5 that platform and self-referential rows are held by other stories. |

### RWB-P7-E2004-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14065 | RWB-PLT-E1043-CON | GAP-2475 |  | State in R5.5 that platform H and self-referential C rows are held by the platform and contract stories, or complete the metadata rows from the table; list the patterns and read their dependencies as pattern-added. |
| CDC-14236 | RWB-PLT-E1047-CON | GAP-2475 |  | State in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories, or complete the metadata rows from the DP table. |

### RWB-P7-E2042-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14098 | RWB-PLT-E1043-CON | GAP-1296 | n/a | Carry the eight platform H and three C DP-added dependencies in the story; keep the metadata as written and Ready to start Day 1 (R5.7 rule 2). |
| CDC-14544 | RWB-PLT-E1072-CON | GAP-1296 |  | Carry the DP-added platform and published contracts in that story as build-against dependencies. Keep the metadata as written and Ready to start Day 1. |

### RWB-PLT-E1047-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14212 | RWB-PLT-E1047-APP | DOR-RWB-PLT-E1047-APP-21 | header | Build status moves from Not started to Done once the contract is published. The app story cannot change this. |
| CDC-14213 | RWB-PLT-E1047-APP | DOR-RWB-PLT-E1047-APP-22 | header | Publish the contract fake library and record its version so this story can cite it. |

### RWB-P7-E2041-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14230 | RWB-PLT-E1047-CON | GAP-2414 | find it | Depends on (build) H list: RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON. Contract dependencies C list: RWB-P3-E2041-CON, RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON. Treat RWB-P7-E2042-APP as the published registry operation set; keep Ready to start Day 1; re-check at wave 2 kick-off. |
| CDC-14499 | RWB-PLT-E1072-CON | GAP-2414 |  | Complete the H and C metadata from the DP table, or state in Template and Rules v1 R5.5 that platform H and self-referential C rows are held by the platform and contract stories. |

### RWB-PLT-E1047-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14237 | RWB-PLT-E1047-CON | GAP-2501 |  | Record the DP-added H and C platform and published contracts as non-blocking, built against their fakes; keep the metadata rows as given. |
| CDC-14238 | RWB-PLT-E1047-CON | GAP-1291 |  | Record the DP-added H and C platform and published contracts as non-blocking, built against their fakes; keep the metadata rows as given. |

### RWB-S6-E6007-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14240 | RWB-PLT-E1047-CON | GAP-3004 |  | Keep the plan H, C, I and X rows; track RWB-PLT-TE006-CON, RWB-PLT-E1047-CON and RWB-P2-E1007-CON as dependencies; split R-DS-25 into one saga. |
| CDC-14522 | RWB-PLT-E1072-CON | GAP-3004 |  | Keep H, C, I and X rows; build on six contract fakes on Day 1; publish AccountsTransferred via platform outbox; track RWB-PLT-TE006-CON, RWB-PLT-E1047-CON and RWB-P2-E1007-CON as dependencies; split R-DS-25 into one saga. |

### RWB-P6-E1073-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14245 | RWB-PLT-E1047-CON | GAP-1218 |  | Add the eight platform CONs to the H list or state them as wave-0 prerequisites in the lane document; keep Ready to start at Day 1. |
| CDC-14535 | RWB-PLT-E1072-CON | GAP-1215 |  | Make the DP-04 row and the RWB-P6-E1073-APP plan line agree on the H and C dependencies. Keep the plan Metadata rows as written. |

### RWB-P7-E1073-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14510 | RWB-PLT-E1072-CON | GAP-2748 | 13 | Carry the LITIGATION package read as a non-blocking consumed row with its fake; record DP-04 with H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON in the Dependency Map. |
| CDC-14511 | RWB-PLT-E1072-CON | GAP-2785 | 13 | Carry the package read as a non-blocking consumed row with its fake; record DP-04 with H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON in the Dependency Map. |

### RWB-S6-E5023-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14525 | RWB-PLT-E1072-CON | GAP-2973 |  | Keep H, C, I and X rows; record rwb-case, rwb-source-data and rwb-decision as class C; add RWB-PLT-TE006-CON, rule kit RWB-PLT-E1072-CON with RWB-P7-E1073-CON; read cap from package; declare deviation_open and fraud_flag as inputs; adopt REQ-S6-001. |
| CDC-14529 | RWB-PLT-E1072-CON | GAP-1947 |  | Keep the metadata rows as stated; declare the four consumed rows in section 12.2 with the operation-name placeholder and the fakes of 12.8; read the DEBTSALE package as data; trace REQ-S6-001 from the FSD. |

### RWB-PLT-N009-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15104 | RWB-PLT-N009-APP | DOR-RWB-PLT-N009-APP-21 | header | Set build status to Done once the contract is published. |
| CDC-15105 | RWB-PLT-N009-APP | DOR-RWB-PLT-N009-APP-22 | header | Record the published contract fake library version. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14044 | RWB-PLT-E1043-CON | DOR-RWB-PLT-E1043-CON-12 | 16, 18 | Add TC-PLT-E1043-CON-01 to TC-PLT-E1043-CON-06 to Test Cases v8, and align the RTM v7 test lists with section 18. |

### OTHER:rwb-reporting base contract for table measure_definition (P9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14048 | RWB-PLT-E1043-CON | GAP-2568 |  | Declare the reference-load element of measure_definition on the rwb-reporting base; keep list values on the rwb-case contract; rwb-case owner confirms whether a P9 table load belongs to the framework. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14051 | RWB-PLT-E1043-CON | GAP-2404 |  | Read H as None plus the five platform contracts from the DP table; read C as RWB-P10-E2032-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and the P4 authorise contract; story stays Day 1. |

### RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14052 | RWB-PLT-E1043-CON | GAP-2448 |  | Keep metadata rows as the work package fixes them; record the DP-table dependencies in section 13, built against fakes on Day 1. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14053 | RWB-PLT-E1043-CON | GAP-1198 |  | Add seven platform contracts and two P3 contracts (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) to its dependency rows, or record them in the release train. |

### OTHER:FSD P7 v3 and TSD P7 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14057 | RWB-PLT-E1043-CON | GAP-2453 | n/a | Make the P7 copy the record side of the template key with one template_use row per accepted answer and fix its table, columns and migration in rwb_decision DB story. |

### OTHER:FSD P4 v3; OTHER:TSD P4 v3 and Delivery plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14059 | RWB-PLT-E1043-CON | GAP-2333 | n/a | Correct REQ-ACA-006 and NFR-042 in next FSD and TSD version; add five platform contracts to H and two rwb-case contracts to C in the plan. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14060 | RWB-PLT-E1043-CON | GAP-0672 | n/a | Record the eight DP H rows as wave-0 prerequisites, publish the model fetch in RWB-P7-E1073-CON, and name the login before the baseline. |

### OTHER:Delivery plan dependency list of the product-code map story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14062 | RWB-PLT-E1043-CON | GAP-0593 | n/a | Add the H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON pair to the dependency list of the product-code map story at next plan revision. |

### OTHER:Work Package WP B2-P3-020 lane and Day-1 allocation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14063 | RWB-PLT-E1043-CON | GAP-2261 | Header | Assembler adds the platform CON dependencies to the lane and Day-1 allocation; metadata row stays as delivered by the WP. |

### RWB-P7-E2006-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14066 | RWB-PLT-E1043-CON | GAP-1343 |  | Publish the six DP-added dependencies in the Story Build Order and Dependency Map with this story as consumer; confirm RWB-P4-E1037-CON at the wave 2 contract review; optionally add it as a C row. |

### RWB-P1-E2008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14067 | RWB-PLT-E1043-CON | GAP-0604 |  | Add RWB-P3-E1043-CON to contract dependencies at the wave 2 freeze and serve the lists from rwb-case reference data; until then build on the client library and fixture, or record the ruling in the Ownership Map and FSD P1. |

### OTHER:Not specified in the source documents (GAP-2501) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14068 | RWB-PLT-E1043-CON | GAP-2501 |  | Keep the metadata rows as the plan gives them; record the DP-added H and C rows in the Dependency Map as non-blocking platform and published contracts built against fakes; section 13 keeps them visible. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14069 | RWB-PLT-E1043-CON | GAP-1223 |  | Read the H list as None plus the platform contracts named by the DP table, and the C list as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON; the story stays Day 1. |

### RWB-S4-E5001-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14070 | RWB-PLT-E1043-CON | GAP-2743 |  | Record the two consumed rows as C dependencies in the Dependency Map; declare notice and template ownership in the Ownership Map; name the P6 operations; add REQ-S4-001 to the trace; decide the D7.1 gate in the EP05 PRD. |

### OTHER:Not specified in the source documents (GAP-2354) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14071 | RWB-PLT-E1043-CON | GAP-2354 |  | Record the six platform CONs as wave-0 platform release train prerequisites of every wave-1 service; add RWB-P3-E1043-CON to the contract rows of stories whose pattern set claims DP-07; keep lane L-P5-W unchanged. |

### RWB-S4-E2025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14072 | RWB-PLT-E1043-CON | GAP-1898 |  | Keep the plan lists and build against the five fakes; when the platform stories and rwb-case contracts publish, add the five H and two C rows, re-run the dependency check and replace the fakes; remove DP-09 and DP-10 from the pattern list. |

### RWB-P8-E2027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14073 | RWB-PLT-E1043-CON | GAP-1291 |  | Keep the metadata rows as the plan gives them; record the DP-added H and C rows in the Dependency Map as non-blocking platform and published contracts built against fakes; keep the DP-04 and DP-14 contracts visible in section 13. |

### OTHER:04 User stories; RWB-P7-E2028-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14074 | RWB-PLT-E1043-CON | GAP-1295 | header | Set Depends on (build) to None plus H RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON; set contract dependencies to RWB-P10-E2028-CON plus C RWB-P3-E1043-CON and the published P3 case-read and P4 authorise contracts. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; OTHER:P3 and P4 CON stories at wave 2 entry, platform DB story; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14076 | RWB-PLT-E1043-CON | GAP-2412 | find it | Publish placement fact element names on rwb.decision-record.v1, the P3 case-read and P4 authorise shapes, the reference-data operation, MSG-P7-009 text, the login name and the secret store entry. |

### RWB-P3-E1043-CON; OTHER:TSD S2 T5.2 next version; RWB-S2-E3006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14077 | RWB-PLT-E1043-CON | GAP-2652 | find it | Publish the set identifiers, the four values and the freshness limit as rows before the wave 2 tag; correct TSD S2 T5.2 to name P3 rwb-case as the reference-data owner. |

### RWB-P3-E1043-CON; OTHER:data steward review of per-code column definitions (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14080 | RWB-PLT-E1043-CON | GAP-0697 | find it | Publish the element names of the load, check-result and version-list resources; hold per-code column definitions as data beside LOV-REF-TABLE; leave types to data steward review. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:Lists sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14081 | RWB-PLT-E1043-CON | GAP-0217 | find it | Copy the 25 LOV-REF-TABLE values unchanged in v5; let the contract name its twelve codes as a subset; reconcile both sets before the first wave 1 reference load. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:Reference data starter sheet, next revision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14082 | RWB-PLT-E1043-CON | GAP-0219 | find it | Add starter rows for S1 rwb-valuation and S7 rwb-writeoff at the next revision, naming the lists each reads. v5 keeps both services open. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14083 | RWB-PLT-E1043-CON | GAP-0220 | find it | Keep the stated derivation rule; service stories confirm their starter rows at design review; a later revision replaces derived rows with confirmed ones. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14084 | RWB-PLT-E1043-CON | GAP-0696 | 13 | Serve the eleven non-DoA codes from the reference surface; read delegation limits via rwb-access GET /doa-limits in its section 12.2; create no delegation_limit copy in rwb_case. |

### RWB-S6-E5025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14088 | RWB-PLT-E1043-CON | GAP-3014 | 18 | Carry the six consumed rows in 12.2 with the operation-name placeholder and fakes in 12.8; hold tape reference, checksum and check result in the decision record; record PII service as unmapped. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14094 | RWB-PLT-E1043-CON | GAP-2389 | 13 | At the next plan revision add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON and the rwb-case contracts of DP-06 and DP-07 to the C list of slice RWB-P6-E2014-APP. |

### OTHER:Work Package B2-P4-021 story line (fixed by the WP) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14095 | RWB-PLT-E1043-CON | GAP-2312 | n/a | No change to the WP metadata rows; confirm at the wave 2 planning gate that no H chain is missing from the lane. |

### OTHER:Build sequence of the wave plan (delivery lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14096 | RWB-PLT-E1043-CON | GAP-2410 | n/a | Record that a secondary slice builds against the platform contracts and published fakes and reads the same service's wave-1 rows through its own schema, keeping lane depth within R5.7 rule 5. |

### OTHER:RWB-E2-041 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14097 | RWB-PLT-E1043-CON | GAP-0719 | n/a | Record the rule-package scope for RWB-E2-041; keep the reference-data checklist and its report with RWB-E1-043. |

### RWB-P3-E2042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14099 | RWB-PLT-E1043-CON | GAP-2398 | n/a | Carry the eleven added rows in the DP application of section 13 and section 18; leave the metadata rows as the WP fixes them. |

### OTHER:Reference tables sheet of the reference workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14101 | RWB-PLT-E1043-CON | GAP-0223 | 8 | Record the owner of each of the five Reference table rows from its map item (Source cells and Ownership Map); name reference_row in rwb-case as the carrier of the message catalogue; leave the Table cells unchanged. |

### OTHER:Work Package plan: wp/B-P4-04.md, wp/B2-P4-010.md and split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14102 | RWB-PLT-E1043-CON | GAP-2278 |  | Remove RWB-AD-016 from the B-P4-04 fanout so B2-P4-010 alone owns it; number the CG and ASM IDs once; add a plan-uniqueness check to checks/run_all.py. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14224 | RWB-PLT-E1047-CON | DOR-RWB-PLT-E1047-CON-12 | 16, 18 | Register TC-PLT-E1047-CON-01 to TC-PLT-E1047-CON-05 in Test Cases v8; align the RWB-PLT-E1047-CON test list in RTM v7 with section 18 |

### RWB-S8-E1021-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14229 | RWB-PLT-E1047-CON | GAP-3075 |  | Correct the metadata rows to record the eight platform H rows and two C rows added by pattern application, once the platform owner confirms publication. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14231 | RWB-PLT-E1047-CON | GAP-1411 |  | Allocate one platform-owned store schema name for feature_flag and feature_flag_change, let the library cache per service, and record the allocation before the store migration is written. |

### RWB-P2-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14233 | RWB-PLT-E1047-CON | GAP-0672 |  | Keep the plan H and C lists as written, record the eight DP H rows as wave-0 prerequisites, publish the model fetch in RWB-P7-E1073-CON, and name the login before the rwb_integration baseline. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14239 | RWB-PLT-E1047-CON | GAP-2412 |  | Publish the placement fact element names and key, the decision-record library signature, the case-read and authorise shapes, the reference-data operation and the MSG-P7-009 text. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14243 | RWB-PLT-E1047-CON | GAP-1279 |  | Fix the rwb-decision login, migration file and sequence, constraint and index names at merge; carry the six platform contracts in preconditions, not an H row. |

### OTHER:WP B2-P8-008 story line (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14244 | RWB-PLT-E1047-CON | GAP-2540 |  | Keep H None and Day 1; carry the six platform contracts as the service baseline in the preconditions and the fakes. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14464 | RWB-PLT-E1072-APP | CG-ALL-1391 | none | Record drools_kiebase_builds_total as an operability counter object (metric) in the owning document |

### OTHER:TSD P7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14477 | RWB-PLT-E1072-APP | GAP-1615 | find it | Add T3.1 entries for rule_package, rule_package_version, rule_row, rule_test_case and appendix T-A rule operations; remove them from TSD P3 and TSD P4; set x-module of nine rule paths to P7 in API Specification. |

### OTHER:Temporal and Drools design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14479 | RWB-PLT-E1072-APP | GAP-0004 | find it | Nominate the owning service for each of the ten route-set packages and schedule one package per route set in the epic that starts that service. |

### OTHER:Platform library baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14481 | RWB-PLT-E1072-APP | GAP-1414 | find it | Record kit artefact group, artefact name and release cadence at version freeze. Fetch error codes come from rwb-decision's document. Story §14 keeps MSG-P3-027 unchanged. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14484 | RWB-PLT-E1072-APP | GAP-3163 | find it | Read Module P3 as consumed by P3, not owned by P3, for RWB-E1-070 to RWB-E1-072; keep the build order in the notes. |

### OTHER:ADR-017 (Architecture decision register) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14485 | RWB-PLT-E1072-APP | GAP-1620 | find it | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime, that a package version names its format, and that conversion is a version change with its own test evidence. |

### OTHER:Recovery Workbench Rules Engine Design v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14486 | RWB-PLT-E1072-APP | GAP-2028 | 3 | Import line in section 3 names the owning service's fact class; the exact fact class names stay Not specified in the source documents (GAP-2028) |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14487 | RWB-PLT-E1072-CON | CG-ALL-1403 | 13 | Create story file RWB-P7-E1073-CON, or name the existing governance story key in section 13 and the header |

### OTHER:rwb-agent screening APP story (legacy RWB-E1-062 split) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14500 | RWB-PLT-E1072-CON | GAP-0614 |  | Fix the run-start operation, request members, refusal codes, feature flag and boundary status in that story and the P10 contract; this story publishes only the rule-model read it uses. |

### OTHER:TSD P7; OTHER:TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14501 | RWB-PLT-E1072-CON | GAP-1615 |  | Re-issue TSD P7 with T3.1 entries and T-A operations for the four rule tables; remove them from TSD P3 and TSD P4; correct x-module of nine rule paths to P7. |

### OTHER:Build Notes v6 (RWB-E1-072 and RWB-E1-073 View notes) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14503 | RWB-PLT-E1072-CON | GAP-3157 |  | Correct the rule tables' schema from recovery to rwb_decision (P7) and state governance in P7 with an evaluated local copy per owning service. |

### RWB-P2-E1073-APP; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14504 | RWB-PLT-E1072-CON | GAP-0672 |  | Record the DP-table H rows as wave-0 prerequisites; publish the model fetch in RWB-P7-E1073-CON; fix the local copy table and login in the rwb_integration story. |

### OTHER:Template and Rules v1 R5.5; RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14507 | RWB-PLT-E1072-CON | GAP-2475 |  | State in R5.5 that platform H and self-referential C rows are held by platform and contract stories, or complete the APP plan metadata from the DP table. |

### RWB-S7-E6017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14512 | RWB-PLT-E1072-CON | GAP-3025 | 13 | Record RWB-PLT-E1072-CON and RWB-P7-E1073-CON as tracked dependencies; keep the plan's H, C, I and X rows as they stand. |

### RWB-S7-E6025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14513 | RWB-PLT-E1072-CON | GAP-3041 | 13 | Record RWB-PLT-E1072-CON, RWB-P7-E1073-CON and RWB-PLT-TE006-CON as tracked dependencies; keep the plan's H, C, I and X rows as they stand. |

### RWB-S8-E7002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14514 | RWB-PLT-E1072-CON | GAP-3053 | 13 | Record RWB-PLT-TE006-CON as the wave 0 library and RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the evaluation kit; keep the H, C, I and X rows. |

### RWB-S8-E7004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14515 | RWB-PLT-E1072-CON | GAP-3057 | 13 | Record RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit and RWB-PLT-TE006-CON as the outbox library; keep the H, C, I and X rows. |

### RWB-S9-E7011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14520 | RWB-PLT-E1072-CON | GAP-3121 |  | Build against the rule set in force and the two faked reads; keep measures, trigger and reporting channel as placeholders; before Done, publish scorecard rule rows in rwb-decision and the two reads, and a reporting path or recorded decision. |

### OTHER:rwb-asset DISPOSAL step story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14521 | RWB-PLT-E1072-CON | GAP-1944 |  | Fetch the DISPOSAL package at its version in force on the rwb-decision package contract at step start; hold it for evaluation; write package code and version to the decision record; declare the row consumed; leave pattern set and event catalogue unchanged. |

### RWB-S7-E6015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14523 | RWB-PLT-E1072-CON | GAP-3021 |  | Keep H, C, I and X rows; record seven consumed rows as class C with placeholders; add C RWB-P10-TE013-CON, H RWB-PLT-TE006-CON, RWB-PLT-E1072-CON and RWB-P7-E1073-CON; adopt REQ-S7-002 and correct TSD T8. |

### RWB-S7-E6013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14524 | RWB-PLT-E1072-CON | GAP-3016 |  | Keep H, C, I and X rows; record rwb-case, rwb-source-data and rwb-decision as class C; add rule kit RWB-PLT-E1072-CON with RWB-P7-E1073-CON, outbox library RWB-PLT-TE006-CON and scheduled job kit RWB-PLT-E1071-CON; declare JOB-16 Schedule and ACE trigger. |

### RWB-S6-E6011-APP; OTHER:C; OTHER:I; OTHER:X rows); 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14526 | RWB-PLT-E1072-CON | GAP-3012 |  | Add plan rows for the six consumed contracts, the inbox library RWB-PLT-TE006-CON, the rule kit RWB-PLT-E1072-CON with RWB-P7-E1073-CON, the settlement stamp and FEAT-DBS-12 as tracked items; keep wave 4 and the release date. |

### RWB-S7-E6016-APP; OTHER:TSD S7 and FSD S7 write-off base (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14527 | RWB-PLT-E1072-CON | GAP-3023 |  | Add the removal operation with a placeholder path; declare removal_reason as free text validated as present and stored in the decision record; record the three consumed contracts and the kit and library rows. |

### OTHER:Build plan of the rwb-access rule-version load story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14530 | RWB-PLT-E1072-CON | GAP-0822 |  | Record that rwb-access embeds no Drools kit and carries no DP-04; compile, checks and the SIT scenario run stay in rwb-decision, which returns the result. |

### OTHER:Build Notes v6, configuration notes RWB-E1-070 to RWB-E1-072 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14533 | RWB-PLT-E1072-CON | GAP-3163 |  | Read Module P3 as consumed by P3 rather than owned by P3; keep the build order in the notes. |

### OTHER:ADR-017 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14534 | RWB-PLT-E1072-CON | GAP-1620 |  | Record that the registry accepts XLS decision table and DMN 1.6 model as two package formats on one runtime, that a version names its format, and that conversion is a version change with its own test evidence. |

### OTHER:Lane document (CG-W0 and wave-1 lane rules) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14536 | RWB-PLT-E1072-CON | GAP-1218 |  | State that the platform CONs of the DP table are wave-0 prerequisites carried outside H for every wave-1 APP story. |

### OTHER:Work Package story line for the eleven-pattern secondary slice and build sequence step D1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14539 | RWB-PLT-E1072-CON | GAP-2488 |  | Name every added row in the pattern table and the fakes of 12.8. Let step D1 decide whether the seven H rows and four consumed contracts enter the dependency map. |

### OTHER:Work Package story line for the twelve-pattern secondary slice and build sequence step D1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14540 | RWB-PLT-E1072-CON | GAP-2496 |  | Name every added row in the pattern table and the fakes of 12.8. Let step D1 decide whether the eight H rows and four consumed contracts enter the dependency map. |

### RWB-S8-E2012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14541 | RWB-PLT-E1072-CON | GAP-3091 |  | Carry the eight platform H rows in section 13 as tracked. Keep Depends on (build) None and Ready to start Day 1. |

### OTHER:WP B2-P4-021 story line (RWB-P8 wave 2 story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14542 | RWB-PLT-E1072-CON | GAP-2312 |  | Keep the metadata rows as the WP fixes them. Carry the platform and rwb-case contracts as build-against dependencies in section 13. |

### OTHER:Build sequence document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14543 | RWB-PLT-E1072-CON | GAP-2410 |  | Record that a secondary slice builds against the platform contracts and published fakes, and reads same-service wave-1 rows through its own schema, within R5.7 rule 5. |

### RWB-S5-E4022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14549 | RWB-PLT-E1072-CON | GAP-2899 | 13 | Load the DISPOSAL package in force through the service template; add no H row for the platform rules kit in this slice; record the reading for the next pattern-set realignment. |

### RWB-S5-E4024-APP; RWB-S5-E4024-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14550 | RWB-PLT-E1072-CON | GAP-2910 | 13 | Load the DISPOSAL package in force through the service template; add no H row for the platform rules kit in this slice; record the reading for the next pattern-set realignment. |

### RWB-S5-E4025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14551 | RWB-PLT-E1072-CON | GAP-2917 | 13 | Load the DISPOSAL package in force; run the second-signature approval on the service's platform templates; add no H row for the rules kit; record the reading. |

### OTHER:Rules Engine Design v3, section 8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14552 | RWB-PLT-E1072-CON | GAP-2033 | n/a | State that 93 is the count of the target table set, and that the rule store's four tables (rule_package, rule_package_version, rule_row, rule_test_case) sit in schema rwb_decision; the distribution is RWB-PLT-NF06-DB split work. |

### OTHER:detcheck P2 field classification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15106 | RWB-PLT-N009-APP | DOR-RWB-PLT-N009-APP-11 | 12.7 | Class P2 fields as not personal data, as the story states none is carried (see 12.7 and TC-PLT-N009-APP-06). |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15311 | RWB-PLT-TE006-APP | DOR-RWB-PLT-TE006-APP-22 | Header | Publish a contract fake library version and record it as published. |

### OTHER:EA (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15312 | RWB-PLT-TE006-APP | GAP-0011 | Header | Hosting recorded as a recommendation only; confirmation and ACE capacity, naming, ACL, registry and environments remain with EA. |

### OTHER:RWB-E1-067 and the P1 ledger contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15330 | RWB-PLT-TE006-APP | GAP-0376 | 7 | P1 runs one consumer group across the three topics, accepts current and previous schema versions, dedupes on CloudEvents id, assigns case_seq under case lock, orders by occurredAt then case_seq, and reports cross-topic inversions; keep the legacy event-to-code map. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15332 | RWB-PLT-TE006-APP | GAP-1622 | find it | Add a contract version to the DecisionRecorded event, record it on decision_log_entry, and have the consumer accept a known set of versions and send an unknown one to the dead-letter topic. |

### OTHER:Information Flow v5 deck (slides 3 and 21) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15333 | RWB-PLT-TE006-APP | GAP-2107 | find it | Describe both Kafka roles: ACE PII topics for logging, unchanged; and the 19 business topics plus the shared rwb.decision-record.v1 ledger topic, with their own ACLs, retention and no personal data. |

### OTHER:TSD P2 v3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15334 | RWB-PLT-TE006-APP | GAP-1992 | find it | Remove outbox_event, outbox_delivery, processed_event, idempotency_key, feature_flag, feature_flag_change and efs_ledger_outcome from T3.1; keep the three P2 business tables; build platform tables once in the shared libraries (RWB-PLT-TE006-CON). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0004 | Drools packages missing for S1 and S3-S9 | RW-COE and architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0011 | Kafka hosting not confirmed | Enterprise Architecture and ACE platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0081 | Owner and table of the model version in force are not stated | ACE | Resolved (directive) |
| GAP-0130 | The values of ce_source and ce_subject are not stated | Solution architect | Resolved (directive) |
| GAP-0217 | LOV-REF-TABLE carries 25 table codes in v4 but the rwb-case reference-data contract fixes twelve | Reference data administrator | Resolved (directive) |
| GAP-0219 | Two services derive no starter row: S1 rwb-valuation and S7 rwb-writeoff | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0220 | No source states which lists a service needs at its first deployment | Data architecture team | Resolved (directive) |
| GAP-0221 | Four source lists are held in another service's table although the sheet calls every list Workbench-held | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0223 | Five reference-data rows name no table, and no message table exists in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0361 | Feature-flag owner, flag operations and the weekly report trigger move in the target | Platform lead | Resolved (directive) |
| GAP-0376 | The event-to-ledger map, the cross-topic ordering rule and the duplicate key after the split into per-service topics are not defined | Solution architect | Resolved (directive) |
| GAP-0382 | TE006 outbox slice: the case-event mapping, the retry and dead-letter values, and the consumer list per event type | Solution architect | Resolved (directive) |
| GAP-0544 | The reference versions, their rows and the lists of values are P3's, the rule rows and their test cases are P7's, and the legacy story names a reference data service that exists in no source | Solution architect | Resolved (directive) |
| GAP-0593 | The product code to product group map is reference data of rwb-case under DP-07, and the Work Package gives this story no reference-data contract dependency | Reference data administrator, P1 and P3 | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0614 | The screening slice in rwb-agent: the run-start path, the parameter and ledger operation paths, the two added events, the screening feature flag, the boundary status of a failed tool call and the route in front of the reads are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-source-data, rwb-deviation, rwb-case, rwb-document and rwb-decision | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0696 | Legacy AC2 and BR1 load DELEGATION_LIMIT through the reference-data service, but the Ownership Map keeps delegation_limit with P4 rwb-access | Solution architect | Resolved (directive) |
| GAP-0697 | The column definitions of each reference table code and the element types of the reference resources have no source field by field | Data steward | Resolved (directive) |
| GAP-0698 | The answer of a dated read with no version in force, and the rights of the verify and the rollback, are not stated | Solution architect | Resolved (directive) |
| GAP-0719 | FSD A2.16 reports reference-data changes while the legacy story and the test cases govern rule package versions | Business analyst | Resolved (directive) |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0822 | rwb-access rule-version load: the compile, the checks and the SIT scenario run need the Drools kit RWB-PLT-E1072-CON, which is not in this story's build list | Solution architect | Resolved (directive) |
| GAP-1147 | The reference lists the template screen needs have no contract row and no DP-07 in this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1215 | RWB-P6-E1073-APP: the DP-04 row of the pattern table names H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON while the plan gives no H and C RWB-P3-E1073-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1400 | The artefact coordinates of the helper, the error-map source, the header format and the ordering with the edge are not specified for the implementation | Platform library lead with the platform architect | Resolved (directive) |
| GAP-1401 | The published problem-detail schema, the error-map table source, the expiry window and the stored-response scope are not specified for the contract | Platform library contract owner with the message-catalogue owner | Resolved (directive) |
| GAP-1409 | Reference-data client artefact coordinates, the cache time-to-live catalog entry, the refresh rule with no change event and the client-to-kit boundary are not specified | Platform team (PLT) architect with the rwb-case and rwb-decision owners | Resolved (directive) |
| GAP-1410 | The published reference-data client contract, the version and row data contract, the LOV-REF-TABLE code list and the no-version failure surface are not specified in a technical specification | Platform team (PLT) contract owner with the rwb-case owner | Resolved (directive) |
| GAP-1411 | Platform feature-flag store, its schema name and the deployment of the admin component are not specified | Platform team (PLT) architect with the ACE DBA | Resolved (directive) |
| GAP-1412 | Feature-flag contract schemas, the schema names of the two PLT tables and the idempotency rule of the POST are not specified | Platform team (PLT) contract owner with the ACE DBA | Resolved (directive) |
| GAP-1413 | The rule-model fetch has no Ownership Map row, the shape of the fetched model is not specified, the RulePackageInForce subscriber list covers only four services, and the package format of phase 1 rests on a proposal | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1414 | The kit contract has no source for its artefact coordinates, for the error codes of a refused model fetch, and for the message prefix of a refusal that now belongs to rwb-decision | Solution architect | Resolved (directive) |
| GAP-1415 | The retry schedule, the JOB-11 sender and the ownership of the exception path are unresolved for the outbox library | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1417 | The baseline package registry, module list, baseline version and release artefacts are not specified | Solution architect | Resolved (directive) |
| GAP-1558 | The parameter and reference-data load interface is claimed by P4 in the API specification and by P3 in the default ruling | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1666 | The retry limit of an event and of a call is stated differently in the BRD and in Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1667 | The feature-flag store has an owner and a schema in the Ownership Map but no service row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1944 | The rule package in force is pushed to four services and not to rwb-asset, and DP-04 is not in the pattern set of this key | Solution architect and the rule owner in rwb-decision | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1947 | RWB-S6-E5023: the eligibility slice has no C row for its four consumed rows, no DP-04 row and no requirement id | Solution architect | Resolved (directive) |
| GAP-1992 | TSD P2 names platform tables and one P1 table as its own | Solution architect | Resolved (directive) |
| GAP-2025 | Rules engine design places Drools in the recovery module, Architecture v5 places it in each service | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2027 | RuleCatalog and the rule store are one interface in version 3 and two owners in the target | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2028 | Fact class of each package is named for the single module, not for a service | TechX (suggested; any team may pick up this story) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2029 | The model load path GET /rule-models/{n}/{v} is in the architecture and in no interface catalogue | TechX (suggested; any team may pick up this story) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2030 | Delivery ownership of E1-072 and E1-073 differs between the story set and the Ownership Map | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2032 | Decision-record write path and activity order change with ADR-022 | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2033 | The rule store is counted in one schema in version 3 and distributed over 19 schemas in the target | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2107 | Kafka has two roles in the deck and only one of them is named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2262 | CaseCreated payload and the resume of a held run are not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2439 | The physical columns of rule_package_version and the payload a compiled package is served in are not in the sources | TechX and the P7 solution architect | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2457 | The physical columns of rule_package, rule_package_version, rule_row and rule_test_case are not in any source | TechX and the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2568 | RWB-E1-013: the definition load of table measure_definition has no target operation, because the table is P9's while the reference-load framework is rwb-case's | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2652 | The reference set that holds the band, the floor and the freshness limit, and the operation that reads it, are not published | P3 rwb-case owner, with the P4 rwb-access owner confirming the superseded row | Resolved (directive) |
| GAP-2743 | The contract baseline of the notice step fixes three operations and two consumed calls whose notice and template ownership, operation names, case answer and requirement id no source states, and the D7.1 approval is declared without a decision on whether it gates the step | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and reference-data owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2748 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |
| GAP-2751 | The four consumed reads and the two handed-over operations of the pack carry no dependency row, and two of the operations have no published name | Solution architect, S4 rwb-litigation, with the P5 rwb-document, P3 rwb-case and P4 rwb-access architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2785 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |
| GAP-2797 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | P7 rwb-decision architect with the solution architect of S4 | Resolved (directive) |
| GAP-2801 | Four consumed surfaces of the appeal have no dependency row, and the plan carries no contract, integration or external dependency for either slice | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case, S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2899 | The step evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2910 | The round branch evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2917 | The step evaluates a DISPOSAL rule package and uses the approval template while neither carries a pattern row of this slice | Solution architect | Resolved (directive) |
| GAP-2924 | The step evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2930 | DP-04 sits outside the declared pattern set while the DISPOSAL package must still be evaluated | Solution architect | Resolved (directive) |
| GAP-2935 | The step evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2953 | The slice consumes an event and evaluates a rule package, while DP-09 and DP-04 are outside its pattern set and no platform build row is carried | S5 rwb-asset service owner with the platform event and workflow owners | Resolved (directive) |
| GAP-2973 | RWB-S6-E5023-APP: the eligibility slice has no plan row for its four consumed contracts, its outbox library, its rule kit, the 54 percent cap criterion or the two eligibility inputs | Solution architect | Resolved (directive) |
| GAP-3004 | RWB-S6-E6007-APP: the transfer slice has no plan row for its five consumed contracts or the buyer-file delivery, no outbox row although it publishes AccountsTransferred, no transfer operation and no column set to record the transfer | Solution architect | Resolved (directive) |
| GAP-3012 | RWB-S6-E6011-APP: the settle-and-cancel slice has no plan row for its six consumed contracts, its inbox library, its rule kit, its settlement stamp, its GL prerequisite or its EP06 wave | Solution architect | Resolved (directive) |
| GAP-3014 | RWB-S6-E5025: the masking rule set, the tape layout, the tape's storage reference, the PII service mapping and the six consumed contracts are given by no source and sit outside the plan's empty C row | Solution architect | Resolved (directive) |
| GAP-3016 | RWB-S7-E6013-APP: the scan slice has no plan row for its four consumed contracts, its rule kit, its ACE read, its inbox and its schedule, and no table or list of values holds the scan | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3021 | RWB-S7-E6015-APP: the pack slice has no plan row for its seven consumed contracts, its agent, outbox and rule-kit dependencies, its pack columns, its requirement id or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3023 | RWB-S7-E6016-APP: the removal slice has no published operation, no field or list for the removal reason, no plan row for its three consumed contracts, and no requirement id | Solution architect | Resolved (directive) |
| GAP-3025 | RWB-S7-E6017-APP: the routing slice has no plan row for its five consumed contracts, its rule kit, its event library, its meeting calendar, the operation it provides or the requirement it serves | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3041 | RWB-S7-E6025-APP: the closure slice has no plan row for its five consumed contracts, its rule kit, its event library, its scheduler marker, the retention period, the placement record or the closing amounts | Solution architect | Resolved (directive) |
| GAP-3053 | RWB-S8-E7002-APP: the X2 slice has no plan row for its four consumed contracts, its outbox library, its EFS touch, its requirement ids, its work-management owners or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3121 | RWB-S9-E7011-APP: the monthly scorecard has no rule row of its own, no trigger, no job, no workflow of its own, no published scorecard read and no reporting channel | Solution architect with the rwb-decision rule owner, the rwb-source-data owner and the platform scheduling owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3157 | The rule tables are described as recovery-schema tables but are owned by rwb-decision | P7 rule owner | Resolved (directive) |
| GAP-3161 | Feature flags are a P2 module table in the story and a platform library object in the Ownership Map | Platform lead | Resolved (directive) |
| GAP-3163 | The Temporal platform and the Drools runtime sit in a P3 module in the story and in platform epics in the split plan | Platform lead | Resolved (directive) |
| GAP-3167 | The number of Epic 1 rule packages is not reconciled with the phase 1 package list | P7 rule owner | Accepted (directive); not applied: value not in the source documents |
| GAP-3193 | The owner of the outbox admin endpoints after the split is not stated | TechX | Resolved (directive) |
| GAP-3232 | The story catalog carries 2,534 dependency rows while the story files carry 2,609 for the same 1,034 stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-PLT-E1047-APP | new AC without TC row | 387 | AC10 is new and no section 16 row covers it |
| RWB-PLT-E1047-APP | new AC without TC row | 387 | AC11 is new and no section 16 row covers it |
