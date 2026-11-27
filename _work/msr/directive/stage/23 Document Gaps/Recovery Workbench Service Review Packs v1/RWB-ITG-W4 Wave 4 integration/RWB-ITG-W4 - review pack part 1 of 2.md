# RWB-ITG-W4 Wave 4 integration - review pack, part 1 of 2 (RWB-ITG-AD014-ITG to RWB-ITG-E6021-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 19 |
| Resolved in the stories | 325 |
| Cross-document (pending in another document) | 213 |
| Not applied (value not in the sources) | 27 |
| Open business decisions | 14 |
| Register gaps linked | 97 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-AD014-ITG | 17 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG AD014 ITG Configure queues - integration v2.md |
| RWB-ITG-AD015-ITG | 15 | 10 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG AD015 ITG Configure service levels and timers - integration v2.md |
| RWB-ITG-AD018-ITG | 22 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG AD018 ITG Interface and job monitor - integration v2.md |
| RWB-ITG-AD019-ITG | 16 | 23 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG AD019 ITG Data quality and reconciliation console - integration v2.md |
| RWB-ITG-AD022-ITG | 10 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG AD022 ITG Partner firms and partner users - integration v2.md |
| RWB-ITG-DM003-ITG | 16 | 14 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM003 ITG Migrate case and ownership - integration v2.md |
| RWB-ITG-DM004-ITG | 15 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM004 ITG Migrate treatment and offers - integration v2.md |
| RWB-ITG-DM005-ITG | 19 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM005 ITG Migrate contact and promises - integration v2.md |
| RWB-ITG-DM006-ITG | 21 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM006 ITG Migrate collateral and assets - integration v2.md |
| RWB-ITG-DM007-ITG | 18 | 10 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM007 ITG Migrate legal events and cases - integration v2.md |
| RWB-ITG-DM008-ITG | 18 | 8 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM008 ITG Migrate partner performance - integration v2.md |
| RWB-ITG-DM009-ITG | 19 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM009 ITG Migrate debt sale - integration v2.md |
| RWB-ITG-DM010-ITG | 19 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM010 ITG Migrate documents and extracted fields - integration v2.md |
| RWB-ITG-DM011-ITG | 19 | 8 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM011 ITG Migrate scores and route economics - integration v2.md |
| RWB-ITG-DM012-ITG | 18 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM012 ITG Migrate decision log - integration v2.md |
| RWB-ITG-DM013-ITG | 18 | 13 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG DM013 ITG Migrate money and closure - integration v2.md |
| RWB-ITG-E6008-ITG | 13 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG E6008 ITG Derecognize and post to the general ledger - integration v2.md |
| RWB-ITG-E6017-ITG | 12 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG E6017 ITG Route the population to the committee and schedule it - integration v2.md |
| RWB-ITG-E6021-ITG | 20 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W4 Wave 4 integration/RWB ITG E6021 ITG Post an approved write-off - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-AD019-ITG | R-09257 | CG-ALL-965 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-DM005-ITG | R-09265 | CG-ALL-1001 | Script gap | Product owner | Open decision DL29 has no assumption | Owner rules DL29; until then build on the recommended option. |
| RWB-ITG-AD014-ITG, RWB-P4-AD014-APP, RWB-P4-AD014-CON | R-21777 | GAP-0859 | Register gap | Product owner | rwb-access queue load: no caseload cap value and no default cap is specified | Keep the cap out of code entirely: a row without a cap is accepted, a cap present is validated as a positive integer, and the values are supplied by the business through DL23 when they are agreed. |
| RWB-ITG-DM005-ITG, RWB-P1-DM005-APP | R-21808 | GAP-2166 | Register gap | Data steward and data product owner | The cutover extract layout, the place of the two ACE business keys on the interaction row and the owning data product of contact_point_ext are not fixed by any target source | Settle the three points at the cutover rehearsal: publish the dump layout and cutover record format with the release pipeline owner, add the two business-key columns to the interaction dictionary rows or state that source_ref carries them, and record in the data product catalog whether contact_point_ext is loaded by the DP05 cutover or by the DP02 story. |
| RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-P1-DM007-APP, RWB-P1-DM008-APP | R-21816 | GAP-0535 | Register gap | Data steward and data product owner of rwb-source-data with the S9 rwb-partner tech lead and the data migration lead | The DM007 and DM008 instruction slice, the handover package format, the recency proof of a product with no ACE view and the field list beyond AC1 are not fixed by one source | Rule the instruction slice at the cutover rehearsal: this key hands over the panel, the partner users and the performance facts of the instructions, RWB-DM-007 hands over the instructions raised for legal actions, and S9 loads both idempotently on the instruction id; fix the package layout and the handover point in the cutover record; count the ten clean days from the reconciliation_result rows of JOB-04 for the business dates after the load, a PASS row with no unexplained variance and no new REC-05 orphan per day, with a break resetting the count; and carry the three legacy field ranges whole so that the field list beyond AC1 is the legacy dictionary's and not the story's. |
| RWB-ITG-DM010-ITG, RWB-P1-DM010-APP | R-21829 | GAP-2174 | Register gap | Data steward and data product owner (RW-DATASTEW) with the rwb-document service owner and the ACE team lead | RWB-DM-010: the owner of the document records, the legacy dump, the handover and the legacy retention period are not specified for the realigned split | Accept the Ownership Map split: rwb-source-data extracts and hands over, rwb-document loads into rwb_document on its own sequence, rwb-case holds recovery_case. Read the dump once from the legacy Workbench cutover dump into a file with a checksum, keep the legacy field range unchanged, and record the source, the handover location and the retention period in the cutover record of the release pipeline at the wave 4 entry check. |
| RWB-ITG-E6021-ITG, RWB-S3-E4013-APP, RWB-S3-E4013-CON, RWB-S7-E6021-APP, RWB-S7-E6021-CON | R-22822 | GAP-1619 | Register gap | Business lead with the center of excellence analyst | A committee decision has no field for the members present or their votes, although the requirement and the screen need both | Agree a member and vote structure for the committee path before Epic 4, either as two child tables of approval or as a versioned structure inside terms, and extend the decision-log entry so the committee's outcome and its members are queryable in the population query. |
| RWB-ITG-DM006-ITG, RWB-P1-DM006-APP | R-28408 | GAP-2168 | Register gap | Data steward and data product owner | Retention period of the legacy tables after cutover is not given | Take the period from the retention class of the record class in retention_rule, and name it in the cutover plan. |
| RWB-ITG-DM012-ITG, RWB-P1-DM012-APP | R-28412 | GAP-2177 | Register gap | Data steward and data product owner | The legacy decision-log extract's source, format and location, the retention period of the legacy tables and the place that holds the sign-off are not specified | Take the extract from the legacy Workbench cutover dump of the release pipeline, name its format and location in the cutover plan, take the retention period from the retention class of the record class in retention_rule, and hold the sign-off in the cutover record. |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-ITG-DM005-ITG | R-33378 | ASM-ALL-1001 | Script assumption |  | Built on the recommended option of DL29: B, named by the business lead. | Data lead with the business lead rules DL29 |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-AD014-ITG | R-03306 | DOR-RWB-ITG-AD014-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size in the story, its readiness review or the '22 Microservice Realignment' documents. The Size row records it as Not specified in the source documents (DOR-RWB-ITG-AD014-ITG-16). |
| RWB-ITG-AD015-ITG | R-03313 | DOR-RWB-ITG-AD015-ITG-16 |  | Definition of Ready item 16 Size: Fail | No size for this split story in 22 Microservice Realignment or earlier searches; entering one invents a value. DoR v3 item 16: squad sizes at refinement. |
| RWB-ITG-AD015-ITG | R-13667 | DOR-RWB-ITG-AD015-ITG-15 | n/a | Definition of Ready item 15 INVEST: Partial | No source gives a size or iteration fit for this story, so none is claimed. The squad must size it (see DOR-RWB-ITG-AD015-ITG-16). |
| RWB-ITG-AD019-ITG | R-03324 | DOR-RWB-ITG-AD019-ITG-16 | header | Definition of Ready item 16 Size: Fail | Size row added and reads Not specified in the source documents; no size value is available, so the item stays open. |
| RWB-ITG-AD019-ITG | R-13687 | DOR-RWB-ITG-AD019-ITG-20 | header | Definition of Ready item 20 Reference data: Partial | Reference data row added; parameters, lists and the reference-data contract (DP-06, DP-07) are Not specified in the source documents, so the item stays open. |
| RWB-ITG-DM003-ITG | R-03334 | DOR-RWB-ITG-DM003-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design for RWB-ITG-W4 in story or sources (grep of *.md for RWB-ITG-W4 sign-off/approved). Recording one would invent a sign-off. |
| RWB-ITG-DM003-ITG | R-03335 | DOR-RWB-ITG-DM003-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size is given in the source documents; the squad sizes at refinement. |
| RWB-ITG-DM003-ITG | R-03337 | DOR-RWB-ITG-DM003-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version in sources. Grep of *.md for fake published/version found only other stories. Stating one would invent a value. |
| RWB-ITG-DM004-ITG | R-03341 | DOR-RWB-ITG-DM004-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size value in the sources; the squad sizes the story at refinement. |
| RWB-ITG-DM007-ITG | R-03358 | DOR-RWB-ITG-DM007-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed RWB-ITG-W4 epic design found in story or sources (grep of sign-off/approved wording). Recording one would invent a sign-off. |
| RWB-ITG-DM007-ITG | R-03359 | DOR-RWB-ITG-DM007-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size is given in the item or story text, and one cannot be invented. The check stays open until the squad sizes the story. |
| RWB-ITG-DM007-ITG | R-03360 | DOR-RWB-ITG-DM007-ITG-21 |  | Definition of Ready item 21 Contract published: Fail | DM007-CON appears only in _work/msr scratch files, no story in 04 User stories. Adding a CON dependency would invent a story key. |
| RWB-ITG-DM007-ITG | R-03361 | DOR-RWB-ITG-DM007-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version in the sources (DM003-ITG has the same gap). Writing a version would invent a value. |
| RWB-ITG-DM007-ITG | R-09274 | CG-ALL-1020 | 11, 16 | Criteria and test data read ACE views directly | §11 now reads DP07 only through the data product contract. §16 TC-01 data is now served by the contract fake. §7 AC1 is not yet checked for direct ACE view reads, so the item stays open. |
| RWB-ITG-DM008-ITG | R-03364 | DOR-RWB-ITG-DM008-ITG-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record for RWB-ITG-W4 in the sources (searched *.md outside 23 Document Gaps). Recording a sign-off would invent a fact. |
| RWB-ITG-DM008-ITG | R-03367 | DOR-RWB-ITG-DM008-ITG-22 |  | Definition of Ready item 22 Fake published: Fail | Service Contract Catalog v2 L1491 gives only the naming rule ('<service> contract fake' + contract version). No published fake is recorded; claiming one would be invented. |
| RWB-ITG-DM008-ITG | R-21821 | GAP-0536 | 7 | RWB-ITG-DM008-ITG states that the cutover load into rwb_partner runs on P1's own Flyway sequence, which DP-01 and the Ownership Map forbid | AC9 states that each service applies its own Flyway sequence, but no correction was made to the statement the item cites in sections 1 and 19. Those sections still need checking. |
| RWB-ITG-DM011-ITG | R-03383 | DOR-RWB-ITG-DM011-ITG-16 | Header | Definition of Ready item 16 Size: Fail | Size row added as Not specified in the source documents; no size exists, so the item stays open until the squad sizes it at refinement. |
| RWB-ITG-DM011-ITG | R-03385 | DOR-RWB-ITG-DM011-ITG-22 | Header | Definition of Ready item 22 Fake published: Fail | Fake library version row added as Not specified in the source documents; no published fake is recorded, so the item stays open. |
| RWB-ITG-DM011-ITG | R-03386 | DOR-RWB-ITG-DM011-ITG-23 | Header | Definition of Ready item 23 Contract version fixed: Fail | Contract version row added as Not specified in the source documents; only the /v1 path is known, so the item stays open. |
| RWB-ITG-DM013-ITG | R-03394 | DOR-RWB-ITG-DM013-ITG-14 | header | Definition of Ready item 14 Epic design: Fail | No signed EP08 design record was found. An Epic design sign-off header row was added reading Not specified; a sign-off cannot be invented. |
| RWB-ITG-DM013-ITG | R-03395 | DOR-RWB-ITG-DM013-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size is given in the sources and none can be invented. A Size header row was added reading Not specified. |
| RWB-ITG-DM013-ITG | R-03397 | DOR-RWB-ITG-DM013-ITG-22 | header | Definition of Ready item 22 Fake published: Fail | No published fake version was found. A Contract fake library version header row was added reading Not specified. |
| RWB-ITG-DM013-ITG | R-03398 | DOR-RWB-ITG-DM013-ITG-23 | Header | Definition of Ready item 23 Contract version fixed: Fail | No contract version is given in the sources. Header row reads Not specified; a version cannot be invented. |
| RWB-ITG-E6008-ITG | R-03987 | DOR-RWB-ITG-E6008-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size for this story is given, so the DoR item stays open. |
| RWB-ITG-E6008-ITG | R-22813 | GAP-0454 | 14, 15 | The derecognition and general ledger posting harness pack for the debt sale journey is not specified | The harness pack remains Not specified in the source documents (GAP-0454; ASM-0646); no agreement, owner or fixture can be recorded. |
| RWB-ITG-E6017-ITG | R-03994 | DOR-RWB-ITG-E6017-ITG-16 | 6 | Definition of Ready item 16 Size: Fail | DoR v4 item 16 needs a squad size; no size exists in the story text or the sources and the source excerpts returned no lines, so any value would be invented. Sizing stays with the squad at refinement. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (27)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00069 | RWB-ITG-DM003-ITG | CG-ALL-978 | 16 | Story side: TC rows 01-04 already present; rows 05-10 added for AC5-AC10. Test Cases v8 has no rows for TC-DM-003-01-ITG to 04-ITG; add 01-ITG to 10-ITG. |
| CDC-00071 | RWB-ITG-DM003-ITG | DOR-RWB-ITG-DM003-ITG-12 | 16 | Story side: TC rows 05-10 added in section 16 for the new criteria; the four original test cases are also missing from v8. |
| CDC-00087 | RWB-ITG-DM004-ITG | CG-ALL-989 | 16 | Add rows TC-DM-004-01-ITG, TC-DM-004-02-ITG, TC-DM-004-03-ITG and TC-DM-004-04-ITG in the next version, with Given, When and Then copied from the criteria they cover. |
| CDC-00089 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-12 | 16 | Add rows TC-DM-004-01-ITG, TC-DM-004-02-ITG, TC-DM-004-03-ITG and TC-DM-004-04-ITG in the next version, with Given, When and Then copied from the criteria they cover. |
| CDC-00099 | RWB-ITG-DM005-ITG | CG-ALL-997 | 16 | Add rows TC-DM-005-01-ITG to TC-DM-005-04-ITG to tab Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-00100 | RWB-ITG-DM005-ITG | DOR-RWB-ITG-DM005-ITG-12 | 16 | Add rows TC-DM-005-01-ITG to TC-DM-005-04-ITG to tab Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-00112 | RWB-ITG-DM006-ITG | CG-ALL-1009 | 16 | TC-DM-006-01-ITG to TC-DM-006-07-ITG need rows in the Test Cases workbook; the story cannot add them. |
| CDC-00113 | RWB-ITG-DM006-ITG | DOR-RWB-ITG-DM006-ITG-12 | 16 | Section 16 maps every criterion to a test case; the workbook still lacks TC-DM-006-01-ITG to TC-DM-006-07-ITG. |
| CDC-00119 | RWB-ITG-DM007-ITG | CG-ALL-1019 | 16 | §16 states that the new TC-DM-007-05-ITG to 07-ITG have no workbook row yet. |
| CDC-00120 | RWB-ITG-DM007-ITG | DOR-RWB-ITG-DM007-ITG-12 | 16 | Add rows TC-DM-007-01-ITG to TC-DM-007-04-ITG with Given, When and Then copied from the criterion each covers. |
| CDC-00128 | RWB-ITG-DM008-ITG | CG-ALL-1026 | 16 | Add rows TC-DM-008-01-ITG to TC-DM-008-04-ITG with Given, When and Then from the criteria they cover |
| CDC-00129 | RWB-ITG-DM008-ITG | DOR-RWB-ITG-DM008-ITG-12 | 16 | Rows 05 to 09 were added to section 16 for the new criteria; the four existing rows are unchanged. The workbook edit is outside this story. |
| CDC-00139 | RWB-ITG-DM009-ITG | CG-ALL-1032 | 16 | Add Story test cases rows for TC-DM-009-01-ITG, TC-DM-009-02-ITG, TC-DM-009-03-ITG and TC-DM-009-04-ITG with Given, When and Then copied from the criteria they cover |
| CDC-00141 | RWB-ITG-DM009-ITG | DOR-RWB-ITG-DM009-ITG-12 | 16 | Story section 16 lists seven TCs, TC-DM-009-01-ITG to TC-DM-009-07-ITG; the test case workbook must carry them. |
| CDC-00147 | RWB-ITG-DM010-ITG | CG-ALL-1041 | 16 | Add story test case rows TC-DM-010-01-ITG, TC-DM-010-02-ITG, TC-DM-010-03-ITG and TC-DM-010-04-ITG, with Given, When and Then copied from the criteria they cover. |
| CDC-00148 | RWB-ITG-DM010-ITG | DOR-RWB-ITG-DM010-ITG-12 | 16 | Add story test case rows TC-DM-010-01-ITG to TC-DM-010-04-ITG, with Given, When and Then copied from the criteria they cover. |
| CDC-00154 | RWB-ITG-DM011-ITG | CG-ALL-1048 | 16 | Add rows for TC-DM-011-01-ITG, TC-DM-011-02-ITG, TC-DM-011-03-ITG and TC-DM-011-04-ITG to Story test cases, with Given, When and Then copied from the criteria in section 16. |
| CDC-00155 | RWB-ITG-DM011-ITG | DOR-RWB-ITG-DM011-ITG-12 | 16 | Add test cases TC-DM-011-01-ITG, TC-DM-011-02-ITG, TC-DM-011-03-ITG, TC-DM-011-04-ITG and TC-DM-011-05-ITG (05 new from this story, AC5). |
| CDC-00163 | RWB-ITG-DM012-ITG | CG-ALL-1057 | 16 | Add Story test cases rows TC-DM-012-01-ITG to TC-DM-012-05-ITG, with Given, When and Then copied from the ITG criteria they cover in section 7 |
| CDC-00164 | RWB-ITG-DM012-ITG | DOR-RWB-ITG-DM012-ITG-12 | 16 | Section 16 now lists eight test cases, TC-DM-012-01-ITG to 08-ITG; the matching rows are missing from Test Cases v8, outside this story. |
| CDC-00170 | RWB-ITG-DM013-ITG | CG-ALL-1067 | 16 | Add rows TC-DM-013-01-ITG to TC-DM-013-04-ITG with Given, When and Then copied from the criteria they cover. |
| CDC-00171 | RWB-ITG-DM013-ITG | DOR-RWB-ITG-DM013-ITG-12 | 16 | Add rows TC-DM-013-01-ITG to TC-DM-013-04-ITG with Given, When and Then copied from the criteria they cover. |
| CDC-01987 | RWB-ITG-E6008-ITG | CG-ALL-1074 | 16 | Add rows TC-E6-008-01-ITG to TC-E6-008-06-ITG to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-01989 | RWB-ITG-E6008-ITG | DOR-RWB-ITG-E6008-ITG-12 | 16 | §16 lists eight TC IDs (TC-E6-008-01-ITG to 08-ITG); the matching rows are missing from Test Cases v8. |
| CDC-01996 | RWB-ITG-E6017-ITG | DOR-RWB-ITG-E6017-ITG-12 | 16 | Add rows for TC-E6-017-01-ITG to TC-E6-017-07-ITG, with Given, When and Then copied from the criteria they cover. |
| CDC-02001 | RWB-ITG-E6017-ITG | CG-ALL-1081 | 16 | Add rows for TC-E6-017-01-ITG to TC-E6-017-06-ITG and TC-E6-017-07-ITG, with Given, When and Then copied from the criteria. |
| CDC-02011 | RWB-ITG-E6021-ITG | CG-ALL-1087 | 16 | Story §16 now also lists TC-E6-021-07-ITG to TC-E6-021-09-ITG; the Test Cases workbook must carry all nine rows. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (24)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00032 | RWB-ITG-AD019-ITG | CG-ALL-956 | 12.2 | Publish GET /api/recovery/source-data/v1/<reconciliation read> through the provider CON story; the story keeps the operation as is. |
| CDC-00033 | RWB-ITG-AD019-ITG | CG-ALL-957 | 12.2 | Publish GET /api/recovery/source-data/v1/<key-resolution read> through the provider CON story; the story keeps the operation as is. |
| CDC-00064 | RWB-ITG-DM003-ITG | CG-ALL-974 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId} through the provider's CON story. |
| CDC-00065 | RWB-ITG-DM003-ITG | CG-ALL-975 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} through the provider's CON story. |
| CDC-00078 | RWB-ITG-DM004-ITG | CG-ALL-983 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId} through the provider's CON story |
| CDC-00079 | RWB-ITG-DM004-ITG | CG-ALL-984 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} through the provider's CON story |
| CDC-00080 | RWB-ITG-DM004-ITG | CG-ALL-985 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP04/records?caseId={caseId} through the provider's CON story |
| CDC-00092 | RWB-ITG-DM005-ITG | CG-ALL-993 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} through the provider's CON story, or agree a published operation to consume. |
| CDC-00093 | RWB-ITG-DM005-ITG | CG-ALL-994 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP05/records?caseId={caseId} through the provider's CON story, or agree a published operation to consume. |
| CDC-00104 | RWB-ITG-DM006-ITG | CG-ALL-1003 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP06/records with query parameter caseId through the provider CON story. |
| CDC-00105 | RWB-ITG-DM006-ITG | CG-ALL-1004 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP01/records with query parameter caseId through the provider CON story. |
| CDC-00106 | RWB-ITG-DM006-ITG | CG-ALL-1005 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP02/records with query parameter caseId through the provider CON story. |
| CDC-00115 | RWB-ITG-DM007-ITG | CG-ALL-1014 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP07/records?caseId={caseId} through the provider's CON story, or have the story consume a published operation. |
| CDC-00116 | RWB-ITG-DM007-ITG | CG-ALL-1015 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} through the provider's CON story, or have the story consume a published operation. |
| CDC-00165 | RWB-ITG-DM013-ITG | CG-ALL-1062 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/{product}/records with caseId query, for DP13, through the provider's CON story. |
| CDC-00166 | RWB-ITG-DM013-ITG | CG-ALL-1063 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/{product}/records with caseId query, for DP01, through the provider's CON story. |
| CDC-00167 | RWB-ITG-DM013-ITG | CG-ALL-1064 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/{product}/records with caseId query, for DP02, through the provider's CON story. |
| CDC-01982 | RWB-ITG-E6008-ITG | CG-ALL-1071 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId} through the provider's CON story |
| CDC-01983 | RWB-ITG-E6008-ITG | CG-ALL-1072 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP09/records?caseId={caseId} through the provider's CON story |
| CDC-01985 | RWB-ITG-E6008-ITG | DOR-RWB-ITG-E6008-ITG-8 | 12.2, 12.4 | Publish the DP01 and DP09 records paths; event type fix already applied in story (CG-ALL-1073) |
| CDC-01995 | RWB-ITG-E6017-ITG | CG-ALL-1079 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId} through the provider's CON story, or the consumer switches to a published operation. |
| CDC-02000 | RWB-ITG-E6017-ITG | DOR-RWB-ITG-E6017-ITG-8 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId} via the provider's CON story. |
| CDC-02007 | RWB-ITG-E6021-ITG | CG-ALL-1085 | 12.2 | Publish GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId} through the provider's CON story, so the consumed operation exists in the yaml. |
| CDC-02010 | RWB-ITG-E6021-ITG | DOR-RWB-ITG-E6021-ITG-8 | header | Publish GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}. The event-type part is resolved in the story at 12.4. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00006 | RWB-ITG-AD014-ITG | DOR-RWB-ITG-AD014-ITG-1 | 1 | Register role name 'QA integration engineer' so the section 1 role resolves |
| CDC-00007 | RWB-ITG-AD014-ITG | DOR-RWB-ITG-AD014-ITG-6 | 10 | Register role code RW-OFF with Rules and parameters R and not A |
| CDC-00021 | RWB-ITG-AD015-ITG | DOR-RWB-ITG-AD015-ITG-6 | 10 | Hold role RW-OFF (officer without the administration rights, no Rules and parameters right) as used in section 10 and AC3. |
| CDC-00027 | RWB-ITG-AD018-ITG | DOR-RWB-ITG-AD018-ITG-1 | 1 | Add or map the role 'QA integration engineer' so section 1 names a role code or role name |
| CDC-00028 | RWB-ITG-AD018-ITG | DOR-RWB-ITG-AD018-ITG-6 | 10 | Add role RW-OFF (officer without the administration rights) used in section 10, AC4 and X6. |
| CDC-00044 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-1 | 1 | Add a role for QA integration engineer, or map the section 1 persona to an existing role code and name. |
| CDC-00045 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-6 | 10 | Add role RW-OFF (no Platform administration R; refused caller of AC5) or confirm the code used in section 10 |
| CDC-00059 | RWB-ITG-AD022-ITG | DOR-RWB-ITG-AD022-ITG-1 | 1 | Add 'QA integration engineer' as a role code or role name, or confirm the role that section 1 should use. |
| CDC-00060 | RWB-ITG-AD022-ITG | DOR-RWB-ITG-AD022-ITG-6 | 10 | Add role RW-OFF, the synthetic caller without Partner portal R used by AC4 and TC-AD-022-03-ITG. |
| CDC-00070 | RWB-ITG-DM003-ITG | DOR-RWB-ITG-DM003-ITG-1 | 1 | Add role code RW-DATASTEW with role name data steward (runs and reads the reconciliation; holds Platform administration R). |
| CDC-00088 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-1 | 1 | Add or confirm role RW-DATASTEW with name data steward so that the section 1 role resolves. |
| CDC-00102 | RWB-ITG-DM005-ITG | DOR-RWB-ITG-DM005-ITG-6 | 10 | Add or confirm role RW-OFF, which section 10 and section 16 use for the refused caller. |
| CDC-00140 | RWB-ITG-DM009-ITG | DOR-RWB-ITG-DM009-ITG-1 | section 1 | Section 1 names the data steward and marks the role code Not specified. URP v5 must define the data steward role code. |
| CDC-01990 | RWB-ITG-E6008-ITG | DOR-RWB-ITG-E6008-ITG-6 | 10 | Add role RW-OFF, which §10 lists and AC6 uses as the refused caller. |
| CDC-02003 | RWB-ITG-E6017-ITG | DOR-RWB-ITG-E6017-ITG-6 | 10 | Add role RW-OFF to the role list, so the section 10 role is held in the roles document. |
| CDC-02013 | RWB-ITG-E6021-ITG | DOR-RWB-ITG-E6021-ITG-6 | 10 | Add role RW-OFF (Case officer), used in §10 as the synthetic caller of AC6 |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00066 | RWB-ITG-DM003-ITG | CG-ALL-976 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story. |
| CDC-00081 | RWB-ITG-DM004-ITG | CG-ALL-986 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story |
| CDC-00094 | RWB-ITG-DM005-ITG | CG-ALL-995 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or agree a published operation to consume. |
| CDC-00107 | RWB-ITG-DM006-ITG | CG-ALL-1006 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider CON story. |
| CDC-00117 | RWB-ITG-DM007-ITG | CG-ALL-1016 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or have the story consume a published operation. |
| CDC-00125 | RWB-ITG-DM008-ITG | CG-ALL-1024 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story |
| CDC-00126 | RWB-ITG-DM008-ITG | DOR-RWB-ITG-DM008-ITG-21 | header | The provider must publish the authorise operation (CG-ALL-1024). The header records it as outstanding and names no separate contract story. |
| CDC-00127 | RWB-ITG-DM008-ITG | DOR-RWB-ITG-DM008-ITG-8 | 12.2 | Same root cause as CG-ALL-1024; the provider must publish the operation. |
| CDC-00133 | RWB-ITG-DM009-ITG | CG-ALL-1030 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's contract story RWB-ITG-DM009-CON |
| CDC-00135 | RWB-ITG-DM009-ITG | DOR-RWB-ITG-DM009-ITG-21 | header | Header names the unpublished authorise contract as a dependency; its story key is not specified. Publication is provider-side. |
| CDC-00138 | RWB-ITG-DM009-ITG | DOR-RWB-ITG-DM009-ITG-8 | header | Same publication gap as CG-ALL-1030; Contract dependencies row names the unpublished authorise contract. |
| CDC-00142 | RWB-ITG-DM010-ITG | CG-ALL-1039 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider's CON story |
| CDC-00146 | RWB-ITG-DM010-ITG | DOR-RWB-ITG-DM010-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider's CON story |
| CDC-00150 | RWB-ITG-DM011-ITG | CG-ALL-1045 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the provider's CON story, or have the consumer use a published operation. |
| CDC-00157 | RWB-ITG-DM012-ITG | CG-ALL-1055 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |
| CDC-00162 | RWB-ITG-DM012-ITG | DOR-RWB-ITG-DM012-ITG-8 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. |

### Epic design record (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00002 | RWB-ITG-AD014-ITG | DOR-RWB-ITG-AD014-ITG-14 | n/a | Record the signed epic design sign-off for RWB-ITG-AD014-ITG. |
| CDC-00017 | RWB-ITG-AD015-ITG | DOR-RWB-ITG-AD015-ITG-14 | n/a | Record the signed epic design sign-off for RWB-ITG-W4 in the epic design record. |
| CDC-00025 | RWB-ITG-AD018-ITG | DOR-RWB-ITG-AD018-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-W4 so the Epic design item can pass |
| CDC-00055 | RWB-ITG-AD022-ITG | DOR-RWB-ITG-AD022-ITG-14 | header | Record the signed epic design sign-off for EP08 wave 4 against RWB-ITG-AD022-ITG. |
| CDC-00082 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-14 | header | Record the signed epic design sign-off for the epic in the epic design record |
| CDC-00095 | RWB-ITG-DM005-ITG | DOR-RWB-ITG-DM005-ITG-14 | header | Record the signed epic design sign-off in the epic design record so the story can cite it. |
| CDC-00108 | RWB-ITG-DM006-ITG | DOR-RWB-ITG-DM006-ITG-14 |  | Record the signed epic design sign-off covering this story. |
| CDC-00134 | RWB-ITG-DM009-ITG | DOR-RWB-ITG-DM009-ITG-14 | header | Record the signed EP08 epic design for wave 4 (RWB-ITG-W4) before build starts, per DoR item 14 |
| CDC-00158 | RWB-ITG-DM012-ITG | DOR-RWB-ITG-DM012-ITG-14 | header | Record the signed epic design (sign-off role and date) for service epic RWB-ITG-W4 covering RWB-ITG-DM012-ITG |
| CDC-01997 | RWB-ITG-E6017-ITG | DOR-RWB-ITG-E6017-ITG-14 |  | Record the signed epic design sign-off for this story in the epic design record. |
| CDC-02008 | RWB-ITG-E6021-ITG | DOR-RWB-ITG-E6021-ITG-14 | 3 | Record the signed sign-off of the EP06 epic design that DoR item 14 asks for; neither the story nor the source excerpts hold a signed design (DOR-RWB-ITG-E6021-ITG-14). |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00001 | RWB-ITG-AD014-ITG | CG-ALL-940 | 12.2 | Publish POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve in rwb-decision.yaml through the provider's CON story. |
| CDC-00005 | RWB-ITG-AD014-ITG | DOR-RWB-ITG-AD014-ITG-8 | 12.2 | Publish POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve in rwb-decision.yaml. |
| CDC-00015 | RWB-ITG-AD015-ITG | CG-ALL-945 | 12.2 | Publish POST /api/recovery/decision/v1/admin/rule-versions in rwb-decision.yaml through the provider's CON story. |
| CDC-00016 | RWB-ITG-AD015-ITG | CG-ALL-946 | 12.2 | Publish POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve in rwb-decision.yaml through the provider's CON story. |
| CDC-00020 | RWB-ITG-AD015-ITG | DOR-RWB-ITG-AD015-ITG-8 | 12.2, 12.4 | Publish POST .../admin/rule-versions and POST .../admin/rule-versions/{versionId}/approve in rwb-decision.yaml. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00068 | RWB-ITG-DM003-ITG | DOR-RWB-ITG-DM003-ITG-8 | 12.2 | Publish the three operations GET DP01 records, GET DP02 records (rwb-source-data) and POST /api/recovery/access/v1/authorise (rwb-access) via the provider CON stories. |
| CDC-00086 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-8 | 12.2 | Publish the three rwb-source-data operations and the rwb-access authorise operation through the provider's CON story |
| CDC-00098 | RWB-ITG-DM005-ITG | DOR-RWB-ITG-DM005-ITG-8 | 12.2 | Publish GET DP02 records, GET DP05 records and POST /api/recovery/access/v1/authorise in the provider yaml files. |
| CDC-00111 | RWB-ITG-DM006-ITG | DOR-RWB-ITG-DM006-ITG-8 | 12.2 | Publish the three DP01, DP02, DP06 records GET operations and the POST authorise operation as named in CG-ALL-1003 to CG-ALL-1006. |
| CDC-00118 | RWB-ITG-DM007-ITG | DOR-RWB-ITG-DM007-ITG-8 | 12.2 | Publish the three failing operations (two DP records paths in rwb-source-data.yaml, POST authorise in rwb-access.yaml) through the provider CON stories, or consume published operations. |

### OTHER:plan/split_plan.json (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00067 | RWB-ITG-DM003-ITG | DOR-RWB-ITG-DM003-ITG-21 | Header | Contract dependencies marked Not specified in the source documents. |
| CDC-00072 | RWB-ITG-DM003-ITG | GAP-0240 | header | Cut each schema over in its owning service's wave in section 9.5 order; keep migration story releases as dated, read as latest date. |
| CDC-00075 | RWB-ITG-DM003-ITG | GAP-0236 | 1 | Record the owner-side Flyway load under RWB-PLT-E1044-CON against the owning service story set, in the same cutover step as the P1 extract story; no story ID invented. |
| CDC-00173 | RWB-ITG-DM013-ITG | GAP-0240 | find it | Cut over RWB-ITG-DM013-ITG in the wave of its owning services using the section 9.5 order; keep release 31 December 2026. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB-ITG-W4 Epic Overview v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00143 | RWB-ITG-DM010-ITG | DOR-RWB-ITG-DM010-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-W4 (signing role and date) in the epic design record |
| CDC-00144 | RWB-ITG-DM010-ITG | DOR-RWB-ITG-DM010-ITG-21 |  | Add contract story RWB-ITG-DM010-CON to the epic story list and publish its contract, then set it as this story's CON dependency |
| CDC-00151 | RWB-ITG-DM011-ITG | DOR-RWB-ITG-DM011-ITG-14 | header | Record the signed epic design for RWB-ITG-W4 (sign-off reference and decision ID) so stories in the epic can cite it |
| CDC-00152 | RWB-ITG-DM011-ITG | DOR-RWB-ITG-DM011-ITG-21 | header | Add contract story RWB-ITG-DM011-CON to the epic and publish its contract; then list it in this story's Contract dependencies row |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00011 | RWB-ITG-AD014-ITG | GAP-0863 | find it | Correct the API-P4-006 authorization wording: the approval is checked on Rules and parameters A, and the sentence that Reference data A is held by no role is removed when the P4 API file is next published. |
| CDC-00137 | RWB-ITG-DM009-ITG | DOR-RWB-ITG-DM009-ITG-23 | header | Header states the contract version is not specified beyond the /v1 path; the provider contract must fix it. |
| CDC-02004 | RWB-ITG-E6017-ITG | GAP-1795 | none | Publish the write-off collection operations (GET and POST /write-offs, POST /write-offs/{id}/submit) under /api/recovery/writeoff/v1 and add them to the Microservice Ownership Map v1 endpoints in the same change. |

### RWB-ITG-AD015-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00018 | RWB-ITG-AD015-ITG | DOR-RWB-ITG-AD015-ITG-21 | header | The contract slice is not a story of the set and must be created elsewhere. The Contract dependencies row records that it is not yet created. |
| CDC-00023 | RWB-ITG-AD015-ITG | GAP-2277 | header | Declare ServiceLevelLoad, ServiceLevelRow and RunningTimerEffect, the load state set, and the 422 and 409 bodies, agreed at the wave 4 contract review. |
| CDC-00024 | RWB-ITG-AD015-ITG | GAP-2276 | 8 | Record once whether the service-level gate keeps Rules and parameters A and C (RW-RISK, RW-COE) or uses the Reference data C and A rights of API-P4-005 and API-P4-006, and apply that letter to the app story and SCR-42. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00034 | RWB-ITG-AD019-ITG | CG-ALL-958 | 12.2 | Publish GET /api/recovery/case/v1/data-quality/reconciliation-breaks through the provider CON story; the story keeps the operation as is. |
| CDC-00035 | RWB-ITG-AD019-ITG | CG-ALL-959 | 12.2 | Publish GET /api/recovery/case/v1/data-quality/referential-completeness through the provider CON story; the story keeps the operation as is. |
| CDC-00036 | RWB-ITG-AD019-ITG | CG-ALL-960 | 12.2 | Publish GET /api/recovery/case/v1/data-quality/stale-products through the provider CON story; the story keeps the operation as is. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00090 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-9 | 14 | Add a message ID and text for the extract and SCR-45 disagreement, since MSG-P1-012 is raised for tolerance breach RWB-E1-002. |
| CDC-00091 | RWB-ITG-DM004-ITG | CG-ALL-988 | 14 | Add a new message ID for the extract and SCR-45 disagreement with the story's text; MSG-P1-012 keeps the tolerance-breach trigger RWB-E1-002. |
| CDC-00172 | RWB-ITG-DM013-ITG | DOR-RWB-ITG-DM013-ITG-9 | 14 | Confirm the v4 text of MSG-P1-001 and MSG-P1-012; section 14 text then follows v4. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00159 | RWB-ITG-DM012-ITG | DOR-RWB-ITG-DM012-ITG-21 | header | Name the published contract and its contract story for the DM012 decision log migration harness, or state that this harness needs no contract |
| CDC-00160 | RWB-ITG-DM012-ITG | DOR-RWB-ITG-DM012-ITG-22 | header | Record the published contract fake library version used by the DM012 integration harness |
| CDC-00161 | RWB-ITG-DM012-ITG | DOR-RWB-ITG-DM012-ITG-23 | header | State the fixed contract version (beyond the /v1 path) that RWB-ITG-DM012-ITG builds against |

### OTHER:Data Migration Approach (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00174 | RWB-ITG-DM013-ITG | GAP-0543 | 11 | No source says who loads proceeds, write_off and the closure, or what survives. That ownership belongs in the Data Migration Approach. Section 11 wording is unchanged. |
| CDC-00175 | RWB-ITG-DM013-ITG | GAP-2178 | find it | Record that rwb-payment loads proceeds, rwb-writeoff loads write_off and rwb-case loads closure facts; handover is a checksummed file; sign-off sits in the cutover record; ten clean days are PASS results on reconciliation_result. |
| CDC-00176 | RWB-ITG-DM013-ITG | GAP-2533 | find it | Name the P1 handover file format, location, count, checksum and retention; name the rwb-payment load command and run record; add a provenance column to the proceeds schema; keep payment_code as business key. |

### RWB-S7-E6017-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01998 | RWB-ITG-E6017-ITG | DOR-RWB-ITG-E6017-ITG-21 | header | Contract dependencies row now names RWB-S7-E6017-CON. |
| CDC-01999 | RWB-ITG-E6017-ITG | DOR-RWB-ITG-E6017-ITG-22 | 12.8 | Publish a fake library version generated from the published RWB-S7-E6017-CON contract and record that published version, so the section 12.8 stub is pinned to a published fake of a published version. |
| CDC-02005 | RWB-ITG-E6017-ITG | GAP-3026 |  | Publish the baseline: name the consumed operations, queue and deviation elements, the 27-state list, the meeting-booking attribute and the error message ids, then tag it after owner confirmation. |

### RWB-P4-AD014-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00008 | RWB-ITG-AD014-ITG | GAP-2273 | find it | Declare POST and GET /api/recovery/access/v1/admin/queue-file-checks; Reference data C for POST, R for GET; queue sheet only |
| CDC-00010 | RWB-ITG-AD014-ITG | GAP-0856 | find it | Declare POST /api/recovery/access/v1/admin/queue-loads (multipart load, JSON approval) and GET .../queue-loads/{loadId}; add to P4 API file at D1 |

### OTHER:rwb-access queue load contract document (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00012 | RWB-ITG-AD014-ITG | GAP-0864 | find it | Declare QueueFileRow with the eight columns, QueueLoad with the five answer fields and QueueValidationError with row, field and detail. Sheet name and header order are Not specified in the source documents (GAP-0864) until frozen with the P3 owner and the reference data administrator. |
| CDC-00013 | RWB-ITG-AD014-ITG | GAP-2274 | find it | Publish the four schemas, the seven Error finding codes, the 200, 400, 401, 403, 404, 409, 422 and 503 answers and the envelope mapping in one OpenAPI 3.1 document on base /api/recovery/access/v1. Declare Reference data C and R on the two operations, leave the approval right with rwb-case, declare the Idempotency-Key header with a 200 replay and a 409 on a different file, and keep the document additive within v1. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00022 | RWB-ITG-AD015-ITG | GAP-2275 | 1 | At the wave 4 contract review name the three access-side paths, file columns, effect fields, parameter rows, reference list codes and the SCR-42 panel split. |
| CDC-00130 | RWB-ITG-DM008-ITG | GAP-2170 | 7 | Apply the proposed fix: one package per owner per cut-over business date, API-P1-003 added, flag rwb.source-data.dm007-cutover in parameter-catalog.csv defaulting off, sign-off and window in the cut-over record. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00037 | RWB-ITG-AD019-ITG | CG-ALL-961 | 12.5 | Add DataQualityFreshnessCheck (P3, rwb-case, queue rwb-case) to Workflows, refreshStaleSet to Activities, and its Schedule to Schedules: every 15 minutes in the business window, SKIP, catch-up window, ID data-quality-freshness-<env>. |
| CDC-00043 | RWB-ITG-AD019-ITG | CG-ALL-962 | 12.5 | Add activity refreshStaleSet with task queue rwb-case, as built by RWB-P3-AD019-APP with its DataQualityFreshnessCheck Schedule. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00039 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-21 | header | Publish the section 12.2 reads through provider CON stories; the story now names the CON dependency in Contract dependencies. |
| CDC-00041 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-23 | 12 | Section 12 states the contract version as Not specified in the source documents, with hop versions pinned in the run report; the version is not yet fixed. |

### RWB-ITG-AD022-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00056 | RWB-ITG-AD022-ITG | DOR-RWB-ITG-AD022-ITG-21 | Metadata | Create the contract story RWB-ITG-AD022-CON and publish the contract of RWB-ITG-AD022-ITG in the contract registry, so the story carries the CON dependency the DOR item reports as missing. |
| CDC-00058 | RWB-ITG-AD022-ITG | DOR-RWB-ITG-AD022-ITG-23 | 13 | The contract version must be fixed in the contract document; the story only records that it is Not specified in the source documents. |

### RWB-P1-DM007-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00123 | RWB-ITG-DM007-ITG | GAP-0532 | find it | Agree package layout and cutover record at rehearsal; hand one package per owner per cutover business date; P1 writes no other service's schema; extract carries legacy keys only. |
| CDC-00124 | RWB-ITG-DM007-ITG | GAP-0534 | find it | Count ten clean days on reconciliation_result rows from JOB-04; a BREAK row or new REC-05 orphan resets to zero; keep ten-day rows and sign-off in the cutover record beside the read-only window; flag defaults off. |

### OTHER:rwb-source-data API yaml (provider contract) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00168 | RWB-ITG-DM013-ITG | DOR-RWB-ITG-DM013-ITG-21 | Header | The consumed operations are not yet published; publishing belongs to the provider. Header records this. |
| CDC-00169 | RWB-ITG-DM013-ITG | DOR-RWB-ITG-DM013-ITG-8 | 12.2 | Story paths depend on rwb-source-data publishing them; not editable in this story. |

### RWB-ITG-AD014-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00003 | RWB-ITG-AD014-ITG | DOR-RWB-ITG-AD014-ITG-21 | n/a | Create contract story RWB-ITG-AD014-CON and list it under Contract dependencies. |

### OTHER:Contract fake library (not in the source set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00004 | RWB-ITG-AD014-ITG | DOR-RWB-ITG-AD014-ITG-22 | n/a | Publish the contract fake library version for the rwb-decision operations used. |

### OTHER:P3 and P7 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00009 | RWB-ITG-AD014-ITG | GAP-0438 | find it | Publish queue file layout, cap range, valid-from parameter name and type, one approval route, overflow-refusal message ID, response schemas |

### OTHER:TSD P4 (Technical Specification P4), section T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00014 | RWB-ITG-AD014-ITG | GAP-0860 | find it | Add LOV-ASSIGN with ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER and SKILL to the P4 list section at D1. The story reads it through the rwb-case reference-data contract and declares no value of it in rwb-access. |

### OTHER:Contract fake library (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00019 | RWB-ITG-AD015-ITG | DOR-RWB-ITG-AD015-ITG-22 | n/a | Publish a contract fake library version for the rwb-decision operations and event used by this story. |

### OTHER:rwb-source-data contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00026 | RWB-ITG-AD018-ITG | DOR-RWB-ITG-AD018-ITG-22 |  | Publish the contract fake library version for GET /admin/jobs, POST /admin/jobs/{jobId}/rerun and GET /data-products/freshness so the run report can pin it |

### OTHER:P2 Criteria and test data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00029 | RWB-ITG-AD018-ITG | DOR-RWB-ITG-AD018-ITG-7 | 11 | Read ACE views only through P1's contract (DP-05), never directly; section 11 already states this rule. |

### RWB-P1-AD018-APP; OTHER:message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00030 | RWB-ITG-AD018-ITG | GAP-0440 | 11 | Answer fields are Not specified (GAP-0440) until P1 publishes its schemas; then each field is asserted from the published contract. Owner: solution architect. |

### RWB-P1-AD018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00031 | RWB-ITG-AD018-ITG | GAP-0514 | 11 | Publish response fields of the job read, rerun answer and freshness answer by field ID: DF-OPS-224 to DF-OPS-232, DF-OPS-001 to DF-OPS-008, DF-ACE-178 to DF-ACE-186. |

### RWB-ITG-AD019-ITG; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00038 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-14 | find it | Record the signed sign-off of the epic design that covers this story. |

### OTHER:Contract fake library for rwb-source-data and rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00040 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-22 | 12.2 | Publish a fake library version covering the section 12.2 reads; the version is not specified in the sources. |

### OTHER:rwb-source-data and rwb-case published API contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00042 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-8 | 12.2, 12.3 | Publish the GET paths of sections 12.2 and 12.3 that detcheck found missing: the reconciliation read, the key-resolution read, and the rwb-case reconciliation-breaks and referential-completeness reads. |

### RWB-P1-AD019-APP; RWB-P3-AD019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00046 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-7 | 11 | Section 11 already routes ACE views behind the P1 read; no change needed here. |

### RWB-P3-AD019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00047 | RWB-ITG-AD019-ITG | DOR-RWB-ITG-AD019-ITG-9 | 14 | Align MSG-P1-012 and MSG-P1-001 text with Error and Message Standard v4 |

### OTHER:rwb-source-data and rwb-case service contracts; OTHER:gateway-bff contract (SCR-45 route) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00048 | RWB-ITG-AD019-ITG | GAP-0441 | 7 | Publish reconciliation, key-resolution and freshness reads with paths, paging and shapes; SCR-45 route with merge rules and per-call timeout; refresh cadence as platform configuration; problem response for unreachable P1 read |

### OTHER:TSD P1 v3 (API-P1-003) and the P1 service contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00049 | RWB-ITG-AD019-ITG | GAP-0519 | 11 | Publish response fields, paging and break-row shape of GET /admin/reconciliation/results, answered from reconciliation_result DF-OPS-118 to DF-OPS-129 plus REC-05 orphan rows |

### RWB-P1-AD019-APP; RWB-P1-AD019-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00050 | RWB-ITG-AD019-ITG | GAP-0520 | 8 | BR9 now states that JOB-04 is event-started in rwb-source-data and runs no Schedule for the console. The DP-10 rows are in the Work Package. |

### OTHER:rwb-case and rwb-source-data contracts; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00051 | RWB-ITG-AD019-ITG | GAP-0728 | 8 | Publish three console reads under rwb-case; name rwb-case login with ACE DB owners; add GET reconciliation, key-resolution and freshness ops with business date query and paged answer to rwb-source-data; fix SCR-45 route |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations sheet) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00052 | RWB-ITG-AD019-ITG | GAP-0268 | find it | Add an Owner column to Reconciliations for REC-01 to REC-08, naming the Ownership Map service that holds the Workbench side; that service answers on its contract, one hop, 2 s timeout; rwb-source-data keeps the ACE side and JOB-04. |

### OTHER:Recovery Workbench reconciliation workbook v3 (Reconciliations and Quality measures sheets) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00053 | RWB-ITG-AD019-ITG | GAP-0269 | find it | Append Owner and Per-service reconciliation columns to Reconciliations and an Owner service column to Quality measures; take each value from the Ownership Map sheet Tables and name the service and its schema. |

### OTHER:Recovery Workbench reconciliation workbook v3 (new sheet Per-service reconciliation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00054 | RWB-ITG-AD019-ITG | GAP-0271 | find it | Add a Per-service reconciliation sheet with one row per service of the 19: its tables, its part of each check, key, tolerance, cadence, break and result route, pattern and basis; use the Template and Rules R9 placeholder where the source gives none. |

### OTHER:Contract fake library (StubSet source) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00057 | RWB-ITG-AD022-ITG | DOR-RWB-ITG-AD022-ITG-22 | 13 | Publish the contract fake library version for the S9 and P4 contracts and record that version as published. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; RWB-P4-E1022-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00061 | RWB-ITG-AD022-ITG | GAP-3104 | 3 | Publish the rwb-access operation names for the consumed row and map EV-20 and EV-21 to their names in the Event and Messaging Design. |

### RWB-S9-AD022-CON; RWB-P4-E1022-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00062 | RWB-ITG-AD022-ITG | GAP-0442 | 3 | Fix the portal route, the firm-scope field name and the refusal-or-ignore rule in the S9 CON story; pin the partner session and MFA assertion shape in the P4 session contract. |

### RWB-S9-AD022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00063 | RWB-ITG-AD022-ITG | GAP-3103 | 3 | Publish partner_user fields in TSD S9 T3.1 and the PRD, name the contract-end Schedule and its clock, decide whether a recall is announced by an event, and confirm the feature the requirement rows serve. |

### OTHER:RWB-DM-003 legacy story (P1 slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00073 | RWB-ITG-DM003-ITG | GAP-0521 | 1 | Move the load of AC1 and AC3 to rwb-case; P1 produces the cutover extract and business-key mapping only and writes no other service's schema. |

### OTHER:RWB-DM-003 legacy story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00074 | RWB-ITG-DM003-ITG | GAP-0522 | 1 | Read the legacy extract once through the cutover run, land nothing in rwb_source_data, and record sign-off in the release pipeline cutover record with reconciliation results as evidence. |

### OTHER:Recovery Workbench migration story set v3 (section 1 How column and section 3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00076 | RWB-ITG-DM003-ITG | GAP-0237 | 1 | Replace the Workbench load with the owner's Flyway step in the owner's schema, run by the owner migrator login from RWB-PLT-N011-DB; P1 never writes another schema. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00077 | RWB-ITG-DM003-ITG | GAP-0241 |  | Story has no retention rule for the legacy tables; retention class and owner belong in the Ownership Map. Retention period not specified in the source documents. |

### OTHER:Contract story of the providing services (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00083 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-21 | header | Contract dependencies row shows the not-specified placeholder. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00084 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-22 | header | Publish the contract fake library version through RWB-ITG-DM004-CON and record it as published |

### OTHER:Contract of the providing services (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00085 | RWB-ITG-DM004-ITG | DOR-RWB-ITG-DM004-ITG-23 | header | Contract version row added with the not-specified placeholder. |

### OTHER:Recovery Workbench story set (contract story for this slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00096 | RWB-ITG-DM005-ITG | DOR-RWB-ITG-DM005-ITG-21 | header | Header states the contract story is not yet in the story set. The contract story must be created in the story set and then named in the header. |

### OTHER:Contract fake library register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00097 | RWB-ITG-DM005-ITG | DOR-RWB-ITG-DM005-ITG-22 | header | Publish a contract fake library version for RWB-ITG-DM005-CON and record it as published. |

### OTHER:23 Document Gaps/Recovery Workbench Assumptions Register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00101 | RWB-ITG-DM005-ITG | DOR-RWB-ITG-DM005-ITG-18 | 11 | Add an assumption for open decision DL29 on RWB-ITG-DM005-ITG (ID from step D1), using the Program BRD v5 section 9 interim answer; check it against the story's twelve months of EFS history. |

### OTHER:P1 DB story for the interaction table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00103 | RWB-ITG-DM005-ITG | GAP-0527 | 11 | Confirm person_key and contact_key as the two business-key columns of interaction when aligning the table with TSD P3 v3 T3.1; no party_id or contact_point_id is invented. |

### OTHER:Provider contract (CON) story in the story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00109 | RWB-ITG-DM006-ITG | DOR-RWB-ITG-DM006-ITG-21 | header | Contract dependencies reads Not specified in the source documents (DOR-RWB-ITG-DM006-ITG-21). |

### OTHER:Provider fake libraries of rwb-source-data, rwb-access, rwb-asset and rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00110 | RWB-ITG-DM006-ITG | DOR-RWB-ITG-DM006-ITG-22 | 12.8 | No published fake library version is recorded in the sources; the providers must publish their fakes before the story can name the versions. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00114 | RWB-ITG-DM006-ITG | DOR-RWB-ITG-DM006-ITG-18 | 18 | Record DL25 as decided with recommended option A (zero; any difference holds the publish) under the programme directive of 26 November 2026. |

### RWB-P1-DM007-APP; OTHER:API-P1-003; OTHER:API-P1-010) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00121 | RWB-ITG-DM007-ITG | GAP-2170 | find it | Add the one-dump read, one package per owner per cut-over business date to S4, P6 and S9, the ten-day count on reconciliation_result rows with reset on break, the cut-over record with sign-off, the flag defaulting off, and API-P1-003 for the out-of-scope tracker and exception rows. |

### OTHER:Release pipeline runbook entry and Flyway version description (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00122 | RWB-ITG-DM007-ITG | GAP-2171 | find it | Record the cutover record, dump interface, clean-day rule and DM007 instruction slice agreed at the cutover rehearsal, with values kept in the values file. |

### OTHER:Release pipeline runbook and Flyway version description for the RWB-DM-008 cutover (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00131 | RWB-ITG-DM008-ITG | GAP-2171 |  | Record the cutover record, dump interface, clean-day rule and DM007 instruction slice agreed at the cutover rehearsal; keep their values in the values file, not in code. |

### OTHER:Functional Specification P1 v3; OTHER:DP08 row of the data product catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00132 | RWB-ITG-DM008-ITG | GAP-2172 |  | Restate the DP08 row with rwb-partner as owner of partner, partner_user and partner_instruction, a pointer to the S9 contract, and the closed handover field list. |

### OTHER:Provider contract fake libraries (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00136 | RWB-ITG-DM009-ITG | DOR-RWB-ITG-DM009-ITG-22 | 12.8 | 12.8 states the fake library version is not specified and not recorded as published; publication is provider-side. |

### RWB-ITG-DM010-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00145 | RWB-ITG-DM010-ITG | DOR-RWB-ITG-DM010-ITG-22 |  | Publish the contract fake library for RWB-ITG-DM010-CON and record its published version |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-valuation.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00149 | RWB-ITG-DM011-ITG | CG-ALL-1044 | 12.2 | Publish GET /api/recovery/valuation/v1/cases/{caseId}/valuation through the provider's CON story, or have the consumer use a published operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-valuation.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00153 | RWB-ITG-DM011-ITG | DOR-RWB-ITG-DM011-ITG-8 | Header | Publish GET /api/recovery/valuation/v1/cases/{caseId}/valuation and POST /api/recovery/access/v1/authorise through the provider CON stories. |

### OTHER:04 User stories/Recovery Workbench Data Migration Stories v3.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00156 | RWB-ITG-DM011-ITG | GAP-0239 |  | Name the expected-return and sale-estimate records in the RWB-DM-011 Data table as held in the rwb_valuation route-decision output (S1); case_list_row and measure_snapshot stay with P1 and P9. |

### OTHER:Screen Specifications v1; OTHER:SCR-45 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00177 | RWB-ITG-DM013-ITG | CG-ALL-1069 | 15 | This story does not build or change SCR-45. Its states belong to Screen Specifications v1. Section 15 points there; empty, error and no-access are Not specified. |

### OTHER:Story backlog (contract story for this epic) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01984 | RWB-ITG-E6008-ITG | DOR-RWB-ITG-E6008-ITG-21 | header | Contract dependencies row reads Not specified in the source documents. |

### OTHER:FSD S6 (A2.1 to A2.16; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:37; OTHER:45 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01986 | RWB-ITG-E6008-ITG | GAP-1770 | 12.2 | Carry v_ace_score.*, v_ace_account.*, v_ace_batch_status.* as contract field names from rwb-source-data; confirm the read path with P1 before wave 3 system test |

### OTHER:Recovery Workbench P3 screen specification (SCR-25; OTHER:SCR-26) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01988 | RWB-ITG-E6008-ITG | DOR-RWB-ITG-E6008-ITG-10 | 15 | Story names SCR-25 and SCR-26 only to say it neither builds nor reads them; their states belong to the P3 screen specification. |

### RWB-S6-E6008-APP; OTHER:C; OTHER:I; OTHER:X and the consumed-contract rows) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01991 | RWB-ITG-E6008-ITG | GAP-3006 |  | Keep the H, C, I and X rows; record the four reads and the interface call as class C with placeholders; carry posting result, item reference and rejection code in the decision record and case state with no new column; run posting and re-post under the service identity; RW-CREDITAD works the R-DS-32 exception task; month-end close as a durable timer of DebtSaleWorkflow with no Schedule; adopt REQ-S6-008; rejected-posting message text as the proposed fix states. |

### RWB-S6-E6008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01992 | RWB-ITG-E6008-ITG | GAP-3007 |  | Publish the baseline with placeholders and the two absence records; confirm the four operation names and interface values with owners before the tag; keep item-type names as baseline names until rwb-integration's interface row is published; bind each error condition to one section 14 message id; record the tag date in the contract README. |

### OTHER:Recovery Workbench P3 screen specification (SCR-25) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01993 | RWB-ITG-E6008-ITG | CG-ALL-1076 | 15 | Story records SCR-25 empty, loading, error and no access as Not specified; the states belong to the P3 screen specification. |

### OTHER:Recovery Workbench P3 screen specification (SCR-26) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-01994 | RWB-ITG-E6008-ITG | CG-ALL-1077 | 15 | Story records SCR-26 empty, loading, error and no access as Not specified; the states belong to the P3 screen specification. |

### RWB-P3-E6017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02002 | RWB-ITG-E6017-ITG | DOR-RWB-ITG-E6017-ITG-10 | none (P3 story) | Add empty, loading, error and no-access states for screen SCR-27 (P3 SCR-27). This story owns no screen and sets no states. |

### RWB-S7-E6017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02006 | RWB-ITG-E6017-ITG | GAP-3025 |  | Add rows for the five consumed contracts, the DP-04 Drools kit and DP-09 event library as tracked dependencies, the meeting calendar, the no-operation declaration and the routing requirement row. |

### OTHER:Contract registry (contract fake library) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02009 | RWB-ITG-E6021-ITG | DOR-RWB-ITG-E6021-ITG-22 | 12.8 | Publish and record the contract-fake library version generated from each pinned contract of section 12.2, so the pinned fake version has a published record (DOR-RWB-ITG-E6021-ITG-22). |

### OTHER:Screen specification that defines SCR-27 (P3 case screens) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02012 | RWB-ITG-E6021-ITG | DOR-RWB-ITG-E6021-ITG-10 | find it | Add empty, loading, error and no-access states for SCR-27 |

### RWB-S7-E6021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02014 | RWB-ITG-E6021-ITG | GAP-3033 | 8 | Record the four consumed rows as class C without changing the H row; add REQ-S7-002 and REQ-S7-005 to traceability of both stories at D1 |

### RWB-S7-E6021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-02015 | RWB-ITG-E6021-ITG | GAP-3034 | 12 | Publish the baseline with the four consumed rows and placeholders, the state enumeration with unprinted values marked, decision_log_id as local record identifier, and the prepared-posting-pack schema |

### 04 User stories/Recovery Workbench Data Migration Stories v3.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20593 | RWB-ITG-DM003-ITG | R-21801 |  | v3 has no How column or sections 1/3 and no Flyway or owner-login text. Loading identity belongs to the legacy migration set. Checked the v3.md mirror; docview not run. |

### 04 User stories/Recovery Workbench Data Migration Stories v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20598 | RWB-ITG-DM011-ITG | R-28411 |  | The legacy RWB-DM-011 Data table is in another document (Data Migration Stories v3 target). This file needs no story edit for the rwb_valuation records. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0236 | The owner-side migration step has no story ID | TechX | Resolved (directive) |
| GAP-0237 | Version 3 has the Workbench run the load; the target makes the schema owner run it | TechX | Resolved (directive) |
| GAP-0239 | The expected-return and sale-estimate records have no table and no schema | Data architecture team | Resolved (directive) |
| GAP-0240 | All 14 migration stories are wave 4 while nine services are wave 1 | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0241 | No retention period and no owner for the legacy Workbench tables after cutover | Data steward | Resolved (directive) |
| GAP-0242 | The custody of migrated document originals is not assigned | TechX | Resolved (directive) |
| GAP-0243 | The target table of the open promises and contact notes is not named | Data architecture team | Resolved (directive) |
| GAP-0268 | The nine reconciliations name one Workbench side, but that side sits in seven service schemas | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0269 | No reconciliation and no quality measure carries an owner | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0271 | No per-service reconciliation rule, cadence or result route | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0438 | Queue file layout, cap values, valid-from parameter, queue-load approval route, overflow-refusal message ID and the publication and read surface of the P3 reference-load and queue reads and the P7 approval are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0439 | RWB-AD-015: the service-level file and its warning layout, the valid-from parameter name, the approval route, the exact timer projection fields, the refusal message ID and the running-timer recompute rule are not published | Solution architect | Resolved (directive) |
| GAP-0440 | The job read, the rerun answer, the job-log fields, the freshness answer, the v_ace_batch_status read path and the two refusal messages of the interface and job monitor are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0441 | The data quality console read shapes, the gateway-bff route specification, the refresh cadence and the unreachable-read message are not stated in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0442 | Partner portal route, firm-scope resolution and partner session are not specified by any source read | Solution architect | Resolved (directive) |
| GAP-0443 | The cutover reconciliation harness pack for case and ownership is not specified | Integration lead | Resolved (directive) |
| GAP-0444 | The cutover reconciliation harness pack for treatment and offers is not specified | Integration lead | Resolved (directive) |
| GAP-0445 | The cutover reconciliation harness pack for contact and promises is not specified | Integration lead | Resolved (directive) |
| GAP-0446 | The cutover reconciliation harness pack for collateral and assets is not specified | Integration lead | Resolved (directive) |
| GAP-0447 | The cutover reconciliation harness pack for legal events and cases is not specified | Integration lead | Resolved (directive) |
| GAP-0448 | Wave 4 partner performance harness environment, fixtures, break-list fields and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0449 | The cutover reconciliation harness pack for debt sale is not specified | Integration lead | Resolved (directive) |
| GAP-0450 | The cutover reconciliation harness pack for documents and extracted fields is not specified | Integration lead | Resolved (directive) |
| GAP-0451 | The cutover reconciliation harness pack for scores and route economics is not specified | Integration lead | Resolved (directive) |
| GAP-0452 | The cutover reconciliation harness pack for the migrated decision log is not specified | Integration lead | Resolved (directive) |
| GAP-0453 | The wave 4 cutover reconciliation harness pack for money and closure is not specified | Integration lead | Resolved (directive) |
| GAP-0454 | The derecognition and general ledger posting harness pack for the debt sale journey is not specified | Integration lead | Resolved (directive) |
| GAP-0455 | The committee routing harness pack, the committee queue code and the committee meeting calendar are not specified | Integration lead | Resolved (directive) |
| GAP-0456 | The write-off posting harness pack, the ALS and general ledger answer and the posting reference format are not specified | Integration lead | Resolved (directive) |
| GAP-0514 | The response shapes of the job read, the rerun answer and the freshness answer are not specified | Tech lead | Resolved (directive) |
| GAP-0515 | job_catalog is P2 rwb-integration while the job read is P1 rwb-source-data | Solution architect | Resolved (directive) |
| GAP-0516 | SCR-44 is a gateway-bff route on a P1 story that builds no screen | DevOps lead | Resolved (directive) |
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
| GAP-0542 | decision_log_entry is P7's and the target writes a local decision record plus the shared topic, while no source says whether the migrated legacy entries are published as records or handed over as a file, or who continues the hash chain | Solution architect | Resolved (directive) |
| GAP-0543 | proceeds is P8's, write_off is S7's and the closure sits on the case (P3) while the legacy money and closure migration is a single P1 slice, and no source says who loads each and what survives of the matching state | Solution architect | Resolved (directive) |
| GAP-0728 | RWB-AD-019 in rwb-case: login name, edge composite route, source-data read shape and contract placement not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0738 | The committee routing of RWB-E6-017 crosses two services with no operation, no committee queue code, no meeting timer type and no requirement ID in the sources | Solution architect | Resolved (directive) |
| GAP-0856 | rwb-access queue-load gate: API Specification v4 declares no rwb-access path for the queue load, the approval or the read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0857 | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Business analyst, P4 | Resolved (directive) |
| GAP-0858 | rwb-access queue load: the queue file layout is not specified, and the legacy file's member sheet is a P3 table | Reference data administrator | Resolved (directive) |
| GAP-0860 | rwb-access queue load: the assignment-method list LOV-ASSIGN is declared in the P3 specification and absent from the P4 specification the gate is written from | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0861 | rwb-access queue load: the required answer carries a version label and a state the owner's load schema does not return, and the load decision code is not specified | Solution architect | Resolved (directive) |
| GAP-0862 | rwb-access queue load: legacy AC1 states an allocation outcome that this story does not own | Business analyst, P4 | Resolved (directive) |
| GAP-0863 | rwb-access queue load: the approval right is declared as Reference data A held by no role, as Rules and parameters A for RW-RISK, and as a per-table approver role | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0864 | rwb-access queue load contract: no source publishes the queue-row schema or the file layout the document must declare | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1770 | FSD S6 reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them and gives S6 no cell to P1 | Solution architect | Resolved (directive) |
| GAP-1779 | Derecognition and the general ledger posting have no interface and no clear owner | Solution architect | Resolved (directive) |
| GAP-1792 | The FSD reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1793 | The FSD posts to ALS and the general ledger from this module, while Architecture v5 gives the posting to rwb-payment | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1795 | Slide 20 names write-off collection operations that neither the Ownership Map nor the API specification holds | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1807 | The FSD has no wait for the ledger acknowledgement that strict mode requires before a posting | Solution architect | Resolved (directive) |
| GAP-1809 | The FSD defers the mirrored GL fields of write_off to DEF-05, which no source read here defines | Data architect | Resolved (directive) |
| GAP-2162 | RWB-AD-018: the job run record, the outbound-action answer and the right-enforcement path are not named in the target sources | P1 tech lead with the data architect and the P4 access owner | Resolved (directive) |
| GAP-2163 | RWB-AD-018: the contract baseline has no field-level detail for the run element and its boundary with the freshness resource is not written down | P1 tech lead with the solution architect | Resolved (directive) |
| GAP-2164 | RWB-AD-018: the alert thresholds, the panel baselines and the per-environment values of the monitor are not in the sources | DevOps team with the platform observability owner | Resolved (directive) |
| GAP-2167 | listing and asset_sale have no owning schema in the P1 table list | Data architect; S5 rwb-asset technical owner | Resolved (directive) |
| GAP-2169 | Migration batch states and cutover evidence format are not specified | Solution architect | Resolved (directive) |
| GAP-2170 | The legal cut-over of RWB-DM-007 has no defined dump, no package format, no evidence store and no agreed API surface in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2171 | No source fixes the cutover mechanics of RWB-DM-008: the extract dump, the pipeline step, the cutover record, the ten-day evidence and the DM007 instruction slice | Solution architect | Resolved (directive) |
| GAP-2172 | The DP08 catalog row and the Ownership Map disagree on which service owns the partner tables of RWB-DM-008 | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2173 | Cutover mechanics of the debt sale migration are not specified | Data steward (RW-DATASTEW), with tech delivery | Resolved (directive) |
| GAP-2175 | The route code and state sit on the case (P3) and the baseline snapshots with rwb-reporting (P9) while only case_list_row is P1's, and no source gives the legacy dump's source or format, the handover locations, the retention period of the legacy tables or where the data steward's sign-off is held | Solution architect | Resolved (directive) |
| GAP-2176 | decision_log_entry is P7's, the record is local and the ledger is central, and no source says whether the migrated legacy entries are published as records or handed over as a file, nor who continues the hash chain | Solution architect | Resolved (directive) |
| GAP-2178 | RWB-DM-013 names three entities and a cutover step but no owner, source, format or sign-off place after the realignment | RW-DATASTEW | Resolved (directive) |
| GAP-2273 | The queue-file check surface, the last two queue columns, the member sheet, the cap limit key, the finding codes, the right of the load and the decision code are not specified in the sources | Solution architect | Resolved (directive) |
| GAP-2274 | The contract document of the queue-file check has no source schemas, no source finding codes and no source right for the approval | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2275 | Service-level load gate: the operations, the file columns, the effect list, the parameter rows and the SCR-42 panel split are not named for rwb-access | Solution architect, P4 and the P3 owner of the service-level and timer contract | Resolved (directive) |
| GAP-2276 | The right letters of the service-level load and approval differ between the legacy story and TSD P4 v3 | Solution architect, security administrator role, P4 | Resolved (directive) |
| GAP-2277 | The contract document of the access-side service-level load has no declared source for its paths, schemas and error bodies | Tech lead, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2533 | rwb-payment cutover load of RWB-DM-013: the handover file, the load command and its run record, a provenance column, the legacy payment_code column and the two schema-level H rows are fixed by no single source, and this slice owns no legacy criterion | Data steward and solution architect of rwb-payment, with the rwb-source-data owner, the schema baseline owner and the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3006 | RWB-S6-E6008-APP: the derecognition and posting slice has no plan row for its four consumed contracts and its interface call, no posting column, no published operation names and no requirement id | Solution architect | Resolved (directive) |
| GAP-3007 | RWB-S6-E6008-CON: the contract baseline declares no operation and no answer property because TSD S6 T-A publishes no derecognition or posting surface and no column carries the result, and the four operation names and the interface values are unpublished | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3025 | RWB-S7-E6017-APP: the routing slice has no plan row for its five consumed contracts, its rule kit, its event library, its meeting calendar, the operation it provides or the requirement it serves | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3026 | RWB-S7-E6017-CON: the consumed operation names, the queue and deviation elements, the unprinted state values and the meeting-booking element have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3033 | RWB-S7-E6021-APP: the plan holds no C or X row for the four consumed contracts of the pack-prepared step, no dependency row for DP-05, no interface for the ALS and general-ledger crossing, and no separate story for the shared pack rule R-WO-05 | Solution architect with the rwb-writeoff tech lead, the rwb-source-data, rwb-case and rwb-decision owners and the wave 4 integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3034 | RWB-S7-E6021-CON: the consumed operation names, the ACE and ledger shapes, the unprinted state values, the prepared-posting-pack element and the ALS and general-ledger interface have no published baseline | Solution architect with the rwb-writeoff tech lead and the owners of rwb-source-data, rwb-case and rwb-decision | Resolved (directive) |
| GAP-3103 | RWB-S9-AD022-APP: the partner user catalogue, the date trigger, the recall event and the legacy predecessor are unstated | Business analyst, S9; solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3104 | RWB-S9-AD022-CON: no element for the partner user, no operation name for the rwb-access read, and no ID mapping for the two events | Solution architect; tech lead of rwb-partner | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-AD022-ITG | unknown story key | 24 | RWB-ITG-AD022-CON is not a story of the set: \| Contract dependencies \| RWB-ITG-AD022-CON (not built yet) \| |
