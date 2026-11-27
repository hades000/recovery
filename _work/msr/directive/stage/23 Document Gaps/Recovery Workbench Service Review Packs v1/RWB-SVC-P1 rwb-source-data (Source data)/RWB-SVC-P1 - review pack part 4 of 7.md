# RWB-SVC-P1 rwb-source-data (Source data) - review pack, part 4 of 7 (RWB-P1-E1017-CON to RWB-P1-E1065-DB)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 10 |
| Resolved in the stories | 200 |
| Cross-document (pending in another document) | 209 |
| Not applied (value not in the sources) | 18 |
| Open business decisions | 14 |
| Register gaps linked | 105 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P1-E1017-CON | 24 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1017 CON Retention and archive rule for the data store - contract v2.md |
| RWB-P1-E1017-OPS | 15 | 16 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1017 OPS Retention and archive rule for the data store - deployment v2.md |
| RWB-P1-E1018-APP | 27 | 27 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1018 APP Case ID issuance and case record v1 v2.md |
| RWB-P1-E1055-APP | 22 | 28 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1055 APP Proof of delivery capture design with WIN v2.md |
| RWB-P1-E1064-APP | 16 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1064 APP Data dictionary for the 14 data products v2.md |
| RWB-P1-E1064-CON | 15 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1064 CON Data dictionary for the 14 data products - contract v2.md |
| RWB-P1-E1064-OPS | 8 | 21 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1064 OPS Data dictionary for the 14 data products - deployment v2.md |
| RWB-P1-E1065-APP | 37 | 21 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1065 APP Sandbox database with synthetic recovery data v2.md |
| RWB-P1-E1065-CON | 16 | 19 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1065 CON Sandbox database with synthetic recovery data - contract v2.md |
| RWB-P1-E1065-DB | 20 | 27 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 E1065 DB Sandbox database with synthetic recovery data - ACE DB v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P1-E1018-APP | R-09720 | CG-ALL-2222 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P7-E1017-APP | R-21967 | GAP-2070 | Register gap | Service owners P7 rwb-decision, P1 rwb-source-data and P4 rwb-access with Compliance | Where the retention period of the ledgers and the access log is held, and which job enforces it | Keep every period as written and mark the owner open: P7 enforces the ledger period, P1 the interaction ledger and P4 the access log, each as a row of its own retention data, until Compliance states where the periods are held. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21971 | GAP-1500 | Register gap | Compliance and PDPA officer | The retention rule table and the archive job move to the document service, while the FSD keeps both here | This service declares the retention class per data product and recovery table as versioned reference data, refuses a rule that names a read-only ACE view or the decision log, and archives nothing itself; the rule table and the monthly archive run belong to rwb-document. Confirm with Compliance that a class declared here and applied there is acceptable for the PDPA position. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-22191 | GAP-2245 | Register gap | Legal and the business lead | Whether a deviation pauses a statutory notice period is not settled by the sources | Keep the notice period unpaused as ASM-B2-P3-016-3 records; if Legal rules that it pauses, the deviation contract gains one signal to the notice clock and one criterion changes. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-28498 | GAP-1618 | Register gap | Compliance and PDPA officer | The decision log and the ledger carry no retention period, and the WORM seal period is unstated | Set the decision-log class period and the seal period under DL26 before the first release, keep the class per record class in reference data, and state in the retention rule that no archive runs inside this service. |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-28627 | GAP-2248 | Register gap | Business lead | The role that receives the expiry of a notice period is not named | Take the escalation role from the SERVICE_LEVEL row in force as ASM-B2-P3-016-6 records, and add a named default role for a missing row if the business lead asks for one. |
| RWB-ITG-E1064-ITG, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS, RWB-P4-E1064-APP | R-28656 | GAP-2308 | Register gap | Compliance and PDPA officer | No source states how many of the 1,366 dictionary fields are personal, so the masking coverage the gate checks has no expected count | Publish the personal-field list of the 14 data products from the dictionary (is_personal true) and the masking pack coverage it must reach, so that the gate can fail a load that leaves a personal field uncovered and the SIT run can assert a count. Until then the gate asserts the rule per field ID and reports the count it finds. At D1 number this row GAP-nnnn and cite it from ASM-B2-P4-020-3. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P1-E1017-OPS | R-04400 | DOR-RWB-P1-E1017-OPS-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the sources; the item stays open. |
| RWB-P1-E1017-OPS | R-04403 | DOR-RWB-P1-E1017-OPS-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version in sources: API Spec v5 rwb-source-data.yaml 5.0.0 lacks retention-run ops; CON verified file and Change Register name none. Placeholder added. |
| RWB-P1-E1017-OPS | R-28502 | GAP-2431 |  | The story file at the Work Package path already existed as a partial artefact of the superseded Work Package B-P7-05, with no fragment, no register rows and citations that resolve to nothing | The item concerns a partial story file left by superseded Work Package B-P7-05; no edit to this story was made for it. |
| RWB-P1-E1018-APP | R-04406 | DOR-RWB-P1-E1018-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record exists in the story or the searched project folders. Decision Log v10 DT05 gives only the sign-off process, so no sign-off can be recorded. |
| RWB-P1-E1018-APP | R-04407 | DOR-RWB-P1-E1018-APP-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the item or story. The Size row reads Not specified in the source documents. |
| RWB-P1-E1018-APP | R-04411 | DOR-RWB-P1-E1018-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version is recorded in this story or in the rwb-source-data story files. Recording one would invent a value. |
| RWB-P1-E1055-APP | R-04414 | DOR-RWB-P1-E1055-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record exists in the sources; a sign-off cannot be asserted or invented. Prior search of folders 03-05 and 09-11 found none. |
| RWB-P1-E1055-APP | R-04415 | DOR-RWB-P1-E1055-APP-16 | header | Definition of Ready item 16 Size: Fail | Header row records Size as not set. No size is given, so the DoR item stays open until the squad sizes the story. |
| RWB-P1-E1055-APP | R-04417 | DOR-RWB-P1-E1055-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in user stories or md/yaml/csv sources (prior search, not repeated here). A version cannot be invented. |
| RWB-P1-E1064-OPS | R-04429 | DOR-RWB-P1-E1064-OPS-16 | Header table | Definition of Ready item 16 Size: Fail | No size is given in the source documents, so item 16 stays open until the squad sizes the story at refinement. |
| RWB-P1-E1065-APP | R-04433 | DOR-RWB-P1-E1065-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed EP01 epic design record in the story or folders 03, 04, 05. Sign-off cannot be invented; needs the epic design record. Left as Not specified. |
| RWB-P1-E1065-CON | R-04440 | DOR-RWB-P1-E1065-CON-16 | header | Definition of Ready item 16 Size: Fail | No size value exists in the sources. The Size row reads Not specified and the squad sizes the story at refinement. |
| RWB-P1-E1065-CON | R-22254 | GAP-2249: Task and timer counts per seeded case, and the timer offsets beyond the FSD P3 AC-ALT-P3-011 offsets, are not in the sources | 7 | Task and timer counts per seeded case, and the timer offsets beyond the FSD P3 AC-ALT-P3-011 offsets, are not in the sources | The sources do not give the counts or offsets, so the story cannot fix them. |
| RWB-P1-E1065-CON | R-22255 | GAP-2250: The distribution of the 2,812 seeded cases across the 12 queues and 48 members is not in the sources | 7 | The distribution of the 2,812 seeded cases across the 12 queues and 48 members is not in the sources | The 40-case cap was not in the sources and is removed. |
| RWB-P1-E1065-CON | R-22256 | GAP-2252: The decision code and the payload of the decision records the seed writes are not in the sources | 7 | The decision code and the payload of the decision records the seed writes are not in the sources | RWB-P3-E1018-APP and RWB-P3-E1019-APP are not in the sources as decision codes, so they are removed. |
| RWB-P1-E1065-CON | R-22257 | GAP-2251: The rwb-case login name, the DEV read-only role name and the field identifiers of six seeded tables are not in the sources | 7 | The rwb-case login name, the DEV read-only role name and the field identifiers of six seeded tables are not in the sources | The read-only role name rwb_sandbox_read is already in BR3. The login and identifiers are not in the sources. |
| RWB-P1-E1065-CON | R-28657 | GAP-1054 | 1 | The count of held intake items per exception shape and the pages each held item carries are not specified | The seed profile names both parameters, but their values are not in the sources and read Not specified. |
| RWB-P1-E1065-DB | R-04443 | DOR-RWB-P1-E1065-DB-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed EP01 epic design record exists in the sources (prior search of md/csv found only forum and DT05 text). Sign-off cannot be asserted; no story edit made. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03015 | RWB-P1-E1017-CON | CG-ALL-2195 | 12.1 | Add path /api/recovery/source-data/v1/retention-runs with the POST operation as documented in RWB-P1-E1017-CON section 12.1 |
| CDC-03016 | RWB-P1-E1017-CON | CG-ALL-2196 | 12.1 | Add path /api/recovery/source-data/v1/retention-runs/{runId} with the GET operation as documented in RWB-P1-E1017-CON section 12.1 |
| CDC-03046 | RWB-P1-E1018-APP | CG-ALL-2212 | 12.1 | Operation kept in story; the path is missing from the owner's yaml and must be published there. |
| CDC-03047 | RWB-P1-E1018-APP | CG-ALL-2213 | 12.1 | Operation kept in story; the path is missing from the owner's yaml and must be published there. |
| CDC-03048 | RWB-P1-E1018-APP | CG-ALL-2214 | 12.1 | Operation kept in story; the path is missing from the owner's yaml and must be published there. |
| CDC-03052 | RWB-P1-E1018-APP | DOR-RWB-P1-E1018-APP-23 | Header | The contract version is not specified in the source; the story records that and the base path. The version must be fixed in the contract. |
| CDC-03053 | RWB-P1-E1018-APP | DOR-RWB-P1-E1018-APP-8 | 12.1 | Add paths /api/recovery/source-data/v1/entry-candidates (GET; query businessDate, threshold, page, size), /api/recovery/source-data/v1/extension-facts/parties/{personKey} (PUT) and /api/recovery/source-data/v1/extension-facts/accounts/{accountKey} (PUT). |
| CDC-03072 | RWB-P1-E1055-APP | CG-ALL-2225 | 12.1 | Publish GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= in rwb-source-data.yaml through the RWB-P1-E1055-CON story. |
| CDC-03073 | RWB-P1-E1055-APP | CG-ALL-2226 | find it | Remove the fixed enum on eventCode so LOV-LEDGER-EVENT values are read as data, as the story rules. |
| CDC-03074 | RWB-P1-E1055-APP | DOR-RWB-P1-E1055-APP-23 | Header | Add GET /proof-of-delivery under /api/recovery/source-data/v1; the path is absent from version 5.0.0. Story header now states version 5.0.0. |
| CDC-03075 | RWB-P1-E1055-APP | DOR-RWB-P1-E1055-APP-8 | find it | Publish the proof-of-delivery path and remove the closed eventCode enum (see CG-ALL-2225 and CG-ALL-2226). |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03025 | RWB-P1-E1017-CON | CG-ALL-2202 | 18 | Trace REQ-RDF-013 to TC-E1-017-01, TC-E1-017-02, TC-E1-017-03 and TC-E1-017-11 as in section 18, dropping the TC-E1-014 and TC-E1-017-05 links. |
| CDC-03038 | RWB-P1-E1017-OPS | CG-ALL-2208 | 18 | Align the REQ-RDF-013 test list to RWB-P1-E1017-OPS section 18 (TC-E1-017-01, TC-E1-017-03) in its next version. |
| CDC-03065 | RWB-P1-E1018-APP | CG-ALL-2221 | 18 | In the next RTM version, align the test lists of REQ-CWC-001, REQ-CWC-003, REQ-CWC-004 and the other three differing requirements with section 18 of RWB-P1-E1018-APP. |
| CDC-03094 | RWB-P1-E1055-APP | CG-ALL-2229 | 18 | Test lists differ for three requirements. Section 18 only adds TC-E1-055-14 and TC-E1-055-16 to REQ-DRI-006; the RTM alignment is due in its next version. |
| CDC-03107 | RWB-P1-E1064-APP | DOR-RWB-P1-E1064-APP-12 | 16, 18 | Align the section 18 test lists to the section 16 test cases, including new TC-E1-064-10 and TC-E1-064-11. |
| CDC-03117 | RWB-P1-E1064-APP | CG-ALL-2236 | 18 | Align the REQ-RDF-001 and REQ-RDF-011 test lists in the next RTM version with section 18 of this story. |
| CDC-03132 | RWB-P1-E1064-CON | CG-ALL-2243 | 18 | Align the REQ-RDF-001 and REQ-RDF-011 test lists with section 18 in the next version. |
| CDC-03152 | RWB-P1-E1064-OPS | CG-ALL-2249 | 18 | Align the REQ-RDF-001 and REQ-RDF-011 test lists with section 18 of this story in the next RTM version. |
| CDC-03169 | RWB-P1-E1065-APP | CG-ALL-2271 | 18 | §18 REQ-RDF-001 now lists the new TC-E1-065-11 to 14. RTM v7 is a separate workbook and must be aligned in its next version. |
| CDC-03189 | RWB-P1-E1065-CON | CG-ALL-2277 | 18 | Align the RTM v7 test lists for REQ-RDF-001 and REQ-RDF-010 with section 18 of this story, or align section 18 with RTM v7, in their next versions. |
| CDC-03215 | RWB-P1-E1065-DB | CG-ALL-2283 | 18 | Align the test lists for REQ-RDF-001 and REQ-RDF-010 with section 18 of this story in the next RTM version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03077 | RWB-P1-E1055-APP | CG-ALL-2224 | 4, 13 | Record recovery.ace_to_date as a conversion object in the owning document, or name the dictionary field instead |
| CDC-03079 | RWB-P1-E1055-APP | DOR-RWB-P1-E1055-APP-7 | 11 | Record recovery.ace_to_date as a conversion object in the owning document, or name the dictionary field instead |
| CDC-03104 | RWB-P1-E1064-APP | CG-ALL-2233 | 1, 3, 12.7, 13, 18 | Record v_data_dictionary as the read model of RWB-P1-E1001-APP, or name the dictionary object the story uses. |
| CDC-03105 | RWB-P1-E1064-APP | CG-ALL-2234 | 2, 7, 12.7, 19 | Record ace_view_owner as the view owner role of the recovery.v_ace_* views, owned by RWB-P1-E1069-DB. |
| CDC-03109 | RWB-P1-E1064-APP | DOR-RWB-P1-E1064-APP-7 | 11 | Add v_data_dictionary (read model) and ace_view_owner (view owner) as entity or field names |
| CDC-03126 | RWB-P1-E1064-CON | DOR-RWB-P1-E1064-CON-7 | 11 | Register ace_view_owner (view owner of recovery.v_ace_*) and v_data_dictionary (read model) as a field or entity in LDM v9 and Data Classification v5. |
| CDC-03144 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-7 | 11 | Add v_data_dictionary as a field or entity, or confirm it is a view outside the LDM; the story names it at lines 396 and 405. |
| CDC-03180 | RWB-P1-E1065-CON | DOR-RWB-P1-E1065-CON-7 | 11 | Confirm ace_view_owner as a field or entity, or name the view owner by an existing field; the story uses it at section 12.7. |
| CDC-03198 | RWB-P1-E1065-DB | CG-ALL-2279 | 12.9 | Record ace_view_owner in the owning document as an index, library table or flag, or add the dictionary name the story should use. |
| CDC-03201 | RWB-P1-E1065-DB | DOR-RWB-P1-E1065-DB-7 | 11 | Confirm ace_view_owner as a field or entity in LDM v9 or Data Classification v5, or record it as a role name. |

### RWB-P1-E1065-CON (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03157 | RWB-P1-E1065-APP | DOR-RWB-P1-E1065-APP-21 | none | Complete RWB-P1-E1065-CON and set its build status to Done. |
| CDC-03163 | RWB-P1-E1065-APP | GAP-3086 | 11 | Publish the deviation seed profile with case references, counts per case and shape-to-code mapping; name the stage contract read operations and fields; publish codes and owner roles of R-DEV-05 and R-DEV-06 and the test level. |
| CDC-03167 | RWB-P1-E1065-APP | GAP-0502 |  | Publish the stage interface and its input and output profile, with the four fixtures (full seed, empty seed, refused seed, timeout) and drift detection as a build failure. |
| CDC-03196 | RWB-P1-E1065-DB | DOR-RWB-P1-E1065-DB-21 | header | Set its build status to Done once the contract is published; it is currently 'Not started'. |
| CDC-03197 | RWB-P1-E1065-DB | DOR-RWB-P1-E1065-DB-22 | header | Record the published contract fake library version once one is published. |
| CDC-03208 | RWB-P1-E1065-DB | GAP-0502 |  | Publish the stage interface with its input and output profile (five elements), the four fixtures (full seed, empty seed, refused seed, timeout) and drift detection as a build failure. |
| CDC-03209 | RWB-P1-E1065-DB | GAP-2249 |  | In the case seed profile, fix one open task and one active timer per active case; set remaining timer offsets as timer-table rows at load review. |
| CDC-03210 | RWB-P1-E1065-DB | GAP-2250 |  | In the case seed file, distribute the 2,812 cases by product group to queue rows and cap every member at 40 open cases; tune as a seed-file row. |
| CDC-03218 | RWB-P1-E1065-DB | GAP-1054 | find it | Fix the held item count per exception shape and the page count per held item as seed parameters; name the review reasons the DEV queue must show in the test data section of RWB-P5-E1049-APP. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03024 | RWB-P1-E1017-CON | CG-ALL-2201 | 16 | The Covers column of section 16 follows this story's own criteria and test text. The criterion references in Test Cases v8 differ and are changed in that workbook. |
| CDC-03049 | RWB-P1-E1018-APP | DOR-RWB-P1-E1018-APP-12 | 16 | Add rows TC-E1-018-17 to -19 to Test Cases v8; confirm TC-E1-018-15 and -16; align RTM v7 with story §18 test lists. |
| CDC-03055 | RWB-P1-E1018-APP | CG-ALL-2218 | 16 | Add rows TC-E1-018-15 (Given, When, Then from AC5) and TC-E1-018-16 (Given, When, Then from AC2) to tab Story test cases in the next version. |
| CDC-03131 | RWB-P1-E1064-CON | CG-ALL-2242 | 16 | Add rows TC-E1-064-C01 to TC-E1-064-C08, with Given, When and Then copied from the criterion each covers. |
| CDC-03143 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-12 | 16, 18 | The eight deployment cases named by the item, and the new TC-P1-E1064-OPS-09, are not in Test Cases v8. Section 18 differs from RTM v7. Both sit outside this story. |
| CDC-03151 | RWB-P1-E1064-OPS | CG-ALL-2248 | 16 | Add rows for TC-P1-E1064-OPS-01 to -08 with Given, When and Then copied from the criterion each covers. |
| CDC-03188 | RWB-P1-E1065-CON | CG-ALL-2275 | 16 | Add a row to tab Story test cases for each of TC-P1-E1065-CON-01 to TC-P1-E1065-CON-06 with Given, When and Then copied from AC1 to AC6. |
| CDC-03214 | RWB-P1-E1065-DB | CG-ALL-2281 | 16 | Add rows for TC-P1-E1065-DB-01 to TC-P1-E1065-DB-06 in the next version, with Given, When and Then copied from the criterion each covers. |

### RWB-P1-E1064-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03101 | RWB-P1-E1064-APP | DOR-RWB-P1-E1064-APP-21 | header | Publish the contract and set its build status to Done; currently Not started. |
| CDC-03113 | RWB-P1-E1064-APP | GAP-0890 | section 4 | Step 7 names the query parameters and the isPersonal flag. |
| CDC-03116 | RWB-P1-E1064-APP | GAP-2309 | 4 | Publish the apply order (gate decides and writes no row; load owner moves the version after the gate; dictionary handler applies the rows) in both contracts and in the reference-load handler note. |
| CDC-03136 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-21 |  | Complete the contract build and publish it so its build status is Done. |
| CDC-03137 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-22 |  | Publish a contract fake library version and record its version. |
| CDC-03138 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-23 | Header table | Fix the contract version this story builds against and record it in the Contract version row. |
| CDC-03146 | RWB-P1-E1064-OPS | GAP-0499 | 11 | Secrets row names the rwb_source_data login (DP-02) |
| CDC-03150 | RWB-P1-E1064-OPS | GAP-2309 | 11 | Section 11 names the service's own load path, applied in the approval transaction; the register and contract apply order remains open. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03034 | RWB-P1-E1017-OPS | DOR-RWB-P1-E1017-OPS-1 |  | Add or confirm 'platform engineer' as a role code or role name. |
| CDC-03108 | RWB-P1-E1064-APP | DOR-RWB-P1-E1064-APP-6 | 10 | Add role SY-DATALOAD (data load) |
| CDC-03124 | RWB-P1-E1064-CON | DOR-RWB-P1-E1064-CON-1 | 1 | Add the role 'recovery developer and data steward' or its role code to Users Roles and Permissions v5, or name the existing role it maps to. |
| CDC-03141 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-1 | 1 | Add the role name DevOps engineer, or the role code it maps to, to the role list. |
| CDC-03148 | RWB-P1-E1064-OPS | GAP-0891 | find it | Give RW-REFADM the Reference data A letter in the SIT and production matrices and record RW-REFADM as the approver of a governance load. |
| CDC-03179 | RWB-P1-E1065-CON | DOR-RWB-P1-E1065-CON-1 | 1 | Add role tech lead to Users Roles and Permissions v5, or name the role code this story should use |
| CDC-03199 | RWB-P1-E1065-DB | DOR-RWB-P1-E1065-DB-1 | 1 | Add role 'ACE database engineer' as a role name, or replace the role in section 1 with an existing role. |

### Epic design record (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03018 | RWB-P1-E1017-CON | DOR-RWB-P1-E1017-CON-14 | find it | Record the signed epic design sign-off for RWB-P1-E1017-CON |
| CDC-03030 | RWB-P1-E1017-OPS | DOR-RWB-P1-E1017-OPS-14 |  | Record the signed epic design sign-off for RWB-P1-E1017-OPS. |
| CDC-03100 | RWB-P1-E1064-APP | DOR-RWB-P1-E1064-APP-14 | header | Record the signed epic design sign-off for RWB-P1-E1064-APP in the epic design record; the story cannot carry it. |
| CDC-03120 | RWB-P1-E1064-CON | DOR-RWB-P1-E1064-CON-14 | find it | Record the signed sign-off of the epic design for this epic in the epic design record. |
| CDC-03135 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-14 |  | Record the signed epic design sign-off for RWB-P1-E1064-OPS in the epic design record. |
| CDC-03177 | RWB-P1-E1065-CON | DOR-RWB-P1-E1065-CON-14 | find it | Record the signed epic design sign-off and link it to RWB-P1-E1065-CON |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03020 | RWB-P1-E1017-CON | CG-ALL-2199 | 5, 14 | MSG-GEN-001 is aligned to the standard's meaning in sections 5 and 14; uses with no message are marked Not specified. A new ID is still needed from the business analyst. |
| CDC-03056 | RWB-P1-E1018-APP | DOR-RWB-P1-E1018-APP-9 | 14 | Section 14 texts are aligned to Standard v4 under CG-ALL-2216 and 2217; the remaining difference sits in the P3 document. |
| CDC-03080 | RWB-P1-E1055-APP | DOR-RWB-P1-E1055-APP-9 | 14 | Confirm MSG-P1-001 wording against the FSD P1 v3 rendering or align the standard text |
| CDC-03093 | RWB-P1-E1055-APP | CG-ALL-2227 | 14 | The v4 wording is not available here (see R-15089), so the story keeps the FSD P1 v3 text of MSG-P1-001. |
| CDC-03129 | RWB-P1-E1064-CON | GAP-2306 | 15 | Fix the marker vocabulary (masked, clear) and the coded check names of MSG-P1-002, for example OWNER_ROLE_UNKNOWN, for the dictionary load checks. |
| CDC-03145 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-9 | 14 | MSG-P1-021 text in section 14 was updated under CG-ALL-2247. Any remaining message gap under item 9 sits with the Error and Message Standard. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03175 | RWB-P1-E1065-APP | GAP-1052 | 7 | Content derivation sentence removed. |
| CDC-03192 | RWB-P1-E1065-CON | GAP-0897 | 8 | Fix the rwb-access login in the platform DB story; publish the DEV-only read-only role and its grant list (SELECT on role and permission only); record the retirement of the single-schema grant with DP-15. |
| CDC-03194 | RWB-P1-E1065-CON | GAP-1052 | 1 | Fix the synthetic file naming pattern next to the sandbox file properties; derive file content from the seed value, the case ID and the type so the hash is stable. |
| CDC-03219 | RWB-P1-E1065-DB | GAP-0897 |  | Fix the rwb-access login in the platform DB story; publish the DEV read-only role rwb_sandbox_read and its grant list (SELECT on role and permission only, no access-entry read) in the Service Template Specification; record the retirement of the single-schema grant with DP-15. |
| CDC-03221 | RWB-P1-E1065-DB | GAP-1052 |  | Fix the synthetic file naming pattern next to the sandbox file properties; state that file content is derived from the seed value, the case ID and the type so the hash is stable. |
| CDC-03222 | RWB-P1-E1065-DB | GAP-1053 |  | Record the DEV storage account and container names, the rwb-document login and the DEV read-only role in the Service Template Specification and the Service Catalog; publish the SCR-30 and SCR-31 composite route with RWB-PLT-N001-CON. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03017 | RWB-P1-E1017-CON | CG-ALL-2197 | 12.5 | Add a Workflows row for RetentionRunWorkflow on task queue rwb-source-data, namespace rwb-recovery, or use a catalogued workflow |
| CDC-03019 | RWB-P1-E1017-CON | CG-ALL-2198 | 12.5 | Add activity validateRules on task queue rwb-source-data, as named in section 12.5 |
| CDC-03029 | RWB-P1-E1017-OPS | CG-ALL-2205 | 12.5 | Add to sheet Workflows a P1 rwb-source-data row for RetentionRunWorkflow (queue rwb-source-data, one run per run date and rule version), with its activities as in story section 12.5. |
| CDC-03033 | RWB-P1-E1017-OPS | DOR-RWB-P1-E1017-OPS-8 | 12.5 | Add the RetentionRunWorkflow row (P1, rwb-source-data) to sheet Workflows, as for CG-ALL-2205. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03059 | RWB-P1-E1018-APP | GAP-2433 |  | Write MSG-P7-009 as one sentence naming the field and case reference, and MSG-P7-012 as one chain-position warning; add both rows to the API specification. |
| CDC-03062 | RWB-P1-E1018-APP | GAP-2434 |  | Add finalCall to the query parameters of API-P7-006; fix the creation filter answer as a page of entries with the thirteen fields this story names. |
| CDC-03111 | RWB-P1-E1064-APP | GAP-0498 | section 10 | The story keeps the read path, parameters and answer shape as Not specified; rwb-case must publish the operation and its fake. |
| CDC-03127 | RWB-P1-E1064-CON | GAP-0498 | 11 | Section 11 now states the read path is Not specified in the source documents (GAP-0498) and bans constant lists; the path must be defined in the rwb-case API yaml. |

### RWB-P6-E1055-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03081 | RWB-P1-E1055-APP | GAP-1597 |  | Keep notice and proof fields in rwb-comms; read proof rows through the RWB-P1 contract; rwb-comms matches proof to notice by barcode; ACE write of v_ace_pod goes to the ACE team. |
| CDC-03082 | RWB-P1-E1055-APP | GAP-2090 |  | Hold barcode, callback date and delivery status on the notice row; no separate proof table unless a DB story needs one. |
| CDC-03083 | RWB-P1-E1055-APP | GAP-2096 |  | rwb-comms reads the proof through the P1 contract on the ACE batch business date, matches by barcode and publishes EV-15 NoticeDelivered; no new job. |
| CDC-03092 | RWB-P1-E1055-APP | GAP-1098 |  | Record that the declared area and right are enforced at gateway-bff on the screen path; add the P4 authorise contract as a C dependency or state that a service identity call carries no user right. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03165 | RWB-P1-E1065-APP | GAP-0895 | 11 | Fix the access seed file path, format, version label and row count, and state whether the DEV seed carries the SIT matrix version or a DEV-only label. |
| CDC-03166 | RWB-P1-E1065-APP | GAP-0898 | 11 | Add POST /authorise and GET /me/permissions with request and answer schemas to the API specification and appendix T-A, and stub them in the contract fake; publish the SCR-43 composite route. |
| CDC-03186 | RWB-P1-E1065-CON | GAP-0898 | find it | Add POST /authorise and GET /me/permissions with request and answer schemas, stub them in the contract fake, and publish the SCR-43 composite route with gateway-bff (DP-19). |
| CDC-03207 | RWB-P1-E1065-DB | GAP-0898 |  | Add POST /authorise and GET /me/permissions with request and answer schemas to the API specification and TSD P4 appendix T-A; stub them in the contract fake; publish the SCR-43 composite route with gateway-bff. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03022 | RWB-P1-E1017-CON | GAP-3158 | 12.6 | Assign retention_rule, retention_action and the retention Schedule JOB-17 to P5 rwb_document; P1 keeps a contract read only. |
| CDC-03039 | RWB-P1-E1017-OPS | GAP-0491 |  | No REST path in any source. Story-side consumption wording lies in section 12 and was not changed. |
| CDC-03159 | RWB-P1-E1065-APP | CG-ALL-2267 | 12.7 | Record ace_view_owner as the owner role of the 30 v_ace_* views, or name the owner by its role in Users Roles and Permissions. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03036 | RWB-P1-E1017-OPS | GAP-2426 | 11 | Decision record row states that the values and payload placement are Not specified |
| CDC-03160 | RWB-P1-E1065-APP | CG-ALL-2269 | find it | Add list LOV-RISK-TIER to Lists, or have the story name an existing Reference Data v5 list. |
| CDC-03161 | RWB-P1-E1065-APP | DOR-RWB-P1-E1065-APP-20 | find it | Add list LOV-RISK-TIER to Lists, or have the story name an existing Reference Data v5 list. |

### RWB-P6-E1055-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03086 | RWB-P1-E1055-APP | GAP-1043 |  | Publish the notice read by notice ID and the dispatch reference as one operation with named fields, including the field carrying the INT-14 document reference. |
| CDC-03088 | RWB-P1-E1055-APP | GAP-1100 |  | Attach the WIN owner INT-14 and INT-15 specifications to the file element of the contract baseline as versioned annexes; treat a layout change as a new file version. |
| CDC-03091 | RWB-P1-E1055-APP | GAP-2243 |  | Confirm the element names of the two rows at contract review (NoticeDelivered.v1 and the notice read); rename in this story only if they differ. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03140 | RWB-P1-E1064-OPS | CG-ALL-2246 | 18, 19 | Record v_data_dictionary as a named object (view) with its owning entity in Fields, or record it in the owning document RWB-P1-E1001-APP. |
| CDC-03158 | RWB-P1-E1065-APP | CG-ALL-2266 | 3 | Record iam_user as an ACE Tier 1 table from 15 ACE DB Alignment/ACE Schema PostgreSQL v1.sql, or confirm it is outside LDM scope. |
| CDC-03178 | RWB-P1-E1065-CON | CG-ALL-2273 | find it | Record ace_view_owner as the view owner object of the 30 v_ace views with its dictionary entry, or name the dictionary field it maps to |

### RWB-P4-E1022-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03162 | RWB-P1-E1065-APP | GAP-0896 | 11 | State that the DEV test identity resolves to role.entra_group rows only; the DEV identity list, key format and retirement rule are owned by the platform administrator. |
| CDC-03182 | RWB-P1-E1065-CON | GAP-0896 | find it | State that the DEV synthetic test identity resolves to role.entra_group rows only; record its key format and retirement rule with DL39 in the Service Template Specification. |
| CDC-03203 | RWB-P1-E1065-DB | GAP-0896 | find it | State that the DEV test identity resolves to role.entra_group rows only; owner, key format and retirement rule (DL39) are Not specified in the source documents. |

### RWB-P4-AD002-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03164 | RWB-P1-E1065-APP | GAP-0900 | 11 | Extend the T6.1 matrix to the 14 LOV-CAPABILITY areas and publish the full matrix version with the pack load story. |
| CDC-03184 | RWB-P1-E1065-CON | GAP-0900 | find it | Extend the T6.1 matrix to the 14 LOV-CAPABILITY areas and publish the matrix version with the pack load story. |
| CDC-03205 | RWB-P1-E1065-DB | GAP-0900 |  | Extend the T6.1 matrix to the 14 capability areas of LOV-CAPABILITY and publish the full matrix version with the pack load story. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03190 | RWB-P1-E1065-CON | GAP-1051 | 1 | Publish the per-case document count and the version depth of a seeded document with RWB-P1-E1065-CON, both kept as seed parameters of this story and RWB-P5-E1025-APP. |
| CDC-03193 | RWB-P1-E1065-CON | GAP-0899 | 1 | Publish the 54-role list with administration and non-human roles marked; reconcile it with the 42 rows of TSD P4 T6.1; fix the DEV seed role count. |
| CDC-03220 | RWB-P1-E1065-DB | GAP-0899 |  | Publish the 54-role list in the Service Contract Catalog with administration and non-human roles marked; reconcile it with the 42 rows of T6.1; fix the role count the DEV seed carries. |

### RWB-PLT-TE012-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03023 | RWB-P1-E1017-CON | GAP-0490 | 12 | Publish the write-once archive container contract: account, credential scope, immutability policy, request shape and manifest schema. |
| CDC-03037 | RWB-P1-E1017-OPS | GAP-0490 | 11 | Specify the write-once container contract: account, credential scope, immutability policy, request shape and manifest schema. |

### RWB-P1-E1017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03031 | RWB-P1-E1017-OPS | DOR-RWB-P1-E1017-OPS-21 | header | Build the contract story to Done and publish the contract. Header now names it as a contract dependency. |
| CDC-03035 | RWB-P1-E1017-OPS | GAP-0489 | 11 | Retention-run API row lists POST and GET paths only; request and answer fields are Not specified |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03045 | RWB-P1-E1018-APP | CG-ALL-2211 | 13 | Record key case.entry.dpd in parameter-catalog.csv; rename case.entry.dpd_threshold to case.entry.dpd in Assumptions Register v1 and Test Cases v8. |
| CDC-03050 | RWB-P1-E1018-APP | DOR-RWB-P1-E1018-APP-20 | 13 | Add key case.entry.dpd to parameter-catalog.csv and align the case.entry.dpd_threshold name in the other documents. |

### RWB-P3-E1018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03058 | RWB-P1-E1018-APP | GAP-0676 |  | Record the field-level OpenAPI schema agreed in the RWB-P3-E1018-CON baseline review: required flags, GET /cases page and sort parameters, caseNo pattern, error codes per operation. |
| CDC-03070 | RWB-P1-E1018-APP | GAP-1038 | find it | Name the rwb_document login and grants under DP-02; publish the case-read request and response field names and the not-found message ID in RWB-P3-E1018-CON. |

### RWB-P3-E1043-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03102 | RWB-P1-E1064-APP | DOR-RWB-P1-E1064-APP-22 | 12.8 | Record the published fake library version for the rwb-case reference-data fake named in section 12.8. |
| CDC-03130 | RWB-P1-E1064-CON | GAP-2309 | 4, 8 | Publish the same apply order: the gate records the decision and writes no row, the version moves after the pass, and the handler applies the rows in one transaction. |

### OTHER:TSD P4 v3 T6.1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03103 | RWB-P1-E1064-APP | GAP-2307 | find it | Add the A letter in Reference data to one role in the next matrix version, name it approver of reference and dictionary loads, and forbid the same role submitting and approving. |
| CDC-03139 | RWB-P1-E1064-OPS | GAP-2307 |  | Add the A letter in Reference data to one role in the next matrix version and name that role as approver of reference and dictionary loads; the same role may not submit and approve. |

### RWB-P1-E1064-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03115 | RWB-P1-E1064-APP | GAP-2306 | section 4 | Step 7 cites GAP-2306. |
| CDC-03149 | RWB-P1-E1064-OPS | GAP-2306 |  | Publish /admin/dictionary-authority: query fieldIds, productCodes, role; answer schema per RWB-P4-E1064-APP v2 section 12; markers masked, clear. Add coded check names of MSG-P1-002: Not specified in the source documents (GAP-2306). |

### OTHER:Work package plan (B-P1-02; OTHER:B2-P1-001) and checks/run_all.py (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03118 | RWB-P1-E1064-APP | GAP-2161 | 18 | Remove RWB-E1-064 from the B-P1-02 fanout or retire B2-P1-001 for this key; number CG-B-P1-02-E1064-101, -201 and -301 once; add a plan-uniqueness check that fails when two Write only blocks name one output path. |
| CDC-03217 | RWB-P1-E1065-DB | GAP-2161 | find it | Keep one Work Package per story slice for RWB-E1-064 and add a plan-uniqueness check on duplicate 'Write only' output paths. |

### 06 Data/Recovery Workbench Physical Schema v7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03119 | RWB-P1-E1064-APP | GAP-1506 | 7 | Map all 30 view rows to one data product per object family; use the physical types the views return; mark the two personal view fields personal; write 'ACE (ingested from X)'; counts 16 and 14. |
| CDC-03155 | RWB-P1-E1064-OPS | GAP-1506 | find it | Correct the seed: one data product per object family, view physical types, two view fields marked personal, the wording ACE (ingested from X), and counts 16 and 14. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03170 | RWB-P1-E1065-APP | GAP-1051 |  | Publish the per-case document count and version depth as seed parameters shared with RWB-P5-E1025-APP. |
| CDC-03216 | RWB-P1-E1065-DB | GAP-1051 | find it | Publish the per-case document count and the version depth, and keep both as seed parameters of this story and of RWB-P5-E1025-APP. |

### RWB-ITG-W1J01-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03181 | RWB-P1-E1065-CON | GAP-2154 | 11 | The story points to RWB-ITG-W1J01-ITG for the fixture set's seed, business date, volumes and identifiers. The values are not stated and belong there. |
| CDC-03202 | RWB-P1-E1065-DB | GAP-0384 | find it | Specify the harness repository, environment, namespace, pipeline stage, tooling, fixture composition, reset, report format and gate thresholds (owner QA lead). |

### RWB-S8-E1065-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03183 | RWB-P1-E1065-CON | GAP-3086 | find it | Publish the deviation seed profile with case references and deviation counts per case, the stage contract read operations and fields, the R-DEV-05 and R-DEV-06 codes and owner roles, and the test level of the ten legacy cases. |
| CDC-03204 | RWB-P1-E1065-DB | GAP-3086 |  | Publish the deviation seed profile with case references, shapes and routed states in RWB-P1-E1065-CON; publish deviation counts per case and shape-to-code mapping; name stage contract read operations and fields; publish R-DEV-05/06 codes, owner roles and version. |

### RWB-P4-E1037-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03185 | RWB-P1-E1065-CON | GAP-0895 | find it | Publish the seed file path, format, version label and row count, and state whether the DEV seed carries the SIT matrix version or a DEV-only label. |
| CDC-03206 | RWB-P1-E1065-DB | GAP-0895 |  | Fix the access seed file in rwb-access as a migration resource with path, format, version label and row count; state whether the DEV seed carries the SIT matrix version or a DEV-only label. |

### OTHER:P3 rwb-case story holding SCR-47 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03021 | RWB-P1-E1017-CON | DOR-RWB-P1-E1017-CON-10 | 14 | Add empty, loading, error and no-access states to SCR-47. |

### OTHER:FSD P7 Decision center and log v3; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03026 | RWB-P1-E1017-CON | GAP-2427 | 14 | Cite MSG-P7-009 and MSG-P7-008 texts from Standard v4; allocate ids and texts for the not-found answer and collection gap alert, and confirm the chain-break report message. |

### OTHER:service template (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03027 | RWB-P1-E1017-CON | GAP-2428 | 4 | Record JOB-14 at 02:00 Asia/Bangkok on queue rwb-decision, page size 5000, one run at a time; property names and flag-off behaviour as configuration decisions. |

### OTHER:Recovery Workbench Sequence v6 (items 19 and 21) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03028 | RWB-P1-E1017-CON | GAP-3230 | find it | Drop the RWB-E1-014 and RWB-TE-007 rows at tracker cutover, or keep them struck through with 'retired, not pulled'. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03032 | RWB-P1-E1017-OPS | DOR-RWB-P1-E1017-OPS-22 |  | Publish a fake library version for RWB-P1-E1017-CON and record its version. |

### OTHER:Functional Specification P7 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03040 | RWB-P1-E1017-OPS | GAP-2427 |  | Message texts and ids are not in any source; the P7 business analyst writes them. Not in this story's section 14. |

### OTHER:Service template of rwb-decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03041 | RWB-P1-E1017-OPS | GAP-2428 |  | JOB-14 belongs to rwb-decision; this story does not carry it. |

### OTHER:Platform secret store (ACE team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03042 | RWB-P1-E1017-OPS | GAP-2430 |  | Login name is not in any source; this story's section 4 keeps the generic service login wording. |

### RWB-P7-E1017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03043 | RWB-P1-E1017-OPS | GAP-2432 |  | Mapping concerns the RWB-P7-E1017-APP slice; this story's Level column stays NFR per its note. |

### OTHER:Recovery Workbench sequence v6 (tracker) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03044 | RWB-P1-E1017-OPS | GAP-3230 | none | Drop rows 19 and 21 at tracker cut-over or keep them struck through as 'retired, not pulled'; remove RWB-E1-014 and RWB-TE-007 from Depends on of RWB-E1-056 and RWB-E1-017. |

### OTHER:rwb-source-data contract story (not in the set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03051 | RWB-P1-E1018-APP | DOR-RWB-P1-E1018-APP-21 | Header | Contract dependency row names the rwb-source-data contract without a story key |

### OTHER:Functional Specification Document P3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03054 | RWB-P1-E1018-APP | GAP-1549 | 7 | Restate the A1.5 read path so P3 reads ACE through the rwb-source-data contract (Arch v5 slide 45, ADR-010); keep the business-key link rules unchanged. |

### OTHER:RWB-SVC-P3 database story and the service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03057 | RWB-P1-E1018-APP | GAP-0675 | none | Allocate rwb-case login name, grant set (schema rwb_case only) and secret reference; value Not specified in the source documents (GAP-0675) |

### OTHER:RWB-P7 Technical Solution Design (T3.1; OTHER:T3.3; OTHER:DF-DEC-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03060 | RWB-P1-E1018-APP | GAP-2435 |  | Restate DF-DEC-002 as an indexed business key with no foreign key; drop the recovery_case row of T3.3; state in T3.1 that the ALS business date is carried inside inputs_ref. |

### OTHER:Package ENTRY workbook (rule-row catalogue) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03061 | RWB-P1-E1018-APP | GAP-2436 |  | Name the rule that admits a case in the rule-row catalogue and supply that identifier for the registry fixture of this story. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03063 | RWB-P1-E1018-APP | GAP-0674 |  | Publish the gateway-bff composite route for SCR-02 and SCR-03: path, parallel calls to rwb-case and rwb-source-data, merge order, customer-field masking, 2 s budget. |

### RWB-P2-E2001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03064 | RWB-P1-E1018-APP | GAP-0592 |  | Publish GET /entry-candidates and GET /entry-candidate-facts?businessDate= (one row per candidate account key with personKey, productGroup, REC-05 resolution); correct per-candidate wording at next version. |

### OTHER:Work package C-WEX (work package index) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03066 | RWB-P1-E1018-APP | GAP-3206 | find it | Correct the heading to the subject of the worked example, RWB-E1-020, or record the (E1-018) label as a scheduling label in the next run. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03067 | RWB-P1-E1018-APP | GAP-0982 | find it | Add the case-authority request and answer schema (authorise path) to the API specification and T-A, publish with RWB-P4-E1037-CON, record where caller teams and regions are held in T3.1, and list the case-record personal field IDs with version. |

### OTHER:Work package build sequence (WP index) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03068 | RWB-P1-E1018-APP | GAP-2437 | find it | Record that a secondary slice builds against the platform contracts and section 12.8 fakes and reads wave-1 tables in its own schema, with no dependency row moved. |

### OTHER:Platform deployment template and rwb-case environment values (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03069 | RWB-P1-E1018-APP | GAP-0677 | find it | Publish the rwb-case deployment topology and environment values as values files, not chart defaults. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03071 | RWB-P1-E1018-APP | GAP-2438 |  | Name the per-service login of rwb-decision in the secret store, keeping the migration role and the application role apart |

### OTHER:rwb-integration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03076 | RWB-P1-E1055-APP | GAP-1602 | 12.1 | Hold the WIN dispatch file layout (record set, fields, order, envelope, naming, encoding, barcode and sent-date return) as a versioned interface definition before wave 2. |

### OTHER:P3 story owning SCR-03 and SCR-45 (not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03078 | RWB-P1-E1055-APP | DOR-RWB-P1-E1055-APP-10 | none | Add empty, loading, error and no-access states for SCR-03 and SCR-45 |

### RWB-P1-E1066-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03084 | RWB-P1-E1055-APP | GAP-1097 |  | Add pod records, freshness and batch-status elements with business date, feed version, batch status and stale marker; until then consume DP07 records and freshness endpoints. |

### RWB-P5-E1054-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03085 | RWB-P1-E1055-APP | GAP-1099 |  | Name the stored-letter document read and claim-check handle; until then consume GET /api/recovery/document/v1/documents/{documentId}, 2 s budget, missing letter is held. |

### OTHER:Recovery Workbench document type table (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03087 | RWB-P1-E1055-APP | GAP-1044 |  | Add a proof-of-delivery receipt type, or confirm the type a receipt is stored as with its retention class and write-once flag; confirm the DEMAND to DEMAND_LETTER mapping. |

### RWB-P6-E1055-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03089 | RWB-P1-E1055-APP | GAP-1102 |  | Record host, port, zone, certificate subject and owner, container names, retention and file sizes as reviewed values per environment; confirm with the WIN owner and Security before SIT cutover. |

### RWB-P6-E1055-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03090 | RWB-P1-E1055-APP | GAP-1103 |  | Fix the rwb-comms deployment slot and namespace under DL35, name the dispatch Schedule, record the Airflow window call in the runbook, and assert both in the registration step. |

### OTHER:TSD P5 T3.1 and FSD P1 v3 A2 (proof of delivery) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03095 | RWB-P1-E1055-APP | GAP-1045 | find it | Name barcode, callback date, delivery status and sent type as field_definitions of the receipt type, and state whether a receipt is one document per file or one per notice. |

### OTHER:Message catalogue of FSD P5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03096 | RWB-P1-E1055-APP | GAP-1046 | find it | Add the text of MSG-P5-016 (malware found) to the message catalogue so the upload refusal shows a written message. |

### OTHER:rwb-comms values files and runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03097 | RWB-P1-E1055-APP | GAP-1104 | find it | Set the alert values and the reviewed late-batch time in the values files, confirm them at UAT with the service owner and observability owner, and record each value in its runbook entry. |

### OTHER:TSD P6 v2 T3.1 hold_reason and FSD P6 v3 A2.2 (reference list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03098 | RWB-P1-E1055-APP | GAP-1105 | find it | Publish hold_reason as a versioned reference list with TEMPLATE_WITHDRAWN as its first row, and add the other values with the business owner. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03099 | RWB-P1-E1055-APP | GAP-2246 | find it | Allocate the Data Dictionary field ID for the nullable notice reference column of timer and add it to the ownership map at the next revision. |

### OTHER:Screen specification holding SCR-40 (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03106 | RWB-P1-E1064-APP | DOR-RWB-P1-E1064-APP-10 | not in chunk | Add empty, loading, error and no-access states to SCR-40. |

### RWB-P1-E1001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03110 | RWB-P1-E1064-APP | GAP-0557 | 12.7 | Create P1's 13 own tables in rwb_source_data from its split migration; keep V0001 as built; name login rwb_source_data |

### RWB-P1-E1064-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03112 | RWB-P1-E1064-APP | GAP-0499 | 12.1 | At baseline review set required and nullable flags and string lengths for the five dictionary schemas; the yaml gives none. Keep property names; login rwb_source_data (DP-02). |

### OTHER:TSD P4 v3 (T6.1 role matrix; OTHER:SIT and production) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03114 | RWB-P1-E1064-APP | GAP-0891 | 4 | Give one role the Reference data A letter for API-P4-006 approval and record which role approves a governance load of the authority tables; the four-eyes rule stays the module's. |

### OTHER:TSD P4 v3; OTHER:T6.1 RBAC matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03121 | RWB-P1-E1064-CON | GAP-2307 | find it | Add an A letter in Reference data to one role in the next matrix version, name that role as approver of reference and dictionary loads, and bar the same role from submitting and approving. |

### RWB-P1-E1069-APP; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03122 | RWB-P1-E1064-CON | CG-ALL-2239 | 12.7 | Record ace_view_owner as the view owner object in the owning document, or use the dictionary name. |

### RWB-P1-E1001-APP; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03123 | RWB-P1-E1064-CON | CG-ALL-2240 | 12.7 | Record v_data_dictionary as the read model object in the owning document, or use the dictionary name. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03125 | RWB-P1-E1064-CON | DOR-RWB-P1-E1064-CON-12 | 16 | Add the TC-E1-064-C01 to C08 rows to Test Cases v8; align the RTM v7 test lists with section 18; C09 boundary row added to section 16. |

### OTHER:TSD P4 v3 T6.1 role matrix; OTHER:SIT and production (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03128 | RWB-P1-E1064-CON | GAP-0891 | find it | Give one role the Reference data A letter and record which role approves a governance load of the authority tables. |

### OTHER:Work Package plan for the run and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03133 | RWB-P1-E1064-CON | GAP-2161 | none | Remove RWB-E1-064 from the B-P1-02 fanout, keep B2-P1-001 as the single WP for this key, and add a plan-uniqueness check to checks/run_all.py. |

### RWB-P1-E1001-APP; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03134 | RWB-P1-E1064-CON | GAP-1506 | none | Correct the seed: one data product per object family, the physical types the views return, the two personal view fields marked personal, the wording 'ACE (ingested from X)', and the counts 16 and 14. |

### OTHER:P3 SCR-40 screen definition (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03142 | RWB-P1-E1064-OPS | DOR-RWB-P1-E1064-OPS-10 |  | Add empty, loading, error and no-access states for SCR-40. |

### RWB-P4-E1064-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03147 | RWB-P1-E1064-OPS | GAP-0890 |  | Add GET /admin/dictionary-authority and POST /admin/dictionary-authority-loads/{loadId}/approve and /return, with the query, answer fields and markers masked, clear exactly as in section 12 of that story. |

### OTHER:SCR-40 screen definition (Screen Specifications) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03153 | RWB-P1-E1064-OPS | CG-ALL-2250 | 15 | Section 15 records the empty, loading, error and no access states as Not specified in the source documents |

### OTHER:Work Package plan generator (checks/run_all.py) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03154 | RWB-P1-E1064-OPS | GAP-2161 | find it | Keep one WP per slice for RWB-E1-064: remove it from B-P1-02 fanout or retire B2-P1-001; number CG-B-P1-02-E1064-101, -201, -301 once; add a plan-uniqueness check on Write only paths. |

### OTHER:Recovery Workbench Service Story Files v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03156 | RWB-P1-E1065-APP | CG-ALL-2270 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that carries the rwb-decision rule evaluation capability for the DP-04 C row. |

### RWB-PLT-NF06-DB; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03168 | RWB-P1-E1065-APP | GAP-2251 |  | Set the rwb-case login at RWB-PLT-NF06-DB and confirm the field identifiers of queue, queue_member, assignment, task, timer, case_entry_exclusion and reference_version against the LDM and Data Dictionary v8. |

### OTHER:Work Package plan (B-P1-02; OTHER:B2-P1-001) and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03171 | RWB-P1-E1065-APP | GAP-2161 |  | Remove RWB-E1-064 from the B-P1-02 fanout or retire B2-P1-001 for this key; add a plan-uniqueness check for duplicate write paths. |

### RWB-P1-E1065-CON; RWB-P5-E1049-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03172 | RWB-P1-E1065-APP | GAP-1054 |  | Fix the held item count per shape and pages per item as seed parameters in RWB-P1-E1065-CON; name the review reasons in the RWB-P5-E1049-APP test data. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:RWB-PLT platform DB story (rwb-access login) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03173 | RWB-P1-E1065-APP | GAP-0897 |  | Publish DEV-only read-only role rwb_sandbox_read with grants SELECT on role and permission only, no access-entry read; fix rwb-access login; record retirement of single-schema grant with DP-15. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:TSD P4 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03174 | RWB-P1-E1065-APP | GAP-0899 |  | Publish the 54-role list with administration and non-human roles marked; reconcile with the 42 rows of T6.1; fix the DEV seed role count. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03176 | RWB-P1-E1065-APP | GAP-1053 |  | Record DEV storage account and container names, the rwb-document login and the DEV read-only role; publish SCR-30 and SCR-31 composite route with RWB-PLT-N001-CON. |

### OTHER:RWB-TE-004 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03187 | RWB-P1-E1065-CON | GAP-1435 | 12 | Fix the staging suffix per service, the per-service extract layout, the personal-data field-registry operation and the tool schema name for the 19-schema load; working defaults ASM-B-PLT-TPL-02-TE004-1, -2 and -3 apply until then. |

### OTHER:Plan generator; OTHER:Work Package plan and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03191 | RWB-P1-E1065-CON | GAP-2161 |  | Remove RWB-E1-064 from B-P1-02 fanout or retire B2-P1-001 for this key; number CG-B-P1-02-E1064 rows once; add a plan-uniqueness check for duplicate Write only paths. |

### RWB-PLT-N001-CON; 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03195 | RWB-P1-E1065-CON | GAP-1053 | 8 | Record the DEV storage account and container names, the rwb-document login and the DEV read-only role; publish the SCR-30 and SCR-31 composite route with RWB-PLT-N001-CON. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03200 | RWB-P1-E1065-DB | DOR-RWB-P1-E1065-DB-12 | 12.7, 16, 18 | Register TC-P1-E1065-DB-01 to 07 in Test Cases v8; align the section 18 test lists with RTM v7 for REQ-RDF-001 and REQ-RDF-010. |

### RWB-P1-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03211 | RWB-P1-E1065-DB | GAP-2252 | find it | Name the decision code of RWB-P3-E1018-APP for the seeded creation record and the code of RWB-P3-E1019-APP or the exclusion rule for seeded exclusions; confirm at the decision-record contract review. |

### RWB-PLT-NF06-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03212 | RWB-P1-E1065-DB | GAP-2251 | find it | Set the rwb-case login name. Confirm field identifiers of queue, queue_member, assignment, task, timer, case_entry_exclusion and reference_version against Logical Data Model and Data Dictionary v8. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-03213 | RWB-P1-E1065-DB | GAP-3194 | find it | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the column drop, or attach the drop to the APP story; cite the chosen story on row 121 before wave 2. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20727 | RWB-P1-E1064-APP | R-22239 |  | Reference data A letter for API-P4-006 and approver role sit in TSD P4 T6.1 matrix; API-P4-006 is not in this FSD (GAP-0891). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0342 | E1017 retention ownership and the P1 interaction path | Solution architect | Resolved (directive) |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0366 | WIN file path, proof-of-delivery read and interaction ledger home move in the target | Tech lead | Resolved (directive) |
| GAP-0373 | Reference-load operation owner, ACE view value read and contract confirmation form are not named for the target | P1 source data owner, P3 case owner and P4 access owner | Resolved (directive) |
| GAP-0374 | The per-schema seed volumes, the seeding order across the 19 baselines and the cutover from the one recovery schema are not stated | Solution architect | Resolved (directive) |
| GAP-0384 | The wave 1 contract-test harness, its pipeline wiring and the synthetic test data set are not specified | QA lead | Resolved (directive) |
| GAP-0488 | retention_rule ownership: TSD P1 v3 keeps it in P1, the Ownership Map and Arch v5 move retention to P5 | Solution architect | Resolved (directive) |
| GAP-0489 | The rwb-source-data retention-run contract shape is not specified | Solution architect | Resolved (directive) |
| GAP-0490 | The write-once archive contract (container, path and manifest) belongs to RWB-PLT-TE012-APP and is not specified | Solution architect | Resolved (directive) |
| GAP-0491 | The legal-hold query is a published interface with no REST path in the sources | Solution architect | Resolved (directive) |
| GAP-0498 | The read of the rwb-case reference-data contract that returns a table of values is not specified | Solution architect | Resolved (directive) |
| GAP-0499 | The field-level detail of the five dictionary schemas and the login wording of the contract baseline are not specified | Tech lead | Resolved (directive) |
| GAP-0500 | No deployment value, probe timing, alert threshold or incident route exists for the dictionary slice | DevOps lead | Resolved (directive) |
| GAP-0501 | The sandbox scope per service and the placement of the generator module are not specified | Solution architect | Resolved (directive) |
| GAP-0502 | The contract of a build tool is not described by any source document | Tech lead | Resolved (directive) |
| GAP-0503 | The sandbox database scope and its read-only role name are not specified | ACE data architect | Resolved (directive) |
| GAP-0557 | RWB-P1-E1001-APP: schema-split mechanics, login name, extension-table delivery boundary and Arch v5 against FSD and TSD P1 | Solution architect | Resolved (directive) |
| GAP-0571 | The entry-candidate contract: the resource and parameter names, the response entity, its field names, the paging, the error status set and the access rule are not fixed by any source, and this legacy key has no contract story of its own | Tech lead of rwb-source-data with the solution architect and the P3 owner of the case contract | Resolved (directive) |
| GAP-0572 | Whether the entry read is one operation for a business date or one operation per account, and how a page of about 28,100 candidates is cut, are not specified | Tech lead of rwb-source-data with the owner of the rwb-case case creation job | Resolved (directive) |
| GAP-0573 | Which service writes account_ext.dispute_open and the party_ext flags, which right the confirmation needs, and where party_ext.vulnerable comes from on the first write are not settled | Solution architect with the P1 service owner, the P3 owner of the exclusion screen and the P4 owner of the role model | Resolved (directive) |
| GAP-0574 | The ALS batch gate before RWB-ACE-001 lands: v_ace_batch_status is a Section B view, and the behaviour of an entry read for a date whose batch record does not exist yet is not specified | Recovery tech lead with the ACE team lead and the platform team that owns the RWB-ACE-001 sequence | Resolved (directive) |
| GAP-0575 | The shape and the home of the REC-05 break list are not specified, and the table that held it leaves the schema | Data architect with the data steward and the P1 owner of the reconciliation job | Resolved (directive) |
| GAP-0576 | The product group of a candidate row: whether the ACE product_category value is passed through or mapped to the LOV-PRODUCT codes, and what happens to a value outside the list, is not specified | Business analyst, P1 with the center of excellence and the owner of the rwb-case reference data | Resolved (directive) |
| GAP-0577 | The address, the answer envelope and the paging of the proof-of-delivery read of rwb-source-data are not fixed by any source: the sources name a data-product records path, the contract of this key names another, and no source names the page parameters, the element types or the error set | Solution architect | Resolved (directive) |
| GAP-0578 | No source settles who writes the delivery entry on the interaction ledger, nor which case the entry belongs to: the legacy story writes it in rwb-comms, the contract and the app story of rwb-comms say rwb-comms calls the ledger writer, the work package of this key gives the write to rwb-source-data, and the pod row carries an account key and no case | Solution architect | Resolved (directive) |
| GAP-0579 | No source names what the proof-of-delivery read answers before RWB-ACE-001 deploys the Section B views, nor the flag that holds it: the sources require the feature to stay behind a flag and the product to show stale, and give neither the answer shape, the reason code nor the flag name | Solution architect | Resolved (directive) |
| GAP-0580 | No source says where the repeat of a proof-of-delivery read is counted when the read writes no second entry: R-UNI-40 asks for the hit to be recorded and names no counter, and the two candidate counters belong to two different mechanisms | Data architect | Resolved (directive) |
| GAP-0581 | No source fixes the render of MSG-P1-001 for the WIN proof of delivery: the legacy story names the product 'DP07 Legal', the FSD names the ACE batch and the product code, and the date is either the last complete business date or the due date | Business analyst | Resolved (directive) |
| GAP-0592 | No source splits the hand-over facts between the candidate rule and the borrower and product-group facts, and the run's contract names a per-candidate customer read | Solution architect, P1 and P2 | Resolved (directive) |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0675 | Per-service login name for rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0676 | Field-level OpenAPI schema of the case resource is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0677 | Deployment topology detail for rwb-case is not specified | DevOps engineer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0890 | The register operations, their field names, the marker vocabulary and the read path are not in the sources | Solution architect, with the data steward | Resolved (directive) |
| GAP-0891 | No role holds the Reference data A letter that API-P4-006 requires of an approver | Security administrator, with the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0892 | The number of personal fields among the 1,366 is not stated | Data steward | Resolved (directive) |
| GAP-0893 | The apply path of an approved governance load is not assigned | Solution architect, with the reference data administrator | Resolved (directive) |
| GAP-0895 | rwb-access sandbox seed: the access seed file's location, format, version label and row count are not specified, and whether the DEV matrix version must equal the SIT version is not stated | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0896 | rwb-access sandbox seed: the owner, the key format and the retirement rule of the DEV synthetic test identity per role are not specified | Platform administrator | Resolved (directive) |
| GAP-0897 | rwb-access sandbox seed: the per-service login name and the DEV-only read-only role over rwb_access are not fixed for the target schema | Platform DB owner | Resolved (directive) |
| GAP-0898 | rwb-access sandbox seed: the authorise and me/permissions request and answer shapes, and the screen route that shows the seeded rows, are absent from the TSD appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0899 | rwb-access sandbox seed: the legacy seed loads 54 roles, while the TSD P4 RBAC matrix tabulates 42 role rows, and the difference is not enumerated | Business analyst, P4 | Resolved (directive) |
| GAP-0900 | rwb-access sandbox seed: the matrix letters for 11 of the 14 capability areas are not tabulated, so the seed content has no source table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1038 | The rwb-document login name, the not-found message ID of the case read and the case-read field names are not specified | Solution architect with the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1043 | The rwb-comms operations and field names behind RWB-P6-E1055-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1044 | The document type of the WIN proof-of-delivery receipt and the notice-type to document-type mapping | Center of excellence analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1045 | The field names of the WIN receipt in document_field and the receipt granularity | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1046 | The text of MSG-P5-016 | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1052 | The file-name pattern of the synthetic documents is not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1054 | The count of held intake items per exception shape and the pages each held item carries are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1097 | The pod and batch-status contract elements are not named in RWB-P1-E1066-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1098 | No access guard story covers the notice read of rwb-comms | Solution architect | Resolved (directive) |
| GAP-1099 | The stored letter retrieval is not named in RWB-P5-E1054-CON | Solution architect | Resolved (directive) |
| GAP-1100 | The INT-14 and INT-15 fixed layouts, their record keys and their transport are not in the source material | Solution architect | Resolved (directive) |
| GAP-1101 | The owner of REC-05 and of the References exception list is not named | Solution architect | Resolved (directive) |
| GAP-1102 | The WIN host, port, zone, certificate owner, container names and file sizes are not in the source material | SCB IT infrastructure | Resolved (directive) |
| GAP-1103 | The deployment slot and namespace of rwb-comms, and the exact form of the JOB-10 Airflow handoff, are not specified | DevOps lead | Resolved (directive) |
| GAP-1104 | No source gives the alert thresholds, the reviewed time of the late WIN batch or the Schedule state per environment | DevOps lead | Resolved (directive) |
| GAP-1105 | Only one hold reason is named for a notice | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1169 | The notice barcode break is REC-09 in RWB-E1-011 and REC-05 in RWB-E1-055, where RWB-E1-011 uses REC-05 for the business-key orphan check | Data steward | Resolved (directive) |
| GAP-1435 | The per-service staging schema, the per-service extract layout, the personal-data field registry operation and the tool schema are not defined for the 19-schema masked copy | Solution architect | Resolved (directive) |
| GAP-1506 | The physical dictionary mapping and the system-of-record wording disagree with the frozen view list | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-2090 | The proof of delivery is named as P6 data but has no table, no DDL and no owner row | Service owner of P6 rwb-comms, with the DB story of the service | Resolved (directive) |
| GAP-2096 | No event, job or window tells rwb-comms that a proof of delivery has arrived | Service owners of P6 rwb-comms and P1 rwb-source-data; integration owner | Resolved (directive) |
| GAP-2137 | Which service seeds which rows of the shared case set is not specified | QA | Resolved (directive) |
| GAP-2154 | The seed, business date, volumes and identifiers of the synthetic fixture set are not stated | QA lead | Resolved (directive) |
| GAP-2161 | Two Work Packages write the same three story files and three fragments for legacy RWB-E1-064 on rwb-source-data | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2243 | Element names of the delivery fact and of the notice answer are not in the sources read for this work package | TechX and rwb-comms contract owner | Resolved (directive) |
| GAP-2246 | The timer has no field for the notice it belongs to, and its field ID is unallocated | rwb-case data owner and the Data Dictionary owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2247 | The notice period is owned by two rwb-case stories of the same legacy loop | TechX | Resolved (directive) |
| GAP-2249 | Task and timer counts per seeded case, and the timer offsets beyond the FSD P3 AC-ALT-P3-011 offsets, are not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2250 | The distribution of the 2,812 seeded cases across the 12 queues and 48 members is not in the sources | TechX and the P3 business analyst | Resolved (directive) |
| GAP-2251 | The rwb-case login name, the DEV read-only role name and the field identifiers of six seeded tables are not in the sources | TechX and the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2252 | The decision code and the payload of the decision records the seed writes are not in the sources | TechX and the rwb-decision contract owner | Resolved (directive) |
| GAP-2306 | No source names the register's request and answer field names, its marker vocabulary or its read path, and the module FSD and TSD give the tables and the endpoint inventory only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2307 | TSD P4 T6.1 gives no role the Reference data A letter that API-P4-006 requires of an approver, so the four-eyes approver of a governance load is unnamed | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2309 | No target source states which service applies an approved dictionary load, and the legacy reference-load endpoint no longer exists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2426 | The decision code, final call, action and outcome values and the payload placement of an archive or purge record are in no source | Solution architect | Resolved (directive) |
| GAP-2427 | The text of MSG-P7-009 and the ids and texts of the not-found answer, the chain-break report and the collection gap alert are not written in any source | Business analyst, P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2428 | The JOB-14 timezone, page size, overlap and catch-up values, the property names and the behaviour of the feature flag when off are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2430 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2431 | The story file at the Work Package path already existed as a partial artefact of the superseded Work Package B-P7-05, with no fragment, no register rows and citations that resolve to nothing | Delivery lead, with the traceability owner | Resolved (directive) |
| GAP-2432 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept | Traceability owner | Resolved (directive) |
| GAP-2433 | The message text of MSG-P7-009 and of the chain warning MSG-P7-012 is named in the sources but never written | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2435 | TSD P7 still models decision_log_entry.case_id as a uuid with a relationship to recovery_case and gives the row no business-date column | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2436 | The literal rule ID of the ENTER rule of package ENTRY is named in no source | Business analyst, Epic 1 | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2438 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3086 | RWB-S8-E1065-APP: the deviation slice of the sandbox has no published case-reference source, no deviation count per case or per code, no operation or field names for the stage contract read, no codes or owner roles for R-DEV-05 and R-DEV-06, no test level for the ten legacy cases and an empty H row for eight patterns | Solution architect, with the rwb-deviation owner, the rwb-case and rwb-document owners, the rwb-source-data sandbox owner, the rule-set owner of the Deviations package, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3158 | The retention tables are P1 tables in the story and P5 tables in the Ownership Map | P5 document owner | Resolved (directive) |
| GAP-3162 | The case story writes the P1 extension tables | P3 case owner | Resolved (directive) |
| GAP-3168 | The sandbox story applies three migrations where 19 schemas now need their own sequence | ACE DB lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3230 | Two retired items still carry v6 windows and dependencies | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P1-E1055-APP | unknown story key | 24 | RWB-P1-E1055-CON is not a story of the set: \| Contract dependencies \| RWB-P6-E1055-CON; RWB-P1-E1055-CON; rwb-source-data.yaml version 5.0.0 (API Specification v5) \| |
| RWB-P1-E1055-APP | unknown story key | 428 | RWB-P1-E1055-CON is not a story of the set: \| TC-E1-055-13 \| AC1, AC6 — contract of the proof-of-delivery operation of §12: the ten fields of the view in the answer \| Contract \| Operat |
