# RWB-SVC-P1 rwb-source-data (Source data) - review pack, part 2 of 7 (RWB-P1-DM012-APP to RWB-P1-E1011-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 9 |
| Resolved in the stories | 184 |
| Cross-document (pending in another document) | 255 |
| Not applied (value not in the sources) | 12 |
| Open business decisions | 14 |
| Register gaps linked | 123 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P1-DM012-APP | 23 | 6 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM012 APP Migrate decision log v2.md |
| RWB-P1-DM013-APP | 15 | 8 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM013 APP Migrate money and closure v2.md |
| RWB-P1-DM014-APP | 13 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM014 APP Migrate reference data v2.md |
| RWB-P1-E1001-APP | 35 | 59 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1001 APP Recovery tables for the 14 data products v2.md |
| RWB-P1-E1002-APP | 25 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1002 APP Case list v1 with case ID, owner and queue v2.md |
| RWB-P1-E1002-CON | 14 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1002 CON Case list v1 with case ID, owner and queue - contract v2.md |
| RWB-P1-E1002-OPS | 12 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1002 OPS Case list v1 with case ID, owner and queue - deployment v2.md |
| RWB-P1-E1011-APP | 31 | 49 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1011 APP Reconciliation and data quality report v2.md |
| RWB-P1-E1011-CON | 16 | 43 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1011 CON Reconciliation and data quality report - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P1-DM012-APP | R-09640 | CG-ALL-1976 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-DM013-APP | R-09643 | CG-ALL-1985 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1002-APP | R-09664 | CG-ALL-2024 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P1-E1002-APP | R-09665 | CG-ALL-2027 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21843 | GAP-0001 | Register gap | Product Owner | Arch v5 waves have no release dates | Keep the dates unchanged and tentative, map waves 0-1 to Release 1 at the plan gate, and confirm the mapping in the verification loop |
| RWB-ITG-E1001-ITG, RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP | R-21856 | GAP-0977 | Register gap | Data steward and data product owner (RW-DATASTEW) | The dictionary rows of the five rwb_access tables have no seeding owner after the split | Declare the 44 business rows as a build artefact of this story, hand the declaration to the one dictionary's seed in rwb_source_data, and let the seed carry the 35 standard-column rows under its own Field IDs. Cite the 44 business Field IDs only. |
| RWB-ITG-E1002-ITG, RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1002-OPS, RWB-P3-E1002-APP | R-21871 | GAP-1502 | Register gap | Product owner | The case list is split between this service and the case service, while the FSD gives screen and rows to one module | This service builds and publishes one row per case account per business date and holds the publication status; rwb-case serves the case list screen and its filters over those rows; the reconciliation and the hold stay here. Agree the split at the Epic 1 story review. |
| RWB-ITG-E1011-ITG, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21922 | GAP-1651 | Register gap | Data steward and data product owner | The reconciliation and the data quality break are P1's, but FSD P9 specifies them as its own features | Read the reconciliation result and the break rows from P1's contract and hold the break view and the closure in P9 |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E2001-ITG, RWB-P1-E1011-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-P7-E2001-APP | R-22306 | GAP-0591 | Register gap | Data steward and data product owner, P1 | The REC-05 break list row for a hand-over key is defined only for keys on an existing Workbench table, not for a candidate that has no row yet | Answer the break in the candidate-facts read as {check: REC-05, keyType: PERSON_KEY or ACCOUNT_KEY, key: <value>} with resolution HELD, write no row and invent no fact, and let RWB-P1-E1011-APP's REC-05 step carry the row for the business date so the data steward and the ACE team read one list. Fix the answer in RWB-P2-E2001-CON. |
| RWB-ITG-DM012-ITG, RWB-P1-DM012-APP | R-28412 | GAP-2177 | Register gap | Data steward and data product owner | The legacy decision-log extract's source, format and location, the retention period of the legacy tables and the place that holds the sign-off are not specified | Take the extract from the legacy Workbench cutover dump of the release pipeline, name its format and location in the cutover plan, take the retention period from the retention class of the record class in retention_rule, and hold the sign-off in the cutover record. |
| RWB-P1-E1002-APP | R-33392 | ASM-ALL-2027 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-P1-DM012-APP | R-35751 | ASM-3512 | Register assumption |  | decision_log_entry is P7's, so RWB-P1-DM012-APP reads the legacy entries once at cutover, records each one as a local decision record plus its outbox row in rwb_source_data through RWB-PLT-E1027-CON, and publishes DecisionRecorded on rwb.decision-record.v1 for rwb-decision to seal into the central ledger; nothing is handed over as a file and no decision_log_entry row is written by P1. | Solution architect and the rwb-decision technical owner at the wave-4 contract review |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P1-DM013-APP | R-04305 | DOR-RWB-P1-DM013-APP-16 | header | Definition of Ready item 16 Size: Fail | No size in the sources. Size row added as Not specified; squad sizes at refinement. |
| RWB-P1-DM013-APP | R-04308 | DOR-RWB-P1-DM013-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version in the sources; only the /v1 path is stated. Contract version row added as Not specified. |
| RWB-P1-DM013-APP | R-14932 | DOR-RWB-P1-DM013-APP-2 | 18 | Definition of Ready item 2 Links: Partial | No feature or L3 process value for RWB-DM-013 in the md sources; a grep for L3 process and Feature with RWB-DM-013 returned only other stories. Adding columns would need placeholders in all 21 rows, so no edit. |
| RWB-P1-DM013-APP | R-21836 | GAP-0453 | 7 | The wave 4 cutover reconciliation harness pack for money and closure is not specified | Harness pack contents are Not specified in the source documents; the AC2 paragraph states that and claims no agreement or owner. |
| RWB-P1-DM014-APP | R-04310 | DOR-RWB-P1-DM014-APP-16 | header | Definition of Ready item 16 Size: Fail | No size is in the source documents; the item stays open until the story is sized. |
| RWB-P1-E1001-APP | R-04315 | DOR-RWB-P1-E1001-APP-16 | section header | Definition of Ready item 16 Size: Fail | No size value is in the sources; the item stays open until the story is sized. |
| RWB-P1-E1001-APP | R-21863 | GAP-2539 |  | DP13 Money and closure is catalogued with the system of record ACE only, while the match on the same row is a Workbench record | No story edit kept. The DP13 seed row in section 13 was not checked; it must be reviewed before this item can be closed. |
| RWB-P1-E1002-CON | R-04326 | DOR-RWB-P1-E1002-CON-16 | Header | Definition of Ready item 16 Size: Fail | Added a Size row that states the size is not in the source documents. The item stays open until the squad sizes the story at refinement. |
| RWB-P1-E1002-CON | R-14967 | DOR-RWB-P1-E1002-CON-7 | 11 | Definition of Ready item 7 Data: Partial | No BR Field ID for Job, Consumed event, rowCount or page number/size. Searched 05 Technical architecture (API yaml, Service Catalog, Event Design); placeholders kept. |
| RWB-P1-E1002-OPS | R-04330 | DOR-RWB-P1-E1002-OPS-16 | header | Definition of Ready item 16 Size: Fail | The header records Size as not specified in the source documents. No value is invented; the readiness item stays open until the squad sizes the story. |
| RWB-P1-E1011-CON | R-04341 | DOR-RWB-P1-E1011-CON-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the story or the source .md files. Header row now records it as not specified. Sign-off needs the epic design record. |
| RWB-P1-E1011-CON | R-04342 | DOR-RWB-P1-E1011-CON-16 | header | Definition of Ready item 16 Size: Fail | Header Size row added, recording that the size is not specified and the squad sizes the story at refinement. No size value invented, so the item stays open until then. |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Source to Target Mapping v5.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20498 | RWB-P1-E1001-APP | R-21850 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |
| CDC-20501 | RWB-P1-E1001-APP | R-21851 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |
| CDC-20502 | RWB-P1-E1001-APP | R-28425 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |
| CDC-20503 | RWB-P1-E1001-APP | R-21849 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |
| CDC-20505 | RWB-P1-E1001-APP | R-28424 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21849', 'R-21850', 'R-21851', 'R-28423', 'R-28424', 'R-28425', 'R-28449', 'R-28940'] |
| CDC-20506 | RWB-P1-E1001-APP | R-28426 |  | Mapping v5 DP06 row could not be read with the permitted tools (no Bash/docview access). No exact old text, so no fix written. Needs a fix in a later run. |
| CDC-20507 | RWB-P1-E1001-APP | R-28427 |  | Mapping v5 DP07 row could not be read with the permitted tools. No exact old text, so no fix written. Needs a fix in a later run. |
| CDC-20508 | RWB-P1-E1001-APP | R-28428 |  | Mapping v5 DP13 row could not be read with the permitted tools. No exact old text, so no fix written. Needs a fix in a later run. |
| CDC-20509 | RWB-P1-E1001-APP | R-28429 |  | Mapping v5 DP05 row could not be read with the permitted tools. No exact old text, so no fix written. Needs a fix in a later run. |
| CDC-20510 | RWB-P1-E1001-APP | R-28430 |  | Mapping v5 DP14 row could not be read with the permitted tools. No exact old text, so no fix written. Needs a fix in a later run. |
| CDC-20511 | RWB-P1-E1001-APP | R-28431 |  | Ownership split basis cell could not be read with the permitted tools. No exact old text, so no fix written. Needs a fix in a later run. |
| CDC-20512 | RWB-P1-E1001-APP | R-28432 |  | Roles, Change process and Quality measures sheets could not be read with the permitted tools. No fix written. Needs a fix in a later run. |
| CDC-20513 | RWB-P1-E1001-APP | R-28433 |  | Ownership and Ownership split cells could not be read with the permitted tools. No exact old text, so no fix written. Needs a fix in a later run. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02556 | RWB-P1-DM012-APP | CG-ALL-1975 | 16 | The Story test cases tab has no row for TC-DM-012-01, 03, 04 or 05; the new TC-DM-012-06 and TC-DM-012-07 must be added with them. |
| CDC-02557 | RWB-P1-DM012-APP | DOR-RWB-P1-DM012-APP-12 | 16 | Test Cases v8 Story test cases needs TC-DM-012-01, 03, 04 and 05, and also the new rows TC-DM-012-06 and TC-DM-012-07. |
| CDC-02562 | RWB-P1-DM013-APP | CG-ALL-1984 | 16 | Add rows for TC-DM-013-01, TC-DM-013-03 and TC-DM-013-04 with Given, When and Then from the criteria they cover |
| CDC-02563 | RWB-P1-DM013-APP | DOR-RWB-P1-DM013-APP-12 | 16 | Add rows for TC-DM-013-01, TC-DM-013-03 and TC-DM-013-04 with Given, When and Then from the criteria they cover |
| CDC-02571 | RWB-P1-DM014-APP | CG-ALL-1989 | 16 | Add rows TC-DM-014-01 to TC-DM-014-04 with Given, When and Then copied from the criteria they cover |
| CDC-02573 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-12 | 16 | Add rows TC-DM-014-01 to TC-DM-014-04 with Given, When and Then copied from the criteria they cover |
| CDC-02588 | RWB-P1-E1001-APP | CG-ALL-2009 | 16 | Add row TC-E1-001-12: Given a catalog file with DP06 naming "CCMS"; When the reference data administrator loads it; Then MSG-P1-003 refusal, no row written (AC11). Also add rows TC-E1-001-13 to -16. |
| CDC-02673 | RWB-P1-E1002-CON | CG-ALL-2036 | 16 | v8 maps tests to criteria numbered up to AC10, but section 7 does not have AC8 to AC10. The story keeps the mapping to its own criteria; v8 needs realigning. |
| CDC-02691 | RWB-P1-E1002-OPS | CG-ALL-2045 |  | The Test Cases v8 AC mapping does not match this story's criteria. The story keeps its own TC-to-AC mapping; QA aligns Test Cases v8. |
| CDC-02703 | RWB-P1-E1011-APP | CG-ALL-2058 | 16 | Add rows TC-E1-011-08 (Covers BR5, BR13; party_ext person_key P0099881 absent from v_ace_customer) and TC-E1-011-09 (Covers AC8, BR12; v_ace_account stub error after MORTGAGE count) with Given, When and Then copied from the criteria they cover. |
| CDC-02728 | RWB-P1-E1011-APP | CG-ALL-2059 | 16 | The workbook maps TC-01 and TC-04 to AC1 and AC4, which are not in this story. Story keeps AC5 and AC8; TC-02 covers AC9. |
| CDC-02771 | RWB-P1-E1011-CON | CG-ALL-2070 | 16 | Add rows for TC-E1-011-08 (AC2, AC7) and TC-E1-011-09 (AC3, AC5) with Given, When and Then copied from the criteria they cover. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02593 | RWB-P1-E1001-APP | GAP-0100 | n/a | List each of the 156 operations under its owning service and Architecture v5 base path; final path and payload per API Specification v5. |
| CDC-02595 | RWB-P1-E1001-APP | GAP-0109 | n/a | Set outbox_event, outbox_delivery, processed_event and idempotency_key to each of the 19 service schemas with no business foreign key; feature_flag and feature_flag_change once in rwb_integration.sql. |
| CDC-02600 | RWB-P1-E1001-APP | GAP-0225 |  | Record S2 as owner of the live treatment record; name S3 and P1 in the basis cell; keep DP04 whole. |
| CDC-02601 | RWB-P1-E1001-APP | GAP-0228 |  | Add rows for the rwb_valuation tables (valuation, route decision, route agent output) owned by S1 rwb-valuation. |
| CDC-02616 | RWB-P1-E1001-APP | GAP-0108 |  | Assign owner S1 to valuation_ext and the route-economics tables, or record the ASM-A6-tables-15 exception, so rwb-valuation owns at least one table. |
| CDC-02619 | RWB-P1-E1001-APP | GAP-0202 |  | Give all 30 recovery.v_ace_* views owning service P1 and target schema 'recovery (ACE, read-only view)' per Architecture v5; add a Views sheet to the map. |
| CDC-02620 | RWB-P1-E1001-APP | GAP-0212 |  | In the By source sheet, set the ACE table(s) cell of the extension-field row to rwb_source_data.party_ext; leave the 1/0/0/1 counts and the Total row unchanged. |
| CDC-02731 | RWB-P1-E1011-APP | GAP-0272 |  | Add the Template and Rules R9 tolerance placeholder to the ten owner rows (P2, P4, P5, P10, S1, S3, S4, S6, S8, S9). No tolerance value is set. |
| CDC-02732 | RWB-P1-E1011-APP | GAP-0274 |  | Keep rwb-valuation as owner of S1, state the Arch v5 capability (valuations, D6 route decision, route agent output), and carry the R9 placeholder until a table is listed. |
| CDC-02775 | RWB-P1-E1011-CON | GAP-0274 |  | Keep rwb-valuation as S1 owner, state the capability Arch v5 gives it, and carry the Template and Rules R9 placeholder until the Ownership Map lists a table for it. |
| CDC-02779 | RWB-P1-E1011-CON | GAP-1173 |  | Add the Platform administration area with right R for the two quality reads and the gateway-bff route; the case notice read keeps Litigation R with scope |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02640 | RWB-P1-E1002-APP | CG-ALL-2014 | 12.1 | Publish GET /api/recovery/source-data/v1/case-list/dates/{businessDate} with the answer shape in story section 12.1, through the RWB-P1-E1002-CON story. |
| CDC-02641 | RWB-P1-E1002-APP | CG-ALL-2015 | 12.1 | Publish GET /api/recovery/source-data/v1/case-list/rows with the answer shape in story section 12.1, through the RWB-P1-E1002-CON story. |
| CDC-02657 | RWB-P1-E1002-CON | CG-ALL-2028 | 12.1 | Publish GET /api/recovery/source-data/v1/case-list/dates/{businessDate} through the rwb-source-data CON story. |
| CDC-02658 | RWB-P1-E1002-CON | CG-ALL-2029 | 12.1 | Publish GET /api/recovery/source-data/v1/case-list/rows through the rwb-source-data CON story. |
| CDC-02693 | RWB-P1-E1011-APP | CG-ALL-2050 | 12.1 | Publish operation GET /admin/reconciliation/results through RWB-P1-E1011-CON, as the story already states. |
| CDC-02694 | RWB-P1-E1011-APP | CG-ALL-2051 | 12.1 | Publish operation GET /admin/reconciliation/results/{resultId} through RWB-P1-E1011-CON, as the story already states. |
| CDC-02695 | RWB-P1-E1011-APP | CG-ALL-2052 | 12.1 | Remove the closed enum on result and declare it as data validated against LOV-REC-RESULT, per the story's reading of the LOV as data. |
| CDC-02742 | RWB-P1-E1011-CON | CG-ALL-2063 | 12.1 | Publish GET /admin/reconciliation/results (base /api/recovery/source-data/v1) as an operation in rwb-source-data.yaml, per this CON story. |
| CDC-02743 | RWB-P1-E1011-CON | CG-ALL-2064 | 12.1 | Publish GET /admin/reconciliation/results/{resultId} (base /api/recovery/source-data/v1) as an operation in rwb-source-data.yaml, per this CON story. |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02552 | RWB-P1-DM012-APP | DOR-RWB-P1-DM012-APP-14 | header | Record the signed epic design sign-off for EP08 (RWB-SVC-P1) in the epic design record |
| CDC-02558 | RWB-P1-DM013-APP | DOR-RWB-P1-DM013-APP-14 | header | Record the signed epic design sign-off for EP08 |
| CDC-02566 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-14 | header | Confirm and record the signed epic design sign-off for EP08 |
| CDC-02581 | RWB-P1-E1001-APP | DOR-RWB-P1-E1001-APP-14 | header | Record the signed epic design sign-off for EP01 in the epic design record; the story cannot carry it. |
| CDC-02662 | RWB-P1-E1002-CON | DOR-RWB-P1-E1002-CON-14 |  | Record the signed epic design sign-off for this story's epic, then re-check DoR item 14. |
| CDC-02677 | RWB-P1-E1002-OPS | DOR-RWB-P1-E1002-OPS-14 | header | Record the signed epic design sign-off for RWB-P1-E1002-OPS in the epic design record. |
| CDC-02697 | RWB-P1-E1011-APP | DOR-RWB-P1-E1011-APP-14 | Header | Record the signed epic design sign-off for RWB-SVC-P1 in the epic design record. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02651 | RWB-P1-E1002-APP | CG-ALL-2020 | 12.5 | Add activity snapshot(page) on task queue rwb-source-data to the Activities sheet. |
| CDC-02665 | RWB-P1-E1002-CON | CG-ALL-2034 | 12.5 | Add activity snapshot(page) on task queue rwb-source-data to the Activities sheet. |
| CDC-02676 | RWB-P1-E1002-OPS | CG-ALL-2042 | 12.5 | Add row CaseListBuildWorkflow: rwb-source-data, queue rwb-source-data, one run per business date (ID = business date), started by AceDataReady and DailyCaseList 07:15 Asia/Bangkok (GAP-0487). |
| CDC-02696 | RWB-P1-E1011-APP | CG-ALL-2054 | 12.5 | Add a row for ReconciliationWorkflow: task queue rwb-source-data, namespace rwb-recovery, one run per business date. |
| CDC-02702 | RWB-P1-E1011-APP | CG-ALL-2055 | 12.5 | Add activity reconciliation on task queue rwb-source-data (namespace rwb-recovery) to the Activities sheet. |
| CDC-02744 | RWB-P1-E1011-CON | CG-ALL-2066 | 12.5 | Add a Workflows row for ReconciliationWorkflow on task queue rwb-source-data, or name the catalogued workflow that replaces it. |
| CDC-02747 | RWB-P1-E1011-CON | CG-ALL-2067 | 12.5 | Add an Activities row for reconciliation on task queue rwb-source-data. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02555 | RWB-P1-DM012-APP | CG-ALL-1973 | 11; 12 | Record flyway_schema_history as a framework table object with its fields, or name its dictionary entry (owner role Data) |
| CDC-02561 | RWB-P1-DM013-APP | CG-ALL-1980 | 12 | Record flyway_schema_history as a library object (index, table or flag) or add it to Fields, owner Data |
| CDC-02565 | RWB-P1-DM013-APP | GAP-2533 | 4 | Publish the handover file's count, checksum and resolution stamp format, location and retention; name the load command and its run record and rights; add a provenance and migration-date column to the next proceeds schema version; record the DP-15 split in the split plan. |
| CDC-02570 | RWB-P1-DM014-APP | CG-ALL-1987 | L214 | Record flyway_schema_history as a Flyway-managed object (index, library table or flag) or give its dictionary name |
| CDC-02604 | RWB-P1-E1001-APP | GAP-1280 |  | Build rule_row with the 21 fields its fields sheet lists. Drop rule_test_case.package_version_id. Keep approval.case_id and approval.delegation_limit_id as values with no foreign key. |
| CDC-02607 | RWB-P1-E1001-APP | GAP-2401 |  | Build rule_row with the 21 fields its fields sheet lists. Drop rule_test_case.package_version_id. Keep approval.case_id and approval.delegation_limit_id as values with no foreign key. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02564 | RWB-P1-DM013-APP | DOR-RWB-P1-DM013-APP-7 | 11 | Add `flyway_schema_history` as an entity or field (the per-service Flyway history written by RWB-PLT-E1044-CON), or state that it sits outside the data model. |
| CDC-02575 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-7 | 11 | Section 11 paragraph states the owner schema for the three tables |
| CDC-02585 | RWB-P1-E1001-APP | CG-ALL-1994 | 13 | Confirm loan_account is not a dictionary entity; the story names it only as a table it must not create. |
| CDC-02586 | RWB-P1-E1001-APP | CG-ALL-1995 | 13 | Confirm account_payment is not a dictionary entity; the story names it only as a table it must not create. |
| CDC-02587 | RWB-P1-E1001-APP | CG-ALL-1996 | 13 | Confirm contact_point is not a dictionary entity; the story names it only as a table it must not create. |
| CDC-02589 | RWB-P1-E1001-APP | DOR-RWB-P1-E1001-APP-7 | 11 | Confirm field DF-INT-038 exists in the LDM v9 Fields sheet for the interaction ledger, or correct the range in section 11 row 12 to the last LDM v9 field. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02642 | RWB-P1-E1002-APP | CG-ALL-2016 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{key} in rwb-case.yaml through the provider's CON story (RWB-P3-E1042-CON). |
| CDC-02643 | RWB-P1-E1002-APP | CG-ALL-2017 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/{lovCode} in rwb-case.yaml through the provider's CON story (RWB-P3-E1043-CON). |
| CDC-02659 | RWB-P1-E1002-CON | CG-ALL-2030 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{key} in rwb-case.yaml through the provider's CON story. |
| CDC-02660 | RWB-P1-E1002-CON | CG-ALL-2031 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/{lovCode} in rwb-case.yaml through the provider's CON story. |
| CDC-02674 | RWB-P1-E1002-OPS | CG-ALL-2039 | 12.2 | Publish GET /api/recovery/case/v1/parameters/{key} in rwb-case.yaml through the provider's CON story. |
| CDC-02675 | RWB-P1-E1002-OPS | CG-ALL-2040 | 12.2 | Publish GET /api/recovery/case/v1/reference-data/{lovCode} in rwb-case.yaml through the provider's CON story. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02610 | RWB-P1-E1001-APP | GAP-2061 | 1 | Add a per-service availability table of 19 rows applying the same two targets; write the shape of one service once; state the composed screen as the product of its called services within the one-hop budget. |
| CDC-02690 | RWB-P1-E1002-OPS | GAP-1991 |  | Keep lake_copy_watermark as the watermark of the last published reporting projection; drop lake extract INT-19 and INT-20 (DP-17). |
| CDC-02718 | RWB-P1-E1011-APP | GAP-1171 | n/a | Serve the quality facts from the rwb-reporting read model for wave 1; settle in wave 2 whether DP-09 and a platform event library story are added. |
| CDC-02734 | RWB-P1-E1011-APP | GAP-0337 |  | Add the three JOB-04 outbound reads to the rwb-source-data row. Publish the case-contract exclusion resource with its path, fields and 2 s budget. |
| CDC-02777 | RWB-P1-E1011-CON | GAP-0337 |  | Add the JOB-04 outbound reads to the rwb-source-data row; publish the exclusion resource on rwb-case with its path, fields and 2 s budget |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02612 | RWB-P1-E1001-APP | CG-ALL-2011 | 18 | Align the REQ-RDF-001 and REQ-RDF-014 test lists with section 18 in the next RTM version. |
| CDC-02656 | RWB-P1-E1002-APP | CG-ALL-2023 | 18 | RTM v7 is another workbook and must be aligned there. In section 18 of this story only the test case range was extended, to TC-E1-002-19. |
| CDC-02692 | RWB-P1-E1002-OPS | CG-ALL-2046 |  | Align the test lists for REQ-RDF-007, REQ-RDF-009 and REQ-DRI-007 with section 18 in the next RTM version. |
| CDC-02729 | RWB-P1-E1011-APP | CG-ALL-2060 | 18 | Align the test lists of REQ-RDF-007, REQ-RDF-008 and REQ-CWC-004 with RWB-P1-E1011-APP section 18 in the next RTM version. |
| CDC-02772 | RWB-P1-E1011-CON | CG-ALL-2072 | 18 | REQ-RDF-007 and REQ-RDF-008 test lists aligned; REQ-CWC-004 unchanged |

### RWB-P1-E1002-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02646 | RWB-P1-E1002-APP | DOR-RWB-P1-E1002-APP-21 | header | Build status to Done and the contract published for RWB-P1-E1002-CON; currently Not started. |
| CDC-02647 | RWB-P1-E1002-APP | DOR-RWB-P1-E1002-APP-22 | header | Record a published contract fake library version for RWB-P1-E1002-CON. |
| CDC-02678 | RWB-P1-E1002-OPS | DOR-RWB-P1-E1002-OPS-21 | header | The header records the contract dependency. The readiness item stays open until RWB-P1-E1002-CON is Done and the contract is published. |
| CDC-02679 | RWB-P1-E1002-OPS | DOR-RWB-P1-E1002-OPS-22 | header | Record the published contract fake library version for the v1 contract (/api/recovery/case/v1) in RWB-P1-E1002-CON. |
| CDC-02688 | RWB-P1-E1002-OPS | GAP-0335 |  | JOB-04 reads GET /api/recovery/case/v1/cases and GET /api/recovery/case/v1/queues/{queueId}/cases; daily extract goes via rwb-integration deliverFile with manifest, FileDelivered and FileFailed events, no lake path. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02650 | RWB-P1-E1002-APP | CG-ALL-2018 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1 in Events (EV-26), and add its ACL. |
| CDC-02664 | RWB-P1-E1002-CON | CG-ALL-2032 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1 in Events row EV-26, with its ACL. |
| CDC-02682 | RWB-P1-E1002-OPS | CG-ALL-2041 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1 with its ACL, or drop the handler |
| CDC-02701 | RWB-P1-E1011-APP | CG-ALL-2053 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1 (Events row EV-26) and add its ACL entry. |
| CDC-02746 | RWB-P1-E1011-CON | CG-ALL-2065 | 12.4 | Add rwb-source-data as a consumer of rwb.source-data.AceDataReady.v1 and add its ACL. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02720 | RWB-P1-E1011-APP | GAP-2232 | Header | Record that rwb-case owns the case-side facts of REC-01, REC-03 and REC-05 over its own tables, writes no reconciliation_result row and owns no legacy criterion; confirm the DP-table CONs are not build dependencies of this story. |
| CDC-02761 | RWB-P1-E1011-CON | GAP-1170 |  | Record that the reconciliation and data quality extracts and the INT-19 path are dropped for RWB-P6-E1011-APP, and that rwb-reporting reads quality facts from the service read model. |
| CDC-02762 | RWB-P1-E1011-CON | GAP-1171 |  | Keep DP-09 out for wave 1, serve quality facts from the service read model, and log the wave-2 decision on DP-09 and rwb-reporting reads. |
| CDC-02764 | RWB-P1-E1011-CON | GAP-2232 |  | Rule that the rwb-case slice owns the case-side facts of REC-01, REC-03 and REC-05 over rwb-case tables, writes no reconciliation_result row, and owns no legacy criterion; record the boundary. |
| CDC-02768 | RWB-P1-E1011-CON | GAP-2237 |  | Keep the link columns as account_key and person_key varchar business keys per the FSD re-base under D-RCV-35; record the uuid form of TSD P3 v3 as a pre-re-base artefact. |

### RWB-P8-E1001-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02633 | RWB-P1-E1001-APP | GAP-2534 | - | Name the primary key, the two indexes and the Field IDs of the seven standard columns at merge under the platform naming convention; the one dictionary seed carries those Field IDs. |
| CDC-02634 | RWB-P1-E1001-APP | GAP-2535 | - | Keep D-RCV-36 T10: match rules are rows of a rule package of rwb-decision; no payment_match_rule table is created in rwb_payment. |
| CDC-02635 | RWB-P1-E1001-APP | GAP-2536 | - | Index the unmatched list on matched_to and received_date and the case read on case_id and received_date; leave the screen field lists with the screen stories. |
| CDC-02636 | RWB-P1-E1001-APP | GAP-2541 |  | The conflict concerns the rwb-payment wave, not this rwb-source-data story. No edit here. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02576 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-9 | 14 | MSG-P3-027 row added with type and text marked Not specified. |
| CDC-02590 | RWB-P1-E1001-APP | DOR-RWB-P1-E1001-APP-9 | 14 | Section 4: allocate a new message ID for the bare source name case (AC11) with the story's English text and Thai text; MSG-P1-003 keeps the standard text. The story then adopts both. |
| CDC-02611 | RWB-P1-E1001-APP | CG-ALL-2008 | 14 | Business analyst adds a new message ID for the bare source name case (story text, AC11); MSG-P1-003 stays '{product} must have exactly one system of record and one named owner.' for its 'Raised when'. |

### OTHER:TSD P1 v3 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02655 | RWB-P1-E1002-APP | GAP-1991 | 8 | Keep lake_copy_watermark as the watermark of the last published reporting projection; remove the decision-log lake copy and INT-19 and INT-20 (DP-17). |
| CDC-02672 | RWB-P1-E1002-CON | GAP-1991 |  | Keep lake_copy_watermark as the watermark of the last published reporting projection; remove the decision log copy to the data lake; drop lake extract INT-19 and INT-20 (DP-17). |
| CDC-02759 | RWB-P1-E1011-CON | GAP-0496 |  | Keep REC-01, REC-02 and REC-05 over P1 tables only; REC-03 goes to RWB-P3-E1011-APP and RWB-S5-E1011-APP, REC-04 to RWB-P6-E1011-APP; remove those rows from the P1 module. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02666 | RWB-P1-E1002-CON | DOR-RWB-P1-E1002-CON-1 | 1 | Add the role 'tech lead' with a role code to the role list for rwb-source-data. |
| CDC-02684 | RWB-P1-E1002-OPS | DOR-RWB-P1-E1002-OPS-1 | 1 | Add 'platform engineer' as a role name in Users Roles and Permissions v5 |
| CDC-02748 | RWB-P1-E1011-CON | DOR-RWB-P1-E1011-CON-1 | 1 | Actor changed to solution architect and kept in the story |

### RWB-P1-E1011-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02698 | RWB-P1-E1011-APP | DOR-RWB-P1-E1011-APP-21 | Header | Move build status from Not started to Done, with the contract published. |
| CDC-02699 | RWB-P1-E1011-APP | DOR-RWB-P1-E1011-APP-22 | Header | Publish the contract fake library and record its published version. |
| CDC-02715 | RWB-P1-E1011-APP | GAP-0497 | 4 | Workflow ID marked Not specified in the source documents |

### OTHER:rwb-case service contract (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02722 | RWB-P1-E1011-APP | GAP-2234 | 12 | Publish the four case-side quality operations with Platform administration R, Reporting R and Platform administration U, the 400, 401, 403, 404, 409 and 503 problem set, and an Idempotency-Key on the rerun. |
| CDC-02766 | RWB-P1-E1011-CON | GAP-2234 |  | Publish the four case-side quality operations with their rights, the 400, 401, 403, 404, 409 and 503 problem set, and an Idempotency-Key on the rerun. |
| CDC-02767 | RWB-P1-E1011-CON | GAP-2236 |  | Expose GET /reconciliation/status on rwb-case returning RELEASED, HELD or NOT_RUN with the unexplained exclusion count per product group; the rwb-source-data gate reads it. |

### OTHER:Contract fake library (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02560 | RWB-P1-DM013-APP | DOR-RWB-P1-DM013-APP-22 | n/a | Publish a fake library version for the contracts this story's tests use |
| CDC-02568 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-22 | 16 | Publish the reference-data contract fake and record its library version |

### OTHER:Screen Specifications (next version) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02579 | RWB-P1-DM014-APP | CG-ALL-1991 | 15 | SCR-44 empty, loading, error and no access marked Not specified. |
| CDC-02580 | RWB-P1-DM014-APP | CG-ALL-1992 | 15 | SCR-45 loading referred to Screen Specifications v1; empty, error and no access marked Not specified. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02582 | RWB-P1-E1001-APP | DOR-RWB-P1-E1001-APP-21 | header | Publish the contract for legacy key RWB-E1-001 in a contract story and move the CON stories it depends on to Done. |
| CDC-02583 | RWB-P1-E1001-APP | DOR-RWB-P1-E1001-APP-22 | header | Record the published fake library version for the contract stories this story depends on. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02596 | RWB-P1-E1001-APP | GAP-0206 | n/a | Cut the 48 table-to-table foreign keys to business-key columns, keep the 11 ACE view references, show all three cases per row; no service DB story creates a cross-schema foreign key. |
| CDC-02606 | RWB-P1-E1001-APP | GAP-2123 |  | Assign the rwb_valuation tables to S1 rwb-valuation so that S1 tests have a schema to seed and assert on. |

### 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02609 | RWB-P1-E1001-APP | GAP-0285 | 1 | Add the cut table: each built schema table to its rwb_* schema, with its baseline migration and data move order; cite it from RWB-PLT-NF06-DB and each per-service DB story. |
| CDC-02615 | RWB-P1-E1001-APP | GAP-0979 | 13 | Platform naming for constraints; primary key on id; role_code unique; single foreign key permission.role_id; one index per read path, leading columns from that story's section 13. |

### OTHER:ERD v5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02617 | RWB-P1-E1001-APP | GAP-0115 |  | Draw the 108 v5 references unchanged; list sys_fields.object_name to sys_objects and sys_objects.data_product to data_product separately in the reconciliation table. |
| CDC-02618 | RWB-P1-E1001-APP | GAP-0116 |  | Group the v5 objects by Ownership Map owner, add a cross-service reference table, and keep the v5 data-product table as section 3. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02644 | RWB-P1-E1002-APP | CG-ALL-2019 | 12.5 | Add a Workflows row for CaseListBuildWorkflow on task queue rwb-source-data, or the story names the catalogued workflow once the catalogue confirms it. |
| CDC-02661 | RWB-P1-E1002-CON | CG-ALL-2033 | 12.5 | Add a Workflows row for CaseListBuildWorkflow, task queue rwb-source-data, one per business date. |

### OTHER:frontend-context.md v2 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02654 | RWB-P1-E1002-APP | GAP-0017 | 8 | Record the screen-to-service map derived from the gateway-bff composite routes in the next context run. |
| CDC-02687 | RWB-P1-E1002-OPS | GAP-0017 |  | Record the screen-to-service map derived from the gateway-bff composite routes in the next context run. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02668 | RWB-P1-E1002-CON | DOR-RWB-P1-E1002-CON-12 | 12.7, 16, 18 | Test Cases v8 covers the criteria this story names; RTM v7 test lists align with section 18. |
| CDC-02749 | RWB-P1-E1011-CON | DOR-RWB-P1-E1011-CON-12 | 12.7, 16, 18 | Add TC-E1-011-08, TC-E1-011-09 and TC-E1-011-10 on tab Story test cases; align the §18 test lists to RTM v7. |

### RWB-P6-E1011-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02711 | RWB-P1-E1011-APP | GAP-1168 | header | The item concerns the C list of the P6 story; this story's contract dependencies are unchanged. |
| CDC-02755 | RWB-P1-E1011-CON | GAP-1168 |  | Add RWB-P3-E1042-CON, RWB-P3-E1043-CON and the rwb-source-data data-product contract to the C list; name the reference-data read in RWB-P3-E1043-CON. |

### OTHER:Build Notes v6 (RWB-E1-011 View note) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02739 | RWB-P1-E1011-APP | GAP-3169 |  | Read 'the case exceptions' as the reconciliation breaks in reconciliation_result, or name P3 case_entry_exclusion if that is meant. |
| CDC-02782 | RWB-P1-E1011-CON | GAP-3169 |  | Replace 'the case exceptions' with the reconciliation breaks in reconciliation_result, or name P3 case_entry_exclusion if that is meant |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02740 | RWB-P1-E1011-APP | GAP-3172 |  | State the wave 1 delivery of rwb-asset in the service epic and the wave plan. Let the rwb-asset service wave govern its later stories. |
| CDC-02783 | RWB-P1-E1011-CON | GAP-3172 |  | State the wave 1 delivery of rwb-asset in the service epic and let the rwb-asset service wave govern its later stories; raise one conflict row per service and business epic |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_case.sql (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20555 | RWB-P1-E1011-CON | R-21924 |  | Needs the column sets of run, result and break and the type of quality_check, none in the sources. Legacy columns are in PS v4 lines 1361-1382. |
| CDC-20556 | RWB-P1-E1011-CON | R-21924 |  | Same change as the other R-21924 item. Needs the run, result and break column sets and the quality_check type, not in the sources. |

### 07 Screens and experience/Recovery Workbench Screen Inventory and Navigation v2.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20579 | RWB-P1-E1011-APP | R-14976 |  | Spec SCR-45 lists only 'Loading; breaks'. Empty, error and no-access states are not in the sources. Needs a business decision. |
| CDC-20583 | RWB-P1-E1011-APP | R-14976 |  | Same as R-14976 above: the workbook was not inspected because no Bash tool was available. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20657 | RWB-P1-E1011-APP | R-21918 |  | Check codes, state names, paths, cron and read style are not in the item or this document. Open row added to T-B. Platform administration right already on API-P3-027. |
| CDC-20658 | RWB-P1-E1011-APP | R-21928 |  | Change Register is outside this document. Link columns need varchar lengths for account_key and person_key, not in the sources (GAP-2237). |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20724 | RWB-P1-E1001-APP | R-28414 |  | The entra_group row repeats about 30 times in the field catalogues, so one replace cannot match uniquely. Needs section-scoped edits (GAP-0980). |
| CDC-20726 | RWB-P1-E1001-APP | R-28414 |  | Same entra_group line repeats in the field catalogues; needs section-scoped edits. Column text not unique for one replace (GAP-0980). |

### OTHER:Recovery Workbench backlog (CON stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02553 | RWB-P1-DM012-APP | DOR-RWB-P1-DM012-APP-21 | header | Set RWB-PLT-E1027-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON to Done, or publish the contract for this key |

### OTHER:Contract fake library (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02554 | RWB-P1-DM012-APP | DOR-RWB-P1-DM012-APP-22 | header | Record the published version of the rwb-decision contract fake library |

### RWB-PLT-E1044-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02559 | RWB-P1-DM013-APP | DOR-RWB-P1-DM013-APP-21 | header | Publish the contracts these two stories own and bring both to Done; then record Definition of Ready item 21 for RWB-P1-DM013-APP as met. |

### RWB-PLT-E1043-CON; RWB-PLT-E1044-CON; RWB-PLT-N001-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02567 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-21 | header | Bring the contract stories this key depends on to Done so the contract is published |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02569 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-23 | header | Contract version row records that the version is not specified. |

### OTHER:Screen design for SCR-44 and SCR-45 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02572 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-10 | 15 | Section 15 marks the missing states as Not specified. |

### OTHER:L3 process mapping (not given in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02574 | RWB-P1-DM014-APP | DOR-RWB-P1-DM014-APP-2 | 18 | Feature and L3 process columns added. |

### OTHER:plan/split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02577 | RWB-P1-DM014-APP | GAP-0240 | Header | Set the schema cutover of each migrated table to the wave of its owning service; keep the migration story releases as the latest date. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02578 | RWB-P1-DM014-APP | GAP-0237 | 11 | Owner-side Flyway load recorded under RWB-PLT-E1044-CON; section 7 steps 6-7 still need rewriting |

### OTHER:ACE database provisioning (ACE team and DBA) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02584 | RWB-P1-E1001-APP | GAP-0012 | header | Create the 19 schemas and logins in wave 0 and set the PgBouncer connection cap per login with the ACE DBA. |

### RWB-P1-E1069-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02591 | RWB-P1-E1001-APP | GAP-0566 | 5, 11, 12.7 | Publish the three read operations with response fields and problem body in RWB-P1-E1069-CON; record that view SQL, helper functions and conformance test are the rwb-source-data application slice, the login, grants, view owner and extension tables the database slice, and the 19-login proof the wave 1 integration slice. |

### RWB-P4-E1037-APP; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02592 | RWB-P1-E1001-APP | GAP-0975 | n/a | Read every 'rwb_access baseline' reference as the version applied by RWB-P4-E1001-APP; RWB-P4-E1037-CON keeps the contract stub and creates no table. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:README and ERD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02594 | RWB-P1-E1001-APP | GAP-0107 | n/a | Derive the 48 cuts from sheet Tables: keep a foreign key only when both tables share an owner, else the column stays uuid. Record the 48 rows in FK cuts, README and ERD. |

### OTHER:v4 workbook; OTHER:Mapping sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02597 | RWB-P1-E1001-APP | GAP-0210 | n/a | Keep the eleven ACE entity names; give each field target schema rwb_source_data and owner P1, read through the rwb-source-data contract; add the four extension tables as Workbench targets at next revision. |

### OTHER:v4 workbook; OTHER:Mapping and ACE gaps sheets (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02598 | RWB-P1-E1001-APP | GAP-0211 | n/a | Add Target schema and Owning service columns, one value per row from Ownership Map sheet Tables; keep columns A to N unchanged. |

### OTHER:v3 workbook; OTHER:Ownership and Ownership split sheets (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02599 | RWB-P1-E1001-APP | GAP-0224 | n/a | Add Owning service (D-RCV-60), Owning schema (D-RCV-60) and Basis (D-RCV-60) at the end of each sheet, one owner per data product from the Ownership Map; keep columns A to K unchanged. |

### OTHER:Per-service DB stories and wave-1 integration run (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02602 | RWB-P1-E1001-APP | GAP-0333 |  | Assign each of the 24 operational objects to its service schema. Wave-1 run asserts the 92 tables and records the 24 as an open list. |

### OTHER:TSD P4 v3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02603 | RWB-P1-E1001-APP | GAP-0976 |  | Fix rwb_access at role, permission, role_conflict, masking_rule and delegation_limit. Treat lov_value, partner_user and rule tables as a superseded module view. |

### OTHER:Functional Specification P1 (field catalogues) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02605 | RWB-P1-E1001-APP | GAP-1512 |  | Add field lists for data_contract, dp_treatment, dp_guarantee_claim and efs_ledger_outcome at TS review before wave 2. Carry placeholders now. |

### OTHER:TSD P8 T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02608 | RWB-P1-E1001-APP | GAP-2538 |  | Declare case_id, treatment_id and account_payment_id as uuid values with no foreign key. Resolve references through the owners' contracts. |

### OTHER:Security and Access Design v4 (to v5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02613 | RWB-P1-E1001-APP | GAP-2035 | 7 | Write section 7 per service: one login per rwb_* schema, grants on the own schema only, view grant on rwb_source_data only, replacing the recovery_svc row with a service login isolation row. |

### OTHER:FSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02614 | RWB-P1-E1001-APP | GAP-0980 |  | Restate v_ace_iam_group.entra_group as Workbench column role.entra_group (DF-REF-039, varchar(120), nullable, empty) read through the rwb-source-data contract; remove 'not a Workbench column'. |

### OTHER:Mapping workbook (v4 Mapping sheet; OTHER:Mapping rules) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02621 | RWB-P1-E1001-APP | GAP-0215 |  | Add a Mapping-rules entry naming contact_point_ext, account_ext and valuation_ext (owner P1, schema rwb_source_data) as extension-field stores. Leave the 133 field rows unchanged until LDM v10. |

### OTHER:Mapping workbook (v4 Mapping sheet, column B) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02622 | RWB-P1-E1001-APP | GAP-0216 |  | Leave column B empty for the 81 blank field rows. Assign their data products at the next LDM revision. Do not guess a DP code. |

### OTHER:Mapping workbook (v4 DP06 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02623 | RWB-P1-E1001-APP | GAP-0226 |  | Record S5 as owner of the Workbench asset data set (asset_sale, listing). Keep ACE collateral and valuation as a P1 read and valuation_ext as P1, as the basis cell states. |

### OTHER:Mapping workbook (v4 DP07 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02624 | RWB-P1-E1001-APP | GAP-0227 |  | Record S4 as owner of the Workbench legal data set (legal_action, hearing). Keep ACE court records as a P1 read and notice and proof of delivery as P6. |

### OTHER:Mapping workbook (v4 DP13 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02625 | RWB-P1-E1001-APP | GAP-0229 |  | Record P8 as owner of the proceeds and matching data set. write_off stays S7. ACE payment and gl_write_off records stay a P1 read. |

### OTHER:Mapping workbook (v4 DP05 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02626 | RWB-P1-E1001-APP | GAP-0230 |  | Record P1 as owner of the interaction ledger and efs_ledger_outcome. Notice and template content stay P6. The case timeline stays a P3 read through the P1 contract. |

### OTHER:Mapping workbook (v4 DP14 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02627 | RWB-P1-E1001-APP | GAP-0231 |  | Record P3 as owner of parameters and reference data. roles, permissions, masking_rule and delegation_limit stay P4. template and merge_field stay P6. |

### OTHER:Mapping workbook (v4 Ownership split basis cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02628 | RWB-P1-E1001-APP | GAP-0232 |  | Keep the count of 88. Append the reconciliation: 93 map rows, 4 extension tables, 1 legacy table (lake_copy_watermark, no target), 88 Tier 4 tables over 19 owners. |

### OTHER:Mapping workbook (v4 Roles; OTHER:Change process and Quality measures sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02629 | RWB-P1-E1001-APP | GAP-0233 |  | Add one role row (service data steward), one change-process step (owner service) and one quality measure (schema isolation). Keep the v3 rows unchanged. |

### OTHER:Mapping workbook (v4 Ownership column G and Ownership split column F) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02630 | RWB-P1-E1001-APP | GAP-0234 |  | Read the six 'Application owner (DL02)' cells as the owning service. Change the two 'Workbench access' cells to the owning service and its schema. Append an owning service column. |

### RWB-P4-E1001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02631 | RWB-P1-E1001-APP | GAP-0978 | - | Name the file V<seq>__rwb_p4_e1001_access_schema.sql with the four-digit sequence taken at merge; its test asserts the version is later than every service baseline and never 0001 of the legacy line. |

### OTHER:RWB-PLT-EVT topic design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02632 | RWB-P1-E1001-APP | GAP-2062 | - | Set the retry and dead-letter policy as target for every topic; use 12 partitions, RF 3 and 7 days from rwb.payment.events.v1 as the default until RWB-PLT-EVT sets each service's count; record the open point. |

### OTHER:Build Notes v6 (rwb-payment service epic and wave plan) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02637 | RWB-P1-E1001-APP | GAP-3171 | - | State the wave 1 delivery of rwb-payment in the service epic and the wave plan; the rwb-payment service wave governs its later stories. |

### OTHER:rwb-decision (P7) stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02638 | RWB-P1-E1001-APP | GAP-1279 |  | Login, migration, naming, Field IDs and dictionary handover of rwb-decision belong to its own stories. |

### RWB-P1-E1016-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02639 | RWB-P1-E1001-APP | GAP-0484 | 4 | Deliver the three indexes, read model v_data_product_catalog, DPA-2026.11 seed, 122/1,366 dictionary conformance check and schema checks; create no table already created by RWB-P1-E1001-APP or RWB-P1-E1069-DB; own no masking row; repeat run changes nothing. |

### RWB-P1-E1002-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02645 | RWB-P1-E1002-APP | DOR-RWB-P1-E1002-APP-14 | header | Record the signed epic design sign-off for RWB-P1-E1002-APP in the epic design record. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; OTHER:rwb-case API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02648 | RWB-P1-E1002-APP | DOR-RWB-P1-E1002-APP-8 | 12.1 | Publish GET /case-list/dates/{businessDate} and GET /case-list/rows in rwb-source-data.yaml; publish GET parameters/{key} and reference-data/{lovCode} in rwb-case; declare the Idempotency-Key header on POST /admin/jobs/{jobId}/rerun. |

### OTHER:Functional Specification P3 (A1.5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02649 | RWB-P1-E1002-APP | GAP-1549 |  | Restate the A1.5 ACE read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### RWB-P3-E1002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02652 | RWB-P1-E1002-APP | DOR-RWB-P1-E1002-APP-10 | 12.5 | Add the error state and the access state to SCR-02 in the P3 story. |

### OTHER:Solution architecture (case list target form); RWB-P1-E1015-CON; RWB-P1-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02653 | RWB-P1-E1002-APP | GAP-2228 | 8, 11, 12, 13 | One CaseListRow per open case with account keys and columns; rwb-case reads RWB-P1-E1015-CON for account and freshness (one hop, 2 s), stamps refreshedAt, X-Data-As-Of and stale flag; drop case_list_row, its key, extract file, lake path and data set (DP-17); REC-01 and REC-05 stay with RWB-P1-E1011. |

### OTHER:Functional Specification Document P3, section A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02663 | RWB-P1-E1002-CON | GAP-1549 |  | Restate the A1.5 read path as a read through the rwb-source-data contract. Keep the business-key link rules unchanged. |

### OTHER:P3 screen specification of SCR-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02667 | RWB-P1-E1002-CON | DOR-RWB-P1-E1002-CON-10 | 15 | This contract story owns no screen; the states belong to SCR-02 in P3. |

### RWB-P1-E1015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02669 | RWB-P1-E1002-CON | GAP-2228 | 15 | Publish one CaseListRow per open case with account keys and legacy account columns; read the account and freshness answers of RWB-P1-E1015-CON for one page, one hop, 2 s budget; stamp refreshedAt and X-Data-As-Of with a stale flag; drop case_list_row, its key, the extract file, the lake path and the DP-17 data set; REC-01 and REC-05 stay with RWB-P1-E1011 in rwb-source-data. |

### OTHER:frontend-context.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02670 | RWB-P1-E1002-CON | GAP-0017 |  | Record the screen-to-service map derived from the gateway-bff composite routes and the screen inventory of the 53 screens with the design tokens, in the next context run. |

### OTHER:Wave-1 contract review record for the rwb-case and rwb-integration contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02671 | RWB-P1-E1002-CON | GAP-0335 |  | Agree JOB-04 reads open case accounts through GET /api/recovery/case/v1/cases and the queue cut through GET /api/recovery/case/v1/queues/{queueId}/cases; the daily extract reaches rwb-reporting via rwb-integration deliverFile on queue rwb-integration with manifest fileId, batchId, sha256 and record count; events rwb.integration.FileDelivered.v1 and rwb.integration.FileFailed.v1 on rwb.integration.events.v1; projection in schema rwb_reporting; no data lake path. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02680 | RWB-P1-E1002-OPS | DOR-RWB-P1-E1002-OPS-8 | none | Publish the two rwb-case operations, add CaseListBuildWorkflow to Workflows, and add rwb-source-data as consumer of rwb.source-data.AceDataReady.v1. |

### OTHER:Functional Specification P3, section A1.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02681 | RWB-P1-E1002-OPS | GAP-1549 | none | Restate the A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02683 | RWB-P1-E1002-OPS | CG-ALL-2043 | 12.5 | Add activity snapshot(page) on task queue rwb-source-data, or use a catalogued activity |

### OTHER:rwb-source-data API yaml (case-list paths) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02685 | RWB-P1-E1002-OPS | GAP-0485 | 11 | Add GET /case-list/dates/{businessDate} and GET /case-list/rows; keep the publish_status gate of RWB-P1-E1011-APP |

### RWB-P1-E1002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02686 | RWB-P1-E1002-OPS | GAP-2228 |  | Publish one CaseListRow per open case with its account keys and account columns; read account and freshness answers of RWB-P1-E1015-CON; stamp refreshedAt and X-Data-As-Of with stale flag; drop case_list_row, its key, extract file, lake path and DP-17 data set. |

### RWB-P1-E1002-CON; RWB-P1-E1002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02689 | RWB-P1-E1002-OPS | GAP-0486 |  | Publish GET /case-list/dates/{businessDate} and GET /case-list/rows with the answer shapes in the proposed fix; page size and sort key stay open at contract review. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02700 | RWB-P1-E1011-APP | DOR-RWB-P1-E1011-APP-8 | 12.1 | Publish both admin operations and fix the result enum in rwb-source-data.yaml; add rwb-source-data as consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1. Two further detcheck items are truncated in the input and not covered. |

### OTHER:Screen catalogue entry for SCR-45 (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02704 | RWB-P1-E1011-APP | DOR-RWB-P1-E1011-APP-10 | find it | Define empty, loading, error and no-access states for SCR-45. |

### RWB-P1-E1015-APP; RWB-P1-E1069-APP; RWB-P1-E1011-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02705 | RWB-P1-E1011-APP | DOR-RWB-P1-E1011-APP-17 | find it | Complete the three build dependencies not yet done so they can be marked done in the header. |

### OTHER:Program BRD v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02706 | RWB-P1-E1011-APP | DOR-RWB-P1-E1011-APP-18 | Header | Open decisions row lists DL16 and DL25 with their assumptions |

### OTHER:TSD P1 v3, sheet Reconciliations (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02707 | RWB-P1-E1011-APP | GAP-0268 | find it | Give each reconciliation row an owner from the Ownership Map sheet Tables; the Workbench side of REC-01 to REC-08 is answered by the owning service on its contract, one hop with a 2 s timeout; rwb-source-data keeps the ACE side and the JOB-04 run. |

### OTHER:TSD P1 v3, sheets Reconciliations and Quality measures (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02708 | RWB-P1-E1011-APP | GAP-0269 | find it | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures, with values from the Ownership Map sheet Tables. |

### OTHER:Business Requirements Document, section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02709 | RWB-P1-E1011-APP | GAP-1456 | find it | State the rule that Epic 1 stories keep the business-epic wave and the delivery lead confirms the build wave per story at build sequencing. |

### OTHER:RWB-E1-055 and the check register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02710 | RWB-P1-E1011-APP | GAP-1169 | 8 | Give the notice barcode break its own code in RWB-E1-055 section 4 step 11 and section 8 BR5, or correct the register; REC-05 stays the business-key orphan check. |

### OTHER:Reconciliation register v3 (Reconciliations row REC-08) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02712 | RWB-P1-E1011-APP | GAP-0270 | 8 | Compare each service's local decision record on rwb.decision-record.v1 with P7 decision_log_entry, on count and last hash, nightly with the 02:00 hash-chain check. |

### OTHER:Reconciliation register v3 (v4 REC numbering block) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02713 | RWB-P1-E1011-APP | GAP-0273 | 8 | Add a REC numbering block mapping each check to its number here and in RWB-E1-011; keep source IDs and rename nothing. |

### OTHER:TSD P1 v3 (T3.6; OTHER:T-A.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02714 | RWB-P1-E1011-APP | GAP-0496 | 8 | Remove REC-03 and REC-04 and the cross-estate REC-05 keys from P1 scope; keep REC-01, REC-02 and the REC-05 orphan list over P1 tables. |

### OTHER:TSD P3; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02716 | RWB-P1-E1011-APP | GAP-0740 |  | Confirm the three check codes and four state names; publish the four operation paths; record REST or Temporal reads; decide account_id or account_key; set the Schedule cron; add the Platform administration right. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md; OTHER:INT-19) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02717 | RWB-P1-E1011-APP | GAP-1170 | 7 | Record the decision that the two lake extracts and INT-19 are dropped and that quality facts are served from GET /api/recovery/comms/v1/quality-results. Story line 120 is already updated to drop the lake send. |

### OTHER:P1 data model (data-model review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02719 | RWB-P1-E1011-APP | GAP-1508 | n/a | Publish the per-account break list within the reconciliation result and its read operation; fix the store at the data-model review before system test. |

### OTHER:rwb-case data model (schema rwb_case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02721 | RWB-P1-E1011-APP | GAP-2233 | n/a | Create case_quality_run, case_quality_result and case_quality_break with the legacy reconciliation_result columns and a unique key on rec_code, quality_check, business_date and product_group; add to baseline migration. |

### OTHER:rwb-source-data data-product contract on /api/recovery/source-data/v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02723 | RWB-P1-E1011-APP | GAP-2235 | Header | Publish the freshness read and one product-coded records read per data product with paging and element names; plan-side REC-03 reads keyed by plan_ref. |

### OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02724 | RWB-P1-E1011-APP | GAP-2236 | 7 | Case-side hold read marked Not specified in the source documents |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02725 | RWB-P1-E1011-APP | GAP-2237 | Header | Record the uuid cross-reference form of account_id and party_id as the pre-re-base artefact in the Change Register; link columns stay ACE business keys account_key and person_key as varchar. |

### OTHER:RWB-P1-E1018 story and P1 data model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02726 | RWB-P1-E1011-APP | GAP-0575 | 4 | Step 8 keeps this story's break list content and marks its durable home Not specified. |

### RWB-P8-E2008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02727 | RWB-P1-E1011-APP | GAP-0601 | 4 | Name the fold rule (one row per payment_code, ordered by paymentCode ascending, both reads unpaged with the cap as configuration), state the over-cap answer, and route a confirmed duplicate payment_code to the REC-05 break list of RWB-P1-E1011-APP. |

### OTHER:Recovery Workbench target workbook v3; OTHER:Reconciliations sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02730 | RWB-P1-E1011-APP | GAP-0271 | find it | Add a Per-service reconciliation sheet with one row per service of the 19: tables, part of each check, key, tolerance, cadence, break and result route, pattern and basis; placeholder per Template and Rules R9 where no source gives cadence or route. |

### OTHER:Quality measures sheet v3 (Timeliness; OTHER:B7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02733 | RWB-P1-E1011-APP | GAP-0276 |  | Define Timeliness as rwb-source-data reading the complete ACE batch and publishing AceDataReady; other services measure the freshness contract; owner is P1 rwb-source-data. |

### RWB-P6-E1011-APP; OTHER:TSD P6 Communications v2; API:(service not named); OTHER:schema folder; OTHER:batch and scheduling design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02735 | RWB-P1-E1011-APP | GAP-1172 |  | Adopt comms_quality_run, comms_quality_result and comms_quality_break; REC-09 with checks ACK and POD; one Schedule after the POD read; GET /quality-runs/{businessDate} and GET /quality-results. |

### OTHER:TSD P6 Communications v2 (T6.1 RBAC matrix) and gateway-bff route (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02736 | RWB-P1-E1011-APP | GAP-1173 |  | Declare the two quality reads in Platform administration with right R, adding that area to the RBAC matrix and the gateway route. Case notice read keeps Litigation R with scope. |

### OTHER:FSD P1 Screens table (SCR-44; OTHER:SCR-45) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02737 | RWB-P1-E1011-APP | GAP-1514 |  | State that this service serves the job, freshness, reconciliation and dictionary operations; the edge owns the composite route; reporting owns the dashboard shell. Fix before Epic 2 acceptance. |

### RWB-P3-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02738 | RWB-P1-E1011-APP | GAP-2238 |  | Case-side facts read by rwb-reporting through rwb-case reads; one Schedule with SKIP overlap and catch-up, cron set at deployment; three alert groups as configuration; flag rwb.p3.case-quality-run. |

### OTHER:Recovery Workbench BRD v4 (section 3 headings) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02741 | RWB-P1-E1011-APP | GAP-1457 | 9 | Renumber section 3 headings by service epic in a later BRD version, keeping every requirement key unchanged. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02745 | RWB-P1-E1011-CON | DOR-RWB-P1-E1011-CON-8 | 12 | Resolve CG-ALL-2063, CG-ALL-2064, CG-ALL-2066, CG-ALL-2065 and CG-ALL-2067 in their owner documents; the +1 gap is not named in the detcheck. |

### OTHER:Recovery Workbench Reconciliations v3 (sheet Reconciliations) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02750 | RWB-P1-E1011-CON | GAP-0268 | find it | Give every reconciliation row an owner service from the Ownership Map; the holding service answers the Workbench side on its contract (one hop, 2 s timeout); rwb-source-data keeps the ACE side and the JOB-04 run. |

### OTHER:Recovery Workbench Reconciliations v3 (Reconciliations and Quality measures sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02751 | RWB-P1-E1011-CON | GAP-0269 | find it | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures, each value from the Ownership Map sheet Tables. |

### OTHER:Recovery Workbench FSD P1 (A2.12; OTHER:A2.19; OTHER:A2.20) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02752 | RWB-P1-E1011-CON | GAP-1499 | find it | Remove the data lake and INT-19 destinations; keep results, freshness and the six measures as this service's output to rwb-reporting; publish measures and regulatory extracts in rwb-reporting; confirm with the data steward before wave 2. |

### OTHER:Recovery Workbench BRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02753 | RWB-P1-E1011-CON | GAP-1456 | find it | State the wave rule in section 8.2: the story keeps its Template and Rules R5.6 wave; the delivery lead confirms the wave per story at build sequencing. |

### OTHER:RWB-E1-055 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02754 | RWB-P1-E1011-CON | GAP-1169 |  | In step 11 and BR5, give the notice barcode break its own code instead of REC-05; REC-05 stays the business-key orphan check. |

### OTHER:v3 Reconciliations workbook (REC-08 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02756 | RWB-P1-E1011-CON | GAP-0270 |  | REC-08 compares each service's local decision record on rwb.decision-record.v1 with P7 decision_log_entry, on count and last hash nightly, with the 02:00 hash-chain check. |

### OTHER:v3 Reconciliations workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02757 | RWB-P1-E1011-CON | GAP-0273 |  | Add a REC numbering block mapping each check to the number used by RWB-E1-011 and the story set; no ID is renumbered. |

### OTHER:_work/msr/plan/split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02758 | RWB-P1-E1011-CON | GAP-0275 |  | At Step D1, add slices for S2 (rwb-treatment) and P8 (rwb-payment) that own the Workbench side of REC-03 and REC-04. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02760 | RWB-P1-E1011-CON | GAP-0740 |  | Confirm the three check codes and state names, publish the four operation paths, and record the P1 read style and Schedule cron, login and right in the rwb-case contract. |

### OTHER:RWB-P1 reconciliation result contract and data model review (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02763 | RWB-P1-E1011-CON | GAP-1508 |  | Publish the per-account break list as part of the reconciliation result and its read operation, and fix its store at the data model review before system test. |

### OTHER:rwb-case data model and service baseline migration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02765 | RWB-P1-E1011-CON | GAP-2233 |  | Create case_quality_run, case_quality_result and case_quality_break in schema rwb_case with the legacy column names and unique key, and add them to the baseline migration. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02769 | RWB-P1-E1011-CON | GAP-1946 |  | Keep H and C at None; record the nine CONs as wave-0 prerequisites and fakes; read the ACE side via DP06 of rwb-source-data; drop the extracts and INT-19 path; serve facts from the two GET quality routes; accept the quality tables, REC-05 checks, run states and AssetQualityWorkflow. |

### RWB-P6-E1011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02770 | RWB-P1-E1011-CON | GAP-1167 |  | Keep H at None; record the seven platform CONs as wave-0 platform prerequisites arriving with the platform release train; add them to the dependency map as platform prerequisites, not lane dependencies; L-P6-C depth unchanged. |

### OTHER:Reconciliation workbook v3, new Per-service reconciliation sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02773 | RWB-P1-E1011-CON | GAP-0271 |  | Add one row per service (19) with its tables, check part, key, tolerance, cadence, break and result route, pattern and basis; use the Template and Rules R9 placeholder where the source gives no cadence or route. |

### OTHER:Reconciliation workbook v3; OTHER:Reconciliations sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02774 | RWB-P1-E1011-CON | GAP-0272 |  | Carry the Template and Rules R9 placeholder in the tolerance cell of the ten rows for P2, P4, P5, P10, S1, S3, S4, S6, S8 and S9; no value set here. |

### OTHER:Recovery Workbench Quality measures v3 (Timeliness; OTHER:B7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02776 | RWB-P1-E1011-CON | GAP-0276 |  | Timeliness reads: the ACE batch is complete when rwb-source-data reads it and publishes AceDataReady; other services measure the freshness contract; owner P1 rwb-source-data |

### OTHER:TSD P6 Communications v2 (T2; OTHER:T3.1; RWB-P6-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02778 | RWB-P1-E1011-CON | GAP-1172 |  | Carry comms_quality_run, comms_quality_result, comms_quality_break, checks ACK and POD, one Schedule and the two quality reads into the P6 API spec, schema folder and batch design |

### OTHER:Functional Specification P1 Screens table (SCR-44; OTHER:SCR-45) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02780 | RWB-P1-E1011-CON | GAP-1514 |  | Fix the screen owner: P1 serves job, freshness, reconciliation and dictionary operations, the edge owns the composite route, reporting owns the dashboard shell; before Epic 2 acceptance |

### OTHER:Batch and scheduling design (rwb-comms and rwb-case quality run) and rwb-reporting read model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02781 | RWB-P1-E1011-CON | GAP-2238 |  | Register one Schedule with SKIP overlap and a catch-up window, cron set at deployment; keep the three legacy alert groups as configuration; name the flag rwb.p3.case-quality-run |

### OTHER:BRD v4 section 3.1 to 3.9 headings (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02784 | RWB-P1-E1011-CON | GAP-1457 |  | In a later BRD version, renumber the section 3 headings by service epic, keeping every requirement key unchanged |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_source_data.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20587 | RWB-P1-E1011-APP | R-21921 |  | Per-account break list belongs to the P1 data model (data-model review), not this SQL file. The file has reconciliation_result only, with no break list. No change here. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0012 | 19 schemas, logins and the connection budget are not created | ACE team and DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0017 | No v5 screen inventory or screen-to-service map | Solution architect and UX lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0062 | Wave conflict P8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0063 | Wave conflict S5 / EP01 | Tech lead | Resolved (directive) |
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
| GAP-0235 | Version 3 gives one recovery schema, not the target schema of each table | Data architecture team | Resolved (directive) |
| GAP-0236 | The owner-side migration step has no story ID | TechX | Resolved (directive) |
| GAP-0237 | Version 3 has the Workbench run the load; the target makes the schema owner run it | TechX | Resolved (directive) |
| GAP-0238 | Reference data is one load in version 3 and six schemas in the Ownership Map | Data architecture team | Resolved (directive) |
| GAP-0240 | All 14 migration stories are wave 4 while nine services are wave 1 | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0268 | The nine reconciliations name one Workbench side, but that side sits in seven service schemas | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0269 | No reconciliation and no quality measure carries an owner | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0270 | REC-08 compares a decision-log copy that the target retires | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0271 | No per-service reconciliation rule, cadence or result route | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0272 | Ten services have no tolerance and no legacy reconciliation row | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0273 | REC-05 and REC-09 are numbered the other way round from RWB-E1-011 | Business analysis team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0274 | S1 rwb-valuation owns no table in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0275 | REC-03 and REC-04 have no per-service owner in the RWB-E1-011 slice set | TechX | Resolved (directive) |
| GAP-0276 | The Timeliness measure reads a Workbench read of the ACE batch that no service but P1 makes | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0285 | No source states how the built recovery schema, 92 tables and 14 data products, is cut across the 19 rwb_* schemas or how each V0001 baseline is produced | ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0333 | The owning rwb_* schema of the 24 operational dictionary objects is not stated | ACE database administrator | Resolved (directive) |
| GAP-0335 | The target read operation that serves the case list and the path by which the daily extract reaches rwb-reporting once the data lake is removed are not defined in the source documents | Solution architect | Resolved (directive) |
| GAP-0336 | Owner of REC-03 and REC-04 and the reporting delivery path of the two extracts are not named for the microservice target | Solution architect | Resolved (directive) |
| GAP-0337 | The connection matrix does not show the rwb-source-data outbound reads and the exclusion operation of the case contract is not named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0452 | The cutover reconciliation harness pack for the migrated decision log is not specified | Integration lead | Resolved (directive) |
| GAP-0453 | The wave 4 cutover reconciliation harness pack for money and closure is not specified | Integration lead | Resolved (directive) |
| GAP-0484 | The DB slice of this legacy key cannot deliver the table DDL, because two other stories already create the tables | ACE database lead | Resolved (directive) |
| GAP-0485 | The case list extract file, the outbound file adapter and the 07:30 Power BI data set have no target after the data lake is removed | Data architect | Resolved (directive) |
| GAP-0486 | The case-list read operations and their answer shapes are not specified in Arch v5 or in TSD P1 | Solution architect | Resolved (directive) |
| GAP-0487 | The case-list workflow name, the schedule name and the 07:15 fallback are not specified | Solution architect | Resolved (directive) |
| GAP-0495 | The two lake extracts and the Power BI data set have no successor in the target, while the legacy story still writes them and reads the report | Solution architect | Resolved (directive) |
| GAP-0496 | TSD P1 keeps REC-03, REC-04 and a cross-estate REC-05 inside P1 while the Change Register gives rwb-case, rwb-asset and rwb-comms their own slices of the same legacy key | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0497 | The reconciliation result path, the result and break-row shape, the ReconciliationQuery interface and the workflow and activity names are not specified in any source | Tech lead | Resolved (directive) |
| GAP-0542 | decision_log_entry is P7's and the target writes a local decision record plus the shared topic, while no source says whether the migrated legacy entries are published as records or handed over as a file, or who continues the hash chain | Solution architect | Resolved (directive) |
| GAP-0543 | proceeds is P8's, write_off is S7's and the closure sits on the case (P3) while the legacy money and closure migration is a single P1 slice, and no source says who loads each and what survives of the matching state | Solution architect | Resolved (directive) |
| GAP-0544 | The reference versions, their rows and the lists of values are P3's, the rule rows and their test cases are P7's, and the legacy story names a reference data service that exists in no source | Solution architect | Resolved (directive) |
| GAP-0557 | RWB-P1-E1001-APP: schema-split mechanics, login name, extension-table delivery boundary and Arch v5 against FSD and TSD P1 | Solution architect | Resolved (directive) |
| GAP-0566 | rwb-source-data view slice: how legacy RWB-E1-069 splits across three stories, where the two view migrations sit on the per-service sequence, and the response shape of the read operations are not specified | Solution architect, P1 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0575 | The shape and the home of the REC-05 break list are not specified, and the table that held it leaves the schema | Data architect with the data steward and the P1 owner of the reconciliation job | Resolved (directive) |
| GAP-0601 | The order of the payment answer, the fold of a repeated payment_code, the row cap of one call and the number of ALS payments per business date are stated by no source | Tech lead with the P8 contract owner | Resolved (directive) |
| GAP-0604 | The data product code and the source system label an answer names are reference data, and the reference-data contract is not in this Work Package's contract list | Business analyst, P1 with the P3 reference-data owner | Resolved (directive) |
| GAP-0740 | The rwb-case slice of RWB-E1-011 leaves the check codes, the four operation paths, the call type to rwb-source-data, the case key columns, the Schedule cron, the access right, the login and every report value that only the data lake held unspecified | Solution architect, with the P1 rwb-source-data owner, the P3 rwb-case owner and the data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0976 | The exact per-service table list of rwb_access is not stated in one place | Solution architect | Resolved (directive) |
| GAP-0978 | The file name and sequence number of the rwb_access baseline migration are not fixed | Tech lead | Resolved (directive) |
| GAP-0979 | The constraint names and the full index set of the five tables are not specified | ACE team (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-0980 | role.entra_group is a column in the technical specification and not a Workbench column in the functional one | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1168 | RWB-P6-E1011-APP: the parameters and reference-data contracts of rwb-case and the rwb-source-data contract the run reads are missing from the story's C list | Solution architect | Resolved (directive) |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1170 | RWB-P6-E1011-APP: the data lake is removed, so the reconciliation and data quality extracts and the report built on them have no target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1171 | RWB-P6-E1011-APP: no event is published because DP-09 is not in the pattern set, and no operation of rwb-reporting or rwb-source-data accepts the quality facts | Solution architect | Resolved (directive) |
| GAP-1172 | RWB-P6-E1011-APP: the quality tables, the check codes, the run cadence and the two quality read operations are not named in any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1173 | RWB-P6-E1011-APP: the right of the quality reads is Platform administration R in the legacy story, and the rwb-comms RBAC matrix has no Platform administration column | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1280 | LDM v8 states 18 fields for rule_row and a rule_test_case.package_version_id that its fields sheet does not define, and both name cross-schema foreign keys that DP-01 forbids | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1457 | Section 3 headings name the ten P modules only, while Epic 1 requirements also carry stories in S5, S8 and S9 | Business analyst | Resolved (directive) |
| GAP-1499 | The data lake and the dashboard connection are removed, so the reporting destinations of three FSD features have no home | Solution architect | Resolved (directive) |
| GAP-1508 | The per-account reconciliation break rows have no store after the quality-exception table leaves the schema | Data architect | Resolved (directive) |
| GAP-1512 | Four tables carry a name, an owner and a purpose but no field list in the read sources | Data architect | Resolved (directive) |
| GAP-1514 | The job monitor and data-quality screens are first-in here and owned by reporting in the architecture | Solution architect | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1984 | The Workbench table count is 92 in version 6 and 93 in the Ownership Map | Data architect | Resolved (directive) |
| GAP-1991 | P1 keeps a lake copy after the data lake is removed | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2061 | The source is written for one recovery module and has no per-service target, size or deployment shape | Architecture with RWB-PLT-OBS and RWB-PLT-DB | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2062 | No per-topic sizing exists for the 19 topics; one topic is sized in the architecture | RWB-PLT-EVT with the owning services | Resolved (directive) |
| GAP-2123 | The Ownership Map assigns no table to rwb-valuation although Architecture v5 gives it a schema | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2132 | The recovery table count of the source and the table count of the Ownership Map do not agree | ACE | Resolved (directive) |
| GAP-2176 | decision_log_entry is P7's, the record is local and the ledger is central, and no source says whether the migrated legacy entries are published as records or handed over as a file, nor who continues the hash chain | Solution architect | Resolved (directive) |
| GAP-2178 | RWB-DM-013 names three entities and a cutover step but no owner, source, format or sign-off place after the realignment | RW-DATASTEW | Resolved (directive) |
| GAP-2179 | The reference versions, their rows and the lists of values belong to rwb-case, the rule registry to rwb-decision, and the legacy story names a reference data service that exists in no source | Solution architect | Resolved (directive) |
| GAP-2228 | The target form of the case list is not fixed by any source: the row shape, the account-data owner in the read path, the freshness stamp, the removal of the lake path and the ownership of the reconciliation | Solution architect | Resolved (directive) |
| GAP-2232 | The split of RWB-E1-011 across the services and the case-side scope are not ruled by any source | Solution architect | Resolved (directive) |
| GAP-2233 | The case-side result row has no table and no check codes in the target | Solution architect | Resolved (directive) |
| GAP-2234 | No source names the operations, rights or response shapes of the case-side quality run | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2235 | The data-product reads that replace the ACE views have no published path, element shape or product code in this story's sources | Solution architect | Resolved (directive) |
| GAP-2236 | The hand-off of the case-side hold to the case-list publish gate is not specified | Solution architect | Resolved (directive) |
| GAP-2237 | TSD P3 v3 declares the case links as uuid cross-references while the FSD re-base and the legacy data table use the ACE business keys | Solution architect | Resolved (directive) |
| GAP-2238 | The report, the Schedule cadence, the alert groups and the feature flag of the case-side run have no source | Solution architect | Resolved (directive) |
| GAP-2401 | The LDM states one field count for rule_row and a rule_test_case column its fields sheet does not define, and both TSD P7 and the LDM name cross-schema foreign keys that DP-01 forbids | Solution architect, P7 rwb-decision, with the data owners of rwb_case and rwb_access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2533 | rwb-payment cutover load of RWB-DM-013: the handover file, the load command and its run record, a provenance column, the legacy payment_code column and the two schema-level H rows are fixed by no single source, and this slice owns no legacy criterion | Data steward and solution architect of rwb-payment, with the rwb-source-data owner, the schema baseline owner and the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2534 | The DDL of proceeds beyond its columns is not published: constraint names, index names, index columns and the Field IDs of the 7 standard columns | ACE team | Resolved (directive) |
| GAP-2535 | TSD P8 T3.1 carries payment_match_rule as a second table of the module, and the Ownership Map gives P8 one table only | Solution architect | Resolved (directive) |
| GAP-2536 | The read paths that proceeds has to serve, and the screens that read it, are stated in no source of the read set | Solution architect | Resolved (directive) |
| GAP-2537 | The handover of a service's field declaration to the one dictionary has no documented mechanism or operation | Solution architect | Resolved (directive) |
| GAP-2538 | TSD P8 T3.3 declares three many-to-one relationships of proceeds and the target keeps them as values | Solution architect | Resolved (directive) |
| GAP-2539 | DP13 Money and closure is catalogued with the system of record ACE only, while the match on the same row is a Workbench record | Business analyst, P8 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2541 | EP01's wave map wave is 1 and rwb-payment's Architecture v5 wave is 2 for the same story | Portfolio lead | Resolved (directive) |
| GAP-3151 | Origin tag where one legacy criterion is carried by several new stories | TechX | Resolved (directive) |
| GAP-3169 | The reconciliation story writes 'the case exceptions' without naming a table | P1 data owner | Resolved (directive) |
| GAP-3171 | Service P8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3172 | Service S5 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P1-E1002-CON | skipped AC ID | 82 | missing: AC8, AC9, AC10 |
