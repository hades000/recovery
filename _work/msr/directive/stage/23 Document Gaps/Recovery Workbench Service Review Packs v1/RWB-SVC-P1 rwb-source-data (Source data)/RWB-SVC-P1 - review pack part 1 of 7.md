# RWB-SVC-P1 rwb-source-data (Source data) - review pack, part 1 of 7 (RWB-P1-ACE001-DB to RWB-P1-DM011-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 17 |
| Resolved in the stories | 319 |
| Cross-document (pending in another document) | 227 |
| Not applied (value not in the sources) | 13 |
| Open business decisions | 23 |
| Register gaps linked | 95 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P1-ACE001-DB | 22 | 38 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 ACE001 DB ACE DB additions for the Recovery Workbench - ACE DB v2.md |
| RWB-P1-AD018-APP | 25 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 AD018 APP Interface and job monitor v2.md |
| RWB-P1-AD018-CON | 20 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 AD018 CON Interface and job monitor - contract v2.md |
| RWB-P1-AD018-OPS | 12 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 AD018 OPS Interface and job monitor - deployment v2.md |
| RWB-P1-AD019-APP | 30 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 AD019 APP Data quality and reconciliation console v2.md |
| RWB-P1-AD019-OPS | 10 | 11 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 AD019 OPS Data quality and reconciliation console - deployment v2.md |
| RWB-P1-DM001-APP | 16 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM001 APP Migrate account and arrears v2.md |
| RWB-P1-DM002-APP | 12 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM002 APP Migrate customer and party v2.md |
| RWB-P1-DM003-APP | 20 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM003 APP Migrate case and ownership v2.md |
| RWB-P1-DM004-APP | 21 | 5 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM004 APP Migrate treatment and offers v2.md |
| RWB-P1-DM005-APP | 19 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM005 APP Migrate contact and promises v2.md |
| RWB-P1-DM006-APP | 19 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM006 APP Migrate collateral and assets v2.md |
| RWB-P1-DM007-APP | 23 | 6 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM007 APP Migrate legal events and cases v2.md |
| RWB-P1-DM008-APP | 18 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM008 APP Migrate partner performance v2.md |
| RWB-P1-DM009-APP | 16 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM009 APP Migrate debt sale v2.md |
| RWB-P1-DM010-APP | 17 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM010 APP Migrate documents and extracted fields v2.md |
| RWB-P1-DM011-APP | 19 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM011 APP Migrate scores and route economics v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P1-AD018-APP | R-09580 | CG-ALL-1849 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-AD018-CON | R-09582 | CG-ALL-1857 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-AD018-OPS | R-09583 | CG-ALL-1862 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-AD019-APP | R-09589 | CG-ALL-1873 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM001-APP | R-09599 | CG-ALL-1890 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM002-APP | R-09603 | CG-ALL-1896 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM003-APP | R-09607 | CG-ALL-1902 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM004-APP | R-09611 | CG-ALL-1911 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM005-APP | R-09617 | CG-ALL-1921 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM005-APP | R-09618 | CG-ALL-1925 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-P1-DM007-APP | R-09622 | CG-ALL-1936 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM008-APP | R-09626 | CG-ALL-1944 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM009-APP | R-09630 | CG-ALL-1953 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM010-APP | R-09634 | CG-ALL-1960 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM011-APP | R-09637 | CG-ALL-1969 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-DM005-ITG, RWB-P1-DM005-APP | R-21808 | GAP-2166 | Register gap | Data steward and data product owner | The cutover extract layout, the place of the two ACE business keys on the interaction row and the owning data product of contact_point_ext are not fixed by any target source | Settle the three points at the cutover rehearsal: publish the dump layout and cutover record format with the release pipeline owner, add the two business-key columns to the interaction dictionary rows or state that source_ref carries them, and record in the data product catalog whether contact_point_ext is loaded by the DP05 cutover or by the DP02 story. |
| RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-P1-DM007-APP, RWB-P1-DM008-APP | R-21816 | GAP-0535 | Register gap | Data steward and data product owner of rwb-source-data with the S9 rwb-partner tech lead and the data migration lead | The DM007 and DM008 instruction slice, the handover package format, the recency proof of a product with no ACE view and the field list beyond AC1 are not fixed by one source | Rule the instruction slice at the cutover rehearsal: this key hands over the panel, the partner users and the performance facts of the instructions, RWB-DM-007 hands over the instructions raised for legal actions, and S9 loads both idempotently on the instruction id; fix the package layout and the handover point in the cutover record; count the ten clean days from the reconciliation_result rows of JOB-04 for the business dates after the load, a PASS row with no unexplained variance and no new REC-05 orphan per day, with a break resetting the count; and carry the three legacy field ranges whole so that the field list beyond AC1 is the legacy dictionary's and not the story's. |
| RWB-ITG-DM010-ITG, RWB-P1-DM010-APP | R-21829 | GAP-2174 | Register gap | Data steward and data product owner (RW-DATASTEW) with the rwb-document service owner and the ACE team lead | RWB-DM-010: the owner of the document records, the legacy dump, the handover and the legacy retention period are not specified for the realigned split | Accept the Ownership Map split: rwb-source-data extracts and hands over, rwb-document loads into rwb_document on its own sequence, rwb-case holds recovery_case. Read the dump once from the legacy Workbench cutover dump into a file with a checksum, keep the legacy field range unchanged, and record the source, the handover location and the retention period in the cutover record of the release pipeline at the wave 4 entry check. |
| RWB-ITG-DM006-ITG, RWB-P1-DM006-APP | R-28408 | GAP-2168 | Register gap | Data steward and data product owner | Retention period of the legacy tables after cutover is not given | Take the period from the retention class of the record class in retention_rule, and name it in the cutover plan. |
| RWB-P1-DM005-APP | R-33391 | ASM-ALL-1925 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-P1-DM006-APP | R-35717 | ASM-3480 | Register assumption |  | The legacy listing, sale instruction and appraisal acceptance tables stay read-only for the retention class of their record class in retention_rule, and the ten clean days of AC3 run inside that period. | Data steward and data product owner at the cutover sign-off |
| RWB-P1-DM010-APP | R-35743 | ASM-3504 | Register assumption |  | rwb-source-data extracts the legacy Workbench document and document field records for the open cases and hands them over as a file with a checksum and per-entity counts; rwb-document loads them into rwb_document on its own Flyway sequence; rwb-case holds recovery_case. rwb_source_data holds no document, document field or custody table, and this story's version creates none. | Data steward and data product owner (RW-DATASTEW) with the rwb-document service owner at the wave 4 entry check |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P1-ACE001-DB | R-04213 | DOR-RWB-P1-ACE001-DB-16 | Header | Definition of Ready item 16 Size: Fail | No size is given in the sources; the squad sizes the story at refinement. |
| RWB-P1-ACE001-DB | R-14752 | DOR-RWB-P1-ACE001-DB-15 | Header | Definition of Ready item 15 INVEST: Partial | INVEST size cannot be confirmed until the squad sizes the story at refinement. |
| RWB-P1-AD018-APP | R-14760 | DOR-RWB-P1-AD018-APP-17 | 3 | Definition of Ready item 17 Dependencies: Partial | RWB-P1-AD018-OPS, RWB-P1-E1069-APP and RWB-PLT-E1056-OPS are named in the dependency rows and section 3; completing them is delivery status of other stories (DOR-RWB-P1-AD018-APP-17). |
| RWB-P1-AD018-OPS | R-04227 | DOR-RWB-P1-AD018-OPS-16 | header | Definition of Ready item 16 Size: Fail | Size is set by the squad at refinement; no value is invented. The header states it is not set, so the item stays open. |
| RWB-P1-AD019-OPS | R-04238 | DOR-RWB-P1-AD019-OPS-16 | section header | Definition of Ready item 16 Size: Fail | No size value is in the story or the item, so the Definition of Ready item stays open; none is invented. |
| RWB-P1-AD019-OPS | R-04240 | DOR-RWB-P1-AD019-OPS-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | No published fake library or version is in the sources, so the Definition of Ready item stays open; the story records only Not specified in the source documents (DOR-RWB-P1-AD019-OPS-22) and invents no publication. |
| RWB-P1-DM001-APP | R-04243 | DOR-RWB-P1-DM001-APP-16 | section header | Definition of Ready item 16 Size: Fail | No size is held by the story or the item, so the Definition of Ready item stays open; no size invented. |
| RWB-P1-DM004-APP | R-04258 | DOR-RWB-P1-DM004-APP-14 |  | Definition of Ready item 14 Epic design: Fail | Searched the story and the cited source excerpts for an epic design sign-off record for RWB-SVC-P1; no line holds one, so the sign-off cannot be confirmed or invented. |
| RWB-P1-DM004-APP | R-04260 | DOR-RWB-P1-DM004-APP-21 |  | Definition of Ready item 21 Contract published: Fail | The Done state of RWB-PLT-E1044-CON and RWB-PLT-N001-CON is delivery status; the source excerpts returned no lines for it. Publishing cannot be asserted without inventing it. |
| RWB-P1-DM004-APP | R-04261 | DOR-RWB-P1-DM004-APP-22 |  | Definition of Ready item 22 Fake published: Fail | Searched the story and the cited source excerpts for a published contract fake library version for these contracts; none found, and no version may be named without inventing one. |
| RWB-P1-DM005-APP | R-14842 | DOR-RWB-P1-DM005-APP-17 | header | Definition of Ready item 17 Dependencies: Partial | No text change: the Ready to start line already gates on RWB-P1-E1001-APP and RWB-P1-E1069-APP; their completion cannot be established by story text. |
| RWB-P1-DM007-APP | R-14860 | DOR-RWB-P1-DM007-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Section 10 text is not in this chunk, so exact old text cannot be copied. Gap CG-ALL-1937 already cited for SCR-45 states in the quarantined copy. |
| RWB-P1-DM008-APP | R-04280 | DOR-RWB-P1-DM008-APP-16 | header | Definition of Ready item 16 Size: Fail | Size row added to the header table, but no size is recorded. The squad sets it at refinement. |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (34)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02337 | RWB-P1-ACE001-DB | CG-ALL-1825 | Header | Record ace_view_owner as a NOLOGIN database role object (grant target), not an entity or field |
| CDC-02338 | RWB-P1-ACE001-DB | CG-ALL-1826 | Header | Add collateral_detail_key as the business key of the new ACE table collateral_detail (15 columns) |
| CDC-02339 | RWB-P1-ACE001-DB | CG-ALL-1827 | 11 | Add a field for account.business_unit (DF-ACC-006), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02340 | RWB-P1-ACE001-DB | CG-ALL-1828 | 11 | Add a field for account.principal_outstanding (DF-ACC-009), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02341 | RWB-P1-ACE001-DB | CG-ALL-1829 | 11 | Add a field for account.interest_outstanding (DF-ACC-010), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02342 | RWB-P1-ACE001-DB | CG-ALL-1830 | 11 | Add a field for account.fees_outstanding (DF-ACC-011), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02343 | RWB-P1-ACE001-DB | CG-ALL-1831 | 11 | Add a field for account.daily_bucket (DF-ACC-015), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02344 | RWB-P1-ACE001-DB | CG-ALL-1832 | 11 | Add a field for account.settlement_booked_date (DF-ACC-030), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02345 | RWB-P1-ACE001-DB | CG-ALL-1833 | 11 | Add a field for account.settlement_booked_amount (DF-ACC-031), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02346 | RWB-P1-ACE001-DB | CG-ALL-1834 | 11 | Add a field for customer.party_type (DF-PTY-003), or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02347 | RWB-P1-ACE001-DB | CG-ALL-1835 | 11 | Add a field for id_type, or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02348 | RWB-P1-ACE001-DB | CG-ALL-1836 | 11 | Add a field for action_contact_status, or record the object that holds it in the owning document. Story name unchanged. |
| CDC-02352 | RWB-P1-ACE001-DB | DOR-RWB-P1-ACE001-DB-7 | 11 | Add the entities and fields named by detcheck, including ace_view_owner, collateral_detail_key, business_unit and principal_outstanding, and record the BR Field IDs for the 31 section 11 rows that have none. |
| CDC-02377 | RWB-P1-AD018-APP | CG-ALL-1842 | 4 | Record the load_run object (the inbound load run) under its dictionary name, or use the dictionary name load_id. |
| CDC-02378 | RWB-P1-AD018-APP | CG-ALL-1843 | 4 | Record run_no as the run log field, or use the dictionary name round_no or run_id. |
| CDC-02379 | RWB-P1-AD018-APP | CG-ALL-1844 | 13 | Record duration_minutes as a run field, or use the dictionary name for run duration. |
| CDC-02380 | RWB-P1-AD018-APP | CG-ALL-1845 | 13 | Record message_id as a field, or use the dictionary name for the message reference. |
| CDC-02384 | RWB-P1-AD018-APP | DOR-RWB-P1-AD018-APP-7 | 11 | Add run_no, duration_minutes and message_id, and the run log that holds them, to LDM v9 and Data Classification v5 for rwb_source_data. |
| CDC-02438 | RWB-P1-DM001-APP | CG-ALL-1880 | 1 | Record loan_account as an object removed by D-RCV-35 (or add the dictionary name) so the story's removed-object references resolve. |
| CDC-02439 | RWB-P1-DM001-APP | CG-ALL-1881 | 1 | Record account_payment as an object removed by D-RCV-35 (or add the dictionary name) so the story's removed-object references resolve. |
| CDC-02440 | RWB-P1-DM001-APP | CG-ALL-1882 | 1 | Record collections_history as an object removed by D-RCV-35 (or add the dictionary name) so the story's removed-object references resolve. |
| CDC-02441 | RWB-P1-DM001-APP | CG-ALL-1883 | 1 | Record load_run as an object removed by D-RCV-35 (or add the dictionary name) so the story's removed-object references resolve. |
| CDC-02442 | RWB-P1-DM001-APP | CG-ALL-1884 | 1 | Record dq_exception as an object removed by D-RCV-35 (or add the dictionary name) so the story's removed-object references resolve. |
| CDC-02443 | RWB-P1-DM001-APP | CG-ALL-1886 | 17 | Record recovery.ace_to_date as a helper function object defined in TSD P1 v3 T3.2, not a field, or add the function to the dictionary with its owner. |
| CDC-02444 | RWB-P1-DM001-APP | CG-ALL-1887 | 17 | Record recovery.ace_to_boolean as a helper function object defined in TSD P1 v3 T3.2, not a field, or add the function to the dictionary with its owner. |
| CDC-02455 | RWB-P1-DM002-APP | CG-ALL-1892 | find it | Record the legacy contact_point table as an object in its owning document, or give the dictionary name; the story names it only to assert that it does not exist. |
| CDC-02473 | RWB-P1-DM003-APP | DOR-RWB-P1-DM003-APP-7 | 11 | Add migrated_at as a field of the migrated recovery_case record and flyway_schema_history as a framework entity, or record both as framework-only in both documents. |
| CDC-02479 | RWB-P1-DM004-APP | DOR-RWB-P1-DM004-APP-7 | 11 | Register or map ai_recommended_plan (ACE source behind v_ace_plan) and flyway_schema_history (framework table) as entities or fields |
| CDC-02489 | RWB-P1-DM005-APP | DOR-RWB-P1-DM005-APP-7 | 11 | Record flyway_schema_history as a framework table or confirm it is out of LDM scope; confirm collections_history is a removed legacy table, not a field. |
| CDC-02501 | RWB-P1-DM007-APP | DOR-RWB-P1-DM007-APP-7 | 11 | Record flyway_schema_history as a Flyway framework table outside the entities, or confirm its exclusion. Story row now labels it so. |
| CDC-02512 | RWB-P1-DM008-APP | DOR-RWB-P1-DM008-APP-7 | 11 | Add migrated_at as a field of the partner tables, or confirm it as S9's column, so that it is named in LDM v9 and Data Classification v5. |
| CDC-02527 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-7 | 11 | Add migrated_at and flyway_schema_history as fields or entities, or confirm them as the framework table and tag names outside the model. |
| CDC-02538 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-7 | 11 | Add migrated_at as a field of document, set by the rwb-document cutover load and read by rwb-source-data (BR6). Record flyway_schema_history as the Flyway framework table outside the business model. |
| CDC-02549 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-7 | 11 | Add flyway_schema_history as a framework table entity or field, or record it as outside the model. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (23)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02394 | RWB-P1-AD018-CON | CG-ALL-1855 | 16 | Add rows for TC-P1-AD018-CON-01 to TC-P1-AD018-CON-06 with Given, When and Then copied from the criterion each row covers. |
| CDC-02405 | RWB-P1-AD018-OPS | CG-ALL-1860 | 16 | Add rows TC-P1-AD018-OPS-01 to TC-P1-AD018-OPS-06 with Given, When and Then copied from the criterion each covers. |
| CDC-02445 | RWB-P1-DM001-APP | CG-ALL-1889 | 16 | Add rows TC-DM-001-01 and TC-DM-001-04 with Given, When and Then from AC1 to AC6, and TC-DM-001-05 from AC7 and AC8 (section 16 of this story). |
| CDC-02446 | RWB-P1-DM001-APP | DOR-RWB-P1-DM001-APP-12 | 16 | Add rows TC-DM-001-01 and TC-DM-001-04 with Given, When and Then copied from their criteria, and TC-DM-001-05 from AC7 and AC8 (section 16). |
| CDC-02451 | RWB-P1-DM001-APP | GAP-0550 | section 16 | Legacy TC IDs TC-DM-001-01 and TC-DM-001-04 kept in section 16 with new Covers; full test text to be recorded in Test Cases v8 under the same IDs. |
| CDC-02456 | RWB-P1-DM002-APP | CG-ALL-1894 | 16 | Add rows for TC-DM-002-01 and TC-DM-002-04 with Given, When and Then copied from AC1 to AC4 and AC6. |
| CDC-02469 | RWB-P1-DM003-APP | CG-ALL-1901 | 16 | Add rows for TC-DM-003-01, TC-DM-003-03 and TC-DM-003-04 with Given, When and Then copied from the criteria they cover. |
| CDC-02472 | RWB-P1-DM003-APP | DOR-RWB-P1-DM003-APP-12 | 16 | Add rows for TC-DM-003-01, TC-DM-003-03 and TC-DM-003-04 under the same IDs, with Given, When and Then from the section 16 Data column; TC-DM-003-04 also covers AC4. |
| CDC-02477 | RWB-P1-DM004-APP | CG-ALL-1910 | 16 | Add rows TC-DM-004-01, TC-DM-004-03 and TC-DM-004-04 to tab Story test cases, with Given, When and Then copied from AC1, AC3 and the Access criterion. |
| CDC-02478 | RWB-P1-DM004-APP | DOR-RWB-P1-DM004-APP-12 | 16 | Add tab Story test cases rows for TC-DM-004-01, TC-DM-004-03 and TC-DM-004-04, and for TC-DM-004-05 added by this story |
| CDC-02486 | RWB-P1-DM005-APP | CG-ALL-1920 | 16 | Add rows for TC-DM-005-03 (covers AC3; BR1, BR3, BR5, BR6, BR7) and TC-DM-005-04 (covers Access; BR9), with Given, When and Then copied from the criteria they cover. |
| CDC-02488 | RWB-P1-DM005-APP | DOR-RWB-P1-DM005-APP-12 | 16 | Add TC-DM-005-03 and TC-DM-005-04 on tab Story test cases with their Given, When and Then, as section 16 states. |
| CDC-02493 | RWB-P1-DM006-APP | CG-ALL-1928 | 16 | Add rows for TC-DM-006-01, TC-DM-006-03 and TC-DM-006-04 with Given, When and Then copied from AC1, AC3 and the Access criterion. |
| CDC-02496 | RWB-P1-DM006-APP | DOR-RWB-P1-DM006-APP-12 | 16 | Add rows for TC-DM-006-01, TC-DM-006-03 and TC-DM-006-04 with Given, When and Then copied from their criteria. |
| CDC-02499 | RWB-P1-DM007-APP | CG-ALL-1934 | 16 | Add rows on tab Story test cases for TC-DM-007-03, TC-DM-007-04, TC-P1-DM007-APP-01 to -04, with Given, When and Then copied from the criteria they cover. |
| CDC-02509 | RWB-P1-DM008-APP | CG-ALL-1943 | 16 | Add rows for TC-DM-008-03 and TC-DM-008-04 in the next version, copying Given, When and Then from the criteria they cover (AC3; section 5 refusal path). |
| CDC-02511 | RWB-P1-DM008-APP | DOR-RWB-P1-DM008-APP-12 | 16 | Add test case rows TC-DM-008-03 and TC-DM-008-04 under tab Story test cases, with the same IDs as section 16. |
| CDC-02522 | RWB-P1-DM009-APP | CG-ALL-1952 | 16 | Add rows for TC-DM-009-01, TC-DM-009-03 and TC-DM-009-04 with Given, When and Then copied from the criteria they cover |
| CDC-02525 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-12 | 16 | Add TC-DM-009-01, TC-DM-009-03 and TC-DM-009-04 to Test Cases v8, and the new TC-DM-009-05 row added in section 16 for BR9. |
| CDC-02534 | RWB-P1-DM010-APP | CG-ALL-1959 | 16 | Add rows TC-DM-010-01 to TC-DM-010-04 with Given, When and Then copied from the criteria they cover |
| CDC-02537 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-12 | 16 | Add TC-DM-010-01, TC-DM-010-02, TC-DM-010-03 and TC-DM-010-04 of RWB-P1-DM010-APP section 16 to the register. |
| CDC-02545 | RWB-P1-DM011-APP | CG-ALL-1968 | 16 | Add rows TC-DM-011-01, TC-DM-011-03 and TC-DM-011-04 with Given, When and Then copied from the criteria they cover. |
| CDC-02548 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-12 | 16 | Add rows for TC-DM-011-01, TC-DM-011-03 and TC-DM-011-04 in Test Cases v8. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02349 | RWB-P1-ACE001-DB | CG-ALL-1837 | 11 | Record flyway_schema_history as the Flyway-managed schema history object of schema rwb_source_data in the owning document, or add it to the LDM dictionary. |
| CDC-02381 | RWB-P1-AD018-APP | DOR-RWB-P1-AD018-APP-11 | 12.7 | Reconcile personal-data classes of job_catalog, run log and data_product_load fields with this story, which carries none. |
| CDC-02467 | RWB-P1-DM003-APP | CG-ALL-1898 | Header | Record migrated_at as the rwb_case field set by the rwb-case cutover migration, or name the dictionary field the story should use. |
| CDC-02468 | RWB-P1-DM003-APP | CG-ALL-1899 | Header | Record flyway_schema_history as a framework table, as the story already states in its data layer section. |
| CDC-02475 | RWB-P1-DM004-APP | CG-ALL-1906 | 2, 4 | Record ai_recommended_plan as an ACE source object of v_ace_plan with its owner, or name the dictionary field it maps to. |
| CDC-02476 | RWB-P1-DM004-APP | CG-ALL-1907 | 4, 11, 12 | Record flyway_schema_history as a framework table, with its columns, in the dictionary, or confirm the name against the framework. |
| CDC-02482 | RWB-P1-DM005-APP | CG-ALL-1915 | 2 | Record the legacy monolith object collections_history (table removed as a copy of EFS data, TSD P1 v3 T3.10) in the owning document, or name the dictionary entity. |
| CDC-02483 | RWB-P1-DM005-APP | CG-ALL-1916 | 4 | Record party_id as a cross-reference name in the owning document, or use the dictionary name for it. |
| CDC-02484 | RWB-P1-DM005-APP | CG-ALL-1917 | 4 | Record contact_point_id as a cross-reference name in the owning document, or use the dictionary name for it. |
| CDC-02485 | RWB-P1-DM005-APP | CG-ALL-1918 | 4 | Record flyway_schema_history as the framework table in the owning document, or use the dictionary name for it. |
| CDC-02498 | RWB-P1-DM007-APP | CG-ALL-1930 | 4, 11, 12.7 | Record flyway_schema_history as the Flyway framework table (not a dictionary entity) in LDM v9, or name the owning object there; story text already labels it a framework table. |
| CDC-02507 | RWB-P1-DM008-APP | CG-ALL-1939 | find it | Record flyway_schema_history as a framework table object (Flyway-managed) or use its dictionary name. |
| CDC-02508 | RWB-P1-DM008-APP | CG-ALL-1940 | find it | Record migrated_at as a partner table column or use the dictionary name for the load timestamp. |
| CDC-02520 | RWB-P1-DM009-APP | CG-ALL-1948 | Header | Record flyway_schema_history as a framework table object (index, library table or flag) in the owning document |
| CDC-02521 | RWB-P1-DM009-APP | CG-ALL-1949 | Header | Add migrated_at as the handover tag field, or name the dictionary field that carries it |
| CDC-02532 | RWB-P1-DM010-APP | CG-ALL-1956 | 9 | Record migrated_at as a field of rwb_document set by the rwb-document migration, or use the dictionary name |
| CDC-02533 | RWB-P1-DM010-APP | CG-ALL-1957 | 9 | Record flyway_schema_history as the Flyway framework table of rwb_source_data |
| CDC-02544 | RWB-P1-DM011-APP | CG-ALL-1965 | 11, 12 | Record flyway_schema_history as a framework table object with its owning document, as the None: framework table rows state. |

### Epic design record (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02336 | RWB-P1-ACE001-DB | DOR-RWB-P1-ACE001-DB-14 | Header | Record the signed epic design sign-off for EP01 and RWB-SVC-P1 |
| CDC-02388 | RWB-P1-AD018-CON | DOR-RWB-P1-AD018-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-P1 in the epic design record. |
| CDC-02396 | RWB-P1-AD018-OPS | DOR-RWB-P1-AD018-OPS-14 |  | Record the signed epic design sign-off for RWB-SVC-P1 and cite it in the story |
| CDC-02423 | RWB-P1-AD019-OPS | DOR-RWB-P1-AD019-OPS-14 | header | Record the signed sign-off of the epic design for EP08 and service epic RWB-SVC-P1. |
| CDC-02434 | RWB-P1-DM001-APP | DOR-RWB-P1-DM001-APP-14 | header | Record the signed epic design sign-off for EP08 so this story can cite it. |
| CDC-02452 | RWB-P1-DM002-APP | DOR-RWB-P1-DM002-APP-14 | find it | Confirm the signed epic design sign-off for RWB-SVC-P1 and record it where this story can cite it. |
| CDC-02464 | RWB-P1-DM003-APP | DOR-RWB-P1-DM003-APP-14 | Header | Record the signed sign-off of the epic design for EP08 in the epic design record; no signed sign-off is in the source documents. |
| CDC-02480 | RWB-P1-DM005-APP | DOR-RWB-P1-DM005-APP-14 | header | Record the signed epic design sign-off for EP08 and RWB-SVC-P1 so DOR item 14 can be confirmed. |
| CDC-02490 | RWB-P1-DM006-APP | DOR-RWB-P1-DM006-APP-14 | n/a | Record the signed epic design sign-off for EP08 in the epic design record. |
| CDC-02504 | RWB-P1-DM008-APP | DOR-RWB-P1-DM008-APP-14 | header | Record the signed epic design sign-off for EP08 in the epic design record. |
| CDC-02516 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-14 | Header | Record the signed epic design sign-off for EP08 against this story's epic |
| CDC-02529 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-14 | header | Record a signed epic design sign-off that covers RWB-P1-DM010-APP |
| CDC-02540 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-14 | header | Record the signed-off epic design for the epic of this story. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02457 | RWB-P1-DM002-APP | DOR-RWB-P1-DM002-APP-11 | find it | Align the personal-data class of the fields flagged by detcheck with the story statement that none is carried. |
| CDC-02471 | RWB-P1-DM003-APP | DOR-RWB-P1-DM003-APP-11 | Header | Classify the P2 fields this story carries as personal data, or confirm none are personal data. |
| CDC-02487 | RWB-P1-DM005-APP | DOR-RWB-P1-DM005-APP-11 | 11 | Review the personal-data class of the fields this story carries in section 11 against its statement that no personal data is carried; the detcheck names no field. |
| CDC-02510 | RWB-P1-DM008-APP | DOR-RWB-P1-DM008-APP-11 | find it | Classify the P2 fields as personal data, or confirm none is carried, to match the story guardrail. |
| CDC-02524 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-11 | Header | Confirm the personal-data classification of the fields this story carries against its statement that none is personal data |
| CDC-02536 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-11 | 9 | Classify the P2 fields carried by this story as personal data, or confirm none are personal data |
| CDC-02547 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-11 | header | Reconcile the personal data classification of the fields this story carries with its statement that no personal data is carried. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02350 | RWB-P1-ACE001-DB | DOR-RWB-P1-ACE001-DB-1 | 1 | Add a role code or role name for ACE database engineer, the role used in section 1 of RWB-P1-ACE001-DB. |
| CDC-02383 | RWB-P1-AD018-APP | DOR-RWB-P1-AD018-APP-6 | 10 | Add role SY-JOBRUN to Users Roles and Permissions v5. |
| CDC-02399 | RWB-P1-AD018-OPS | DOR-RWB-P1-AD018-OPS-1 |  | Add the role 'platform engineer' used in section 1 of RWB-P1-AD018-OPS, or map it to an existing role |
| CDC-02425 | RWB-P1-AD019-OPS | DOR-RWB-P1-AD019-OPS-1 | 1 | Add DevOps engineer of rwb-source-data as a role code, or map the story role to a listed role code. |
| CDC-02494 | RWB-P1-DM006-APP | DOR-RWB-P1-DM006-APP-1 | 1 | Add the data steward role with its role code, or confirm the existing role it maps to, so §1 resolves. |
| CDC-02546 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-1 | 1 | Add role code RW-DATASTEW for the data steward role used in this story. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02362 | RWB-P1-ACE001-DB | CG-ALL-1838 | 18 | Align the test lists of REQ-RDF-001 and REQ-RDF-002 with section 18 of RWB-P1-ACE001-DB in the next RTM version. |
| CDC-02382 | RWB-P1-AD018-APP | DOR-RWB-P1-AD018-APP-12 | 12.7, 16, 18 | Align the section 18 test lists with section 16 (TC-AD-018-01 to -09) in RTM v7. |
| CDC-02387 | RWB-P1-AD018-APP | CG-ALL-1848 | 18 | Align the REQ-DRI-007 test cases between RTM v7 and section 18 in the next version of each. |
| CDC-02395 | RWB-P1-AD018-CON | CG-ALL-1856 | 18 | Align the REQ-DRI-007 trace with section 18 of this story (TC-P1-AD018-CON-02 and TC-P1-AD018-CON-04), and align the other REQ-DRI-007 rows in the same way. |
| CDC-02406 | RWB-P1-AD018-OPS | CG-ALL-1861 | 18 | Align the test lists of REQ-DRI-007 and the second differing requirement with section 18 in the next RTM version. |
| CDC-02503 | RWB-P1-DM007-APP | CG-ALL-1935 | 18 | Align REQ-RDF-001 and REQ-RDF-008 test lists with section 18 of RWB-P1-DM007-APP (TC-DM-007-03, TC-P1-DM007-APP-03, TC-P1-DM007-APP-01) in its next version. |

### RWB-P1-AD018-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02375 | RWB-P1-AD018-APP | DOR-RWB-P1-AD018-APP-21 | header | Set the build status to Done once the contract is published. |
| CDC-02386 | RWB-P1-AD018-APP | GAP-0514 | 11 | Section 11 names the field IDs. Job read and rerun shapes are published in RWB-P1-AD018-CON; the freshness shape is owned by RWB-P1-E1015-CON. |
| CDC-02397 | RWB-P1-AD018-OPS | DOR-RWB-P1-AD018-OPS-21 |  | Set build status to Done (contract published) before this story starts |
| CDC-02398 | RWB-P1-AD018-OPS | DOR-RWB-P1-AD018-OPS-22 |  | Publish a contract fake library version and record its version number |
| CDC-02403 | RWB-P1-AD018-OPS | GAP-0514 | none | Publish response field lists for the job read, the rerun and the freshness answer from DF-OPS-224 to DF-OPS-232, DF-OPS-001 to DF-OPS-008 and DF-ACE-178 to DF-ACE-186. |
| CDC-02404 | RWB-P1-AD018-OPS | GAP-2163 | 11 | Fix the Job resource, the run element field lengths, the five run states, the two 409 conditions of the rerun, and the rule for which run a list answer returns. |

### RWB-PLT-E1044-CON; RWB-PLT-N001-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02465 | RWB-P1-DM003-APP | DOR-RWB-P1-DM003-APP-21 | header | Bring RWB-PLT-E1044-CON and RWB-PLT-N001-CON to Done with their contracts published, so the contract-published check passes for RWB-P1-DM003-APP. |
| CDC-02491 | RWB-P1-DM006-APP | DOR-RWB-P1-DM006-APP-21 | n/a | Publish the contract these build dependencies need so it is available for this story; the stories are not Done. |
| CDC-02505 | RWB-P1-DM008-APP | DOR-RWB-P1-DM008-APP-21 | header | Publish the contract and reach Done status on these CON stories before this story starts. |
| CDC-02518 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-21 | Header | Publish the contract and reach Done for the build dependencies the story depends on |
| CDC-02541 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-21 | header | Publish the contract stories this story depends on and bring them to Done. |
| CDC-02543 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-23 | header | Record the contract version this story builds against; the source documents give only the /v1 path. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02389 | RWB-P1-AD018-CON | CG-ALL-1854 | 4, 14 | Add a new message ID for 'No session on a read or a rerun' with text 'Your session has ended. Sign in again.'; the story cites it in section 14 once it exists. |
| CDC-02392 | RWB-P1-AD018-CON | DOR-RWB-P1-AD018-CON-9 | 14 | Align MSG-P1-001 wording to v4 and confirm MSG-P4-001 meaning matches v4, or re-key the session message there. |
| CDC-02539 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-9 | 14 | MSG-P1-001 text in section 14 was aligned to Standard v4 under CG-ALL-1958. Any remaining message difference is passed to the standard. |
| CDC-02550 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-9 |  | MSG-P1-001 and MSG-P1-012 now carry the standard's wording (CG-ALL-1966, CG-ALL-1967); MSG-GEN-001 and MSG-P4-002 keep the legacy text. Any remaining gap belongs to the standard. |

### OTHER:Contract fake library (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02492 | RWB-P1-DM006-APP | DOR-RWB-P1-DM006-APP-22 | n/a | Publish a contract fake library version for the CON dependencies and record its version. |
| CDC-02519 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-22 | Header | Publish a fake library version for the contract and record it as published |
| CDC-02531 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-22 | header | Record a published fake library version for RWB-PLT-E1044-CON and RWB-PLT-N001-CON |
| CDC-02542 | RWB-P1-DM011-APP | DOR-RWB-P1-DM011-APP-22 | header | Record the published fake library version this story runs against. |

### RWB-P1-AD018-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02374 | RWB-P1-AD018-APP | DOR-RWB-P1-AD018-APP-14 | header | Record the signed sign-off for the EP08 epic design in the epic design record. |
| CDC-02376 | RWB-P1-AD018-APP | DOR-RWB-P1-AD018-APP-22 | header | Record the published contract fake library version. |
| CDC-02390 | RWB-P1-AD018-CON | DOR-RWB-P1-AD018-CON-10 | find it | Empty, loading, error and no-access states of SCR-44 belong in the app story, which owns the screen. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02391 | RWB-P1-AD018-CON | DOR-RWB-P1-AD018-CON-12 | 12.7, 16, 18 | Register TC-P1-AD018-CON-01 to -07 in Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-02401 | RWB-P1-AD018-OPS | DOR-RWB-P1-AD018-OPS-12 | 16 | Add TC-P1-AD018-OPS-01 to -06 to Test Cases v8; align section 18 test lists with RTM v7 |
| CDC-02500 | RWB-P1-DM007-APP | DOR-RWB-P1-DM007-APP-12 | 12.7, 16, 18 | Add rows for TC-DM-007-03, TC-DM-007-04 and TC-P1-DM007-APP-01 to -06 in Test Cases v8; align the section 18 test lists with RTM v7. Story side: added contract and boundary rows 05 and 06. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02412 | RWB-P1-AD019-APP | CG-ALL-1868 | 12.5 | Add an Activities row for runRec02, type Activity, task queue rwb-source-data, with its purpose from section 12.5. |
| CDC-02413 | RWB-P1-AD019-APP | CG-ALL-1869 | 12.5 | Add an Activities row for resolveRec05, type Activity, task queue rwb-source-data, with its purpose from section 12.5. |
| CDC-02414 | RWB-P1-AD019-APP | CG-ALL-1870 | 12.5 | Add an Activities row for writeReconciliationResult, type Activity, task queue rwb-source-data, with its purpose from section 12.5. |

### RWB-PLT-E1044-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02435 | RWB-P1-DM001-APP | DOR-RWB-P1-DM001-APP-21 | header | Bring the CON stories this key depends on to Done, then publish the contract for the account and arrears read path. |
| CDC-02453 | RWB-P1-DM002-APP | DOR-RWB-P1-DM002-APP-21 | find it | Reach Done and publish the contract that this story depends on. |
| CDC-02454 | RWB-P1-DM002-APP | DOR-RWB-P1-DM002-APP-22 | find it | Publish a contract fake library version and record it against this story. |

### 06 Data/Recovery Workbench Party and Customer Master Data Design v4.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20590 | RWB-P1-ACE001-DB | R-28942 |  | Wording fix deferred to the next content review of the Party design; narrative sits in v3 and is carried in v4. Not changed in this realignment copy. |
| CDC-20591 | RWB-P1-ACE001-DB | R-28943 |  | Source-column label reading rule belongs to the v3 workbook. No change to this story or to this v4 copy. |
| CDC-20592 | RWB-P1-ACE001-DB | R-28944 |  | Blocked: no Bash/docview access, so v4 design-note row 5 text could not be read; exact old text unknown. Rerun to write the replace. |

### OTHER:P1 service contract (API-P1-003) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02418 | RWB-P1-AD019-APP | GAP-0519 | find it | Publish response fields, paging and break-row shape of GET /admin/reconciliation/results from reconciliation_result DF-OPS-118 to DF-OPS-129 and REC-05 orphan rows. |
| CDC-02424 | RWB-P1-AD019-OPS | DOR-RWB-P1-AD019-OPS-21 | section header | Contract dependencies row names the P1 service contract of API-P1-003; no story key given. |

### RWB-P1-E1069-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02437 | RWB-P1-DM001-APP | DOR-RWB-P1-DM001-APP-23 | section header | Contract version row records that the version is not specified in the source documents. |
| CDC-02449 | RWB-P1-DM001-APP | GAP-0549 | 4 | Add GET /accounts/{id} on /api/recovery/source-data/v1 with its parameters and its answer field names. |

### OTHER:Screen specification for SCR-45 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02495 | RWB-P1-DM006-APP | DOR-RWB-P1-DM006-APP-10 | n/a | Define empty, loading, error and no-access states for SCR-45. |
| CDC-02497 | RWB-P1-DM006-APP | CG-ALL-1929 | 15 | Section 15 marks the empty, error and no access states as Not specified; the screen specification for SCR-45 must define them. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02523 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-10 | Header | Define empty, loading, error and no-access states for SCR-45 |
| CDC-20573 | RWB-P1-DM009-APP | R-14879 |  | SCR-45 empty, loading, error and no-access states are not in any source. Defining them needs a business decision, so none were added. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02351 | RWB-P1-ACE001-DB | DOR-RWB-P1-ACE001-DB-12 | 16, 18 | RTM: add TC-ACE-001-01, -02, -08, -10 to REQ-RDF-001 and TC-ACE-001-02, -03, -07, -10 to REQ-RDF-002, keeping existing tests. Test Cases, tab Story test cases: add TC-ACE-001-10 (AC9). |

### OTHER:API catalog (API-P1-003 entry) and the P1 cut-over story for RWB-DM-007 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02353 | RWB-P1-ACE001-DB | GAP-2170 |  | Add API-P1-003 to the API catalog for the cut-over package hand-off. Set flag rwb.source-data.dm007-cutover to default off. Pipeline calls API-P1-002, API-P1-003 and API-P1-010 as the proposed fix states. |

### RWB-P4-AD001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02354 | RWB-P1-ACE001-DB | GAP-0777 |  | Grant to a login named rwb_access per the section R4 pattern and let the platform DB story set the real name and pool. Keep mapping rows in role.entra_group, with TSD P4 v3 outranking FSD v3. Read ACE group facts only through the P1 contract. |

### OTHER:P1 proof-of-delivery read contract story and TSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02355 | RWB-P1-ACE001-DB | GAP-0579 |  | Answer 200 with no row, ten field names marked not available with reason SECTION_B_NOT_DEPLOYED, DP07 STALE and MSG-P1-001, behind platform flag rwb.dataengine.pod-read. Never a guessed date or fallback to data_as_of. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; RWB-P4-E1022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02356 | RWB-P1-ACE001-DB | GAP-0896 |  | Platform administrator owns the DEV identity list. Fix the synthetic key format in the Service Template Specification. Record the retirement rule with DL39. Sign-in story states the identity resolves to role.entra_group rows only. |

### OTHER:P2 integration stories (rwb-integration contract on base /api/recovery/integration/v1) and the P1; OTHER:P3 and P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02357 | RWB-P1-ACE001-DB | GAP-0662 |  | Read holding and DP02 freshness via rwb-source-data, parties via rwb-case, authorise and masking via rwb-access, audit via ACE Common INT-22. Flag rwb.integration.customer-products. Fix field names in P1, P3 and P4 contracts. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02358 | RWB-P1-ACE001-DB | GAP-3194 |  | Raise one ACE DB story per service lacking one (S2, S4, S5, S6, S7, P6, P8) for the column drop, or attach the drop to the creating APP story. Cite the chosen story on row 121 before wave 2. |

### OTHER:P1 rwb-source-data contract story (customer operations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02359 | RWB-P1-ACE001-DB | GAP-0244 |  | Add a contact read to the rwb-source-data customer contract, either GET /customers/{id}/contacts or contact points in the customer payload. Cite that operation in the sheet Read paths. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02360 | RWB-P1-ACE001-DB | GAP-0245 | 3 | Define command operations for the party flags and for contact consent and verification; state that no other service writes rwb_source_data. |

### OTHER:Interface Specifications v3 (INT-21) and the access and security design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02361 | RWB-P1-ACE001-DB | GAP-2001 | 3 | Name the path: rwb-source-data reads v_ace_iam_group and publishes the mapping as reference data; rwb-access subscribes and caches it; ACE keeps the table and view. |

### OTHER:TSD P4 v3 (T3.1 role table) and FSD P4 v3 field catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02363 | RWB-P1-ACE001-DB | GAP-0980 | 3 | Keep role.entra_group (DF-REF-039) nullable and empty; read the mapping at run time through the rwb-source-data contract; align the FSD reading. |

### OTHER:Legacy RWB-E1-007 story, section 16 test table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02364 | RWB-P1-ACE001-DB | GAP-1165 |  | Keep TC-E1-007-05 and TC-E1-007-06 as NFR rows asserting absence of the inbound adapter, folder listing, DQ-057/DQ-059 and run table; state behaviour is ACE ingestion and EV-27 AceDataLate; close when ACE ingestion publishes its checks. |

### OTHER:FSD P1 (A1.3) and TSD P1 (T6.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02365 | RWB-P1-ACE001-DB | GAP-0570 |  | ACE team lead confirms the Tier 1 table list and publishes the 21 names or the 22nd table name in the next versions; legacy RWB-E1-069 grant block stays the enumeration until then. |

### OTHER:v5 field mapping workbook; OTHER:Mapping rules (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02366 | RWB-P1-ACE001-DB | GAP-0214 |  | Add 'Status after realignment' stating RWB-ACE-001 work is carried by RWB-P1-ACE001-DB; keep Status text and the 80/53 split unchanged. |

### OTHER:P1 CON and S3 CON stories; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02367 | RWB-P1-ACE001-DB | GAP-0246 |  | State v_ace_ca_relation is served by GET /api/recovery/source-data/v1/accounts/{id} and name the route services that read it in the P1 CON and S3 CON stories. |

### OTHER:v3 Party fields and Match rules rows 2 and 11 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02368 | RWB-P1-ACE001-DB | GAP-0247 |  | Read 'reaches the Workbench' as 'is served by rwb-source-data'; correct the wording at the next content review, not in the realignment copy. |

### OTHER:v3 Party fields (Source column) and Match rules row 9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02369 | RWB-P1-ACE001-DB | GAP-0249 |  | Keep the Source column; read 'Workbench' as the owning service named in the Target schema column of the same row. |

### OTHER:v3 Party fields row 5 (design note) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02370 | RWB-P1-ACE001-DB | GAP-0250 |  | Reword the note to 'there is no party master and no contact-point master'; party_ext and contact_point_ext stay with P1 as Workbench-only extension tables. |

### OTHER:Interface Specifications v3, rows INT-35 and INT-36 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02371 | RWB-P1-ACE001-DB | GAP-2008 |  | Name rwb-treatment as consumer of INT-35 and rwb-document as consumer of INT-36, both read through the rwb-source-data contract; name the consumer in the next version of each row. |

### OTHER:Information Flow v5 slides 8-9 and new fallback slide; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02372 | RWB-P1-ACE001-DB | GAP-2101 |  | Read the batch record through recovery.v_ace_batch_status in P1 rwb-source-data only and name P1 rwb-source-data as the service raising AceDataLate; slide wording stays as issued. |

### OTHER:v3 opening paragraph; OTHER:How to use; OTHER:Template and Rules R5.3 and U3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02373 | RWB-P1-ACE001-DB | GAP-3239 |  | Replace squad wording with the five team types (TechX, ACE team, SCB IT infrastructure, DevOps team, QA team) and state the daily board in team-type terms. |

### OTHER:P1 rwb-source-data OpenAPI and AsyncAPI documents and the message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02385 | RWB-P1-AD018-APP | GAP-0440 | 14 | Publish the job read, rerun, job-log, freshness and v_ace_batch_status read schemas at the wave 4 entry check, and add the refused-rerun and not-a-Workbench-job messages. |

### OTHER:openapi/rwb-source-data-v1.yaml; OTHER:rwb-source-data AsyncAPI document; OTHER:message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02393 | RWB-P1-AD018-CON | GAP-0440 | 11 | Publish response schemas for the job read with job-log fields and run number, the rerun answer, the freshness answer with unknown-freshness case, and the v_ace_batch_status read path; add refused-rerun and not-a-Workbench-job messages. |

### OTHER:P2 Fields document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02400 | RWB-P1-AD018-OPS | DOR-RWB-P1-AD018-OPS-11 |  | Correct the personal-data classification of the flagged fields to match BR8 of RWB-P1-AD018-OPS, or name them in the story |

### OTHER:rwb-source-data OpenAPI and AsyncAPI documents and the message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02402 | RWB-P1-AD018-OPS | GAP-0440 | none | Publish schemas for the job read with job-log fields and run number, the rerun answer, the freshness answer with its unknown case, and the v_ace_batch_status read path; add the refused-rerun and not-a-Workbench-job messages. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02407 | RWB-P1-AD019-APP | CG-ALL-1864 | 12.1 | Publish GET /admin/reconciliation/results in rwb-source-data.yaml through RWB-P1-E1011-CON, or remove the operation from 12.1. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02408 | RWB-P1-AD019-APP | CG-ALL-1866 | 12.5 | Add workflow ReconciliationWorkflow on task queue rwb-source-data, as published by RWB-P1-E1011-CON section 12.5. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02409 | RWB-P1-AD019-APP | DOR-RWB-P1-AD019-APP-8 | find it | Close CG-ALL-1864, CG-ALL-1865, CG-ALL-1866 and CG-ALL-1867 in those catalogues, including the three further detcheck findings. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; OTHER:Events row EV-26 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02410 | RWB-P1-AD019-APP | CG-ALL-1865 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1, with its ACL. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02411 | RWB-P1-AD019-APP | CG-ALL-1867 | 12.5 | Add activity runRec01 on task queue rwb-source-data. |

### RWB-P3-AD019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02415 | RWB-P1-AD019-APP | DOR-RWB-P1-AD019-APP-10 | 15 | SCR-45 Data quality: add empty, error and no-access states beside the loading, breaks, referential completeness and stale states. |

### OTHER:gateway-bff contract and P1 reconciliation operations publication (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02416 | RWB-P1-AD019-APP | GAP-0447 | find it | Specify the cutover harness pack: environment and base hosts, synthetic extract fixture and layout, SCR-45 route and break-list fields, extract format and retention, gate, seeding set. |

### OTHER:rwb-source-data contract and gateway-bff contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02417 | RWB-P1-AD019-APP | GAP-0441 | find it | Publish reconciliation, key-resolution and freshness reads with paths, paging and field shapes; SCR-45 composite route with merge rules and timeouts; refresh cadence; unreachable-read problem response. |

### OTHER:rwb-case service contract, rwb-source-data contract; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02419 | RWB-P1-AD019-APP | GAP-0728 | find it | Publish the three console reads under rwb-case; name the rwb-case login with ACE DB owners; fix the SCR-45 composite route; add GET reconciliation, key-resolution and freshness operations to the rwb-source-data contract. |

### OTHER:Reconciliations sheet of the reconciliation workbook v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02420 | RWB-P1-AD019-APP | GAP-0268 | find it | Give each reconciliation row an owner from the Ownership Map Tables sheet, with the service that holds its Workbench side and its per-service reconciliation. |

### OTHER:Reconciliations and Quality measures sheets of the reconciliation workbook v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02421 | RWB-P1-AD019-APP | GAP-0269 | find it | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures, values taken from the Ownership Map Tables sheet. |

### OTHER:v3 Reconciliations register (sheet Reconciliations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02422 | RWB-P1-AD019-APP | GAP-0271 | 4 | Add a Per-service reconciliation sheet with one row per service of the 19, giving tables, check part, key, tolerance, cadence, break and result route, pattern and basis; use the Template and Rules R9 placeholder where no cadence or route is stated. |

### OTHER:Cutover reconciliation harness pack (wave 4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02426 | RWB-P1-AD019-OPS | GAP-0447 |  | Agree environment, base hosts and fixture layout at the wave 4 entry check; fix extract format and retention with the data steward; gate is all five criteria passing on stubs and on real owners. |

### RWB-P1-AD019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02427 | RWB-P1-AD019-OPS | GAP-0441 |  | Publish reconciliation, key-resolution and freshness reads with paths, paging and field shapes; publish gateway-bff SCR-45 route with path, merge rules and per-call timeout ownership; fix refresh cadence as platform configuration; add unreachable-read problem response. |

### OTHER:P1 service contract (API-P1-003; RWB-P1-AD019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02428 | RWB-P1-AD019-OPS | GAP-0519 | 18 | Publish response fields from reconciliation_result DF-OPS-118 to DF-OPS-129, paging, and the REC-05 break-list row shape. |

### RWB-P1-AD019-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02429 | RWB-P1-AD019-OPS | GAP-0520 | 4 | Mark DP-10 on RWB-P1-AD019-OPS as JOB-04 event-started from AceDataReady on the workflow kit, with no Temporal Schedule. |

### RWB-P3-AD019-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; RWB-P1-AD019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02430 | RWB-P1-AD019-OPS | GAP-0728 | 4 | Name the rwb-case login with the ACE DB owners; publish the three console reads under the rwb-case contract; add reconciliation, key-resolution and freshness GET operations to the rwb-source-data contract with business date query and paged answer; fix SCR-45 composite route with RWB-PLT-N001-CON. |

### OTHER:Recovery Workbench reconciliation workbook v3, sheet Reconciliations (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02431 | RWB-P1-AD019-OPS | GAP-0268 |  | Give each reconciliation row an owner from the Ownership Map; the owning service answers on its contract in one hop with a 2 s timeout; rwb-source-data keeps the ACE side and the JOB-04 run. |

### OTHER:Recovery Workbench reconciliation workbook v3, sheets Reconciliations and Quality measures (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02432 | RWB-P1-AD019-OPS | GAP-0269 |  | Append Owner and Per-service reconciliation columns to Reconciliations, and Owner service column to Quality measures, with values from the Ownership Map sheet Tables. |

### OTHER:Reconciliations v3 workbook (Reconciliations sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02433 | RWB-P1-AD019-OPS | GAP-0271 | find it | Add a Per-service reconciliation sheet with one row per service (19 services) giving its tables, the part of each check it runs, key, tolerance, cadence, break and result route, pattern and basis. Where no cadence or result route is stated, use the Template R9 placeholder. Route reconciliation_result to rwb-source-data. |

### OTHER:Contract fake library (owner of the RWB-P1 contract fakes) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02436 | RWB-P1-DM001-APP | DOR-RWB-P1-DM001-APP-22 | header | Publish a contract fake library version for the /v1 account and arrears read path and record its version. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02447 | RWB-P1-DM001-APP | GAP-0552 | find it | Confirm RWB-P1-DM002-APP is the rework of withdrawn RWB-DM-002, delivers the read path only, has no extract, load, reconciliation or cutover in scope, and that its retained TC IDs carry new text. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02448 | RWB-P1-DM001-APP | GAP-0235 | find it | Each migrated table names the schema of its owner per Ownership Map v1 sheet Tables; section 9.2 lists the tables and the schema of each. |

### OTHER:Data Migration Stories v3 (next story-master version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02450 | RWB-P1-DM001-APP | GAP-0546 | find it | Correct the title of RWB-P1-DM001-APP to name the read path; story key and legacy key unchanged. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02458 | RWB-P1-DM002-APP | GAP-0552 | 18 | Confirm RWB-P1-DM002-APP as rework of withdrawn RWB-DM-002: read path only, no extract, load, reconciliation or cutover; TC-DM-002-01 and TC-DM-002-04 carry new text. |

### RWB-P1-E1069-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02459 | RWB-P1-DM002-APP | GAP-0553 | 11 | Fix the read-path answer as the customer fields of v_ace_customer, one row per contact_key of v_ace_contact, one row per account of v_ace_ca_relation, party_ext flags as an optional object, and consent and quality per contact row; absent object for no extension row. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02460 | RWB-P1-DM002-APP | GAP-0554 | 11 | Record that the masking answer for ACE-sourced fields is taken by rwb-source-data on the rwb-access authorise decision; add the contract dependency at the next plan revision. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02461 | RWB-P1-DM002-APP | GAP-0556 | 18 | Record RWB-P1-E1069-APP and RWB-P1-E1069-DB as preconditions without an H edge; publish the answer schema in the RWB-P1-E1069-APP contract; fix the read-path switch key in the Service Template Specification. |

### OTHER:Legacy RWB-DM-005 data row and DP05 catalog definition (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02462 | RWB-P1-DM002-APP | GAP-0528 | 8 | The DM-005 cutover load writes the legacy consent and contact-quality rows into contact_point_ext; the DP05 catalog keeps interaction as its only Workbench table. |

### OTHER:Template and Rules R5.7 rule 8 (Day-1 Work Allocation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02463 | RWB-P1-DM002-APP | GAP-0555 | header | State that Ready to start is computed from the dependency graph only; a wave 4 business-epic story may be picked up on Day 1 when its build edges are platform contracts; the wave tag stays the business epic tag. |

### OTHER:rwb-case contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02466 | RWB-P1-DM003-APP | DOR-RWB-P1-DM003-APP-22 | Header | Publish the contract fake library version and record it as published; no version is recorded in the source documents. |

### OTHER:P3 screen SCR-44 (P3 document) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02470 | RWB-P1-DM003-APP | DOR-RWB-P1-DM003-APP-10 | 15 | Section 15 lists the empty, loading, error and no access states. |

### OTHER:plan/split_plan.json; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02474 | RWB-P1-DM003-APP | GAP-0240 | header | Slice RWB-P1-DM003-APP into the wave of its owning service in the order of section 9.5, keeping releases 30 November 2026 and 31 December 2026 and reading them as the latest date. |

### RWB-P1-DM005-APP; 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02481 | RWB-P1-DM005-APP | DOR-RWB-P1-DM005-APP-21 |  | Record item 21 as Pass only when RWB-PLT-E1044-CON and RWB-PLT-N001-CON reach Done; the story already names both as build dependencies. |

### OTHER:P1 API yaml for rwb-source-data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02502 | RWB-P1-DM007-APP | GAP-2170 | 11, 13 | Add API-P1-003 as the call the cut-over pipeline makes, as the proposed fix states. Story side: sign-off and window placed in release pipeline cut-over record; API-P1-002, -003, -010 named. |

### OTHER:Contract fake library (published fake version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02506 | RWB-P1-DM008-APP | DOR-RWB-P1-DM008-APP-22 | header | Record the published contract fake library version for this story's contract. |

### RWB-P1-DM007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02513 | RWB-P1-DM008-APP | GAP-2170 | find it | Adopt the proposed fix: one dump read, one package per owner per cut-over business date to S4, P6 and S9, with the ten clean days counted from reconciliation_result rows. |

### RWB-ITG-DM008-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02514 | RWB-P1-DM008-APP | GAP-0536 | 4 | Correct the two sentences in section 1 and section 19 that say the cutover load into rwb_partner is P1's own migration on P1's own Flyway sequence; restate as handover to rwb-partner loaded on S9's sequence. |

### OTHER:FSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02515 | RWB-P1-DM008-APP | GAP-2172 | 8 | Restate the DP08 row in A2.2.2 with rwb-partner as owner of partner, partner_user and partner_instruction, a pointer to the S9 contract, and a closed handover field list. |

### OTHER:Squad refinement (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02517 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-16 | Header | Size row added, marked Not specified in the source documents. |

### RWB-P1-E1001-APP; RWB-P1-E1069-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02526 | RWB-P1-DM009-APP | DOR-RWB-P1-DM009-APP-17 | Header | Complete the build of RWB-P1-E1001-APP and RWB-P1-E1069-APP before this story starts. |

### RWB-ITG-DM009-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02528 | RWB-P1-DM009-APP | GAP-0537 | 8 | Replace the statement that P1's own cutover migration loads the lot and account records with: rwb-debtsale loads them on its own Flyway sequence from P1's handover package. |

### RWB-PLT-E1044-CON; RWB-PLT-N001-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02530 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-21 | header | Complete and publish both CON stories (not Done). Add GET /admin/reconciliation/results (API-P1-003), read by this story, to rwb-source-data.yaml; no match found in v5. |

### OTHER:P3 screen specification for SCR-44 and SCR-45 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02535 | RWB-P1-DM010-APP | DOR-RWB-P1-DM010-APP-10 | 9 | Screen states belong to the screen specification. State rows added in section 15 under CG-ALL-1962 and CG-ALL-1963 mark the gaps as Not specified in the source documents. |

### OTHER:Case state model and stories of rwb-case (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02551 | RWB-P1-DM011-APP | NEWAC-RWB-P1-DM011-APP-AC6 |  | This story changes no case status and writes no rwb_case row (BR1), so a refused transition cannot be tested here. No AC6 or test row added. |

### 06 Data/Recovery Workbench Source to Target Mapping v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20504 | RWB-P1-ACE001-DB | R-28940 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |

### 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20550 | RWB-P1-DM005-APP | R-04265 |  | Pass record for item 21 belongs to the readiness record of RWB-P1-DM005-APP. Needs RWB-PLT-E1044-CON and RWB-PLT-N001-CON at Done, which no source here establishes. |

### 04 User stories/Recovery Workbench Data Migration Stories v3.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20594 | RWB-P1-DM002-APP | R-28406 |  | The RWB-DM-005 data row already lists contact_point_ext. The DP05 catalog definition belongs elsewhere. Checked the v3.md mirror; docview not run. |

### 04 User stories/Recovery Workbench Data Migration Stories v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20599 | RWB-P1-DM001-APP | R-28948 |  | Item note keeps the legacy title here (§R5.2). Read-path deliverable already stated in section 1 (change log, Feature, read contract). Story key unchanged. |

### 11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20622 | RWB-P1-AD019-OPS | R-21789 |  | Blocked: no Bash tool here, so docview.py could not run and the .docx text (v4) could not be read. Re-run with Bash access to confirm wave 4 text. |

### 04 User stories/Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20623 | RWB-P1-DM002-APP | R-29040 |  | Rule text is Template and Rules R5.7 rule 8, not in this workbook (sheets Realignment v5 and Defects). Header already reads Day 1. No change here. |

### 05 Technical architecture/Recovery Workbench Interface Specifications v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20891 | RWB-P1-ACE001-DB | R-22947 |  | Needs an edit to the INT-21 Approach cell, but the v4 xlsx could not be read in this run (no shell or xlsx reader), so the current value is unverified (GAP-2001). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0214 | Eighty rows carry the legacy key RWB-ACE-001 in the Status cell | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0235 | Version 3 gives one recovery schema, not the target schema of each table | Data architecture team | Resolved (directive) |
| GAP-0236 | The owner-side migration step has no story ID | TechX | Resolved (directive) |
| GAP-0237 | Version 3 has the Workbench run the load; the target makes the schema owner run it | TechX | Resolved (directive) |
| GAP-0239 | The expected-return and sale-estimate records have no table and no schema | Data architecture team | Resolved (directive) |
| GAP-0240 | All 14 migration stories are wave 4 while nine services are wave 1 | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0241 | No retention period and no owner for the legacy Workbench tables after cutover | Data steward | Resolved (directive) |
| GAP-0242 | The custody of migrated document originals is not assigned | TechX | Resolved (directive) |
| GAP-0243 | The target table of the open promises and contact notes is not named | Data architecture team | Resolved (directive) |
| GAP-0244 | Contact points and consent have no named operation in the rwb-source-data contract | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0245 | No write operation is defined for party_ext and contact_point_ext under the single-writer rule | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0246 | v_ace_ca_relation has no named consumer or operation in Architecture v5 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0247 | The match-rule narrative still assumes a customer row lands in the Workbench | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0249 | The label Workbench no longer identifies an owner in a 19-service design | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0250 | The statement 'there is no local party or contact_point table' conflicts with the two extension tables | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0268 | The nine reconciliations name one Workbench side, but that side sits in seven service schemas | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0269 | No reconciliation and no quality measure carries an owner | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0271 | No per-service reconciliation rule, cadence or result route | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0440 | The job read, the rerun answer, the job-log fields, the freshness answer, the v_ace_batch_status read path and the two refusal messages of the interface and job monitor are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0441 | The data quality console read shapes, the gateway-bff route specification, the refresh cadence and the unreachable-read message are not stated in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0443 | The cutover reconciliation harness pack for case and ownership is not specified | Integration lead | Resolved (directive) |
| GAP-0444 | The cutover reconciliation harness pack for treatment and offers is not specified | Integration lead | Resolved (directive) |
| GAP-0445 | The cutover reconciliation harness pack for contact and promises is not specified | Integration lead | Resolved (directive) |
| GAP-0446 | The cutover reconciliation harness pack for collateral and assets is not specified | Integration lead | Resolved (directive) |
| GAP-0447 | The cutover reconciliation harness pack for legal events and cases is not specified | Integration lead | Resolved (directive) |
| GAP-0448 | Wave 4 partner performance harness environment, fixtures, break-list fields and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0449 | The cutover reconciliation harness pack for debt sale is not specified | Integration lead | Resolved (directive) |
| GAP-0450 | The cutover reconciliation harness pack for documents and extracted fields is not specified | Integration lead | Resolved (directive) |
| GAP-0451 | The cutover reconciliation harness pack for scores and route economics is not specified | Integration lead | Resolved (directive) |
| GAP-0514 | The response shapes of the job read, the rerun answer and the freshness answer are not specified | Tech lead | Resolved (directive) |
| GAP-0515 | job_catalog is P2 rwb-integration while the job read is P1 rwb-source-data | Solution architect | Resolved (directive) |
| GAP-0516 | SCR-44 is a gateway-bff route on a P1 story that builds no screen | DevOps lead | Resolved (directive) |
| GAP-0517 | The ACE migration version and the interface numbers of the 14 ingestion jobs are not specified for the target | ACE team lead | Resolved (directive) |
| GAP-0518 | The legacy grant names the monolith service role, the target names ace_view_owner and 19 logins | ACE DBA | Resolved (directive) |
| GAP-0519 | The shape of the reconciliation read and of the REC-05 break list is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0520 | DP-10 is listed on the P1 slice while JOB-04 is an event-started workflow and the freshness Schedule is rwb-case's | Solution architect | Resolved (directive) |
| GAP-0521 | The case and ownership tables are P3's while the legacy migration and its AC1 and AC3 sit on the P1 slice | Solution architect | Resolved (directive) |
| GAP-0522 | The source, format and evidence of the legacy Workbench extract and of the cutover sign-off are not specified | Data steward | Resolved (directive) |
| GAP-0523 | The treatment table is S2's and the DP04 copy is P1's, while the legacy migration and its AC1 and AC3 sit on the P1 slice | Solution architect | Resolved (directive) |
| GAP-0524 | The treatment extract format and the carrying of the plan reference are not specified beyond AC1 | Data steward | Resolved (directive) |
| GAP-0526 | The cutover extract format, the cutover record and the field list beyond the AC wording are not specified | Data steward | Resolved (directive) |
| GAP-0527 | The legacy interaction carries person_key and contact_key while the ledger table has party_id and contact_point_id and no P1 DDL | Data architect | Resolved (directive) |
| GAP-0528 | contact_point_ext is DP02's Workbench table in the FSD while the legacy DM-005 data row and this cutover slice carry it | Data steward | Resolved (directive) |
| GAP-0529 | The rows of the legacy migration are split across P1 and S5, the case asset link has no table in the target, and no single source gives the extract, handover or field list | Solution architect with the data steward and the S5 rwb-asset tech lead | Resolved (directive) |
| GAP-0530 | No source defines a clean day for a WEEKLY product, or where the ten day count and the sign-off are kept | Data steward with the P1 reconciliation owner and the release manager | Resolved (directive) |
| GAP-0531 | The valuation_key proof and the DP06 freshness read depend on Section B views that ship with RWB-ACE-001, and no source says how the cutover behaves before that week | Solution architect with the ACE team lead and the data steward | Resolved (directive) |
| GAP-0532 | Three services own the legal action, notice and instruction rows of one legacy key, and no source fixes the handover package format or which keys travel beyond the legacy AC wording | Solution architect | Resolved (directive) |
| GAP-0533 | partner_instruction sits in the data table of two legacy keys and no source rules which facts each migration slice carries | Data steward | Resolved (directive) |
| GAP-0534 | The ten clean days, the sign-off record, the read-only window and the feature-switch default are stated as outcomes and fixed by no source | Data steward | Resolved (directive) |
| GAP-0536 | RWB-ITG-DM008-ITG states that the cutover load into rwb_partner runs on P1's own Flyway sequence, which DP-01 and the Ownership Map forbid | Solution architect with the S9 rwb-partner and P1 rwb-source-data tech leads | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0537 | debt_sale_lot and debt_sale_account are S6's while the legacy migration and its AC1 and AC3 sit on the P1 slice, and no source says who loads | Solution architect | Resolved (directive) |
| GAP-0538 | The extract and handover formats, the field list beyond AC1, the ON_CHANGE recency proof and the ten-day record are not specified beyond the AC wording | Data steward | Resolved (directive) |
| GAP-0540 | document and document_field are P5's while the legacy document extract and its AC1 and AC3 sit on the P1 slice, and no source gives the extract's source, format or handover | Solution architect | Resolved (directive) |
| GAP-0541 | The route code sits on the case (P3), the baseline measure snapshots with rwb-reporting (P9) and the case list row with P1, and no source says which side keeps, loads or freezes each of them at cutover | Solution architect | Resolved (directive) |
| GAP-0546 | The legacy key is withdrawn while the Work Package still asks for an APP story under the legacy title | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0547 | The account and arrears read path is given as a legacy row, not as a deliverable with an answer shape or a cut-off | Tech lead | Resolved (directive) |
| GAP-0548 | A Day-1 story is tagged wave 4 while its service is wave 1 and the account read is needed by the wave 1 case screens | Tech lead | Resolved (directive) |
| GAP-0549 | The account operation named by the architecture is absent from the TSD P1 endpoint inventory, and the answer field names are in no module specification | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0550 | The withdrawn migration's file name and its test text are held by no source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0551 | The role RW-CUSTSERV named for this story is held by no source | Business analyst | Resolved (directive) |
| GAP-0552 | The legacy key is Removed by D-RCV-35 (U1) while the Work Package still asks for an APP story under it, so the story states a withdrawal and a build in one document | Recovery tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0553 | The read path that replaces the migration is described in one legacy row only: no source fixes the fields the answer carries, the join of a person to many contact points, or the use of the two extension tables beyond their column list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0554 | Where the masking of the ACE-sourced personal fields is answered is fixed in another service's story, while this story may declare no contract dependency and no masking pattern | Solution architect | Resolved (directive) |
| GAP-0555 | A wave 4 story is marked Ready to start Day 1 on a platform Flyway contract, and the readiness rule does not name the case | Programme manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0556 | The read operation, its request and answer field names, and the feature switch of the read path are owned elsewhere or named by no source, while the story must still build and be switched | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0570 | The number of Tier 1 ACE tables is 21 in legacy RWB-E1-069 and 22 in FSD P1 and TSD P1, and the grant list is enumerated only in the legacy story | ACE team lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0574 | The ALS batch gate before RWB-ACE-001 lands: v_ace_batch_status is a Section B view, and the behaviour of an entry read for a date whose batch record does not exist yet is not specified | Recovery tech lead with the ACE team lead and the platform team that owns the RWB-ACE-001 sequence | Resolved (directive) |
| GAP-0579 | No source names what the proof-of-delivery read answers before RWB-ACE-001 deploys the Section B views, nor the flag that holds it: the sources require the feature to stay behind a flag and the product to show stale, and give neither the answer shape, the reason code nor the flag name | Solution architect | Resolved (directive) |
| GAP-0596 | How the read answers the three Section B columns, and which flag holds it back, is stated nowhere | Data architect | Resolved (directive) |
| GAP-0662 | rwb-integration customer products read: login, contract field names, ACE view owner, endpoint and route names, masking rows and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0728 | RWB-AD-019 in rwb-case: login name, edge composite route, source-data read shape and contract placement not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0777 | The rwb-access login name, the ACE group source behind a mapping row and the column set of the three library objects are not specified for the schema slice | ACE database engineer with the rwb-access service owner and the P1 data owner | Resolved (directive) |
| GAP-0896 | rwb-access sandbox seed: the owner, the key format and the retirement rule of the DEV synthetic test identity per role are not specified | Platform administrator | Resolved (directive) |
| GAP-0980 | role.entra_group is a column in the technical specification and not a Workbench column in the functional one | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1165 | The retired inbound load leaves TC-E1-007-05, TC-E1-007-06 and the file checks DQ-057 and DQ-059 without a target in this service | Business analyst and QA lead | Resolved (directive) |
| GAP-1505 | The Section B views and every Tier 2 feature depend on ACE additions that the ACE team has not accepted | ACE team lead | Resolved (directive) |
| GAP-1507 | No freshness source is named for the period before the ACE batch record exists | Solution architect | Resolved (directive) |
| GAP-1557 | DL43 is open: the ACE Tier 2 tables, columns and fields are not accepted, so dependent P3 features stay behind flags | ACE team lead | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-2001 | INT-21 reads the group-to-role mapping through v_ace_iam_group, which only rwb-source-data may read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2008 | INT-35 and INT-36 name no consuming service | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2101 | Two rows read the ACE table ace_batch_run, which ADR-010 does not allow | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2162 | RWB-AD-018: the job run record, the outbound-action answer and the right-enforcement path are not named in the target sources | P1 tech lead with the data architect and the P4 access owner | Resolved (directive) |
| GAP-2163 | RWB-AD-018: the contract baseline has no field-level detail for the run element and its boundary with the freshness resource is not written down | P1 tech lead with the solution architect | Resolved (directive) |
| GAP-2164 | RWB-AD-018: the alert thresholds, the panel baselines and the per-environment values of the monitor are not in the sources | DevOps team with the platform observability owner | Resolved (directive) |
| GAP-2165 | RWB-ACE-001 database slice: the ACE migration version, the ingestion job identifiers and the grantee role name are not fixed in the sources | ACE team lead; ACE DBA; Recovery data architect | Resolved (directive) |
| GAP-2167 | listing and asset_sale have no owning schema in the P1 table list | Data architect; S5 rwb-asset technical owner | Resolved (directive) |
| GAP-2169 | Migration batch states and cutover evidence format are not specified | Solution architect | Resolved (directive) |
| GAP-2170 | The legal cut-over of RWB-DM-007 has no defined dump, no package format, no evidence store and no agreed API surface in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2171 | No source fixes the cutover mechanics of RWB-DM-008: the extract dump, the pipeline step, the cutover record, the ten-day evidence and the DM007 instruction slice | Solution architect | Resolved (directive) |
| GAP-2172 | The DP08 catalog row and the Ownership Map disagree on which service owns the partner tables of RWB-DM-008 | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2173 | Cutover mechanics of the debt sale migration are not specified | Data steward (RW-DATASTEW), with tech delivery | Resolved (directive) |
| GAP-2175 | The route code and state sit on the case (P3) and the baseline snapshots with rwb-reporting (P9) while only case_list_row is P1's, and no source gives the legacy dump's source or format, the handover locations, the retention period of the legacy tables or where the data steward's sign-off is held | Solution architect | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3239 | Version 3 is written for two squads, while D-RCV-60 works by five team types across 19 services | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
