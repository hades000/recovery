# RWB-PLT-LIB Shared libraries - review pack, part 4 of 4 (RWB-PLT-TE006-CON to RWB-PLT-TE006-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 1 |
| Resolved in the stories | 26 |
| Cross-document (pending in another document) | 92 |
| Not applied (value not in the sources) | 3 |
| Open business decisions | 5 |
| Register gaps linked | 86 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-TE006-CON | 26 | 91 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT TE006 CON Outbox and retry for outbound work - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-PLT-TE006-CON | R-11962 | CG-ALL-1445 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-TE006-ITG, RWB-PLT-N009-APP, RWB-PLT-N009-CON, RWB-PLT-TE006-APP, RWB-PLT-TE006-CON | R-22913 | GAP-1674 | Register gap | Compliance | The retention of the platform rows, of the stored idempotent answer and of the telemetry is not stated | Set the retention per platform object under DL26 and record it in the Logical Data Model next version. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23236 | GAP-3031 | Register gap | Solution architect; business lead | RWB-S7-E6020-APP: the review date has no property, field ID, column or list, the legacy timer table is not S7's, R-WO-17's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes four contracts, DP-04, DP-09 and DP-10 are absent, and no source publishes a rule, a message or a state for a date in the past or a second decision at DEFERRED | Keep the plan's H, C, I and X rows as they stand; carry the review date as an additive request property recorded in the decision record and the case move, with no column and no field ID until the business lead and rwb-case confirm them; set the review timer as a durable workflow timer and let rwb-case own the timer row; map R-WO-17's owner to the roles that hold right A for the act and to the write-off team for the return; declare the four consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-09 and DP-10 rows; leave a second decision at DEFERRED and a past review date unpublished and tracked |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S7-E6019-APP, RWB-S7-E6019-CON | R-23240 | GAP-3029 | Register gap | Solution architect; business lead | RWB-S7-E6019-APP: the reject reason and the decision code have no field, column or list, R-WO-16's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes three contracts, DP-04 and DP-09 are absent, and no published row moves a case out of RETURNED_TO_PURSUE | Keep the plan's H, C, I and X rows as they stand; record the reason and the decision code as request and record inputs with a placeholder until the business lead confirms them; map R-WO-16's owner to the four roles that hold right A in TSD S7 T6.1; declare the three consumed rows in sections 12.2 and 12.8 and record the absent DP-04 and DP-09 rows; leave the onward path of RETURNED_TO_PURSUE to the case owner and raise it in the next planning cut; keep committee_date and every other write_off column out of the reject slice |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S9-E6034-APP, RWB-S9-E6034-CON | R-23241 | GAP-3117 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S9-E6034-APP: the legacy story names two read endpoints and no operation that places the account, partner_instruction carries no rule-version or decision column, S9 owns no route set so the placement rule is only expressible as the D9 rows R-WO-29 to R-WO-32, the legacy permission table gives the Partner portal right R while the issue needs C and the FSD also-uses role has no matrix row, both screens are list states with no placement form, the plan C row is empty while the case and the rule package are consumed, DP-04 and DP-09 are absent, the EV-20 consumer set and payload are not published, and no requirement row traces to FEAT-PRM-06 | Keep the plan H, C, I and X rows as they stand; issue the placement through API-S9-002 and never through a new path; record the rule version and the picked agency on the local decision record and add no column to partner_instruction; read the placement rows from rwb-decision as data and record the absent DP-04 rows; read the case on the rwb-case contract and record the absent C rows; authorise the issue on the Partner portal right C the matrix gives and record the legacy right R and the missing also-uses row as conflicts; serve the placement from the list state of SCR-35 through the composite route and carry the form as a placeholder; publish EV-20 with IDs only and record the absent DP-09 row; let the trace rest on the legacy key and the feature row until the E6 BRD and the PRD publish a requirement |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-TE006-CON | R-22914 | GAP-0382 | 7, 12, 16 | TE006 outbox slice: the case-event mapping, the retry and dead-letter values, and the consumer list per event type | Fix edits sections 7, 12 and 16, whose text is not in this chunk. No exact old text was supplied, so nothing was edited. Re-run with those parts. |
| RWB-PLT-TE006-CON | R-22915 | GAP-1415 | 3, 4, 5, 12 | The retry schedule, the JOB-11 sender and the ownership of the exception path are unresolved for the outbox library | Retry ladder, relay and exception-path text is in sections 3, 4, 5 and 12, none of which is in this chunk. No exact old text was supplied, so nothing was edited. |
| RWB-PLT-TE006-CON | R-23293 | GAP-1401 | 12.7 | The published problem-detail schema, the error-map table source, the expiry window and the stored-response scope are not specified for the contract | Section 12.7 holds the schema, error-map source and scope lines, and is not in this chunk. No exact old text was supplied, so nothing was edited. |

## 5. Cross-document changes (pending in the target document)


### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15343 | RWB-PLT-TE006-CON | CG-ALL-1446 | header | Renumber the duplicate FR-PLT-001 row so each ID has one meaning. |
| CDC-15344 | RWB-PLT-TE006-CON | CG-ALL-1447 | header | Renumber the duplicate FR-PLT-009 row so each ID has one meaning. |
| CDC-15345 | RWB-PLT-TE006-CON | CG-ALL-1448 | header | Renumber the duplicate FR-PLT-010 row so each ID has one meaning. |
| CDC-15346 | RWB-PLT-TE006-CON | CG-ALL-1449 | header | Renumber the duplicate FR-PLT-011 row so each ID has one meaning. |
| CDC-15347 | RWB-PLT-TE006-CON | CG-ALL-1450 | header | Renumber the duplicate FR-PLT-012 row so each ID has one meaning. |
| CDC-15348 | RWB-PLT-TE006-CON | CG-ALL-1451 | header | Renumber the duplicate FR-PLT-013 row so each ID has one meaning. |
| CDC-15349 | RWB-PLT-TE006-CON | CG-ALL-1452 | header | Renumber the duplicate FR-PLT-021 row so each ID has one meaning. |
| CDC-15350 | RWB-PLT-TE006-CON | CG-ALL-1453 | header | Renumber the duplicate FR-PLT-022 row so each ID has one meaning. |
| CDC-15351 | RWB-PLT-TE006-CON | CG-ALL-1454 | header | Renumber the duplicate FR-PLT-023 row so each ID has one meaning. |
| CDC-15352 | RWB-PLT-TE006-CON | CG-ALL-1455 | header | Renumber the duplicate FR-PLT-024 row so each ID has one meaning. |
| CDC-15353 | RWB-PLT-TE006-CON | CG-ALL-1456 | header | Renumber the duplicate FR-PLT-025 (stuck-workflow scan or smoke workflow) in the next PRD version. |
| CDC-15354 | RWB-PLT-TE006-CON | CG-ALL-1457 | header | Renumber the duplicate FR-PLT-026 (mutual TLS or admin audit or break-glass decode) in the next PRD version. |
| CDC-15355 | RWB-PLT-TE006-CON | CG-ALL-1458 | header | Renumber the duplicate FR-PLT-028 (topics, retry and dead-letter) in the next PRD version. |
| CDC-15356 | RWB-PLT-TE006-CON | CG-ALL-1459 | header | Renumber the duplicate FR-PLT-029 (blob, key store and transfer resources) in the next PRD version. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15363 | RWB-PLT-TE006-CON | GAP-1206 |  | Add H RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, C RWB-P3-E1042-CON, RWB-P3-E1043-CON, and the third C row for the rwb-case read (ID not given in the item). |
| CDC-15371 | RWB-PLT-TE006-CON | GAP-2501 |  | Record the DP-added H and C rows as non-blocking platform and published contracts, built against their fakes. |
| CDC-15389 | RWB-PLT-TE006-CON | GAP-2419 | none | Record RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON and RWB-P3-E1043-CON as wave 0 contract fakes; read authorise via the platform guard; swap the agent fake for RWB-P10-TE013-CON on landing. |
| CDC-15413 | RWB-PLT-TE006-CON | GAP-1335 | none | Carry the six platform contracts and the two rwb-case contracts in the wave 2 dependency map so sequencing is visible outside the metadata table. |
| CDC-15414 | RWB-PLT-TE006-CON | GAP-1337 | none | Carry the platform contracts and the rule-package, parameters and reference-data contracts of rwb-case in the wave 2 dependency map. |
| CDC-15417 | RWB-PLT-TE006-CON | GAP-1277 | Header | Carry the six platform H dependencies, the published C dependency and the two service baselines as DP-added and baseline rows; correct the metadata rows at the next story-set version. |
| CDC-15418 | RWB-PLT-TE006-CON | GAP-1282 | Header | Carry the six platform H dependencies and the three published C dependencies as DP-added rows; correct the metadata rows at the next story-set version. |
| CDC-15419 | RWB-PLT-TE006-CON | GAP-1286 | Header | Carry the six platform H dependencies and the two rwb-case C dependencies as DP-added rows; correct the metadata rows at the next story-set version. |
| CDC-15420 | RWB-PLT-TE006-CON | GAP-1288 | Header | Carry the six platform H dependencies, the two rwb-case C dependencies, the store baseline and the rwb-access authorise contract as DP-added rows; correct the metadata rows at the next story-set version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15337 | RWB-PLT-TE006-CON | CG-ALL-1439 | 4 | Record ce_specversion as a dictionary field or object, or record it as a CloudEvents 1.0 binary-mode header attribute in the owning document. |
| CDC-15338 | RWB-PLT-TE006-CON | CG-ALL-1440 | 4, 5, 9, 12.7, 13, 16 | Record ce_id as a dictionary field or object, or record it as a CloudEvents 1.0 binary-mode header attribute in the owning document. |
| CDC-15339 | RWB-PLT-TE006-CON | CG-ALL-1441 | 4, 5, 13 | Record ce_type as a dictionary field or object, or record it as a CloudEvents 1.0 binary-mode header attribute in the owning document. |
| CDC-15340 | RWB-PLT-TE006-CON | CG-ALL-1442 | 4 | Record ce_source as a dictionary field or object, or record it as a CloudEvents 1.0 binary-mode header attribute in the owning document. |
| CDC-15341 | RWB-PLT-TE006-CON | CG-ALL-1443 | 4 | Record ce_subject as a dictionary field or object, or record it as a CloudEvents 1.0 binary-mode header attribute in the owning document. |
| CDC-15342 | RWB-PLT-TE006-CON | CG-ALL-1444 | 4 | Record ce_time as a dictionary field or object, or record it as a CloudEvents 1.0 binary-mode header attribute in the owning document. |

### RWB-PLT-TE006-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15357 | RWB-PLT-TE006-CON | DOR-RWB-PLT-TE006-CON-10 | none | Add empty, loading, error and no-access states for SCR-44. |
| CDC-15405 | RWB-PLT-TE006-CON | GAP-2843 |  | Take RWB-PLT-TE006-CON into the next plan revision as a platform dependency of the AssetTakenOn event in the APP and CON stories. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15422 | RWB-PLT-TE006-CON | GAP-2107 | Header | Describe both Kafka roles: the ACE PII topics for logging, unchanged; and the 19 business topics plus the shared rwb.decision-record.v1 ledger topic, with their own ACLs, retention and no personal data. |
| CDC-15425 | RWB-PLT-TE006-CON | GAP-2868 | Header | Declare no event for this step; name RWB-PLT-TE006-CON as an absent H row of the S5 slice; step D1 decides whether the subscribes cells and a cost or work-order event are needed. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15335 | RWB-PLT-TE006-CON | DOR-RWB-PLT-TE006-CON-14 | header | Record the signed epic design sign-off for RWB-PLT-TE006-CON; the story cannot supply it. |

### OTHER:ACE platform confirmation of Kafka hosting (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15336 | RWB-PLT-TE006-CON | GAP-0011 | header | Kafka hosting recorded as not yet confirmed; fallback recorded in header |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15358 | RWB-PLT-TE006-CON | DOR-RWB-PLT-TE006-CON-11 | 17 | Confirm the Personal data flag of the P2 fields that detcheck flagged; this story carries none, and the four contract tables are already Personal data No. |

### OTHER:Recovery Workbench PRD (holds FR-PLT-001 to FR-PLT-011) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15359 | RWB-PLT-TE006-CON | DOR-RWB-PLT-TE006-CON-2 | 18 | Resolve the two meanings of FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011 and the other duplicated FR-PLT IDs. Story Feature and BRD section values for section 18 are not in the chunk and were not added. |

### OTHER:Platform DB story of the rwb-access schema (key not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15360 | RWB-PLT-TE006-CON | GAP-0777 | 11 | Grant to login rwb_access per section R4; keep mapping in role.entra_group; read ACE group facts only through the P1 contract. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15361 | RWB-PLT-TE006-CON | GAP-2404 | 13 | Read H as None plus RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON; read C as RWB-P10-E2032-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and the P4 authorise contract. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15362 | RWB-PLT-TE006-CON | GAP-1198 | 13 | Add H RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, and C RWB-P3-E1042-CON and RWB-P3-E1043-CON; or record them in the platform release train. |

### OTHER:FSD P4 and TSD P4 (REQ-ACA-006; OTHER:NFR-042); OTHER:plan record; OTHER:permission matrix load (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15364 | RWB-PLT-TE006-CON | GAP-2333 |  | Record Reporting letters for the remaining roles in the matrix load; correct the lake-copy access rule and REQ-ACA-006 and NFR-042 to the served-read entry; add five platform H and two rwb-case C rows to the plan. |

### OTHER:P1 rwb-source-data consumer contract (Solution architect) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15365 | RWB-PLT-TE006-CON | GAP-0376 | 4 and 8 | One consumer group across CaseCreated, CaseAllocated, CaseTransferred, TimerBreached, DocumentStored and DecisionRecorded topics; accept current and previous schema version; dedupe on CloudEvents id in rwb_source_data.processed_event with idempotency key as business key; assign case_seq under the case lock; ledger orders by occurredAt then case_seq and reports unresolved cross-topic inversions. Event-to-code map stays legacy. Section 4 text not in chunk, so this slice's BR4 was not edited. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15366 | RWB-PLT-TE006-CON | GAP-1328 |  | Complete the APP metadata rows from the DP table (eight H rows, one C row of DP-06 and DP-07, DP-09 pattern) or state in R5.5 that platform H and self-referential C rows are held elsewhere. |

### RWB-PLT-E1047-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15367 | RWB-PLT-TE006-CON | GAP-2262 | 4 and 12 | Limit CaseCreated payload to caseId, caseNo, productGroup, personKey, businessDate, accountKeys, entryDate and dpdAtEntry; resume a run held at the 09:00 cut-off by durable timer; screens while held Not specified in the source documents (GAP-2262). Retry settings are fixed in this story's BR5. |

### OTHER:Day-1 allocation and lane assignment (assembler) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15368 | RWB-PLT-TE006-CON | GAP-2261 |  | Add platform CON dependencies RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON to the lane and Day-1 allocation. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15369 | RWB-PLT-TE006-CON | GAP-2470 |  | Complete the metadata rows from the DP table, or keep the plan rows and state in R5.5 that the DP rows are added by the patterns. |

### RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15370 | RWB-PLT-TE006-CON | GAP-2475 |  | State in R5.5 that platform H and self-referential C rows are held by the platform and contract stories, or complete the metadata rows from the table. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15372 | RWB-PLT-TE006-CON | GAP-1223 |  | Read the H list as None plus the platform contracts named by the DP table, and the C list as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. |

### OTHER:rwb-comms template catalogue (escalation template for MSG-P7-011) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15373 | RWB-PLT-TE006-CON | GAP-1220 |  | Add one template row with message ID MSG-P7-011, placeholders {decision} and {caseNo}, a channel from LOV-CHANNEL and status Approved; template code and channel agreed at wave 2 design review. |

### RWB-S4-E2025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15374 | RWB-PLT-TE006-CON | GAP-1898 |  | Keep the plan lists, keep Day 1 with RWB-P5-E2025-CON as the only contract dependency, add the five H rows and two C rows when published, and remove DP-09 and DP-10 from the pattern list. |

### RWB-P7-E2028-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15375 | RWB-PLT-TE006-CON | GAP-1295 |  | Read H as None plus the six platform contracts in the DP table, and C as RWB-P10-E2028-CON plus RWB-P3-E1043-CON and the published P3 case-read and P4 authorise contracts; stays Day 1. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15376 | RWB-PLT-TE006-CON | GAP-2412 |  | Publish placement fact element names on rwb.decision-record.v1, the P3 case-read, P4 authorise and reference-data shapes at wave 2 entry, MSG-P7-009 text in the message standard, and the login name and secret entry. |

### RWB-S7-E6017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15377 | RWB-PLT-TE006-CON | GAP-3025 |  | Record rwb-case, rwb-deviation and rwb-decision as class C with placeholders; track RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and a meeting-calendar element; declare no REST operation; add a routing requirement row at next revision. |

### RWB-S7-E6021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15378 | RWB-PLT-TE006-CON | GAP-3033 |  | Record four consumed rows as class C; treat DP-05 as consumed on the rwb-source-data contract; keep ALS and GL crossing with RWB-ITG-E6021-ITG; read R-WO-05 as the assertion of RWB-S7-E6015-APP; add REQ-S7-002 and REQ-S7-005 to traceability at D1. |

### RWB-S7-E6025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15379 | RWB-PLT-TE006-CON | GAP-3041 |  | Record rwb-case and rwb-decision as class C; track RWB-PLT-E1072-CON, RWB-P7-E1073-CON and RWB-PLT-TE006-CON; read the Workbench scheduler as the workflow durable timer; carry retention as versioned reference data with a placeholder under DL26; agree the placement read; carry closing amounts as entry attributes. |

### RWB-S9-E6029-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15380 | RWB-PLT-TE006-CON | GAP-3106 |  | Publish the partner onboarding write under /api/recovery/partner/v1 as one create-and-update shape; add partner_user field list with BR Field IDs; add C rows RWB-P3-E1043-CON and RWB-PLT-TE006-CON; carry partner gateway edge dependency; bind 409 to a message ID. |

### RWB-S8-E7001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15381 | RWB-PLT-TE006-CON | GAP-3051 |  | Keep the H, C, I and X rows; record rwb-document and rwb-source-data as C with fakes; adopt DeviationRaised and DeviationCleared as EV-06 and EV-07 on rwb.deviation.events.v1 using RWB-PLT-TE006-CON for publication; use the DL22 value for the X1 service level; declare the stage clock pause signal. |

### RWB-S8-E7002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15382 | RWB-PLT-TE006-CON | GAP-3053 |  | Record the four consumed rows as class C with placeholders; add the DP-09 library row RWB-PLT-TE006-CON and the DP-04 kit rows; confirm the EFS touch, owners and EV-06 and EV-07 names. |

### RWB-S8-E7003-APP; RWB-S8-E7003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15383 | RWB-PLT-TE006-CON | GAP-3055 |  | Record the four consumed rows as class C with placeholders; record RWB-PLT-TE006-CON as the outbox and inbox library dependency of the branch. |

### RWB-S8-E7004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15384 | RWB-PLT-TE006-CON | GAP-3057 |  | Record the consumed rows as class C; add RWB-PLT-E1072-CON with RWB-P7-E1073-CON, RWB-PLT-TE006-CON, and RWB-PLT-E1037-CON with RWB-P4-E1037-CON. |

### OTHER:Metadata and split plan for the X5 deviation slices (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15385 | RWB-PLT-TE006-CON | GAP-3059 |  | Carry the claim deadline, SLA and Legal route as versioned reference rows with placeholders; declare Case record U; trace both slices to FEAT-DVF-05. |

### RWB-S8-E7006-APP; RWB-S8-E7006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15386 | RWB-PLT-TE006-CON | GAP-3061 |  | Declare the four consumed rows as class C with placeholders and fakes; record the absent DP-05, DP-09, DP-14 and DP-20 rows in the registers. |

### RWB-S8-E7007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15387 | RWB-PLT-TE006-CON | GAP-3063 |  | Fix the six operation names and the claim, appraisal and return-point properties in the wave 4 review; add RWB-PLT-TE006-CON to the X7 pattern set. |

### RWB-S8-E7007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15388 | RWB-PLT-TE006-CON | GAP-3064 |  | Publish the DeviationOutcome and Deviation answer schema with required flags and the return-point property; add the six operation names and the RWB-PLT-TE006-CON row. |

### RWB-S6-E6007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15390 | RWB-PLT-TE006-CON | GAP-3004 | none | Keep H, C, I and X rows; add RWB-PLT-TE006-CON, RWB-PLT-E1047-CON and RWB-P2-E1007-CON as tracked dependencies; publish AccountsTransferred via the platform outbox (DP-09). |

### RWB-S7-E6015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15391 | RWB-PLT-TE006-CON | GAP-3021 | none | Add C rows for the seven consumed contracts; add C RWB-P10-TE013-CON (DP-20), RWB-PLT-TE006-CON (wave 0 library) and RWB-PLT-E1072-CON with RWB-P7-E1073-CON (rule kit). |

### RWB-S7-E6013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15392 | RWB-PLT-TE006-CON | GAP-3016 | none | Add C rows for the four consumed contracts; add RWB-PLT-E1072-CON with RWB-P7-E1073-CON (rule kit), RWB-PLT-TE006-CON (outbox and inbox library) and RWB-PLT-E1071-CON (Scheduled job kit). |

### RWB-S6-E5023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15393 | RWB-PLT-TE006-CON | GAP-2973 | none | Add RWB-PLT-TE006-CON to the H row as the wave 0 library for topic rwb.debtsale.events.v1 (DP-09); add RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit. |

### RWB-S6-E6011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15394 | RWB-PLT-TE006-CON | GAP-3012 | none | Add RWB-PLT-TE006-CON to the H row as the inbox library (DP-09) for event 25 ProceedsMatched; add RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit. |

### RWB-S7-E6016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15395 | RWB-PLT-TE006-CON | GAP-3023 | none | Record RWB-PLT-TE006-CON as the wave 0 library the topic needs and RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit; add a removal operation with a placeholder path. |

### RWB-S6-E5024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15396 | RWB-PLT-TE006-CON | GAP-2975 | none | Add RWB-PLT-TE006-CON as the wave 0 outbox library for topic rwb.debtsale.events.v1 (DP-09) and RWB-P10-TE013-CON as the agent contract for the estimate (DP-20). |

### RWB-S7-E6023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15397 | RWB-PLT-TE006-CON | GAP-3037 | none | Fix the posting product and its event on the rwb-source-data contract with its cross-reference; record no provided operation or Schedule; trace the step to REQ-S7-005 with a placeholder. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15398 | RWB-PLT-TE006-CON | GAP-2669 | none | Keep REQ-S2-009 as written: allocate rwb.treatment.PlanBroken.v1 with its payload and consumers; add DP-09 with H RWB-PLT-TE006-CON to both stories and add the outbox row. |

### RWB-S5-E3019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15399 | RWB-PLT-TE006-CON | GAP-2837 |  | Add the plan rows for rwb-source-data and rwb-case as class C, add DP-09 with H RWB-PLT-TE006-CON, adopt REQ-S5-001, and state that only RWB-S5-E3023-APP runs the R-DIS-06 clocks. |

### RWB-S5-E3021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15400 | RWB-PLT-TE006-CON | GAP-2847 |  | Keep H, C, I and X rows as the plan states them, declare the AuctionResult event and three REST rows as facts with Day 1 fakes, and record RWB-PLT-TE006-CON as the wave 0 library. |

### RWB-S6-E6004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15401 | RWB-PLT-TE006-CON | GAP-2988 |  | Add the five consumed rows as class C with placeholders, add DP-08 and DP-09 with H RWB-PLT-TE006-CON, fix API-S6-005 as this key's operation, and assign R-DS-18 to this key only. |

### RWB-S7-E6018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15402 | RWB-PLT-TE006-CON | GAP-3027 |  | Keep H, C, I and X rows; record five consumed rows as class C with placeholders; add DP-06 to DP-09; read delegation_limit as reference data; claim EV-24 for the approved path. |

### RWB-P4-E1038-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15403 | RWB-PLT-TE006-CON | GAP-0973 |  | Add DP-09 to the pattern list and H RWB-PLT-TE006-CON to the build dependency rows at service-baseline review. |

### OTHER:RWB-S5-E3019 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15404 | RWB-PLT-TE006-CON | GAP-1908 |  | Add DP-09 with H RWB-PLT-TE006-CON to the pattern set and declare AssetTakenOn on rwb.asset.events.v1 from the outbox. |

### OTHER:RWB-S6-E5023 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15406 | RWB-PLT-TE006-CON | GAP-1948 |  | Add DP-09 with H RWB-PLT-TE006-CON to the pattern set; declare no event at this step and no consumed event, with 12.3 and 12.4 as None. |

### OTHER:RWB-S6-E6005 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15407 | RWB-PLT-TE006-CON | GAP-2991 |  | Add DP-09 with H RWB-PLT-TE006-CON to the pattern set and publish rwb.debtsale.LotAwarded.v1 from the outbox in the award transaction. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15408 | RWB-PLT-TE006-CON | GAP-1622 | none | Add a contract version to the DecisionRecorded event, record it on decision_log_entry, and send unknown versions to the dead-letter topic. |

### RWB-P7-E1008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15409 | RWB-PLT-TE006-CON | GAP-1228 | none | Add DP09 and RWB-PLT-TE006-CON to the H row, or record that RWB-P7-E1008-DB creates the three library objects under its X row and the consumer is built against the template. |

### OTHER:Platform DB work (login naming convention) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15410 | RWB-PLT-TE006-CON | GAP-1232 | header | Publish the rwb-<short>_app login naming with an owner role, keeping the migration account separate from the runtime login. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15411 | RWB-PLT-TE006-CON | GAP-2455 | none | Confirm rwb-decision appends every DecisionRecorded fact to decision_log_entry, the producer record is the working record, the ledger entry is the record of record, and the platform contracts are wave-0 and wave-1 baseline outside H. |

### RWB-P6-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15412 | RWB-PLT-TE006-CON | GAP-1212 | none | Add the eight DP-added H and C rows to the dependency lists, or record the platform contracts and gateway route as wave-0 baseline with the P3 reads answered by contract fakes. |

### RWB-S8-E2012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15415 | RWB-PLT-TE006-CON | GAP-3091 | Header; 13 | Add the eight platform contract rows (RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) to the H list at the next plan revision. Story keeps Depends on (build) None and Ready to start Day 1. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15416 | RWB-PLT-TE006-CON | GAP-2389 | Header | Add the six platform contracts and the two rwb-case contracts to the C list at the next plan revision; keep the H list empty. |

### OTHER:TSD S8 v2 (deviation contract baseline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15421 | RWB-PLT-TE006-CON | GAP-3060 | Header | Publish the deviation contract with the primary key on id as the only index; declare the case announcement as a consumed shape with a placeholder operation name; name both vocabularies without fixing a pair; declare the two event payloads from the three fields each carries and carry the outbox as a gap; fix the statuses, causes and message-ID slots of the 400 and 409 and leave the text unnamed. |

### OTHER:TSD P2 v3 (T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15423 | RWB-PLT-TE006-CON | GAP-1992 | Header | Remove outbox_event, outbox_delivery, processed_event, idempotency_key, feature_flag and feature_flag_change from T3.1 as shared-library tables built once in RWB-PLT-TE006-CON; keep efs_ledger_outcome with P1. |

### OTHER:split_plan.json (S5 slices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15424 | RWB-PLT-TE006-CON | GAP-2953 | Header | Keep the pattern set DP03, DP05, DP13 and DP19; declare the inbox and outbox as platform capabilities and the package as loaded through the service template; add no new H row this wave; raise the platform dependency question at the next plan revision. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20804 | RWB-PLT-TE006-CON | R-22234 |  | write failed: WRITE FAILED (nothing was written): X003-F1: old text found 0 time(s), expected 1: 'the document store and the data lake copy is written to the access |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0011 | Kafka hosting not confirmed | Enterprise Architecture and ACE platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0376 | The event-to-ledger map, the cross-topic ordering rule and the duplicate key after the split into per-service topics are not defined | Solution architect | Resolved (directive) |
| GAP-0382 | TE006 outbox slice: the case-event mapping, the retry and dead-letter values, and the consumer list per event type | Solution architect | Resolved (directive) |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0777 | The rwb-access login name, the ACE group source behind a mapping row and the column set of the three library objects are not specified for the schema slice | ACE database engineer with the rwb-access service owner and the P1 data owner | Resolved (directive) |
| GAP-0973 | Publishing DoaLimitChanged needs the outbox library of DP-09, which this slice's dependency list and pattern list do not carry | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1220 | The template code, channel, notice kind, state vocabulary, retry limit, template owner and MSG-GEN-006 text of the escalation notice are not specified in any source | Solution architect | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1228 | The ledger consumes the shared topic and dedupes in an inbox while its patterns and H row carry no DP-09 | Platform event owner with the rwb-decision tech lead | Resolved (directive) |
| GAP-1232 | The rwb-decision login, the schema owner separation and the library-object column set are unspecified | ACE database administrator with the platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1401 | The published problem-detail schema, the error-map table source, the expiry window and the stored-response scope are not specified for the contract | Platform library contract owner with the message-catalogue owner | Resolved (directive) |
| GAP-1415 | The retry schedule, the JOB-11 sender and the ownership of the exception path are unresolved for the outbox library | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1416 | The library contract shape, its publication channel and the split of the retry and exception path are not specified | Platform team | Resolved (directive) |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1666 | The retry limit of an event and of a call is stated differently in the BRD and in Architecture v5 | Solution architect | Resolved (directive) |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1899 | DP-09 and DP-10 are in the pattern list but this slice produces no event, consumes no event and registers no Schedule, and DocumentFieldsExtracted is consumed by rwb-case only | Solution architect | Resolved (directive) |
| GAP-1908 | RWB-S5-E3019: the published asset event has no DP-09 row in the plan | Solution architect | Resolved (directive) |
| GAP-1948 | RWB-S6-E5023: the service owns a topic and two events while DP-09 and its outbox library are absent from the plan | Solution architect | Resolved (directive) |
| GAP-1992 | TSD P2 names platform tables and one P1 table as its own | Solution architect | Resolved (directive) |
| GAP-2107 | Kafka has two roles in the deck and only one of them is named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2262 | CaseCreated payload and the resume of a held run are not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2569 | RWB-E1-013: the Ownership Map gives rwb-reporting no event while the wave 1 harness names rwb.reporting.ReportPublished.v1 on the service topic | Solution architect | Resolved (directive) |
| GAP-2669 | REQ-S2-009 says a broken plan raises an event, and the ownership rows and the plan give this legacy key no event to raise | Solution architect with the owner of the Kafka event platform and the business analyst of module S2 | Resolved (directive) |
| GAP-2837 | RWB-S5-E3019-APP: the take-on slice has no plan row for its cross-service reads, its outbox library, its requirement id or the duplicated R-DIS-06 criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2843 | Event 22 AssetTakenOn needs the outbox library of DP-09, which the pattern set and the build row of this key do not carry | Platform library owner | Resolved (directive) |
| GAP-2847 | RWB-S5-E3021: the take-on step consumes and publishes an event and reads four owner contracts, while the plan carries no C or I row and its pattern set omits DP-09 | Solution architect | Resolved (directive) |
| GAP-2868 | The connection matrix shows subscribes cells and Temporal cells towards four services, and no source names the events, the operations or the outbox library of this step | S5 rwb-asset service owner with the platform event library owner and the solution architect | Resolved (directive) |
| GAP-2953 | The slice consumes an event and evaluates a rule package, while DP-09 and DP-04 are outside its pattern set and no platform build row is carried | S5 rwb-asset service owner with the platform event and workflow owners | Resolved (directive) |
| GAP-2973 | RWB-S6-E5023-APP: the eligibility slice has no plan row for its four consumed contracts, its outbox library, its rule kit, the 54 percent cap criterion or the two eligibility inputs | Solution architect | Resolved (directive) |
| GAP-2975 | RWB-S6-E5024-APP: the lot build and price slice has no plan row for its four consumed contracts, its agent contract, the R-DS-04 criterion split, the rules that carry no value or the outbox library | Solution architect | Resolved (directive) |
| GAP-2988 | RWB-S6-E6004-APP: the take-bids slice has no plan row for its five consumed contracts, its guard and outbox libraries, the publish-first story of API-S6-005, the bid and realised-recovery columns, the two rules it shares with sibling keys, the reporting destination of R-DS-34, its wave or its requirement id | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2991 | RWB-S6-E6005: the step publishes LotAwarded (EV-23) while DP-09 and its outbox library are absent from the plan's pattern set and H row | Solution architect | Resolved (directive) |
| GAP-3004 | RWB-S6-E6007-APP: the transfer slice has no plan row for its five consumed contracts or the buyer-file delivery, no outbox row although it publishes AccountsTransferred, no transfer operation and no column set to record the transfer | Solution architect | Resolved (directive) |
| GAP-3012 | RWB-S6-E6011-APP: the settle-and-cancel slice has no plan row for its six consumed contracts, its inbox library, its rule kit, its settlement stamp, its GL prerequisite or its EP06 wave | Solution architect | Resolved (directive) |
| GAP-3016 | RWB-S7-E6013-APP: the scan slice has no plan row for its four consumed contracts, its rule kit, its ACE read, its inbox and its schedule, and no table or list of values holds the scan | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3021 | RWB-S7-E6015-APP: the pack slice has no plan row for its seven consumed contracts, its agent, outbox and rule-kit dependencies, its pack columns, its requirement id or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3023 | RWB-S7-E6016-APP: the removal slice has no published operation, no field or list for the removal reason, no plan row for its three consumed contracts, and no requirement id | Solution architect | Resolved (directive) |
| GAP-3025 | RWB-S7-E6017-APP: the routing slice has no plan row for its five consumed contracts, its rule kit, its event library, its meeting calendar, the operation it provides or the requirement it serves | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3027 | RWB-S7-E6018-APP: the delegation table and its owner, the approver and the limit applied have no column, the credit committee outcome is claimed by no story, and the plan's C row is empty while five rows are consumed | Solution architect | Resolved (directive) |
| GAP-3033 | RWB-S7-E6021-APP: the plan holds no C or X row for the four consumed contracts of the pack-prepared step, no dependency row for DP-05, no interface for the ALS and general-ledger crossing, and no separate story for the shared pack rule R-WO-05 | Solution architect with the rwb-writeoff tech lead, the rwb-source-data, rwb-case and rwb-decision owners and the wave 4 integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3037 | RWB-S7-E6023-APP: the reconciliation step has no published operation, no posting-product operation or event name, no matching cross-reference, no plan C row for its three consumed services, no job or Schedule for its monthly trigger and no requirement row | Solution architect | Resolved (directive) |
| GAP-3041 | RWB-S7-E6025-APP: the closure slice has no plan row for its five consumed contracts, its rule kit, its event library, its scheduler marker, the retention period, the placement record or the closing amounts | Solution architect | Resolved (directive) |
| GAP-3051 | RWB-S8-E7001-APP: the X1 slice has no plan row for its two cross-service reads, no event names, no complaint service level and no published case-clock boundary, and its happy path has no acceptance criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3053 | RWB-S8-E7002-APP: the X2 slice has no plan row for its four consumed contracts, its outbox library, its EFS touch, its requirement ids, its work-management owners or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3055 | RWB-S8-E7003-APP: the X3 branch has no plan row for its four consumed contracts, its rule read, its outbox and its workflow, and no source names the claim reference, the heir notification or the escalation level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3059 | Seven values of the X5 deviation have no source: the claim deadline, the Legal handler route, the case contract and its two event families, the platform outbox, the legal counsel's right, the requirement identifier and the sign-off | Solution architect | Resolved (directive) |
| GAP-3060 | Five shapes of the deviation contract have no source: the index set, the case announcement operation name, the outcome-to-state mapping, the outbox behind the two events and the unnamed 400 and 409 message text | Solution architect | Resolved (directive) |
| GAP-3061 | RWB-S8-E7006-APP: the X6 slice has no plan row for its consumed contracts, its skip-trace sources, its events, its agent dispatch, its 30-day clock or the deviation service level | Solution architect | Resolved (directive) |
| GAP-3063 | X7 collateral-event slice: consumed operation names, claim and re-appraisal answer shapes, event library row and the legacy AC3 rule condition are not published | Solution architect, TechX rwb-deviation tech lead, owners of rwb-case, rwb-decision, rwb-guarantee, rwb-valuation and rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3064 | X7 outcome contract: element properties beyond TSD S8 T3.1 and T-A.2, six consumed operation names and the outbox library row are not published | Solution architect, TechX rwb-deviation tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3106 | RWB-S9-E6029-APP: the onboarding write has no published operation, partner_user has no field list, the terms have no linking column, and the reference-data read has no plan row | Solution architect with the rwb-partner tech lead, the rwb-case reference-data owner and the API owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3193 | The owner of the outbox admin endpoints after the split is not stated | TechX | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
