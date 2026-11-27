# RWB-SVC-P8 rwb-payment (Payment) - review pack, part 1 of 3 (RWB-P8-DM013-APP to RWB-P8-E2008-OPS)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 5 |
| Resolved in the stories | 142 |
| Cross-document (pending in another document) | 213 |
| Not applied (value not in the sources) | 14 |
| Open business decisions | 12 |
| Register gaps linked | 108 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P8-DM013-APP | 10 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 DM013 APP Migrate money and closure v2.md |
| RWB-P8-E1001-APP | 34 | 52 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E1001 APP Recovery tables for the 14 data products v2.md |
| RWB-P8-E2008-APP | 47 | 46 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E2008 APP Payment matching with the missed payment event v2.md |
| RWB-P8-E2008-CON | 32 | 47 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E2008 CON Payment matching with the missed payment event - contract v2.md |
| RWB-P8-E2008-OPS | 19 | 53 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E2008 OPS Payment matching with the missed payment event - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P8-DM013-APP | R-11387 | CG-ALL-7489 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P8-E1001-APP | R-11393 | CG-ALL-7501 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P8-E2008-APP | R-11405 | CG-ALL-7521 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21843 | GAP-0001 | Register gap | Product Owner | Arch v5 waves have no release dates | Keep the dates unchanged and tentative, map waves 0-1 to Release 1 at the plan gate, and confirm the mapping in the verification loop |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21856 | GAP-0977 | Register gap | Data steward and data product owner (RW-DATASTEW) | The dictionary rows of the five rwb_access tables have no seeding owner after the split | Declare the 44 business rows as a build artefact of this story, hand the declaration to the one dictionary's seed in rwb_source_data, and let the seed carry the 35 standard-column rows under its own Field IDs. Cite the 44 business Field IDs only. |
| RWB-ITG-E2008-ITG, RWB-P1-E1015-APP, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22404 | GAP-0600 | Register gap | Solution architect with the P1 data product owner | FSD P1 A2.2 stamps a payment read on DP01 Account and arrears while the Work Package slice note names DP05, and no source states whether the read or the rwb-payment run answers a held business date | Hold both gates on DP01 Account and arrears and answer 409 with MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run, with no row of any kind; record DP05 as not the stamp of a payment read and correct the slice note in the Work Package and the data product map in the next version of FSD P1 A2.2; state in RWB-P8-E2008-CON that the run's own refusal for the business date is its own and that the read's 409 is the answer to a call made anyway. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22414 | GAP-1630 | Register gap | Finance and CFO delegate | The posting file has no layout, no schedule and no receiving ledger in any source | Fix one line per posting with case, account key, entry type, amount, value date, business date and posting reference, a manifest with count and checksum, and delivery through rwb-integration. Agree the layout with Finance and the ledger owner before wave 3. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22415 | GAP-1632 | Register gap | Business lead | A reversed payment has no product behaviour in the FSD although the routing rules require the case to reopen | Decide whether a reversal is in scope for this service. If it is, add a reversal source value, a reversal state on the proceeds record and an event that reopens the case through rwb-case. Until then the capability is out of scope and listed as an open question. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22416 | GAP-1633 | Register gap | Finance and CFO delegate | The fee tables that the fee feature reads are not defined anywhere | Name the fee table, its owner and its schedule, and hold the fee rate, the cap and the basis as versioned rows. Until then the fee calculation has no input and the feature cannot be tested. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-22419 | GAP-1636 | Register gap | Finance and CFO delegate | The order in which a receipt is applied to the balance is named but not specified | Hold the application order as versioned rows with an owner and a valid-from date, record the version on each proceeds row, and let Finance set the sequence before wave 3. |
| RWB-ITG-E2008-ITG, RWB-P1-E2008-APP, RWB-P4-E2008-APP, RWB-P7-E2008-APP, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E2008-OPS, RWB-S2-E2008-APP | R-28740 | GAP-1638 | Register gap | Product owner | The only success measure of the module has no baseline and no measurement definition | Take the measure from the decision log as the FSD says, and have the product owner set the baseline, the target and the definition of 'the same day' before the wave-2 release note. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P8-DM013-APP | R-06963 | DOR-RWB-P8-DM013-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources (03 Requirements, 23 Document Gaps, 05 API spec). Directive gives no sign-off. Header left as Not specified. |
| RWB-P8-E1001-APP | R-06968 | DOR-RWB-P8-E1001-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources. Grep found only scratch and queue files. Sign-off must be confirmed against the epic design record, which is not in the document set. |
| RWB-P8-E2008-APP | R-06976 | DOR-RWB-P8-E2008-APP-17 | find it | Definition of Ready item 17 Dependencies: Fail | Clears only when RWB-P8-E2008-OPS is done and CG-ALL-7511 is resolved. Both are states of other work, so no story text can resolve it. No edit made. |
| RWB-P8-E2008-APP | R-26465 | CG-ALL-7522 | 3, 3.1 | Flyway file V2_008__payment_matching.sql is not in the V0001..Vnnnn form | Migration line 353 is outside this chunk and is blank here. The Flyway sequence number was not found: a project grep for V2_008 and db/migration hit only the v2 Service Template Specification. No edit made. |
| RWB-P8-E2008-APP | R-28744 | GAP-2498 | find it | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept, and the legacy levels have no counterpart in the template | The Covers column, sections 1 and 16, the ten test case rows and the level mapping recorded in section 7 are not in this chunk, so no edit can be anchored. No edit made. |
| RWB-P8-E2008-CON | R-18249 | DOR-RWB-P8-E2008-CON-10 | 7, 16 | Definition of Ready item 10 Screens and states: Partial | Sections 7 and 16 are not in this chunk, so the empty, loading, error and no-access criteria and test rows cannot be anchored. Re-send both sections. |
| RWB-P8-E2008-CON | R-22408 | GAP-1348 | 11, 13 | RWB-E2-008: the proceeds field set and its idempotency tables disagree between the legacy story and TSD P8 T3.1 | Sections 11 and 13 are not in this chunk, so the legacy proceeds and idempotency text cannot be matched. Re-send both sections to apply the fix. |
| RWB-P8-E2008-CON | R-22409 | GAP-1350 | 9 | RWB-E2-008: the contract artefact names, the problem+json body, the MatchRequest shape and the registry mode of rwb-payment are not fixed by any source | Section 9 contract artefact text is not in this chunk, so the old text cannot be matched. Re-send section 9 to apply the OpenAPI, AsyncAPI and MatchRequest fix. |
| RWB-P8-E2008-CON | R-22410 | GAP-1352 | not in chunk | RWB-E2-008: the deployment targets, the tier sizes, the rollout strategy and the rollback procedure of rwb-payment have no source | Deployment, tier and rollout text is not in this chunk and the item names no section. Replica floor, ceiling and sizes are not specified in the source documents (GAP-1352). |
| RWB-P8-E2008-CON | R-26474 | CG-ALL-7545 | 3.1 | Flyway file V2_008__payment_matching.sql is not in the V0001..Vnnnn form | Migration name V2_008 is not in the story text (L298 is the event row). No Service Template Spec or Flyway sequence found in 03 folder; next number not in sources. |
| RWB-P8-E2008-OPS | R-18259 | DOR-RWB-P8-E2008-OPS-4 | 8 | Definition of Ready item 4 Business rules: Partial | Fix needs new AC rows in section 7 and test rows in section 16; neither is in this chunk. Resubmit with sections 7 and 16. Section 8 rules BR1 to BR10 were not changed. |
| RWB-P8-E2008-OPS | R-22408 | GAP-1348 | 11, 13 | RWB-E2-008: the proceeds field set and its idempotency tables disagree between the legacy story and TSD P8 T3.1 | Proceeds field set, ux_proceeds_payment_code index and migration name sit in sections 11 and 13, not in this chunk. Resubmit with those sections. |
| RWB-P8-E2008-OPS | R-22410 | GAP-1352 | not in chunk (deployment sections) | RWB-E2-008: the deployment targets, the tier sizes, the rollout strategy and the rollback procedure of rwb-payment have no source | Deployment sections are not in this chunk. Worker floor, ceiling, sizes and rollback window have no source value, so none were invented. Resubmit with the deployment sections. |
| RWB-P8-E2008-OPS | R-26481 | CG-ALL-7561 | 7 | Criteria and tests keep legacy job and decision-log wording | Section 12.5 already has no JOB-nn, decision log or job record wording. AC5 in section 7 (JOB-07 run view) is not in this chunk's story text, so it is unedited. Needs its own chunk. |

## 5. Cross-document changes (pending in the target document)


### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12847 | RWB-P8-DM013-APP | DOR-RWB-P8-DM013-APP-9 | 14 | Message texts now read Not specified rather than deferring to standard text |
| CDC-12850 | RWB-P8-DM013-APP | CG-ALL-7486 | 14 | MSG-P1-001 text marked Not specified in the source documents |
| CDC-12851 | RWB-P8-DM013-APP | CG-ALL-7487 | 14 | MSG-P1-012 text marked Not specified in the source documents |
| CDC-12920 | RWB-P8-E2008-APP | DOR-RWB-P8-E2008-APP-9 | 14 | Confirm the text of MSG-P3-027 against this standard and supply the standard text so section 14 can align it. |
| CDC-12944 | RWB-P8-E2008-APP | GAP-1637 |  | Publish wording, Thai text, channel and blocking flag for MSG-P8-001 and MSG-P8-002, and confirm whether MSG-P8-001 is a screen message, a run summary line or both. |
| CDC-12959 | RWB-P8-E2008-CON | CG-ALL-7538 | 4, 14 | Add a new message ID for 'A run summary carries unmatched payments' with the standard's text; the story then cites that ID in place of MSG-P8-001. |
| CDC-12960 | RWB-P8-E2008-CON | CG-ALL-7539 | 4, 14 | Add a new message ID for 'No PAYMENT_MATCH version is in force' with the standard's text; the story then cites that ID in place of MSG-P8-002. |
| CDC-12961 | RWB-P8-E2008-CON | CG-ALL-7540 | 4, 14 | Add a new message ID for 'The rule version is refused' with the standard's text; the story then cites that ID in place of MSG-P3-027. |
| CDC-12962 | RWB-P8-E2008-CON | CG-ALL-7541 | 4, 14 | Add a new message ID for 'The ACE batch is late or not complete' with the standard's text; the story then cites that ID in place of MSG-P1-001. |
| CDC-12963 | RWB-P8-E2008-CON | CG-ALL-7542 | 4, 14 | Add a new message ID for 'The role lacks the right' with the standard's text; the story then cites that ID in place of MSG-P4-002. |
| CDC-12968 | RWB-P8-E2008-CON | DOR-RWB-P8-E2008-CON-9 | 14 | English text column holds placeholders for all five IDs; no text is taken from the standard. |
| CDC-12994 | RWB-P8-E2008-CON | GAP-1637 | find it | Publish wording, Thai text, channel (screen, run summary or both) and blocking flag for MSG-P8-001 and MSG-P8-002. |
| CDC-13001 | RWB-P8-E2008-OPS | CG-ALL-7554 | 4, 14 | Add a new message ID for the text 'The ACE batch is late or not complete', then cite it in section 4 and section 14 in place of MSG-P1-001. |
| CDC-13002 | RWB-P8-E2008-OPS | CG-ALL-7555 | 4, 14 | Add a new message ID for the text 'The run summary carries unmatched payments', then cite it in sections 4 and 14 in place of MSG-P8-001. |
| CDC-13003 | RWB-P8-E2008-OPS | CG-ALL-7556 | 4, 14 | Add a new message ID for the text 'No PAYMENT_MATCH version is in force', then cite it in sections 4 and 14 in place of MSG-P8-002. |
| CDC-13004 | RWB-P8-E2008-OPS | CG-ALL-7557 | 4, 14 | Add a new message ID for the text 'The rule version is refused', then cite it in sections 4 and 14 in place of MSG-P3-027. |
| CDC-13005 | RWB-P8-E2008-OPS | CG-ALL-7558 | 4, 14 | Add a new message ID for the text 'The record cannot be written', then cite it in sections 4 and 14 in place of MSG-P7-003. |
| CDC-13008 | RWB-P8-E2008-OPS | DOR-RWB-P8-E2008-OPS-9 | 14 | Supply English text for MSG-P1-001, MSG-P8-001, MSG-P8-002, MSG-P3-027, MSG-P7-003 and resolve the meaning clash with the standard |
| CDC-13043 | RWB-P8-E2008-OPS | GAP-1637 | — | Add MSG-P8-001 and MSG-P8-002 with Thai wording, channel (screen, run summary or both) and blocking flag; the story keeps the IDs. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12840 | RWB-P8-DM013-APP | CG-ALL-7484 | 8; 11 | Add account_payment_id (ACE payment identifier) to LDM v9 Fields, or record the object in the owning document. |
| CDC-12841 | RWB-P8-DM013-APP | CG-ALL-7485 | 11; 12 | Record flyway_schema_history as the Flyway-managed table in rwb_payment in LDM v9, or in the owning document. |
| CDC-12849 | RWB-P8-DM013-APP | GAP-2533 | 3, 4 | Add a provenance column and a migration-date column to proceeds; settle the account_payment_id fill with the baseline owner; record DP-15 in the split plan. |
| CDC-12875 | RWB-P8-E1001-APP | GAP-2401 |  | Entity sheet: rule_row 21 fields; drop rule_test_case.package_version_id; approval case_id and delegation_limit_id as values with no foreign key; keep five rwb_decision foreign keys. |
| CDC-12943 | RWB-P8-E2008-APP | GAP-0927 |  | Carry the filter and row count in the actions list of the decision-record entry; add the capability area and the right to the same list in the next LDM version. |
| CDC-12954 | RWB-P8-E2008-CON | CG-ALL-7530 | 4, 12.7 | Add the decision_record library table (created in rwb_payment by RWB-PLT-E1027-CON) to Fields, or record it in RWB-PLT-E1027-CON. |
| CDC-12955 | RWB-P8-E2008-CON | CG-ALL-7531 | 4, 12.4, 12.7 | Add the inbox_event library table (created in rwb_payment by RWB-PLT-E1027-CON or DP-09 owner) to Fields, or record it in the owning document. |
| CDC-12956 | RWB-P8-E2008-CON | CG-ALL-7532 | 11, 12.7 | Record account_payment_id as a field or name the object (index, library table or flag) in LDM v9, or the story uses the dictionary name. |
| CDC-12957 | RWB-P8-E2008-CON | CG-ALL-7533 | 12.7 | Record consumer_group as a field or name the object (index, library table or flag) in LDM v9, or the story uses the dictionary name. |
| CDC-12958 | RWB-P8-E2008-CON | CG-ALL-7534 | 12.7 | Record payment_missed_event_key as a field or name the object (index, library table or flag) in LDM v9, or the story uses the dictionary name. |
| CDC-12982 | RWB-P8-E2008-CON | GAP-1634 | 11 | DF-FIN row reverted to account_payment_id pending the owning document |
| CDC-12992 | RWB-P8-E2008-CON | GAP-0927 | find it | Carry filter and row count in the actions list of the decision-record entry; add capability area and right to the same list in the next LDM version. |
| CDC-13000 | RWB-P8-E2008-OPS | CG-ALL-7551 | 12.7 | Record inbox_event as the PLT library table in rwb_payment (section 12.7 of this story), or give its dictionary name; no entity of that name exists in LDM v9 or Data Classification v5. |
| CDC-13041 | RWB-P8-E2008-OPS | GAP-0927 | — | Carry filter and row count in the actions list of the decision-record entry; add capability area and right to the same list in the next LDM version. |

### RWB-P8-E2008-CON (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12838 | RWB-P8-DM013-APP | DOR-RWB-P8-DM013-APP-21 |  | Contract dependency named as RWB-P8-E2008-CON, the existing payment contract story |
| CDC-12907 | RWB-P8-E2008-APP | DOR-RWB-P8-E2008-APP-21 | header | Build status moves from Not started to Done. |
| CDC-12927 | RWB-P8-E2008-APP | GAP-0599 | 12.1 | Publish the two operations on /api/recovery/source-data/v1 with resource names, businessDate query parameter, element names and the status set of section 12.1. |
| CDC-12938 | RWB-P8-E2008-APP | GAP-2693 |  | Serve plan position from TSD columns; apply ProceedsMatched and PaymentMissed via inbox as applyProceedsMatched and holdMissedInstallment; confirm package and frequency at contract freeze. |
| CDC-12939 | RWB-P8-E2008-APP | GAP-1347 | 3 | Publish the three event schemas (rwb.payment.TreatmentBooked.v1, PaymentMissed.v1, ProceedsMatched.v1) with the data fields the legacy story names: PaymentMissed treatmentId, dueDate, amountDue; ProceedsMatched proceedsId, caseId, amount; TreatmentBooked fields Not specified in the source documents (GAP-1347). Use the platform CloudEvents envelope, keep the decision-record element with its library owner, and require a new schema version for any added business field. |
| CDC-12998 | RWB-P8-E2008-OPS | DOR-RWB-P8-E2008-OPS-21 | header | Set the build status to Done with the contract published; it is currently Not started. |
| CDC-12999 | RWB-P8-E2008-OPS | DOR-RWB-P8-E2008-OPS-22 | header | Publish a contract fake library version and record its version number; none is recorded now. |
| CDC-13017 | RWB-P8-E2008-OPS | GAP-0601 |  | Name the paymentCode ascending order and the one-row-per-payment_code fold rule in the OpenAPI fragment and RWB-P8-E2008-CON; record the cap-exceeded answer in the next API Specification version. |
| CDC-13030 | RWB-P8-E2008-OPS | GAP-2494 |  | Fix one DecisionRecorded shape and one consumer group. Take decision codes from LOV-DECISION. Carry inputs_ref as an opaque reference. Keep the input age limit key as a placeholder read through DP-06. Publish the read page default with the read. |
| CDC-13031 | RWB-P8-E2008-OPS | GAP-2504 |  | Publish v1 with the two operations, three event schemas, nine declarations, schema baseline and message map. Mark unsettled elements with the placeholder and one review row. Gate the tag on contract tests and schema lint. |
| CDC-13033 | RWB-P8-E2008-OPS | GAP-1347 | 12.4 | Publish the three event schemas (TreatmentBooked, PaymentMissed, ProceedsMatched) with the data fields the legacy story names per event and the platform CloudEvents envelope; keep the decision-record element with its library owner; require a new schema version for any added business field. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12846 | RWB-P8-DM013-APP | DOR-RWB-P8-DM013-APP-7 | 11 | Add account_payment_id (field on proceeds) and flyway_schema_history (the P1 library history entity in rwb_payment) as fields or entities. |
| CDC-12854 | RWB-P8-E1001-APP | CG-ALL-7491 | 4, 8, 11, 13 | Add or map account_payment_id (uuid value on proceeds, BR5) under its dictionary name, or record the ACE payment object it refers to. |
| CDC-12857 | RWB-P8-E1001-APP | DOR-RWB-P8-E1001-APP-7 | 11 | Register account_payment_id, account_payment, inbox_event and decision_record as fields or entities, as used in RWB-P8-E1001-APP sections 8 and 11. |
| CDC-12909 | RWB-P8-E2008-APP | CG-ALL-7506 | 3, 11, 12.7 | Record payment_missed_event_key in the owning document (index, library table or flag), or align the story to its dictionary name. |
| CDC-12910 | RWB-P8-E2008-APP | CG-ALL-7507 | 3, 11, 12.7 | Record account_payment_id in the owning document (index, library table or flag), or align the story to its dictionary name. |
| CDC-12911 | RWB-P8-E2008-APP | CG-ALL-7508 | 11, 12.7 | Record decision_record in the owning document (index, library table or flag), or align the story to its dictionary name. |
| CDC-12912 | RWB-P8-E2008-APP | CG-ALL-7509 | 11, 12.4, 12.7 | Record inbox_event in the owning document (index, library table or flag), or align the story to its dictionary name. |
| CDC-12913 | RWB-P8-E2008-APP | CG-ALL-7510 | 12.7 | Record account_payment in the owning document (index, library table or flag), or align the story to its dictionary name. |
| CDC-12919 | RWB-P8-E2008-APP | DOR-RWB-P8-E2008-APP-7 | 11 | Add the entities or fields payment_missed_event_key, account_payment_id, decision_record, inbox_event and the three further detcheck names, or confirm them as library objects. Story side now states their status. |
| CDC-12967 | RWB-P8-E2008-CON | DOR-RWB-P8-E2008-CON-7 | 11 | Register decision_record, inbox_event, account_payment_id, consumer_group and the one further name flagged by detcheck |
| CDC-13007 | RWB-P8-E2008-OPS | DOR-RWB-P8-E2008-OPS-7 | 11 | Confirm decision_record and inbox_event as LDM entities or fields, or rename the section 12.7 library rows; BR Field ID column added to section 11 as placeholders |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12862 | RWB-P8-E1001-APP | GAP-0107 | find it | Derive the 48 cuts from sheet Tables: keep a foreign key only when both tables share an owner, otherwise the column stays uuid. Record the 48 rows in the README and the ERD. |
| CDC-12863 | RWB-P8-E1001-APP | GAP-0109 | find it | Replace schema 'platform' on the six PLT rows: outbox_event, outbox_delivery, processed_event and idempotency_key go to each service schema with no business foreign key; feature_flag and feature_flag_change go once to rwb_integration.sql for the admin API. |
| CDC-12864 | RWB-P8-E1001-APP | GAP-0206 | find it | Cut the 48 table-to-table FKs to business-key columns, keep the 11 ACE view references, show all three cases per row, and fill the FK cuts sheet. |
| CDC-12869 | RWB-P8-E1001-APP | GAP-0228 | find it | Record S1 as DP11 owner; add rwb_valuation rows (valuation, route decision, route agent output) at the Ownership Map's next revision. |
| CDC-12885 | RWB-P8-E1001-APP | GAP-0108 | none | Write rwb_valuation.sql with schema, platform library objects and a note; read ACE through rwb-source-data contract until a TSD adds a local table. |
| CDC-12887 | RWB-P8-E1001-APP | GAP-0114 | none | Keep lake_copy_watermark DDL in rwb_source_data.sql with a retirement note; P1 DB story drops it. |
| CDC-12890 | RWB-P8-E1001-APP | GAP-0202 |  | Add a Views sheet listing the 30 recovery.v_ace_* views with owning service P1 and target schema 'recovery (ACE, read-only view)', taken from Architecture v5. |
| CDC-12966 | RWB-P8-E2008-CON | DOR-RWB-P8-E2008-CON-24 | 12.4 | Producer service column added to the 12.4 table from the event names; owner column holds the placeholder. |
| CDC-12989 | RWB-P8-E2008-CON | GAP-1639 | find it | Removed the claim that the story names both workflows; JOB-07 name is Not specified. |

### OTHER:FSD P8 v3 (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12926 | RWB-P8-E2008-APP | GAP-1631 | find it | Read ALS through the rwb-source-data contract, route ledger postings through rwb-integration, and treat ATS, AMIS and LED routes as outside the 19 services. |
| CDC-12935 | RWB-P8-E2008-APP | GAP-1635 |  | A2.11.2: reconcile FEAT-PAY-11 to the ACE payment and account position and the posting file; ledger position as an open question until the ledger publishes a return. |
| CDC-12980 | RWB-P8-E2008-CON | GAP-1627 | 7 | In AC-EXC-P8-001-02 and AC-EXC-P8-002-02, replace the data quality exception list with a break row on the rwb-source-data reconciliation break list, check name References. Confirm the name with the data steward. |
| CDC-12981 | RWB-P8-E2008-CON | GAP-1629 |  | In A1.2 move FEAT-PAY-06 first release from E4 to E3 (wave 2, EP03) so booking confirmation ships with the booking. |
| CDC-12983 | RWB-P8-E2008-CON | GAP-1635 | 7 | In A2.11.2 replace the 'ALS and GL' integration points with the ACE payment and account position and the posting file delivered. Record a ledger return as an open question until the ledger owner publishes one. |
| CDC-12984 | RWB-P8-E2008-CON | GAP-1640 | 7 | In AC-BG-P8-001-01 keep one run per business date and record the payment-received same-day trigger as an open question. Add an intraday run only when an interface carrying payments during the day is named. |
| CDC-13016 | RWB-P8-E2008-OPS | GAP-1631 | find it | Replace ALS, GL, ATS and AMIS interface points with rwb-source-data reads and rwb-integration postings; auto-debit and LED outside the 19 services |
| CDC-13026 | RWB-P8-E2008-OPS | GAP-1635 |  | In A2.11.2, reconcile FEAT-PAY-11 to the ACE payment and account position and the posting file delivered. Add a ledger return and an open question only if the ledger owner publishes one. |
| CDC-13027 | RWB-P8-E2008-OPS | GAP-1640 |  | Keep one matching run per business date in wave 2. Record the payment-received same-day trigger as an open question. Add an intraday run only when an interface carrying payments intraday is named. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12842 | RWB-P8-DM013-APP | CG-ALL-7488 | 16 | Add rows TC-DM-013-01 to TC-DM-013-04 to the next Test Cases version, with Given, When and Then copied from the criteria they cover. |
| CDC-12845 | RWB-P8-DM013-APP | DOR-RWB-P8-DM013-APP-12 | 16 | Add TC-DM-013-01 to TC-DM-013-04, and TC-DM-013-05 to TC-DM-013-07 (added by this story for AC7 to AC9), as test case rows. |
| CDC-12855 | RWB-P8-E1001-APP | CG-ALL-7498 | 16 | Add a row TC-E1-001-12 with Given, When and Then copied from the AC6, AC8 and BR1 criteria it covers. |
| CDC-12880 | RWB-P8-E1001-APP | CG-ALL-7499 | 16 | Covers kept on this story's scenario numbers |
| CDC-12987 | RWB-P8-E2008-CON | CG-ALL-7543 | 16 | Add rows for TC-P8-E2008-CON-01 to TC-P8-E2008-CON-08 under Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-13035 | RWB-P8-E2008-OPS | CG-ALL-7559 | 16 | Add rows for TC-P8-E2008-OPS-01 to TC-P8-E2008-OPS-07 under Story test cases, with Given, When and Then copied from AC1 to AC7 of RWB-P8-E2008-OPS. |

### RWB-P8-E2008-APP (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12940 | RWB-P8-E2008-APP | GAP-0604 | 3 | RWB-P3-E1043-CON is already in this story's Contract dependencies row. Keep the gap open until it is published. Confirm whether the data product list and source-system list are rwb-case reference data or this service's own data_product rows, and record the ruling in the Ownership Map and FSD P1 data product section. |
| CDC-13011 | RWB-P8-E2008-OPS | GAP-2503 | find it | Workflow name is not set in the story (see R-01918). |
| CDC-13012 | RWB-P8-E2008-OPS | GAP-1346 | find it | Name the seven consumed rows in section 12.2 with the placeholder, and have the solution architect confirm the scope of the named P3 and P7 contracts |
| CDC-13023 | RWB-P8-E2008-OPS | GAP-1354 |  | Reallocate AC1, AC3, AC4 and AC5 to RWB-P8-E2008-APP in the next split plan revision, or add a coverage note to the epic overview. |
| CDC-13032 | RWB-P8-E2008-OPS | GAP-2693 |  | Build the plan position from TSD columns. Apply ProceedsMatched and PaymentMissed through the inbox. Name activities applyProceedsMatched and holdMissedInstallment. Serve the position in API-S2-002. Confirm package and frequency at contract freeze. |
| CDC-13047 | RWB-P8-E2008-OPS | GAP-2498 | — | Keep TC-E2-008-01 to -10 in WP order with Covers naming the slice criteria; map System to Component and Access to Contract per R7.2; leave legacy criteria with owning slices and RWB-ITG-E2008-ITG. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12881 | RWB-P8-E1001-APP | CG-ALL-7500 | 18 | Align the REQ-RDF-001 and REQ-RDF-014 test lists with this story's s18 IDs; remove or keep other-story IDs only where those stories own the test. |
| CDC-12918 | RWB-P8-E2008-APP | DOR-RWB-P8-E2008-APP-12 | 16 | Confirm the test lists of REQ-CHO-007 and REQ-CHO-009 against the test case IDs in section 16 of RWB-P8-E2008-APP (TC-E2-008-02 to -18). |
| CDC-12941 | RWB-P8-E2008-APP | CG-ALL-7520 | 18 | Align the test lists for REQ-CHO-007 (story TC-E2-008-02, TC-E2-008-06) and REQ-CHO-009 (story TC-E2-008-07, TC-E2-008-08, TC-E2-008-09) with the RTM rows in its next version, or align §18 to the RTM. |
| CDC-12988 | RWB-P8-E2008-CON | CG-ALL-7544 | 18 | Align the test lists for REQ-CHO-007 and REQ-CHO-009 to RWB-P8-E2008-CON section 18 (REQ-CHO-007: -03, -04; REQ-CHO-009: -01, -05, -08). |
| CDC-13036 | RWB-P8-E2008-OPS | CG-ALL-7560 | 18 | In the next RTM version, align the test lists of REQ-CHO-007 and REQ-CHO-009 with section 18 of RWB-P8-E2008-OPS. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12905 | RWB-P8-E2008-APP | CG-ALL-7514 | 12.5 | Add a Workflows row for the JOB-07 workflow of rwb-payment on queue rwb-payment, or confirm its catalogued name so the story uses it. |
| CDC-12950 | RWB-P8-E2008-CON | CG-ALL-7536 | 12.5 | Name the event-started workflow of JOB-07 (matchPayments) in the Workflows sheet; the row is still the placeholder (GAP-0144; ASM-0225). Story text unchanged. |
| CDC-12951 | RWB-P8-E2008-CON | CG-ALL-7537 | 12.5 | Name the event-started workflow of JOB-08 (confirmBookings) in the Workflows sheet; the row is still the placeholder (GAP-0144; ASM-0225). Story text unchanged. |
| CDC-12953 | RWB-P8-E2008-CON | DOR-RWB-P8-E2008-CON-8 | 12.5 | Name the JOB-07 and JOB-08 event-started workflows in the Workflows sheet so both story workflows are catalogued (GAP-0144; ASM-0225). |
| CDC-13038 | RWB-P8-E2008-OPS | GAP-1639 | 12.5 | Workflow names replaced by placeholders in the Object and workflow tables |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12914 | RWB-P8-E2008-APP | CG-ALL-7515 | 12.5 | Add activity readFacts to the Activities sheet, or use a catalogued activity. |
| CDC-12915 | RWB-P8-E2008-APP | CG-ALL-7516 | 12.5 | Add activity evaluateMatch to the Activities sheet, or use a catalogued activity. |
| CDC-12916 | RWB-P8-E2008-APP | CG-ALL-7517 | 12.5 | Add activity recordAndApply to the Activities sheet, or use a catalogued activity. |
| CDC-12917 | RWB-P8-E2008-APP | CG-ALL-7518 | 12.5 | Add activity raiseMissedPayment to the Activities sheet, or use a catalogued activity. |

### RWB-P1-E1001-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12852 | RWB-P8-E1001-APP | Definition of Ready item 22 Fake published: Fail | Header | The story now runs tests through the rwb-source-data contract fake; its version and publication belong to RWB-P1-E1001-APP. |
| CDC-12859 | RWB-P8-E1001-APP | GAP-0557 | find it | Adopt the five wave 1 assumptions: keep the built baseline as built; create P1's 13 own tables in rwb_source_data from the split migration; name schema and login rwb_source_data; leave the four extension tables to RWB-P1-E1069-DB while seeding their 49 dictionary fields; keep catalog, dictionary and v_data_dictionary in rwb_source_data with no REST operation added here. |
| CDC-12876 | RWB-P8-E1001-APP | GAP-2539 | 18 | Under a new catalog version, correct the DP13 row to name ACE for the money facts and the Workbench for the match, as one product with one row. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12903 | RWB-P8-E1001-APP | GAP-2062 |  | Use 12 partitions, RF 3 and 7 days retention as the default for each topic until RWB-PLT-EVT sets it per service. Record the open point in the change table. |
| CDC-13015 | RWB-P8-E2008-OPS | GAP-1626 | find it | Replace the slide 17 pair with API Specification v4 GET /proceeds and POST /proceeds/{proceedsId}/match; confirm before contract closure |
| CDC-13049 | RWB-P8-E2008-OPS | GAP-1349 | find it | Slide 17 IN line: answer the case payment list through GET /proceeds with case scope and publish no extra operation. Slide 44 JOB-07: read the run view from the edge contract. Story already names matchPayments and four activities. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12906 | RWB-P8-E2008-APP | DOR-RWB-P8-E2008-APP-14 | header | Record the signed epic design sign-off. |
| CDC-12952 | RWB-P8-E2008-CON | DOR-RWB-P8-E2008-CON-14 | header | Record the signed epic design sign-off for the epic of RWB-P8-E2008-CON. |
| CDC-12997 | RWB-P8-E2008-OPS | DOR-RWB-P8-E2008-OPS-14 | header | Record the signed epic design sign-off for RWB-P8-E2008-OPS against service epic RWB-SVC-P8. |

### RWB-P4-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12929 | RWB-P8-E2008-APP | GAP-0925 | n/a | Extend the envelope with area, right, scope, resource, filter, rowCount and matrixVersion; fix the three answer codes at the wave 2 contract review. |
| CDC-12977 | RWB-P8-E2008-CON | GAP-0925 | 9 | Extend envelope with area, right, scope, resource, filter, rowCount and matrixVersion; fix answer codes allow, refuse by right and refuse by scope at wave 2 contract review. |
| CDC-13020 | RWB-P8-E2008-OPS | GAP-0925 |  | Extend the envelope with area, right, scope, resource, filter, rowCount and matrixVersion, and fix the three answer codes (allow, refuse by right, refuse by scope) at the wave 2 contract review. |

### OTHER:NFR Spec v3 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12936 | RWB-P8-E2008-APP | GAP-1643 |  | Add a receipts-per-business-date volume from the receipt-to-installment ratio on ACE busy-month data, marked as an assumption until the number is set. |
| CDC-12985 | RWB-P8-E2008-CON | GAP-1643 | 16 | State a receipts-per-business-date volume in the next NFR version. Until then the volume test uses the receipt-to-installment ratio as an assumption; the ratio is not specified in the source documents (GAP-1643). |
| CDC-13028 | RWB-P8-E2008-OPS | GAP-1643 |  | State the receipt-to-installment ratio observed on ACE data for a busy month in the next NFR version. Until then the volume test uses that ratio as an assumption. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12946 | RWB-P8-E2008-APP | GAP-2495 |  | Publish the dry run as a read-only operation returning testResult with total, passed, failed, failing case IDs, per-case expected and actual results and recorded dry-run counts. |
| CDC-12990 | RWB-P8-E2008-CON | GAP-0602 | find it | Record the GET /accounts/{id} resource of Architecture v5 slide 15 as unowned and unpublished; keep nextInstallmentDate on the installment-facts read. |
| CDC-13039 | RWB-P8-E2008-OPS | GAP-0602 | 12.2 | Record GET /accounts/{id} from Architecture v5 slide 15 as unowned and unpublished; keep nextInstallmentDate on the installment-facts read. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12844 | RWB-P8-DM013-APP | DOR-RWB-P8-DM013-APP-11 |  | Reconcile the personal-data class of the proceeds fields with the story's statement that no personal data is carried. |
| CDC-12856 | RWB-P8-E1001-APP | DOR-RWB-P8-E1001-APP-11 | 11 | Confirm the personal-data class of proceeds fields (account_payment_id, case_id, treatment_id, source, amount, received_date, matched_to, posting_ref); the story states none is carried. Not specified in the source documents for which field. |

### 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12878 | RWB-P8-E1001-APP | GAP-0285 |  | Add one cut table (built schema table to rwb_* schema, baseline migration, data move order) and cite it from RWB-PLT-NF06-DB and each per-service DB story. |
| CDC-12886 | RWB-P8-E1001-APP | GAP-0112 | none | Define per-service Flyway sequence: one V0001 baseline per service schema; view file follows source V0002 and V0003 sections. |

### OTHER:ERD v5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12888 | RWB-P8-E1001-APP | GAP-0115 | none | Draw 108 v5 references unchanged; state sys_fields.object_name to sys_objects and sys_objects.data_product to data_product separately in the reconciliation table. |
| CDC-12889 | RWB-P8-E1001-APP | GAP-0116 |  | Group the v5 objects by the Ownership Map owner and add a cross-service reference table; keep the data-product table of v5 as section 3. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12921 | RWB-P8-E2008-APP | GAP-3175 | find it | List LoadCompleted as the legacy alias of AceDataReady (EV-26) on rwb.source-data.events.v1. Story already uses AceDataReady. |
| CDC-13009 | RWB-P8-E2008-OPS | GAP-3175 | find it | List AceDataReady (EV-26) as the target name on rwb.source-data.events.v1 with LoadCompleted as its legacy alias |

### OTHER:FSD P8 v3 (A2.10; OTHER:A2.11; OTHER:A2.17) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12924 | RWB-P8-E2008-APP | GAP-1703 | find it | Rewrite A2.10, A2.11 and A2.17 so rwb-payment owns booking, matching and posting; this service records the TreatmentBooked reference and the PaymentMissed break. |
| CDC-13013 | RWB-P8-E2008-OPS | GAP-1703 | find it | Record the booking reference from TreatmentBooked and the break from PaymentMissed; rwb-payment owns booking, matching and posting |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12925 | RWB-P8-E2008-APP | GAP-1625 | find it | Replace placeholder ACs AC-P8-003-01 to AC-P8-011-01 with testable criteria marked new; FSD owner confirms before wave 3 system test. |
| CDC-13014 | RWB-P8-E2008-OPS | GAP-1625 | find it | Write testable main-flow criteria for AC-P8-003-01 to AC-P8-011-01 marked new; FSD owner confirms before wave 3 system test |

### OTHER:Payment matching integration harness pack (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12930 | RWB-P8-E2008-APP | GAP-0393 | 15 | Record the composite proceeds and exception route path and merge order, harness environment, ALS fixture format, seed pack, evidence format, retention and pass or fail gate. |
| CDC-13021 | RWB-P8-E2008-OPS | GAP-0393 |  | Record the composite proceeds and exception route path and merge order, harness environment, ALS fixture format, seed pack, evidence format, retention and pass/fail gate at the wave 2 entry check. |

### RWB-P8-E2008-OPS (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12931 | RWB-P8-E2008-APP | GAP-1352 | n/a | Set worker floor and ceiling, tier sizes, topic partitions and retention, environment gates, PROD rollout step, release approvers and rollback procedure. |
| CDC-12937 | RWB-P8-E2008-APP | GAP-2505 |  | Set login secret reference, replica counts, partition and retention, alert thresholds, aggregation window, backfill limit and build ID policy as environment values; review five runbook entries with on-call before promotion. |

### OTHER:WP B-P8-01 split plan (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12932 | RWB-P8-E2008-APP | GAP-1354 | n/a | Reallocate AC1, AC3, AC4 and AC5 to RWB-P8-E2008-APP in the next revision of the split plan, or add a coverage note to the epic overview. |
| CDC-12979 | RWB-P8-E2008-CON | GAP-1354 | 7 | Reallocate AC1, AC3, AC4 and AC5 to RWB-P8-E2008-APP in the next revision, or add a coverage note to the epic overview. |

### OTHER:TSD P8 v2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12934 | RWB-P8-E2008-APP | GAP-1634 |  | Define account_payment_id as one varchar(255) business-key column holding ACE payment_code with no foreign key; remove the uuid CROSS_REF to account_payment (T3.1, T3.3). |
| CDC-13025 | RWB-P8-E2008-OPS | GAP-1634 |  | Drop the account_payment_id CROSS_REF uuid (T3.1 DF-FIN-004, T3.3). Keep one varchar(255) business-key column paymentCode holding the ACE payment_code, with no foreign key. |

### OTHER:Platform secret store (ACE team allocation) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12947 | RWB-P8-E2008-APP | GAP-2497 |  | Allocate the rwb-decision login on schema rwb_decision and record it in the platform secret store. The story keeps the phrase until then. |
| CDC-13046 | RWB-P8-E2008-OPS | GAP-2497 | — | ACE team allocates the rwb-decision login with schema rwb_decision and records it in the platform secret store. |

### RWB-P6-E1073-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12971 | RWB-P8-E2008-CON | GAP-2395 | find it | Read the three package codes and version labels through the contract as the fixture set; prove AC1 and AC5; settle rwb-comms package assignment with the rule registry owner before integration |
| CDC-13010 | RWB-P8-E2008-OPS | GAP-2395 | find it | Use the three Epic 2 package codes and version labels as the fixture set; settle the rwb-comms package assignment with the rule registry owner |

### RWB-P8-E2008-APP; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12991 | RWB-P8-E2008-CON | GAP-0603 | find it | Record the payment-matching run of rwb-payment (workload identity token) as caller and its operator in the authority table; correct the P8-to-P1 activity to one REST hop. |
| CDC-13040 | RWB-P8-E2008-OPS | GAP-0603 | — | Record the payment-matching run's workload identity as caller of both reads in the authority table; record the P8 to P1 step as one REST hop wrapped by the run's Temporal activity; correct the catalogue activity description. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12839 | RWB-P8-DM013-APP | DOR-RWB-P8-DM013-APP-22 | header | Record the published contract fake library version this story builds against. |

### OTHER:SCR-45 screen spec (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12843 | RWB-P8-DM013-APP | DOR-RWB-P8-DM013-APP-10 |  | Specify the empty, loading, error and no access states for SCR-45. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12848 | RWB-P8-DM013-APP | GAP-2178 | 3, 19 | Status changed from Resolved to Cross-document; owner, source and sign-off place stated, format left as Not specified |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:39; OTHER:47; OTHER:ACE database capacity) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12853 | RWB-P8-E1001-APP | GAP-0012 | find it | Create the 19 schemas and logins on the ACE PostgreSQL server in wave 0 and set and record the connection cap per login with the ACE DBA. |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12858 | RWB-P8-E1001-APP | GAP-0566 | find it | Publish the three read operations with response fields and problem body in RWB-P1-E1069-CON. Record that view SQL, helper functions and conformance test are the application slice, the login, grants, view owner and four extension tables the database slice, and the 19-login proof the wave 1 integration slice. |

### RWB-P4-E1001-APP; RWB-P4-E1037-APP; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12860 | RWB-P8-E1001-APP | GAP-0975 | find it | Confirm the DDL, keys, indexes and migration of the five rwb_access tables belong to RWB-P4-E1001-APP. Read sibling 'rwb_access baseline' references as the version that story applies. RWB-P4-E1037-CON keeps the contract stub and creates no table. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12861 | RWB-P8-E1001-APP | GAP-0100 | find it | List each operation under its owning service and its Architecture v5 base path. Leave the final operation path and payload to API Specification v5. |

### OTHER:Mapping sheet of v4 workbook; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12865 | RWB-P8-E1001-APP | GAP-0210 | find it | Keep the 11 ACE entity names; give each rwb_source_data schema and owner P1 via the rwb-source-data contract; add the four extension tables as Workbench targets at next revision. |

### OTHER:v4 Mapping sheet and ACE gaps sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12866 | RWB-P8-E1001-APP | GAP-0211 | find it | Add 'Target schema' and 'Owning service' columns, one value per row from Ownership Map Tables; keep columns A to N unchanged. |

### OTHER:Data products workbook v3 (Ownership and Ownership split sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12867 | RWB-P8-E1001-APP | GAP-0224 | find it | Add 'Owning service (D-RCV-60)', 'Owning schema (D-RCV-60)' and 'Basis (D-RCV-60)' columns after K; one owner per product from Ownership Map. |

### OTHER:Data products workbook v4 (Ownership sheet; OTHER:DP04 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12868 | RWB-P8-E1001-APP | GAP-0225 | find it | Keep DP04 whole, record S2 as owner of the live record, name S3 and P1 in the basis cell; split DP04 at next LDM revision if wanted. |

### OTHER:Per-service DB stories and wave-1 integration run (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12870 | RWB-P8-E1001-APP | GAP-0333 | find it | Each service DB story assigns its operational objects to its schema; integration run records the 24 objects as an open list and does not fail on them. |

### OTHER:TSD P4 v3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12871 | RWB-P8-E1001-APP | GAP-0976 | find it | Fix rwb_access at the five authority tables; treat the TSD declarations of lov_value, partner_user and rule tables as the monolith module view, superseded by ownership rulings. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:TSD P7 v2 (T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12872 | RWB-P8-E1001-APP | GAP-1280 | find it | Build rule_row with its 21 fields; drop rule_test_case.package_version_id; keep approval.case_id and delegation_limit_id as plain values; correct the three sources next version. |

### OTHER:Functional specification P1 field catalogues (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12873 | RWB-P8-E1001-APP | GAP-1512 | find it | Carry field lists for data_contract, dp_treatment, dp_guarantee_claim and efs_ledger_outcome as placeholders; fix them at TS review before wave 2. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12874 | RWB-P8-E1001-APP | GAP-2123 |  | Assign the rwb_valuation tables (valuations, D6 route decision, route agent output) to S1 rwb-valuation so its tests have a schema to seed and assert on. |

### RWB-PLT-NF06-DB; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12877 | RWB-P8-E1001-APP | GAP-0150 |  | Record the split as the platform DB story and 19 per-service DB stories, each in its own schema with its own Flyway sequence; keep 92-table and 30-view counts. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:RWB-PLT-OBS and RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12879 | RWB-P8-E1001-APP | GAP-2061 |  | Add a per-service availability table (19 rows) applying the same two targets; state one service shape once; define a composed screen as the product of its called services within the one-hop budget. |

### OTHER:Security and Access Design v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12882 | RWB-P8-E1001-APP | GAP-2035 | none | Section 7 per service: one login rwb_<short> per service, grants on own schema only, rwb_source_data sole holder of recovery view grant, recovery_svc row replaced by service login isolation row; state change in realignment table. |

### OTHER:Functional Specification P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12883 | RWB-P8-E1001-APP | GAP-0980 | none | Align field catalog: role.entra_group kept as nullable, empty Workbench column per Technical Specification P4 v3 DF-REF-039; mapping read at run time through rwb-source-data contract, no ACE fact copied. |

### OTHER:Technical Specification P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12884 | RWB-P8-E1001-APP | GAP-0979 | none | Section T3.3: platform naming convention for constraint names; primary key on id; unique on role_code; single foreign key permission.role_id; one index per read path with leading columns of section 13. |

### OTHER:v4 Mapping workbook ('By source' sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12891 | RWB-P8-E1001-APP | GAP-0212 |  | In the Aric via COLLINS row, read ACE table as rwb_source_data.party_ext; leave the 1/0/0/1 counts and the Total row unchanged. |

### OTHER:v5 Mapping rules (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12892 | RWB-P8-E1001-APP | GAP-0215 |  | Name contact_point_ext, account_ext and valuation_ext under 'Extension fields'; leave the 133 field rows unchanged until LDM v10 lists extension columns. |

### OTHER:v5 Mapping (column B) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12893 | RWB-P8-E1001-APP | GAP-0216 |  | Leave the 81 blank data-product cells empty in v5; assign the 81 fields at the next LDM revision. |

### OTHER:v4 Mapping DP06 row (basis cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12894 | RWB-P8-E1001-APP | GAP-0226 |  | Record S5 as owner of the Workbench asset data set; ACE collateral and valuation remain a P1 read; valuation_ext remains P1. |

### OTHER:v4 Mapping DP07 row (basis cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12895 | RWB-P8-E1001-APP | GAP-0227 |  | Record S4 as owner of the Workbench legal data set; ACE court records remain a P1 read; notice and proof of delivery remain P6. |

### OTHER:v4 Mapping DP13 row (basis cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12896 | RWB-P8-E1001-APP | GAP-0229 |  | Record P8 as owner of the proceeds and matching data set; write_off stays S7; ACE payment and GL records stay a P1 read. |

### OTHER:v4 Mapping DP05 row (basis cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12897 | RWB-P8-E1001-APP | GAP-0230 |  | Record P1 as owner of the interaction ledger; notice content and delivery stay P6; case timeline stays a P3 read through the P1 contract. |

### OTHER:v4 Mapping DP14 row (basis cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12898 | RWB-P8-E1001-APP | GAP-0231 |  | Record P3 as owner of parameters and reference data; roles and DoA stay P4; templates and merge fields stay P6. |

### OTHER:Ownership split workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12899 | RWB-P8-E1001-APP | GAP-0232 |  | Keep the count of 88. In the row 4 basis cell, add: 93 rows, 4 extension tables, 1 legacy table with no target, 88 Tier 4 tables over 19 owners. |

### OTHER:Roles; OTHER:Change process and Quality measures (v4 workbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12900 | RWB-P8-E1001-APP | GAP-0233 |  | Add a service data steward role row, an owner-service change-process step and a schema-isolation quality measure. Keep the v3 rows unchanged. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Ownership sheet and Ownership split (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12901 | RWB-P8-E1001-APP | GAP-0234 |  | Append an owning service column. Change the Workbench access cells of Ownership split rows 7 and 8 to the owning service and its schema. Replace the DL02 wording at the next revision. |

### OTHER:Target Architecture v6 slide 11 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12902 | RWB-P8-E1001-APP | GAP-1984 |  | State the target count once as 93 Ownership Map rows (87 Workbench tables and 6 platform library tables). Record 92 as the version 6 monolith count that the physical schema work replaces. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12904 | RWB-P8-E2008-APP | CG-ALL-7511 | 13 | Create story RWB-P7-E1073-CON or name the existing story that carries the DP-04 rule-kit capability; then the §13 C row points to it. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12908 | RWB-P8-E2008-APP | DOR-RWB-P8-E2008-APP-8 | 12.5 | Add matchPayments and activities readFacts, evaluateMatch, recordAndApply, raiseMissedPayment to Temporal Catalog v1; confirm ProceedsMatched.v1 and PaymentMissed.v1 topics with retry and DLT topics. |

### OTHER:Rule registry (package assignment of rwb-comms) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12922 | RWB-P8-E2008-APP | GAP-2395 | find it | Settle the package assignment of rwb-comms with the rule registry owner before the integration stage; no fourth package code is invented. |

### OTHER:Per-service contract bases of rwb-source-data, rwb-case, rwb-treatment and rwb-rules; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12923 | RWB-P8-E2008-APP | GAP-2503 | find it | Declare the nine consumed operations with one hop and a 2 s timeout; name workflow matchPayments; record in RTM that AC1, AC3, AC4 and AC5 of the legacy key are carried by no story of this split. |

### OTHER:TSD P4 T6.1 (RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12928 | RWB-P8-E2008-APP | GAP-0926 | n/a | Publish permission letters for all 14 capability areas per role, with each role's default scope; load through RWB-P4-AD002-APP. |

### OTHER:Epics 3 to 8 BRD and FSD P8 v3 A1.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12933 | RWB-P8-E2008-APP | GAP-1629 |  | Build settlement booking confirmation with EP03 in wave 2; keep proceeds features in wave 3; align FEAT-PAY-06 first release to E3. |

### OTHER:FSD P8 v3 and TSD P8 v2 T8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12942 | RWB-P8-E2008-APP | GAP-1624 | 18 | Fill the FSD P8 v3 'Requirements served' table and TSD P8 v2 T8 'Requirement traceability' with the REQ IDs served, or state that P8 has no requirement ID of its own. |

### OTHER:Delivery plan (work packages B-P1-08 and B2-P1-014; OTHER:plan generator) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12945 | RWB-P8-E2008-APP | GAP-2180 |  | Keep one Work Package per story slice; drop the duplicate for RWB-P1-E2008-APP; number CG rows once; add a plan-uniqueness check to checks/run_all.py. |

### OTHER:Program BRD v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12948 | RWB-P8-E2008-APP | GAP-1641 | 9 | Add section 5.11 (REQ-S4-010) to the section 11 note in the next version. Story-side citation not applied: target section text not in chunk. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12949 | RWB-P8-E2008-APP | GAP-1349 | 9 | Publish the SCR-28 field list and the run view in the edge contract. Case payment read via GET /proceeds and workflow matchPayments are story-side choices not applied: sections not in chunk. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12964 | RWB-P8-E2008-CON | DOR-RWB-P8-E2008-CON-1 | 1 | Add the role 'contract owner of the payment service (TechX)' with a role code, or name the existing role code that the story should use. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12965 | RWB-P8-E2008-CON | DOR-RWB-P8-E2008-CON-12 | 12.7, 16, 18 | Add test case rows TC-P8-E2008-CON-01 to -09 to Test Cases v8; align the section 18 test lists to RTM v7 |

### OTHER:Data Migration Approach and TSD P8 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12969 | RWB-P8-E2008-CON | GAP-2533 | find it | Publish the handover file with count, checksum and resolution stamp; name its format, location and retention; name the load command, run record and rights; add provenance and migration-date column to the proceeds schema |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12970 | RWB-P8-E2008-CON | GAP-3175 | find it | List LoadCompleted as the legacy alias of AceDataReady (EV-26) and keep AceDataReady as the target name |

### RWB-P8-E2008-APP; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12972 | RWB-P8-E2008-CON | GAP-2503 | 11 | Name workflow matchPayments and its four activities; record in the RTM that AC1, AC3, AC4 and AC5 of the legacy key are carried by no story of this split |

### OTHER:FSD P8 v3; OTHER:S2 A2.10; OTHER:A2.11 and A2.17 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12973 | RWB-P8-E2008-CON | GAP-1703 | 12.1 | Remove writes to NLEADS, ALS, GL and CCMS; record booking reference from TreatmentBooked and break from PaymentMissed; rwb-payment owns booking, matching and posting. |

### OTHER:FSD P8 v3; OTHER:A2.3.4.1 to A2.11.4.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12974 | RWB-P8-E2008-CON | GAP-1625 | 7 | Replace placeholder AC rows with testable main-flow criteria written from feature statement, business rules and field list, marked new; FSD owner confirms before wave 3 system test. |

### OTHER:FSD P8 v3, integration points of A2.1 and A2.3 to A2.11 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12975 | RWB-P8-E2008-CON | GAP-1631 | 12.1 | Replace ALS, GL, ATS, AMIS and LED interface points: read ALS position via rwb-source-data after next ACE batch; ledger postings via rwb-integration; auto-debit and LED routes outside 19 services. |

### OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12976 | RWB-P8-E2008-CON | GAP-0926 | 9 | Publish letters of all 14 capability areas per role with each role's default scope as a new T6.1 version; load via RWB-P4-AD002-APP. |

### OTHER:Payment matching harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12978 | RWB-P8-E2008-CON | GAP-0393 | 15 | Record composite proceeds and exception route path and merge order, harness environment, ALS payment fixture format, seed pack, evidence format, retention and pass or fail gate at wave 2 entry check. |

### OTHER:Treatment story of RWB-E2-008 S2 slice (rwb-treatment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12986 | RWB-P8-E2008-CON | GAP-2693 | 12 | Build the plan position from the TSD columns; apply ProceedsMatched and PaymentMissed of RWB-P8-E2008-CON through the inbox; name activities applyProceedsMatched and holdMissedInstallment; serve the position in the treatment read of API-S2-002; confirm package and frequency at contract freeze. |

### OTHER:rwb-payment AsyncAPI document; OTHER:TSD P8 v2 T5.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12993 | RWB-P8-E2008-CON | GAP-1351 | find it | Name DecisionRecorded as a produced event owned by rwb-decision on rwb.decision-record.v1, published only via the DP-03 local library. |

### OTHER:Work Package plan generator (B-P1-08; OTHER:B2-P1-014, checks/run_all.py) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12995 | RWB-P8-E2008-CON | GAP-2180 | find it | Keep one WP per story slice: drop B2-P1-014 or drop RWB-E2-008 from B-P1-08 fanout; add plan-uniqueness check failing on duplicate Write only files. |

### OTHER:FSD P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-12996 | RWB-P8-E2008-CON | GAP-2495 | find it | Publish the dry run of an existing version as read-only, returning testResult (total, passed, failed, failing case IDs), per-case expected and actual, and recorded dry-run counts. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13006 | RWB-P8-E2008-OPS | DOR-RWB-P8-E2008-OPS-12 | 12, 12.7, 16, 18 | Register TC-P8-E2008-OPS-01 to -09 in Test Cases v8; align the section 18 test lists of RWB-P8-E2008-OPS with RTM v7. |

### OTHER:rwb-payment service baseline OpenAPI fragment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13018 | RWB-P8-E2008-OPS | GAP-0599 |  | Publish the two reads on /api/recovery/source-data/v1 with the resource names, businessDate query parameter, element names and status set of section 12.1; confirm MSG-P2-007 with the P1 message owner. |

### RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13019 | RWB-P8-E2008-OPS | GAP-0926 |  | Publish the letters of all 14 capability areas per role with each role's default scope as a new TSD P4 T6.1 version; load them through RWB-P4-AD002-APP. |

### OTHER:TSD P8 v2 T-A.2 and service OpenAPI 3.1 and AsyncAPI documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13022 | RWB-P8-E2008-OPS | GAP-1350 |  | Publish one OpenAPI 3.1 and one AsyncAPI document per service, problem+json on every non-2xx status, MatchRequest shape, next Flyway number, major version 1 with BACKWARD acceptance. |

### OTHER:FSD P8 v3 (AC-EXC-P8-001-02) and rwb-source-data reconciliation break list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13024 | RWB-P8-E2008-OPS | GAP-1627 |  | Report the orphan payment as a break row on the reconciliation break list with check name 'References'; remove the exception-table reference; confirm the check name with the data steward. |

### OTHER:Work Package B2-P7-022 story line (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13029 | RWB-P8-E2008-OPS | GAP-2493 |  | Keep rwb-decision placement. Split the record: rwb-payment writes the local record in its own transaction and publishes it; rwb-decision holds package, rows, test cases, collects records, appends to the ledger and runs JOB-14, and evaluates no payment. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13034 | RWB-P8-E2008-OPS | GAP-0604 | header | Contract dependencies row names RWB-P3-E1043-CON for the reference data; wave 2 freeze wording removed |

### OTHER:FSD P8 v3 and TSD P8 v2 section T8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13037 | RWB-P8-E2008-OPS | GAP-1624 | 18 | Fill the Requirements served table and the T8 Requirement traceability table with REQ IDs and FSD feature and AC IDs, or state that P8 has no requirement ID of its own. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13042 | RWB-P8-E2008-OPS | GAP-1351 | — | Keep DecisionRecorded owned by rwb-decision on topic rwb.decision-record.v1; name it in the rwb-payment AsyncAPI as a produced event with the owner's schema, published via DP-03 library. |

### OTHER:Delivery work package plan (B-P1-08; OTHER:B2-P1-014) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13044 | RWB-P8-E2008-OPS | GAP-2180 | — | Keep one WP per story slice: drop B2-P1-014 or drop RWB-E2-008 from B-P1-08 fanout; number CG rows once; add plan-uniqueness check on Write only blocks. |

### OTHER:Rule-registry API contract (P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13045 | RWB-P8-E2008-OPS | GAP-2495 | — | Publish dry run as read-only operation returning testResult with total, passed, failed, failing case IDs, per-case expected and actual, and recorded dry-run counts; keep boundary cases in rule_test_case set. |

### OTHER:Program BRD v5 section 11 note (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13048 | RWB-P8-E2008-OPS | GAP-1641 | header | Story side cited; the BRD note change belongs to the BRD owner. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20803 | RWB-P8-E1001-APP | R-28414 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: 'the document store and the data lake copy is written to the access |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0012 | 19 schemas, logins and the connection budget are not created | ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0062 | Wave conflict P8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0100 | Ownership Map endpoints are the monolith operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0107 | The Ownership Map 'FK cuts' sheet has no rows while 48 cross-owner foreign keys exist | Architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0108 | rwb-valuation owns no table in the Ownership Map | Architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0109 | The map does not say which schema holds the six PLT library tables | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0112 | The per-service Flyway sequence is not specified | ACE team | Resolved (directive) |
| GAP-0113 | The four extension tables have no table comment | Data steward | Resolved (directive) |
| GAP-0114 | lake_copy_watermark has an owner but no target | Architecture team | Resolved (directive) |
| GAP-0115 | ERD v5 draws 90 foreign keys and Physical Schema v6 has 92 | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0116 | ERD v5 has no owner or service grouping | Architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0150 | FEAT-RDF-01 still creates one recovery schema of 92 tables while D-RCV-60 gives each service its own schema | ACE database team lead and the platform DB solution architect | Resolved (directive) |
| GAP-0202 | The 30 recovery.v_ace_* views have no row in the Ownership Map, so the model gives them no owner | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0206 | The 104 relationships are single-schema references and the Ownership Map's FK cut sheet is empty | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0210 | Eleven 'Workbench entity' names in v4 are ACE entities with no row in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0211 | v4 has no owner column and no target schema, so ownership is carried only by the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0212 | The 'By source' sheet counts the extension field against ACE table 'recovery' | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0215 | Only party_ext appears in the mapping; the other three extension tables are absent | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0216 | 81 of the 133 field rows carry no data product | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0224 | v3 states no owning service and no owning schema for any of the 14 data products | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0225 | DP04 Treatment and offers has three owners after the realignment | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0226 | DP06 Collateral and assets mixes ACE data, S5 asset records and a P1 extension table | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0227 | DP07 Legal events and cases mixes ACE court records, S4 legal actions and P6 notices | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0228 | DP11 Scores and route economics has no table row in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0229 | DP13 Money and closure mixes P8 proceeds, S7 write-off and ACE payment and GL data | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0230 | DP05 Contact and promises splits into a P1 ledger, P6 letters and a P3 case timeline | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0231 | DP14 Reference data splits into P3 parameters and lists, P4 roles and DoA, and P6 templates | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0232 | The 88 Workbench tables of Tier 4 cannot be reconciled with the 93 rows of the Ownership Map from v3 alone | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0233 | Roles, Change process and Quality measures still describe one Workbench owner, one backlog and one check set | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0234 | Six Ownership rows name 'Application owner (DL02)' and two Ownership split rows name 'the recovery module' | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0285 | No source states how the built recovery schema, 92 tables and 14 data products, is cut across the 19 rwb_* schemas or how each V0001 baseline is produced | ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0333 | The owning rwb_* schema of the 24 operational dictionary objects is not stated | ACE database administrator | Resolved (directive) |
| GAP-0393 | Payment matching integration harness: composite proceeds and exception route, harness environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0453 | The wave 4 cutover reconciliation harness pack for money and closure is not specified | Integration lead | Resolved (directive) |
| GAP-0543 | proceeds is P8's, write_off is S7's and the closure sits on the case (P3) while the legacy money and closure migration is a single P1 slice, and no source says who loads each and what survives of the matching state | Solution architect | Resolved (directive) |
| GAP-0557 | RWB-P1-E1001-APP: schema-split mechanics, login name, extension-table delivery boundary and Arch v5 against FSD and TSD P1 | Solution architect | Resolved (directive) |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0599 | The two read operations, their resource and element names and their error status set are stated by no source, because the legacy read was an in-process Java interface with no path, no query parameter and no status code | Solution architect with the P8 contract owner | Resolved (directive) |
| GAP-0601 | The order of the payment answer, the fold of a repeated payment_code, the row cap of one call and the number of ALS payments per business date are stated by no source | Tech lead with the P8 contract owner | Resolved (directive) |
| GAP-0602 | Architecture v5 slide 15 names a GET /accounts/{id} of rwb-source-data that TSD P1 T-A.1 does not carry and no Work Package owns, while this story answers nextInstallmentDate | Solution architect with the P1 tech lead | Resolved (directive) |
| GAP-0603 | The caller of both reads has no actor of record after the data-load actor was retired, and the architecture names the P8 to P1 call as a Temporal activity while the Work Package fixes one REST hop | Solution architect with the P8 tech lead and the P4 owner | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0925 | POST /authorise request and response shape is not specified for the payment-matching reads | Solution architect | Resolved (directive) |
| GAP-0926 | Permission letters for WRITE_OFF_AND_POSTING and TREATMENT_AND_OFFER and the scope of the Credit Administration role are absent from the RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0927 | The field that carries the filter and the row count in an AC-READ or AC-DENY entry is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0976 | The exact per-service table list of rwb_access is not stated in one place | Solution architect | Resolved (directive) |
| GAP-0978 | The file name and sequence number of the rwb_access baseline migration are not fixed | Tech lead | Resolved (directive) |
| GAP-0979 | The constraint names and the full index set of the five tables are not specified | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-0980 | role.entra_group is a column in the technical specification and not a Workbench column in the functional one | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1280 | LDM v8 states 18 fields for rule_row and a rule_test_case.package_version_id that its fields sheet does not define, and both name cross-schema foreign keys that DP-01 forbids | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1346 | RWB-E2-008: the seven consumed operation names and payloads are not published, and the plan C row names four P3 contracts only | Solution architect | Resolved (directive) |
| GAP-1347 | RWB-E2-008: the three event payloads and the decision-record element are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1348 | RWB-E2-008: the proceeds field set and its idempotency tables disagree between the legacy story and TSD P8 T3.1 | Solution architect | Resolved (directive) |
| GAP-1349 | RWB-E2-008: the case payment read, the SCR-28 and run-view field lists and the activity names of JOB-07 are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1350 | RWB-E2-008: the contract artefact names, the problem+json body, the MatchRequest shape and the registry mode of rwb-payment are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1351 | RWB-E2-008: the producer and the owner of DecisionRecorded disagree between the event catalogue and the messaging design | Solution architect | Resolved (directive) |
| GAP-1352 | RWB-E2-008: the deployment targets, the tier sizes, the rollout strategy and the rollback procedure of rwb-payment have no source | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1353 | RWB-E2-008: no source fixes a numeric target for the outbox-lag, dead-letter or workflow-failure alerts of rwb-payment | Platform administrator | Resolved (directive) |
| GAP-1354 | Legacy AC1, AC3, AC4 and AC5 of RWB-E2-008 are owned by no story in this split | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1512 | Four tables carry a name, an owner and a purpose but no field list in the read sources | Data architect | Resolved (directive) |
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
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1984 | The Workbench table count is 92 in version 6 and 93 in the Ownership Map | Data architect | Resolved (directive) |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2061 | The source is written for one recovery module and has no per-service target, size or deployment shape | Architecture with RWB-PLT-OBS and RWB-PLT-DB | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2062 | No per-topic sizing exists for the 19 topics; one topic is sized in the architecture | RWB-PLT-EVT with the owning services | Resolved (directive) |
| GAP-2123 | The Ownership Map assigns no table to rwb-valuation although Architecture v5 gives it a schema | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2132 | The recovery table count of the source and the table count of the Ownership Map do not agree | ACE | Resolved (directive) |
| GAP-2178 | RWB-DM-013 names three entities and a cutover step but no owner, source, format or sign-off place after the realignment | RW-DATASTEW | Resolved (directive) |
| GAP-2180 | Two Work Packages of the same stage write the same story file for RWB-P1-E2008-APP | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2395 | No source names which of the three Epic 2 packages a notice of rwb-comms reads, nor the package code the service is assigned | Business analyst | Resolved (directive) |
| GAP-2401 | The LDM states one field count for rule_row and a rule_test_case column its fields sheet does not define, and both TSD P7 and the LDM name cross-schema foreign keys that DP-01 forbids | Solution architect, P7 rwb-decision, with the data owners of rwb_case and rwb_access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2493 | The Work Package places the payment-matching decision and its record in rwb-decision, while DP-03 keeps the record write in the owning service's transaction and DP-04 keeps the evaluation there, so no source fixes where a match record becomes central | Solution architect, with the decision service owner and the payment service owner | Resolved (directive) |
| GAP-2494 | No source names the target operations, the DecisionRecorded payload, the decision code of a missed payment, the inputs reference, the parameter key of the input age limit or the read page | Solution architect, with the owners of rwb-payment, rwb-access and rwb-case | Resolved (directive) |
| GAP-2495 | The dry-run answer of a rule-package version beyond testResult and dryRunCounts, and whether a caller may supply boundary cases, is in no source | Solution architect, with the rule registry owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2497 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2498 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept, and the legacy levels have no counterpart in the template | Traceability owner | Resolved (directive) |
| GAP-2503 | rwb-payment payment matching (application slice): the consumed operation names and elements, the workflow and activity names, the payment code and the missed-payment key, the owner of the treatment record and the account of the legacy AC1, AC3, AC4 and AC5 are settled by no single source | Solution architect, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the payment service | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2504 | rwb-payment payment matching (contract slice): the element names of the nine consumed operations, the extra event payload fields, the operation the architecture lists and the ownership map does not, and the schema baseline of proceeds are fixed by no single source | Contract owner of rwb-payment, with the owners of rwb-source-data, rwb-case, rwb-treatment, rwb-decision and the event platform | Resolved (directive) |
| GAP-2505 | rwb-payment payment matching (deployment slice): the login and secret reference, the replica and threshold values, the partition and retention values, the build ID policy, the backfill limit and the runbook ownership are fixed by no source | DevOps team, with the platform administrator, the observability owner, the event platform owner and the workflow kit owner | Resolved (directive) |
| GAP-2533 | rwb-payment cutover load of RWB-DM-013: the handover file, the load command and its run record, a provenance column, the legacy payment_code column and the two schema-level H rows are fixed by no single source, and this slice owns no legacy criterion | Data steward and solution architect of rwb-payment, with the rwb-source-data owner, the schema baseline owner and the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2534 | The DDL of proceeds beyond its columns is not published: constraint names, index names, index columns and the Field IDs of the 7 standard columns | ACE team | Resolved (directive) |
| GAP-2535 | TSD P8 T3.1 carries payment_match_rule as a second table of the module, and the Ownership Map gives P8 one table only | Solution architect | Resolved (directive) |
| GAP-2536 | The read paths that proceeds has to serve, and the screens that read it, are stated in no source of the read set | Solution architect | Resolved (directive) |
| GAP-2537 | The handover of a service's field declaration to the one dictionary has no documented mechanism or operation | Solution architect | Resolved (directive) |
| GAP-2538 | TSD P8 T3.3 declares three many-to-one relationships of proceeds and the target keeps them as values | Solution architect | Resolved (directive) |
| GAP-2539 | DP13 Money and closure is catalogued with the system of record ACE only, while the match on the same row is a Workbench record | Business analyst, P8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2541 | EP01's wave map wave is 1 and rwb-payment's Architecture v5 wave is 2 for the same story | Portfolio lead | Resolved (directive) |
| GAP-2693 | The delivery route of a match to rwb-treatment, the plan-position elements and the payment frequency of a plan are not specified for the S2 slice of RWB-E2-008 | Tech lead of rwb-treatment with the P8 rwb-payment owner, the P3 rwb-case owner and the P7 rwb-decision package owner at the wave 2 contract freeze | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3151 | Origin tag where one legacy criterion is carried by several new stories | TechX | Resolved (directive) |
| GAP-3171 | Service P8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3175 | The load event is LoadCompleted (EV-26) in the build notes and AceDataReady (EV-26) in the architecture catalogue | Solution architect with the integration lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P8-E2008-APP | skipped AC ID | 126 | missing: AC1, AC3, AC4, AC5, AC17 |
| RWB-P8-E2008-APP | Not specified without item ID | 24 | \| Contract artefacts \| Not specified in the source documents for the artefact names, the error body and the registry mode (GAP-1350); DecisionRecorded is produc |
