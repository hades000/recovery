# RWB-SVC-P3 rwb-case (Case and workflow) - review pack, part 6 of 12 (RWB-P3-E1055-APP to RWB-P3-E1073-INF)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 7 |
| Resolved in the stories | 131 |
| Cross-document (pending in another document) | 201 |
| Not applied (value not in the sources) | 22 |
| Open business decisions | 25 |
| Register gaps linked | 103 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P3-E1055-APP | 19 | 40 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1055 APP Proof of delivery capture design with WIN v2.md |
| RWB-P3-E1065-APP | 28 | 29 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1065 APP Sandbox database with synthetic recovery data v2.md |
| RWB-P3-E1066-APP | 15 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1066 APP Interaction ledger store and writer v2.md |
| RWB-P3-E1067-APP | 14 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1067 APP Every Workbench action into the interaction ledger v2.md |
| RWB-P3-E1073-APP | 24 | 37 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1073 APP Rule authoring, validation, test scenarios, approval and rollback in Drools v2.md |
| RWB-P3-E1073-CON | 23 | 25 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1073 CON Rule authoring, validation, test scenarios, approval and rollback in Drools - contract v2.md |
| RWB-P3-E1073-INF | 8 | 33 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P3 rwb-case (Case and workflow)/RWB P3 E1073 INF Rule authoring, validation, test scenarios, approval and rollback in Drools - infrastructure v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P3-E1055-APP | R-00803 | CG-ALL-3854 | Script gap | Product owner | The story adds NOTICE_PERIOD_DAYS to the closed list LOV-SEND-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-E1055-APP | R-00804 | CG-ALL-3855 | Script gap | Product owner | The story adds NOTICE_PERIOD_DAYS to the closed list LOV-TIMER | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-E1055-APP | R-00805 | CG-ALL-3856 | Script gap | Product owner | The story adds NOTICE_PERIOD_DAYS to the closed list LOV-TIMER-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-E1066-APP | R-00816 | CG-ALL-3892 | Script gap | Product owner | The story adds CONTACT_TRIED to the closed list LOV-LEDGER-EVENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P3-E1055-APP | R-10334 | CG-ALL-3869 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1066-APP | R-10339 | CG-ALL-3896 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1067-APP | R-10342 | CG-ALL-3903 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1073-APP | R-10349 | CG-ALL-3918 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P3-E1073-APP | R-10350 | CG-ALL-3925 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1055-ITG, RWB-ITG-E2034-ITG, RWB-P1-E1055-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P2-E2034-CON, RWB-P2-E2034-OPS, RWB-P3-E1055-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-S9-E2034-APP | R-22176 | GAP-3211 | Register gap | Product owner | Requirements with no PRD functional requirement | The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-22191 | GAP-2245 | Register gap | Legal and the business lead | Whether a deviation pauses a statutory notice period is not settled by the sources | Keep the notice period unpaused as ASM-B2-P3-016-3 records; if Legal rules that it pauses, the deviation contract gains one signal to the notice clock and one criterion changes. |
| RWB-ITG-E1066-ITG, RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1066-OPS, RWB-P3-E1066-APP | R-22263 | GAP-2253 | Register gap | rwb-case reference data owner and Compliance | LOV-LEDGER-EVENT carries 14 values in the TSD and 12 in the legacy story | Load the fourteen values of TSD P3 v3 T5.1 as the reference rows of LOV-LEDGER-EVENT, with PARTNER_RESULT and OFFER included and the Thai labels of DL10, and let RWB-P1-E1066-CON validate against the same list; the two extra values add no rule and remove none. |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS | R-28627 | GAP-2248 | Register gap | Business lead | The role that receives the expiry of a notice period is not named | Take the escalation role from the SERVICE_LEVEL row in force as ASM-B2-P3-016-6 records, and add a named default role for a missing row if the business lead asks for one. |
| RWB-ITG-E1073-ITG, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28681 | GAP-0006 | Register gap | RW-COE and RW-RISK | Rule format XLS decision tables or DMN 1.6 | Keep XLS tables for the Phase 1 packages and convert one table at a time, with both formats on the same runtime |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28693 | GAP-2047 | Register gap | Solution architect with Risk and Internal Audit | The decision log is now written locally by each service and sealed centrally | Version 4 measures the local decision record of each service and the central ledger of P7 rwb-decision as two instances of the same two alerts, with the chain check read per service and once for the ledger. |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28694 | GAP-2051 | Register gap | P7 rwb-decision with Compliance and Internal Audit | The hash chain check now spans 19 local chains and one central ledger | Version 4 raises the alert on the local chain of each service and once on the central ledger, and attributes a break to the service whose chain fails; the run book of RWB-E1-073 and RWB-E2-037 names the check. |
| RWB-P3-E1073-APP | R-33419 | ASM-ALL-3925 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-P3-E1055-APP | R-36325 | ASM-3701 | Register assumption |  | A NOTICE_PERIOD timer has no warning point: warn_at and warned_at stay null, no MSG-P3-003 is sent for this clock, and the only output of the clock before its expiry is the due date on the case read. | Business lead and Legal at the wave 1 refinement |
| RWB-P3-E1055-APP | R-36326 | ASM-3702 | Register assumption |  | The notice period is a legal clock: a deviation raised on the case pauses the SERVICE_LEVEL clock and leaves the NOTICE_PERIOD clock RUNNING with its started_at and expires_at unchanged, and the case record still shows the prescription date under MSG-P3-004. | Legal and the business lead |
| RWB-P3-E1055-APP | R-36329 | ASM-3705 | Register assumption |  | The expiry of a notice period is published as rwb.case.TimerBreached.v1 with escalateTo taken from the escalation role of the SERVICE_LEVEL row in force for the case's queue and status, and a case with no such row expires with the role of the row that last applied. | Business lead |
| RWB-P3-E1066-APP | R-36335 | ASM-3711 | Register assumption |  | LOV-LEDGER-EVENT is loaded with the fourteen values of TSD P3 v3 T5.1 — CONTACT, LETTER, PROMISE, PAYMENT, HANDOVER, CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED, DECISION_TAKEN, CORRECTION, PARTNER_RESULT, OFFER — with the Thai labels of DL10, and the two values the legacy story does not list are kept. | Reference data load of wave 1, with the rwb-case reference data owner and Compliance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P3-E1055-APP | R-05121 | DOR-RWB-P3-E1055-APP-14 | 13 | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off date in the story or sources (checked sections 3 and 13, DoR v4 extract table 3 row 3). Needs the epic design record. |
| RWB-P3-E1055-APP | R-05124 | DOR-RWB-P3-E1055-APP-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | No published contract fake library version in sections 3, 12.8, 12.9 or the DoR v4 extract. Value not in sources; needs the fake library publication record. |
| RWB-P3-E1055-APP | R-05125 | DOR-RWB-P3-E1055-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Sources state only the /v1 path for RWB-P6-E1055-CON, not a contract version (checked sections 3, 12 and DoR v4 extract). Placeholder written. |
| RWB-P3-E1055-APP | R-10325 | CG-ALL-3859 | 12.1 | HTTP errors with no message ID: 503 store down. The three reads are idempotent by nature and write nothing | Error and Message Standard v4 s.4 and s.14 hold no system-unavailable ID; MSG-GEN-006 queued-and-retried text does not fit these reads. Placeholder written. |
| RWB-P3-E1065-APP | R-24996 | CG-ALL-3886 | 3, 3.1 | Flyway file V1065_1__case_estate_seed.sql is not in the V0001..Vnnnn form | Next number of the rwb-case Flyway sequence is Not specified in the source documents (CG-ALL-3886); file name not in story text. Searched the source excerpts and found no sequence. |
| RWB-P3-E1067-APP | R-00820 | CG-ALL-3904 | 1 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | No package segment for 'case' in Service Template Specification v1 (05 Technical architecture); naming one would invent a value. Needs the Solution architect's ruling. |
| RWB-P3-E1067-APP | R-00821 | CG-ALL-3905 | 12.7 | Java package th.co.scb.ace.workbench.recovery.case.ledgerevents uses the reserved word 'case' | Same as CG-ALL-3904: no segment for the ledgerevents package in the sources (Service Template Specification v1 s3.1). Needs the Solution architect's ruling. |
| RWB-P3-E1067-APP | R-05144 | DOR-RWB-P3-E1067-APP-14 | Not specified in the source documents (DOR-RWB-P3-E1067-APP-14) | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off found in 03 Requirements and specifications (Epic design search returned no matches). Sign-off cannot be written without the record. |
| RWB-P3-E1073-APP | R-10344 | CG-ALL-3912 | Not in chunk | Rule R-ALLOC-014 is not in Business Rules v4 | The R-ALLOC-014 citation is outside this chunk. No Business Rules v4 rule ID is named in the sources, so none was chosen; choosing one is a BA decision. |
| RWB-P3-E1073-APP | R-16045 | DOR-RWB-P3-E1073-APP-11 | Not in chunk | Definition of Ready item 11 Guardrails: Partial | Personal-data classing of the P2 fields is not in this chunk or the sources checked. Sections 4 and 12.7 unchanged. |
| RWB-P3-E1073-APP | R-16047 | DOR-RWB-P3-E1073-APP-18 | Not in chunk | Definition of Ready item 18 Open decisions: Partial | DL24 appears only in Decision Log v11. Section 18 text is not in this chunk and no DL24 assumption text was found, so none written. |
| RWB-P3-E1073-APP | R-25010 | CG-ALL-3921 | 3 | Flyway file V1073_1__rule_version_index.sql is not in the V0001..Vnnnn form | Next free number of the rwb-case Flyway sequence is not in the chunk or sources (searched for V1073_1 and rwb-case migrations; no authoritative hit). Needs a value from the solution architect. |
| RWB-P3-E1073-APP | R-25011 | CG-ALL-3922 | 7 | Criteria and tests keep legacy job and decision-log wording | Section 12.5 has no JOB-nn or decision-log wording. The AC4 line and the TC-E1-073-04 row are in sections 7 and 16, outside this chunk, so they cannot be edited here. |
| RWB-P3-E1073-CON | R-10352 | CG-ALL-3928 | 12.8 | Rule R-ALLOC-014 is not in Business Rules v4 | R-ALLOC-014 sits in 12.8, not in the supplied story parts. No R-ALLOC-0nn rule found in the Business Rules v4 .md export, so no replacement rule can be cited. |
| RWB-P3-E1073-CON | R-16060 | DOR-RWB-P3-E1073-CON-8 | 8 | Definition of Ready item 8 Contract: Partial | Section 8 is not in the supplied story parts, so no exact old text exists to edit. Form to use: CaseWorkflow with workflow ID = case ID (Case and Workflow Model v6). |
| RWB-P3-E1073-CON | R-22291 | GAP-0701 | 5 | The KieBase cache sizing, the JVM heap and the storage of a local model artefact are not specified | No heap, request, limit or cache-bound value for rwb-case in the sources. Section 5 is not in the supplied parts. Needs load test and platform owner confirmation. |
| RWB-P3-E1073-CON | R-28687 | GAP-2031 | 5 | The effective-date job is a Quartz job owned by RW-COE in version 3 and a Temporal Schedule in rwb-decision in Architecture v5 | The effective-date step text is not in the supplied story parts, so no old text exists to edit. Directive fix: JOB-20 Temporal Schedule in rwb-decision (P7), publishing RulePackageInForce (EV-30). |
| RWB-P3-E1073-INF | R-05158 | DOR-RWB-P3-E1073-INF-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design or sign-off for E1073 is recorded in the sources; only slide 15 of the Temporal and Drools design is cited. Sign-off cannot be confirmed. |
| RWB-P3-E1073-INF | R-05159 | DOR-RWB-P3-E1073-INF-16 | header | Definition of Ready item 16 Size: Fail | No source gives a size, so the item cannot be resolved in this story. |
| RWB-P3-E1073-INF | R-16064 | DOR-RWB-P3-E1073-INF-4 | 8 | Definition of Ready item 4 Business rules: Partial | Needs AC rows in section 7 and test rows in section 16 for BR9 and BR10. Neither section is in this chunk, and the story file could not be located to read them. |
| RWB-P3-E1073-INF | R-22089 | GAP-2414 | find it | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Four published contracts are cited but only two are named. The other two are not in the sources read here. |
| RWB-P3-E1073-INF | R-30633 | NEWAC-RWB-P3-E1073-INF-AC7 | 8 | AC7: §8 BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 belongs in section 7 and its test row in section 16, neither in this chunk. The proposed test is Not specified in the source documents (NEWAC-RWB-P3-E1073-INF-AC7). |

## 5. Cross-document changes (pending in the target document)


### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06184 | RWB-P3-E1055-APP | CG-ALL-3857 | 13 | Add to the Fields sheet, entity timer, the nullable varchar(40) notice-reference field the story writes and indexes (`reference_ref`), with its DF-WRK field ID, so `ux_timer_notice_running ON timer (case_id, reference_ref)` rests on an LDM v9 field. |
| CDC-06189 | RWB-P3-E1055-APP | DOR-RWB-P3-E1055-APP-7 | 11 | Add field reference_ref to entity timer in LDM v9, or name the existing LDM v9 timer field that carries the notice reference of the clock. |
| CDC-06244 | RWB-P3-E1065-APP | GAP-2251 |  | Confirm field identifiers of queue, queue_member, assignment, task, timer, case_entry_exclusion and reference_version; rwb-case login set at RWB-PLT-NF06-DB. |
| CDC-06261 | RWB-P3-E1066-APP | DOR-RWB-P3-E1066-APP-7 | 11 | Record interaction_link as a technical table of rwb_case with no BR Field ID, or add it under a dictionary name. |
| CDC-06309 | RWB-P3-E1073-APP | GAP-2457 |  | Define physical columns, types and nullability of rule_package, rule_package_version, rule_row and rule_test_case from legacy field names DF-REF-274 to DF-REF-299. |
| CDC-06315 | RWB-P3-E1073-APP | GAP-0205 |  | Add rule_package and rule_package_version as entities of P7 in the next LDM version; rename no row of v6. Resolve entity Rule to rule_row with owner P7. |
| CDC-06335 | RWB-P3-E1073-CON | GAP-2457 | find it | Add physical columns, types and nullability for rule_package, rule_package_version, rule_row and rule_test_case on the legacy field names; confirm artifact columns with RWB-PLT-E1072-CON. |
| CDC-06366 | RWB-P3-E1073-INF | GAP-2457 | n/a | Take column names, types and nullability for rule_package, rule_package_version, rule_row and rule_test_case from the LDM; confirm artifact columns with RWB-PLT-E1072-CON. |
| CDC-06373 | RWB-P3-E1073-INF | GAP-0205 | find it | Add rule_package and rule_package_version as entities of P7 in the next version; keep rule_row named 'Rule' and rename no row of v6. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06217 | RWB-P3-E1055-APP | CG-ALL-3868 | 18 | Align the test lists of the requirements that differ, including REQ-OCC-003 and REQ-ILG-004, with RWB-P3-E1055-APP section 18 at the next RTM version. |
| CDC-06245 | RWB-P3-E1065-APP | CG-ALL-3883 | 18 | Align the REQ-RDF-001 test list with section 18 of RWB-P3-E1065-APP in the next version of both |
| CDC-06259 | RWB-P3-E1066-APP | DOR-RWB-P3-E1066-APP-12 | 12.7, 16, 18 | Align REQ-ILG-001 test cases with section 18 of RWB-P3-E1066-APP, which now includes TC-E1-066-10 (boundary of 12.7 tables). |
| CDC-06267 | RWB-P3-E1066-APP | CG-ALL-3895 | 18 | Align the RTM v7 test lists for REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008 with section 18 of RWB-P3-E1066-APP in the next RTM version. |
| CDC-06283 | RWB-P3-E1067-APP | CG-ALL-3902 | 18 | Align the RTM test lists of REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007 with section 18 of RWB-P3-E1067-APP. |
| CDC-06295 | RWB-P3-E1073-APP | DOR-RWB-P3-E1073-APP-12 | 12, 12.7, 16, 18 | Added TC-E1-073-21 to -25 to section 16, covering AC16 to AC20 |
| CDC-06312 | RWB-P3-E1073-APP | CG-ALL-3917 | 18 | Align the differing test lists for REQ-CWC-013 and the other requirements to section 18 of RWB-P3-E1073-APP in the next version. |
| CDC-06339 | RWB-P3-E1073-CON | CG-ALL-3931 | 18 | Align the test lists of the four requirements with section 18 of RWB-P3-E1073-CON. |
| CDC-06370 | RWB-P3-E1073-INF | CG-ALL-3935 | 18 | Align the test lists for the four differing requirements, including REQ-CWC-013, with section 18 of this story in the next RTM version. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06186 | RWB-P3-E1055-APP | CG-ALL-3870 | 1, 13 | The P3 row (L371) must record the package segment the solution architect rules for rwb-case in place of the Java reserved word `case`, so the package compiles; section 1 and section 13 of the story then copy that segment. |
| CDC-06187 | RWB-P3-E1055-APP | CG-ALL-3871 | 13 | The same P3 row (L371) segment rules the parent package, so `th.co.scb.ace.workbench.recovery.<segment>.noticeperiod` follows from it; section 13 Package of the story copies it. |
| CDC-06227 | RWB-P3-E1065-APP | CG-ALL-3884 | none | Rule the Java package segment for rwb-case that replaces the reserved word 'case' in th.co.scb.ace.workbench.recovery.case; the story then copies that name. |
| CDC-06228 | RWB-P3-E1065-APP | CG-ALL-3885 | none | Rule the Java package segment for rwb-case that replaces the reserved word 'case' in th.co.scb.ace.workbench.recovery.case.sandboxseed; the story then copies that name. |
| CDC-06249 | RWB-P3-E1065-APP | GAP-0897 |  | Publish the DEV-only read-only role and its grant list (SELECT on role and permission only, no access-entry read); record retirement of the single-schema grant with DP-15; fix the rwb-access login in the platform DB story. |
| CDC-06251 | RWB-P3-E1065-APP | GAP-1052 |  | Fix the synthetic file naming pattern next to the sandbox file properties and state that file content derives from the seed value, case ID and document type so the hash is stable. |
| CDC-06288 | RWB-P3-E1073-APP | CG-ALL-3919 |  | Architecture to rule a Java package segment for rwb-case that is not a reserved word, replacing 'case' in th.co.scb.ace.workbench.recovery.case (P3 row; same package in Service Catalog v1 and Service Contract Catalog v1). Then the story copies it. |
| CDC-06289 | RWB-P3-E1073-APP | CG-ALL-3920 |  | Architecture to rule a Java package segment for rwb-case that is not a reserved word, replacing 'case' in th.co.scb.ace.workbench.recovery.case.rules. Then the story copies it. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06212 | RWB-P3-E1055-APP | GAP-1101 | 12 | Record that rwb-comms computes the barcode break on its notice rows and publishes it, and that rwb-source-data owns the References list and the data-quality read. |
| CDC-06294 | RWB-P3-E1073-APP | GAP-1329 | 13 | Adopt the /admin/rule-versions family for the registry in both; restate RWB-ITG-E1073-ITG and the contract story on it; publish GET /rule-catalog as owned or remove it from the consumed set. |
| CDC-06301 | RWB-P3-E1073-APP | GAP-0700 | 12.2 | Add rows for the seven rwb-decision operations (load, version list, approve, rollback, dry run, model read, catalog read) under P7 with rights, answer shapes, error codes and field-level types. |
| CDC-06325 | RWB-P3-E1073-CON | GAP-1329 | find it | Use the /admin/rule-versions family for the registry in both; publish GET /rule-catalog as an owned operation or remove it from the consumed set; then restate this story on that family. |
| CDC-06329 | RWB-P3-E1073-CON | GAP-0700 | n/a | Add rows for the seven rwb-decision operations (load, version list, approve, rollback, dry run, model read, catalog read) with rights, answers, error codes and field shapes. |
| CDC-06356 | RWB-P3-E1073-INF | GAP-0383 | find it | Assign package code and version label to rwb-comms and rwb-integration; add GET /rule-models/{packageCode}/{versionLabel} with checksum under P7; publish refused load as MSG-P3-027 with its {check} values. |
| CDC-06358 | RWB-P3-E1073-INF | GAP-0700 | find it | Add P7 rows for the five authoring operations and the model and catalog reads, with rights, answers, error codes and field shapes. |

### RWB-P1-E1065-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06231 | RWB-P3-E1065-APP | DOR-RWB-P3-E1065-APP-22 | Header | Publish the contract fake library and record its version; the story then cites that version. |
| CDC-06235 | RWB-P3-E1065-APP | GAP-0384 | find it | Name the harness repository, environment, namespace, pipeline stage, tooling, fixture composition, reset, report format and all-green gate, and pin the stub set per build, agreed by QA lead, integration lead and DevOps. |
| CDC-06241 | RWB-P3-E1065-APP | GAP-0374 |  | Map the 92 tables to the 19 rwb_* schemas, state the baseline order and per-schema seed counts summing to 2,812 (seed 20261128), and keep one rwb_sandbox database. |
| CDC-06242 | RWB-P3-E1065-APP | GAP-0501 |  | One DEV sandbox database per service release (rwb_sandbox for rwb-source-data); the generator is a separate build module not in the service artefact. |
| CDC-06243 | RWB-P3-E1065-APP | GAP-0502 |  | Publish the stage interface with its input and output profile, the four fixtures (full, empty, refused, timeout) and drift detection as a build failure. |
| CDC-06246 | RWB-P3-E1065-APP | GAP-1051 | 3 | Publish the per-case synthetic document count and version depth as seed parameters, shared with RWB-P5-E1025-APP so a change is a parameter, not a code release. |
| CDC-06248 | RWB-P3-E1065-APP | GAP-1054 | 3 | Fix held intake item count per exception shape and pages per held item as seed parameters; name the review reasons the DEV queue must show in the RWB-P5-E1049-APP test data section. |

### RWB-P3-E1073-CON (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06292 | RWB-P3-E1073-APP | DOR-RWB-P3-E1073-APP-21 | header | Complete the build and publish the contract; the story currently shows build status Not started. |
| CDC-06293 | RWB-P3-E1073-APP | DOR-RWB-P3-E1073-APP-22 | header | Publish a contract fake library version from RWB-P3-E1073-CON and record its version. |
| CDC-06306 | RWB-P3-E1073-APP | GAP-2458 | 12.2 | Add the paged open-case fact read (filtered by status, paged) to the rwb-case contract and API Specification; the dry run uses it under RWB-P3-E1073-CON with a 2 s one-hop timeout. |
| CDC-06349 | RWB-P3-E1073-INF | DOR-RWB-P3-E1073-INF-21 | find it | Publish the contract and set its build status from Not started to Done. |
| CDC-06350 | RWB-P3-E1073-INF | DOR-RWB-P3-E1073-INF-22 | find it | Record the published fake library version. |
| CDC-06355 | RWB-P3-E1073-INF | GAP-1330 | find it | State whether it publishes the case reads its consumers need, or move this story's contract dependency to the P3 story that does. |
| CDC-06363 | RWB-P3-E1073-INF | GAP-2458 | n/a | Add a paged open-case fact read filtered by status, with the product group, queue, region, exposure band and deviation flag, under the 2 s one-hop timeout. |

### RWB-P1-E1066-CON (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06205 | RWB-P3-E1055-APP | GAP-1097 |  | Add pod records, freshness and batch-status elements with business date, feed version, batch status and stale marker. Until then consume DP07 records and freshness GETs, 2 s budget. |
| CDC-06208 | RWB-P3-E1055-APP | GAP-0577 |  | Publish GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= with the ten-field record, ascending pod_key order, paging and error set; align the consumed row in RWB-P6-E1055-CON section 12.2. |
| CDC-06256 | RWB-P3-E1066-APP | DOR-RWB-P3-E1066-APP-22 | 12.8 | Publish the rwb-source-data contract fake under RWB-P1-E1066-CON and record its library version as published. |
| CDC-06263 | RWB-P3-E1066-APP | GAP-0375 | 12 | Publish the append as POST /api/recovery/source-data/v1/cases/{caseId}/interactions with Idempotency-Key. Answers: 201 with entry ID and case_seq; 200 or 409 on a repeated key with the first entry; 422 MSG-GEN-001; 503 MSG-P1-022 when the write fails. Caller is a saga step that treats any non-2xx as a failed action. |
| CDC-06264 | RWB-P3-E1066-APP | GAP-0504 | 12 | Publish the append as POST /interactions on the rwb-source-data base. Answer 403 without Case record C; 404 for an unknown or out-of-scope case with MSG-P4-003; 409 for a reused Idempotency-Key with a different body. |
| CDC-06265 | RWB-P3-E1066-APP | GAP-0505 | 12 | Fix the ledger path as /interactions on the rwb-source-data base. Name the login as the rwb_source_data login. Take property names from the API specification and settle required flags at the baseline review. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06196 | RWB-P3-E1055-APP | CG-ALL-3867 | 16 | Add rows TC-E1-055-13 to TC-E1-055-16 with Given, When and Then from the criteria they cover (AC4, BR3, BR9; AC5, BR4; AC3, BR5; AC8, BR10). Also add TC-E1-055-17. |
| CDC-06229 | RWB-P3-E1065-APP | DOR-RWB-P3-E1065-APP-12 | 16 | Add TC-P3-E1065-01 and TC-E1-065-11 to -14 to tab Story test cases; align Traceability section 18 test lists with RTM v7. |
| CDC-06233 | RWB-P3-E1065-APP | CG-ALL-3880 | 16 | Add row TC-P3-E1065-01 covering AC9 and BR1, with Given, When and Then copied from AC9 of RWB-P3-E1065-APP section 7. |
| CDC-06338 | RWB-P3-E1073-CON | CG-ALL-3930 | 16 | Add rows for TC-P3-E1073-CON-01 to TC-P3-E1073-CON-08 with Given, When and Then copied from the criterion each covers. |
| CDC-06369 | RWB-P3-E1073-INF | CG-ALL-3934 | 16 | Add story test case rows TC-P3-E1073-INF-01 to TC-P3-E1073-INF-06 to Story test cases, with Given, When and Then copied from the criterion each row covers. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06199 | RWB-P3-E1055-APP | GAP-1597 |  | Confirm that the notice record and its proof fields stay in rwb-comms, that proof rows are read through the rwb-source-data contract, and that the ACE team confirms which system writes v_ace_pod. |
| CDC-06201 | RWB-P3-E1055-APP | GAP-2096 |  | Add EV-15 NoticeDelivered as a rwb-comms producer row in the event catalogue (slide 42) and record the P1 proof read on the ACE batch business date in the job map. |
| CDC-06281 | RWB-P3-E1067-APP | GAP-1056 | 16 | Name the actor extension attribute on rwb.document.events.v1 alongside the standard attributes. |
| CDC-06299 | RWB-P3-E1073-APP | GAP-0383 | 1 | Assign one package code and version label each to rwb-comms and rwb-integration; add GET /rule-models/{packageCode}/{versionLabel} to the Ownership Map and API Specification under P7 with checksum; publish the refused load in the rwb-decision message catalogue keeping MSG-P3-027. |
| CDC-06330 | RWB-P3-E1073-CON | GAP-1216 | n/a | Publish one row per package with its owning service, version labels and target queues, including the rwb-comms assignment, before the wave-1 build. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06192 | RWB-P3-E1055-APP | CG-ALL-3861 | 12.4 | Add rwb-case as a consumer of rwb.case.CaseStateChanged.v1 in the catalog and in its ACL. |
| CDC-06307 | RWB-P3-E1073-APP | GAP-2459 | 12 | Name rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1 keyed by package code, carrying package code, version label, in-force time and SHA-256; map it to EV-08, EV-09 or EV-30. |
| CDC-06334 | RWB-P3-E1073-CON | GAP-2459 | n/a | Name the announcement rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1, keyed by package code, and map it to the free identifier of EV-08, EV-09 or EV-30. |
| CDC-06364 | RWB-P3-E1073-INF | GAP-2459 | n/a | Name rwb.decision.RulePackageInForce.v1 on rwb.decision.events.v1 keyed by package code, with package code, version label, in-force time and SHA-256; map to EV-08, EV-09 and EV-30. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06230 | RWB-P3-E1065-APP | DOR-RWB-P3-E1065-APP-14 | header | Record the signed epic design sign-off for this story. |
| CDC-06254 | RWB-P3-E1066-APP | DOR-RWB-P3-E1066-APP-14 | Header | Record the signed epic design sign-off for EP01 in the epic design record. |
| CDC-06290 | RWB-P3-E1073-APP | DOR-RWB-P3-E1073-APP-14 | header | Record the signed epic design sign-off for EP01 so the story can cite it. |
| CDC-06324 | RWB-P3-E1073-CON | DOR-RWB-P3-E1073-CON-14 | find it | Record the signed epic design sign-off in the epic design record; the story cannot hold a sign-off it does not have. |

### RWB-P1-E1067-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06272 | RWB-P3-E1067-APP | DOR-RWB-P3-E1067-APP-21 | header | Confirm the contract is published; the story already names RWB-P1-E1067-CON as its contract dependency. No RWB-P3 contract story exists in the sources. |
| CDC-06273 | RWB-P3-E1067-APP | DOR-RWB-P3-E1067-APP-22 | header | Publish the contract fake library and record its published version. |
| CDC-06278 | RWB-P3-E1067-APP | GAP-0376 | not in chunk | Adopt one consumer group across the three topics, dedupe on the CloudEvents id with the event idempotency key as business key, assign case_seq under the case lock, read ordered by occurredAt then case_seq, and keep the legacy event-to-code map. |
| CDC-06279 | RWB-P3-E1067-APP | GAP-0507 | not in chunk | Fix the intake map rows: EV-16 DocumentStored as rwb.document.DocumentStored.v1 and EV-19 TimerBreached as rwb.case.TimerBreached.v1, with each producer signing off its row. |

### RWB-P6-E1055-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06209 | RWB-P3-E1055-APP | GAP-1043 | 12 | Publish the notice read by notice ID and the dispatch reference as one operation with named fields, including the field that carries the INT-14 document reference. |
| CDC-06211 | RWB-P3-E1055-APP | GAP-1100 | 12 | Attach the WIN owner INT-14 and INT-15 specifications as versioned annexes to the contract baseline; declare the file element as a shape until then. |
| CDC-06215 | RWB-P3-E1055-APP | GAP-2243 | 12 | Confirm the JSON element names of NoticeDelivered.v1 and the notice read at contract review; rename in this story only if they differ. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06224 | RWB-P3-E1065-APP | CG-ALL-3876 | 13 | Remove the fixed enum on status so LOV-CASE-STATUS values are accepted as data without a code change. |
| CDC-06225 | RWB-P3-E1065-APP | CG-ALL-3877 | 13 | Remove the fixed enum on routeCode so LOV-ROUTE values are accepted as data without a code change. |
| CDC-06226 | RWB-P3-E1065-APP | CG-ALL-3878 | 13 | Remove the fixed enum on stageCode so LOV-STAGE values are accepted as data without a code change. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06250 | RWB-P3-E1065-APP | GAP-0899 |  | Publish the 54-role list with administration and non-human roles marked, reconcile it with the 42 rows of TSD P4 T6.1, and fix the role count the DEV seed carries. |
| CDC-06336 | RWB-P3-E1073-CON | GAP-0672 | find it | Record the eight DP H rows as wave-0 platform prerequisites; publish the model fetch in RWB-P7-E1073-CON; fix the local copy table in the rwb_integration DB story; name the login before the baseline. |
| CDC-06368 | RWB-P3-E1073-INF | GAP-0672 | header | Record the eight DP H rows (RWB-PLT-E1027, E1072, E1042, E1043, E1071, E1047, E1044, N001) as wave-0 platform prerequisites; keep the plan's H and C lists as written. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06253 | RWB-P3-E1066-APP | CG-ALL-3894 | 12.2 | Publish POST /api/recovery/source-data/v1/interactions in rwb-source-data.yaml through RWB-P1-E1066-CON, with the InteractionRequest and Interaction schemas and the 201, 409, 422 and 503 answers. |
| CDC-06255 | RWB-P3-E1066-APP | DOR-RWB-P3-E1066-APP-21 | Header | Publish the POST operation under RWB-P1-E1066-CON so the contract is published (see CG-ALL-3894). The story's CON dependency is RWB-P1-E1066-CON. |
| CDC-06257 | RWB-P3-E1066-APP | DOR-RWB-P3-E1066-APP-8 | 12.2 | Publish POST /api/recovery/source-data/v1/interactions in rwb-source-data.yaml through RWB-P1-E1066-CON. |

### API:(service not named) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06266 | RWB-P3-E1066-APP | GAP-2256 | 12 | Retire API-P3-014 (GET /api/recovery/v1/cases/{caseId}/interactions) and API-P3-015 (POST /api/recovery/v1/cases/{caseId}/interactions). Keep the two ledger operations in the rwb-source-data document. |
| CDC-06268 | RWB-P3-E1066-APP | GAP-2072 | header | Correct the module specifications so the interaction table and the two interaction endpoints sit with rwb_source_data (P1), with rwb-case reading through the P1 contract. Clear x-module P3 on the interaction paths. |
| CDC-06284 | RWB-P3-E1067-APP | GAP-2072 |  | Correct the module specifications so the interaction ledger and its writer stay with P1 rwb-source-data, with rwb-case reading through the P1 contract. |

### RWB-P3-E1073-INF (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06302 | RWB-P3-E1073-APP | GAP-0701 | 12 | Record heap request, heap limit and KieBase cache bound (20 package versions) per environment as reviewed values, backed by a load test; keep the evaluated copy in memory only; confirm with the platform owner before wave 1. |
| CDC-06316 | RWB-P3-E1073-APP | GAP-0702 |  | Record readiness gate, probe timings, ports, certificate subject and image-scan window as reviewed values per environment in deployment files; confirm with platform and security owners at SIT; keep them out of code and chart constants. |
| CDC-06343 | RWB-P3-E1073-CON | GAP-0702 | Not specified in the source documents (GAP-0702) | Record readiness gate, probe timings, ports, certificate subject and image-scan window as reviewed values per environment; confirm with platform and security owners at SIT; keep them out of code and chart constants. |

### RWB-P6-E1073-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06303 | RWB-P3-E1073-APP | GAP-1216 | 12 | Publish the package-to-service map of the rule programme before the wave-1 build, one row per package with its owning service, version labels and target queues; rwb-comms package assignment to be recorded there. |
| CDC-06304 | RWB-P3-E1073-APP | GAP-1217 | 12 | Publish the model fetch in the rwb-decision API document and the wave-1 contract story: GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}, DRL, SHA-256, version state, valid-from date, 404 and 409 cases, 2 s budget. |
| CDC-06308 | RWB-P3-E1073-APP | GAP-1214 | 12 | Fix the local copy table name and columns, the two parameter rows and their read path, the two added check codes with message text, the scenario-set shape, and the 300 ms measurement point. |

### OTHER:ADR-017 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06313 | RWB-P3-E1073-APP | GAP-1620 |  | Record XLS decision table and DMN 1.6 model as two package formats on one Drools runtime; a version names its format; conversion is a version change with its own test evidence. |
| CDC-06340 | RWB-P3-E1073-CON | GAP-1620 | find it | Record that the registry accepts an XLS decision table and a DMN 1.6 model as two package formats on one runtime, with the format named on each package version. |
| CDC-06371 | RWB-P3-E1073-INF | GAP-1620 | find it | Record that the registry accepts XLS decision tables and DMN 1.6 models as two package formats on one runtime, with a version naming its format. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06314 | RWB-P3-E1073-APP | GAP-0118 |  | Amend T1 so the workflow runs on the owning service task queue; amend T2 so each scheduled job becomes a Temporal Schedule or event-started workflow in the owning service, with JOB-05 behind TimerScheduler until Epic 3. |
| CDC-06341 | RWB-P3-E1073-CON | GAP-0118 | find it | Confirm amended D-RCV-36 T1 and T2: the workflow runs on the owning service task queue; each scheduled job is a Temporal Schedule or event-started workflow; JOB-05 stays behind TimerScheduler until Epic 3. |
| CDC-06372 | RWB-P3-E1073-INF | GAP-0118 | find it | Confirm the amended D-RCV-36 T1 and T2: the workflow runs on the owning service's task queue; each scheduled job becomes a Temporal Schedule or event-started workflow there, with JOB-05 behind the TimerScheduler port until Epic 3. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06317 | RWB-P3-E1073-APP | GAP-1219 |  | Update row 30 of RulePackageInForce to name every service that evaluates a package, including rwb-comms, or publish the package-to-service map; until then consume the event in rwb-comms on the slide 20 rule. |
| CDC-06344 | RWB-P3-E1073-CON | GAP-1219 | Not specified in the source documents (GAP-1219) | Name rwb-comms in the RulePackageInForce consumers of row 30, or publish the package-to-service map. Until then consume the event in rwb-comms on the slide 20 rule. |
| CDC-06375 | RWB-P3-E1073-INF | GAP-1219 | find it | Name every service that evaluates a package, rwb-comms included, in row 30, or publish the package-to-service map that completes it. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06321 | RWB-P3-E1073-APP | GAP-2460 |  | Register rules.testcases.min with value 50, marked assumed, owner P3 parameter owner; confirm with RW-COE at the first package load; the guard reads the parameter and no value is written in code. |
| CDC-06346 | RWB-P3-E1073-CON | GAP-2460 | Not specified in the source documents (GAP-2460) | Add rules.testcases.min with value 50 (assumed in source) and confirm with RW-COE at first package load; the guard reads the parameter, no value in code. |
| CDC-06379 | RWB-P3-E1073-INF | GAP-2460 | 8 | Register rules.testcases.min with value 50 (assumed) under the P3 parameter owner; confirm with RW-COE at first package load. Guard reads the parameter, no value in code. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06322 | RWB-P3-E1073-APP | GAP-2461 | 12 | Record that the five rule-package operations and the package list move from access module recovery.accessadmin.rulepackages to rwb-decision (P7) per the Ownership Map; rights stay rows of the rwb-access role model. |
| CDC-06347 | RWB-P3-E1073-CON | GAP-2461 | find it | Record that the five legacy operations, their authority checks and the package list move from access module package recovery.accessadmin.rulepackages to P7 rwb-decision as the Ownership Map has them; rights stay rows of the rwb-access role model. |
| CDC-06380 | RWB-P3-E1073-INF | GAP-2461 | none | Record the move of the five rule-package operations and their authority checks from the access module (recovery.accessadmin.rulepackages) to rwb-decision, as the Ownership Map has them. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06193 | RWB-P3-E1055-APP | CG-ALL-3863 | 12.5 | Add activity WriteNoticeTimer on task queue rwb-case to the Activities sheet. |
| CDC-06194 | RWB-P3-E1055-APP | CG-ALL-3864 | 12.5 | Add activity CalculateDueDate, reused from RWB-P3-E1045-APP, on task queue rwb-case to the Activities sheet. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06197 | RWB-P3-E1055-APP | DOR-RWB-P3-E1055-APP-12 | 16, 18 | Add story test cases TC-E1-055-13 to TC-E1-055-21 with their Given, When and Then, and align the RTM v7 test lists of REQ-OCC-003, REQ-ILG-004 and REQ-DRI-006 with the section 18 lists |
| CDC-06353 | RWB-P3-E1073-INF | DOR-RWB-P3-E1073-INF-12 | 16, 18 | Add TC-P3-E1073-INF-01 to -06 to Test Cases v8; align the section 18 test lists with RTM v7. |

### RWB-P6-E1055-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06204 | RWB-P3-E1055-APP | GAP-0580 | 5, 7 | Count each repeat of a proof-of-delivery read as one increment of data_product_load.duplicate_count on the DP07 stamp of the business date (DF-OPS-009); write no interaction-ledger row and no log-only hit for the repeat |
| CDC-06216 | RWB-P3-E1055-APP | GAP-1098 |  | Record that the declared area and right are enforced at gateway-bff on the screen path; add RWB-P4-E1037-CON as a C dependency or state that service identity calls carry no user right. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06223 | RWB-P3-E1055-APP | GAP-2246 | find it | Allocate the Data Dictionary field ID for the nullable notice reference column on the timer table and add it to the ownership map at the next revision. |
| CDC-06342 | RWB-P3-E1073-CON | GAP-0205 | Not specified in the source documents (GAP-0205) | Map entity 'Rule' to rule_row in the ownership basis (owner P7); add rule_package and rule_package_version as P7 entities in the next LDM version. Rename no v6 row. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06260 | RWB-P3-E1066-APP | DOR-RWB-P3-E1066-APP-6 | 10 | Add role SY-DATALOAD (data load, Case record C scope, used for load actions in section 10 of RWB-P3-E1066-APP). |
| CDC-06352 | RWB-P3-E1073-INF | DOR-RWB-P3-E1073-INF-1 | 1 | Add an infrastructure engineer role, or confirm the role name section 1 uses. |

### OTHER:Functional Specification P7 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06262 | RWB-P3-E1066-APP | GAP-1612 | 18 | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; rwb-source-data owns the one ledger. |
| CDC-06277 | RWB-P3-E1067-APP | GAP-1612 | 18 | Re-issue without FEAT-ILG-01 to FEAT-ILG-10 and A2.26 to A2.35; keep REQ-ILG-001 to REQ-ILG-014 traced to CAP-P1-012; confirm rwb-source-data owns the ledger at wave 1 contract review. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06269 | RWB-P3-E1066-APP | GAP-0267 | 12 | Set the Owner column on the 29 interaction fields to P1 rwb-source-data, matching the Ownership Map Tables row for interaction. P3 rwb-case reads the ledger through the P1 contract for the case timeline. |
| CDC-06327 | RWB-P3-E1073-CON | GAP-0383 | n/a | At wave-1 contract review, assign one package code and version label each to rwb-comms and rwb-integration; add GET /rule-models/{packageCode}/{versionLabel} under P7 rwb-decision; keep MSG-P3-027 and its check values. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06287 | RWB-P3-E1073-APP | CG-ALL-3910 | 13 | Create RWB-P7-E1073-CON or name the existing story that provides the rwb-decision rule contract; then align DP-04 and the dependency row in the header. |
| CDC-06291 | RWB-P3-E1073-APP | DOR-RWB-P3-E1073-APP-17 | header | Complete build of RWB-P3-E1073-INF; RWB-P7-E1073-CON gap is tracked under CG-ALL-3910. |

### OTHER:Template and Rules v1 section R5.5 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06311 | RWB-P3-E1073-APP | GAP-1328 |  | State that platform H rows and self-referential C rows are held by the platform and contract stories and are not repeated on the APP line. |
| CDC-06337 | RWB-P3-E1073-CON | GAP-1328 | find it | Complete the plan metadata rows from the DP table, or state in R5.5 that pattern-added platform H rows and self-referential C rows are held by the platform and contract stories. |

### RWB-P7-E1073-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06361 | RWB-P3-E1073-INF | GAP-1217 | n/a | Specify GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}: DRL, SHA-256, version state, valid-from date, 404 and 409 responses, 2 s budget. |
| CDC-06362 | RWB-P3-E1073-INF | GAP-1327 | n/a | Publish registry resources with physical columns, the model answer, dry-run count shape, workbook container and object name, version-list panel ID, service login and the two parameter codes. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06185 | RWB-P3-E1055-APP | CG-ALL-3858 | 12.2 | Publish POST /api/recovery/access/v1/authorise, as consumed by RWB-P3-E1055-APP section 12.2, through the rwb-access provider's CON story. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06188 | RWB-P3-E1055-APP | DOR-RWB-P3-E1055-APP-5 | 9 | Confirm NOTICE_PERIOD_DAYS is not a member of the closed lists LOV-SEND-STATUS, LOV-TIMER or LOV-TIMER-STATUS; it is a parameter-catalog key read by this story. |

### OTHER:rwb-access API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06190 | RWB-P3-E1055-APP | DOR-RWB-P3-E1055-APP-8 | 12.1 | Publish POST /api/recovery/access/v1/authorise in the rwb-access API yaml, or remove the path from the story. The path is not in the chunk. |

### OTHER:rwb-integration INT-14 WIN interface definition (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06191 | RWB-P3-E1055-APP | GAP-1602 | find it | Publish a versioned file layout for INT-14 WIN daily dispatch (record set, fields and order, envelope, naming, encoding, barcode and sent-date return) as a contract item before wave 2. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06195 | RWB-P3-E1055-APP | CG-ALL-3866 | 14 | Add a new message ID for 'No session on a read' ('Your session has ended. Sign in again.') in section 4; story MSG-P4-001 then cites that ID. |

### OTHER:Check-code register (REC codes); OTHER:RWB-E1-055 (legacy story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06198 | RWB-P3-E1055-APP | GAP-1169 | find it | Keep REC-05 for the business-key orphan check; give the notice barcode break its own code in RWB-E1-055 and RWB-E1-011 section 19; correct RWB-E1-055 step 11 and BR5. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P6 v2 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06200 | RWB-P3-E1055-APP | GAP-2090 |  | Hold barcode, callback date and delivery status as columns on the notice row; add no separate proof table unless a DB story needs it. |

### OTHER:TSD P1 v3; OTHER:FSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06202 | RWB-P3-E1055-APP | GAP-0579 |  | Define the pre-deployment answer: 200 with no row, the ten fields marked not available with reason SECTION_B_NOT_DEPLOYED, DP07 STALE and MSG-P1-001, behind flag rwb.dataengine.pod-read. |

### RWB-P1-E1055-APP; RWB-P1-E1066-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06203 | RWB-P3-E1055-APP | GAP-0578 | 1, 11, 19 | Give the delivery entry to rwb-source-data: its ledger writer records it inside the same transaction as the pod read, against the caseId the caller names on the read; rwb-comms writes only the dispatch entry through POST /api/recovery/source-data/v1/cases/{caseId}/interactions; a read without caseId writes nothing |

### RWB-P5-E1054-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06206 | RWB-P3-E1055-APP | GAP-1099 |  | Name the document read and claim-check handle for the stored letter of a notice; until then use GET /api/recovery/document/v1/documents/{documentId}, 2 s budget, missing letter held. |

### RWB-P6-E1055-APP; RWB-P1-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06207 | RWB-P3-E1055-APP | GAP-0366 | 1, 12.6 | Run JOB-10 as the Airflow file window plus the P6 NoticeDispatchWorkflow, let rwb-integration deliver the INT-14 file and return the acknowledgment, read the pod rows and freshness through rwb-source-data, write the letter interaction through rwb-source-data's ledger writer and prove the P3 timer from NoticeDelivered, keeping every legacy value, barcode, date and message |

### OTHER:FSD P5 document type table (AC-ALT-P5-003-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06210 | RWB-P3-E1055-APP | GAP-1044 |  | Add a proof-of-delivery receipt type, or name the stored type with its retention class and write-once flag; confirm DEMAND maps to DEMAND_LETTER at the next type table version. |

### RWB-P6-E1055-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06213 | RWB-P3-E1055-APP | GAP-1102 |  | Record host, port, zone, certificate subject and owner, container names, retention and sizes as reviewed values per environment; confirm with the WIN owner and Security before SIT cutover. |

### RWB-P6-E1055-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06214 | RWB-P3-E1055-APP | GAP-1103 |  | Fix the deployment slot and namespace under DL35, name the Schedule, record the Airflow window call in the runbook, and assert both in the registration step. |

### OTHER:FSD P1 v3 (A2.1; OTHER:A2.2; OTHER:OQ-P1-07) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06218 | RWB-P3-E1055-APP | GAP-0581 | find it | Correct the MSG-P1-001 wording and the product value under OQ-P1-07 to the FSD wording and the catalogue product name DP07 with the last complete business date. Story sections 7 and 14 are not in this chunk and are not edited here. |

### OTHER:TSD P5 v3 T3.1 (document_field and receipt field_definitions) and FSD P5 A2 proof of delivery (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06219 | RWB-P3-E1055-APP | GAP-1045 | find it | Name the four receipt fields (barcode, callback date, delivery status, sent type) in the field_definitions of the receipt type and state whether a receipt is one document per file or one per notice in FSD A2. |

### OTHER:Message catalogue of FSD P5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06220 | RWB-P3-E1055-APP | GAP-1046 | find it | Add the text of MSG-P5-016 (malware found) to the message catalogue so the 422 upload refusal shows a written message. |

### OTHER:rwb-comms values files and the runbook entries their alerts link to (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06221 | RWB-P3-E1055-APP | GAP-1104 | find it | Set the alert thresholds, windows, evaluation interval and the reviewed late-batch time, confirm them at UAT with the service owner and the platform observability owner, and record each agreed value in the runbook. |

### OTHER:TSD P6 v2 T3.1 (DF-LEG-032 hold_reason) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06222 | RWB-P3-E1055-APP | GAP-1105 | find it | Publish hold_reason as a versioned reference list with TEMPLATE_WITHDRAWN as its first row and add the other hold reasons with the business owner before the Epic 2 dispatch refinements. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06232 | RWB-P3-E1065-APP | DOR-RWB-P3-E1065-APP-8 | Header | Replace the closed enums for status, routeCode and stageCode with references to LOV-CASE-STATUS, LOV-ROUTE and LOV-STAGE. |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06234 | RWB-P3-E1065-APP | DOR-RWB-P3-E1065-APP-10 | 15 | Add the empty, loading, error and no-access states for SCR-02, SCR-03, SCR-07 and SCR-09 |

### RWB-P4-E1022-APP; 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06236 | RWB-P3-E1065-APP | GAP-0896 | 8 | Assign the DEV identity list to the platform administrator, fix the synthetic key format, record the retirement rule with DL39, and state that the identity resolves to role.entra_group rows only. |

### RWB-S8-E1065-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06237 | RWB-P3-E1065-APP | GAP-3086 | find it | Publish the deviation seed profile, case references, deviation counts per case and code, stage contract read operations and fields, R-DEV-05 and R-DEV-06 codes and owners, and the test level of the legacy cases. |

### OTHER:TSD P4 (T6.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06238 | RWB-P3-E1065-APP | GAP-0900 | find it | Extend the T6.1 matrix to the 14 capability areas of LOV-CAPABILITY and publish the matrix version with RWB-P4-AD002-APP. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06239 | RWB-P3-E1065-APP | GAP-0895 | find it | Fix the access seed file path, format and owner in rwb-access, publish its version label and row count, and state whether the DEV matrix version equals the SIT version. |

### OTHER:TSD P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06240 | RWB-P3-E1065-APP | GAP-0898 | find it | Add POST /authorise and GET /me/permissions with request and answer schemas, publish them with RWB-P4-E1037-CON, and publish the SCR-43 composite route with gateway-bff. |

### OTHER:Work Package B-P1-02 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06247 | RWB-P3-E1065-APP | GAP-2161 |  | Remove RWB-E1-064 from B-P1-02 fanout or retire B2-P1-001 for this key; add a plan-uniqueness check to checks/run_all.py. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md; OTHER:Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06252 | RWB-P3-E1065-APP | GAP-1053 |  | Record the DEV storage account and container names, the rwb-document login and the DEV read-only role; publish the gateway-bff SCR-30 and SCR-31 composite route and field masking with RWB-PLT-N001-CON. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06258 | RWB-P3-E1066-APP | CG-ALL-3893 | 11, 12.7 | Record interaction_link as a technical table of rwb_case with no BR Field ID, or add it under a dictionary name. |

### OTHER:rwb-source-data deployment chart values per environment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06270 | RWB-P3-E1066-APP | GAP-0506 | 14 | Carry the LEDGER_WRITE_FAILED alert text, threshold, window and route as named chart values per environment. Fail the release when the append-only trigger is missing. No values exist in the sources, so each must be supplied by DevOps. |

### RWB-P1-E1066-CON; RWB-P1-E1066-APP; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06271 | RWB-P3-E1066-APP | GAP-2254 | 13 | Record that event_code, actor_type, actor_ref, source_ref and case_seq are NOT NULL as the legacy migration states them, and that idempotency_key, decision_log_id and corrects_entry_id are optional. |

### OTHER:P2 story text named in the detcheck report (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06274 | RWB-P3-E1067-APP | DOR-RWB-P3-E1067-APP-11 | 15 | Set personal-data classification to none on the P2 field rows that the P3 story at L470 says carry no personal data. |

### OTHER:Recovery Workbench decision register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06275 | RWB-P3-E1067-APP | DOR-RWB-P3-E1067-APP-18 | not in chunk | Record open decision DL10 with assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 as confirmed by the directive of 26 November 2026. |

### OTHER:P2 contract document (payloads of rwb.case.CaseTransferred.v1 and rwb.case.TimerBreached.v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06276 | RWB-P3-E1067-APP | DOR-RWB-P3-E1067-APP-8 | not in chunk | Align both payloads to Kafka Catalog v1; this story's payloads follow BR7 and are not changed here. |

### OTHER:TSD P5; OTHER:T5.3 header schema (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06280 | RWB-P3-E1067-APP | GAP-1055 | not in chunk | Derive the DocumentStored idempotency key from the document row and publish it in a CloudEvents extension attribute read from configuration. |

### OTHER:API and event specification of rwb-case (platform event library) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06282 | RWB-P3-E1067-APP | GAP-2257 |  | Record ce_idempotencykey and ce_actor as extension attributes, the legacy key shape for the four events, the relay publish limit as a platform parameter, and the registry subject derived from rwb.case.events.v1; re-test envelopes at contract level. |

### OTHER:contract/ledger-intake-map-v1.yaml (rwb-source-data contract artefacts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06285 | RWB-P3-E1067-APP | GAP-0508 |  | Publish the intake map with one row per consumed event type, its version label as a document field, and the six rows of section 12.4. |

### OTHER:rwb-document event contract (AsyncAPI document and JSON Schema registry configuration for rwb.document.events.v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06286 | RWB-P3-E1067-APP | GAP-1058 |  | Name the registry subject of DocumentStored and the AsyncAPI document location from platform naming and registry convention, held in configuration. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06296 | RWB-P3-E1073-APP | GAP-2414 | not in chunk | Set build dependency H to None plus RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON; set contract C to RWB-P3-E2041-CON plus RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON. |

### OTHER:TSD P7; OTHER:TSD P3; OTHER:TSD P4; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06297 | RWB-P3-E1073-APP | GAP-1615 | not in chunk | Re-issue TSD P7 with T3.1 entries for the four rule tables and appendix T-A rule operations; remove them from TSD P3 and TSD P4; correct x-module of the nine rule paths to P7. |

### OTHER:TSD P3 v3; OTHER:TSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06298 | RWB-P3-E1073-APP | GAP-1993 | not in chunk | Remove ownership of rule_package, rule_package_version, rule_row and rule_test_case; build the registry in rwb-decision and read through the P7 contract (DP-04). |

### OTHER:Recovery Workbench TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06300 | RWB-P3-E1073-APP | GAP-0699 | 1 | Correct the ownership labels of rule_package, rule_package_version, rule_row and rule_test_case to P7 rwb-decision, consistent with ASM-A6-tables-3; keep the registry in RWB-P7-E1073-APP. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06305 | RWB-P3-E1073-APP | GAP-1327 | 12 | Publish the registry physical columns, the model answer shape, dry-run count shape, workbook container and object name, version-list panel identifier, service login and the two parameter codes. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; RWB-P7-E1073-CON; OTHER:rwb_integration DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06310 | RWB-P3-E1073-APP | GAP-0672 | 3 | Record eight DP H rows as wave-0 prerequisites; publish model fetch in RWB-P7-E1073-CON; fix local copy table; name the login before baseline. |

### OTHER:Temporal and Drools design (slide 15 version states) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06318 | RWB-P3-E1073-APP | GAP-1331 |  | State that REFUSED is a state of a stored version that failed its promotion checks, and that a load refused at a check leaves no version row and is proved by its decision log entry. |

### OTHER:Rules Engine Design v3 (section 4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06319 | RWB-P3-E1073-APP | GAP-2031 |  | Keep RulePackageEffectiveDateJob as the step name and state that it runs as JOB-20, a Temporal Schedule in rwb-decision (P7), publishing RulePackageInForce (EV-30). |

### OTHER:Rules Engine Design v3 (section 2 alert row and section 4 run book) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06320 | RWB-P3-E1073-APP | GAP-2049 |  | Version 4 keeps MSG-P3-027 unchanged, raises the alert in the service that loads the package, names P7 rwb-decision as registry owner, and keeps RWB-E1-073 as run book owner. |

### OTHER:Template and Rules v1 (section R5.5 DP-04 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06323 | RWB-P3-E1073-APP | GAP-1215 |  | Correct the DP-04 row so H and C agree with the plan Metadata rows (Depends on build None; Contract dependencies RWB-P3-E1073-CON), or update the plan at the next rules-of-record pass. |

### OTHER:Technical Specification P7 rwb-decision (with TSD P3; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06326 | RWB-P3-E1073-CON | GAP-1615 | find it | Re-issue with T3.1 entries and appendix T-A for the four rule tables and the rule-version and rule-package operations; remove them from TSD P3 and P4; set x-module P7 on the nine rule paths in API Specification v4. |

### OTHER:TSD P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06328 | RWB-P3-E1073-CON | GAP-0699 | n/a | Correct ownership labels: rule_package, rule_package_version, rule_row and rule_test_case belong to rwb-decision (P7), not P4 or P3. This story already states the registry is not held here (L162, L291). |

### OTHER:rwb-decision API document and wave-1 contract story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06331 | RWB-P3-E1073-CON | GAP-1217 | n/a | Publish GET /api/recovery/decision/v1 model fetch with packageCode and versionLabel segments, DRL, SHA-256, state, valid-from date, 404 and 409 responses under the 2 s budget. |

### OTHER:rwb-decision contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06332 | RWB-P3-E1073-CON | GAP-1327 | n/a | Publish registry resource columns, the model answer, dry-run counts, workbook container and object name, version-list panel ID, service login and the two parameter codes. |

### RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06333 | RWB-P3-E1073-CON | GAP-2458 | Header | Add a paged open-case fact read filtered by status to the rwb-case contract and its API Specification row. |

### OTHER:Temporal and Drools design (slide 15) and RWB-E1-073 legacy story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06345 | RWB-P3-E1073-CON | GAP-1331 | Not specified in the source documents (GAP-1331) | State that REFUSED is a state of a stored version that failed promotion checks and a refused load leaves no version row, proved by its decision log entry; or add a REFUSED row and define its content. |

### OTHER:Template and Rules v1 (section R5.5; OTHER:DP-04 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06348 | RWB-P3-E1073-CON | GAP-1215 | Not specified in the source documents (GAP-1215) | Correct the DP-04 row so H is RWB-PLT-E1072-CON and C is RWB-P3-E1073-CON or the plan is aligned, so both sources agree at the next rules-of-record pass. |

### API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06351 | RWB-P3-E1073-INF | GAP-1329 | find it | Fix one rule registry path family, then publish GET /rule-catalog as an owned operation or remove it from the consumed set. |

### OTHER:Technical Specification P7 (rwb-decision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06354 | RWB-P3-E1073-INF | GAP-1615 | find it | Add T3.1 entries for the four rule tables and appendix T-A rule-version and rule-package operations; remove them from TSD P3 and TSD P4; correct x-module of nine rule paths in API Specification to P7. |

### OTHER:Technical Specification P3 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06357 | RWB-P3-E1073-INF | GAP-0699 | find it | Correct the T3.1 ownership labels of rule_package, rule_package_version, rule_row and rule_test_case to P7 rwb-decision. |

### OTHER:Source documents for KieBase cache sizing; OTHER:JVM heap and local model artefact storage (GAP-0701) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06359 | RWB-P3-E1073-INF | GAP-0701 | find it | No source gives the cache sizing, heap or artefact storage, so the story cannot state them; the load-test and memory-only wording was invented and is removed. |

### OTHER:Recovery Workbench rule programme package map (solution architect) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06360 | RWB-P3-E1073-INF | GAP-1216 | n/a | Publish a package-to-service map with one row per package giving owning service, version labels and target queues, including rwb-comms; until then use synthetic ALLOCATION fixtures. |

### OTHER:rwb-decision and rwb-comms contract review; OTHER:rwb_integration DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06365 | RWB-P3-E1073-INF | GAP-1214 | n/a | Fix local copy table name and columns, the two parameter rows and read path, the two added check values with message text, scenario-set transfer shape and the 300 ms measurement point. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:RWB-E1-073) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06367 | RWB-P3-E1073-INF | GAP-3157 | n/a | Keep governance, registry and test cases in P7 rwb_decision; give owning services only the evaluated copy (DP-04); correct the recovery-schema note. |

### OTHER:Deployment configuration files per environment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06374 | RWB-P3-E1073-INF | GAP-0702 | find it | Record the readiness gate, probe timings, ports, certificate subject and image-scan window as reviewed per-environment values, confirmed at SIT, and keep them out of code and chart constants. |

### OTHER:Temporal and Drools design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06376 | RWB-P3-E1073-INF | GAP-1331 | find it | State that REFUSED is a state of a stored version that failed promotion checks, and that a load refused at a check leaves no version row and is proved by its decision log entry. |

### OTHER:Rules Engine Design v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06377 | RWB-P3-E1073-INF | GAP-2031 | find it | Keep RulePackageEffectiveDateJob as the step name and state that it runs as JOB-20, a Temporal Schedule in rwb-decision (P7), publishing RulePackageInForce (EV-30). |

### OTHER:Rules Engine Design v3 (next version v4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06378 | RWB-P3-E1073-INF | GAP-2049 | find it | Keep MSG-P3-027 unchanged, raise the alert in the loading service, name P7 rwb-decision as registry owner and keep RWB-E1-073 as run book owner. |

### OTHER:Template and Rules v1 section R5.5 (DP-04 row) or the split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-06381 | RWB-P3-E1073-INF | GAP-1215 | header | At the next rules-of-record pass, correct the DP-04 row or the plan so the H and C entries agree. Story Metadata rows kept as written. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-case.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20584 | RWB-P3-E1067-APP | R-16043 |  | Target is the P2 contract document; P2 payload text is not in this document, so no change here. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20711 | RWB-P3-E1073-INF | R-22289 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21918', 'R-22054', 'R-22286', 'R-22289', 'R-22316', 'R-28613'] |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20864 | RWB-P3-E1066-APP | R-28666 |  | LEDGER_WRITE_FAILED alert values belong to rwb-source-data chart values. None in sources, so Not specified in the source documents (GAP-0506). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0118 | The amendment of D-RCV-36 T1 and T2 has no wording in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0205 | The entity called Rule is rule_row, and the model holds neither rule_package nor rule_package_version | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0267 | The interaction ledger is defined by the case module but the Ownership Map gives it to P1 | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0366 | WIN file path, proof-of-delivery read and interaction ledger home move in the target | Tech lead | Resolved (directive) |
| GAP-0374 | The per-schema seed volumes, the seeding order across the 19 baselines and the cutover from the one recovery schema are not stated | Solution architect | Resolved (directive) |
| GAP-0375 | The cross-service ledger-write contract and its failure mapping are not defined | Solution architect | Resolved (directive) |
| GAP-0376 | The event-to-ledger map, the cross-topic ordering rule and the duplicate key after the split into per-service topics are not defined | Solution architect | Resolved (directive) |
| GAP-0383 | The rule package of rwb-comms and of rwb-integration, the rule-model fetch path and its owner, and the message family of the refusal are not stated in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0384 | The wave 1 contract-test harness, its pipeline wiring and the synthetic test data set are not specified | QA lead | Resolved (directive) |
| GAP-0501 | The sandbox scope per service and the placement of the generator module are not specified | Solution architect | Resolved (directive) |
| GAP-0502 | The contract of a build tool is not described by any source document | Tech lead | Resolved (directive) |
| GAP-0503 | The sandbox database scope and its read-only role name are not specified | ACE data architect | Resolved (directive) |
| GAP-0504 | The append path, its authorisation handling and its 404 semantics are a target choice, not a legacy value | Solution architect | Resolved (directive) |
| GAP-0505 | The exact ledger resource path, the login wording and the field-level required flags are not specified | Tech lead | Resolved (directive) |
| GAP-0506 | No deployment value, alert threshold, probe timing or incident route exists for the ledger writer | DevOps lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0507 | The mapping of the document fact and the timer fact onto the target event types is not specified | Solution architect | Resolved (directive) |
| GAP-0508 | The format and version label of the ledger intake map are not specified | Tech lead | Resolved (directive) |
| GAP-0577 | The address, the answer envelope and the paging of the proof-of-delivery read of rwb-source-data are not fixed by any source: the sources name a data-product records path, the contract of this key names another, and no source names the page parameters, the element types or the error set | Solution architect | Resolved (directive) |
| GAP-0578 | No source settles who writes the delivery entry on the interaction ledger, nor which case the entry belongs to: the legacy story writes it in rwb-comms, the contract and the app story of rwb-comms say rwb-comms calls the ledger writer, the work package of this key gives the write to rwb-source-data, and the pod row carries an account key and no case | Solution architect | Resolved (directive) |
| GAP-0579 | No source names what the proof-of-delivery read answers before RWB-ACE-001 deploys the Section B views, nor the flag that holds it: the sources require the feature to stay behind a flag and the product to show stale, and give neither the answer shape, the reason code nor the flag name | Solution architect | Resolved (directive) |
| GAP-0580 | No source says where the repeat of a proof-of-delivery read is counted when the read writes no second entry: R-UNI-40 asks for the hit to be recorded and names no counter, and the two candidate counters belong to two different mechanisms | Data architect | Resolved (directive) |
| GAP-0581 | No source fixes the render of MSG-P1-001 for the WIN proof of delivery: the legacy story names the product 'DP07 Legal', the FSD names the ACE batch and the product code, and the date is either the last complete business date or the due date | Business analyst | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0699 | The rule package registry and the workbook object are declared in the P3 module and owned by P7 | P7 rwb-decision owner with the P3 tech lead | Resolved (directive) |
| GAP-0700 | The five authoring operations and the two rule reads have no Ownership Map row and no field-level shape | P7 rwb-decision owner with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0701 | The KieBase cache sizing, the JVM heap and the storage of a local model artefact are not specified | SCB IT infrastructure with the rwb-case owner team | Resolved (directive) |
| GAP-0702 | No source gives the readiness gate, the probe timings, the ports, the certificate subject or the image-scan window | SCB IT infrastructure with the platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0895 | rwb-access sandbox seed: the access seed file's location, format, version label and row count are not specified, and whether the DEV matrix version must equal the SIT version is not stated | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0896 | rwb-access sandbox seed: the owner, the key format and the retirement rule of the DEV synthetic test identity per role are not specified | Platform administrator | Resolved (directive) |
| GAP-0897 | rwb-access sandbox seed: the per-service login name and the DEV-only read-only role over rwb_access are not fixed for the target schema | Platform DB owner | Resolved (directive) |
| GAP-0898 | rwb-access sandbox seed: the authorise and me/permissions request and answer shapes, and the screen route that shows the seeded rows, are absent from the TSD appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0899 | rwb-access sandbox seed: the legacy seed loads 54 roles, while the TSD P4 RBAC matrix tabulates 42 role rows, and the difference is not enumerated | Business analyst, P4 | Resolved (directive) |
| GAP-0900 | rwb-access sandbox seed: the matrix letters for 11 of the 14 capability areas are not tabulated, so the seed content has no source table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1043 | The rwb-comms operations and field names behind RWB-P6-E1055-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1044 | The document type of the WIN proof-of-delivery receipt and the notice-type to document-type mapping | Center of excellence analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1045 | The field names of the WIN receipt in document_field and the receipt granularity | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1046 | The text of MSG-P5-016 | Business analyst, P5 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1052 | The file-name pattern of the synthetic documents is not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1054 | The count of held intake items per exception shape and the pages each held item carries are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1055 | The exact idempotency-key format of rwb.document.DocumentStored.v1 is not stated for the target topic | Tech lead | Resolved (directive) |
| GAP-1056 | The CloudEvents attribute names that carry the actor and the occurred time on rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
| GAP-1057 | The retry limit applied to the JOB-11 outbox relay of rwb-document is not stated | Platform administrator | Resolved (directive) |
| GAP-1058 | The JSON Schema registry subject name and the AsyncAPI document location for rwb.document.events.v1 are not stated | Solution architect | Resolved (directive) |
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
| GAP-1214 | RWB-P6-E1073-APP: the local copy table and its columns, the parameter read path, the two added check names and the local run record are not specified in the source documents | Solution architect | Resolved (directive) |
| GAP-1215 | RWB-P6-E1073-APP: the DP-04 row of the pattern table names H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON while the plan gives no H and C RWB-P3-E1073-CON | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1216 | RWB-P6-E1073-APP: no source names the rule package rwb-comms is assigned, its version labels or its target queues | Solution architect | Resolved (directive) |
| GAP-1217 | RWB-P6-E1073-APP: the model fetch operation, its path segments, its request fields and its response fields are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1219 | RWB-P6-E1073-APP: Arch v5 slide 43 lists four consumers of RulePackageInForce while slide 20 says every service refreshes its cache on it, and the ITG story makes rwb-comms an evaluator | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1327 | RWB-P7-E1073-APP: the model answer, the dry-run report, the refusal of the model read, the workbook object, the version-list panel, the service login, the parameter codes and the physical registry columns are fixed by no source in the read set | Service owner of rwb-decision with the solution architect and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1329 | RWB-P7-E1073-APP: the same rule registry is named as /admin/rule-versions by API Specification v4 and the integration story and as /admin/rule-package* by the legacy story and the Ownership Map, and a third read /rule-catalog is consumed but unowned | Solution architect with the API owner and the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1330 | RWB-P7-E1073-APP: the case read that feeds the dry run is attributed to RWB-P3-E1073-CON by the plan and to RWB-P3-E1023-CON by the P3 contract story, which serves no operation | Solution architect with the rwb-case contract owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1331 | RWB-P7-E1073-APP: REFUSED is one of the six version states while a load refused at a check writes no rule_package_version row, so no stored version ever reaches it | Solution architect with the rwb-decision service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1511 | Two module specifications define the ledger tables and the ownership map leaves both here | Solution architect | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1602 | The layout of the WIN registered-mail dispatch file is not stated in any source | Solution architect with rwb-integration | Resolved (directive) |
| GAP-1608 | Proof of delivery depends on a Section B ACE view that the ACE team has not accepted | ACE team lead with the solution architect | Resolved (directive) |
| GAP-1612 | The interaction ledger is built in the P7 functional specification while the ownership ruling and DP-18 give the one ledger to rwb-source-data | Solution architect with the rwb-source-data and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1615 | The rule registry, its four tables and its version operations are claimed by three documents and owned by one service | Solution architect with the platform contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1620 | The rule model format is XLS decision tables today and DMN 1.6 in the target, with no ruling on which the registry accepts | Center of excellence analyst with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1993 | The rule package registry is claimed by P3 and P4 as well as P7 | Solution architect | Resolved (directive) |
| GAP-2030 | Delivery ownership of E1-072 and E1-073 differs between the story set and the Ownership Map | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2031 | The effective-date job is a Quartz job owned by RW-COE in version 3 and a Temporal Schedule in rwb-decision in Architecture v5 | TechX (suggested; any team may pick up this story) | Resolved (directive) |
| GAP-2049 | The rule package compile alert names P3 while the registry is P7 and the load happens in every owning service | P7 rwb-decision with the centre of excellence | Resolved (directive) |
| GAP-2072 | The interaction ledger is claimed by rwb-case and by rwb-source-data | Service owner P1 rwb-source-data with P3 rwb-case | Resolved (directive) |
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
| GAP-2254 | The ledger columns are required in the legacy migration and optional in the TSD | rwb-source-data contract owner (TechX) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2255 | The case-side link table, its states, its key and the write order are not in the sources | TechX | Resolved (directive) |
| GAP-2256 | API-P3-015 and API-P3-014 of the TSD have no rwb-case counterpart after the split | rwb-source-data contract owner and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2257 | The CloudEvents key and actor attributes, the idempotency-key format, the relay publish limit and the registry subject of the case topic are not in the sources | rwb-case contract owner and the platform event library owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2457 | The physical columns of rule_package, rule_package_version, rule_row and rule_test_case are not in any source | TechX and the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2458 | No provided operation of the case service returns the open case facts a dry run needs | P3 and P7 contract owners | Resolved (directive) |
| GAP-2459 | Which owned event announces a rule package version in force is not stated | P7 solution architect and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2460 | The value of rules.testcases.min is assumed and no parameter catalogue holds it | P3 parameter owner and the P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2461 | The legacy endpoints and their controller sit in the access module, while the Ownership Map gives them to P7 | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3086 | RWB-S8-E1065-APP: the deviation slice of the sandbox has no published case-reference source, no deviation count per case or per code, no operation or field names for the stage contract read, no codes or owner roles for R-DEV-05 and R-DEV-06, no test level for the ten legacy cases and an empty H row for eight patterns | Solution architect, with the rwb-deviation owner, the rwb-case and rwb-document owners, the rwb-source-data sandbox owner, the rule-set owner of the Deviations package, the ACE DB team lead and the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3157 | The rule tables are described as recovery-schema tables but are owned by rwb-decision | P7 rule owner | Resolved (directive) |
| GAP-3168 | The sandbox story applies three migrations where 19 schemas now need their own sequence | ACE DB lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P3-E1055-APP | skipped AC ID | 98 | missing: AC10, AC11 |
