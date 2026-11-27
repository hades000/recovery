# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 2 of 11 (RWB-P4-AD008-CON to RWB-P4-AD015-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 15 |
| Resolved in the stories | 272 |
| Cross-document (pending in another document) | 216 |
| Not applied (value not in the sources) | 27 |
| Open business decisions | 11 |
| Register gaps linked | 68 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-AD008-CON | 14 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD008 CON Access review list - contract v2.md |
| RWB-P4-AD009-APP | 18 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD009 APP Load a list of values version v2.md |
| RWB-P4-AD009-CON | 19 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD009 CON Load a list of values version - contract v2.md |
| RWB-P4-AD010-APP | 22 | 10 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD010 APP Approve a reference data load v2.md |
| RWB-P4-AD010-CON | 17 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD010 CON Approve a reference data load - contract v2.md |
| RWB-P4-AD011-APP | 11 | 14 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD011 APP Load a rule version v2.md |
| RWB-P4-AD011-CON | 16 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD011 CON Load a rule version - contract v2.md |
| RWB-P4-AD012-APP | 21 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD012 APP Approve a rule version v2.md |
| RWB-P4-AD012-CON | 19 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD012 CON Approve a rule version - contract v2.md |
| RWB-P4-AD013-APP | 21 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD013 APP Roll back a rule or reference version v2.md |
| RWB-P4-AD013-CON | 22 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD013 CON Roll back a rule or reference version - contract v2.md |
| RWB-P4-AD014-APP | 22 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD014 APP Configure queues v2.md |
| RWB-P4-AD014-CON | 22 | 8 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD014 CON Configure queues - contract v2.md |
| RWB-P4-AD015-APP | 11 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD015 APP Configure service levels and timers v2.md |
| RWB-P4-AD015-CON | 17 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD015 CON Configure service levels and timers - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-AD013-APP | R-01143 | CG-ALL-4762 | Script gap | Product owner | The story adds REFERENCE to the closed list LOV-ROUTE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-AD014-APP | R-01151 | CG-ALL-4782 | Script gap | Product owner | The story adds ASSIGNMENT_METHOD_UNKNOWN to the closed list LOV-ASSIGN | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-AD011-APP | R-10590 | CG-ALL-4735 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-AD014-ITG, RWB-P4-AD014-APP, RWB-P4-AD014-CON | R-21777 | GAP-0859 | Register gap | Product owner | rwb-access queue load: no caseload cap value and no default cap is specified | Keep the cap out of code entirely: a row without a cap is accepted, a cap present is validated as a positive integer, and the values are supplied by the business through DL23 when they are agreed. |
| RWB-P4-AD011-APP, RWB-P4-E8007-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON | R-28970 | GAP-0878 | Register gap | Business analyst, with the compliance and PDPA officer | The legacy story carries a rule-change capability it does not have | Keep the capability, the two criteria, the five messages and the four test ids, leave the rule-version endpoints and the rule_row row with RWB-P4-E8007-APP and RWB-P4-AD011-APP, and read the rule version of AC1 as the version of the parameter row in force. |
| RWB-P4-AD011-APP | R-33447 | ASM-ALL-4735 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-AD008-CON | R-05499 | DOR-RWB-P4-AD008-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off value in the story or source docs (searched project folder for 'epic design'; only _work scratch hits). Cannot record without inventing a value. |
| RWB-P4-AD010-APP | R-05513 | DOR-RWB-P4-AD010-APP-14 |  | Definition of Ready item 14 Epic design: Fail | Not specified in the source documents (DOR-RWB-P4-AD010-APP-14). Grep of the project folder found no signed epic design record, so sign-off cannot be confirmed. |
| RWB-P4-AD010-APP | R-05516 | DOR-RWB-P4-AD010-APP-22 |  | Definition of Ready item 22 Fake published: Fail | Not specified in the source documents (DOR-RWB-P4-AD010-APP-22). Grep found no contract fake library or published fake version; publishing one would invent a value. |
| RWB-P4-AD011-APP | R-05523 | DOR-RWB-P4-AD011-APP-14 |  | Definition of Ready item 14 Epic design: Fail | Sign-off section not in chunk; story file not found under folder 22. Epic design record not in sources (DOR-RWB-P4-AD011-APP-14). |
| RWB-P4-AD011-APP | R-05527 | DOR-RWB-P4-AD011-APP-23 |  | Definition of Ready item 23 Contract version fixed: Fail | Section naming the contract build was not in chunk; story file not found under folder 22. No contract version in sources (DOR-RWB-P4-AD011-APP-23). |
| RWB-P4-AD011-APP | R-16488 | DOR-RWB-P4-AD011-APP-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 text not in chunk; story file not found under folder 22, so no old text to copy. Needs the SCR-39 and SCR-47 states there. |
| RWB-P4-AD011-APP | R-16490 | DOR-RWB-P4-AD011-APP-18 | 2 | Definition of Ready item 18 Open decisions: Partial | Section 2 not in chunk; story file not found under folder 22. No assumption ID for DL24 in sources (DOR-RWB-P4-AD011-APP-18). |
| RWB-P4-AD011-APP | R-22983 | GAP-0821 | metadata | rwb-access rule-version load: the rule registry is P7's but the story's contract-dependency list carries no P7 rule-package contract | RWB-P7-AD011-CON is not in the sources or the story set; the dependency ID cannot be given here. |
| RWB-P4-AD011-APP | R-22985 | GAP-0868 | 8 and 11 | The rule-change request record while the registry, the load gate and the approval belong to other stories | Sections 8 and 11 not in chunk; story file not found under folder 22. Five values not in sources, so the proposed fix cannot be applied here. |
| RWB-P4-AD011-APP | R-23025 | GAP-0825 | 7 and 17 | rwb-access rule-version load: whether a row without a test case ID refuses the version at upload or at approval is ambiguous | AC2 (section 7) and section 17 not in chunk; story file not found under folder 22. Refuse-at-upload change must be made where that text sits. |
| RWB-P4-AD011-APP | R-23217 | GAP-2288 |  | The pack, its three check codes, the two operations, the five schemas, the parameter rows, the decided-version rule and the record code are not in the sources | Pack, check and schema text not in chunk; story file not found under folder 22. Pack definition not in sources (GAP-2288). |
| RWB-P4-AD011-CON | R-22983 | GAP-0821 | header | rwb-access rule-version load: the rule registry is P7's but the story's contract-dependency list carries no P7 rule-package contract | Contract dependencies row was not changed in the story. Replacing None with RWB-P7-AD011-CON conflicts with GAP-0857 (R-28514), which keeps None. |
| RWB-P4-AD012-APP | R-05533 | DOR-RWB-P4-AD012-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source documents. Grep found hits only in _work/msr directive scratch files, not sources. Sign-off value not specified; no edit. |
| RWB-P4-AD012-CON | R-25288 | CG-ALL-4761 | find it | Story cites document versions that are not the highest | API Specification v4 citation is not in the supplied story parts. Grep of the project found no match in the RWB-P4-AD012-CON story. Nothing to edit. |
| RWB-P4-AD013-CON | R-05550 | DOR-RWB-P4-AD013-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for EP08 or RWB-SVC-P4 in the story. A grep of 22 Microservice Realignment for 'epic design' found only generic mentions, so the sign-off cannot be confirmed without an invented value. No edit. |
| RWB-P4-AD013-CON | R-28974 | GAP-0850 | 7 | rwb-access rollback gate: 'with an immediate date' is not defined, and no source says whether a rollback may be dated in the future or the past | No source says whether a rollback may be dated in the past or future. A past-date refusal was not sourced and has been removed. Left for an owner decision. |
| RWB-P4-AD014-APP | R-28514 | GAP-0857 | 12.2 | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Section 12.2 endpoints row is not in the supplied text. Story file not found under 22 Microservice Realignment by key, so old text cannot be copied exactly. Needs 12.2 text. |
| RWB-P4-AD014-CON | R-05563 | DOR-RWB-P4-AD014-CON-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the chunk or sources (previously searched). Sign-off cannot be stated; needs the epic design record. |
| RWB-P4-AD014-CON | R-21776 | GAP-0858 | not in chunk | rwb-access queue load: the queue file layout is not specified, and the legacy file's member sheet is a P3 table | Queue file section not in this chunk. Sheet name and header order stay Not specified in the source documents (GAP-0858). Resend that section. |
| RWB-P4-AD014-CON | R-21779 | GAP-0864 | not in chunk | rwb-access queue load contract: no source publishes the queue-row schema or the file layout the document must declare | Contract schema section not in this chunk. Sheet name and header order stay Not specified in the source documents (GAP-0864). Resend that section. |
| RWB-P4-AD014-CON | R-28400 | GAP-0861 | not in chunk | rwb-access queue load: the required answer carries a version label and a state the owner's load schema does not return, and the load decision code is not specified | Load answer section not in this chunk. Load decision code stays Not specified in the source documents (GAP-0861). Resend that section. |
| RWB-P4-AD014-CON | R-28401 | GAP-0862 | not in chunk | rwb-access queue load: legacy AC1 states an allocation outcome that this story does not own | AC1 and its test row not in this chunk. Resend sections 7 and 16 so the rwb-case contract proof can be added (GAP-0862). |
| RWB-P4-AD014-CON | R-28514 | GAP-0857 | not in chunk | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Endpoints table and RWB-E1-019 dependency text not in this chunk; header rows say None. Resend those parts to edit (GAP-0857). |
| RWB-P4-AD015-APP | R-05567 | DOR-RWB-P4-AD015-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-P4-AD015-APP in the story or 22 Microservice Realignment. Grep hits are generic DoR and governance text. Sign-off cannot be confirmed from sources. |
| RWB-P4-AD015-APP | R-05570 | DOR-RWB-P4-AD015-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in the sources searched (22 Microservice Realignment). Writing one would invent a value. Story sections beyond the header were not supplied. |
| RWB-P4-AD015-APP | R-05571 | DOR-RWB-P4-AD015-APP-23 |  | Definition of Ready item 23 Contract version fixed: Fail | Story names only the /v1 path. No contract version found in the sources searched (22 Microservice Realignment). Story sections beyond the header were not supplied, so no text could be edited. |
| RWB-P4-AD015-CON | R-25309 | CG-ALL-4814 | find it | Story cites document versions that are not the highest | No API Specification v4 citation in the header lines given (1-32) or the section headings. Needs the chunk holding the citation (section text), then cite v5. Not in this chunk. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (43)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07601 | RWB-P4-AD008-CON | CG-ALL-4685 | 12.1 | Publish GET /api/recovery/access/v1/admin/access-reviews/{reviewId} in rwb-access.yaml, through RWB-P4-AD008-CON. |
| CDC-07602 | RWB-P4-AD008-CON | CG-ALL-4686 | 12.1 | Publish POST /api/recovery/access/v1/admin/access-reviews/{reviewId}/decisions in rwb-access.yaml, through RWB-P4-AD008-CON, with the Idempotency-Key header. |
| CDC-07603 | RWB-P4-AD008-CON | CG-ALL-4687 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through provider story RWB-P4-E1037-CON. |
| CDC-07605 | RWB-P4-AD008-CON | DOR-RWB-P4-AD008-CON-8 | 12.1, 12.2 | Publish GET and POST access-reviews paths and POST /api/recovery/access/v1/authorise, with the Idempotency-Key header on the POST decisions operation. |
| CDC-07620 | RWB-P4-AD009-APP | CG-ALL-4695 | 12.1 | Publish POST /api/recovery/access/v1/admin/lov-loads in rwb-access.yaml through RWB-P4-AD009-CON. |
| CDC-07621 | RWB-P4-AD009-APP | CG-ALL-4696 | 12.1 | Publish GET /api/recovery/access/v1/admin/lov-loads/{loadId} in rwb-access.yaml through RWB-P4-AD009-CON. |
| CDC-07622 | RWB-P4-AD009-APP | CG-ALL-4697 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through RWB-P4-AD009-CON; owner is this service. |
| CDC-07626 | RWB-P4-AD009-APP | DOR-RWB-P4-AD009-APP-8 | 12.1 | Publish the lov-loads POST and GET operations and POST /api/recovery/access/v1/authorise in rwb-access.yaml. |
| CDC-07631 | RWB-P4-AD009-CON | CG-ALL-4705 | 12.1 | Add path /admin/lov-loads with POST under base /api/recovery/access/v1, per section 12.1 (multipart, Idempotency-Key, 201/401/403/409/422/503). |
| CDC-07632 | RWB-P4-AD009-CON | CG-ALL-4706 | 12.1 | Add path /admin/lov-loads/{loadId} with GET under base /api/recovery/access/v1 (200 LovLoad, 404 unknown loadId, 401/403/503). |
| CDC-07633 | RWB-P4-AD009-CON | CG-ALL-4707 | 12.2 | Add path /api/recovery/access/v1/authorise with POST, owner P4 rwb-access, as the recommended provider-side publication. |
| CDC-07634 | RWB-P4-AD009-CON | DOR-RWB-P4-AD009-CON-8 | 12.1 | Publish POST /admin/lov-loads with the required Idempotency-Key header, plus the GET /admin/lov-loads/{loadId} and POST /api/recovery/access/v1/authorise paths. |
| CDC-07639 | RWB-P4-AD010-APP | CG-ALL-4711 | 12.1 | Publish POST /api/recovery/access/v1/admin/lov-loads/{loadId}/approve through RWB-P4-AD010-CON |
| CDC-07640 | RWB-P4-AD010-APP | CG-ALL-4712 | 12.1 | Publish POST /api/recovery/access/v1/admin/lov-loads/{loadId}/return through RWB-P4-AD010-CON |
| CDC-07641 | RWB-P4-AD010-APP | CG-ALL-4713 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story |
| CDC-07643 | RWB-P4-AD010-APP | DOR-RWB-P4-AD010-APP-8 | 12.1 | Publish POST approve, POST return and POST /api/recovery/access/v1/authorise in the yaml as in CG-ALL-4711 to CG-ALL-4713 |
| CDC-07649 | RWB-P4-AD010-CON | CG-ALL-4720 | 12.1 | Add path POST /api/recovery/access/v1/admin/lov-loads/{loadId}/approve as the operation in RWB-P4-AD010-CON §12.1 |
| CDC-07650 | RWB-P4-AD010-CON | CG-ALL-4721 | 12.1 | Add path POST /api/recovery/access/v1/admin/lov-loads/{loadId}/return as the operation in RWB-P4-AD010-CON §12.1 |
| CDC-07651 | RWB-P4-AD010-CON | CG-ALL-4722 | 12.2 | Publish POST /api/recovery/access/v1/authorise as an rwb-access operation, consumed by RWB-P4-AD010-CON §12.2 |
| CDC-07662 | RWB-P4-AD011-APP | CG-ALL-4729 | 12.2 | Publish POST /api/recovery/access/v1/authorise through RWB-P4-AD011-CON. |
| CDC-07675 | RWB-P4-AD011-CON | CG-ALL-4736 | 12.1 | Publish POST /api/recovery/access/v1/admin/rule-version-loads as documented in section 12.1 |
| CDC-07676 | RWB-P4-AD011-CON | CG-ALL-4737 | 12.1 | Publish GET /api/recovery/access/v1/admin/rule-version-loads/{versionId} as documented in section 12.1 |
| CDC-07678 | RWB-P4-AD011-CON | CG-ALL-4739 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml |
| CDC-07688 | RWB-P4-AD012-APP | CG-ALL-4743 | 12.1 | Publish operation POST /admin/rule-version-approvals in rwb-access.yaml through the RWB-P4-AD012-CON story, or remove it from 12.1 |
| CDC-07689 | RWB-P4-AD012-APP | CG-ALL-4744 | 12.1 | Publish operation GET /admin/rule-version-approvals/{versionId} in rwb-access.yaml through the RWB-P4-AD012-CON story, or remove it from 12.1 |
| CDC-07690 | RWB-P4-AD012-APP | CG-ALL-4745 | 12.2 | Publish operation POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider CON story |
| CDC-07692 | RWB-P4-AD012-APP | DOR-RWB-P4-AD012-APP-8 | 12.1, 12.2, 12.3 | Publish POST and GET admin rule-version-approvals operations and POST /api/recovery/access/v1/authorise; event name corrected in story |
| CDC-07706 | RWB-P4-AD012-CON | CG-ALL-4753 | 12.1 | Publish POST /api/recovery/access/v1/admin/rule-version-approvals with the §12.1 shape, Idempotency-Key and the listed answers. |
| CDC-07707 | RWB-P4-AD012-CON | CG-ALL-4754 | 12.1 | Publish GET /api/recovery/access/v1/admin/rule-version-approvals/{versionId} answering RuleVersionApproval. |
| CDC-07708 | RWB-P4-AD012-CON | CG-ALL-4755 | 12.2 | Publish POST /api/recovery/access/v1/authorise under rwb-access (owner P4) in rwb-access.yaml. |
| CDC-07724 | RWB-P4-AD013-APP | CG-ALL-4763 | 12.1 | Publish POST /api/recovery/access/v1/admin/version-rollbacks through the provider's CON story RWB-P4-AD013-CON |
| CDC-07725 | RWB-P4-AD013-APP | CG-ALL-4764 | 12.1 | Publish GET /api/recovery/access/v1/admin/version-rollbacks/{rollbackId} through the provider's CON story RWB-P4-AD013-CON |
| CDC-07726 | RWB-P4-AD013-APP | CG-ALL-4765 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story RWB-P4-AD013-CON |
| CDC-07746 | RWB-P4-AD013-CON | CG-ALL-4773 | 12.1 | Publish POST /api/recovery/access/v1/admin/version-rollbacks with the VersionRollbackRequest body, the 201 VersionRollback answer and the Idempotency-Key header, or remove the operation. |
| CDC-07747 | RWB-P4-AD013-CON | CG-ALL-4774 | 12.1 | Publish GET /api/recovery/access/v1/admin/version-rollbacks/{rollbackId} answering VersionRollback, or remove the operation. |
| CDC-07748 | RWB-P4-AD013-CON | CG-ALL-4775 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml as the service's own guard, or consume a published operation instead. |
| CDC-07749 | RWB-P4-AD013-CON | DOR-RWB-P4-AD013-CON-8 | 12.1 | Publish the POST and GET admin/version-rollbacks paths and POST /api/recovery/access/v1/authorise; the Idempotency-Key header is already declared on the POST in §12.1. |
| CDC-07763 | RWB-P4-AD014-APP | CG-ALL-4784 | 12.1 | Publish POST /api/recovery/access/v1/admin/queue-file-checks in rwb-access.yaml through RWB-P4-AD014-CON. |
| CDC-07764 | RWB-P4-AD014-APP | CG-ALL-4785 | 12.1 | Publish GET /api/recovery/access/v1/admin/queue-file-checks/{checkId} in rwb-access.yaml through RWB-P4-AD014-CON. |
| CDC-07778 | RWB-P4-AD014-CON | CG-ALL-4789 | 12.1 | Publish POST /api/recovery/access/v1/admin/queue-file-checks (multipart file and validFrom, header Idempotency-Key, 200 QueueFileCheckAnswer; 401, 403, 409, 422, 503), or remove it from 12.1. |
| CDC-07779 | RWB-P4-AD014-CON | CG-ALL-4790 | 12.1 | Publish GET /api/recovery/access/v1/admin/queue-file-checks/{checkId} (200 QueueFileCheckAnswer; 401, 403, 404, 503), or remove it from 12.1. |
| CDC-07789 | RWB-P4-AD015-APP | CG-ALL-4797 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider CON story, or consume a published operation |
| CDC-07804 | RWB-P4-AD015-CON | CG-ALL-4808 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation instead. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07616 | RWB-P4-AD008-CON | CG-ALL-4692 | 16 | Add rows for TC-AD-008-CON-01 to TC-AD-008-CON-06 with Given, When and Then copied from AC1 to AC6 of section 7. |
| CDC-07627 | RWB-P4-AD009-APP | CG-ALL-4699 | 16 | Add rows TC-AD-009-05 and TC-AD-009-06 to tab Story test cases, with Given, When and Then from AC3, BR3, BR4, BR6 and from AC5, BR8. |
| CDC-07636 | RWB-P4-AD009-CON | CG-ALL-4708 | 16 | Add rows TC-AD-009-CON-01 to TC-AD-009-CON-06 under Story test cases, with Given, When and Then copied from AC1 to AC6 of section 7. |
| CDC-07644 | RWB-P4-AD010-APP | CG-ALL-4715 | 16 | Add rows TC-AD-010-05 and TC-AD-010-06 with Given, When and Then copied from the section 7 criteria AC4 and AC5 they cover. |
| CDC-07657 | RWB-P4-AD010-CON | CG-ALL-4724 | 16 | Add rows for TC-AD-010-CON-01 to TC-AD-010-CON-08 with Given, When and Then copied from AC1 to AC8 in section 7 of RWB-P4-AD010-CON. |
| CDC-07665 | RWB-P4-AD011-APP | CG-ALL-4730 | 16 | Add rows TC-AD-011-04 and TC-AD-011-05 with Given, When and Then copied from AC4 and AC5. |
| CDC-07685 | RWB-P4-AD011-CON | CG-ALL-4740 | 16 | Add rows TC-AD-011-CON-01 to TC-AD-011-CON-06 with Given, When and Then copied from AC1 to AC6 of section 7. |
| CDC-07694 | RWB-P4-AD012-APP | CG-ALL-4748 | 16 | Add rows TC-AD-012-05 and TC-AD-012-06 with Given, When and Then copied from the criteria they cover (AC4, BR6, BR7; AC3, AC7, BR5, BR10, BR11) |
| CDC-07695 | RWB-P4-AD012-APP | DOR-RWB-P4-AD012-APP-12 | 16, 18 | TC-AD-012-07 added in section 16 as a BR3/BR14 component test. |
| CDC-07719 | RWB-P4-AD012-CON | CG-ALL-4758 | 16 | Add rows TC-AD-012-CON-01 to TC-AD-012-CON-06 with Given, When and Then copied from the criteria they cover. |
| CDC-07733 | RWB-P4-AD013-APP | CG-ALL-4768 | 16 | Add rows TC-AD-013-04 to TC-AD-013-08 with Given, When and Then copied from the criteria they cover (AC2, AC3, AC4, AC6, AC5); add TC-AD-013-09 to TC-AD-013-12 from section 16. |
| CDC-07734 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-12 | 16, 18 | Add TC-AD-013-04 to TC-AD-013-08 to tab Story test cases. Requirements Traceability Matrix v7 rows REQ-CWC-013, REQ-DRI-010, REQ-ACA-013, R-UNI-38 and R-UNI-39 hold no TC-AD-013 IDs; add them to match section 18. |
| CDC-07759 | RWB-P4-AD013-CON | CG-ALL-4777 | 16 | Add rows TC-AD-013-CON-01 to TC-AD-013-CON-06 in the next version, with Given, When and Then copied from the criteria they cover. |
| CDC-07793 | RWB-P4-AD015-APP | CG-ALL-4800 | 16 | Add rows for TC-AD-015-05, TC-AD-015-06 and TC-AD-015-07 to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-07795 | RWB-P4-AD015-APP | DOR-RWB-P4-AD015-APP-12 | 12.7, 16, 18 | Add TC-AD-015-05, TC-AD-015-06 and TC-AD-015-07 (CG-ALL-4800). Align the section 18 test lists with Recovery Workbench Requirements Traceability Matrix v7.md. |
| CDC-07811 | RWB-P4-AD015-CON | CG-ALL-4811 | 16 | Add rows for TC-AD-015-CON-01 to TC-AD-015-CON-06 with Given, When and Then copied from AC1 to AC6 of section 7 of RWB-P4-AD015-CON. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07617 | RWB-P4-AD008-CON | CG-ALL-4693 | 18 | Align the trace of REQ-ACA-002 and REQ-ACA-011 to the section 18 test IDs TC-AD-008-CON-01, -02, -05 and -06, since this story is the source for its own test cases. |
| CDC-07629 | RWB-P4-AD009-APP | CG-ALL-4700 | 18 | Align the test lists for REQ-DRI-011 and the other differing requirement with RWB-P4-AD009-APP section 18 in the next RTM version. |
| CDC-07637 | RWB-P4-AD009-CON | CG-ALL-4709 | 18 | Align REQ-DRI-011 in RTM v7 with section 18 of this story: TC-AD-009-CON-02, -04, -05 and -07. |
| CDC-07647 | RWB-P4-AD010-APP | CG-ALL-4716 | 18 | Align the REQ-DRI-011 test list with section 18 of RWB-P4-AD010-APP in the next version. |
| CDC-07658 | RWB-P4-AD010-CON | CG-ALL-4725 | 18 | Align the REQ-DRI-011 test list and the second differing requirement to section 18 of RWB-P4-AD010-CON; add TC-AD-010-CON-07 under REQ-ACA-003. |
| CDC-07672 | RWB-P4-AD011-APP | CG-ALL-4731 | 18 | Align the test case list of each of the 3 differing requirements in RTM v7 with section 18 of RWB-P4-AD011-APP in its next version. |
| CDC-07686 | RWB-P4-AD011-CON | CG-ALL-4741 | 18 | Align the REQ-CWC-013 trace to TC-AD-011-CON-01, -02 and -04 as in section 18. The other RTM tests belong to other stories. |
| CDC-07702 | RWB-P4-AD012-APP | CG-ALL-4749 | 18 | Align the REQ-CWC-013 and REQ-DRI-010 test lists with section 18 of RWB-P4-AD012-APP in the next RTM version. |
| CDC-07720 | RWB-P4-AD012-CON | CG-ALL-4759 | 18 | Align the REQ-CWC-013 test list and the second differing requirement with section 18 in the next RTM version. |
| CDC-07741 | RWB-P4-AD013-APP | CG-ALL-4769 | 18 | Align the test lists for REQ-CWC-013 and REQ-DRI-010 with RWB-P4-AD013-APP section 18 in the next RTM version |
| CDC-07760 | RWB-P4-AD013-CON | CG-ALL-4778 | 18 | Align the test lists of REQ-CWC-013 and the other differing requirement with section 18 of RWB-P4-AD013-CON in the next RTM version. |
| CDC-07800 | RWB-P4-AD015-APP | CG-ALL-4801 | 18 | Align the test lists of REQ-CWC-011, REQ-DRI-005 and the other differing requirement with section 18 of RWB-P4-AD015-APP |
| CDC-07812 | RWB-P4-AD015-CON | CG-ALL-4812 | 18 | Align the traced test cases of the four differing requirements (including REQ-CWC-011 and REQ-DRI-005) with section 18 of RWB-P4-AD015-CON. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07693 | RWB-P4-AD012-APP | CG-ALL-4747 | 4 | Add a new message ID for 'An item of the seven-item change checklist is missing or empty'; the story then cites that ID in section 14 in place of MSG-P3-022 |
| CDC-07697 | RWB-P4-AD012-APP | DOR-RWB-P4-AD012-APP-9 | 14 | Add a new message ID for 'An item of the seven-item change checklist is missing or empty'; the story then cites it in section 14 |
| CDC-07710 | RWB-P4-AD012-CON | CG-ALL-4757 | 4, 14 | Add a new message ID for 'An item of the seven-item checklist is missing'; the story then cites it. |
| CDC-07732 | RWB-P4-AD013-APP | CG-ALL-4767 | 4, 14 | Add a new message ID for 'The caller is the loader of the version in force', separate from MSG-P7-002; the story cites it in sections 4 and 14 once it exists. |
| CDC-07736 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-9 | 14 | Add a new message ID for 'The caller is the loader of the version in force' (see CG-ALL-4767); section 14 then cites it. |
| CDC-07750 | RWB-P4-AD013-CON | CG-ALL-4776 | 4, 14 | Add a new message ID for 'The caller is the loader of the version in force'; MSG-P7-002 keeps the standard's meaning. The story cites the new ID after it exists. |
| CDC-07752 | RWB-P4-AD013-CON | DOR-RWB-P4-AD013-CON-9 | 14 | Confirm the standard's meaning of MSG-P7-002; if it differs from the separation-of-duty use, the standard owner issues a separate message ID. |
| CDC-07792 | RWB-P4-AD015-APP | CG-ALL-4799 | 4, 14 | Add a new message ID for 'The approver is the author of the load' with its wording. The story then cites that ID in place of MSG-P7-002 in sections 4, 8 (BR6), 14 and 16 (TC-AD-015-03). |
| CDC-07797 | RWB-P4-AD015-APP | DOR-RWB-P4-AD015-APP-9 | 14 | Add the new ID for the author-approver refusal (see CG-ALL-4799); the §14 row then cites it. |
| CDC-07807 | RWB-P4-AD015-CON | CG-ALL-4810 | 4, 14 | Add a new message ID for the approver-is-author condition; MSG-P7-002 keeps its meaning of approver prepared the decision. |
| CDC-07809 | RWB-P4-AD015-CON | DOR-RWB-P4-AD015-CON-9 | 14 | Confirm MSG-P7-002 for a four-eyes refusal or assign a new ID; sections 5, 7 and 14 use it for that case |

### API:(service not named) (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07668 | RWB-P4-AD011-APP | GAP-2273 | none | Add POST and GET /api/recovery/access/v1/admin/queue-file-checks as rwb-access operations, Reference data C and R; keep queue, member and reference-load rows with rwb-case. |
| CDC-07713 | RWB-P4-AD012-CON | GAP-2273 | find it | Keep queue, member and reference-load rows with rwb-case; place the queue-file gate in rwb-access as POST and GET /api/recovery/access/v1/admin/queue-file-checks; name finding codes in the contract only. |
| CDC-07714 | RWB-P4-AD012-CON | GAP-1615 | find it | Re-issue TSD P7 with the four rule tables and their operations; remove them from TSD P3 and TSD P4; set x-module P7 on the nine rule paths. |
| CDC-07715 | RWB-P4-AD012-CON | GAP-1565 | find it | Re-issue TSD P4 without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 to rwb-decision; set x-module P7 on the six paths. |
| CDC-07756 | RWB-P4-AD013-CON | GAP-0845 | AC1, 12.2 | Add POST /api/recovery/access/v1/admin/version-rollbacks and GET /api/recovery/access/v1/admin/version-rollbacks/{rollbackId}; confirm both with console and owners at contract review. |
| CDC-07757 | RWB-P4-AD013-CON | GAP-0852 | 18 | Record POST /admin/version-rollbacks and GET /admin/version-rollbacks/{rollbackId} of rwb-access as new operations in the API Specification index at the next version. |
| CDC-07782 | RWB-P4-AD014-CON | GAP-0856 | 12.2 | Add POST /api/recovery/access/v1/admin/queue-loads (multipart load and JSON approval shapes) and GET /api/recovery/access/v1/admin/queue-loads/{loadId} at D1. |
| CDC-07783 | RWB-P4-AD014-CON | GAP-0863 | find it | Correct API-P4-006 authorization: replace 'Reference data A is held by no role' with the A letter in Rules and parameters for RW-RISK, keeping the four-eyes check on the caller. |
| CDC-07810 | RWB-P4-AD015-CON | GAP-2277 | 9 | Declare the access-side load paths and the ServiceLevelLoad, ServiceLevelRow and RunningTimerEffect schemas, or name this document as their source |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07628 | RWB-P4-AD009-APP | DOR-RWB-P4-AD009-APP-7 | 11 | Confirm field IDs DF-REF-034 to DF-REF-039 (role id, role_code, role_name, role_class, default_scope, entra_group); DF-REF-039 is absent from LDM v9 and must be added or confirmed. |
| CDC-07645 | RWB-P4-AD010-APP | DOR-RWB-P4-AD010-APP-7 | 11 | Add or confirm DF-REF-039, the sixth field of role in rwb_access (entra_group), so the BR Field ID resolves; the section 11 range is unchanged. |
| CDC-07667 | RWB-P4-AD011-APP | DOR-RWB-P4-AD011-APP-7 | 11 | Register DF-REF-039 in LDM v9 so the section 11 range DF-REF-034 to DF-REF-039 resolves. |
| CDC-07696 | RWB-P4-AD012-APP | DOR-RWB-P4-AD012-APP-7 | 11 | Confirm DF-REF-039 as a field ID of the role table, or correct the DF-REF-034 to DF-REF-039 range in section 11 |
| CDC-07735 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-7 | 11 | Confirm LDM v9 holds DF-REF-039 for the role table; if it does not, the BR Field ID in section 11 must be corrected to an LDM v9 ID. |
| CDC-07796 | RWB-P4-AD015-APP | DOR-RWB-P4-AD015-APP-7 | 11 | Add or confirm DF-REF-039 for role, or correct the §11 range DF-REF-034 to DF-REF-039 to the IDs LDM v9 holds. |

### RWB-P4-AD014-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07765 | RWB-P4-AD014-APP | DOR-RWB-P4-AD014-APP-21 | header | Move the contract story build status from Not started to Done once the contract is published. |
| CDC-07769 | RWB-P4-AD014-APP | GAP-2273 | find it | Keep queue rows, member rows and reference load with rwb-case (RWB-P3-E1019-APP, -CON, -DB). Place the queue-file check gate in rwb-access as POST and GET /api/recovery/access/v1/admin/queue-file-checks, with Reference data C for the check and R for the read. Read DF-WRK-007 and DF-WRK-008 as capacity_cap and overflow_queue_code; name the seven finding codes in the contract document only. |
| CDC-07771 | RWB-P4-AD014-APP | GAP-0856 | find it | Declare POST /api/recovery/access/v1/admin/queue-loads with its multipart load and JSON approval request shapes, and GET /api/recovery/access/v1/admin/queue-loads/{loadId}. Keep the owner's reference-load family consumed. Add both operations to the P4 API file at D1. |
| CDC-07772 | RWB-P4-AD014-APP | GAP-0858 | find it | Declare the queue file as one row per queue with queue_code, queue_name, team_code, role_code, assignment_method, caseload_cap, overflow_queue_code and valid_from. Fix sheet name and header order with the reference data administrator and rwb-case owner before the parser is frozen. Route member rows through the rwb-case reference load as its own table code. |
| CDC-07774 | RWB-P4-AD014-APP | GAP-0864 | find it | Declare QueueFileRow with the eight columns, QueueLoad with its five answer fields and QueueValidationError with row, field and detail. Freeze the sheet name and header order with the P3 owner and the reference data administrator at contract review. |
| CDC-07775 | RWB-P4-AD014-APP | GAP-2274 | find it | Publish the four schemas, the seven Error finding codes and the 200, 400, 401, 403, 404, 409, 422 and 503 answers in one OpenAPI 3.1 document on base /api/recovery/access/v1. Declare Reference data C and R on the two operations. Declare the Idempotency-Key header with a 200 replay and a 409 on a different file. Keep v1 additive. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07786 | RWB-P4-AD015-APP | CG-ALL-4794 | 12.2 | Publish POST /api/recovery/case/v1/admin/service-levels in rwb-case.yaml through the provider CON story, or consume a published operation |
| CDC-07787 | RWB-P4-AD015-APP | CG-ALL-4795 | 12.2 | Publish POST /api/recovery/case/v1/admin/service-levels/{loadId}/approve in rwb-case.yaml through the provider CON story, or consume a published operation |
| CDC-07788 | RWB-P4-AD015-APP | CG-ALL-4796 | 12.2 | Publish GET /api/recovery/case/v1/admin/service-levels/{loadId} in rwb-case.yaml through the provider CON story, or consume a published operation |
| CDC-07801 | RWB-P4-AD015-CON | CG-ALL-4805 | 12.2 | Publish POST /api/recovery/case/v1/admin/service-levels in rwb-case.yaml, or the provider's CON story consumes a published operation instead. |
| CDC-07802 | RWB-P4-AD015-CON | CG-ALL-4806 | 12.2 | Publish POST /api/recovery/case/v1/admin/service-levels/{loadId}/approve in rwb-case.yaml, or consume a published operation instead. |
| CDC-07803 | RWB-P4-AD015-CON | CG-ALL-4807 | 12.2 | Publish GET /api/recovery/case/v1/admin/service-levels/{loadId} in rwb-case.yaml, or consume a published operation instead. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07623 | RWB-P4-AD009-APP | DOR-RWB-P4-AD009-APP-14 | Not specified in the source documents (DOR-RWB-P4-AD009-APP-14) | Confirm the signed epic design sign-off for EP08 from the epic design record; this story does not record it. |
| CDC-07652 | RWB-P4-AD010-CON | DOR-RWB-P4-AD010-CON-14 |  | Record the signed epic design sign-off for RWB-P4-AD010-CON |
| CDC-07679 | RWB-P4-AD011-CON | DOR-RWB-P4-AD011-CON-14 | header | Record the signed epic design sign-off for EP08 and RWB-SVC-P4 in the epic design record |
| CDC-07709 | RWB-P4-AD012-CON | DOR-RWB-P4-AD012-CON-14 | header | Confirm and record the signed epic design sign-off for EP08. |
| CDC-07727 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-14 | n/a | Record the signed epic design sign-off for EP08 in the epic design record |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07606 | RWB-P4-AD008-CON | CG-ALL-4683 | 11, 12.7 | Record access_review as a new P4 (rwb_access) entity created by RWB-P4-AD008-APP in LDM v9 and Data Classification v5. |
| CDC-07607 | RWB-P4-AD008-CON | CG-ALL-4684 | 11; 12.7 | Record access_review and access_review_item as P4 tables owned by rwb_access, created by RWB-P4-AD008-APP, or name the dictionary entries |
| CDC-07767 | RWB-P4-AD014-APP | CG-ALL-4783 | find it | Record overflow_queue_code as a field: the queue_code of the overflow queue, sourced from DF-WRK-008 in rwb-case. |
| CDC-07768 | RWB-P4-AD014-APP | DOR-RWB-P4-AD014-APP-7 | 11 | Add `overflow_queue_code` as a field or entity. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07610 | RWB-P4-AD008-CON | DOR-RWB-P4-AD008-CON-1 | 1 | Add the role 'tech lead' as a role code or role name, or the story §1 role is changed to a listed role |
| CDC-07653 | RWB-P4-AD010-CON | DOR-RWB-P4-AD010-CON-1 | 1 | Add a role row for the contract author role named 'tech lead' (role code, name, class, group, unit, default scope, first release): Not specified in the source documents (DOR-RWB-P4-AD010-CON-1) |
| CDC-07794 | RWB-P4-AD015-APP | DOR-RWB-P4-AD015-APP-1 | 1 | Add or confirm a role code and name for the reference data administrator; the story §1 then cites it. |
| CDC-07808 | RWB-P4-AD015-CON | DOR-RWB-P4-AD015-CON-1 | 1 | Name a role code or role name for the contract-slice actor; section 1 now carries a placeholder in place of tech lead |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07604 | RWB-P4-AD008-CON | CG-ALL-4689 | 12.5 | Add a Workflows row for AccessReviewWorkflow (task queue rwb-access), or name the catalogued workflow that replaces it; no catalogued access-review workflow exists. |
| CDC-07608 | RWB-P4-AD008-CON | CG-ALL-4690 | 12.5 | Add activity BuildReviewList to the Activities sheet with its workflow kit type and task queue rwb-access |
| CDC-07609 | RWB-P4-AD008-CON | CG-ALL-4691 | 12.5 | Add activity RequestRemoval to the Activities sheet with its workflow kit type and task queue rwb-access |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07611 | RWB-P4-AD008-CON | DOR-RWB-P4-AD008-CON-12 | 12.7, 16, 18 | Added TC-07 and TC-08 for §12.7 tables and events, and TC-09 for AC8; §16 now has nine cases |
| CDC-07681 | RWB-P4-AD011-CON | DOR-RWB-P4-AD011-CON-12 | 12.7, 16, 18 | Add TC-AD-011-CON-01 to -06 to Test Cases v8 and align the P3 section 18 test lists with RTM v7 |
| CDC-07751 | RWB-P4-AD013-CON | DOR-RWB-P4-AD013-CON-12 | 16, 18 | Add rows TC-AD-013-CON-01 to -07 under tab Story test cases; align the P3 section 18 test lists to RTM v7. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07701 | RWB-P4-AD012-APP | GAP-0828 | 12.1 | Add the seven checklist item codes (request, impact, test result, approver, load, verify, rollback plan) with labels and required flags to the rwb-case parameter catalogue. |
| CDC-07717 | RWB-P4-AD012-CON | GAP-0828 | 16 | Add the seven checklist item codes with labels and required flags under rwb-case as versioned reference data; the jsonb shape is per GAP-0828 proposed fix. |
| CDC-07744 | RWB-P4-AD013-APP | GAP-0851 | 2, 8 | Length bounds are marked as Not specified placeholders in BR13 and section 2. |

### RWB-P4-AD013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07728 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-21 | n/a | Set the build status to Done and publish the contract |
| CDC-07729 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-22 | n/a | Publish the contract fake library version and record that version against this story |
| CDC-07745 | RWB-P4-AD013-APP | GAP-0854 | find it | No change to row status. |

### RWB-P4-AD009-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07624 | RWB-P4-AD009-APP | DOR-RWB-P4-AD009-APP-21 | — | Set build status to Done once the contract is published. |
| CDC-07625 | RWB-P4-AD009-APP | DOR-RWB-P4-AD009-APP-22 | — | Publish a contract fake library version for RWB-P4-AD009-CON and record it as published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07661 | RWB-P4-AD011-APP | CG-ALL-4728 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions/{versionId} through the provider's P7 rule-package contract story. |
| CDC-07677 | RWB-P4-AD011-CON | CG-ALL-4738 | 12.2 | Publish GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions/{versionId} in rwb-decision.yaml |

### RWB-P4-AD011-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07663 | RWB-P4-AD011-APP | DOR-RWB-P4-AD011-APP-21 | header | Publish the contract and set its build status to Done. |
| CDC-07673 | RWB-P4-AD011-APP | GAP-0823 | 7 | Declare the Drools XLS workbook format: sheet name and header order fixed with the P7 registry owner and the centre of excellence; test_case_id on every row. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07666 | RWB-P4-AD011-APP | DOR-RWB-P4-AD011-APP-12 | 12.7, 16, 18 | Add rows TC-AD-011-04, TC-AD-011-05 and TC-AD-011-06 to tab Story test cases; align RTM v7 test lists with section 18. |
| CDC-07711 | RWB-P4-AD012-CON | DOR-RWB-P4-AD012-CON-12 | 12.7, 16, 18 | Register TC-AD-012-CON-01 to TC-AD-012-CON-08 in Test Cases v8 and align the test lists of section 18 with RTM v7. |

### RWB-P4-AD012-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07671 | RWB-P4-AD011-APP | GAP-0826 | metadata | Add RWB-P7-AD011-CON (or the id the P7 split allocates) to its contract dependencies at D1. |
| CDC-07716 | RWB-P4-AD012-CON | GAP-0826 | find it | Add the P7 rule-package contract (approve and version list) to its contract dependencies at D1 and build the gate against the fake until published. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07730 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-5 | 9 | Add REFERENCE to the closed list LOV-ROUTE, or remove REFERENCE from §9 and §12.1 |
| CDC-07766 | RWB-P4-AD014-APP | DOR-RWB-P4-AD014-APP-5 | 9 | ASSIGNMENT_METHOD_UNKNOWN must not be added to LOV-ASSIGN by this story; the LOV owner adds it only if it is a real closed-list value the allocation engine emits. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07740 | RWB-P4-AD013-APP | GAP-2280 | 2 | Record that FEAT-ADM-06 is carried twice: by RWB-P4-E8011 for tables rwb-access owns and by RWB-P4-AD013 for rule and reference versions; freeze config-rollback paths and four target kinds at contract review. |
| CDC-07758 | RWB-P4-AD013-CON | GAP-2280 | 1 | Record that FEAT-ADM-06 is carried twice: by RWB-P4-E8011 for tables rwb-access owns and by RWB-P4-AD013 for rule and reference versions of rwb-decision and rwb-case; freeze config-rollback paths and four target kinds at contract review. |

### RWB-P4-AD015-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07790 | RWB-P4-AD015-APP | DOR-RWB-P4-AD015-APP-21 | header | Build status Done (currently Not started) |
| CDC-07799 | RWB-P4-AD015-APP | GAP-2277 | 7 | Declare ServiceLevelLoad, ServiceLevelRow and RunningTimerEffect, the load state set and the 422 and 409 bodies, agreed at the wave 4 review, then freeze as the fake pack in section 12.8 |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20772 | RWB-P4-AD010-CON | R-28966 |  | MSG-P7-002 entry belongs to the P4 message catalogue, not this FSD. Story RWB-P4-AD010-APP already uses the id. |
| CDC-20773 | RWB-P4-AD010-CON | R-28966 |  | Reference-data four-eyes catalogue entry belongs to the P4 message catalogue (rwb-access), not this FSD. Story AD010-CON cites MSG-P7-002 in AC3. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07612 | RWB-P4-AD008-CON | GAP-0806 | find it | Add access_review (reviewId, cycle code, opened_on, closes_on, state) and access_review_item (review, role code, holder reference, decision state, decision, reason, decided_at, decided_by reference, removal request reference); allocate field IDs at next dictionary version; carry into the RWB-P4-AD008-APP migration. |

### OTHER:Integration catalogue (ACE Common group membership removal; OTHER:INT-21) and P4 contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07613 | RWB-P4-AD008-CON | GAP-0808 | find it | Specify the removal request (group, role code, holder reference, review, reason), the answer (request reference, accepted or refused), the INT-21 reference and the failure contract that leaves the item open with a task and an incident. |

### OTHER:Access model and PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07614 | RWB-P4-AD008-CON | GAP-0809 | find it | Record that the owner of a role is the holder of the A letter in Platform administration for that role (RW-SECADM and RW-PLATADM per TSD P4 T6.1), with RW-COE for the reference-data roles; a caller with R only owns no role and is refused. |

### OTHER:Operations story of legacy RWB-AD-008 (JOB-18 Schedule) and DL38 deployment configuration (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07615 | RWB-P4-AD008-CON | GAP-0807 | header | Create the access-review Schedule with the cron as deployment configuration under the DL38 six-month placeholder until the bank IAM standard value is supplied. |

### OTHER:Access model; OTHER:PRD and screen text (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07618 | RWB-P4-AD008-CON | GAP-0810 | find it | State that a review item with no decision at the close is not confirmed and triggers the removal request, and that the removal is requested within the DL38 leaver interval of the same working day. |

### OTHER:Versioned interface configuration and file layout for the access review file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07619 | RWB-P4-AD008-CON | GAP-1572 | find it | Register one interface row for the access review file (direction, pattern, data product, owner role, alert role), publish the file layout and review-date convention, and agree with the rwb-integration contract owner how a file-level delivery with no case is matched. |

### OTHER:Technical Specification P4 v3 T3.1; OTHER:rwb-access contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07630 | RWB-P4-AD009-APP | GAP-1567 | 8 | Drop lov_value and partner_user from TSD P4 T3.1; keep the lists of values in TSD P3 and the partner identity in TSD S9; the rwb-access contract states which list-of-values versions and partner identity attributes it reads and how often it refreshes them. |

### OTHER:rwb-case contract (reference-load path and table or lovCode name) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07635 | RWB-P4-AD009-CON | GAP-0811 | 11 | Console path /api/recovery/access/v1/admin/lov-loads stated in section 11 |

### OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07638 | RWB-P4-AD009-CON | GAP-1567 | 11 | Drop lov_value and partner_user from T3.1; keep lists of values in TSD P3 and partner identity in TSD S9. |

### RWB-P4-AD010-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07642 | RWB-P4-AD010-APP | DOR-RWB-P4-AD010-APP-21 | header | Build status must move from Not started to Done before this story can be ready |

### RWB-P4-E1038-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07646 | RWB-P4-AD010-APP | GAP-0789 | 11 | Add the valid-from, valid-to and approver-reference columns to permission; define the matrix load, reads and versions list under /api/recovery/access/v1/admin/permission-matrix, ending at VALIDATED. |

### OTHER:P4 message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07648 | RWB-P4-AD010-APP | GAP-0820 | 14 | Add MSG-P7-002 word for word, as the legacy criterion writes it, so the separation-of-duty refusal keeps one message id. |

### OTHER:RWB-P3 reference-data contract (rwb-case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07654 | RWB-P4-AD010-CON | GAP-1564 | 11 | Confirm load, approve, verify and rollback stay with rwb-case and rwb-access publishes the authorise, masking and DoA lookups; otherwise restore API-P4-005, 006, 009, 010 to P4 and record the Ownership Map ruling. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07655 | RWB-P4-AD010-CON | GAP-0816 | 3, 12.1, 12.2 | Reconcile POST /admin/reference-loads/{loadId}/approve (P3, ASM-A6-api-4) with the P4 gate path /admin/lov-loads before the contract is frozen. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07656 | RWB-P4-AD010-CON | GAP-0817 | 8, 18 | Correct the Reference data row: list owner holds A through RW-REFADM and RW-COE per TSD P4 v3 T6.1; a service identity may author a load but not approve it. |

### OTHER:Recovery Workbench P4 message catalogue (rwb-access) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07659 | RWB-P4-AD010-CON | GAP-0820 | 7 | Add MSG-P7-002 unchanged, text 'You prepared this decision, so you cannot approve it.', as the P4 entry for the reference-data four-eyes refusal; do not renumber |

### OTHER:DP-03 decision-code list (decision-record library) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07660 | RWB-P4-AD010-CON | GAP-0830 | 7 | Add the decision code for a rule-version approval or refusal (LOADED to APPROVED or refused, outcome REQUESTED) with entry fields package, version label, valid-from date and approver reference |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07664 | RWB-P4-AD011-APP | DOR-RWB-P4-AD011-APP-8 | 12.2 | Publish the two operations named in CG-ALL-4728 and CG-ALL-4729. |

### OTHER:Technical Specification P7; OTHER:TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07669 | RWB-P4-AD011-APP | GAP-1615 | 8, 12.7 | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule operations; remove them from TSD P3 and P4; set x-module of the nine rule paths to P7. |

### OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07670 | RWB-P4-AD011-APP | GAP-1565 | 18 | Re-issue TSD P4 without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 to rwb-decision documents; set x-module of six paths to P7. |

### OTHER:Work Package plan for B-P4-04 and B2-P4-006 (split_plan.json generator and checks/run_all.py) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07674 | RWB-P4-AD011-APP | GAP-2271 |  | Keep one Work Package per slice: remove RWB-AD-012 from B-P4-04 fanout or retire B2-P4-006; number CG and ASM IDs once at D1; add plan-uniqueness check that fails on duplicate Write-only output paths. |

### OTHER:P3 screen record for SCR-39 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07680 | RWB-P4-AD011-CON | DOR-RWB-P4-AD011-CON-10 | find it | Define empty, loading, error and no-access states for SCR-39 in the P3 screen record |

### OTHER:Technical Specification P4 v3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07682 | RWB-P4-AD011-CON | GAP-2273 | none | Keep queue, member and reference-load rows with rwb-case; place the gate in rwb-access as POST and GET /api/recovery/access/v1/admin/queue-file-checks; name the seven finding codes in the contract document only. |

### OTHER:Technical Specification P7; OTHER:Technical Specifications P3 and P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07683 | RWB-P4-AD011-CON | GAP-1615 | none | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule-version and rule-package operations; remove them from TSD P3 and P4; set the nine rule paths to x-module P7. |

### OTHER:Technical Specification P4 v3; API:(service not named); OTHER:rwb-decision documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07684 | RWB-P4-AD011-CON | GAP-1565 | none | Re-issue TSD P4 without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 with its criteria to rwb-decision documents; set the six paths to x-module P7. |

### OTHER:Technical specification P4 (T-A.2; OTHER:T3.1) and rwb-access contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07687 | RWB-P4-AD011-CON | GAP-0823 | 7 | Declare the Drools XLS sheet name and header order, with the rule_row columns and test_case_id, agreed with the P7 registry owner and the centre of excellence. |

### RWB-P4-AD012-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07691 | RWB-P4-AD012-APP | DOR-RWB-P4-AD012-APP-21 | header | Set build status to Done once the contract is published; it is currently Not started |

### RWB-P3-E1019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07698 | RWB-P4-AD012-APP | GAP-2273 |  | Keep queue rows, member rows and reference load with rwb-case (RWB-P3-E1019-APP, -CON, -DB). Place POST and GET /api/recovery/access/v1/admin/queue-file-checks in rwb-access as Reference data C (check) and R (read). |

### OTHER:TSD P7 (rwb-decision); OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07699 | RWB-P4-AD012-APP | GAP-1615 | 12.1 | Re-issue TSD P7 with T3.1 entries for rule_package, rule_package_version, rule_row and rule_test_case and appendix T-A rule-version and rule-package operations; remove them from TSD P3 and TSD P4; set x-module P7 on the nine rule paths in the API Specification. |

### OTHER:TSD P4; API:(service not named); OTHER:rwb-decision documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07700 | RWB-P4-AD012-APP | GAP-1565 | 12.1 | Re-issue TSD P4 without the four rule tables, RulePackageStore and the six rule-package operations; move FEAT-ADM-02 to rwb-decision documents; keep RULES_AND_PARAMETERS rights in P4; set x-module P7 on the six paths. |

### OTHER:Work Packages B-P4-04 and B2-P4-006 and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07703 | RWB-P4-AD012-APP | GAP-2271 | find it | Remove RWB-AD-012 from the B-P4-04 fanout or retire B2-P4-006 for this key; number CG-B-P4-04-AD012-101 to -107 and ASM-B-P4-04-AD012-101 to -107 once; add a plan-uniqueness check. |

### OTHER:Work Packages B-P4-04 and B2-P4-007 and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07704 | RWB-P4-AD012-APP | GAP-2272 | find it | Remove RWB-AD-013 from the B-P4-04 fanout or retire B2-P4-007 for this key; number CG-B-P4-04-AD013-101 to -112 and ASM-B-P4-04-AD013-101 to -112 once; add a plan-uniqueness check. |

### OTHER:Work Packages B-P4-04 and B2-P4-010 and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07705 | RWB-P4-AD012-APP | GAP-2278 | find it | Remove RWB-AD-016 from the B-P4-04 fanout or retire B2-P4-010 for this key; number CG-B-P4-04-AD016-101 to -111 and ASM-B-P4-04-AD016-101 to -111 once; add a plan-uniqueness check. |

### OTHER:Message catalogue (P2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07712 | RWB-P4-AD012-CON | DOR-RWB-P4-AD012-CON-9 | 14 | Confirm the meaning of MSG-P3-022 against the standard, or assign the seven-item checklist message its own id. |

### API:(service not named); OTHER:v4.yaml is the highest file present and is not edited) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07718 | RWB-P4-AD012-CON | GAP-0831 | find it | Declare RuleVersionApproval with versionId, packageCode, versionLabel, validFrom, checklistState, decisionRecordReference, decisionRecordState, state, approverReference, approvedAt and the effective-dating statement; ChecklistItem per item code; DecisionRecordRef with entry id, chain sequence and outcome |

### OTHER:Work Package plan generator (B-P4-04; OTHER:B2-P4-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07721 | RWB-P4-AD012-CON | GAP-2271 | Header | Keep one Work Package per AD-012 slice: remove RWB-AD-012 from the B-P4-04 fanout or retire B2-P4-006; allocate one citation set; add a plan-uniqueness check to checks/run_all.py. |

### OTHER:Work Package plan: B-P4-04 and B2-P4-007 (split_plan.json) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07722 | RWB-P4-AD012-CON | GAP-2272 | n/a | Remove RWB-AD-013 from the B-P4-04 fanout or retire B2-P4-007 for this key. Number CG-B-P4-04-AD013-101 to -112 and ASM-B-P4-04-AD013-101 to -112 once, and add a plan-uniqueness check to checks/run_all.py. |

### OTHER:Work Package plan: B-P4-04 and B2-P4-010 (split_plan.json) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07723 | RWB-P4-AD012-CON | GAP-2278 | n/a | Remove RWB-AD-016 from the B-P4-04 fanout or retire B2-P4-010 for this key. Number CG-B-P4-04-AD016-101 to -111 and ASM-B-P4-04-AD016-101 to -111 once, and add a plan-uniqueness check to checks/run_all.py. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07731 | RWB-P4-AD013-APP | DOR-RWB-P4-AD013-APP-8 | 1, 11 | Publish POST /api/recovery/access/v1/admin/version-rollbacks, GET /api/recovery/access/v1/admin/version-rollbacks/{rollbackId} and POST /api/recovery/access/v1/authorise; align the DecisionRecorded event type to rwb.decision.DecisionRecorded.v1. |

### OTHER:TSD P7 rwb-decision; OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07737 | RWB-P4-AD013-APP | GAP-1615 | 1 | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule operations; remove them from TSD P3 and TSD P4; set x-module P7 on the nine rule paths. |

### OTHER:TSD P4 v3; OTHER:FEAT-ADM-02 in the P4 feature set; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07738 | RWB-P4-AD013-APP | GAP-1565 | 1 | Re-issue TSD P4 without the four rule tables, RulePackageStore and the six rule-package operations; move FEAT-ADM-02 with its criteria to rwb-decision documents; set x-module P7 on the six paths. |

### API:(service not named); OTHER:TSD P4 v3 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07739 | RWB-P4-AD013-APP | GAP-0852 | 12.1 | Record POST /admin/version-rollbacks and GET /admin/version-rollbacks/{rollbackId} under /api/recovery/access/v1 as new operations at the next index version. |

### OTHER:split_plan.json and the plan generator (Work Packages B-P4-04 and B2-P4-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07742 | RWB-P4-AD013-APP | GAP-2271 | find it | Keep one Work Package per RWB-AD-012 story slice: remove RWB-AD-012 from the B-P4-04 fanout or retire B2-P4-006; number CG and ASM IDs once; add a plan-uniqueness check to checks/run_all.py |

### OTHER:split_plan.json and the plan generator (Work Packages B-P4-04 and B2-P4-007) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07743 | RWB-P4-AD013-APP | GAP-2272 | find it | Keep one Work Package per RWB-AD-013 story slice: remove RWB-AD-013 from the B-P4-04 fanout or retire B2-P4-007; number CG and ASM IDs once; add a plan-uniqueness check to checks/run_all.py |

### OTHER:Technical Specification P7; OTHER:Technical Specification P3 and P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07753 | RWB-P4-AD013-CON | GAP-1615 | 12.7 | Re-issue TSD P7 with the four rule tables and rule-version and package operations; remove them from TSD P3 and P4; set x-module of the nine rule paths to P7. |

### OTHER:Technical Specification P4; API:(service not named); OTHER:rwb-decision feature documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07754 | RWB-P4-AD013-CON | GAP-1565 |  | Re-issue TSD P4 without the four rule tables, RulePackageStore and six rule-package operations; move FEAT-ADM-02 to rwb-decision; set x-module of the six paths to P7. |

### RWB-P4-AD013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07755 | RWB-P4-AD013-CON | GAP-0844 | AC4 | Add a C dependency on the P7 rule-package rollback contract at D1; the P3 reference-load dependency is already listed. |

### OTHER:Work Package plan (B-P4-04; OTHER:B2-P4-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07761 | RWB-P4-AD013-CON | GAP-2271 |  | Keep one Work Package per story slice: remove RWB-AD-012 from the B-P4-04 fanout or retire B2-P4-006 for this key; add a plan-uniqueness check to checks/run_all.py. |

### OTHER:Work Package B-P4-04 and split_plan.json (plan generator, checks/run_all.py) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07762 | RWB-P4-AD013-CON | GAP-2272 |  | Remove RWB-AD-013 from the B-P4-04 fanout or retire B2-P4-007 for this key; number CG-B-P4-04-AD013-101 to -112 and ASM-B-P4-04-AD013-101 to -112 once; add a plan-uniqueness check. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON; RWB-P3-E1019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07770 | RWB-P4-AD014-APP | GAP-0438 | find it | Publish the queue file layout with required columns and cap value or range; the valid-from parameter name and type; one named approval route for a queue load and which operation writes the decision record; the overflow-refusal message ID and text; and response schemas for the seven P3 and P7 operations. |

### API:(service not named); OTHER:API-P4-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07773 | RWB-P4-AD014-APP | GAP-0863 | find it | Check the A letter in Rules and parameters for the approval, as the legacy story and TSD T6.1 state, and keep the four-eyes comparison (409 MSG-P7-002). Correct the Reference data A wording of API-P4-006 when the P4 API file is next published. |

### OTHER:TSD P4 T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07776 | RWB-P4-AD014-APP | GAP-0860 | 12.2 | Add LOV-ASSIGN to the P4 list section at D1 with values ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL as in TSD P3 T3.2 |

### OTHER:Decision-record library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07777 | RWB-P4-AD014-APP | GAP-0861 | 12.2 | Declare the load entry decision code as the owner's approve entry code until P3 and P7 owners name one |

### OTHER:the app story of this key (owner of SCR-42 and SCR-43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07780 | RWB-P4-AD014-CON | DOR-RWB-P4-AD014-CON-10 | none | Add empty, loading, error and no-access states to SCR-42 and SCR-43. |

### OTHER:P3 and P7 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07781 | RWB-P4-AD014-CON | GAP-0438 | 11, 12.2, 14 | Publish the queue file layout with required columns and cap value or range; the valid-from parameter name and type; one named approval route for a queue load with the order of the two approve calls and which one writes the decision record; the overflow-refusal message ID and text; and the response schemas of the P3 and P7 operations. |

### OTHER:OpenAPI 3.1 contract document for rwb-access v1 (base /api/recovery/access/v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07784 | RWB-P4-AD014-CON | GAP-2274 | find it | Publish the four schemas, the seven finding codes, the 200, 400, 401, 403, 404, 409, 422 and 503 answers, Reference data C and R on the two operations, and the Idempotency-Key header with a 200 replay and a 409 on a different file; keep additive within v1. |

### OTHER:TSD P4 v3, section T3.2 list section (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07785 | RWB-P4-AD014-CON | GAP-0860 | find it | Add LOV-ASSIGN to the P4 list section so it matches TSD P3 T3.2 (ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL). |

### OTHER:rwb-case API yaml; OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07791 | RWB-P4-AD015-APP | DOR-RWB-P4-AD015-APP-8 | 4 | Publish POST /api/recovery/case/v1/admin/service-levels, POST /api/recovery/case/v1/admin/service-levels/{loadId}/approve and GET /api/recovery/case/v1/admin/service-levels/{loadId} in rwb-case; POST /api/recovery/access/v1/authorise in rwb-access; and the one further path named in the detcheck. |

### OTHER:Wave 4 contract review (P3 owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07798 | RWB-P4-AD015-APP | GAP-2275 | 7 | Column names and effect fields are fixed at the wave 4 contract review; placeholder kept. Parameter rows and SCR-42 split stay open at that review. |

### RWB-P4-AD015-CON; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07805 | RWB-P4-AD015-CON | DOR-RWB-P4-AD015-CON-14 | - | Record the signed epic design sign-off for RWB-P4-AD015-CON; no sign-off exists in the story or source documents. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07806 | RWB-P4-AD015-CON | DOR-RWB-P4-AD015-CON-8 | 12.2 | Publish the four consumed operations that are not yet declared: the three rwb-case service-level paths and the rwb-access authorise path. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20851 | RWB-P4-AD014-APP | R-28400 |  | Load entry decision code and load answer fields sit in the Decision-record library, section 12.2, not in this AsyncAPI file. |

### 05 Technical architecture/Recovery Workbench Interface Specifications v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20893 | RWB-P4-AD008-CON | R-23018 |  | Removal request, answer and failure contract belong in the P4 contract and the integration catalogue INT-21 entry. The bank IAM call contract is not in any source (GAP-0808). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0438 | Queue file layout, cap values, valid-from parameter, queue-load approval route, overflow-refusal message ID and the publication and read surface of the P3 reference-load and queue reads and the P7 approval are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0439 | RWB-AD-015: the service-level file and its warning layout, the valid-from parameter name, the approval route, the exact timer projection fields, the refusal message ID and the running-timer recompute rule are not published | Solution architect | Resolved (directive) |
| GAP-0789 | The version status, the effective dates, the approver reference, the four matrix operations and the right of the load are not specified for the permission matrix | Tech lead of rwb-access with the security administrator and the application owner | Resolved (directive) |
| GAP-0793 | The masking-profile operations, the PII read record and the view-column naming of a masking_rule row are not specified in any source | Solution architect | Resolved (directive) |
| GAP-0806 | rwb-access access review list: the review-cycle store is not defined in any source | Solution architect and the rwb-access tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0807 | rwb-access access review list: JOB-18 is a Temporal Schedule but the story metadata carries no workflow-kit dependency and no cron | Solution architect and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0808 | rwb-access access review list: the bank IAM removal API is not specified | Solution architect and the ACE team integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0809 | rwb-access access review list: the sources do not name the role owner who certifies a role | Security administrator and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0810 | rwb-access access review list: the state not confirmed is not defined | Security administrator | Resolved (directive) |
| GAP-0811 | List-of-values rows and reference-load endpoints are P3's while the console load is P4's | Solution architect | Resolved (directive) |
| GAP-0812 | The list-of-values load file format is not specified | Tech lead | Resolved (directive) |
| GAP-0813 | The source and scope of the count of records using a value code are not specified | Tech lead | Resolved (directive) |
| GAP-0814 | The load checks other than the English label are not specified, and the FSD has no load section | Tech lead | Resolved (directive) |
| GAP-0815 | The file-size and row caps of a load are not specified | Tech lead | Resolved (directive) |
| GAP-0816 | The reference-load approve path is P3's while the approval gate is P4's | Solution architect | Resolved (directive) |
| GAP-0817 | The legacy permission row gives Reference data A to service identities while the legacy criterion has a person approving | Security administrator | Resolved (directive) |
| GAP-0818 | An approval given before the valid-from date is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0819 | How the four-eyes rule treats a service-identity author is not specified | Solution architect | Resolved (directive) |
| GAP-0820 | The refused self-approval uses MSG-P7-002, a decision-centre message | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0821 | rwb-access rule-version load: the rule registry is P7's but the story's contract-dependency list carries no P7 rule-package contract | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0822 | rwb-access rule-version load: the compile, the checks and the SIT scenario run need the Drools kit RWB-PLT-E1072-CON, which is not in this story's build list | Solution architect | Resolved (directive) |
| GAP-0823 | rwb-access rule-version load: the route-set workbook format (sheet, header order, required columns) is not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0824 | rwb-access rule-version load: what the result attached to the version means is not specified | Business analyst, P4 | Resolved (directive) |
| GAP-0825 | rwb-access rule-version load: whether a row without a test case ID refuses the version at upload or at approval is ambiguous | Business analyst, P4 | Resolved (directive) |
| GAP-0826 | rwb-access rule-version approval: the registry's approve contract is not in the story's dependency list | Solution architect | Resolved (directive) |
| GAP-0827 | rwb-access rule-version approval: no rwb-access path is declared for the approval gate | Solution architect | Resolved (directive) |
| GAP-0828 | rwb-access rule-version approval: the change checklist content, its evidence and its catalogue are not specified | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0829 | rwb-access rule-version approval: MSG-P3-022 is a P3 message whose text no source gives | Business analyst, P4 | Resolved (directive) |
| GAP-0830 | rwb-access rule-version approval: the decision code and the entry fields of an approval record are not specified | Solution architect | Resolved (directive) |
| GAP-0831 | rwb-access rule-version approval contract: the checklist state and the decision-record reference have no source definition | Tech lead of rwb-access | Resolved (directive) |
| GAP-0832 | rwb-access rule-version approval contract: the version row is read through the package version list, whose change_checklist property is not declared | Solution architect | Resolved (directive) |
| GAP-0844 | rwb-access rollback gate: the rule arm calls the P7 rule-package rollback, but the story's contract-dependency list carries only P3 contracts | Solution architect | Resolved (directive) |
| GAP-0845 | rwb-access rollback gate: no rwb-access rollback path and no read-back resource exist in the API Specification v4 or the P4 technical specification | Solution architect | Resolved (directive) |
| GAP-0846 | rwb-access rollback gate: one legacy action covers a rule version and a reference-data version whose restores belong to two owners, and no source defines a request that carries the target kind | Business analyst, P4 | Resolved (directive) |
| GAP-0847 | rwb-access rollback gate: the loader's right on a rule or reference version is given as C in the legacy permission checks and as U in the technical specification and API-P4-018 | Business analyst, P4 | Resolved (directive) |
| GAP-0848 | rwb-access rollback gate: 'and the owner approves' leaves the approver's area right, the message text and the refusal status of a self-approval open | Business analyst, P4 | Resolved (directive) |
| GAP-0849 | rwb-access rollback gate: the two decision-record entries of a rollback have no decision code and no field set in any source | Business analyst, P4 | Resolved (directive) |
| GAP-0850 | rwb-access rollback gate: 'with an immediate date' is not defined, and no source says whether a rollback may be dated in the future or the past | Business analyst, P4 | Resolved (directive) |
| GAP-0851 | rwb-access rollback gate: the rollback reason has no length, no coded list and no required flag in either owner's RollbackRequest | Business analyst, P4 | Resolved (directive) |
| GAP-0852 | rwb-access rollback contract: the two provided operations and the read of a rollback have no source path, operation id or resource to baseline against | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0853 | rwb-access rollback contract: the restored version, the effective-from time, the two decision-record references and the statement about decisions from that time have no field-level definition | Solution architect | Resolved (directive) |
| GAP-0854 | rwb-access rollback contract: the two decision codes of the entries have no published list, so the contract declares proposed values | Business analyst, P4 | Resolved (directive) |
| GAP-0855 | rwb-access rollback contract: the self-approval refusal has no text in the P4 module and its status is 403 in one P4 story and 409 in the FSD examples | Solution architect | Resolved (directive) |
| GAP-0856 | rwb-access queue-load gate: API Specification v4 declares no rwb-access path for the queue load, the approval or the read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0857 | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Business analyst, P4 | Resolved (directive) |
| GAP-0858 | rwb-access queue load: the queue file layout is not specified, and the legacy file's member sheet is a P3 table | Reference data administrator | Resolved (directive) |
| GAP-0860 | rwb-access queue load: the assignment-method list LOV-ASSIGN is declared in the P3 specification and absent from the P4 specification the gate is written from | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0861 | rwb-access queue load: the required answer carries a version label and a state the owner's load schema does not return, and the load decision code is not specified | Solution architect | Resolved (directive) |
| GAP-0862 | rwb-access queue load: legacy AC1 states an allocation outcome that this story does not own | Business analyst, P4 | Resolved (directive) |
| GAP-0863 | rwb-access queue load: the approval right is declared as Reference data A held by no role, as Rules and parameters A for RW-RISK, and as a per-table approver role | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0864 | rwb-access queue load contract: no source publishes the queue-row schema or the file layout the document must declare | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0868 | The rule-change request record while the registry, the load gate and the approval belong to other stories | Tech lead of rwb-access | Resolved (directive) |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1565 | The rule package registry, the rule-package operations and the change report are claimed by the P4 technical specification while the Ownership Map gives them to rwb-decision | Solution architect with the rwb-decision contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1572 | The six-monthly access review list has no interface, no file layout, no review-date convention and no recipient | Security administrator with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2271 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-012 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2272 | Two Work Packages write the same two story files and two fragments for legacy RWB-AD-013 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2273 | The queue-file check surface, the last two queue columns, the member sheet, the cap limit key, the finding codes, the right of the load and the decision code are not specified in the sources | Solution architect | Resolved (directive) |
| GAP-2274 | The contract document of the queue-file check has no source schemas, no source finding codes and no source right for the approval | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2275 | Service-level load gate: the operations, the file columns, the effect list, the parameter rows and the SCR-42 panel split are not named for rwb-access | Solution architect, P4 and the P3 owner of the service-level and timer contract | Resolved (directive) |
| GAP-2276 | The right letters of the service-level load and approval differ between the legacy story and TSD P4 v3 | Solution architect, security administrator role, P4 | Resolved (directive) |
| GAP-2277 | The contract document of the access-side service-level load has no declared source for its paths, schemas and error bodies | Tech lead, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2280 | The configuration-rollback writes, the four target kinds, the version-before rule, the act date, the right that opens it and the two record codes are not in the sources, and the feature is already carried by another P4 story | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2283 | The legacy right of the panel change and the capability area of the technical specification disagree on who publishes it | Security administrator | Resolved (directive) |
| GAP-2288 | The pack, its three check codes, the two operations, the five schemas, the parameter rows, the decided-version rule and the record code are not in the sources | Tech lead of rwb-access | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P4-AD013-APP | Not specified without item ID | 53 | - The reason a rollback must carry is required; its length is Not specified in the source documents, read as 20 to 1000 characters as a placeholder until either |
