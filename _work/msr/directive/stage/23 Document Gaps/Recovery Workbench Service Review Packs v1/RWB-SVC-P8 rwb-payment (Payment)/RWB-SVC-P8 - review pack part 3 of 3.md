# RWB-SVC-P8 rwb-payment (Payment) - review pack, part 3 of 3 (RWB-P8-E4048-CON to RWB-P8-E6036-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 5 |
| Resolved in the stories | 107 |
| Cross-document (pending in another document) | 86 |
| Not applied (value not in the sources) | 5 |
| Open business decisions | 5 |
| Register gaps linked | 25 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P8-E4048-CON | 25 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4048 CON Run the deed in lieu rental auto-debit - contract v2.md |
| RWB-P8-E4049-APP | 22 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4049 APP Apply proceeds to the case balance v2.md |
| RWB-P8-E4049-CON | 12 | 22 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4049 CON Apply proceeds to the case balance - contract v2.md |
| RWB-P8-E4050-APP | 28 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E4050 APP Reconcile money movements daily v2.md |
| RWB-P8-E6036-APP | 20 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P8 rwb-payment (Payment)/RWB P8 E6036 APP Produce provision inputs v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P8-E4050-APP | R-11518 | CG-ALL-7786 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E4050-ITG, RWB-P8-E4050-APP | R-22796 | GAP-2561 | Register gap | P1 rwb-source-data owner with the P8 owner, the solution architect and the data product owner | The reconciliation_result owner and read, the rule set behind REC-04 and REC-05, the ACE product code and the local outcome record are not specified | Keep reconciliation_result, its rec_code, its business date and the reconciliation workflow with P1 as the map records them; have this service compute and record the payment side, read the owner's result through its contract and write no row outside rwb_payment; pin the product code and the two unnamed read operations in the contract registry at the wave 3 entry check. |
| RWB-P8-E6036-APP | R-23161 | GAP-2565 | Register gap | P8 solution architect and the finance-feed interface owner | No table, file, interface or acknowledgement is published for the provision input or for the finance provision feed | Publish the finance provision feed as a numbered interface with its file layout, transport, recipient, retry policy and acknowledgement, and decide whether the built input is held in rwb_payment or handed straight to the feed; until then the input set stays the answer of the build step. |
| RWB-ITG-E4050-ITG, RWB-P8-E4050-APP | R-28900 | GAP-1490 | Register gap | Data steward and data product owner | The daily case list reconciliation has no variance tolerance | Report the variance by data product with no tolerance until DL25 is decided, and apply the agreed tolerance by version once it is set. |
| RWB-P8-E6036-APP | R-37718 | ASM-4231 | Register assumption |  | The built provision-input set is the answer of the build step: no table, no column and no event is created for it, and it is neither staged in rwb_payment nor delivered to Finance by this story; the finance provision feed, its file layout, its interface number, its transport, its retry policy and its acknowledgement stay out of scope until an interface is published, while the month-end close window of R-WO-26 is read as a policy timer of the write-off route and not as a Schedule of this service. | P8 solution architect and the finance-feed interface owner at the interface review |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P8-E4049-APP | R-18386 | DOR-RWB-P8-E4049-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 text not in chunk, so no anchor for new AC or TC rows. No source gives a BR ID for VR-P8-010-1 or BR-P8-010 (grep found none). |
| RWB-P8-E4049-CON | R-11506 | CG-ALL-7764 | find it | Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5 | Lines 64 and 253 are not in the supplied story text. No dictionary name is confirmed; nearest names are not a confirmed mapping. Owning document not confirmed. No edit. |
| RWB-P8-E4049-CON | R-11507 | CG-ALL-7765 | find it | Name `ce_source` is not a field or entity in LDM v9 or Data Classification v5 | Lines 64, 253 and 365 are not in the supplied story text. No dictionary name is confirmed; owning document not confirmed. No edit. |
| RWB-P8-E4049-CON | R-23143 | GAP-1892 | find it | ProceedsMatched does not list rwb-litigation as a consumer, so the payment fact cannot arrive as an event | Sections 12.3, 12.4 and the section 8 note are not in the supplied story text, so None cannot be set there. No edit possible; the catalogue is not changed. |
| RWB-P8-E6036-APP | R-26543 | CG-ALL-7794 | 8, 14 | MSG-P1-001 text differs from the Error and Message Standard v4 | The standard's wording is not in the sources, so the FSD text stays until it is confirmed (DOR-RWB-P8-E6036-APP-9). |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13324 | RWB-P8-E4048-CON | CG-ALL-7739 | 12.2 | Declare the REST base of /api/recovery/treatment/v1 for the rental read, as recorded in the Document Index service table. |
| CDC-13325 | RWB-P8-E4048-CON | CG-ALL-7740 | 12.2 | Declare the REST base of /api/recovery/source-data/v1 for the ACE batch receipt read, as recorded in the Document Index service table. |
| CDC-13326 | RWB-P8-E4048-CON | CG-ALL-7741 | 12.2 | Declare the REST base of /api/recovery/case/v1 for the case read, as recorded in the Document Index service table. |
| CDC-13327 | RWB-P8-E4048-CON | CG-ALL-7742 | 12.2 | Declare the REST base of /api/recovery/decision/v1 for the rule-package read, as recorded in the Document Index service table. |
| CDC-13330 | RWB-P8-E4048-CON | DOR-RWB-P8-E4048-CON-8 | 12.2 | Declare REST bases for /api/recovery/treatment/v1, /api/recovery/source-data/v1, /api/recovery/case/v1 and /api/recovery/decision/v1 (items CG-ALL-7739 to CG-ALL-7742). |
| CDC-13344 | RWB-P8-E4049-APP | CG-ALL-7753 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the receipt and balance read operation. |
| CDC-13345 | RWB-P8-E4049-APP | CG-ALL-7754 | 12.2 | Declare the REST base /api/recovery/case/v1 for the case read and balance-application answer operations. |
| CDC-13346 | RWB-P8-E4049-APP | CG-ALL-7755 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rule-package read operation. |
| CDC-13362 | RWB-P8-E4049-CON | CG-ALL-7770 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the P1 rwb-source-data provider, using the base in the Document Index service table. |
| CDC-13363 | RWB-P8-E4049-CON | CG-ALL-7771 | 12.2 | Declare the REST base /api/recovery/case/v1 for the P3 rwb-case provider, using the base in the Document Index service table. |
| CDC-13364 | RWB-P8-E4049-CON | CG-ALL-7772 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the P7 rwb-decision provider, using the base in the Document Index service table. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13331 | RWB-P8-E4048-CON | Name account_payment_id is not a field or entity in LDM v9 or Data Classification v5 | 11 | Section 11 intro now states that account_payment_id (DF-FIN-004) is not an LDM v9 or DC v5 field. |
| CDC-13332 | RWB-P8-E4048-CON | CG-ALL-7738 | 12.7 | Record decision_record as an entity or field in the owning document, or name the dictionary entity it maps to. |
| CDC-13352 | RWB-P8-E4049-APP | CG-ALL-7751 |  | Record account_payment_id as an object in the owning document or confirm the dictionary name (Data role). |
| CDC-13353 | RWB-P8-E4049-APP | CG-ALL-7752 | 12.7 | Record decision_record as the PLT library table created in rwb_payment (DP-03) or confirm the dictionary name (Data role). |
| CDC-13357 | RWB-P8-E4049-APP | DOR-RWB-P8-E4049-APP-7 | 11 | Add field account_payment_id and entity decision_record, or name their existing equivalents so the story names resolve. |
| CDC-13368 | RWB-P8-E4049-CON | CG-ALL-7766 | find it | Record ce_subject as the CloudEvents 1.0 envelope attribute of the ProceedsMatched message, or add it to the dictionary under its owner; the story keeps the envelope name. |
| CDC-13370 | RWB-P8-E4049-CON | CG-ALL-7768 | find it | Record ce_specversion as the CloudEvents 1.0 envelope attribute of the message, not as a dictionary field. |
| CDC-13371 | RWB-P8-E4049-CON | CG-ALL-7769 | find it | Record ce_id as the CloudEvents 1.0 envelope attribute of the message, not as a dictionary field. |
| CDC-13376 | RWB-P8-E4049-CON | DOR-RWB-P8-E4049-CON-7 | 11 | Add ce_type, ce_source, ce_subject and account_payment_id as fields or entities, or confirm the names against the owner. |
| CDC-13394 | RWB-P8-E4050-APP | DOR-RWB-P8-E4050-APP-7 | 11 | Add decision_record as an entity (platform template object of RWB-PLT-E1027-CON, DP-03) and classify it. |
| CDC-13405 | RWB-P8-E6036-APP | DOR-RWB-P8-E6036-APP-7 | 11 | No BR Field ID added; ID cell holds a Not specified placeholder. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13337 | RWB-P8-E4048-CON | DOR-RWB-P8-E4048-CON-12 | 12.7 | Add rows for TC-P8-E4048-CON-01 to TC-P8-E4048-CON-08 under tab Story test cases with Given, When and Then |
| CDC-13342 | RWB-P8-E4048-CON | CG-ALL-7747 | 16 | Add rows for TC-P8-E4048-CON-01 to TC-P8-E4048-CON-05 with Given, When and Then copied from the criterion each covers |
| CDC-13355 | RWB-P8-E4049-APP | CG-ALL-7760 | 16 | Add TC-E4-049-01 to TC-E4-049-04 with Given, When and Then from their criteria, plus TC-E4-049-05 (QA). |
| CDC-13374 | RWB-P8-E4049-CON | DOR-RWB-P8-E4049-CON-12 | 12.7, 16 | Add rows TC-P8-E4049-CON-01 to -05 under the same IDs, and TC-P8-E4049-CON-06 for the §12.7 table boundary. |
| CDC-13378 | RWB-P8-E4049-CON | GAP-2529 | 11 | Carry the receipt and balance data set into the four legacy test case rows of the Test Cases master; add the FEAT-PAY-10 requirement row to FSD P8 Requirements served. |
| CDC-13383 | RWB-P8-E4049-CON | CG-ALL-7776 | 16 | Add rows for TC-P8-E4049-CON-01 to TC-P8-E4049-CON-05 in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-13393 | RWB-P8-E4050-APP | CG-ALL-7784 | 16 | Add rows for TC-E4-050-01 to TC-E4-050-04 with the Given, When and Then copied from the criteria they cover. |
| CDC-13404 | RWB-P8-E6036-APP | CG-ALL-7795 | 16 | Add rows TC-E6-036-01 to TC-E6-036-05 with Given, When and Then copied from the criterion each row covers in section 16. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13328 | RWB-P8-E4048-CON | CG-ALL-7743 | 12.5 | Add a Workflows row for the JOB-07 event-started run (`PaymentMatchingWorkflow` in the matching story; the name is a target design choice). |
| CDC-13347 | RWB-P8-E4049-APP | CG-ALL-7757 | 12.5 | Name the event-started workflow of JOB-07 in the Workflows sheet. It is still a placeholder there: Not specified in the source documents (GAP-0144; ASM-0225). Then RWB-P8-E4049-APP section 12.5 can use the catalogued name. |
| CDC-13372 | RWB-P8-E4049-CON | CG-ALL-7774 | 12.5 | Add the application-step activity of JOB-07 on task queue rwb-payment, using the name GAP-2530 settles; the name is Not specified in the source documents (GAP-2530; ASM-4183). |
| CDC-13395 | RWB-P8-E4050-APP | DOR-RWB-P8-E4050-APP-8 | 12 | Add activities proceedsReconciliation and the rule-in-force read. Name message IDs for HTTP 400, 401, 404 and 503, or confirm none is defined. |
| CDC-13398 | RWB-P8-E6036-APP | CG-ALL-7792 | 12.5 | Name the AceDataReady-started payment workflow row (JOB-07) with its catalogued workflow name. No source document gives the name (GAP-2563; ASM-4229). |
| CDC-13401 | RWB-P8-E6036-APP | DOR-RWB-P8-E6036-APP-8 | 12.5 | Add the provision-input build activity and name the AceDataReady-started payment workflow row. Neither name is in any source (GAP-2563; ASM-4229). |
| CDC-13403 | RWB-P8-E6036-APP | CG-ALL-7793 | 12.5 | Add an Activities row for the provision-input build step, with its activity name once known. The name is not in any source (GAP-2563; ASM-4229). |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13329 | RWB-P8-E4048-CON | DOR-RWB-P8-E4048-CON-14 | header | Record the signed epic design sign-off for RWB-P8-E4048-CON. |
| CDC-13348 | RWB-P8-E4049-APP | DOR-RWB-P8-E4049-APP-14 | Header | Record the signed epic design sign-off for RWB-P8-E4049-APP, or confirm that none exists. |
| CDC-13366 | RWB-P8-E4049-CON | DOR-RWB-P8-E4049-CON-14 | find it | Record the signed epic design sign-off for business epic EP04 and confirm it against this story. |
| CDC-13384 | RWB-P8-E4050-APP | DOR-RWB-P8-E4050-APP-14 |  | Confirm and record the signed epic design sign-off for this service epic. |
| CDC-13399 | RWB-P8-E6036-APP | DOR-RWB-P8-E6036-APP-14 | find it | Record the signed epic design sign-off for RWB-P8-E6036-APP's epic; the story cannot state it without that record. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13333 | RWB-P8-E4048-CON | CG-ALL-7744 | 12.5 | Add a catalogued activity row for the rental arm step of matchPayments, or confirm the step is covered by the matchPayments row. |
| CDC-13354 | RWB-P8-E4049-APP | CG-ALL-7758 | 12.5 | Add a row for the application step of JOB-07 once its name is set under GAP-2530, or use a catalogued activity (Solution architect). |
| CDC-13391 | RWB-P8-E4050-APP | CG-ALL-7781 |  | Add activity proceedsReconciliation on queue rwb-payment in namespace rwb-recovery, or designate a catalogued activity. |
| CDC-13392 | RWB-P8-E4050-APP | CG-ALL-7782 |  | Add the rule-in-force read activity provided by rwb-decision on queue rwb-decision, or designate a catalogued activity. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13334 | RWB-P8-E4048-CON | CG-ALL-7746 | 4, 14 | Add a new message ID for 'no payment_match_rule row in force on the business date' and keep MSG-P8-002 for the standard's meaning; the story then cites the new ID. |
| CDC-13338 | RWB-P8-E4048-CON | Definition of Ready item 9 Messages: Partial | 14 | MSG-P8-002 keeps the placeholder (GAP-2522; ASM-4179); the standard must add an ID for the payment-match meaning. MSG-P1-001 text copied from the standard. |
| CDC-13390 | RWB-P8-E4050-APP | CG-ALL-7780 | 12.1 | Placeholders 'Not specified in the source documents (CG-ALL-7780)' written for 400, 401, 404 and 503 in section 12.1. |
| CDC-13406 | RWB-P8-E6036-APP | DOR-RWB-P8-E6036-APP-9 | 14 | Align the text of MSG-P1-001 with the wording of the Error and Message Standard v4 for that message. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13335 | RWB-P8-E4048-CON | DOR-RWB-P8-E4048-CON-1 | 1 | Add the role 'tech lead of rwb-payment' as a role code or role name, or confirm the existing role that section 1 should name. |
| CDC-13356 | RWB-P8-E4049-APP | DOR-RWB-P8-E4049-APP-6 | 10 | Add role SY-DATALOAD (data load from COLLINS) with Write-off and posting right U, as named in section 10 of this story. |
| CDC-13373 | RWB-P8-E4049-CON | DOR-RWB-P8-E4049-CON-1 | 1 | Add the role 'tech lead of rwb-payment' with its role code, or confirm the existing role code that §1 should name. |
| CDC-13375 | RWB-P8-E4049-CON | DOR-RWB-P8-E4049-CON-6 | 10 | Add role SY-DATALOAD, named in section 10 Write-off and posting U row. |

### RWB-P8-E4048-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13336 | RWB-P8-E4048-CON | Definition of Ready item 10 Screens and states: Partial | 15 | Empty, error and no access states of SCR-28 marked Not specified (CG-ALL-7749); the app story must add the states. |
| CDC-13339 | RWB-P8-E4048-CON | GAP-1377 | 7 | Keep legacy criteria AC1, AC2 and TC-E4-048-01 to TC-E4-048-04 verbatim with origin tag; BA to replace placeholders with named values in a later legacy master. |

### RWB-P8-E4049-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13349 | RWB-P8-E4049-APP | DOR-RWB-P8-E4049-APP-21 | Header | Set the build status to Done once the contract is published. |
| CDC-13350 | RWB-P8-E4049-APP | DOR-RWB-P8-E4049-APP-22 | Header | Publish the contract fake library and record its version. |

### OTHER:P7 rule registry; 06 Data/Recovery Workbench Physical Schema v7; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13359 | RWB-P8-E4049-APP | GAP-2530 | 4, 8, 11 | Publish PAYMENT_MATCH application-order rule rows, state value, JOB-07 run and activity names; story placeholders replaced afterwards. |
| CDC-13379 | RWB-P8-E4049-CON | GAP-2530 | 8 | Publish the PAYMENT_MATCH application order as rule rows with package code and rule IDs; name the applied state value; name the JOB-07 run and its application activity. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13369 | RWB-P8-E4049-CON | CG-ALL-7767 | find it | Add account_payment_id as a field of proceeds in rwb_payment, or record its owning object, as the DF-FIN-001 to DF-FIN-009 identifier of the account payment fact. |
| CDC-13402 | RWB-P8-E6036-APP | CG-ALL-7790 | 11 | Record account_payment_id as a proceeds field under its dictionary name, or record the object in the owning document, per the proposed fix (Data role). |

### RWB-PLT-E1027-CON; RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13386 | RWB-P8-E4050-APP | DOR-RWB-P8-E4050-APP-21 |  | Publish the contract and bring these CON stories to Done before this story starts; this legacy key has no contract story of its own. |
| CDC-13388 | RWB-P8-E4050-APP | DOR-RWB-P8-E4050-APP-23 | header | Contract version row added as a Not specified placeholder |

### OTHER:rwb-treatment contract (S2 contract epic) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13340 | RWB-P8-E4048-CON | GAP-2523 | 12.5 | Publish the rental read with its operation name, path and fields: rental reference, treatment reference, case reference, rental amount, debit day, due date |

### RWB-P8-E4048-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13341 | RWB-P8-E4048-CON | GAP-2524 | 12.5 | Add C rows for the rwb-treatment rental read, rwb-source-data receipt read, rwb-case case answer and rwb-decision package read; name the rental match rule code in the P8 matching-rule story |

### OTHER:Delivery plan (next refresh) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13343 | RWB-P8-E4048-CON | GAP-1379 | section header | rwb-treatment is declared as a contract dependency in the story header; the delivery plan must carry it at the next refresh. The field list stays unpublished. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13351 | RWB-P8-E4049-APP | DOR-RWB-P8-E4049-APP-8 | 12.4 | Add base paths /api/recovery/source-data/v1, /api/recovery/case/v1 and /api/recovery/decision/v1 to the yaml; align the ProceedsMatched topic and its retry and dlt topics in the catalog. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; OTHER:FSD P8 v3 (Requirements served table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13358 | RWB-P8-E4049-APP | GAP-2529 | 7, 16 | Carry the receipt and balance data set on TC-E4-049-01 to 04 and add the FEAT-PAY-10 requirement row to the Requirements served table. |

### OTHER:FSD P8 v3 (Data table and A2.10.3.1); OTHER:pattern table (DP-05 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13360 | RWB-P8-E4049-APP | GAP-2531 | 4, 8, 11 | Correct the Data table and the DP-05 row so only rwb-source-data reads the recovery.v_ace_* views; drop the v_ace reads of this service. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13361 | RWB-P8-E4049-APP | GAP-2532 | 7, 11 | Publish the applied-amount element of Proceeds, MatchRequest and ProceedsPage field lists, ProceedsMatched payload, and the rwb-case balance-application operation with its answer. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13365 | RWB-P8-E4049-CON | CG-ALL-7773 | 12.5 | Add a Workflows row for the JOB-07 event-started run: started by AceDataReady, task queue rwb-payment, namespace rwb-recovery, as §12.5 describes. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13367 | RWB-P8-E4049-CON | DOR-RWB-P8-E4049-CON-8 | 12.2, 12.5 | Declare the REST bases for /api/recovery/source-data/v1, /api/recovery/case/v1 and /api/recovery/decision/v1; add the JOB-07 event-started workflow row. |

### RWB-S4-E5022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13377 | RWB-P8-E4049-CON | GAP-1891 | 10 | Add the three P8 rows to the C list once the solution architect confirms owner contracts; record in the wave 3 harness which legacy balance application maps to which P8 operation. |

### OTHER:FSD P8 v3 and DP-05 pattern table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13380 | RWB-P8-E4049-CON | GAP-2531 | 11 | Correct the Data table and the DP-05 row so only rwb-source-data reads recovery.v_ace_* views; retire the v_ace_account, v_ace_payment and v_ace_batch_status reads of this service. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13381 | RWB-P8-E4049-CON | GAP-2532 | 7 | Publish the applied-amount element of Proceeds, the MatchRequest and ProceedsPage field lists, the ProceedsMatched payload and the rwb-case balance-application operation and answer; then replace the placeholders. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; OTHER:FSD P1 precedence ruling (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13382 | RWB-P8-E4049-CON | CG-ALL-7775 | 14 | Reverted MSG-P1-001 text to the original wording |

### OTHER:Squad refinement record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13385 | RWB-P8-E4050-APP | DOR-RWB-P8-E4050-APP-16 | header | Size row changed to a Not specified placeholder |

### RWB-P8-E4043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13387 | RWB-P8-E4050-APP | DOR-RWB-P8-E4050-APP-22 |  | Publish the contract fake library and record its version; the fakes are owned in that story. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13389 | RWB-P8-E4050-APP | CG-ALL-7779 |  | Record decision_record as the platform library template object it is (DP-03), or name the dictionary entity it maps to in LDM v9. |

### OTHER:Wave 3 journey harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13396 | RWB-P8-E4050-APP | GAP-0436 | 16 | Record at the wave 3 entry check: harness environment and pipeline, seeding set, business date, ACE batch, product codes, evidence format and retention, gate name and thresholds, and the three unnamed operations. |

### OTHER:P1 rwb-source-data data-product contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13397 | RWB-P8-E4050-APP | GAP-0434 | 12 | Name the reconciliation_result read operation and result codes, the ACE product code, the JOB-04 job identifier, the REC-04 to REC-06 package and rule IDs, and the rwb-writeoff read. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13400 | RWB-P8-E6036-APP | DOR-RWB-P8-E6036-APP-22 | find it | Publish a fake library version for RWB-P8-E6036-APP's contract and record that version. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13407 | RWB-P8-E6036-APP | GAP-2562 | header | Add the requirement row for FEAT-PAY-08 so the FSD and TSD traceability tables can name it. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13408 | RWB-P8-E6036-APP | GAP-2563 | 12.5 | Publish the provision-input field list, period, frequency, package code, rule IDs (Q-005) and the run and activity names. |

### OTHER:RWB-E6-036 legacy Data table; OTHER:FSD P8 v3 A2.8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13409 | RWB-P8-E6036-APP | GAP-2564 | 4, 8 | Correct the Data table reads of v_ace_payment, v_ace_npa_asset and v_ace_batch_status in the next versions. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0434 | The reconciliation_result owner, the ACE product code, the reconciliation operation and the wave 3 harness pack are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-1377 | The acceptance criteria and test cases of RWB-E4-048 are generic placeholders that name no rental value | Business analyst | Resolved (directive) |
| GAP-1378 | No source gives the rental amount, the debit day or the arrears threshold of the deed in lieu rental | NPA and asset manager | Resolved (directive) |
| GAP-1379 | The rental terms arrive through the rwb-treatment contract, which the plan does not carry as a contract dependency, and the field list of that answer is not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1380 | The test cases of RWB-E4-048 are generic placeholders and name no contract element | QA lead | Resolved (directive) |
| GAP-1381 | No source gives a rental-specific property or a separate receipt and arrears operation, and the consumed rental-terms element has no field list | Solution architect | Resolved (directive) |
| GAP-1382 | The name of the rental collection workflow and the package code that decides the arrears threshold are not specified | Solution architect | Resolved (directive) |
| GAP-1891 | The target gives the matching, the proceeds and the balance application to rwb-payment while the legacy story gives them to S4, and the plan adds no contract dependency for them | Solution architect | Resolved (directive) |
| GAP-1892 | ProceedsMatched does not list rwb-litigation as a consumer, so the payment fact cannot arrive as an event | Solution architect | Resolved (directive) |
| GAP-1896 | The LED round result, the percentage of official value, the proceeds source code and three operation names have no field or name in any source | Solution architect | Resolved (directive) |
| GAP-2522 | The wording of MSG-P8-001 and MSG-P8-002 is not in the read sources | Business analyst, P8 | Resolved (directive) |
| GAP-2523 | The rental read of rwb-treatment has no published operation name, path or field list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2524 | Four reads are consumed as class C while the plan's contract row is None, and the rental rule code is not named | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2525 | FSD P8 A2.9 names ATS and AMIS while TSD P8 T5.1 names ALS and GL only | Solution architect | Resolved (directive) |
| GAP-2526 | The rental fields of the PaymentMissed and ProceedsMatched payloads are not published | Solution architect | Resolved (directive) |
| GAP-2527 | Two contract stories of one service declare the same base surface | Solution architect | Resolved (directive) |
| GAP-2528 | LOV-MATCH holds no value that names a rental | Business analyst, P8 | Resolved (directive) |
| GAP-2529 | The legacy criterion of RWB-E4-049 is generic, its test cases carry no data and the story master gives no requirement id | P8 business analyst and the FSD owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2530 | The application order of the proceeds is published nowhere, and the package code, the rule IDs, the applied state value and the run and activity names are not published either | P7 rule owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2531 | The legacy story reads v_ace_account and v_ace_payment in process while the target gives the ACE views to rwb-source-data alone | P1 source-data owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2532 | The applied-amount answer, the MatchRequest field list, the ProceedsMatched payload and the rwb-case balance-application operation are not published | P8 solution architect and the rwb-case contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2562 | The legacy criteria of RWB-E6-036 are generic, its test cases carry no data and the story master gives no requirement id | P8 business analyst and the FSD owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2563 | The field list, the period, the rule rows and the run and activity names of the provision-input build are published nowhere | P7 rule owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2564 | The legacy story reads v_ace_payment and v_ace_npa_asset in process, while the target gives the ACE views to rwb-source-data alone and the asset position to rwb-asset | P1 source-data owner, S5 asset owner and the P8 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
